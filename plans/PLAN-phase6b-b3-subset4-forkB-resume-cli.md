# PLAN — Phase 6B B3 subset #4 Fork B: `resume` emit CLI

**Domain:** dat-kit maintenance (v8 Phase E, telemetry-v3 B-line).
**Branch/base:** `feature/telemetry-v3-b3`, base HEAD `f43aceb` (subset #4 Fork A, clean tree after switch).
**Gate tier:** C (execution code in `telemetry.py`) — per PLAN-v8 §6: Tier A + `pytest` + 1 sequential reviewer; security-reviewer only if input reaches a path/shell.
**Model:** sonnet (bounded, extends existing CLI pattern); reviewers opus-pinned per `agents/*.md` (unchanged).

## Goal

Give the `task-handoff` linkage responsibility a *trusted-by-construction* emit surface: a `resume`
subcommand that derives the `task_resumed` payload + lineage via the already-shipped, already-reviewed
pure helper `build_resume_linkage(events, task_id)` (Fork A) and appends the event through the existing
`_append_lifecycle_event` path — so an operator resuming a task cannot hand-mis-build the payload,
mis-copy `handoff_ref`/`resumed_from_event_id`, or drop the parent/delegation lineage.

Today a caller *can* emit `task_resumed` only via the generic `append --event task_resumed
--payload-json '…'`, hand-building the closed payload and knowing the lineage — exactly the error class
Fork A exists to remove. Fork A built the derivation; Fork B wires it to the CLI.

## Scope — IN

1. `scripts/telemetry.py`: one new `resume` subparser (`--task-id` required) and its `_execute_command`
   branch. The branch: `_require_uuid4(args.task_id, "task_id")` (explicit, in-branch — mirrors `append`) →
   `existing = validate_lifecycle_events(root)` (already loaded) → `linkage = build_resume_linkage(existing,
   args.task_id)` → `event = _new_event(linkage["task_id"], "task_resumed", linkage["payload"],
   parent_task_id=linkage["parent_task_id"], delegation_id=linkage["delegation_id"])` → `stored =
   _append_lifecycle_event(root, existing, event)` → return the standard `{status, command, task_id, event_id}`
   shape. **Helper return keys verified** at `git show feature/telemetry-v3-b3:scripts/telemetry.py` L1124:
   `build_resume_linkage` returns exactly `{"task_id","payload","parent_task_id","delegation_id"}` (resolves
   plan-reviewer W1 — no KeyError risk).
2. `resume` joins the `DAT_KIT_TELEMETRY=off` disabled-set and the `TELEMETRY_OPERATIONAL_FAILURE`
   degraded-set (same treatment as `start`/`append`/`finish` in `main`), so a resume degrades gracefully
   rather than raising.
3. Tests: CLI-level tests (1/2/7 below) **extend `scripts/tests/test_telemetry_cli.py`**, reusing its
   existing `invoke()/start()/append()` helpers (no duplicate harness); seam-level precondition tests (3–6)
   extend `scripts/tests/test_resume_linkage.py` next to the helper's own tests.
4. **Observation pre-registration (before the first product edit):** a NEW file
   `docs/spikes/phase-6b/b3-subset4-forkB-observation.md` — task ID minted at start, immutable scope (this
   plan's IN/OUT), intended paths, auto-decisions, threat model, acceptance criteria; red counts and reviewer
   rows appended only as each fact exists. `docs/spikes/**` is append-only: Fork A's
   `b3-subset4-observation.md` is a closed historical record and is NOT edited.
5. **Plan lands in the repo at commit time:** this plan text is committed as
   `plans/PLAN-phase6b-b3-subset4-forkB-resume-cli.md` in the phase commit (repo convention, per Fork A).
   Until Dat approves a commit it stays in the session scratchpad only.

## Scope — OUT (explicit non-goals)

- **No producer activation.** `telemetry/producers.json` `task-handoff` stays `planned`, `event_id` null.
  Contract T3.12 (`docs/contracts/telemetry-v3.md` 603–625): the generic lifecycle CLI is **not** a trusted
  LOAD/HARVEST context and must not activate a producer. Fork B is emit convenience only.
- **No `handoff` / `delegate` subcommands, no delegation-*creation* helper** — deferred (still Fork B siblings,
  but each is its own unit; this plan ships only `resume`, the direct pairing with the Fork A helper).
- **No `domain_id` schema field** — net-new event-envelope field, needs the v8 task-loop branch + validator
  changes; deferred to a post-reconciliation unit (Dat chose branch strategy A).
- No schema/validator change, no new path/enum literal, no new committed byte-compared corpus (no
  `.gitattributes` change), no engine/adapter/report change. `build_resume_linkage` itself is unchanged.

## Design notes / traps guarded

- **`resume` reuses the SAME validators as the trusted write path** — it appends through
  `_append_lifecycle_event`, so the emitted event re-validates through the unchanged `task_resumed`
  validator + `_validate_task_sequences`; no parallel/looser validation copy is introduced
  (lessons-learned 2026-07-23 "same closed validator" rule).
- **No `str(Path(...))` reaching a serialized/compared value** — the branch adds no path literal; it reads
  the fixed lifecycle corpus via the existing `root` join only (lessons-learned 2026-07-23 POSIX-literal rule).
- **`_CliParser.error` already redacts** — invalid CLI is `"command line is invalid"`, no value echo; the
  new `--task-id` rides the existing `_require_uuid4` no-echo path.
- Purity of `build_resume_linkage` is unchanged; Fork B only *consumes* its return value.
- **Byte-bound owner named** (lessons-learned 2026-07-23 "Fork B here" entry): the `resume` branch adds **no
  new input source** — it reads the lifecycle corpus through the existing `validate_lifecycle_events(root)`,
  which owns the pre-decode per-record byte-bound on the disk read. Fork B introduces no second read path, so
  no new pre-decode limit is owed.
- **No contract edit needed (verified):** `docs/contracts/telemetry-v3.md` does not enumerate the CLI
  subcommand set (it names "lifecycle CLI" as an owed implementation, ~L651); adding `resume` touches no
  frozen contract surface and no R8 diagnostic-code table (no new code is minted — existing
  `TELEMETRY_EVENT_INVALID` details only).
- **Generic `append --event task_resumed` stays valid** — `test_telemetry_cli.py` L199 exercises it and is
  untouched. `resume` is an additive convenience surface, not a restriction of the generic path; restricting
  `append` is an explicit non-goal.

## Tests — red-before-green (targeted)

**Code-collision caveat (resolves plan-reviewer W2).** `build_resume_linkage`'s three preconditions raise via
`_error` (verified at L1150–1156 on the branch — NOT `_lifecycle_error`, which would mint
`TELEMETRY_LIFECYCLE_INVALID`), so they carry the default `code="TELEMETRY_EVENT_INVALID"` (L259) — the same
code `_CliParser.error` produces for an unknown subcommand — and `main` emits **only the code**, never the
`detail`. Red-state parser reject and green-state helper preconditions therefore produce the *identical* CLI
output (`{status:error, code:"TELEMETRY_EVENT_INVALID"}`, exit 2). Exit-code/status assertions therefore CANNOT
distinguish red from green for the error cases — those tests must assert the specific `TelemetryError.detail`
at the `_execute_command` seam, not the CLI code. Genuinely red-anchored at the CLI boundary: **tests 1, 2, 7**.

Red-anchored CLI-level tests (invoke `main([...])` against a temp repo root, per `test_telemetry_runtime.py`):

1. **Happy path (red-anchored):** seed `start`→`append(handoff_created)`, run `resume --task-id <id>`; assert
   exit 0, one `task_resumed` appended with `handoff_ref`/`resumed_from_event_id`/`resumed_from_handoff=true`
   matching the open handoff, and a following `validate` reports coverage `full`. Red (no branch): unknown
   command, exit 2, **no `task_resumed` appended** → distinct from green.
2. **Delegated child (red-anchored):** non-null parent/delegation task; `resume` emits with the lineage pair
   preserved. Red: no event. Green: event with correct lineage.
7. **Disabled (red-anchored):** `DAT_KIT_TELEMETRY=off` → `{status:disabled, command:"resume"}`, exit 0,
   nothing appended (requires `resume` in the disabled-set). Red: unknown command, exit 2 → distinct status+exit.

Precondition tests (assert the specific `detail`, at the `_execute_command` seam via a hand-built
`argparse.Namespace(command="resume", repository_root=root, task_id=<id>)` — the seam surfaces
`TelemetryError.detail`, which the CLI hides):

3. No unmatched handoff → `TelemetryError.detail == "no unmatched handoff to resume"`; corpus unchanged.
4. Already-finished task → `detail == "cannot resume a finished task"`; corpus unchanged.
5. No lifecycle events for the task → `detail == "resume target has no lifecycle events"`; corpus unchanged.
   (Red anchor for 3–5, verified against `_execute_command`: with no `resume` branch, the Namespace falls
   through to the `else`/finish path, which touches `args.completion_only` — absent on the hand-built
   Namespace → red fails with **`AttributeError`**, clearly distinct from the green-state specific `detail`.)
6. **Invalid task_id no-echo (resolves plan-reviewer W3, per lessons-learned 2026-07-23):** poison =
   `task_id="NOT-A-UUID"`; the rejection MUST fire **on task_id** via the in-branch `_require_uuid4`
   (green path, not the parser); assert `detail == "task_id must be a canonical lowercase UUIDv4"` and that
   the poison token `"NOT-A-UUID"` is **absent** from the message. Tested at the seam so the reject is the
   helper/branch validator, not `_CliParser.error`.
8. Producer invariant (not red-anchored — keep as a guard): `telemetry/producers.json` `task-handoff` still
   `planned`, `event_id` null after a successful resume.

State the red counts (expected: tests 1/2/7 fail red at the CLI; 3–6 fail red at the seam) in the
observation ledger before freeze.

## Gates (Tier C, run in Linux sandbox — `validate.py` false-reds on Windows console, lessons-learned 2026-07-14)

`python scripts/validate.py` · `python -m pytest scripts/tests` · `ruff check .` · `git diff --check`.
No `*.sh` touched → `bash -n`/`shellcheck` N/A (state in report). `mypy` report-only, non-blocking (R1).
Append one scorecard line at HARVEST, then **re-run `validate.py` after the append** (lessons-learned
2026-07-21 scorecard-enum rule).

## Reviewer chain (sequential, diff-scoped)

`plan-reviewer` (this file, before approval gate) → build → `qa-agent` → `code-reviewer` →
`security-reviewer` **only if triggered**. Trigger analysis: `resume` adds no new untrusted path/shell input
(task-id is UUIDv4-validated; payload is derived internally from already-validated events; corpus path is
the fixed existing one), so security is expected **SKIP-with-reason**, final call deferred to code-reviewer —
same disposition as Fork A. If any fix lands → findings-scoped re-review + regression qa.

## Risks & rollback

- Risk: `resume` branch diverges from validator expectations → caught by test 1/2 (round-trip through the
  unchanged validators) — no second source of truth.
- Risk: a resume on a corpus with the operational-failure path → covered by the degraded-set wiring (scope 2).
- Rollback: one subparser + one `_execute_command` branch + one test file; revert the commit. No schema,
  no migration, no data.

## Operational preconditions (host-side, before/after git writes)

- Switch to the branch first: `allow_cowork_file_delete` → `git checkout feature/telemetry-v3-b3` →
  `git status --short --branch` vs `git ls-tree feature/telemetry-v3-b3 -r --name-only` for stray files
  (lessons-learned 2026-07-23 checkout rule).
- The sandbox cannot push and may leave a stale `.git/index.lock`; commit only when Dat asks, and Dat
  clears the lock host-side (`del D:\project\dat-kit\.git\index.lock`) if a later git op needs it.

## Exit

`resume --task-id <id>` emits a linkage-correct `task_resumed` and a follow-up `validate` shows the task
`full`; producer stays `planned`; all Tier-C gates green; scorecard line appended and re-validated.
