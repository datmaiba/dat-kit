# HANDOFF 2026-07-21 — RC2 migration-safety correction, external release gates open

## Goal

Close the post-tag review findings against Plan v7 Phase 5 / §13.1 without
publishing a release artifact whose migration planner can discard customized
`AGENTS.md` policy.

## Runtime

`codex / GPT-5`

## Workflow

`build-loop` with sequential plan, QA, code, and security review.

## Canonical contract

`dat-kit 1.16.0` (root maintainer contract; generated-project canonical
revision remains `dat-kit 2.0`).

## Git state

Branch `feature/open-platform-v2`; implementation commit
`697e9ac2289cc58b87c1a10727cb7698ab553b72`. The branch was 19 commits ahead
of `origin/feature/open-platform-v2` when this handoff was written. The tree
was clean before adding this handoff; commit this file as the only follow-up
docs change.

The existing local annotated tag `v2.0.0` is tag object `9bb07fe` on stale
commit `1ec1a15`. It has not been pushed (last successful remote check in the
review session found no `refs/tags/v2.0.0`); a later retry was blocked by
sandbox network access. Do not push this tag.

## State

- DONE:
  1. Migration classifier now neutralizes a rendered `AGENTS.md` title only
     when its project name exactly matches the inspected target directory
     basename; all other divergence fails closed to `MERGE_REQUIRED`.
  2. Clean, customized-body, unexpected-title, renamed/forged-title,
     deterministic/read-only, preservation-destination, and CRLF behavior are
     covered by revision-state tests.
  3. CI now triggers on `v*` tag pushes; release notes, migration guide,
     README status, RC1 warning, RC2 evidence, and diff hygiene are corrected.
  4. Red-before-green receipts, gates, QA/code/security verdicts, and two
     append-only scorecard records are committed in `697e9ac`.
- IN PROGRESS: none repo-side.
- NOT STARTED:
  1. RC2 clean/customized application rehearsal plus one isolated real v1.16
     project migration on commit `697e9ac` or its handoff-only descendant.
  2. Final pre-tag evidence commit and review after those receipts land.
  3. Recut/push `v2.0.0`, verify Actions on the exact tagged SHA, then record
     §13.1 item 13 closure in a post-tag commit.

## Decisions in effect

- D-5a-1 — historical snapshots are recognition records; only the canonical
  snapshot scaffolds and live-verifies templates.
- D-5b-B / registry R9 — registry format remains frozen; this correction
  changes checker behavior and tests, not frozen registry data.
- D-11-A — Cursor live-checklist gap remains an accepted named limitation.
- RC2 safety boundary — target-directory metadata, not agreement between two
  user-editable headings, authorizes subtractive project-name normalization.
- Release status — the old local tag is stale evidence; release exit is open
  until real-project and tagged-SHA CI receipts exist.

## Files touched

- `scripts/contract_check.py` — fail-closed rendered-title normalization and
  customized-policy action selection.
- `scripts/tests/test_revision_states.py` — migration safety and forged-title
  regressions.
- `scripts/tests/test_contract_check.py`, `.github/workflows/ci.yml` — tag
  trigger regression and configuration.
- `docs/releases/migration-2.0.md`, `docs/releases/v2.0.0.md`, `README.md` —
  corrected public behavior and release status.
- `docs/spikes/phase-5/evidence.md`, `docs/spikes/phase-5/rc1-bundle.md` — RC2
  repository evidence and RC1 historical warning.
- `benchmarks/scorecard.jsonl` — two append-only Codex records (review and
  implementation); validated after each append.
- `handoffs/CONTEXT-2026-07-18-lean-dat-kit-improvement.md`,
  `scripts/tests/test_registry_catalog.py`,
  `scripts/tests/test_registry_render.py` — `git diff --check` cleanup.
- This handoff — uncommitted at write time; no other working-tree change.

## Verified gates

- `python scripts/validate.py` — `✓ all checks green`, including after the
  final scorecard and RC2 evidence append.
- `python -m pytest scripts/tests` — **277 passed, 6 skipped** (283 collected).
- `python scripts/render.py --check` — exit 0.
- `bash -n scripts/init.sh` — exit 0.
- `shellcheck scripts/init.sh` — exit 0.
- `git diff --check` — exit 0.
- QA — `PHASE DONE` after migration boundary attacks.
- Code review — `APPROVE` after findings-scoped re-review.
- Security review — `APPROVE`; one MEDIUM forged-heading finding fixed and
  findings-scoped re-review approved.
- External real-project RC2 migration — **unverified**.
- Actions on corrected tagged SHA — **unverified**.

## Third-party tool risks

None reported. No installer ran.

## Next steps

1. On the owner's machine, clone the real v1.16 project to an isolated scratch
   directory and run:
   `python D:\project\dat-kit\scripts\contract_check.py --target <clone> --migration-plan`.
   Confirm a clean project stays `MIGRATE_REPLACE`; if `AGENTS.md` differs or
   the clone directory was renamed, confirm it fails closed to
   `MERGE_CANONICAL_POLICY`. Apply the reviewed plan manually and require the
   corrected checker to exit 0 with project-owned policy preserved.
2. Repeat the clean and customized fixture application receipts from Phase 5
   on the corrected commit; append exact hashes/results to
   `docs/spikes/phase-5/evidence.md` and re-run the full gate set.
3. Commit and review that final pre-tag evidence. Only then delete the stale
   **local** `v2.0.0` tag and create a new annotated tag on the approved commit.
4. Push the branch and new tag. Because `.github/workflows/ci.yml` now has
   `push.tags: ["v*"]`, wait for both jobs and verify the run's `headSha`
   equals `git rev-list -n 1 v2.0.0`.
5. In a post-tag commit, record the tag object hash, tagged commit hash,
   Actions URL/SHA, and §13.1 item 13 closure. Never move a pushed tag.

## Traps

- Do not treat matching user-editable headings as independent evidence; that
  was the security review's MEDIUM finding.
- A renamed target deliberately becomes `MERGE_REQUIRED`; this safe false
  positive prevents destructive false-clean classification.
- A static CI trigger test is not tagged-commit CI evidence; verify the real
  run and exact SHA.
- Never close a tag receipt inside the tree being tagged; use the post-tag
  closure commit.
- Any scorecard append must be followed by `scripts/validate.py` in the same
  phase.

## Glossary

- RC2
- migration source
- preservation destination
- tagged SHA
