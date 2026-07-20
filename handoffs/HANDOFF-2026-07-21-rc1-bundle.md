# Handoff — Phase 5 step 8 (RC1 evidence bundle) CLOSED, awaiting owner go/no-go

**Written:** 2026-07-21, Cowork session (Windows sandbox, Claude Opus 4.8).
**Branch:** `feature/open-platform-v2`. **HEAD at handoff:** `dc3fe81`.
**Reads with, not instead of:** `handoffs/CONTEXT-2026-07-18-plan-v7-execution.md`
(still the active execution context — its 5c and 5-ext deferral blocks are now
partly discharged; see below).

## Goal / state

Step 8 is **CLOSED**. RC1 exists as an artifact:
`docs/spikes/phase-5/rc1-bundle.md`, reviewed and APPROVEd.

**Phase 5 is now complete except step 11** (migration guide + release notes +
tag). Steps 1–10 and the external gates are all closed with evidence.

Commits this session, in semantic-owner order:

| Commit | Contents |
|---|---|
| `bdf2a00` | 4 approved lessons appended (D-RC-C), own commit, first |
| `802e21c` | RC1 evidence bundle — §9.3 shape + §13.1 matrix |
| `dc3fe81` | Review fix-up (6 MINOR fixed), evidence § step 8, scorecard |

## Decisions in effect (owner-confirmed 2026-07-21, one batch)

- **D-RC-A** — RC1 opened with the **Cursor manual evidence checklist as a named
  known limitation**, to be closed before the `v2.0.0` tag. Not silently assumed.
- **D-RC-B** — every §13.1 item verified against a named receipt; unprovable
  item = STOP.
- **D-RC-C** — all four pending lesson candidates approved and appended first.
- **D-RC-D** — Gemini `repo_only`-vs-declared-`project_artifact` quirk stays a
  documented known limitation; fixed after the tag under the R9 amendment
  procedure (the fix edits FROZEN registry data).

## The §13.1 result — the thing step 11 depends on

**12 PASS · 1 OPEN-by-design · 0 STOP** over the 13 checkboxes at
`plans/PLAN-v7-platform.md:880-905`. The open item is #13 (tag + release notes),
which an RC structurally cannot close. **No item was closed on assumption.**

Do not re-derive this matrix — it is in the bundle §4 with per-item citations.

## Facts that bind the next session (in addition to CONTEXT's)

- **Format freeze still BINDING.** The RC diff touched no `registry/`,
  `templates/`, or `scripts/` path (verified). Step 11 must not either, beyond
  what the tag itself requires.
- `release_version` remains `2.0.0`, **no rc suffix** (D-5b-A). RC1 is an
  evidence bundle, not a version string. "RC artifact equals tagged artifact" is
  a Phase 5 Exit criterion — **tag from the approved RC commit**, do not rebuild.
- The §13.1 checklist has **13** items, not 14 as
  `handoffs/SESSION-ORDER-2026-07-21-rc-bundle.md:110` states. The order
  document was deliberately not edited.
- Machine quirks unchanged, plus one new: the documented `/tmp/kit` scratch path
  may already exist owned by another uid — use a fresh path (`/tmp/rc1` this
  session). Stale `index.lock` needed Cowork file-delete permission, as expected.

## Step 11 — exactly what remains

1. **Owner go/no-go on RC1.** This is a STOP; nothing below starts without it.
2. Close or formally accept the **Cursor gap** (the D-RC-A commitment).
3. Publish **migration guide + release notes** (§6 step 11).
4. **Re-run `release/1.x` gates on their own branch** — a Phase 5 Exit criterion
   NOT yet re-run. The branch is untouched by this work, but Exit requires the
   check, not the inference. (Bundle known limitation 8.)
5. Tag `v2.0.0` **from the approved RC commit**.

## Open items carried forward (bundle §6 has all eight)

New this session, neither is a release blocker:

- **software-dev descriptor↔loop-profile link is not test-pinned** while
  knowledge-work's is (`test_knowledge_work_pack.py:49,163,164,169`).
  `test_software_dev_pack.py:63` pins the profile sentence but nothing asserts
  the descriptor's `loop_ceiling`. Post-tag candidate.
- **`.gitattributes`/`expected_outputs()` coverage check not mechanized.** All
  three projection destinations are pinned today; nothing stops a fourth from
  landing unpinned. The appended lesson calls for the check — post-tag.

Two RC1 lesson candidates await owner approval in evidence § RC1 (evidence-bundle
diff-scope must be generated from the real diff; a review verdict belongs in a
commit that can cite the RC hash).

## Traps

- The bundle's value is **citation exactness**. If you edit it, re-verify the
  `file:line` references — code review caught an off-by-two that a reader would
  have taken as fabrication.
- `docs/codex.md` redirect stub is **load-bearing** while v1.17.1 is the rollback
  target. Never delete it.
- Never restate cited evidence as a fresh claim in the bundle. It aggregates.
