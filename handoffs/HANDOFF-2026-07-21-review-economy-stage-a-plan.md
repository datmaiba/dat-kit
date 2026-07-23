# HANDOFF 2026-07-21 — Review Economy Stage A plan audit

**Current phase:** PLAN — independent Claude audit pending

**Execution authorization:** none; Stage A has not started

**Stage B:** closed; no design or implementation is authorized

## Goal

Give a cold Claude reviewer one compact file containing the current state and
the next-step plan. Stage A measures reviewer invocations across three real
software tasks while preserving every current quality and authority rule. It
does not change verdict validity, reviewer routing, or policy.

Success for this handoff means Claude can review the plan in under five minutes
without opening the earlier v2/v3 drafts. Those files are provenance only.

## Runtime

`codex / GPT-5`; next reviewer: Claude, model unspecified.

## Workflow

`dat-kit:build-loop` for the plan and one fresh independent review;
`dat-kit:handoff` for this cold-start artifact.

## Canonical contract

`dat-kit 1.16.0`, from root `AGENTS.md`.

## Git state

- Branch: `feature/telemetry-v3`
- HEAD: `8748b00eee562bb7730035f7520dbf0680b03edb`
- Phase 6A contract SHA-256:
  `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde`
- Worktree: dirty only with untracked planning/handoff artifacts; no policy,
  engine, reviewer charter, test, or telemetry implementation is modified.

## State

### DONE

1. Phase 6A contract-only work is closed at HEAD; `scripts/telemetry.py` and
   `telemetry/` remain absent.
2. Review Economy v2 was rejected as too broad because of governance,
   stale-verdict, classifier, and regression-order risk.
3. V3 narrowed the direction to measure-first but remained too long and
   designed Stage B before evidence existed.
4. One new independent agent reviewed v3 for correctness and context cost. Its
   verdict was `IMPROVE`.
5. This handoff incorporates that review and becomes the single next-session
   entrypoint.

### IN PROGRESS

1. Independent Claude audit of this Stage A plan only.
2. Explicit maintainer approval after Claude returns a verdict.

### NOT STARTED

1. Stage A observation on a real task.
2. Any new schema, signal, checker, policy, proposal, or authority change.
3. Stage B. It may be planned separately only after measured evidence shows a
   repeated, mechanically pure closure-only review restart.

## Decisions in effect

- No `spec/08-decisions.md` exists.
- Stage A is policy-neutral only while its packet and ledger remain task-local
  operational notes. Registering a schema/signal, using the ledger as gate or
  authority evidence, or changing verdict validity requires separate governance.
- Canonical order remains: plan audit → implementation → QA → code review →
  conditional security review → final regression QA.
- R1–R4 remain binding: sequential only; frozen diff scope plus gate evidence;
  findings-scoped re-review; static-only code/security review with capped output.
- QA remains runtime/gate owner. No packet or ledger may issue `PHASE DONE`.
- REPORT/HARVEST follows REVIEW. A normal scorecard append does not by itself
  create a new feature candidate, but its specific validator or `validate.py`
  must run after append before claiming final green.
- Tokens remain `unknown` unless the runtime supplies exact attribution.
- Reviewer model pins, engine, loop ceiling, and Telemetry v3 remain unchanged.
- Stage A observations may motivate a later proposal; they cannot authorize
  verdict reuse or approve a weaker policy.

## Stage A next-step plan

### Scope

Measure why reviewer invocations repeat across three substantive tasks. Reduce
context re-reading with one frozen packet; do not reduce required review roles.

Out of scope: semantic verdict caching, impact-surface taxonomy, new telemetry,
new durable evidence schema, policy changes, model changes, and Stage B design.

### Step A1 — freeze one eligible candidate

Before QA:

1. Land all planned code, contract, policy, tests, fixtures, and projections.
2. Use a clean committed tree; dirty candidates are not eligible.
3. Record base commit, candidate commit/tree, and exact changed paths/status,
   including renames and deletions.
4. Run current declared gates and keep concise results plus log locations.

### Step A2 — reuse one compact packet sequentially

The task-local packet contains only:

```text
task goal and non-goals
base commit; candidate commit/tree
changed paths with status
applicable contract/plan references
gate summary and log locations
security-trigger decision
known risks and open finding IDs
```

QA, code review, and conditional security receive the same frozen facts in
canonical sequence. Any semantic/test/policy/gate/fixture edit creates a new
candidate. A findings fix gets a short delta note linked to the prior packet;
inherited green evidence is never presented as execution on the new candidate.

### Step A3 — run the complete current chain

1. QA runs all canonical gates and task-specific attacks.
2. Code reviewer audits the QA-stable candidate.
3. Security reviewer runs only when current trigger surfaces apply; skip and
   reason are reported explicitly.
4. Fixes receive current findings-scoped re-review.
5. Final regression QA runs on the final frozen candidate.
6. REPORT and HARVEST run; validate any appended scorecard record afterward.

### Step A4 — append a factual invocation ledger after review

Use the existing task report or handoff, not the reviewed artifact and not a new
registered schema. Record one compact row per invocation:

```text
ordinal | role | candidate commit/tree | full/findings-scoped |
trigger/finding IDs | verdict | elapsed if known | tokens=unknown |
invalidation reason or none
```

Future verdict IDs must never be embedded inside the artifact they will review.

### Step A5 — observe and decide

Run Stage A on three substantive tasks, then classify every repeat:

- new semantic/test/policy/gate candidate;
- numbered reviewer finding;
- mechanically pure post-review closure append;
- unknown/ambiguous.

Exit rules:

- No pure closure-only restart → close with no policy change.
- Mixed or semantic restart → legitimate review; improve candidate stability,
  not verdict caching.
- Repeated pure closure-only restart → write a separate Class C plan and seek
  fresh approval; do not execute an exception from this handoff.
- Cause cannot be proven → remain fail-closed and collect more observations.

Stage A acceptance:

- three tasks observed with every invocation bound to an exact candidate;
- zero stale or missing required verdicts;
- final regression QA present for every final candidate;
- all conditional-review skips justified;
- elapsed reported only when known and tokens otherwise `unknown`;
- no policy, schema, signal, model-pin, engine, or telemetry change.

## Files touched

- `handoffs/HANDOFF-2026-07-21-review-economy-stage-a-plan.md` → this untracked
  final plan + handoff; single entrypoint for Claude.
- `plans/PLAN-review-economy-v3-measure-first.md` → untracked expanded source;
  provenance only, not required reading.
- `plans/PLAN-review-economy-v2.md` and the prior audit handoff → untracked
  provenance only.
- Tracked project files → unchanged.

## Verified gates

- Fresh independent v3 audit: `IMPROVE`.
- Audit scope: plan correctness, policy neutrality, next phase, and context cost.
- Full project suite: unverified for this plan-only task; tracked source is
  unchanged.
- This handoff: all 13 mandatory sections present; no trailing whitespace;
  SHA-256 is reported by the creating session, not self-referenced here.
- Claude plan verdict: pending.

## Third-party tool risks

None reported. No installer or external plugin ran.

## Next steps

1. `handoffs/HANDOFF-2026-07-21-review-economy-stage-a-plan.md` → Claude cold-
   reviews this file only and returns the verdict below; no edits or execution.
2. Maintainer reads Claude's blockers and explicitly approves, revises, or
   rejects Stage A.
3. After approval only, a later session selects the next eligible substantive
   task and executes Steps A1–A4 under current policy.
4. After three observed tasks, report facts and either close with no policy
   change or draft a separate governed Stage B plan.

### Claude verdict contract

Return exactly `KEEP`, `IMPROVE`, or `REPLAN`, followed only by blocking defects.
Verify that Stage A:

- changes no policy or verdict-validity rule;
- preserves QA → code → conditional security → final regression QA;
- keeps the packet/ledger task-local and non-authoritative;
- leaves model pins unchanged and tokens `unknown`;
- does not implement `telemetry.py` or design/authorize Stage B.

Do not edit files, execute Stage A, design Stage B, or perform a broad repository
rediscovery. Open a cited source only when this handoff's claim cannot be checked
from the file itself.

## Traps

- A detailed plan does not replace independent plan review.
- Do not rerun reviewers on a moving candidate; freeze first.
- Findings-scoped means prior findings plus directly affected delta, not a fresh
  full repository review.
- Do not infer Phase 6A token totals or expected savings from the reconstructed
  `8 software / 3 security / 4 QA` invocation count.
- Validate scorecard data after append; write success is not validation success.
- Do not place future review receipts inside their reviewed artifact.
- Do not let observation evidence silently become an active signal or gate.

## Glossary

- Stage A
- frozen candidate
- compact review packet
- candidate-bound invocation ledger
- findings-scoped re-review
- final regression QA
- post-review closure append
