# Codex support

dat-kit v1.15.0 supports Codex without changing its Claude Code adapter. The same `skills/` directory is the workflow source of truth; Codex receives it through `.codex-plugin/plugin.json`.

## Install

For published releases, add the repository marketplace and install `dat-kit` from it:

```bash
codex plugin marketplace add datmaiba/dat-kit
codex plugin add dat-kit@dat-kit
```

Start a new Codex task after installing or updating so skill metadata is refreshed. In the desktop app, the repository marketplace is also discoverable from the plugin directory.

## Project scaffolding

`project-init` creates both `CLAUDE.md` and `AGENTS.md`. `CLAUDE.md` remains the canonical shared project contract; `AGENTS.md` is a concise Codex entrypoint that routes the agent to it, the spec, working rules, lessons, and glossary.

Brownfield scaffolding remains additive: existing `AGENTS.md` and `CLAUDE.md` are never overwritten.

## Host-specific behavior

| Capability | Claude Code | Codex |
|---|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` |
| Session bootstrap | Included through `hooks.json` | No hook in v1; skills plus `AGENTS.md` provide the workflow |
| Reviewer profiles | `agents/*.md` frontmatter and model routing | Fresh subagents use the same reviewer charters; no unverified model-routing schema |
| Token enrichment | Claude transcript parser | Unsupported in v1; scorecard tokens remain `null` |

## Scorecard

Use `scripts/scorecard.py --provider claude` only when parsing Claude Code transcripts. `--provider codex` intentionally leaves token fields unchanged and reports that parser support has not been verified yet. It never estimates token usage.

## Development checks

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
```

The validator checks both plugin manifests, both marketplaces, and the shared skill path. CI also smoke-tests that scaffolding creates the Codex entrypoint without overwriting existing project guidance.
