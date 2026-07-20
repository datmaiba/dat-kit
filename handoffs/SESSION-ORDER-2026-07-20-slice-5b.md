# Session order — Phase 5 slice 5b (scope PROPOSED; owner confirms at start)

Context: dat-kit repo, branch `feature/open-platform-v2`. HEAD must be
`86091ac` ("docs(5a): handoff status — 5a CLOSED + evidence bundle (D-5a-1,
proofs, reviews) + 5a deferrals/flags + scorecard line"); history `86091ac
ede8670 b0d829a b6d7f38 d1e9d14 3cbabd6 fe7ced8 7beffac 2f5f8a0`. Phases
0A→4 CLOSED. Phase 5 slice 5a CLOSED: atomic templates flip (2.0 snapshot +
descriptor hashes + adapter rows + marker + tsv) under decision D-5a-1, FU-1
marker hardening, render body-field guard — evidence
`docs/spikes/phase-5/evidence.md`, reviews code+security APPROVE. This
session opens the NEXT Phase 5 slice (5b).

## Step 1 — minimal bootstrap (read nothing else)

Read `AGENTS.md` (root) + `handoffs/CONTEXT-2026-07-18-plan-v7-execution.md`
(the "5a deferrals/flags → later Phase 5 slices" block BINDS this slice) +
`plans/PLAN-v7-platform.md` ONLY §6 Phase 5 (steps 1–11 + Exit) + §9 + §16 +
`docs/spikes/phase-5/evidence.md` (whole file — it is short and carries
D-5a-1 + the pending lesson candidates).

Verify: `git log --oneline -9` matches; tree clean; gates green:
`python3 -m pytest scripts/tests -q` (expect **271 passed 3 skipped**),
`python3 scripts/validate.py`, `python3 scripts/render.py --check`.

Machine quirks (Windows Cowork sandbox, confirmed at 5a — do NOT rediscover):

- Mounted-FS pytest exceeds the 45s bash cap AND each bash call is a fresh
  sandbox (`--die-with-parent`: no background process survives between
  calls; a `pgrep -f` can false-match the sandbox wrapper). Protocol:
  `rsync -a --delete <mnt>/dat-kit/ <local-tmp>/kit/` then run the suite in
  the copy (~3s). Edits + git stay in the mounted repo.
- `git config core.filemode false` once per session.
- Stale `.git/index.lock` → request Cowork file-delete permission, `rm`.
- CRLF warnings on commit are normal; `.gitattributes` normalizes. Verify
  rendered files stay LF before `render --check` panics.

## Facts that bind (established at 5a — never re-litigate silently)

- **D-5a-1**: the canonical revision's snapshot is the ONLY scaffold source
  and the ONLY live-verified snapshot; historical snapshots are immutable
  records (descriptor↔snapshot consistency only, never scaffold, never
  live-hashed). Future cutovers author a new canonical snapshot and demote
  the old one — never edit a historical snapshot. `registry.md` R6 amended.
- Greenfield scaffolds are GREEN under the v2 checker; `init.sh` rerun is
  truly idempotent. `registry/snapshots/project-contract-1.16.json` remains
  IMMUTABLE (sha256 `be98855c…`).
- `release_version` is still `"1.17.1"` — the bump was deliberately out of
  5a scope; `version_targets` mirrors it into 3 plugin manifests.
- Test fixtures: `scaffold_v116_contract` = frozen 1.16 project;
  `scaffold_contract` = current (v2) templates.
- `_marker_scan_text` (contract_check.py) must stay strictly SUBTRACTIVE —
  it may hide markers, never emit/fuse substrings (false-green guarantee).
- `UNSAFE_FIELD_CHARS` literal is pinned; extending the charset requires
  updating `test_unsafe_field_charset_is_pinned` in the SAME commit.
- Pinned eval phrases ("run the build loop" / "write a researched report")
  must survive any description edit.
- 3 lesson candidates await owner approval in the 5a evidence §last — ask
  at session start; on approval append to `lessons-learned/` first.

## Step 2 — proposed 5b scope (plan §6 steps 1–5 + 7 repo-side; CONFIRM)

OPEN DECISIONS for the owner before executing (present as one batch):

- D-5b-A: version scheme for step 2 — bump `release_version` straight to
  `2.0.0`, or an RC scheme first (plan step 8 mentions RC1/RC2)? The bump
  propagates through `version_targets` to both plugin manifests +
  marketplace.json.
- D-5b-B: what "freeze registry and contract format revisions" (step 1
  tail) must produce beyond the landed flip — a freeze statement in the
  contract docs, a format_revision pin test, or both?

Deliverables (after decisions):

1. Step 1 tail: registry + contract format freeze per D-5b-B.
2. Step 2: version-owner bump per D-5b-A (platform.json + mirrored
   targets; validate.py version-mirror check must stay green).
3. Step 3: render + byte-check all projections (should be a no-op check —
   any diff is a red flag, stop and inspect).
4. Step 4: full suites — unit, contract, registry, projection, migration,
   skill-eval (`benchmarks/skill-evals.jsonl` runner if present).
5. Step 5: clean-install smokes — Linux side runnable in the sandbox
   (fresh dir, `init.sh`, `contract_check`); Windows Git Bash smoke is an
   EXTERNAL gate for the maintainer — list it, never fake it.
6. Step 7 repo-side: migrate the clean AND customized v1.16 fixtures
   through the migration path and verify with the new checker; the "one
   real v1.16 project" half stays EXTERNAL with the maintainer.

OUT OF SCOPE 5b: RC bundle (step 8), rollback rehearsal (9), docs sweep
(10), tag (11), live host smokes (6 — external). Ledger-close stays
fixture-only.

Evidence: append a §5b to `docs/spikes/phase-5/evidence.md` — gate outputs,
decision records, smoke transcripts, migration-fixture results.

Reviews per §16: sequential, diff-scoped, ≤30-line reports; security review
FIRES if registry/migration surfaces are touched (the version bump alone is
registry data — dispatch it). Dispatch with changed-file list + pasted gate
outputs + diff range AND end-state files (reviewers may lack git).

Commit order by semantic owner: registry (freeze + bump) → maintainers
(tests) → evidence + handoff + scorecard.

Discipline: slice budget ~50–80k tokens, checkpoint at 70%; grep before
Read; STOP on scope overflow — especially anything touching migration
SEMANTICS or historical snapshots. When 5b is done, STOP, report, wait.

External gates unchanged: push + real Actions runs (Ubuntu + Windows), live
host smokes per ADAPTER.md, release-train tail (RC, rollback, tag).
