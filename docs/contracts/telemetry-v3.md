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
| `producer` | closed object `{id, revision}`; both are stable IDs from T3.3.1 |
| `revisions` | closed object with all revision references in T3.4 |
| `lineage` | closed object `{parent_task_id, delegation_id, correction_of}`; every key is present and nullable |
| `source_class` | `runtime`, `repository`, `human`, `legacy_import`, or `derived` |
| `privacy_class` | `public`, `project`, or `local_private` |
| `coverage` | closed coverage object from T3.5 |
| `tokens` | closed token-attribution object from T3.5 |
| `elapsed` | closed elapsed-attribution object from T3.5 |
| `payload` | the closed object selected by `event_type` in T3.6 |

UUID values use the textual `8-4-4-4-12` form. Nil UUIDs and non-v4 UUIDs are
invalid. Nullable fields use JSON `null`; an empty string is never a null
substitute. Arrays described as sets are sorted, contain no duplicates, and
use the identity rules of their element type.

### T3.3.1 String grammars

No telemetry field accepts free-form text. Every non-enum string is one of:

- **stable ID**: 1-128 ASCII characters matching
  `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`;
- **stable reference**: 1-512 ASCII characters matching
  `[A-Za-z0-9][A-Za-z0-9._:/#@-]{0,511}`; or
- **path**: a 1-512 character canonical repository-relative POSIX path with
  no empty, `.`, or `..` segment, no control character, no backslash, no
  Windows-reserved basename, and no trailing space or dot.

Hashes, UUIDs, timestamps, and literal paths use their narrower declared
grammar. Arbitrary descriptions, error messages, prompt excerpts, copied
source, and user-entered notes have no field in v3. Producers map a condition
to a closed enum and store only a stable evidence reference.

### T3.3.2 Source and privacy classes

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

- `value` is a stable reference and `unavailable_reason` is
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
  `completion_only | unsupported_host_start | telemetry_disabled | legacy_import | producer_failure | in_progress`.

`full` requires an empty missing list and a null reason. `partial` requires a
non-empty missing list and a non-null reason. Partial coverage is valid data,
not an error to hide. A completion-only scorecard may mint a task ID, but its
events must use `partial` with reason `completion_only` and name the lifecycle
events that were not observed.

At minimum, full coverage requires both `task_started` and `task_finished` in
valid T3.6 order. The validator derives the required set, then requires
`missing_event_types` to equal the required types absent from the stream:

- every task: `task_started`, `task_finished`;
- `workflow=build-loop`: at least one `gate_result` and one `review_result`;
- `workflow=knowledge-work`: at least one `fact_check_recorded` carrying the
  load-bearing fact-check verdict;
- `resumed_from_handoff=true`: `task_resumed`;
- any delegated parent/child pair: the linked `delegation_started` event;
- any emitted handoff: `handoff_created`.

An isolated `task_finished` therefore cannot claim `full`. Unknown workflows
owe the universal start/finish pair; their producer revision may declare a
stricter required-event profile but may never weaken this floor.

`in_progress` is valid only before the original `task_finished`. On each
non-terminal event, `missing_event_types` is the exact required set not yet
observed at that append position, including `task_finished`; the list may
shrink as evidence arrives. The original `task_finished` and any correction of
it carry the terminal `full` or degraded `partial` result and cannot use
`in_progress`. Reports use that latest valid terminal coverage, never an
earlier in-progress snapshot.

When more than one terminal degradation cause applies, the single reason is
selected by this strict precedence:
`telemetry_disabled` > `legacy_import` > `producer_failure` > `unsupported_host_start` > `completion_only`.
The missing-event list still exposes the complete loss; the reason identifies
the highest-precedence cause and is never selected opportunistically to improve
a coverage report.

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

Each payload contains exactly the fields below. `stable-id`, `stable-ref`, and
`path` use T3.3.1. `verdict_source` is always
`human | agent | automation`. In the table, slash-separated values are the
exact closed enum alternatives, not free text.

The load-bearing named fields include `resumed_from_handoff`, `first_pass`,
`verdict_source`, `introduced_task`, `approving_reviewers`,
`gate_that_should_have_caught_it`, and `kit_facing`; their exact owning
payloads and types are fixed below.

| `event_type` | Exact payload fields |
|---|---|
| `task_started` | `{workflow: stable-id}` |
| `task_finished` | `{outcome: completed/aborted/unknown, scorecard_ref: path or null}` |
| `handoff_created` | `{handoff_ref: path, reason: context_ceiling/deliberate_pause/delegation_brief}` |
| `task_resumed` | `{handoff_ref: path, resumed_from_handoff: true, resumed_from_event_id: UUIDv4}` |
| `delegation_started` | `{delegation_id: UUIDv4, child_task_id: UUIDv4, delegated_role: stable-id, brief_ref: path}` |
| `gate_result` | `{gate_id: stable-id, outcome: pass/fail/skipped, first_pass: bool, verdict_source: human/agent/automation, evidence_ref: stable-ref or null}` |
| `review_result` | `{reviewer_id: stable-id, reviewer_class: plan/qa/software-dev/knowledge-work/security/owner, round: positive-integer, verdict: approve/return_to_builder/phase_done/revise/skipped, verdict_source: human/agent/automation, finding_count: non-negative-integer, evidence_ref: stable-ref or null}` |
| `defect_recorded` | `{defect_id: stable-id, introduced_task: UUIDv4 or null, approving_reviewers: sorted-unique-stable-id-array, gate_that_should_have_caught_it: stable-id, evidence_ref: stable-ref}` |
| `rework_recorded` | `{cause_event_id: UUIDv4, round: positive-integer, reason: gate_failure/review_finding/spec_correction/other, evidence_ref: stable-ref or null}` |
| `lesson_candidate_recorded` | `{kit_facing: bool, root_cause_ref: stable-ref, candidate_ref: stable-ref}` |
| `fact_check_recorded` | `{gate_id: stable-id, verdict: sourced/return_to_builder, verdict_source: human/agent/automation, finding_count: non-negative-integer, failure_classes: sorted-unique-fact-check-failure-array, evidence_ref: stable-ref}` |
| `scorecard_imported` | `{source_path: "benchmarks/scorecard.jsonl", source_record_ordinal: positive-integer, source_record_hash: lowercase-sha256, source_record_ref: stable-ref}` |
| `benchmark_exported` | `{export_batch_id: UUIDv4, target_path: "benchmarks/telemetry-v3.jsonl" or "benchmarks/defects.jsonl", prior_hash: lowercase-sha256 or null, exported_event_ids: sorted-unique-UUIDv4-array}` |

`gate_result.first_pass` reports whether this gate passed on its first
attempt for the task; it is not reconstructed from a later final result.
Human-run gates use `verdict_source=human`; deterministic commands use
`automation`; an AI reviewer or agent uses `agent`.

For `fact_check_recorded`, `sourced` is the machine value for the
knowledge-work charter's `SOURCED` verdict: `finding_count` is zero and
`failure_classes` is empty. `return_to_builder` records the charter's numbered
failure outcome: the count is positive and the array is non-empty. Its closed
failure values are `unsupported_claim`, `weaker_than_claim`, `contradiction`,
`unreliable_source`, `stale_source`, `inadequate_coverage`, and
`prose_contradiction`. The `evidence_ref` points to the complete numbered
finding record; telemetry never copies its prose.

Exactly one original `task_started` exists for every normally observed task.
Exactly one original `task_finished` also exists. The original start is the task's first
event and the original finish follows every work, gate, review, handoff,
delegation, and HARVEST event for that task. Duplicate starts, duplicate
finishes, finish-before-start, and an original event appended after finish are
invalid. Correction events do not alter this original-event cardinality.

The completion-only degraded path has exactly one original `task_finished`, no
`task_started`, and the T3.5.1 partial-coverage label.

A resumed execution preserves the same `task_id` and does not emit another `task_started`. It emits `task_resumed` after an earlier unmatched `handoff_created.event_id` for that same task and before finish. Its
`resumed_from_event_id` names that event, its `handoff_ref` is identical, and
`resumed_from_handoff` is the literal true. One task may have multiple ordered
handoff/resume pairs, but a handoff event can be consumed at most once. A
completed task has no unmatched non-delegation handoff; an aborted task may
end with one and remains partial.

## T3.7 Lineage and corrections

`lineage.parent_task_id` is null for a root task and the parent task UUID for
a delegated child. `lineage.delegation_id` is null outside a delegated child
and is copied from the parent's `delegation_started.payload.delegation_id` to
every child event. A child always has its own `task_id`; it never reuses the
parent's identity.

All original events for one task carry one immutable `(parent_task_id, delegation_id)` pair. A delegation ID identifies exactly one parent-child task pair,
appears in exactly one parent `delegation_started` payload whose
`child_task_id` names that child, and cannot be reused for another parent or
child. The parent event keeps the parent's own lineage pair; a root parent may
therefore delegate multiple children through distinct payload delegation IDs
without lineage drift. A parent ID without a delegation ID, a delegation ID
without a parent ID on the child, pair drift within a task, or a parent/child
cycle is invalid.

`lineage.correction_of` is null for an original event. A correction is a new,
complete event with a new `event_id` and the same `event_type` as its target;
it carries the corrected envelope and payload rather than a JSON patch. The
target remains byte-for-byte present. A validator resolves the latest valid
correction in append order but preserves the entire chain.

Immutable target fields are `schema_version`, `task_id`, `event_type`,
`source_class`, `lineage.parent_task_id`, and `lineage.delegation_id`; a
correction must equal its target for all of them. Replacement fields are
`coverage`, `tokens`, `elapsed`, and `payload`; the correction supplies their
complete current values. Correction-evidence fields are `event_id`,
`occurred_at`, `producer`, and `revisions`; they describe the correcting write
and may differ from the target. `lineage.correction_of` names the immediate
target. `privacy_class` may stay equal or tighten only in the order
`public` -> `project` -> `local_private`; it may never loosen. Aggregation uses
the immutable identity from the chain and the latest replacement values, so it
never merges unspecified fields.

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

The T3.3.1 grammar and size bounds apply before persistence, including
`workflow`, producer and reviewer identity, gate/defect IDs, every reason,
and every evidence/root-cause/candidate reference. A producer may not place
free-form text in a stable-ref field merely because the characters happen to
match the grammar; the value must resolve to a stable artifact, identifier, or
closed enum owned by the producer.

Disable and error paths obey the same rules. A diagnostic may name a field but
never print its rejected secret-like value.

## T3.10 Import, export, retention, and durable history

### T3.10.1 Legacy import

A v2 scorecard import reads `benchmarks/scorecard.jsonl` without modifying it
and emits exactly one `scorecard_imported` and one `task_finished` for each
valid source line, in that order, with the same task ID. The importer mints one
UUIDv4 task ID on the first import of the source-record identity. If append is
interrupted after either event, retry finds the existing event by source
identity, reuses that task ID after an interrupted import, and emits only the
missing member of the pair.

The source-record identity is path + ordinal + hash. Each linked event identity
is that source-record identity + event type. The ordinal is the one-based
physical line number. To compute `source_record_hash`, take the exact
UTF-8 bytes of that physical JSON record, normalize only its terminal CRLF or CR to LF, include that LF in the SHA-256 input, and perform no JSON
reserialization or other normalization. The stable source reference is
`benchmarks/scorecard.jsonl#line-<ordinal>`. Two byte-identical source lines at
different ordinals remain distinct historical records.

Both linked events use `source_class=legacy_import`, terminal partial coverage
with reason `legacy_import`, and explicit unknowns for unavailable lifecycle,
token, elapsed, and revision facts. `task_finished.payload.scorecard_ref` is
`benchmarks/scorecard.jsonl`; `scorecard_imported` carries the exact ordinal,
hash, and source reference.

No import may normalize, reorder, truncate, or rewrite existing scorecard
bytes. Historical schema-v1 and schema-v2 scorecard records remain valid in
their original file.

### T3.10.2 Export

General export copies the complete eligible validated event to
`benchmarks/telemetry-v3.jsonl`. A `defect_recorded` event also appends this
closed projection to `benchmarks/defects.jsonl`:

| Defect projection field | Normative value |
|---|---|
| `schema_version` | integer literal `3` |
| `event_id` | source defect event UUIDv4 |
| `task_id` | source event task UUIDv4 |
| `parent_task_id` | source lineage value, UUIDv4 or null |
| `delegation_id` | source lineage value, UUIDv4 or null |
| `correction_of` | source lineage value, UUIDv4 or null |
| `occurred_at` | source event RFC 3339 UTC timestamp |
| `defect_id` | source payload stable ID |
| `introduced_task` | source payload UUIDv4 or null |
| `approving_reviewers` | source payload sorted unique stable reviewer IDs |
| `gate_that_should_have_caught_it` | source payload stable gate ID |
| `evidence_ref` | source payload stable reference |

The projection has no other fields. A corrected defect appends a new projection
record with its new `event_id` and `correction_of`; it never rewrites the prior
projection. Consumers resolve the correction chain by source event identity.

Export is idempotent by `event_id`:

- an existing identical event is a no-op;
- the same ID with different canonical bytes fails with
  `TELEMETRY_EXPORT_COLLISION`;
- a new event appends one record and never rewrites existing benchmark bytes.

The exporter verifies and records the target's prior-byte hash before the
batch and emits `benchmark_exported` only after the target append succeeds.
Partial failure leaves already-valid append-only records intact and reports
the unexported IDs; retry deduplicates the completed IDs.

`benchmark_exported` events are never export-eligible and never appear in
`exported_event_ids`. A no-op export with no new eligible events emits no new
receipt. The stream is caught up when every eligible non-receipt event is
present identically in its target, so an export cannot create an endless tail
of receipts that makes pruning unreachable.

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
| task/handoff schema | emit `task_resumed.resumed_from_handoff=true`, preserve the original task ID across handoff, and preserve parent/delegation linkage | a real resumed or delegated task |
| reports | derive the per-reviewer view and event-coverage-rate view from valid events | report fixtures plus representative software-dev and knowledge-work observations |

Every producer begins `planned`. It becomes `active` only when its runtime,
artifact/schema revision, validation, and a real producer receipt exist.
Contract prose, a schema fixture, or a synthetic event alone cannot activate a
producer.

The per-reviewer view groups `review_result` rounds by the payload's explicit
`reviewer_id` and `reviewer_class`, then joins linked
`defect_recorded.approving_reviewers` on the same stable reviewer IDs. The
producer identity is not a substitute for reviewer identity. The view reports
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
