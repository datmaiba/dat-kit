# HANDOFF 2026-07-23 — Replan B3 subset #1 producer authority

## Goal

Complete B3 subset #1 without allowing caller-shaped references or raw task
UUIDs to become producer authority. Full security review returned one HIGH and
one MEDIUM finding. Correct closure requires authenticated receipt provenance
and trusted task-completion authority, which are not present in the approved
subset architecture. D-B3-3 requires `STOP + REPLAN`.

Maintainer Dat resolved the immediate direction on 2026-07-23: keep subset #1
paused and prepare a prerequisite plan for trusted LOAD-bound task context and
authenticated receipt evidence before resuming the live producer. This
authorizes planning only; implementation still requires the reviewed plan's
explicit approval gate.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop`; sequential QA → code review → security review;
`dat-kit:handoff` at this mandatory security-authority stop.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- HEAD: `b091a3e` (`fix(telemetry): preserve harvest task identity`).
- Candidate chain:
  `4bd5715` → QA privacy fix `141e87c` → code-review fix `b091a3e`.
- Worktree before this handoff: clean except eight pre-existing user-owned
  untracked provenance files.
- This handoff is new and uncommitted.

## State

- DONE:
  1. Initial candidate committed and full freeze gates passed once.
  2. QA-1 closed; independent findings-scoped QA returned `PHASE DONE`.
  3. Code review's two P1 and one P2 findings fixed under two explicit
     maintainer replans.
  4. Focused regression on the code-review fix:
     `39 passed, 2 skipped`.
  5. Added product/test size is 625 under the maintainer-approved
     approximately 650 reviewer-fix-only ceiling.
  6. Findings-scoped code re-review returned `APPROVE`.
  7. Full security review completed and returned `RETURN TO BUILDER`.
- IN PROGRESS:
  1. Prerequisite architecture planning for the security HIGH/MEDIUM findings.
  2. Security HIGH: `_require_evidence_ref` proves namespace/shape only.
     Caller-invented 64-hex references can be persisted by the trusted
     producer and later satisfy event-shape activation checks. Closure requires
     authenticated producer-side existence-and-task binding.
  3. Security MEDIUM: possession of a visible task UUID authorizes attaching a
     lesson and finishing that task. Closure requires trusted LOAD/runtime
     identity propagation or a one-time completion capability bound to the
     scorecard completion.
- NOT STARTED:
  1. Independent review and maintainer approval of the prerequisite plan.
  2. Security findings fix and findings-scoped security re-review.
  3. Post-fix regression QA if required by the approved plan.
  4. Observation ledger, scorecard append, validator rerun, five-part report,
     and stop before subset #2.

## Decisions in effect

- D-B3-1/D-B3-5: producer activation requires a validated real receipt; all
  committed statuses remain `planned`.
- D-B3-3: approximately 650 combined added product/test lines, with every line
  above 469 reviewer-fix/regression-only. Stop for new architecture, authority,
  schema, append internals, or another subset's wiring.
- D-B3-4: public writer surfaces only; locked append/strict-tail/corpus-check
  internals remain untouched.
- Approved task-identity replan: reuse an existing LOAD-minted task; no
  candidate inputs means no event; LOAD/start integration remains deferred.
- No decision authorizes a new receipt resolver, completion capability, or
  cross-subset trusted context.
- Direction decision (maintainer Dat, 2026-07-23): pause subset #1 and prepare
  the trusted-context/authenticated-receipt prerequisite plan. Planning is
  authorized; implementation is not yet authorized.

## Files touched

- `telemetry/producers.py` → committed helper, receipt namespace checks,
  existing-task validation, and active-event binding; implicated by both
  security findings.
- `scripts/scorecard.py` → committed CLI seam accepting task ID and receipt
  inputs; implicated by raw-UUID completion authority.
- `scripts/tests/test_telemetry_producers.py` → committed regression suite.
- `telemetry/producers.json` → committed; all five producers remain planned.
- `docs/spikes/phase-6b/b3-observation.md` → committed pre-registration;
  closure ledger not appended.
- Four prior B3 handoff/decision records → committed.
- `scripts/telemetry.py` → untouched.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-security-authority-replan.md`
  → this uncommitted mandatory-stop record.

## Verified gates

- Freeze `4bd5715`:
  - validator PASS;
  - pytest `375 passed, 8 skipped`;
  - Bash syntax PASS;
  - ShellCheck PASS;
  - diff check PASS.
- QA privacy fix `141e87c`:
  - targeted `18 passed`;
  - findings-scoped independent QA: 6 checks passed; `PHASE DONE`.
- Code-review fix `b091a3e`:
  - focused `39 passed, 2 skipped`;
  - findings-scoped code review: `APPROVE`.
- Full security review on `b091a3e`:
  - HIGH: producer-owned reference provenance is not authenticated;
  - MEDIUM: raw task UUID is treated as completion authority;
  - verdict `RETURN TO BUILDER`.

## Third-party tool risks

none reported

## Next steps

1. Draft and independently review the prerequisite plan. It must remove
   caller-supplied CLI authority, define the LOAD-to-HARVEST trust boundary,
   bind root-cause/candidate receipts to the task, and state whether schema or
   storage changes are required.
2. Present the reviewed plan and stop for explicit maintainer implementation
   approval.
3. If architecture expansion is approved, revise the line ceiling before
   implementation; only approximately 25 product/test lines remain.
4. Implement red-before-green security regressions, commit the fix, and send
   only the HIGH/MEDIUM findings to the same security reviewer.
5. After security `APPROVE`, run required regression QA, then complete
   observation and scorecard closure.

## Traps

- A namespace-shaped hash is not authenticated producer ownership.
- A task UUID is correlation data, not mutation/completion authority.
- Event validity does not prove the referenced artifact exists or belongs to
  the task.
- Correct closure likely crosses the task-lifecycle subset boundary.
- Do not place resolver logic in locked append internals.
- Do not dispatch observation/scorecard closure while security is red.
- Preserve the eight user-owned untracked provenance files.

## Glossary

- producer authority
- authenticated receipt resolver
- completion capability
- LOAD-bound task identity
- activation receipt
