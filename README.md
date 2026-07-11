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
| `skills/project-init` | Scaffold a new project (or adopt an existing one) with CLAUDE.md, spec skeleton, rules, and a stack profile. |
| `skills/scorecard` | Benchmark every task: fixed 1-5 complexity rubric, estimated manual hours (labeled as estimates), real wall time and gates — appended to `benchmarks/scorecard.jsonl`. `scripts/scorecard.py` fills real token usage from Claude Code transcripts and prints the aggregate table. |
| `agents/` | Independent reviewers: `plan-reviewer`, `qa-agent`, `code-reviewer` — the builder never grades its own work. |
| `templates/` | `common/` (stack-agnostic CLAUDE.md, spec 00–08 skeleton, rules) + `profiles/laravel-react/` (battle-tested architecture rules). |
| `hooks.json` | SessionStart bootstrap: injects the working discipline automatically — no manual skill invocation. |

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

Templates split into `common/` (discipline, applies everywhere) and `profiles/<stack>/` (architecture rules per stack). `laravel-react` ships first — extracted from a production migration project. New profiles are added when battle-tested, not speculatively.

## Roadmap

- [x] v0.1.0 — plugin skeleton, marketplace, manifest
- [x] v0.2.0 — `build-loop` skill
- [x] v0.3.0 — `fable-mode`, `fable-pro`, `guardian-builder`
- [x] v0.4.0 — templates + `project-init` (greenfield & `--here` brownfield)
- [x] v0.5.0 — SessionStart hook + reviewer agents
- [x] v0.6.0 — CI (skill lint, shellcheck, info gate), docs, end-to-end smoke test
- [x] v0.7.0 — `scorecard` benchmark: complexity rubric, hours estimate, real token usage from transcripts
- [x] v1.0.0 — dogfooded on a real project

## License

MIT — see [LICENSE](LICENSE).
