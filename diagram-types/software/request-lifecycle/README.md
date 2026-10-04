# Request lifecycle

The numbered path of one request from the client to the data store and back, with every hop as a box, every step as a badge on its arrow, and a latency bar that splits the total time across the hops. The example follows `GET /v1/orders/42` through Route 53, Cloudflare, an AWS load balancer, an orders-api pod on Kubernetes, a Redis cache miss and a Postgres read, then the 200 response.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Where the time goes in a slow endpoint, hop by hop, before anyone opens a profiler
- What happens on a cache miss versus a hit, and which layer terminates TLS
- Onboarding: the path a request takes through the edge, load balancer, pod and databases

Not for: many interacting requests over time or async fan-out; use `sequence-diagram` or `data-pipeline`.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Hop | `d-box g0..g5` + `d-logo` + `d-t` + `d-s` | One box per network hop, product logo, and what it does to this request |
| Main path | `d-edge acc` + marker | Left to right on one row, short verb label under each arrow |
| Side lookups | `d-edge` + marker | Elbow connectors to DNS and data stores, off the main row |
| Response | `d-edge acc dash` + marker | Returns along its own line under the main row |
| Step number | `d-badge` + `d-bt` | One per arrow, in time order, never on an arrowhead |
| Legend | `d-k` + `d-s` | Says what each group of numbers means |
| Latency bar | `d-fill g0..g5` + `d-tw` | Width proportional to milliseconds, same color as the hop it times |

## Tips

- Pick one concrete request with a real path and id; "a request" teaches nothing.
- Keep arrow labels to one or two words and put detail (status, TTL, port) in the box subtitle.
- If a segment is too thin for its label, put the label under the bar instead of shrinking the text.

Reference: Figma template Request lifecycle

Source: [example.svg](example.svg)
