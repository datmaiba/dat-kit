# Codex support

dat-kit v1.16.0 supports Codex without changing its Claude Code adapter. The same `skills/` directory is the workflow source of truth; Codex receives it through `.codex-plugin/plugin.json`.

## Install

For published releases, add the repository marketplace and install `dat-kit` from it:

```bash
codex plugin marketplace add datmaiba/dat-kit
codex plugin add dat-kit@dat-kit
```

Start a new Codex task after installing or updating so skill metadata is refreshed. In the desktop app, the repository marketplace is also discoverable from the plugin directory.

## Project scaffolding

`project-init` creates a canonical `AGENTS.md`, shared `docs/agent-*.md`, and
pointer-only compatibility files (`CLAUDE.md`, `.claude/CLAUDE.md`, and
`.cursorrules`). All hosts read `AGENTS.md` first; no adapter may duplicate its
policy.

Brownfield scaffolding remains additive: existing `AGENTS.md` and `CLAUDE.md` are never overwritten.

## Host-specific behavior

| Capability | Claude Code | Codex |
|---|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` |
| Session bootstrap | Included through `hooks.json` | No shipped hook; skills plus `AGENTS.md` provide the workflow |
| Reviewer profiles | `agents/*.md` frontmatter and model routing | Fresh subagents use the same reviewer charters; no unverified model-routing schema |
| Token enrichment | Claude transcript parser | Unsupported in v1; scorecard tokens remain `null` |

## Scorecard

Use `scripts/scorecard.py --provider claude` only when parsing Claude Code transcripts. `--provider codex` intentionally leaves token fields unchanged and reports that parser support has not been verified yet. It never estimates token usage.

New scorecard lines record `agent_runtime` (`claude-code`, `codex`, or `other`)
and `workflow` (`build-loop`, `standalone`, or a Domain Pack). Historical JSONL
lines remain append-only and valid without those fields.

## Development checks

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
```

The validator checks both plugin manifests, both marketplaces, and the shared skill path. CI also smoke-tests that scaffolding creates the Codex entrypoint without overwriting existing project guidance.

## Optional companion tools

CodeGraph and Headroom are local, opt-in companions; neither is required for
dat-kit. Keep `.codegraph/codegraph.db` machine-local and commit only its
generated `.codegraph/.gitignore`. Restart Codex after changing a global MCP
entry. A configured Headroom MCP server exposes tools but does not activate proxy
routing; `headroom wrap codex` is the explicit opt-in route. Do not run
`specify init --here --force` in an existing dat-kit repository without an
approved file-by-file migration plan.
