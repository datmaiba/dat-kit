# Phase 6B B0 governance-admission review

## Reviewed candidate

- Proposal: `proposal-27d40cbf7ff8c9cebe93`
- Policy: `platform-contract-policy/1`
- Policy hash: `868a6ba79241dc15907d7bb72b41a24516c8c6d8eaa14dc5e8308c472242d902`
- Base: `8c8b4e08c9768fe5f78363c77a74a0a11625987c`
- Candidate commit: `4eba5b39cb36b9eac5d4d0e5b6d01d32f78475a8`
- Candidate tree: `0bddd8e0957834155eeae41cae5ffd310c3ec718`

The candidate changes seven paths: the Class C proposal, immutable baseline,
`registry/evolution.json`, one shared evidence-test helper, and three test
files. It adds one governed root (`telemetry`) and one component
(`telemetry-v3-runtime`) with exactly two globs: `scripts/telemetry.py` and
`telemetry/**`. No Telemetry v3 runtime, schema, local event stream, or durable
event data exists in the candidate.

## Path and red-before-green receipts

- Before admission, `telemetry`, `telemetry/schema-v3.json`, and
  `telemetry/events.jsonl` matched zero governed roots; `scripts/telemetry.py`
  matched zero component classes.
- Existing `scripts/tests/**` and all three benchmark surfaces already resolved
  to their existing maintainer components and were not broadened.
- Before the registry edit, the three B0 admission tests produced
  `2 failed, 1 passed`; after the edit they produced `3 passed`.
- On the reviewed candidate, all four positive paths resolve only to
  `telemetry-v3-runtime`, owner `maintainers`, class B,
  `maintainer-policy/1`.
- `telemetry-v3/events.jsonl` and `scripts/telemetry.py.bak` remain
  `EVOLUTION_ORPHAN_PATH`; missing and overlapping component fixtures fail as
  orphan and ambiguity respectively.

## Full regression and reviews

Candidate `4eba5b3`:

- `scripts/validate.py`: PASS.
- `pytest scripts/tests`: `291 passed, 6 skipped`.
- `bash -n scripts/init.sh`: PASS.
- `shellcheck scripts/init.sh`: PASS.
- `git diff --check`: PASS.
- QA: `PHASE DONE`; positive, boundary, missing, ambiguous, frozen-blob,
  lifecycle, duplicate-approval, and runtime-absence attacks PASS. The first QA
  invocation stopped only because `pytest` was not on that agent's PATH; the
  findings-scoped rerun used the installed pytest executable and passed.
- Software-dev review: initial `RETURN TO BUILDER` found current-tree-bound
  historical verification, duplicated evidence assertions, and a lifecycle
  cardinality error. Fix commit `4eba5b3` bound evidence to frozen Git blobs,
  centralized shared assertions, and allowed later append-only lifecycle
  decisions while rejecting duplicate approvals. Findings-scoped re-review:
  `APPROVE`.
- Knowledge-work review: `SOURCED`.
- Security review: `APPROVE`, zero findings. It covered glob boundaries,
  ambiguity, authority/policy hashes, immutable evidence, Git-path construction,
  rollback, and runtime absence.

## Rollback rehearsal

An isolated local clone at candidate `4eba5b3` restored only
`registry/evolution.json` and the admission-specific registry tests from base
`8c8b4e0`, while preserving the proposal, baseline evidence, shared immutable
evidence verifier, and Phase 6A historical verification fix.

Observed after rollback:

- `telemetry/events.jsonl`: `EVOLUTION_ORPHAN_PATH`, zero governed roots.
- `scripts/telemetry.py`: `EVOLUTION_ORPHAN_PATH`, zero component classes.
- No telemetry runtime/root existed.
- Proposal and baseline evidence remained present.
- `scripts/validate.py`: PASS.
- `pytest scripts/tests`: `288 passed, 6 skipped`.
- Bash syntax, ShellCheck, and diff-check: PASS.

This proves the ownership admission and its active-behavior tests can revert as
one slice without deleting append-only governance evidence or weakening the
pre-existing tree.

## Authority gate

Status: **platform-owner approval pending**.

On explicit approval, append
`decision-27d40cbf7ff8c9cebe93-0001` with:

- approval reference
  `appointment/platform-owner-1#proposal-27d40cbf7ff8c9cebe93`;
- gate evidence
  `gate/full-cross-component-regression-4eba5b39` and
  `gate/rollback-rehearsal-4eba5b39`; and
- effective boundary `run-2026-07-22-phase6b-b0-4eba5b39`.

Approval closes B0 only. It does not authorize B1 or create any telemetry
runtime path.

