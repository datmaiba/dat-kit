# HANDOFF 2026-07-23 — B3 subset #3 context: knowledge-work fact-check footer

## Goal

Prepare and execute Phase 6B B3 **subset #3 only**: the knowledge-work
`fact_check_recorded` producer — a **machine-readable fact-check footer** on the
knowledge-work fact-check deliverable that **preserves the human verdict** and
does not automate it. Not yet planned, approved, or implemented.

Contract responsibility (telemetry-v3 T3.12): "emit a machine-readable
`fact_check_recorded` footer while preserving the human verdict"; required
evidence before `active` = "a real knowledge-work task with human-vs-agent-vs-
automation source distinguished." Follow the subset #2 precedent: build the
footer + emitter **runtime and tests only**, keep the producer `planned`; do
NOT synthesize a receipt to activate it.

## Runtime

Recommended executor: **Claude Opus** (cross-layer: domain deliverable +
telemetry emitter + verdict-vocabulary mapping + tests). Sonnet only after an
approved plan reduces a task to bounded pattern edits. Review agents Opus.

## Workflow

`dat-kit:build-loop`, `software-dev` Domain Pack, attended. Independently
planned, observed, reviewed, approved. **Plan-gated**: draft plan →
`plan-reviewer` → STOP for explicit user approval before any product edit.

## Canonical contract

`dat-kit 1.16.0`. Read root `AGENTS.md` → `docs/agent-workflow.md`,
`docs/agent-working-rules.md`, `lessons-learned/lessons-learned.md` first.

## Git state (expected at start)

- Branch: `feature/telemetry-v3-b3`.
- HEAD should be the amended subset #2 commit (`78a1991` or its amend) — the
  defect projection landed. Verify with `git log --oneline -3` and a clean tree
  before starting. If the tree is dirty, read the newest `handoffs/` file first.
- Subset #2 left these committed: `benchmarks/defects.jsonl` (empty), the
  telemetry export runtime, and the `.gitattributes` `eol=lf` pin for it.

## Known surfaces (verified this session — do not re-derive, but confirm)

- **Telemetry event already validated**: `scripts/telemetry.py:537-553`
  validates `fact_check_recorded` with closed payload `{gate_id (stable-id),
  verdict (sourced|return_to_builder), verdict_source (human|agent|automation),
  finding_count (int≥0), failure_classes (sorted-unique array), evidence_ref
  (stable-ref)}`. Closed failure classes: `unsupported_claim`,
  `weaker_than_claim`, `contradiction`, `unreliable_source`, `stale_source`,
  `inadequate_coverage`, `prose_contradiction`. Rule: `sourced` ⇒ finding_count
  0 and empty classes; `return_to_builder` ⇒ count>0 and non-empty classes.
- **Contract prose**: telemetry-v3 §T3.6 note (around lines 290-297) — `sourced`
  is the machine value for the charter's `SOURCED` verdict; `evidence_ref`
  points to the complete numbered finding record and **telemetry never copies
  its prose**. Producer status/activation rules: T3.12 (producer stays
  `planned` until a real receipt; the generic CLI is not a trusted producer
  context).
- **Producer registry**: `telemetry/producers.py` + `telemetry/producers.json`
  — `knowledge-work-fact-check` is `planned`, event_id null. The validator
  hard-rejects any `active` entry (subset #1 lockdown). Leaving it `planned`
  needs no change there. Do NOT touch the activation block.
- **Deliverable to extend**: `domains/knowledge-work/deliverables/
  fact-check.template.md` (human-facing prose: verdict summary + claim-by-claim
  table + verification record). The machine footer is ADDED to this, preserving
  the human verdict section.
- **Verdict vocabulary source**: `domains/knowledge-work/gates.md`,
  `domains/knowledge-work/reviewers.md`, `domains/knowledge-work/workflow.md` —
  the human gates are G2 (source states the claim), G3 (reliability), G4
  (staleness), G6 (contradiction), plus coverage. The plan must map this human
  vocabulary to the closed `failure_classes` enum (e.g. G2→`unsupported_claim`/
  `weaker_than_claim`, G3→`unreliable_source`, G4→`stale_source`,
  G6→`contradiction`/`prose_contradiction`, coverage→`inadequate_coverage`) —
  **confirm the exact mapping against reviewers.md, do not assume it.**
- **Existing tests to mirror**: `scripts/tests/test_knowledge_work_pack.py`,
  `scripts/tests/test_telemetry_cli.py` (a `fact_check_recorded` append example
  already exists ~line 189), `scripts/tests/test_telemetry_defect_projection.py`
  (subset #2's pattern: red-before-green, disabled, redaction, producer stays
  planned).
- **CLI dispatch**: `scripts/telemetry.py` `_parser()` / `_execute_command()`
  (~line 1410+) and the disabled-mode set in `main()` — the subset #2 `export`
  subcommand shows the wiring pattern if an emit/footer command is needed.

## Decisions to carry in (mirror subset #2)

- **Runtime + tests only; producer stays `planned`.** No synthetic/retroactive
  receipt; activation waits for a real knowledge-work task (separate candidate).
- **Preserve the human verdict.** The footer is machine-readable metadata
  DERIVED from the human `SOURCED`/`RETURN_TO_BUILDER` decision; it must not
  replace, override, or auto-compute that decision. `verdict_source` is `human`
  when a person judged; `agent`/`automation` only when genuinely so.
- **No prose copy into telemetry.** `evidence_ref` points to the numbered
  finding record; the event never carries the finding prose (T3.6).
- **Contract path/enum values are POSIX literals**, never `str(Path(...))`
  (subset #2 Windows lesson, 2026-07-23).
- **Any new byte-compared committed artifact needs its own `.gitattributes
  eol=lf` pin in the same commit** (2026-07-20 + 2026-07-23 lessons).
- Scope boundary: this is subset #3 only. Task/handoff linkage (#4) and report
  views (#5) and general export (B4) are OUT.

## Open questions to resolve in the plan (not before)

1. **Footer format**: what exact machine-readable block goes into
   `fact-check.template.md` (fenced JSON? a structured trailer table?) and how a
   helper parses it into the `fact_check_recorded` payload. Decide in-plan;
   plan-reviewer audits it.
2. **Failure-class mapping**: the precise G2/G3/G4/G6/coverage →
   `failure_classes` map, confirmed against `reviewers.md`. This is load-bearing
   correctness — get it exact.
3. **Emitter surface**: is there a CLI/helper that reads the footer and emits
   `fact_check_recorded` (mirroring subset #2's `export`), and does it stay
   `planned` (emit into local stream but no activation)? Or is subset #3 just
   the footer format + validator with emission deferred? Frame both, recommend
   one, and treat "does subset #3 emit or only define the footer" as the pivotal
   fork to confirm with the user (like subset #2's two forks).

## Suggested first steps for the executing session

1. `git log --oneline -3` + `git status` — confirm subset #2 landed and the tree
   is clean; read this file first.
2. Read telemetry-v3 §T3.6/§T3.12, `scripts/telemetry.py:537-553` and
   `:1070-1145` (fact-check coverage), and the four
   `domains/knowledge-work/*.md` gate/reviewer/workflow files.
3. `python scripts/registry.py explain-evolution <path>` for every proposed new
   path before planning.
4. Create a fresh subset #3 observation (pre-registration) +
   complete plan (scope, footer format, exact failure-class mapping, threat
   model, red-before-green test list, rollback, reviewer chain, budget, demo).
5. Dispatch `plan-reviewer`; present with verdict; STOP for explicit user
   approval before editing product files.
6. On approval: build in dependency order, run gates (validate, pytest, bash -n,
   shellcheck, diff-check, ruff) with red-before-green for any new gate, then
   qa-agent → code-reviewer → security-reviewer (if paths/input touched) →
   regression qa → HARVEST (scorecard FIRST then validate.py; lessons; 5-part
   wrap-up).

## Verified gates (subset #2 baseline, for reference)

`python scripts/validate.py` PASS · `pytest scripts/tests` `394 passed, 3
skipped` (Linux) / telemetry subset `85 passed, 3 skipped` (Windows) · `bash -n`
PASS · `shellcheck` 0.8.0 PASS · `git diff --check` clean · `ruff` clean. Note:
one pre-existing `test_contract_check.py` test fails only under Microsoft Store
Python (WinError 1920 copying the exec alias) — environment, not code; use a
python.org interpreter for a clean full-suite run.

## Third-party tool risks

- A fresh Cowork sandbox lacks `pytest` and `shellcheck`; install ad hoc
  (`pip install --break-system-packages pytest`; fetch shellcheck binary).
- `mypy` (pinned `2.3.0`) is report-only and not installable in-sandbox; skip,
  non-blocking per R1.
- Git writes on the Cowork mount can leave an unremovable `.git/index.lock`;
  clear it host-side (`del .git\index.lock .git\HEAD.lock`) if commits stall.

## Traps

- Do NOT auto-decide a human fact-check verdict; the footer preserves it.
- Do NOT flip `knowledge-work-fact-check` to `active` without a real receipt.
- Do NOT copy finding prose into the telemetry event (`evidence_ref` only).
- Do NOT assume the failure-class mapping — confirm against `reviewers.md`.
- Keep contract values POSIX literals; pin any new byte-compared artifact.

## Glossary

`fact_check_recorded` · machine-readable footer · `SOURCED` /
`return_to_builder` · `failure_classes` (7 closed values) · `verdict_source`
(human/agent/automation) · `evidence_ref` (numbered finding record, no prose) ·
`planned`/`active` producer · knowledge-work Domain Pack
