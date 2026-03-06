# PM Agent Cluster

This design assumes one orchestrator plus a small set of specialist agents. The goal is not to maximize the number of agents. The goal is to reduce switching cost, make outputs predictable, and preserve continuity when teams change.

## Design principles

- One control plane, many specialist agents
- Shared memory contract across all agents
- Standard input packet and standard output packet
- Small-code tasks stay inside the cluster instead of creating a separate engineering workflow

## Shared memory contract

All agents should read from the same layers when available:

1. Global memory
   Personal working style, preferences, and durable context
2. Team context
   Product, users, metrics, stakeholders, constraints, glossary
3. Current handoff
   Latest status, next actions, blockers, changed assumptions
4. Task brief
   The goal, constraints, expected output, deadline, and success metric

## Agent roster

| Agent | Strength | When to use | Typical output | Reads |
| --- | --- | --- | --- | --- |
| PM Orchestrator | task framing, routing, synthesis | any new request, ambiguous work, multi-step work | execution plan, routed workflow, final synthesis | all layers |
| Memory Curator | continuity, context hygiene, handoff updates | resume work, switch teams, close a session, update durable context | memory updates, handoff snapshot, missing-context checklist | all layers |
| Trend Researcher | market scan, competitor review, opportunity framing | market research, trend watch, competitor teardown, landscape mapping | market brief, opportunity map, implications | global, team, task |
| Feedback Synthesizer | user feedback clustering and insight extraction | interview notes, tickets, app reviews, support logs, survey text | pain-point clusters, user themes, evidence summary | team, task |
| Metrics Analyst | KPI tree, funnel diagnosis, metric reading | growth issues, retention drop, funnel questions, metric review | KPI diagnosis, hypotheses, instrumentation gaps | team, task |
| Prioritization Planner | RICE, impact-effort, roadmap sorting | backlog sorting, sprint planning, tradeoff decisions | ranked list, rationale, suggested sequencing | team, handoff, task |
| PRD Architect | problem framing, scope writing, acceptance definition | new features, iterative specs, requirement docs | PRD, user stories, acceptance criteria, edge cases | team, task |
| Experiment Designer | growth loop, A/B plan, learning agenda | growth ideas, onboarding optimization, conversion work | experiment plan, variants, success criteria, guardrails | team, task |
| Delivery Coordinator | plan tracking, risk management, alignment | execution follow-up, launch prep, dependency tracking | delivery plan, risk list, owner list, milestones | team, handoff, task |
| UX Reviewer | flow review, interaction critique, usability risk | review flows, copy, empty states, onboarding, IA | UX risk list, flow improvements, content fixes | team, task |
| Technical Copilot | light code, SQL, scripts, API thinking, implementation review | metrics SQL, scripts, small UI changes, API review, technical validation | SQL, scripts, technical notes, implementation checklist | team, task |

## Recommended starter cluster

Do not start with all agents active by default. For a product manager handling internet product work plus light technical tasks, the best starting set is:

- PM Orchestrator
- Memory Curator
- Trend Researcher
- Feedback Synthesizer
- Prioritization Planner
- PRD Architect
- Technical Copilot

Add the rest only when the work volume justifies them:

- add `Metrics Analyst` when KPI and funnel analysis becomes frequent
- add `Experiment Designer` when growth experimentation is a core motion
- add `Delivery Coordinator` when cross-team execution risk becomes high
- add `UX Reviewer` when flows and interaction quality need dedicated review

## Recommended department view

### Control layer

- PM Orchestrator
- Memory Curator

### Insight layer

- Trend Researcher
- Feedback Synthesizer
- Metrics Analyst

### Planning layer

- Prioritization Planner
- PRD Architect
- Experiment Designer

### Delivery layer

- Delivery Coordinator
- UX Reviewer
- Technical Copilot

## Routing rules

### Rule 1

Every request starts with `PM Orchestrator`. It decides:

- whether the task is single-agent or multi-agent
- which agent leads
- which two support agents, if any, should join
- what memory files must be read first

### Rule 2

Any request that mentions "continue", "resume", "handoff", "switch team", "pick up where we left off", or "what changed" must also invoke `Memory Curator`.

### Rule 3

Any request that produces a new product decision, roadmap change, metric definition, or stakeholder commitment must end with a `Memory Curator` update.

### Rule 4

Light code tasks should only happen after the product intent is explicit. In practice:

- `PRD Architect` or `PM Orchestrator` defines scope
- `Technical Copilot` validates or implements the small technical task
- `Delivery Coordinator` records the result if it affects execution

## Standard multi-agent workflows

### Opportunity discovery

1. Trend Researcher
2. Feedback Synthesizer
3. Metrics Analyst
4. Prioritization Planner
5. PM Orchestrator

Use for new market opportunities, feature bets, and strategic scanning.

### New feature definition

1. PM Orchestrator
2. PRD Architect
3. UX Reviewer
4. Technical Copilot
5. Delivery Coordinator
6. Memory Curator

Use for a new feature, redesign, or scope definition that needs execution alignment.

### Iteration planning

1. Feedback Synthesizer
2. Metrics Analyst
3. Prioritization Planner
4. Delivery Coordinator
5. Memory Curator

Use for backlog grooming, sprint planning, or release reshaping.

### Growth experiment cycle

1. Metrics Analyst
2. Experiment Designer
3. UX Reviewer
4. Technical Copilot
5. PM Orchestrator

Use for onboarding, retention, activation, or conversion optimization.

### Team switch onboarding

1. Memory Curator
2. PM Orchestrator
3. Trend Researcher
4. Delivery Coordinator

Use when you join a new team and need fast situational awareness.

## Standard input packet

Every substantial request should provide or infer:

- objective
- background
- target user
- success metric
- deadline or cadence
- constraints
- source materials
- desired output format

If the packet is incomplete, `PM Orchestrator` should state assumptions explicitly instead of waiting unless the missing information is high risk.

## Standard output packet

Every agent output should end with:

- conclusion
- assumptions
- open questions
- next actions
- memory updates required

This makes synthesis and handoff cheap.

## Suggested default behavior

When you open a new session, ask the system to:

1. read global memory
2. read current team context
3. read current handoff
4. classify the request
5. select the lead agent and optional support agents
6. answer in the output packet structure

## Scope boundary

This cluster is optimized for:

- internet product management
- research and synthesis work
- strategy and prioritization
- PRD and delivery coordination
- small technical tasks

It is not optimized for:

- heavy software implementation
- deep data science work
- pixel-perfect design production

Those should be escalated into dedicated engineering or design workflows when needed.
