# Evolution governance contract

Status: normative for dat-kit 2.0 manual governance and registry ownership.
Telemetry v3 automation is deferred to 2.1; governed proposal mining and
candidate patches are deferred to 2.2. Their planned fields cannot satisfy a
2.0 gate or authority requirement.

## EV1. Governed universe

`registry/evolution.json` is authoritative for:

| Field | v2.0 meaning |
|---|---|
| `format_revision` | Registry child format; v2.0 requires `1`. |
| `registry_revision` | Revision matched by the bootstrap child reference. |
| `contract_revision` | Evolution governance contract revision. |
| `governed_roots` | Canonical repository-relative roots whose tracked product files require ownership. |
| `explicit_exclusions` | Exact paths/subtrees intentionally outside product governance, each with reason and owner. |
| `component_classes` | Path matchers assigning one stable owner and default governance class. |
| `signals` | Active/proxy/planned evidence references; v2.0 may use honest generic proxies. |
| `authorities` | Stable closer/reviewer references needed by policies; full catalog behavior is deferred to 2.2. |
| `policies` | Class requirements, required evidence, gates, reviewers, authority, and rollback. |

Every tracked product file beneath a governed root resolves to exactly one
component owner and governance class unless exactly one explicit exclusion
applies. Zero matches is orphaned; multiple owner/class matches are ambiguous.
Generated files resolve to their source descriptor owner and inherit its class.

Path matching uses canonical repository-relative POSIX paths and is
case-sensitive on every host. Governed roots are literal component-boundary
paths and may not overlap (no root may be another root's ancestor). An
exclusion's `path` covers that exact path and descendants at `/` boundaries;
an exclusion may sit beneath exactly one root or inventory a top-level path; it
may not sit beneath multiple roots or overlap another exclusion.

`path_globs` use only literal path-segment characters plus `*` within one
segment and a complete terminal `**` segment for zero or more descendant
segments. `?`, character classes, braces, escapes, backslashes, absolute paths,
`.`/`..`, and embedded `**` are invalid. Matching is against the whole canonical
repository-relative path, not a substring.

Resolution order is fixed:

1. Canonicalize and reject unsafe paths under Registry R3.
2. Find exclusions by exact/subtree boundary. Exactly one returns an exclusion
   explanation without a governance class; more than one is ambiguous.
3. Otherwise find exactly one component-boundary governed root; none is
   `EVOLUTION_ORPHAN_PATH`, more than one is invalid registry data.
4. Otherwise match all component globs. Exactly one supplies owner/class/policy;
   zero is `EVOLUTION_ORPHAN_PATH`; more than one is
   `EVOLUTION_OWNERSHIP_AMBIGUOUS`.

Exclusion precedence is explicit, not silent. An exclusion beneath a governed
root must share that root's owner; a top-level exclusion may inventory an
intentionally ungoverned tracked path and names its accountable owner. Its
reason is mandatory, and boundary fixtures show the excluded path, a sibling,
and the first path outside the subtree.

The inventory input is every tracked plus non-ignored candidate path in the
checkout/release artifact. Therefore a new top-level path with neither a root
nor exclusion is orphaned; “outside” is not a green classification. VCS metadata
itself is outside the artifact input, not an implicit exclusion.

New top-level product paths must update this graph in the same change. Unknown
impact defaults to Class C, never to an exclusion.

v2.0 record shapes are closed:

- governed root: `{path, owner}`;
- exclusion: `{path, reason, owner}`;
- component class: `{component_id, path_globs, owner, governance_class,
  policy_ref}`;
- signal reference: `{signal_id, status, producer,
  artifact_or_schema_revision, quality_limitations, retention}`;
- authority reference: `{authority_id, role_type, allowed_decision_classes,
  allowed_closer, appointments, succession_rule, approval_evidence_contract,
  revocation_rule}`; and
- policy: `{policy_id, revision, owner, allowed_classes, required_signals,
  required_gates, required_reviewers, closer_authority_ref,
  rollback_evidence}`.

These shapes let v2.0 explain manual governance. Status `planned` remains
non-satisfying; automated producer/catalog enforcement remains deferred under
EV7.

An authority `appointments` array is non-empty and contains closed immutable
records `{appointment_id, identity, role, effective_from, revoked_at,
successor_of, evidence_ref, evidence_hash}`. IDs are unique; identity/role/refs
are non-empty; `role` equals the containing `authority_id`; `effective_from` and
non-null `revoked_at` are canonical `YYYY-MM-DDTHH:MM:SSZ` instants with
revocation strictly after effectiveness; `successor_of` is null or a prior
appointment ID; and `evidence_hash` is lowercase SHA-256. Records are retained
after revocation. A successor becomes authorized at its own effective boundary,
never merely because succession prose names a possibility.

## EV2. Path explanation and manual workflow

`python scripts/registry.py explain-evolution <path>` is read-only and reports:

- canonical input path and matched governed root/exclusion;
- source descriptor, stable owner, and governance class;
- policy revision;
- required signals/evidence, gates, reviewers, closer authority, and rollback;
- any diagnostic preventing a unique explanation.

The v2.0 manual workflow is:

```text
explain path → record baseline/evidence → classify → review/approve
  → apply isolated change → gates → authorized closure → observation/rollback
```

The tool does not propose, approve, mutate, weaken a policy, or infer authority.
Proposal and decision records are append-only evidence. Corrections point to a
prior record; history is never rewritten.

## EV3. Governance classes

### EV3.A Class A — low-risk reversible tuning

Examples: wording clarification without semantic change, non-authoritative
examples, or threshold tuning inside a pre-approved range.

Required: deterministic identity, including manually created proposals; an affected-owner gate; one
authorized reviewer, and rollback note. A Markdown policy change is not Class A
merely because it is documentation.

### EV3.B Class B — behavior or evidence change

Includes Domain Pack workflow/gate/reviewer changes, Host Adapter behavior,
telemetry producers or schema-compatible changes, benchmark/eval corpus changes,
new active/proxy signals, skill bodies, and scripts.

Required: pre-change baseline, independent behavioral evidence (including
red-before-green when a gate changes), owner review, observation window, and no
same-proposal self-certification. An eval created or materially changed by a
proposal cannot be decisive evidence approving that proposal.

### EV3.C Class C — contract, authority, or enforcement change

Includes canonical `AGENTS.md` semantics; registry format/bootstrap; project
contract revision rules; governance policies/authorities; enforcement capable
of weakening gates; self-modification; automatic merge authority; early removal
of a migration source; capability ladder/loop ceiling; reviewer model-pin policy;
and unknown impact.

Required: immutable baseline and input hashes, explicit named authority, two
independent reviews or approved equivalent, full cross-component regression,
rollback rehearsal, effective-from-run boundary, and a decision record with
policy revision and hash.

Generated artifacts inherit the class of their source owner. A change spanning
classes follows the highest class.

## EV4. Evidence and authority

v2.0 signals may be `active`, `proxy`, or `planned`. An active signal has a
working producer and known artifact/schema. An approved proxy is honest about
its limitations. Planned signals cannot satisfy a gate. Until 2.1/2.2, lessons,
CI results, evals, user reports, and independent reviews may be explicit proxies.

Every policy names owner, allowed decision class, required signals, gates,
reviewers, closer authority, rollback evidence, and revision. Proposer and
closer cannot be the same actor. Authority has a succession rule; absence or
revocation blocks closure. A policy cannot approve a proposal that weakens that
same policy unless routed through its Class C parent authority.

A proxy is approved for v2.0 only when it is present in the reviewed
`evolution.json` revision and named by the policy's `required_signals`; a
`planned` record can be inventoried but never satisfies that reference.

A gate that is actually gamed triggers a same-day lesson and Class B proposal
to revise the gaming line. Acceptance rate is diagnostic only; it is not a
quality objective.

## EV5. v2.0 proposal and decision evidence

In v2.0, proposal files are closed UTF-8 JSON objects in the already-authorized
manual evidence bundle at
`docs/decisions/evolution-<proposal_id>.proposal.json`. They reject duplicate
keys and contain exactly:

`format_revision`, `proposal_id`, `created_at`, `proposer_identity`,
`policy_revision`, `policy_hash`, `governed_owner`, `governance_class`,
`evidence_window`, `input_hashes`, `affected_paths`, `baseline_refs`,
`evidence_refs`, `hypothesis`, `patch_scope`, `required_gates`,
`required_reviewers`, `closer_authority_ref`, `observation_window`, and
`rollback_condition`.

`format_revision` is `1`; `created_at` is RFC 3339 UTC; `evidence_window` and
`observation_window` are exact `{start, end}` RFC 3339 UTC objects; for each,
`start` strictly precedes `end`, so empty or reversed windows fail. Policy and
input hashes are lowercase SHA-256. `governance_class` is `A`, `B`, or `C`.
`affected_paths` and `patch_scope` are sorted unique canonical-path arrays;
`baseline_refs`, `evidence_refs`, `required_gates`, and `required_reviewers`
are sorted unique stable-reference arrays. `input_hashes` is a non-empty sorted
array of exact `{path, sha256}` records. Remaining fields are non-empty strings.
Once created, a proposal file is immutable; a changed semantic input creates a
different ID/file.

The proposal ID is deterministic in v2.0 and binds the complete immutable
proposal, not only its evidence inputs. Copy every proposal field except
`proposal_id`; normalize every input/affected/patch path to Registry R3 POSIX
form; sort `input_hashes` by canonical JSON bytes and every already-set-like
path/ref/gate/reviewer array by its canonical value; then serialize UTF-8 JSON
with sorted keys, compact separators, and one terminal LF. ID is `proposal-`
plus the first 20 lowercase hex characters of that payload's SHA-256. Array
order and input path separators are non-semantic; any change to identity,
timestamps/windows, evidence, hypothesis, action paths/scope, class, gates,
reviewers/authority, observation, or rollback changes identity. v2.2 may
automate mining but cannot redefine this identity.

`policy_hash` is the lowercase SHA-256 of one canonical JSON graph containing
exactly `{policy, closer_authority, required_signals}`. `policy` is the complete
closed current policy object; `closer_authority` is the complete closed authority
object selected by `closer_authority_ref`; `required_signals` contains the
complete referenced signal objects sorted by `signal_id`. Canonical JSON uses
UTF-8, sorted keys, compact separators, and one terminal LF. Thus the hash binds
the transitive authorization/evidence policy rather than accepting an arbitrary
64-hex claim.

Before accepting a proposal, the Catalog resolves every `affected_paths` and
`patch_scope` entry through the same canonical path/exclusion/glob algorithm as
`explain_path`. Both arrays are non-empty, patch scope is a subset of affected
paths, and every path must resolve to exactly one component. v2.0 requires the
resolved components to share one owner and policy; a cross-policy change must be
split or routed through a separately declared Class C parent policy. The
proposal owner and exact current policy revision/hash must match that resolution;
its class is exactly the highest affected component class and must be allowed by
the policy/authority; gates, reviewers, and closer authority equal the policy's
closed lists/reference. Any mismatch fails before review.

In v2.0, decisions append as one closed UTF-8 JSON object per line to
`docs/decisions/evolution-manual.decisions.jsonl`; prior bytes never change. A
record contains exactly:

`format_revision`, `decision_id`, `proposal_id`, `decision`, `decided_at`,
`policy_revision`, `policy_hash`, `closer_identity`, `closer_role`,
`approval_reference`, `gate_evidence_refs`, `effective_from_run`,
`observation_status`, and `correction_of`.

`decision` is `approved`, `rejected`, `withdrawn`, `rolled_back`, or
`observation_closed`. `observation_status` is `not_started`, `observing`,
`measured`, or `unmeasured`. `correction_of` is null or a prior `decision_id`;
`effective_from_run` is a non-empty run ID for approved/rolled-back/observation
records and null for rejected/withdrawn records. `decision_id` is
`decision-<proposal-hash>-<four-digit per-proposal append sequence>`; sequences
start at `0001` with no reuse. Other IDs/refs are non-empty strings, hashes are
lowercase SHA-256, and `decided_at` is RFC 3339 UTC.
corrections append and never replace. The lifecycle is derived in append order:
no decision = review-ready; approved = observing; rejected/withdrawn = closed;
rolled_back = closed with rollback; observation_closed requires measured or
unmeasured and closes an approved proposal. Invalid transitions fail closed.

For closure, `closer_role` equals the proposal's authority ID, that authority
allows the proposal class, and one appointment matches the closer identity/role
at `decided_at`. `approval_reference` is exactly
`<appointment_id>#<proposal_id>`; fabricated, blank, future-effective, revoked,
or superseded appointments fail. The appointment is included in the policy hash
graph, and `closer_identity` must also differ from `proposer_identity`. Approved records
contain exactly one sorted `gate_evidence_refs` entry per required gate, named
`gate/<gate-id>-<stable-evidence-id>` in required-gate order. The decision's
proposal ID and exact policy revision/hash must match the immutable proposal;
otherwise closure is unauthorized.

No proposal is called successful before its observation window closes with a
realized outcome or it is marked unmeasured. Outcome reporting is stratified by
class and includes realized outcome, first-pass gate/review-round deltas,
reliable token/elapsed deltas, defect/revert rate, unmeasured rate, and time to
decision; volume/acceptance are context only.

## EV6. Extension and retirement protocol

Adding a governed root, exclusion, component class, active/proxy signal,
authority, or policy is at least the class of the behavior it can affect; format
or enforcement changes are Class C. The change must include path explanations
for positive, boundary, orphan, and ambiguity cases.

Retirement first disables new use, records replacement/succession and retention,
keeps old records interpretable, then removes producers or paths only after their
compatibility/observation obligations close. Retiring a signal cannot make old
decisions unverifiable. Retiring an authority requires a successor or blocks
affected policies.

Rollback restores the prior policy/descriptor and its generated artifacts as
one slice, preserves append-only evidence, records a corrective decision, and
never changes a historical record's policy hash or effective boundary.

## EV7. Deferred program boundaries

- 2.0 ships governed paths, component classes, generic proxies, and the manual
  explain/proposal/closure path.
- 2.1 ships telemetry v3 producers, durable export, retention/privacy rules,
  and coverage reporting. Existing append-only benchmark history is untouched.
- 2.2 may ship `kit-evolve` only after active producers exist. It may create
  proposals/candidate patches in isolation and run predeclared gates; it cannot
  approve, merge, change authority, or weaken its governing policy.
- Only at 2.2 do new records move to `evolution/proposals/` and
  `evolution/decisions.jsonl`. v2.0 evidence remains immutable in
  `docs/decisions/`; the 2.2 reader inventories both locations without moving or
  rewriting earlier bytes.
- Time-based authority remains locked until the separately approved evidence
  horizon and Class C authorization; elapsed time alone unlocks nothing.

## EV8. Diagnostics

| Code | Required condition |
|---|---|
| `EVOLUTION_ORPHAN_PATH` | Governed product path has no owner/class and no valid exclusion. |
| `EVOLUTION_OWNERSHIP_AMBIGUOUS` | More than one owner/class matches. |
| `EVOLUTION_EXCLUSION_AMBIGUOUS` | Exclusions overlap or conflict with ownership. |
| `EVOLUTION_POLICY_MISSING` | Owner/class has no resolvable policy. |
| `EVOLUTION_SIGNAL_UNAVAILABLE` | Required signal is missing or only planned. |
| `EVOLUTION_AUTHORITY_REQUIRED` | Closer absent, unauthorized, revoked, or same as proposer. |
| `EVOLUTION_CLASS_UNDERSTATED` | Declared class is below the affected component/change class. |
| `EVOLUTION_BASELINE_REQUIRED` | Required immutable baseline/input hashes absent. |
| `EVOLUTION_ROLLBACK_REQUIRED` | Required rollback note/rehearsal/evidence absent. |
| `EVOLUTION_POLICY_STALE` | Proposal/decision policy revision or hash is no longer the approved one. |
| `EVOLUTION_SELF_CERTIFICATION` | Proposal supplies its own decisive evidence or approval. |
| `EVOLUTION_OBSERVATION_OPEN` | Success claimed before measured/unmeasured closure. |

## EV9. Compatibility expectations

Policies are interpreted by their recorded revision/hash. New code must keep old
proposal/decision evidence readable for its retention window. A future format
or producer unavailable to 2.0 is explicit degradation, not silently treated as
green. Manual operation remains supported when automation is disabled.

## EV10. Review-only Python protocol sketch

```python
from typing import Literal, TypedDict

GovernanceClass = Literal["A", "B", "C"]

class GovernedRoot(TypedDict):
    path: str
    owner: str

class ExplicitExclusion(TypedDict):
    path: str
    reason: str
    owner: str

class ComponentClass(TypedDict):
    component_id: str
    path_globs: tuple[str, ...]
    owner: str
    governance_class: GovernanceClass
    policy_ref: str

class GovernedPathSet(TypedDict):
    governed_roots: tuple[GovernedRoot, ...]
    explicit_exclusions: tuple[ExplicitExclusion, ...]
    component_classes: tuple[ComponentClass, ...]

class OwnershipExplanation(TypedDict):
    path: str
    governed_root: str | None
    exclusion: str | None
    source_descriptor: str | None
    owner: str | None
    governance_class: GovernanceClass | None
    policy_revision: str | None
    required_signals: tuple[str, ...]
    required_gates: tuple[str, ...]
    required_reviewers: tuple[str, ...]
    authority_ref: str | None
    diagnostics: tuple[str, ...]

class SignalDescriptor(TypedDict):
    signal_id: str
    status: Literal["active", "proxy", "planned"]
    producer: str
    artifact_or_schema_revision: str
    quality_limitations: str
    retention: str

class AuthorityAppointment(TypedDict):
    appointment_id: str
    identity: str
    role: str
    effective_from: str
    revoked_at: str | None
    successor_of: str | None
    evidence_ref: str
    evidence_hash: str

class AuthorityDescriptor(TypedDict):
    authority_id: str
    role_type: str
    allowed_decision_classes: tuple[GovernanceClass, ...]
    allowed_closer: str
    appointments: tuple[AuthorityAppointment, ...]
    succession_rule: str
    approval_evidence_contract: str
    revocation_rule: str

class EvolutionPolicyRecord(TypedDict):
    policy_id: str
    revision: str
    owner: str
    allowed_classes: tuple[GovernanceClass, ...]
    required_signals: tuple[str, ...]
    required_gates: tuple[str, ...]
    required_reviewers: tuple[str, ...]
    closer_authority_ref: str
    rollback_evidence: str

class EvolutionCatalog(TypedDict):
    format_revision: Literal[1]
    registry_revision: str
    contract_revision: str
    governed_roots: tuple[GovernedRoot, ...]
    explicit_exclusions: tuple[ExplicitExclusion, ...]
    component_classes: tuple[ComponentClass, ...]
    signals: tuple[SignalDescriptor, ...]
    authorities: tuple[AuthorityDescriptor, ...]
    policies: tuple[EvolutionPolicyRecord, ...]

class TimeWindow(TypedDict):
    start: str
    end: str

class InputHash(TypedDict):
    path: str
    sha256: str

class EvolutionProposal(TypedDict):
    format_revision: Literal[1]
    proposal_id: str
    created_at: str
    proposer_identity: str
    policy_revision: str
    policy_hash: str
    governed_owner: str
    governance_class: GovernanceClass
    evidence_window: TimeWindow
    input_hashes: tuple[InputHash, ...]
    affected_paths: tuple[str, ...]
    baseline_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    hypothesis: str
    patch_scope: tuple[str, ...]
    required_gates: tuple[str, ...]
    required_reviewers: tuple[str, ...]
    closer_authority_ref: str
    observation_window: TimeWindow
    rollback_condition: str

class EvolutionDecision(TypedDict):
    format_revision: Literal[1]
    decision_id: str
    proposal_id: str
    decision: Literal["approved", "rejected", "withdrawn", "rolled_back", "observation_closed"]
    decided_at: str
    policy_revision: str
    policy_hash: str
    closer_identity: str
    closer_role: str
    approval_reference: str
    gate_evidence_refs: tuple[str, ...]
    effective_from_run: str | None
    observation_status: Literal["not_started", "observing", "measured", "unmeasured"]
    correction_of: str | None
```

The sketch reflects EV1–EV5 only; it does not activate deferred automation.

## EV11. Implementation task references

- Phase 1B implements governed roots, exclusions, component classes, path
  explanation, and orphan/ambiguity fixtures under EV1–EV2 and EV8.
- Phases 1B–5 classify changes with EV3–EV4 and record manual evidence under
  EV5; registry/contract work is Class C.
- Programs 2.1 and 2.2 remain bounded by EV6–EV7 and cannot use planned signals
  as evidence.
