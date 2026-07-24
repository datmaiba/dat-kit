# HANDOFF 2026-07-24 — v8 Phase B DONE; next is Phase C (docs sweep)

## Goal

Phase B (the generic `task-loop` router) is **built, reviewed, committed** on
`feature/v8-rename-code-loop`. This handoff hands the branch to a fresh session to
(1) push if not yet pushed, and (2) run **Phase C** (docs sweep — the "two doors"
narrative). `code-loop` (software-dev) and the engine are unchanged.

## Runtime

Controller: opus. Per PLAN §9: Phase C docs sweep (README/domains/loops/HUONG_DAN)
→ **sonnet** (prose, structured). Reviewers stay opus-pinned in `agents/*.md`
(Class C — do NOT change).

## Workflow

`code-loop` (software-dev pack), attended, plan-gated. Phase C is **Tier A** per
PLAN §6 (docs only, no script behavior change): gates = `validate.py` +
`render.py --check` byte-exact + trigger-eval pos/neg + one invoke smoke. No qa/
code/security reviewer required for Tier A, but keep the always-on floor: any
skill description edit needs its skill-eval updated, reviewers stay sequential.

## Canonical contract

`dat-kit 1.16.0`. Read root `AGENTS.md` → `docs/agent-workflow.md`,
`docs/agent-working-rules.md`, `lessons-learned/lessons-learned.md` FIRST.

## Git state

- Branch **`feature/v8-rename-code-loop`**, HEAD **`f097361`** (Phase B, committed,
  tree clean, all gates green). Parent `5e5fa71` (Phase B context handoff) on
  `7b6bb10` (Phase A rename).
- **NOT PUSHED YET** — the sandbox has no GitHub credentials
  (`could not read Username for https://github.com`). Push host-side:
  `git push origin feature/v8-rename-code-loop`.
- Sandbox `.git` quirk (unchanged from Phase A/B): it can create but not `unlink`
  files under `.git` ("Operation not permitted"); a stale `.git/index.lock` must be
  cleared host-side (`del D:\project\dat-kit\.git\index.lock`). During this session
  the lock cleared on its own between calls; the commit still succeeded.
- Telemetry subset #4 WIP stays isolated on `feature/telemetry-v3-b3` (`f43aceb`) —
  do not touch (resumes at Phase E).

## State

- DONE: **Phase A** (`build-loop→code-loop`, `7b6bb10`) and **Phase B** (`task-loop`
  router, `f097361`).
- IN PROGRESS: none.
- NOT STARTED: **Phase C** (docs sweep) → D (optional non-code pack) → E (telemetry
  subset #4, memory `dat-kit-b3-subset3-next`) → F (evolution). See `plans/PLAN-v8-refocus.md` §4.

## What Phase B shipped (so Phase C stays consistent)

- **task-loop is a router**, not a domain: one generated trigger
  `skills/task-loop/SKILL.md` listing every `active`, non-excluded pack and routing
  the chosen one through that pack's own descriptor + six slots. It **raises no loop
  ceiling** and carries no domain policy.
- **Design 1 (approved by Dat):** the exclusion lives in the registry as a denylist —
  `registry/domains.json#/task_loop = {trigger:{name,description,aliases}, excluded_domain_ids:["software-dev"]}`.
  A new non-software active pack (e.g. via `domain-builder`) appears in the router
  with **no code edit**; software-dev stays out because `code-loop` is its front door.
- **Second projection type:** `render.py render_task_loop_router()`, wired into
  `expected_outputs()` with a destination-collision guard; `closed()` gained an
  `optional=` param so `task_loop` is an optional domains-child envelope.
- **knowledge-work unchanged:** its standalone `skills/knowledge-work` trigger stays;
  the router merely lists it. (PLAN §3's "redirect/fold" both judged unnecessary.)
- Contract: `docs/contracts/domain-pack.md` DP2.1 (router envelope) + DP5 (two
  projection types); `docs/contracts/registry.md` R7 (three projections) + two new
  R8 codes `REGISTRY_TASK_LOOP_EXCLUSION_UNKNOWN` / `REGISTRY_TASK_LOOP_EXCLUSION_DUPLICATE`.
- Governed: `skills/task-loop/**` glob added to the `utility-skills` component.
- Evals: positive `trg-taskloop-01` (match "run the task loop", collision-free) +
  negative `neg-taskloop-01`.

## Decisions in effect

- PLAN §1: KEEP telemetry + evolution (north star; not parked).
- PLAN §2 non-negotiables intact: one policy owner; `task-loop` raises no ceiling;
  governed universe resolves every path; exclusion declared in registry, not the trigger.
- **Strict exclusion** (Dat/reviewer-endorsed): an `excluded_domain_ids` entry must
  reference a registered domain (fail-closed `..._UNKNOWN`), same house rule as
  `gate_authority_ref`/`evolution_profile_ref`. So deleting a domain must also drop it
  from the denylist — `test_engine_deletion` now pops `task_loop` when it empties domains.
- **Rendered aliases sort** (code-review M1): `render.py` sorts aliases in the
  "Registered aliases:" line of BOTH trigger types (DP5 says sorted). Existing triggers
  were already sorted, so only the router's bytes changed.

## Verified gates (commit f097361)

- `python scripts/validate.py` → `✓ all checks green`
- `python scripts/render.py --check` → RC 0 (byte-exact, all three projections)
- `python -m pytest scripts/tests` → `428 passed, 3 skipped` (8 new task-loop fixtures,
  authored red-before-green)
- `ruff check scripts/` → pass; `shellcheck scripts/init.sh` → pass; `git diff --check` → clean
- mypy report-only: mypy 2.3.0 crashes with an INTERNAL ERROR (its own bug); non-blocking
  per contract R1 (`required:false`). Re-check on a working mypy build.
- Smoke: router lists `knowledge-work`, excludes `software-dev`; `closed(optional=…)`
  backward-compatible; plan-reviewer + code-reviewer both approve-with-changes, all folded.

## Phase C scope (PLAN §4 Phase C / §8)

- README: "Hai cửa vào" section up top — `code-loop` (code) / `task-loop` (non-code).
- `docs/domains.md` + `docs/loops.md`: boundary table; remove leftover "final/permanent"
  wording (ADR 0001 debt).
- `HUONG_DAN.vi.md`: Vietnamese guide for both commands + aliases (`build-loop`, `task loop`).
- Exit: reading a description makes code-vs-non-code obvious; trigger-eval pos/neg pass.

## Traps

- `templates/common/**` is snapshot hash-pinned (`expected_content_hash` in
  `platform.json` + `snapshots/project-contract-2.0.json`) — editing content trips
  `REGISTRY_SNAPSHOT_HASH_MISMATCH`. Do not edit in a docs phase.
- New diagnostic codes must be documented under `docs/contracts/registry.md` R8 or
  `test_diagnostic_codes.py` goes red (both directions).
- New `skills/<name>/SKILL.md` with the GENERATED marker must be owned by a
  `registry/evolution.json` component glob AND be in `render.py expected_outputs`, or
  it is `EVOLUTION_ORPHAN_PATH` / `PROJECTION_STALE_OUTPUT`.
- `pytest`/`pyyaml`/`ruff`/`shellcheck` not preinstalled in the sandbox:
  `pip install pytest pyyaml ruff --break-system-packages`; shellcheck via apt or `shellcheck-py`.
- Telemetry `workflow` enum + `domain-id` telemetry are **Phase E** scope, not Phase C.

## Glossary

work-loop engine · Domain Pack (six slots) · Registry Catalog · projection / thin
trigger · router envelope (`task_loop`) · `expected_outputs()` · `explain_path` /
governed inventory · loop ceiling (Turn/Goal/Time/Proactive) · lifecycle
(`active`/`legacy`/`retired`) · Tier A–D gate model (PLAN §6).
