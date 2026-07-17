# Codex support

dat-kit v1.17.1 supports Codex without changing its Claude Code adapter. The same `skills/` directory is the workflow source of truth; Codex receives it through `.codex-plugin/plugin.json`.

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

Brownfield scaffolding is two-pass and fail-closed. `init.sh --here` requires
Python and runs `scripts/contract_check.py --target .` before any mutation. A
competing `AGENTS.md`, substantive runtime pointer, legacy contract, unsafe
symlink, or incompatible partial install produces a named diagnostic and leaves
the complete destination unchanged. Starting in v1.17.0, generate a deterministic
read-only migration plan:

```bash
python "<DAT_KIT_ROOT>/scripts/contract_check.py" --target . --migration-plan
python "<DAT_KIT_ROOT>/scripts/contract_check.py" --target . --migration-plan --format json
```

The plan exits non-zero while drift remains and never changes the target. Review
and approve it separately, then reconcile policy, replace static files, inspect
runtime adapters, and rerun the checker.

### Contract file ownership

| Class | Files | Migration rule |
|---|---|---|
| Static dat-kit assets | `CLAUDE.md`, `.claude/CLAUDE.md`, `.cursorrules`, `docs/agent-workflow.md` | Inventory any project additions, move them to project-owned policy, then replace from the exact shipped template. |
| Project-owned policy | `AGENTS.md`, `docs/agent-working-rules.md` | Semantic merge; never byte-replace or discard local rules. |
| Runtime adapters | `.codex/config.toml`, `.codex/hooks.json` | Inspect tracking, routing, commands, and workflow dependencies manually before removal. |

For a typical v1.15 project, inventory policy from the old canonical file and
runtime pointers, merge it into the v1.16 `AGENTS.md` plus working rules, replace
the three pointers and static workflow from templates, inspect local adapters,
then require `contract_check.py --target .` to exit 0. The package version and
project-contract revision are independent: v1.17.1 continues to accept the
unchanged `dat-kit 1.16.0` contract layout.

## Host-specific behavior

| Capability | Claude Code | Codex |
|---|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` |
| Session bootstrap | Included through `hooks.json` | No shipped hook; skills plus `AGENTS.md` provide the workflow |
| Reviewer profiles | `agents/*.md` frontmatter and model routing | Fresh subagents use the same reviewer charters; no unverified model-routing schema |
| Token attribution | Exact session totals only when one session maps to one task | Parser unverified; new records keep `tokens: null` with `unsupported_provider` |

## Scorecard

Append through the helper instead of writing JSONL directly:

```bash
python3 scripts/scorecard.py --provider codex --project . --append-record record.json
```

`--provider codex` records `tokens: null` with the reason
`unsupported_provider`; it never estimates usage. Claude Code may use
`--provider claude`, but session totals are persisted only when exactly one
transcript session maps to the new task and no prior scorecard task maps to the
same session. Running the helper without `--append-record` may enrich a report
in memory; it never writes those display-only values back to history.

New scorecard lines use schema v2 and record `agent_runtime` (`claude-code`,
`codex`, `cursor`, or `other`), workflow, canonical-contract revision, and Git
state. Historical v1 lines remain append-only and valid only before the first
v2 record. The optional `token_attribution` object is additive, so v1.17 readers
that do not know it continue to ignore it safely.

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

## Local adapter cleanup

`.codex/config.toml` and `.codex/hooks.json` are intentionally untracked. Keep
proxy URLs, absolute paths, MCP servers, and statuslines machine-local and
opt-in. This repository also ignores `.claude/settings.local.json`; if it still
contains a Headroom SessionStart hook, remove that hook manually and verify with
`git check-ignore .claude/settings.local.json` plus a fresh session. Do not edit
the ignored file as part of a repository migration.

The Claude SessionStart adapter calls `node` only to print a neutral pointer to
root `AGENTS.md`. If the hook or `node` is unavailable, startup remains safe:
supported runtimes read `AGENTS.md` directly, and no unique policy lives in the
adapter.

Installed plugins and already-open sessions retain prior metadata until the
plugin is updated/reinstalled and a fresh session starts. The no-drift claim
applies only after `contract_check.py` validates the canonical installation;
unmigrated brownfield repositories may still contain competing policy.
