# Agent workflow — dat-kit maintainers

This document is part of the root `AGENTS.md` contract.

## Execution

Load the approved plan, current Git state, relevant source, and lessons before
editing. Work dependency-first, keep changes commit-sized, and run every declared
gate before reporting completion. Plans and spec amendments require explicit
approval; execution of an already approved plan does not require a second gate.

## QA evidence intake (R1 — External Verification Receipt Gate)

The `review-evidence` CI job (`.github/workflows/ci.yml`) runs Ruff, mypy
(report-only), pytest with JUnit output, validate.py, and ShellCheck, and
writes `reports/summary.json` for the candidate commit. For the QA step of
the review order below:

1. Confirm the candidate commit has a completed `review-evidence` run:
   `gh run list --commit <sha> --json databaseId,conclusion,workflowName`.
2. Read that run's `summary.json` artifact
   (`gh run download <run-id> -n review-evidence-<sha>`) instead of
   re-running `pytest scripts/tests` / `python scripts/validate.py` inside
   the session.
3. Treat `gates.<name>.outcome` for every entry in `required_gate_set` as
   the QA verdict. Any non-"pass" required gate, or a missing/stale run for
   the candidate SHA, means QA is NOT satisfied — fall back to running the
   commands locally and report that the evidence job did not cover this
   commit.
4. mypy is report-only (`required: false`) and never blocks QA on its own;
   its finding_count is informational only in R1.

This replaces re-execution of the mechanical checks only. It does not
change, skip, or shorten code review or security review — those still run
per the order below. See `plans/PLAN-external-verification-receipt-gate-v2.md`
for the phases this belongs to and why the reviewer-agent order itself is
untouched until a separately approved R2/R3.

## Review

Use the build-loop review order: plan audit, implementation, QA, code review,
security review when paths, permissions, public input, or external writes are
touched, then regression QA. If independent agents are unavailable, perform a
clearly disclosed fresh-eyes pass against the same charters.

## Contract migration

`scripts/contract_check.py` is the shared source for runtime pointers, contract
diagnostics, brownfield preflight, and evidence enums. Never add an independent
pointer inventory to shell, CI, documentation, or another validator.

All legacy migration is manual. A conflict report must name the diagnostic and
link to `docs/codex.md`; no scaffold path may transform existing policy.

## Reporting and handoff

Report concrete gate counts/results, intentional deferrals, and exact remaining
commands. A paused task uses the handoff skill and records runtime, workflow,
contract revision, Git state, decisions, and verified gates.
