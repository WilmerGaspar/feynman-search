---
name: deep
description: Gather, verify, and synthesize a deep research brief.
---

## researcher
output: research.md

Investigate {task}. Gather the strongest relevant primary sources, inspect them directly, and produce an evidence-first research brief.

## verifier
reads: research.md
output: verification.md

Verify the claims, source quality, and unresolved gaps in research.md for {task}. Produce a verification table and prioritized corrections.

## writer
reads: research.md+verification.md
output: deepresearch.md
progress: true

Write the final deep research brief for {task} using research.md and verification.md. Keep only supported claims, preserve caveats, and end with Sources.
