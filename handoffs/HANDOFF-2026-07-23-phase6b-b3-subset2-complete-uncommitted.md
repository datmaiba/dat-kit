# HANDOFF 2026-07-23 — B3 subset #2 defect projection: built, reviewed, uncommitted tail

## Goal

B3 subset #2 (diagnosing-bugs defect projection) is implemented, reviewed, and
gate-green in the working tree. One commit landed; the remaining changes could
not be committed because of an unremovable git lock (see Git state). The next
session must land the uncommitted tail, then continue B3 subset #3.

## Runtime

Built this session on **Claude Opus** in Cowork. Review agents ran Opus.
Recommended executor to finish: any tier — the remaining action is a commit,
not new design.

## Workflow

`dat-kit:build-loop`, `software-dev` Domain Pack, attended. Subset #2 is
complete through HARVEST; only the commit and lessons write remain.

## Canonical contract

`dat-kit 1.16.0`

## Git state

- Branch: `feature/telemetry-v3-b3`.
- Landed commit: `78a1991` (`feat(telemetry): project defect_recorded to durable
  defects.jsonl`) on base `72ca145`.
- **Blocker**: `.git/index.lock` and `.git/HEAD.lock` exist and are NOT
  removable from the Cowork sandbox (mounted-drive permission denies unlink).
  Clear them on the host (`del .git\index.lock .git\HEAD.lock`) before any
  further git write.
- Uncommitted, all part of subset #2 (commit or `--amend` into `78a1991`):
  `scripts/telemetry.py` (POSIX target-literal security fix),
  `scripts/tests/test_telemetry_defect_projection.py` (POSIX guard test),
  `.gitattributes` (`benchmarks/defects.jsonl text eol=lf` pin),
  `benchmarks/scorecard.jsonl` (subset #2 line),
  `docs/spikes/phase-6b/b3-observation.md` (subset #2 ledger),
  `lessons-learned/lessons-learned.md` (two new entries + one forward ref).
- Preserve existing untracked handoffs/plans. Do not push unless asked.

## State

### DONE

1. `defect_recorded → benchmarks/defects.jsonl` projection (T3.10.2 closed
   13-field), append-only, idempotent by `event_id`, `TELEMETRY_EXPORT_COLLISION`
   on same-id-different-bytes, `benchmark_exported` receipt emitted only after
   the durable append; no-op emits no receipt.
2. `telemetry export --task-id <uuid> --target benchmarks/defects.jsonl`
   subcommand; `DAT_KIT_TELEMETRY=off` honored.
3. Consuming validator `validate_defect_projection` wired into
   `scripts/validate.py`; the three path-safety helpers parametrized with a
   `path=` label (default preserves `events.jsonl` behavior).
4. `.gitattributes` pin added (QA finding); contract `target_path` uses the
   canonical POSIX literal `DEFECT_PROJECTION_TARGET` (security finding).
5. Reviews: plan-reviewer RETURN (13-field blocker + receipt envelope) →
   resolved; code-reviewer APPROVE; security-reviewer APPROVE. Gates: validate
   PASS, pytest `394 passed, 3 skipped`, bash -n PASS, shellcheck 0.8.0 PASS,
   diff-check PASS, ruff PASS. Red-before-green proven. Demo walked end-to-end.

### IN PROGRESS

None.

### NOT STARTED

1. Land the uncommitted tail (see Git state) after clearing the lock; re-run
   `python scripts/validate.py` and `pytest scripts/tests` to confirm.
2. Push / open PR only if the user asks.
3. B3 subset #3: knowledge-work machine-readable `fact_check_recorded` footer
   without automating the human verdict. Then subset #4 (task/handoff linkage)
   and subset #5 (reports views).

## Decisions in effect

- D-S2-1: subset #2 builds the defect-specific projection only; general durable
  export/aggregation/import stays B4 (user-approved 2026-07-23).
- D-S2-2: runtime only — `diagnosing-bugs` stays `planned` with a null event
  ID; no activation, no synthetic/retroactive receipt; `telemetry/producers.py`
  activation block untouched. Activation waits for a real post-mortem defect in
  a future candidate.
- The projection is the closed 13-field T3.10.2 record; the receipt
  `producer.id` is the channel-injected `dat-kit-cli`, never `diagnosing-bugs`.

## Files touched

- `scripts/telemetry.py` — projection writer, `export` subcommand, consuming
  validator, parametrized path helpers, `DEFECT_PROJECTION_TARGET` literal.
- `scripts/validate.py` — imports + defects.jsonl validation branch.
- `scripts/tests/test_telemetry_defect_projection.py` — 16 tests.
- `benchmarks/defects.jsonl` — new committed empty durable artifact (in `78a1991`).
- `.gitattributes`, `benchmarks/scorecard.jsonl`,
  `docs/spikes/phase-6b/b3-observation.md`, `lessons-learned/lessons-learned.md`.

## Verified gates

On the working tree (base `72ca145` + `78a1991` + uncommitted tail):
- `python scripts/validate.py` → PASS.
- `pytest scripts/tests` → `394 passed, 3 skipped`.
- `bash -n scripts/init.sh` → PASS.
- `shellcheck scripts/init.sh` → PASS (0.8.0).
- `git diff --check` → clean.
- `python -m ruff check` (touched files) → clean.
- Red-before-green: dropping `evidence_ref` from the projection writer turned
  the 13-field shape test red; revert restored green.

## Third-party tool risks

- `shellcheck` and `pytest` are absent from a fresh Cowork sandbox; installed
  ad hoc this session (`shellcheck` binary fetched to `/tmp`). Re-provision on a
  new session.
- `mypy` (pinned `2.3.0`) is report-only and was not run — pinned version not
  installable in this environment; non-blocking per R1.

## Next steps

1. Host: `del .git\index.lock .git\HEAD.lock`, then commit (or `--amend` into
   `78a1991` so the `.gitattributes` pin lands with the projection per the
   byte-compare lesson).
2. Re-run `python scripts/validate.py` + `pytest scripts/tests` post-commit.
3. Begin B3 subset #3 (knowledge-work fact-check footer) through build-loop:
   fresh observation, plan, plan-reviewer, approval gate, then build.

## Traps

- Do NOT flip `diagnosing-bugs` to `active` — needs a real post-mortem defect
  and a separate governed activation path; subset #2 does not authorize it.
- Do NOT rewrite existing `benchmarks/defects.jsonl` bytes; export is
  append-only and fails closed on collision.
- Keep contract path values as POSIX literals, never `str(Path(...))`.
- A green gate on a Linux-only run does not prove Windows checkout/separator
  behavior — verify line-ending/path-literal changes against a real
  `git clone -c core.autocrlf=true`.

## Glossary

`defect_recorded` · defect tuple · `benchmarks/defects.jsonl` · projection ·
`benchmark_exported` receipt · `TELEMETRY_EXPORT_COLLISION` ·
`DEFECT_PROJECTION_TARGET` · `planned`/`active` producer · idempotent-by-event_id
