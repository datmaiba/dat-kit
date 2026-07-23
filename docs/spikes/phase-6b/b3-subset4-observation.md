# Phase 6B B3 subset #4 observation and review ledger

## Pre-registration

- Observation task ID: `663e1041-c771-4e35-81ae-110c56133a9e`.
- Registered before the first subset #4 product or test edit on 2026-07-23.
- Immutable scope: subset #4 only — the `task-handoff` **linkage producer**,
  delivered as Fork A (define a pure linkage constructor, no CLI surface). One
  artifact: a pure helper `build_resume_linkage(events, task_id)` in
  `scripts/telemetry.py` that derives, from an already-validated event stream,
  the linkage-correct `task_resumed` payload (`resumed_from_handoff=true`, the
  `handoff_ref` and `resumed_from_event_id` of the most recent unmatched
  `handoff_created`) together with the parent/delegation lineage pair the resume
  event must carry — so the original task ID and parent/delegation linkage are
  preserved in one tested place instead of by hand-built JSON.
- Intended product/test paths: `scripts/telemetry.py` (pure
  `build_resume_linkage` + a small named error path; no new path/enum literal,
  no new committed corpus), `scripts/tests/test_resume_linkage.py`.
- Task-local evidence path: `docs/spikes/phase-6b/b3-subset4-observation.md`.
- Closure-only append: `benchmarks/scorecard.jsonl`, after all verdicts.
- Explicit non-goals: producer activation; any synthetic/retroactive receipt; a
  dedicated emit CLI subcommand — `handoff`/`resume`/`delegate` (Fork B,
  deferred); a delegation-*creation* helper that mints a new child task
  (Fork B); report views (subset #5); general export (B4); any schema, engine,
  Host Adapter, validator-contract, retention, or reporting change. The existing
  `_validate_task_sequences` / `_validate_delegations` / `_expected_coverage`
  linkage validators are NOT modified.
- One task ID covers the whole subset #4 slice; internal commits do not create
  new observation units.
- Reviewer chain (planned): plan-reviewer before the first product edit; then
  full QA, code review, and — only if paths/input/external-write surfaces are
  touched — security review, findings-scoped re-review, final regression QA.

## Ground-truth answers and auto-decisions

1. The `task-handoff` producer responsibility is exactly: emit
   `task_resumed.resumed_from_handoff=true`, preserve the original task ID
   across handoff, and preserve parent/delegation linkage; evidence before
   `active` is a real resumed or delegated task. Source:
   `docs/contracts/telemetry-v3.md` line 598 (producer table) and 601-604
   (every producer begins `planned`).
2. The `task_resumed` payload is the closed object
   `{handoff_ref (path), resumed_from_handoff (literal true),
   resumed_from_event_id (UUIDv4)}`. Source: `scripts/telemetry.py:486-491` and
   the payload table `docs/contracts/telemetry-v3.md:274`.
3. A resume must consume exactly one earlier **unmatched** `handoff_created`
   whose `reason` is not `delegation_brief`, and its `handoff_ref` must equal
   that source handoff's `handoff_ref`. Source:
   `scripts/telemetry.py:1114-1121` (`_unmatched_handoffs`) and 1223-1239
   (`_validate_task_sequences` resume/handoff matching).
4. "Preserve the original task ID" = the `task_resumed` event carries the same
   `task_id` as the task's originals; "preserve parent/delegation linkage" = it
   carries the same `(parent_task_id, delegation_id)` lineage pair, which
   `_validate_task_sequences` requires to be constant across a task's lifecycle.
   Source: `scripts/telemetry.py:1216-1221` (lineage-pair stability).
5. The producer stays `planned`. Fork A adds no activation, no receipt, and no
   CLI; `telemetry/producers.json` `task-handoff` is untouched (`planned`,
   `event_id` null). The helper is pure and emits nothing — construction and
   emission remain separate, mirroring subset #3's payload-only parser. Source:
   T3.12 lines 601-627; subset #3 precedent
   (`docs/spikes/phase-6b/b3-subset3-observation.md:44-47`).

Auto-decisions (low-severity, spec-consistent, reversible — logged here per the
build-loop severity rubric):

- **A-S4-1 — resume targets the most recent unmatched handoff.** When a task has
  more than one unmatched `handoff_created` (handed off, resumed, handed off
  again), the helper selects the **last** (most recent, insertion order from
  `_unmatched_handoffs`). Rationale: a resume answers the latest pause; the
  validator permits any unmatched source but LIFO is the deterministic,
  intuitive choice and keeps at most one open handoff after each resume.
- **A-S4-2 — return data, not an event.** The helper returns
  `{payload, parent_task_id, delegation_id}`, not a built or appended event, so
  it stays pure and CLI-agnostic (Fork A). The caller builds the event with the
  existing `_new_event(task_id, "task_resumed", payload, parent_task_id=...,
  delegation_id=...)`. Reversible; no new surface.
- **A-S4-3 — reject rather than guess on precondition failure.** No lifecycle
  events for the task, no eligible unmatched handoff, or a task that already has
  a terminal `task_finished`, each raise a bounded, no-echo `_error`
  (`TelemetryError`). Mirrors the subset #2/#3 diagnostic discipline.

No open question remains; no decision-log file exists in this repository.

## Threat model

| Boundary | Threat | Required control |
|---|---|---|
| Event-stream input | Caller passes events for a task with no unmatched handoff, or an already-finished task | Precondition checks raise a bounded `_error`; no event is fabricated |
| Linkage forgery | Constructed payload points `resumed_from_event_id` at a handoff whose `handoff_ref` differs, or at a `delegation_brief` handoff | Source is taken only from `_unmatched_handoffs` (excludes `delegation_brief`); `handoff_ref` copied from that same source; result re-validates through the unchanged `task_resumed` validator + `_validate_task_sequences` in the round-trip test |
| Task-ID / lineage drift | Resume event carries a different task ID or lineage pair | Helper reads the lineage pair from the task's first original and returns it unchanged; caller reuses the same `task_id` |
| Producer status | Constructing a resume flips the producer to `active` | Helper is pure; no activation path; `producers.json` untouched |
| Value echo | Diagnostics leak stream contents | `_error` raises a fixed message, never echoing the rejected value |

## Acceptance criteria

- A stream with one open handoff yields a payload with that handoff's
  `handoff_ref`, `resumed_from_event_id` = that handoff's `event_id`, and
  `resumed_from_handoff` literal `true`, plus the task's lineage pair.
- With multiple unmatched handoffs, the helper selects the most recent
  (A-S4-1); after a matching resume, the older handoff remains the only open
  one.
- A `handoff_created` with `reason=delegation_brief` is never selected.
- A delegated child task (non-null `parent_task_id`/`delegation_id`) round-trips
  with its lineage pair preserved.
- No lifecycle events, no eligible unmatched handoff, and an already-finished
  task are each rejected with a stable, no-echo error.
- The built event (helper payload + returned lineage) passes
  `_validate_payload("task_resumed", …)` and a full
  `validate_lifecycle_events` round-trip (start → handoff → resume → finish
  reports coverage `full`).
- The helper writes nothing (purity) and `telemetry/producers.json` is
  unchanged; no producer is activated.
- Targeted tests show red-before-green; canonical full gates and the reviewer
  chain pass on a frozen committed candidate.

## Candidate and invocation ledger

Candidate/base/tree IDs and changed paths are recorded at freeze. Reviewer
invocation rows and pre-freeze receipts are appended only after each fact
exists; this pre-registration claims no future evidence.

## Pre-freeze receipts (2026-07-23)

- Base HEAD at start: `f8cb45d` (subset #3), clean tree, branch
  `feature/telemetry-v3-b3`.
- Changed paths: `scripts/telemetry.py` (one added pure function
  `build_resume_linkage`, after `_unmatched_handoffs`),
  `scripts/tests/test_resume_linkage.py` (13 tests), this observation, and
  `plans/PLAN-phase6b-b3-subset4-resume-linkage.md`; closure-only
  `benchmarks/scorecard.jsonl` append. No `*.sh` in the diff
  (`bash -n`/`shellcheck` N/A). No new path/enum literal and no new
  byte-compared committed corpus (no `.gitattributes` change required).
- Red-before-green: with `build_resume_linkage` removed, the targeted suite
  reported `12 failed` (AttributeError at call for every test); restored,
  `13 passed` (a 13th test — real handoff selected over a `delegation_brief` —
  was added per the code-review NOTE and re-run green).
- Full gates on the working tree: `python3 scripts/validate.py` `✓ all checks
  green`; `python3 -m pytest scripts/tests -q` `432 passed, 3 skipped`;
  `python3 -m ruff check …` `All checks passed`; `git diff --check` clean.
  `mypy` report-only and not installable in-sandbox (skipped, non-blocking
  per R1).
- Producer unchanged: `telemetry/producers.json` `task-handoff.status` remains
  `planned`, `event_id` null.

## Reviewer chain (2026-07-23)

- plan-reviewer: `APPROVE` — 0 blockers; 2 WARN (echo `task_id` back; add the
  all-consumed error test) + 1 NOTE (input-immutability assert) all folded into
  the plan before the first product edit. Confirmed LIFO safe (helper shares
  `_unmatched_handoffs`' exact predicate with the validator, so it cannot build
  a rejected event) and the finished-task precondition matches the contract.
- qa-agent: static attack pass across ten spec-edge vectors, zero defects
  (delegation_brief non-resumable, LIFO + older-remains, round-trip to `full`,
  finished/empty/all-consumed rejected, corrections ignored, pure/no-write,
  producer planned). Gate execution unavailable in its sandbox; supplied by the
  builder's verified green run above (disclosed build-loop substitution: gates
  are deterministic; diff scope confirmed, no `*.sh`).
- code-reviewer: `APPROVE`. No blockers, no duplication, no scaffolding; chose
  `_error` over `_lifecycle_error` (avoids a spurious path echo for a file-less
  helper) — flagged as a positive exemplar of the 2026-07-23 no-echo/POSIX
  lessons, not a new lesson. One optional NOTE (mixed delegation_brief stream)
  applied as the 13th test.
- security-reviewer: SKIPPED — argued. The diff touches none of the 6b trigger
  surfaces (no auth, no new untrusted-input parse — `handoff_ref` is copied from
  already-validated event data, no file write, no CLI/endpoint, no permission
  or money). Both code-reviewer and the builder concur.

The closure commit is the commit introducing this section plus the scorecard
append; it is identified by Git history, never by a self-referential hash.
