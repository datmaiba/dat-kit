# dat-kit

A spec-driven development toolkit for Claude Code, distilled from real production workflows. One install gives your agent a complete working discipline: think before coding, plan before building, verify before claiming, and harvest lessons after shipping.

> Status: **v1.0.0 — dogfooded on a real project**. All skills, templates, agents, hooks, and CI have landed. See [Roadmap](#roadmap).

## What's inside

| Component | What it does |
|---|---|
| `skills/build-loop` | Self-questioning build loop: context load → self-question against spec → plan → approval gate → build → verified checks → independent review → lessons harvest. Supports one-shot PREFLIGHT + autopilot. |
| `skills/fable-mode` | Careful-working discipline with three effort levels (low/medium/high) scaling reasoning, verification, and reporting. For repos *without* the dat-kit scaffold — scaffolded projects already get this via the rules file and session hook. |
| `skills/fable-pro` | The same discipline, adapted for any profession — accounting, law, design, medicine. |
| `skills/guardian-builder` | Generate a project-specific "guardian" skill: guardrails, naming rules, plan gate, lessons integration for any repo. |
| `skills/project-init` | Scaffold a new project (or adopt an existing one) with CLAUDE.md, spec skeleton, rules, CONTEXT.md glossary, and a stack profile. |
| `skills/handoff` | Compact a session into a resumable handoff document in `handoffs/` — survives across sessions and machines; build-loop recovery reads it first; its format doubles as the builder brief for delegated builds. |
| `skills/scorecard` | Benchmark every task: fixed 1-5 complexity rubric, estimated manual hours (labeled as estimates), real wall time and gates — appended to `benchmarks/scorecard.jsonl`. `scripts/scorecard.py` fills real token usage from Claude Code transcripts and prints the aggregate table. |
| `skills/diagnosing-bugs` | Disciplined diagnosis loop for hard bugs and perf regressions: feedback-loop-first → reproduce+minimise → ranked falsifiable hypotheses → instrument one variable → fix behind a regression test → post-mortem into lessons-learned. The backward counterpart to build-loop. |
| `skills/improve-codebase-architecture` | Find "deepening" refactors (shallow → deep modules) for testability and AI-navigability: Explore subagent walk → ranked candidates in a fixed depth/seam vocabulary → grill the chosen one → hand the design to build-loop. |
| `skills/git-worktrees` | Set up an isolated workspace before a feature or a build-loop plan: detect existing isolation → prefer native worktree tools → git fallback (verified gitignored) → project setup → clean-baseline check. |
| `skills/domain-builder` | Interview a real practitioner and encode *their* discipline as a Domain Pack (ground-truth · gates · reviewers · deliverables · loop-profile). Enforces gate-validity (real worked cases + a "gamed by X" line + sign-off) and caps interview-authored domains at Turn/Goal. Only encodes domains someone in the room actually practices. |
| `skills/cookbook-lookup` | Source a proven recipe from the official [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) (MIT) when the repo has no local template for a Claude-API/agent pattern (RAG, tool use, evals, prompt caching, sub-agents, Agent SDK…): exhaust local sources first → locate + vet the recipe → hand it to `build-loop` to adapt and verify → attribute + harvest. Sourcing only; never bypasses a gate. |
| `skills/terse-mode` | Native output-compression toggle (`lite`/`full`) — cut filler while keeping every load-bearing detail. Zero dependency, no second hook, no statusline contention. Hard carve-out: never compresses evidence, gate results, error strings, the approval stop, or reviewer verdicts; reviewer subagents stay full. The built-in default; caveman is the opt-in companion for its extras. |
| `skills/knowledge-work` | First non-dev Domain Pack — research, writing, analysis. Ground yourself in primary sources, verify every claim against its cited source, pass the citation/fidelity/reliability/currency/coverage/consistency gates with an independent fact-check. Capped at the Goal loop (its load-bearing gate needs a human to close). |
| `docs/` | `loops.md` — the two-axis model (Domain × Loop) and the capability ladder (Turn/Goal/Time/Proactive, unlocked by gate quality). `domains.md` — the domain registry. `model-selection.md` — which model tier (`haiku`/`sonnet`/`opus`/`fable`/inherit) a subagent should run at, and the consult-dispatch escalation for surprise difficulty. |
| `agents/` | Independent reviewers: `plan-reviewer`, `qa-agent`, `code-reviewer`, `security-reviewer` — the builder never grades its own work. |
| `templates/` | `common/` (stack-agnostic CLAUDE.md, spec 00–08 skeleton, rules) + `profiles/` (battle-tested architecture rules per stack: `laravel-react`, `react`). |
| `hooks.json` | SessionStart bootstrap: injects the working discipline automatically — no manual skill invocation. |
| `scripts/statusline.py` | Per-turn + per-session token statusline for Claude Code (incremental transcript parse, ~cost, ctx %). One-time setup: `python3 scripts/statusline.py --install`. |

## Install

```
/plugin marketplace add datmaiba/dat-kit
/plugin install dat-kit@dat-kit
```

Local development / testing from a checkout:

```
claude --plugin-dir /path/to/dat-kit
```

## Quick start

```
/dat-kit:project-init my-app        # scaffold: CLAUDE.md + spec/ + rules + stack profile
/dat-kit:build-loop phase 0         # run the loop: self-question → plan → (approve) → build → verify
```

## Philosophy

- **Spec is law** — the agent answers its own questions from the spec and escalates only what the spec cannot answer.
- **One approval stop** — PREFLIGHT batches every decision up front; autopilot runs phases without interruptions, pausing only for high-severity questions (secrets, destructive ops, spec deviation, cost, public contracts).
- **Independent review** — a fresh subagent audits plans, attacks builds with edge cases, and reviews diffs. The builder never grades its own work.
- **Evidence over claims** — a phase without green checks and a working demo is not done. Reports state concrete results ("pest 24/24 ✓, tsc ✓"), never "everything works".
- **Lessons compound** — every correction becomes a lessons-learned entry that future sessions must read. Pairs with lesson-miner (companion tool) when installed.

## Stack profiles

Templates split into `common/` (discipline, applies everywhere) and `profiles/<stack>/` (architecture rules per stack). `laravel-react` shipped first — extracted from a production migration project; `react` (standalone SPA, no in-repo backend) followed. New profiles are added when battle-tested, not speculatively.

## Roadmap

- [x] v0.1.0 — plugin skeleton, marketplace, manifest
- [x] v0.2.0 — `build-loop` skill
- [x] v0.3.0 — `fable-mode`, `fable-pro`, `guardian-builder`
- [x] v0.4.0 — templates + `project-init` (greenfield & `--here` brownfield)
- [x] v0.5.0 — SessionStart hook + reviewer agents
- [x] v0.6.0 — CI (skill lint, shellcheck, info gate), docs, end-to-end smoke test
- [x] v0.7.0 — `scorecard` benchmark: complexity rubric, hours estimate, real token usage from transcripts
- [x] v1.0.0 — dogfooded on a real project
- [x] v1.1.0 — `security-reviewer` agent + hardened harvest flow (scorecard-first, 5-part wrap-up, autopilot lesson auto-append)
- [x] v1.2.0 — `scripts/statusline.py`: per-turn/per-session token usage in the Claude Code statusline
- [x] v1.3.0 — `CONTEXT.md` shared-language glossary (template + project-init + build-loop wiring) + `handoff` skill for cross-session resumption
- [x] v1.4.0 — delegated-build mode: fresh builder subagent per task, two-stage review (spec compliance → code quality), main session as orchestrator; briefs reuse the handoff format (v1.2.0–v1.4.0 shipped as one release train; ideas adapted from obra/superpowers and mattpocock/skills)
- [x] v1.5.0 — `diagnosing-bugs`, `improve-codebase-architecture`, `git-worktrees` skills (adapted from mattpocock/skills and obra/superpowers; folded into dat-kit's single-file, self-contained style)
- [x] v1.6.0 — skill-eval harness: `benchmarks/skill-evals.jsonl` + a static trigger-regression / collision check in `validate.py` (CI-enforced), guarding skill triggering when descriptions change
- [x] v1.7.0 — `project-init` suggests optional local-first companion tools (CodeGraph, Headroom) on a fresh repo — detect + suggest the exact command only, never auto-install (no coupling, no privileged commands)
- [x] v1.8.0 — general work-loop pivot (additive): Domain × Loop model (`docs/loops.md`), Domain Pack contract, `domain-builder` skill with gate-validity gating, `knowledge-work` as the first non-dev pack, domain registry (`docs/domains.md`). No structural moves; the dev experience is unchanged. Structural consolidation and Time/Proactive runners deferred behind a go/no-go once the pivot proves value on a real non-dev task.
- [x] v1.9.0 — model-selection guidance (`docs/model-selection.md`): tier table (`haiku`/`sonnet`/`opus`/`fable`/inherit) for routing subagent dispatches by cost-of-being-wrong, reviewer agents pinned to `opus`, and the consult-dispatch escalation — on objective failure (gates still red, hypotheses exhausted) a cheap builder gets ONE higher-tier read-only consult returning `PLAN` or `TAKE_OVER`, logged to `benchmarks/escalations.jsonl`.
- [x] v1.10.0 — `react` stack profile (`templates/profiles/react/`): architecture, gates (dev-container or host execution shapes), and traps for a standalone React + TypeScript SPA with no in-repo backend — extracted from production project lessons.
- [x] v1.11.0 — `cookbook-lookup` skill: source a vetted recipe from the official `anthropics/claude-cookbooks` (MIT) when no local template covers a Claude-API/agent pattern, then hand it to `build-loop` to adapt and verify. Sourcing step only — exhausts spec/profiles/CONTEXT/lessons/codebase first, never lowers the verification bar, and harvests recurring recipes toward a real stack-profile template.
- [x] v1.12.0 — `terse-mode` skill: a dat-kit-native output-compression toggle (`lite`/`full`) inspired by the caveman skill but built in — no second SessionStart hook, no statusline contention, and a hard carve-out so it compresses prose only and never evidence, gate results, error strings, the approval stop, or reviewer verdicts (reviewer subagents stay full). `project-init` now suggests caveman/cavemem as optional orthogonal companions under the existing detect-don't-install doctrine, pointing at `terse-mode` first and steering away from `cavekit` (a competing build loop).
- [x] v1.13.0 — knowledge-work `fact-check.template.md` deliverable; pack-contract completeness guard in `validate.py` (declared slot files must exist beside the pack's SKILL.md); domain-builder interview now asks required-inputs/missing-info policy and for a real input→output pair; lessons-learned: an install copy is not the source of record
- [x] v1.14.0 — dogfood lessons upstreamed from a real full-stack build: build-loop gains the "a green gate proves nothing until you've seen it fail" verification rule plus Reuse and rate-limit/retention self-question lenses; `laravel-react`/`react` profiles fix the no-op `tsc --noEmit` gate (→ `tsc -b`) and add traps for vitest's ESM-export blindness, `vite preview` proxy, vite-config reloads, public-endpoint retention, borrowed-method contracts, and framework exception conversion (v1.13.1 rode ahead as a patch: `validate.py` false-red on Windows cp1252 consoles)

## Maintenance

Plugin update workflow (in order, every time anything changes):

1. Edit the file (skill/agent/template/script/hook)
2. `python scripts/validate.py` — must print "all checks green" (same checks CI runs)
3. Bump version in BOTH `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — skip this and clients never see the update. Patch (`x.y.Z`) for fixes, minor (`x.Y.0`) for new features
4. `git add -A && git commit && git push` — check the GitHub Actions tab is green
5. In Claude Code: `/plugin` → Marketplaces → update dat-kit → Installed tab shows the new version (manual step by design — the model can't drive this UI, and it's a deliberate security checkpoint)
6. Open a NEW session — a running session still uses the version loaded at startup (or `/reload-plugins` if only a hook/agent changed)

## License

MIT — see [LICENSE](LICENSE).
