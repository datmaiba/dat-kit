# Phase 1B evidence bundle — Registry, Projection, FilePlan foundations

Date: 2026-07-18 · Branch: `feature/open-platform-v2`
Commits: `dbe42db` (WIP restore) → `38464bd` (smoke out of tree) → `f8395cc`
(cp1252 mojibake repair) → `8a98077` (review-fix batch) → this commit.
Environment: Linux sandbox (Cowork), Python 3.10.12, bash 5. Windows evidence
pending CI (below).

## Gates run (commands and results)

| Command | Result |
|---|---|
| `python3 -m pytest scripts/tests/ -q` | 116 passed, 3 skipped (Windows-only skips) |
| `python3 scripts/validate.py` | ✓ all checks green |
| `python3 scripts/render.py --check` | exit 0, byte-exact |
| `bash -n scripts/init.sh` | clean |
| greenfield smoke (`init.sh --here --profile react`, PATH without python) | 17 files, exit 0 |
| scaffold-output diff vs `v1.17.1` worktree (same project name) | byte-identical |

## Extension fixtures (red-before-green, all present and passing)

`test_registry_render.py`: synthetic registry-only domain (no Python edit);
synthetic adapter template → manifest row (no shell edit); deleted
descriptor-owned projection → `PROJECTION_MISSING`; byte-exact check never
repairs. `test_registry_catalog.py`: unknown field with JSON path; future
bootstrap fails before child read; mixed format fails atomically; orphan
product path. `test_registry_fail_closed.py` (added after review): B1
children-malformed variants; per-kind missing-child naming; invalid trigger
name/aliases are diagnostics not exceptions; lifecycle-filtered plans;
symlinked child rejected. `test_diagnostic_codes.py`: emitted ⊆ documented and
documented ⊆ emitted ∪ reserved, both directions, mechanical.

## Reviews

- QA (independent subagent): items 1–5 PASS; item 6 split — see adjudication.
- Code review (independent subagent): REQUEST-CHANGES — B1 blocker (fail-open
  empty-diagnostic bootstrap), M1–M8, minors. All closed in `8a98077`.
- Security review (independent subagent): APPROVE; LOW findings F1 (allowlist)
  and F3 (read-side symlink) closed in `8a98077` anyway.
- Fix verification: 10-item adversarial re-check run locally on a /tmp copy
  (B1×5, M1, M3×2, M5, M6, F1×2, F3, M2, full regression) — all PASS.

## Adjudication — QA item 6 (adapter artifact lifecycle)

QA read the exit criterion as "all adapter project artifacts `repo_only`".
The plan's actual constraint (§6 Phase 1B) is "**new** project adapter
artifacts stay `repo_only` until Phase 3". `.claude/CLAUDE.md`, `CLAUDE.md`,
and `.cursorrules` are pre-existing dat-kit 1.16 scaffolding carried forward
byte-identically (host-adapter contract HA7); Phase 1B introduces no new
`scaffold_active` artifact, and the scaffold-output diff above proves public
behavior is unchanged. Resolution: PASS as intended wording; criterion text
tightened here for the record.

## Known limitations / deferred to external gates

- A workflow file is not CI evidence: the Windows + Ubuntu jobs in
  `.github/workflows/ci.yml` need a real Actions run on the pushed branch.
- Non-ASCII pass/fail paths on a real cp1252 Windows console not yet
  demonstrated this phase (reconfigure guards added; covered by CI job).
- Host smokes (installed plugin, fresh session) are Phase 2+ scope.

## Rollback note

Phase 1B is additive plus `validate.py`/`init.sh`/`contract_check.py` edits.
Rollback = revert the five Phase 1B commits; `v1.17.1` tooling and public
scaffolding output are unaffected (proven identical above).
