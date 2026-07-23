# HANDOFF 2026-07-22 — Phase 6B B2 stopped at the pre-registered REPLAN threshold

## Goal

Complete Phase 6B B2 only: lifecycle-state validation and the host-neutral
`start | append | finish | validate` CLI, UUID task identity, delegation and
handoff/resume linkage, completion-only behavior, and disable/downgrade
semantics. B3 remains out of scope and requires separate approval.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop` with the software-development Domain Pack, the approved
B2 token-economy controls, and `dat-kit:handoff` at the mandatory stop.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3`.
- HEAD: `258236a19093814f88469456d8426f8cc42a42b2`.
- HEAD tree: `42b41988233fbcca398d36daae9f549672b94afe`.
- Tracked tree was clean before this handoff was created.
- This handoff is uncommitted when first written.
- Preserve and do not stage, modify, delete, or fold in these pre-existing
  user-owned untracked files:
  - `handoffs/HANDOFF-2026-07-21-review-economy-claude-audit.md`
  - `handoffs/HANDOFF-2026-07-21-review-economy-stage-a-plan.md`
  - `handoffs/HANDOFF-2026-07-22-phase6b-b2-execution-context.md`
  - `handoffs/HANDOFF-2026-07-22-review-economy-stage-a-plan-v2.md`
  - `plans/PLAN-review-economy-v2.md`
  - `plans/PLAN-review-economy-v3-measure-first.md`

## State

- DONE:
  1. B2 observation task `8227f7f9-5b3c-42ec-b351-4bc6c1fb5954` was
     pre-registered before the first product edit.
  2. Initial B2 candidate commit:
     `119800aab463a897235d45195b7755e29e6aaf16`, tree
     `0886b0ee398cd78738fb56338897d116053e30ce`.
  3. Code-review fix candidate/current HEAD:
     `258236a19093814f88469456d8426f8cc42a42b2`, tree
     `42b41988233fbcca398d36daae9f549672b94afe`.
  4. Independent QA on the initial candidate returned `PHASE DONE` after
     environment-path retries. Code review found three issues; all were fixed
     in `258236a` and findings-scoped re-review returned `APPROVE`.
  5. Full mechanical regression on `258236a` is green.
- IN PROGRESS:
  1. B2 security closure. Full security review on `258236a` returned
     `RETURN TO BUILDER` with one HIGH and two MEDIUM findings listed below.
  2. Product/test diff from the approved base is already 847 added lines
     (`scripts/telemetry.py`: 507 additions/9 deletions;
     `scripts/tests/test_telemetry_cli.py`: 340 additions). The required
     security fix would cross the pre-registered “approaches 900 lines” stop.
     No security-fix product edit has been made.
- NOT STARTED:
  1. A maintainer-approved revised B2 continuation plan/line budget.
  2. Security finding fixes and tests.
  3. Findings-scoped security re-review.
  4. Final regression QA on the security-approved candidate.
  5. Observation closure append, scorecard append/validation, closure receipt,
     and B2 completion report.
  6. B3. Do not begin it without separate approval.

## Decisions in effect

- `spec/08-decisions.md`: none; this repository has no such file.
- The approved B2 decisions in
  `handoffs/HANDOFF-2026-07-22-phase6b-b2-execution-context.md` remain in force.
- CLI completion-only minting keeps its fixed `completion_only` reason; strict
  corpus validation also accepts higher-precedence evidence such as T3.11
  `telemetry_disabled` imports.
- No new architecture, schema, public authority, module split, or B3 wiring is
  authorized by this handoff.

## Files touched

- `docs/spikes/phase-6b/b2-observation.md` → committed B2 pre-registration and
  pre-freeze receipts; post-review ledger/closure is not appended yet.
- `scripts/telemetry.py` → committed B2 lifecycle validator and CLI plus the
  closed code-review fixes; open security findings remain.
- `scripts/tests/test_telemetry_cli.py` → committed B2 tests plus code-review
  regression cases; security finding cases are not added.
- `benchmarks/scorecard.jsonl` → unchanged; HARVEST has not run because B2 is
  not review-closed.
- `handoffs/HANDOFF-2026-07-22-phase6b-b2-replan-required.md` → this new,
  uncommitted resume record.

## Verified gates

- Targeted telemetry after the code-review fixes: `56 passed, 1 skipped`.
- `python scripts/validate.py`: PASS (`✓ all checks green`).
- `pytest scripts/tests`: `338 passed, 7 skipped in 25.87s`.
- `bash -n scripts/init.sh`: PASS.
- `shellcheck scripts/init.sh`: PASS.
- `git diff --check`: PASS.
- QA: `PHASE DONE` on `119800a`.
- Code review: `APPROVE` on `258236a` after findings 1–3 closed.
- Security review: `RETURN TO BUILDER` on `258236a`:
  1. HIGH — lifecycle validation occurs before, not inside, the writer lock;
     concurrent finishes/resumes can validate one stale snapshot, and the CLI
     path can recover a newly raced interrupted tail instead of rejecting it.
  2. MEDIUM — lifecycle dereferences payload fields before closed payload
     validation; `KeyError`, `TypeError`, or JSON `RecursionError` can escape
     structured CLI errors.
  3. MEDIUM — read-only validation checks `Path.exists()` before `lstat`, so a
     dangling link-like `telemetry/` parent can be reported as an empty corpus.
- Final regression QA on a security-approved candidate: unverified.

### Reviewer invocation ledger

Runtime input/output tokens and elapsed time were not exposed and remain
`unknown`. Dispatch bytes are exact UTF-8 byte counts of supplied packets and
exclude reviewer-private reads/reasoning.

```text
task | ordinal | role | from candidate/tree | to candidate/closure tree | full/findings-scoped | restart_of_ordinal | restart cause | trigger/finding IDs | verdict | elapsed if known | runtime input/output tokens or unknown | dispatch bytes | invalidation reason or none | avoidable_under_narrow_rule yes/no + reason
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 1 | qa | 119800a/0886b0e | 119800a/0886b0e | full | none | none | B2-QA | RETURN TO BUILDER | unknown | unknown | 1582 | none | no — initial QA is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 2 | qa | 119800a/0886b0e | 119800a/0886b0e | full | 1 | pytest PATH correction | B2-QA | interrupted/no verdict | unknown | unknown | 653 | invocation exceeded the 120-second ceiling and was stopped | no — mandatory QA restart
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 3 | qa | 119800a/0886b0e | 119800a/0886b0e | full | 2 | bounded timeout restart | B2-QA | RETURN TO BUILDER | unknown | unknown | 840 | shellcheck executable access denied | no — mandatory QA restart
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 4 | qa | 119800a/0886b0e | 119800a/0886b0e | findings-scoped | 3 | resolved shellcheck path | B2-QA-ENV | PHASE DONE | unknown | unknown | 529 | none | no — required gate closure
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 5 | code | 119800a/0886b0e | 119800a/0886b0e | full | none | none | C1,C2,C3 | RETURN TO BUILDER | unknown | unknown | 1581 | none | no — initial code review is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 6 | code | 258236a/42b4198 | 258236a/42b4198 | findings-scoped | 5 | C1–C3 fix commit | C1,C2,C3 | APPROVE | unknown | unknown | 971 | none | no — findings re-review is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 7 | security | 258236a/42b4198 | 258236a/42b4198 | full | none | public-input/path/write triggers | S1,S2,S3 | RETURN TO BUILDER | unknown | unknown | 1754 | none | no — initial security review is never avoidable
```

Total reviewer invocations: 7. Full: 5. Findings-scoped: 2. Exact dispatch
proxy: 7,910 bytes. Avoidable under the pre-registered narrow closure-only
rule: 0. The observation task is incomplete and does not enter the decision
denominator.

## Third-party tool risks

`none reported`

## Next steps

1. Maintainer approval → approve or revise a B2-only continuation plan that
   explicitly raises/replaces the 900-line stop for the three named security
   findings. Do not edit product files before this replan gate.
2. `scripts/tests/test_telemetry_cli.py` → after approval, add red cases for
   locked-snapshot duplicate finish/resume, raced interrupted-tail rejection,
   missing/type-confused/deep payload errors, and dangling link-like parent
   validation.
3. `scripts/telemetry.py` → validate the actual opened corpus plus proposed
   lifecycle event under `_WRITE_LOCK` immediately before mutation; preserve
   B1 recovery for the generic writer while making the CLI lifecycle path
   strict on a raced interrupted tail.
4. `scripts/telemetry.py` → closed-payload validate before lifecycle field
   access, convert parser recursion/input-shape failures to structured strict
   diagnostics, and use `lstat` to distinguish absent from dangling/link-like
   parents.
5. Full gates → run once after the single batched security-fix round.
6. Security reviewer → findings-scoped S1–S3 re-review only.
7. QA reviewer → final regression QA on the security-approved candidate.
8. `docs/spikes/phase-6b/b2-observation.md` and
   `benchmarks/scorecard.jsonl` → append real closure/ledger evidence and the
   scorecard only after verdicts; run the consuming validator afterward.
9. Stop after B2. Do not start B3 without separate approval.

## Traps

- The approved B2 stop is triggered by product/test size, not context
  exhaustion: 847 added lines already approach 900 before the security fix.
- Do not treat the current code-review approval or old QA verdict as security
  closure; final QA must run on the security-approved candidate.
- The generic B1 writer intentionally recovers interrupted tails. The B2 CLI
  path needs a locked strict-tail check without weakening that B1 behavior.
- Validate payload shape before any lifecycle-specific dictionary indexing;
  structured error guarantees include deeply nested JSON/parser failures.
- `Path.exists()` follows links and collapses dangling links into false; path
  safety checks must begin with `lstat`.
- QA review consumed four invocations because executable discovery differed in
  the reviewer sandbox. A resumed packet should name the known Python, Git
  Bash, and ShellCheck executable paths up front.
- Do not append the scorecard before all verdicts, and re-run its validator
  after the append.
- Preserve the six pre-existing user-owned untracked provenance files.

## Glossary

- B2
- B3
- completion-only
- product candidate
- locked snapshot
- strict tail
- invocation ledger
- dispatch bytes
- findings-scoped re-review
- closure tree
