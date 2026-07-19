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
| 4a | CLOSED — ownership map, tripwire CLEAR, round-2 APPROVE (3 findings fixed) | `docs/spikes/phase-4/ownership-map.md` |
| 4b | CLOSED — engine extracted per map (work-loop/1, no bump); code + security APPROVE (3 MINOR + 1 MEDIUM/2 LOW fixed, findings-scoped re-review APPROVE); skills byte-identical | `engine/work-loop/ENGINE.md`, `engine/work-loop/engine.json`, validate.py §1b, `scripts/tests/test_engine_manifest.py` |
| 4c | CLOSED — domains/software-dev/ six slots per map (§16 R1–R4 exact sw phrasing in reviewers.md; agents/*.md stay in place, reviewers.md is the binding surface); descriptor active + rendered thin trigger byte-exact; loop-profile migrated; 24 behavioral/purity tests; code APPROVE (4 MINOR fixed) + security APPROVE (1 MEDIUM frontmatter-injection guard in render.py + 2 LOW fixed, findings-scoped re-review APPROVE) | `domains/software-dev/`, `scripts/tests/test_software_dev_pack.py`, validate.py §3b |
| 4d | CLOSED — domains/knowledge-work/ six slots per map (A→G playbook + engine-phase correspondence in workflow.md with the PLAN approval stop bound at B, no plan reviewer declared; §16 R1–R4 exact kw phrasing in reviewers.md, prose format — no charter-table rows, fact-checker has no agents/ charter; loop-profile absorbs SKILL.md L47–49, Goal human-run ceiling mirrored in descriptor); descriptor active + rendered thin trigger byte-exact (description keeps "write a researched report" for trg-knowwork-01); six legacy files deleted from skills/knowledge-work/; 17 behavioral/purity tests; code APPROVE (1 MINOR fixed) + security APPROVE (1 LOW Unicode line-break guard in render.py fixed, findings-scoped re-review APPROVE) | `domains/knowledge-work/`, `scripts/tests/test_knowledge_work_pack.py` |
| 4e–4f, 5 | not started — 4e next (domain-builder rewrite + synthetic pack) | — |

4b deferrals/flags for later slices: docs/loops.md L7 rewrite (five-slot →
six-slot, domains/ paths) deferred to 4f — map §9 tags it "4b/4f" but the
domains/ layout doesn't exist until 4c/4d, so rewriting now would state
falsehoods. Security LOW flag for the platform owner: engine-work-loop sits at
class B/maintainer-policy while contract surfaces are class C — revisit at 4f
conformance. domain-pack.md DP2 phase list aligned to map convention 5 names
(FRAME → SELF-QUESTION, + REPORT); one-line Class C-surface edit, flagged for
owner blessing via this commit. 4d note: engine PLAN's attended approval stop
has no kw phase-B counterpart — workflow.md's correspondence must address it.

4c deferrals/flags for later slices: validate.py §3b now resolves reviewer
tables for ACTIVE domains via `<pack_location>/reviewers.md` (legacy still via
trigger SKILL.md) and only probes names matching `[a-z][a-z0-9-]*` — 4d: kw
reviewers.md has no `| \`` table rows today; if 4d adds one, only real
agents/*.md names or non-matching ids are safe. render.py now rejects
multi-line/control-char trigger descriptions (frontmatter-injection guard) —
4e's domain-builder rewrite must inherit this constraint when authoring
descriptors. The sw trigger description was rewritten for the rendered
frontmatter; skill-eval `trg-buildloop-01` ("run the build loop") keys on it —
any future description edit must keep that phrase. docs/domains.md got a
minimal truth-fix (six-slot wording, sw row); full re-derivation stays 4f.
Transient note: commits C2 (pack) and C3 (descriptor+trigger) briefly
duplicate sw policy across old/new locations within the slice — revert unit is
the whole 4c slice, not C2 alone.

4d deferrals/flags for later slices: MARKER DECISION (map row 19c) — the last
bare "Contract files live beside this one." instance retired at 4d with the
kw SKILL.md replacement, earlier than the map's "survive to 4f" note; that
note is internally in tension with map §3 L1–15 (the 4d-rendered thin trigger
cannot carry policy per DP5). Decision: validate.py §2b is vacuous from 4d
(green mechanically — it matches no file); the detection MECHANISM (validate.py
§2b code + domain-builder SKILL.md L37 authoring rule) survives untouched
until 4f's registry-conformance cutover. 4f still removes the mechanism, and
must NOT treat "no marker instances" as the retirement already done. Pinned in
test_no_bare_pack_marker_remains_but_the_mechanism_survives. Security INFO
(pre-existing, fold into 4f): §2b silently skips a hand-authored legacy pack
missing the exact marker sentence. render.py's field guard now also rejects
U+0085/U+2028/U+2029 via shared UNSAFE_FIELD_CHARS (both trigger-description
and manifest guards) — one-line Class C-surface edit flagged for
platform-owner blessing (commit 300c7fb); 4e's domain-builder rewrite inherits
this constraint. Eval trg-knowwork-01 keys on "write a researched report" in
the kw trigger description — any future description edit must keep it.
ENGINE.md's kw A→G correspondence table and domains/knowledge-work/workflow.md's
table are row-identical after a code-review fix — 4f's deletion test can key on
either. docs/domains.md got a minimal truth-fix (kw row, both-packs paragraph);
docs/contracts/examples/domains.example.json still shows kw legacy — examples
re-derivation stays 4f (evolution.example.json already matched the 4d glob).
Transient note: commits C2 (pack) and C3 (descriptor+trigger) briefly
duplicate kw policy across old/new locations within the slice — revert unit is
the whole 4d slice, not C2 alone.

## Next: Phase 4 — isolated structural cutover, SPLIT INTO SIX SLICES

Prerequisite reading per session: plan §6 Phase 4 + §16 + this file only.
One slice per session-budget (~50–80k each); each commits by semantic owner
and reverts alone; NO partial six-slot claim reaches master. §16 rules 1–4
must land in both domains' reviewers.md via the map (rule carried from §16).

- **4a — Ownership map (read-only doc).** Line-level map over
  skills/build-loop/SKILL.md + loop-profile.md, skills/knowledge-work/*
  (SKILL.md + 5 slots), docs/loops.md, reviewer tables, domain-builder,
  templates: every substantive line → engine | domain-pack |
  project-contract | maintainer-policy | retired-with-reason. Output
  docs/spikes/phase-4/ownership-map.md. Independent tripwire review BEFORE
  any move (any engine line requiring domain knowledge = STOP). Est 60–90k.
- **4b — Engine extraction.** engine/work-loop/ENGINE.md (LOAD→…→HARVEST,
  host-neutral, per map only) + engine revision in registry + composition/
  contradiction rules. No skill file moves yet. Est 40–60k.
- **4c — software-dev pack.** domains/software-dev/ six slots per map;
  descriptor → active; rendered thin trigger replaces build-loop body;
  behavioral before/after tests (normal, autopilot, delegated, security,
  recovery, harvest). Est 70–100k.
- **4d — knowledge-work pack.** domains/knowledge-work/ six slots
  (workflow.md absorbs A→G playbook; 5 slot files migrate; loop-profile
  keeps Goal-human-run ceiling mirrored in descriptor); rendered trigger;
  report + fact-check path tests before/after. Est 50–80k.
- **4e — domain-builder rewrite + synthetic pack.** Authors descriptor + six
  slots + rendered trigger + inherited evolution profile; synthetic
  non-software pack completes the engine lifecycle; alias-collision and
  negative trigger evals. Est 40–60k.
- **4f — Cutover closure.** Engine deletion test (no domain policy left),
  replace sentence-marker pack detection with registry conformance,
  docs/examples re-derived, templates flip AGENTS.md marker → "dat-kit 2.0"
  (greenfield becomes green under the v2 checker), full sequential reviews
  of the whole cutover, evidence + scorecard. Est 60–90k.

Phase 3 follow-ups FU-1..3 live in docs/spikes/phase-3/evidence.md — fold
FU-1 (marker hardening) into 4f if budget allows, else keep tracked.

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
