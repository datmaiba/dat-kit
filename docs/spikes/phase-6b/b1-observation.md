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

Final product candidate:

- Commit: `049c3ce63434cc18e25c5882c7f823ad6b1f7100`.
- Tree: `772879e34ff3f5e7335e5c92df430556204f3d21`.
- Base: `191f618a2824186ec099381bb491bd16b4b44452`.
- Changed paths from base: the five pre-registered paths above, all added.
- Canonical gates: validator PASS; full pytest `324 passed, 7 skipped`;
  targeted B1 pytest `33 passed, 1 skipped`; Bash syntax PASS; ShellCheck
  PASS; diff check PASS.
- Final verdicts: QA `PHASE DONE`; code review `APPROVE`; security review
  `APPROVE`; final regression QA `PHASE DONE`.

Tokens are `unknown / unsupported_provider` for every invocation. Elapsed time
was not exposed by the reviewer runtime. Dispatch bytes count only the compact
prompt intentionally supplied to that invocation.

| Ordinal | Role | Candidate/tree transition | Scope / restart | Cause, trigger, or finding IDs | Verdict | Dispatch bytes | Invalidation | Avoidable under narrow rule |
|---|---|---|---|---|---|---:|---|---|
| 1 | QA | `b340b21/3e99d6f` -> `6807e9a/c50a32c` | full / none | initial B1 QA; `QA-1` cross-channel diagnostic | `RETURN TO BUILDER` | 2492 | semantic source/test fix | no: initial QA |
| 2 | QA | `6807e9a/c50a32c` -> same | findings / 1 | `QA-1` | `PHASE DONE` | 1079 | later semantic code-review fixes | no: findings re-review |
| 3 | code | `6807e9a/c50a32c` -> `6f3ee62/2db4f12` | full / none | `CODE-1` through `CODE-5` | `RETURN TO BUILDER` | 2163 | semantic source/test fixes | no: initial code review |
| 4 | code | `6f3ee62/2db4f12` -> same | findings / 3 | `CODE-1` remained open; `CODE-2..5` resolved | `RETURN TO BUILDER` | 1394 | authority finding remained open | no: findings re-review |
| 5 | code | `6f3ee62/2db4f12` -> `e89b89a/3376a05` | findings advisory / 4 | minimum trusted-composition design for `CODE-1` | `REVISE` | 857 | semantic authority refactor | no: open-finding consultation |
| 6 | code | `e89b89a/3376a05` -> same | findings / 4 | `CODE-1` | `APPROVE` | 1494 | later semantic security fixes | no: findings re-review |
| 7 | security | `e89b89a/3376a05` -> `049c3ce/772879e` | full / none | path/input trigger; `SEC-1`, `SEC-2` | `RETURN TO BUILDER` | 2721 | semantic policy/source/test/schema fixes | no: initial security review |
| 8 | security | `049c3ce/772879e` -> same | findings / 7 | `SEC-1`, `SEC-2` | `APPROVE` | 1726 | none | no: findings re-review |
| 9 | QA | `049c3ce/772879e` -> same | full final regression / none | mandatory final regression; no open findings | `PHASE DONE` | 1779 | none | no: final regression QA is mandatory |
| 10 | QA | `624119e/4367730` -> same | full closure regression / none | mandatory closure-tree proof; no open findings | `PHASE DONE` | 1640 | none | no: final regression QA is mandatory |

Observed: 10 invocations, 5 full, 4 findings-scoped, 1 findings advisory,
17,345 dispatch bytes, and 0 avoidable invocations. Every restart was initial,
findings-driven, or mandatory; no verdict was reused.

Scorecard record: `benchmarks/scorecard.jsonl` line 32, schema v2, complexity
4, estimated manual effort 12 hours, actual wall time 57 minutes, tokens
`null`, attribution `unknown / unsupported_provider`.

## Closure receipt and classification

- Closure commit: `624119ee2f90a7ce37c67700a0637a46e22008bd`.
- Closure tree: `436773041efae09d7999db79aee05b3b8792ffe1`.
- Candidate-to-closure paths: only `benchmarks/scorecard.jsonl` and this
  task-local ledger/report.
- Closure validator: PASS.
- Closure regression: validator PASS; full pytest `324 passed, 7 skipped`;
  targeted B1 pytest `33 passed, 1 skipped`; Bash syntax PASS; ShellCheck
  PASS; diff check PASS. Outcomes were unchanged from the product candidate.
- QA classification: `mechanically pure closure-only`. All four pre-registered
  conditions passed and no reviewer finding was open.
- Counterfactual result: 0 avoidable invocations. The closure regression QA is
  mandatory, and no passing code or security verdict was rerun across the
  closure-only transition.

This follow-up document edit is the receipt for the already-reviewed closure
commit above; it is not presented as part of that reviewed tree.

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
