# dat-kit v6.0.0 Open Platform Plan

**Status:** DRAFT — proposed replacement for `PLAN-v5.0.0-open-platform.md`  
**Program releases:** dat-kit 2.0.0, 2.1.0, and 2.2.0  
**Maintenance prerequisite:** dat-kit 1.17.1  
**Prepared:** 2026-07-17  
**Decision required before implementation:** approve the contracts, compatibility model, and release boundaries in §14.

---

## 0. Executive decision

The v5 direction is sound and should be retained:

- Domain Packs become first-class components.
- `AGENTS.md` remains the single generated-project policy contract.
- AI hosts remain thin adapters and never become policy owners.
- registries replace host/domain hardcoding.
- telemetry becomes append-only and useful for measured tuning.
- `kit-evolve` proposes changes but cannot bypass gates or review.

However, v5 is not yet implementation-safe. Its remaining defects are at the boundaries between otherwise good components:

1. an old project contract is described as “supported” without distinguishing a green current contract from a recognized migration source;
2. registry implementation begins before the normative registry and evolution contracts exist;
3. generated Domain Pack triggers have no named renderer or executable conformance path;
4. registry bootstrap and unknown-format behavior are unspecified;
5. the scorecard write bug is left as an optional fix and the maintenance branch is cut too early;
6. registry inventory is not connected to a generic scaffold materialization protocol;
7. `task_id` is minted too late to join early gate and review events;
8. evolution signals and authorities are mentioned but not defined as governed registries;
9. acceptance rate is still treated as an optimization signal, which rewards easy proposals instead of useful outcomes;
10. v2.1 and v2.2 have feature work but not complete release trains.

This v6 plan closes those gaps without redesigning the platform. It makes the contracts precede their implementations, adds explicit state machines and generated projections, and gives every program release an executable route to RC, rollback, and tag.

**Verdict on v5:** REVISE, not reject.  
**Replacement:** use this document as the implementation plan after the decisions in §14 are approved.

---

## 1. Product outcome

dat-kit becomes an open discipline platform whose stable center is a work contract, not a particular coding agent.

The platform must support five outcomes.

### 1.1 Multi-profession composition

A profession is installed as one Domain Pack under `domains/<domain-id>/` plus one descriptor in `registry/domains.json`. The software-development discipline is no longer embedded in `build-loop`; it is one Domain Pack composed with a reusable work-loop engine.

### 1.2 Host-neutral policy

Generated projects have one canonical instruction contract: `AGENTS.md`. Claude Code, Codex, Gemini CLI, Cursor, and future hosts receive only pointer/configuration artifacts registered as Host Adapters. Those artifacts may select or point to policy but may not duplicate, weaken, or override it.

### 1.3 Registry-driven extension

Adding a valid host or domain changes descriptors, templates, and generated projections—not validator branching, shell copy lists, or hand-maintained inventories. Validators are generic over registered component types and declared format revisions.

### 1.4 Measured I/O improvement

Telemetry v3 records enough context to understand input/output cost and workflow quality over time: tokens when attribution is safe, first-pass gate rate, review rounds, defects, elapsed time, event coverage, and relevant component revisions.

### 1.5 Governed learning from history

`kit-evolve` mines telemetry and lessons, including explicitly imported evidence from real projects, and generates deterministic proposals. It may improve any governed component, including itself. It may never merge its own proposal, weaken its own evidence requirements, or use a newly created evaluation to approve the same proposal.

---

## 2. Non-negotiable architectural claims

These claims are program invariants. Any exception is a Class C governance decision.

1. **One generated-project policy owner:** `AGENTS.md`.
2. **Thin host adapters:** pointers/configuration only; no copied policy.
3. **One descriptor owner per component:** no independent second inventory.
4. **Generated artifacts are projections, not authorities:** every projection has a marker and byte-exact `--check` validation.
5. **Normative contracts precede implementations:** code cannot define an undocumented format by accident.
6. **Recognized old is not valid current:** migration-source revisions are diagnostic and non-green.
7. **Inspect before mutate:** brownfield projects are never rewritten merely because their old revision is recognized.
8. **Telemetry facts are immutable:** corrections are new events, never edits.
9. **Evolution proposals are deterministic and review-bound:** mining is automated; authority is not.
10. **Governance evidence is temporally independent:** a proposal cannot manufacture the corpus or gate that certifies itself.
11. **Extension tests prove deletion of hardcoding:** a synthetic component must work without editing a validator, renderer consumer, or scaffold copy list.
12. **Release claims require release trains:** implementation DoD is insufficient without RC, migration, smoke, rollback, and tag evidence.

---

## 3. Architecture

### 3.1 Six-slot Domain Pack contract

Every active Domain Pack has exactly six semantic slots:

| Slot | Responsibility | Required |
|---|---|---:|
| `descriptor` | identity, revisions, aliases, dependencies, lifecycle | yes |
| `workflow` | domain-specific phases and decision flow | yes |
| `ground_truth` | authoritative sources and evidence hierarchy | yes |
| `deliverables` | output contracts and completion criteria | yes |
| `gates` | mechanical and judgment gates | yes |
| `reviewers` | reviewer roles, routing, and escalation | yes |

The reusable work-loop engine owns only cross-domain mechanics:

```text
LOAD → FRAME → PLAN → EXECUTE → VERIFY → REVIEW → HARVEST
```

The engine does not own software terminology, repository operations, test commands, or a profession’s standards of truth. The Domain Pack supplies those meanings.

Composition order is deterministic:

```text
canonical project contract
  → work-loop engine revision
  → Domain Pack descriptor and six slots
  → optional project profile
  → Host Adapter projection
```

Later layers may narrow execution but may not contradict earlier policy. A contradiction produces a named diagnostic and stops composition.

### 3.2 Projection Module

Registry data cannot remain aspirational metadata. A single Projection Module owns all committed derived artifacts.

Required interface:

```text
catalog.render_domain_trigger(domain_id) -> bytes
catalog.render_scaffold_manifest() -> bytes
catalog.render_adapter_projection(adapter_id, artifact_id) -> bytes
catalog.render_version_projection(target_id) -> bytes
catalog.check_projections() -> Diagnostic[]
```

The command surface is provided by `scripts/render.py`:

```text
python scripts/render.py domain-trigger <domain-id>
python scripts/render.py scaffold-manifest
python scripts/render.py all
python scripts/render.py --check
```

Rules:

- all output is deterministic for the same repository state;
- generated files contain `GENERATED FROM REGISTRY — DO NOT EDIT` plus the source descriptor revision;
- `--check` compares byte-for-byte and never rewrites;
- normal generation is explicit and reports every changed projection;
- paths, identifiers, aliases, and action names are validated before rendering;
- no generated artifact becomes a second source of truth.

#### Domain trigger projection

The Domain Pack descriptor owns the user-facing skill name, description, aliases, Domain Pack ID, and required engine revision. The renderer owns the standardized thin body.

The body must:

1. resolve the descriptor through the Registry Catalog;
2. load the declared engine revision;
3. load all six slots in contract order;
4. load the project profile when declared;
5. fail with a named diagnostic on a missing slot or revision mismatch;
6. execute deliverable, gate, and reviewer routing from the loaded pack.

The trigger must not contain independent domain policy.

#### Scaffold manifest projection

To preserve Bash-only greenfield initialization while removing hardcoded copy lists, the Projection Module renders:

```text
templates/common/.dat-kit-files.tsv
```

Each validated row contains:

```text
source_rel<TAB>target_rel<TAB>ownership<TAB>action<TAB>introduced_revision<TAB>lifecycle
```

Constraints:

- tabs, newlines, traversal segments, absolute paths, shell metacharacters, and unknown actions are forbidden in path fields;
- action is a closed, versioned enum;
- only `scaffold_active` rows may be materialized;
- `scripts/init.sh` reads the manifest generically and never uses `eval`, `grep` parsing, or ad hoc JSON parsing;
- a synthetic Host Adapter becomes materializable after registry/template changes and rendering, with no shell edit.

The TSV is a shipped projection for runtimes without Python. `registry/platform.json` and component registries remain its authority.

### 3.3 Registry Module and bootstrap

The Registry Module is a deep module, not a shared JSON helper collection.

Its public interface is the Registry Catalog:

```text
Catalog.load(repo_root) -> Catalog | Diagnostic[]
Catalog.domains() -> DomainDescriptor[]
Catalog.adapters() -> AdapterDescriptor[]
Catalog.evolution_policy() -> EvolutionPolicy
Catalog.scaffold_file_plan(mode) -> FilePlan
Catalog.version_targets() -> VersionTarget[]
Catalog.governed_paths() -> GovernedPathSet
Catalog.explain_path(path) -> OwnershipExplanation
```

The only implementation hardcodes allowed for registry discovery are:

1. bootstrap filename `registry/platform.json`;
2. the set of registry-format revisions understood by the running code;
3. named bootstrap diagnostics.

Everything else is discovered from `platform.json`.

Bootstrap behavior is fail-closed:

| Condition | Required diagnostic |
|---|---|
| file missing | `REGISTRY_BOOTSTRAP_MISSING` |
| malformed JSON | `REGISTRY_BOOTSTRAP_MALFORMED` |
| unknown/future format | `REGISTRY_FORMAT_UNSUPPORTED` |
| referenced child missing | `REGISTRY_CHILD_MISSING` |
| child revision mismatch | `REGISTRY_CHILD_REVISION_MISMATCH` |
| mixed incompatible code/data upgrade | `REGISTRY_ATOMIC_UPGRADE_REQUIRED` |

The Registry Module uses a bespoke standard-library validator. It must provide path-aware diagnostics and must not imply JSON Schema compliance unless JSON Schema becomes an explicit later dependency.

### 3.4 Normative registry documents

The following documents are written and approved before registry implementation:

- `docs/contracts/registry.md`
- `docs/contracts/evolution.md`
- `docs/contracts/domain-pack.md`
- `docs/contracts/host-adapter.md`

They define formats, ownership, lifecycle, diagnostics, extension protocol, and compatibility rules. Tests and Python types implement those documents; neither code nor example JSON silently becomes the normative contract.

### 3.5 Project materialization and FilePlan

The Registry Catalog produces a typed FilePlan. The same plan semantics drive greenfield scaffolding, brownfield inspection, and migration previews.

A FilePlan entry contains at least:

```text
source_template
target_relative_path
ownership_class
materialization_action
artifact_lifecycle
project_contract_revision
expected_content_hash
precondition
```

Materialization modes:

| Mode | Allowed behavior |
|---|---|
| `greenfield` | create the full active plan in an empty target |
| `add-missing` | create only absent, independently safe artifacts |
| `inspect-brownfield` | report differences; do not mutate |
| `migrate-approved` | apply an explicit migration plan after backup and review |

`scripts/init.sh` is a compatibility launcher and greenfield materializer over the generated manifest. Python-side contract and migration tools consume the Registry Catalog directly. They must agree on the FilePlan through conformance fixtures.

### 3.6 Project contract revision state machine

`registry/platform.json` defines project contract compatibility explicitly:

```text
canonical_revision
green_revisions[]
migratable_source_revisions[]
unsupported_revisions[]
revision_descriptors[]
migration_edges[]
```

Semantics:

- **canonical revision:** emitted by current scaffolding;
- **green revision:** accepted as current by the current checker;
- **migratable source revision:** recognized for inspection and migration, but never reported as green;
- **unsupported revision:** known or unknown revision with no safe migration path.

For dat-kit 2.0:

```text
canonical_revision = dat-kit 2.0
green_revisions = [dat-kit 2.0]
migratable_source_revisions = [dat-kit 1.16.0]
```

A v1.16 project produces `CONTRACT_MIGRATION_REQUIRED` and a nonzero brownfield scaffold result. Recognition prevents data loss; it does not certify currency.

Every recognized revision has an immutable descriptor containing:

- contract marker rules;
- required pointer set;
- static-template hashes where relevant;
- migration edges;
- snapshot provenance;
- the last release allowed to remove support.

Snapshots ship under `registry/snapshots/`; migration logic may not depend on Git history being present. Removing the v1.16 migration source before the next major release requires a Class C proposal.

### 3.7 Host Adapter lifecycle

Every Host Adapter artifact has one lifecycle state:

```text
repo_only → migration_ready → scaffold_active → retired
```

Meaning:

- `repo_only`: conformance-tested inside dat-kit but never emitted to projects;
- `migration_ready`: migration preview and fixtures exist, but greenfield emission is off;
- `scaffold_active`: greenfield and approved migration may emit it;
- `retired`: descriptor retained for recognition/removal guidance, not emitted.

Activation gates:

1. repository conformance passes;
2. official host behavior is fact-checked;
3. clean and customized brownfield fixtures pass;
4. the adapter does not duplicate policy;
5. rollback removes only adapter-owned artifacts;
6. only then may lifecycle become `scaffold_active`.

This prevents a registry entry from silently becoming a project mutation.

### 3.8 Governed universe

`registry/evolution.json` declares the universe `kit-evolve` is allowed to reason about:

```text
governed_roots[]
explicit_exclusions[]
component_classes[]
signals[]
authorities[]
policies[]
```

Every tracked product file under a governed root must resolve to exactly one owner and governance class. A newly added top-level product path that is neither governed nor excluded fails with `EVOLUTION_ORPHAN_PATH`.

Generated files resolve to their source descriptor owner, not to an independent generated-file owner.

### 3.9 Signal and authority catalogs

Evolution policies must not refer to informal names.

A signal descriptor includes:

```text
signal_id
producer
artifact_or_schema_revision
status = active | proxy | planned
quality_limitations
retention
```

A policy may use an `active` or explicitly approved `proxy` signal. A `planned` signal cannot satisfy a gate.

An authority descriptor includes:

```text
authority_id
role_type
allowed_decision_classes
allowed_closer
succession_rule
approval_evidence_contract
revocation_rule
```

Proposal decisions record:

```text
policy_revision
policy_hash
closer_identity_or_role
approval_reference
decision_timestamp
effective_from_run
```

There must be a usable manual proposal path before `kit-evolve` exists:

```text
python scripts/registry.py explain-evolution <path>
```

The command reports owner, class, required signals, gates, reviewers, authority, and expected evidence. `docs/contracts/evolution.md` defines how a maintainer creates and closes the proposal by hand.

### 3.10 Telemetry task lifecycle

A task identifier must exist before gates and reviews occur. Telemetry v3 therefore has a lifecycle, not only a completion writer:

```text
python scripts/telemetry.py start
python scripts/telemetry.py append --task-id <uuid> --event <type> ...
python scripts/telemetry.py finish --task-id <uuid> ...
```

Rules:

- a UUIDv4 is minted at `LOAD` or the first equivalent work-loop step;
- the ID propagates through handoffs, delegated work, gate events, review events, and HARVEST;
- the scorecard finalizes the task at HARVEST; it does not normally mint the ID;
- a standalone completion-only scorecard may mint an ID but must record `event_coverage = partial`;
- event writes are append-only, atomic at the record boundary, and protected against concurrent writers;
- correction events point to the incorrect event and never replace it;
- Windows and Linux concurrency behavior is fixture-tested.

Token attribution remains nullable. Exact totals are recorded only when a source can unambiguously attribute them to one task. Otherwise telemetry stores a reason code, not a fabricated value.

### 3.11 Evolution objectives

Proposal acceptance rate is diagnostic only. It must not be optimized because a miner could improve it by proposing small or easy changes.

Primary outcome reporting is stratified by governance class and includes:

- realized post-change outcome;
- first-pass gate-rate delta;
- review-round delta;
- token or elapsed-time delta where attribution is reliable;
- defect and revert rate;
- unmeasured-outcome rate;
- time to decision;
- proposal volume and acceptance rate as context, not target.

No proposal is called successful until its declared observation window closes or it is explicitly marked unmeasured.

---

## 4. Target repository layout

```text
AGENTS.md
docs/
  agent-workflow.md
  agent-working-rules.md
  domains.md
  loops.md
  contracts/
    registry.md
    evolution.md
    domain-pack.md
    host-adapter.md
    telemetry-v3.md                 # v2.1
engine/
  work-loop/
    ENGINE.md
    profiles/
registry/
  platform.json
  domains.json
  adapters.json
  evolution.json
  snapshots/
    project-contract-1.16.json
domains/
  software-dev/
    domain.json
    workflow.md
    ground-truth.md
    deliverables.md
    gates.md
    reviewers.md
skills/
  build-loop/
    SKILL.md                         # generated thin trigger
  domain-builder/
    SKILL.md
  scorecard/
    SKILL.md
  kit-evolve/                       # v2.2
    SKILL.md
adapters/
  claude-code/
  codex/
  gemini-cli/
  cursor/
templates/
  common/
    AGENTS.md
    .dat-kit-files.tsv              # generated projection
  contracts/
scripts/
  registry.py
  render.py
  contract_check.py
  init.sh
  telemetry.py                      # v2.1
  evolve.py                         # v2.2
  tests/
benchmarks/
  skill-evals/
  migration/
  registry/
  evolution/
telemetry/
  README.md
  schema-v3.json                    # v2.1
  events.jsonl                      # local, ignored or fixture-only
evolution/
  proposals/                        # v2.2
  decisions.jsonl                   # v2.2
```

Names may change only through the ownership map in Phase 4. Semantic owners and interfaces may not be silently merged for convenience.

---

## 5. Release and branch topology

The scorecard defect is a prerequisite maintenance fix, not optional acceptance debt.

```text
master at 1.17.0
  └─ maintenance/scorecard-no-rewrite
       └─ tag v1.17.1
            ├─ release/1.x
            └─ feature/open-platform-v2
                 ├─ tag v2.0.0
                 ├─ tag v2.1.0
                 └─ tag v2.2.0
```

Rules:

- `release/1.x` is cut from the v1.17.1 fixed commit, never from the known-bad v1.17.0 state;
- the open-platform branch also starts from that fixed commit;
- maintenance changes are merged or cherry-picked through review; no hidden branch divergence;
- each program release has its own RC evidence bundle and rollback note;
- no v2-only registry or telemetry behavior is backported to 1.x unless separately approved.

---

## 6. Implementation phases

### Phase 0A — Mandatory scorecard maintenance release (v1.17.1)

**Purpose:** stop a known evidence-corruption path before branching.

Current behavior reads and rewrites the full scorecard file during token filling. That contradicts append-only claims and can ambiguously attribute session totals to a task.

Implement the smallest safe maintenance patch:

1. disable persistent post-hoc token enrichment of existing records;
2. allow exact session totals only in the newly appended record when attribution is unambiguous;
3. otherwise write null plus a reason code in the existing compatible field surface or omit enrichment according to the current schema contract;
4. update the scorecard skill and documentation so they no longer promise unsafe filling;
5. do not introduce telemetry v3 or a sidecar in this maintenance release.

Required tests:

- hash the file prefix, run scorecard completion, and prove prior bytes are unchanged;
- ambiguous multi-task session leaves tokens unknown;
- exact single-task attribution writes only the new record;
- malformed last record does not cause older records to be rewritten;
- concurrent append failure leaves existing bytes intact;
- existing v1.17 scorecard readers continue to work.

Exit criteria:

- all repository gates pass;
- release notes explain the behavioral correction;
- v1.17.1 is tagged;
- `release/1.x` and the v2 feature branch are based on the fixed commit.

No “dated acceptance” alternative is permitted.

### Phase 0B — Decisions, spikes, and escape hatch

Before structural changes:

1. approve the six-slot Domain Pack contract;
2. approve Python standard-library validation rather than JSON Schema;
3. approve Bash-only greenfield support via a generated sanitized manifest;
4. approve the contract revision state machine;
5. approve adapter artifact lifecycles;
6. approve the v2.0/v2.1/v2.2 release split;
7. record exact official-doc facts for all initial Host Adapters;
8. capture the current gate commands and expected fixture behavior.

Run narrow spikes for:

- deterministic domain-trigger rendering;
- sanitized manifest parsing in Bash on Windows Git Bash and Linux;
- unknown/future registry-format diagnostics;
- project-contract snapshot matching without Git history;
- append locking strategy on Windows and Linux;
- deterministic proposal IDs across path separators.

Create:

- an isolated worktree or branch for the cutover;
- a revert map by phase;
- a fixture inventory;
- a line-level ownership draft for files split in Phase 4.

Exit criteria:

- every spike has a short decision report with alternatives, result, and rejected risks;
- unresolved decisions block the dependent phase;
- no public scaffolding behavior has changed.

### Phase 1A — Normative contracts before code

Write and approve:

1. `docs/contracts/registry.md`;
2. `docs/contracts/evolution.md`;
3. `docs/contracts/domain-pack.md`;
4. `docs/contracts/host-adapter.md`.

The contracts must include:

- bootstrap and format revision behavior;
- all named diagnostics;
- descriptor field ownership;
- generated projection rules;
- six-slot semantics;
- adapter lifecycle;
- project contract revision states;
- governed roots, exclusions, signals, authorities, and policies;
- extension and retirement protocol;
- compatibility and rollback expectations.

Also define Python protocol types for review, but do not let type definitions add undocumented semantics.

Exit criteria:

- contract review passes;
- examples validate against the prose rules;
- contradictions between documents are resolved;
- implementation tasks reference contract clauses.

### Phase 1B — Registry, Projection, and FilePlan foundations

Implement:

- `registry/platform.json` as bootstrap and version owner;
- `registry/domains.json` for current Domain Pack inventory;
- `registry/adapters.json` for current Host Adapter inventory;
- `registry/evolution.json` for governed paths and initial manual policies;
- `scripts/registry.py` as the Registry Catalog;
- `scripts/render.py` as the Projection Module;
- the generated scaffold manifest;
- immutable v1.16 project-contract snapshot metadata;
- generic registry and projection validation in `scripts/validate.py`.

Important lifecycle constraints:

- current domain descriptors are marked `legacy` until the six-slot cutover in Phase 4;
- new project adapter artifacts remain `repo_only` until Phase 3;
- Phase 1 does not claim six-slot behavioral conformance;
- Phase 1 does not emit new project artifacts.

Extension fixtures:

1. add a synthetic registry-only domain and validate it without editing Python;
2. add a synthetic host descriptor and template, render the manifest, and prove no shell copy-list edit is needed;
3. add an unknown descriptor field and receive a path-aware diagnostic;
4. add an unknown/future bootstrap format and receive `REGISTRY_FORMAT_UNSUPPORTED` before child loading;
5. simulate mixed code/data revisions and fail atomically;
6. create a new governed product path and receive `EVOLUTION_ORPHAN_PATH`;
7. delete a descriptor referenced by a projection and fail byte-exact projection check.

Exit criteria:

- current validators consume the Registry Catalog for inventory;
- no host/domain tuple remains in validator logic outside fixtures;
- generated projections are byte-exact in CI;
- existing public scaffolding output remains unchanged;
- greenfield initialization still works without Python from a released package.

### Phase 2 — Repository-side Host Adapter conformance

Create or normalize repository-side adapter packages for:

- Claude Code;
- Codex;
- Gemini CLI;
- Cursor.

Each descriptor declares:

- host ID and aliases;
- official documentation reference and verification date;
- repository artifact paths;
- project artifact paths;
- pointer semantics;
- policy-content prohibition;
- supported host capability assumptions;
- artifact lifecycle;
- conformance fixtures and smoke command.

All newly introduced project artifacts remain `repo_only` in this phase.

Conformance tests must prove:

- the adapter points to `AGENTS.md` or selects it through an officially supported mechanism;
- the adapter contains no duplicated policy blocks;
- missing `AGENTS.md` produces a clear failure or documented host degradation;
- adding a synthetic adapter changes registry/templates/projections only;
- retirement removes only adapter-owned artifacts;
- official-doc assertions are recorded with dates and source links.

Exit criteria:

- repository-side adapter packages are green;
- host smoke tests pass where the host is available;
- unavailable hosts have an explicit manual evidence checklist;
- no new project artifact is emitted yet.

### Phase 3 — Contract migration state machine and adapter activation

Implement the project contract revision model in `contract_check.py` and scaffolding preflight.

Required fixtures:

| Fixture | Expected result |
|---|---|
| clean v1.16 project | nonzero `CONTRACT_MIGRATION_REQUIRED`, deterministic preview |
| customized v1.16 project | nonzero diagnostic, custom files preserved, conflicts reported |
| clean v2 project | green |
| partially migrated project | named incomplete-migration diagnostic |
| unknown contract revision | unsupported, no mutation |
| missing marker with recognizable files | ambiguous, no mutation |

Migration sequence:

1. inspect and classify;
2. emit immutable pre-change report and hashes;
3. build a migration FilePlan;
4. require explicit approval for replacement/removal actions;
5. back up changed adapter-owned files;
6. apply the plan;
7. run contract and host conformance;
8. emit rollback instructions.

Adapter artifacts progress:

```text
repo_only → migration_ready
```

Only after clean and customized fixtures pass may an approved artifact become:

```text
migration_ready → scaffold_active
```

Exit criteria:

- v1.16 never reports green under a v2 checker;
- brownfield default behavior is inspect-only;
- greenfield output is registry-driven;
- project artifacts are activated individually, not by registry presence alone;
- rollback is fixture-tested.

### Phase 4 — Isolated structural cutover to six-slot Domain Packs

Perform the cutover in the isolated worktree created in Phase 0B.

Before moving lines, complete a line-level ownership map for:

- current `build-loop` instructions;
- `docs/loops.md`;
- software development gates and reviewer rules;
- generated-project templates;
- domain-builder guidance;
- maintainer-only rules.

Every substantive existing instruction is assigned exactly one destination:

```text
engine | domain-pack | project-contract | maintainer-policy | retired-with-reason
```

Implement:

- the host-neutral work-loop engine;
- `domains/software-dev/` with all six slots;
- an active six-slot software-dev descriptor;
- a generated thin `build-loop` trigger;
- domain-builder authoring through descriptor + six slots + renderer;
- docs and examples derived from the new owners where appropriate.

Behavioral tests:

1. software-dev happy path loads all six slots;
2. a synthetic non-software Domain Pack completes the same engine lifecycle;
3. missing or stale generated trigger fails projection check;
4. hand-edited trigger fails byte-exact check;
5. alias collision fails registry validation;
6. changed required engine revision fails composition;
7. skill eval verifies that actual Domain Pack files are loaded, not merely that their names appear in text;
8. negative trigger cases remain included in the eval corpus;
9. current software-dev behavior is compared with the ownership map and approved differences.

Cutover discipline:

- commit by semantic owner, not arbitrary file batches;
- run validation after each owner moves;
- if a move fails, revert that semantic slice rather than patching duplicate policy into both locations;
- no partial six-slot claim may reach `master`.

Exit criteria:

- software development is an active Domain Pack;
- the engine contains no software-specific policy;
- `build-loop` is a generated thin trigger;
- synthetic non-software behavior passes;
- the ownership map has no unassigned or duplicate policy lines.

### Phase 5 — dat-kit 2.0.0 release train

2.0.0 contains the open platform foundation, Domain Pack cutover, Host Adapter model, and migration path. It does not claim telemetry v3 or automated evolution.

Release train:

1. freeze registry and contract format revisions;
2. bump the version owner in `platform.json`;
3. render and byte-check all derived versions and projections;
4. run unit, contract, registry, projection, migration, and skill eval suites;
5. run clean-install smoke tests on Windows Git Bash and Linux;
6. run available-host smoke tests plus manual evidence for unavailable hosts;
7. migrate clean and customized v1.16 fixtures;
8. build RC1 and archive its evidence bundle;
9. resolve findings through reviewed commits and issue RC2 if needed;
10. validate rollback to v1.17.1 tooling and preservation of project files;
11. publish migration guide, adapter support table, and release notes;
12. tag v2.0.0 only from the approved RC commit.

2.0.0 exit criteria:

- all §13 v2.0 program gates pass;
- no unresolved Class B or C decision remains;
- the RC artifact equals the tagged artifact;
- `release/1.x` gates still pass on its own branch.

### Phase 6 — Telemetry v3 and dat-kit 2.1.0

Write and approve `docs/contracts/telemetry-v3.md` before implementation.

The schema includes:

- event ID, task ID, parent/delegation ID where applicable;
- timestamps and producer revision;
- domain, engine, adapter, contract, and profile revisions;
- gate outcomes and first-pass status;
- review rounds and reviewer class;
- defects and rework;
- tokens with attribution status and reason;
- elapsed time with clock source;
- event coverage;
- privacy/source class;
- correction linkage.

Implement:

- `scripts/telemetry.py start|append|finish|validate`;
- append locking and recovery;
- scorecard HARVEST integration;
- early task-ID creation in work-loop triggers;
- handoff/delegation propagation;
- v2-to-v3 import as new events or explicitly separate legacy input, never history rewrite;
- producer coverage for active signals declared in `evolution.json`.

Required tests:

- concurrent writers on Windows and Linux;
- interrupted append and last-record recovery;
- prior-byte hash preservation;
- duplicate event ID rejection;
- correction event behavior;
- partial completion-only task coverage;
- exact versus ambiguous token attribution;
- handoff and delegated child linkage;
- no secrets or raw prompts in default telemetry.

2.1.0 release train:

1. freeze telemetry schema v3;
2. bump version owner and render projections;
3. run all 2.0 regression suites plus telemetry tests;
4. run an RC observation sample on representative tasks;
5. verify schema downgrade/disable behavior;
6. publish privacy, retention, and migration notes;
7. verify 1.x compatibility branch remains unaffected;
8. tag v2.1.0 from the approved RC commit.

### Phase 7 — Governed self-evolution and dat-kit 2.2.0

Implement `kit-evolve` only after active telemetry producers exist.

Inputs:

- telemetry v3 events;
- lessons learned;
- approved external project evidence with provenance;
- registry component revisions;
- prior proposals and decisions;
- active/proxy signal definitions.

Outputs:

- deterministic proposal ID;
- governed owner and class;
- evidence window and input hashes;
- hypothesis and predicted outcome;
- proposed patch scope;
- required gates, reviewers, and closer authority;
- pre-change baseline snapshot;
- observation plan;
- rollback condition;
- decision record after closure.

Automation boundary:

- the miner may create proposal artifacts and candidate patches in an isolated branch;
- it may run predeclared gates;
- it may not approve, merge, change authority, or weaken the policy governing its own proposal;
- any enforcement path capable of weakening governance is Class C;
- eval and benchmark artifacts are at least Class B;
- an eval/corpus created or materially changed by a proposal cannot be used as the decisive evidence approving that same proposal;
- the proposal must use a pre-existing gate revision or obtain independent external evidence.

Determinism fixtures:

- same normalized inputs yield the same proposal ID and content;
- path separator and record order normalization do not change identity;
- changed evidence window changes identity;
- stale policy hash prevents closure;
- unauthorized closer fails;
- post-change observation cannot rewrite the baseline;
- a planned-only signal cannot satisfy a policy;
- self-modification routes to Class C review.

2.2.0 release train:

1. freeze proposal and decision formats;
2. bump version owner and render projections;
3. run all prior regression suites plus evolution fixtures;
4. execute shadow mode where proposals are generated but cannot create patches;
5. audit false positives, orphan coverage, and authority routing;
6. execute one Class A and one Class B end-to-end rehearsal without merge automation;
7. verify emergency disable and rollback;
8. publish governance, privacy, and operator guides;
9. tag v2.2.0 from the approved RC commit.

### Phase 8 — Earliest time-based unlock (v2.3 or later)

No self-adjusting policy or merge automation is considered before all of the following are true:

- at least 90 days of representative telemetry exists;
- unmeasured-outcome rate is within an approved bound;
- defect and revert rates are stable;
- authority and succession have been exercised;
- a red-team review covers gaming and evidence poisoning;
- a Class C proposal approves the exact additional authority;
- rollback is independently demonstrated.

Time elapsed alone does not unlock anything.

---

## 7. Migration invariants

All project migration work obeys these invariants:

1. detect before write;
2. classify the source revision explicitly;
3. snapshot relevant pre-change state and hashes;
4. distinguish untouched generated files from customized files;
5. preserve user-authored policy and local instructions;
6. do not infer that a recognized revision is current;
7. never emit a new adapter artifact solely because it exists in the registry;
8. show the FilePlan before destructive replacement or removal;
9. keep rollback instructions alongside migration evidence;
10. verify the post-migration project with the new checker and relevant host smoke tests.

No phase may weaken these invariants to accelerate adoption.

---

## 8. Governance classes

### Class A — low-risk, reversible tuning

Examples:

- wording clarification with no semantic change;
- adding a non-authoritative example;
- tuning a threshold inside a pre-approved safe range.

Requirements:

- deterministic proposal;
- affected-owner gate;
- one authorized reviewer;
- rollback note.

### Class B — behavioral or evidence change

Examples:

- Domain Pack workflow/gate/reviewer changes;
- Host Adapter behavior;
- telemetry producer/schema-compatible changes;
- benchmark and eval corpus changes;
- new active or proxy signals.

Requirements:

- pre-change baseline;
- independent behavioral evidence;
- domain/adapter owner review;
- observation window;
- no same-proposal self-certification.

### Class C — contract, authority, or enforcement change

Examples:

- canonical `AGENTS.md` semantics;
- registry format or bootstrap;
- project contract revision rules;
- governance policies or authority descriptors;
- core registry, contract-check, risk, or evolution code that can weaken enforcement;
- `kit-evolve` self-modification;
- automatic merge authority;
- early removal of a migration-source revision.

Requirements:

- immutable baseline and input hashes;
- explicit named authority;
- at least two independent reviews or the approved equivalent;
- full cross-component regression;
- rollback rehearsal;
- effective-from-run boundary;
- decision record that includes policy revision and hash.

Generated artifacts inherit the class of their source owner.

---

## 9. Test and evidence strategy

### 9.1 Layered gates

Every phase runs the smallest relevant gate first, then the full suite before completion.

```text
format/static checks
  → registry and projection unit tests
  → contract and migration fixtures
  → shell syntax and cross-platform materialization
  → skill eval positive and negative cases
  → host conformance smoke
  → full repository validation
  → release-candidate evidence bundle
```

### 9.2 Extension proof

The extension claim is not proven by comparing a registry set to a hardcoded set. It is proven only when a synthetic component passes through all relevant generic consumers.

For a Host Adapter, the fixture must cover:

```text
descriptor → Registry Catalog → projection → scaffold manifest
→ greenfield materialization → contract checker → retirement
```

For a Domain Pack, the fixture must cover:

```text
descriptor → registry validation → trigger rendering
→ six-slot composition → execution eval → evolution ownership
```

No production Python or shell file may be edited for the synthetic component.

### 9.3 Evidence bundle

Each phase archives:

- commit and registry revisions;
- commands and exit codes;
- fixture names and results;
- generated projection check result;
- fact-check sources and dates where relevant;
- known limitations;
- reviewer and decision references;
- rollback notes.

A prose statement that “tests pass” is insufficient.

### 9.4 Fact-check discipline

Host claims are verified against official primary documentation at implementation time and again before the affected release RC. The descriptor records the verification date and capability assumption. If official behavior is ambiguous, the adapter remains `repo_only` or documents a named degradation; the plan does not invent host guarantees.

---

## 10. Known risks and controls

| Risk | Consequence | Control |
|---|---|---|
| legacy revision treated as current | stale projects appear compliant | explicit green vs migration-source state and nonzero diagnostic |
| registry becomes a god module | changes couple unrelated behavior | narrow Catalog interface; separate Projection Module; contract tests |
| generated file becomes second authority | descriptor and runtime drift | marker, byte-exact check, owner resolution |
| Bash manifest allows injection | arbitrary execution or bad paths | closed actions, strict path grammar, no `eval`, cross-platform red fixtures |
| registry entry emits files too early | surprise project mutation | adapter lifecycle and activation fixtures |
| trigger exists but does not load pack | fake Domain Pack composition | standardized renderer plus behavioral file-load eval |
| old template recognition depends on Git | packaged migration cannot classify | shipped immutable revision snapshot metadata |
| task ID minted at completion | early gate/review data cannot join | start/append/finish telemetry lifecycle |
| concurrent JSONL writes corrupt history | evidence loss | atomic record append, locking, recovery fixtures |
| miner games acceptance rate | many easy, low-value proposals | outcome metrics; acceptance rate diagnostic only |
| miner creates its own passing eval | self-certification | evals Class B+, temporal independence rule |
| new product path escapes governance | unreviewed evolution surface | governed roots and orphan-path diagnostic |
| future registry format partially loads | inconsistent behavior | bootstrap check before child registries; atomic upgrade diagnostic |
| release feature works but cannot ship safely | incomplete migration/rollback | release train for every program version |

---

## 11. Explicitly out of scope

The program does not include:

- autonomous merge in v2.0–v2.2;
- dynamic network installation of untrusted Domain Packs;
- a general plugin marketplace;
- a universal ontology for every profession;
- raw prompt or secret collection in default telemetry;
- exact token counts when the host cannot attribute them safely;
- rewriting all historical scorecards into telemetry v3;
- supporting every editor/agent at v2.0;
- automatic removal of customized brownfield files;
- JSON Schema claims without adopting and governing a real JSON Schema implementation.

---

## 12. Documentation deliverables

By v2.0:

- open-platform architecture overview;
- Domain Pack author guide;
- Host Adapter author and conformance guide;
- registry format and bootstrap reference;
- evolution governance/manual proposal guide;
- v1.16 → v2 migration guide;
- generated-project contract reference;
- adapter support/degradation matrix;
- greenfield and brownfield troubleshooting.

By v2.1:

- telemetry v3 schema and event lifecycle;
- privacy and retention guidance;
- token attribution limitations;
- concurrency and recovery behavior.

By v2.2:

- `kit-evolve` operator guide;
- proposal/decision format reference;
- governance-class and authority guide;
- evidence poisoning and gaming guidance;
- emergency disable and rollback guide.

---

## 13. Program Definition of Done

### 13.1 v2.0.0 DoD

- [ ] v1.17.1 maintenance release exists and both long-lived branches start from it.
- [ ] normative registry, evolution, Domain Pack, and Host Adapter contracts are approved.
- [ ] registry bootstrap rejects malformed, old/unknown, future, and mixed formats deterministically.
- [ ] the Registry Catalog owns component inventory.
- [ ] Projection Module output is deterministic and byte-exact checked.
- [ ] greenfield Bash initialization consumes the generated sanitized manifest.
- [ ] a synthetic Host Adapter requires no validator or shell edit.
- [ ] a synthetic non-software Domain Pack composes through the work-loop engine.
- [ ] software development is a six-slot Domain Pack.
- [ ] `build-loop` is a generated thin trigger and behaviorally loads its pack.
- [ ] `AGENTS.md` remains the only generated-project policy owner.
- [ ] initial Host Adapters are thin and lifecycle-governed.
- [ ] v1.16 is recognized only as a migration source, never green.
- [ ] clean and customized migration fixtures pass without silent mutation.
- [ ] governed roots have no orphan product paths.
- [ ] full release train, rollback, RC evidence, and tag complete.

### 13.2 v2.1.0 DoD

- [ ] telemetry v3 contract is approved.
- [ ] task IDs begin before early workflow events.
- [ ] handoff and delegated work preserve linkage.
- [ ] event history is append-only under normal, interrupted, and concurrent writes.
- [ ] token attribution is exact or explicitly unknown.
- [ ] active evolution signals have real producers.
- [ ] privacy/retention documentation and disable behavior are tested.
- [ ] v2.1 release train and tag complete.

### 13.3 v2.2.0 DoD

- [ ] deterministic proposal and decision formats are frozen.
- [ ] manual and automated paths use the same evolution policy.
- [ ] authority succession and stale-policy rejection are tested.
- [ ] governed universe coverage has no unexplained orphan.
- [ ] evaluation artifacts cannot self-certify their creating proposal.
- [ ] outcome reporting includes defect, revert, unmeasured, and realized-effect rates.
- [ ] shadow mode and end-to-end Class A/B rehearsals pass.
- [ ] no autonomous merge authority exists.
- [ ] v2.2 release train and tag complete.

---

## 14. Approval checklist

Implementation must not begin until maintainers answer these questions explicitly:

1. Is `dat-kit 2.0` the only green project contract revision for the v2 checker?
2. Is `dat-kit 1.16.0` accepted as a migration source with a mandatory nonzero diagnostic?
3. Is the generated sanitized TSV manifest approved as the Bash-only greenfield bridge from registry to scaffold?
4. Are `repo_only`, `migration_ready`, `scaffold_active`, and `retired` the approved adapter artifact states?
5. Are the six Domain Pack slots normative and exhaustive for v2?
6. Are generated triggers and manifests committed projections checked byte-for-byte?
7. Is acceptance rate explicitly non-optimizing for `kit-evolve`?
8. Are benchmark/eval changes at least Class B and enforcement changes that can weaken governance Class C?
9. Is the same-proposal self-certification ban approved?
10. Is v1.17.1 mandatory before `release/1.x` and v2 branch creation?
11. Are telemetry v3 and `kit-evolve` correctly deferred to v2.1 and v2.2?
12. Are v2.1 and v2.2 required to pass full RC/rollback/tag release trains?

Record the answers in an approved issue or decision record and link it from this plan.

---

## 15. Review history and fact-check footer

### Review basis

This v6 plan was produced by reviewing v5 against:

- the current maintainer workflow and working rules;
- the current registry-free hardcoding in scaffold and contract-check paths;
- current scorecard append/enrichment behavior;
- existing build-loop and scorecard skill flow;
- current validation and skill-eval coverage;
- the stated five open-platform goals;
- an independent fresh-eyes architecture pass.

### Material changes from v5

1. replaces ambiguous “supported old revision” language with a compatibility state machine;
2. moves all normative component contracts before registry implementation;
3. adds a named Projection Module and executable render/check commands;
4. adds a generated sanitized scaffold manifest so new hosts do not require shell edits;
5. adds Registry Catalog bootstrap/version rules and atomic mixed-upgrade failure;
6. adds adapter artifact lifecycle gates;
7. makes the scorecard maintenance fix mandatory and bases both branches on v1.17.1;
8. moves task-ID creation to workflow start and defines telemetry lifecycle commands;
9. defines governed roots, signals, authorities, policies, and an executable manual evolution path;
10. makes acceptance rate diagnostic rather than an optimization target;
11. makes eval/corpus temporal independence explicit;
12. adds full v2.1 and v2.2 release trains.

### External host facts to re-verify during implementation

Official documentation reviewed while preparing the plan indicates:

- Claude Code plugins are copied to a cache; plugin paths must remain inside the plugin root, and custom skill directories are supported.
- Gemini CLI extensions use `gemini-extension.json` at the extension root and support context-file and skill declarations.
- Cursor CLI reads `AGENTS.md` and `CLAUDE.md` in addition to Cursor rules.
- Cursor documents `.cursorrules` as supported but deprecated.

These facts justify keeping adapters thin and host-native, but they are not permanent guarantees. Each adapter descriptor must record a fresh official-doc verification date before activation and before the affected release candidate.

### Plan integrity

- This file is a standalone replacement plan; it does not modify the downloaded v5 source.
- A phase is complete only when its evidence and exit criteria exist, not when its code is merely drafted.
- Any factual assumption discovered to be false must update the relevant contract and decision record before dependent work continues.
