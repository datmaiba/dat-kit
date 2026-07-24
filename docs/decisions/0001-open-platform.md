# ADR 0001: Open-platform registry and six-slot Domain Packs

- Status: accepted
- Date: 2026-07-18
- Owner and approving authority: Dat Mai Ba
- Supersedes: the 2026-07-14 flat-layout freeze in `docs/domains.md` and
  `docs/loops.md`
- Decision source: approved `PLAN-v7-platform.md`, approval record 12/12

## Context

The 2026-07-14 decision declared the flat `skills/*` layout settled and not open to revision.
That wording froze an implementation before installed-host materialization had
been tested and left software-specific policy fused into `build-loop`. It also
made the shipped `knowledge-work` pack structurally different from the flagship
software workflow.

Evidence that changed the decision:

1. Claude Code 2.1.211 and Codex CLI 0.144.4 both loaded a disposable skill in
   a fresh session and read `pack/probe.txt`, which was inside the plugin root
   but outside `skills/`. Both returned the same per-run nonce that was
   unpublished and unavailable outside the target file at execution time; the
   evidence report records its SHA-256 rather than the oracle.
2. Both hosts produced an observable missing-file failure (`File does not
   exist` on Claude, `ENOENT` on Codex), so a missing pack does not silently
   degrade into invented content.
3. The approved architecture now needs two real, conforming Domain Packs
   (`software-dev` and `knowledge-work`) behind one host-neutral work-loop
   engine. The flat layout cannot express that ownership without duplication.

The complete evidence is in `docs/spikes/phase-0b/01-host-materialization.md`.

## Decision

Adopt physical Option A: keep the reusable engine under `engine/` and Domain
Pack content under `domains/`, outside `skills/` but inside the plugin root.
Generated thin skill entrypoints remain under `skills/` and load the registered
pack. The semantic Domain Pack interface is exactly six slots:

`workflow`, `ground_truth`, `gates`, `reviewers`, `deliverables`, and
`loop_profile`.

Registry descriptors are metadata, not a seventh slot. `loop_ceiling` is a
required descriptor field and must agree with `loop-profile.md`. Registry
validation uses only the Python standard library. Greenfield initialization
remains Bash-only by consuming a generated, sanitized TSV projection. Host
Adapter artifacts follow `repo_only → migration_ready → scaffold_active →
retired`. `dat-kit 2.0` is the only green v2 project contract revision;
`dat-kit 1.16.0` is a recognized migration source that must return a nonzero
migration-required diagnostic.

Telemetry v3 remains deferred to 2.1 and governed self-evolution remains
deferred to 2.2.

## Accepted migration cost

We accept a registry and Projection Module, generated trigger and scaffold
projections, immutable v1.16 snapshots, adapter lifecycle fixtures, a staged
brownfield migration, fresh-session host smokes, and a semantic ownership
cutover of the two existing Domain Packs. Phase 4 must move one semantic owner
at a time and may not duplicate policy between the old and new locations.

## Conditions to revisit

Revisit the physical layout only if an official host update or a repeatable
fresh-session conformance test shows that a supported host no longer copies or
resolves files elsewhere inside its plugin root, or if a security review finds
that such reads cross a newly documented trust boundary. A host-specific
failure selects the Option B relocation escape hatch without changing the
six-slot interface, stable IDs, ownership, or conformance suite.

Any revisit is Class C: it needs current official-host evidence, two independent
reviews, rollback proof, and a new decision record.

## Architecture-language rule

Architecture documentation must not call a current layout “final” or
“permanent.” It may state a versioned decision, its evidence, compatibility
window, and explicit conditions to revisit. This rule applies to future
decision records, generated architecture prose, and release documentation.
