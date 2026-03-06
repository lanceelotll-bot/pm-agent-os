# PM Agent OS

[English](README.md) | [简体中文](README.zh-CN.md)

This workspace contains a reusable operating model for a product manager who may switch teams often and still wants continuity across conversations, memory, and execution.

## What this solves

- Keep stable personal memory outside any single chat thread
- Keep team-specific context separate from personal memory
- Make every task easy to hand off and resume
- Route work to a small set of specialized PM-oriented agents

## Recommended memory layers

1. Global memory
   Put durable personal context in `~/.codex/memories/memory.md`.
2. Team context
   Put team-specific context in a repo-local file based on `templates/team-context.template.md`.
3. Task brief
   Create one short task packet for any non-trivial request.
4. Handoff
   Update one current handoff file at the end of each work session.
5. Manifest
   Use `templates/context-manifest.template.yaml` when you want one canonical loading contract across models and platforms.

## Recommended team repo structure

```text
context/
  team-context.md
  team-context.example.md
handoffs/
  current.md
  current.example.md
tasks/
  active/
    current.md
    current.example.md
docs/
  pm-agent-cluster.md
```

## Operating routine

1. Fill `templates/personal-memory.template.md` once and place the result into `~/.codex/memories/memory.md`.
2. For each new team, create `context/team-context.md` from `templates/team-context.template.md`.
3. For each substantial piece of work, create a brief from `templates/task-brief.template.md`.
4. End each session by updating `handoffs/current.md` using `templates/handoff.template.md`.
5. Start the next session with the bootstrap prompt in `templates/session-bootstrap-prompt.template.md`.
6. In this workspace, `AGENTS.md` can act as the same-platform auto-loader policy for Codex-compatible sessions.
7. For Git repos, keep live state files local and commit only `.example` files plus templates.

## Practical rule

Do not rely on chat history as the source of truth. Treat chat as execution space and files as memory space.

## Git Hygiene

- Commit templates, docs, scripts, skills, and `.example` context files.
- Keep `context/team-context.md`, `handoffs/current.md`, and `tasks/active/current.md` local.
- Copy from `.example` files after cloning, or create new live files from the templates.

## Files in this workspace

- `docs/pm-agent-cluster.md`: the PM-oriented agent cluster design
- `docs/platform-adapters.md`: platform-specific startup guidance
- `templates/personal-memory.template.md`: durable self-context template
- `templates/team-context.template.md`: per-team context template
- `templates/task-brief.template.md`: standard task packet
- `templates/handoff.template.md`: resume-from-here template
- `templates/session-bootstrap-prompt.template.md`: prompt for seamless continuation
- `templates/platform-prompts/`: adapter prompts for Codex, Claude, and Kimi
- `templates/context-manifest.template.yaml`: portable loading contract
- `docs/cross-platform-memory-protocol.md`: cross-platform continuity design
- `AGENTS.md`: workspace-level auto-load policy
- `skills/pm-agent-os/`: reusable skill package for Codex-style invocation
- `scripts/build_context_pack.py`: export the current state into a single portable prompt pack
