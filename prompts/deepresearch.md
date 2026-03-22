---
description: Run a thorough, source-heavy investigation on a topic and produce a durable research brief with explicit evidence and source links.
---
Run a deep research workflow for: $@

Requirements:
- If the task is broad, multi-source, or obviously long-running, prefer delegating through the `subagent` tool. Use the project `researcher`, `verifier`, and `writer` agents, or the project `deep` chain when that decomposition fits.
- If the user wants it to run unattended, or the sweep will clearly take a while, prefer background execution with `subagent` using `clarify: false, async: true`, then report how to inspect status.
- If the topic is current, product-oriented, market-facing, regulatory, or asks about latest developments, start with `web_search` and `fetch_content`.
- If the topic has an academic literature component, use `alpha_search`, `alpha_get_paper`, and `alpha_ask_paper` for the strongest papers.
- Do not rely on a single source type when the topic spans both current reality and academic background.
- Build a compact evidence table before synthesizing conclusions.
- Distinguish clearly between established facts, plausible inferences, disagreements, and unresolved questions.
- Produce a durable markdown artifact in `outputs/`.
- End with a `Sources` section containing direct URLs for every source used.
