# HANDOFF 2026-07-23 — Replan B3 subset #1 at the line-budget stop

## Goal

Complete Phase 6B B3 subset #1 only: the build-loop HARVEST producer,
`lesson_candidate_recorded` lifecycle, five-producer status registry,
scorecard integration, tests, and observation ledger. The approved execution
context is
`handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-execution-context.md`.
Work stopped before freeze because the batch reached 469 combined added
product/test lines, triggering D-B3-3's mandatory `STOP + REPLAN` threshold.
Maintainer Dat resolved that stop on 2026-07-23: keep the 469 lines as-is and
raise the subset #1 ceiling to approximately 600 combined added product/test
lines. The remaining headroom is reserved exclusively for reviewer-driven
fixes and their regression tests.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop` with the `software-dev` Domain Pack; `dat-kit:handoff` at
this mandatory stop.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`, created from current `master`.
- HEAD: `1a2cd5423ee5a0600b9fd5a212aa686d2ce5219f`.
- The source handoff recorded older master `d8058ec`; current master differs
  only by commit `1a2cd54` (`docs(handoff): B3 subset #1 execution context for
  Codex`).
- Worktree: dirty with uncommitted B3 files listed below.
- Eight pre-existing user-owned untracked provenance files under `handoffs/`
  and `plans/` remain unmodified, unstaged, and must stay that way.

## State

- DONE:
  1. Loaded the canonical maintainer contract, lessons, approved B3 handoff,
     Telemetry v3 sections T3.1/T3.3.1/T3.5.1/T3.6/T3.9/T3.11/T3.12, B3 plan
     section, build-loop engine, and all six software-dev Domain Pack slots.
  2. Created `feature/telemetry-v3-b3` from current `master`.
  3. Pre-registered observation task
     `01457374-634f-457e-a912-4b44c3c8cc37` before product or test edits.
  4. Captured red-before-green: targeted collection failed because
     `telemetry/producers.py` did not exist.
  5. Implemented the first batched candidate through public
     `TelemetryStore`/`ProducerWriter.append`; no forbidden append, lock,
     strict-tail, or corpus-check internal has a diff.
  6. New targeted tests pass: `16 passed in 0.43s`; adjacent scorecard and
     telemetry selection passes: `98 passed, 4 skipped in 3.21s`.
- IN PROGRESS:
  1. The uncommitted implementation is functionally targeted-green but is not
     frozen, adversarially self-checked, fully gated, committed, reviewed, or
     closure-harvested.
  2. Added product/test line count is 469: `telemetry/producers.py` 216,
     `scripts/tests/test_telemetry_producers.py` 174, and
     `scripts/scorecard.py` +79/-1. The resolved ceiling is approximately 600;
     unused headroom may be consumed only by reviewer-driven fixes and their
     regression tests.
- NOT STARTED:
  1. Freeze and candidate commit without slimming the current implementation.
  2. The canonical full gates exactly once, then adversarial self-check.
  3. Sequential QA → code review → security review and any findings-scoped
     loops.
  4. Observation ledger closure, scorecard skill append, validator rerun,
     five-part report, and mandatory end-of-subset stop.
  5. B3 subsets #2–#5 remain out of scope and must not start.

## Decisions in effect

- D-B3-1: `telemetry/producers.json` is the five-producer planned/active
  registry; active requires an activating receipt event ID.
- D-B3-2: this subset is live scorecard/HARVEST emission; legacy import is B4.
- D-B3-3 (resolved replan, maintainer Dat, 2026-07-23): keep the current 469
  added product/test lines; the subset #1 ceiling is approximately 600. The
  approximately 130 lines of headroom are reserved exclusively for fixes and
  regression tests required by QA, code review, or security review. They may
  not fund feature growth or scope expansion. All other D-B3-3 stop conditions
  remain unchanged.
- D-B3-4: producer code lives in `telemetry/producers.py`; append internals are
  not modified.
- D-B3-5: all producers remain `planned`; synthetic tests and prose cannot
  activate them.
- Session-local auto-decision, recorded in
  `docs/spikes/phase-6b/b3-observation.md`: validate the producer registry at
  the narrowest existing owner without a second registry or schema.
- No new unrecorded decision exists.

## Files touched

- `docs/spikes/phase-6b/b3-observation.md` → uncommitted pre-registration,
  threat model, acceptance criteria, and ledger schema.
- `telemetry/producers.py` → uncommitted producer helper, closed locus
  classification, lifecycle emission, registry validation, and degraded/
  disabled results.
- `telemetry/producers.json` → uncommitted five-entry registry; all entries
  are `planned` with null event IDs.
- `scripts/scorecard.py` → uncommitted scorecard-to-HARVEST seam and CLI locus/
  reference inputs.
- `scripts/tests/test_telemetry_producers.py` → uncommitted 16-case producer,
  lifecycle, classification, stable-ref, disable, degraded, and registry
  coverage.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-replan-line-budget.md` →
  this uncommitted mandatory-stop record.
- `scripts/telemetry.py` → untouched; `git diff -- scripts/telemetry.py` is
  empty.

## Verified gates

- Red receipt:
  `pytest scripts/tests/test_telemetry_producers.py -q` → collection error,
  missing `telemetry/producers.py`.
- Targeted green:
  `pytest scripts/tests/test_telemetry_producers.py -q` →
  `16 passed in 0.43s`.
- Adjacent regression:
  `pytest` on producer, scorecard append, telemetry CLI/runtime/contract files
  → `98 passed, 4 skipped in 3.21s`.
- `python scripts/validate.py` → unverified; freeze not reached.
- `pytest scripts/tests` → unverified; freeze not reached.
- `bash -n scripts/init.sh` → unverified; freeze not reached.
- `shellcheck scripts/init.sh` → unverified; freeze not reached.
- `git diff --check` → PASS.
- Independent QA/code/security verdicts → unverified; dispatch is forbidden
  until the replan and frozen candidate.

## Third-party tool risks

none reported

## Next steps

1. Freeze the current 469-line candidate without slimming or feature growth,
   stage only the B3 subset #1 paths, and commit it.
2. Run the canonical full gates exactly once:
   `python scripts/validate.py`;
   `pytest scripts/tests`;
   `bash -n scripts/init.sh`;
   `shellcheck scripts/init.sh`;
   `git diff --check`.
3. Perform the adversarial self-check and dispatch
   sequential QA → code review → security review with scoped packets and the
   executable paths named up front.
4. After all verdicts exist, append the observation ledger and scorecard,
   rerun the consuming validator, print the five-part report, and stop before
   B3 subset #2.

## Traps

- D-B3-3 was resolved at 469 lines. The approximately 600-line ceiling remains
  binding, and all unused headroom is reviewer-fix-only.
- Never edit `_WRITE_LOCK`, `_append_local_event`,
  `ProducerWriter._append`, or locked/strict-tail/corpus-check internals.
- The producer must stay `planned`; tests are synthetic receipts.
- HARVEST-only build-loop coverage is `partial`, never `full`.
- Scorecard history must be validated again after the closure append.
- Reviewer dispatches are sequential and diff-scoped; packet budget scales
  with finding count.
- The eight protected untracked provenance files are user-owned.

## Glossary

- B3 subset #1
- producer status registry
- activation receipt
- scope fence
