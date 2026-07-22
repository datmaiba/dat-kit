# Phase 6B B2 observation and review ledger

## Pre-registration

- Observation task ID: `8227f7f9-5b3c-42ec-b351-4bc6c1fb5954`.
- Registered before the first B2 product or test edit on 2026-07-22.
- Immutable scope: B2 only — lifecycle-state validation and the host-neutral
  `start | append | finish | validate` CLI, UUIDv4 task creation, delegation
  and handoff/resume linkage, completion-only behavior, and disable/downgrade
  semantics.
- Intended product/test paths: `scripts/telemetry.py` and
  `scripts/tests/test_telemetry_cli.py`.
- Task-local evidence path: `docs/spikes/phase-6b/b2-observation.md`.
- Closure-only append: `benchmarks/scorecard.jsonl`, after all verdicts.
- Explicit non-goals: schema changes; B3 producer wiring; engine, Domain Pack,
  skill, hook, Host Adapter, export, retention, or reporting changes; any work
  from Phase 6A, B0, or B1.
- One task ID covers the whole B2 slice; internal commits do not create new
  observation units.
- Reviewer roles: plan-reviewer already returned `REVISE` and its four
  blockers are incorporated in the approved plan; candidate chain is full QA,
  full code review, full security review, findings-scoped re-review when
  needed, then final regression QA.
- Budget: 50–80k total-token slice, mandatory checkpoint at 70% remaining
  context; stop for `REPLAN` at the handoff's scope, architecture, or size
  thresholds.

## Ground-truth answers and auto-decisions

1. Normal task identity is minted at LOAD and remains one UUIDv4 through start,
   append, handoff/resume, delegation, gates, reviews, HARVEST, and finish.
   Completion-only finish-time minting is the sole exception. Source:
   `docs/contracts/telemetry-v3.md` T3.6.
2. Normal lifecycle cardinality is one original start followed by one original
   finish, with no later original event. Completion-only has one original
   finish and no start. Source: T3.6 and the approved B2 handoff.
3. Coverage arrays are exact, sorted, and unique at every append position;
   terminal reason selection follows the fixed T3.5 precedence. Source:
   `docs/contracts/telemetry-v3.md` T3.5.
4. `append` accepts only the schema-defined closed lifecycle event set and
   validates its exact payload. Producer identity, source/verdict authority,
   and metadata namespaces remain fixed trusted policy, never caller-owned.
   Source: T3.6 and the existing B1 `TelemetryStore`/`ProducerWriter` contract.
5. Disabled writes succeed without mutation; operational writer/storage
   failures are nonblocking degraded results; malformed input, invalid state,
   corrupt history, and future schema remain strict nonzero/no-mutation errors.
   Source: T3.11 and the approved B2 result matrix.
6. Auto-decision: CLI JSON is accepted only through a bounded UTF-8 object
   input, never echoed in diagnostics, and success output contains generated
   identifiers/status only. This is the safest reversible implementation of
   the approved bounded-input and no-secret-echo requirement.

No open question remains; no decision-log file exists in this repository.

## Threat model

| Boundary | Threat | Required control |
|---|---|---|
| CLI input | Oversized, duplicate-key, malformed, or non-object JSON | Bound bytes before parsing, reject duplicate keys, validate exact shape, never echo rejected values |
| Producer authority | Caller forges producer/source/verdict/revision namespace | CLI constructs a fixed producer policy and injects producer identity; input cannot supply authority metadata |
| Lifecycle history | Duplicate start/finish, post-finish append, mismatched resume, delegation reuse/cycle | Validate the complete trusted corpus and proposed transition before append |
| Storage | Corrupt/future history, interrupted tail, link/path substitution, partial write | Reuse B1 validation/recovery/path controls; strict errors do not rewrite trusted history |
| Downgrade | Telemetry failure blocks the work loop or disable mutates history | Disabled and operational failure return structured non-errors without deletion/rewrite |
| Privacy | Secret or untrusted value appears in stdout/stderr | Emit closed result/diagnostic fields and stable codes only; never include raw input values |

## Lifecycle state matrix

| Existing task state | Command/event | Result |
|---|---|---|
| absent | `start` | Mint UUIDv4 and append the sole original `task_started` |
| absent | `finish --completion-only` | Mint UUIDv4 and append the sole original `task_finished` with partial `completion_only` coverage |
| absent | `append` or normal `finish` | Strict invalid-transition error; no mutation |
| started, unfinished | closed `append` event | Append only if payload, identity, lineage, handoff, and delegation rules hold |
| started, unfinished | second `start` | Strict duplicate-start error; no mutation |
| started, unfinished | normal `finish` | Append the sole finish with exact terminal coverage |
| finished | any original event or finish | Strict post-finish/duplicate-finish error; no mutation |
| unmatched non-delegation handoff | matching `task_resumed` | Same task, same ref/event ID, one-use consumption |
| no matching handoff | `task_resumed` | Strict error; no mutation |
| any history | `delegation_started` | Unique delegation ID, fixed parent-child pair, distinct task IDs, no lineage cycle |

## Error and mutation matrix

| Condition | Exit | Structured status | Mutation |
|---|---:|---|---|
| Success | 0 | `ok` | Exactly one valid append, except `validate` |
| `DAT_KIT_TELEMETRY=off` | 0 | `disabled` | None |
| Operational producer/storage failure | 0 | `degraded` | No trusted-history rewrite or corruption |
| Malformed/bounded-input failure | nonzero | `error` | None |
| Invalid lifecycle transition | nonzero | `error` | None |
| Corrupt history or future schema | nonzero | `error` | None |
| `validate` failure | nonzero | `error` | Read-only |

## Acceptance criteria

- `start`, `append`, `finish`, and `validate` have deterministic parsing,
  structured JSON output, documented exit behavior, bounded JSON input, and no
  rejected-value/secret echo.
- Start mints UUIDv4; task identity and immutable lineage are enforced across
  the corpus; normal and completion-only cardinalities are distinct.
- Generic append covers every schema-defined event type needed by later
  producers, including `gate_result` and `review_result`, without accepting
  arbitrary shapes or caller-authored authority.
- Handoff/resume matching and delegation uniqueness/fixed-pair/no-cycle rules
  reject invalid transitions without mutation.
- Coverage arrays and terminal reason precedence are exact.
- Disabled and degraded paths are nonblocking; strict input/state/history/
  schema failures remain nonzero and non-mutating; validate remains read-only.
- Existing B1 append, recovery, correction-authority, privacy, producer-policy,
  record-boundary, and path-hardening tests remain green.
- Targeted tests show red-before-green; the canonical full gates and sequential
  reviewer chain pass on a frozen committed candidate.

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
Reviewer-private reads are never estimated. Reports target at most 2.5 KB per
packet and a clean-chain dispatch proxy below 10–12 KB.

## Pre-freeze receipts

- Red-before-green: the first executable B2 run reported `13 failed`; every
  case stopped at the absent `telemetry.main` entry point before runtime
  implementation existed.
- Targeted green after implementation and the batched adversarial self-check:
  `55 passed, 1 skipped` across `test_telemetry_cli.py`,
  `test_telemetry_runtime.py`, and `test_telemetry_contract.py`.
- The self-check found and fixed two issues before independent dispatch:
  completion-only history could accept a non-canonical degradation reason,
  and storage-open failures were not yet distinguished from corrupt history.
- Product candidate/tree, full-gate receipts, reviewer invocations, closure
  tree, and scorecard receipt are appended only after each fact exists; this
  pre-registration does not claim future evidence.

## Candidate receipts (appended at freeze, 2026-07-22/23)

- Initial B2 candidate: `119800aab463a897235d45195b7755e29e6aaf16`, tree
  `0886b0ee398cd78738fb56338897d116053e30ce`.
- Code-review fix candidate: `258236a19093814f88469456d8426f8cc42a42b2`, tree
  `42b41988233fbcca398d36daae9f549672b94afe`. QA `PHASE DONE`, code `APPROVE`
  (C1–C3 closed), security `RETURN TO BUILDER` (S1 HIGH, S2/S3 MEDIUM).
- Security-fix product candidate (final): `bd4e844`, tree
  `926ac586f873f67532360a3ff7fbe656d0900684`. Red-before-green receipt for the
  S1–S3 cases: `7 failed, 16 passed` before the fix; targeted green after:
  `66 passed` across the three telemetry test files. Full gates on `bd4e844`:
  `validate.py` PASS; `pytest scripts/tests` `351 passed, 3 skipped`;
  `bash -n` PASS; `shellcheck` PASS; `git diff --check` PASS.
- The closure commit is the commit introducing this section plus the scorecard
  append; it is identified by Git history, never by a self-referential hash.

## Invocation ledger (closure)

Rows 1–7 are transcribed verbatim from the 2026-07-22 replan handoff record;
rows 8–10 are new. Runtime tokens/elapsed were not exposed and remain
`unknown`; dispatch bytes are exact UTF-8 byte counts of supplied packets and
exclude reviewer-private reads/reasoning.

```text
task | ordinal | role | from candidate/tree | to candidate/closure tree | full/findings-scoped | restart_of_ordinal | restart cause | trigger/finding IDs | verdict | elapsed if known | runtime input/output tokens or unknown | dispatch bytes | invalidation reason or none | avoidable_under_narrow_rule yes/no + reason
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 1 | qa | 119800a/0886b0e | 119800a/0886b0e | full | none | none | B2-QA | RETURN TO BUILDER | unknown | unknown | 1582 | none | no — initial QA is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 2 | qa | 119800a/0886b0e | 119800a/0886b0e | full | 1 | pytest PATH correction | B2-QA | interrupted/no verdict | unknown | unknown | 653 | invocation exceeded the 120-second ceiling and was stopped | no — mandatory QA restart
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 3 | qa | 119800a/0886b0e | 119800a/0886b0e | full | 2 | bounded timeout restart | B2-QA | RETURN TO BUILDER | unknown | unknown | 840 | shellcheck executable access denied | no — mandatory QA restart
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 4 | qa | 119800a/0886b0e | 119800a/0886b0e | findings-scoped | 3 | resolved shellcheck path | B2-QA-ENV | PHASE DONE | unknown | unknown | 529 | none | no — required gate closure
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 5 | code | 119800a/0886b0e | 119800a/0886b0e | full | none | none | C1,C2,C3 | RETURN TO BUILDER | unknown | unknown | 1581 | none | no — initial code review is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 6 | code | 258236a/42b4198 | 258236a/42b4198 | findings-scoped | 5 | C1–C3 fix commit | C1,C2,C3 | APPROVE | unknown | unknown | 971 | none | no — findings re-review is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 7 | security | 258236a/42b4198 | 258236a/42b4198 | full | none | public-input/path/write triggers | S1,S2,S3 | RETURN TO BUILDER | unknown | unknown | 1754 | none | no — initial security review is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 8 | security | 258236a/42b4198 | bd4e844/926ac58 | findings-scoped | 7 | S1–S3 fix commit | S1,S2,S3 | APPROVE | unknown | unknown | 3401 | none | no — findings re-review is never avoidable
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 9 | qa | bd4e844/926ac58 | bd4e844/926ac58 | full | none | none | B2-QA-FINAL | interrupted/no verdict | unknown | unknown | 1660 | pinned qa-agent context exposed no executor; gates unexecuted, honest refusal to certify | no — mandatory final regression dispatch
8227f7f9-5b3c-42ec-b351-4bc6c1fb5954 | 10 | qa | bd4e844/926ac58 | bd4e844/926ac58 | full | 9 | charter-substituted executor-capable QA per the build-loop substitution rule | B2-QA-FINAL | PHASE DONE | unknown | unknown | 1901 | none | no — required gate closure
```

Total reviewer invocations: 10. Full: 7. Findings-scoped: 3. Exact dispatch
proxy: 14,872 bytes (packets 8–10 ran under a verbose-brief runtime; the
pre-registered ≤2.5 KB packet target was exceeded by row 8 at 3,401 bytes).
Avoidable under the pre-registered narrow closure-only rule: 0. The security
closure chain on `bd4e844` is: findings-scoped security `APPROVE` (row 8) →
final regression QA `PHASE DONE` (row 10). B2 is review-closed; this completed
ledger enters the Review-Economy-v3 Stage A decision denominator as
observation task #1.
