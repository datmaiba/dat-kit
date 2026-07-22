# DECISION — Unify Receipt Gate (R1) with Review Economy v3 (Stage A)

**Date:** 2026-07-22 · **Decider:** Dat (maintainer) · **Status:** APPROVED

**Problem this fixes:** two parallel initiatives targeted review-token cost on
the same day without knowing about each other — `PLAN-review-economy-v3-
measure-first.md` (independent review: IMPROVE → findings-scoped KEEP) and
`PLAN-external-verification-receipt-gate-v2.md` (this session; R0 measured,
R1 implemented). Any future session (Codex or Claude) must read this file
before starting new review-cost work.

## The decision

1. **Both plans continue — with assigned roles.** Receipt Gate provides the
   *infrastructure* (CI evidence, `summary.json`, QA read-side). Review
   Economy provides the *measurement and decision discipline* (frozen packet,
   invocation ledger, 3-task observation, exit criteria).
2. **The joint seam:** the RE-v3 packet field
   `gate_result_summary_and_log_refs` is satisfied by the R1 `review-evidence`
   run link + `summary.json` for the candidate SHA. One artifact serves both
   plans.
3. **RG-R2 (3 reviewers → 1 scoped review) is DEFERRED and gated by RE-v3
   Stage A exit.** Collapsing reviewers changes review order; RE-v3 (already
   independently reviewed) freezes review order during measurement. R2 may
   only be proposed after the 3-task ledger exists, shaped by that evidence.
4. **RG-R3 (receipt authority / GREEN path) remains deferred indefinitely**
   per R0: GREEN-eligible rate at the review-unit level is ~16% and those
   tasks already run reduced chains. Revisit only if the work profile shifts.
5. `PLAN-external-verification-receipt-gate-v1.md` is **superseded** by v2
   (kept for history, do not execute from it).

## Unified sequence, gates, and model assignment

| # | Step | Gate to proceed | Executor / model |
|---|---|---|---|
| 1 | Commit + push R1 branch; verify `review-evidence` red→green on real Actions (deliberately break Ruff once, observe red, revert) | Real red AND real green run observed for the branch | **Dat (git push)** + **Claude Sonnet** for CI monitoring/fixes — mechanical, safety-netted by the red/green protocol |
| 2 | Run RE-v3 **Stage A** over the next 3 substantive tasks: frozen candidate, one packet (gate evidence = R1 summary.json link), invocation ledger rows in task handoffs | 3 tasks observed (or early-stop per RE-v3 A5) | Build tasks: whatever the task needs (default **Sonnet**; builder model is not changed by this decision). Packet assembly + ledger bookkeeping: **Sonnet** — clerical. Reviewer agents: **unchanged current pins** (RE-v3 binding rule: no reviewer model change until Telemetry v3 evidence) |
| 3 | **Single decision point:** analyze the ledger to answer (a) does RG-R2's reviewer collapse pay? (b) does RE-v3 Stage B's closure-append exception matter? Produce one written verdict with numbers | Ledger from step 2 complete; verdict written to plans/ | **Fable 5 subagent, one-shot** — this is the load-bearing judgment of the whole program; everything downstream hangs on reading the evidence correctly. Cheap models here are false economy |
| 4a | IF (a) is yes: propose + build RG-R2 | Step-3 verdict + Dat approval | Split: deterministic tests/replay scripts — **Sonnet**; barrier/race regression test + `docs/agent-workflow.md` policy edit — **Fable 5**; independent review of the diff — **Opus or Fable 5** (reviewer never cheaper than builder) |
| 4b | IF (b) is yes: open RE-v3 Stage B (Class C, 15 negative cases, fail-closed checker) | Step-3 verdict + Dat approval + Class C routing resolved per RE-v3 §6 B3 | **Fable 5** for checker + governance surfaces (policy-critical, self-approval traps); **Sonnet** for negative-case test scaffolding; independent review **Fable 5** |
| — | Anything not listed (R3, verdict caching, model-pin changes) | Separate approved plan | — |

Standing rule for all steps: **builder may be cheap; the reviewer of a
policy-touching or concurrency-touching diff may not be cheaper than the
builder.**

## Cleanup owed (from the R1 session's sandbox limits)

- `git worktree prune` + delete stray branch
  `codex/external-verification-receipt-gate` if present as an empty worktree
  leftover; remove `_probe_test.txt` if it exists at repo root.
- The sandbox that authored R1 cannot delete files on this mount; future
  sessions should prefer write/overwrite operations or hand git actions to
  the maintainer.

## Files this decision governs

- `plans/PLAN-external-verification-receipt-gate-v2.md` (adopted, active)
- `plans/R0-feasibility-report.md` (evidence for this decision)
- `plans/PLAN-review-economy-v3-measure-first.md` (active, Stage A next)
- `plans/PLAN-external-verification-receipt-gate-v1.md` (superseded)
- R1 implementation: `.github/workflows/ci.yml` (`review-evidence` job),
  `ruff.toml`, `mypy.ini`, `requirements-review.txt`,
  `scripts/review_summary.py`, `scripts/tests/test_review_summary.py`,
  `docs/agent-workflow.md` ("QA evidence intake" section)
