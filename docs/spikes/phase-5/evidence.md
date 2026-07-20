# Phase 5 evidence — slice 5a: atomic templates-flip package

Branch `feature/open-platform-v2`. Baseline `3cbabd6` (4f close), slice range
`3cbabd6..ede8670` + this evidence commit. Executed 2026-07-19/20 (Windows
Cowork sandbox; suite run on a fast local copy of the exact tree because the
mounted-FS run exceeds the sandbox's 45s command cap — same bytes, rsync'd
per gate run).

## Decision D-5a-1 (platform owner, 2026-07-19) — recorded stop

The dictated flip package could not be green under pre-5a `registry.py`
semantics; builder STOPPED per the slice instruction and presented options:

- Conflict 1 (new finding): `scaffold_file_plan` flattened EVERY loaded
  snapshot into one FilePlan and raised `REGISTRY_PATH_COLLISION` before
  lifecycle filtering — a 2.0 snapshot listing AGENTS.md/docs rows collides
  with the immutable 1.16 snapshot's identical targets. No arrangement of
  hashes avoids this.
- Conflict 2 (the 4f cascade): `_validate_snapshots` live-hashed every
  file-backed snapshot's `source_template`; both snapshots point at
  `templates/common/AGENTS.md`, only one revision's bytes can match →
  `REGISTRY_SNAPSHOT_HASH_MISMATCH` ×2.

**Decision: Option A — "historical = record".** Only the canonical
revision's snapshot is a scaffold source and live-verified against template
bytes; historical snapshots verify descriptor↔snapshot internal consistency
and never scaffold. The 1.16 snapshot file stays byte-identical (strongest
immutability proof). Class C amendment to `docs/contracts/registry.md` R6 +
diagnostics table wording blessed via this decision. Rejected: Option B
(archive 1.16 template bytes + repoint the "immutable" snapshot's
source_template paths — still needed the FilePlan change and weakened the
immutability story); Option C (halt the slice).

## 5a deliverables

1. **Atomic flip** — `d1e9d14` (registry half: 2.0 snapshot + descriptor
   `static_template_hashes`/`snapshot_provenance` + 3 adapter
   `project_contract_revision` rows 1.16→2.0 + registry.py D-5a-1 semantics
   + registry.md amendment + 4 registry tests) and `b6d7f38` (template
   half: AGENTS.md marker → "dat-kit 2.0" + `.dat-kit-files.tsv` re-render
   + fixture updates). The two commits are one semantic unit split by
   owner; only the pair is green (the registry half alone live-verifies a
   2.0 snapshot against a still-1.16 template).
2. **FU-1** (phase-3 evidence) — `b0d829a`: `_marker_scan_text` strips
   fenced blocks + inline code spans before marker matching, applied at all
   marker sites. Boundary pinned: prose mentions still count
   (`test_mixed_markers_are_partial` untouched).
3. **Render body-field guard** (4f security INFO) — `ede8670`:
   `UNSAFE_FIELD_CHARS` applies to trigger name, domain_id,
   required_engine_revision, pack_location, and every alias. Charset
   literal UNCHANGED; 4e pin test untouched.
4. **Housekeeping pins verified, no change**: `test_engine_deletion.py`
   two-pack hardcode noted only (ledger-close stayed fixture-only); pinned
   eval phrases intact in `registry/domains.json` AND
   `benchmarks/skill-evals.jsonl` (no description edits this slice);
   single-line description guard unchanged.

## Proofs

- **Gates (post-slice)**: `python3 -m pytest scripts/tests -q` → **271
  passed, 3 skipped** (baseline 254+3; +17 new, 0 removed, 1 renamed:
  `test_canonical_rerun_is_readonly_migration_gate` →
  `test_canonical_rerun_is_readonly_and_idempotent`). `validate.py` →
  "✓ all checks green". `render.py --check` → exit 0.
- **Greenfield-green (live)**: `init.sh --here --profile react` in an empty
  dir → exit 0; `contract_check.py --target <dir>` → exit 0; scaffolded
  AGENTS.md carries "**Canonical contract revision:** dat-kit 2.0". Pinned
  by `test_greenfield_scaffold_is_green_under_v2` (state green, zero
  diagnostics).
- **1.16 immutability**: `git diff 3cbabd6..HEAD --
  registry/snapshots/project-contract-1.16.json` → empty; sha256 of the
  file `be98855cf093c0c44c6e28371bb886d5ef35ff63ba3e5891b55539688ddb2648`;
  1.16 descriptor `static_template_hashes` unchanged in platform.json
  (AGENTS.md still `e4ad841c…`).
- **Red-before-green**: (a) registry — new tests against pre-D-5a-1 code
  failed with `REGISTRY_SNAPSHOT_HASH_MISMATCH` ×2 (snapshot
  expected_content_hash + descriptor static_template_hashes), reproducing
  the 4f cascade; (b) FU-1 — both fixtures failed with
  `CONTRACT_PARTIAL_MIGRATION` (fenced/inline 1.16 marker read as mixed)
  before the scan helper; (c) render guard — 10 parametrized cases
  (6 alias chars + 4 body fields) failed before the guard landed.
- **v1.16 fixture fidelity**: `scaffold_v116_contract` reconstructs the
  pre-flip template byte-exactly (only the marker line ever differed);
  migration-fixture EXPECTATIONS updated, semantics untouched.

## Review (per §16: sequential, diff-scoped, ≤30-line reports)

- code-reviewer over `3cbabd6..ede8670`: **APPROVE** — 2 INFO
  (read-based scope verification, discharged by builder's
  `git diff --name-only` matching the declared list exactly; historical
  mismatch diagnostic's json-path points at the descriptor rather than the
  snapshot row — cosmetic, no change).
- security-reviewer (fired: registry + migration + guard surfaces):
  **APPROVE** — 0 CRITICAL/HIGH/MEDIUM/LOW, 3 INFO confirmations:
  (1) historical-snapshot relaxation opens no tamper path (bypass requires
  editing platform.json — the equal-trust root — and historical snapshots
  have no data-flow into FilePlans or classification); (2)
  `_marker_scan_text` is strictly subtractive — it can hide a marker
  (fails safe toward non-green) but can never forge or fuse one, so no
  false-green; (3) no unguarded registry string reaches a generated file
  (revision strings are STABLE_ID-constrained; backticks in aliases cannot
  inject a line under the pinned charset). First dispatch was cut off by a
  session limit after file reads only; clean restart produced the full
  report.
- No fix rounds required; no findings-scoped re-review needed.

## Known limitations / rolled forward

- Rest of Phase 5 (steps 2–11): release_version/version-owner bump, format
  freeze, RC bundle, host smokes, migration of a real v1.16 project,
  rollback rehearsal, docs sweep, tag — later slices, per the 5a scope.
- security INFO from review 2 to keep pinned in future review: the
  subtractive-normalizer invariant of `_marker_scan_text` (a change that
  substitutes spans with "" instead of "``" could fuse fragments) — lesson
  candidate below.
- External gates unchanged: push + real Actions runs, live host smokes.

## Lesson candidates (pending owner approval — normal mode)

1. A shipped snapshot that doubles as recognition record AND live-template
   proof deadlocks any revision flip (PATH_COLLISION + HASH_MISMATCH);
   split the roles (D-5a-1) before future cutovers.
2. Subtractive-normalizer invariant: a pre-match sanitizer must only
   remove/neutralize, never emit new substrings — that property is the
   whole false-green guarantee of FU-1.
3. Trust-domain equivalence test for relaxing redundant integrity checks:
   bypass must require editing an equal-or-higher-trust, independently
   gated artifact, AND the relaxed artifact must have no data-flow into
   privileged outputs. Both were shown here; require both next time.

---

# Phase 5 evidence — slice 5b: format freeze + 2.0.0 bump + suites + smokes + fixture migrations

Branch `feature/open-platform-v2`. Baseline `86091ac` (5a close) + `c1ffaf0`
(session-order doc, owner-committed — accepted as a benign deviation from the
dictated HEAD; history beneath matched exactly). Slice range
`c1ffaf0..024882b` + this evidence commit. Executed 2026-07-20 (Windows
Cowork sandbox; suites run on an rsync'd local copy of the exact tree per the
5a machine-quirk protocol).

## Decisions (owner-confirmed at session start, one batch)

- **Scope**: plan §6 steps 1–5 + 7 repo-side confirmed as proposed; OUT: RC
  bundle (8), rollback (9), docs sweep (10), tag (11), live host smokes (6).
- **D-5b-A — straight bump to 2.0.0** (no rc suffix). Rationale: Phase 5
  Exit requires "RC artifact equals tagged artifact"; an rc-suffixed version
  string would force a post-RC diff. RC1/RC2 (step 8) are evidence bundles,
  not version strings.
- **D-5b-B — freeze = docs statement + pin test, coupled.** R9 freeze block
  in `docs/contracts/registry.md` + `scripts/tests/test_format_freeze.py`;
  amending either requires the other in the same commit (docs→test coupling
  enforced by the anchor test).
- **5a lesson candidates: all 3 approved** and appended first
  (`6181816`).

## 5b deliverables

1. **Lessons harvest** — `6181816`: snapshot dual-role deadlock,
   subtractive-normalizer invariant, trust-domain equivalence test.
2. **Step 1 tail + step 2** — `291dd78`: R9 format-freeze statement
   (format_revision 1 everywhere; canonical `dat-kit 2.0`; green/migratable
   lists frozen) + `release_version` 1.17.1→2.0.0 in platform.json with all
   three version_targets mirrored (marketplace.json, .claude-plugin
   plugin.json, .codex-plugin plugin.json).
3. **Tests** — `024882b`: `test_format_freeze.py` (4 tests: format_revision
   pin across bootstrap/children/snapshots, contract-revision state pin,
   child-revision/bootstrap-row equality, docs-anchor coupling) +
   `test_registry_catalog.py` release_version expectation → 2.0.0.

## Proofs

- **Gates (committed tree `024882b`)**: pytest → **275 passed, 3 skipped**
  (baseline 271+3; +4 freeze tests, 0 removed). `validate.py` → "✓ all
  checks green" (incl. version-mirror equality at 2.0.0 and the skill-eval
  corpus check — the step-4 skill-eval suite). `render.py --check` → exit 0:
  the step-3 byte-check is the required NO-OP (version strings reach no
  rendered projection).
- **Red-before-green (new gate only)**: on a disposable copy, mutating
  `registry/domains.json` `format_revision`→2 failed
  `test_format_revision_is_frozen_at_1_everywhere`; stripping the R9 anchor
  failed `test_freeze_statement_anchored_in_registry_contract`; clean tree
  → 4 passed.
- **Step 5 Linux clean-install smoke (live)**: empty dir → `init.sh --here
  --profile react` exit 0 → `contract_check.py --target` exit 0 → AGENTS.md
  carries "**Canonical contract revision:** dat-kit 2.0"; rerun of init.sh
  exit 0 + recheck exit 0 (idempotent). **Windows Git Bash smoke = EXTERNAL
  gate for the maintainer** (hosts absent in sandbox).
- **Step 7 repo-side — v1.16 fixture migrations** (via
  `contract_check.py --migration-plan`, steps applied as dictated,
  byte-snapshots kept):
  - *Clean* (`scaffold_v116_contract`): pre-check exit 1
    (CONTRACT_MIGRATION_REQUIRED ×2); plan S001–S005; applied
    MIGRATE_REPLACE AGENTS.md (2.0 template), RETIRE .cursorrules, ADD
    `.cursor/rules/dat-kit.mdc` (copy, hash-pinned adapter row); post-check
    **exit 0**.
  - *Customized* (same + hash-pinned `docs/agent-workflow.md` customized +
    user spec content): pre-check exit 1 adds CONTRACT_MIGRATION_CONFLICT +
    PARTIAL_INSTALL_MISMATCH; plan adds S005 MERGE_CANONICAL_POLICY with
    PRESERVATION destination `docs/agent-working-rules.md`; applied merge —
    canonical workflow bytes restored, custom policy appended to the
    user-owned destination with a provenance heading; post-check **exit 0**;
    custom policy text and user spec content verified present after
    migration. **"One real v1.16 project" half stays EXTERNAL** with the
    maintainer.

## Review (per §16: sequential, diff-scoped, ≤30-line reports)

- code-reviewer over `c1ffaf0..024882b`: **APPROVE** — 1 MINOR
  (`test_child_revisions_match_bootstrap_rows` re-implements Catalog's
  REGISTRY_CHILD_REVISION_MISMATCH check and slightly overreaches the
  D-5b-B freeze charter; intentional pin redundancy, kept), 1 INFO
  (coupling is docs→test only: deleting the pin test while docs stay is not
  mechanically caught — future hardening candidate).
- security-reviewer (fired: registry data touched): **APPROVE** — 0
  findings. Invariants confirmed: UNSAFE_FIELD_CHARS pin, `_marker_scan_text`,
  1.16 snapshot, eval phrases all untouched; "2.0.0" flows only into the
  version-mirror equality check, no rendered surface.
- No fix rounds; no findings-scoped re-review needed.

## Auto-decisions logged this slice (low severity)

1. HEAD `c1ffaf0` (session-order doc) accepted as benign vs. the dictated
   `86091ac`; history beneath verified identical.
2. No end-to-end migration-apply pin test added (beyond the dictated
   deliverable; the applied transcripts above are the evidence) — candidate
   for a later slice if the owner wants it mechanized.
3. Customized-fixture merge wrote the preserved policy under a provenance
   heading in `docs/agent-working-rules.md` (the plan's stated PRESERVATION
   destination).

## Known limitations / rolled forward

- Remaining Phase 5: RC bundle (8), rollback rehearsal to v1.17.1 (9), docs
  sweep (10 — README/HUONG_DAN/codex.md still cite 1.17.1/1.16 where
  applicable), migration guide + tag (11), live host smokes (6).
- External gates unchanged: push + real Actions runs (Ubuntu + Windows),
  Windows Git Bash clean-install smoke, real v1.16 project migration, live
  host smokes per ADAPTER.md.
- Code-review INFO to roll: one-way freeze coupling (see review above).

## Lesson candidates (5b)

None — the slice applied existing lessons; reviewers proposed none.

# Phase 5 evidence — slice 5c: rollback rehearsal (step 9) + docs sweep (step 10)

Branch `feature/open-platform-v2`. Baseline `b14d648` (owner-committed 5c
session-order doc on the dictated `8d5fb70`; history beneath verified
identical — same benign-deviation pattern as 5b's `c1ffaf0`). Slice range
`b14d648..a6a1be6` + this evidence commit. Executed 2026-07-20 (Windows
Cowork sandbox; suites and the rehearsal run on an rsync'd local copy per
the 5a machine-quirk protocol; edits + git in the mounted repo).

## Decisions (owner-confirmed at session start, one batch)

- **D-5c-A — live rollback rehearsal in the sandbox** (worktree at tag
  `v1.17.1` from the local copy; era-appropriate tooling against a
  2.0-scaffolded AND a 1.16 project dir; transcript below).
- **D-5c-B — full README rewrite per plan** (architecture + per-host
  capability/support table); HUONG_DAN.vi.md follows the same depth.
- **D-5c-C — RC bundle (step 8) stays OUT of 5c**, opens only after the
  external gates return (Windows smoke, real v1.16 project, Actions runs,
  host smokes) so the RC evidence bundle is complete.

## Deliverable 1 — step 9: rollback rehearsal to v1.17.1 (live transcript)

Setup: `git worktree add /tmp/kit-run/v1171 v1.17.1` (in the rsync'd copy —
mounted repo untouched); `proj20` scaffolded by HEAD tooling
(`scripts/init.sh --here --profile react`, AGENTS.md marker `dat-kit 2.0`,
current `contract_check --target` exit 0); `proj116` scaffolded by v1.17.1
tooling (marker `dat-kit 1.16.0`). Both got user content (spec/00-vision.md
+ USER-NOTES.md); sha256 of every file recorded pre-rehearsal (18 files
each).

| Run | Command (v1.17.1 tooling) | Target | Result |
|---|---|---|---|
| A | `contract_check.py --target` | proj116 | **exit 0** (own-era green, silent success) |
| B | `contract_check.py --target` | proj20 | **exit 1**, named diagnostic `COMPETING_AGENTS: AGENTS.md is not the current dat-kit canonical contract` — no traceback |
| B2 | `--target --migration-plan` | proj20 | exit 1; plan S001–S003 with `UNRESOLVED AGENTS.md: POLICY_DESTINATION` — proposes, resolves nothing, applies nothing |
| C | `init.sh --here --profile react` rerun | copy of proj116 | **exit 0**; dir **byte-identical** (idempotent, user files preserved) |
| D | `init.sh --here --profile react` rerun | copy of proj20 | **exit 1**, fails closed: `COMPETING_AGENTS` + `BROWNFIELD_CONTRACT_CONFLICT: migrate manually; see …/docs/codex.md`; dir **byte-identical** — 2.0 AGENTS.md, user notes, spec content all intact |
| E | CURRENT `contract_check.py --target` | proj116 post-rehearsal | exit 1, `CONTRACT_MIGRATION_REQUIRED` ×2 — still cleanly migratable forward |

Read-only proof: sha256 manifests of proj20 and proj116 identical before and
after A/B/B2 (`diff` empty both). v1.17.1 tooling self-health: its
`validate.py` in the worktree → "✓ all checks green".

**Rollback notes**: (1) reverting to v1.17.1 tooling never mutates or
corrupts a project tree of either revision — old init refuses the newer
contract fail-closed with named diagnostics and preserves every byte;
(2) v1.17.1 error text points users at `docs/codex.md`, which makes the
step-10 redirect stub **load-bearing for rollback users** — the stub must
survive as long as v1.17.1 remains the rollback target; (3) round trip is
safe: a 1.16 project that lived through the rollback era remains a clean
`CONTRACT_MIGRATION_REQUIRED` source for 2.0 tooling. Step 9 repo-side:
**CLOSED**.

## Deliverable 2 — step 10: docs sweep

- `e751d5f` — README.md full rewrite (three-layer architecture section;
  per-host capability/support table derived row-by-row from
  `registry/adapters.json` incl. lifecycles and `official_facts verified_on
  2026-07-18` per plan §9.4; 2.0/1.16 migration truth; roadmap gains the
  v2.0.0 in-train entry; stale 1.17.1-as-current claims removed) +
  HUONG_DAN.vi.md rewritten to mirror the same facts in Vietnamese.
- `a6a1be6` — `docs/codex.md` folded into `adapters/codex/ADAPTER.md`
  (host guide + migration reference, truth-updated: the former "v1.17.1
  continues to accept the unchanged dat-kit 1.16.0 layout" claim is
  replaced by the proven fail-closed 1.16 semantics); `docs/codex.md` is
  now a redirect stub carrying the migration-plan command only — kept
  because `scripts/init.sh`, `scripts/contract_check.py`,
  `docs/agent-workflow.md`, `skills/project-init/SKILL.md` AND rolled-back
  v1.17.1 tooling (rehearsal run D) all point at that path.
- `docs/domains.md` + `docs/loops.md`: **verified already compliant, no
  edit** — zero "final/permanent" instances (removed by the 4f rewrite,
  decision 0001 satisfied; repo-wide grep found only benign non-layout
  uses) and zero stale version citations. No commit needed.
- Pinned eval phrases untouched (no SKILL.md in the diff).

## Proofs (gates on the end-state tree `a6a1be6`)

pytest → **275 passed, 3 skipped** (unchanged — docs-only diff adds no
tests); `validate.py` → "✓ all checks green"; `render.py --check` → exit 0.
Format freeze respected: no registry/, templates/, scripts/ path in the
diff.

## Review (per §16: sequential, diff-scoped, ≤30-line report)

- code-reviewer over `b14d648..a6a1be6`: **APPROVE** — 0 actionable; 2 INFO
  (Gemini row "None committed" is looser than the registry, which defines a
  GEMINI.md `project_artifact` despite `repo_only` — registry-internal
  quirk, not editable under the freeze; cell wording). All five dictated
  checks PASS (truth-derivation, 2.0 semantics, stub function, VI
  consistency, decision-0001 language).
- security-reviewer: **SKIPPED, stated reason** — pure docs sweep (four
  .md files) + read-only rehearsal in /tmp; no registry data, migration
  code, path handling, or public-input surface touched, so the §16 trigger
  does not fire.

## Auto-decisions logged this slice (low severity)

1. HEAD `b14d648` (owner session-order doc) accepted as benign vs. the
   dictated `8d5fb70`; history beneath verified identical.
2. Inbound `docs/codex.md` references in scripts/agent-workflow/project-init
   left pointing at the redirect stub intentionally (scripts frozen this
   slice; stub proven load-bearing by rehearsal run D).
3. No third commit for domains/loops — nothing to change; recorded as a
   verification instead.
4. Rehearsal artifacts kept out of the repo (transcript lives in this
   section, per the 5b evidence pattern); raw logs remained in the sandbox.

## Known limitations / rolled forward

- Remaining Phase 5: RC bundle (8, per D-5c-C after external gates),
  migration guide + tag (11), live host smokes (6).
- External gates unchanged: push + real Actions runs (Ubuntu + Windows),
  Windows Git Bash clean-install smoke, real v1.16 project migration, live
  host smokes per ADAPTER.md.
- Rolled INFOs: one-way freeze coupling (from 5b); Gemini
  `repo_only`-vs-defined-`project_artifact` registry quirk (from 5c review)
  — reconcile before RC, registry edit requires the freeze-amendment
  procedure (R9 + pin test, same commit) if it touches frozen surfaces.

## Lesson candidates (5c)

1. (from code review) A lifecycle label and a declared artifact list can
   silently contradict each other across descriptors — `repo_only` is
   defined in the codex ADAPTER as "no project artifact exists or is
   emitted" while the gemini-cli descriptor defines a GEMINI.md
   `project_artifact` at the same lifecycle. Registry semantics need one
   canonical definition per lifecycle state, enforced by a conformance
   check, not per-adapter prose. (Awaiting owner approval.)

# Phase 5 evidence — external gates (Gate 1-4), owner machine, 2026-07-20

Maintainer-run verification of the D-5c-C external gates (plan §6 steps 5,
6, 7 external halves + step 1's real Actions run), executed by the owner on
their own Windows machine after slice 5c closed at `c7d25e7`. This session
guided each gate, diagnosed and fixed two CI-only defects Gate 1 surfaced,
and independently reviewed the fix.

## Gate 1 — push + real Actions run

First real push of `feature/open-platform-v2` (PR #2) surfaced two failures
never caught by sandbox verification (which only ever ran gates against an
rsync'd copy, never a real git checkout):

- `PROJECTION_BYTE_MISMATCH` on `skills/build-loop/SKILL.md` and
  `skills/knowledge-work/SKILL.md`, Windows job only. Root cause:
  `.gitattributes` did not pin these two generated projections to
  `eol=lf`; a Windows Actions checkout (`core.autocrlf=true`, GH-hosted
  default) normalized the committed LF bytes to CRLF, while
  `render.py`'s `render_domain_trigger` always emits LF — `validate.py`'s
  `check_outputs()` byte-compare (same function `render.py --check` uses)
  failed on Windows only.
- ShellCheck SC2015 on `scripts/init.sh` (then line 113): the classic
  `A && B || C` non-if-then-else shape. Never caught before because
  Actions had never run on this branch prior to this push.

**Fix** (`ba77045`): `.gitattributes` gains `skills/**/SKILL.md text
eol=lf`, matching the existing `registry/**`/`templates/**`/`*.py`/`*.sh`
pins; `scripts/init.sh` rewritten to `if ! { [ -f ... ] && [ ! -L ... ];
}; then ...; fi` — identical diagnostic string and exit code for all three
cases (real file / missing / symlink), verified by extracting the logic
into a standalone script and running all three.

**Red-before-green**: `git clone -c core.autocrlf=true --quiet .
/tmp/before` at the pre-fix commit reproduced the exact CI failure locally
(both SKILL.md files came back CRLF, `validate.py` printed the identical 2
diagnostics). Same clone simulation against `ba77045` came back green
(LF-only, `validate.py` "✓ all checks green", pytest 275+3, `bash -n`
clean).

**Real Actions proof**: run
[`29744500620`](https://github.com/datmaiba/dat-kit/actions/runs/29744500620)
on commit `ba77045`, PR #2 — **Status: Success**, jobs `validate` (13s)
and `windows-python` (53s) both green. Only 2 informational Node.js-20
deprecation warnings, unrelated.

**code-reviewer** (diff-scoped, `ba77045` only): **APPROVE**, 0 blocking
findings. Confirmed: `skills/**/SKILL.md` glob correctly matches both
affected files and no others; format freeze (registry R9) untouched (no
`registry/` file in the diff); init.sh rewrite behavior-preserving for all
three cases; no other un-suppressed SC2015 pattern in scope; no other
byte-checked projection (`render.py`'s `expected_outputs()` — only the TSV
manifest and `skills/*/SKILL.md`) left unpinned. 2 lesson candidates
(below). security-reviewer: **skipped, reason stated** — line-ending pin +
shell control-flow rewrite, no registry/migration/public-input/path-logic
surface touched.

## Gate 2 — Windows Git Bash clean-install smoke

Fresh `git clone --branch feature/open-platform-v2` into
`C:\tmp\dk-smoke\dat-kit` (real Windows Git Bash / MINGW64, not the
sandbox), then in a separate empty project dir:

- `bash .../scripts/init.sh --here --profile react` → 17 files created,
  exit 0.
- `grep "Canonical contract revision" AGENTS.md` → `dat-kit 2.0`.
- `python3 .../scripts/contract_check.py --target .` → exit 0.
- Rerun both: `init.sh` → **0 created, 17 skipped** (existing files never
  overwritten; correctly named the one manual-merge case,
  `docs/agent-working-rules.md`, for the react profile); `contract_check`
  → exit 0 again. Idempotent.

## Gate 3 — real v1.16 project migration (owner's blog project)

Target: `D:\project\blog` (real project, git history, in active use —
working tree had substantial unrelated uncommitted WIP). To avoid mixing
migration changes with that WIP, verification ran against an **isolated
clone** (`git clone` of the same repo to a scratch directory, committed
history only) rather than the live working tree.

- `contract_check.py --target . --migration-plan` on the real repo (dirty
  tree, read-only) → plan S001-S005: `AGENTS.md` MIGRATE_REPLACE,
  `.cursorrules` RETIRE_LEGACY → `.cursor/rules/dat-kit.mdc` ADD.
- Manual inspection (direct file read, not user-relayed) of `AGENTS.md`
  and `.cursorrules` confirmed both are byte-identical to the shipped
  1.16-era template except the project-name substitution and the revision
  line — a clean migration case, no custom content at risk.
  `docs/agent-working-rules.md` (the real project-owned policy — full
  laravel-react stack rules, gates, traps, ~140 lines) is correctly
  **absent from the plan entirely** — the tool recognizes it as
  project-owned and never touches it.
- Pre-check on the isolated clone: `contract_check.py --target .` → exit
  1, 2 diagnostics (`CONTRACT_MIGRATION_REQUIRED` for both files) —
  matches the plan.
- Applied the 3 steps (replace AGENTS.md from the 2.0 template with the
  project name substituted, remove `.cursorrules`, add
  `.cursor/rules/dat-kit.mdc` from the template) on the isolated clone
  only.
- Post-check: `contract_check.py --target .` → **exit 0**.
- Preservation proof: `sha256sum docs/agent-working-rules.md` identical
  before and after (`736ec0c6833ef74ad4daf05b392c9765d774b65e4381bde8780f2
  8f777a87e69`). `git status --porcelain` on the isolated clone showed
  exactly the 3 predicted changes and nothing else.
- The owner's real `D:\project\blog` working tree was **never modified**;
  the isolated clone was discarded after verification. The exact 4
  commands to apply for real (whenever the owner is ready, ideally after
  committing current WIP) are recorded for them.

## Gate 4 — live host smokes

**Claude Code** (`claude --plugin-dir D:\project\dat-kit`, fresh session):
invoked `run the build loop` → loaded `dat-kit:build-loop`, correctly
identified real repo state (`HEAD ba77045`, tree clean,
`feature/open-platform-v2`), cited real evidence file paths
(`docs/spikes/phase-5/evidence.md`, `plans/PLAN-v7-platform.md §6`), and
correctly surfaced the open Gemini-quirk decision in the D-5c-* pattern
rather than proceeding to build — proving both pack read (content outside
`skills/`) and discipline (stopped at a real open decision instead of
barreling ahead). Instructed to stand down (smoke test only); no files
changed by that session.

**Codex** (`codex exec "run the build loop"`, fresh session, plugin
installed from a temporary local marketplace descriptor pointing
`source: url` + `ref: feature/open-platform-v2` at the real GitHub repo —
the default `codex plugin marketplace add <repo> --ref <branch>` was
tried first but does not override the nested per-plugin source ref baked
into the fetched `marketplace.json`, so a scratch marketplace file was
authored instead, mirroring the proven working schema with the ref
corrected): session transcript (`~/.codex/sessions/.../*.jsonl`, 232
records) confirms it read all six domain-pack slot files
(`domains/software-dev/{workflow,ground-truth,gates,reviewers,loop-profile}.md`,
`deliverables/`) plus `engine/work-loop/{ENGINE.md,engine.json}`, and the
installed plugin cache path correctly read `2.0.0`
(`~/.codex/plugins/cache/dat-kit-branch/dat-kit/2.0.0`).

**Side effect, reverted**: this Codex run (sandbox `workspace-write`,
approval `never`) went beyond the smoke-test scope on its own initiative —
it re-ran parts of Gates 1-2 itself, attempted (and failed, for reasons
local to its own sandboxed subprocess: `EPERM` on
`~/.claude/session-env`, then no visible OAuth) to invoke Claude Code
itself, and **wrote** `handoffs/HANDOFF-2026-07-20-phase5-external-gates.md`
plus one `benchmarks/scorecard.jsonl` append recording "Claude pack-read
FAIL after 3 rounds". That claim is accurate only about Codex's own
sandboxed attempt — it does not contradict this session's independent,
real-terminal Claude Code evidence above. Both artifacts were uncommitted
and were reverted/discarded (not a rewrite of committed history) to avoid
a stale, confusing claim sitting in `handoffs/` (which build-loop reads
first on resume) or the scorecard. Lesson candidate below.

**Cursor / Gemini**: owner does not have Cursor installed — manual
evidence checklist (`adapters/cursor/ADAPTER.md`) **not gathered this
session**, left as a known gap, not silently assumed. Gemini CLI stays
`repo_only`; its activation gates are a separate, not-yet-required track
per its own ADAPTER.md — correctly out of scope here.

## Gates re-verified after the CI fix

pytest 275 passed 3 skipped; `validate.py` "✓ all checks green"; `render.py
--check` exit 0 (all on the rsync'd sandbox copy at `ba77045`, plus the
real Windows/Ubuntu Actions run above as the authoritative cross-platform
proof).

## Lesson candidates (external gates)

1. `* text=auto` alone does not protect a byte-compared generated file on
   Windows checkout — every `render.py` projection destination needs an
   explicit `.gitattributes` `eol=lf` pin. Add a repo check that every
   path in `expected_outputs()` is covered by such a pin, so a future new
   projection can't silently reintroduce this class of bug.
2. Sandbox rsync-copy verification cannot see `.gitattributes`/checkout
   normalization bugs — a real `git clone -c core.autocrlf=true` (or
   equivalent) belongs in pre-push verification, not just post-push
   discovery via Actions.
3. `codex exec` with default `sandbox: workspace-write` +
   `approval: never` will treat an unscoped prompt like "run the build
   loop" as full authorization to execute real work end-to-end (writing
   handoffs, appending scorecards, attempting to shell out to other
   tools) — a host-conformance smoke prompt for Codex must explicitly
   restrict scope ("read-only, report three facts, do not modify files or
   execute the plan" — the phrasing Codex itself later recommended for
   re-testing Claude) or run under a read-only sandbox flag.
(RESOLVED — all 3 approved by the owner 2026-07-21 under D-RC-C and appended in
`bdf2a00`, together with the 5c candidate.)

# Phase 5 evidence — step 8: RC1 evidence bundle

Executed 2026-07-21 (Windows Cowork sandbox; suites on an rsync'd local copy per
the 5a machine-quirk protocol; edits + git in the mounted repo). Baseline
`ab6abb0` (owner-committed RC session-order doc) on the dictated `222cac6` —
the same benign session-order deviation pattern as 5b (`c1ffaf0`) and 5c
(`b14d648`); history beneath verified identical.

**The bundle itself is `docs/spikes/phase-5/rc1-bundle.md`.** This section is
the slice receipt; the bundle is the deliverable and is not restated here.

## Decisions (owner-confirmed at session start, one batch)

- **D-RC-A** — open RC1 now with the **Cursor manual evidence checklist as a
  named known limitation**, to be closed before the `v2.0.0` tag.
- **D-RC-B** — verify **every** §13.1 item against a named artifact/test/evidence
  citation; an unprovable item is a STOP.
- **D-RC-C** — approve **all four** pending lesson candidates (3 from 5-ext, 1
  from 5c) and append them first, in their own commit.
- **D-RC-D** — the Gemini `repo_only`-vs-declared-`project_artifact` quirk stays
  a **documented known limitation**, fixed after the tag under the R9
  freeze-amendment procedure.

## Deliverables

- `bdf2a00` — 4 approved lessons appended (D-RC-C), own commit, first.
- `802e21c` — RC1 evidence bundle: §9.3 shape (commit + registry revisions,
  commands + exit codes, fixtures, projection check, fact-check sources + dates,
  known limitations, reviewer + decision references, rollback notes) plus the
  §13.1 Definition-of-Done matrix.
- Review fix-up commit — six MINOR code-review findings fixed, two INFO gaps
  promoted to known limitations, review verdict recorded in the bundle §10, and
  this evidence section.

## §13.1 result (per D-RC-B)

**12 PASS · 1 OPEN-by-design · 0 STOP** over the 13 checkbox items at
`plans/PLAN-v7-platform.md:880-905`. The single open item is #13 ("full release
train, rollback, RC evidence, and tag complete") — open only in the part RC1
structurally cannot close: the `v2.0.0` tag and the migration guide/release
notes, both step 11. No item was closed on assumption.

Note: the session order says "14-item"; §13.1 contains 13. Recorded in the
bundle, order document not edited.

## Proofs (gates at RC time)

pytest → **275 passed, 3 skipped** (278 collected; unchanged — the RC adds no
code and no tests); `validate.py` → "✓ all checks green"; `render.py --check` →
exit 0; `registry.py explain-evolution domains/software-dev/workflow.md` → exit
0, governed, class B (run live rather than asserted, for §13.1 item 12).
Authoritative cross-platform proof remains Actions run `29744500620` on
`ba77045`. Format freeze respected: no `registry/`, `templates/`, or `scripts/`
path in the diff.

## Review (per §16: sequential, diff-scoped, ≤30-line report)

- **code-reviewer** over `222cac6..802e21c`: **APPROVE** — 0 blocking, 0 MAJOR;
  6 MINOR (all fixed in the follow-up commit) + INFO. It independently resolved
  every spot-checked citation: all 16 named tests exist with matching per-file
  counts, every `file:line` reference exact, quoted strings verbatim, §13.1 row
  texts matching the plan in order. Confirmed no fabricated citation, no
  restated claim, item 13 not disguised, item 9's asymmetry real, freeze clean.
- **security-reviewer: SKIPPED, stated reason** — the RC diff is
  evidence/lessons documentation only; no registry data, migration code, path
  handling, auth, or public-input surface is touched, so the §16 trigger does
  not fire. The §13.1 pass forced **zero code changes**, so this skip is
  evaluated on the actual diff, not inherited from the session order's advance
  note.

## Auto-decisions logged this slice (low severity)

1. HEAD `ab6abb0` (owner session-order doc) accepted as benign vs. the dictated
   `222cac6`; history beneath verified identical.
2. Sandbox scratch path moved from `/tmp/kit` to `/tmp/rc1` — the documented
   path existed owned by another uid and was not writable. Protocol otherwise
   unchanged.
3. The six MINOR review findings were fixed rather than rolled forward: in a
   document whose entire value is citation exactness, an off-by-two line
   reference is a defect in the deliverable, not a nit.
4. `<RC_COMMIT>` resolved to the bundle commit `802e21c` with the RC tree
   defined as the following fix-up commit, rather than rewriting history to make
   a document contain its own hash.

## Known limitations / rolled forward

Eight, enumerated in the bundle §6: Cursor gap (D-RC-A); Gemini registry quirk
(D-RC-D); freeze coupling docs→test only (5b); software-dev descriptor↔profile
link not test-pinned (new); migration-apply proven by transcript not pin test
(5b); `docs/codex.md` stub load-bearing (5c); `.gitattributes`/`expected_outputs()`
coverage check not mechanized (new); `release/1.x` gates not re-run at RC time
(new — carried into step 11).

## Lesson candidates (RC1, from code review — awaiting owner approval)

1. An evidence bundle that lists files it *plans* to touch alongside files it
   *has* touched breaks its own citation contract. The diff-scope statement in
   an evidence artifact must be generated from the actual diff at commit time,
   not copied from the session order's plan.
2. A self-referential review pointer ("see §10" inside §10) is scaffolding that
   survives into a release artifact. A review verdict belongs in a commit or
   appendix that can cite the RC commit hash, since the RC document itself
   cannot contain its own hash.

## Next

**STOP for owner go/no-go on RC1.** Step 11 (migration guide + release notes +
tag `v2.0.0` from the approved RC commit) is a separate session and additionally
requires re-verifying that `release/1.x` gates still pass on their own branch.
