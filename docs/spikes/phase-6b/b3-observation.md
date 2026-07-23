# Phase 6B B3 observation and review ledger

## Pre-registration

- Observation task ID: `01457374-634f-457e-a912-4b44c3c8cc37`.
- Registered before the first B3 product or test edit on 2026-07-23.
- Immutable scope: B3 across its five independently approved subsets; this
  candidate is subset #1 only — build-loop HARVEST scorecard integration,
  `lesson_candidate_recorded`, lifecycle emission, and producer status
  truthfulness.
- Intended product/test paths for subset #1:
  `telemetry/producers.py`, `telemetry/producers.json`,
  `scripts/scorecard.py`, `scripts/tests/test_telemetry_producers.py`, and,
  only if required for the new registry invariant, `scripts/validate.py` or
  its directly owned validator.
- Task-local evidence path: `docs/spikes/phase-6b/b3-observation.md`.
- Closure-only append: `benchmarks/scorecard.jsonl`, after all verdicts.
- Explicit subset #1 non-goals: diagnosing-bugs producer, knowledge-work
  footer, task/handoff integration, report views, legacy scorecard import,
  durable export, producer activation, and changes to `_WRITE_LOCK`,
  `_append_local_event`, `ProducerWriter._append`, locked/strict-tail, or
  corpus-check internals in `scripts/telemetry.py`.
- One observation ID covers all B3 subsets; each subset is an internal,
  independently reviewed candidate and requires separate approval.
- Reviewer chain: full QA, full code review, full security review because
  producer authority surfaces change, findings-scoped re-review when needed,
  then final regression QA when a review fix invalidates prior QA.
- Budget: approximately 500 combined added product and test lines for subset
  #1; stop for `REPLAN` on approach to the budget or any required architecture,
  schema, append-internals, or other-subset change.

## Ground-truth answers and auto-decisions

1. The scorecard append completes before telemetry starts. Telemetry disabled
   or operationally degraded results never fail or roll back the scorecard
   append. Source: `docs/contracts/telemetry-v3.md` T3.11 and the approved B3
   handoff.
2. A live HARVEST lifecycle is one task ID across `task_started`,
   `lesson_candidate_recorded`, and `task_finished`. Its terminal coverage is
   `partial`, because build-loop also requires `gate_result` and
   `review_result`. Source: T3.5.1, T3.6, and D-B3-2.
3. `kit_facing=true` is closed to dat-kit skill, template, and gate root-cause
   loci. Agent/reviewer charter, CI, git, and host behavior loci are false.
   Source: T3.12 and the approved B3 handoff.
4. `root_cause_ref` and `candidate_ref` are producer-owned `evidence:*`
   stable references, never prose, paths to dereference, or copied source.
   Source: T3.3.1 and T3.9.
5. All five producer registry entries remain `planned`. No fixture, synthetic
   event, prose record, or this subset's tests can activate a producer.
   Source: T3.12 and D-B3-1/D-B3-5.
6. The producer uses only the existing public B1/B2 telemetry surfaces. If
   correct lifecycle emission requires changes to append or strict-tail
   internals, the subset stops for replan. Source: the B3 hard scope fence.
7. Auto-decision: registry validation is implemented at the narrowest existing
   validation owner that can check the committed artifact, without introducing
   a second producer registry or schema. This is reversible, Class B, and does
   not alter the v3 event contract.

No open question remains; the approved handoff is the decision record for this
subset.

## Threat model

| Boundary | Threat | Required control |
|---|---|---|
| Scorecard-to-telemetry seam | Telemetry failure blocks or rolls back a valid scorecard append | Invoke only after successful append; catch operational telemetry failures and return a structured degraded result |
| Disable switch | `DAT_KIT_TELEMETRY=off` still creates an event file | Return structured disabled status before telemetry storage mutation |
| Producer authority | Caller supplies producer identity, source class, verdict authority, or arbitrary metadata | Bind a fixed registered producer policy and use only the public writer surface |
| Root-cause classification | Vague labels make non-kit failures appear kit-facing | Accept a closed locus enum; map true only for skill, template, and gate |
| Stable references | Prose, secrets, or dereferenceable content is stored in reference fields | Require producer-owned `evidence:*` stable references and never echo rejected values |
| Lifecycle | Duplicate IDs, wrong ordering, or false full coverage enters the stream | Mint UUIDv4 once, emit start → candidate → finish, then run the consuming lifecycle validator |
| Status registry | Planned work is reported active without real evidence | Validate the closed five-entry registry and require a receipt event ID for every active entry |
| Local storage | Path, link, corrupt-history, or append failure damages the work loop | Reuse existing public telemetry storage controls; degrade without rewriting trusted history |

## Acceptance criteria

- A successful scorecard append invokes the HARVEST producer and then reruns
  the consuming telemetry lifecycle validator.
- The emitted lifecycle is start → `lesson_candidate_recorded` → finish on one
  UUIDv4 task ID, with exact in-progress coverage and terminal `partial`
  coverage naming the missing build-loop gate and review evidence.
- Skill, template, and gate loci set `kit_facing=true`; agent-charter, CI, git,
  and host loci set it false.
- Non-`evidence:*` or prose-like root-cause/candidate references fail before
  mutation and rejected values are not echoed.
- Disabled telemetry creates no event file and does not prevent the scorecard
  append.
- An unavailable telemetry target leaves the scorecard append successful and
  yields a structured degraded result.
- `telemetry/producers.json` contains exactly five planned producers; its
  validator rejects unknown shapes/statuses and `active` without a receipt
  event ID.
- Targeted tests show red-before-green. If the repository validator learns the
  registry invariant, an isolated broken registry proves red before final
  green.
- The canonical five gates and sequential independent reviewer chain pass on
  a frozen committed candidate.

## Candidate and invocation ledger

Candidate/base/tree IDs and changed paths are recorded at freeze. Append one
row per reviewer invocation using this schema:

```text
task | ordinal | role | from candidate/tree | to candidate/closure tree |
full/findings-scoped | restart_of_ordinal | restart cause |
trigger/finding IDs | verdict | elapsed if known |
runtime input/output tokens or unknown | dispatch bytes |
invalidation reason or none | avoidable_under_narrow_rule yes/no + reason
```

`dispatch bytes` is only intentionally supplied packet size, not token usage.
Reviewer-private reads are never estimated. Packets target at most 2.5 KB for
one finding set, scaling by roughly 800 bytes per finding.

## Pre-freeze receipts

- Pre-registration exists before the first subset #1 product or test edit.
- Red-before-green, targeted green, adversarial self-check, candidate/tree,
  full-gate, reviewer, and closure receipts are appended only after each fact
  exists; this pre-registration does not claim future evidence.

## Option-A deferment supersession and subset #1 closure

The live-emission acceptance criteria above describe the superseded candidate
that triggered the authority replan. They are retained as historical evidence,
not as the approved implementation state.

Platform-owner decision `decision-0acfe665bc066c31dd5e-0001` made
`proposal-0acfe665bc066c31dd5e` effective from
`run-2026-07-23-phase6b-b3-deferment-83f065e`. Under that contract:

- build-loop HARVEST remains required but `planned/deferred`;
- the generic scorecard CLI is not trusted producer authority;
- live emission remains blocked pending separately approved Host Adapter trust
  and producer-owned receipt resolution;
- no capability, resolver, receipt store, schema, append internal, or producer
  activation was added;
- all five producer registry entries remain `planned` with null event IDs.

Slice B removed the superseded live helper and caller-selected task/reference/
locus options. Final candidate `671c9fe` is 117 additions and 547 deletions
against `b091a3e`, net negative by 430 lines. Independent QA returned
`PHASE DONE`, code review returned `APPROVE`, security review returned
`APPROVE`, and unconditional final QA returned `PHASE DONE` with pytest
`373 passed, 8 skipped` plus targeted B3 `41 passed, 2 skipped`. Detailed
candidate, red-green, gate, and invocation receipts are in
`b3-deferment-runtime-cleanup-observation.md`.

B3 subset #1 closes as deferred, not active.

## B3 subset #2 — diagnosing-bugs defect projection

Pre-registration (immutable scope): implement the defect-specific
`defect_recorded -> benchmarks/defects.jsonl` projection required by
telemetry-v3 T3.10.2, and only that. Intended paths: `scripts/telemetry.py`
(projection writer, `export` subcommand, consuming validator), `scripts/tests/
test_telemetry_defect_projection.py`, `scripts/tests/test_telemetry_cli.py`
(if extended), `scripts/validate.py` (wire the consuming validator),
`benchmarks/defects.jsonl` (new committed durable artifact), `.gitattributes`
(the byte-compared projection needs its own `eol=lf` pin per the 2026-07-20
lesson — added on the QA finding),
`docs/spikes/phase-6b/b3-observation.md` (this ledger). Applicable reviewer
roles: plan, qa, software-dev (code), security. Scope decisions D-S2-1
(defect-specific projection only; general export stays B4) and D-S2-2 (runtime
only; producer stays `planned`, no synthetic/retroactive receipt, activation
block untouched) were approved by the user on 2026-07-23.

Decisions in effect:

- the durable projection is the closed 13-field T3.10.2 record; the projection
  has no other fields;
- export is append-only and idempotent by `event_id` (identical is a no-op,
  same id with different canonical bytes fails `TELEMETRY_EXPORT_COLLISION`);
- the `benchmark_exported` receipt is emitted into the local stream only after
  the durable append succeeds; a no-op export emits no receipt;
- the receipt's `producer.id` is the channel-injected `dat-kit-cli`; the
  `diagnosing-bugs` producer registry entry stays `planned` with a null event
  ID and no activation authority is added.

Verified gates on the working tree (pre-review): `python scripts/validate.py`
green; `pytest scripts/tests` `393 passed, 3 skipped`; `bash -n scripts/init.sh`
pass; `shellcheck scripts/init.sh` pass (0.8.0); `git diff --check` pass; ruff
clean on the touched sources; mypy is report-only and not run locally (pinned
version unavailable in this environment). Red-before-green proven: dropping
`evidence_ref` from the projection writer turned the 13-field shape test red,
and reverting restored green. Independent QA, code, and security reviews are
recorded after this pre-registration.

Reviewer receipts: plan-reviewer RETURN (13-field blocker + receipt-envelope)
then resolved; code-reviewer APPROVE; security-reviewer APPROVE (one Windows
path-separator LOW fixed by deriving the contract `target_path` from a canonical
POSIX literal). QA edge-case attack passed statically on all nine surfaces; the
five gates were executed by the builder (validate PASS, pytest 394 passed/3
skipped, bash -n PASS, shellcheck 0.8.0 PASS, diff-check PASS, ruff PASS) and
the demo was walked end-to-end. The `diagnosing-bugs` producer remains
`planned` with a null event ID; no activation authority was added.

B3 subset #2 runtime is built, reviewed, and self-verified. Producer activation
remains deferred to a future candidate with a real post-mortem defect.
