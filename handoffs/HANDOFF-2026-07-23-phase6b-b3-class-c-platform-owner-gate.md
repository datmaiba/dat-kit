# HANDOFF 2026-07-23 — B3 Class C platform-owner gate

## Goal

Complete B3 subset #1 through option-A deferment: make build-loop HARVEST
truthfully `planned/deferred`, remove unsafe authority only after the Class C
decision is effective, and stop before B3 subset #2.

## Runtime

`codex / GPT-5`

## Workflow

`dat-kit:build-loop`; option-A Class C contract slice, then post-effective
Class B cleanup.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- HEAD: `716095a83056a580520ca74deaa6c97b71aebb08`.
- Main worktree is clean except eight pre-existing user-owned untracked
  provenance files; do not stage or edit them.
- Review worktree: `.worktrees/b3-deferment-review`, detached at `83f065e`.
- Rollback worktree: `.worktrees/b3-deferment-rollback`, detached at
  `83f065e` with only its intentionally reverted
  `docs/contracts/telemetry-v3.md`; do not use it for forward work.

## State

- DONE:
  1. Option-A plan approved and recorded in `497069e`.
  2. Class C candidate/proposal frozen in `748b8ac`; canonical-blob proposal
     correction in `83f065e`; evidence ledger in `716095a`.
  3. Exact proposal `proposal-0acfe665bc066c31dd5e` binds only
     `docs/contracts/telemetry-v3.md`, policy
     `platform-contract-policy/1`, policy hash
     `868a6ba79241dc15907d7bb72b41a24516c8c6d8eaa14dc5e8308c472242d902`,
     and candidate contract hash
     `ccd0892f58f96f14d763a4b7fb39017cfa23d77dcf6326fef6f8474a6937bff2`.
  4. Both independent Class C reviews returned `APPROVE`, no findings.
  5. Exact inverse-patch rollback rehearsal restored contract SHA-256
     `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde`.
- IN PROGRESS:
  1. Mandatory `platform-owner` approval and effective-run decision for the
     exact proposal. The candidate is review-ready only; do not treat it as
     effective or start Slice B.
- NOT STARTED:
  1. Append Class C `approved` decision and bind `effective_from_run`.
  2. Slice B observation, net-negative removal of unsafe scorecard/HARVEST
     authority, its QA/code/security/final-QA chain, and closure ledgers.

## Decisions in effect

- Maintainer Dat selected option A: no capability broker, authority ledger,
  Host Adapter implementation, receipt store/resolver implementation, schema
  work, append-internal change, or producer activation.
- HARVEST remains required but `planned/deferred`; all five producer registry
  entries remain `planned`.
- Slice B may start only after the Class C decision has a non-empty effective
  run. No `spec/08-decisions.md` exists in this repository.

## Files touched

- `docs/contracts/telemetry-v3.md` → T3.12/T3.13 deferment wording only.
- `docs/decisions/evolution-proposal-0acfe665bc066c31dd5e.proposal.json` →
  immutable Class C proposal.
- `docs/spikes/phase-6b/b3-harvest-deferment.contract.patch` → canonical
  zero-context patch; apply/reverse requires `--unidiff-zero`.
- `docs/spikes/phase-6b/b3-deferment-class-c-observation.md` → baseline,
  hashes, threat model, reviews, gates, rollback receipts.
- `docs/decisions/evolution-manual.decisions.jsonl` → unchanged; next allowed
  write only after explicit platform-owner approval.

## Verified gates

- Supporting temporary QA in isolated worktree: `9 passed`.
- Exact candidate `83f065e`: `python scripts/validate.py` → `✓ all checks green`.
- Exact candidate: `pytest scripts/tests` → `380 passed, 8 skipped in 26.78s`.
- Cross-component telemetry/CLI/scorecard/producer tests →
  `103 passed, 4 skipped in 4.41s`.
- `bash -n scripts/init.sh` → PASS; `shellcheck scripts/init.sh` → PASS;
  `git diff --check` → PASS.
- Rollback rehearsal: validator PASS; `pytest scripts/tests` →
  `380 passed, 8 skipped in 26.15s`; Bash, ShellCheck, and diff-check PASS.

## Third-party tool risks

none reported

## Next steps

1. Ask Dat Mai Ba, as `platform-owner`, to approve exactly
   `proposal-0acfe665bc066c31dd5e` with proposed effective run
   `run-2026-07-23-phase6b-b3-deferment-83f065e`.
2. On explicit approval, append one closed `approved` record to
   `docs/decisions/evolution-manual.decisions.jsonl` using current RFC 3339
   `decided_at`, closer identity `Dat Mai Ba`, role `platform-owner`, approval
   reference `appointment/platform-owner-1#proposal-0acfe665bc066c31dd5e`,
   policy revision/hash above, and exactly these sorted gate refs:
   `gate/full-cross-component-regression-83f065e` and
   `gate/rollback-rehearsal-83f065e`.
3. Commit the decision, rerun the consuming validator, confirm its effective
   run, then create the fresh Slice B observation before product edits.
4. Execute Slice B only as the approved net-negative cleanup in
   `plans/PLAN-phase6b-b3-harvest-authority-prerequisite.md`; do not add any
   authority architecture or start subset #2.

## Traps

- The earlier user `ok` approved implementation planning, not the Class C
  platform-owner closure; do not append a decision without the explicit
  approval in next step 1.
- Proposal hashes use canonical LF-normalized Git bytes, not Windows raw
  working-tree hashes.
- `git apply` needs `--unidiff-zero`; a zero-context patch otherwise fails.
- Caller-owned UUIDs and namespace-shaped references are correlation/shape,
  not HARVEST authority.
- Preserve the eight user-owned untracked provenance files.

## Glossary

- option-A deferment
- Class C
- platform-owner
- effective-from-run
- planned/deferred
- producer authority
