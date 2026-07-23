# HANDOFF 2026-07-22 — Review Economy Stage A plan audit (v2)

**Current phase:** PLAN — independent Codex re-review pending

**Execution authorization:** none; Stage A has not started

**Stage B:** closed; no design or implementation is authorized

**Supersedes:** `handoffs/HANDOFF-2026-07-21-review-economy-stage-a-plan.md`
(that file is provenance only). This v2 folds in a Claude plan audit whose
verdict was `IMPROVE`; the six blocking defects it raised (B1–B6) are resolved
in the sections below.

## Goal

Give a cold reviewer one compact file containing the current state and the
next-step plan. Stage A measures reviewer invocations across three real
software tasks while preserving every current quality and authority rule. It
does not change verdict validity, reviewer routing, or policy.

Success for this handoff means a reviewer can audit the plan in under five
minutes without opening the earlier v2/v3 drafts or the v1 handoff. Those files
are provenance only.

## Runtime

`codex / GPT-5`; this v2 was revised by Claude (model unspecified) acting as
plan editor. Next reviewer: `codex / GPT-5`.

## Workflow

`dat-kit:build-loop` for the plan and one fresh independent review;
`dat-kit:handoff` for this cold-start artifact.

## Canonical contract

`dat-kit 1.16.0`, from root `AGENTS.md` (`**Canonical contract revision:**
dat-kit 1.16.0`).

## Git state

- Branch: `feature/telemetry-v3`
- HEAD: `8748b00eee562bb7730035f7520dbf0680b03edb`
- Phase 6A contract artifact SHA-256 (of `AGENTS.md` at HEAD):
  `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde`
  (reviewer: recompute with `git show HEAD:AGENTS.md | sha256sum` to confirm the
  hashed path; if it does not match, treat the hash as unverified).
- Worktree: dirty only with untracked planning/handoff artifacts; no policy,
  engine, reviewer charter, test, or telemetry implementation is modified.

## State

### DONE

1. Phase 6A contract-only work is closed at HEAD; `scripts/telemetry.py` and
   `telemetry/` remain absent (verified: neither path exists at HEAD).
2. Review Economy v2 was rejected as too broad because of governance,
   stale-verdict, classifier, and regression-order risk.
3. V3 narrowed the direction to measure-first but remained too long and
   designed Stage B before evidence existed.
4. One independent agent reviewed v3; verdict `IMPROVE`.
5. The v1 Stage A handoff was audited by an independent Claude; verdict
   `IMPROVE` with six blocking defects (B1–B6).
6. This v2 handoff resolves B1–B6 and becomes the single next-session
   entrypoint.

### IN PROGRESS

1. Independent Codex re-review of this v2 Stage A plan only.
2. Explicit maintainer approval after the reviewer returns a verdict.

### NOT STARTED

1. Stage A observation on a real task.
2. Any new schema, signal, checker, policy, proposal, or authority change.
3. Stage B. It may be planned separately only after measured evidence shows a
   repeated, mechanically pure closure-only review restart (threshold in A5).

## Decisions in effect

- No `spec/` directory exists in this repo; dat-kit here records decisions in
  tracked handoffs, not `spec/08-decisions.md`. **D-SA1:** this handoff and its
  two source plans must be committed to `feature/telemetry-v3` as planning
  artifacts before Stage A executes, so the policy-neutrality constraint below
  does not live only in an untracked file. (Resolves B6.)
- **D-SA2:** Stage A is policy-neutral only while its packet and ledger remain
  task-local operational notes. Registering a schema/signal, using the ledger as
  gate or authority evidence, or changing verdict validity requires separate
  governance.
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

Measure why reviewer invocations repeat across three substantive tasks. Stage A
is **measure-only**. The one packet standardizes the facts each reviewer
receives; Stage A makes **no claim** about how much context re-reading the
packet saves, because there is no pre-packet baseline in this design. The only
quantity guaranteed to be observable is the **count of reviewer invocations and
their classification**; elapsed is recorded only when known and tokens are
always `unknown`. No required review role is reduced. (Resolves B5.)

Out of scope: semantic verdict caching, impact-surface taxonomy, new telemetry,
new durable evidence schema, policy changes, model changes, and Stage B design.

### Step A1 — freeze one eligible candidate

Before QA:

1. Land all planned code, contract, policy, tests, fixtures, and projections.
2. Use a clean committed tree; dirty candidates are not eligible.
3. Record base commit, candidate commit/tree, and exact changed paths/status,
   including renames and deletions.
4. Run current declared gates as an **eligibility pre-check only**. This result
   is **never evidence**: QA at A3.1 must independently re-execute every gate on
   the frozen candidate. In the packet, label this field `pre-check
   (non-evidence)` with its log location. (Resolves B4.)

### Step A2 — reuse one compact packet sequentially

The task-local packet contains only:

```text
task goal and non-goals
base commit; candidate commit/tree
changed paths with status
applicable contract/plan references
gate pre-check summary (non-evidence) and log locations
security-trigger decision
known risks and open finding IDs
```

The packet is a convenience index, **not a source of truth**. Before starting,
each reviewer must independently confirm `base commit`, `candidate commit/tree`,
and `changed paths with status` against `git` on the frozen candidate. Any
packet–repo mismatch **voids** that invocation: record it in the ledger with
`invalidation reason = packet mismatch`, correct the packet, and re-invoke the
reviewer on the unchanged candidate. (Resolves B1.)

QA, code review, and conditional security receive the same frozen facts in
canonical sequence. Any semantic/test/policy/gate/fixture edit creates a new
candidate. Doc-only, comment-only, and scorecard-append changes do **not**
create a new candidate. A findings fix gets a short delta note linked to the
prior packet; inherited green evidence is never presented as execution on the
new candidate. (Resolves B2, in part.)

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

#### A5.0 — candidate delta classification

A restart is `mechanically pure closure-only` **if and only if** the diff
between candidate N and candidate N+1 satisfies **all** of:

- (a) touches no source, test, fixture, policy, contract, or gate-config file;
- (b) touches only report, handoff, scorecard record, or ledger files;
- (c) changes no gate outcome.

Fail any condition → classify `semantic`. Cannot be proven from the diff →
`unknown/ambiguous`. `unknown` is **never** counted as pure. (Resolves B2.)

#### A5.1 — observe

Run Stage A on three substantive tasks, then classify every repeat using A5.0
plus:

- new semantic/test/policy/gate candidate;
- numbered reviewer finding;
- mechanically pure post-review closure append;
- unknown/ambiguous.

#### A5.2 — exit rules (counted)

- `pure closure-only` appears in **0 tasks** → close with no policy change.
- appears in **exactly 1 task** → insufficient; record and keep observing; do
  not draft Class C.
- appears in **≥2 of the 3 tasks** → eligible to write a separate Class C plan
  and seek fresh approval; do not execute an exception from this handoff.
- any task contains `unknown/ambiguous` → that task stays fail-closed and
  contributes no evidence for or against a restart. (Resolves B3.)

Any mixed or semantic restart is a legitimate review; the response is to improve
candidate stability, not to cache verdicts.

Stage A acceptance:

- three tasks observed with every invocation bound to an exact candidate;
- zero stale or missing required verdicts;
- final regression QA present for every final candidate;
- all conditional-review skips justified;
- elapsed reported only when known and tokens otherwise `unknown`;
- no conclusion about context/token savings is drawn from Stage A;
- no policy, schema, signal, model-pin, engine, or telemetry change.

## Files touched

- `handoffs/HANDOFF-2026-07-22-review-economy-stage-a-plan-v2.md` → this
  untracked final plan + handoff; single entrypoint for the next reviewer.
- `handoffs/HANDOFF-2026-07-21-review-economy-stage-a-plan.md` → superseded v1;
  provenance only.
- `plans/PLAN-review-economy-v3-measure-first.md` → untracked expanded source;
  provenance only, not required reading.
- `plans/PLAN-review-economy-v2.md` and the prior audit handoff → untracked
  provenance only.
- Tracked project files → unchanged.

## Verified gates

- Fresh independent v3 audit: `IMPROVE`.
- Independent Claude audit of v1 Stage A handoff: `IMPROVE` (defects B1–B6).
- Repo facts re-verified for this v2: HEAD `8748b00`; worktree dirty only with
  the four untracked planning artifacts; `scripts/telemetry.py` and
  `telemetry/` absent; `AGENTS.md` canonical revision `dat-kit 1.16.0`.
- Full project suite: unverified for this plan-only task; tracked source is
  unchanged.
- This handoff: all 13 mandatory sections present; no trailing whitespace;
  SHA-256 is reported by the creating session, not self-referenced here.
- Codex re-review verdict for this v2: pending.

## Third-party tool risks

None reported. No installer or external plugin ran.

## Next steps

1. `handoffs/HANDOFF-2026-07-22-review-economy-stage-a-plan-v2.md` → Codex cold-
   reviews this file only and returns the verdict below; no edits or execution.
2. Maintainer reads the blockers and explicitly approves, revises, or rejects
   Stage A; on approval, commit this handoff and its two source plans per D-SA1.
3. After approval only, a later session selects the next eligible substantive
   task and executes Steps A1–A4 under current policy.
4. After three observed tasks, report facts and either close with no policy
   change or draft a separate governed Stage B plan.

### Reviewer verdict contract

Return exactly `KEEP`, `IMPROVE`, or `REPLAN`, followed only by blocking defects.
Verify that Stage A:

- changes no policy or verdict-validity rule;
- preserves QA → code → conditional security → final regression QA;
- keeps the packet/ledger task-local and non-authoritative;
- keeps the A1 pre-check strictly non-evidence (B4);
- keeps the packet non-authoritative with a mandatory git reconciliation (B1);
- defines `pure closure-only` by a verifiable diff test (B2);
- gives the Class C exit rule a counted threshold (B3);
- draws no context/token-savings conclusion (B5);
- flushes the policy-neutrality decision to a tracked artifact (B6);
- leaves model pins unchanged and tokens `unknown`;
- does not implement `telemetry.py` or design/authorize Stage B.

Do not edit files, execute Stage A, design Stage B, or perform a broad
repository rediscovery. Open a cited source only when this handoff's claim
cannot be checked from the file itself.

## Traps

- A detailed plan does not replace independent plan review.
- An unverified packet is a silent single point of failure for all three
  verdicts; reconcile it against git before every invocation.
- Do not rerun reviewers on a moving candidate; freeze first.
- Findings-scoped means prior findings plus directly affected delta, not a fresh
  full repository review.
- Do not infer Phase 6A token totals or expected savings from the reconstructed
  `8 software / 3 security / 4 QA` invocation count.
- Validate scorecard data after append; write success is not validation success.
- Do not place future review receipts inside their reviewed artifact.
- Do not let observation evidence silently become an active signal or gate.
- `unknown/ambiguous` is never counted as a pure closure-only restart.

## Glossary (defined inline; no CONTEXT.md exists in this repo)

- **Stage A** — the measure-only observation phase: run the full review chain on
  three real tasks and classify every reviewer repeat; no policy change.
- **frozen candidate** — a clean, committed tree whose base and candidate
  commit/tree and changed paths are recorded and do not move during review.
- **compact review packet** — a task-local, non-authoritative index of frozen
  facts handed to each reviewer; must be reconciled against git.
- **candidate-bound invocation ledger** — one factual row per reviewer call,
  each bound to an exact candidate commit/tree; not a registered schema, not
  gate or authority evidence.
- **findings-scoped re-review** — re-review limited to prior findings plus the
  directly affected delta, not a fresh full-repo review.
- **final regression QA** — the QA pass re-run on the final frozen candidate
  after all fixes.
- **post-review closure append** — a doc/report/scorecard/ledger-only change
  after a verdict; `pure` only when it meets all A5.0 conditions.
