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
- this is the file-reading path, not the embedded-context path

## Claude

Best mode: manual bootstrap or wrapper auto-load

Recommended process:

1. generate a context pack with `scripts/build_context_pack.py`
2. paste or upload the generated markdown
3. prepend the Claude adapter prompt from `templates/platform-prompts/claude.template.md`

Expectation:

- Claude client/web should not be assumed to read local files directly
- Claude continues from the pasted context pack, not from hidden file access or platform-native memory

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

Expectation:

- Kimi client/web should not be assumed to read local files directly
- Kimi continues from the pasted context pack, not from hidden file access or platform-native memory

Use Kimi mainly for:

- Chinese synthesis
- long document condensation
- source-heavy reading

## Qwen / other web clients

Best mode: manual bootstrap or wrapper auto-load

Recommended process:

1. generate a context pack with `scripts/build_context_pack.py`
2. paste or upload the generated markdown
3. use the platform-specific resume prompt if one exists, otherwise use the generic embedded-context prompt

Expectation:

- web clients should not be assumed to read local files directly
- they continue from pasted state, not from disk access

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
