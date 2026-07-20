# RC1 — dat-kit 2.0.0 release candidate evidence bundle

**Plan reference:** PLAN-v7 §6 Phase 5 step 8 · shape per §9.3 · acceptance
criteria per §13.1 · reviews per §16.
**RC commit:** `802e21c` (the bundle commit; RC tree = the fix-up commit that follows it) on `feature/open-platform-v2`.
**Prepared:** 2026-07-21, Windows Cowork sandbox (suites on an rsync'd local
copy per the 5a machine-quirk protocol; edits + git in the mounted repo).

This bundle is an **aggregator, not a re-claim**. Every row below cites the
underlying receipt — the per-slice sections of `docs/spikes/phase-5/evidence.md`
and the earlier phase bundles remain the primary evidence. Where this document
states a result, it is either (a) a citation, or (b) a check re-run at RC time
and labelled as such. Nothing here is restated as a fresh claim.

RC1 is an **evidence bundle, not a version string**: `release_version` is
`2.0.0` with no `-rc` suffix, by decision D-5b-A, because Phase 5 Exit requires
"RC artifact equals tagged artifact".

## Decisions governing this RC

| ID | Decision | Owner-confirmed |
|---|---|---|
| D-RC-A | Open RC1 now with the **Cursor manual checklist recorded as a named known limitation**, to be closed before the `v2.0.0` tag. §13.1 does not require Cursor live evidence, and `adapters/cursor/ADAPTER.md` states no scriptable headless Cursor exists — this is a manual checklist, not an automated gate. | 2026-07-21 |
| D-RC-B | **Verify every §13.1 item** against a named artifact/test/evidence citation, recording the receipt per item; an item that cannot be closed is a STOP, not a soft note. | 2026-07-21 |
| D-RC-C | **Approve all four pending lesson candidates** (3 from 5-ext, 1 from 5c) and append them first, in their own commit. | 2026-07-21 |
| D-RC-D | **Gemini registry quirk stays a documented known limitation**, fixed after the tag — the fix edits frozen registry data and would require the R9 freeze-amendment procedure, reopening the release train. | 2026-07-21 |

Prior binding decisions carried in, not re-litigated: D-5a-1 (canonical vs
historical snapshot roles), D-5b-A (`2.0.0`, no rc suffix), D-5b-B (format
freeze), D-5c-A/B/C (rollback rehearsal, docs sweep, RC-after-external-gates).

## 1. Commit and revision state

| Item | Value |
|---|---|
| Branch | `feature/open-platform-v2` |
| RC commit | `802e21c` (bundle) + the review fix-up commit that follows |
| Baseline for this session | `ab6abb0` (session order) on `222cac6` (external-gate evidence) |
| Commits since `v1.17.1` | 62 |
| `format_revision` | `1` (FROZEN — registry.md R9) |
| `registry_revision` | `platform/1` |
| Child revisions | `domains/1` · `adapters/1` · `evolution/1` |
| Contract revisions | `domain-pack/1` · `host-adapter/1` · `evolution/1` |
| Engine revision | `work-loop/1` |
| `canonical_revision` | `dat-kit 2.0` |
| `green_revisions` | `["dat-kit 2.0"]` |
| `migratable_source_revisions` | `["dat-kit 1.16.0"]` |
| `unsupported_revisions` | `["pre-marker", "unknown"]` |
| `release_version` | `2.0.0` (platform.json + 3 mirrored targets) |

Format-freeze compliance for the RC diff itself. The RC diff is `222cac6..802e21c`,
exactly two commits and exactly two files:

- `bdf2a00` — `lessons-learned/lessons-learned.md` (4 approved entries appended)
- `802e21c` — `docs/spikes/phase-5/rc1-bundle.md` (this file, new)

**No `registry/`, `templates/`, or `scripts/` path is in the diff**, so R9 is
not engaged and the release train is not reopened. (The review verdict in §10,
the evidence pointer, and the scorecard land in a following commit — they are
review/harvest output about this RC, not part of the reviewed artifact, and they
touch no frozen surface either.)

## 2. Commands and exit codes (re-run at RC time)

Run on the rsync'd copy of the RC tree, 2026-07-21:

| Command | Result | Exit |
|---|---|---|
| `python3 -m pytest scripts/tests -q` | **275 passed, 3 skipped** | 0 |
| `python3 scripts/validate.py` | `✓ all checks green` | 0 |
| `python3 scripts/render.py --check` | (silent; byte-exact) | 0 |
| `python3 scripts/registry.py explain-evolution domains/software-dev/workflow.md` | governed; owner `software-dev`, class **B**, closer `software-dev-reviewer`, gate `software-regression` | 0 |

278 tests collected; 275 pass, 3 skip. The counts match every prior Phase 5
slice (5b, 5c, 5-ext) — this RC adds no tests because it adds no code.

**Authoritative cross-platform proof is not this sandbox** but the real GitHub
Actions run [`29744500620`](https://github.com/datmaiba/dat-kit/actions/runs/29744500620)
on `ba77045` — jobs `validate` (13s) and `windows-python` (53s) both green.
See evidence § External gates → Gate 1.

## 3. Projection check

`render.py --check` exit 0 — byte-exact, never repairing
(`test_projection_check_is_byte_exact_and_never_repairs`). Projection
destinations from `expected_outputs()`: `templates/common/.dat-kit-files.tsv`
plus `skills/<trigger>/SKILL.md` for each active domain
(`skills/build-loop/SKILL.md`, `skills/knowledge-work/SKILL.md`). All three are
pinned `eol=lf` in `.gitattributes` as of `ba77045` — the fix for the Windows
checkout defect Gate 1 surfaced.

## 4. §13.1 — v2.0.0 Definition of Done matrix (per D-RC-B)

**Item-count note:** `handoffs/SESSION-ORDER-2026-07-21-rc-bundle.md:110` refers
to a "14-item" checklist; `plans/PLAN-v7-platform.md:880-905` as written contains
exactly **13** checkbox items (confirmed independently by code review, row texts
matching in order). The discrepancy is recorded **here** — the order document was
not edited to match. 13 is correct; all 13 are verified below.

| # | §13.1 item | Status | Receipt |
|---|---|---|---|
| 1 | v1.17.1 exists; both long-lived branches start from it; 1.x install route demonstrated live on both hosts | **PASS** | Tag `v1.17.1` present; `git merge-base --is-ancestor v1.17.1 <branch>` true for **both** `feature/open-platform-v2` and `release/1.x` (re-verified at RC time). Live 1.x route: `docs/spikes/phase-0b/01-host-materialization.md` — "Existing dat-kit 1.17.1 install: enabled from the `release/1.x` marketplace route" recorded for **Claude Code 2.1.211** (§Claude Code) *and* **Codex CLI 0.144.4** (§Codex CLI). Demonstrated, not asserted. |
| 2 | Decision record 0001 merged; "final/permanent" wording removed from docs | **PASS** | `docs/decisions/0001-open-platform.md` present (with `0002-authority-appointments.md`). Wording sweep re-run at RC time: `grep -niE '\b(final\|permanent)\b' docs/domains.md docs/loops.md` → **zero matches**. Closure recorded in evidence §5c Deliverable 2 (verified-compliant, no edit needed). |
| 3 | Normative registry, evolution, Domain Pack, Host Adapter contracts approved | **PASS** | All four exist: `docs/contracts/{registry,evolution,domain-pack,host-adapter}.md`. Approval: PLAN-v7 §14 Approval record 2026-07-17, all twelve questions **approve** (Q3 adapter lifecycle, Q4 six slots normative). Phase 1A commit `7e26541`. |
| 4 | Registry bootstrap rejects malformed/old/unknown/future/mixed formats deterministically | **PASS** | `scripts/tests/test_registry_fail_closed.py` (7 tests) + `test_registry_catalog.py`: `test_future_bootstrap_fails_before_missing_child_is_read`, `test_unknown_descriptor_field_has_json_path`, `test_mixed_code_and_child_format_fails_atomically`, `test_malformed_children_always_produces_diagnostics`, `test_symlinked_registry_child_is_rejected_fail_closed`. Named diagnostics, no tracebacks. |
| 5 | Registry Catalog owns component inventory; Projection output deterministic and byte-exact checked | **PASS** | Catalog: `test_current_catalog_is_atomic_and_cutover_state_matches_plan`, `test_catalog_results_are_defensive_copies`, `test_fileplan_scaffold_rows_come_only_from_the_canonical_snapshot`. Projection: `test_projection_check_is_byte_exact_and_never_repairs`, `test_missing_descriptor_owned_projection_fails_byte_exact_check`; `render.py --check` exit 0 §2 above. |
| 6 | Greenfield Bash initialization consumes the generated sanitized manifest | **PASS** | `scripts/init.sh:86 materialize_manifest()` reads `templates/common/.dat-kit-files.tsv` — the exact `MANIFEST_PATH` emitted by `render.py:22` / `render_scaffold_manifest()` — and validates **every row** through the allowlist `validate_manifest_path()` before publishing any file. Live: Gate 2 Windows Git Bash clean install, 17 files created, exit 0 (evidence § External gates → Gate 2); Linux equivalent evidence §5b step 5. |
| 7 | A synthetic Host Adapter requires no validator or shell edit; a synthetic non-software Domain Pack composes through the engine | **PASS** | Adapter: `test_synthetic_adapter_template_reaches_manifest_without_shell_edit`; domain: `test_synthetic_registry_only_domain_renders_without_python_change` (both `test_registry_render.py`). Non-software pack composition: the **ledger-close** (bookkeeping) fixture, `test_end_to_end_dry_run_catalog_engine_check_six_slots_in_dp1_order` + `test_engine_revision_mismatch_is_the_composition_stop` (`test_domain_builder_pack.py`). Fixture-only by the 4e decision — nothing committed to `registry/` or `domains/`. |
| 8 | Software-dev AND knowledge-work are active six-slot Domain Packs; both triggers generated and behaviorally load their packs | **PASS** | Registry (re-read at RC time): both descriptors `lifecycle: active`, `pack_location` `domains/software-dev` / `domains/knowledge-work`, triggers `build-loop` / `knowledge-work`. Six slots present on disk in both packs. Mechanical: `test_software_dev_pack.py` (12 tests) + `test_knowledge_work_pack.py` (15), incl. `test_trigger_is_generated_and_resolves_every_named_file`. **Behavioral, live**: Gate 4 — Claude Code loaded `dat-kit:build-loop` and read pack content outside `skills/`; Codex session JSONL confirms it read all six software-dev slot files + `engine/work-loop/{ENGINE.md,engine.json}` (evidence § External gates → Gate 4). |
| 9 | Every domain descriptor declares a `loop_ceiling` consistent with its loop-profile; ceiling changes are Class C | **PASS (with INFO)** | Both descriptors declare `loop_ceiling: "Goal"` (re-read at RC time). Profiles agree: `domains/knowledge-work/loop-profile.md:4` ("Domain ceiling: Goal (human-run) — mirrored in the descriptor's `loop_ceiling`") and `domains/software-dev/loop-profile.md:20` ("**Goal.** No build-loop task safely unlocks Time or Proactive yet"; §heading at :18). `loop_ceiling` is a required member of `DOMAIN_KEYS` (`scripts/registry.py:233`), so an absent/unknown field fails closed. Class C governance: PLAN-v7 §8 + §13.1. **INFO:** the descriptor↔profile *link* is test-pinned for knowledge-work only — `test_knowledge_work_pack.py:49,163,164,169` asserts both `descriptor["loop_ceiling"] == "Goal"` and the profile's mirroring sentence. `test_software_dev_pack.py:63` pins the profile's ceiling sentence but **no test anywhere asserts the software-dev descriptor's `loop_ceiling` value**, so the two halves are not tied together for that domain; the agreement was verified by reading both artifacts at RC time. See Known limitations §6. |
| 10 | `AGENTS.md` remains the only generated-project policy owner; initial adapters are thin and lifecycle-governed | **PASS** | All four adapters declare `policy_prohibition.canonical_owner: "AGENTS.md"` with forbidden categories (re-read at RC time). Lifecycles are the typed four-state machine: `claude-code` `scaffold_active`, `cursor` `migration_ready`, `codex` `repo_only`, `gemini-cli` `repo_only`. Adapter artifacts are pointers (`.claude/CLAUDE.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/dat-kit.mdc`) with `ownership_class: adapter`, never policy. Conformance: `test_adapter_conformance.py`; Phase 2 bundle `docs/spikes/phase-2/evidence.md`. |
| 11 | v1.16 recognized only as a migration source, never green; clean + customized fixtures + one real project pass without silent mutation; `.cursorrules` has typed `RETIRE_LEGACY` semantics | **PASS** | Registry (re-read): `green_revisions: ["dat-kit 2.0"]`, `migratable_source_revisions: ["dat-kit 1.16.0"]` — 1.16 is never green. Fixtures: clean + customized v1.16 migrated via `--migration-plan` → checker exit 0 with custom policy preserved (evidence §5b). **Real project**: Gate 3, owner's blog project via isolated clone — plan S001–S005, applied, `contract_check` exit 0, and `docs/agent-working-rules.md` sha256 **identical before and after** (`736ec0c6…87e69`); the real working tree never touched. `RETIRE_LEGACY` is a typed action in `MATERIALIZATION_ACTIONS` (`scripts/registry.py:35`) and `contract_check.py:112,1122-1124,1337,1379` maps `.cursorrules` → `REMOVE_LEGACY_POINTER`; `test_contract_migration.py`. |
| 12 | Governed roots have no orphan product paths; `explain-evolution` works as the manual improvement path | **PASS** | Orphan check is not merely tested but **executed on every run**: `validate.py:71` calls `catalog.validate_governed_inventory()` (`registry.py:913`), which emits `EVOLUTION_ORPHAN_PATH` / `EVOLUTION_OWNERSHIP_AMBIGUOUS`; `validate.py` is green at RC time, so the live tree has zero orphans. Negative case pinned by `test_new_governed_product_path_without_component_is_orphaned`. `explain-evolution` **run live at RC time** (§2 above), returning full governance for a real governed path — not asserted. |
| 13 | Full release train, rollback, RC evidence, and tag complete | **OPEN — by design; closes at step 11** | Release train steps 1–10 complete: freeze + bump (§5b), render/byte-check (§3), suites (§2), Windows + Linux clean-install smokes (Gate 2, §5b), host smokes (Gate 4), fixture + real-project migration (§5b, Gate 3), **RC evidence = this document**, rollback rehearsal (§5c Deliverable 1, transcript runs A–E). **Not complete: the `v2.0.0` tag itself and the migration guide + release notes** — plan §6 step 11, explicitly out of scope for RC1 and gated on the owner's go/no-go on this bundle. This is the single item RC1 structurally cannot close; it is what makes this a release *candidate*. |

**Result: 12 PASS · 1 OPEN-by-design (item 13, the tag) · 0 STOP.** No §13.1
item failed verification, and no item was closed on assumption.

## 5. Fixtures and results (cited)

| Fixture / smoke | Result | Source |
|---|---|---|
| Clean v1.16 fixture migration | plan → apply → `contract_check` exit 0 | evidence §5b |
| Customized v1.16 fixture migration | exit 0, custom policy preserved | evidence §5b |
| Real v1.16 project (owner's blog, isolated clone) | exit 0; project-owned policy sha256-identical | § External gates → Gate 3 |
| Linux clean-install smoke | 17 created, exit 0, idempotent rerun | evidence §5b |
| Windows Git Bash clean-install smoke | 17 created, exit 0; rerun 0 created / 17 skipped | § External gates → Gate 2 |
| Rollback to v1.17.1 tooling (runs A–E) | fail-closed with named diagnostics; every byte preserved | evidence §5c |
| `scaffold_v116_contract` (frozen 1.16 fixture) | green | `test_contract_check.py` |
| ledger-close synthetic non-software pack | composes through the engine | `test_domain_builder_pack.py` |
| Claude Code fresh-session pack read | PASS | § External gates → Gate 4 |
| Codex fresh-session pack read (JSONL-verified) | PASS, cache `…/dat-kit/2.0.0` | § External gates → Gate 4 |
| Real Actions run `29744500620` | `validate` + `windows-python` both PASS | § External gates → Gate 1 |

## 6. Known limitations

1. **Cursor manual evidence checklist NOT gathered** (D-RC-A). The owner does
   not have Cursor installed. `adapters/cursor/ADAPTER.md` states no scriptable
   headless Cursor exists, so this is a manual checklist rather than an
   automated gate, and §13.1 does not require Cursor live evidence. The `cursor`
   adapter remains `migration_ready` with declared artifacts and typed
   `RETIRE_LEGACY` semantics that ARE mechanically tested. **Named, not
   assumed — to be closed before the `v2.0.0` tag.**
2. **Gemini `repo_only` vs declared `project_artifact`** (D-RC-D). Confirmed
   precisely at RC time: `codex` is `repo_only` with `project_artifacts: []`,
   while `gemini-cli` is `repo_only` **and** declares a `GEMINI.md`
   `project_artifact` — contradicting the `repo_only` definition in
   `adapters/codex/ADAPTER.md` ("no project artifact exists or is emitted").
   Registry-internal; no runtime effect (gemini-cli scaffolds nothing). The fix
   edits FROZEN registry data and requires the R9 amendment procedure, so it is
   deferred past the tag. Lesson appended this session.
3. **Freeze coupling is docs→test only** (rolled INFO from 5b). Deleting
   `scripts/tests/test_format_freeze.py` is not mechanically caught by the R9
   statement. Unchanged this RC.
4. **§13.1 item 9's software-dev half is not test-pinned** (new, surfaced by
   this bundle's item-9 pass). The knowledge-work descriptor↔loop-profile
   agreement has three assertions; software-dev has none — it was verified by
   reading both artifacts here. A future ceiling edit to software-dev could
   drift from its profile without a red test. Not a release blocker (both agree
   today, and `loop_ceiling` is fail-closed as a required key), but it is the
   asymmetric half of an otherwise mechanized rule.
5. **Migration-apply is proven by live transcripts, not a pin test** (rolled
   from 5b). Mechanizing it remains an optional later candidate.
6. **`docs/codex.md` redirect stub is load-bearing** and must survive while
   v1.17.1 is the rollback target — current scripts and rolled-back v1.17.1
   tooling both print "see docs/codex.md" (rehearsal run D).
7. **The `.gitattributes`/`expected_outputs()` coverage check is not yet
   mechanized** (added by code review of this bundle). The lesson appended this
   session states that every `render.py` projection destination needs an
   explicit `eol=lf` pin and that a repo check should assert it. Today all three
   destinations ARE pinned (§3), but nothing stops a future projection from
   landing unpinned — same species as limitation 3: a rule that lives in prose
   and is not mechanically caught.
8. **`release/1.x` gates have not been re-run at RC time.** That branch is
   untouched by this work, but Phase 5 Exit requires the check rather than the
   inference. Carried into step 11 (§11 item 4).

## 7. Fact-check sources and dates (§9.4)

- Host capability claims in `registry/adapters.json` `official_facts`:
  `verified_on` **2026-07-18** for all adapters — re-read at RC time and
  unchanged. Sources cited per adapter in `docs/spikes/phase-0b/host-facts.md`
  (Claude plugin cache/root boundary; Codex local marketplace + new-session
  requirement; Gemini extension reference + `GEMINI.md` context).
- Host versions used for live evidence: Claude Code 2.1.211, Codex CLI 0.144.4
  (0B spike); Gate 4 re-confirmed both hosts on the owner's machine 2026-07-20.
- §9.4 requires re-verification "again before the affected RC". The 2026-07-18
  facts are **3 days old at RC time** and no adapter descriptor changed since;
  no host behavior claim in this bundle rests on anything newer.

## 8. Reviewer and decision references

- Phase 5 slice reviews: 5a code + security **APPROVE** (0 actionable); 5b code
  **APPROVE** (1 MINOR, 1 INFO) + security **APPROVE** (0 findings); 5c code
  **APPROVE** (0 actionable, 2 INFO) + security **skipped with stated reason**;
  5-ext CI fix code **APPROVE** (0 blocking) + security **skipped with stated
  reason**. Full text in the cited evidence sections.
- Phase 4 (all six slices) and Phases 1B/2/3 reviews: their own evidence
  bundles, all closed APPROVE.
- Decisions in force: D-5a-1, D-5b-A/B, D-5c-A/B/C, D-RC-A/B/C/D. **No
  unresolved Class B/C decision** — Phase 4 Class C blessings are discharged in
  `docs/spikes/phase-4/evidence.md`.
- **This RC's own review**: see §10.

## 9. Rollback notes

Rehearsed live at 5c (evidence §5c Deliverable 1), not theorized:

1. Reverting to v1.17.1 tooling **never mutates or corrupts** a project tree of
   either revision — old `init.sh` refuses the newer contract fail-closed
   (`COMPETING_AGENTS`, `BROWNFIELD_CONTRACT_CONFLICT`) and preserves every
   byte; sha256 manifests identical before/after.
2. A 1.16 project that lived through the rollback era remains a clean
   `CONTRACT_MIGRATION_REQUIRED` source for 2.0 tooling — the round trip is
   safe.
3. v1.17.1's own `validate.py` is green in its worktree.
4. Revert units: per `docs/spikes/phase-0b/revert-map.md` row 5 — "drop an
   unapproved RC branch or revert the RC commit before tagging; after a public
   tag, publish a corrective version rather than moving the tag."
5. Applied project migrations use migration backups; release tags and
   append-only evidence are immutable.

## 10. Review of this RC bundle (per §16)

- **code-reviewer** over the RC diff `222cac6..802e21c` (two commits, two files;
  gate outputs pasted into the dispatch per §16 rule 2): **APPROVE — 0 blocking,
  0 MAJOR.** The reviewer independently resolved every spot-checked citation —
  all 16 named tests exist with matching per-file counts, every `file:line`
  reference is exact, the quoted `revert-map.md` and ADAPTER.md strings match,
  and the §13.1 row texts match `plans/PLAN-v7-platform.md:880-905` in order. It
  confirmed: no fabricated or misdescribed citation; no restated claim (every row
  ends in a citation or an explicitly labelled RC-time re-run); item 13's OPEN
  status not disguised; item 9's asymmetry real; freeze compliance clean; the
  13-item count correct.
  Six MINOR precision findings were raised and **all six fixed in the follow-up
  commit**: a loop-profile line reference off by two (:18 → :20); limitation 4's
  "software-dev has none" overstated (the profile sentence IS pinned at
  `test_software_dev_pack.py:63` — what is unpinned is the descriptor↔profile
  link); §1's file list overstating the diff; §10's self-referential review
  pointer plus the unresolved `<RC_COMMIT>` placeholder; the item-count note
  implying the correction lived in the order document; and a missing reciprocal
  forward-reference on the 2026-07-13 lesson entry. Two further INFO gaps were
  promoted into §6 as limitations 7 and 8. Reviewer lesson candidates are
  recorded in `docs/spikes/phase-5/evidence.md` § RC1.
- **security-reviewer: SKIPPED — stated reason.** The RC diff is
  evidence/lessons documentation only (`lessons-learned/lessons-learned.md`,
  `docs/spikes/phase-5/rc1-bundle.md`, `docs/spikes/phase-5/evidence.md`,
  handoff/scorecard). It touches **no** registry data, migration code, path
  handling, auth, or public-input surface, so the §16 security trigger does not
  fire. The §13.1 pass forced **zero code changes**, so this skip is evaluated
  on this diff and not inherited from the session order's advance note.

## 11. RC verdict and what step 11 still needs

**RC1 status: complete and ready for the owner's go/no-go.** 12 of 13 §13.1
items PASS with named receipts; item 13 is open only in the part RC1 cannot
close (the tag itself).

Before tagging `v2.0.0` (step 11, separate session):

1. Owner **go/no-go on this bundle**.
2. Close or formally accept the **Cursor gap** (D-RC-A commitment).
3. Publish the **migration guide + release notes** (§6 step 11).
4. Verify **`release/1.x` gates still pass on its own branch** — a Phase 5 Exit
   criterion not yet re-run at RC time (that branch is untouched by this work,
   but Exit requires the check, not the inference).
5. Tag from the **APPROVED RC commit**, preserving "RC artifact equals tagged
   artifact" (D-5b-A).
