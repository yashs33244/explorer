# Network diagram

A network diagram shows where things run and how traffic is allowed to move between them: networks, subnets, gateways and the hosts or tasks inside. It reads left to right like the template chain, internet to gateway to the network block, and then top to bottom through the subnet tiers. The example is a production AWS VPC across two availability zones, with a load balancer in public subnets, ECS tasks in private subnets and RDS Multi-AZ in data subnets.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a request reaches a service: internet gateway, load balancer, target port.
- Why private tasks can reach out but not be reached (NAT egress, route tables).
- What survives an AZ failure, and which traffic crosses AZs (writes to the RDS primary).

Not for: service-level dependencies (use `c4-model`) or the order of calls (use `sequence-diagram`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Internet, gateway | `circle.d-box g1` + icons | a short chain on the left, joined by plain lines |
| VPC | `d-box g2` + `d-logo` | the outer block, CIDR and region in the header |
| Availability zones | `d-blob2` + `d-k` | dashed columns, one per AZ |
| Subnet tiers | `d-band g3` / `g1` / `g5` | public, private, data rows; CIDRs in the left gutter |
| Resources | `d-box g0` / `g4` | load balancer spans both AZs, one NAT per AZ |
| Traffic | `d-edge`, `d-edge dash` + `d-lab` | label with the port or purpose |
| Rules | `d-note` + `d-tn` | route tables and security groups as sticky notes |

## Tips

- Put CIDRs in a gutter, not inside the subnets, so vertical traffic arrows never cross text.
- Draw anything that spans zones (an ALB) as one shape across both columns.
- Show the one cross-AZ path explicitly; it is usually the latency or cost surprise.
- Keep firewall and routing rules in notes instead of as more arrows.

Reference: Figma template Network diagram

Source: [example.svg](example.svg)
