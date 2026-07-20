# dat-kit Open Platform Program Plan

**Status:** APPROVED — §14 checklist answered 12/12 "approve" by the maintainer (Dat), 2026-07-17; see the approval record at the end of §14. Implementation may begin at Phase 0A.
**Plan revision:** v7 (2026-07-17), amended v7.1 (2026-07-18 — §16 token discipline) — plan revisions are not product versions
**Program releases:** dat-kit 2.0.0 (platform kernel) → 2.1.0 (telemetry) → 2.2.0 (self-evolution)
**Maintenance prerequisite:** dat-kit 1.17.1
**Supersedes:** `plans/PLAN-v5.0.0-open-platform.md` (plan rev v5) and the uploaded plan rev v6
**Decision required before implementation:** approve §14.

This document is a plan, not execution authority. Approval authorizes phases
and release boundaries; it does not waive per-phase evidence, review,
migration, security, or release gates.

## 0. Executive decision

Plan rev v6 (Codex) is adopted as the skeleton: its boundary machinery is a
genuine advance over v5 — the contract-revision state machine, adapter
artifact lifecycle, mandatory v1.17.1 maintenance release, registry bootstrap
diagnostics, sanitized scaffold manifest, task-ID-at-LOAD telemetry lifecycle,
temporal-independence rule for evals, acceptance-rate-as-diagnostic, and full
RC/rollback/tag release trains for every program release.

Review round 4 (independent fable) found v6 had lost contact with the actual
repository — verdict ADOPT-WITH-AMENDMENTS 6/10, four blockers: the live host
materialization spike was dropped (the whole layout rests on an unproven
assumption about installed-plugin file resolution, with no Codex evidence at
all); the real `knowledge-work` pack vanished (zero mentions — goal 1 demoted
to synthetic-only while a shipped skill becomes an orphan); the capability
ladder / loop ceiling was unhoused (v6's descriptor slot replaced
loop-profile and dropped the repo's core automation-safety mechanism); and
the target layout deleted host-mandated manifests, reviewer agents, hooks,
and existing append-only benchmarks — read literally, a plugin no host can
install. v7 = v6 + the round-4 amendment list (12 items) + restored v5
mechanisms that rounds 1–3 had already paid for.

## 1. Product outcome

dat-kit becomes an open discipline platform whose stable center is a work
contract, not a particular coding agent. Five outcomes:

### 1.1 Multi-profession composition
A profession is one Domain Pack under `domains/<domain-id>/` plus one
descriptor in `registry/domains.json`. Software development is no longer
embedded in `build-loop`; it is one Domain Pack composed with a reusable
work-loop engine. **`knowledge-work` — the shipped second pack — migrates to
the same Interface**; multi-profession is proven by two real domains plus one
synthetic, not by a synthetic alone.

### 1.2 Host-neutral policy
Generated projects have one canonical instruction contract: `AGENTS.md`.
Claude Code, Codex, Gemini CLI, Cursor, and future hosts receive only
pointer/configuration artifacts registered as Host Adapters. Those artifacts
may select or point to policy but may not duplicate, weaken, or override it.
**Scope of the claim:** "conflict-free" never means dat-kit can neutralize
arbitrary user, organization, or third-party host instructions. It means
dat-kit itself introduces no substantive duplicate policy, reserves only
named adapter files, preserves brownfield content, and reports known
conflicts before mutation.

### 1.3 Registry-driven extension
Adding a valid host or domain changes descriptors, templates, and generated
projections — not validator branching, shell copy lists, or hand-maintained
inventories.

### 1.4 Measured I/O improvement
Telemetry v3 records enough context to understand input/output cost and
workflow quality over time: tokens when attribution is safe, first-pass gate
rate, review rounds, defects, elapsed time, event coverage, and component
revisions — with named decision reports, not just raw events.

### 1.5 Governed learning from history
`kit-evolve` mines telemetry and lessons, including explicitly imported
evidence from real projects, and generates deterministic proposals. It may
improve any governed component, including itself. It may never merge its own
proposal, weaken its own evidence requirements, or use a newly created
evaluation to approve the same proposal. Until v2.2 lands, the operative
improvement path is manual proposals against the governed universe via
`explain-evolution` — every component is born with its path.

## 2. Non-negotiable architectural claims

Program invariants; any exception is a Class C governance decision.

1. One generated-project policy owner: `AGENTS.md`.
2. Thin host adapters: pointers/configuration only; no copied policy.
3. One descriptor owner per component: no independent second inventory.
4. Generated artifacts are projections, not authorities: marker + byte-exact
   `--check`.
5. Normative contracts precede implementations.
6. Recognized old is not valid current: migration-source revisions are
   diagnostic and non-green.
7. Inspect before mutate; brownfield is never rewritten merely because its
   old revision is recognized.
8. Telemetry facts are immutable: corrections are new events, never edits.
9. Evolution proposals are deterministic and review-bound: mining is
   automated; authority is not.
10. Governance evidence is temporally independent: a proposal cannot
    manufacture the corpus or gate that certifies itself.
11. Extension tests prove deletion of hardcoding: a synthetic component works
    without editing a validator, renderer consumer, or scaffold copy list.
12. Release claims require release trains: RC, migration, smoke, rollback,
    and tag evidence — implementation DoD alone is insufficient.
13. **Loop capability is earned, never assumed:** every domain declares a
    loop ceiling (Turn/Goal/Time/Proactive) justified by gate quality; raising
    a ceiling is Class C.

## 3. Architecture

### 3.1 Six-slot Domain Pack contract

Every active Domain Pack has exactly six semantic slots (restoring v5
membership — the registry descriptor is the pack's registry entry, not a
slot):

| Slot | Artifact | Responsibility |
|---|---|---|
| `workflow` | `workflow.md` | domain-specific phases and decision flow; required-input and missing-information behavior |
| `ground_truth` | `ground-truth.md` | authoritative sources and evidence hierarchy; trust and currency rules |
| `gates` | `gates.md` | stable gate IDs, criteria, worked pass/fail cases, gaming lines, automation status |
| `reviewers` | `reviewers.md` | reviewer roles, routing, authority, verdict contract, escalation |
| `deliverables` | `deliverables/` | one or more output templates/examples (directory — matches the shipped packs and the current §2b validator) |
| `loop_profile` | `loop-profile.md` | allowed Turn/Goal/Time/Proactive modes and why the ceiling is earned |

The **descriptor** (in `registry/domains.json`) declares: stable domain ID,
pack location, trigger metadata (name, description, aliases), required engine
revision, gate-authority reference, **`loop_ceiling` (mirrors and is
validated against `loop-profile.md`)**, evolution profile, lifecycle, and
contract revision. Gate authority is a typed role or opaque stable reference
with a succession rule; proposer and closer may not be the same actor.

The reusable work-loop engine owns only cross-domain mechanics:

```text
LOAD → FRAME → PLAN → EXECUTE → VERIFY → REVIEW → HARVEST
```

It does not own software terminology, repository operations, test commands,
or a profession's standards of truth.

Composition order is deterministic; later layers may narrow execution but may
not contradict earlier policy; contradiction = named diagnostic + stop:

```text
canonical project contract → engine revision → Domain Pack descriptor + six slots
  → optional project profile → Host Adapter projection
```

**Gaming-line freshness rule:** a gate that is actually gamed produces, the
same day, a lessons-learned entry and a Class B proposal revising that gate's
gaming line.

### 3.2 Projection Module (scoped)

A single Projection Module (`scripts/render.py`) owns committed derived
artifacts. **v2.0 scope: exactly two projections** — `domain-trigger` and
`scaffold-manifest`. (`render_adapter_projection` / `render_version_projection`
from plan rev v6 are cut until a second consumer exists.)

```text
python scripts/render.py domain-trigger <domain-id>
python scripts/render.py scaffold-manifest
python scripts/render.py all
python scripts/render.py --check
```

Rules: deterministic output for the same repo state; generated files carry
`GENERATED FROM REGISTRY — DO NOT EDIT` + source descriptor revision;
`--check` is byte-exact and never rewrites; paths/IDs/aliases validated
before rendering; no generated artifact becomes a second source of truth.

**Domain trigger projection.** The descriptor owns the user-facing skill
name/description/aliases; the renderer owns the standardized thin body,
which must: resolve the descriptor via the Registry Catalog → load the
declared engine revision → load all six slots in contract order → load the
project profile when declared → fail with a named diagnostic on a missing
slot or revision mismatch → execute deliverable/gate/reviewer routing from
the loaded pack. No independent domain policy in the trigger.

**Cache-invalidation trap (paid-for lesson):** a re-rendered trigger changes
host behavior only after plugin reinstall/update + a fresh session. Every
description-tuning loop is: edit descriptor JSON → render → eval → reinstall
+ fresh session. Skill evals may run against the rendered preview
(`render.py domain-trigger` output) to keep iteration fast; the installed
smoke still validates the cached copy.

**Scaffold manifest projection.** To keep Bash-only greenfield while deleting
the hardcoded copy list (`init.sh:87-92`), render
`templates/common/.dat-kit-files.tsv`; each validated row:
`source_rel<TAB>target_rel<TAB>ownership<TAB>action<TAB>introduced_revision<TAB>lifecycle`.
Constraints: no tabs/newlines/traversal/absolute paths/shell metacharacters
in path fields; closed versioned action enum; only `scaffold_active` rows
materialize; `init.sh` reads the manifest generically — no `eval`, no ad hoc
JSON parsing; a synthetic Host Adapter becomes materializable with no shell
edit. The TSV is a shipped projection; registries remain its authority.

### 3.3 Registry Module and bootstrap

The Registry Module (`scripts/registry.py`) is a deep module. Public
interface — the Registry Catalog:

```text
Catalog.load(repo_root) -> Catalog | Diagnostic[]
Catalog.domains() / adapters() / evolution_policy()
Catalog.scaffold_file_plan(mode) -> FilePlan
Catalog.version_targets() -> VersionTarget[]
Catalog.governed_paths() -> GovernedPathSet
Catalog.explain_path(path) -> OwnershipExplanation
```

Only hardcodes allowed: bootstrap filename `registry/platform.json`; the set
of registry-format revisions the running code understands; named bootstrap
diagnostics. Bootstrap is fail-closed:

| Condition | Diagnostic |
|---|---|
| file missing | `REGISTRY_BOOTSTRAP_MISSING` |
| malformed JSON | `REGISTRY_BOOTSTRAP_MALFORMED` |
| unknown/future format | `REGISTRY_FORMAT_UNSUPPORTED` |
| referenced child missing | `REGISTRY_CHILD_MISSING` |
| child revision mismatch | `REGISTRY_CHILD_REVISION_MISMATCH` |
| mixed incompatible code/data upgrade | `REGISTRY_ATOMIC_UPGRADE_REQUIRED` |

Validation is a bespoke standard-library validator with path-aware
diagnostics; it must not imply JSON Schema compliance (no new dependency).

### 3.4 Normative contracts before code

Written and approved before registry implementation:
`docs/contracts/registry.md`, `evolution.md`, `domain-pack.md`,
`host-adapter.md`. They define formats, ownership, lifecycle, diagnostics,
extension/retirement protocol, and compatibility rules. Code and example
JSON implement the documents; neither silently becomes the contract.

### 3.5 Project materialization and FilePlan

The Catalog produces a typed FilePlan driving greenfield scaffolding,
brownfield inspection, and migration previews alike. Entry fields:
`source_template, target_relative_path, ownership_class,
materialization_action, artifact_lifecycle, project_contract_revision,
expected_content_hash, precondition`. Modes: `greenfield`, `add-missing`,
`inspect-brownfield` (report only), `migrate-approved` (after backup and
review). `init.sh` is a compatibility launcher + greenfield materializer
over the generated manifest; Python tools consume the Catalog directly;
conformance fixtures prove both agree on the FilePlan.

### 3.6 Project contract revision state machine

`registry/platform.json` defines: `canonical_revision`, `green_revisions[]`,
`migratable_source_revisions[]`, `unsupported_revisions[]`,
`revision_descriptors[]`, `migration_edges[]`.

For dat-kit 2.0: canonical = `dat-kit 2.0`; green = `[dat-kit 2.0]`;
migratable source = `[dat-kit 1.16.0]`. A v1.16 project produces
`CONTRACT_MIGRATION_REQUIRED` (nonzero) — recognition prevents data loss, it
does not certify currency. **Pre-marker projects** (dat-kit installs
predating the 1.16 contract marker) classify as unsupported-with-guidance:
named diagnostic, manual migration notes, never silent mutation.

Every recognized revision has an immutable descriptor (marker rules,
required pointer set, static-template hashes, migration edges, snapshot
provenance, last release allowed to remove support). Snapshots ship under
`registry/snapshots/`; migration logic may not depend on Git history.
Removing the v1.16 source before the next major release is Class C.

### 3.7 Host Adapter artifact lifecycle

```text
repo_only → migration_ready → scaffold_active → retired
```

`repo_only`: conformance-tested in dat-kit, never emitted. `migration_ready`:
preview + fixtures exist; greenfield emission off. `scaffold_active`:
greenfield and approved migration may emit. `retired`: recognized for
removal guidance, not emitted. Activation gates: repository conformance;
official host behavior fact-checked; clean + customized brownfield fixtures;
no duplicated policy; rollback removes only adapter-owned artifacts. A
registry entry never silently becomes a project mutation.

### 3.8 Governed universe

`registry/evolution.json` declares `governed_roots[]`,
`explicit_exclusions[]`, `component_classes[]`, `signals[]`, `authorities[]`,
`policies[]`. Every tracked product file under a governed root resolves to
exactly one owner and governance class; an ungoverned, unexcluded new
top-level path fails `EVOLUTION_ORPHAN_PATH`. Generated files resolve to
their source descriptor owner.

**v2.0 scope-down:** v2.0 ships governed roots + exclusions + component
classes + the manual path (`python scripts/registry.py explain-evolution
<path>` — reports owner, class, required signals, gates, reviewers,
authority, expected evidence; `docs/contracts/evolution.md` defines manual
proposal/closure). Full signal and authority catalogs (§3.9) land with v2.2;
until then signal references may be the honest generic proxies (lessons, CI,
evals, user reports).

### 3.9 Signal and authority catalogs (v2.2)

Signal descriptor: `signal_id, producer, artifact_or_schema_revision,
status = active | proxy | planned, quality_limitations, retention`. A policy
may use `active` or approved `proxy`; `planned` cannot satisfy a gate.
Authority descriptor: `authority_id, role_type, allowed_decision_classes,
allowed_closer, succession_rule, approval_evidence_contract,
revocation_rule`. Proposal decisions record policy revision + hash, closer
identity/role, approval reference, timestamp, effective-from-run.

### 3.10 Telemetry task lifecycle (v2.1)

```text
python scripts/telemetry.py start | append --task-id <uuid> --event <type> | finish --task-id <uuid>
```

- UUIDv4 minted at `LOAD` (or first equivalent step); ID propagates through
  handoffs, delegated work, gate events, review events, HARVEST.
- Scorecard finalizes at HARVEST; a completion-only scorecard may mint an ID
  but records `event_coverage = partial` — **a first-class degraded path,
  not an anomaly**.
- **Per-host start mechanism:** Claude Code — SessionStart hook (`hooks.json`
  stays); other hosts — trigger-prose instruction in the rendered domain
  trigger; the telemetry report includes an **event-coverage-rate view** so
  degraded coverage is measured, not hidden.
- Event writes are append-only and atomic at the record boundary.
  **Concurrency scope-down:** single-writer atomic append (O_APPEND) +
  interrupted-append recovery fixture is the v2.1 requirement; multi-writer
  locking is deferred until delegated agents actually write concurrently.
- Corrections point to the incorrect event, never replace it.
- Token attribution is exact or explicitly unknown with a reason code —
  never fabricated.
- **Durable corpus:** committed append-only files under `benchmarks/` remain
  the durable, cross-machine record (existing `scorecard.jsonl` and
  `skill-evals.jsonl` stay in place, untouched); `telemetry/events.jsonl` is
  the local working stream; Phase 6 defines the export/aggregation step from
  local events to committed benchmarks and the retention rules. Goal 5's
  history must outlive one laptop.

### 3.11 Evolution objectives

Acceptance rate is diagnostic only — optimizing it rewards easy proposals.
Outcome reporting is stratified by governance class: realized post-change
outcome, first-pass gate-rate delta, review-round delta, token/elapsed delta
where attribution is reliable, defect and revert rate, unmeasured-outcome
rate, time to decision; volume and acceptance rate as context. No proposal
is called successful before its observation window closes or it is marked
unmeasured.

## 4. Target repository layout (complete)

```text
AGENTS.md
HUONG_DAN.vi.md                      # updated in Phase 5
.claude-plugin/{plugin.json,marketplace.json}    # host-mandated, stays at root
.codex-plugin/plugin.json                        # host-mandated, stays at root
.agents/plugins/marketplace.json                 # host-mandated, stays at root
hooks.json                                       # Claude SessionStart bootstrap, stays
docs/
  agent-workflow.md
  agent-working-rules.md
  domains.md                         # projection-checked against registry
  loops.md                           # capability ladder (kept; "final" wording removed)
  model-selection.md
  codex.md                           # redirect stub after fold into adapters/codex/
  contracts/{registry.md,evolution.md,domain-pack.md,host-adapter.md,telemetry-v3.md†}
  decisions/0001-open-platform.md    # reversal record, Phase 0B
engine/work-loop/ENGINE.md
registry/
  platform.json  domains.json  adapters.json  evolution.json
  snapshots/project-contract-1.16.json
domains/
  software-dev/{workflow.md,ground-truth.md,gates.md,reviewers.md,deliverables/,loop-profile.md}
  knowledge-work/{workflow.md,ground-truth.md,gates.md,reviewers.md,deliverables/,loop-profile.md}
skills/
  build-loop/SKILL.md                # generated thin trigger (software-dev)
  knowledge-work/SKILL.md            # generated thin trigger
  domain-builder/SKILL.md
  scorecard/SKILL.md
  kit-evolve/SKILL.md†
  ...all other utility skills unchanged unless explicitly migrated
    (fable-mode, fable-pro, guardian-builder, project-init, handoff,
     diagnosing-bugs, improve-codebase-architecture, git-worktrees,
     cookbook-lookup, terse-mode)
agents/{plan-reviewer,qa-agent,code-reviewer,security-reviewer}.md
adapters/{claude-code,codex,gemini-cli,cursor}/ADAPTER.md
templates/
  common/                            # AGENTS.md, pointer set, spec/, docs/, session-bootstrap.txt,
                                     # .dat-kit-files.tsv (generated projection)
  profiles/{laravel-react,react}/
scripts/{registry.py,render.py,contract_check.py,validate.py,init.sh,scorecard.py,statusline.py,
         telemetry.py†,evolve.py‡,tests/}
benchmarks/
  scorecard.jsonl  skill-evals.jsonl # existing append-only history, in place, untouched
  defects.jsonl† escalations.jsonl† evolution.jsonl‡   # additive
lessons-learned/  handoffs/  plans/
telemetry/{README.md,schema-v3.json†,events.jsonl†}    # events.jsonl local/ignored; export → benchmarks
evolution/{proposals/,decisions.jsonl}‡
```

† lands v2.1 · ‡ lands v2.2. Physical location of `engine/` and `domains/`
is subject to the Phase 0B materialization spike (Option A/B below). Names
change only through the Phase 4 ownership map.

### Physical-layout decision (Option A/B)

- **Option A:** installed Claude and Codex plugins reliably resolve pack
  files outside `skills/` from a live session → layout above.
- **Option B:** at least one host cannot → pack content stays physically
  beside the domain entrypoint under `skills/`; the six-slot Interface,
  descriptors, IDs, ownership, and conformance suite are preserved
  unchanged. Option B relocates implementation only; it does not re-fuse
  software policy into the engine.

## 5. Release and branch topology

The scorecard defect is a prerequisite maintenance fix, not optional debt.

```text
master at 1.17.0
  └─ maintenance/scorecard-no-rewrite → tag v1.17.1
       ├─ release/1.x
       └─ feature/open-platform-v2 → tags v2.0.0, v2.1.0, v2.2.0
```

Rules: `release/1.x` and the feature branch are both cut from the fixed
v1.17.1 commit, never from known-bad v1.17.0; maintenance merges via review;
each program release has its own RC evidence bundle and rollback note; no
v2-only behavior backports to 1.x without separate approval.

## 6. Implementation phases

Every implementation phase appends a scorecard line (dogfooding).

### Phase 0A — Mandatory scorecard maintenance release (v1.17.1)

Current behavior (`scorecard.py:79-88,139`) session-window-matches token
totals onto multiple entries and rewrites `benchmarks/scorecard.jsonl` in
place. Patch minimally:

1. disable persistent post-hoc token enrichment of existing records;
2. exact session totals only in the newly appended record when attribution
   is unambiguous;
3. otherwise null + reason code;
4. **report-time (non-persistent) token display remains allowed** so goal-4
   data does not go dark until v2.1;
5. update the scorecard skill/docs; no telemetry v3, no sidecar here;
6. correct the stale README "release pending" line (tag `v1.17.0` is pushed
   at `origin/master`).

Tests: prefix-hash proves prior bytes unchanged; ambiguous multi-task
session leaves tokens unknown; single-task attribution writes only the new
record; malformed last record doesn't trigger rewrites; concurrent-append
failure leaves existing bytes intact; v1.17 readers still work.

Exit: gates pass; release notes explain the correction; v1.17.1 tagged;
both long-lived branches based on the fixed commit; **the `release/1.x`
install/update route is demonstrated live on Claude Code and Codex** (not
asserted). No dated-acceptance alternative.

### Phase 0B — Decisions, spikes, escape hatch

Approve before structural work: six-slot contract; stdlib validation (no
JSON Schema); Bash-only greenfield via generated manifest; contract revision
state machine; adapter lifecycles; the 2.0/2.1/2.2 split; recorded
official-doc facts for all initial Host Adapters (**including Codex** —
plan rev v6 had no Codex facts at all); current gate commands baseline.

Spikes (each produces a short decision report):

- **Live host materialization spike (restored — round-1 blocker B1, round-4
  blocker 1):** install the current plugin on fresh Claude Code AND Codex
  sessions; make a thin experimental skill resolve and read a test file
  outside `skills/`; record plugin-root resolution, cached layout,
  fresh-session requirements, failure behavior per host. **Its recorded
  outcome selects physical Option A or B (§4).**
- deterministic domain-trigger rendering;
- sanitized manifest parsing in Bash on Windows Git Bash and Linux;
- unknown/future registry-format diagnostics;
- project-contract snapshot matching without Git history;
- append/recovery behavior on Windows and Linux;
- deterministic proposal IDs across path separators.

Create: isolated worktree/branch for the cutover; revert map by phase;
fixture inventory; line-level ownership draft for Phase 4 files.
**Write `docs/decisions/0001-open-platform.md`:** formally reverses the
2026-07-14 "flat layout is permanent/final" decision (`docs/domains.md:14`,
`docs/loops.md:3`) with owner, date, evidence that changed the decision,
accepted migration cost, conditions-to-revisit, and a standing prohibition
on "final"/"permanent" architecture wording.

Exit: every spike reported; Option A/B selected; unresolved decisions block
dependent phases; no public scaffolding behavior changed.

### Phase 1A — Normative contracts before code

Write and approve the four `docs/contracts/` documents (bootstrap/format
behavior, all named diagnostics, descriptor field ownership, projection
rules, six-slot semantics, adapter lifecycle, revision states, governed
roots/exclusions, extension and retirement protocol, compatibility and
rollback expectations). Python protocol types are drafted for review but add
no undocumented semantics. Exit: contract review passes; examples validate
against prose; contradictions resolved; implementation tasks reference
contract clauses.

### Phase 1B — Registry, Projection, FilePlan foundations

Implement: `registry/*.json` for the CURRENT state; `scripts/registry.py`;
`scripts/render.py` (two projections only); generated scaffold manifest;
immutable v1.16 snapshot metadata; generic registry/projection validation in
`validate.py`. Lifecycle constraints: current domain descriptors are
`legacy` until the Phase 4 cutover; new project adapter artifacts stay
`repo_only` until Phase 3; Phase 1 claims no six-slot behavioral
conformance and emits no new project artifacts.

Red-before-green extension fixtures: synthetic registry-only domain
(no Python edit); synthetic host descriptor + template → manifest render
(no shell edit); unknown descriptor field → path-aware diagnostic;
unknown/future bootstrap format → `REGISTRY_FORMAT_UNSUPPORTED` before child
loading; mixed code/data revisions → atomic failure; new governed product
path → `EVOLUTION_ORPHAN_PATH`; descriptor referenced by a projection
deleted → byte-exact check fails.

Exit: validators consume the Catalog for inventory; no host/domain tuple in
validator logic outside fixtures; projections byte-exact in CI; existing
public scaffolding output unchanged; greenfield still works without Python
from a released package; **a standing Windows CI job runs the Python
validators/tests** (cp1252 was a real shipped false-red).

### Phase 2 — Repository-side Host Adapter conformance

Adapter packages for Claude Code, Codex, Gemini CLI, Cursor. Each
descriptor: host ID + aliases; official-doc reference + verification date;
repo artifact paths; project artifact paths; pointer semantics; policy
prohibition; capability assumptions; lifecycle; conformance fixtures + smoke
command. All new project artifacts remain `repo_only`.

Conformance proves: the adapter points to/selects `AGENTS.md` through an
officially supported mechanism; no duplicated policy blocks; missing
`AGENTS.md` → clear failure or documented degradation; a synthetic adapter
changes registry/templates/projections only; retirement removes only
adapter-owned artifacts; official-doc assertions recorded with dates;
**where a host is available, the smoke invokes a thin domain trigger and
reads the pack from a fresh installed session** (restored from v5 —
pointer checks alone don't prove the toolkit runs). Extend the personal-info
gate to new public config/text suffixes including `.mdc`.

Exit: adapter packages green; host smokes pass where hosts are available;
unavailable hosts have an explicit manual evidence checklist; no new
project artifact emitted.

### Phase 3 — Contract migration state machine and adapter activation

Implement the revision model in `contract_check.py` + scaffolding preflight.

Fixtures: clean v1.16 → nonzero `CONTRACT_MIGRATION_REQUIRED` +
deterministic preview; customized v1.16 → nonzero, custom files preserved,
conflicts reported; clean v2 → green; partially migrated → named
diagnostic; unknown revision → unsupported, no mutation; missing marker with
recognizable files → ambiguous, no mutation. **`.cursorrules` gets typed
`RETIRE_LEGACY` semantics** (Cursor documents it deprecated; Agent mode
ignores it): recognized, inventoried, replaced by the `.cursor/rules`
pointer only in an approved migration plan.

Migration sequence: inspect/classify → immutable pre-change report + hashes
→ migration FilePlan → explicit approval for replace/remove → backup →
apply → contract + host conformance → rollback instructions. Adapter
artifacts progress `repo_only → migration_ready`, and to `scaffold_active`
only after clean + customized fixtures pass.

Exit: v1.16 never green under the v2 checker; brownfield default is
inspect-only; greenfield is registry-driven; artifacts activate
individually; rollback fixture-tested.

### Phase 4 — Isolated structural cutover to six-slot Domain Packs

In the Phase 0B worktree. **Before moving lines,** complete the line-level
ownership map for: current `build-loop` instructions (including PREFLIGHT,
severity rubric, autopilot transitions, delegated-build two-stage review,
interrupted-session recovery, the software lens table, Git/commit
conventions, demo walk, review-team table); **`skills/knowledge-work/`
(SKILL.md playbook A→G + five slot files)**; `docs/loops.md`; software gates
and reviewer rules; generated-project templates; domain-builder guidance;
maintainer-only rules. Every substantive instruction gets exactly one
destination: `engine | domain-pack | project-contract | maintainer-policy |
retired-with-reason`. The map is independently reviewed as the pre-move
tripwire (any engine line requiring domain knowledge = stop); this is a
substantive rewrite of battle-tested skills, budgeted as such.

Implement: host-neutral engine; `domains/software-dev/` six slots + active
descriptor; **`domains/knowledge-work/` six slots** (workflow.md absorbs the
A→G playbook; existing five slot files migrate; `loop-profile.md` keeps the
Goal-human-run ceiling, mirrored in the descriptor's `loop_ceiling`);
generated thin triggers for both; domain-builder rewritten to author
descriptor + six slots + rendered trigger + inherited evolution profile;
docs/examples re-derived. Replace sentence-marker pack detection with
registry conformance.

Behavioral tests: software-dev happy path loads six slots; **knowledge-work
report + fact-check paths before/after**; synthetic non-software pack
completes the engine lifecycle; missing/stale generated trigger fails
`--check`; hand-edited trigger fails byte-exact; alias collision fails;
changed engine revision fails composition; eval verifies actual pack files
load (not just names in text); negative trigger cases; build-loop normal,
autopilot, delegated, security, recovery, harvest paths before/after;
installed Claude/Codex pack reads; end-to-end dry-run domain-builder pack;
same conformance under Option A or B.

Cutover discipline: commit by semantic owner; validate after each owner
moves; a failed move reverts that semantic slice (never duplicate policy
into both locations); no partial six-slot claim reaches `master`.

Exit: software-dev AND knowledge-work are active six-slot packs; the engine
contains no domain-specific policy; deletion test proves engine depth; both
triggers are generated and behaviorally load their packs; synthetic pack
passes; ownership map has no unassigned or duplicate lines.

### Phase 5 — dat-kit 2.0.0 release train

1. freeze registry and contract format revisions;
2. bump the version owner in `platform.json`;
3. render + byte-check all projections;
4. run unit, contract, registry, projection, migration, and skill-eval
   suites;
5. clean-install smokes on Windows Git Bash and Linux;
6. available-host smokes (trigger invocation + pack read) + manual evidence
   checklists for unavailable hosts;
7. migrate clean and customized v1.16 fixtures + one real v1.16 project;
8. RC1 + evidence bundle; findings via reviewed commits; RC2 if needed;
9. validate rollback to v1.17.1 tooling with project files preserved;
10. **docs sweep:** README rewrite (architecture + per-host capability/
    support table), `docs/codex.md` folds into `adapters/codex/ADAPTER.md`
    with a redirect stub, `HUONG_DAN.vi.md` updated, `docs/domains.md` +
    `docs/loops.md` "final/permanent" wording removed per decision 0001;
11. publish migration guide + release notes; tag `v2.0.0` from the approved
    RC commit.

Exit: §13.1 passes; no unresolved Class B/C decision; RC artifact equals
tagged artifact; `release/1.x` gates still pass on its branch.

### Phase 6 — Telemetry v3 and dat-kit 2.1.0

Write and approve `docs/contracts/telemetry-v3.md` first. Schema: event ID,
task ID, parent/delegation ID; timestamps + producer revision; domain/
engine/adapter/contract/profile revisions; gate outcomes + first-pass
status; review rounds + reviewer class; defects and rework; tokens with
attribution status/reason; elapsed time + clock source; event coverage;
privacy/source class; correction linkage.

Implement: `telemetry.py start|append|finish|validate`; atomic single-writer
append + interrupted-append recovery (multi-writer deferred); scorecard
HARVEST integration; early task-ID creation in rendered triggers + the
Claude SessionStart hook; handoff/delegation propagation; v2→v3 import as
new events only; local-events → committed-benchmarks export/aggregation +
retention rules (durable corpus, §3.10).

**Named signal producers (restored from v5 — schemas without producers stay
empty):**

1. build-loop HARVEST gains the **kit-facing lesson candidate** tag (root
   cause in a dat-kit skill/template/gate, not the project) — the automatic
   upstream channel;
2. diagnosing-bugs post-mortem gains a mandatory check: a defect rooted in
   previously approved work logs
   `{defect, introduced_task, approving_reviewers, gate_that_should_have_caught_it}`
   → `benchmarks/defects.jsonl`;
3. knowledge-work fact-check template gains a machine-readable per-gate
   result footer (human verdicts recorded — recording is not automating;
   the ceiling stands);
4. task schema gains `resumed_from_handoff: bool`;
5. reports include a **per-reviewer view** (defects + review rounds per
   reviewer) making the `model: opus` pins re-litigable on evidence, and an
   **event-coverage-rate view** per host.

Tests: interrupted append + last-record recovery; prior-byte hash
preservation; duplicate event ID rejection; correction behavior; partial
completion-only coverage; exact vs ambiguous token attribution; handoff and
delegated-child linkage; no secrets/raw prompts by default.

2.1.0 release train: freeze schema v3; bump + render; 2.0 regression suites
+ telemetry tests; RC observation sample on representative tasks (one real
software-dev AND one real knowledge-work task with human-run gate verdicts
recorded); downgrade/disable behavior verified; privacy/retention notes;
1.x unaffected; tag from approved RC.

### Phase 7 — Governed self-evolution and dat-kit 2.2.0

Implement `kit-evolve` only after active telemetry producers exist. Inputs:
telemetry v3 events; lessons; approved external project evidence with
provenance; registry component revisions; prior proposals/decisions;
active/proxy signal definitions. Outputs: deterministic proposal ID;
governed owner + class; evidence window + input hashes; hypothesis +
predicted outcome; patch scope; required gates/reviewers/closer; pre-change
baseline; observation plan; rollback condition; decision record.

Cold-start honesty: at program start the corpus is small; first proposals
come from lessons themes, eval-collision analysis, and defects/fact-check
records as they accumulate.

Automation boundary: the miner may create proposal artifacts and candidate
patches in an isolated branch and run predeclared gates; it may not approve,
merge, change authority, or weaken the policy governing its own proposal;
enforcement paths that can weaken governance are Class C; eval/benchmark
artifacts are ≥ Class B; an eval created or materially changed by a proposal
cannot be the decisive evidence approving that proposal.

Determinism/security fixtures: same normalized inputs → same proposal ID;
path-separator/record-order normalization; changed evidence window changes
identity; stale policy hash blocks closure; unauthorized closer fails;
post-change observation cannot rewrite the baseline; planned-only signal
cannot satisfy a policy; self-modification routes to Class C;
prompt-injection lessons; traversal/symlink/oversized/malformed exports;
threshold edges; understated risk; trivial eval change that cannot prove its
stated outcome.

2.2.0 release train: freeze proposal/decision formats; bump + render; all
prior regressions + evolution fixtures; shadow mode (proposals without
patches); false-positive/orphan/authority audit; one Class A and one Class B
end-to-end rehearsal without merge automation; emergency disable + rollback
verified; governance/privacy/operator guides; tag from approved RC. First
legitimate merged Class B is a success metric, not a manufactured DoD.

### Phase 8 — Earliest time-based unlock (v2.3+)

No self-adjusting policy or merge automation before ALL of: ≥90 days of
representative telemetry; unmeasured-outcome rate within an approved bound;
stable defect/revert rates; authority + succession exercised; red-team
review of gaming and evidence poisoning; a Class C proposal approving the
exact additional authority; independently demonstrated rollback. Time
elapsed alone unlocks nothing. The Time runner may open proposal
branches/PRs; it does not auto-merge; Class C keeps human sign-off;
Proactive remains notify-only.

## 7. Migration invariants

1. Detect before write. 2. Classify the source revision explicitly.
3. Snapshot pre-change state and hashes. 4. Distinguish untouched generated
files from customized files. 5. Preserve user-authored policy. 6. Never
infer that a recognized revision is current. 7. Never emit a new adapter
artifact solely because it exists in the registry. 8. Show the FilePlan
before destructive actions. 9. Keep rollback instructions with migration
evidence. 10. Verify post-migration with the new checker + host smokes.
No phase may weaken these to accelerate adoption.

## 8. Governance classes

**Class A — low-risk, reversible tuning.** Wording clarification without
semantic change; non-authoritative examples; threshold tuning inside a
pre-approved range. Requires: deterministic proposal; affected-owner gate;
one authorized reviewer; rollback note.

**Class B — behavioral or evidence change.** Domain Pack
workflow/gate/reviewer changes; Host Adapter behavior; telemetry producers/
schema-compatible changes; benchmark and eval corpus changes; new active or
proxy signals; skill bodies and scripts. Requires: pre-change baseline;
independent behavioral evidence (red-before-green where a gate changes);
owner review; observation window; no same-proposal self-certification.

**Class C — contract, authority, or enforcement change.** Canonical
`AGENTS.md` semantics; registry format/bootstrap; project contract revision
rules; governance policies and authority descriptors; enforcement code that
can weaken gates; `kit-evolve` self-modification; automatic merge authority;
early removal of a migration-source revision; **capability ladder and any
domain's loop ceiling**; reviewer `model:` pin policy. Requires: immutable
baseline + input hashes; explicit named authority; two independent reviews
or approved equivalent; full cross-component regression; rollback rehearsal;
effective-from-run boundary; decision record with policy revision + hash.

Generated artifacts inherit the class of their source owner. Markdown that
changes policy is not Class A merely because it is documentation. Unknown
impact is Class C. A gamed gate triggers the same-day freshness rule (§3.1).

## 9. Test and evidence strategy

### 9.1 Layered gates

```text
format/static checks → registry+projection unit tests → contract+migration fixtures
→ shell syntax + cross-platform materialization → skill-eval positive/negative
→ host conformance smoke → full repository validation → RC evidence bundle
```

**Standing disciplines:** every skill/trigger description change requires an
updated positive trigger-eval case (new triggers add collision cases);
changed gates prove red-before-green with isolated fixtures; non-ASCII
Python output proves pass AND fail paths on the maintainer's Windows
console; a standing Windows CI job runs Python validators/tests; every
implementation phase appends a scorecard line; registry, migration,
public-input, export, path, or external-write phases require security
review; review order is plan audit → implementation → QA → code review →
conditional security review → regression QA.

**Standing traps (paid-for lessons — unnamed traps get re-tripped):**

- Until Phase 1B lands, `validate.py` hardcodes `skills/build-loop/SKILL.md`
  and the flat one-level `skills/*/SKILL.md` glob — nothing moves early.
- `ci.yml` hardcoded pointer/count assertions go stale — replaced by
  semantic checks in Phase 1B; greppable until then.
- A workflow file is not CI evidence; verify a real Actions run on the
  actual default branch.
- An install copy is never the source of record — read the repo.
- A SKILL.md cannot execute logic; prose references paths, validators
  resolve them.
- Installed plugins and open sessions cache old versions — every smoke and
  every re-rendered trigger needs reinstall/update + a fresh session.
- Never encode evolution policy only in plan prose — thresholds, scopes,
  gaming lines live in versioned artifacts a proposal can target.

### 9.2 Extension proof

Proven only when a synthetic component passes all generic consumers with no
production Python or shell edit. Host Adapter chain: descriptor → Catalog →
projection → scaffold manifest → greenfield materialization → contract
checker → retirement. Domain Pack chain: descriptor → registry validation →
trigger rendering → six-slot composition → execution eval → evolution
ownership.

### 9.3 Evidence bundle

Each phase archives: commit + registry revisions; commands + exit codes;
fixture names/results; projection check result; fact-check sources + dates;
known limitations; reviewer and decision references; rollback notes. "Tests
pass" as prose is insufficient.

### 9.4 Fact-check discipline

Host claims are verified against official primary documentation at
implementation time and again before the affected RC. Descriptors record
verification date + capability assumption. Ambiguous official behavior →
the adapter stays `repo_only` or documents a named degradation.

## 10. Known risks and controls

| Risk | Control | Kill-switch |
|---|---|---|
| Installed host cannot resolve pack files outside `skills/` | Phase 0B live spike on BOTH hosts | Option B physical layout; Interface unchanged |
| legacy revision treated as current | green vs migration-source states, nonzero diagnostic | — |
| registry becomes a god module | narrow Catalog; separate Projection Module; contract tests | stop before Phase 2 if extension edits implementation |
| generated file becomes second authority | marker, byte-exact check, owner resolution | — |
| Bash manifest allows injection | closed actions, strict path grammar, no `eval`, red fixtures | — |
| registry entry emits files too early | adapter lifecycle + activation fixtures | — |
| trigger exists but does not load pack | standardized renderer + behavioral file-load eval | — |
| old template recognition depends on Git | shipped immutable snapshots | — |
| task ID minted at completion | start/append/finish lifecycle; `event_coverage=partial` labeled | — |
| interrupted/concurrent JSONL writes | atomic append + recovery fixtures (multi-writer deferred) | — |
| miner games acceptance rate | outcome metrics; acceptance diagnostic only | — |
| miner creates its own passing eval | evals ≥ Class B; temporal independence | — |
| new product path escapes governance | governed roots + `EVOLUTION_ORPHAN_PATH` | — |
| future registry format partially loads | bootstrap check before children; atomic upgrade diagnostic | — |
| cutover stalls mid-move | isolated worktree; commit-by-owner; slice revert | `master` untouched; keep v1 layout |
| release works but cannot ship safely | release train per program version | rollback to v1.17.1 tooling |
| migration loses policy | read-only planner, preservation, hashes | block migration; `release/1.x` |

## 11. Explicitly out of scope

Autonomous merge in v2.0–v2.2; dynamic network installation of untrusted
Domain Packs; a general plugin marketplace; a universal ontology of
professions; raw prompt/secret collection in default telemetry; exact token
counts without safe attribution; rewriting historical scorecards into v3;
supporting every editor/agent at v2.0; automatic removal of customized
brownfield files; JSON Schema claims without adopting a real implementation;
rewriting utility skills for tree uniformity (they carry governed-universe
rows and are fair game for proposals post-2.0); new profession packs
(enabled by v2.0, authored later with real practitioners); unverified
host-specific model routing (Claude-side reviewer pins stay, re-litigable on
v2.1 per-reviewer evidence — Class C).

## 12. Documentation deliverables

By v2.0: architecture overview; Domain Pack author guide; Host Adapter
author + conformance guide; registry format + bootstrap reference; evolution
governance / manual proposal guide; v1.16→v2 migration guide; generated-
project contract reference; adapter support/degradation matrix (in README);
greenfield/brownfield troubleshooting; **updated `HUONG_DAN.vi.md`**;
decision record 0001. By v2.1: telemetry v3 schema + lifecycle; privacy and
retention; token attribution limitations; recovery behavior. By v2.2:
kit-evolve operator guide; proposal/decision format reference; governance
class + authority guide; gaming/evidence-poisoning guidance; emergency
disable + rollback guide.

## 13. Program Definition of Done

### 13.1 v2.0.0

- [ ] v1.17.1 exists; both long-lived branches start from it; 1.x install
      route demonstrated live on both hosts.
- [ ] Decision record 0001 (layout-freeze reversal, revisit conditions)
      merged; "final/permanent" wording removed from docs.
- [ ] Normative registry, evolution, Domain Pack, Host Adapter contracts
      approved.
- [ ] Registry bootstrap rejects malformed/old/unknown/future/mixed formats
      deterministically.
- [ ] Registry Catalog owns component inventory; Projection Module output is
      deterministic and byte-exact checked.
- [ ] Greenfield Bash initialization consumes the generated sanitized
      manifest.
- [ ] A synthetic Host Adapter requires no validator or shell edit; a
      synthetic non-software Domain Pack composes through the engine.
- [ ] **Software-dev AND knowledge-work are active six-slot Domain Packs;
      both triggers are generated and behaviorally load their packs.**
- [ ] Every domain descriptor declares a `loop_ceiling` consistent with its
      loop-profile; ceiling changes are Class C.
- [ ] `AGENTS.md` remains the only generated-project policy owner; initial
      adapters are thin and lifecycle-governed.
- [ ] v1.16 is recognized only as a migration source, never green; clean and
      customized migration fixtures + one real project pass without silent
      mutation; `.cursorrules` has typed `RETIRE_LEGACY` semantics.
- [ ] Governed roots have no orphan product paths; `explain-evolution` works
      as the manual improvement path.
- [ ] Full release train, rollback, RC evidence, and tag complete.

### 13.2 v2.1.0

- [ ] Telemetry v3 contract approved; task IDs begin at LOAD; handoff and
      delegated work preserve linkage.
- [ ] Event history append-only under normal and interrupted writes; token
      attribution exact or explicitly unknown.
- [ ] **The five named producers work** (HARVEST kit-facing tag; diagnosing-
      bugs → defects.jsonl; knowledge-work fact-check footer;
      `resumed_from_handoff`; per-reviewer + event-coverage report views) —
      not just schemas.
- [ ] Durable corpus: local events export/aggregate to committed append-only
      benchmarks; existing scorecard history untouched.
- [ ] One real software-dev and one real knowledge-work task recorded with
      human/automated verdicts distinguished.
- [ ] Privacy/retention docs + disable behavior tested; v2.1 release train
      and tag complete.

### 13.3 v2.2.0

- [ ] Deterministic proposal/decision formats frozen; manual and automated
      paths use the same evolution policy.
- [ ] Authority succession and stale-policy rejection tested; governed
      universe has no unexplained orphan.
- [ ] Eval artifacts cannot self-certify their creating proposal; outcome
      reporting includes defect/revert/unmeasured/realized rates.
- [ ] Shadow mode + Class A/B end-to-end rehearsals pass; no autonomous
      merge authority exists; v2.2 release train and tag complete.

## 14. Approval checklist

1. Is `dat-kit 2.0` the only green project contract revision for the v2
   checker, with `dat-kit 1.16.0` a mandatory-nonzero migration source and
   pre-marker projects unsupported-with-guidance?
2. Is the generated sanitized TSV manifest approved as the Bash-only
   greenfield bridge?
3. Are `repo_only / migration_ready / scaffold_active / retired` the
   approved adapter artifact states?
4. Are the six Domain Pack slots (workflow, ground-truth, gates, reviewers,
   deliverables/, loop-profile) normative and exhaustive for v2, with
   `loop_ceiling` a required descriptor field?
5. Are generated triggers and manifests committed projections checked
   byte-for-byte, with the reinstall+fresh-session cache rule documented?
6. Is acceptance rate explicitly non-optimizing for kit-evolve, with
   benchmark/eval changes ≥ Class B and governance-weakening changes Class C?
7. Is the same-proposal self-certification ban approved?
8. Is v1.17.1 mandatory before `release/1.x` and the v2 branch, with the
   1.x install route demonstrated live?
9. Are telemetry v3 and kit-evolve correctly deferred to v2.1/v2.2, with
   manual proposals via `explain-evolution` as the improvement path in
   between?
10. Are v2.1 and v2.2 required to pass full RC/rollback/tag release trains?
11. Is the Phase 0B live materialization spike (both hosts) the deciding
    evidence for physical Option A vs B?
12. Is decision record 0001 (reversing the 2026-07-14 layout freeze, with
    conditions-to-revisit) approved?

Record the answers in an approved issue or decision record linked from this
plan.

### Approval record — 2026-07-17

All twelve questions answered **approve** by the maintainer (Dat) on
2026-07-17, via interactive review in a Cowork session:

| Q | Decision |
|---|---|
| 1 | Approved — `dat-kit 2.0` sole green; 1.16 migration source (nonzero); pre-marker unsupported-with-guidance |
| 2 | Approved — generated sanitized TSV manifest; Bash-only greenfield |
| 3 | Approved — `repo_only → migration_ready → scaffold_active → retired` |
| 4 | Approved — six slots normative; `loop_ceiling` required in descriptor |
| 5 | Approved — committed byte-exact projections + reinstall/fresh-session cache rule |
| 6 | Approved — acceptance rate diagnostic-only; evals ≥ B; governance-weakening = C |
| 7 | Approved — same-proposal self-certification ban (temporal independence) |
| 8 | Approved — v1.17.1 mandatory first; 1.x route demonstrated live on both hosts |
| 9 | Approved — telemetry → v2.1, kit-evolve → v2.2; manual `explain-evolution` path in between |
| 10 | Approved — full RC/rollback/tag release trains for v2.1 and v2.2 |
| 11 | Approved — Phase 0B live spike decides physical Option A vs B |
| 12 | Approved — decision record 0001 reverses the 2026-07-14 layout freeze, with revisit conditions |

Per-phase evidence, review, migration, security, and release gates remain in
force; this approval authorizes phases and release boundaries only.

## 15. Review history and fact-check footer

- Plan rev v1 → fable review #1 (general): REVISE 6/10 — host
  materialization unproven, domain-builder unrewritten, escape hatch
  untested; fixed in v2.
- v2 → fable review #2 (evolution coverage): REVISE — pipeline reached ~5 of
  19 component classes; fixed in v3 (proposal classes, coverage registry,
  named producers, self-proposable kit-evolve artifacts).
- v3 → Codex review + fresh-eyes pass: REVISE — registry depth, six-slot
  interface, task attribution, migration ordering not executable; produced
  v4.
- v4 → fable review #3: ADOPT-WITH-AMENDMENTS 7.5/10 — stdlib/JSON-Schema
  contradiction, no mid-cutover failure path, live append-only violation,
  ~8 dropped v3 mechanisms; merged as v5.
- v5 → Codex improvement: produced v6 (state machine, lifecycle, mandatory
  v1.17.1, projection module, telemetry lifecycle, release trains).
- v6 → fable review #4: ADOPT-WITH-AMENDMENTS 6/10 — four blockers (spike
  dropped, knowledge-work orphaned, capability ladder unhoused, layout
  deleted host-mandated artifacts) + majors (telemetry corpus location,
  adoption reality, silent token blackout, unaccounted skills); merged as
  this v7.

**External host facts to re-verify during implementation** (evidence inputs,
not permanent truth; each adapter records a fresh verification date before
activation and before the affected RC):

- Claude Code plugins are copied to a cache; plugin paths must remain inside
  the plugin root; `.claude-plugin/plugin.json` at repo root; SessionStart
  hooks supported.
- **Codex:** `.codex-plugin/plugin.json` with `"skills": "./skills/"`;
  whether an installed Codex plugin materializes files outside `skills/` is
  UNVERIFIED — this is exactly what the Phase 0B spike decides.
- Gemini CLI extensions use `gemini-extension.json` at the extension root;
  context-file (`GEMINI.md`/`contextFileName`) loads into every session —
  pointer-only.
- Cursor reads `AGENTS.md` natively; `.cursor/rules/*.mdc` is the current
  rules mechanism; `.cursorrules` is documented deprecated and ignored in
  Agent mode.

**Plan integrity:** a phase is complete only when its evidence and exit
criteria exist, not when its code is drafted. Any factual assumption found
false updates the relevant contract and decision record before dependent
work continues.

## 16. Amendment v7.1 (2026-07-18) — Token discipline

Motivation: executing phases 0A–1B on two machines (Claude Fable 5 Pro,
Codex 5.6) exhausted token budgets prematurely. Measured worst offender: one
3-agent parallel review round ≈ 284k tokens — roughly 60-70% of a session.
Root causes were execution-discipline gaps, not plan-architecture flaws.

Standing rules (extend §9.1; Class B change, maintainer-approved 2026-07-18):

1. **Sequential reviewers only.** The §9.1 review order is a strict sequence.
   Running reviewers in parallel is forbidden — a parallel security review of
   a diff that code review then changes is wasted work.
2. **Diff-scoped reviewers.** A reviewer reads the phase diff, the files it
   touches, and directly referenced contract/spec sections — never the whole
   repository. The dispatching prompt MUST name the changed-file list and
   paste the gate outputs so the reviewer verifies claims instead of
   re-discovering them.
3. **Findings-scoped re-reviews.** Round 2+ verifies the previous findings
   against the new diff only — never a fresh full review.
4. **Charter enforcement.** code-reviewer and security-reviewer are
   static-analysis-only (no PoC, no runtime attacks — those are qa-agent's
   alone). Reviewer reports are capped: findings ≤ ~30 lines.
5. **Session context protocol.** A session executing phase N of this plan
   loads: `AGENTS.md` + its linked docs, the newest `handoffs/` file, §6 for
   phase N only, §9, and this amendment. It does NOT read the whole plan or
   sections for phases already completed.
6. **Main-thread economy.** Grep before Read; Read targeted line ranges of
   large files; never re-read a just-edited file; resume from handoffs, not
   tree re-discovery.
7. **Model tiering stays deferred** per §11: reviewer `model:` pins change
   only on v2.1 per-reviewer evidence (Class C). This amendment does not
   change any pin.

Phase 4 must carry rules 1–4 into the software-dev and knowledge-work
`reviewers.md` slots via the ownership map, so the discipline survives the
cutover.
