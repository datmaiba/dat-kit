# Review Economy v2 — bounded invalidation and reviewer convergence

**Status:** DRAFT — awaiting plan review and maintainer approval  
**Date:** 2026-07-21  
**Trigger:** Phase 6A used 8 software-review, 3 security-review, and 4 QA
invocations while per-agent token counts were unavailable. The quality findings
were valuable; the redundant invalidation and closure passes were not.

## 1. Scope

This change tightens dat-kit's software-dev review orchestration so independent
review remains fail-closed while a verdict is invalidated only by a change that
intersects its reviewed responsibility. It introduces a closed review-impact
matrix, review epochs, specialist-before-general ordering, bounded re-review,
and a cheap closure path.

Out of scope:

- weakening SW-G3 or removing any required independent reviewer;
- parallel reviewers;
- replacing findings-scoped re-review with self-review;
- changing any reviewer `model:` pin before Telemetry v3 has real per-reviewer
  cost and quality evidence;
- implementing telemetry or inferring token totals unavailable from the host;
- changing the domain loop ceiling or the work-loop engine.

## 2. Ground-truth findings

1. R1–R4 already require sequential, diff-scoped, findings-scoped, static,
   capped review, but do not define verdict invalidation after later edits
   (`plans/PLAN-v7-platform.md` §16; `domains/software-dev/reviewers.md`).
2. The workflow currently says every code-review fix re-runs QA and code review,
   while the security path similarly re-runs QA and security. It does not
   distinguish semantic, test-only, evidence-only, or authority-closure changes.
3. QA's charter already says re-runs are failed-gate/failed-attack scoped, but
   the orchestrator can still request a full suite repeatedly.
4. The paid-for lesson at `lessons-learned/lessons-learned.md` (2026-07-18)
   addresses whole-repo/parallel review cost, not stale-verdict and closure cost.
5. Registry routing makes the policy edits Class B under
   `software-dev-policy/1`, while their maintainer tests are Class B under
   `maintainer-policy/1`; evolution proposals must therefore remain split.

## 3. Decisions proposed for approval

### D-RE-1 — Review epoch and verdict binding

A **semantic review epoch** begins when the builder freezes a semantic diff and
its declared gates are green. Every verdict binds the exact baseline/candidate,
reviewed paths, responsibility surfaces, and gate evidence. A later candidate
may reuse a prior verdict only when the deterministic path-and-surface test in
section 5 proves non-intersection; otherwise the verdict is invalidated.
Unknown or ambiguous impact fails closed as semantic, starts a successor epoch,
and invalidates every verdict whose non-intersection cannot be proved.

### D-RE-2 — Closed impact classes; reason is orthogonal

| Class | Definition | Required follow-up |
|---|---|---|
| `semantic` | runtime, contract, gate behavior, security boundary, public behavior, or normative policy changed | start a successor epoch and rerun every intersecting stage in canonical order |
| `test_only` | tests become stricter; production/contract/policy bytes unchanged | targeted QA + declared gates, then software/code review of the test delta (and its declared specialist when applicable); invalidate every path- or `test_or_gate_logic`-intersecting verdict and reuse only proven non-intersecting verdicts |
| `evidence_only` | append-only scorecard, handoff, receipt, or non-authoritative evidence; no authority or policy transition | schema/append validator and governing path review only |
| `authority_closure` | an authorized decision/closure record binds an already reviewed artifact without changing its bytes or authority policy | decision-schema/hash/appointment audit only; do not restart feature QA/code/security |

`delta_reason` is separately one of `planned_change` or
`review_finding_fix:<verdict-id>:<finding-id>`. A finding fix never receives a
cheaper impact class merely because a reviewer requested it: a code/policy fix
is still `semantic`, and all intersecting verdicts are invalidated. The
originating verdict is always invalidated and must close findings-scoped after
all earlier invalidated stages are green.

The builder cannot make a permissive free-form classification. The phase report
contains a closed **Review Impact Manifest**; the next independent reviewer
audits it. Any new path, new trigger surface, changed normative bytes, unknown
surface, or failed classification assertion upgrades the delta to `semantic`.

### D-RE-3 — Reviewer order

For a semantic epoch, run:

1. QA once on the frozen semantic candidate;
2. contract-/governance-declared specialist reviewers, narrowest first;
3. software/code reviewer on the specialist-stable candidate;
4. conditional security reviewer last.

Downstream reviewers never run before an upstream `RETURN TO BUILDER` is closed.
The strict sequence is preserved; the change prevents knowingly stale work.

### D-RE-4 — Re-review and final regression

- A findings fix reruns impacted QA/gates, every prior verdict invalidated by
  path or responsibility-surface intersection, and the originating reviewer,
  in canonical order. Non-intersecting verdict reuse requires recorded proof.
- A reviewer may identify a direct regression caused by the fix, but may not
  reopen unrelated pre-existing scope during findings-scoped re-review.
- Run one initial full phase QA for the frozen candidate chain and at most one
  final full regression after all semantic fixes. Successor epochs run all
  invalidated targeted checks/stages; an ambiguous manifest or unrelated scope
  expansion restarts the full chain.
- Test/evidence/closure deltas use their matrix rows instead of another full
  feature QA only when every non-intersection assertion is proven.
- After two findings-scoped returns by the same reviewer in one epoch, STOP and
  re-plan; do not spend an unbounded third review loop.

### D-RE-5 — Cost evidence without invented tokens

Until Telemetry v3 exposes trustworthy per-reviewer attribution, report only:
reviewer role, full vs findings-scoped, epoch, invocation count, elapsed time if
known, verdict, and invalidation reason. Token values remain unknown. Model-pin
changes are deferred to a separate Class C proposal using real telemetry.

## 4. Files to create or modify

### Slice P — this planning artifact (`maintainer-policy/1`, Class B)

| File | Action | Purpose |
|---|---|---|
| `plans/PLAN-review-economy-v2.md` | create | approved design, oracle scenarios, governance split, and rollback plan |

The plan is not an unscoped evidence input. Before it is adopted or committed,
route its exact hash as the sole patch scope of its own immutable evolution
proposal. Its evidence is the pre-existing engine/domain/governance baseline and
an independent plan review; the plan cannot certify itself or either later
slice.

### Slice A — software-dev policy (`software-dev-policy/1`, Class B)

| File | Action | Purpose |
|---|---|---|
| `domains/software-dev/reviewers.md` | modify | add D-RE-1 through D-RE-5 as the binding closed matrix and ordering rules |
| `domains/software-dev/workflow.md` | modify | make VERIFY/REVIEW consume the Review Impact Manifest instead of blindly restarting the chain |
| `domains/software-dev/gates.md` | modify | define acceptable evidence for epoch binding, impacted QA, and final regression |
| `domains/software-dev/deliverables/phase-plan.template.md` | modify | add Review Impact Manifest and review-budget sections |
| `agents/qa-agent.md` | modify | require epoch ID and reject unrequested full reruns on findings/test/evidence deltas |
| `agents/code-reviewer.md` | modify | audit change class and prohibit unrelated findings in re-review |
| `agents/security-reviewer.md` | modify | preserve trigger rules but distinguish security findings fixes from unrelated closure deltas |
| `agents/plan-reviewer.md` | modify | check that plans declare review order, invalidation rules, and budget |

Slice A gets its own immutable evolution proposal, software regression gate,
software-dev reviewer, and semantic-owner rollback receipt.

### Slice B — maintainer enforcement (`maintainer-policy/1`, Class B)

| File | Action | Purpose |
|---|---|---|
| `scripts/tests/test_software_dev_pack.py` | modify | structurally pin the closed matrix, ordering, manifest, bounded reruns, and unchanged model pins |

Slice B starts only after Slice A has an approved decision. Its separate
proposal names that already-approved policy revision/decision as the independent
behavioral oracle. New or changed tests are supporting enforcement evidence,
never decisive evidence for their own proposal. Pre-existing full regression
and validator results plus an independent scenario audit supply the remaining
evidence; same-proposal self-certification is rejected.

No change is planned for `engine/work-loop/ENGINE.md`, generated skill triggers,
registry policy, reviewer model pins, or Telemetry v3.

## 5. Interfaces and shapes

No public API or runtime interface changes.

The new plan/report interface contains a closed Review Impact Manifest:

```text
epoch_id
baseline_ref
candidate_ref
change_class
delta_reason
semantic_paths
test_paths
evidence_paths
impact_surfaces
gate_inputs_changed
required_stages
invalidated_verdicts
reused_verdicts_with_reason
review_rounds_by_role
```

Every referenced verdict has this closed record:

```text
verdict_id
reviewer_role
epoch_id
baseline_ref
candidate_ref
reviewed_paths
responsibility_surfaces
gate_evidence_refs
verdict
finding_ids
```

The closed responsibility taxonomy is:

```text
runtime_behavior
public_contract
normative_policy
test_or_gate_logic
security_boundary
build_or_projection
evidence_record
authority_record
```

The implementation binds a closed, multi-label derivation table; matching more
than one row emits every listed surface:

| Changed path/byte/trigger class | Derived `impact_surfaces` |
|---|---|
| non-test runtime implementation or behavior fixture | `runtime_behavior` |
| public API/schema/CLI/compatibility contract | `public_contract` plus `runtime_behavior` when implementation bytes also change |
| normative workflow/gate/reviewer/agent policy | `normative_policy`; also `test_or_gate_logic` when gate semantics change |
| tests, gate implementation/configuration, or test fixtures | `test_or_gate_logic` |
| existing security trigger (auth, secret, sandbox, external input, network, privacy) | `security_boundary`; also `runtime_behavior` when runtime bytes change |
| build, render, projection source/configuration/output | `build_or_projection` |
| append-only scorecard, handoff, receipt, or non-authoritative run evidence | `evidence_record` |
| proposal, decision, appointment, authority, or closure record | `authority_record` |

Path patterns and trigger names are copied from the current registry and
reviewer charters into the binding matrix; they are not free-form manifest
input. Unmatched paths, byte classes, or triggers emit `unknown` and fail closed
to `semantic` with affected verdicts invalidated.

Each reviewer charter declares a non-empty taxonomy subset; a specialist may
narrow that subset only through its existing declared trigger. For each prior
verdict, invalidate it when any of these is true:

1. changed paths intersect `reviewed_paths`;
2. `impact_surfaces` intersect `responsibility_surfaces`;
3. a referenced gate input or projection input changed;
4. the verdict is the origin of `delta_reason`; or
5. required data is absent, unknown, or ambiguous.

Reuse is permitted only when all five checks are deterministically false and
the manifest records the non-intersection proof. Lists are sorted and
path-scoped. Missing fields, unknown classes/surfaces, or an unproved reuse fail
closed to `semantic` and invalidate the affected verdict.

## 6. Test list

Add structural/behavioral tests in `scripts/tests/test_software_dev_pack.py`:

1. `test_review_impact_matrix_is_closed_and_complete`
2. `test_unknown_review_impact_fails_closed_to_semantic`
3. `test_specialists_run_before_general_and_security_reviewers`
4. `test_finding_reason_does_not_override_semantic_impact_class`
5. `test_finding_fix_invalidates_every_intersecting_verdict_and_origin`
6. `test_test_only_delta_preserves_nonintersecting_semantic_verdicts`
7. `test_evidence_and_authority_closure_use_bounded_audits`
8. `test_candidate_chain_has_one_initial_qa_and_one_final_regression_ceiling`
9. `test_third_findings_return_stops_for_replan`
10. `test_manifest_and_verdict_schemas_are_closed_and_complete`
11. `test_unknown_intersection_data_invalidates_verdict_fail_closed`
12. `test_reviewer_model_pins_remain_unchanged`

Red-before-green proof: on a disposable copy, remove one matrix row and one
manifest field, prove the new tests fail, then run the unchanged tree green.
This proof supports Slice B but does not approve it; the decisive behavioral
oracle is the separately approved Slice A policy.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| stale approval reused after a semantic change | unknown impact and any normative-byte change fail closed to a new epoch |
| builder labels a semantic fix `test_only` | independent reviewer audits the manifest; structural assertions compare touched paths and declared classes |
| specialist finds changes after code review | specialists run before the general reviewer |
| security fix breaks general contract logic | widened/intersecting fix becomes semantic and restarts at the earliest affected stage |
| closure record changes authority rather than merely recording it | `authority_closure` requires unchanged authority policy plus appointment/hash audit; otherwise semantic |
| cross-policy proposal mixes domain policy and maintainer tests | two proposals/slices; no shared patch scope |
| cost reduction weakens quality | reviewer existence and strict sequence remain unchanged; only invalidation and rerun scope change |
| model downgrade hides findings | model pins remain unchanged until measured Class C evidence exists |

## 8. Execution phases

### Phase 0 — Governance and baseline

1. Route the exact approved plan hash through Slice P; do not treat the plan as
   evidence for itself.
2. Create separate immutable proposals for Slice A and, only after Slice A is
   approved, Slice B.
3. Record the Phase 6A baseline: 8 software, 3 security, 4 QA invocations;
   tokens explicitly unknown.
4. Capture current green software-dev pack tests and validator output as
   pre-existing regression evidence.

### Phase 1 — Software-dev policy candidate (Slice A)

1. Add the closed impact matrix, verdict schema, deterministic invalidation
   algorithm, and Review Impact Manifest to domain policy/template.
2. Update four reviewer charters consistently.
3. Independently walk the predeclared scenarios and review Slice A under its
   own software-dev policy proposal; keep engine, registry, generated triggers,
   and model pins byte-identical.
4. Obtain the authorized Slice A decision before opening Slice B.

### Phase 2 — Independent enforcement (Slice B)

1. Create Slice B against the approved Slice A revision/decision as its external
   behavioral oracle.
2. Add the twelve tests without weakening existing R1–R4 pins.
3. Run the disposable-copy mutation proof and retain red output as supporting,
   not decisive, evidence.
4. Run the pre-existing full regression/validator and an independent scenario
   audit; reject any attempt to use the changed tests as self-approval.

### Phase 3 — Verification and dogfood

Walk these table scenarios without spawning real redundant reviewers:

1. semantic contract + specialist finding → impacted QA, every intersecting
   verdict, then originating specialist in canonical order;
2. security finding that changes runtime bytes → successor semantic epoch;
   impacted QA + software/code + security rerun, so no stale code verdict;
3. test-only tightening → project gates + test-delta review only;
4. scorecard append → append/schema validation only;
5. owner decision binding unchanged artifact → one authority-closure audit;
6. ambiguous/new-path fix → successor semantic epoch and full applicable chain.

Run `scripts/validate.py`, full pytest, `render.py --check`, Bash syntax,
ShellCheck, and `git diff --check`.

### Phase 4 — Independent review and closure

Run one QA phase review and one software-dev review on the final semantic diff.
Security review is skipped unless implementation unexpectedly changes a current
security trigger surface; state the skip reason. Findings re-reviews obey the
new matrix. Record invocation counts, not invented token totals.

## 9. Demo steps

1. Render the closed matrix from `reviewers.md` and show all four impact rows.
2. Feed each Phase 3 scenario into the structural fixtures and display the
   exact required stage sequence plus each verdict's intersection decision.
3. Demonstrate that changing an evidence-only path does not invalidate a
   contract verdict, while changing a normative contract path does.
4. Demonstrate the third findings return produces STOP/re-plan.
5. Show `model:` lines for all reviewer charters are byte-identical to baseline.

## 10. Done evidence

- SW-G1: full declared project gates green plus red-before-green mutation proof.
- SW-G2: all six scenario sequences observed as specified.
- SW-G3: QA `PHASE DONE`; software-dev reviewer `APPROVE`; security reviewer
  `APPROVE` or a trigger-based skip recorded.
- Slice P, Slice A, and Slice B proposals/rollback receipts remain explicitly
  routed; the two policy owners are never mixed in one proposal.
- Slice B cites the approved Slice A policy as its oracle and never uses its new
  tests as decisive self-certification.
- No telemetry token claim and no reviewer model-pin change.

## 11. Rollback

Revert Slice B before Slice A using their separate semantic commits, then
regenerate/check projections and run the full regression suite. Withdraw or
supersede Slice P separately if the design is abandoned. Because the engine and
registry remain unchanged, rollback restores the current R1–R4 behavior without
format migration or data rewrite.
