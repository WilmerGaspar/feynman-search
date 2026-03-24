---
description: Delegate a research task to a remote Agent Computer machine for cloud execution.
args: <task>
section: Internal
---
Delegate the following task to a remote Agent Computer machine: $@

## Workflow

1. **Check CLI** — Verify `computer` or `aicomputer` is installed and authenticated. If not, install with `npm install -g aicomputer` and run `computer login`.
2. **Pick a machine** — Run `computer ls --json` and choose an appropriate machine. If none are running, tell the user to create one with `computer create`.
3. **Pick an agent** — Run `computer agent agents <machine> --json` and choose an installed agent with credentials (prefer Claude).
4. **Create a session** — Use `computer agent sessions new <machine> --agent claude --name research --json`.
5. **Send the task** — Translate the user's research task into a self-contained prompt and send it via `computer agent prompt`. The prompt must include:
   - The full research objective
   - Where to write outputs (default: `/workspace/outputs/`)
   - What artifact to produce when done (summary file)
   - Any tools or data sources to use
6. **Monitor** — Use `computer agent watch <machine> --session <session_id>` to stream progress. Report status to the user at meaningful milestones.
7. **Retrieve results** — When the remote agent finishes, pull the results back with `computer agent prompt <machine> "cat /workspace/outputs/<slug>.md" --session <session_id>` (derive the slug from the task topic). Present results to the user.
8. **Clean up** — Close the session with `computer agent close <machine> --session <session_id>` unless the user wants to continue.
