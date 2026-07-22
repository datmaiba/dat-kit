# HANDOFF 2026-07-21 — start Phase 6 Telemetry v3 contract-first

## Goal

Prepare a cold session to execute PLAN-v7 Phase 6 (`plans/PLAN-v7-platform.md`
§6 Phase 6 and §13.2) and release dat-kit 2.1.0. The first work item is
**Phase 6A: write, independently review, and obtain approval for
`docs/contracts/telemetry-v3.md` before implementing `scripts/telemetry.py` or
creating telemetry data files.** Gemini and Cursor v2.0.x follow-ups are
explicitly deferred and are outside this phase.

## Runtime

`codex / GPT-5` (exact minor model identifier not exposed).

## Workflow

This file was prepared with the `handoff` workflow. The receiving session must
run `dat-kit:build-loop` for Phase 6, including plan-reviewer before the
approval gate and the sequential QA → code-review → conditional security chain.

## Canonical contract

`dat-kit 1.16.0` — maintainer contract at root `AGENTS.md`.

## Git state

- Branch: `feature/telemetry-v3`.
- Base HEAD: `f3cf0e47f2eb40914b883c713050d7e84b559811`, the merge commit of PR #2
  into `master`.
- At authoring time the branch is identical to `master`; this handoff is the
  only new working-tree file. Verify the final context commit with
  `git log -1 --oneline` rather than relying on a forward hash inside the file.

## State

### DONE

1. dat-kit v2.0.0 is public: annotated tag `v2.0.0` points to `c018a31`; the
   GitHub Release is public and latest at
   `https://github.com/datmaiba/dat-kit/releases/tag/v2.0.0`.
2. PR #2 merged `feature/open-platform-v2` into `master` at `f3cf0e4`.
   GitHub Actions run `29777177244` passed on that exact merge SHA:
   `validate` success and `windows-python` success.
3. The owner explicitly deferred both shipped v2.0.x known limitations:
   Cursor's live-in-editor checklist and the Gemini `repo_only` registry
   inconsistency. Neither blocks or belongs to Phase 6.
4. `feature/telemetry-v3` was created from the clean, synchronized `master`
   merge commit.
5. Phase 6 reconnaissance confirmed the contract-first ordering, the v2.1
   Definition of Done, the existing signal producers, and two governance gaps
   that must be resolved before implementation.

### IN PROGRESS

1. Session-entry context only. No telemetry contract, schema, runtime,
   producer, registry, hook, benchmark, or test implementation has started.

### NOT STARTED

1. Phase 6A — independently reviewed and owner-approved Telemetry v3 contract.
2. Phase 6 governance slice — governed ownership for the new telemetry root
   and runtime files, resolved before those files land.
3. Phase 6B — telemetry lifecycle/runtime, storage/recovery, import/export,
   privacy/retention/disable behavior, task-ID propagation, and five named
   producers.
4. Phase 6C — full verification, two representative real-task observations,
   RC/rollback, version bump, tag, CI, and dat-kit 2.1.0 release closure.

## Decisions in effect

1. `docs/decisions/0001-open-platform.md`: Telemetry v3 is deferred to 2.1;
   governed self-evolution remains deferred to 2.2. Phase 6 must not implement
   `kit-evolve` or automatic authority.
2. Approved PLAN-v7 §3.10: task UUIDv4 begins at LOAD, propagates through
   handoff/delegation/gates/reviews/HARVEST, and corrections append links to an
   earlier event rather than replacing it.
3. Approved PLAN-v7 §3.10: v2.1 requires single-writer atomic append and
   interrupted-append recovery. Multi-writer locking stays deferred until
   delegated writers actually run concurrently.
4. Approved PLAN-v7 §3.10: completion-only scorecards are a supported partial
   coverage path; token attribution is exact or explicitly unknown with a
   reason; raw prompts and secrets are excluded by default.
5. Approved PLAN-v7 Phase 6: `docs/contracts/telemetry-v3.md` must be written
   and approved before implementation.
6. Owner decision, 2026-07-21: do not work on Gemini or Cursor now; resume them
   only as a later v2.0.x follow-up when the required host/tool is available.
7. Session-local preparation decision: use a new `feature/telemetry-v3` branch
   from merged `master`; do not continue Phase 6 on the completed v2 branch.

There is no root `spec/08-decisions.md`; the approved plan and
`docs/decisions/` are the maintainer decision record for this program.

## Files touched

- `handoffs/HANDOFF-2026-07-21-phase6-telemetry-v3-entry.md` → new cold-session
  entry context; the only file changed during preparation.
- No Phase 6 product, contract, registry, runtime, hook, benchmark, domain, or
  test file has been modified.

Candidate Phase 6 paths below are a reconnaissance map, not an approved diff:

- Contract/governance: `docs/contracts/telemetry-v3.md`,
  `registry/evolution.json`, `docs/contracts/evolution.md`, governance tests.
- Runtime/storage: `scripts/telemetry.py`, `telemetry/README.md`,
  `telemetry/schema-v3.json`, ignored local `telemetry/events.jsonl`, export to
  committed append-only `benchmarks/` records.
- Lifecycle integration: `engine/work-loop/ENGINE.md`, `hooks.json`,
  `scripts/scorecard.py`, `skills/scorecard/SKILL.md`, handoff/delegation
  surfaces, registry/render sources and their generated trigger projections.
- Named producers: build-loop HARVEST; `skills/diagnosing-bugs/SKILL.md`;
  `domains/knowledge-work/deliverables/fact-check.template.md`; task schema's
  `resumed_from_handoff`; per-reviewer and per-host coverage reports;
  `benchmarks/defects.jsonl`.
- Tests: a new telemetry-focused suite plus affected scorecard, engine,
  domain-pack, render, hook, validation, privacy, and evidence tests.

## Verified gates

- Baseline merge tree `f3cf0e4`: GitHub Actions run `29777177244` —
  `validate` **success**, `windows-python` **success**.
- Handoff-only branch diff gates: `python scripts/validate.py` **PASS**;
  `python -m pytest scripts/tests` **277 passed, 6 skipped**;
  `python scripts/render.py --check` **PASS**; `bash -n scripts/init.sh`
  **PASS**; `shellcheck scripts/init.sh` **PASS**; `git diff --check` **PASS**.

## Third-party tool risks

None reported. No installer ran during Phase 6 preparation.

## Next steps

1. `git switch feature/telemetry-v3` — then run `git status --short` and
   `git log -1 --oneline`; read this handoff, root `AGENTS.md`, linked
   maintainer docs, newest lessons, PLAN-v7 §3.10 / Phase 6 / §13.2, and ADR
   0001.
2. Invoke `dat-kit:build-loop` and declare **Phase 6A contract only**. Generate
   SELF-Q&A across schema boundaries, privacy/source classes, retention,
   correction behavior, partial coverage, downgrade/disable, import/export,
   and producer responsibilities.
3. Draft a complete Phase 6A plan and dispatch `plan-reviewer` before asking
   for owner approval. Do not combine plan approval with execution.
4. Run
   `python scripts/registry.py explain-evolution docs/contracts/telemetry-v3.md`.
   Treat its result as binding: `registry-contract`, **Class C**,
   `platform-owner` closer, both `knowledge-work-reviewer` and
   `software-dev-reviewer`, full cross-component regression, and rollback
   rehearsal.
5. After plan approval, create only `docs/contracts/telemetry-v3.md` plus the
   directly required Class-C decision/evidence/tests. The contract must cover:
   event/task/parent/delegation identity; producer revisions; lifecycle and
   event types; gates/reviews/defects/rework; token and elapsed attribution;
   coverage; privacy/source class; retention/export; correction linkage;
   disable/downgrade behavior; compatibility and schema freeze.
6. Before Phase 6B, resolve governance explicitly. Current probes return
   `EVOLUTION_ORPHAN_PATH` for both `scripts/telemetry.py` and
   `telemetry/schema-v3.json`. Add approved governed-root/component ownership
   and negative tests before either implementation path lands; do not hide the
   orphan diagnostics with an unrelated broad glob.
7. Implement Phase 6B in dependency order: schema/storage → lifecycle CLI →
   task-ID propagation → scorecard/handoff integration → five named producers
   → export/retention/disable → reports. Use commit-sized slices and red-before-
   green for every new/changed gate.
8. Close against every PLAN-v7 §13.2 item, including one real software-dev and
   one real knowledge-work task with human vs automated verdicts distinguished,
   then run the full 2.1 RC/rollback/tag/CI release train.

## Traps

1. `.codegraph/` is absent; use `rg`/targeted reads. Do not index the repo as
   part of Phase 6 unless the owner separately asks.
2. Contract-first is a hard gate. A telemetry schema without active producers
   is explicitly rejected by the plan, but producers still cannot precede the
   approved contract.
3. `docs/contracts/telemetry-v3.md` is already governed as Class C. Do not
   treat it as harmless documentation or close it with a same-author review.
4. `scripts/telemetry.py` is not covered by the current `maintainer-scripts`
   globs, and `telemetry/` is not a governed root. Both fail closed today.
5. Existing `benchmarks/scorecard.jsonl` and `benchmarks/skill-evals.jsonl`
   are append-only history. v2→v3 import creates new linked events; it never
   rewrites old bytes.
6. The shipped Claude producer surface is root `hooks.json` (registered and
   validated), not ignored machine-local `.claude/settings.local.json` and not
   `.codex/hooks.json`.
7. Rendered skills are projections. Change their registry/pack/render source
   and verify `scripts/render.py --check`; do not hand-edit generated trigger
   bytes.
8. A workflow file is not CI evidence. Verify real Ubuntu and Windows Actions
   runs on the exact RC/tag SHA. The current Actions stack also emits a
   non-blocking Node 20 deprecation warning for `actions/checkout@v4` and
   `actions/setup-python@v5`; keep it separate from Phase 6 unless it becomes a
   real gate failure or receives separately approved scope.
9. Every HARVEST append that changes validator input must be followed by a
   validator rerun. Never close a release/tag item before its external receipt
   exists; record post-tag facts in a post-tag commit.

## Glossary

- work-loop engine
- Domain Pack
- Host Adapter
- telemetry task lifecycle
- event coverage
- partial coverage
- durable corpus
- source class
- correction linkage
- first-pass gate status
- parent/delegation linkage
- producer revision
- single-writer atomic append
- interrupted-append recovery
