# Session Bootstrap Prompt Template

Use one of the prompts below at the start of a new conversation.

## Continue Work In The Same Team

```text
Read my global memory, then read the current team context and current handoff, then continue the task.

Files to read first:
- ~/.codex/memories/memory.md
- context/team-context.md
- handoffs/current.md

After reading, do four things:
1. summarize the current state in 5 bullets
2. list missing context if any
3. choose the lead agent and optional support agents
4. continue the work
```

## Join A New Team Fast

```text
I am switching to a new team. Read my global memory first, then read the new team context, and build a 30-minute onboarding brief.

Files to read first:
- ~/.codex/memories/memory.md
- context/team-context.md

Output:
1. what this team does
2. key metrics and stakeholders
3. likely risks and unknowns
4. top 5 questions I should answer this week
5. which agent should lead my first three tasks
```

## Resume A Specific Task

```text
Read my global memory, team context, current handoff, and this task brief. Then resume from the most valuable next action.

Files to read first:
- ~/.codex/memories/memory.md
- context/team-context.md
- handoffs/current.md
- tasks/active/<task-name>.md

Output:
1. current status
2. best next action
3. draft deliverable
4. memory updates needed after this task
```
