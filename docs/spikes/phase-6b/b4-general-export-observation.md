# Phase 6B B4 observation and review ledger

## Pre-registration

- Immutable scope: B4 only — the **general event export** to
  `benchmarks/telemetry-v3.jsonl` (telemetry-v3 T3.10.2), the piece missing after
  subset #2's defect projection. Copies every eligible validated event WHOLE to the
  committed, append-only corpus; idempotent by `event_id`; emits `benchmark_exported`;
  activates no producer.
- Product paths: `scripts/telemetry.py` (`GENERAL_EXPORT_PATH`/`GENERAL_EXPORT_TARGET`
  constants, `_export_eligible` helper, `export_event_corpus`, and CLI wiring — extend
  `export --target` choices + a dispatch branch), `.gitattributes` (new `eol=lf` pin),
  `benchmarks/telemetry-v3.jsonl` (0-byte committed corpus), `scripts/tests/test_telemetry_general_export.py` (new).
- Supporting: `plans/PLAN-phase6b-b4-general-export.md`, this observation.
- Closure-only: `benchmarks/scorecard.jsonl` append + post-append `validate.py` re-run.
- Gate tier: **C with the §6 footnote² security condition triggered** — new file path +
  privacy eligibility filter + committed byte-exact corpus.

## Ground-truth decisions

1. **Scope corpus-wide, receipt task-attributed (D-1).** Mirrors the shipped
   `export_defect_projection` (`telemetry.py`): it selects events corpus-wide and uses
   `task_id` only for the receipt's `parent_task_id`/`delegation_id` lineage.
2. **Separate function + separate receipt per target (D-2).** `benchmark_exported.target_path`
   is a single-value enum per receipt; each export operation targets one path and emits one
   receipt. `export_defect_projection` is left byte-for-byte unchanged; only a CLI dispatch
   branch is added.
3. **Wire the existing `export` CLI (D-3).** The `export` subcommand already ships
   (`--target`, dispatched to the defect export); the faithful mirror extends `--target`
   choices with `benchmarks/telemetry-v3.jsonl` and branches to `export_event_corpus`. This is
   not producer activation — export emits a receipt, never flips a producer.
4. **Eligibility = exclude `local_private` (T3.9) + `benchmark_exported` (T3.10.2 L545);**
   everything else — `project`/`public`, every type, corrections — copied whole. Factored into
   the pure `_export_eligible` helper for direct testing.
5. **Existing-target parser = `_split_history` (schema + ID-uniqueness + correction-shape),
   never `validate_lifecycle_events`** — the eligible subset is not a complete lifecycle corpus
   (no receipts, filtered `local_private`), so a lifecycle validator would falsely reject it.

### Load-bearing correctness / security invariant (plan-reviewer finding 3)

`_split_history` → `_validate_existing_corpus` requires every stored correction's `correction_of`
to name an earlier record IN the target file. This is safe ONLY because privacy monotonicity
(`_validate_correction_shape`, a correction may never loosen privacy) guarantees an eligible
(`public`/`project`) correction can never target an excluded `local_private` original — the
original would have to be `local_private` too, hence also excluded, and its correction with it.
The invariant is asserted at the helper level (`_export_eligible` excludes `local_private`), not
assumed. Also load-bearing: the export receipt is a lifecycle event, so it must be owned by a
still-open task — a receipt cannot append after its own task's `task_finished` (tests use a
separate open exporter task when finished data is exported).

## Threat model (for the mandatory security review)

| Boundary | Threat | Control |
|---|---|---|
| `--target` CLI input | Arbitrary path → traversal/writes outside repo | Closed `choices` enum in argparse; unknown value → `command line is invalid`, no echo (redaction test) |
| Committed corpus write | Symlink / parent swap / mid-write identity change | Reuses the proven `_verify_parent`/`_verify_target_before_open`/`_handle_identity` before+after `os.write`, `O_NOFOLLOW`, `_WRITE_LOCK` |
| Privacy leak | `local_private` event reaches the committed corpus | `_export_eligible` excludes `local_private` (unit-tested); export copies only the eligible list |
| Endless receipt tail | `benchmark_exported` copied → receipts about receipts | `_export_eligible` excludes `benchmark_exported` (unit + end-to-end tests) |
| Idempotency / tamper | Re-export duplicates or silently overwrites committed bytes | Collision-by-`event_id` (`TELEMETRY_EXPORT_COLLISION`); append-only; no-op emits no receipt |
| Path literal | `str(Path)` backslash self-rejects on Windows | `GENERAL_EXPORT_TARGET` POSIX literal for `target_path`/`--target`; `Path` only for filesystem joins |

## Pre-freeze receipts (2026-07-24)

- Red-before-green: with the new symbols absent, the suite failed at collection with
  `AttributeError: module 'telemetry' has no attribute 'GENERAL_EXPORT_PATH'`; after the
  constants/helper/function/CLI landed, an intermediate run surfaced the real
  receipt-after-finish lifecycle constraint (`TELEMETRY_LIFECYCLE_INVALID`) which was fixed by
  owning the receipt with an open exporter task. Final: `15 passed`.
- Full gates (Linux sandbox — `validate.py` false-reds on Windows on the `✓` print):
  `python3 scripts/validate.py` `✓ all checks green` (RC 0); `python3 -m pytest scripts/tests -q`
  `471 passed, 3 skipped` (baseline 456 + 15 new); `ruff check .` `All checks passed`;
  `git diff --check` clean. No `*.sh` in the diff → `bash -n`/`shellcheck` N/A. `mypy`
  report-only, not installed in-sandbox (skipped, non-blocking per R1).
- `.gitattributes` pin verified active: `git check-attr text eol -- benchmarks/telemetry-v3.jsonl`
  → `text: set`, `eol: lf`. The corpus is committed 0-byte, so there are no bytes for a
  `core.autocrlf` checkout to rewrite yet; the pin is in the same change that introduces the
  corpus (lessons-learned 2026-07-20 & 07-23).
- Scorecard append re-validated: `validate.py` re-run green after the append (lessons 2026-07-21).

## Reviewer chain (2026-07-24)

- plan-reviewer: `RETURN` → all five findings folded before code (1 BLOCKER: false "no CLI"
  claim → wire the existing `export` CLI; 2 add the "ALSO"-clause test; 3 constrain the target
  parser to `_split_history` + assert the privacy-monotonicity invariant; 4 commit the
  partial-failure test unconditionally; 5 fix the "Tier D-lite" label to Tier C). Approved to build.
- code-reviewer: `APPROVE`. One non-blocking duplication note — `export_event_corpus` is a
  ~90-line intentional mirror of `export_defect_projection`; extracting a shared
  `_append_export_batch` helper would remove it but is deferred (D-2 keeps the shipped defect
  export untouched; both blocks are proven). Recorded as a lesson candidate.
- security-reviewer: `APPROVE`, no findings (MANDATORY for this phase). Confirmed the privacy-leak
  invariant is unbreakable: monotonicity (`_validate_correction_shape` rank check) means an
  eligible correction can only target an eligible original, so neither a mixed-privacy corpus nor
  the `_split_history` read-back can smuggle a `local_private` event or a dangling `correction_of`
  into the committed corpus. Path safety, redaction, collision/append-only integrity, and no
  producer activation all verified.
- qa-agent: `PHASE DONE` (static — no executor in its subagent context; mechanical gates from the
  builder's verified run above, per lessons-learned 2026-07-23). All 11 attack lenses pass
  (local_private leak, receipt tail, idempotency, collision, receipt-after-append, prior_hash, no
  activation, disabled, redaction, `_split_history` false-reject, 0-byte init). Raised one
  contract-interpretation item for the owner (below), not a code defect.

### "ALSO"-clause interpretation — ratified D-2 (owner decision)

Contract L509-511: "General export copies the complete eligible validated event to
`telemetry-v3.jsonl`. A `defect_recorded` event ALSO appends this closed projection to
`defects.jsonl`." A strict single-operation reading would have one general export of a
`defect_recorded` write BOTH targets. B4 does NOT: it writes only `telemetry-v3.jsonl`; the
projection stays the separate `--target defects.jsonl` operation (shipped `export_defect_projection`).
Rationale (D-2, owner-approved 2026-07-24): `benchmark_exported.target_path` is a single-value enum
per receipt, so one operation = one target = one receipt; a cascading write would need two receipts
or an impossible two-target receipt, and would entangle the two targets' partial-failure semantics.
The owner ratified the separate-operation reading; revisiting to a cascade would return to the
builder as a new unit.

The closure commit is the commit introducing these receipts plus the scorecard append; it is
identified by Git history, never by a self-referential hash.
