# Choosing a diagram type

Pick the type whose shape matches what you are explaining, then start from its example: `diagram-types/<category>/<slug>/example.svg` in the explorer repo (its README lists the anatomy). Put the bare slug (the first column, for example `layered-architecture`) in `meta.json` as `"type"`. Generated from `diagram-types/catalog.json`.

## Software and systems

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `layered-architecture` | `software/layered-architecture` | Showing what runs in each tier of a service platform, the rule that calls only go down, and where cross-cutting concerns like tracing plug in. | tiers, layers, n-tier, presentation, application, data layer, observability, cross-cutting, dependency rule |
| `state-machine` | `software/state-machine` | Explaining an entity's status field, which transitions are legal, and which ones our code triggers versus webhooks and timers. | states, transitions, events, lifecycle, status enum, payment, terminal state, retry |
| `data-pipeline` | `software/data-pipeline` | Explaining how data moves from an OLTP database through streaming and batch stages to a dashboard, with the latency and contracts at each hop. | ETL, ELT, CDC, streaming, Kafka, warehouse, dbt, fan-out, data flow |
| `directory-tree` | `software/directory-tree` | Showing where code lives in a repo, which folders deploy versus get imported, who owns each area, and how paths map to CI. | monorepo, folder layout, repo structure, ownership, turborepo, pnpm, codeowners |
| `request-lifecycle` | `software/request-lifecycle` | Walking through one request end to end to show which hop does what and where the latency goes. | https request, latency, cdn, load balancer, cache miss, dns, end to end |

## Technical and architecture

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `cloud-architecture` | `technical/cloud-architecture` | Explaining which managed cloud services a system runs on, where the region and network boundaries are, and how the request path and async path move through them. | cloud, azure, architecture, front door, app service, service bus, functions, cosmos db, key vault, region, vnet, managed identity |
| `functional-decomposition` | `technical/functional-decomposition` | Explaining how a service or endpoint breaks into functions and sub-functions, and which team owns each branch. | functional decomposition, tree, hierarchy, checkout, functions, ownership, breakdown, refactor |
| `uml-use-case` | `technical/uml-use-case` | Showing who can trigger what on an internal platform and which behaviours are always included versus conditional. | uml, use case, actors, include, extend, ci/cd, system boundary |

## Diagramming and mapping

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `euler-diagram` | `mapping/euler-diagram` | Showing how policy or permission sets in a system contain one another, and which workloads fall entirely outside a rule. | euler, sets, containment, subset, service catalog, PII, backups, policy |
| `dichotomous-key` | `mapping/dichotomous-key` | Writing down a team's tech-selection or triage rule as a chain of yes or no questions that always ends in one answer. | dichotomous key, decision tree, yes no, datastore selection, database choice, triage |
| `family-tree` | `mapping/family-tree` | Tracing the lineage of a codebase, database or library through forks, rewrites and acquisitions, one generation per column. | family tree, lineage, fork, PostgreSQL, derivatives, genealogy, history |
| `tech-stack-mapping` | `mapping/tech-stack-mapping` | Explaining which tools a system uses per concern, and a migration plan from the current stack to the target stack with the status of each move. | tech stack, migration, heroku, aws ecs, mysql, postgresql, jenkins, github actions, new relic, datadog, redis, cloudflare, logos |
| `er-diagram` | `mapping/er-diagram` | Explaining which tables a service owns, which foreign keys tie them together, and the cardinality and constraints a migration must respect. | database, schema, tables, primary key, foreign key, crow's foot, postgres, cardinality, join table |
| `class-diagram` | `mapping/class-diagram` | Explaining an adapter or plugin seam in a codebase: one interface, one class per vendor, and which objects own or call which. | uml, class, interface, inheritance, realization, composition, association, oop, adapter |
| `mind-map` | `mapping/mind-map` | Explaining the surface area of a platform or framework to a new engineer, grouped by concern. | mind map, brainstorm, topic, branches, kubernetes, onboarding, radial |
| `kinship-diagram` | `mapping/kinship-diagram` | Show which forks, vendored copies and maintained siblings of a library exist and which ones need a security fix backported by hand. | kinship, lineage, fork, vendored, upstream, node.js, io.js, electron, package genealogy |
| `pedigree-chart` | `mapping/pedigree-chart` | Show which supported release branches inherit a security defect, which are only carriers through a transitive or shaded dependency, and where the defect was first detected. | pedigree, inheritance, CVE, log4shell, log4j, release branches, carrier, backport, security |
| `causal-loop` | `mapping/causal-loop` | Explaining feedback in an engineering system, such as why a team keeps slowing down as tech debt and on-call load grow, or how retry storms amplify an incident. | feedback loop, reinforcing, balancing, polarity, tech debt, on-call, velocity, systems thinking |
| `social-network` | `mapping/social-network` | Explaining who reviews or owns whose code across teams, where review load concentrates (bus factor), and which engineers bridge teams. | graph, nodes, edges, clusters, code review, teams, bus factor, hub |
| `venn-diagram` | `mapping/venn-diagram` | Explaining how three technologies, services or team responsibilities overlap before making a choice, for example which database family fits a service's needs. | sets, overlap, comparison, SQL, NoSQL, NewSQL, database choice, intersection |
| `c4-model` | `mapping/c4-model` | Showing which deployable containers a system is made of, the technology and protocol of each, and which datastore each service owns. | c4, container, microservices, api gateway, kafka, postgres, system boundary, architecture |
| `system-context` | `mapping/system-context` | Showing a single system from the outside: who uses it, which external systems push into it and which ones it drives. | system context, c4 level 1, integrations, webhook, deploy platform, kubernetes, pagerduty, slack, github |
| `network-diagram` | `mapping/network-diagram` | Showing where workloads run in a cloud network and how traffic is allowed to flow between the internet, subnets, availability zones and databases. | network, aws, vpc, subnets, availability zones, alb, nat gateway, rds, ecs, infrastructure |

## Process and workflow

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `cross-functional-flowchart` | `process-workflow/cross-functional-flowchart` | Showing how an incident, release or request is handed off between teams, with each step in the lane of the team that owns it. | swimlane, handoff, incident, on-call, roles, lanes, runbook |
| `sequence-diagram` | `process-workflow/sequence-diagram` | Showing the time-ordered calls between a client and services, such as an auth handshake or one request fanning out to an API and a database. | sequence, lifeline, activation, oauth, pkce, messages, request response |
| `bpmn` | `process-workflow/bpmn` | Showing a formal release or approval process across teams and systems, with events, gateways and message flows between pools. | bpmn, pools, gateway, events, release process, message flow, approval |
| `flowchart` | `process-workflow/flowchart` | Walk through how a request handler branches on rate limits, credentials and MFA, which status code each path returns, and where failure paths converge. | flowchart, decision, login, MFA, TOTP, rate limit, redis, argon2id, auth, request handling |
| `hiring-process-flowchart` | `process-workflow/hiring-process-flowchart` | Explain how an engineering interview loop is staged, which tool runs each round, and where candidates drop out. | hiring, interview loop, funnel, stage board, candidates, recruiting, kanban |
| `change-control-process` | `process-workflow/change-control-process` | Explain how a risky production change such as a database migration passes human gates, who owns each gate, and where it loops back or rolls back. | change control, CAB, RFC, change management, migration, rollback, ITIL, approval |
| `pdca-cycle` | `process-workflow/pdca-cycle` | Explain an iterative reliability or performance improvement loop with a measured before and after, such as cutting flaky CI tests. | PDCA, Deming cycle, continuous improvement, iteration, flaky tests, CI, kaizen |

## Data visualization

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `bar-graph` | `data-visualization/bar-graph` | Comparing one metric (build time, cost, error count) across services or pipelines, and showing which ones break a target. | bar chart, CI, build time, p95, SLO, comparison, services |
| `pie-chart` | `data-visualization/pie-chart` | Showing how one total, such as a cloud bill, traffic or storage, splits across a handful of services or teams. | pie chart, cloud cost, AWS bill, FinOps, share, breakdown |
| `supply-demand-graph` | `data-visualization/supply-demand-graph` | Explaining where latency and throughput settle for a service, and why adding capacity (supply) and cutting retries (demand) move that point differently. | supply and demand, capacity planning, autoscaling, HPA, latency, throughput, equilibrium |
| `bracket` | `data-visualization/bracket` | Explaining a pairwise elimination process in engineering, such as a hackathon, a vendor or library bake-off, or build candidates knocked out round by round until one ships. | bracket, tournament, elimination, hackathon, bake-off, knockout, rounds |
| `infographic` | `data-visualization/infographic` | Summarising a project's, platform's or migration's results in one glanceable card of small charts, each panel answering one question. | infographic, year in review, dashboard card, stats, open source, npm downloads, contributors, donut, bar chart, area chart |
| `radar-chart` | `data-visualization/radar-chart` | Comparing two or three technology options (databases, queues, frameworks) or a service's maturity scores across several normalised dimensions. | radar chart, spider chart, comparison, database selection, PostgreSQL, Cassandra, trade-offs, scoring |
| `heat-map` | `data-visualization/heat-map` | Showing when or where activity clusters across two categories, such as deploys, incidents or errors by day and hour or by service and region. | heat map, heatmap, deploy frequency, weekday hour, change freeze, DORA, incidents, matrix |

## Analysis and comparison

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `product-comparison` | `analysis/product-comparison` | Explaining why a design doc chose one queue, database or framework over its alternatives against agreed criteria. | comparison, checklist, vendor selection, kafka, rabbitmq, sqs, build vs buy, feature matrix |
| `quad-chart` | `analysis/quad-chart` | Explaining which tech debt or backlog items a team should fund now, plan, fill in, or decline, based on impact and effort. | 2x2, quadrant, impact effort, prioritization, tech debt, matrix, backlog |
| `bubble-map` | `analysis/bubble-map` | Explaining the character of one component (a cache, queue or index) to a new engineer, with each property backed by a setting or metric. | bubble map, thinking map, adjectives, describe, cache, redis, properties |
| `sandwich-chart` | `analysis/sandwich-chart` | Explaining the sections of a PR, RFC or incident template, the order they go in and which audience reads each one. | pr description, template, layers, pull request, rollout, review |
| `decision-tree` | `analysis/decision-tree` | Explaining how an architecture decision or triage rule reached its choice through a series of yes or no questions. | decision, adr, kafka, sqs, kinesis, rabbitmq, queue, stream |
| `outcome-mapping` | `analysis/outcome-mapping` | Explaining how a platform or DevEx investment turns from activities into countable outputs, behavior outcomes and delivery impact. | outcome, impact, logic model, devex, onboarding, enablement, metrics |

## Planning and management

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `vertical-timeline` | `planning/vertical-timeline` | Explaining how an incident, a release or a service's history unfolded in order, with exact timestamps and the system involved at each step. | timeline, incident, postmortem, utc, phases, chronology, sre |
| `project-plan` | `planning/project-plan` | Explaining a migration or platform project phase by phase, with who owns each deliverable, when it is due and which phase is at risk. | project plan, migration, phases, owners, status, strangler fig, table |
| `yearly-calendar` | `planning/yearly-calendar` | Explaining a team's release train across a year: release dates, major versions and the code freeze windows to plan around. | calendar, year, release train, code freeze, cadence, releases, planning |
| `gantt-chart` | `planning/gantt-chart` | Explaining a software release plan: which workstreams run in parallel, what blocks launch, where a slip lands relative to today, and who owns each step. | gantt, schedule, release plan, dependencies, milestone, critical path, today line |
| `horizontal-timeline` | `planning/horizontal-timeline` | Explaining the release or deprecation history of a platform or service, and why an upgrade or migration path looks the way it does. | timeline, horizontal, release history, kubernetes, deprecation, milestones, eras |
| `calendar-planner` | `planning/calendar-planner` | Explaining how a team's sprint cadence, release trains, code freezes, infra change windows and on-call rotation line up across one month. | calendar, month, sprint, release, code freeze, on-call, planner |
| `time-blocking` | `planning/time-blocking` | Explaining how an engineer protects focus time around standups, reviews, deploys and on-call interrupts, and what an on-call week costs in calendar time. | time blocking, calendar, deep work, focus, on-call, code review, schedule |
| `weekly-schedule` | `planning/weekly-schedule` | Explaining the ceremony rhythm of a sprint week, where focus time survives, and what happens on ship day. | weekly schedule, sprint week, ceremonies, focus blocks, ship day, release |
| `todo-list` | `planning/todo-list` | Showing what must be true before a release or cutover ships, who owns each item, and which open item is blocking it. | checklist, release, priorities, owners, progress, todo |

## Customer and user experience

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `service-blueprint` | `customer-ux/service-blueprint` | Showing which hidden backend services and infrastructure sit behind each user-visible step of a self-serve product flow, and who owns each layer. | service blueprint, frontstage, backstage, line of visibility, self-serve, provisioning, control plane, swimlane |
| `marketing-funnel` | `customer-ux/marketing-funnel` | Explaining which product events define each funnel stage, where developer activation leaks, and how the numbers flow from tracking to the dashboard. | funnel, conversion, activation, growth, analytics events, developer tool, drop-off |
| `territory-map` | `customer-ux/territory-map` | Showing which on-call team owns which cloud regions and how a follow-the-sun rotation hands off to cover 24 hours. | territory map, on-call, follow-the-sun, timezone, ownership, regions, coverage, pagerduty |
| `customer-journey` | `customer-ux/customer-journey` | Explaining API or SDK developer experience end to end and where time-to-first-call or activation is lost. | journey, developer experience, emotion curve, touchpoints, pain points, TTFC |
| `employee-journey` | `customer-ux/employee-journey` | Explaining an engineering onboarding plan, who owns each phase, and where new hires lose time before joining on-call. | onboarding, employee journey, on-call, phases, mood, engineering ramp-up |
| `ux-workflow` | `customer-ux/ux-workflow` | Explaining a login or onboarding flow that crosses the CLI and the browser, what each screen shows, which backend call moves the user to the next screen, and the error branches that need their own screens. | ux flow, user flow, screen flow, device code, oauth, cli login, onboarding, decision, screens |

## Design and content

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `wireframe` | `design-content/wireframe` | Explaining the layout of a docs portal or console page before it is built, which API or data source feeds each block, and the design decisions a page review should question. | wireframe, lo-fi, landing page, docs site, layout, mockup, annotations, page design |
| `sitemap` | `design-content/sitemap` | Explaining the URL and route structure of a docs site or web app, where a new page belongs, which redirects a restructure needs, and which pages depend on external systems. | sitemap, site map, information architecture, routes, url structure, docs site, navigation, tree |
| `storyboard` | `design-content/storyboard` | Replaying how an incident, release or migration played out, step by step, showing what the engineer saw on screen at each moment. | storyboard, incident, timeline, panels, rollback, canary, postmortem, runbook |
| `concept-map` | `design-content/concept-map` | Explaining how the concepts of a protocol or domain relate, where each arrow reads as a sentence, before someone reads the code or spec. | concept map, propositions, TLS, handshake, cryptography, domain vocabulary, cross-link |
| `brand-guidelines` | `design-content/brand-guidelines` | Explaining which design tokens and UI rules a frontend codebase enforces, with each token named the way it appears in code. | brand guidelines, design system, design tokens, type scale, color tokens, do and don't, frontend |
| `culture-design-process` | `design-content/culture-design-process` | Explaining how an engineering practice such as blameless postmortems or code review norms becomes concrete rituals, tracked actions and CI-enforced rules. | culture canvas, engineering culture, blameless postmortem, code review norms, discover define design embed, values, rituals |

## Organization and hierarchy

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `org-chart` | `org-hierarchy/org-chart` | Explaining which engineering team owns which system and how headcount and on-call ownership are spread across the org. | org chart, reporting lines, engineering org, teams, ownership, headcount, hierarchy |
| `project-org-chart` | `org-hierarchy/project-org-chart` | Explaining who owns each workstream of a cross-team migration or release, who makes the go/no-go call, and the milestone each workstream is driving to. | project org chart, workstreams, database migration, sponsor, tech lead, milestones, RACI |
| `geographic-org-structure` | `org-hierarchy/geographic-org-structure` | Explaining which engineering hub owns which services and how on-call hands off across time zones. | org chart, regions, hubs, time zones, follow-the-sun, on-call, site lead, distributed teams |
| `succession-planning` | `org-hierarchy/succession-planning` | Explaining who can take over critical engineering roles, how a promotion cascades, and where a system is left with a bus factor of one. | succession, bench, ready now, ready later, bus factor, staff engineer, engineering manager, risk |
| `nine-box-talent-matrix` | `org-hierarchy/nine-box-talent-matrix` | Explaining where engineers land in a calibration and what the next step is for each group. | 9 box, nine box, talent, calibration, performance, potential, promotion, grid |

## Business and strategy

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `rean-model` | `business-strategy/rean-model` | Explaining how an open source project or developer tool turns visitors into active users and contributors, and which channel and team drives each stage. | REAN, reach, engage, activate, nurture, open source growth, devrel, adoption funnel |
| `cynefin-framework` | `business-strategy/cynefin-framework` | Explaining why production incidents need different response playbooks depending on how knowable the cause is. | cynefin, incident response, complex, complicated, chaotic, clear, runbook, sre |
| `balance-wheel` | `business-strategy/balance-wheel` | Explaining a team or service engineering health check across tests, docs, on-call, deploy frequency, security and onboarding, and why the weakest areas get next quarter's time. | balance wheel, engineering health, team health check, scorecard, dora, on-call, onboarding |
| `smart-goals` | `business-strategy/smart-goals` | Explaining whether an engineering target such as a latency SLO or error budget is specific, measured, feasible, relevant and dated before a team commits to it. | smart, goal, okr, slo, latency, p95, target, objective |
| `value-stream-map` | `business-strategy/value-stream-map` | Explaining where a change spends its time from commit to production and which delivery bottleneck to fix first. | value stream, vsm, lead time, flow efficiency, dora, delivery, wait time, lean |
| `sipoc` | `business-strategy/sipoc` | Explaining the boundary of a CI or release pipeline: who supplies what it consumes, what it produces, and which downstream teams depend on each output. | sipoc, ci pipeline, scope, suppliers, inputs, outputs, customers, supply chain |
| `quick-reference-guide` | `business-strategy/quick-reference-guide` | Showing the handful of commands or facts an engineer needs under pressure, grouped by intent, with the risky ones flagged. | cheat sheet, quick reference, on-call, git, kubectl, commands, runbook card |
| `marketing-mix` | `business-strategy/marketing-mix` | Explaining how a developer tool or SDK is packaged, priced, distributed and announced, and where engineering choices carry go-to-market decisions. | 4Ps, marketing mix, product, price, place, promotion, developer CLI, launch |
| `pest-analysis` | `business-strategy/pest-analysis` | Showing the outside forces (regulation, cost, developer expectations, technology) that shape a platform launch and which decisions they drove. | PEST, political, economic, social, technological, external factors, vector database, launch |

## Education

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `sentence-diagram` | `education/sentence-diagram` | Showing how an API call or runbook line reads as a sentence, so receiver, method, argument and policy flags each map to a grammatical role and an ambiguous modifier is easy to spot. | reed-kellogg, grammar, parts of speech, api naming, method call, runbook, scheduler, retry |
| `interview-cheat-sheet` | `education/interview-cheat-sheet` | Laying out what an engineering interview loop or review covers round by round, so each round has distinct questions and a clear signal. | interview, hiring loop, backend, system design, coding round, behavioral, cheat sheet, on-call |
| `journaling` | `education/journaling` | Showing a repeatable daily engineering log format (shipped, blocked, learned, plan) and how on-call load and delivery look across several days. | journal, daily log, engineering log, standup, on-call, shipped blocked learned, reflection |
| `frayer-model` | `education/frayer-model` | Pinning down a term a codebase relies on, such as idempotency, by showing what it is and the near misses that are not. | frayer, definition, concept, idempotency, examples, non-examples, glossary, quadrant |
| `study-guide` | `education/study-guide` | Laying out what an engineer needs to revise for a service, an on-call rotation or a system design interview, grouped by kind of material. | study guide, notebook, revision, interview prep, system design, cheat sheet, onboarding |
| `research-outline` | `education/research-outline` | Showing the argument structure of a systems paper, design doc or RFC section by section before it is written or reviewed. | research outline, paper, rfc, design doc, raft, consensus, sections, distributed systems |

## Creative

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `vision-board` | `creative/vision-board` | Showing where an engineering team wants its platform to be in a year, with one measurable target per theme. | vision, goals, platform, north star, targets, FY plan |
| `kudos-cards` | `creative/kudos-cards` | Recognising who did what during an incident response or launch as the close of a blameless postmortem. | kudos, thank you, recognition, incident, postmortem, team |
| `work-anniversary` | `creative/work-anniversary` | Telling an engineer's multi-year impact through the systems they shipped. | anniversary, celebration, milestones, tenure, certificate, recognition |

## Admin and reference

| Slug | Folder | Use it to explain | Match on |
|---|---|---|---|
| `time-zone-clock` | `admin/time-zone-clock` | Explaining a follow-the-sun on-call rotation, or regional batch and deploy windows, and where the handoff overlaps fall in UTC. | on-call, follow-the-sun, time zone, rotation, handoff, pagerduty, utc, clock |
| `periodic-table` | `admin/periodic-table` | Explaining which tools a platform team runs, grouped by job, as a scannable catalogue with real product logos. | devops, toolchain, catalog, platform team, periodic table, logos, tooling radar |
| `phone-tree` | `admin/phone-tree` | Explaining an incident or DR escalation path: who calls whom, in what order, by when, and what happens on no answer. | escalation, sev1, incident, call tree, on-call, runbook, pagerduty |

