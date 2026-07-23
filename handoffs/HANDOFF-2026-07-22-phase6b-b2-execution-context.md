# HANDOFF 2026-07-22 — execute Phase 6B B2 with reduced review/token churn

## Goal

Resume Phase 6B after completed B1 and, after explicit maintainer approval,
execute B2 only: lifecycle state validation plus the host-neutral
`start | append | finish | validate` CLI, task UUID creation, delegation and
handoff/resume linkage, completion-only behavior, and disable/downgrade
semantics. Stop after B2; B3 requires separate approval.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop` with the software-development Domain Pack. Use the
Phase 6B per-slice review protocol and the B2 token-economy controls recorded
below.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3`.
- HEAD: `9e89b7c7c3a36c5c33e33bec284d8a11ad65bd28`.
- HEAD tree: `2403265cf24a8ec35f91180879dd0dca9f8980d8`.
- Upstream state when this handoff was written: ahead of
  `origin/feature/telemetry-v3` by 13 commits.
- The tracked tree is clean before this handoff. The following pre-existing,
  user-owned untracked provenance files must be preserved and left untouched:
  - `handoffs/HANDOFF-2026-07-21-review-economy-claude-audit.md`
  - `handoffs/HANDOFF-2026-07-21-review-economy-stage-a-plan.md`
  - `handoffs/HANDOFF-2026-07-22-review-economy-stage-a-plan-v2.md`
  - `plans/PLAN-review-economy-v2.md`
  - `plans/PLAN-review-economy-v3-measure-first.md`
- This handoff itself is uncommitted when first written.

## State

- DONE:
  1. Phase 6A and Phase 6B B0 were completed before this context; do not redo
     or rediscover them.
  2. B1 product candidate:
     `049c3ce63434cc18e25c5882c7f823ad6b1f7100`, tree
     `772879e34ff3f5e7335e5c92df430556204f3d21`.
  3. B1 reviewed closure:
     `624119ee2f90a7ce37c67700a0637a46e22008bd`, tree
     `436773041efae09d7999db79aee05b3b8792ffe1`.
  4. B1 closure receipt is current HEAD `9e89b7c7c3a36c5c33e33bec284d8a11ad65bd28`.
     Final B1 verdicts were QA `PHASE DONE`, code `APPROVE`, security
     `APPROVE`, final regression QA `PHASE DONE`.
  5. An independent B2 plan review returned `REVISE`. Its four blockers were
     incorporated into the plan below: completion-only cardinality, generic
     closed `append` coverage including gate/review events, explicit error
     semantics, and retention of the 50–80k/70% budget controls. No plan-review
     blocker remains in the revised draft.
- IN PROGRESS:
  1. B2 execution approval. The revised combined B2/token-economy plan is
     ready, but product implementation has not started. Treat a direct command
     in the new session to “approve/run B2 from this handoff” as explicit
     approval; otherwise obtain approval before editing product files.
- NOT STARTED:
  1. B2 observation pre-registration.
  2. B2 tests, lifecycle implementation, CLI implementation, gates, reviews,
     closure ledger, and scorecard.
  3. B3 integrations and five named producers. B3 is out of scope and must not
     start without separate approval.

## Decisions in effect

- `spec/08-decisions.md`: none; this repository has no such file.
- B2 product boundary: modify `scripts/telemetry.py`, create
  `scripts/tests/test_telemetry_cli.py`, and create/update
  `docs/spikes/phase-6b/b2-observation.md`; append
  `benchmarks/scorecard.jsonl` only during closure.
- Do not modify `telemetry/schema-v3.json`, engine/domain/skills/hooks/host
  adapters, exports, or reports in B2.
- B2 exposes the primitive required by later producers but does not wire those
  producers. Fixed CLI producer policy/revision is layered over the existing
  `ProducerWriter.append` surface; it is not a breaking replacement.
- Normal lifecycle: exactly one original `task_started` followed by exactly
  one original `task_finished`; no original event after finish.
- Completion-only degraded lifecycle is the sole exception: exactly one
  original `task_finished`, no `task_started`, and finish-time task-ID minting
  with partial coverage reason `completion_only`.
- `append` accepts the schema-defined closed lifecycle set needed by later
  producers, including handoff/resume/delegation, `gate_result`, and
  `review_result`; it must not accept arbitrary event shapes or caller-owned
  authority metadata.
- One observation task ID covers the whole B2 slice. Internal commits are not
  separate observation units.

## Files touched

- `handoffs/HANDOFF-2026-07-22-phase6b-b2-execution-context.md` → this new,
  uncommitted execution context.
- B2 product/test/report files → none touched; B2 has not started.
- Pre-existing user-owned untracked files listed under Git state → unchanged.

## Verified gates

- Last reviewed B1 product/closure result:
  - `python scripts/validate.py`: PASS.
  - `pytest scripts/tests`: `324 passed, 7 skipped`.
  - B1 targeted pytest: `33 passed, 1 skipped`.
  - `bash -n scripts/init.sh`: PASS.
  - `shellcheck scripts/init.sh`: PASS.
  - `git diff --check`: PASS.
- B2 targeted tests: unverified; not created.
- B2 full gates: unverified; B2 has not started.

## Third-party tool risks

`none reported`

## Next steps

1. `git status --short --branch` → verify branch `feature/telemetry-v3`, HEAD
   `9e89b7c`, and only the preserved untracked provenance files plus this
   handoff; do not rediscover the repository.
2. Read root `AGENTS.md`, `docs/agent-workflow.md`,
   `docs/agent-working-rules.md`, relevant entries in
   `lessons-learned/lessons-learned.md`, this handoff, B2 plus standing
   discipline in
   `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md`, and only
   T3.5/T3.6/T3.11 plus the current public surfaces of
   `scripts/telemetry.py`. Do not reload whole plans or repo history.
3. Confirm explicit maintainer approval to run the revised B2 plan. Do not
   edit product files before approval.
4. `docs/spikes/phase-6b/b2-observation.md` → before the first product edit,
   pre-register one task ID, immutable scope, intended paths, reviewer roles,
   threat model, lifecycle state matrix, error/no-mutation matrix, acceptance
   criteria, and invocation-ledger schema.
5. `scripts/tests/test_telemetry_cli.py` → capture the red-before-green receipt,
   then cover:
   - CLI parsing, bounded JSON input, structured output, exit codes, and no
     secret/untrusted-value echo;
   - UUIDv4 start, duplicate start, task identity, normal finish cardinality,
     completion-only finish, and rejection after finish;
   - closed append types, delegation ID uniqueness/fixed parent-child pair/no
     cycles, and handoff/resume same-task/same-ref/one-use matching;
   - exact coverage arrays/reason precedence;
   - disabled no-write success, operational degraded/nonblocking failure, and
     strict malformed/state/corrupt/future-schema rejection without mutation;
   - B1 path, recovery, correction-authority, privacy, and producer-authority
     regressions.
6. `scripts/telemetry.py` → implement the lifecycle state machine and CLI:
   - `start` mints UUIDv4 at caller-invoked LOAD and emits `task_started`;
   - `append --task-id <uuid> --event <type>` validates the closed lifecycle
     type/payload against trusted fixed producer policy;
   - `finish --task-id <uuid>` emits normal finish, while an explicit
     completion-only mode is the sole permitted finish-time minting path;
   - `validate` remains strict and read-only.
7. Apply this exact result matrix:
   - `DAT_KIT_TELEMETRY=off`: exit 0, structured `disabled`, no write;
   - operational producer/storage failure: exit 0, structured `degraded`, no
     corruption or trusted-history rewrite;
   - malformed input, invalid transition, corrupt history, or future schema:
     nonzero, no write/rewrite;
   - `validate` failure: nonzero and read-only.
8. During build, run targeted tests only. Before independent review, perform a
   main-agent adversarial self-check against QA, code, and security charters;
   this self-check is not an independent verdict.
9. At candidate freeze, run the canonical full gates once:
   `python scripts/validate.py`; `pytest scripts/tests`;
   `bash -n scripts/init.sh`; `shellcheck scripts/init.sh`;
   `git diff --check`.
10. Run reviewers sequentially: full QA → full code review → full security
    review → batch each reviewer’s findings into one semantic fix round →
    findings-scoped re-review → final regression QA. Findings-scoped re-review
    must precede final regression. A broader semantic/trigger change restarts
    the applicable full chain on the new candidate.
11. `docs/spikes/phase-6b/b2-observation.md` → record every reviewer invocation
    using the standing ledger schema. Keep reviewer packets at or below about
    2.5 KB and target a clean-chain dispatch proxy below 10–12 KB. Runtime
    tokens remain `unknown` when the provider does not expose them; never
    estimate private reviewer reads.
12. `benchmarks/scorecard.jsonl` → append only after verdicts, run the consuming
    validator, distinguish product candidate/tree from closure/tree and any
    follow-up receipt, then report and stop. Do not begin B3.

Budget and stop controls for steps 4–12:

- Run B2 in a fresh session with a 50–80k total-token slice budget and perform
  the mandatory checkpoint at 70% remaining context. The handoff-producing
  session was already near 58% and must not be used to implement B2.
- Use one full regression at freeze and one after each batched semantic finding
  round, not after every individual finding. Use a 120-second timeout for full
  suites; do not make short-timeout probe runs.
- Soft size target: roughly +300–450 runtime lines and +250–350 test lines.
- Stop and request `REPLAN` before continuing if product/test change approaches
  900 lines, the slice/budget checkpoint is exceeded, schema or B3 wiring is
  required, an unplanned module split is required, or review exposes missing
  architecture outside the pre-approved threat/state/error matrices.
- Do not create orphan `scripts/telemetry_*.py` helper modules merely to stay
  under a line-count target.

## Traps

- B1 consumed 10 reviewer invocations because trust/security architecture was
  discovered after candidate freeze. Pre-register the B2 trust boundary and
  run adversarial self-review before the first independent dispatch.
- B1 reached five semantic product candidates. Batch findings per reviewer and
  stop/replan on architectural expansion instead of consulting reviewers
  repeatedly during design.
- Do not read the full Phase 6B plan when only B2 plus standing discipline is
  needed; that caused duplicate/truncated reads in the prior session.
- Dispatch bytes (`17,345` for B1) measure only prompt material and exclude
  reviewer-private reads/reasoning; do not present them as total token usage.
- `avoidable_under_narrow_rule=0` in B1 does not mean the session was
  efficient; findings were real but could have been prevented by earlier
  threat/state modeling.
- Preserve the five user-owned untracked provenance files. Do not stage,
  modify, delete, or fold them into B2.
- Completion-only is not a normal task with an omitted start: it is the sole
  explicitly degraded path with its own cardinality and partial-coverage label.
- Disabled/nonblocking operational failure must not be confused with malformed
  input, invalid lifecycle state, corrupt history, or future schema; the latter
  remain strict errors.

## Glossary

- B1
- B2
- B3
- product candidate
- closure tree
- completion-only
- observation task ID
- invocation ledger
- dispatch bytes
- findings-scoped re-review
- degraded result
- trusted history
