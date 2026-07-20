# Phase 4 evidence bundle — isolated structural cutover to six-slot Domain Packs

Date: 2026-07-19 · Branch: `feature/open-platform-v2`
Slices: 4a `b41f242` → 4b `b174314..` → 4c `..d76c179` → 4d `..09694ef` →
4e `..b3858e7` → 4f (this bundle). Environment: Linux sandbox (Cowork,
Windows mount), Python 3.10.12.

## Gates (4f close)

| Command | Result |
|---|---|
| `python3 -m pytest scripts/tests -q` | 254 passed, 3 skipped |
| `python3 scripts/validate.py` | ✓ all checks green |
| `python3 scripts/render.py --check` | exit 0, byte-exact |
| `python3 scripts/spikes/phase1a/validate_contract_examples.py` | PHASE1A_CONTRACT_EXAMPLES_OK |

Red-before-green for the two gates 4f added/changed: poisoned ENGINE.md →
3 deletion-test fails; marker reintroduced into validate.py → marker test
fails. Both reverted, both green after.

## Exit criteria vs plan §6 Phase 4 (verbatim)

- **"software-dev AND knowledge-work are active six-slot packs"** — PROVEN:
  `registry/domains.json` both `lifecycle: active`, `pack_location:
  domains/<id>`; Catalog fail-closed on any missing slot
  (`DOMAIN_SLOT_MISSING`); behavioral pins in
  `test_software_dev_pack.py` (24) + `test_knowledge_work_pack.py` (17).
- **"the engine contains no domain-specific policy"** — PROVEN: static half
  `test_engine_manifest.py` FORBIDDEN purity scan; 4f dynamic half
  `test_engine_deletion.py` re-runs the scan in the deleted fixture.
- **"deletion test proves engine depth"** — PROVEN (4f):
  `test_engine_deletion.py` — both packs deleted from a registry fixture
  (descriptor rows + pack trees); unmodified engine composes through
  unmodified production modules; no engine byte changes; the binding is the
  pack-declared kw A→G correspondence, pinned row-identical between
  `ENGINE.md` and `domains/knowledge-work/workflow.md`, keyed on the engine
  phase sequence.
- **"both triggers are generated and behaviorally load their packs"** —
  PROVEN: `render.py --check` byte-exact on both `skills/*/SKILL.md`;
  pack tests resolve every file the triggers name and assert the policy
  content loads (not just names in text).
- **"synthetic pack passes"** — PROVEN: `test_domain_builder_pack.py`
  ledger-close FIXTURE-ONLY (4e decision — nothing committed to registry/,
  evolution.json, or domains/; the installed-host pack read is a Phase 5
  step 6 external smoke); full lifecycle Catalog → engine-revision check →
  six slots in DP1 order → fail-closed negatives (alias/destination
  collision, authority, orphan, missing/stale trigger), zero dispatch edits.
- **"ownership map has no unassigned or duplicate lines"** — PROVEN: map
  §Coverage check — files fully covered, one DECLARED clause-level split
  (kw L19a/b/c), each `retired-with-reason` line retired at its named slice.

## 4f deliverables

1. Engine deletion test (dynamic half) — `583a797`.
2. Sentence-marker detection retired, SINGLE FIRE — `f19f845`: validate.py
   §2b (comment + SLOT_ROW + marker regex) and domain-builder's quoted
   legacy note left in the same commit; marker test rewritten to final form
   (sentence NOWHERE on operative surfaces, validate.py included; archival
   records excluded as history). Registry conformance (Catalog load + §3b +
   render --check) is the only pack detection.
3. Docs re-derived — `0bbf2cb`: loops.md L7 six-slot rewrite per map §9
   (L44–46 scope boundary untouched); docs/domains.md full re-derivation.
   Contracts example — `2f5f8a0`: both rows active under domains/;
   phase-1a example validator re-derived in the same commit.
4. Templates flip AGENTS.md marker → "dat-kit 2.0": **DEFERRED to Phase 5
   by platform-owner decision (2026-07-19)** — the live template is
   hash-pinned as the v1.16 record (immutable snapshot
   `expected_content_hash` + platform.json 1.16 descriptor
   `static_template_hashes`); flipping alone raises
   `REGISTRY_SNAPSHOT_HASH_MISMATCH` ×2 and fails 17 tests (verified, then
   reverted). A correct flip is one atomic registry change: 2.0 snapshot +
   2.0 descriptor hashes + adapters.json revision rows — Phase 5 steps 1–3
   territory. Until then greenfield scaffolds remain v1.16-marked and
   migratable, never silently mixed.

## Class C / flagged-surface blessings (platform owner, recorded 2026-07-19)

- 4b `domain-pack.md` DP2 phase-list edit (map convention 5 names):
  BLESSED — contract text matches the shipped engine phases.
- 4c `render.py` frontmatter-injection guard (multi-line/control-char
  trigger descriptions rejected): BLESSED — fail-closed rendering guard on
  a Class C contract surface.
- 4d `UNSAFE_FIELD_CHARS` Unicode extension (NEL/LS/PS, commit `300c7fb`):
  BLESSED — charset literal pinned by
  `test_unsafe_field_charset_is_pinned`; NOT extended at 4f, pin untouched.
- 4b engine class placement revisit: DECIDED — `engine-work-loop` stays
  governance class B / `maintainer-policy` (`registry/evolution.json`). The
  engine is maintainer-owned mechanism; the Class C surfaces remain the
  contract documents that bind it, and the deletion test proves the engine
  carries no policy a pack author must negotiate with.
- 4d security INFO (§2b silently skipped hand-authored legacy packs missing
  the marker): DISCHARGED as moot — §2b removed at `f19f845`; detection is
  registry conformance, which fails closed instead of skipping silently.

## Known limitations / rolled forward

- Templates flip + greenfield-green-under-v2: Phase 5 (owner decision above).
- FU-1 marker-parsing hardening (contract_check.py, fence/anchor-aware):
  kept tracked (phase-3 evidence) — its surface (revision-marker matching)
  is unchanged by 4f and belongs with the Phase 5 flip work.
- Installed Claude/Codex pack reads: external host smokes, Phase 5 step 6.
- Live host smokes for adapters: unchanged external gates (ADAPTER.md).

## Review

Whole-cutover sequential reviews (code → security) over `b41f242..HEAD`
(4b through 4f; the 4c-close hash `d76c179` would drop 4b/4c
implementation). Verdicts recorded in the 4f handoff block.
