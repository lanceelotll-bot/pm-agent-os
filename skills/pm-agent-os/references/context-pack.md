# Context Pack Reference

Use the portable context pack as the source of truth.

## Files

- `~/.codex/memories/memory.md`
- `context/team-context.md`
- `handoffs/current.md`
- `tasks/active/current.md`
- `context/context-manifest.yaml`

## Intent

Each file has a different stability level:

- global memory changes rarely
- team context changes when teams or team knowledge change
- handoff changes often
- active task changes per task

## Update policy

Update only the layer that actually changed.

Do not write the same information to all files.

## Resume policy

At the start of a new session:

1. read the current state files
2. summarize current status
3. list missing context
4. choose the lead role
5. continue from the best next action
