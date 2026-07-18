# dat-kit Open Platform Program — Plan v4

**Status:** DRAFT — awaiting maintainer approval (plan gate per root `AGENTS.md`)  
**Base:** `v1.17.0` at current `origin/master`  
**Program:** `v2.0.0` platform kernel → `v2.1.0` telemetry → `v2.2.0` self-evolution  
**Plan revision:** v4 (2026-07-17)  
**Supersedes after approval:** downloaded `PLAN-v2.0.0-open-platform.md` revision v3

This document is a plan, not execution authority. Approval authorizes the
phases and release boundaries below; it does not waive per-phase evidence,
review, migration, security, or release gates.

## 0. Why v4 exists

v3 established the right five goals but left four architectural blockers:

1. `build-loop` was called domain-neutral while still owning software-specific
   planning, data/API/security, Git, demo, and reviewer behavior.
2. Three registry files were proposed without a deep Registry Module; pointer,
   runtime, scaffold, and manifest knowledge would still be duplicated across
   Python, shell, CI, and docs.
3. Telemetry promised per-task token I/O although the current collector sees
   Claude sessions, not task boundaries, and rewrites append-only history.
4. `kit-evolve` was defined as prose without a deterministic, safe, testable
   mining implementation.

v4 keeps the vision, closes those blockers, moves migration before the
structural release candidate, and replaces one overloaded release with a
three-release program. Only the platform one-way door burns `2.0.0`;
telemetry and evolution ship when their own evidence is ready.

### Review history

- v1 → independent general review: REVISE 6/10.
- v2 → independent evolution-coverage review: REVISE; most component classes
  had no proposal path.
- v3 → Codex maintainer review plus independent fresh-eyes architecture pass:
  REVISE; registry depth, Domain Pack Interface, task attribution, migration
  ordering, and evolution implementation were not executable.
- v4 → resolves those findings through a six-slot Domain Pack, one registry
  Interface, migration-first sequencing, immutable telemetry, deterministic
  proposal mining, and release-specific definitions of done.

## 1. Owner goals and precise claims

| # | Goal | v4 claim |
|---|---|---|
| 1 | Multi-profession | A profession is a first-class Domain Pack with a complete Interface and a generated/thin host entrypoint. Software development uses the same Interface as later professions. |
| 2 | Multi-host without dat-kit policy conflict | `AGENTS.md` remains the only substantive dat-kit project contract. Adapters add no second dat-kit policy and known competing project instruction sources fail closed. User/managed host rules remain an explicit external limitation. |
| 3 | Open-ended growth | A new host or domain is registered through data plus owned files. Generic validators, scaffold, migration, and docs code do not change. Synthetic extension fixtures prove this property. |
| 4 | Optimize I/O over time | Telemetry records immutable, provenance-bearing task/gate/review events. Token usage is called task-scoped only when a verified collector observes a task boundary; session-only data is labelled session-scoped. |
| 5 | Learn from history | A deterministic read-only miner can propose against every governed Module class. Risk controls who may close a gate; unknown risk fails closed. No proposal may weaken and immediately use its own gate. |

“Conflict-free” never means dat-kit can neutralize arbitrary user,
organization, or third-party host instructions. It means dat-kit itself
introduces no substantive duplicate policy, reserves only named adapter files,
preserves brownfield content, and reports known conflicts before mutation.

## 2. Reversal of the 2026-07-14 layout freeze

This plan reopens the decision in `docs/domains.md` and `docs/loops.md` that the
flat `skills/*` layout was permanent/final.

The former decision was correct for the earlier goal: moving files solely to
make the tree look cleaner had no user benefit and would break a hardcoded
validator. The current goal is different. With multiple professions, hosts,
telemetry sources, and evolution paths, keeping software-dev fused into
`build-loop` makes the Domain Pack Interface false and forces each extension to
edit implementation code.

Phase 0 records the reversal in `docs/decisions/0001-open-platform.md` with:

- owner and date;
- evidence that changed the decision;
- accepted migration cost;
- conditions under which the decision should be revisited;
- explicit prohibition on “final” or “permanent” architecture wording.

Generated-project `templates/common/spec/08-decisions.md` is not a maintainer
decision source.

## 3. Architectural design

### 3.1 Deep work-loop Module

The shared work loop becomes a deep Module with a small Interface:

```text
run(task, domain_id, loop_mode, user_authority)
```

Its implementation owns only invariant orchestration:

```text
clarify → decompose → ground → execute → verify → report → harvest
```

It does not own software entities, API lenses, Git deliverables, citation
rules, reviewer names, or domain-specific gates. Those belong to a Domain Pack.

The deletion test must pass: if the work-loop Module disappeared,
orchestration complexity would have to be duplicated across at least
software-dev and knowledge-work. If deletion only requires inlining a few
references into one caller, the Module is still shallow and cutover stops.

### 3.2 Six-slot Domain Pack Interface

The existing five slots cannot support a thin trigger because the domain
execution playbook currently lives in each `SKILL.md`. v4 adds `workflow.md`:

| Slot | Required artifact | Responsibility |
|---|---|---|
| Workflow | `workflow.md` | Domain meaning of clarify, decompose, execute, report, and harvest; required-input and missing-information behavior. |
| Ground truth | `ground-truth.md` | Sources that must be consulted before acting; trust and currency rules. |
| Gates | `gates.md` | Stable gate IDs, criteria, worked pass/fail cases, gaming lines, automation status, and loop ceiling. |
| Reviewers | `reviewers.md` | Independent reviewer roles, authority, evidence expected, and verdict contract. |
| Deliverables | `deliverables/` | One or more output templates/examples. |
| Loop profile | `loop-profile.md` | Allowed Turn/Goal/Time/Proactive modes and why the ceiling is earned. |

Every domain descriptor declares a stable domain ID, pack location, trigger
metadata, gate-authority reference, loop ceiling, evolution profile, and
contract revision.

Gate authority is a typed role or opaque stable reference, not mandatory
public personal information. It defines succession when the original
practitioner is unavailable. The proposer and gate closer may not be the same
actor.

### 3.3 Host-facing skill Adapters

`skills/` remains the host discovery location where required. It is not called
“triggers only” because utility skills may legitimately keep implementation
beside `SKILL.md`.

Domain entrypoints are thin Adapters. They select a domain ID, resolve the
work-loop and pack, and preserve current trigger names/descriptions:

- `skills/build-loop/SKILL.md` remains the compatibility entrypoint for
  `software-dev`;
- `skills/knowledge-work/SKILL.md` selects `knowledge-work`;
- future domain entrypoints are deterministic projections from domain
  descriptors, not a second hand-maintained trigger source.

### 3.4 One Registry Module, not multiple inventories

Registry JSON is implementation data behind one stdlib-only Registry Module.
The Module owns loading, schema validation, path safety, referential integrity,
case correctness, duplicate detection, resolution, and projections.

Conceptual Interface:

```text
load_platform(root) -> PlatformCatalog
catalog.domain(id)
catalog.adapter(id, surface)
catalog.project_pointers()
catalog.version_targets()
catalog.evolution_policy(path)
```

Consumers may not parse registry JSON independently:

- `scripts/validate.py` imports the Module;
- `scripts/contract_check.py` remains the public project-contract,
  brownfield, migration, and evidence Interface;
- `scripts/init.sh` queries `contract_check.py`; it owns no pointer inventory;
- CI invokes the same Interfaces and owns no component counts;
- README/domain/capability tables are checked/generated projections;
- tests inject a root and exercise the real Module.

The maintainer contract is amended atomically in Phase 1 to describe
`registry.py` plus registry data as implementation behind the public
`contract_check.py` Interface. No temporary third inventory is permitted.

### 3.5 Registry files and schemas

```text
registry/
  platform.json
  domains.json
  adapters.json
  evolution.json
  schemas/
    platform.schema.json
    domains.schema.json
    adapters.schema.json
    evolution.schema.json
```

`platform.json` owns package version, canonical project-contract revision,
supported contract revisions, and registry schema revisions. Package version
and project-contract revision remain independent.

`domains.json` owns Domain Pack descriptors. A domain inherits its evolution
profile through its descriptor; adding one does not require a second
per-domain row in another registry.

`adapters.json` owns one descriptor per host/surface with:

- host and surface IDs plus verified/minimum version;
- adoption mode: `native`, `pointer`, or `manual`;
- repo artifacts and host-mandated physical locations;
- generated-project pointers/templates;
- at most one session bootstrap per surface, distinct from project pointers;
- manifest paths and optional version JSON pointers;
- capabilities and limitations;
- smoke-test procedure and evidence type;
- evolution profile.

There is no hardcoded number of version-bearing manifests. The Registry Module
derives version targets from descriptors. Redundant version fields are removed
where a host does not require them.

`evolution.json` owns typed policy by governed Module kind:

- stable `module_kind`;
- non-overlapping path selectors;
- typed signal IDs;
- minimum semantic proposal class;
- typed gate closer role;
- required proof and review chain.

Every governed product path must match exactly one policy row. Zero matches and
multiple matches both fail. Historical plans, handoffs, fixtures, and evidence
are explicitly included or excluded by schema, not hidden exceptions.

### 3.6 Host Adapter Contract

The contract distinguishes four things v3 mixed together:

1. host-mandated repo artifacts/manifests;
2. project pointers loaded by a host;
3. optional session bootstrap behavior;
4. documentation/capability projections.

An Adapter may contain manifests, pointers, install instructions, smoke tests,
and limitations. It may not contain substantive shared policy.

Conformance has two levels:

- static: schema parses, version targets resolve, reserved pointers contain no
  policy, paths are safe, and `AGENTS.md` remains the sole dat-kit contract;
- behavioral: install on a declared host/surface/version, start a fresh
  session, verify contract adoption, invoke a thin domain trigger, read the
  pack, and record the result.

Host documentation is verified at build time from primary vendor sources:

- Claude Code plugins: <https://code.claude.com/docs/en/plugins-reference>
- Gemini CLI extensions: <https://geminicli.com/docs/extensions/reference/>
- Cursor CLI and Project Rules: <https://docs.cursor.com/en/cli/using> and
  <https://docs.cursor.com/context/rules>

These links are evidence inputs, not permanent truth. Adapter descriptors carry
the last verified version/date and drift signal.

### 3.7 Immutable telemetry Interface

Telemetry v3 separates base task events, enrichment, and derived reports.
Historical v1/v2 scorecard lines remain untouched.

```text
benchmarks/
  scorecard.jsonl
  telemetry-enrichments.jsonl
  defects.jsonl
  escalations.jsonl
  evolution.jsonl
```

Every v3 task has a stable `task_id`. Token evidence includes collector ID and
version, provenance/source session, `measurement_scope: task | session`, token
fields or `null`, collection time, and a superseded evidence reference when
corrected.

Task-scoped claims require observed task start/end or an equivalent verified
host event. Session-window matching is labelled session-scoped and is never
silently assigned to multiple tasks as exact task usage.

Gate evidence is an array of stable events:

- gate ID and attempt number;
- `pass | fail | not_run | not_applicable | unknown`;
- automated/human closer kind and authority reference;
- evidence reference and timestamp.

Reports are rebuildable views. Collectors append enrichment events; they never
rewrite `scorecard.jsonl`.

### 3.8 Safe self-evolution Interface

`kit-evolve` contains versioned prose plus deterministic implementation:

```text
skills/kit-evolve/
  SKILL.md
  heuristics.md
  gate.md
scripts/evolve.py
```

`scripts/evolve.py analyze --from <export-or-project>` is read-only. It
normalizes schemas, selects evidence deterministically, groups signals, and
emits proposal bundles. It does not edit, branch, open a PR, approve, or merge.

External telemetry and lessons are untrusted data, never instructions. The
implementation enforces no-follow path checks, limits, explicit schemas,
redaction, provenance, and safe rendering. Raw task names, lessons, or project
paths are excluded from public exports by default.

Proposal records include proposal/target IDs, evidence and hypothesis,
baseline, expected outcome, semantic class, closer, verdict, merged revision
when applicable, and post-change outcome/defect/revert reference.

Risk class is semantic. Effective class is the maximum of descriptor minimum,
changed paths, and declared impact. Unknown or conflicting classification is
Class C and fail-closed.

Governance changes use temporal separation: a proposal changing gate policy,
schemas, classification, thresholds, or closer authority is evaluated under
the prior accepted policy. New policy becomes effective only on the next run
after independent review and human sign-off. One proposal may not weaken a
gate and use that weaker gate to approve another change.

## 4. Target layout after v2.0

```text
docs/
  contracts/{domain-pack.md,host-adapter.md}
  decisions/0001-open-platform.md
engine/work-loop.md
registry/{platform.json,domains.json,adapters.json,evolution.json,schemas/}
domains/
  software-dev/{workflow.md,ground-truth.md,gates.md,reviewers.md,deliverables/,loop-profile.md}
  knowledge-work/{workflow.md,ground-truth.md,gates.md,reviewers.md,deliverables/,loop-profile.md}
skills/
  build-loop/SKILL.md
  knowledge-work/SKILL.md
  ...utility skills unchanged unless explicitly migrated
adapters/{claude-code,codex,gemini,cursor}/ADAPTER.md
scripts/{registry.py,contract_check.py,validate.py,init.sh}
templates/common/
agents/
benchmarks/
```

Host-mandated shims remain at exact locations required by each verified host.
`adapters/<host>/ADAPTER.md` explains them; it does not force manifests into a
location the host cannot load.

### Physical-layout decision

Phase 0 chooses physical layout from live evidence:

- **Option A:** installed Claude and Codex plugins reliably resolve pack files
  outside `skills/`; use the layout above.
- **Option B:** at least one host cannot; keep pack content physically beside
  the domain entrypoint but preserve the six-slot Interface, descriptors, IDs,
  ownership, and conformance suite.

Option B changes implementation location only. It does not remove the logical
domains catalog or re-fuse software policy into the shared engine.

## 5. Execution phases

Every phase is dependency-ordered and commit-sized. A phase does not inherit a
later phase's DoD.

### Phase 0 — Baseline, decisions, escape hatch, host spikes

**Work**

1. Reconcile release truth: `v1.17.0` exists at current `origin/master`;
   correct stale README “release pending” language.
2. Create protected `release/1.x` from tag `v1.17.0`. Do not create a moving
   tag named `release/1.x`.
3. Demonstrate Claude/Codex install and update routes pinned to that branch.
4. On fresh Claude and Codex sessions, make a thin experimental skill resolve
   and read a test file outside `skills/`.
5. Record plugin-root resolution, cached layout, fresh-session requirements,
   and failure behavior.
6. Verify Gemini distribution shape and Cursor surfaces against current docs.
7. Write the maintainer decision with revisit conditions.

**DoD**

- 1.x route works on both current supported hosts;
- Option A/B is selected without changing logical Interface;
- decision artifact is reviewable;
- baseline and a real CI run are green;
- no structural move has occurred.

### Phase 1 — Registry Module and schemas, behavior-preserving

**Work**

1. Add versioned schemas/descriptors for current state only.
2. Implement `scripts/registry.py` with injected-root support.
3. Refactor `validate.py` into parameterized checks and a thin CLI.
4. Remove hidden global-`ROOT` reads from root-accepting contract operations.
5. Make `contract_check.py` query registry for project pointers, runtime enums,
   version targets, and templates.
6. Make `init.sh` consume only `contract_check.py` outputs.
7. Replace CI/template counts with semantic inventory checks.
8. Generate or exactly check docs projections.
9. Amend maintainer ownership docs atomically.
10. Add Windows CI for Python validators/tests; retain shell gates on Linux.

**Red-before-green fixtures**

- missing/wrong-cased/absolute/traversal/symlink paths;
- duplicate IDs and dangling references;
- derived manifest version mismatch;
- orphaned/overlapping evolution selectors;
- injected root different from repository root;
- synthetic host and domain added only through descriptors plus owned files.

Synthetic fixtures exercise validation, pointer planning, and scaffold
inventory. Comparing dictionaries is insufficient.

**DoD**

- deleting a descriptor fails with a named diagnostic;
- adding a complete synthetic host/domain changes no Python, shell, CI, or docs
  inventory implementation;
- v1.17 behavior remains intentionally compatible;
- Windows pass and injected-fail output are safe;
- a real CI run is green.

### Phase 2 — Contracts and additive repo-side host adapters

**Work**

1. Write six-slot Domain Pack and Host Adapter contracts.
2. Register current Claude/Codex behavior.
3. Add Gemini/Cursor descriptors and repo-side artifacts through registry.
4. Put each manifest at the location proven by the live distribution spike.
5. Derive version fields from descriptor JSON pointers; encode no fixed count.
6. Extend the personal-info gate to new public config/text suffixes.

For every supported surface record exact version, discovery success,
native/pointer/manual AGENTS adoption, thin-trigger invocation, pack read,
capabilities, limitations, conflict sources, and fresh-session evidence.

**DoD**

- Gemini/Cursor land without validator/scaffold implementation edits;
- claims match live smoke and primary docs;
- adapters contain no shared policy;
- unsupported surfaces are labelled honestly;
- a real CI run is green.

### Phase 3 — Migration-first project contract `dat-kit 2.0`

No structural release candidate may precede this phase.

**Work**

1. Add `dat-kit 2.0` as canonical while retaining `dat-kit 1.16.0` during the
   supported migration window.
2. Add typed actions and bump public migration schema when required:
   `ADD_FROM_TEMPLATE`, `REPLACE_POINTER`, `RETIRE_LEGACY`, `MERGE_REQUIRED`,
   and existing unsafe/blocking actions.
3. Plan every adapter-owned project addition/replacement from descriptors.
4. Treat substantive existing Gemini/Cursor/reserved files as
   preservation-first conflicts; never overwrite.
5. Preserve project-owned policy semantically in AGENTS/working-rules.
6. Add greenfield templates only after the v1→v2 planner supports them.

**Required fixtures**

- clean v1.16 project;
- customized pointer and competing AGENTS;
- substantive Gemini/Cursor legacy rules;
- missing new pointer and partial v2 install;
- unsafe path/symlink race;
- mixed revisions;
- exact no-mutation hashes around planner runs.

**DoD**

- a real v1 project receives a deterministic read-only plan;
- additions, replacements, merges, and unresolved items are named;
- `init.sh --here` remains inspect-before-mutate and fail-closed;
- both supported revisions behave as documented;
- a real CI run is green.

### Phase 4 — Work-loop and Domain Pack structural cutover

**Work**

1. Map all current behavior:
   - invariant orchestration → `engine/work-loop.md`;
   - software planning/data/API/security/build/Git/demo → software workflow;
   - knowledge-work A→G → knowledge workflow;
   - gates/reviewers/templates → named pack slots.
2. Extract software-dev into six slots.
3. Move/map knowledge-work to the same Interface.
4. Rewrite current domain skills as thin Adapters with compatible triggers.
5. Rewrite domain-builder to create descriptor, six slots, deterministic
   trigger, authority reference, and inherited evolution profile.
6. Replace sentence-marker pack detection with registry/schema conformance.
7. Update project-init, fixtures, projections, and non-historical live refs.

**Behavioral proof**

- before/after build-loop normal, autopilot, delegated, security, recovery, and
  harvest paths;
- before/after knowledge report and fact-check cases;
- positive/collision/negative triggers;
- installed Claude/Codex pack reads;
- end-to-end dry-run domain-builder pack;
- same conformance under physical Option A or B.

**DoD**

- shared engine contains no domain-specific gate/reviewer policy;
- both domains satisfy the same six slots;
- deletion test proves engine Depth;
- dry-run domain needs no validator edit;
- v1 migration remains available;
- fresh-session host smokes and real CI are green.

### Phase 5 — v2.0 release train

1. `2.0.0-alpha.1` after Phase 4 static/behavioral checks.
2. Rehearse migration on at least one real v1.16-contract project.
3. Run fresh install/reinstall smokes on supported surfaces.
4. `2.0.0-rc.1` only after migration and 1.x escape route pass.
5. Observe RC, review defects, then release/tag `2.0.0`.

**v2.0 DoD**

- goals 1–3 proven by synthetic extensions;
- software-dev conforms to six-slot Interface;
- Registry Module is sole inventory implementation;
- AGENTS is sole substantive dat-kit project contract;
- v1→v2 migration is preservation-first;
- `release/1.x` still installs post-release;
- version targets are derived, not counted;
- real CI and host smoke evidence are recorded.

Telemetry v3 and kit-evolve are not v2.0 blockers. Coverage rows use honest
current signals such as CI, lessons, evals, user reports, and conformance
failures; they do not claim future collectors exist.

### Phase 6 — v2.1 immutable telemetry

**Work**

1. Write telemetry contract before implementation.
2. Add stable task/domain/gate/reviewer/host/collector IDs.
3. Keep v1/v2 records untouched; add strict v3 records.
4. Replace token rewrite with append-only enrichment.
5. Label measurement scope/provenance.
6. Add gate attempts/verdicts/evidence, including human-run gates.
7. Add escaped-defect and escalation schemas.
8. Add privacy-preserving project export; raw text requires explicit opt-in.
9. Build reports from immutable events.

**Proof**

- rewrite-detection red fixture;
- two tasks in one session do not share an exact full-session total;
- mixed schema and correction/out-of-order fixtures;
- unknown collectors remain null;
- export redaction/path/symlink tests;
- one real software-dev and knowledge-work v3 task.

**v2.1 DoD**

- reports rebuild from immutable history;
- token scope is honest;
- gates have stable IDs and evidence states;
- real domain runs distinguish human/automated verdicts;
- raw external content is excluded by default;
- real CI is green.

### Phase 7 — v2.2 kit-evolve Goal loop

**Work**

1. Add versioned skill, heuristics, and gate artifacts.
2. Implement/test read-only `scripts/evolve.py analyze`.
3. Resolve signals/targets through registry.
4. Map every governed path exactly once.
5. Emit evidence-backed proposal bundles.
6. Route accepted proposals through ordinary plan/build/review gates; miner
   never grades or merges itself.
7. Append accepted/rejected/merged/reverted/post-window outcomes.
8. Enforce semantic max risk and temporal separation.

**Security/gaming fixtures**

- prompt-injection lessons;
- traversal/symlink/oversized/malformed exports;
- empty/mixed/duplicate evidence;
- threshold edges;
- understated risk and self-gate changes;
- overlapping selectors;
- trivial eval change that cannot prove stated outcome.

**v2.2 DoD**

- a real historical signal yields a non-trivial proposal;
- independent gate accepts or rejects it with reasons;
- one proposal uses a redacted real-project export;
- all governed Module kinds are reachable;
- forced merge is not a release requirement;
- first legitimate merged Class B is a success metric, not manufactured DoD;
- real CI is green.

### Phase 8 — Time loop unlock, earliest v2.3

Time remains locked until at least five real proposals complete review,
false-positive/acceptance evidence exists, the gaming line is exercised,
maintainer signs off, execution is idempotent/duplicate-suppressing, and GitHub
permissions/external writes are explicitly authorized and audited.

The Time runner may open proposal branches/PRs. It does not auto-merge. Class C
still requires human sign-off. Proactive remains notify-only.

## 6. Shared gates and evidence

Every implementation phase runs, as applicable:

```text
python scripts/validate.py
pytest scripts/tests
bash -n scripts/init.sh
shellcheck scripts/init.sh
git diff --check
```

Additional rules:

- Changed gates prove red-before-green with isolated fixtures.
- Non-ASCII Python output proves pass and fail on maintainer Windows console.
- Registry, migration, public-input, export, path, or external-write phases
  require security review.
- Review order is plan audit → implementation → QA → code review → conditional
  security review → regression QA.
- A workflow file is not CI evidence; executable/validator/scaffold/manifest
  changes record a real Actions run.
- Plugin smoke uses fresh sessions after install/update.
- Evidence/benchmarks are append-only; corrections reference superseded data.
- User-owned and unrelated worktree changes are preserved.

Evidence records state phase/release, Git revision, host/surface/version, exact
gate counts, deliberate red diagnostic when applicable, reviewer verdicts,
security review or skip reason, real CI ID/URL, deferrals, and remaining
commands.

## 7. Migration invariants

1. Inspect before mutation; planner never edits target.
2. Fail closed on competing policy, unsafe paths, incompatible partial install.
3. Never byte-replace project-owned AGENTS or working-rules.
4. Replace reserved pointers only after inventory/preservation and approval.
5. Do not promote host-specific routing into shared policy.
6. Package and project-contract revisions remain independent.
7. During transition, recognize old/new revisions and produce actionable plans.
8. New pointer types get typed migration semantics before scaffold emits them.
9. Version public migration-output schema changes.
10. Recheck `release/1.x` after v2.0 release.

## 8. Evolution governance

| Class | Typical impact | Minimum gate |
|---|---|---|
| A | Non-policy docs projection, examples, eval additions, deliverable formatting | Standard build-loop, validation, independent review. |
| B | Skill/workflow behavior, Domain Pack content, scripts, adapters, hooks, CI, telemetry collectors, benchmark schemas | Class A plus red-before-green behavioral fixture/eval; security review when relevant. |
| C | Canonical contracts, registry/risk schemas, gate/authority policy, capability ladder, loop ceiling, reviewer model policy, kit-evolve governance | Class B plus authorized human sign-off; prior policy evaluates change. |

Markdown changing policy is not Class A merely because it is documentation.
Unknown impact is Class C.

Coverage means the governed path universe is declared; each path resolves
exactly once; signals and closers resolve; every target is reachable; no row is
“unreachable”; and future signals are distinct from active signals.

“No signal yet” is not a final row. A component may use an honest generic proxy
such as user reports plus lessons while a dedicated collector is planned, with
that limitation visible in reports.

## 9. Risks and kill-switches

| Risk | Prevention | Kill-switch |
|---|---|---|
| Thin trigger cannot read pack | Phase 0 live spike; same suite for layouts | Select physical Option B without changing Interface. |
| Registry stays shallow | One Module; consumers cannot parse JSON; synthetic fixtures | Stop before Phase 2 if extension changes implementation code. |
| Work-loop remains software-specific | Full ownership map and deletion test | Keep v1 layout until both domains pass Interface. |
| Adapter drifts | Versioned surface descriptors, docs check, live smoke | Mark surface unsupported/degraded. |
| Migration loses policy | Read-only planner, preservation, hashes | Block migration; use `release/1.x`. |
| Telemetry invents precision | Scope/provenance and null defaults | Report session/unknown; never estimate. |
| Telemetry leaks data | Redacted opt-in export and limits | Reject export; alter no source data. |
| Miner follows malicious history | Inputs are data; deterministic parser | Reject bundle and log diagnostic. |
| Miner weakens its gate | Max class, prior-policy evaluation, separation | Block; require Class C human review. |
| DoD incentivizes fake improvement | Proposal-quality proof; no forced merge | Release with reviewed rejection. |
| Scope expands | Separate release DoDs | Ship only completed release. |

## 10. Out of scope

- New profession packs; v2.0 enables them, real practitioners author later.
- Toolkit parity on every host.
- Unverified host-specific model routing.
- Rewriting all utility skills for tree uniformity.
- Time/Proactive work-domain runners in v2.0–v2.2.
- Auto-merge by kit-evolve.
- Raw private project harvesting without export/consent.
- Rewriting historical scorecards, plans, or handoffs.

## 11. Program definition of done

1. Synthetic domain adds one descriptor plus owned/generated files, with zero
   validator/scaffold implementation edits.
2. Synthetic host/surface adds one descriptor plus owned files, with zero
   validator/scaffold/CI inventory edits.
3. Software-dev and knowledge-work satisfy the same six-slot Interface and use
   the same deep work-loop Module.
4. AGENTS is sole substantive dat-kit project contract; known conflicts are
   preservation-first and fail closed.
5. A real v1 project follows deterministic v2 migration; 1.x still installs.
6. Immutable telemetry records two domains without rewrite or false precision.
7. Evolution maps every governed path exactly once with typed signals, risk,
   and independent authority.
8. A real-project signal produces a non-trivial independently reviewed
   proposal.
9. Governance cannot approve itself; evolution cannot auto-merge.
10. Each release has real CI, required host smoke, explicit deferrals, and its
    own completed DoD.

## 12. Approval checklist

Maintainer approval of v4 explicitly chooses:

- [ ] Six-slot Domain Pack with `workflow.md`.
- [ ] One deep Registry Module and no two-inventory compromise.
- [ ] `contract_check.py` as public project-contract Interface backed by the
      Registry Module.
- [ ] Host claim scoped to no duplicate dat-kit policy plus known-conflict
      detection, not universal conflict freedom.
- [ ] Migration before structural RC.
- [ ] `v2.0` platform kernel, `v2.1` telemetry, `v2.2` self-evolution.
- [ ] Immutable enrichment rather than scorecard rewrite.
- [ ] Semantic risk classification with unknown → Class C.
- [ ] Prior-policy evaluation and temporal separation for governance changes.
- [ ] No forced Class B merge as a release gate.

Until these boxes are approved, implementation does not begin.
