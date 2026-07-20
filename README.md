# dat-kit

A spec-driven working-discipline toolkit for AI coding agents, distilled from real production workflows. One install gives your agent a complete working loop: think before coding, plan before building, verify before claiming, and harvest lessons after shipping. Since 2.0, the loop is an open platform: one host-neutral engine, per-domain policy packs, and a registry that generates every host-facing surface.

> Status: **v2.0.0 — open-platform release train** (branch `feature/open-platform-v2`; format frozen, tag pending the RC evidence bundle). Last shipped tag: `v1.17.1`. See [Roadmap](#roadmap).

## Architecture

Three layers, connected only through the registry:

| Layer | Location | What it owns |
|---|---|---|
| **Work-loop engine** | `engine/work-loop/` | The host-neutral phase machine (LOAD → SELF-QUESTION → PLAN → BUILD → VERIFY → REVIEW → HARVEST), composition and contradiction rules. No domain knowledge. |
| **Domain Packs** | `domains/<id>/` | What one *type of work* means, via the six-slot contract: `workflow` · `ground-truth` · `gates` · `reviewers` · `deliverables` · `loop-profile` (`docs/contracts/domain-pack.md`). Shipped: `software-dev` (flagship), `knowledge-work` (first non-dev pack). |
| **Registry + projections** | `registry/`, `scripts/render.py` | Descriptors are the single source of truth. Thin skill triggers under `skills/` and the greenfield scaffold plan are *generated* projections, byte-checked in CI (`render.py --check`). Registry validation is Python-stdlib-only; greenfield init stays Bash-only via a sanitized TSV projection. |

Generated projects carry one canonical contract: root `AGENTS.md`, revision **`dat-kit 2.0`** — the only green revision. `dat-kit 1.16.0` is a recognized migration source: the checker fails closed with `CONTRACT_MIGRATION_REQUIRED` and a deterministic, read-only migration plan (see [Quick start](#quick-start)). Runtime files (`CLAUDE.md`, `.cursor/rules/*.mdc`, …) are pointer-only adapters and never carry policy. Architecture decisions are versioned with evidence and revisit conditions — see [ADR 0001](docs/decisions/0001-open-platform.md) and `docs/loops.md` (the Domain × Loop model).

## Host support

Host claims follow the fact-check discipline in the platform plan §9.4: each row is backed by `registry/adapters.json` `official_facts` (all verified **2026-07-18** against official docs; re-verified before any RC that touches them). Lifecycle states: `repo_only → migration_ready → scaffold_active → retired` (`docs/contracts/host-adapter.md`).

| Host | Lifecycle | Contract access | Project artifacts | Notes |
|---|---|---|---|---|
| **Claude Code** | `scaffold_active` | `CLAUDE.md` + `.claude/CLAUDE.md` import `AGENTS.md` (memory-import mechanism) | Two pointer files | SessionStart bootstrap via `hooks.json`; plugin install below. `adapters/claude-code/ADAPTER.md` |
| **Codex** | `repo_only` | Reads `AGENTS.md` natively | **None** — zero pointer files | Plugin manifests only (`.codex-plugin/`, `.agents/plugins/`). `adapters/codex/ADAPTER.md` |
| **Cursor** | `migration_ready` | Reads root `AGENTS.md` and `CLAUDE.md` | `.cursor/rules/dat-kit.mdc` pointer (via approved migration only) | `.cursorrules` is deprecated → typed `RETIRE_LEGACY` inside a migration plan. `adapters/cursor/ADAPTER.md` |
| **Gemini CLI** | `repo_only` | `GEMINI.md` context + `@file` imports (documented, not live-verified) | None committed | No live-host run yet — activation gates listed in `adapters/gemini-cli/ADAPTER.md` |

Live host smokes (fresh-session trigger invocation + pack read) are maintainer-run gates recorded per ADAPTER.md checklist; repo-side conformance is enforced by `test_adapter_conformance.py` fixtures.

## What's inside

| Component | What it does |
|---|---|
| `skills/build-loop` | Generated trigger for the **software-dev** pack + engine. Self-questioning build loop: context load → self-question against spec → plan → approval gate → build → verified checks → independent review → lessons harvest. Supports one-shot PREFLIGHT + autopilot + delegated builds. |
| `skills/knowledge-work` | Generated trigger for the **knowledge-work** pack — research, writing, analysis. Primary-source grounding, citation/fidelity/reliability/currency/coverage/consistency gates, independent fact-check. Capped at the Goal loop (its load-bearing gate needs a human to close). |
| `skills/domain-builder` | Interview a real practitioner and encode *their* discipline as a six-slot Domain Pack, registered through the registry. Enforces gate-validity (real worked cases + a "gamed by X" line + sign-off) and caps interview-authored domains at Turn/Goal. |
| `skills/project-init` | Scaffold a new project (or adopt an existing one): canonical `AGENTS.md`, pointer-only runtime adapters, spec skeleton `00→08`, shared agent docs, `CONTEXT.md` glossary, stack profile. Brownfield is preflight-gated and fail-closed. |
| `skills/handoff` | Compact a session into a resumable handoff document in `handoffs/` — survives across sessions and machines; build-loop recovery reads it first; doubles as the delegated-build builder brief. |
| `skills/scorecard` | Benchmark every task: fixed 1-5 complexity rubric, estimated manual hours (labeled), real wall time and gates — appended to `benchmarks/scorecard.jsonl` without rewriting history. |
| `skills/diagnosing-bugs` | Disciplined diagnosis loop for hard bugs and perf regressions — feedback-loop-first, ranked falsifiable hypotheses, fix behind a regression test. The backward counterpart to build-loop. |
| `skills/improve-codebase-architecture` | Find "deepening" refactors (shallow → deep modules) for testability and AI-navigability, then hand the design to build-loop. |
| `skills/git-worktrees` | Isolated workspace before a feature or build-loop plan: native worktree tools preferred, git fallback, clean-baseline check. |
| `skills/fable-mode` / `skills/fable-pro` | Careful-working discipline with three effort levels — for repos *without* the dat-kit scaffold; `fable-pro` adapts it to any profession. |
| `skills/guardian-builder` | Generate a project-specific "guardian" skill: guardrails, naming rules, plan gate, lessons integration for any repo. |
| `skills/cookbook-lookup` | Source a vetted recipe from [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) (MIT) when no local template covers a Claude-API/agent pattern; hand it to build-loop to adapt and verify. |
| `skills/terse-mode` | Output-compression toggle (`lite`/`full`) — compresses prose only, never evidence, gate results, error strings, approval stops, or reviewer verdicts. |
| `agents/` | Independent reviewers: `plan-reviewer`, `qa-agent`, `code-reviewer`, `security-reviewer` — the builder never grades its own work. |
| `docs/` | `loops.md` (Domain × Loop model + capability ladder), `domains.md` (domain registry), `model-selection.md` (subagent tier routing + consult escalation), `contracts/` (normative registry/pack/adapter/contract formats). |
| `templates/` | `common/` (canonical AGENTS.md, pointer adapters, shared agent docs, spec skeleton) + `profiles/` (`laravel-react`, `react`). |
| `scripts/` | `validate.py` (full repo gate, CI-mirrored), `render.py` (projection generate + `--check`), `contract_check.py` (read-only brownfield preflight + migration planner), `init.sh`, `scorecard.py`, `statusline.py`. |

## Install

### Claude Code

```
/plugin marketplace add datmaiba/dat-kit
/plugin install dat-kit@dat-kit
```

Local development / testing from a checkout: `claude --plugin-dir /path/to/dat-kit`

### Codex

```bash
codex plugin marketplace add datmaiba/dat-kit
codex plugin add dat-kit@dat-kit
```

See [`adapters/codex/ADAPTER.md`](adapters/codex/ADAPTER.md) for host-specific setup, behavior, and migration guidance (formerly `docs/codex.md`).

## Quick start

```
/dat-kit:project-init my-app        # scaffold: AGENTS.md (dat-kit 2.0) + pointer adapters + docs/agent-* + spec/ + stack profile
/dat-kit:build-loop phase 0         # run the loop: self-question → plan → (approve) → build → verify
```

For an existing repository, `bash scripts/init.sh --here` first runs a read-only Python contract preflight. Competing policy, legacy files, unsafe links, and incompatible partial installs fail before mutation with a named diagnostic. A `dat-kit 1.16.0` project fails closed with `CONTRACT_MIGRATION_REQUIRED`; generate the deterministic, read-only plan first:

```bash
python "<DAT_KIT_ROOT>/scripts/contract_check.py" --target . --migration-plan
```

Migration application remains manual and separately approved; the plan preserves project-owned policy (`AGENTS.md` customizations, `docs/agent-working-rules.md`) by semantic merge with a provenance heading — never byte-replacement.

## Philosophy

- **Spec is law** — the agent answers its own questions from the spec and escalates only what the spec cannot answer.
- **One approval stop** — PREFLIGHT batches every decision up front; autopilot runs phases without interruptions, pausing only for high-severity questions (secrets, destructive ops, spec deviation, cost, public contracts).
- **Independent review** — a fresh subagent audits plans, attacks builds with edge cases, and reviews diffs. The builder never grades its own work.
- **Evidence over claims** — a phase without green checks and a working demo is not done. Reports state concrete results ("pest 24/24 ✓, tsc ✓"), never "everything works".
- **Generated, never hand-drifted** — host-facing surfaces are projections of registry descriptors, byte-checked in CI; editing a generated file is a build error, not a contribution.
- **Lessons compound** — every correction becomes a lessons-learned entry that future sessions must read.

## Stack profiles

Templates split into `common/` (discipline, applies everywhere) and `profiles/<stack>/` (architecture rules per stack). `laravel-react` shipped first — extracted from a production migration project; `react` (standalone SPA) followed. New profiles are added when battle-tested, not speculatively.

## Roadmap

- [x] v0.1.0–v1.14.0 — plugin skeleton → build-loop → reviewer agents → templates/profiles → scorecard + statusline → skill-eval harness → Domain × Loop pivot (`knowledge-work`, `domain-builder`) → model-selection guidance → `cookbook-lookup`, `terse-mode` → dogfood-hardened gates and traps (full per-release history: `git log --oneline v0.1.0..v1.14.0` or the release notes)
- [x] v1.15.0 — Codex adapter: native plugin manifest + marketplace, shared skills, dual-host validation
- [x] v1.16.0 — Shared-agent migration: `AGENTS.md` becomes the sole canonical contract; runtime files become pointers
- [x] v1.17.0 — Contract migration recovery: typed diagnostics + deterministic read-only migration planner; package versions decoupled from contract revision
- [x] v1.17.1 — Scorecard maintenance correction (append-only history, exact attribution or explicit unknown)
- [ ] **v2.0.0 — open platform (this branch)**: work-loop engine extracted; six-slot Domain Packs (`software-dev`, `knowledge-work`); registry-driven generated triggers + scaffold; host-adapter lifecycle with dated official facts; contract revision `dat-kit 2.0` with fail-closed 1.16 migration; format frozen (registry contract R9) — remaining: external host smokes, RC evidence bundle, migration guide, tag
- [ ] v2.1.0 — telemetry v3 (deferred by ADR 0001)
- [ ] v2.2.0 — governed self-evolution (deferred by ADR 0001)

The no-drift guarantee applies to installations that pass `python scripts/contract_check.py --target .`; unmigrated brownfield repos may still contain competing guidance. Installed plugins and active sessions keep old metadata until update/reinstall and a fresh session.

## Maintenance

Plugin update workflow (in order, every time anything changes):

1. Edit the file (skill/agent/template/script/hook) — never edit a generated projection by hand; edit the registry descriptor and run `python scripts/render.py`
2. `python scripts/validate.py` — must print "all checks green" (same checks CI runs); `python scripts/render.py --check` must exit 0
3. Bump `release_version` in `registry/platform.json`; its three mirrored version targets (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`) must match — validator-enforced. Update `.agents/plugins/marketplace.json` only if its source metadata changes
4. `git add -A && git commit && git push` — check the GitHub Actions tab is green (Ubuntu + Windows jobs)
5. In Claude Code: `/plugin` → Marketplaces → update dat-kit. In Codex: reinstall from the configured marketplace. Confirm the installed version in each host
6. Open a NEW session — a running session still uses the version loaded at startup

## License

MIT — see [LICENSE](LICENSE).
