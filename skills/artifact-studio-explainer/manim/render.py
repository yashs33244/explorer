"""
Manim engine runner: storyboard.json in, narrated out/explainer.mp4 out.

    .venv/bin/python render.py STORYBOARD.json            # voice, render, mux
    .venv/bin/python render.py STORYBOARD.json --no-voice # silent, 150 wpm timing
    .venv/bin/python render.py STORYBOARD.json --stills   # last frame per scene to OUT/stills/ID.png
    options: --out DIR (default: <storyboard dir>/out), --jobs N,
             --only SCENE_ID (writes OUT/SCENE_ID.mp4, never OUT/explainer.mp4)

TTS, first that is available: daybook reel's voice module (kokoro-js under bun,
only when $DAYBOOK_REEL points at a checkout), then macOS say, then espeak-ng.
Word timing is ESTIMATED: the speech span (silence trimmed) is shared across
words by character count, with extra weight for pauses after punctuation.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = HERE / ".venv" / "bin" / "python"
DAYBOOK_REEL = Path(os.environ["DAYBOOK_REEL"]) if os.environ.get("DAYBOOK_REEL") else None
LAYOUTS = ("title", "repomap", "flow", "table", "points", "figure")
ACTIONS = ("show", "highlight", "dim", "flow")
sys.path.insert(0, str(HERE))
import figure as fig  # noqa: E402
TAIL = 0.6
LEAD = 0.12          # a reveal lands this much before its phrase is spoken
WPM = 150


class Fail(SystemExit):
    def __init__(self, msg: str):
        super().__init__(f"render.py: {msg}")


def tokens(word: str) -> list[str]:
    """Match tokens: case and apostrophes dropped, hyphens split, other punctuation ignored.

    >>> tokens("Cache's"), tokens("step-by-step,"), tokens("..."), tokens("3.5")
    (['caches'], ['step', 'by', 'step'], [], ['35'])
    """
    w = re.sub("['’]", "", word.lower())
    return re.sub(r"[^a-z0-9\s]", "", re.sub("[-‐‑–]", " ", w)).split()


def norm(word: str) -> str:
    return "".join(tokens(word))


def phrase_hits(words: list[str], phrase: str) -> list[int]:
    """Index into words of each place the phrase starts.

    >>> w = "the cache then the database, then step by step: cache's warm".split()
    >>> phrase_hits(w, "cache"), phrase_hits(w, "the database"), phrase_hits(w, "step-by-step")
    ([1], [3], [6])
    >>> phrase_hits(w, "caches warm"), phrase_hits(w, "missing")
    ([9], [])
    """
    want = [t for w in phrase.split() for t in tokens(w)]
    toks = [(i, t) for i, w in enumerate(words) for t in tokens(w)]
    flat = [t for _, t in toks]
    hits = [toks[k][0] for k in range(len(flat) - len(want) + 1) if flat[k:k + len(want)] == want]
    return sorted(set(hits))


ABBREV = {"e.g.", "i.e.", "vs.", "etc.", "dr.", "mr.", "mrs.", "ms.", "st.", "approx.", "no."}


def split_sentences(text: str) -> list[str]:
    """Sentences to voice one at a time. Abbreviations, initials and decimals do not end one.

    >>> split_sentences("Use a cache, e.g. Redis. It is 2.5x faster vs. disk! Ask Dr. Lee or J. R. R. Tolkien.")
    ['Use a cache, e.g. Redis.', 'It is 2.5x faster vs. disk!', 'Ask Dr. Lee or J. R. R. Tolkien.']
    >>> split_sentences("Tables, files, etc. stay. Done?  Yes, i.e. no.")
    ['Tables, files, etc. stay.', 'Done?', 'Yes, i.e. no.']
    """
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        bare = w.lower().strip("\"'()[]“”‘’")
        if bare[-1:] in ".!?" and bare not in ABBREV and not re.fullmatch(r"(?:[a-z]\.)+", bare):
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def validate(sb: dict) -> None:
    if not isinstance(sb, dict) or not isinstance(sb.get("scenes"), list) or not sb["scenes"]:
        raise Fail("storyboard needs a non-empty scenes list")
    seen = set()
    for i, s in enumerate(sb["scenes"]):
        if not isinstance(s, dict):
            raise Fail(f"scene #{i}: must be an object, got {type(s).__name__}")
        sid = s["id"] if isinstance(s.get("id"), str) and s["id"] else f"#{i}"
        if not re.fullmatch(r"[A-Za-z0-9_-]+", sid):
            raise Fail(f"scene {sid}: id must be letters, digits, - or _")
        if sid in seen:
            raise Fail(f"scene {sid}: duplicate id")
        seen.add(sid)
        if s.get("layout") not in LAYOUTS:
            raise Fail(f"scene {sid}: layout must be one of {LAYOUTS}")
        if not isinstance(s.get("narration"), str) or not s["narration"].strip():
            raise Fail(f"scene {sid}: narration must be a non-empty string")
        if "\u2014" in json.dumps(s, ensure_ascii=False):
            raise Fail(f"scene {sid}: contains an em dash; use a hyphen or rewrite")
        build = s.get("build", [])
        if not isinstance(build, list):
            raise Fail(f"scene {sid}: build must be a list of steps, got {type(build).__name__}")
        allowed = fig.FIG_ACTIONS if s["layout"] == "figure" else ACTIONS
        for b in build:
            if not isinstance(b, dict):
                raise Fail(f"scene {sid}: each build step must be an object, got {b!r}")
            at = b.get("at")
            if not isinstance(at, str) or not [t for w in at.split() for t in tokens(w)]:
                raise Fail(f"scene {sid}: build step {b} needs 'at', a phrase with at least one word")
            if b.get("action") not in allowed:
                raise Fail(f"scene {sid}: build action must be one of {allowed}, got {b.get('action')!r}")
            if b.get("action") == "all":
                continue
            if b.get("target") is None or b.get("target") == "":
                raise Fail(f"scene {sid}: build step without target: {b}")


def resolve_phrases(s: dict) -> list[tuple[int, dict]]:
    """Word index of each build step: the first hit at or after the previous step's word."""
    words = s["narration"].split()
    out, last, prev = [], 0, None
    for b in s.get("build", []):
        at = b["at"]
        hits = phrase_hits(words, at)
        if not hits:
            raise Fail(f"scene {s['id']}: phrase not found in narration: {at!r}\n  narration: {s['narration']}")
        later = [i for i in hits if i >= last]
        if not later:
            raise Fail(f"scene {s['id']}: phrase {at!r} only occurs before the previous step's phrase {prev!r}; "
                       "each 'at' must come at or after the previous step in the narration, so reorder the "
                       f"steps or pick a later phrase\n  narration: {s['narration']}")
        out.append((later[0], b))
        last, prev = later[0], at
    return out


def check_figures(scenes: list[dict], base: Path) -> list[tuple[dict, "fig.Source", list[dict]]]:
    """Figure scenes: files exist, actions, rects and steps are valid. Runs before any render."""
    out = []
    for s in scenes:
        if s["layout"] != "figure":
            continue
        steps = [{"action": b["action"], "target": b.get("target")} for b in s.get("build", [])]
        try:
            src = fig.load_source(s, base)
            fig.check_steps(s, src, steps)
        except fig.FigureError as e:
            raise Fail(str(e)) from None
        out.append((s, src, steps))
    return out


def check_layouts(scenes: list[dict], resolved: dict[str, list[tuple[int, dict]]]) -> None:
    """Other layouts: build each scene's items and schedule its steps, with the word index standing
    in for time, so a bad target id or a step before its parent fails before any voicing."""
    scenes = [s for s in scenes if s["layout"] != "figure"]
    if not scenes:
        return
    import engine  # imports manim, so only when needed
    for s in scenes:
        steps = [{"time": float(i), "action": b["action"], "target": b.get("target")} for i, b in resolved[s["id"]]]
        try:
            items, _ = engine.build(s, steps, {"visible": set()})
            engine.schedule(s, items, steps)
        except engine.StoryboardError as e:
            raise Fail(f"storyboard error: {e}") from None
        except (KeyError, TypeError, ValueError) as e:
            raise Fail(f"scene {s['id']}: {s['layout']} layout is missing or has a bad field: {e!r}") from None


# ---------- audio ----------

def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe_duration(path: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    if r.returncode != 0:
        raise Fail(f"ffprobe failed on {path}: {r.stderr.strip()}")
    return float(r.stdout.strip())


def ffq(p: Path) -> str:
    """A path quoted for an ffmpeg concat list: a ' inside single quotes is written '\\''."""
    return "'" + str(p).replace("'", "'\\''") + "'"


def has_daybook() -> bool:
    return DAYBOOK_REEL is not None and shutil.which("bun") is not None and (DAYBOOK_REEL / "src/voice.ts").exists()


def local_voice() -> str | None:
    """The local fallback voice: macOS say, else espeak-ng."""
    return next((b for b in ("say", "espeak-ng") if shutil.which(b)), None)


NO_VOICE = ("no voice found. Install espeak-ng (apt install espeak-ng, or brew install espeak-ng), "
            "use macOS say, or set DAYBOOK_REEL to a daybook reel checkout with bun for kokoro. "
            "Or render silently with --no-voice.")


def tts_daybook(text: str, voice: str) -> tuple[Path, str] | None:
    if not has_daybook():
        return None
    r = run(["bun", "run", "src/voice.ts", "--text", text, "--voice", voice], cwd=DAYBOOK_REEL, timeout=600)
    if r.returncode != 0:
        print(f"  daybook voice failed, using {local_voice()}: {r.stderr.strip()[-300:]}", file=sys.stderr)
        return None
    try:
        data = json.loads(r.stdout[r.stdout.index("{"):])
    except (ValueError, json.JSONDecodeError):
        return None
    return Path(data["wavPath"]), data.get("engine", "kokoro")


def tts_local(text: str, wav: Path) -> str:
    """Voice text with macOS say or espeak-ng into a 24 kHz mono wav; returns the engine name."""
    eng = local_voice()
    if eng is None:
        raise Fail(NO_VOICE)
    raw = wav.with_suffix(".aiff" if eng == "say" else ".raw.wav")
    r = run(["say", "-o", str(raw), text] if eng == "say" else ["espeak-ng", "-w", str(raw), text])
    if r.returncode != 0:
        raise Fail(f"{eng} failed: {r.stderr.strip()}")
    r = run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-ar", "24000", "-ac", "1", str(wav)])
    raw.unlink(missing_ok=True)
    if r.returncode != 0:
        raise Fail(f"ffmpeg could not convert {eng} output: {r.stderr}")
    return eng


GAP = 0.28   # s of silence between voiced sentences


def voice_scene(text: str, voice: str, wav: Path) -> tuple[str, list[tuple[list[str], float, float]]]:
    """Voice one sentence at a time (kokoro truncates long input), join them with short gaps,
    and return the engine plus each sentence's words with its measured speech span."""
    sents = split_sentences(text)
    parts, engine = [], 'kokoro'
    for i, sn in enumerate(sents):
        part = wav.with_name(f"{wav.stem}.{i:02d}.wav")
        got = tts_daybook(sn, voice)
        if got is not None:
            src, eng = got
            engine = eng if eng != 'kokoro' else engine
        else:
            src = part.with_suffix('.local.wav')
            engine = tts_local(sn, src)
        r = run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-ar", "24000", "-ac", "1", str(part)])
        if r.returncode != 0:
            raise Fail(f"ffmpeg could not normalise sentence audio: {r.stderr}")
        parts.append(part)
    gap = wav.with_name(f"{wav.stem}.gap.wav")
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono", "-t", str(GAP), str(gap)])
    lst = wav.with_name(f"{wav.stem}.list.txt")
    lst.write_text("".join(f"file {ffq(p)}\nfile {ffq(gap)}\n" for p in parts))
    r = run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(wav)])
    if r.returncode != 0:
        raise Fail(f"ffmpeg could not join sentence audio: {r.stderr}")
    spans, off = [], 0.0
    for sn, part in zip(sents, parts):
        d = probe_duration(part)
        a, b = speech_span(part, d)
        spans.append((sn.split(), off + a, off + b))
        off += d + GAP
    return engine, spans


def speech_span(wav: Path, dur: float) -> tuple[float, float]:
    """Leading and trailing silence trimmed, from ffmpeg silencedetect."""
    r = run(["ffmpeg", "-v", "info", "-i", str(wav), "-af", "silencedetect=noise=-40dB:d=0.12", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    a, b = 0.0, dur
    if starts and starts[0] < 0.05 and ends:
        a = ends[0]
    if starts and starts[-1] > a and (len(ends) < len(starts) or ends[-1] >= dur - 0.05):
        b = starts[-1]
    if b - a < 0.3:
        a, b = 0.0, dur
    return a, b


def word_timings(words: list[str], a: float, b: float) -> list[dict]:
    """ESTIMATED timing: char weights plus pause weight after punctuation."""
    marks, cur = [], 0.0
    for w in words:
        n = max(1, len(norm(w)) or 1)
        marks.append((cur, cur + n))
        cur += n
        cur += 5.0 if w[-1:] in ".?!" else 2.5 if w[-1:] in ",;:" else 0.6
    total = max(cur, 1e-6)
    k = (b - a) / total
    return [{"w": w, "start": round(a + s * k, 3), "end": round(a + e * k, 3)} for w, (s, e) in zip(words, marks)]


# ---------- main ----------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard")
    ap.add_argument("--no-voice", action="store_true", help="silent, timing from 150 wpm")
    ap.add_argument("--stills", action="store_true", help="last frame of each scene to OUT/stills/ID.png")
    ap.add_argument("--out", help="output folder (default: <storyboard dir>/out)")
    ap.add_argument("--jobs", type=int, default=max(1, min(4, (os.cpu_count() or 2) // 2)))
    ap.add_argument("--only", help="render just this scene id, to OUT/ID.mp4")
    args = ap.parse_args()

    if not PY.exists():
        raise Fail(f"no env at {PY}; run {HERE / 'setup.sh'} first")
    sb_path = Path(args.storyboard).resolve()
    sb = json.loads(sb_path.read_text())
    validate(sb)
    scenes = [s for s in sb["scenes"] if not args.only or s["id"] == args.only]
    if not scenes:
        raise Fail(f"no scene with id {args.only!r}")
    resolved = {s["id"]: resolve_phrases(s) for s in scenes}   # fail on a bad phrase before any work
    figures = check_figures(scenes, sb_path.parent)             # and on a bad figure file, rect or step
    check_layouts(scenes, resolved)                             # and on a bad target or step order
    out = Path(args.out).resolve() if args.out else sb_path.parent / "out"
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    voice = sb.get("meta", {}).get("voice", "af_heart")
    silent = args.no_voice or args.stills
    if not silent and not has_daybook() and local_voice() is None:
        raise Fail(NO_VOICE)
    stills = out / "stills"
    t0 = time.time()

    # 1. voice and timing
    specs, engines = [], {}
    for s in scenes:
        words = s["narration"].split()
        wav = work / f"{s['id']}.wav"
        if silent:
            dur = max(2.0, len(words) / WPM * 60)
            a, b = 0.15, dur
            engines[s["id"]] = "none"
        else:
            engines[s["id"]], spans = voice_scene(s["narration"], voice, wav)
            dur = probe_duration(wav)
        if silent:
            timing = word_timings(words, a, b)
        else:
            # time words inside each sentence's measured span, so drift never crosses a sentence
            timing = [t for ws, sa, sb_ in spans for t in word_timings(ws, sa, sb_)]
            if [t["w"] for t in timing] != words:
                raise Fail(f"{s['id']}: sentence split lost words")
        steps = [{"time": round(max(0.0, timing[i]["start"] - LEAD), 3), "action": st["action"],
                  "target": st.get("target")} for i, st in resolved[s["id"]]]
        spec = {"scene": s, "duration": round(dur + TAIL, 3), "words": timing, "steps": steps,
                "audio": None if silent else str(wav), "base": str(sb_path.parent)}
        (work / f"{s['id']}.json").write_text(json.dumps(spec, indent=1))
        specs.append(spec)
        print(f"  {s['id']}: {dur:.2f}s audio, voice {engines[s['id']]}")

    # 2. figure sources: render each svg state once (cached) before the parallel scene renders
    for s, src, steps in figures:
        if src.kind == "svg":
            import svgshot
            w = fig.svg_width(s, src, steps)
            t1 = time.time()
            try:
                svgshot.shoot(src.paths[0], w)
            except (Exception, SystemExit) as e:  # a Chrome crash mid-render ends in a message, not a traceback
                raise Fail(f"{s['id']}: could not render {src.paths[0].name} with headless Chrome: {e}")
            print(f"  {s['id']}: {src.paths[0].name} at {w}px, states ready ({time.time() - t1:.1f}s)")

    # 3. render scenes in parallel
    def render_one(spec: dict) -> Path:
        sid = spec["scene"]["id"]
        mp4 = work / f"{sid}.mp4"
        cmd = [str(PY), str(HERE / "engine.py"), str(work / f"{sid}.json"), str(mp4)]
        if args.stills:
            cmd += ["--still", str(stills / f"{sid}.png")]
        r = run(cmd)
        if r.returncode != 0:
            raise Fail(f"scene {sid} failed:\n{r.stderr.strip()[-2500:]}")
        return mp4

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(render_one, specs))
    if args.stills:
        print(f"stills in {stills} ({time.time() - t0:.1f}s)")
        return

    # 4. mux each scene with its audio padded to the video length, then concat
    parts = []
    for spec in specs:
        sid = spec["scene"]["id"]
        mp4, av = work / f"{sid}.mp4", work / f"{sid}.av.mp4"
        vdur = probe_duration(mp4)
        if spec["audio"]:
            audio_in = ["-i", spec["audio"]]
        else:
            audio_in = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        r = run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), *audio_in, "-filter:a", "apad,aresample=48000",
                 "-ac", "2", "-t", f"{vdur:.3f}", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                 "-c:a", "aac", "-b:a", "160k", str(av)])
        if r.returncode != 0:
            raise Fail(f"mux failed for {sid}: {r.stderr}")
        parts.append(av)
    lst = work / "concat.txt"
    lst.write_text("".join(f"file {ffq(p)}\n" for p in parts))
    final = out / (f"{args.only}.mp4" if args.only else "explainer.mp4")   # --only never replaces the full video
    r = run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
             "-movflags", "+faststart", str(final)])
    if r.returncode != 0:
        raise Fail(f"concat failed: {r.stderr}")
    used = sorted(set(engines.values()))
    print(f"wrote {final} ({probe_duration(final):.1f}s) in {time.time() - t0:.1f}s, voice: {', '.join(used)}")


if __name__ == "__main__":
    main()
