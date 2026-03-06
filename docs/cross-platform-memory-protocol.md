# Cross-Platform Memory Protocol

This protocol is the portable layer that lets you switch:

- teams
- chat threads
- models
- platforms

without depending on any single vendor's native memory feature.

## Core rule

Do not move conversation history across platforms. Move the current state instead.

The current state should be stored in a small portable context pack:

1. global memory
2. team context
3. current handoff
4. active task brief
5. optional manifest

## Portable context pack

Use open formats only:

- Markdown for human-authored context
- YAML for manifest and routing metadata

Recommended files:

```text
~/.codex/memories/memory.md
context/team-context.md
handoffs/current.md
tasks/active/<task-name>.md
context/context-manifest.yaml
```

## Auto-load modes

There are only three realistic modes.

### Mode A: Native auto-load

Use when the platform supports project-level instructions, shared files, or workspace bootstrapping.

Examples in principle:

- workspace instructions
- project instructions
- repository-level agent instructions
- startup automations

This is the closest to your desired "open a new chat and it already knows the context".

### Mode B: Wrapper auto-load

Use an external control layer to inject the context pack into the model request.

Examples:

- your own script
- an API gateway
- a local app
- an MCP or agent framework

This is the most portable option across vendors.

### Mode C: Manual bootstrap

Upload or paste the context pack at the start of a session.

This is the fallback for platforms that do not support file-aware startup or shared project memory.

## What happens on the same platform

If you stay inside one platform, near-automatic loading is feasible only when one of these is true:

- the platform supports workspace or project instructions that always run
- the assistant can access the same files each session
- you configure a startup automation or reusable skill

If none of those are true, even the same platform will still need an explicit bootstrap step.

## What happens across platforms

Cross-platform continuity is not automatic by default.

If Claude, Kimi, or another platform cannot directly read the same files or receive them through a wrapper, then yes, you must manually provide context at session start.

But you do not need to load the full old dialogue.

You only need the latest portable context pack.

## Recommended model orchestration pattern

Use a role-based contract, not a vendor-specific contract.

Recommended generic roles:

- planner
- executor
- critic
- memory curator

Example assignment pattern:

- GPT-family model: planning, task routing, PRD structure, technical framing
- Kimi-like model: long-document digestion, Chinese-language synthesis, bulk source condensation
- Claude-like model: critique, rewrite quality, edge-case review
- Codex-like environment: repository tasks, file edits, structured execution

Treat the assignments above as operational preferences, not universal truths. Recalibrate them based on your real outputs.

## Required contracts between models

Never pass raw chat transcripts between models unless necessary.

Pass these packets instead:

### Input packet

- objective
- background
- constraints
- files read
- required output
- current assumptions

### Output packet

- conclusion
- evidence
- assumptions
- open questions
- next actions
- memory deltas

This keeps model switching cheap.

## Best practical answer to your goal

### Goal 1

Same platform should auto-load memory when possible.

Best implementation:

- workspace `AGENTS.md`
- reusable skill
- shared context files
- optional automation

### Goal 2

Different platforms should not require full conversation migration.

Best implementation:

- one portable context pack
- one manifest file
- one bootstrap prompt adapted per platform

### Goal 3

Model combination should be selectable per task.

Best implementation:

- one planner chooses the model routing
- every model reads the same task packet
- every model emits the same output packet

## Hard limitation

No vendor-native memory feature is reliably portable across all platforms.

If you want stable cross-platform continuity, the source of truth must live outside the platforms.
