# PLAN — Phase 6B B3 subset #4: task/handoff resume-linkage helper (Fork A)

Observation: `docs/spikes/phase-6b/b3-subset4-observation.md`
(task `663e1041-c771-4e35-81ae-110c56133a9e`).
Branch `feature/telemetry-v3-b3`, base HEAD `f8cb45d` (subset #3), clean tree.

## Goal

Discharge the `task-handoff` producer's linkage responsibility (telemetry-v3
line 598 — "emit `task_resumed.resumed_from_handoff=true`, preserve the original
task ID across handoff, and preserve parent/delegation linkage") with a single
**pure constructor** that computes a linkage-correct `task_resumed` from an
already-validated event stream, so callers stop hand-building the payload and
its `resumed_from_event_id`/`handoff_ref`. Producer stays `planned`; no CLI, no
activation, no receipt — the subset #3 payload-only precedent.

## Why this is the gap (not new validation)

`_validate_task_sequences`, `_validate_delegations`, and `_expected_coverage`
already enforce every linkage invariant. The `append` CLI already emits these
events from raw `--payload-json`. What is missing is anything that *constructs*
a correct `task_resumed` — today a caller must locate the unmatched
`handoff_created` event_id, copy its `handoff_ref`, and set
`resumed_from_handoff=true` by hand. That construction burden is exactly the
producer responsibility; Fork A puts it in one tested pure function.

## Scope (immutable)

IN: one pure helper + its tests. OUT: CLI subcommands (Fork B),
delegation-creation helper, activation, report views, export, any validator or
schema change. Enforced by the observation's non-goals.

## Design

Add to `scripts/telemetry.py` (near the existing lifecycle helpers, after
`_unmatched_handoffs`):

```python
def build_resume_linkage(events, task_id) -> dict:
    """Derive the linkage-correct task_resumed payload and lineage for task_id.

    Pure: reads an already-validated event stream and returns
    {"task_id": ..., "payload": {...}, "parent_task_id": ...,
    "delegation_id": ...}. Emits nothing, writes nothing, activates no
    producer. Echoing task_id back makes the caller's original-task-ID
    preservation foolproof: build the event with
    _new_event(result["task_id"], "task_resumed", result["payload"],
    parent_task_id=result["parent_task_id"],
    delegation_id=result["delegation_id"]) (plan-reviewer WARN 4).
    """
```

Behaviour:
1. `task_events = _task_originals(events, task_id)`; empty → `_error` (A-S4-3).
2. If the task's last original is `task_finished` → `_error` (cannot resume a
   completed/terminal task) (A-S4-3).
3. `unmatched = _unmatched_handoffs(task_events)` (already excludes
   `delegation_brief`); empty → `_error` "no unmatched handoff to resume".
4. Select the **last** unmatched entry (A-S4-1, LIFO). `source_id`,
   `source = unmatched[source_id]`.
5. `lineage = task_events[0]["lineage"]`.
6. Return `{"task_id": task_id, "payload": {"handoff_ref":
   source["payload"]["handoff_ref"], "resumed_from_handoff": True,
   "resumed_from_event_id": source_id},
   "parent_task_id": lineage["parent_task_id"],
   "delegation_id": lineage["delegation_id"]}`.

No new module-level path or enum literal is introduced (avoids the `str(Path)`
cross-platform trap); no new committed byte-compared corpus is introduced
(avoids the `.gitattributes eol=lf` trap). Reuses the existing `_error`,
`_task_originals`, `_unmatched_handoffs`.

## Tests — `scripts/tests/test_resume_linkage.py` (red-before-green)

Helpers build events with `_new_event` / append via a temp lifecycle file,
mirroring `test_telemetry_runtime.py`.

1. Single open handoff → payload `handoff_ref`/`resumed_from_event_id`/
   `resumed_from_handoff=true` correct; lineage pair `(None, None)`.
2. Two unmatched handoffs → selects the most recent (A-S4-1).
3. After a resume consumes the newer handoff, a second call selects the older
   remaining one.
4. `handoff_created` with `reason=delegation_brief` is never selected (a task
   with only a delegation_brief handoff → "no unmatched handoff" error).
5. Delegated child task (non-null parent/delegation) → lineage pair preserved
   in the returned dict.
6. No lifecycle events for the task → stable error, no value echo.
7. Already-finished task → stable error.
8. **Round-trip**: build `task_started` → `handoff_created` → resume event from
   the helper → `task_finished`; `validate_lifecycle_events` accepts it and the
   task's coverage is `full`.
9. Helper writes nothing (assert the lifecycle file is unchanged / absent after
   a call) — purity.
10. Returned payload passes `_validate_payload("task_resumed", payload)`
    directly.
11. Handoff created **and already resumed** (one created+resumed pair, nothing
    open) → stable "no unmatched handoff" error — the distinct all-consumed
    precondition branch (plan-reviewer WARN 7).
12. Input immutability: the passed `events` sequence is unchanged after the call
    (plan-reviewer NOTE 8), complementing the on-disk purity check (#9).

Red-before-green: with `build_resume_linkage` removed, the suite fails at import
/ NameError for every constructor test (round-trip and purity included); with it
restored, all pass.

## Gates (canonical, from `docs/agent-working-rules.md`)

`python scripts/validate.py` · `pytest scripts/tests` · `git diff --check` ·
`ruff check .`. No `*.sh` touched → `bash -n`/`shellcheck` N/A (state in
report). `mypy` report-only, non-blocking (R1). No new gate command is added, so
no red-before-green-on-the-gate step is required.

## Reviewer chain

plan-reviewer (this step) → build → qa-agent → code-reviewer →
security-reviewer **only if triggered**. Trigger analysis: the helper reads an
already-validated in-memory stream, copies an existing `handoff_ref` (does not
parse a new untrusted path), writes no file, adds no public endpoint or
permission change. Expected: 6b **skipped with reason**; final call deferred to
code-reviewer. → regression qa if any fix lands.

## Risks & rollback

- Risk: wrong unmatched-handoff selection semantics. Mitigation: A-S4-1 stated;
  test 2/3 pin LIFO; round-trip test proves validator acceptance.
- Risk: helper diverges from validator expectations. Mitigation: tests 8 & 10
  validate the built event through the unchanged validators — no second source
  of truth.
- Rollback: single new function + one new test file; revert the commit. No
  migration, no data, no schema.

## Budget & demo

~40-60 product lines + ~10 tests, well under the ~500-line B3-subset ceiling.
Stop for REPLAN on any need to touch a validator, schema, the CLI parser, or
`producers.json`.

Demo: in a REPL, append `task_started`+`handoff_created` for a task, call
`build_resume_linkage(events, task_id)`, build the event, append
`task_finished`, run `validate_lifecycle_events` → coverage `full`; show
`producers.json` unchanged.
