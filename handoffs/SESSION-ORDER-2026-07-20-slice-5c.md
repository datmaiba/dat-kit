# Session order — Phase 5 slice 5c (scope PROPOSED; owner confirms at start)

Context: dat-kit repo, branch `feature/open-platform-v2`. HEAD must be
`8d5fb70` ("docs(5b): handoff status — 5b CLOSED + evidence §5b (decisions
D-5b-A/B, proofs, reviews) + 5b deferrals/flags + scorecard line"); history
`8d5fb70 024882b 291dd78 6181816 c1ffaf0 86091ac ede8670 b0d829a b6d7f38`.
Phases 0A→4 CLOSED. Phase 5 slices 5a + 5b CLOSED: atomic templates flip
(D-5a-1) then format freeze (D-5b-B) + release_version 2.0.0 (D-5b-A) +
suites + Linux smoke + both v1.16 fixture migrations — evidence
`docs/spikes/phase-5/evidence.md` §5a/§5b, all reviews APPROVE. This session
opens the NEXT Phase 5 slice (5c).

## Step 1 — minimal bootstrap (read nothing else)

Read `AGENTS.md` (root) + `handoffs/CONTEXT-2026-07-18-plan-v7-execution.md`
(the "5b deferrals/flags → later Phase 5 slices" block BINDS this slice) +
`plans/PLAN-v7-platform.md` ONLY §6 Phase 5 (steps 9–10 + Exit) + §9 + §16 +
`docs/spikes/phase-5/evidence.md` §5b only (grep for "slice 5b").

Verify: `git log --oneline -9` matches; tree clean; gates green:
`python3 -m pytest scripts/tests -q` (expect **275 passed 3 skipped**),
`python3 scripts/validate.py`, `python3 scripts/render.py --check`.

Machine quirks (Windows Cowork sandbox, confirmed at 5a/5b — do NOT
rediscover):

- Mounted-FS pytest exceeds the 45s bash cap AND each bash call is a fresh
  sandbox. Protocol: `rsync -a --delete <mnt>/dat-kit/ <local-tmp>/kit/`
  then run the suite in the copy (~3s). Edits + git stay in the mounted
  repo. `pip install pytest --break-system-packages` may be needed once.
- `git config core.filemode false` once per session.
- Stale `.git/HEAD.lock`/`index.lock` → request Cowork file-delete
  permission, `rm -f`, retry; transient "unable to unlink tmp_obj" warnings
  are harmless (fsck dangling objects are expected residue).
- CRLF warnings on commit are normal; `.gitattributes` normalizes.

## Facts that bind (established 5a/5b — never re-litigate silently)

- **Format freeze is BINDING** (registry.md R9 + `scripts/tests/
  test_format_freeze.py`): any change to `format_revision`, canonical
  revision `dat-kit 2.0`, or the green/migratable lists before the v2.0.0
  tag reopens the release train and must amend the R9 statement AND the pin
  test in the SAME commit.
- `release_version` is `"2.0.0"` everywhere (platform.json + 3 mirrored
  targets). Do not touch it this slice.
- D-5a-1: canonical snapshot = only scaffold source / only live-verified;
  historical snapshots are immutable records.
  `registry/snapshots/project-contract-1.16.json` IMMUTABLE (sha256
  `be98855c…`).
- `_marker_scan_text` strictly SUBTRACTIVE; `UNSAFE_FIELD_CHARS` literal
  pinned (charset change requires updating the 4e pin test same commit).
- Pinned eval phrases ("run the build loop" / "write a researched report")
  MUST survive the docs sweep — if any SKILL.md description is edited,
  keep the phrases; `benchmarks/skill-evals.jsonl` asserts them.
- Rolled code-review INFO (5b): freeze coupling is docs→test only —
  optional hardening, not required this slice.
- Decision 0001 (docs/decisions/): "final/permanent" wording in
  docs/domains.md + docs/loops.md must be removed by step 10.

## Step 2 — proposed 5c scope (plan §6 steps 9 + 10 repo-side; CONFIRM)

OPEN DECISIONS for the owner before executing (present as one batch):

- **D-5c-A — rollback rehearsal method (step 9).** Options: (1) live
  rehearsal in the sandbox — `git worktree`/copy at tag `v1.17.1`, run its
  tooling (validate/init/contract-check era-appropriate) against a
  2.0-scaffolded AND a 1.16 project dir, prove project files preserved and
  diagnostics sane, transcript into evidence (recommended); (2)
  document-only rollback procedure, live rehearsal deferred to the
  maintainer as an external gate. Consequence: (1) is real evidence but
  costs budget; (2) is cheaper but Phase 5 Exit needs the proof eventually.
- **D-5c-B — README rewrite depth (step 10).** Options: (1) full rewrite
  per plan — architecture + per-host capability/support table
  (recommended); (2) truth-fix only (2.0 facts, stale 1.17.1/1.16 citations
  fixed), full rewrite deferred to a 5d docs slice. HUONG_DAN.vi.md follows
  the same choice (Vietnamese).
- **D-5c-C — RC bundle timing.** Recommend: step 8 (RC1) stays OUT of 5c
  and opens only after the external gates return (Windows smoke, real
  v1.16 project, Actions runs, host smokes) so the RC evidence bundle is
  complete — confirm.

Deliverables (after decisions):

1. Step 9 per D-5c-A: rollback-to-v1.17.1 rehearsal with project files
   preserved; transcript + rollback notes into evidence §5c.
2. Step 10 per D-5c-B: docs sweep — README rewrite, `docs/codex.md` folds
   into `adapters/codex/ADAPTER.md` with a redirect stub, `HUONG_DAN.vi.md`
   updated, docs/domains.md + docs/loops.md "final/permanent" wording
   removed (decision 0001), stale 1.17.1/1.16 citations corrected
   (README/HUONG_DAN/codex.md per 5b deferrals). Docs are truth-derived
   from registry/contracts — never invent capability claims; per-host rows
   follow §9.4 fact-check discipline (cite ADAPTER.md verification dates).
3. Gates re-run after the sweep (docs edits can break validate.py doc
   checks and eval-phrase pins — treat any red as STOP-and-inspect).

OUT OF SCOPE 5c: RC bundle (8), migration guide + tag (11), any registry/
template/scripts code change (freeze is binding), live host smokes (6 —
external), Windows smoke + real-project migration (external halves of 5/7).
Evidence: append §5c to `docs/spikes/phase-5/evidence.md` — decision
records, rehearsal transcript, sweep file list, gate outputs.

Reviews per §16: sequential, diff-scoped, ≤30-line reports; code-reviewer
always; security-reviewer fires ONLY if registry/migration/path surfaces
are touched (a pure docs sweep + read-only rehearsal does not fire — state
the skip and reason explicitly). Dispatch with changed-file list + pasted
gate outputs + diff range AND end-state files.

Commit order by semantic owner: rehearsal evidence artifacts (if any repo
files) → docs sweep (may split: README/HUONG_DAN → codex fold →
domains/loops wording) → evidence + handoff + scorecard.

Discipline: slice budget ~50–80k tokens, checkpoint at 70%; grep before
Read; STOP on scope overflow — especially anything touching registry data,
templates, or migration SEMANTICS. When 5c is done, STOP, report, wait.

External gates unchanged: push + real Actions runs (Ubuntu + Windows),
Windows Git Bash clean-install smoke, one real v1.16 project migration,
live host smokes per ADAPTER.md, then release-train tail (RC bundle 8,
migration guide + tag 11).
