# Cloud architecture diagram

A cloud architecture diagram shows which managed services a workload runs on, how they sit inside account, region and network boundaries, and how requests and data move between them. This example is a checkout workload in one Azure region: Front Door routes shoppers to App Service, orders go through a Service Bus queue to Functions and land in Cosmos DB, Key Vault serves secrets through managed identity, and one Log Analytics workspace holds the Application Insights traces and the Key Vault audit logs (sent there by a diagnostic setting). Task and constraint panels sit on top, like the whiteboard template, so the drawing answers a stated design question.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a service is deployed on a cloud provider: which managed services, which region, which network.
- Where the request path ends and the async path (queues, workers) begins.
- What a reviewer must check for resilience and security: failover, secrets, telemetry.

Not for: the order of calls in one request (use a sequence diagram) or the internal modules of one service (use a component or layered diagram).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Task and constraint panels | `d-blob` + `d-k`, `d-t`, `d-s` | State the workload and the limits the design must meet, top of the canvas |
| Region or network boundary | `d-blob2` + `d-h`, `d-m` | One dashed boundary per region, VNet or account, with its CIDR or id |
| Managed service | `d-box g0`..`g5` + `d-logo` | Real product logo, short product name, real resource name in `d-m` |
| Request path | `d-edge acc` | Verb label in `d-lab`, arrowhead on every edge |
| Secret or config read | `d-edge` | Plain solid line, so it does not read as part of the request path |
| Telemetry or secondary path | `d-edge dash` | Say in a legend line what each line style means |
| Design note | `d-note` + `d-tn` | Failover, identity or cost decisions, outside the boundary |

## Tips

- Name resources the way they exist in the subscription (`app-checkout-prod`), not just the service type.
- Keep the async hop visible: the queue between the API and the worker is the decision a reviewer cares about.
- Global services (CDN, Front Door, DNS) sit outside the region boundary.
- Many services from one vendor share a vendor logo; the title and resource name do the distinguishing.

Reference: Figma template Cloud architecture diagram

Source: [example.svg](example.svg)
