---
name: scorecard
description: >-
  Benchmark scoring for AI-assisted work sessions. Invoke at the END of any
  substantive task — or whenever the user says "scorecard", "score this
  task", "benchmark this session", "log this work". Scores the task on a
  fixed 1-5 complexity rubric, estimates manual hours saved (clearly labeled as
  an estimate), records actual wall time and gate results, and appends one JSONL
  line to the project's benchmarks/scorecard.jsonl. Token usage is filled in
  later by scripts/scorecard.py, which parses Claude Code transcripts for real
  numbers. The build-loop skill calls this automatically at the end of every
  phase; use it standalone for one-off tasks outside the build loop.
---

# scorecard — score a completed task

Score honestly. A benchmark built on flattering numbers is worse than no benchmark: it teaches the user to trust noise. Estimated values are always labeled as estimates.

## Complexity rubric (fixed — never improvise your own scale)

| Score | Meaning |
|---|---|
| 1 | One file, cosmetic or config change, no logic risk |
| 2 | Single-layer logic change, few files, existing tests cover it |
| 3 | Multi-file feature inside one layer/module, new tests needed |
| 4 | Cross-layer feature (data → domain → UI), migrations or new contracts, edge-case surface |
| 5 | Multi-phase or architectural: DB schema + public contract + several modules, high blast radius |

Half-points are allowed (e.g. 3.5) when genuinely between levels.

## Fields to record

- `date` — ISO date. `ts` — ISO timestamp of task end (used to match tokens to a session later).
- `task` — short label ("blog phase 1", "fix Form.config ftCode bug").
- `complexity` — from the rubric, with one line of justification in `notes`.
- `est_manual_hours` — your estimate of hands-on hours a competent developer would need without AI. Propose it with your reasoning in one line; if the user is present, let them adjust — their number wins. This is an ESTIMATE and stays labeled as such.
- `actual_wall_minutes` — real elapsed time for the task (from session timestamps if known, otherwise ask).
- `gates` — concrete results string ("pest 24/24 ✓, tsc ✓") or "none run" — never invent.
- `tokens` — always `null` at write time; `scripts/scorecard.py` fills real numbers from transcripts.
- `model` — which model did the work, if known.
- `agent_runtime` — `claude-code`, `codex`, or `other`; identifies the host that ran the work.
- `workflow` — `build-loop`, `standalone`, or a named Domain Pack; identifies the working discipline used.

Existing JSONL lines are historical records and remain valid without these two
fields. Every new line must include both; never rewrite earlier lines merely to
normalize attribution.

## Process

### Host support

Resolve `DAT_KIT_ROOT` from the selected skill directory (two parent directories
up to the package root) before invoking the helper.
Use `python3 "$DAT_KIT_ROOT/scripts/scorecard.py" --provider claude` to parse
Claude Code transcripts. Use `--provider codex` in Codex: token enrichment is
not implemented until its transcript schema has a verified fixture, so the
script leaves `tokens` as `null` rather than estimating.

1. Compute/propose all fields. Show the line to the user in one compact block.
2. Append to `benchmarks/scorecard.jsonl` in the project root (create the directory on first use). Append-only — never edit or delete existing lines; corrections are new lines with a `supersedes` field.
3. Remind (once per session, not nagging): run the host-appropriate command from **Host support**. Never invoke the Claude transcript parser from Codex.

Example line:

```json
{"ts":"2026-07-12T15:04:00+07:00","date":"2026-07-12","task":"blog phase 1 — data layer","complexity":4,"notes":"migrations + repos + DTOs across api/, seeders","est_manual_hours":6,"actual_wall_minutes":42,"gates":"pest 18/18 ✓, pint ✓","tokens":null,"model":"sonnet-5","agent_runtime":"codex","workflow":"build-loop"}
```

## What NOT to do

Do not inflate `est_manual_hours` to make the tool look good — when unsure, estimate low. Do not fill `tokens` by guessing. Do not score trivial Q&A exchanges — the benchmark is for work, not chat.
