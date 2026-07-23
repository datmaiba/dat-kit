# HANDOFF 2026-07-23 — Replan B3 subset #1 reviewer-fix line budget

## Goal

Close the three findings from B3 subset #1 code review under the
maintainer-approved contract amendment: reuse an existing LOAD-minted task,
emit no lesson event without real receipts, and bind activation status to a
validated producer receipt. The uncommitted reviewer-driven fix reaches 625
combined added product/test lines against the base, exceeding the approved
approximately 600-line ceiling. D-B3-3 requires `STOP + REPLAN`.

Maintainer Dat resolved this stop on 2026-07-23 by raising the subset #1
ceiling to approximately 650 lines. Every line above the original 469 remains
reserved exclusively for reviewer-driven fixes and their regression tests.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop` with sequential independent reviewers;
`dat-kit:handoff` at the mandatory line-budget stop.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- HEAD: `141e87c`.
- Committed candidate chain: `4bd5715` → QA-1 fix `141e87c`.
- Uncommitted reviewer-driven changes:
  `telemetry/producers.py`, `scripts/scorecard.py`,
  `scripts/tests/test_telemetry_producers.py`, and
  `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-contract-replan.md`.
- This handoff is also new and uncommitted.
- Eight pre-existing user-owned provenance files under `handoffs/` and
  `plans/` remain untouched and untracked.

## State

- DONE:
  1. Full freeze gates passed once on `4bd5715`: validator PASS; pytest
     `375 passed, 8 skipped`; Bash PASS; ShellCheck PASS; diff check PASS.
  2. QA-1 fixed in `141e87c`; findings-scoped QA returned `PHASE DONE`.
  3. Code review returned two P1 findings and one P2 finding.
  4. Maintainer approved the recommended contract replan: require an existing
     LOAD-minted task and real receipts; no candidate means no event; defer
     LOAD/start integration and activation.
  5. Uncommitted fix removes HARVEST task minting, makes no-candidate scorecard
     completion `not_applicable`, and validates active receipt IDs against
     lifecycle-validated producer events/revisions.
  6. Focused regression is green: `39 passed, 2 skipped in 2.00s`.
- IN PROGRESS:
  1. Reviewer-fix diff awaits commit and findings-scoped code re-review.
  2. Approved added product/test lines against `1a2cd54`:
     `scripts/scorecard.py` 86,
     `scripts/tests/test_telemetry_producers.py` 252, and
     `telemetry/producers.py` 287; total 625.
- NOT STARTED:
  1. Commit of the three-finding fix.
  2. Findings-scoped code re-review.
  3. Full security review.
  4. Observation ledger, scorecard append, validator rerun, five-part report,
     and stop before subset #2.

## Decisions in effect

- D-B3-1/D-B3-5: all registry entries remain `planned`; activation requires a
  validated real receipt and cannot come from tests or prose.
- D-B3-3 resolved again (maintainer Dat, 2026-07-23): ceiling approximately
  650 combined added product/test lines. Every line above the original 469 is
  reviewer-fix/regression-only. New architecture, schema, locked internals, or
  another subset's wiring still requires replan.
- D-B3-4: public telemetry writer surfaces only; append/lock/strict-tail
  internals remain untouched.
- Contract replan approved 2026-07-23: existing LOAD-minted task plus real
  receipt inputs are required; no-candidate scorecard appends emit no event;
  task-start/LOAD integration remains deferred.
- The current 625-line diff is approved; no decision authorizes exceeding
  approximately 650 lines.

## Files touched

- `telemetry/producers.py` → uncommitted existing-task lifecycle and validated
  activation-receipt fix.
- `scripts/scorecard.py` → uncommitted task-ID input and no-candidate
  `not_applicable` behavior.
- `scripts/tests/test_telemetry_producers.py` → uncommitted regressions for all
  three code-review findings.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-contract-replan.md` →
  uncommitted record of the approved contract amendment.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-review-fix-line-budget.md` →
  this uncommitted stop record.
- `scripts/telemetry.py` → untouched.

## Verified gates

- Full freeze gates on `4bd5715`: PASS as listed above.
- QA-1 findings-scoped re-review on `141e87c`: 6 checks passed;
  `PHASE DONE`.
- Current focused regression:
  `pytest scripts/tests/test_telemetry_producers.py
  scripts/tests/test_scorecard_append.py -q` →
  `39 passed, 2 skipped in 2.00s`.
- Current full gates → intentionally not rerun; the approved process allowed
  one freeze run and findings-scoped reviewer regressions.
- Code findings re-review → not dispatched.
- Security review → not dispatched.

## Third-party tool risks

none reported

## Next steps

1. Recount the exact base diff, commit the reviewer fix, and
   send only the three prior findings to the same code reviewer.
2. Continue only after code `APPROVE`: full security review, then observation
   and scorecard closure.

## Traps

- The current 625 lines fit the approved approximately 650 ceiling; any
  additional line must still be reviewer-driven.
- Do not remove regression meaning merely to hit a line number.
- Do not reintroduce HARVEST-time task minting or digest-manufactured lesson
  receipts.
- Do not accept UUID shape as activation proof.
- Do not dispatch security review before code approval.
- Preserve the user-owned untracked provenance files.

## Glossary

- LOAD-minted task ID
- activation receipt
- reviewer-fix-only headroom
- scope fence
