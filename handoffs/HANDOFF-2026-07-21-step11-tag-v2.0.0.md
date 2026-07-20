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

Branch `feature/open-platform-v2`. HEAD at handoff: `54dafce`. Tree clean.
Commits this session, in order: `8143a32` (lessons) → `d97c218` (D-11-F fix)
→ `fe985a4` (migration guide) → `e7820c9` (release notes) → `e0f52f4`
(release/1.x evidence + §13.1 closure) → `238d7fb` (review fix-up) →
`54dafce` (scorecard). **The `v2.0.0` tag has not been cut yet as of this
handoff** — it is the immediate next action.

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
   §4 row 13 / §11 updated — §13.1 now reads **13 PASS / 0 OPEN / 0 STOP**
   (`e0f52f4`).
8. code-reviewer APPROVE (1 MINOR, fixed in `238d7fb`); security-reviewer
   SKIPPED, stated reason (docs + one data-line correction, no
   registry/migration/path surface touched).
9. Scorecard line for step 11 appended and re-validated post-append
   (`54dafce`).

**IN PROGRESS:** none — all step-11 deliverables are committed. Only the tag
itself remains.

**NOT STARTED (this session):**
1. Cut the annotated `v2.0.0` tag on HEAD `54dafce` (D-11-D: the tag reads
   "RC artifact equals tagged artifact" as the RC-approved tree plus release
   documentation and the D-11-F correction — not the literal RC commit
   `5154f3f`, which is red on `validate.py`).
2. Push the tag + branch (explicitly **not this session** per the session
   order's "After the tag" section).
3. Verify the Actions run on the tagged commit is green.

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

1. Cut the tag: `git tag -a v2.0.0 -m "<summary — three-layer architecture, six-slot Domain Packs, registry-driven adapters, AGENTS.md sole policy owner; see docs/releases/v2.0.0.md>" 54dafce` (or current HEAD if it has moved — confirm `git log -1` first).
2. Confirm `git tag -v v2.0.0` / `git show v2.0.0 --stat` looks right before
   anything is pushed.
3. **Do not push** in this session — per the session order, push + Actions
   verification is explicitly deferred to "after the tag (not this session)".
4. Hand the push instructions to the owner, or open a fresh session scoped
   only to "push the tag, verify Actions green" when ready.
5. Post-tag housekeeping (v2.0.x, not blocking): Cursor checklist (if the
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
