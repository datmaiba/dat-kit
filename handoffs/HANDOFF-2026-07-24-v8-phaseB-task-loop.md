# HANDOFF 2026-07-24 — Execute PLAN v8 Phase B: the `task-loop` command

## Goal

Add the generic, registry-driven **`task-loop`** command (PLAN v8 §4 Phase B): one
trigger that routes to every *non-software* `lifecycle=active` Domain Pack, so non-code
work gets a stable entry point without writing a new skill per pack. `code-loop`
(software-dev) stays unchanged. This is the second command in the code-loop / task-loop
pair; the engine stays `work-loop`.

**Not yet approved → plan-gated.** Draft the Phase B plan → `plan-reviewer` → STOP for
Dat's approval before any product edit. (Phase A followed exactly this and it paid off —
plan-reviewer caught three inherited errors.)

## Runtime

- Controller session: highest tier in play. Per PLAN §9: design exclusion rule + contract
  edit (`docs/contracts/domain-pack.md`) → **opus**; code the `render.py` projection →
  **sonnet**; reviewers (plan/qa/code/security) → **opus** (pins in `agents/*.md` — do NOT
  change, Class C). `fable` only per-dispatch if a step needs judgment beyond opus.

## Workflow

`code-loop` (software-dev pack), attended, plan-gated. Review order per **PLAN §6** (not v7
§9.1). **Tier is the first open question** (see Next steps §1): PLAN §6 lists "Phase B
task-loop routing" under **Tier B**, but the same table puts any change to `render.py`
execution logic at **Tier C** (adds `pytest` + one sequential, diff-scoped reviewer). If
task-loop needs new renderer code (likely), it is Tier C. Resolve this with `plan-reviewer`.

## Canonical contract

`dat-kit 1.16.0`. Read root `AGENTS.md` → `docs/agent-workflow.md`,
`docs/agent-working-rules.md`, `lessons-learned/lessons-learned.md` FIRST.

## Git state

- Branch: **`feature/v8-rename-code-loop`**, HEAD **`7b6bb10`** (Phase A rename, committed).
  Worktree clean, all gates green.
- Parent `2ceae62` (v8 plan/handoff docs) on green `f8cb45d`. Subset #4 telemetry WIP is
  isolated at `f43aceb` on `feature/telemetry-v3-b3` — **do not touch** (resumes at Phase E).
- Build Phase B **on top of `7b6bb10`** (same branch, or cut `feature/v8-task-loop` from it).
- Sandbox CAN write `.git` here once no stale lock exists. If a git op fails on
  `.git/index.lock` ("Operation not permitted"), clear host-side: `del D:\project\dat-kit\.git\index.lock`.
  Before any branch switch that deletes files, call `allow_cowork_file_delete` first
  (lesson 2026-07-23), then verify with `git status` + `git ls-tree`.

## State

- DONE: **Phase A** — `build-loop → code-loop` rename + `build-loop` alias, commit `7b6bb10`.
  code-loop is the rendered software-dev trigger; build-loop is a marker-free redirect stub.
- IN PROGRESS: none.
- NOT STARTED: **Phase B** (this handoff). Then C (docs/two-doors narrative), D (optional
  non-code pack), E (resume telemetry-v3 subset #4), F (resume evolution). See PLAN §4.

## Decisions in effect

(dat-kit maintainer repo has no `spec/08-decisions.md`; decisions live in PLAN v8 + handoffs.)

- PLAN §1: KEEP telemetry + evolution (north star; not parked). Names: `code-loop` (code) /
  `task-loop` (non-code); engine stays `work-loop`.
- PLAN §2 non-negotiables: one policy owner (`AGENTS.md`); one descriptor owner per component;
  **`task-loop` raises NO pack's loop ceiling**; governed universe intact (every product path
  must resolve an owner — `EVOLUTION_ORPHAN_PATH`); exclusion of software-dev declared in the
  **registry**, never hardcoded in the trigger (PLAN §3).
- PLAN §5: no 3-agent parallel review; reviewers sequential + diff-scoped.
- Phase A session-local decisions carried forward: (1) telemetry `workflow` enum rename →
  Phase E; (2) `templates/common/**` command-refs are snapshot hash-pinned → need R6/R9
  amendment, not Tier B/C; (3) `contract_check.py` `build-loop` detection tokens → small
  Tier-C follow-up. `skills/fable-dat/` does NOT exist (phantom in the old handoff).

## Files touched

None yet (Phase B not started). Phase A's committed surface is in `git show 7b6bb10 --stat`.

## Verified gates

Phase A final (commit `7b6bb10`), verbatim:
- `python scripts/validate.py` → `✓ all checks green`
- `python scripts/render.py --check` → RC 0 (byte-exact)
- `python -m pytest scripts/tests` → `420 passed, 3 skipped`
- alias+smoke: code-loop resolves `work-loop/1` + 6 real slots; build-loop stub marker-free,
  redirects; `explain_path` owns both; evals collision-free (`run the code loop`→code-loop,
  `run the build loop`→build-loop).
- Phase B gates: **unverified** (not started).

## Third-party tool risks

none reported.

## Next steps

1. **Resolve the tier + design question FIRST** (drives the whole plan): can the `task-loop`
   trigger be produced from registry *data alone* through the existing renderer (→ Tier B,
   no `render.py` logic), or does it need a new projection function in `render.py` (→ Tier C:
   `pytest` + one sequential reviewer)? Read `scripts/render.py` `expected_outputs()` /
   `render_domain_trigger()` and `scripts/registry.py` to decide. Record the answer in the plan.
2. **Design the exclusion model** (opus): how the registry marks a pack as task-loop-eligible
   (`lifecycle=active` AND not `software-dev`) — a declared field/group in `registry/domains.json`,
   NOT a hardcode in the trigger. Declare it in `docs/contracts/domain-pack.md`.
3. **Decide `skills/knowledge-work` fate** (PLAN §4 Phase B): redirect-alias to
   `task-loop knowledge-work`, or fold into `task-loop`. Mirror Phase A's alias-stub pattern if
   keeping it (marker-free stub; keep its `skills/knowledge-work/**` evolution glob).
4. **Author red-before-green fixtures** (PLAN §4 Phase B): (a) a synthetic non-software active
   pack appears in `task-loop` with NO Python/shell edit; (b) `software-dev` does NOT appear in
   `task-loop`; (c) a hand-edited generated trigger fails `render.py --check`; (d) selecting a
   pack loads its correct 6 slots (assert real files, not just names).
5. **Add/update skill-evals** for `task-loop` (positive + negative) in
   `benchmarks/skill-evals.jsonl`; keep match phrases collision-free (validate.py §6 enforces
   this mechanically — a match phrase must be in exactly one skill's frontmatter description).
6. Run the tier's gates; append one scorecard line (`agent_runtime:"other"` for Cowork;
   re-run `validate.py` AFTER the append — lesson 2026-07-21); STOP before merge for Dat.

## Traps

- **Projection ownership**: any new `skills/<name>/SKILL.md` must be owned by a
  `registry/evolution.json` component `path_globs` entry or it is `EVOLUTION_ORPHAN_PATH`
  (validate red). Phase A hit exactly this with `skills/code-loop/**`. `task-loop` will need
  its own glob added to a component.
- **Orphan/stale check**: `render.py check_outputs()` flags any `skills/*/SKILL.md` containing
  the `GENERATED FROM REGISTRY` marker with no active descriptor → `PROJECTION_STALE_OUTPUT`.
  A hand-authored stub must be marker-free.
- **eval collision (validate.py §6)**: each positive eval `match` must appear in its
  `expect_skill` frontmatter description AND no other — design task-loop's description phrases
  to not collide with code-loop / knowledge-work.
- **`templates/common/**` is hash-pinned** (`expected_content_hash` in `platform.json` +
  `registry/snapshots/project-contract-2.0.json`) — editing content trips
  `REGISTRY_SNAPSHOT_HASH_MISMATCH`. Do not edit those files in a routing phase.
- **Telemetry enum coupling**: `workflow` value `build-loop` lives in `telemetry.py` +
  producers + telemetry tests; leave it for Phase E. Adding `task-loop`/`domain-id` telemetry
  is Phase E scope (PLAN §4 Phase E), not Phase B.
- Reviewer subagents sometimes lack an executor (lesson 2026-07-23): if a pinned reviewer
  reports "no executor," that's a correct refusal — dispatch a substitute with real bash and
  log both.
- `pytest`/`pyyaml` are not preinstalled in the sandbox: `pip install pytest pyyaml --break-system-packages`.

## Glossary

work-loop engine · Domain Pack (six slots) · Registry Catalog · projection / thin trigger ·
`expected_outputs()` · `explain_path` / governed inventory · loop ceiling (Turn/Goal/Time/
Proactive) · lifecycle (`active` / `repo_only`) · Tier A–D gate model (PLAN §6).
