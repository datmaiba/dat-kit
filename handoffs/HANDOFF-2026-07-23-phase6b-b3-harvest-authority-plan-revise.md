# HANDOFF 2026-07-23 — Harvest authority prerequisite plan requires redesign

## Goal

Prepare a prerequisite plan that can close B3 subset #1's security findings:
authenticated lesson-receipt provenance and trusted LOAD-bound completion
authority. Independent plan review returned `REVISE` with seven BLOCKERs and
two WARNs. No prerequisite implementation is authorized.

Maintainer Dat selected option A on 2026-07-23: do not build the capability
broker or authority ledger now. Prepare a bounded Class C deferment amendment
that removes the unsafe live CLI authority, keeps the producer `planned`, and
permits live emission only after a separately approved Host Adapter supplies a
trusted LOAD-bound context and producer-owned resolver.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop` PLAN phase with independent `plan-reviewer`;
`dat-kit:handoff` at the mandatory plan-revision stop.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- HEAD: `b091a3e`.
- Product/reviewer-fix commits remain unchanged.
- Uncommitted planning records:
  `plans/PLAN-phase6b-b3-harvest-authority-prerequisite.md`,
  updated security-authority handoff, and this handoff.
- Eight pre-existing user-owned untracked provenance files remain untouched.

## State

- DONE:
  1. B3 subset #1 candidate chain reached QA `PHASE DONE` and code
     `APPROVE`.
  2. Full security review returned HIGH receipt-provenance and MEDIUM task-
     completion-authority findings.
  3. Maintainer approved pausing subset #1 and preparing a prerequisite plan.
  4. Draft plan proposed a LOAD-minted one-use capability, producer-owned
     authority/receipt ledger, receipt-derived stable refs, removal of raw
     task/ref CLI authority, red security tests, and Class C governance.
  5. Independent plan reviewer completed a cold audit and returned `REVISE`.
- IN PROGRESS:
  1. Rewrite the draft as the selected bounded Class C deferment plan.
  2. BLOCKER: Class C authorization lacks an exact proposal hash,
     effective-from-run boundary, required dual-domain reviews,
     cross-component regression, and rollback rehearsal.
  2. BLOCKER: a new exact Class C authority path conflicts with the existing
     Class B `telemetry/**` ownership glob; the exact registry transformation
     and ambiguity tests are unspecified.
  3. BLOCKER: no public T3.8-safe append surface can write the new ledger.
     Current choices are forbidden private-internal refactoring or forbidden
     weaker duplication; the conditional stop is already reached.
  4. BLOCKER: no concrete, portable LOAD→HARVEST capability transport owns
     issuance, trust root, Windows/POSIX delivery, lifetime, closure, and
     non-echo behavior.
  5. BLOCKER: receipt → lesson → finish → consume ordering is not retryable
     after a crash following finish. Durable states, idempotency IDs, every
     crash boundary, and double-spend serialization are undefined.
  6. BLOCKER: receipt field types, canonical hash preimages, domain
     separation, receipt-ID uniqueness, and trusted determination of
     root-cause/candidate bindings are unspecified; hashing caller-shaped
     inputs repeats the original provenance flaw.
  7. BLOCKER: this architecture cannot reuse B3 observation ID/budget; it
     requires its own task ID, pre-registration, and exact numeric budget.
  8. WARN: require full gates after every finding fix, unconditional final
     regression QA, and validator reruns after every closure append.
  9. WARN: add closed-record, duplicate-transition, link/replacement,
     short-write/fsync, simultaneous replay, and secret-nonappearance tests.
- NOT STARTED:
  1. Revised option-A plan with the applicable blockers closed or rendered
     explicitly not applicable by removing the proposed ledger/capability
     architecture.
  3. Second independent plan review and explicit implementation approval.
  4. Any prerequisite code, B3 subset #1 security re-review, or closure.

## Decisions in effect

- B3 subset #1 remains paused and `planned`; no security closure exists.
- No live producer may activate from the current candidate, tests, prose, or
  namespace-shaped hashes.
- Maintainer approved planning only, not a new ledger, capability system,
  registry split, append refactor, schema change, or cross-subset build.
- Architecture direction (maintainer Dat, 2026-07-23): option A. Defer live
  emission, remove unsafe CLI authority, keep the producer planned, and do not
  add the proposed ledger/broker/append architecture.
- D-B3-3 scope fence remains binding.

## Files touched

- `plans/PLAN-phase6b-b3-harvest-authority-prerequisite.md` → uncommitted draft;
  plan-review verdict `REVISE`.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-security-authority-replan.md`
  → uncommitted direction record updated with planning-only approval.
- `handoffs/HANDOFF-2026-07-23-phase6b-b3-harvest-authority-plan-revise.md` →
  this uncommitted stop record.
- Product/test files → unchanged since committed `b091a3e`.

## Verified gates

- No code changed during prerequisite planning; no new mechanical gate was
  required.
- Latest product evidence:
  - freeze validator PASS;
  - pytest `375 passed, 8 skipped`;
  - Bash/ShellCheck/diff check PASS;
  - focused reviewer-fix regression `39 passed, 2 skipped`;
  - QA `PHASE DONE`;
  - code review `APPROVE`;
  - security review `RETURN TO BUILDER`.
- Plan review → `REVISE`, seven BLOCKERs and two WARNs.

## Third-party tool risks

none reported

## Next steps

1. Obtain maintainer direction. Recommended: formally stop B3 subset #1 as
   security-blocked/planned and open a separate Class C “trusted telemetry
   authority” architecture task with a fresh observation ID and budget.
2. In that separate task, decide the trust root and portable capability
   transport before selecting storage or code paths.
3. Decide whether to extract a reusable public T3.8-safe append abstraction.
   This is locked-append/concurrency architecture and requires explicit
   Fable-5-tier authorization plus rollback design.
4. Specify the exact Class C registry split, authority state machine,
   idempotency/crash table, canonical receipt preimages, and producer-owned
   source of candidate bindings.
5. Draft the exact amendment/proposal record, obtain both required independent
   reviews, bind approval to the proposal hash/effective run, then rerun
   plan-reviewer.
6. Resume B3 subset #1 only after the prerequisite is implemented, gated,
   reviewed, and handed off with a trusted interface.

## Traps

- Do not treat “prepare a plan” as approval to implement Class C architecture.
- Do not hide an exact Class C path under the Class B `telemetry/**` glob.
- Do not duplicate private safe-append logic.
- Do not claim stdin/handle is a capability transport without an owning host
  lifecycle and Windows/POSIX contract.
- Do not make pre-CONSUME crash states “retryable” when lifecycle finish is
  already terminal.
- Do not hash caller-shaped prose and call it producer provenance.
- Do not reuse the existing B3 observation or reviewer-fix budget.

## Glossary

- Class C proposal hash
- trust root
- authority ledger
- idempotency state machine
- producer-owned binding
- T3.8-safe append surface
