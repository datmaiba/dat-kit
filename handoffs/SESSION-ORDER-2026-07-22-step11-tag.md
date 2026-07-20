# Session order — Phase 5 step 11 (migration guide + release notes + tag v2.0.0) — scope PROPOSED; owner confirms at start

**PRECONDITION — this session does not start without it:** the owner has given
an explicit **go on RC1** (`docs/spikes/phase-5/rc1-bundle.md`). If that go has
not been given, STOP and ask for it. RC1 is APPROVED by review but not yet by
the owner; a tag from an unapproved RC violates Phase 5 Exit ("RC artifact
equals tagged artifact" presumes an *approved* RC).

**Run this session on `opus` or `fable`, not `sonnet`.** Per
`docs/model-selection.md`, tagging a release is the last irreversible act of the
train — a judge/verify role, and the one step where a public tag cannot be moved
afterwards, only superseded. If the session starts on a lower tier, say so and
ask the owner to raise it with `/model` before substantive work.

Context: dat-kit repo, branch `feature/open-platform-v2`. HEAD must be
`5154f3f` ("docs(5): RC1 handoff + scorecard line …"); the RC commits beneath it
are `dc3fe81 802e21c bdf2a00 ab6abb0 222cac6`. Phases 0A→4 CLOSED. Phase 5
steps 1–10 CLOSED, external gates VERIFIED, **step 8 (RC1) CLOSED** with
§13.1 at 12 PASS / 1 open-by-design / 0 STOP. Step 11 is the only thing left in
the whole v2.0.0 program.

## Step 1 — minimal bootstrap (read nothing else)

Read `AGENTS.md` (root) + `handoffs/HANDOFF-2026-07-21-rc1-bundle.md` (the
newest handoff — it BINDS this session and already lists step 11's five items) +
`handoffs/CONTEXT-2026-07-18-plan-v7-execution.md` (the 5c/5-ext deferral blocks
only) + `docs/spikes/phase-5/rc1-bundle.md` **§4 (the §13.1 matrix), §6 (known
limitations), §11 (what step 11 needs)** + `plans/PLAN-v7-platform.md` ONLY §6
Phase 5 (step 11 + Exit) + §12 (documentation deliverables) + §16.

**Do NOT re-derive the §13.1 matrix.** It is done, receipted, and reviewed. Read
it; do not rebuild it. The only §13.1 item still open is #13, and this session
is what closes it.

Verify: `git log --oneline -6` matches; tree clean; gates green:
`python3 -m pytest scripts/tests -q` (expect **275 passed 3 skipped**),
`python3 scripts/validate.py`, `python3 scripts/render.py --check`.

Machine quirks (Windows Cowork sandbox, confirmed 5a→RC1 — do NOT rediscover):

- Mounted-FS pytest exceeds the 45s bash cap AND each bash call is a fresh
  sandbox. Protocol: `rsync -a --delete <mnt>/dat-kit/ <local-tmp>/kit/` then run
  the suite in the copy (~3s). Edits + git stay in the mounted repo.
  **`/tmp/kit` may already exist owned by another uid — use a fresh scratch path.**
  `pip install pytest --break-system-packages` may be needed once.
- `git config core.filemode false` once per session.
- Stale `.git/HEAD.lock`/`index.lock` → request Cowork file-delete permission,
  `rm -f`, retry; transient "unable to unlink tmp_obj" warnings are harmless.
- CRLF warnings on commit are normal; `.gitattributes` normalizes.
- Sandbox rsync copies do NOT reproduce checkout normalization. Anything
  line-ending-related must be verified via
  `git clone -c core.autocrlf=true <repo> <tmp>` (lesson, 2026-07-20).

## Facts that bind (established 5a→RC1 — never re-litigate silently)

- **Format freeze is BINDING** until the tag (registry.md R9 +
  `scripts/tests/test_format_freeze.py`): any change to `format_revision`,
  canonical revision `dat-kit 2.0`, or the green/migratable lists reopens the
  release train and must amend the R9 statement AND the pin test in the SAME
  commit. **Step 11 must not touch these.** A needed change = STOP and reopen.
- `release_version` is `"2.0.0"` everywhere (platform.json + 3 mirrored targets).
  D-5b-A: straight `2.0.0`, **no rc suffix** — RC1 was an evidence bundle, not a
  version string. There is nothing to "un-suffix" before tagging.
- **Tag from the APPROVED RC commit.** Phase 5 Exit requires "RC artifact equals
  tagged artifact". Do not rebuild, re-render, or amend the RC tree to make it
  prettier before tagging — that breaks the criterion.
- The §13.1 checklist has **13** items, not 14 (the RC session order said 14;
  the discrepancy is recorded in the bundle §4 and the plan was NOT edited).
- `docs/codex.md` redirect stub is LOAD-BEARING while v1.17.1 is the rollback
  target — current scripts AND rolled-back v1.17.1 tooling print
  "see docs/codex.md". Never delete it.
- D-5a-1 registry semantics, `_marker_scan_text` subtractivity,
  `UNSAFE_FIELD_CHARS` pin, pinned eval phrases, `skills/**/SKILL.md text eol=lf`
  — all unchanged and out of scope here.

## Step 2 — proposed step-11 scope (plan §6 step 11 + Exit; CONFIRM before executing)

OPEN DECISIONS for the owner, present as ONE batch:

- **D-11-A — the Cursor gap, final disposition.** RC1 recorded it as a named
  known limitation "to be closed before the `v2.0.0` tag" (D-RC-A). That
  commitment now comes due. (1) **Formally accept it as a shipped known
  limitation** of v2.0.0, documented in the release notes and the cursor
  ADAPTER, with the manual checklist deferred to a v2.0.x follow-up
  (recommended — `adapters/cursor/ADAPTER.md` states no scriptable headless
  Cursor exists, so this is a manual checklist rather than an automated gate;
  the adapter's `RETIRE_LEGACY`/migration semantics ARE mechanically tested, and
  §13.1 never required Cursor live evidence). (2) Install Cursor, run the
  checklist, then tag. Consequence: (1) ships honestly with the gap named in
  user-facing release notes; (2) is stricter but blocks the tag on software the
  owner may not want. **Either way the release notes must name it** — silently
  dropping it now would retroactively falsify the RC.
- **D-11-B — `release/1.x` gate verification.** Phase 5 Exit requires
  "`release/1.x` gates still pass on its own branch"; this was never re-run
  (RC1 known limitation 8). (1) **Check out `release/1.x` in an isolated
  worktree and run its own-era gates, recording the output as evidence**
  (recommended — Exit demands the check, not the inference). (2) Infer from "the
  branch is untouched by this work". Consequence: (2) is exactly the kind of
  "probably fine" the whole train has refused so far.
- **D-11-C — migration guide placement + depth.** (1) A new
  `docs/migration-2.0.md` written from the PROVEN transcripts (5b clean +
  customized fixtures, Gate 3 real project, 5c rollback runs A–E) and linked
  from README + `adapters/codex/ADAPTER.md` (recommended — the receipts already
  exist; the guide cites them rather than inventing new claims). (2) Fold it
  into the README. Consequence: (2) bloats a file just rewritten at 5c.
  **Constraint either way:** the guide is user-facing and must state the real
  failure modes (`CONTRACT_MIGRATION_REQUIRED`, `COMPETING_AGENTS`,
  `BROWNFIELD_CONTRACT_CONFLICT`) and the backup/rollback path.
- **D-11-D — tag mechanics.** (1) **Annotated tag `v2.0.0` on the approved RC
  commit, pushed after the release notes commit lands, with the notes commit
  itself included in the tagged tree** (recommended — but note this means the
  tagged commit is NOT `5154f3f`; confirm explicitly that "RC artifact equals
  tagged artifact" is read as *the RC-approved tree plus release documentation*,
  which is the normal reading, and record that reading as a decision). (2) Tag
  `5154f3f` exactly and publish notes afterwards on a follow-up commit.
  Consequence: this is the one ambiguity in the Exit criterion — **do not
  resolve it silently in either direction.**
- **D-11-E — the two RC1 lesson candidates** (evidence-bundle diff-scope must be
  generated from the real diff; a review verdict belongs in a commit that can
  cite the RC hash) plus any lesson this session pays for. Approve for append,
  or defer? Recommended: approve and append FIRST (own commit), as at 5b and RC1.

Deliverables (after decisions):

1. **Migration guide** per D-11-C — v1.16 → 2.0, from proven transcripts only.
2. **Release notes** for v2.0.0 — what changed (three-layer architecture, six-slot
   Domain Packs, registry-driven adapters, `AGENTS.md` as sole policy owner),
   the migration route, **the named known limitations** (Cursor per D-11-A,
   Gemini `repo_only` quirk per D-RC-D), and the rollback path to v1.17.1.
3. **`release/1.x` gate evidence** per D-11-B.
4. **Tag `v2.0.0`** per D-11-D.
5. **Phase 5 Exit closure**: record §13.1 item 13 as CLOSED, with the tag as its
   receipt, in `docs/spikes/phase-5/evidence.md` § step 11 — and update the RC
   bundle §4 row 13 / §11 to point at it. This is the moment the program's
   Definition of Done reads 13/13.
6. Lessons per D-11-E; gates re-run + review per §16.

OUT OF SCOPE step 11: any registry/template/scripts code change (freeze binding
until the tag — a needed change means STOP and reopen the train per R9); the two
post-tag items from RC1 §6 (software-dev descriptor↔loop-profile test pin;
`.gitattributes`/`expected_outputs()` coverage check) — both are v2.0.x work;
the Gemini quirk fix (D-RC-D: after the tag, under the R9 amendment procedure);
Cursor activation; Phase 6 telemetry.

Reviews per §16: sequential, diff-scoped, ≤30-line reports. code-reviewer
always — and it must verify that **every claim in the release notes and
migration guide traces to a real receipt**, since these are the first
user-facing documents of the release (the RC review caught an off-by-two line
reference; user-facing docs get the same scrutiny). security-reviewer: fires
only if registry/migration/path surfaces are touched — a docs-plus-tag step does
NOT fire it; state the skip and reason explicitly. If anything forces a code
change, that changes the answer AND engages R9 — re-evaluate, don't inherit.

Commit order by semantic owner: lessons (if approved) → migration guide →
release notes → `release/1.x` evidence → evidence/handoff/scorecard → **tag
last**.

Discipline: budget ~50–80k tokens, checkpoint at 70%; grep before Read; STOP on
scope overflow. **The tag is irreversible in public** — after it, corrections
ship as a new version, never as a moved tag (`docs/spikes/phase-0b/revert-map.md`
row 5). Treat the pre-tag checklist as a real gate, not a formality.

## After the tag (not this session)

- Push the tag + branch; verify the Actions run on the tagged commit is green.
- v2.0.x follow-ups: Cursor checklist (if deferred at D-11-A), Gemini registry
  quirk under the R9 amendment procedure, the two RC1 §6 mechanization gaps.
- Phase 6 (telemetry v3 → 2.1.0) opens only after the tag is published.
