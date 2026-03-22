---
name: auto
description: Plan, investigate, verify, and draft an end-to-end autoresearch run.
---

## planner
output: plan.md

Clarify the objective, intended contribution, artifact, smallest useful experiment, and key open questions for {task}.

## researcher
reads: plan.md
output: research.md

Gather the strongest evidence, prior work, and concrete experiment options for {task} using plan.md as the scope guard.

## verifier
reads: plan.md+research.md
output: verification.md

Check whether the evidence and proposed claims for {task} are strong enough. Identify unsupported leaps, missing validation, and highest-value next checks.

## writer
reads: plan.md+research.md+verification.md
output: autoresearch.md
progress: true

Produce the final autoresearch artifact for {task}. If experiments were not run, be explicit about that. Preserve limitations and end with Sources.
