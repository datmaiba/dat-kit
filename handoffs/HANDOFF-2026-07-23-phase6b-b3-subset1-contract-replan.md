# HANDOFF 2026-07-23 — Replan B3 subset #1 task identity and receipt truthfulness

## Goal

Complete Phase 6B B3 subset #1 only: the build-loop HARVEST producer,
`lesson_candidate_recorded`, five-producer status registry, scorecard
integration, tests, and observation ledger. Independent code review found
that the approved subset shape cannot satisfy Telemetry v3 T3.6 without
task-identity wiring that belongs to another subset. D-B3-3 therefore requires
`STOP + REPLAN` before security review or closure.

Maintainer Dat resolved this stop on 2026-07-23 by approving the recommended
amendment: subset #1 emits only when the caller supplies an existing
LOAD-minted task ID and real producer-owned root-cause/candidate receipts. A
scorecard append with no candidate emits no telemetry. Task-start/LOAD
integration and activation remain deferred to their separately approved
subset.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop` with the `software-dev` Domain Pack; sequential QA then
code review; `dat-kit:handoff` at this mandatory stop.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- HEAD: `141e87c` (`fix(telemetry): restrict harvest evidence refs`).
- Frozen product candidate: `4bd5715`
  (`feat(telemetry): add build-loop harvest producer`).
- Worktree before this handoff: clean except the eight pre-existing,
  user-owned untracked provenance files under `handoffs/` and `plans/`.
- This handoff is new and uncommitted.

## State

- DONE:
  1. D-B3-3 line-budget replan recorded as resolved: ceiling approximately
     600, reviewer-fix-only headroom.
  2. Candidate `4bd5715` committed with 469 combined added product/test lines.
  3. Full freeze gates passed once: validator PASS; pytest `375 passed,
     8 skipped`; Bash syntax PASS; ShellCheck PASS; diff check PASS.
  4. Adversarial builder self-check passed the declared scope fence,
     planned-status, partial-coverage, disable, degraded, and locus checks.
  5. QA returned one finding: grammar-valid prose could pass as an evidence
     reference.
  6. QA-1 fixed in `141e87c` with closed SHA-256 evidence namespaces and two
     regression cases. Targeted suite: `18 passed`; combined added
     product/test lines: 476.
  7. Findings-scoped QA re-review: 6 checks passed; `PHASE DONE`.
  8. Full code review completed and returned `RETURN TO BUILDER`.
- IN PROGRESS:
  1. Reviewer-driven implementation of the approved replan and all three
     code-review findings.
- NOT STARTED:
  1. Findings-scoped code re-review after the approved fix.
  2. Security review; it must not run before code review approves.
  3. Observation ledger closure, scorecard append, validator rerun, five-part
     report, and end-of-subset stop.
  4. B3 subsets #2–#5 remain unauthorized.

## Decisions in effect

- D-B3-1: `telemetry/producers.json` is the five-producer planned/active
  registry; active requires a real activating receipt event ID.
- D-B3-2: subset #1 is the live scorecard/HARVEST producer; B4 legacy import is
  excluded.
- D-B3-3 resolved line rule: ceiling approximately 600; unused headroom is
  reviewer-fix-only. Stop for new architecture, schema change, locked-append
  changes, or another subset's wiring.
- D-B3-4: producer code remains in `telemetry/producers.py`; public writer
  surfaces only.
- D-B3-5: all producers remain `planned`; synthetic evidence cannot activate.
- Contract replan (maintainer Dat, 2026-07-23): subset #1 requires an existing
  LOAD-minted task ID plus real producer-owned lesson receipts; no candidate
  means no telemetry event. Task-start/LOAD integration and activation remain
  deferred. This replaces the earlier requirement that the helper mint and
  drive its own start event.

## Files touched

- `docs/spikes/phase-6b/b3-observation.md` → committed observation
  pre-registration; closure ledger not appended.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-replan-line-budget.md` →
  committed resolved line-budget decision.
- `scripts/scorecard.py` → committed scorecard-to-HARVEST seam; implicated by
  the task-ID and manufactured-candidate findings.
- `scripts/tests/test_telemetry_producers.py` → committed producer tests plus
  QA-1 regression coverage.
- `telemetry/producers.json` → committed; all five entries remain `planned`.
- `telemetry/producers.py` → committed helper and QA-1 namespace hardening;
  implicated by all three code-review findings.
- `scripts/telemetry.py` → untouched; the hard scope fence remains intact.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-contract-replan.md` → this
  uncommitted mandatory-stop record.

## Verified gates

- Freeze candidate `4bd5715`:
  - `python scripts/validate.py` → PASS.
  - `pytest scripts/tests` → `375 passed, 8 skipped in 32.54s`.
  - `bash -n scripts/init.sh` → PASS.
  - `shellcheck scripts/init.sh` → PASS.
  - `git diff --check` → PASS.
- QA-1 fix candidate `141e87c`:
  - `pytest scripts/tests/test_telemetry_producers.py -q` →
    `18 passed in 0.39s`.
  - Independent findings-scoped QA → 6 checks passed; `PHASE DONE`.
- Independent full code review → `RETURN TO BUILDER` with two P1 findings and
  one P2 finding.
- Security review → unverified and intentionally not dispatched.

## Third-party tool risks

none reported

## Next steps

1. Fix the two P1 findings under the approved amendment and make
   active-registry validation
   bind the event ID to a validated producer event/revision.
2. Run only directly affected regression tests, commit the reviewer-driven
   fix, and send the three findings to the same code reviewer for a
   findings-scoped re-review.
3. After code `APPROVE`, run full security review, then complete the observation
   ledger, scorecard append, validator rerun, five-part report, and mandatory
   stop before subset #2.

## Traps

- A UUID-shaped value is not proof of a real activation receipt.
- HARVEST cannot mint the task identity that T3.6 says was minted at LOAD.
- A scorecard record is not automatically a lesson/root-cause receipt.
- Fixing task identity by adding LOAD/handoff wiring crosses the approved
  subset boundary and triggers D-B3-3.
- Do not dispatch security review on a code-review-red candidate.
- Do not consume reviewer-fix headroom for feature growth.
- Preserve the eight user-owned untracked provenance files.

## Glossary

- B3 subset #1
- producer status registry
- activation receipt
- LOAD-minted task ID
- scope fence
