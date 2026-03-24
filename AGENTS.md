# Agents

`AGENTS.md` is the repo-level contract for agents working in this repository.

Pi subagent behavior does **not** live here. The source of truth for bundled Pi subagents is `.feynman/agents/*.md`, which the runtime syncs into the Pi agent directory. If you need to change how `researcher`, `reviewer`, `writer`, or `verifier` behave, edit the corresponding file in `.feynman/agents/` instead of duplicating those prompts here.

## Pi subagents

Feynman ships four bundled research subagents:

- `researcher`
- `reviewer`
- `writer`
- `verifier`

They are defined in `.feynman/agents/` and invoked via the Pi `subagent` tool.

## What belongs here

Keep this file focused on cross-agent repo conventions:

- output locations and file naming expectations
- provenance and verification requirements
- handoff rules between the lead agent and subagents
- remote delegation conventions

Do **not** restate per-agent prompt text here unless there is a repo-wide constraint that applies to all agents.

## Output conventions

- Research outputs go in `outputs/`.
- Paper-style drafts go in `papers/`.
- Session logs go in `notes/`.
- Plan artifacts for long-running workflows go in `outputs/.plans/`.
- Intermediate research artifacts are written to disk by subagents and read by the lead agent. They are not returned inline unless the user explicitly asks for them.

## File naming

Every workflow that produces artifacts must derive a short **slug** from the topic (lowercase, hyphens, no filler words, ≤5 words — e.g. `cloud-sandbox-pricing`). All files in a single run use that slug as a prefix:

- Plan: `outputs/.plans/<slug>.md`
- Intermediate research: `<slug>-research-web.md`, `<slug>-research-papers.md`, etc.
- Draft: `outputs/.drafts/<slug>-draft.md`
- Cited brief: `<slug>-brief.md`
- Verification: `<slug>-verification.md`
- Final output: `outputs/<slug>.md` or `papers/<slug>.md`
- Provenance: `<slug>.provenance.md` (next to the final output)

Never use generic names like `research.md`, `draft.md`, `brief.md`, or `summary.md`. Concurrent runs must not collide.

## Provenance and verification

- Every output from `/deepresearch` and `/lit` must include a `.provenance.md` sidecar.
- Provenance sidecars should record source accounting and verification status.
- Source verification and citation cleanup belong in the `verifier` stage, not in ad hoc edits after delivery.
- Verification passes should happen before delivery when the workflow calls for them.

## Delegation rules

- The lead agent plans, delegates, synthesizes, and delivers.
- Use subagents when the work is meaningfully decomposable; do not spawn them for trivial work.
- Prefer file-based handoffs over dumping large intermediate results back into parent context.
- When delegating to remote machines, retrieve final artifacts back into the local workspace and save them locally.

## Remote delegation

Feynman can delegate tasks to remote cloud machines via the `computer-fleet` and `computer-acp` skills. Load those skills on demand for CLI usage, session management, ACP bridging, and file retrieval.
