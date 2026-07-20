# HANDOFF 2026-07-21 — Phase 5 step 11 CLOSED; v2.0.0 tag cut this session

## Goal

Close the last item of the dat-kit v2.0.0 release train: migration guide,
release notes, `release/1.x` gate re-verification, §13.1 item 13 closure, and
the `v2.0.0` annotated tag itself (`plans/PLAN-v7-platform.md` §6 Phase 5 step
11 + Exit).

## Runtime

Cowork (Windows sandbox), Claude Opus 4.8 — matches `docs/model-selection.md`'s
requirement that tagging run on opus/fable, not sonnet.

## Workflow

`build-loop` (dat-kit maintainer discipline, per root `AGENTS.md`).

## Canonical contract

`dat-kit 1.16.0` (root `AGENTS.md`'s own literal header, unchanged by this
branch's work on the maintainer repo itself — distinct from the registry's
`canonical_revision`/`green_revisions` = `dat-kit 2.0`, which governs what
revision *generated projects* receive from v2.0.0 tooling). Scorecard lines
since 5a have recorded `"dat-kit 2.0"` for this field by established
convention on this branch; noted here as a discrepancy worth a future look,
not resolved this session (out of step-11 scope).

## Git state

Branch `feature/open-platform-v2`. Tree clean. Commits this session, in order:
`8143a32` (lessons) → `d97c218` (D-11-F fix) → `fe985a4` (migration guide) →
`e7820c9` (release notes) → `e0f52f4` (release/1.x evidence + step-11
evidence) → `238d7fb` (review fix-up) → `54dafce` (scorecard) → `a7aa0ad`
(first handoff) → an audit fix-up commit (this file's corrections, F1–F5
below) which is **the commit the `v2.0.0` tag is cut on** → a post-tag commit
recording the tag hash and §13.1 item 13 closure.

**This file lives inside the tagged tree, so it states no hash it cannot
contain.** The tag's own hash and the tagged commit's hash are recorded in the
post-tag commit and in `docs/spikes/phase-5/evidence.md` § Step 11 as amended
there — verify mechanically with `git rev-list -n1 v2.0.0`.

## State

**DONE:**
1. RC1 go/no-go — owner confirmed 2026-07-21.
2. D-11-A..E decided (all recommended options); D-11-F (new finding) fixed.
3. `benchmarks/scorecard.jsonl` line 23 corrected: `agent_runtime`
   `"cowork"` → `"other"` (`d97c218`) — `validate.py` was red on HEAD at
   session start, green after.
4. `docs/releases/migration-2.0.md` written from proven transcripts only
   (`fe985a4`, review fix-up `238d7fb`).
5. `docs/releases/v2.0.0.md` release notes, naming both shipped known
   limitations (`e7820c9`).
6. `release/1.x` gates re-verified in an isolated worktree at its own HEAD
   `ee4b982`: pytest 88 passed/3 skipped, `validate.py` exit 0 (`e0f52f4`).
7. `docs/spikes/phase-5/evidence.md` § Step 11 + `docs/spikes/phase-5/rc1-bundle.md`
   §4 row 13 / §11 updated with step-11 decisions, proofs, and item-13 status
   (`e0f52f4`, corrected by the audit fix-up).
8. code-reviewer APPROVE (1 MINOR, fixed in `238d7fb`); security-reviewer
   SKIPPED, stated reason (docs + one data-line correction, no
   registry/migration/path surface touched). Verdict recorded in
   `evidence.md` § Step 11 → Review.
9. Scorecard line for step 11 appended and re-validated post-append
   (`54dafce`).
10. **Owner-requested self-audit of this session** found five defects, all
    fixed in the audit fix-up commit this tag sits on: (F1) §13.1 item 13 was
    marked CLOSED citing the tag as receipt four commits *before* the tag
    existed — closing on assumption, which D-RC-B forbids; (F2) the first
    handoff, inside the tagged tree, asserted the tag "has not been cut yet";
    (F3) two unfilled placeholders survived into `evidence.md`
    ("see below … once complete", "commit recorded once cut") — the exact
    defect the 2026-07-21 self-referential-pointer lesson warns about;
    (F4) the README roadmap still listed migration guide and tag as
    "remaining" and left v2.0.0 unticked, inside the tree being tagged as
    v2.0.0; (F5) `plan-reviewer` was never dispatched (build-loop step 3),
    an undeclared process deviation.

**IN PROGRESS:** none — all step-11 deliverables are committed and the audit
findings are fixed.

**NOT STARTED:**
1. Push the tag + branch (explicitly **not this session** per the session
   order's "After the tag" section).
2. Verify the Actions run on the tagged commit is green.

## Decisions in effect

- **D-11-A** — Cursor gap formally accepted as a shipped known limitation,
  named in `docs/releases/v2.0.0.md` + `adapters/cursor/ADAPTER.md`; manual
  checklist deferred to v2.0.x.
- **D-11-B** — `release/1.x` gates re-verified in an isolated worktree, not
  inferred. Receipt: `docs/spikes/phase-5/evidence.md` § Step 11.
- **D-11-C** — migration guide is a new file, `docs/releases/migration-2.0.md`
  (auto-decided location under `docs/releases/**` rather than a bare
  `docs/migration-2.0.md`, to avoid an `EVOLUTION_ORPHAN_PATH` red gate
  without touching frozen `registry/evolution.json` — see Traps).
- **D-11-D** — annotated `v2.0.0` tag, cut after all release documentation
  commits land, tagging the tree that includes them (not the literal
  `5154f3f` RC commit, which is red — see D-11-F).
- **D-11-E** — 3 lessons approved and appended first (`8143a32`): the two
  RC1 candidates (evidence-bundle diff-scope, self-referential review
  pointer) plus one from D-11-F (scorecard append must re-validate).
- **D-11-F** (new, not in the original batch) — HEAD's `validate.py` was red
  at session start (`SCORECARD_AGENT_RUNTIME` on the RC1 handoff's scorecard
  line). Fixed, own commit, lesson appended.

## Files touched

- `benchmarks/scorecard.jsonl` — 2 lines changed/added (D-11-F fix + step-11
  scorecard line). Committed.
- `docs/releases/migration-2.0.md` — new (146 lines + 1 precision fix).
  Committed.
- `docs/releases/v2.0.0.md` — new (109 lines). Committed.
- `docs/spikes/phase-5/evidence.md` — +97 lines, § Step 11 appended.
  Committed.
- `docs/spikes/phase-5/rc1-bundle.md` — §4 row 13 + §11 rewritten, two
  forward-reference notes added to §6. Committed.
- `lessons-learned/lessons-learned.md` — +24 lines, 3 new entries. Committed.
- `README.md`, `adapters/codex/ADAPTER.md` — one-line links to the migration
  guide each. Committed.

Nothing uncommitted.

## Verified gates

- `pytest scripts/tests -q` (sandbox copy, re-run 4× across the session) →
  **275 passed, 3 skipped**, consistently.
- `python scripts/validate.py` (sandbox copy) → **red at session start**
  (`SCORECARD_AGENT_RUNTIME: line 23`), **green after `d97c218`**, verified
  green again after every subsequent commit including the final scorecard
  append.
- `python scripts/render.py --check` → exit 0, unchanged all session.
- `release/1.x` own-era gates (isolated worktree at `ee4b982`) →
  pytest **88 passed, 3 skipped**; `validate.py` → **"✓ all checks green"**.

## Third-party tool risks

None reported.

## Next steps

1. `git push origin feature/open-platform-v2 && git push origin v2.0.0` —
   the tag and branch are committed locally and verified, but **deliberately
   not pushed** by the session that cut them, per the session order's "After
   the tag" section.
2. Verify the GitHub Actions run on the tagged commit is green (both
   `validate` and `windows-python` jobs, as in run `29744500620`). Until this
   passes, the tag is local-only and still correctable; **once pushed, it is
   public and must never be moved** — corrections ship as a new version
   (`docs/spikes/phase-0b/revert-map.md` row 5).
3. Post-tag housekeeping (v2.0.x, not blocking): Cursor checklist (if the
   owner wants D-11-A revisited), Gemini `repo_only` registry quirk under the
   R9 amendment procedure, the two RC1 §6 mechanization gaps (software-dev
   descriptor↔loop-profile test pin; `.gitattributes`/`expected_outputs()`
   coverage check). Phase 6 (telemetry v3 → 2.1.0) opens only after the tag
   is published.

## Traps

- **A HARVEST step that appends to a `validate.py`-checked file must
  re-validate in the same phase before declaring green** (the D-11-F lesson,
  2026-07-21 in lessons-learned.md). Applied to this session's own scorecard
  append — do the same for any future append to `benchmarks/scorecard.jsonl`.
- **A bare new file directly under `docs/` will likely trip
  `EVOLUTION_ORPHAN_PATH`** unless its path matches an existing
  `registry/evolution.json` `maintainer-documentation` glob
  (`docs/agent-*.md`, `docs/codex.md`, `docs/decisions/**`, `docs/domains.md`,
  `docs/loops.md`, `docs/model-selection.md`, `docs/releases/**`,
  `docs/spikes/**`). Editing that registry file is a frozen `registry/` path
  — forbidden during any step where the format freeze (R9) is binding. Prefer
  an existing governed glob over a registry edit.
- **`docs/codex.md` redirect stub is load-bearing** while v1.17.1 remains a
  rollback target — v1.17.1's own error text still points there. Never
  delete it.
- Machine quirks unchanged from prior sessions (mounted-FS pytest timeout →
  rsync to local scratch; stale `.git/*.lock` → `mcp__cowork__allow_cowork_file_delete`
  with the **VM path**, not the Windows path, then `rm -f`).

## Glossary

R9 (format freeze), §13.1 (v2.0.0 Definition of Done matrix), D-RC-A/D-RC-D
(Cursor/Gemini known limitations from the RC1 bundle), D-11-A..F (this
session's decisions).
