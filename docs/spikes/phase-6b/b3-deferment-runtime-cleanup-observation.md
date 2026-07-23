# Phase 6B B3 HARVEST deferment — runtime cleanup observation

## Pre-registration

- Observation task ID: `a0c67829-f505-4d40-9995-464db4a4f9f0`.
- Registered on 2026-07-23 before the first Slice B product or test edit.
- Baseline commit: `6f5393b` (`proposal-0acfe665bc066c31dd5e`
  approved by the platform owner).
- Effective contract run:
  `run-2026-07-23-phase6b-b3-deferment-83f065e`.
- Owner/class: `maintainers`, Class B.
- Components: `maintainer-scripts` and `telemetry-v3-runtime`; split the
  proposal if Catalog resolution cannot govern both without ambiguity.
- Budget: at most 120 added product/test lines and a net-negative product/test
  diff against `b091a3e`.
- Scope: remove caller-selected scorecard/HARVEST authority while retaining
  ordinary scorecard behavior and closed producer-registry validation.
- Non-goals: Host Adapter, capability, resolver, receipt store, schema,
  append/lock/strict-tail/corpus-check internal, producer activation, or B3
  subset #2.

## Ground-truth boundary

1. Build-loop HARVEST remains required but `planned/deferred`; it cannot
   satisfy Phase 6 completion.
2. The generic scorecard CLI is not trusted LOAD/HARVEST context and must not
   accept task UUIDs, evidence references, root-cause locus, or capability as
   producer authority.
3. Live emission requires a separately approved Host Adapter trust contract
   and a producer-owned receipt resolver; neither exists in this slice.
4. All five producer registry entries remain `planned` with null event IDs.
5. The cleanup is subtractive: it adds no replacement authority architecture.

## Threat model

| Boundary | Threat | Required control |
|---|---|---|
| Scorecard CLI | Caller-selected UUID/reference becomes HARVEST authority | Remove every telemetry authority option and keep ordinary scorecard append only |
| Producer module | A callable helper can still mint live HARVEST events | Remove event construction and live-emission exports |
| Registry | Cleanup weakens status truthfulness | Retain closed IDs and shape/status validation; all entries remain planned/null |
| Storage | Cleanup reaches append or corruption controls | Do not change telemetry append, lock, strict-tail, or corpus-check internals |
| Scope | Deferment silently grows replacement architecture | Add no Host Adapter, resolver, capability, schema, storage, or environment surface |
| Compatibility | Scorecard or B0–B2 behavior regresses | Preserve ordinary append/report behavior and run the full cross-component suite |

## Planned product/test scope

- Modify `scripts/scorecard.py`, `telemetry/producers.py`,
  `scripts/tests/test_telemetry_producers.py`,
  `scripts/tests/test_scorecard_append.py`, and
  `scripts/tests/test_telemetry_contract.py`.
- Keep `telemetry/producers.json` byte-identical.
- Append factual closure evidence to
  `docs/spikes/phase-6b/b3-observation.md` only after that evidence exists.

## Red-before-green and acceptance

1. Removed scorecard telemetry flags are rejected.
2. Ordinary `--append-record` succeeds without creating a telemetry event
   file.
3. `telemetry.producers` exports no live-emission helper or caller-selected
   authority path.
4. The registry validator retains exactly five planned/null producers and
   rejects invalid active state.
5. Contract tests pin the effective T3.12 deferment and both future
   prerequisites.
6. B0–B2 lifecycle, CLI, runtime, disable, privacy, and downgrade tests remain
   green.
7. No rejected value, secret, prompt, environment value, or provider
   transcript is introduced.

## Gate and review ledger

| Stage | Required evidence | Status |
|---|---|---|
| Pre-registration | this observation committed before product/test edits | PASS |
| Red-before-green | authority-removal guards fail on the pre-cleanup baseline | PASS |
| Canonical QA | five project gates plus edge-case attack | PASS |
| Code review | diff-scoped independent `APPROVE` | PASS |
| Security review | authority-surface independent `APPROVE` | PASS |
| Final regression QA | unconditional post-review canonical gates | PASS |
| Closure | observation and scorecard append, then consuming-validator rerun | PASS |

No row claims future evidence. Candidate IDs, gate counts, reviewer invocations,
and closure receipts are appended only after each fact exists.

## Candidate and gate receipts

- Pre-registration commit: `2058bc5`.
- Initial product candidate: `3f0cab9`, tree
  `0faaabd69ae1341a984fb2470ca0ffb40a6fb463`.
- Code-review fix candidate: `9ed5821`, tree
  `d1db29bd0a969aa1dac1300c683959a3c696d359`.
- Final candidate: `671c9fe`, tree
  `a71e2453adf2091e4557a338b8aa32b1e343c9b4`.
- Final product/test diff against `b091a3e`: 117 additions and 547 deletions,
  net negative by 430 lines; the 120-added-line cap is satisfied.
- Initial authority-removal red proof: `7 failed, 30 passed, 2 skipped`.
  Targeted green after cleanup: `37 passed, 2 skipped`.
- Rejected-value redaction red proof: `8 failed, 18 passed, 2 skipped`.
  Targeted green after the fix: `26 passed, 2 skipped`.
- No `review-evidence` run existed for the local final SHA, so the declared
  local fallback ran: validator PASS; pytest `373 passed, 8 skipped`; Bash
  syntax PASS; ShellCheck PASS; diff-check PASS.
- Unconditional final regression QA on unchanged `671c9fe`: the same five
  gates PASS; targeted B3 suite `41 passed, 2 skipped`.
- `telemetry/producers.json` remained byte-identical and all five entries
  remained `planned` with null event IDs.
- Scorecard closure receipt: `benchmarks/scorecard.jsonl` line 34; the
  consuming validator passed immediately after the append.

## Invocation ledger

```text
task | ordinal | role | from candidate/tree | to candidate/tree | scope | finding/restart | verdict
a0c67829-f505-4d40-9995-464db4a4f9f0 | 1 | qa (pinned) | 3f0cab9/0faaabd | 3f0cab9/0faaabd | full | pytest unavailable on isolated PATH | RETURN TO BUILDER
a0c67829-f505-4d40-9995-464db4a4f9f0 | 2 | qa (executor-capable substitute) | 3f0cab9/0faaabd | 3f0cab9/0faaabd | full | restart of 1 with canonical PATH restored | PHASE DONE
a0c67829-f505-4d40-9995-464db4a4f9f0 | 3 | code | 3f0cab9/0faaabd | 3f0cab9/0faaabd | full | C1 duplicated CLI test setup | RETURN TO BUILDER
a0c67829-f505-4d40-9995-464db4a4f9f0 | 4 | code | 3f0cab9/0faaabd | 9ed5821/d1db29b | findings-scoped | C1 | APPROVE
a0c67829-f505-4d40-9995-464db4a4f9f0 | 5 | security | 9ed5821/d1db29b | 9ed5821/d1db29b | full | S1 rejected authority value echo | RETURN TO BUILDER
a0c67829-f505-4d40-9995-464db4a4f9f0 | 6 | qa | 9ed5821/d1db29b | 671c9fe/a71e245 | findings-scoped | S1 regression | PHASE DONE
a0c67829-f505-4d40-9995-464db4a4f9f0 | 7 | security | 9ed5821/d1db29b | 671c9fe/a71e245 | findings-scoped | S1 | APPROVE
a0c67829-f505-4d40-9995-464db4a4f9f0 | 8 | qa | 671c9fe/a71e245 | 671c9fe/a71e245 | full final regression | none | PHASE DONE
```

Runtime token and elapsed counts were not exposed and remain unknown. The first
QA refusal is retained as evidence rather than erased; its substitute reran
the complete charter with an executor-capable environment.
