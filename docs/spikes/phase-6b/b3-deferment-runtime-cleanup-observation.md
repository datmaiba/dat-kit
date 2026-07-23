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
| Pre-registration | this observation committed before product/test edits | pending |
| Red-before-green | authority-removal guards fail on the pre-cleanup baseline | pending |
| Canonical QA | five project gates plus edge-case attack | pending |
| Code review | diff-scoped independent `APPROVE` | pending |
| Security review | authority-surface independent `APPROVE` | pending |
| Final regression QA | unconditional post-review canonical gates | pending |
| Closure | observation and scorecard append, then consuming-validator rerun | pending |

No row claims future evidence. Candidate IDs, gate counts, reviewer invocations,
and closure receipts are appended only after each fact exists.
