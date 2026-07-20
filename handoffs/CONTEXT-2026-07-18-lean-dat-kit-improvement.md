# Active context — lean dat-kit improvement

**Status:** active execution context, not execution authority
**Date:** 2026-07-18
**Purpose:** preserve Plan v7's product and safety outcomes while minimizing avoidable context, implementation, test, and review tokens.
**Supersedes for future sessions:** `handoffs/HANDOFF-2026-07-18-token-discipline-portable.md` as the default context file. Keep that file only as historical evidence; do not execute its patch recipe again.

## 0. Hard boundary

- The user stopped Plan v7 execution. Do not resume Phase 1B or mutate its worktree without explicit authorization.
- This document is a compact decision and execution context. It does not approve a phase, a scope increase, a commit, a push, or a release.
- The gate-runner/evidence-packet design below is approved guidance, not an implemented feature or authorization to add it to Phase 1B. Because trusted-green receipt generation is enforcement code that could weaken gates, its implementation is a **Class C** slice requiring the admission test, explicit approval, and the full Class C evidence listed below.
- On resume, load only root `AGENTS.md`, the documents it directly requires, this file, and the exact approved slice. Do not reread the full plan or the superseded handoff unless a missing fact requires it.
- Preserve all existing uncommitted work. First identify its branch and worktree with read-only Git commands.

## 1. Outcomes that must survive optimization

Token reduction must not weaken these original goals:

1. dat-kit becomes an open discipline platform centered on a work contract, not a coding-only agent.
2. Multiple professions compose through Domain Packs; software development remains supported and knowledge work remains a shipped reference domain.
3. `AGENTS.md` remains the single generated-project policy owner; host adapters stay thin.
4. Every component has one descriptor owner. Generated artifacts are byte-exact projections, never competing authorities.
5. Normative contracts precede implementation, and recognized obsolete revisions never report green.
6. Brownfield paths inspect before mutation and do not rewrite recognized files merely because they exist.
7. Telemetry is immutable; evolution proposals are deterministic and review-bound; outcomes remain temporally independent from proposals.
8. Extensibility is proven by a synthetic component without validator, renderer, or scaffold hardcoding.
9. Loop capability is earned through evidence; it is not enabled by assertion.
10. Release claims still require the applicable migration, security, smoke, rollback, release-candidate, and tag evidence.

Deferred boundaries remain deliberate:

- v2.1: telemetry.
- v2.2: self-evolution.
- Do not pull either boundary into a v2.0 slice to make the architecture look complete.

## 2. Verified repository state at handoff

### Maintainer checkout

- Observed checkout: repository root on branch `draft/wip-2026-07-18`, HEAD `8747b3e`.
- Token-discipline edits are already present but uncommitted in reviewer charters, `docs/agent-working-rules.md`, `skills/build-loop/SKILL.md`, and `lessons-learned/lessons-learned.md`.
- `plans/PLAN-v7-platform.md` contains the v7.1 token-discipline amendment.
- Therefore: do not blindly reapply section B of the superseded portable handoff.

### Platform implementation worktree

- Branch: `feature/open-platform-v2`.
- Safe committed/pushed point: `7e26541` (`docs(platform): define Phase 1A normative contracts`).
- Phase 0B and Phase 1A are committed and pushed.
- Phase 1B is unfinished, unreviewed, unstaged WIP. It includes registry/render implementation, catalog data, tests, manifest work, CI/init/validation edits, and a smoke fixture.
- Reported by the interrupted session: its last greenfield smoke failed with `SCAFFOLD_MANIFEST_INVALID: bad provenance header`. Reproduce narrowly before treating that report as current evidence.
- No related execution process was running when this context was written.
- Preserve the WIP unchanged until the user explicitly chooses to continue, reduce, salvage, or discard it.

### Cost evidence

- Phase 0B scorecard: **529,479 tokens** total (`132,361` input, `5,090` output, `104,851` cache creation, `287,177` cache read).
- Phase 1A exact token count is unavailable because its scorecard recorded `unsupported_provider`; do not estimate it as fact.
- The prior handoff and lessons report one parallel three-reviewer round at approximately **284k tokens** (`122k` code, `94k` security, `68k` QA). Treat this as a recorded operational estimate, not independently verified telemetry.

## 3. Where tokens were spent without proportional value

Working diagnosis from the interrupted session, ranked by likely avoidable cost:

1. Multiple full reviewers inspected the same broad, still-changing diff in parallel.
2. A large Phase 1B implementation was produced before narrowing the first real consumer and exit condition.
3. Full files, the full plan, and already-known state were repeatedly loaded instead of symbols, ranges, diffs, and handoffs.
4. Full test suites and cross-platform gates were repeated after small local edits.
5. Spec, validator, fixtures, and error taxonomy expanded together before a minimum vertical slice proved the ownership model.
6. Review fixes triggered broad re-reviews instead of findings-scoped verification.
7. External smoke fixtures and release-shaped evidence were attempted before the local implementation was stable.

Required work is not waste: normative contracts, brownfield safety, deterministic diagnostics, negative tests, scoped security review, migration evidence, and release gates remain mandatory when their triggering surface is actually changed.

## 4. Admission test for any improvement task

Do not start a slice unless all six answers are explicit:

1. **Current pain:** what observed failure, duplication, or maintenance cost exists now?
2. **Real consumer:** what existing command or workflow will use the change immediately?
3. **Simplification:** what hardcoded branch, duplicate list, or manual step will be deleted or made authoritative?
4. **Bounded exit:** what smallest observable result proves the slice complete?
5. **Rollback:** how can the slice be reverted without corrupting brownfield state?
6. **Scope ceiling:** what is explicitly excluded, and what condition forces a stop and re-plan?

If any answer is missing, defer the work. Architectural completeness by itself is not a consumer.

## 5. Smallest sensible next slice — only if explicitly authorized

Before coding, audit the parked Phase 1B diff and choose one action: **salvage a narrow subset**, **park all**, or **discard specific files with user approval**. Do not assume the existing WIP defines the target design.

The preferred vertical slice is a **Minimum Viable Registry**:

- Bootstrap a canonical registry with child revision awareness.
- Expose read-only inventory for domains, adapters, and versions.
- Connect exactly one existing consumer: `scripts/validate.py`.
- Prove deterministic output and approximately six high-value diagnostics, including malformed input, unknown reference, obsolete recognized revision, and synthetic extension behavior.
- Preserve inspect-before-mutate and byte-exact projection rules.

Completing this intermediate slice does **not** complete Phase 1B, waive its remaining fixtures or exit criteria, or authorize the next slice. Report it only as a bounded vertical result.

Explicit non-goals for that slice:

- Evolution proposal runtime or authority lifecycle.
- Telemetry collection.
- Migration state machine or snapshot engine.
- Broad materialization/render framework.
- Four host-package implementations.
- Domain Pack cutover.
- Release automation or release claims.
- New abstraction layers without a second current consumer.

Heuristic ceiling, not a product invariant:

- Aim for no more than about 350 new production lines and eight focused tests.
- If the slice exceeds either ceiling, introduces a second persistence model, or needs more than one new authority, stop and re-plan before generating more code.

## 6. Lean execution protocol

### Context loading

1. Read root `AGENTS.md` and only its directly required maintainer documents.
2. Read this context once.
3. Read only the approved plan subsection or issue, not the entire plan.
4. Use CodeGraph when indexed; otherwise use `rg`, symbol search, and narrow line ranges before opening whole files.
5. Cap routine command output at roughly 200 lines. Redirect large evidence to a file and inspect only the relevant tail, summary, or matches.
6. Do not repeat state discovery already recorded here unless Git state changed or the fact affects a decision.

### Implementation

1. State the six admission-test answers and the file allowlist before editing.
2. Build one vertical path from descriptor owner to one consumer and one focused test group.
3. Prefer deleting hardcoding and duplicate ownership over adding a generalized framework.
4. Run the narrowest relevant test after each coherent change.
5. Freeze a stable diff before review. Do not ask reviewers to inspect moving code.
6. Keep evidence as machine-readable files or concise summaries; do not paste large logs into agent context.

### Gate-runner, receipt, and review packet

This is the preferred evidence pipeline once separately approved and implemented:

1. The builder runs only focused tests while the diff is changing.
2. The builder freezes the slice snapshot.
3. QA invokes one gate-runner that executes every canonical gate required for that snapshot. Third-party tools such as ShellCheck may be leaf executors inside the runner.
4. The runner emits a concise, locatable **phase receipt**; it does not issue `PHASE DONE` or replace QA judgment.
5. QA uses the receipt plus the frozen diff and relevant contract clauses to perform spec-aware negative/edge-case attacks and issue the QA verdict.
6. A **review packet** reuses the same snapshot facts sequentially for code review and mandatory/conditional security review.
7. A code, test, contract, gate-config, or reviewed-document change invalidates the packet for that snapshot. A findings-scoped fix produces a new **delta receipt** linked to the previous full receipt; it records only what actually reran and never presents inherited green results as execution on the new snapshot.
8. Regression QA runs against the resolved finding set and affected surfaces. Before completion or handoff, the final frozen snapshot receives a fresh full canonical receipt.

Gate-runner implementation governance — mandatory Class C evidence:

- immutable pre-change baseline and input hashes;
- explicit named authority and approved decision record with policy revision/hash;
- red-before-green proof that a failing canonical gate cannot produce a green receipt;
- two independent reviews or an explicitly approved equivalent;
- full cross-component regression and rollback rehearsal;
- an effective-from-run boundary so old receipts are never silently reinterpreted;
- no coupling to the parked Phase 1B registry WIP.

Minimum phase-receipt fields:

- snapshot identity: base/head plus a dirty-diff or content hash when applicable;
- exact gate commands and environment/runner identity;
- exit code, test count, duration, and short result per gate;
- paths to full logs and generated evidence, never pasted log dumps;
- red-before-green evidence when a gate itself changed;
- skipped boundary checks with the exact contract reason, or `none`.

Receipt types:

- **Full receipt:** all canonical gates required for one exact frozen snapshot ran on that snapshot.
- **Delta receipt:** only named finding-adjacent gates/attacks reran on a later snapshot; it links to a prior full receipt and lists inherited evidence separately.
- Only a fresh full receipt for the final frozen snapshot can support completion/handoff. A delta receipt alone cannot.

Minimum review-packet fields:

- phase/slice goal and explicit non-goals;
- changed-file allowlist and frozen diff locator;
- applicable plan/contract clauses only;
- phase-receipt locator and summary;
- known risks, security-trigger decision, and unresolved finding IDs;
- scope-overflow rule and report cap.

Until a gate-runner exists, produce the same compact evidence shape manually. Under the current contract QA must still run the canonical gates; an old CI result or third-party `green` is supplementary evidence, not a substitute.

### Gate cadence

- During coding: targeted unit/contract tests only.
- At a stable local slice: QA invokes every canonical gate once for the frozen snapshot, preferably through the gate-runner.
- Cross-platform or external smoke: once after local green when either the changed surface or the approved phase/exit contract requires that boundary.
- Final validation: every applicable phase, migration, security, smoke, rollback, and release gate remains mandatory before the corresponding completion or release claim.
- Re-run a full gate only when a fix can plausibly affect it; otherwise run the failing or adjacent target.

### Review cadence

- For every new phase or materially changed scope, perform a concise plan audit before implementation. The complete order remains: plan audit, implementation, QA, code review, conditional security review, regression QA.
- Invoke only roles required by the changed surface, sequentially.
- Security review is mandatory for any phase touching registry, migration, public input, export, paths, or external writes. Other trust-boundary or enforcement changes may also require it; omission must be justified by the unchanged surface, not by token cost.
- Contract review is required for normative contract changes, but not for implementation-only edits that conform to an unchanged approved contract.
- Reviewer input: the current frozen review packet—diff, changed files, applicable contract clauses, phase receipt, exact tests, and known risks. No full repository tour.
- Reviewer output: findings first, approximately 30 lines maximum unless evidence requires more.
- Code and security reviewers perform static analysis only. They may state a one-line exploit scenario but must not run PoCs, live attacks, or the feature; runtime verification belongs to QA.
- After fixes, re-review only the named findings and directly affected lines/tests.
- Run regression QA once after the finding set is resolved, not after each edit.

### Scope overflow

When a required fix crosses the file allowlist or non-goal boundary:

1. Stop implementation.
2. Record the cause, required new files, affected invariant, token impact, and smallest alternative.
3. Ask for an explicit scope decision.
4. Do not solve the overflow speculatively.

## 7. Token control

- Default slice budget: **50k–80k tokens**, including discovery, implementation, tests, and review.
- At roughly 70% of the budget, checkpoint: current diff, green evidence, unresolved risk, and remaining work.
- Do not continue past the budget without either a green vertical result or an explicit user decision.
- Use one primary implementation agent. Add no parallel implementation agents unless tasks are genuinely independent and their combined context is smaller than serial work.
- Use reviewers as gates, not as duplicate implementers or exploratory researchers.
- Keep reviewer `model:` pins unchanged until v2.1 supplies per-reviewer evidence. Changing pin policy is a Class C governance change, not a token-saving shortcut.
- Record one scorecard at the end of a substantive slice; do not repeatedly rescore an unchanged diff.
- Optimize cache reuse by keeping prompts and context stable, but never load irrelevant files solely to create cache hits.

### Reduction priorities and planning estimates

These ranges are non-additive planning heuristics, not measured telemetry:

| Lever | Estimated reduction | Safety condition |
|---|---:|---|
| One real-consumer vertical slice | 20–40% of a phase | Slice completion never implies phase completion or waives exit criteria. |
| One frozen review packet reused sequentially | 15–30% of review tokens | Reuse only while the snapshot is unchanged. |
| Findings-scoped re-review | 50–80% of a repeated review round | New surfaces require a broader new review. |
| Handoff/context delta instead of rediscovery | 10–25% of input tokens | Revalidate only facts affected by changed Git state. |
| Targeted coding tests plus correctly timed full gates | 5–15% of phase tokens | All gates required by the changed surface and phase contract still run. |
| Exact reviewer routing | 0–33% of review tokens | Never skip a required role; registry work requires security review. |

Practical target after the pipeline is proven:

- reduce a review round like the recorded approximately 284k round by about **40–55%**;
- reduce a bounded vertical slice by about **20–35%** overall;
- recalibrate after three measured slices, preserving `unknown` when attribution is unavailable.

Do not pursue these percentages by weakening QA verdict ownership, security triggers, Class B/C evidence, reviewer model pins, brownfield protection, or final/release gates.

## 8. Stop conditions

Stop and report instead of continuing when:

- the user has not explicitly resumed the plan;
- the parked WIP conflicts with the narrow approved design;
- ownership cannot be expressed with one canonical descriptor;
- a brownfield path would be overwritten without a proven migration/rollback path;
- tests require inventing behavior absent from an approved contract;
- the heuristic scope ceiling is crossed;
- reviewers are being asked to inspect an unstable diff;
- an external gate fails for an unrelated environment reason after one focused diagnosis;
- the remaining work belongs to v2.1 or v2.2.

## 9. Definition of success

A lean improvement is successful only when:

- it solves one current, evidenced problem for one real consumer;
- it preserves all applicable Plan v7 invariants and release gates;
- it removes or centralizes more duplicated authority than it introduces;
- focused tests and the applicable final gate are green;
- reviewer findings are resolved with scoped evidence;
- the result can be handed off without rereading the full plan or replaying repository history;
- deferred capabilities remain deferred.

Token reduction is a constraint on process and scope, never a reason to lower correctness, security, brownfield safety, or evidence quality.

## 10. Compact resume prompt

Use this in a fresh session:

> Read root `AGENTS.md`, its directly required maintainer documents, and `handoffs/CONTEXT-2026-07-18-lean-dat-kit-improvement.md`. Do not read the full Plan v7 or the superseded token-discipline handoff unless a specific missing fact requires it. Do not resume Phase 1B until I explicitly authorize a slice. First report branch/worktree status, the parked WIP boundary, and the proposed six admission-test answers in at most 15 lines. If authorized, execute only the named vertical slice under a 50k–80k total budget, use targeted tests while editing, freeze the diff before sequential scoped review, and stop on scope overflow.

For an explicitly approved gate-runner slice, append:

> Implement only the evidence pipeline described in this context. QA remains the canonical-gate runner and verdict owner; third-party tools are leaf checks. Bind each receipt/review packet to a frozen snapshot, keep full logs out of agent context, invalidate the packet on reviewed-surface changes, and prove that a failing gate cannot produce a green receipt. Do not mix this slice with Phase 1B registry implementation.

> Treat the gate-runner as Class C enforcement code: record immutable baseline/input hashes, named authority, a policy-revision decision record, two independent reviews or approved equivalent, full cross-component regression, rollback rehearsal, and an effective-from-run boundary. Distinguish full receipts from findings-scoped delta receipts; never carry green execution claims across snapshots, and require a fresh full receipt for the final snapshot.

## 11. Evidence confidence

- **Verified from Git/files:** branches, safe commit `7e26541`, uncommitted Phase 1B boundary, existing token-discipline markers, Plan v7 goals/invariants, and Phase 0B scorecard.
- **Recorded but not independently metered:** the approximately 284k three-reviewer round and its role breakdown.
- **Unknown:** exact Phase 1A token usage.
- **Decision heuristic:** the 50k–80k slice budget, line/test ceilings, percentage-reduction ranges, and three-slice recalibration target. Adjust only from measured future scorecards, not intuition.
