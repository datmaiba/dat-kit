# HANDOFF 2026-07-23 — B3 subset #2 diagnosing-bugs defect projection

## Goal

Prepare and execute Phase 6B B3 subset #2 only: the diagnosing-bugs producer
and its durable `defect_recorded` projection. This is the next independently
governed B3 subset after subset #1; it is not yet planned, approved, or
implemented.

The contract-level responsibility is to emit `defect_recorded` from a real
post-mortem and project it to `benchmarks/defects.jsonl`. The required defect
tuple is defined in `docs/contracts/telemetry-v3.md` T3.7/T3.10.2/T3.12:
`defect_id`, `introduced_task`, `approving_reviewers`,
`gate_that_should_have_caught_it`, and `evidence_ref`.

## Runtime

Current session: `codex / GPT-5`. Recommended executor: **Claude Opus**.
Subset #2 needs cross-layer contract, producer, durable projection, and
security/authority judgment. Use Sonnet only after an approved plan reduces a
task to clearly bounded pattern-following edits. Review agents remain Opus.

## Workflow

`dat-kit:build-loop` with the `software-dev` Domain Pack, attended mode.
Subsets are independently planned, observed, reviewed, and approved.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- HEAD: `72ca145` (`docs(spike): close B3 HARVEST deferment`).
- Tracked worktree is clean.
- Preserve all existing user-owned untracked handoffs/plans. This handoff is
  newly created and may remain untracked for the receiving Claude session.
- Do not push unless the user separately requests it.

## State

### DONE

1. B3 subset #1 was closed as deferred, not active.
2. Platform-owner approval for proposal
   `proposal-0acfe665bc066c31dd5e` was recorded in commit `6f5393b` and is
   effective from
   `run-2026-07-23-phase6b-b3-deferment-83f065e`.
3. Unsafe scorecard/HARVEST authority was removed in `3f0cab9`; code-review
   cleanup landed in `9ed5821`; rejected CLI-value redaction landed in
   `671c9fe`; closure ledgers and scorecard receipt landed in `72ca145`.
4. All five producer rows remain `planned` with null event IDs. No live
   HARVEST helper, resolver, Host Adapter, capability, schema, storage, or
   activation mechanism was added.
5. Final subset #1 evidence: validator PASS; pytest `373 passed, 8 skipped`;
   Bash syntax PASS; ShellCheck PASS; diff-check PASS; targeted B3 suite
   `41 passed, 2 skipped`; QA `PHASE DONE`; code `APPROVE`; security `APPROVE`;
   final QA `PHASE DONE`.

### IN PROGRESS

None. Subset #2 has not begun.

### NOT STARTED

1. Load the diagnosing-bugs contract sections and existing project/runtime
   conventions.
2. Create a fresh subset #2 observation and a complete phase plan before
   product edits.
3. Run `plan-reviewer`, resolve blockers, and stop for explicit user approval.
4. After approval, implement the smallest commit-sized units, then run the
   sequential QA → code review → security review → final QA chain.
5. Record real post-mortem evidence only; no synthetic or retroactive defect
   receipts.

## Decisions in effect

- B3 subset #2 = diagnosing-bugs defect projection, not build-loop HARVEST,
  knowledge-work fact-check, task/handoff linkage, or reports.
- The producer responsibility is `defect_recorded` plus the durable
  `benchmarks/defects.jsonl` projection.
- A producer remains `planned` until a real post-mortem, validated event, and
  required artifact/projection evidence exist.
- The subset #1 deferment does not authorize subset #2 implementation or any
  new authority architecture.
- No `spec/08-decisions.md` exists in this repository; do not invent one.

## Files touched

- `docs/contracts/telemetry-v3.md` → authoritative event/projection contract;
  read only until the plan proves an amendment is needed.
- `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md` → prior B3
  producer ordering and real-receipt matrix.
- `docs/spikes/phase-6b/b3-observation.md` → historical B3 ledger; append only
  after subset #2 evidence exists, never rewrite subset #1 facts.
- Prospective subset #2 product/test paths → **unknown until discovery**;
  resolve them with `scripts/registry.py explain-evolution` before planning.

## Verified gates

Subset #1 final gates on `671c9fe`/`72ca145`:

- `python scripts/validate.py` → PASS.
- `pytest scripts/tests` → `373 passed, 8 skipped`.
- `bash -n scripts/init.sh` → PASS.
- `shellcheck scripts/init.sh` → PASS.
- `git diff --check` → PASS.
- Targeted B3 tests → `41 passed, 2 skipped`.

Subset #2 has no gates yet; state them as unverified until its approved plan
and candidate exist. There was no external `review-evidence` receipt for the
local subset #1 commit, so local fallback gates were used.

## Third-party tool risks

none reported

## Next steps

1. Read `docs/contracts/telemetry-v3.md` around T3.7, T3.10.2, T3.12 and the
   event table; read the B3 producer ordering in
   `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md`.
2. Inspect the current diagnosing-bugs skill/runtime surfaces and run
   `python scripts/registry.py explain-evolution <candidate-path>` for every
   proposed path; do not assume paths from the contract are already admitted.
3. Create a fresh observation plus a complete subset #2 plan covering scope,
   exact defect tuple/projection shape, threat model, red-before-green tests,
   rollback, reviewer chain, budget, and demo.
4. Dispatch `plan-reviewer`; present the reviewed plan and stop for explicit
   user approval before editing product files.
5. On approval only, implement subset #2 in dependency order and run its full
   gate/review chain. Append observations and scorecard only after evidence
   exists; rerun the consuming validator after each append.

## Traps

- Do not treat subset #1’s effective Class C decision as approval for subset #2.
- Do not backfill `defect_recorded` from old post-mortem prose; receipts must
  come from a real task lifecycle.
- Do not activate a producer from fixtures, hashes, prose, or synthetic events.
- Keep reviewers sequential and findings-scoped after fixes.
- A missing external QA receipt requires the documented local fallback, not a
  claim that CI ran.
- The scorecard append must be followed by `python scripts/validate.py`.
- Rejected CLI/input values must not be echoed into logs; test both separated
  and `--flag=value` forms where applicable.

## Glossary

`B3` · `defect_recorded` · defect tuple · `benchmarks/defects.jsonl` ·
`approving_reviewers` · `gate_that_should_have_caught_it` · producer receipt ·
`planned` · `active` · evidence reference · post-mortem
