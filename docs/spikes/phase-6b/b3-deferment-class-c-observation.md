# Phase 6B B3 HARVEST deferment — Class C observation

## Pre-registration

- Observation task ID: `526b37e7-12ff-4c2d-8346-1d7b94b364cc`.
- Registered at `2026-07-23T07:00:25Z`, before the first Slice C contract edit.
- Baseline commit: `b091a3e645621cdaf5f875f67eebf071eaa6d560`.
- Owner/component: `registry-platform` / `registry-contract`.
- Policy/class: `platform-contract-policy/1`, Class C.
- Patch scope/affected path: `docs/contracts/telemetry-v3.md` only.
- Budget: at most 250 added Slice C contract/evidence lines; no committed tests.
- Hypothesis: defer live HARVEST until trusted LOAD context and producer-owned
  receipt resolution prevent caller-selected UUID/reference authority.
- Non-goals: activation, runtime/Host Adapter/resolver/capability/schema/
  append-internal work, and B3 subset #2.
## Immutable baseline and inputs

| Path | SHA-256 |
|---|---|
| `docs/contracts/evolution.md` | `45e188e19ff7d2398640e4aafbe3c54ed61f7a259be4fb669c1fbbf4c6c7a83a` |
| `docs/contracts/telemetry-v3.md` | `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde` |
| `registry/evolution.json` | `0c61f25588005f72c2c921cb488854063bf2d3b8d1eed990da0cbb6529ae132d` |
| `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-execution-context.md` | `5e1df39f7359959c45697b7d114419ef4cc24e3d8b485903d67bef8c7b02a256` |
| `handoffs/HANDOFF-2026-07-23-phase6b-b3-subset1-security-authority-replan.md` | `34525336dbc54d4e76467688164706dea0d8a5c413af86646c9ba1bc1b231072` |
| `plans/PLAN-phase6b-b3-harvest-authority-prerequisite.md` | `bc422c3922b2c8ca14a31ef26588589b2392b47b51afb2bf3003b7cbdae37156` |

`explain-evolution` resolved the contract uniquely to `registry-contract`,
owner `registry-platform`, Class C, `platform-contract-policy/1`.

## Candidate binding

- Patch: `docs/spikes/phase-6b/b3-harvest-deferment.contract.patch`.
- Patch SHA-256: `d8b0151221abe7715734cceda5ed632d3ab5049afc4a83bdeb0cd3b1fd2e1e46`.
- Post-apply contract SHA-256: `ccd0892f58f96f14d763a4b7fb39017cfa23d77dcf6326fef6f8474a6937bff2`.
- Policy hash: `868a6ba79241dc15907d7bb72b41a24516c8c6d8eaa14dc5e8308c472242d902`.
- Proposal: `proposal-0acfe665bc066c31dd5e`.
- The exact patch passes reverse-apply checking with `--unidiff-zero`.
- Temporary QA rejected the predecessor's CRLF working-tree hashes; this
  proposal binds canonical LF-normalized Git blobs.
## Ground-truth answers

1. T3.12 still requires HARVEST; deferment cannot satisfy Phase 6 completion.
2. A raw task UUID is correlation data, not mutation or completion authority.
3. Reference shape does not authenticate receipt existence/ownership/binding.
4. The generic scorecard CLI is not a trusted LOAD/HARVEST context.
5. Live emission requires separately approved Host Adapter trust and resolver.
6. Neither is approved; all five registry entries remain `planned`.
## Threat model

| Boundary | Threat | Required contract control |
|---|---|---|
| CLI to HARVEST | Caller supplies a task UUID as completion authority | State that generic scorecard input is untrusted and cannot confer authority |
| Evidence reference | Namespace-shaped or synthetic value impersonates a receipt | Require producer-owned resolution of existence and exact task/cause/candidate/revision/activation binding |
| Status registry | Prose, fixtures, hashes, or synthetic events activate a producer | Keep status `planned`; enumerate non-activating artifacts |
| Scope | Deferment silently approves new architecture | Explicitly approve no transport, store, schema field, event, resolver, or activation mechanism |
| Compatibility | Amendment weakens storage, privacy, disable, or downgrade rules | Preserve T3.1, T3.2, T3.6, T3.9, and T3.11 unchanged |

## Gate and review ledger

| Stage | Required evidence | Status |
|---|---|---|
| Exact patch binding | immutable canonical patch plus post-apply contract hash | PASS |
| `full-cross-component-regression` | canonical gates on exact candidate | pending |
| `knowledge-work-reviewer` | wording, claims, contradictions, evidence fidelity | pending |
| `software-dev-reviewer` | semantics, truthfulness, compatibility, scope | pending |
| `rollback-rehearsal` | inverse patch restores baseline bytes and green gates | pending |
| Platform-owner closure | approved decision bound to proposal/hash and effective run | pending |
## Rollback matrix

| Trigger | Required action |
|---|---|
| Contract ambiguity or weakened producer responsibility | append `rolled_back`; apply exact inverse patch |
| Weakened disable, privacy, downgrade, or storage guarantee | append `rolled_back`; apply exact inverse patch |
| Synthetic or caller-selected activation becomes possible | append `rolled_back`; apply exact inverse patch |
| Existing B0–B2 consumer regression | append `rolled_back`; apply exact inverse patch |

Before an authorized `effective_from_run`, the candidate is not effective.
