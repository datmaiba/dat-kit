# External Verification Receipt Gate — v2 (revised)

**Status:** ADOPTED 2026-07-22 — R0 complete, R1 implemented; R2 deferred and
gated by Review Economy v3 Stage A (see
`DECISION-2026-07-22-unify-receipt-gate-and-review-economy.md`); R3 deferred
indefinitely per R0 evidence.

**Date:** 2026-07-22

**Supersedes:** `PLAN-external-verification-receipt-gate-v1.md` (v1 principles retained; v1 sequencing and scope rejected)

**Scope:** externalize deterministic QA / static / security checks out of LLM
reviewer sessions so Codex/Claude reads *results*, not re-runs the work. Same
goal as v1. This revision re-prices the plan against the **actual repo** and
re-sequences it so token savings arrive in days, not after five phases.

---

## 0. Why v2 exists — three findings that change the plan

An independent Fable-5 review ground-truthed v1 against the real repository. Three
facts invalidate v1's sequencing (not its principles):

1. **The repo is PUBLIC** (`datmaiba/dat-kit`, verified). Therefore CodeQL
   default setup is **free** and GitHub Actions minutes are **unmetered**. v1's
   worry about CodeQL licensing and CI cost is moot. This *inverts* an earlier
   recommendation: CodeQL becomes the cheap keep; Semgrep becomes the cut.

2. **The GREEN path is nearly empty for this repo.** Applying v1's own yellow
   triggers (Section 7) to recent history, essentially every substantive commit
   touches lifecycle/append/atomicity/recovery code, schemas, contracts,
   policy, or reviewer-authority — all YELLOW triggers. dat-kit *is* a
   contracts-gates-schemas project; its work profile **is** the yellow list.
   GREEN-eligible commits are basically docs. So v1's headline benefit
   ("green candidates use zero reviewer agents") applies to ~0–10% of real work.

3. **"Tamper-evident" self-computed hashes are not a trust anchor.** Whatever
   writes the receipt can recompute every SHA-256 consistently. The cheaper
   *and* stronger design is to **not trust a local receipt file at all** — have
   the verifier query the GitHub API for the check-run conclusion and artifacts
   bound to the exact candidate commit SHA. GitHub is the anchor; staleness and
   tampering are both closed by construction, and most of v1's rejection matrix
   collapses to "does GitHub have a green run for this SHA?"

**Consequence:** the recoverable savings are NOT the GREEN receipt path. They are
**(a)** eliminating the QA-agent by reading CI results instead of re-executing
checks in-context, and **(b)** collapsing three broad reviewer agents into ONE
scoped, diff-bounded review on yellow. Both need ~20% of v1's machinery.

---

## 1. Decision requested

Approve, revise, or reject this re-sequenced approach:

1. **Measure first** (R0) whether the savings are real for this repo's work
   profile — before building anything.
2. Ship CI evidence + a lightweight summary and switch the QA step to *reading*
   CI results (R1). This is where most savings land.
3. Collapse the three reviewer agents into one scoped yellow review (R2).
4. Build the full receipt/verifier/authority machinery (R3) **only if** R0/R2
   measurements show a GREEN rate that justifies it.

Approving this authorizes R0–R2 only. R3 authority change needs a separate,
smaller decisions-file entry. B2 stays stopped at REPLAN; B3 stays prohibited.

---

## 2. Goals and non-goals

### Goals

1. QA-agent invocations per task → **0** (Codex reads CI results, never
   re-executes green checks in-context). Directly fixes the documented B2 pain:
   "reviewer environment could not reliably locate executables."
2. Substantive-task reviewer invocations **3 → 1** (one scoped yellow review
   instead of QA + code + security agents).
3. Every accepted finding becomes a durable test/rule when mechanically
   expressible (the mechanism that shrinks review need over time).
4. Trust anchored to GitHub for the exact candidate SHA — stale/tampered results
   fail by construction.
5. Governance proportionate to a **solo maintainer**: a reviewed decisions-file
   entry, not a multi-stage authority proposal that itself burns tokens.

### Non-goals

- no B2 product/test edit; no B3 work;
- no claim of token savings before R0 measures them;
- no bespoke tamper-evidence scheme (GitHub API is the anchor);
- no claim scanners prove concurrency/architecture correct;
- no prospective triple dual-run (retrospective replay instead — see R2).

---

## 3. Tooling decisions (re-priced for a public 11.6k-line Python repo)

| Purpose | Tool | Decision vs v1 |
|---|---|---|
| Existing gates | Actions + `validate.py` + pytest + ShellCheck | **Keep** |
| Test evidence | pytest `--junitxml` | **Keep** (built-in, no plugin) |
| Fast defects | Ruff (pinned) | **Keep, make required** — passes fast on this size; enable S (security) rules |
| Type defects | mypy (pinned) | **Keep, report-only + changed-file ratchet.** Budget triage on `telemetry.py` (~1.5k lines) and `contract_check.py` (~1.5k lines) |
| Security scan | CodeQL default setup | **Keep as free advisory** (public repo) — non-blocking, off the latency path |
| Pattern security | ~~Semgrep~~ | **CUT** — overlaps CodeQL + Ruff S-rules; per-rule authoring/triage unjustified at this size |
| Dependency audit | ~~pip-audit gate~~ | **DOWNGRADE to monthly advisory** — `requirements-dev.txt` has 2 deps (PyYAML, pytest); near-zero marginal value as a per-candidate gate |
| Stateful tests | ~~Hypothesis state machines~~ | **DEFER** — deterministic barrier + parametrized tests are the MVP; state machines are a hard, later nice-to-have |
| Evidence | `actions/upload-artifact` (pinned) | **Keep** |
| Result intake | `gh api` / `gh run view` | **Keep, promote to trust anchor** (query the candidate SHA directly) |
| Merge enforcement | required status check | **R3 only** |

Rationale for cuts is measured, not stylistic: fewer overlapping scanners = less
triage noise, less latency, less maintenance for one person.

---

## 4. Re-sequenced phasing

### R0 — Feasibility measurement (half a day, do FIRST)

1. Apply the yellow triggers to the last 30–50 commits; classify each
   GREEN / YELLOW / RED.
2. Pull reviewer token/invocation costs from `benchmarks/scorecard.jsonl`
   (already recorded) as the economic baseline.
3. Produce two projected savings figures: **QA-elimination** and
   **3-reviewers → 1-scoped-yellow**. Report the measured GREEN rate.

**Gate:** if projected savings < the R1–R2 build effort, **stop**. If GREEN
rate is low (expected), that is not a failure — it says "build R1+R2, skip R3."

**COMPLETED 2026-07-22 — see `plans/R0-feasibility-report.md`. Verdict:
PROCEED R1+R2 (R2 later re-gated by Stage A per the unification decision);
DEFER R3; metric = invocation counts + wall time, not tokens.**

### R1 — CI evidence + receipt-lite (1–2 days) — ~70% of the savings

1. Pinned Ruff (required) + mypy (report-only, changed-file ratchet).
2. `pytest --junitxml` + `actions/upload-artifact` (pinned revision).
3. CodeQL default setup enabled as free, non-blocking advisory.
4. Emit a ~15-field `summary.json` (candidate SHA, gate ids + outcomes,
   test collected/passed/failed/skipped, tool versions) — **no schema
   ceremony, no hash matrix yet**.
5. **Change the loop contract:** the QA step = Codex runs
   `gh run view` / `gh api` for the candidate SHA and reads `summary.json`;
   it never re-executes green checks in-context.
6. Deliberately break each gate once, observe red, revert, then trust green.

**Exit / metrics:** QA-agent invocations per task → 0; required-gate CI latency
≤ ~4 min (split fast-required from slow-advisory so CodeQL never blocks the loop);
every gate has observed-red and green evidence.

**IMPLEMENTED 2026-07-22 (steps 1–5): `review-evidence` job in ci.yml,
`ruff.toml`, `mypy.ini`, `requirements-review.txt`, `scripts/review_summary.py`
(+13 tests), "QA evidence intake" section in `docs/agent-workflow.md`.
Step 6 (real red→green on Actions) is owed at first push.**

### R2 — Yellow-collapse (1 day) — the second saving

**GATED: do not start until Review Economy v3 Stage A completes its 3-task
observation and the step-3 verdict approves it (see unification decision).**

1. Replace {QA-agent + code-reviewer + security-reviewer} with: mechanical
   evidence from R1 **plus ONE** scoped Codex review that receives *only* the
   diff, changed-path risk flags, and any failed findings. Name it honestly:
   this is scoped Codex review, not an "external verdict."
2. Encode the three B2 findings as **deterministic pytest regressions**:
   - stale-snapshot finish/resume race → barrier/process test (no sleeps);
   - malformed/deep payload → parametrized structured-error tests
     (Hypothesis deferred);
   - dangling telemetry parent → explicit link/path regression test.
3. **Retrospective shadow, not prospective:** replay the pipeline against
   already-reviewed B1/B2 commits and compare to recorded verdicts in
   `docs/spikes/phase-6b/*-observation.md` + `scorecard.jsonl`. This gets the
   agreement evidence for near-zero reviewer tokens (v1's prospective 3×
   dual-run is the most expensive possible evaluation).

**Exit / metrics:** reviewer invocations per substantive task 3 → 1; invocation
count + wall-time delta vs the Stage A ledger baseline; both B2 regressions
observed red then green; 100% agreement with historical verdicts on
deterministic gates.

### R3 — Verifier + GREEN path (build ONLY if R0 justifies it)

Trigger to build R3: R0/R2 show a GREEN-eligible rate high enough to pay back,
OR the work profile shifts toward routine feature code.

1. Small **stdlib-only** `verify_review_receipt.py` (~few hundred lines) that
   queries the **GitHub API** for the candidate SHA (trust anchor) and enforces:
   required checks concluded green; no skip-count increase; artifacts present.
2. **Verifier-enforced YELLOW (not routing convention)** — hard-fail to yellow
   if the diff touches `.github/workflows/**`, tool configs (`ruff.toml`,
   `mypy.ini`), `scripts/verify_*`, or any existing test file. This closes the
   two worst GREEN-bypass holes (see §5).
3. Negative-test fixtures for every rejection (v1 got this right — keep it).
4. Authority change = **one reviewed `docs/decisions/` entry** + branch-
   protection required check. No standalone Class C apparatus.

**Exit:** retrospective replay shows 100% rejection of stale/incomplete/tampered
fixtures; the decisions entry is approved; the ordinary reviewer chain remains a
fail-closed fallback.

---

## 5. Where bad code can slip through GREEN (and the mitigation)

1. **Test tampering in the same candidate** (weaken/skip/delete existing tests,
   receipt still green) → verifier rejects GREEN if existing test files change or
   skip counts rise → route yellow.
2. **Pipeline self-modification** — on GitHub a `pull_request` run executes the
   PR's *own* workflow file, so a candidate can neuter its gates → **verifier-
   enforced** rejection when the diff touches workflows/configs/verifier, not a
   soft routing trigger.
3. **Spec non-compliance with passing tests** — scanners certify "no mechanical
   defect," not "does what the spec says." GREEN eligibility requires
   new/changed behavior to ship with tests whose IDs the summary lists; anything
   without accompanying tests routes yellow.
4. **Semantic / concurrency / logic bugs** — exactly the class the B2 security
   reviewer caught; scanners are weak here (v1 admits this). Defense is the
   yellow trigger list; risk is trigger drift, so keep triggers **path-based and
   over-inclusive**.
5. **Stale-receipt race** — GitHub-API anchoring on the exact candidate SHA
   closes this by construction.

---

## 6. What is kept from v1 (principles were sound)

Fail-closed posture; checker-can't-self-approve; **observed-red-before-trusted-
green** (v1 EV1 step 5 — excellent, kept verbatim); commit-SHA binding; B2
findings encoded as durable tests; negative-tested verifier; report-only-then-
ratchet for new tools; pinned tool/action versions; the honest non-goal that
scanners cannot prove concurrency correct.

## 7. What is cut or downgraded (and why)

Semgrep (overlap); pip-audit as a gate (2 deps); Hypothesis state machines
(hard, deferred); prospective 3-task dual-run (retrospective replay is cheaper);
standalone Class C authority process (one decisions entry for a solo dev);
bespoke hash rejection matrix (GitHub API anchoring replaces it). CodeQL is
promoted, not cut — it is free here.

## 8. Approval boundary

Approving this authorizes **R0–R2 only** (R2 additionally gated by the
unification decision). R3 (receipt authority) needs a separate reviewed
decisions entry. B2 remains stopped at its security REPLAN threshold; B3
remains prohibited without separate approval.

---

### Appendix — confidence on the load-bearing claims

- Repo public: **verified** (github.com metadata).
- CodeQL free + Actions unmetered on public repos: **high** — confirm in
  Settings → Code scanning (two minutes).
- GREEN rate: **measured** in R0 — 44% per commit but **16% per review-unit**
  (the unit that matters); see `plans/R0-feasibility-report.md`.
- CI latency (~3–5 min CodeQL; ~6–10 min full pipeline): **medium** — the first
  real `review-evidence` run confirms.
- Savings concentrated in QA-elimination + yellow-collapse: **medium-high** —
  the Stage A invocation ledger turns it into a measurement.
