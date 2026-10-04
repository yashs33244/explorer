# Supply and demand graph

A supply and demand graph plots two opposing curves on the same axes and reads the answer where they cross. This example treats a checkout API under load like a market: the "price" is p99 latency and the "quantity" is requests per second. Client demand falls as latency rises (timeouts, users leaving), while cluster supply only serves more by queueing longer. With 6 pods the curves meet at 2.5k rps and 200 ms, over the 180 ms SLO; when the HorizontalPodAutoscaler adds 4 pods the supply curve shifts right and the new equilibrium is 3.0k rps at 160 ms, back under it. Numbered badges mark both points and the side panel explains them.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Where latency and throughput settle for a service, and why adding capacity moves the point.
- Why retries and client backoff matter: they shift demand, which scaling cannot fix.
- Capacity planning trade-offs: how many pods, nodes or partitions buy which latency.

Not for: a measured time series of load (use a line chart) or the request path itself (use a sequence diagram).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Canvas and plot panel | `d-box g2`, `d-fillpaper` | Plot on a plain panel inside a colored frame, like the template |
| Axes and ticks | `d-axis`, `d-fillink` dots, `d-s` | Quantity on x, price on y, units named |
| Demand curve | `d-edge acc thick` | Slopes down; labelled at its start with `d-lab` |
| Supply curve | `d-edge thick` | Slopes up; a shifted curve is `dash` with its own label |
| Shift | `d-edge acc` + marker + `d-lab` | Arrow from old to new curve with a verb (scale out) |
| Equilibrium | `d-badge` + `d-bt`, `d-grid` guides | Guides drop to both axes so the values can be read |
| Explanation | `d-box` with matching badge, `d-logo` box, `d-note` | Before and after values, the mechanism config, the lesson |

## Tips

- Say in the drawing what "price" and "quantity" mean for the system; that mapping is the insight.
- Shift one curve at a time and keep the original visible, so the move is obvious.
- Put the real values of each equilibrium in text; readers should not estimate them from the grid.

Reference: Figma template Supply and demand graph

Source: [example.svg](example.svg)
