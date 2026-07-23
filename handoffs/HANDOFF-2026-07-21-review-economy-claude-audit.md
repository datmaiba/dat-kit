# HANDOFF 2026-07-21 — independently review Review Economy v2

## Goal

Give Claude a cold-start, review-only brief for deciding whether
`plans/PLAN-review-economy-v2.md` is the best practical dat-kit improvement.
The current Codex audit recommends replacing its broad verdict-invalidation
taxonomy with a narrow post-review append exception. Claude must independently
confirm, revise, or reject that recommendation before the plan is changed or
approved. This is a dat-kit policy review, not a Codex-runtime change and not
Telemetry v3 implementation.

## Runtime

`codex / GPT-5`; the requested next reviewer is Claude, model unspecified.

## Workflow

`dat-kit:build-loop`, review-only. One fresh independent audit agent was used;
no QA, software-dev, or security reviewer was invoked for that audit.

## Canonical contract

`dat-kit 1.16.0`, from root `AGENTS.md`.

## Git state

- Branch: `feature/telemetry-v3`
- HEAD: `8748b00eee562bb7730035f7520dbf0680b03edb`
- Worktree: dirty only because the proposed plan and this handoff are
  untracked; no policy or implementation file has been changed.
- Approved Phase 6A contract SHA-256:
  `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde`
- Current Review Economy plan SHA-256:
  `c303bdfc4426aa5ea0227e64e290a982b55a068df48b2f4d20e0e5b74caf3bc4`

## State

### DONE

1. Phase 6A contract-only work was approved and closed at HEAD; no
   `scripts/telemetry.py` or `telemetry/` implementation exists.
2. `plans/PLAN-review-economy-v2.md` was drafted to reduce redundant reviewer
   invocations while preserving fail-closed review.
3. Its original plan reviewer returned `APPROVE` after two findings-scoped
   revisions.
4. A second fresh independent audit, explicitly instructed not to trust the
   first verdict, returned `REPLAN`.
5. Codex checked the load-bearing audit claims against the canonical maintainer
   workflow, evolution contract, registry policy, Git history, lessons learned,
   and the current plan. The conflicts described below are real enough to block
   approval of the current plan.

### IN PROGRESS

1. Independent Claude review of whether the current plan should be repaired or
   replaced by the narrower alternative below.
2. Neither the plan nor this handoff is staged or committed.

### NOT STARTED

1. Any rewrite of `plans/PLAN-review-economy-v2.md`.
2. Evolution proposal/authority routing for the improvement.
3. Any change to Domain Pack policy, reviewer charters, tests, engine, model
   pins, or Telemetry v3.

## Decisions in effect

- No `spec/08-decisions.md` exists in this repository.
- User directive: use an independent agent/Claude to review the plan before it
  is changed or approved.
- Review-only boundary: do not edit the plan, policy, tests, engine, registry,
  model pins, or telemetry during Claude's review.
- Per-reviewer token counts are unavailable from this Codex runtime. Report
  invocation counts and mark tokens `unknown`; do not infer token totals.
- Preserve existing R1–R4 discipline: sequential reviewers, diff-scoped input,
  findings-scoped re-review, static-only code/security review, capped reports.

## Files touched

- `plans/PLAN-review-economy-v2.md` → untracked draft plan; no implementation
  has occurred. SHA-256 is recorded above.
- `handoffs/HANDOFF-2026-07-21-review-economy-claude-audit.md` → this untracked
  cold-review brief.
- No tracked file was changed for this review.

## Verified gates

- Independent audit: `REPLAN`.
- Current plan hash: verified as
  `c303bdfc4426aa5ea0227e64e290a982b55a068df48b2f4d20e0e5b74caf3bc4`.
- Git state before this handoff: only
  `?? plans/PLAN-review-economy-v2.md`.
- Full test suite: unverified for this review-only task; no implementation or
  tracked source changed.
- Phase 6A's previously closed gates are historical evidence only; do not treat
  them as gates for this proposed policy change.

## Third-party tool risks

None reported. No installer or external plugin ran.

## Independent-audit findings Claude must challenge

### 1. Governance may be under-classified

The plan declares its software-dev policy slice Class B. However, it changes
when SW-G3 may reuse a verdict even though the current gate rejects verdicts on
a stale diff. `docs/contracts/evolution.md` EV3.C classifies enforcement capable
of weakening gates and unknown impact as Class C, requiring immutable inputs,
named authority, two independent reviews, full cross-component regression,
rollback rehearsal, an effective-from boundary, and a decision record. It also
says a policy cannot approve a proposal weakening itself unless routed through
its Class C parent. The current `software-dev-policy/1` registry entry only
allows A/B, so Claude must resolve the actual Class C parent/authority rather
than assuming Slice A can approve itself.

Evidence:

- `domains/software-dev/gates.md`, SW-G3
- `docs/contracts/evolution.md`, EV3.C and EV4
- `registry/evolution.json`, `software-dev-policy/1`
- current plan §§3–4

### 2. The broad exception may not yield the claimed savings

The only durable task record does not attribute each of the reported Phase 6A
invocations to a candidate. `benchmarks/scorecard.jsonl` records terminal
verdicts, not the claimed `8 software / 3 security / 4 QA` invocation ledger.
Git history contains the initial contract proposal plus multiple later
normative contract candidates (`4c520b6` through `0213833`). Under the draft's
own semantic-intersection rule, those candidates still invalidate software
review. The closure commit `8748b00` also changed contract tests, so it is not a
pure authority-only example.

Claude should reconstruct as much of the 15-invocation baseline as durable
evidence permits. If exact reconstruction is impossible, mark the baseline
partial and do not claim a predicted token or invocation reduction.

### 3. Current governance still routes evidence paths through review

`maintainer-policy/1` requires `full-script-regression` and
`software-dev-reviewer`. Proposal gates and reviewers must exactly match the
resolved policy. Therefore the plan's `evidence_only` and `authority_closure`
rows cannot silently bypass those requirements. Either a correctly routed
Class C change authorizes a narrow exception, or those rows do not save the
review invocation they claim to avoid.

### 4. The proposed classifier is underspecified and expensive

The plan describes a manifest and responsibility taxonomy but not an operative,
single-source classifier. Missing or ambiguous items include:

- schema revision and canonical candidate/delta digest;
- exact changed-path set and authority-path bucket;
- rename, deletion, and file-mode semantics;
- dirty-worktree identity;
- canonical source ownership for path/byte/trigger mappings;
- how `test_only` mechanically proves a test became stricter.

Copying mutable registry/charter rules into policy prose risks drift. Structural
tests of the prose do not create an executable classifier.

### 5. Internal consistency problems

- Security trigger examples do not exactly preserve the current charter's
  uploads/path handling, permission, and payment/money triggers.
- Generic specialist responsibility resolution is not defined.
- Every semantic findings fix starts a successor epoch, but the retry ceiling
  counts returns within one epoch; the counter can reset before it fires.
- The phase report is asked to contain verdict IDs and review-round counts that
  do not exist until after review. This conflicts with the lesson that review
  receipts belong in a later appendix/commit, not inside the reviewed artifact.
- `docs/agent-workflow.md` requires QA → code → conditional security →
  regression QA. The plan makes the final regression optional/at-most-once and
  omits `docs/agent-workflow.md` and `domains/software-dev/loop-profile.md` from
  its file list.

### 6. Acceptance, observation, and rollback are incomplete

The plan lacks a real-task observation window, a measured invocation-reduction
threshold, and a zero-stale-verdict acceptance threshold. Its rollback section
only reverts commits; it does not append corrective governance decisions,
invalidate open reuse records, restore the effective boundary, or run the
canonical maintainer chain afterward.

## Candidate simpler alternative for Claude to evaluate

Prefer a narrow `post_review_append` exception instead of a general verdict
cache and eight-surface taxonomy:

1. Freeze implementation, tests, policy, spec, and contract at one committed
   Git tree.
2. Run the current independent chain unchanged, including final regression QA.
3. Any later code, contract, policy, spec, test, gate, fixture, handoff prose,
   receipt prose, rename, deletion, mixed delta, or unknown path invalidates the
   chain from the earliest applicable stage.
4. Reuse feature verdicts only when a later commit changes exclusively an exact
   allowlist of mechanically validated records:
   - one schema-valid append-only scorecard record; and/or
   - one authorized decision record whose artifact hash equals the reviewed
     artifact and whose appointment/policy/gate references validate.
5. Prove append-only byte-prefix preservation and validate the specific record.
   Any failed assertion returns to the ordinary full chain.
6. Split evidence into:
   - immutable pre-review candidate manifest: candidate commit/tree, exact
     changed paths, gate evidence, required roles;
   - later append-only review ledger: role, candidate, full/findings-scoped,
     triggering delta, verdict, elapsed time if known, reuse/closure receipt.
7. Count retry returns across the whole task/candidate chain, not per semantic
   epoch.
8. Route the candidate policy under the current policy through the correct
   Class C parent, two independent reviews, rollback rehearsal, observation
   window, and effective-from boundary.
9. Before accepting any broader taxonomy, replay Phase 6A and require:
   - zero stale or missing required verdicts;
   - 100% mechanical rejection of mixed/ambiguous deltas;
   - at least 5 fewer invocations than the known 15-invocation proxy baseline.

Known comparison bounds only:

- reported Phase 6A proxy: 8 software + 3 security + 4 QA = 15;
- theoretical clean canonical chain: 2 QA + 1 software + 1 security = 4;
- tokens: unknown;
- neither figure is a defensible expected result without a candidate-bound
  invocation ledger.

## Claude review deliverable

Return exactly one verdict: `BEST_AS_WRITTEN`, `IMPROVE`, or `REPLAN`.

Then provide:

1. Which independent-audit findings above are valid, overstated, or wrong,
   with repo citations.
2. Whether the broad taxonomy or narrow `post_review_append` exception is the
   better first change, considering benefit, complexity, and quality risk.
3. The exact governance class, parent policy, reviewers, gates, authority, and
   observation/rollback requirements.
4. A minimal file list and phased plan for the preferred option.
5. A Phase 6A replay table if it can be reconstructed; otherwise identify the
   missing evidence explicitly.
6. Expected reviewer-invocation impact using known counts only; tokens remain
   `unknown`.
7. Any simpler alternative that preserves the canonical final regression.

Review only. Do not edit files, create proposals, implement policy, change
model pins, or implement Telemetry v3.

## Next steps

1. `handoffs/HANDOFF-2026-07-21-review-economy-claude-audit.md` → give Claude
   this exact instruction: “Review this handoff independently, then review the
   referenced plan and repository evidence. Follow the Claude review deliverable
   exactly. Do not edit files.”
2. `plans/PLAN-review-economy-v2.md` → after Claude's verdict, compare its
   recommended scope with the current SHA-256; do not patch before the user
   chooses broad versus narrow scope.
3. `docs/contracts/evolution.md` and `registry/evolution.json` → resolve the
   correct Class C routing before any implementation proposal is created.
4. If Claude recommends a rewrite, create a new reviewed plan revision and
   present its new SHA-256 for explicit maintainer approval.

## Traps

- Do not confuse dat-kit policy with Codex runtime behavior.
- Do not invent per-agent token totals; this runtime does not expose them.
- Do not treat a changed test suite as decisive evidence approving its own
  proposal (`EV3.B` self-certification rule).
- Do not let a proposed weaker policy approve itself; the current policy and
  correct parent authority govern the transition.
- Do not place future review verdicts inside the artifact they review; use a
  later append-only ledger/appendix.
- Do not call a commit `authority_closure` when it also changes tests, prose,
  policy, or any other non-allowlisted path.
- Do not weaken or omit final regression QA from the canonical maintainer order.
- Keep reviewer model pins unchanged until reliable Telemetry v3 evidence
  exists.

## Glossary

- Review Impact Manifest
- review epoch
- verdict invalidation
- post_review_append
- candidate-bound review ledger
- SW-G3
- Class B
- Class C
- effective-from boundary
- same-proposal self-certification
