# Model Routing Reference

Use role-based model routing when multiple platforms are available.

## Generic roles

- planner
- executor
- critic
- memory curator

## Suggested mapping

- Assign planning, framing, and final synthesis to the model that is strongest at structure and instruction-following.
- Assign long-source digestion to the model that handles your largest practical context windows best.
- Assign critique and rewrite to the model that produces the sharpest review quality in your workflow.
- Assign repository and file tasks to the model environment with the best local tooling access.

## Safe handoff rule

Do not hand off only a request sentence.

Hand off a compact packet:

- task
- context
- constraints
- files read
- expected output
- current assumptions

Require the receiving model to return:

- conclusion
- rationale
- assumptions
- open questions
- next actions
- memory deltas
