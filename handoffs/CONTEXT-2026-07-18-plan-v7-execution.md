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
| 3 | implementation committed `92699ce`; reviews PENDING | this file §Next |
| 4, 5 | not started | — |

## Phase 3 — what exists and what remains

Committed in `92699ce`: registry-driven revision state machine in
`contract_check.py` (`Catalog.revision_model()`, R4-amended); five states
green/migration-source/partial/unsupported/unclassified; typed
`RETIRE_LEGACY` for `.cursorrules` + `ADD_RULES_POINTER` step (plan-only);
cursor `.mdc` artifact at `migration_ready`; 9 state fixtures. Gates at
commit time: pytest 133 passed/3 skipped; validate green; render --check
byte-exact; scaffold output unchanged (.cursor never emitted).

**Remaining to close Phase 3:** sequential reviews per §16 — qa-agent
(runtime attacks) → code-reviewer (static) → security-reviewer (static;
mandatory: migration/path surface) → findings fixed → regression QA →
evidence bundle `docs/spikes/phase-3/evidence.md` + scorecard line.

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
