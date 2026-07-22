# HANDOFF 2026-07-22 — Phase 6B execution with token-economy observation (v3)

**Current phase:** PLAN — independent review and maintainer approval pending

**Execution authorization:** none from this handoff; Phase 6B has not started

**Review Economy Stage B:** not started and unauthorized; no verdict-reuse or
policy exception exists

**Supersedes as the execution entrypoint:**
`handoffs/HANDOFF-2026-07-22-review-economy-stage-a-plan-v2.md`. That file and
the earlier Review Economy plans remain provenance only.

## Goal

Resume the approved PLAN-v7 Phase 6 from its first missing item — Phase 6B —
while applying the existing token-discipline rules and measuring whether
review restarts contain a repeated, mechanically pure closure-only class.

The observation is an overlay on real Phase 6B work, not a prerequisite that
parks Phase 6 and not a new telemetry or governance authority. It may justify
a later proposal; it cannot change the current review chain.

Success for this plan means:

1. Phase 6B advances in dependency-ordered, reviewable slices toward every
   PLAN-v7 §13.2 receipt.
2. The first three classifiable eligible Phase 6B review chains produce a
   candidate-bound invocation ledger.
3. Token savings are reported only from trustworthy attribution; otherwise
   tokens remain `unknown` and only invocation counts and dispatch-size
   proxies are reported.

## Ground truth

- Branch: `feature/telemetry-v3`; HEAD at planning time: `8748b00`.
- Canonical maintainer contract: `dat-kit 1.16.0`, root `AGENTS.md`.
- Phase 6A is closed. The exact approved Telemetry v3 contract is
  `docs/contracts/telemetry-v3.md`, SHA-256
  `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde`.
- Its Class C decision is
  `decision-f80fa03211e51c3f68c5-0001`, recorded as `approved` in
  `docs/decisions/evolution-manual.decisions.jsonl`.
- `scripts/telemetry.py` and `telemetry/` are absent at HEAD. Phase 6B runtime,
  producers, export, reports, observations, RC, and release remain undone.
- PLAN-v7 Phase 6 and §13.2, plus `docs/contracts/telemetry-v3.md` T3.12–T3.13,
  govern implementation and closure.

The superseded v2 handoff mislabeled the contract hash above as the hash of
`AGENTS.md`. The `AGENTS.md` SHA-256 at HEAD is
`d7cd3fd39bacc8694b4f8585250d7445ea79bc489eefac30b32e4b0aafa00737`.

## Scope and authority

### In scope

- Phase 6B implementation and Phase 6C/release preparation already required by
  the approved PLAN-v7 and Telemetry v3 contract.
- The governance admission needed for currently orphaned implementation paths.
- Existing token-discipline mechanics: sequential reviewers, frozen diff,
  scoped packets, findings-scoped re-review, and final regression QA.
- Task-local observation rows attached to each Phase 6B task report/handoff.

### Out of scope

- Semantic verdict caching or reuse.
- Any new review-validity rule, registered signal, durable evidence schema, or
  gate based on the observation ledger.
- Reviewer model-pin changes.
- `kit-evolve`, Stage B implementation, or automatic authority.
- A token-saving claim inferred from the historical
  `8 software / 3 security / 4 QA` reconstruction.

## Execution plan

### B0 — governance admission before runtime paths

1. Run `scripts/registry.py explain-evolution` for every proposed new governed
   root and implementation path, including `scripts/telemetry.py`,
   `telemetry/schema-v3.json`, local event storage, and durable exports.
2. Resolve every orphan diagnostic through one canonical ownership source and
   negative tests; do not mask it with an unrelated broad glob.
3. Treat admission of the new roots as Class C. Create its proposal and frozen
   input hashes; run the registry-declared two independent reviewers, full
   cross-component regression, and rollback rehearsal; obtain platform-owner
   approval; and record the effective-from boundary.
4. Stop after the approved B0 governance commit. B0 approval is not B1
   implementation approval.

Exit: all B1 paths have explicit ownership and no unresolved orphan; no
telemetry runtime file exists before this exit.

### B1 — schema, storage, validation, and recovery

Implement the frozen v3 schema and the smallest vertical runtime slice:

- local single-writer append;
- validation and duplicate-ID rejection;
- correction linkage and prior-byte preservation;
- interrupted-append recovery;
- privacy/source-class rejection at the storage boundary.

Prove every new gate red-before-green. Freeze one clean committed candidate,
then run the complete current review chain.

### B2 — lifecycle CLI and task identity propagation

Implement `start | append | finish | validate`, task UUID creation at LOAD,
parent/delegation linkage, handoff resume linkage, and disable/downgrade
behavior. Do not add producers whose required lifecycle primitives are not yet
green.

### B3 — integrations and five named producers

Implement in dependency order:

1. scorecard/HARVEST integration and kit-facing lesson candidate;
2. diagnosing-bugs defect projection;
3. knowledge-work machine-readable fact-check footer without automating the
   human verdict;
4. `resumed_from_handoff` and stable task linkage;
5. per-reviewer and event-coverage-rate report views.

Each independently reviewable subset is its own committed candidate. Generated
skills change through their registry/pack/render source, never by hand-editing
the projections.

No producer becomes `active` from prose, fixtures, or synthetic events. Close
the following receipt matrix with real tasks:

| Producer | Required real receipt |
|---|---|
| build-loop HARVEST | validated `lesson_candidate_recorded` with `kit_facing=true` from a real root-cause case |
| diagnosing-bugs | real post-mortem emitting the required defect tuple and `benchmarks/defects.jsonl` projection |
| knowledge-work | real fact-check footer with human, agent, and automation source distinguished |
| task/handoff | real resumed or delegated task preserving task and parent linkage |
| reports | fixtures plus real per-reviewer and per-host event-coverage views |

### B4 — durable export, retention, and compatibility

Add append-only local-to-durable export/aggregation, v2-to-v3 import as new
linked events, retention/privacy documentation, compatibility coverage, and
recovery/disable tests. Existing benchmark history is never rewritten.

### B5 — Phase 6C observations and release closure

Record one real software-development task and one real knowledge-work task,
distinguishing human, agent, and automation verdict sources. Then complete
schema freeze and downgrade/disable verification; bump the version and render
all projections **before** freezing the RC. Run full regression, rollback
rehearsal, and Ubuntu and Windows CI on that exact RC SHA. Obtain RC approval,
tag that same SHA, and record external tag/release receipts afterward as
required by PLAN-v7 §13.2.

Phase 6 is not complete merely because B1–B4 code exists.

## Per-slice review protocol

For every B1–B4 slice:

1. Pre-register an observation task ID, immutable slice scope, intended paths,
   and applicable reviewer roles before work begins. Finish source, policy,
   tests, fixtures, generated projections, and planned
   documentation before review freeze.
2. Require a clean committed candidate and record both commit and tree IDs,
   base commit, and changed paths with status, including renames/deletions.
3. Run eligibility gates as `pre-check (non-evidence)` only.
4. Give every reviewer the same compact task-local packet containing task goal
   and non-goals; base and candidate commit/tree; changed paths with status;
   applicable plan/contract locators; pre-check summary marked non-evidence and
   log locations; security-trigger decision; known risks; and open finding
   IDs. Before review, the
   reviewer independently reconciles candidate and changed-path facts against
   Git. A mismatch voids the invocation and is recorded.
5. Run the canonical chain sequentially: QA execution → code review → security
   review when current triggers apply → findings-scoped re-review → final
   regression QA → REPORT → HARVEST.
6. Any source, test, fixture, policy, contract, gate-config, or generated
   projection edit creates a new candidate. Prior green execution is never
   presented as execution on that candidate.
7. A post-review report, handoff, scorecard, or ledger append records a separate
   closure-tree ID. Re-run the validator that consumes the append before
   claiming final green.
8. Budget each implementation slice at 50–80k total tokens with a checkpoint at
   70%. Use targeted tests while editing; run the full declared gates at review
   freeze and after any finding fix. Stop on scope or budget overflow rather
   than silently expanding the slice.

The packet is a convenience index, never gate evidence or authority.

## Token-economy observation overlay

### Sampling rule

Observe the first three **consecutive eligible** pre-registered Phase 6B task
IDs reaching QA after this plan is approved; do not select tasks after seeing
their results. The immutable sampling unit is one pre-registered slice scope
carried through one committed-candidate review chain. An eligible task changes
at least one Phase 6B product/contract/test surface, has its own committed
candidate, and runs the complete applicable review chain. Planning-only and
provenance-only edits are ineligible. Splitting or merging a scope after
registration cannot change the sample: the registered task remains incomplete,
and any new scope receives a later task ID.

If a task contains an `unknown/ambiguous` restart, retain it in the ledger but
exclude it from the decision denominator and observe the next consecutive
eligible task. The first decision checkpoint occurs after three classifiable
tasks. A one-positive result may extend the pre-registered sequence to at most
five classifiable tasks. Phase 6C is the hard stop; if the required denominator
does not exist by then, close the experiment as insufficient evidence.

### Invocation ledger

Append one row per reviewer invocation to the task report/handoff:

```text
task | ordinal | role | from candidate/tree | to candidate/closure tree |
full/findings-scoped | restart_of_ordinal | restart cause |
trigger/finding IDs | verdict | elapsed if known |
runtime input/output tokens or unknown | dispatch bytes |
invalidation reason or none | avoidable_under_narrow_rule yes/no + reason
```

`dispatch bytes` measures only material intentionally supplied in the dispatch;
it is a context-size proxy, not token telemetry and not proof of total savings.
Do not estimate files privately opened by a reviewer.

An invocation is `avoidable_under_narrow_rule=yes` only when it is a repeated
code or security review of the same product candidate, the only transition is
proven pure closure-only below, the same role already returned a passing
verdict, no finding or trigger changed, and final regression QA still runs on
the closure tree. Initial QA/review, findings re-review, and mandatory final
regression QA are never counted as avoidable. This is the sole counterfactual
used by the five-invocation threshold.

### Restart classification

A restart is `mechanically pure closure-only` only when all are proven:

1. the candidate-to-closure diff touches only report, handoff, scorecard, or
   task-local ledger files;
2. it touches no source, test, fixture, policy, contract, gate configuration,
   generated projection, or security-trigger surface;
3. the consuming validator and final regression QA have receipts on the
   closure tree and show no changed gate outcome;
4. the restart was not caused by an open reviewer finding.

Fail any condition: `semantic`. Insufficient evidence: `unknown/ambiguous`.
Unknown is never counted as pure.

### Pre-registered decision rule

After three classifiable tasks:

- pure closure-only in 0 tasks: close with no policy proposal;
- in 1 task: extend observation to at most five classifiable tasks; Stage B is
  eligible only if a second task qualifies;
- in at least 2 of 3 tasks: a separate Class C Stage B plan may be drafted;
- regardless of task count, no Stage B plan may claim material economy unless
  the exact narrow rule would have avoided at least 5 invocations in the
  observed ledger, matching the existing 15-invocation proxy threshold;
- any stale/missing required verdict, changed gate result, or security-trigger
  ambiguity closes fail-closed with no exception proposal.

Eligibility permits drafting and fresh approval only; it authorizes nothing.

## Reporting token reduction

The planning heuristics remain non-additive and are not acceptance criteria:

- bounded vertical slice: 20–35% total-token reduction target;
- review round: 40–55% review-token reduction target;
- frozen packet: 15–30% of review tokens;
- findings-scoped repeated review: 50–80% of that repeated round.

Report an achieved percentage only when comparable tasks have trustworthy
runtime attribution. Otherwise report:

- total and avoidable invocation counts;
- full versus findings-scoped counts;
- dispatch-byte deltas;
- elapsed only when known;
- tokens as `unknown`.

The theoretical `15 → 4` clean-chain floor is not a forecast and must not be
reported as a Phase 6A or Stage A saving.

## Approval and next steps

1. Independent plan reviewer returns `KEEP`, `IMPROVE`, or `REPLAN`, followed
   only by blocking defects.
2. Maintainer explicitly approves, revises, or rejects this plan.
3. On approval, commit this plan as the tracked execution entrypoint. The
   superseded Review Economy artifacts remain provenance and are not required
   runtime reading.
4. Start B0 only. Do not bundle B0 approval with B1 implementation.

## Traps

- Do not let the measurement experiment park Phase 6B.
- Do not treat Phase 6A's approved contract decision as ownership approval for
  currently orphaned runtime paths.
- Do not compare historical 15-invocation reconstruction with a clean-chain
  floor as though candidates and task scopes were equal.
- Do not turn `dispatch bytes` into invented tokens.
- Do not reuse a verdict across a semantic candidate or weaken final QA.
- Do not append scorecard/ledger data after the last validator run.
- Do not place future review receipts inside the artifact they review.
