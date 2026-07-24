# Phase 6B B3 subset #5 observation and review ledger

## Pre-registration

- Immutable scope: subset #5 only — the two **reports-producer read-only views**,
  derived from an already-validated lifecycle corpus: a per-reviewer view and an
  event-coverage-rate view (telemetry-v3 T3.12). Two pure functions in
  `scripts/telemetry.py` (`build_per_reviewer_view`, `build_event_coverage_rate_view`)
  plus one supporting helper (`_latest_terminal_coverage_status`). No CLI, no emit,
  no producer activation.
- Intended product/test paths: `scripts/telemetry.py` (two public view functions +
  one private helper, placed beside the coverage helpers; no new path/enum literal,
  no new committed corpus, no schema/validator change),
  `scripts/tests/test_telemetry_reports.py` (new).
- Supporting docs: `docs/decisions/0003-report-view-host-and-window.md` (host/window
  mapping, D-1), this observation, `plans/PLAN-phase6b-b3-subset5-report-views.md`.
- Closure-only append: `benchmarks/scorecard.jsonl`, after all verdicts, with a
  post-append `validate.py` re-run (lessons-learned 2026-07-21).
- Explicit non-goals: producer activation (`reports` stays `planned`, `producers.json`
  untouched); any CLI subcommand (D-2 — a generic CLI is not a trusted context,
  T3.12 ~616); time-window slicing (deferred to B4); the `domain_id` envelope field
  (needs the v8 task-loop branch; deferred); any schema, validator, engine, Host
  Adapter, retention, or export change.
- Gate tier: **C** (execution code in `telemetry.py`) — PLAN-v8 §6: Tier A + `pytest`
  + one sequential reviewer; security only if a path/external-input surface is touched.

## Ground-truth answers and decisions

1. **Per-reviewer view** groups original `review_result` rounds by
   (`reviewer_id`, `reviewer_class`) and joins `defect_recorded.approving_reviewers`
   on the stable reviewer ID. It reports association, not causal blame, and never
   drops a defect (T3.12 ~629–634). Producer identity is never substituted for
   reviewer identity — the view reads only reviewer-authored fields.
2. **Event-coverage-rate view** = tasks whose latest valid terminal coverage is `full`
   over all completed tasks observed by finish or scorecard, per host (T3.12 ~636–646).
   Completion-only, partial, and aborted tasks remain in the denominator; a host with
   zero completed tasks reports `rate: null`, reason `no_observed_tasks`.
3. **D-1 (decision 0003):** host = `revisions.adapter.value`; window = whole corpus this
   subset (time-slicing deferred to B4). The envelope has no `host`/`window` field and
   none is added.
4. **D-2:** views are pure functions, no CLI subcommand — a generic CLI is not a trusted
   LOAD/HARVEST context (T3.12 ~616), and read-only derivation must not be confused with
   producer activation.
5. **D-3:** "completed task" in the denominator = terminal-observed (an original
   `task_finished` OR `scorecard_imported`), regardless of `outcome`; an
   `outcome=aborted` task is terminal-observed and counts. The contract defines the
   denominator by "observed by finish or scorecard", i.e. terminal-observation, and
   confirms completion-only/partial stay in it (T3.12 ~644).

### Load-bearing correctness finding (plan-reviewer round 1, BLOCKER)

The numerator must use the **latest valid terminal coverage**, which is correction-aware
(T3.5.1 ~207–209). Reusing `_expected_coverage` for the numerator is wrong: it runs only
on `_task_originals` (corrections filtered out) and *recomputes* coverage from event-type
presence, so a `task_finished` later corrected to a different terminal coverage would be
scored on its pre-correction value. The view instead reads the stored `coverage.status`
off the latest event in the correction chain rooted at the original `task_finished`
(`_latest_terminal_coverage_status`), never an in-progress snapshot.

## Threat model

| Boundary | Threat | Control |
|---|---|---|
| View input | Malformed / hostile event reaches the view | Views run on the already-validated corpus (`validate_event`); tests re-validate every fixture, so no second validation copy exists |
| Producer status | A view flips `reports` to `active` | No activation path; `producers.json` untouched; derivation only |
| Path / shell | New untrusted path or command surface | None — pure in-memory derivation; no file read/write, no CLI, no path/enum literal added |
| Blame vs association | Producer identity masquerades as reviewer identity | Per-reviewer view keys on reviewer-authored `reviewer_id`/`reviewer_class`; defects join on `approving_reviewers`; unknown/unlinked defects surfaced, not dropped |

Security-reviewer is therefore **SKIP-eligible** (argued): no path/input/external-write
surface is added (PLAN-v8 §6 footnote²). Stated at the gate, not silent (lessons 2026-07-21).

## Acceptance criteria

- Per-reviewer view: rounds and verdicts grouped per (reviewer_id, reviewer_class);
  defect joins on `approving_reviewers`; empty-approving defect → `unlinked_defects`;
  an approving ID with no review → `unknown_reviewers` while known co-approvers stay
  linked; corrections do not double-count.
- Coverage-rate view: numerator only full via latest valid terminal coverage
  (correction-aware); denominator keeps completion-only, partial, aborted, scorecard-only;
  zero completed → `null` + `no_observed_tasks`; grouped and sorted by host.
- `reports` producer stays `planned`; `producers.json` unchanged.
- Targeted tests red-before-green; canonical full gates green on the candidate.

## Pre-freeze receipts (2026-07-24)

- Red-before-green: with the two view functions absent, `test_telemetry_reports.py`
  reported `13 failed` with `AttributeError: module 'telemetry' has no attribute
  'build_*_view'` (fixtures validate cleanly through the unchanged `validate_event`;
  the only missing symbols were the views). With the functions added, `13 passed`.
- Full gates on the working tree (Linux sandbox — `validate.py` false-reds on Windows
  via `UnicodeEncodeError` on the `✓` print): `python3 scripts/validate.py`
  `✓ all checks green` (RC 0); `python3 -m pytest scripts/tests -q`
  `454 passed, 3 skipped` (baseline 441 + 13 new); `ruff check .` `All checks passed`;
  `git diff --check` clean. No `*.sh` in the diff → `bash -n`/`shellcheck` N/A. `mypy`
  report-only, not installed in-sandbox (skipped, non-blocking per R1).
- Scorecard append re-validated: `validate.py` re-run `✓ all checks green` after the
  `benchmarks/scorecard.jsonl` append (lessons-learned 2026-07-21).

## Reviewer chain (2026-07-24)

- plan-reviewer: `REVISE` → all five findings folded before any code
  (1 BLOCKER correction-aware numerator; 2 aborted-denominator → D-3; 3 decision-log
  path → `docs/decisions/0003`; 4 mixed known/unknown approving edge → `unknown_reviewers`;
  5 malformed per-reviewer shape / stray `first_pass`). Approved to build by the owner.
- code-reviewer: `RETURN` → `APPROVE`. Round 1 RETURN, one BLOCKER: a
  `defect_recorded` whose `approving_reviewers` were ALL unknown surfaced in no defect
  list (dropped defect, T3.12 L633-634) — only the mixed case was saved by a known
  co-approver. Two minor findings: scorecard-path numerator not correction-aware; test
  gaps. Fixed: the defect loop now tracks `matched_known` so empty-approving AND
  all-unknown both land in `unlinked_defects` (mixed stays linked); both terminal kinds
  route through `_latest_terminal_coverage_status`; two tests added (all-unknown defect,
  multi-level correction chain). Round 2 APPROVE, findings-scoped, all three verified.
- security-reviewer: SKIP — argued above (no path/input/external-write surface); code
  and qa concur (pure in-memory derivation).
- qa-agent: `PHASE DONE` (static — no executor in its subagent context, correct refusal
  per lessons-learned 2026-07-23; mechanical gates supplied by the builder's verified
  green run above). Attacked every spec-named edge (dropped-defect empty/all-unknown,
  mixed approver, single+multi-level correction numerator, completion-only/partial/
  aborted/scorecard-only denominator, zero→null, multi-host sort, no producer
  activation) — all pass. Two non-blocking observations: (1) the per-reviewer view is
  correction-*excluded* (uses `_originals`) while the coverage view is correction-*aware*,
  so a corrected `review_result`/`defect_recorded` shows the original value there — T3.12
  does not define correction handling for the per-reviewer view, so this is a documented
  choice, not a violation; (2) coverage-view host is read from the original terminal
  event while status follows the correction tip — a latent edge only if a correction ever
  changed `revisions.adapter`, which corrections copy in practice.

The closure commit is the commit introducing these receipts plus the scorecard append;
it is identified by Git history, never by a self-referential hash.
