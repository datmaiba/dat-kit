# HANDOFF 2026-07-23 — B3 option-A deferment plan is review-ready

## Goal

Implement the maintainer-selected option A for B3 subset #1: a Class C
contract deferment followed, only after its effective run, by Class B removal
of unsafe live scorecard/HARVEST authority. The independent plan reviewer
returned `APPROVE`; implementation still awaits explicit maintainer approval.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop` PLAN phase with full independent plan review;
`dat-kit:handoff` at the mandatory implementation approval gate.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- HEAD: `b091a3e`.
- Product candidate remains security-red but code-review-approved.
- Uncommitted planning records include the revised plan and the post-security
  handoffs; no option-A product or contract edit has started.
- Eight pre-existing user-owned untracked provenance files remain untouched.

## State

- DONE:
  1. Maintainer selected option A: no ledger, broker, capability transport,
     Host Adapter, append refactor, or live producer activation.
  2. Plan v1 received `REVISE` with seven BLOCKERs and two WARNs.
  3. Plan v2 removes the proposed architecture and splits governance:
     - Slice C: contract-only Class C deferment under
       `platform-contract-policy/1`;
     - Slice B: post-effective, net-negative runtime/test cleanup under
       maintainer policy.
  4. Fresh observation IDs and exact budgets are fixed:
     - Slice C `526b37e7-12ff-4c2d-8346-1d7b94b364cc`, at most 250 added
       contract/evidence lines, no committed test changes;
     - Slice B `a0c67829-f505-4d40-9995-464db4a4f9f0`, at most 120 added
       product/test lines and net-negative against `b091a3e`.
  5. Class C process binds an immutable exact patch/post-apply hash,
     deterministic proposal ID, current policy hash, two independent reviews,
     cross-component regression, rollback rehearsal, platform-owner decision,
     and `effective_from_run`.
  6. Temporary Slice C negative fixtures are uncommitted and non-decisive;
     durable guards are governance-routed to Slice B.
  7. Findings-scoped plan re-review returned `APPROVE`, no findings.
- IN PROGRESS:
  1. Mandatory maintainer implementation approval gate.
- NOT STARTED:
  1. Slice C pre-registration, immutable baseline, candidate patch, and
     proposal.
  2. Class C reviews/gates/rollback/owner decision/effective run.
  3. Slice B pre-registration and net-negative cleanup.
  4. QA/code/security/final-QA chain and closure.

## Decisions in effect

- Option A selected by maintainer Dat on 2026-07-23.
- No live emission or activation is authorized.
- No new storage, schema field, capability, resolver, Host Adapter, or append
  architecture is authorized.
- Slice B cannot start before Slice C's approved decision is effective.
- The reviewed plan is
  `plans/PLAN-phase6b-b3-harvest-authority-prerequisite.md`.

## Files touched

- `plans/PLAN-phase6b-b3-harvest-authority-prerequisite.md` → uncommitted
  reviewed plan v2; plan-reviewer `APPROVE`.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-security-authority-replan.md`
  → uncommitted planning-direction record.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-harvest-authority-plan-revise.md` →
  uncommitted plan-v1 review record and option-A decision.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-deferment-plan-review-ready.md` →
  this uncommitted approval-gate record.
- Product/contract files → unchanged since `b091a3e`.

## Verified gates

- Plan review round 1 → `REVISE`, seven BLOCKERs and two WARNs.
- Findings-scoped plan re-review round 2 → `REVISE`, one routing BLOCKER.
- Final findings-scoped plan re-review → `APPROVE`, no findings.
- No implementation gate run was needed because option-A product/contract
  files have not changed.
- Latest product evidence remains:
  validator PASS; pytest `375 passed, 8 skipped`; Bash/ShellCheck/diff PASS;
  focused `39 passed, 2 skipped`; QA `PHASE DONE`; code `APPROVE`; security
  `RETURN TO BUILDER`.

## Third-party tool risks

none reported

## Next steps

1. Obtain explicit maintainer approval to implement the reviewed option-A plan.
2. After approval, create the Slice C observation before the first contract or
   committed evidence edit.
3. Execute Slice C only through its Class C decision/effective-run gate.
4. Start Slice B only after that gate, with its own observation and budget.
5. End with all producers planned, unsafe authority removed, closure evidence
   appended and validators rerun; do not start B3 subset #2.

## Traps

- Selecting option A did not itself approve implementation.
- The Class C proposal affects only `docs/contracts/telemetry-v3.md`.
- Slice C commits no `scripts/tests/**` changes.
- Temporary candidate tests cannot approve their own proposal.
- Do not start Slice B before `effective_from_run`.
- Do not activate any producer.
- Preserve the user-owned untracked provenance files.

## Glossary

- option-A deferment
- contract-only Slice C
- post-effective Slice B
- effective-from-run
- net-negative cleanup
