# Phase 6B B3 subset #3 observation and review ledger

## Pre-registration

- Observation task ID: `2fabae17-4b33-4586-9940-21c6e4258871`.
- Registered before the first subset #3 product or test edit on 2026-07-23.
- Immutable scope: subset #3 only — the knowledge-work `fact_check_recorded`
  **footer producer**, delivered as Fork A (define + parse). Two artifacts:
  (1) a machine-readable footer appended to the fact-check deliverable that
  preserves the human verdict section, and (2) a pure parser that maps a footer
  to a validated `fact_check_recorded` payload through the existing validator.
- Intended product/test paths: `domains/knowledge-work/deliverables/
  fact-check.template.md`, `scripts/telemetry.py` (pure
  `parse_fact_check_footer`), `scripts/tests/test_fact_check_footer.py`,
  `.gitattributes` (eol pin for the template).
- Task-local evidence path: `docs/spikes/phase-6b/b3-subset3-observation.md`.
- Closure-only append: `benchmarks/scorecard.jsonl`, after all verdicts.
- Explicit non-goals: producer activation; any synthetic/retroactive receipt;
  a dedicated emit CLI subcommand (Fork B, deferred); task/handoff linkage
  (subset #4); report views (subset #5); general export (B4); any schema,
  engine, Host Adapter, retention, or reporting change.
- One task ID covers the whole subset #3 slice; internal commits do not create
  new observation units.
- Reviewer chain: plan-reviewer returned `REVISE` (three WARNs: gate_id
  convention, input-surface controls, newline/eol handling) — all incorporated
  in the approved plan. Candidate chain: full QA, full code review, full
  security review (parser reads external text), findings-scoped re-review,
  final regression QA.

## Ground-truth answers and auto-decisions

1. The footer carries exactly the T3.6 closed `fact_check_recorded` payload:
   `gate_id` (stable-id), `verdict` (`sourced`/`return_to_builder`),
   `verdict_source` (`human`/`agent`/`automation`), `finding_count` (int ≥ 0),
   `failure_classes` (sorted-unique subset of the seven closed values),
   `evidence_ref` (stable-ref). Source: `docs/contracts/telemetry-v3.md` T3.6
   (lines 281, 290-297) and `scripts/telemetry.py:537-553`.
2. The footer is DERIVED from the human `SOURCED`/`RETURN_TO_BUILDER` verdict
   and preserves it: the parser never computes, overrides, or replaces the
   verdict; `verdict_source` is authored, not forced. Source: T3.12 producer
   responsibility "preserving the human verdict" (line 597).
3. `evidence_ref` points to the numbered finding record; the event carries no
   finding prose. Source: T3.6 lines 296-297.
4. The producer stays `planned`. Fork A adds no activation and no receipt;
   `telemetry/producers.json` is untouched. Emission remains available through
   the existing generic `append` command, which is not a trusted producer
   context. Source: T3.12 lines 597, 601-627.
5. `gate_id` for a fact-check is the single stable id `gate:fact` (the fact-check
   is one gate spanning G2-G6; failure detail lives in `failure_classes`, not in
   a per-finding gate id). Matches the existing example
   `scripts/tests/test_telemetry_cli.py:183`.
6. Failure-class mapping (confirmed against `domains/knowledge-work/reviewers.md`
   and `gates.md`, plan-reviewer verified exact):
   - G2 fidelity — source does not state the claim / no citation →
     `unsupported_claim`; source weaker than the claim → `weaker_than_claim`;
     source contradicts the claim → `contradiction`.
   - G3 reliability → `unreliable_source`.
   - G4 staleness → `stale_source`.
   - G5 adequacy/coverage → `inadequate_coverage`.
   - G6 prose (claim-vs-claim across the document) → `prose_contradiction`.
   `contradiction` (G2, source-vs-claim) and `prose_contradiction` (G6,
   claim-vs-claim) are distinct.
7. Auto-decision: the parser reuses the existing bounded-input path
   (`MAX_RECORD_BYTES`), duplicate-key rejection (`_duplicate_object_pairs`),
   and no-echo `_error` diagnostics; it normalizes `\r\n`/`\r` to `\n` before
   locating the fenced block so a CRLF checkout parses identically. Safest
   reversible reuse of the subset #2 input-surface baseline.

No open question remains; no decision-log file exists in this repository.

## Threat model

| Boundary | Threat | Required control |
|---|---|---|
| Footer text input | Oversized, malformed, non-object, or duplicate-key JSON | Bound bytes before parsing, reject duplicate keys, require an object, never echo the rejected value |
| Verdict authority | Footer forges a `verdict`/`verdict_source` outside the closed enums, or a `sourced` verdict smuggling findings | Validate through the existing `fact_check_recorded` validator (closed enums, sorted-unique classes, `sourced`⇒0 findings, `return_to_builder`⇒>0) |
| Prose leakage | Footer copies finding prose into the event | Only the closed payload fields are extracted; `evidence_ref` carries a reference, never prose |
| Producer status | Parsing/emitting flips the producer to `active` | Parser is pure; no activation path; `producers.json` untouched |
| Newline/encoding | CRLF checkout or non-UTF-8 bytes change the parsed block | Normalize newlines, decode UTF-8 with bounded length, pin the template `eol=lf` |

## Acceptance criteria

- A filled `SOURCED` footer parses to a payload with `finding_count` 0 and empty
  `failure_classes`; a `return_to_builder` footer parses to positive count and a
  non-empty sorted-unique class array.
- Each of the seven closed failure classes round-trips.
- Malformed footers (unsorted/duplicate classes, `sourced`-with-findings,
  missing key, duplicate JSON key, oversized input, non-object) are rejected
  with a stable error and no rejected-value echo.
- The template still contains the human verdict summary and claim-by-claim
  section after the footer is added (verdict preserved).
- `telemetry/producers.json` is unchanged; no producer is activated.
- Targeted tests show red-before-green; canonical full gates and the sequential
  reviewer chain pass on a frozen committed candidate.

## Candidate and invocation ledger

Candidate/base/tree IDs and changed paths are recorded at freeze. Reviewer
invocation rows and pre-freeze receipts are appended only after each fact
exists; this pre-registration claims no future evidence.

## Pre-freeze receipts (2026-07-23)

- Base HEAD at start: `68f5345` (amended subset #2), clean tree, branch
  `feature/telemetry-v3-b3`.
- Changed paths: `scripts/telemetry.py` (pure `parse_fact_check_footer` + 3
  constants), `domains/knowledge-work/deliverables/fact-check.template.md`
  (machine footer), `.gitattributes` (template eol=lf pin),
  `scripts/tests/test_fact_check_footer.py` (26 tests), this observation doc.
  No `*.sh` in the diff (`bash -n`/`shellcheck` N/A).
- Red-before-green: with the parser removed, the targeted suite reported
  `25 failed, 1 passed` (the one pass is the human-section check that does not
  call the parser); with the parser restored, `26 passed`.
- Full gates on the working tree: `python3 scripts/validate.py` PASS;
  `python3 -m pytest scripts/tests -q` `420 passed, 3 skipped`;
  `python3 -m ruff check .` PASS; `git diff --check` clean. `mypy` report-only
  and not installable in-sandbox (skipped, non-blocking per R1).
- Producer unchanged: `telemetry/producers.json`
  `knowledge-work-fact-check.status` remains `planned`, `event_id` null.

## Reviewer chain (2026-07-23)

- plan-reviewer: `REVISE` — three WARNs (gate_id convention, input-surface
  controls, newline/eol handling); all incorporated before the first product
  edit. Failure-class mapping, producer-stays-planned, no-prose, and Fork A
  confirmed correct.
- qa-agent: zero defects across eight spec-edge attacks; failure-class mapping
  exact. Sole open item was gate execution, which its sandbox could not run;
  supplied by the builder's verified green run above (build-loop substitution:
  gate execution is deterministic and diff-scope was confirmed 3+1 files, no
  `*.sh`).
- code-reviewer: `APPROVE`. N1 (no-echo test strengthened) applied; N2 (no
  production caller) is intended Fork-A staging.
- security-reviewer: `APPROVE`, zero CRITICAL/HIGH/MEDIUM findings; two lesson
  candidates (pre-decode boundary ownership; single-validator reuse pattern).
- Final regression gates re-run green after the N1 test edit.

The closure commit is the commit introducing this section plus the scorecard
append; it is identified by Git history, never by a self-referential hash.
