# Telemetry v3 contract

- Contract revision: `telemetry-v3/1`
- Event schema version: `3`
- Governance: Class C under `platform-contract-policy/1`
- Status: proposed; not effective until an authorized decision names an
  `effective_from_run`

This contract defines the host-neutral Telemetry v3 event model for dat-kit
2.1. It is normative for future producers, validators, storage, imports,
exports, retention, reports, disable behavior, and downgrade behavior.
`PLAN-v7-platform.md` section 3.10, Phase 6, and section 13.2 are its approved
program source.

No implementation may claim Telemetry v3 conformance, create the local event
stream, or mark a producer `active` before this contract has both required
independent reviews and an authorized `platform-owner` decision. In
particular, this proposal does not authorize `scripts/telemetry.py`, a
`telemetry/` root, hooks, rendered triggers, or benchmark data files.

## T3.1 Scope and non-goals

Telemetry v3 records task lifecycle evidence needed to evaluate dat-kit's
work loops without turning telemetry into authority. Events describe what ran,
which contract and producer revisions were involved, what gates and reviewers
reported, what rework followed, and how complete the observation was.

Telemetry does not approve a plan, close a gate, merge a change, modify a
Domain Pack, or make an evolution decision. Human and reviewer authority stays
where the governing workflow places it. Raw prompts and secrets are not
telemetry inputs.

The following are explicitly outside v3:

- automatic self-evolution or automatic merge authority;
- multi-writer correctness or a multi-process locking claim;
- retroactive rewriting of scorecard, defect, or telemetry history;
- inferred token counts, inferred elapsed time, or inferred reviewer verdicts;
- guaranteed full coverage on hosts that cannot emit lifecycle-start events.

## T3.2 Storage surfaces and ownership boundary

The v3 surfaces are exact:

| Surface | Role | Durability |
|---|---|---|
| `telemetry/events.jsonl` | machine-local working event stream | local, uncommitted, not a cross-machine corpus |
| `benchmarks/telemetry-v3.jsonl` | general exported v3 event corpus | committed, append-only |
| `benchmarks/defects.jsonl` | defect producer's durable projection | committed, append-only |
| `benchmarks/scorecard.jsonl` | existing scorecard history and legacy import source | committed, append-only; existing bytes stay untouched |

This contract governs semantics only. Before a future phase creates
`scripts/telemetry.py` or any path under `telemetry/`, that phase must first
resolve their current `EVOLUTION_ORPHAN_PATH` results with narrowly scoped
governed ownership. A broad glob that merely hides an orphan diagnostic is not
conformance.

Every JSONL surface uses UTF-8, one closed JSON object per line, and one
terminal LF per complete record. Unknown fields are invalid. A reader may
recover one interrupted final record as specified in T3.8; it may not skip an
invalid interior record.

## T3.3 Closed event envelope

Every v3 event contains exactly these required top-level fields:

| Field | Type and rule |
|---|---|
| `schema_version` | integer literal `3` |
| `event_id` | canonical lowercase UUIDv4 string; unique across the corpus |
| `task_id` | canonical lowercase UUIDv4 string |
| `event_type` | one closed event-type value from T3.6 |
| `occurred_at` | RFC 3339 UTC timestamp ending in `Z`; describes when this record was emitted |
| `producer` | closed object `{id, revision}`; both are non-empty stable strings |
| `revisions` | closed object with all revision references in T3.4 |
| `lineage` | closed object `{parent_task_id, delegation_id, correction_of}`; every key is present and nullable |
| `source_class` | `runtime | repository | human | legacy_import | derived` |
| `privacy_class` | `public | project | local_private` |
| `coverage` | closed coverage object from T3.5 |
| `tokens` | closed token-attribution object from T3.5 |
| `elapsed` | closed elapsed-attribution object from T3.5 |
| `payload` | the closed object selected by `event_type` in T3.6 |

UUID values use the textual `8-4-4-4-12` form. Nil UUIDs and non-v4 UUIDs are
invalid. Nullable fields use JSON `null`; an empty string is never a null
substitute. Arrays described as sets are sorted, contain no duplicates, and
use the identity rules of their element type.

### T3.3.1 Source and privacy classes

`source_class` describes provenance:

- `runtime`: emitted directly by a work-loop runtime or host adapter;
- `repository`: derived from a tracked repository artifact or gate result;
- `human`: an explicit owner or human-run gate/review verdict;
- `legacy_import`: derived from a pre-v3 durable record;
- `derived`: calculated only from already-valid v3 events.

`privacy_class` describes the maximum handling boundary:

- `public`: already public, allowlisted metadata;
- `project`: project-scoped allowlisted metadata that may enter committed
  benchmarks;
- `local_private`: allowlisted metadata that must remain local and must never
  be exported.

A class is not permission to copy arbitrary source content. T3.9's field
allowlist and forbidden-value rules always win.

## T3.4 Revision references

`revisions` contains exactly these required keys:

`domain`, `engine`, `adapter`, `canonical_contract`, and `profile`.

Each value is a closed object `{value, unavailable_reason}`. Exactly one is
non-null:

- `value` is a non-empty stable revision string and `unavailable_reason` is
  null; or
- `value` is null and `unavailable_reason` is one of
  `not_applicable | not_emitted | unsupported_host | legacy_source | ambiguous`.

Missing revision data must never be filled from memory or guessed from a
nearby checkout. `producer.revision` follows the same honesty rule but is
required: a producer unable to identify its own revision must not emit a v3
event.

## T3.5 Coverage and attribution

### T3.5.1 Coverage

`coverage` contains exactly `{status, missing_event_types, reason}`:

- `status` is `full | partial`;
- `missing_event_types` is a sorted unique array of T3.6 event types;
- `reason` is null for `full`, otherwise exactly one of
  `completion_only | unsupported_host_start | telemetry_disabled | legacy_import | producer_failure`.

`full` requires an empty missing list and a null reason. `partial` requires a
non-empty missing list and a non-null reason. Partial coverage is valid data,
not an error to hide. A completion-only scorecard may mint a task ID, but its
events must use `partial` with reason `completion_only` and name the lifecycle
events that were not observed.

### T3.5.2 Tokens

`tokens` contains exactly `{total, attribution_status, reason}`.
`attribution_status` is `exact | unknown`:

- `exact`: `total` is a non-negative integer and `reason` is null;
- `unknown`: `total` is null and `reason` is one of
  `unsupported_provider | missing_timestamp | no_matching_session |
  multiple_matching_sessions | ambiguous_multi_task_session | not_reported |
  legacy_source | telemetry_disabled`.

Estimates are forbidden. The existing scorecard v2 unknown reasons retain
their current meaning.

### T3.5.3 Elapsed time

`elapsed` contains exactly `{milliseconds, clock_source, reason}`:

- measured: `milliseconds` is a non-negative integer, `clock_source` is
  `monotonic | wall`, and `reason` is null;
- unknown: `milliseconds` is null, `clock_source` is `unknown`, and `reason`
  is `not_reported | unsupported_host | ambiguous | legacy_source |
  telemetry_disabled`.

Durations prefer a monotonic clock. A wall-clock duration is permitted only
when labeled `wall`; clock corrections must not silently produce a negative
duration.

## T3.6 Lifecycle and closed event payloads

The normal lifecycle is:

```text
task_started -> work/gate/review/handoff/delegation events -> task_finished
```

The task UUIDv4 is minted at LOAD, before SELF-QUESTION or its domain
equivalent. The same `task_id` propagates through gates, reviews, handoffs,
HARVEST, and finish. A completion-only degraded producer is the sole path that
may mint the task ID at finish; T3.5.1 then requires partial coverage.

Each payload contains exactly the fields below. `string` means non-empty.
`path` means a canonical repository-relative POSIX path; absolute paths and
`..` segments are invalid. `verdict_source` is always
`human | agent | automation`.

The load-bearing named fields include `resumed_from_handoff`, `first_pass`,
`verdict_source`, `introduced_task`, `approving_reviewers`,
`gate_that_should_have_caught_it`, and `kit_facing`; their exact owning
payloads and types are fixed below.

| `event_type` | Exact payload fields |
|---|---|
| `task_started` | `{workflow: string, resumed_from_handoff: bool, handoff_ref: path|null}` |
| `task_finished` | `{outcome: completed|aborted|unknown, scorecard_ref: path|null}` |
| `handoff_created` | `{handoff_ref: path, reason: context_ceiling|deliberate_pause|delegation_brief}` |
| `task_resumed` | `{handoff_ref: path, resumed_from_task_id: UUIDv4}` |
| `delegation_started` | `{child_task_id: UUIDv4, delegated_role: string, brief_ref: path}` |
| `gate_result` | `{gate_id: string, outcome: pass|fail|skipped, first_pass: bool, verdict_source: human|agent|automation, evidence_ref: string|null}` |
| `review_result` | `{reviewer_class: plan|qa|software-dev|knowledge-work|security|owner, round: positive-integer, verdict: approve|return_to_builder|phase_done|revise|skipped, verdict_source: human|agent|automation, finding_count: non-negative-integer, evidence_ref: string|null}` |
| `defect_recorded` | `{defect_id: string, introduced_task: UUIDv4|null, approving_reviewers: sorted-unique-string-array, gate_that_should_have_caught_it: string, evidence_ref: string}` |
| `rework_recorded` | `{cause_event_id: UUIDv4, round: positive-integer, reason: string, evidence_ref: string|null}` |
| `lesson_candidate_recorded` | `{kit_facing: bool, root_cause_ref: string, candidate_ref: string}` |
| `fact_check_recorded` | `{gate_id: string, verdict: supported|unsupported|mixed|unverified, verdict_source: human|agent|automation, evidence_ref: string}` |
| `scorecard_imported` | `{source_path: "benchmarks/scorecard.jsonl", source_record_hash: lowercase-sha256, source_record_ref: string}` |
| `benchmark_exported` | `{export_batch_id: UUIDv4, target_path: "benchmarks/telemetry-v3.jsonl"|"benchmarks/defects.jsonl", prior_hash: lowercase-sha256|null, exported_event_ids: sorted-unique-UUIDv4-array}` |

`task_started.resumed_from_handoff` is true exactly when the task begins from
a handoff. In that case `handoff_ref` is non-null and a `task_resumed` event is
required for full coverage. Otherwise `handoff_ref` is null.

`gate_result.first_pass` reports whether this gate passed on its first
attempt for the task; it is not reconstructed from a later final result.
Human-run gates use `verdict_source=human`; deterministic commands use
`automation`; an AI reviewer or agent uses `agent`.

## T3.7 Lineage and corrections

`lineage.parent_task_id` is null for a root task and the parent task UUID for
a delegated child. `lineage.delegation_id` is null outside delegation and is a
UUIDv4 shared by the parent's `delegation_started` event and every child event.
A child always has its own `task_id`; it never reuses the parent's identity.

`lineage.correction_of` is null for an original event. A correction is a new,
complete event with a new `event_id` and the same `event_type` as its target;
it carries the corrected envelope and payload rather than a JSON patch. The
target remains byte-for-byte present. A validator resolves the latest valid
correction in append order but preserves the entire chain.

The target must be an earlier event in the same corpus. A forward, self, missing, or cyclic correction is invalid. A correction never changes the identity or
bytes of its target and never authorizes removal of the original.

## T3.8 Append, validation, and recovery

The v2.1 guarantee is a single writer using the released append primitive's
semantics: open with `O_APPEND`, hold the record-boundary lock for validation,
write, and recovery, require an exact positive write count, flush before
success, and re-check replacement-aware path identity while the lock is held.
Multi-writer locking is deferred until delegated agents actually write
concurrently; v3 must not claim it today.

Before append, the writer validates the closed envelope, payload, privacy
allowlist, correction target, and corpus-wide ID uniqueness. Duplicate `event_id` values are invalid. The same ID with different bytes is never a correction;
it is a collision.

Recovery may truncate only an interrupted final record that lacks a complete
UTF-8 JSON object plus terminal LF. Truncation returns exactly to the byte
offset after the last validated line, under the same lock. An invalid interior
record, invalid UTF-8 before the tail, path replacement, symlink/reparse point,
hard link, or ambiguous recovery boundary fails closed without mutation.

Normative diagnostic families are:

- `TELEMETRY_SCHEMA_UNSUPPORTED`;
- `TELEMETRY_EVENT_INVALID`;
- `TELEMETRY_DUPLICATE_EVENT_ID`;
- `TELEMETRY_CORRECTION_INVALID`;
- `TELEMETRY_HISTORY_CORRUPT`;
- `TELEMETRY_PRIVACY_VIOLATION`;
- `TELEMETRY_EXPORT_COLLISION`.

Diagnostics identify the path and event or line when known but must not echo a
forbidden value.

## T3.9 Privacy and source handling

Persisted values are allowlisted metadata only. Raw prompts, full user
messages, tool request or response bodies, environment values, credentials,
secrets, arbitrary file contents, and provider transcripts are forbidden.
They must be omitted, not masked and stored. A producer that cannot prove a
value is allowlisted must omit it or fail with `TELEMETRY_PRIVACY_VIOLATION`.

References may contain stable IDs, canonical repository-relative paths,
lowercase hashes, enum verdicts, counts, and durations. They must not contain
absolute home paths, access tokens, query strings carrying secrets, or copied
source text. `local_private` events stay only in `telemetry/events.jsonl` and
are excluded from every committed export. `project` and `public` events are
exportable only field-for-field under this contract's allowlist.

Disable and error paths obey the same rules. A diagnostic may name a field but
never print its rejected secret-like value.

## T3.10 Import, export, retention, and durable history

### T3.10.1 Legacy import

A v2 scorecard import reads `benchmarks/scorecard.jsonl` without modifying it
and emits new `scorecard_imported`-linked v3 events. The source record's
canonical hash and stable record reference provide provenance. Imported
records use `source_class=legacy_import`; unavailable lifecycle, token, and
revision facts remain explicitly unknown. Import is idempotent by source
record hash plus event type.

No import may normalize, reorder, truncate, or rewrite existing scorecard
bytes. Historical schema-v1 and schema-v2 scorecard records remain valid in
their original file.

### T3.10.2 Export

General export copies eligible validated events to
`benchmarks/telemetry-v3.jsonl`. A `defect_recorded` event also projects the
closed defect payload plus event/task lineage into
`benchmarks/defects.jsonl`. Export is idempotent by `event_id`:

- an existing identical event is a no-op;
- the same ID with different canonical bytes fails with
  `TELEMETRY_EXPORT_COLLISION`;
- a new event appends one record and never rewrites existing benchmark bytes.

The exporter verifies and records the target's prior-byte hash before the
batch and emits `benchmark_exported` only after the target append succeeds.
Partial failure leaves already-valid append-only records intact and reports
the unexported IDs; retry deduplicates the completed IDs.

### T3.10.3 Retention

No automatic TTL exists in v2.1. Local events remain until an explicit prune
operation. Prune is allowed only after verified export proves every selected
exportable event is present in its durable target; `local_private` records
require a separate explicit selection because they have no export receipt.

Committed benchmark records are retained indefinitely under v3 and are never
deleted, normalized, or rewritten by retention. A future retention change to
the durable corpus requires a separately governed contract and cannot act
retroactively without explicit authority.

## T3.11 Disable, downgrade, and compatibility

The host-neutral disable switch is `DAT_KIT_TELEMETRY=off`. In disabled mode,
start, append, and finish perform no new telemetry writes and return a
non-error disabled result; telemetry failure must not block the work loop,
gates, reviews, or scorecard completion. Disable does not delete or rewrite
existing local or committed history.

When a completion-only producer still emits a scorecard outside the disabled
writer, any later import labels the resulting v3 evidence `partial` with
reason `telemetry_disabled`.

dat-kit 2.0 and 1.x tooling must ignore v3 artifacts it does not own or fail
closed with `TELEMETRY_SCHEMA_UNSUPPORTED`; downgrade must never mutate v3
files. v3 readers reject future `schema_version` values without attempting a
partial load. v3 exports do not change the schema or bytes of existing
scorecard history.

The schema freeze begins only at the authorized decision's
`effective_from_run`. Before that boundary this document is a proposal. After
the schema freeze, any new top-level field, payload field, enum value, event
type, or changed interpretation that a strict v3 reader would reject requires
a new schema version and Class C approval. Producer-only changes that preserve
all v3 bytes and meaning follow their separately governed class.

## T3.12 Required producers and status truthfulness

Schema without producers is not Phase 6 completion. The five required PLAN-v7
producer responsibilities are:

| PLAN item | Producer responsibility | Required evidence before `active` |
|---|---|---|
| build-loop HARVEST | emit `lesson_candidate_recorded` with `kit_facing=true` only when root cause is in a dat-kit skill, template, or gate | a real HARVEST task plus validated event |
| diagnosing-bugs | emit `defect_recorded` and export its projection to `benchmarks/defects.jsonl` | a real post-mortem with the required defect tuple |
| knowledge-work fact-check | emit a machine-readable `fact_check_recorded` footer while preserving the human verdict | a real knowledge-work task with human-vs-agent-vs-automation source distinguished |
| task/handoff schema | emit `task_started.resumed_from_handoff` and `task_resumed`, preserving parent/delegation linkage | a real resumed or delegated task |
| reports | derive the per-reviewer view and event-coverage-rate view from valid events | report fixtures plus representative software-dev and knowledge-work observations |

Every producer begins `planned`. It becomes `active` only when its runtime,
artifact/schema revision, validation, and a real producer receipt exist.
Contract prose, a schema fixture, or a synthetic event alone cannot activate a
producer.

The per-reviewer view groups `review_result` rounds and linked
`defect_recorded.approving_reviewers` by reviewer class and identity. It reports
association, not causal blame, and includes unknown/unlinked defects rather
than dropping them.

For each host and observation window, the event-coverage-rate view is:

```text
tasks whose latest valid coverage status is full
------------------------------------------------
all completed tasks observed by finish or scorecard in the window
```

Completion-only and other partial tasks remain in the denominator. A window
with zero completed tasks reports null with the reason `no_observed_tasks`,
never a fabricated zero or 100 percent.

## T3.13 Conformance and release boundary

Phase 6B may begin only after the authorized Class C decision for this exact
contract hash. Implementations then owe schema/storage, lifecycle CLI,
task-ID propagation, five named producers, privacy/retention/disable behavior,
import/export, reports, recovery, and compatibility tests without weakening
this contract.

dat-kit 2.1 release closure additionally requires one real software-dev task
and one real knowledge-work task with human, agent, and automation verdict
sources distinguished; downgrade/disable verification; durable export; schema
freeze; full regression; rollback evidence; an approved RC; and a tag on the
exact approved artifact. None of those later receipts is claimed by this
contract-only proposal.
