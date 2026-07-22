# HANDOFF 2026-07-22 — review B1, then wait for separate approval

## Goal

Start the next Phase 6B step from the completed B0 governance admission.
First review B1 in
`handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md`, return a short
`KEEP`, `IMPROVE`, or `REPLAN` verdict with blocking defects only, and stop for
maintainer approval. Do not implement B1 in the same approval turn.

B1's bounded outcome is the Telemetry v3 schema/storage vertical slice:
single-writer local append, validation and duplicate-event-ID rejection,
correction linkage with prior-byte preservation, interrupted-append recovery,
and privacy/source-class rejection at the storage boundary.

## Runtime

`codex / GPT-5` (exact minor identifier unavailable).

## Workflow

Use `dat-kit:build-loop` for B1 execution after approval. The approval-review
turn is review-only. B1 is expected to be the first eligible implementation
slice for the plan-v3 token-economy observation, so pre-registration must occur
before implementation work begins.

## Canonical contract

`dat-kit 1.16.0`, root `AGENTS.md`.

## Git state

- Branch: `feature/telemetry-v3`, tracking `origin/feature/telemetry-v3`.
- Baseline HEAD before this context-only commit:
  `84f8362165059e3c937332321d09ad49fa294c0d`
  (`docs(telemetry): close B0 governance admission`).
- Tree: `5515e553e423f41366c93b4febbe73e2da928178`.
- Branch is five commits ahead of origin; nothing from B0 has been pushed.
- Tracked worktree was clean before this context file was created.
- Five older Review Economy provenance artifacts remain intentionally
  untracked; preserve them unless the maintainer explicitly chooses a commit
  scope.
- Rollback rehearsal clone remains at
  `C:\tmp\dat-kit-phase6b-b0-rollback-4eba5b3`.

## State

### DONE

1. Phase 6A contract approval remains closed by
   `decision-f80fa03211e51c3f68c5-0001`.
2. Phase 6B plan v3 was approved and committed at `8c8b4e0`.
3. B0 admitted `telemetry/**` and exact `scripts/telemetry.py` to one owner,
   `telemetry-v3-runtime` / `maintainers` / class B /
   `maintainer-policy/1`.
4. B0 proposal `proposal-27d40cbf7ff8c9cebe93` was approved by
   `decision-27d40cbf7ff8c9cebe93-0001`, effective from
   `run-2026-07-22-phase6b-b0-4eba5b39`.
5. B0 final regression closed at commit `84f8362`; no telemetry runtime or
   event data exists.

### IN PROGRESS

1. B1 plan review and maintainer approval only. No B1 task ID, candidate, or
   product file exists yet.

### NOT STARTED

1. B1 implementation: schema, storage, validation, correction, recovery, and
   privacy/source boundary.
2. B2 lifecycle CLI and task-identity propagation.
3. B3 integrations and five real producer receipts.
4. B4 durable export, retention, and compatibility.
5. B5 observations, RC, CI, rollback, tag, and 2.1.0 closure.
6. Review Economy Stage B; it remains unauthorized.

## Decisions in effect

- PLAN-v7 Phase 6 and §13.2 remain the program scope and Definition of Done.
- Telemetry v3 contract hash remains
  `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde`.
- B0 approval admits ownership only. It does not authorize B1 behavior.
- B1 requires a separate approval after plan review. Plan approval and B1
  implementation must not occur in the same turn.
- B1 is limited to schema/storage primitives. Lifecycle CLI behavior belongs
  to B2; producers to B3; durable export to B4; release closure to B5.
- Every new or changed gate needs a red-before-green receipt.
- Runtime tokens are exact or `unknown`; Codex attribution is currently
  `unknown / unsupported_provider`. Dispatch bytes are context proxies only.
- No `spec/08-decisions.md` exists in this maintainer repo. Approved plans and
  append-only records under `docs/decisions/` are the decision log.

## Files touched

- `registry/evolution.json` → B0 governed root and narrow runtime component.
- `docs/decisions/evolution-proposal-27d40cbf7ff8c9cebe93.proposal.json` →
  immutable B0 Class C proposal.
- `docs/decisions/evolution-manual.decisions.jsonl` → B0 approval append.
- `docs/spikes/phase-6b/b0-governance-baseline.md` → pre-admission paths,
  red receipt, and frozen inputs.
- `docs/spikes/phase-6b/b0-governance-review.md` → candidate, reviews,
  rollback, and authority receipts.
- `scripts/tests/evolution_evidence.py` → shared frozen-Git evidence checks.
- `scripts/tests/test_phase6b_governance.py` → proposal/decision lifecycle
  checks.
- `scripts/tests/test_registry_catalog.py` → positive, boundary, orphan, and
  ambiguity admission tests.
- `scripts/tests/test_telemetry_contract.py` → historical Phase 6A evidence
  now verifies frozen Git blobs instead of the current tree.
- `benchmarks/scorecard.jsonl` → one validated schema-v2 B0 record.
- `handoffs/HANDOFF-2026-07-22-phase6b-b1-plan-approval-context.md` → this
  context-only transition artifact.

No `scripts/telemetry.py`, `telemetry/schema-v3.json`,
`telemetry/events.jsonl`, `benchmarks/telemetry-v3.jsonl`, or
`benchmarks/defects.jsonl` was created by B0.

## Verified gates

Final B0 closure commit `84f8362`, tree `5515e553…`:

- `scripts/validate.py` → PASS.
- `pytest scripts/tests` → `291 passed, 6 skipped`.
- `bash -n scripts/init.sh` → PASS.
- `shellcheck scripts/init.sh` → PASS.
- `git diff --check` → PASS.
- QA → `PHASE DONE` on the final closure tree.
- Software-dev review → `APPROVE` after one findings-scoped re-review.
- Knowledge-work review → `SOURCED`.
- Security review → `APPROVE`, zero findings.
- Rollback rehearsal → validator PASS; `288 passed, 6 skipped`; both runtime
  targets returned to `EVOLUTION_ORPHAN_PATH`; append-only proposal/baseline
  evidence remained present.
- Final runtime-absence attack → PASS: neither `scripts/telemetry.py` nor the
  `telemetry/` root exists.

B1 product tests and observation ledger are unverified because B1 has not
started.

## Third-party tool risks

None reported. No installer or external plugin ran.

## Next steps

1. Read root `AGENTS.md`, this context, and only the B1 plus standing-discipline
   sections of
   `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md`; return
   `KEEP`, `IMPROVE`, or `REPLAN`, then wait for explicit maintainer approval.
2. After approval, invoke `dat-kit:build-loop` for B1 only and pre-register the
   observation task ID, immutable slice scope, exact intended paths, reviewer
   roles, and security-trigger decision before editing.
3. Implement the smallest schema/storage vertical slice. Do not add B2 CLI
   lifecycle behavior, B3 producers, B4 exports, or B5 release work.
4. Freeze a clean committed candidate and record commit/tree/base/changed paths.
   Run the canonical sequential chain with one compact packet: QA → code →
   conditional security → final regression QA.
5. Append one candidate-bound ledger row per reviewer invocation. Tokens remain
   `unknown` unless the runtime provides exact attribution; record dispatch
   bytes as a proxy, never as tokens.
6. Stop after B1 closure and request separate direction for B2.

## Traps

- Do not treat B0 ownership admission as B1 implementation approval.
- Pre-register B1 before the first product edit; post-hoc registration breaks
  the consecutive-sampling rule.
- Freeze input and policy evidence against immutable Git blobs, not the current
  checkout. Checkout-byte hashes on Windows can differ from canonical LF
  hashes.
- On this machine, use the installed pytest executable or Python module path;
  `pytest` may be absent from `PATH` even when pytest is installed.
- Any source, test, fixture, policy, contract, gate configuration, or generated
  projection edit creates a new candidate and invalidates stale execution
  claims.
- Reviewer invocations are sequential and diff-scoped; re-reviews are
  findings-scoped.
- Re-run the consuming validator after every scorecard or ledger append.
- Do not infer achieved token savings from invocation counts or dispatch bytes.
- Preserve the five untracked provenance artifacts.

## Glossary

Phase 6B; B0; B1; governance admission; frozen candidate; compact review
packet; candidate-bound invocation ledger; dispatch bytes; final regression
QA; mechanically pure closure-only; effective-from boundary.
