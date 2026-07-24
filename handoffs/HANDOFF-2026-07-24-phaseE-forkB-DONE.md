# HANDOFF 2026-07-24 — v8 Phase E Fork B DONE; next is subset #5 (report views)

## Goal

Phase E's first work unit — **B3 subset #4 Fork B, the `resume` emit CLI** — is
**built, reviewed, committed** on `feature/telemetry-v3-b3` at **`0a222b3`**. This
hands the branch to a fresh session to (1) push if wanted, and (2) continue the
telemetry-v3 B-line: **subset #5** (report views) → **B4** (durable
export/aggregation) → **B5** (release closure). The work-loop engine, the six-slot
Domain Packs, and `build_resume_linkage` (Fork A) are unchanged and green.

## First actions in the new session (do in order)

1. Read root `AGENTS.md` → `docs/agent-workflow.md`, `docs/agent-working-rules.md`,
   `lessons-learned/lessons-learned.md`. Canonical contract: **`dat-kit 1.16.0`**.
2. Read `plans/PLAN-v8-refocus.md` §4 (Phase E), §6 (Tier A–D gate model), §9
   (model selection). Load only the phase section you are about to run, per token
   discipline.
3. This is dat-kit maintenance, attended, **plan-gated**: draft a plan, run it past
   `dat-kit:plan-reviewer`, STOP for the user's approval before editing. Only commit
   when the user asks. The user (Dat) works plan-gated and replies in Vietnamese with
   English technical terms.

## Git state

- Branch **`feature/telemetry-v3-b3`**. The Fork B code commit is **`0a222b3`**
  (`feat(telemetry): resume emit CLI wrapping build_resume_linkage (Fork B)`, 5 files,
  +488/-3). This handoff sits one `docs(handoff)` commit on top of it.
  Ancestors: `f43aceb` (subset #4 Fork A) → `2ceae62` (v8 plan) → `f8cb45d` (subset #3)
  → `68f5345` → `78a1991` (subset #2).
- **NOT PUSHED** — the sandbox has no GitHub credentials (`could not read Username`).
  Push host-side: `git push origin feature/telemetry-v3-b3`.
- **Sandbox `.git` quirk (persists):** it can create but not `unlink` under `.git`,
  leaving a stale `.git/index.lock`. Commits still succeed; if a git op complains,
  clear host-side: `del D:\project\dat-kit\.git\index.lock`.
- **Two-branch divergence (unchanged, important):** the v8 rename work
  (`code-loop`/`task-loop`, Phases A–C) lives on a SEPARATE branch
  `feature/v8-rename-code-loop` at `a4ab63c`, which is **not** an ancestor of this
  branch (merge-base `2ceae62`). Per Dat's branch-strategy decision **A** (2026-07-24),
  telemetry continues on `feature/telemetry-v3-b3`; the `domain_id` event field and
  branch reconciliation are deferred until after the B-line — see "Deferred" below.

## State

- DONE: **subset #1/#2/#3**, **subset #4 Fork A** (`f43aceb`), **subset #4 Fork B**
  (`0a222b3`).
- IN PROGRESS: none.
- NOT STARTED: **subset #5** (report views) → **B4** (durable export/aggregation) →
  **B5** (release closure). Then Phase F (evolution), which requires an active
  telemetry producer first.

## What Fork B shipped (commit `0a222b3`, 5 files)

- **`scripts/telemetry.py`** — a `resume` subparser (`--task-id` required) in
  `_parser`; an `elif args.command == "resume":` branch in `_execute_command` that
  calls `_require_uuid4` → `build_resume_linkage(existing, task_id)` → `_new_event(...)`
  → `_append_lifecycle_event(...)`; `"resume"` added to the `DAT_KIT_TELEMETRY=off`
  disabled-set and both `TELEMETRY_OPERATIONAL_FAILURE` degraded-sets in `main`.
- **`scripts/tests/test_telemetry_cli.py`** — 8 tests (+`import argparse`). CLI-boundary
  (happy→full coverage, delegated-child lineage, kill-switch disabled) are red-anchored
  at the CLI; the four precondition tests assert the exact `TelemetryError.detail` at
  the `_execute_command` seam (see the load-bearing finding below); one producer-invariant
  guard.
- **`docs/spikes/phase-6b/b3-subset4-forkB-observation.md`** — observation + review ledger.
- **`plans/PLAN-phase6b-b3-subset4-forkB-resume-cli.md`** — the approved plan.
- **`benchmarks/scorecard.jsonl`** — one closure line (re-validated after append).

## Ground truth (verify against the code before quoting in any doc)

- The generic lifecycle CLI is **not** a trusted LOAD/HARVEST context and must NOT
  activate a producer (`docs/contracts/telemetry-v3.md` T3.12, ~L616–620). `resume`
  therefore emits `task_resumed` but leaves `telemetry/producers.json` `task-handoff`
  **`planned`**, `event_id` null. All five producers (`build-loop-harvest`,
  `diagnosing-bugs`, `knowledge-work-fact-check`, `task-handoff`, `reports`) are still
  `planned`.
- `build_resume_linkage(events, task_id)` (`scripts/telemetry.py` ~L1124) returns
  `{"task_id","payload","parent_task_id","delegation_id"}`; `payload` is the closed
  `task_resumed` object sourced from the most-recent unmatched `handoff_created`
  (excludes `delegation_brief`). Unchanged by Fork B.
- **Load-bearing test-design finding:** `_error` defaults to `code="TELEMETRY_EVENT_INVALID"`
  and `main` emits code-only (not `detail`), so the parser's unknown-subcommand reject
  and the helper's green-state preconditions produce the *identical* CLI output. Error-path
  tests MUST assert `TelemetryError.detail` at the `_execute_command` seam, not the CLI
  code/exit (which are vacuous). Red anchor at the seam = `AttributeError` (a hand-built
  `Namespace` lacking `completion_only` falls into the finish else-branch).

## Verified gates (commit `0a222b3`; run in Linux sandbox)

- `python3 scripts/validate.py` → `✓ all checks green` (RC 0)
- `python3 -m pytest scripts/tests -q` → `441 passed, 3 skipped` (baseline 433 + 8 new)
- `ruff check .` → `All checks passed`; `git diff --check` clean
- No `*.sh` in the diff → `bash -n`/`shellcheck` N/A. `mypy` report-only, not installed
  in-sandbox (skipped, non-blocking per R1).
- Reviewers: plan-reviewer RETURN→APPROVE (2 rounds); qa-agent PHASE DONE (static, no
  executor in its subagent — gates from the builder's run per lessons-learned 2026-07-23);
  code-reviewer APPROVE (one scaffolding-comment WARN fixed); security-reviewer SKIP
  (argued: UUIDv4 `--task-id` + internally-derived payload, no new path/shell).
- **Windows caveat:** `validate.py` exits non-zero on Windows via `UnicodeEncodeError`
  on the `✓` print despite passing — run gates in the Linux sandbox (lessons-learned records this).

## Next: subset #5 (report views) — PLAN §4 Phase E + §6 gates + §9 model

- **Subset #5 = report/aggregation views** over the lifecycle corpus: coverage reports use
  the latest valid `partial` result (contract ~L208–216), event-coverage-rate, and the
  `reports` producer (currently `planned`). Design against `docs/contracts/telemetry-v3.md`
  (reports/aggregation sections) — confirm the exact view shape before quoting.
- **Gate tier:** almost certainly **Tier C** (execution code in `telemetry.py`): Tier A
  (`validate.py` + `pytest` + `ruff` + `diff-check`) + 1 sequential reviewer; add
  security-reviewer only if a view reads/writes a path or parses external input (e.g. an
  export/report target path → traversal). Model: **sonnet** (bounded, extends existing
  pattern); reviewers stay opus-pinned in `agents/*.md` (Class C — do NOT change pins).
- After subset #5: **B4** (durable export/aggregation — likely a committed byte-exact
  projection → REMEMBER the `.gitattributes eol=lf` pin trap below) → **B5** (release
  closure). Then Phase F (evolution) once an active telemetry producer exists.

## Deferred (do NOT start without a fresh decision from Dat)

- **`domain_id` event field** — `domain_id` is NOT yet in the contract; adding it is a
  net-new event-envelope schema change that also needs the v8 `task-loop` concept (on the
  other branch). It measures non-code work (plan §E). Deferred until branch reconciliation.
- **Branch reconciliation** — merging `feature/v8-rename-code-loop` (a4ab63c) into this
  branch (or both into master). Risky on the Cowork mount (index.lock unlink, no push creds).
  Dat chose strategy A: defer. Surface it as an explicit decision before subset #5's
  `domain_id`-touching work, if any.

## Traps (still in force)

- **Producer activation needs a trusted context**, not a CLI — never flip a producer to
  `active` from a generic command (contract T3.12).
- **Byte-exact corpora need `.gitattributes eol=lf`** — any committed file whose bytes are
  compared for equality (render output OR a runtime-written append-only corpus like a B4
  export) needs its own `eol=lf` pin in the same commit (lessons-learned 2026-07-20 & 07-23).
- **No-echo on errors** — reject untrusted input through the SAME closed validator as the
  trusted path; keep every `_error`/`_lifecycle_error` message a fixed string; assert the
  specific rejected token is absent (lessons-learned 2026-07-23).
- **No `str(Path(...))` reaching a serialized/compared value** — derive contract-facing path
  literals from one canonical POSIX constant (lessons-learned 2026-07-23).
- **Scorecard append must re-run `validate.py`** after writing (lessons-learned 2026-07-21).
- **Reviewers stay sequential, diff-scoped, opus-pinned** (Class C — do NOT change pins).
  `docs/spikes/**` is append-only historical evidence — never edit past observation files.
- **Sandbox deps:** `pip install pytest pyyaml ruff --break-system-packages`; add
  `~/.local/bin` to `PATH`; shellcheck via apt or `shellcheck-py` if a `*.sh` is touched.

## Glossary

work-loop engine · lifecycle corpus (`benchmarks/*.jsonl`) · producer (`planned`/`active`;
trusted LOAD/HARVEST context) · `build_resume_linkage` (Fork A helper) · `resume` emit CLI
(Fork B) · `_execute_command` seam vs CLI boundary · coverage (`full`/`partial`) · Tier A–D
gate model (PLAN §6) · branch-strategy A (telemetry stays on `feature/telemetry-v3-b3`).
