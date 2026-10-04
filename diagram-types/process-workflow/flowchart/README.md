# Flowchart

A flowchart shows one process as a spine of steps (rectangles) and decisions (diamonds), with every branch labelled yes or no and every path ending in a terminal (pill). Here it walks one `POST /api/login` request through an auth service: a Redis-backed rate limit, an argon2id password check, an optional TOTP challenge and a shared failure counter, ending in 429, 401 or 200 with a session cookie.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a request handler branches: guard clauses, early returns and which status code each path produces.
- Where two failure paths converge on the same side effect (here, both bad passwords and bad codes increment one counter).
- The order of checks in a security-sensitive flow, so a reviewer can see the rate limit runs before the expensive hash.

Not for: handoffs between teams or services (use a cross-functional flowchart or sequence diagram) or long-lived states (use a state machine).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Start and end | `d-box g1` / `g3` rect, `rx` 20 | green for success, pink for an error response |
| Step | `d-box g0` rect | title in `d-t`, the real call or key in `d-m` |
| Decision | `d-box g2` polygon | a question of 2 to 4 words ending in "?" |
| Flow | `d-edge` + marker | main path straight down; branches leave from the diamond's side |
| Branch label | `d-lab` | "yes" or "no" next to the diamond it leaves |
| Product | `d-logo` | logo slot beside the step that uses it |

## Tips

- Keep the happy path on one vertical spine; send failures right and skips left so lines never cross.
- Merge repeated side effects into one node and point both branches at it.
- Put the concrete detail (key name, hash, status code) in the node, not a caption.

Reference: Figma template Flowchart

Source: [example.svg](example.svg)
