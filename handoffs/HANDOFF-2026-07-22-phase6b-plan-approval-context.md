# HANDOFF 2026-07-22 — approve Phase 6B plan, then begin governance admission

## Goal

Resume PLAN-v7 Phase 6 after the completed Phase 6A contract slice. Review and
approve, revise, or reject
`handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md`; after explicit
approval, execute only B0 governance admission. The token-economy observation
is an overlay on real Phase 6B slices and must not park Phase 6 or weaken the
current review chain.

## Runtime

`codex / GPT-5` (exact minor identifier unavailable).

## Workflow

`dat-kit:knowledge-work` produced and independently reviewed the plan;
`dat-kit:build-loop` is required for Phase 6B execution.

## Canonical contract

`dat-kit 1.16.0`, root `AGENTS.md`.

## Git state

- Branch: `feature/telemetry-v3`, tracking `origin/feature/telemetry-v3`.
- HEAD: `8748b00eee562bb7730035f7520dbf0680b03edb`
  (`docs(telemetry): record Phase 6A approval`).
- Worktree: dirty. `benchmarks/scorecard.jsonl` has one uncommitted append;
  the Phase 6B v3 plan and five Review Economy provenance artifacts are
  untracked. No Phase 6B runtime/product implementation exists.

## State

### DONE

1. Phase 6A contract-only work is approved and closed at HEAD `8748b00`.
2. `docs/contracts/telemetry-v3.md` SHA-256 is
   `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde`.
3. Class C decision `decision-f80fa03211e51c3f68c5-0001` is approved in
   `docs/decisions/evolution-manual.decisions.jsonl`.
4. The earlier Stage A v2 plan was audited as `IMPROVE`.
5. The new integrated v3 plan fixed six blockers: definite Class C B0,
   RC/version/tag identity, five-producer receipts, immutable sampling,
   ledger counterfactual, and unambiguous Stage B status.
6. Independent findings-scoped re-review of v3 returned `KEEP`.

### IN PROGRESS

1. Maintainer approval of the untracked v3 plan.
2. Decide which provenance artifacts to commit with the v3 entrypoint.
3. The scorecard append for the plan task is uncommitted but validated.

### NOT STARTED

1. B0 — Class C governance admission for the new telemetry root and runtime
   paths.
2. B1 — schema, storage, validation, and interrupted-append recovery.
3. B2 — lifecycle CLI and task/handoff identity propagation.
4. B3 — integrations and five real producer receipts.
5. B4 — durable export, retention, privacy, disable, and compatibility.
6. B5 — real observations, RC/rollback/CI, tag, and dat-kit 2.1.0 closure.
7. Review Economy Stage B — not started and unauthorized.

## Decisions in effect

- PLAN-v7 Phase 6 and §13.2 remain governing scope and Definition of Done.
- Telemetry v3 contract T3.12–T3.13 is binding; schema without active real
  producers is not Phase 6 completion.
- Phase 6A approval covers the exact contract artifact only. It does not admit
  the currently orphaned `scripts/telemetry.py` or `telemetry/` paths.
- Review order remains QA → code → conditional security → final regression QA.
- Token attribution is exact or `unknown`; dispatch bytes are only a context
  proxy. No achieved token-saving percentage has been established.
- Planning targets remain non-additive: 20–35% per bounded slice and 40–55%
  per review round.
- No `spec/08-decisions.md` exists. The approved plan and `docs/decisions/`
  are the decision record. The v3 plan is not in effect until maintainer
  approval.

## Files touched

- `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md` → untracked
  proposed execution entrypoint; independent review `KEEP`.
- `benchmarks/scorecard.jsonl` → one uncommitted append for the plan task;
  Codex token attribution is `unknown / unsupported_provider`.
- `handoffs/HANDOFF-2026-07-22-phase6b-plan-approval-context.md` → this
  untracked cold-start context.
- `handoffs/HANDOFF-2026-07-21-review-economy-claude-audit.md` → untracked
  provenance.
- `handoffs/HANDOFF-2026-07-21-review-economy-stage-a-plan.md` → untracked
  superseded provenance.
- `handoffs/HANDOFF-2026-07-22-review-economy-stage-a-plan-v2.md` → untracked
  superseded provenance.
- `plans/PLAN-review-economy-v2.md` and
  `plans/PLAN-review-economy-v3-measure-first.md` → untracked source-plan
  provenance.

## Verified gates

- Phase 6A historical HEAD: approval recorded at `8748b00`; contract SHA-256
  verified as `c9fa5e6b…6b70dde`.
- v3 initial independent plan review: `IMPROVE`, six blocking defects.
- v3 findings-scoped re-review: `KEEP`.
- After scorecard append: `python scripts/validate.py` → `✓ all checks green`.
- `git diff --check` → PASS; Git emitted only the existing Windows LF/CRLF
  warning for `benchmarks/scorecard.jsonl`.
- Phase 6B product tests: unverified because implementation has not started.

## Third-party tool risks

None reported. No installer or external plugin ran.

## Next steps

1. Read `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md` and
   return maintainer decision: approve, revise, or reject. Do not implement B0
   in the same approval step.
2. On approval, decide and commit the v3 entrypoint, this context, the validated
   scorecard append, and only the provenance artifacts the maintainer wants to
   retain.
3. Invoke `dat-kit:build-loop` for **B0 only** and run
   `scripts/registry.py explain-evolution` on every planned telemetry root/path.
4. Prepare the separate Class C governance proposal, frozen input hashes, two
   independent reviews, full cross-component regression, rollback rehearsal,
   platform-owner approval, and effective-from boundary.
5. Stop after the approved B0 governance commit; request separate approval for
   B1 implementation.

## Traps

- Do not restart Phase 6A; it is complete.
- Do not start `scripts/telemetry.py` or `telemetry/` before B0 closes.
- Do not let Review Economy measurement delay Phase 6B or become authority.
- Do not infer token savings from the historical 15-invocation reconstruction.
- Do not move version bump/render after RC approval; the approved RC SHA must
  be the tagged artifact.
- Do not mark a producer `active` without its real T3.12 receipt.
- Re-run the consuming validator after every scorecard/ledger append.
- Preserve the user's untracked provenance files unless the maintainer decides
  their commit scope.

## Glossary

- Phase 6A
- Phase 6B
- Phase 6C
- governance admission
- frozen candidate
- compact review packet
- candidate-bound invocation ledger
- mechanically pure closure-only
- dispatch bytes
- final regression QA
- producer receipt
- effective-from boundary
