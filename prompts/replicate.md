---
description: Plan or execute a replication workflow for a paper, claim, or benchmark.
---
Design a replication plan for: $@

Requirements:
- Use the `subagent` tool for decomposition when the replication needs separate planning, evidence extraction, and execution passes.
- Identify the canonical paper or source material first.
- Use `alpha_get_paper` for the target paper.
- Use `alpha_ask_paper` to extract the exact implementation or evaluation details you still need.
- If the paper links code, inspect it with `alpha_read_code`.
- Determine what code, datasets, metrics, and environment are needed.
- If enough information is available locally, implement and run the replication steps.
- Save notes, scripts, and results to disk in a reproducible layout.
- Be explicit about what is verified, what is inferred, and what is still missing.
- End with a `Sources` section containing paper and repository URLs.
