# PLAN — Phase 6B B3 live-HARVEST deferment (option A)

## Status and approval boundary

Revised draft for independent plan review. Maintainer Dat selected option A on
2026-07-23:

- do not build a capability broker, authority ledger, or new append surface;
- remove the unsafe caller-authorized live HARVEST seam;
- keep the build-loop HARVEST producer `planned`;
- permit live emission only after a separately approved Host Adapter provides
  trusted LOAD-bound task context and a producer-owned receipt resolver.

This is planning authority only. No contract change, runtime cleanup, proposal
decision, or producer activation is approved until this reviewed plan passes
its explicit approval gate.

## Problem and outcome

Security review of candidate `b091a3e` found:

1. namespace/shape validation cannot prove a root-cause or lesson receipt is
   producer-owned; and
2. a raw task UUID is correlation data, not authority to attach evidence or
   finish a task.

Option A closes the unsafe surface by removing it rather than inventing missing
authority. The final truthful state is:

- `scripts/scorecard.py` performs scorecard work only and accepts no telemetry
  task/ref/locus authority inputs;
- `telemetry/producers.py` contains the closed status-registry validator only;
- all five entries in `telemetry/producers.json` remain `planned`;
- no code path emits `lesson_candidate_recorded` for build-loop HARVEST;
- T3.12 explicitly records the deferred prerequisite for future activation;
- no test, prose, scorecard digest, UUID, proxy, or synthetic event can satisfy
  activation.

## Scope split and governance

The work is two separately governed slices. They never share one proposal.

### Slice C — contract deferment

- Owner/component: `registry-platform` / `registry-contract`.
- Policy/class: `platform-contract-policy/1`, Class C.
- Patch scope: `docs/contracts/telemetry-v3.md` only.
- Purpose: amend T3.12 and the release boundary so the build-loop HARVEST
  producer remains required but explicitly `planned/deferred`; live emission
  requires a later approved Host Adapter trust contract and producer-owned
  resolver.
- Fresh observation task ID:
  `526b37e7-12ff-4c2d-8346-1d7b94b364cc`.
- Exact budget: at most 250 added contract/evidence lines. Slice C commits no
  `scripts/tests/**` change.

### Slice B — runtime authority removal

- Owner/component: `maintainers`; `maintainer-scripts` and
  `telemetry-v3-runtime`.
- Policy/class: separate Class B owner-reviewed cleanup after Slice C becomes
  effective. If the Catalog rejects the two maintainer components as one
  proposal, split them into B-script and B-runtime proposals; never route them
  through the Class C contract proposal.
- Purpose: remove the unsafe live producer helper and raw scorecard authority
  options while preserving registry validation and non-telemetry scorecard
  behavior.
- Fresh observation task ID:
  `a0c67829-f505-4d40-9995-464db4a4f9f0`.
- Exact budget: at most 120 added product/test lines and a net-negative
  product/test diff against `b091a3e`.

No `registry/evolution.json` component change is planned. No new path or
storage surface is created, so the Class B `telemetry/**` classification
remains unambiguous.

## Slice C — exact Class C process

### Immutable baseline and exact amendment binding

Before the first contract edit:

1. create
   `docs/spikes/phase-6b/b3-deferment-class-c-observation.md` with the Slice C
   task ID, immutable scope, numeric budget, threat model, gate/review ledger,
   and rollback matrix;
2. capture SHA-256 inputs for:
   - `docs/contracts/evolution.md`;
   - `docs/contracts/telemetry-v3.md`;
   - `registry/evolution.json`;
   - the B3 execution-context handoff;
   - the security-authority replan handoff;
   - this approved plan;
3. author the exact candidate contract amendment as an immutable canonical
   patch artifact under
   `docs/spikes/phase-6b/b3-harvest-deferment.contract.patch`;
4. compute and record the candidate post-apply
   `docs/contracts/telemetry-v3.md` SHA-256;
5. create the closed proposal file
   `docs/decisions/evolution-<proposal_id>.proposal.json`.

The proposal:

- has `affected_paths` and `patch_scope` exactly
  `["docs/contracts/telemetry-v3.md"]`;
- resolves only to `registry-contract`;
- uses the current computed `platform-contract-policy/1` transitive
  `policy_hash`, never a copied assumption;
- includes the canonical patch artifact and this plan in `input_hashes`;
- names required gates exactly:
  `full-cross-component-regression`, `rollback-rehearsal`;
- names required reviewers exactly:
  `knowledge-work-reviewer`, `software-dev-reviewer`;
- names `platform-owner` as closer;
- uses deterministic EV5 proposal identity over every field except
  `proposal_id`;
- states an observation window with exact RFC 3339 start/end values;
- rolls back if deferment creates contract ambiguity, weakens disable/privacy
  guarantees, permits synthetic activation, or breaks existing B0–B2
  consumers.

Any semantic change to the patch, hashes, evidence, window, scope, reviewers,
gates, or rollback creates a new proposal ID/file. The proposal is immutable.

Slice C test support is governance-isolated: candidate-specific negative
assertions run as temporary, uncommitted fixtures inside the isolated review
worktree. They are recorded as supporting QA evidence, never included in the
Class C patch/proposal scope and never treated as decisive evidence approving
the proposal they were created to test. Durable regression guards land only
in post-effective Slice B under `maintainer-policy`.

### Candidate amendment semantics

The exact patch must say:

1. build-loop HARVEST remains one of the five required producer
   responsibilities;
2. its status remains `planned` and cannot satisfy Phase 6 completion;
3. the current generic scorecard CLI is not a trusted LOAD/HARVEST context and
   must not accept task UUIDs or evidence references as producer authority;
4. live emission requires both:
   - an independently approved Host Adapter contract that propagates the
     LOAD-minted task identity through a trusted, non-caller-selected context;
   - a producer-owned resolver that verifies receipt existence and exact task,
     root-cause, candidate, producer-revision, and activation binding;
5. no capability transport, receipt store, schema field, event, or activation
   mechanism is approved by this deferment;
6. fixtures, prose, scorecard records, namespace-shaped hashes, task UUIDs, and
   synthetic events cannot activate the producer;
7. a future implementation is a new proposal with its own observation,
   budget, threat model, cross-host contract, and security review.

T3.1, T3.6, T3.9, T3.11, and the exact T3.2 storage surfaces remain unchanged.

### Independent evidence and closure

On the exact candidate patch in an isolated worktree:

1. run the canonical full gates;
2. run cross-component telemetry contract/runtime/CLI/scorecard tests;
3. obtain an independent knowledge-work review for wording, claim support,
   contradiction, and evidence fidelity;
4. obtain an independent software-dev review for contract semantics,
   activation truthfulness, downgrade/disable compatibility, and scope;
5. rehearse rollback by applying the exact inverse patch in a separate
   isolated worktree and rerunning the canonical gates;
6. record immutable gate/review/rollback evidence refs.

Only the appointed `platform-owner`, distinct from the proposer, may append an
`approved` record to `docs/decisions/evolution-manual.decisions.jsonl`.
The decision must bind the exact proposal ID/policy hash, one evidence ref per
required gate, the appointment reference, and a non-empty
`effective_from_run`. Before that append, Slice C is not approved. The exact
candidate patch is applied only in the named effective run and its resulting
contract SHA-256 must equal the proposal-bound candidate hash.

Rollback appends a `rolled_back` decision and applies the exact inverse
contract patch. Prior proposal/decision/evidence bytes remain append-only.

## Slice B — runtime authority removal

Slice B starts only after Slice C's approved decision is effective.

Before product edits, create
`docs/spikes/phase-6b/b3-deferment-runtime-cleanup-observation.md` with its own
task ID, baseline, threat model, exact budget, and review ledger.

Files:

| File | Planned change |
|---|---|
| `scripts/scorecard.py` | remove `_harvest_producers`, `append_scorecard_with_harvest`, `--telemetry-task-id`, `--root-cause-locus`, `--root-cause-ref`, and `--lesson-candidate-ref`; restore ordinary scorecard append/report behavior |
| `telemetry/producers.py` | remove event construction, receipt regexes, producer policy, and `emit_build_loop_harvest`; retain closed producer IDs and registry load/shape/status validation |
| `telemetry/producers.json` | unchanged bytes: exactly five `planned` entries with null event IDs |
| `scripts/tests/test_telemetry_producers.py` | replace live-emission tests with deferment guards and registry truthfulness tests |
| `scripts/tests/test_scorecard_append.py` | pin that the generic scorecard CLI exposes no telemetry authority flags and creates no telemetry file |
| `scripts/tests/test_telemetry_contract.py` | add durable post-effective guards for the exact T3.12 deferment and future-prerequisite wording |
| `docs/spikes/phase-6b/b3-observation.md` | append factual supersession/deferment and reviewer ledger only after evidence exists |

No append/lock/strict-tail/corpus-check internal is changed. No new storage,
dependency, environment variable, capability, resolver, or Host Adapter is
added.

## Red-before-green tests

Slice C temporary supporting QA (isolated worktree, never committed):

1. contract test initially fails until T3.12 states the deferment and both
   future prerequisites;
2. contract test rejects wording that treats scorecard/UUID/hash/prose/test
   evidence as activation;
3. proposal validation rejects wrong policy hash, changed patch hash, missing
   reviewer/gate, cross-owner path, missing effective run, or non-deterministic
   ID;
4. rollback rehearsal proves the prior contract bytes and full gates restore.

These temporary assertions are non-decisive; the two independent reviews,
cross-component regression, and rollback rehearsal close the Class C gates.

Slice B durable committed regression:

1. scorecard parser rejects all removed telemetry authority flags;
2. ordinary `--append-record` succeeds and creates no telemetry event file;
3. `telemetry.producers` exports no live-emission helper;
4. all five registry entries remain planned/null;
5. `active` remains invalid without a future approved resolver contract;
6. no product path accepts task UUID, root-cause ref, candidate ref, locus, or
   caller-provided capability for HARVEST emission;
7. B0–B2 telemetry lifecycle/CLI/runtime tests remain green;
8. the committed contract test pins the exact deferment/prerequisite wording
   that became effective in Slice C;
9. no rejected value, secret, prompt, environment value, or provider
   transcript is introduced.

Any new/changed validator rule receives an isolated broken fixture before its
final green result.

## Gates and review order

For each slice and after every reviewer-driven fix:

1. `python scripts/validate.py`;
2. `pytest scripts/tests`;
3. `bash -n scripts/init.sh`;
4. `shellcheck scripts/init.sh`;
5. `git diff --check`.

Slice C review order:

1. knowledge-work independent review;
2. software-dev independent review;
3. Class C rollback rehearsal;
4. platform-owner decision;
5. post-effective-run full regression and consuming-validator rerun.

Slice B review order:

1. QA `PHASE DONE`;
2. code review `APPROVE`;
3. security review `APPROVE`;
4. unconditional final regression QA;
5. observation/scorecard append;
6. consuming validator rerun after every append.

Reviews are sequential and diff-scoped. Findings re-reviews are
findings-scoped, but every finding fix also reruns the full canonical gates.

## Demo

1. Before Slice C decision, show the proposal is review-ready but not
   effective and runtime bytes are unchanged.
2. After the effective Class C run, show T3.12 states the planned deferment
   while T3.1/T3.2/T3.6/T3.9/T3.11 remain unchanged.
3. After Slice B, run ordinary scorecard append: scorecard succeeds and no
   telemetry event file is created.
4. Pass each former telemetry authority flag: parser rejects it.
5. Load `telemetry/producers.json`: all five entries validate as planned/null.
6. Show no live-emission helper or authority path exists.
7. Apply the rollback rehearsal in isolation and show prior contract plus all
   gates restore.

## Mandatory stops

- proposal path resolves to more than one component or wrong owner/policy;
- candidate patch/hash changes after proposal creation;
- either independent Class C reviewer returns a blocker;
- platform-owner decision is absent, stale, or bound to another proposal/hash;
- runtime cleanup starts before `effective_from_run`;
- cleanup requires any Host Adapter, schema, storage, append-internal, or
  capability work;
- Slice C exceeds 250 added lines or Slice B exceeds 120 added product/test
  lines or ceases to be net-negative;
- any producer status changes from `planned`;
- any gate or required reviewer is red.

## Done evidence

- fresh Slice C and Slice B observations;
- immutable proposal and exact candidate patch/hash;
- knowledge-work and software-dev reviews on the exact patch;
- cross-component regression and isolated rollback rehearsal;
- platform-owner approved decision with effective run;
- post-effective contract hash receipt;
- net-negative Class B cleanup with QA/code/security/final-QA verdicts;
- validator reruns after observation and scorecard appends;
- all producers still `planned`;
- five-part report ending with subset #1 deferred, not active, and no subset #2
  started.
