# Active context — plan v7 execution (SUPERSEDES both 2026-07-18 predecessors)

**Status:** active execution context for `feature/open-platform-v2`
**Written:** 2026-07-18, Cowork session (Mac), after Phase 3 implementation commit
**Supersedes:** `CONTEXT-2026-07-18-lean-dat-kit-improvement.md` (state facts
stale) and `HANDOFF-2026-07-18-token-discipline-portable.md` (§B patches now
committed — never reapply). Their protocol content survives as plan §16
(amendment v7.1) + scope-discipline blocks in `agents/*.md` — read THOSE, not
the predecessors.

## Corrections to the superseded files (do not trust their state sections)

- Phase 1B is NOT parked WIP: it is CLOSED — implemented, three-review round
  passed, evidence `docs/spikes/phase-1b/evidence.md`, scorecard appended.
- The `SCAFFOLD_MANIFEST_INVALID: bad provenance header` failure was cp1252
  mojibake in `init.sh`, fixed in `f8395cc`. Not reproducible.
- Phase 2 is CLOSED repo-side: `docs/spikes/phase-2/evidence.md`. Live host
  smokes remain OPEN external gates (checklists inside each ADAPTER.md).
- The user explicitly re-authorized full plan execution to v2.0.0 in this
  session; the "do not resume Phase 1B" boundary is obsolete.

## Phase status (branch feature/open-platform-v2)

| Phase | State | Evidence |
|---|---|---|
| 0A v1.17.1 | done, tagged, both branches cut from it | tag `v1.17.1` |
| 0B | done — Option A chosen | `docs/decisions/0001…`, `docs/spikes/phase-0b/` |
| 1A | done — 4 contracts + examples | commit `7e26541` |
| 1B | done + reviewed | `docs/spikes/phase-1b/evidence.md`, commits `dbe42db..1e409de` |
| 2 | done repo-side; host smokes = external | `docs/spikes/phase-2/evidence.md`, `eae1ca5..55dfa2c` |
| v7.1 | token-discipline amendment committed | `7c06383`, plan §16 |
| 3 | CLOSED — impl `92699ce`, reviews 3/3 APPROVE, fixes `89f63d2` | `docs/spikes/phase-3/evidence.md` |
| 4, 5 | not started | — |

## Next: Phase 4 — isolated structural cutover (the heaviest phase)

Prerequisite reading for the executing session: plan §6 Phase 4 + §16 only.
First deliverable is the LINE-LEVEL OWNERSHIP MAP over: skills/build-loop/
SKILL.md (+loop-profile.md), skills/knowledge-work/* (SKILL.md + 5 slot
files), docs/loops.md, agents/*.md tables, templates — every substantive
line → engine | domain-pack | project-contract | maintainer-policy |
retired-with-reason. The map is independently reviewed BEFORE any move
(tripwire: engine line requiring domain knowledge = stop). §16 rules 1–4
must land in both domains' reviewers.md via the map. Then: engine/work-loop/
ENGINE.md; domains/{software-dev,knowledge-work}/ six slots; descriptors →
active; triggers rendered; domain-builder rewrite; behavioral tests;
commit-by-semantic-owner. Phase 3 follow-ups FU-1..3 live in
docs/spikes/phase-3/evidence.md.

## Standing execution rules (do not re-derive)

Plan §16 (v7.1) governs: sequential diff-scoped reviewers with the dispatch
template, pasted gate outputs, ≤30-line reports, findings-scoped re-reviews,
no PoC outside qa-agent, grep-before-read, resume-from-handoffs. Slice budget
~50–80k tokens, checkpoint at 70%. Security review fires on registry/
migration/public-input/path surfaces. Evidence bundles follow the compact
shape used in `docs/spikes/phase-{1b,2}/evidence.md` (manual receipts; the
gate-runner stays an unimplemented Class C design — see superseded context).

## Known machine quirks (this Mac / Cowork sandbox)

- Mount denies unlink until Cowork grants delete permission; git may report a
  transient "corrupt loose object" mid-commit — retry the commit; fsck clean.
- `plans/PLAN-v7-platform.md` file mode may be read-only after copy from
  uploads (chmod u+w before editing).
- Hosts (claude/codex/cursor/gemini CLIs) are NOT installed here: all live
  host smokes are external gates for the maintainer.

## External gates open for the maintainer (blocking v2.0.0, not Phase 3/4)

1. Push branch; verify real Actions runs (Ubuntu + Windows jobs) on GitHub.
2. Live host smokes per ADAPTER.md checklists (claude-code, codex; manual
   evidence for cursor/gemini).
3. Release-train steps of Phase 5 (RC bundle, rollback rehearsal, tag).
