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
