# Phase 6B B1 observation and review ledger

## Pre-registration

- Task ID: `60ac8d19-2839-4652-8863-ecf565724642`.
- Registered at: `2026-07-22T05:54:42Z`.
- Registration base commit: `191f618a2824186ec099381bb491bd16b4b44452`.
- Registration base tree: `345913380399fc2668d5ee1f65b9a134381de037`.
- Immutable slice: B1 schema, local single-writer storage, validation,
  duplicate-event-ID rejection, correction linkage and authority,
  prior-byte preservation, interrupted-final-append recovery, and
  privacy/source-class rejection at the storage boundary.
- Explicit non-goals: lifecycle CLI and task propagation (B2), producers and
  reports (B3), durable export/import/retention (B4), and release closure (B5).
- Intended product paths:
  `scripts/telemetry.py`, `telemetry/schema-v3.json`,
  `telemetry/.gitignore`, and `scripts/tests/test_telemetry_runtime.py`.
- Evidence path: `docs/spikes/phase-6b/b1-observation.md`.
- Reviewer sequence: QA -> software-dev code review -> security review ->
  final regression QA. Re-review is findings-scoped only.
- Security trigger: **yes**. B1 handles repository-relative paths, local file
  creation/recovery, caller-supplied event metadata, privacy rejection, and
  correction evidence authority.
- Runtime token attribution: `unknown / unsupported_provider`. Dispatch bytes
  are recorded only as a context-size proxy.

This task is the first eligible observation unit. The plan's per-slice protocol
applies to B1-B4 implementation slices; completed B0 was governance admission,
not an implementation slice, and therefore is outside that population. This
classification is fixed before B1 results are known.

## Ground-truth answers and auto-decisions

1. The persisted schema is the closed Telemetry v3 envelope and all closed
   payload shapes in `docs/contracts/telemetry-v3.md` T3.2-T3.6.
2. B1 validates persisted event and corpus invariants needed by the storage
   boundary. It exposes no `start | append | finish | validate` lifecycle CLI;
   those commands remain B2.
3. The only B1 write target is `telemetry/events.jsonl` under an explicitly
   supplied canonical repository root. Durable benchmark writes remain B4.
4. Producer identity is injected through a registered channel argument rather
   than accepted from event input. Correction evidence is verified through a
   channel-owned resolver before append, per T3.7.
5. The new targeted pytest cases are treated as the changed gate surface: a
   failing pre-implementation run is captured before the first product edit,
   followed by the green run and the full declared gates.
6. `telemetry/events.jsonl` is ignored locally; the schema and ignore rule are
   tracked. Tests write only beneath pytest temporary repository roots.

## Planned test cases

- Closed schema accepts one complete event for every event type and rejects
  unknown or missing fields, invalid UUID/timestamp/string/path grammars,
  unsorted/duplicate/bounded arrays, invalid coverage/tokens/elapsed pairs,
  and records over 65,536 encoded bytes.
- Storage appends exactly one UTF-8 JSON object plus LF, rejects duplicate IDs,
  preserves all prior bytes, and flushes before success.
- Recovery truncates only an interrupted final record; corrupt UTF-8 or an
  invalid interior/complete record fails without mutation.
- Correction chains preserve target bytes and immutable fields, allow only
  replacement fields plus permitted evidence fields/privacy tightening, and
  reject missing, forward, self, cyclic, cross-channel, or unauthorized links.
- The fixed local path rejects traversal, symlink/reparse components, hard
  links, non-regular files, containment ambiguity, and path replacement.
- Privacy/source handling rejects forbidden values and never echoes them in a
  diagnostic.

## Candidate and invocation ledger

Candidate facts and one row per reviewer invocation are appended only after a
clean committed candidate exists.

## Red-before-green receipt

- Command: `C:\Users\lateo\AppData\Local\Programs\Python\Python312\python.exe -m pytest scripts/tests/test_telemetry_runtime.py -q`.
- Pre-implementation result: collection failed with
  `ModuleNotFoundError: No module named 'telemetry'` because the intended
  `scripts/telemetry.py` product path did not yet exist.
- A preceding `python -m pytest` attempt used the host agent virtual
  environment, which has no pytest installation. It is an environment probe,
  not the red receipt above.
- Green command: the same installed Python 3.12 module invocation.
- Pre-freeze result: `26 passed, 1 skipped`. The skip is the Windows host's
  unavailable unprivileged symlink fixture; hard-link, containment, recovery,
  correction-authority, privacy, and 65,537-byte attack cases ran.
