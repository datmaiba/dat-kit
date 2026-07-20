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
| 4e | CLOSED — domain-builder rewritten per map §10 (descriptor + six slots + rendered trigger + inherited evolution profile; scope boundary and capability ladder dedup to docs/loops.md as canonical; interview extended with descriptor + evolution questions and maps onto ENGINE.md's full declare-list; gate-validity semantics unchanged; registration step added with DP5 fresh-session evidence rule; 4c/4d constraints encoded: single-line descriptions incl. CR + U+0085/U+2028/U+2029, pinned eval phrases, §3b reviewer-row rule, alias collision); synthetic ledger-close pack FIXTURE-ONLY completes the engine lifecycle (Catalog → engine-revision check → six slots in DP1 order, files actually load, alias/destination collision + authority/governance + missing/stale trigger all fail closed, no dispatch edit — DP6); code APPROVE (1 MAJOR + 2 MINOR + 2 INFO fixed, findings-scoped re-review APPROVE) + security APPROVE (1 LOW charset pin fixed, findings-scoped re-review closed) | `skills/domain-builder/SKILL.md`, `scripts/tests/test_domain_builder_pack.py` |
| 4f | CLOSED — cutover closure: engine deletion test (dynamic half; keyed on the kw A→G correspondence, pinned row-identical ENGINE.md ↔ workflow.md); sentence-marker detection retired SINGLE FIRE (validate.py §2b + domain-builder quoted note in one commit; marker test final form — sentence nowhere on operative surfaces, archival prefixes excluded); docs/loops.md L7 six-slot rewrite + docs/domains.md re-derived + domains.example.json active rows (phase-1a example validator re-derived same commit); templates flip DEFERRED to Phase 5 by platform-owner decision (live template is hash-pinned as the v1.16 record — see 4f flags); whole-cutover sequential reviews over b41f242..HEAD: code APPROVE (1 INFO) + security APPROVE (1 LOW fixed fe7ced8, findings-scoped re-review APPROVE; 1 INFO rolled) | `docs/spikes/phase-4/evidence.md` |
| **Phase 4** | **CLOSED** — all six slices closed; plan §6 Exit criteria proven in the evidence bundle | `docs/spikes/phase-4/evidence.md` |
| 5a | CLOSED — atomic templates flip landed (2.0 snapshot + descriptor hashes + adapter rows + marker + tsv, D-5a-1 "historical = record" registry semantics with registry.md R6 amendment); FU-1 closed; 4f alias-embed security INFO closed; greenfield GREEN under v2 checker; 1.16 snapshot byte-identical; code + security APPROVE (0 actionable) | `docs/spikes/phase-5/evidence.md`, commits `d1e9d14..ede8670` |
| 5b | CLOSED — format freeze (R9 statement + pin test, D-5b-B) + release_version 2.0.0 (D-5b-A, mirrored ×3); render byte-check no-op; suites 275+3; Linux clean-install smoke green (incl. idempotent rerun); clean + customized v1.16 fixtures migrated via --migration-plan → checker exit 0 with custom policy preserved; 3 approved 5a lessons appended; code APPROVE (1 MINOR, 1 INFO) + security APPROVE (0 findings) | `docs/spikes/phase-5/evidence.md` §5b, commits `6181816..024882b` |
| 5c | CLOSED — step 9 live rollback rehearsal to v1.17.1 (D-5c-A: worktree tooling vs 2.0 + 1.16 project dirs; fail-closed named diagnostics, every byte preserved, forward-migratability intact, v1.17.1 validate green) + step 10 docs sweep (D-5c-B full README/HUONG_DAN rewrite with §9.4-dated per-host table; codex.md folded into adapters/codex/ADAPTER.md + load-bearing redirect stub; domains/loops verified already 0001-compliant, no edit); code APPROVE (0 actionable, 2 INFO) + security skip stated (pure docs + read-only rehearsal) | `docs/spikes/phase-5/evidence.md` §5c, commits `e751d5f..a6a1be6` |
| 5 (rest) | OPEN — steps 6 (external), 8 RC bundle (per D-5c-C: only after external gates return), 11 migration guide + tag; external halves of 5 (Windows smoke) and 7 (real project) | — |

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

4e deferrals/flags for later slices: MARKER DECISION RESOLVED — the rewritten
domain-builder keeps ONE quoted legacy note ("validate.py still detects old
five-slot packs via the sentence …"); §2b stays vacuous, no bare marker
anywhere, and 4f removes validate.py §2b + that note in a SINGLE fire (the
kw marker test's comment pins this; 4f must not treat the quoted note as a
second retirement). SYNTHETIC PACK DECISION — fixture-only: ledger-close
(bookkeeping) lives entirely in scripts/tests/test_domain_builder_pack.py on
the registry fixture; DP6 asks for a synthetic/non-software *fixture* and the
plan's "installed Claude/Codex pack reads" is an external host smoke (Phase 5
step 6), so nothing was committed to registry/, evolution.json, or domains/ —
4f/5 must not expect a committed ledger-close pack. The 4e tests prove BOTH
evolution fail-closed halves (EVOLUTION_AUTHORITY_REQUIRED at Catalog.load;
EVOLUTION_ORPHAN_PATH via validate_governed_inventory) — reusable for 4f's
registry-conformance cutover. Pinned eval phrases are now asserted against
benchmarks/skill-evals.jsonl (test_pinned_eval_phrases_still_come_from_the_
eval_corpus) — a phrase change in the eval corpus breaks the pin loudly.
UNSAFE_FIELD_CHARS literal is pinned in the same file (security LOW fix) —
extending the guard charset at 4f+ requires updating that pin in the same
commit. Still 4f: docs/loops.md L7 rewrite, docs/contracts examples
re-derivation, §2b mechanism removal, engine deletion test, FU-1 marker
hardening fold-in.

4f deferrals/flags → Phase 5: TEMPLATES FLIP DEFERRED (platform-owner
decision 2026-07-19) — templates/common/AGENTS.md is hash-pinned as the
v1.16 record in TWO places (snapshot `expected_content_hash` +
platform.json 1.16 descriptor `static_template_hashes`); flipping the
marker alone raises REGISTRY_SNAPSHOT_HASH_MISMATCH ×2 and fails 17 tests
(verified live, then reverted — no residue, confirmed by
`git diff --name-only b41f242..HEAD` containing no templates/ or
registry/platform/snapshot paths). The correct flip is ONE atomic Phase 5
registry change (steps 1–3): project-contract-2.0 snapshot + 2.0 descriptor
static_template_hashes + adapters.json project_contract_revision rows +
the template marker itself; until then greenfield scaffolds stay
1.16-marked and migratable — never silently mixed. FU-1 (contract_check.py
fence/anchor-aware marker matching) stays tracked: same surface as the
flip, do them together. Security INFO (pre-existing, render.py): trigger
`aliases` embed into the generated SKILL.md body WITHOUT the
UNSAFE_FIELD_CHARS check the description gets — close the asymmetry in
Phase 5, updating the 4e charset pin test in the same commit if the guard
charset changes. Code-review INFO: test_engine_deletion.py hard-codes
exactly the two cutover packs and needs a live git repo — registering a
third pack must update that assertion. Class C blessings (DP2 edit,
frontmatter guard, UNSAFE_FIELD_CHARS 300c7fb, engine stays class
B/maintainer-policy) + the 4d security INFO (§2b silent-skip, moot):
discharged in `docs/spikes/phase-4/evidence.md`. Review-range note:
whole-cutover reviews ran b41f242..HEAD — d76c179 is the 4c CLOSE commit,
so the dictated range would have dropped 4b/4c implementation from review.

5a deferrals/flags → later Phase 5 slices: D-5a-1 (2026-07-19) changed
registry semantics — historical snapshots verify descriptor↔snapshot
consistency only and never scaffold; `scaffold_file_plan` draws snapshot
rows from the CANONICAL revision's snapshot only (registry.md R6 amended,
Class C blessed via the decision). Any future revision cutover authors a
new canonical snapshot and demotes the old one to historical — never edits
a historical snapshot. `scaffold_v116_contract` (test_contract_check.py) is
now the frozen 1.16 fixture; `scaffold_contract` scaffolds the CURRENT
templates (green v2). init.sh rerun is now truly idempotent
(test_canonical_rerun_is_readonly_and_idempotent). Marker matching is
fence/inline-code-aware (FU-1) — prose mentions still count, pinned by
test_mixed_markers_are_partial; keep `_marker_scan_text` strictly
subtractive (must never emit new substrings — false-green guarantee).
render.py guards ALL body fields with the unchanged UNSAFE_FIELD_CHARS pin.
Three lesson candidates await owner approval in the 5a evidence §last.
Still with later slices: release_version bump (platform.json still
"1.17.1"), format freeze, RC bundle, rollback rehearsal, docs sweep
(README/HUONG_DAN still describe 1.16 scaffolds where applicable), tag.

5b deferrals/flags → later Phase 5 slices: 5a lesson candidates RESOLVED
(all 3 approved + appended, `6181816`). Format freeze is BINDING from 5b
(registry.md R9 + `scripts/tests/test_format_freeze.py`): any
format_revision bump, canonical-revision change, or green/migratable list
edit before the v2.0.0 tag reopens the release train and must update BOTH
the R9 statement and the pin test in one commit. release_version is
"2.0.0" everywhere (platform.json + 3 mirrors) — the rollback rehearsal
(step 9) must prove reverting to v1.17.1 tooling against this state.
Code-review INFO rolled: freeze coupling is docs→test only (deleting the
pin test is not mechanically caught). Migration-apply is proven by live
fixture transcripts in evidence §5b, not by a pin test — mechanizing it is
an optional later-slice candidate. Docs sweep (step 10) now also owns the
stale "1.17.1" citations in README/HUONG_DAN/docs/codex.md. External
halves still open: Windows Git Bash clean-install smoke (step 5), one real
v1.16 project migration (step 7), live host smokes (step 6).

5c deferrals/flags → later Phase 5 slices: D-5c-C BINDS — RC bundle (8)
opens only after the external gates return (Windows Git Bash smoke, real
v1.16 project migration, Actions runs, live host smokes), so the RC
evidence bundle is complete; then migration guide + tag (11). The
`docs/codex.md` redirect stub is LOAD-BEARING: current scripts AND
rolled-back v1.17.1 tooling print "see docs/codex.md" (rehearsal run D) —
never delete it while v1.17.1 remains the rollback target. Rolled INFOs
for the RC window: one-way freeze coupling (5b); Gemini
`repo_only`-vs-declared-GEMINI.md-`project_artifact` registry quirk (5c
code review) — reconciling it touches frozen registry surfaces, so it
requires the R9 freeze-amendment procedure (statement + pin test, same
commit). One 5c lesson candidate (lifecycle-label vs artifact-list
contradiction needs a conformance check, not per-adapter prose) awaits
owner approval in evidence §5c. Docs sweep is DONE — steps 9 + 10 closed;
README/HUONG_DAN/ADAPTER.md are now the 2.0 truth surfaces; keep future
edits consistent with `registry/adapters.json` official_facts dates.

## Phase 4 — isolated structural cutover, SPLIT INTO SIX SLICES (all CLOSED)

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
