# PLAN — Phase 6B B3 subset #2: diagnosing-bugs defect projection

**Status:** DRAFT — awaiting plan-reviewer, then explicit user approval. No
product files may be edited until approved.
**Canonical contract:** dat-kit 1.16.0
**Branch:** `feature/telemetry-v3-b3` · **Base HEAD:** `72ca145`
**Workflow:** `dat-kit:build-loop`, `software-dev` Domain Pack, attended.

## Approved scope decisions (user, 2026-07-23)

- **D-S2-1 (export scope):** Build the **defect-specific projection only** —
  the `defect_recorded → benchmarks/defects.jsonl` path required by T3.10.2 and
  the line-134 receipt matrix. General multi-target export / aggregation /
  import stays in **B4**.
- **D-S2-2 (activation):** **Runtime only; producer stays `planned`.** No
  synthetic or retroactive receipt. `telemetry/producers.py` activation block is
  NOT touched. `diagnosing-bugs` remains `planned`, `event_id` null. Activation
  waits for a genuine post-mortem defect in a later candidate.

## SELF-Q&A (answered from the contract)

1. **Defect tuple?** → `defect_id` (stable-id), `introduced_task` (UUIDv4 or
   null), `approving_reviewers` (sorted-unique stable-id array ≤64),
   `gate_that_should_have_caught_it` (stable-id), `evidence_ref` (stable-ref,
   non-null). Source: telemetry-v3 §T3 event table (line 278);
   `scripts/telemetry.py:517-523` already validates this exactly.
2. **Projection record shape?** → the closed **13-field** record in T3.10.2
   (table rows lines 515-527): `schema_version`=int `3`, `event_id`, `task_id`,
   `parent_task_id`, `delegation_id`, `correction_of`,
   `correction_evidence_ref`, `occurred_at`, `defect_id`, `introduced_task`,
   `approving_reviewers`, `gate_that_should_have_caught_it`, `evidence_ref`.
   "The projection has no other fields." (13 rows — the validator and Test #1
   enforce exactly these 13 keys; the parent handoff's "12-field" phrasing is
   an error, do not trust it.)
3. **Export semantics?** → idempotent by `event_id`: identical event = no-op;
   same id + different canonical bytes = `TELEMETRY_EXPORT_COLLISION`; new event
   appends exactly one record and never rewrites existing benchmark bytes
   (T3.10.2 lines 533-538). Verify + record the target's prior-byte hash before
   the batch; emit `benchmark_exported` (target `benchmarks/defects.jsonl`)
   **only after** the target append succeeds (lines 540-541). Partial failure
   leaves valid append-only records intact and reports unexported IDs.
4. **Corrections?** → a corrected defect appends a NEW projection record with
   its new `event_id` and `correction_of`; it never rewrites the prior
   projection (lines 529-531). Consumers resolve the chain by source event
   identity.
5. **Where does the source event live?** → local stream
   `telemetry/events.jsonl` (gitignored); read via `validate_local_events`
   (`telemetry.py:1018`). The durable projection `benchmarks/defects.jsonl` is
   the committed, append-only artifact (does not exist yet).
6. **`benchmark_exported` never re-exports itself?** → correct; receipts are
   never export-eligible and never appear in `exported_event_ids` (line 545).
7. **Producer activation?** → out of scope by D-S2-2. `producers.py` already
   rejects any `active` entry; leaving `diagnosing-bugs` `planned` needs no
   change there.

**OPEN QUESTIONS for the user:** none remain — both forks were resolved above.
Any new high-severity question surfacing during BUILD stops per the rubric.

## Scope

### IN
1. A **defect projection writer** in `scripts/telemetry.py`: read validated
   local events, select `defect_recorded`, build the exact T3.10.2 record,
   append append-only to `benchmarks/defects.jsonl`, idempotent by `event_id`,
   reusing the module's existing path-safety discipline (lstat / `O_NOFOLLOW` /
   link-like rejection) because this WRITES a committed file.
2. Emit `benchmark_exported` (required `export_batch_id` UUIDv4, target
   `benchmarks/defects.jsonl`, `prior_hash` = sha256 of the pre-batch target
   bytes **or null for the first append into an empty file**, sorted-unique
   `exported_event_ids`) into the local stream **only after** the durable append
   succeeds. The receipt is a normal lifecycle append: the `export` subcommand
   takes `--task-id <uuid>` naming an already-`started` task in the stream, so
   the receipt carries that task's lineage and validates against its lifecycle
   corpus exactly like any other appended event (`_append_lifecycle_event`).
   `producer.id` is channel-injected as `dat-kit-cli` (never `diagnosing-bugs`).
3. A **CLI subcommand** `export --task-id <uuid> --target benchmarks/defects.jsonl`
   (defect projection only) wired into `_parser()` / `_execute_command()`,
   honoring `DAT_KIT_TELEMETRY=off` (no writes, non-error disabled result) like
   the other write commands.
4. A **consuming validator** for `benchmarks/defects.jsonl`: closed **13-field**
   shape, append-only, correction chain by source event identity. Rerun after
   each append (handoff requirement) AND wired into `scripts/validate.py` so the
   standard gate checks the durable file, not only a manual rerun.
   The projection is written and byte-compared for `TELEMETRY_EXPORT_COLLISION`
   using the module's canonical encoder (`json.dumps(..., sort_keys=True,
   separators=(",", ":"))` + terminal LF) — one deterministic encoding for both
   write and collision comparison.
5. **Red-before-green tests** in `scripts/tests/` (new
   `test_telemetry_defect_projection.py`, plus additions to
   `test_telemetry_cli.py`).
6. **Observation** pre-registration appended to
   `docs/spikes/phase-6b/b3-observation.md` (task ID, immutable slice scope,
   intended paths, reviewer roles) as BUILD step 0. BUILD step 0 also runs
   `python scripts/registry.py explain-evolution <path>` for each new path
   (`benchmarks/defects.jsonl`, the new test file) to confirm no
   `EVOLUTION_ORPHAN_PATH` (both fall under the `benchmarks`/`scripts` governed
   roots per `registry/evolution.json`, so admission is expected).
7. `benchmarks/defects.jsonl` created as a new committed artifact (may start
   empty until the demo/export runs).

### OUT (explicitly)
- Activating `diagnosing-bugs` or any producer (D-S2-2).
- Editing the `producers.py` activation block or `producers.json` statuses.
- General export to `benchmarks/telemetry-v3.jsonl`, aggregation, v2→v3 import,
  retention/prune — all **B4**.
- Any Host Adapter / resolver / capability transport for HARVEST (T3.12
  deferment, untouched).
- Backfilling a `defect_recorded` from subset #1 prose or any historic
  post-mortem.

## Files (create/modify)

| Path | Change |
|---|---|
| `scripts/telemetry.py` | + defect-projection writer, + `export` subcommand, + `benchmarks/defects.jsonl` consuming validator helper (closed 13-field) |
| `scripts/validate.py` | + call the projection consuming validator on `benchmarks/defects.jsonl` so the standard gate covers it |
| `scripts/tests/test_telemetry_defect_projection.py` | NEW — projection shape, idempotency, receipt ordering, correction chain, path-safety, disabled behavior |
| `scripts/tests/test_telemetry_cli.py` | + `export` CLI happy-path / collision / disabled cases |
| `benchmarks/defects.jsonl` | NEW committed append-only durable artifact |
| `docs/spikes/phase-6b/b3-observation.md` | + subset #2 observation pre-registration (append only) |
| `benchmarks/scorecard.jsonl` | + one v2 record at HARVEST (append only) |

**No** change to: `telemetry/producers.py`, `telemetry/producers.json`,
`telemetry/schema-v3.json` (projection is a committed artifact, not a v3 event —
no new event type or payload field), `docs/contracts/telemetry-v3.md`.

## Threat model

| Threat | Mitigation |
|---|---|
| Symlink / path-traversal on the committed target `benchmarks/defects.jsonl` (WRITE surface) | Reuse existing `_verify_parent` / `O_NOFOLLOW` / lstat / link-like checks; fail closed `TELEMETRY_HISTORY_CORRUPT` |
| Retroactive rewrite of durable history (T3.1 ban) | Append-only; same-id-different-bytes → `TELEMETRY_EXPORT_COLLISION`, never overwrite |
| Receipt emitted before durable append (false "exported") | Emit `benchmark_exported` strictly after target append confirmed |
| Partial batch failure corrupts corpus | Leave valid records intact, report unexported IDs, retry deduplicates by `event_id` |
| Rejected CLI input echoed into logs (subset #1 lesson) | Diagnostics name field/path only, never echo the rejected value; test `--flag value` and `--flag=value` |
| Activation-authority creep | Writer/CLI accept no task UUID/ref as authority to activate; producer registry untouched (assert in tests) |
| Corrupt/interrupted source stream | Reuse `validate_local_events` guarantees; interrupted trailing record already fails closed |

## Test list (red-before-green — this ADDS a gate/command, so prove red first)

1. Projection record equals exactly the **13** T3.10.2 fields (closed key set),
   emitted with the canonical encoder — no missing, no extra field.
2. Idempotent no-op: re-export identical event → zero new bytes, no new receipt.
3. Collision: same `event_id`, different canonical bytes → `TELEMETRY_EXPORT_COLLISION`,
   no mutation.
4. Append: new defect → exactly one new projection record + one
   `benchmark_exported` receipt in the local stream. First append into the
   newly-created empty file uses `prior_hash: null`; the receipt validates
   against its owning `--task-id` lifecycle corpus.
5. Receipt ordering: simulated target-append failure → NO `benchmark_exported`
   emitted, corpus unchanged.
6. Correction chain: corrected defect → new record with `correction_of`, prior
   record byte-preserved.
7. Path-safety: link-like `benchmarks/defects.jsonl` parent/target → fail closed,
   no write.
8. Disabled: `DAT_KIT_TELEMETRY=off` → export performs no writes, non-error
   disabled result.
9. Rejected-value redaction: bad `--target` value not echoed; both `--flag value`
   and `--flag=value` forms.
10. Producer registry unchanged: `diagnosing-bugs` still `planned`, `event_id`
    null after export.
11. Consuming validator rejects a malformed projection line (extra field / wrong
    type / rewritten prior record).
12. Gate red-before-green: break the projection writer once, confirm the new
    test goes red, revert, confirm green.

## Quality gates (from AGENTS.md → agent-working-rules)

```
python scripts/validate.py
pytest scripts/tests
bash -n scripts/init.sh
shellcheck scripts/init.sh
git diff --check
```
Plus targeted: `pytest scripts/tests/test_telemetry_defect_projection.py
scripts/tests/test_telemetry_cli.py -q`. QA intake follows R1 (review-evidence
receipt if present for the candidate SHA; else documented local fallback).

## Reviewer chain

plan-reviewer (now) → BUILD → qa-agent (loop to PHASE DONE) → code-reviewer
(loop to APPROVE) → **security-reviewer** (triggered: new committed-file write,
path handling, durable external artifact) → regression qa → HARVEST. Reviewers
sequential, findings-scoped, Opus.

**HARVEST ordering (mandatory):** run the scorecard append to
`benchmarks/scorecard.jsonl` FIRST, then re-run `python scripts/validate.py`
**after** that append — the gate reads the scorecard back, so the append must
precede its own validation (lessons-learned 2026-07-21; handoff trap: "The
scorecard append must be followed by `python scripts/validate.py`").

## Rollback

All changes additive. Revert = drop the subset #2 commit(s) and delete
`benchmarks/defects.jsonl`. No producer-status migration, no schema change, no
contract amendment → nothing to unwind in `telemetry/` state.

## Budget

One reviewable candidate. Est. ~2 commits: (a) runtime + validator + tests,
(b) observation/docs. Runtime edit is a bounded addition to one module reusing
existing helpers; no cross-host or capability work.

## Demo

1. On a temp repo root, `telemetry start`, `telemetry append` a `defect_recorded`
   with the required tuple.
2. `telemetry export --target benchmarks/defects.jsonl` → show the projection
   record matches T3.10.2 field-for-field; show the `benchmark_exported` receipt
   in the local stream.
3. Re-run export → no-op (no new bytes, no new receipt).
4. `telemetry validate` + `python scripts/validate.py` → PASS.
5. Show `telemetry/producers.json` still five `planned` producers.

## Observation pre-registration (materialized as BUILD step 0)

- Slice: B3 subset #2 defect projection, immutable scope = the IN list above.
- Intended paths: exactly the Files table.
- Reviewer roles: plan, qa, software-dev (code), security.
- Receipt matrix row `diagnosing-bugs` stays OPEN (planned) — this subset
  delivers the projection runtime, not the activation receipt.
