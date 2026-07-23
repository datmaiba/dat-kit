# Review Economy v3 — measure first, narrow closure only if proven

**Status:** DRAFT FOR INDEPENDENT CLAUDE REVIEW — not approved for execution

**Date:** 2026-07-21

**Supersedes:** nothing until approved; `PLAN-review-economy-v2.md` remains an
unapproved historical draft

**Scope:** dat-kit review orchestration and evidence; no Codex-runtime change

## 1. Decision requested

Review and approve, revise, or reject this two-stage approach:

1. **Measure-first operation:** use the current canonical review chain on a
   frozen candidate, reuse one compact review packet sequentially, and record a
   candidate-bound invocation ledger for three real tasks. This stage changes no
   review policy and skips no required role.
2. **Conditional narrow amendment:** only if the observation proves that
   mechanically pure post-review closure records restart feature review, add a
   Class C `post_review_append` exception. Do not implement the broad verdict
   cache, semantic epochs, or responsibility-surface taxonomy proposed by v2.

The default outcome is **no policy change** when the measured cost is caused by
real semantic candidates or unstable review input rather than closure-only
appends.

## 2. Why v2 is not ready

The previous draft proposed four impact classes, verdict reuse across semantic
epochs, an eight-surface taxonomy, and a multi-record Review Impact Manifest.
One plan reviewer approved it after findings-scoped fixes. A later fresh audit,
explicitly told not to trust that verdict, returned `REPLAN`. The load-bearing
findings were independently checked against the repository:

1. **Governance:** changing when SW-G3 accepts or reuses a verdict can weaken
   enforcement. `docs/contracts/evolution.md` EV3.C requires Class C handling,
   while `software-dev-policy/1` currently allows only A/B and cannot approve a
   weakening of itself.
2. **Canonical order:** `docs/agent-workflow.md` requires implementation → QA →
   code → conditional security → regression QA. V2 made final regression
   optional/at-most-once rather than unconditionally preserving this order.
3. **Evidence gap:** Phase 6A's `8 software / 3 security / 4 QA` count is a
   session reconstruction, not a durable candidate-bound ledger.
   `benchmarks/scorecard.jsonl` records terminal verdicts only.
4. **Real semantic churn:** Git history contains the initial contract candidate
   plus multiple normative contract revisions from `4c520b6` through `0213833`.
   Those reviews are not safely removable by verdict caching.
5. **Closure was mixed:** commit `8748b00` changed contract tests as well as
   closure evidence, so it is not a valid pure-authority-append example.
6. **Classifier gap:** V2 did not define an operative canonical classifier for
   dirty trees, renames, deletions, modes, exact byte deltas, or the claim that
   a test became stricter.
7. **Self-reference:** its phase-report manifest contained future verdict IDs
   and review rounds. `lessons-learned/lessons-learned.md` requires verdict
   receipts to live in a later appendix/commit, not inside the artifact being
   reviewed.
8. **Retry bug:** each semantic fix started a successor epoch while the retry
   ceiling counted returns inside one epoch, allowing the counter to reset.

These findings justify narrowing the first change rather than adding more fixes
to the general taxonomy.

## 3. Ground truth and known baseline

### Binding rules that remain unchanged

- Engine sequence: LOAD → SELF-QUESTION → PLAN → EXECUTE → VERIFY → REVIEW →
  REPORT → HARVEST.
- Maintainer review order: plan audit → implementation → QA → code review →
  conditional security review → regression QA.
- R1: reviewers run sequentially, never in parallel.
- R2: reviewers receive the frozen diff, changed files, relevant contract
  clauses, and pasted/linked gate evidence—not a whole-repository rediscovery.
- R3: round 2+ is findings-scoped.
- R4: code/security reviewers are static-only and reports stay capped.
- QA remains the runtime/gate owner; a packet or checker cannot issue
  `PHASE DONE`.
- Reviewer model pins remain unchanged until trustworthy Telemetry v3 evidence
  exists.

### Counts known from Phase 6A

| Role | Reconstructed invocations | Durable per-candidate attribution |
|---|---:|---|
| software review | 8 | unavailable |
| security review | 3 | unavailable |
| QA | 4 | unavailable |
| total | 15 | unavailable |

Tokens are `unknown`; the current runtime exposes no reliable per-agent token
counter. The earlier approximately 284k parallel-review incident is a separate
historical estimate and must not be presented as Phase 6A telemetry.

No expected savings may be claimed from these counts until each invocation is
bound to a candidate and trigger.

## 4. Scope

### In scope

- freeze review input before invoking QA;
- ensure all planned implementation, contract, policy, tests, and fixtures land
  before the semantic review freeze;
- provide every reviewer the same compact, candidate-bound packet sequentially;
- record one row per review invocation in the task report/handoff during the
  observation window;
- distinguish semantic churn from mechanically pure post-review appends;
- decide from observed evidence whether a narrow Class C amendment is useful.

### Out of scope

- general verdict caching or responsibility-surface inference;
- skipping a required QA, code, security, specialist, governance, or final
  regression role;
- treating tests, handoffs, receipts, policy prose, or mixed commits as cheap
  closure;
- changing `engine/work-loop/ENGINE.md`, reviewer model pins, or domain loop
  ceiling;
- implementing `scripts/telemetry.py`, a telemetry producer, or inferred token
  accounting;
- weakening Class B/C evidence, authority, observation, or rollback rules.

## 5. Stage A — measure-first operation with current policy

Stage A is an operational experiment under the current contract. It creates no
new acceptance rule and cannot authorize verdict reuse on a changed semantic
candidate.

### A1. Freeze the candidate

Before QA starts:

1. Land every planned source, contract, policy, test, fixture, and generated
   projection in the candidate.
2. Require a clean committed Git tree. Dirty worktrees are ineligible for the
   observation experiment.
3. Record `base_commit`, `candidate_commit`, `candidate_tree`, and the exact
   `git diff --name-status` result, including renames/deletions.
4. Run the declared pre-review gates and store concise results plus locators to
   full logs; do not paste large logs into reviewer context.

### A2. Use one frozen review packet

The packet is immutable for one candidate and contains:

```text
packet_revision
task_id
goal
non_goals
base_commit
candidate_commit
candidate_tree
changed_paths_with_status
applicable_contract_refs
gate_result_summary_and_log_refs
security_trigger_decision
known_risks
open_finding_ids
```

QA, code, and conditional security receive this same packet in canonical
sequence. A semantic/test/policy/gate/fixture change creates a new candidate and
packet. A findings fix creates a concise delta note linked to the original
packet; it does not claim inherited gates ran on the new candidate.

Until a separately approved runner exists, the packet is assembled manually.
It is context compression, not a gate or verdict.

### A3. Preserve the complete chain

For every observed task:

1. plan audit;
2. implementation and focused builder tests;
3. QA runs all canonical gates and attacks the frozen candidate;
4. code review;
5. conditional security review when current trigger surfaces apply;
6. findings-scoped fixes/re-reviews as currently required;
7. one final regression QA on the final frozen candidate;
8. REPORT and HARVEST.

No post-review scorecard append is treated as a new feature candidate merely
because HARVEST occurs after REVIEW; this is the existing engine phase order,
not a new verdict-reuse rule. If current governance is interpreted otherwise,
record the disagreement as evidence and stop before inventing an exception.

### A4. Candidate-bound invocation ledger

The task report/handoff appends one row per invocation after the reviewed
artifact, never inside it:

```text
task_id
invocation_ordinal
reviewer_role
candidate_commit
candidate_tree
full_or_findings_scoped
trigger
originating_finding_ids
verdict
elapsed_time_if_known
token_status=unknown
invalidation_reason_or_none
```

This is a manual observation record, not a new active telemetry signal or a
replacement for Telemetry v3. Claude must decide whether recording it in the
existing task report/handoff is sufficient under current governance; if a new
durable schema/file is required, that addition must be routed separately and
cannot self-certify its own proposal.

### A5. Observation window

Observe three substantive tasks, or stop earlier after three consecutive tasks
with no closure-driven repeat. For each task calculate:

- total invocations by role;
- number caused by a new semantic/test/policy/gate candidate;
- number caused by a numbered reviewer finding;
- number caused only by a post-review append;
- stale/missing required verdict count;
- mixed/ambiguous delta count;
- elapsed time when available;
- tokens as `unknown` unless a trusted runtime supplies exact attribution.

### A6. Stage A exit decision

- **No post-review-only repeat observed:** close the experiment with no policy
  change. Improve candidate stability or packet discipline instead.
- **Repeat involved code, tests, policy, contract, fixture, handoff prose, or
  mixed paths:** classify it as legitimate review-affecting work; do not create
  an exception.
- **Mechanically pure closure append repeatedly restarted feature review:**
  proceed to Stage B only after user approval and correct Class C routing.
- **Evidence cannot distinguish causes:** remain fail-closed and collect more
  observations; do not infer savings.

## 6. Stage B — conditional narrow `post_review_append` amendment

Stage B is not pre-approved by approval of Stage A. It requires a new plan
revision and explicit approval after observation evidence exists.

### B1. Eligibility

A later commit may preserve already-complete feature verdicts only when every
condition below is mechanically proven:

1. Its ancestry resolves to the exact clean candidate that completed the full
   canonical review chain and final regression QA.
2. The changed-path set is a subset of an exact allowlist approved by the Class
   C policy. Initial candidates for review—not automatic approval—are:
   - `benchmarks/scorecard.jsonl`;
   - `docs/decisions/evolution-manual.decisions.jsonl`.
3. Each changed file preserves the complete prior byte prefix and appends
   exactly one terminal-LF JSON object; no earlier byte, encoding, or newline is
   rewritten.
4. The scorecard record passes the existing production scorecard validator.
5. An evolution decision passes a production governance validator that checks
   proposal identity, policy revision/hash, appointment, closer separation,
   required gates/reviewers, valid transition, effective-from boundary, and the
   exact artifact/input hashes.
6. There is no rename, deletion, file-mode change, untracked input, second
   append, handoff/prose/test change, or mixed delta.
7. Any missing data, unsupported path, or validator disagreement rejects the
   exception and restores the ordinary current-policy chain.

The allowlist is closed. `handoffs/`, receipt prose, tests, fixtures, plans,
contracts, policy, generated projections, and unknown paths are explicitly not
eligible.

### B2. Evidence split

- **Pre-review candidate manifest:** immutable candidate identity, exact path
  list, required roles, and gate evidence locators. It contains no future
  verdict IDs.
- **Post-review ledger/closure receipt:** appended later and binds verdicts to
  the reviewed candidate. It may cite the candidate; the candidate never cites
  its future receipt.

### B3. Governance prerequisite

Treat the amendment as Class C because it changes enforcement and may change
governance policy. The current policy governs the transition; the candidate
rule cannot approve itself.

Registry routing currently shows:

| Surface | Current route |
|---|---|
| `docs/contracts/evolution.md` | `platform-contract-policy/1`, Class C |
| `registry/evolution.json` | `platform-contract-policy/1`, Class C |
| `scripts/registry.py` | `platform-contract-policy/1`, Class C |
| `domains/software-dev/*` | `software-dev-policy/1`, Class B only |
| `docs/agent-workflow.md` and general scripts | `maintainer-policy/1`, Class B only |

Before implementation, resolve whether `platform-contract-policy/1` is the
declared Class C parent for the child-policy transition. If no explicit parent
link/authority exists, STOP and amend governance first; do not route a
cross-policy patch through convenience.

At minimum the Class C proposal owes:

- immutable baseline and exact input hashes;
- platform-owner authority and effective-from-run boundary;
- knowledge-work and software-dev independent reviews, or the exact approved
  equivalent named by current policy;
- full cross-component regression;
- rollback rehearsal;
- an observation window and decision record with exact policy revision/hash;
- policy-owner-separated proposals/slices where the registry requires them;
- no same-proposal self-certification by a newly created checker or test.

### B4. Conditional implementation surfaces

Claude must minimize and confirm this list after resolving governance:

#### Platform Class C slice

- `docs/contracts/evolution.md` — define the exact closure exception and parent
  authority semantics.
- `registry/evolution.json` — register parent/child routing, allowlist owner,
  gate/reviewer/authority requirements, and effective revision.
- `scripts/registry.py` or a newly registered registry-owned module — production
  validation for proposal/decision/closure eligibility. The current production
  registry validates catalog structure and path routing but does not validate
  manual proposal/decision lifecycle records; only a Phase 1A spike contains
  such validation today.
- focused registry/evolution tests — negative cases first.

#### Child policy slices, only if the Class C parent requires them

- `docs/agent-workflow.md` — preserve the canonical review order and state the
  post-review boundary without making regression optional.
- `domains/software-dev/reviewers.md`, `gates.md`, and `loop-profile.md` — modify
  only if the exception changes their binding semantics; otherwise leave them
  byte-identical.
- reviewer charters — modify only if their operative input/output changes;
  otherwise leave them byte-identical.

Do not change the engine, model pins, loop ceiling, or Telemetry v3.

## 7. Stage B tests and attacks

The operative checker, not prose assertions alone, must fail before it is
trusted green. Required negative cases:

1. mixed decision append plus test change;
2. modified earlier JSONL byte;
3. two appended records when exactly one is allowed;
4. missing terminal LF or encoding change;
5. rename, deletion, or file-mode change;
6. stale candidate/tree/artifact hash;
7. dirty or untracked input;
8. unknown path;
9. unauthorized/revoked/wrong closer;
10. same proposer and closer;
11. missing or stale required gate/reviewer evidence;
12. invalid decision transition or effective-from boundary;
13. candidate without final regression QA;
14. candidate-policy self-approval;
15. test, handoff, receipt prose, policy, or contract mislabeled as closure.

Positive cases are limited to one valid scorecard append and one valid
authorized decision append, each on an exact fully reviewed candidate.

The proposal's new tests/checker are supporting evidence only. Decisive evidence
must come from the pre-existing contract/baseline, independent reviews, full
cross-component regression, and rollback rehearsal required by current Class C
policy.

## 8. Acceptance criteria

### Stage A

- three observed tasks or the early-stop condition completed;
- every invocation bound to an exact candidate and trigger;
- zero stale or missing required verdicts;
- current canonical final regression present on every final candidate;
- tokens reported as exact only when trustworthy, otherwise `unknown`;
- no policy or model-pin change made from unmeasured assumptions.

### Stage B, if opened

- 100% rejection of every mixed, unknown, stale, or malformed negative case;
- zero stale or policy-missing verdicts in replay and dogfood;
- exact current-policy Class C evidence and authority complete;
- one real task dogfood after the effective-from boundary;
- rollback rehearsal restores the ordinary full-chain behavior;
- append-only corrective decision records preserve all historical evidence;
- broader verdict caching remains deferred unless at least three observed tasks
  demonstrate a plausible reduction of five or more invocations versus the
  known 15-invocation proxy without skipping required review.

The theoretical clean-chain floor of two QA invocations, one software review,
and one security review is four. It is not a promise or a comparable Phase 6A
result because Phase 6A had multiple semantic candidates.

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Optimizing a reconstructed count | Stage A candidate-bound ledger before policy |
| Stale verdict reuse | Stage A performs no reuse; Stage B is exact allowlist + fail-closed checker |
| Governance self-approval | current Class C parent, two reviews, independent decisive evidence |
| New framework costs more than it saves | Stage B opens only on repeated measured closure cost |
| Tests land after review freeze | candidate freeze requires all tests/fixtures first |
| Scorecard append confused with telemetry | manual invocation count; no token inference or telemetry producer |
| Decision validator duplicated from spike | promote/design one production owner; do not copy mutable rules into prose/tests |
| Final regression weakened | canonical regression QA remains mandatory and explicitly tested |

## 10. Rollback

Stage A needs no policy rollback: stop the observation and retain factual task
reports/handoffs.

If Stage B is implemented:

1. append the corrective/rollback governance decision; never rewrite history;
2. invalidate every open `post_review_append` reuse record from the rollback's
   effective boundary;
3. revert child slices before the platform Class C slice in owner-separated
   commits/proposals;
4. restore the ordinary current-policy review chain for every later delta;
5. run the canonical maintainer chain and full cross-component regression;
6. preserve old proposal, decision, observation, and rollback evidence.

## 11. Claude independent-review contract

Review this file as a cold reader. Read the repository sources named below and
do not rely on the prior Codex verdict:

- root `AGENTS.md`, `docs/agent-workflow.md`, and
  `docs/agent-working-rules.md`;
- `engine/work-loop/ENGINE.md`;
- all six `domains/software-dev` slots and operative reviewer charters;
- `docs/contracts/evolution.md` and `registry/evolution.json`;
- `scripts/registry.py`, scorecard validator/writer, and Phase 1A evolution
  validation spike;
- `plans/PLAN-v7-platform.md` §16;
- `lessons-learned/lessons-learned.md`;
- Phase 6A commits, scorecard entry, and relevant handoffs.

Return exactly one verdict: `BEST_AS_WRITTEN`, `IMPROVE`, or `REPLAN`.

Then answer:

1. Is Stage A truly policy-neutral under the current engine and governance, or
   does even its manual ledger require a governed proposal?
2. Does REPORT/HARVEST already permit scorecard append without reopening
   REVIEW, making a scorecard exception unnecessary?
3. Is there durable evidence of a pure authorized-decision append causing a
   redundant feature review?
4. Is `platform-contract-policy/1` the correct Class C parent for any Stage B
   child-policy transition? If not, name the exact route or blocker.
5. Can Stage B be smaller—possibly evolution-decision validation only—without
   changing the software-dev Domain Pack?
6. Are the allowlist, candidate identity, byte-prefix proof, negative tests,
   acceptance thresholds, observation window, and rollback sufficient?
7. Which files can be removed from the conditional implementation scope?
8. What reviewer-invocation reduction is defensible from known evidence?
   Tokens must remain `unknown`.

Review only. Do not edit files, create proposals, implement policy/checkers,
change model pins, or implement Telemetry v3.

## 12. Sources consolidated by this file

- `plans/PLAN-review-economy-v2.md` — broad draft retained for history.
- `handoffs/HANDOFF-2026-07-21-review-economy-claude-audit.md` — independent
  audit brief retained for provenance.
- `handoffs/CONTEXT-2026-07-18-lean-dat-kit-improvement.md` — existing frozen
  review-packet, final-receipt, and token-discipline guidance.

This v3 document is the single file Claude needs for the next review. The source
files remain unchanged and must not be deleted until v3 is independently
reviewed and explicitly approved.
