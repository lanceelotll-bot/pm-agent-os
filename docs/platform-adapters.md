# Platform Adapters

Use one shared context pack across platforms. Adapt only the startup method.

## Codex / GPT workspace

Best mode: native auto-load

Use:

- `AGENTS.md`
- `skills/pm-agent-os`
- `context/context-manifest.yaml`

Expectation:

- the workspace can read the shared files directly
- the assistant can follow the loading order automatically

## Claude

Best mode: manual bootstrap or wrapper auto-load

Recommended process:

1. generate a context pack with `scripts/build_context_pack.py`
2. paste or upload the generated markdown
3. prepend the Claude adapter prompt from `templates/platform-prompts/claude.template.md`

Use Claude mainly for:

- critique
- long-form rewrite
- edge-case review

## Kimi

Best mode: manual bootstrap or wrapper auto-load

Recommended process:

1. generate a context pack with `scripts/build_context_pack.py`
2. paste or upload the generated markdown
3. prepend the Kimi adapter prompt from `templates/platform-prompts/kimi.template.md`

Use Kimi mainly for:

- Chinese synthesis
- long document condensation
- source-heavy reading

## Generic API or wrapper

Best mode: wrapper auto-load

Recommended process:

1. the wrapper reads the context files
2. the wrapper injects the context pack before the user prompt
3. the wrapper logs output packet sections and memory deltas

## Practical rule

Cross-platform continuity should transfer:

- state
- assumptions
- next actions
- memory deltas

Do not transfer raw chat history unless there is a legal or audit requirement.
