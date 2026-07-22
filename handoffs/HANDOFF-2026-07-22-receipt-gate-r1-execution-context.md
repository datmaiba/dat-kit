# HANDOFF 2026-07-22 — External Verification Receipt Gate: R1 done, R2 gated, execution context

## Goal

Reduce the token cost of the QA / code-review / security-review chain by moving
deterministic mechanical work into CI and having the agent read a result
(`summary.json`) instead of re-executing checks in-context. This handoff carries
the state needed to (1) finish R1's real-CI verification, (2) run Review Economy
v3 Stage A, and (3) reach the single decision point that shapes R2 — with the
model assignment for each step so a fresh session picks the right agent.

Read first, in order:
1. `plans/DECISION-2026-07-22-unify-receipt-gate-and-review-economy.md` — the
   binding decision and the per-step model table. This is the entrypoint.
2. `plans/PLAN-external-verification-receipt-gate-v2.md` — the adopted plan.
3. `plans/R0-feasibility-report.md` — the measured evidence behind the decision.
4. `plans/PLAN-review-economy-v3-measure-first.md` — the other half of the
   unified program (Stage A is the next executable step).

## Runtime / model policy for this workstream

This workstream deliberately assigns different models to different steps. Do NOT
run the whole thing on one model. Standing rule: **the builder may be cheap; the
reviewer of a policy-touching or concurrency-touching diff may not be cheaper
than the builder.**

| Step | Work | Model / agent |
|---|---|---|
| 1. Finish R1 | Push branch; watch `review-evidence`; do the observed-red→green (break Ruff once, see red, revert) | git push by **maintainer (Dat)**; CI monitoring + any YAML/script fix by **Claude Sonnet** — mechanical, red/green-netted |
| 2. Stage A | 3 substantive tasks under current policy: frozen candidate, one packet (gate evidence = the R1 `summary.json` link for the candidate SHA), invocation-ledger rows in the task handoff | Build work: task's normal builder, default **Sonnet**. Packet + ledger clerical work: **Sonnet**. Reviewer agents: **UNCHANGED current pins** — RE-v3 forbids reviewer-model changes until trustworthy Telemetry v3 exists |
| 3. Decision point | Read the 3-task ledger; answer (a) does RG-R2's 3→1 reviewer collapse pay? (b) does RE-v3 Stage B closure-append exception matter? Write ONE verdict with numbers into `plans/` | **Fable 5, one-shot subagent** — load-bearing judgment; cheap model here is false economy |
| 4a. R2 (if approved) | deterministic tests + retrospective replay script → **Sonnet**; barrier/race regression test + `docs/agent-workflow.md` policy edit → **Fable 5**; independent diff review → **Opus or Fable 5** | as noted |
| 4b. Stage B (if approved) | Class C checker + governance surfaces → **Fable 5**; 15 negative-case scaffolding → **Sonnet**; independent review → **Fable 5** | as noted |

## Workflow

`dat-kit:build-loop` for any build step; RE-v3 Stage A operating procedure for
step 2 (freeze candidate → one packet → full canonical chain → invocation
ledger). `dat-kit:handoff` at any mandatory stop.

## Canonical contract

`dat-kit 1.16.0`.

## Git state

- Intended branch for R1: `codex/external-verification-receipt-gate` off
  `master` (`f3cf0e4`). Create it fresh on the maintainer's machine — see the
  cleanup note; a sandbox-created worktree could not be removed remotely.
- The R1 files are already written into the working tree of `D:\project\dat-kit`
  by the authoring session (writes only; no commit was possible from the
  sandbox because that mount cannot delete files, which git needs for lock
  handling).
- Do NOT touch the `feature/telemetry-v3` branch: it carries 15 unpushed B2
  commits stopped at the security REPLAN threshold. B2 stays stopped; B3 stays
  prohibited.

### Cleanup owed on the maintainer's machine (before committing R1)

```
git worktree list                       # find the locked /tmp/dat-kit-r1 entry
git worktree unlock /tmp/dat-kit-r1     # if path-not-found on Windows, instead:
#   Remove-Item -Recurse -Force .git\worktrees\dat-kit-r1
git worktree prune
git branch -D codex/external-verification-receipt-gate
del _probe_test.txt                     # stray empty probe file at repo root, if present
```

Then create the branch and commit the R1 + unification files:

```
git checkout -b codex/external-verification-receipt-gate master
git add .github/workflows/ci.yml ruff.toml mypy.ini requirements-review.txt \
        scripts/review_summary.py scripts/tests/test_review_summary.py \
        docs/agent-workflow.md \
        plans/DECISION-2026-07-22-unify-receipt-gate-and-review-economy.md \
        plans/PLAN-external-verification-receipt-gate-v2.md \
        plans/R0-feasibility-report.md \
        handoffs/HANDOFF-2026-07-22-receipt-gate-r1-execution-context.md
git commit -m "R1 + unification: receipt-gate CI evidence, QA read-side, unified decision with Review Economy v3"
git push -u origin codex/external-verification-receipt-gate
```

## State

- DONE:
  1. **R0 measured** (see report): GREEN rate 44% per commit but **16% per
     review-unit**; token attribution unavailable (`unsupported_provider` on all
     Codex sessions) → metric is invocation-count + wall-time, not tokens.
     Verdict: PROCEED R1+R2, DEFER R3.
  2. **R1 implemented and locally verified** (writes into the repo tree):
     - `.github/workflows/ci.yml` — new `review-evidence` job (Ruff required,
       mypy report-only, pytest `--junitxml`, validate.py, ShellCheck,
       `summary.json` producer, artifact upload pinned to
       `actions/upload-artifact@b4b15b8…` = v4.4.3 verified via GitHub API,
       fail-if-required-gate-failed step).
     - `ruff.toml` — select `F,E9,S,B`; `scripts/tests/**` ignore `S101/S105/S106`.
     - `mypy.ini` — report-only.
     - `requirements-review.txt` — `ruff==0.15.22`, `mypy==2.3.0` (pinned,
       verified on PyPI).
     - `scripts/review_summary.py` — producer only (reads reports; does not
       execute tools); two Ruff findings (S603/S314) suppressed with
       owner+reason+review-condition, not blindly.
     - `scripts/tests/test_review_summary.py` — 13 tests, all green locally;
       Ruff clean; mypy clean; CLI exercised green (exit 0) and red (exit 1).
     - `docs/agent-workflow.md` — new "QA evidence intake" section (read-side of
       the contract). Review order/headcount deliberately UNCHANGED.
  3. **Unification decided**: RG v2 + RE-v3 run as one program; RG-R2 deferred
     and gated by RE-v3 Stage A; RG-R3 deferred indefinitely.

- IN PROGRESS / NEXT (step 1):
  1. Push the branch and observe the FIRST real `review-evidence` run.
  2. Do the observed-red→green protocol: introduce one deliberate Ruff
     violation, confirm the job goes red and `summary.json` records
     `gates.ruff.outcome == "fail"` with required-gate failure, then revert and
     confirm green. R1 is not "done" until a real red AND a real green run exist
     for this job (per plan v2 §4-R1 step 6; the repo's own rule
     "a workflow file is not proof CI ran").

- BLOCKED / DEFERRED:
  - R2 (yellow-collapse) — blocked until Stage A's 3-task ledger exists and the
    step-3 Fable verdict approves it.
  - R3 (receipt authority / GREEN path) — deferred indefinitely per R0.
  - B2 / B3 — out of scope, stopped.

## Verified gates (R1, local)

`pytest scripts/tests/test_review_summary.py` → 13 passed. `ruff check` →
all checks passed. `mypy scripts --config-file mypy.ini` → success.
`review_summary.py` CLI → exit 0 on all-pass, exit 1 on ruff-fail. `ci.yml`
parses as valid YAML; jobs = windows-python, validate, review-evidence.
NOT yet verified: a real GitHub Actions run (owed in step 1).

## Decisions / traps carried forward

- Trust anchor for any future R3 is the GitHub API queried by candidate SHA —
  not a local receipt file's self-computed hashes (v2 §0.3).
- CodeQL default setup is free on this PUBLIC repo; enable via Settings →
  Security → Code scanning, not a workflow file — keep it off the required
  latency path.
- Two separate same-day initiatives collided once already; anyone starting
  review-cost work MUST read the DECISION file first to avoid a third parallel
  plan.
- Do not change reviewer model pins or the review order during Stage A.
