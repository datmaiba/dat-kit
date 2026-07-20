# Phase 2 evidence bundle — repository-side Host Adapter conformance

Date: 2026-07-18 · Branch: `feature/open-platform-v2`
Commits: `eae1ca5` (implementation) → `f890359` (review fixes + plan v7
committed). Environment: Linux sandbox, Python 3.10.12.

## Gates

| Command | Result |
|---|---|
| `python3 -m pytest scripts/tests/ -q` | 124 passed, 3 skipped |
| `python3 scripts/validate.py` | ✓ all checks green |
| `python3 scripts/render.py --check` | exit 0, byte-exact |
| greenfield smoke | 17 files; `GEMINI.md` (repo_only) correctly absent |

## Scope delivered

Adapter packages `adapters/{claude-code,codex,gemini-cli,cursor}/ADAPTER.md`;
`gemini-cli` descriptor added `repo_only` with thin `@AGENTS.md` pointer
template and real canonical hash; ADAPTER.md registered as repository
artifact + rollback-owned for all four; `adapters/` governed root;
personal-info gate extended to `.mdc/.toml/.tsv`;
`test_adapter_conformance.py` (8 tests). `.cursor/rules/*.mdc` pointer
deliberately deferred to Phase 3 (RETIRE_LEGACY lives in an approved
migration plan; descriptor lifecycle must mirror artifact minimum).

## Review (lean mode: one combined QA+code subagent, diff-scoped)

Checklist 5/5 PASS with adversarial spot-checks (lifecycle-mirror rejection,
greenfield exclusion, hash match). Findings closed in `f890359`: MAJOR —
retired-artifact fixture was vacuous (load failed before its assertion; now
asserts load AND exclusion); MINOR — governed-root owner naming; plus the
reviewer's discovery that the approved plan v7 was never committed
(`plans/PLAN-v7-platform.md` now tracked). Security review not separately
run: Phase 2 introduces no new parser/input surface (descriptor JSON +
markdown only); §9.1 security trigger next fires at Phase 3 migration.

## Exit criteria vs plan §6 Phase 2

- Adapter packages green: YES (validator + conformance tests).
- Host smokes where hosts available: NOT AVAILABLE in this sandbox —
  explicit manual evidence checklists live in each ADAPTER.md (claude-code,
  codex installed-session smokes; cursor manual; gemini pre-activation).
  These remain OPEN external gates for the maintainer before Phase 5 RC.
- No new project artifact emitted: YES (proven by smoke + TSV lifecycle
  column + `test_repo_only_artifacts_stay_out_of_greenfield...`).

## Rollback

Revert `eae1ca5` + `f890359`; no public scaffolding output changed.
