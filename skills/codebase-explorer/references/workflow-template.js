// Workflow template for the Explorer pipeline (research, verify, draw, critique, fix).
// Run with the Workflow tool, passing args:
//   { subject: "PostgreSQL", repo: "/abs/path/to/repo", scratch: "/abs/work/dir", skill: "/abs/path/to/skills/codebase-explorer",
//     topics: [{ key: "wal", title: "WAL and recovery", focus: "what to read and run for this topic" }] }
// The scratch dir must contain topics/ and diagrams/ (the script creates files under them via the agents).
// Workflows can spawn dozens of agents. Only run this when the user opted into orchestration.
export const meta = {
  name: 'explorer-research-and-draw',
  description: 'Research each topic from the real source, fact-check it, hand-draw three SVG diagrams, render and critique them',
  phases: [
    { title: 'Research' }, { title: 'Verify' }, { title: 'Draw' }, { title: 'Critique' }, { title: 'Fix' },
  ],
}

const { subject, repo, scratch, skill, topics } = args
const RENDER = `${skill}/scripts/render.sh`

const RESEARCH = {
  type: 'object',
  properties: {
    key: { type: 'string' }, title: { type: 'string' }, one_liner: { type: 'string' }, analogy: { type: 'string' },
    big_picture: { type: 'array', items: { type: 'string' } },
    flow: { type: 'array', items: { type: 'object', properties: { step: { type: 'string' }, detail: { type: 'string' }, where: { type: 'string' } }, required: ['step', 'detail', 'where'] } },
    diagram: { type: 'object', properties: { claim: { type: 'string' }, nodes: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, label: { type: 'string' }, group: { type: 'string' } }, required: ['id', 'label'] } }, edges: { type: 'array', items: { type: 'object', properties: { from: { type: 'string' }, to: { type: 'string' }, label: { type: 'string' } }, required: ['from', 'to', 'label'] } } }, required: ['claim', 'nodes', 'edges'] },
    key_files: { type: 'array', items: { type: 'object', properties: { path: { type: 'string' }, what: { type: 'string' } }, required: ['path', 'what'] } },
    interview: { type: 'array', items: { type: 'object', properties: { q: { type: 'string' }, answer: { type: 'array', items: { type: 'string' } }, trap: { type: 'string' } }, required: ['q', 'answer'] } },
    contributor_tips: { type: 'array', items: { type: 'string' } },
    glossary: { type: 'array', items: { type: 'object', properties: { term: { type: 'string' }, meaning: { type: 'string' } }, required: ['term', 'meaning'] } },
    try_it: { type: 'array', items: { type: 'object', properties: { cmd: { type: 'string' }, shows: { type: 'string' } }, required: ['cmd', 'shows'] } },
    file_tree: { type: 'array', items: { type: 'object', properties: { path: { type: 'string' }, what: { type: 'string' } }, required: ['path', 'what'] } },
  },
  required: ['key', 'title', 'one_liner', 'analogy', 'big_picture', 'flow', 'diagram', 'key_files', 'interview', 'contributor_tips', 'glossary'],
}
const VERIFY = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    wrong_claims: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, correction: { type: 'string' } }, required: ['claim', 'correction'] } },
    bad_paths: { type: 'array', items: { type: 'object', properties: { claimed: { type: 'string' }, fix: { type: 'string' } }, required: ['claimed', 'fix'] } },
    missing_essentials: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string', enum: ['good', 'needs_fixes'] },
  },
  required: ['key', 'wrong_claims', 'bad_paths', 'missing_essentials', 'verdict'],
}
const DRAW = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    diagrams: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, role: { type: 'string', enum: ['architecture', 'lifecycle', 'structure'] }, title: { type: 'string' }, caption: { type: 'string' }, badges: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, meaning: { type: 'string' } }, required: ['n', 'meaning'] } } }, required: ['file', 'role', 'title', 'caption'] } },
  },
  required: ['key', 'diagrams'],
}
const CRITIC = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    issues: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' }, severity: { type: 'string', enum: ['blocker', 'major', 'minor'] } }, required: ['file', 'problem', 'fix', 'severity'] } },
    verdict: { type: 'string', enum: ['pass', 'fix'] },
  },
  required: ['key', 'issues', 'verdict'],
}

const STYLE = 'Audience: a complete beginner who wants to learn this system and contribute. Plain short sentences, no unexplained jargon. Never use the em dash character. Never invent anything: every path, function, file and command must be real.'
const KIT = `Read ${skill}/references/diagram-guide.md, ${skill}/assets/icons.md and the bottom half of ${skill}/assets/style.css first. Draw hand-drawn style inline SVG using ONLY the kit classes. Every id must start with "<key>-d<N>-". Labels 1 to 5 words, text at least 12 units, every arrow labeled with a verb, numbered badges with a legend.`
const LOOP = `After writing each svg run ${RENDER} <file.svg> <file.png> light, Read the PNG, then once more with dark. Fix overlaps, clipped text, wrong arrows. Validate XML with python3 -c "import xml.dom.minidom,sys;xml.dom.minidom.parse(sys.argv[1])" <file>. Up to 3 rounds per diagram.`

const results = await pipeline(
  topics,
  (t) => agent(
    `You are a senior engineer onboarding a brand new contributor to ${subject}. Research this topic from the REAL source and, where possible, from REAL runs, then fill the schema.\nTopic: ${t.title} (key ${t.key}). Repo (read only): ${repo}.\nScope: ${t.focus}\nRules: scratch servers or files go only in ${scratch}/tmp-${t.key} and must be stopped and deleted at the end. Verify every path with ls. Give 8 to 10 interview questions, easiest first, with simple bullet answers and a common trap where useful. 7 to 12 nodes in the diagram. Also write your final JSON to ${scratch}/topics/${t.key}.json.\n${STYLE}\nSet key to "${t.key}".`,
    { label: `research:${t.key}`, phase: 'Research', schema: RESEARCH }
  ),
  (r, t) => !r ? null : agent(
    `You are a skeptical reviewer. Fact-check this research about "${t.title}" against the real repo ${repo} (read only). Check paths (ls), names (grep) and every interview answer. Report only real problems with the exact correction.\n${JSON.stringify(r)}\nSet key to "${t.key}".`,
    { label: `verify:${t.key}`, phase: 'Verify', schema: VERIFY }
  ).then((v) => ({ research: r, verify: v })),
  (p, t) => !p ? null : agent(
    `You are a senior technical illustrator. Topic "${t.title}" (key ${t.key}). Ground truth: ${scratch}/topics/${t.key}.json. Reviewer corrections you must respect: ${JSON.stringify({ wrong: p.verify.wrong_claims, paths: p.verify.bad_paths })}.\nDraw THREE diagrams into ${scratch}/diagrams/${t.key}/d1.svg, d2.svg, d3.svg: d1 architecture (components and labeled arrows in dashed blobs), d2 lifecycle (numbered scenario in time order), d3 structure (annotated anatomy of the key layout).\n${KIT.split('<key>').join(t.key)}\n${LOOP}\n${STYLE}\nReturn each diagram's file path, role, short title, one beginner sentence caption and badge legend. Also write them as an array to ${scratch}/diagrams/${t.key}/meta.json with file names relative to that folder.`,
    { label: `draw:${t.key}`, phase: 'Draw', schema: DRAW }
  ).then((d) => ({ ...p, draw: d })),
  (p, t) => !p || !p.draw ? p : agent(
    `You are a fussy art director and domain expert. Review three hand-drawn SVGs for topic ${t.key}: ${p.draw.diagrams.map((d) => d.file).join(', ')}. Ground truth: ${scratch}/topics/${t.key}.json. For each file render light and dark with ${RENDER} and Read both PNGs. Check: clipped, overlapping or tiny text (under 12 units) in either theme; arrows pointing the wrong way or unlabeled; technically wrong content; unclear for a beginner; crowded or unaligned; anything outside the viewBox; hex colors, style or script tags, ids without the "${t.key}-d" prefix. Report only real problems with a concrete fix. verdict pass only if no blocker or major issue.\nSet key to "${t.key}".`,
    { label: `critic:${t.key}`, phase: 'Critique', schema: CRITIC }
  ).then((c) => ({ ...p, critic: c })),
  (p, t) => !p || !p.critic || p.critic.verdict === 'pass' || !p.critic.issues.some((i) => i.severity !== 'minor') ? p : agent(
    `Repair the SVG diagrams for topic ${t.key} in place. Issues: ${JSON.stringify(p.critic.issues)}. Files: ${p.draw.diagrams.map((d) => d.file).join(', ')}.\n${KIT.split('<key>').join(t.key)}\n${LOOP}\nRe-render each changed file and Read the PNG. Return the same structure.`,
    { label: `fix:${t.key}`, phase: 'Fix', schema: DRAW }
  ).then((d) => ({ ...p, draw: d && d.diagrams && d.diagrams.length ? d : p.draw, fixed: true }))
)

const ok = results.filter(Boolean)
log(`${ok.length}/${topics.length} topics done, ${ok.filter((r) => r.fixed).length} needed a fix pass`)
return ok.map((r) => ({ key: r.research.key, verify: r.verify, draw: r.draw, critic: r.critic && { verdict: r.critic.verdict, issues: r.critic.issues }, fixed: !!r.fixed }))
