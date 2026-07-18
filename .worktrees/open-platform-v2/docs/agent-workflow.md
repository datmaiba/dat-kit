# Agent workflow — dat-kit maintainers

This document is part of the root `AGENTS.md` contract.

## Execution

Load the approved plan, current Git state, relevant source, and lessons before
editing. Work dependency-first, keep changes commit-sized, and run every declared
gate before reporting completion. Plans and spec amendments require explicit
approval; execution of an already approved plan does not require a second gate.

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
