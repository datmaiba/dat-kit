# Phase 6B B3 subset #4 Fork B observation and review ledger

## Pre-registration

- Observation task ID: `c91b4bbe-d474-431d-8473-7d00def82f82`.
- Registered before the first subset #4 Fork B product or test edit on 2026-07-24.
- Immutable scope: subset #4 Fork B only — the `resume` **emit CLI subcommand**
  that wraps the already-shipped pure helper `build_resume_linkage` (Fork A,
  `f43aceb`) so an operator resuming a task cannot hand-mis-build the
  `task_resumed` payload or drop the parent/delegation lineage. One product
  artifact: a `resume` subparser + `_execute_command` branch in
  `scripts/telemetry.py`, plus `resume` joining the `main` disabled/degraded
  sets.
- Intended product/test paths: `scripts/telemetry.py` (one `resume` subparser,
  one `_execute_command` branch, three set-membership additions in `main`; no
  new path/enum literal, no new committed corpus), `scripts/tests/test_telemetry_cli.py`
  (CLI-boundary tests 1/2/7), `scripts/tests/test_resume_linkage.py` (seam
  precondition tests 3–6).
- Task-local evidence path: `docs/spikes/phase-6b/b3-subset4-forkB-observation.md`.
- Plan: `plans/PLAN-phase6b-b3-subset4-forkB-resume-cli.md`.
- Closure-only append: `benchmarks/scorecard.jsonl`, after all verdicts, with a
  post-append `validate.py` re-run (lessons-learned 2026-07-21).
- Explicit non-goals: producer activation (`task-handoff` stays `planned`); the
  `handoff` and `delegate` subcommands and any delegation-*creation* helper
  (each its own unit); the `domain_id` event-envelope field (needs the v8
  task-loop branch + validator change; deferred to a post-reconciliation unit);
  any schema, validator, engine, Host Adapter, retention, or reporting change;
  restricting the generic `append --event task_resumed` path. `build_resume_linkage`
  itself is unchanged. Fork A's `b3-subset4-observation.md` is a closed
  historical record and is NOT edited (docs/spikes is append-only).
- One task ID covers the whole Fork B slice; internal commits do not create new
  observation units.
- Reviewer chain (planned): plan-reviewer before the first product edit (done,
  2 rounds: RETURN→APPROVE); then full QA, code review, and — only if
  paths/input/external-write surfaces are touched — security review,
  findings-scoped re-review, final regression QA.

## Ground-truth answers and auto-decisions

1. The generic lifecycle CLI is **not** a trusted LOAD/HARVEST context and must
   not activate a producer. Source: `docs/contracts/telemetry-v3.md` T3.12
   (~616–620) and the producer table (line 598). Therefore `resume` emits a
   `task_resumed` event but leaves `telemetry/producers.json` `task-handoff`
   `planned`, `event_id` null.
2. The `resume` branch derives its payload + lineage only from
   `build_resume_linkage(events, task_id)` (`scripts/telemetry.py:1124`), which
   returns the closed `{task_id, payload, parent_task_id, delegation_id}` dict;
   the branch builds the event via the existing `_new_event(...)` and appends
   via the existing `_append_lifecycle_event(...)`, so the event re-validates
   through the UNCHANGED `task_resumed` validator + `_validate_task_sequences`.
3. `--task-id` is validated in-branch by `_require_uuid4` (no value echo), then
   the corpus is read once through `validate_lifecycle_events(root)` — the layer
   that owns the pre-decode per-record byte-bound. No second read path is added.

Auto-decisions (low-severity, spec-consistent, reversible — logged per the
build-loop severity rubric):

- **A-FB-1 — `resume` joins all three CLI sets.** It joins the
  `DAT_KIT_TELEMETRY=off` disabled-set and both `TELEMETRY_OPERATIONAL_FAILURE`
  degraded-sets in `main`, exactly like `start`/`append`/`finish`, so a resume
  degrades gracefully instead of raising. Rationale: a lifecycle-writing command
  must fail soft on operational I/O failure, matching its siblings.
- **A-FB-2 — ship only `resume`.** `handoff`/`delegate` deferred (Dat's
  decision, 2026-07-24). One artifact per subset.
- **A-FB-4 — all Fork B tests live in `test_telemetry_cli.py`.** Both the
  CLI-boundary tests and the seam precondition tests need an on-disk seeded
  lifecycle corpus (`_execute_command` reads from disk), and that seeding harness
  (`invoke`/`start`/`append`/`records`) lives in `test_telemetry_cli.py` — not in
  `test_resume_linkage.py`, whose helpers build in-memory event lists only.
  Reversible placement choice; the pre-registration's "intended paths" named
  `test_resume_linkage.py` for the seam tests, overridden here to reuse the
  correct harness.
- **A-FB-3 — precondition tests at the `_execute_command` seam.** Because the
  CLI emits only the error `code` (not `detail`) and `build_resume_linkage`
  raises via `_error` (default code `TELEMETRY_EVENT_INVALID`, the same code the
  parser emits for an unknown subcommand), CLI-boundary assertions cannot
  distinguish red from green for the error cases. Those tests assert the exact
  `TelemetryError.detail` at the seam; red anchor is `AttributeError` (a
  hand-built `Namespace` lacking `completion_only` falls into the finish
  else-branch).

No open question remains; no decision-log file exists in this repository.

## Threat model

| Boundary | Threat | Required control |
|---|---|---|
| CLI `--task-id` input | Non-UUID or malformed task ID | In-branch `_require_uuid4` raises a fixed, no-echo error before any read |
| Event-stream derivation | Emitted `task_resumed` points at a wrong/`delegation_brief` handoff or drops lineage | Payload+lineage come solely from `build_resume_linkage`, whose source is `_unmatched_handoffs` (excludes `delegation_brief`); the appended event re-validates through the unchanged validators |
| Producer status | `resume` flips `task-handoff` to `active` | No activation path; `producers.json` untouched; asserted by an invariant test |
| Value echo | Diagnostics leak the rejected task ID or stream contents | `_require_uuid4` / `_error` raise fixed messages; poison-token-absent asserted |
| Operational I/O | Corpus read/write failure raises instead of degrading | `resume` in the disabled/degraded sets → `{status:degraded}` exit 0 |

## Acceptance criteria

- `resume --task-id <id>` on a task with one open handoff appends a
  `task_resumed` whose `handoff_ref`/`resumed_from_event_id`/`resumed_from_handoff=true`
  match that handoff; a following `validate` reports the task coverage `full`.
- A delegated child task round-trips with its `(parent_task_id, delegation_id)`
  lineage preserved on the emitted event.
- `DAT_KIT_TELEMETRY=off` → `{status:disabled, command:"resume"}`, exit 0,
  nothing appended.
- No unmatched handoff / already-finished task / no lifecycle events each raise
  the exact helper `detail` at the seam, with no corpus mutation.
- A non-UUIDv4 `--task-id` is rejected on `task_id` with the poison token absent
  from the message.
- `telemetry/producers.json` `task-handoff` stays `planned` after a successful
  resume; the helper and the generic `append` path are unchanged.
- Targeted tests show red-before-green; canonical full gates and the reviewer
  chain pass on a frozen committed candidate.

## Candidate and invocation ledger

Candidate/base/tree IDs and changed paths are recorded at freeze. Reviewer
invocation rows and pre-freeze receipts are appended only after each fact
exists; this pre-registration claims no future evidence.

Base HEAD at start: `f43aceb` (subset #4 Fork A), clean tree, branch
`feature/telemetry-v3-b3`. Baseline gates on the untouched tree: `validate.py`
`✓ all checks green`; `pytest scripts/tests` `433 passed, 3 skipped`; `ruff`
`All checks passed`; `git diff --check` clean.

Changed paths (pre-commit): `scripts/telemetry.py` (one `resume` subparser, one
`_execute_command` branch, three `main` set-membership additions),
`scripts/tests/test_telemetry_cli.py` (8 tests + `import argparse`), this
observation, `plans/PLAN-phase6b-b3-subset4-forkB-resume-cli.md`; closure-only
`benchmarks/scorecard.jsonl` append. No `*.sh` in the diff. No new path/enum
literal, no new byte-compared committed corpus (no `.gitattributes` change).

## Pre-freeze receipts (2026-07-24)

- Red-before-green: with the `resume` subparser+branch removed, the targeted
  suite reported `7 failed, 4 passed` — the four passing were pre-existing
  `resume`-substring tests; the seam tests failed with the expected
  `AttributeError: 'Namespace' object has no attribute 'completion_only'`
  (Namespace falls into the finish else-branch). With the branch added,
  `11 passed` (8 new + 3 pre-existing). The non-red-anchored producer-invariant
  guard passes in both states, as pre-registered (A-FB-3).
- Full gates on the working tree: `python3 scripts/validate.py`
  `✓ all checks green`; `python3 -m pytest scripts/tests -q`
  `441 passed, 3 skipped`; `ruff check .` `All checks passed`;
  `git diff --check` clean. `mypy` report-only, not installed in-sandbox
  (skipped, non-blocking per R1).
- Scorecard append re-validated: `validate.py` re-run `✓ all checks green` after
  the `benchmarks/scorecard.jsonl` append (lessons-learned 2026-07-21).

## Reviewer chain (2026-07-24)

- plan-reviewer: two rounds. Round 1 `RETURN` — W1 (helper return keys
  unverified), W2 (red-before-green false for the error-case tests: `_error`
  shares `TELEMETRY_EVENT_INVALID` with the parser reject and the CLI emits
  code-only), W3 (invalid-`task_id` test risked the 2026-07-23 no-echo vacuity).
  All three folded (keys verified by `git show`; error tests moved to the seam
  asserting exact `.detail`; test 6 poisons `task_id` and asserts token
  absence). Round 2 `APPROVE`, findings-scoped, one advisory prose note also
  folded (helper uses `_error`, not `_lifecycle_error`).
- qa-agent: `PHASE DONE` — static review of the exact diff, no defects across
  five attacked invariants (no producer activation; cannot emit an invalid
  `task_resumed`; no-echo holds; red-before-green sound; zero corpus mutation on
  reject). Gate execution unavailable in its subagent context (correct refusal
  per lessons-learned 2026-07-23); gates supplied by the builder's verified green
  run above (deterministic, diff scope confirmed, no `*.sh`).
- code-reviewer: `APPROVE`. One WARN — a phase/fork-tagged section-header comment
  in `test_telemetry_cli.py` (design-node scaffolding barred from committed
  source) — fixed by rewording to drop the identifiers while keeping the
  seam-vs-CLI rationale; regression `pytest -k resume` `11 passed`, `ruff` clean,
  `validate.py` green after the fix. One NOTE (no-echo assert pairing) kept as a
  deliberate guard.
- security-reviewer: SKIPPED — argued. The `resume` branch adds no new untrusted
  path/shell surface: its only external input is `--task-id`, UUIDv4-validated
  in-branch by `_require_uuid4` (no-echo) before any read; payload and lineage
  are internally derived by `build_resume_linkage` from the already-decoded
  corpus; no new file path, enum literal, or write target; `producers.json`
  untouched. Both code-reviewer and qa-agent concur.

The closure commit is the commit introducing these receipts plus the scorecard
append; it is identified by Git history, never by a self-referential hash.
