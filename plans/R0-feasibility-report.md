# R0 — Feasibility Measurement Report

**Date:** 2026-07-22 · **Status:** COMPLETE — decision taken, see
`DECISION-2026-07-22-unify-receipt-gate-and-review-economy.md`
**Plan:** PLAN-external-verification-receipt-gate-v2.md, phase R0

---

## 1. GREEN rate (measured, not estimated)

Yellow triggers (path-based, per plan §7/v2 §4-R3) applied to real history:

| Unit | Sample | GREEN | YELLOW | Notes |
|---|---|---|---|---|
| **Commit** | last 40 (39 excl. merge) | 17 (44%) | 22 (56%) | GREEN = docs/handoff/scorecard-only diffs |
| **Task (review unit)** | all 32 scorecard records | 5 (16%) | 27 (84%) | The unit that actually gets a reviewer chain |

Key nuance: commit-level GREEN (44%) is misleading — dat-kit reviews per
**task/phase**, and docs-only commits live *inside* yellow phases. At the
review-unit level GREEN is **16%**, and those 5 docs-only tasks already run a
reduced chain today (security-reviewer explicitly skipped on docs-only diffs).

**Marginal value of a GREEN receipt path (R3): LOW.** Confirms deferring R3.

Yellow-trigger breakdown across the 22 yellow commits: `scripts/telemetry.py`
lifecycle/atomicity code, existing-test modification, `docs/contracts/`,
`telemetry/schema-v3.json`, `registry/`, `docs/decisions/`, one
`.github/workflows/` touch. The work profile IS the yellow list, as predicted.

## 2. Token baseline (finding: scorecard cannot provide one)

- 31/32 records have `tokens: unknown` — reasons: `unsupported_provider` (9,
  all Codex sessions), `no_matching_session` (13), absent (9).
- Only exact anchor: Phase 0B full session = **529,479 tokens** (Claude).
- **Consequence:** post-R1/R2 savings must be measured by **reviewer-invocation
  counts + wall time**, not tokens. (v2 already anticipated this; now confirmed.
  This aligns with Review Economy v3's invocation-ledger approach — see the
  unification decision.)

## 3. Reviewer-invocation baseline (proxy metric, undercounted — terse notes)

| Signal | Count / 32 tasks |
|---|---|
| QA agent ran | ≥ 7 (plus in-gates evidence of pytest re-run "3×", "6×" per session) |
| code-reviewer ran | ≥ 10 |
| security-reviewer ran | ≥ 8 (5 explicit docs-only skips) |
| **Tasks with re-review / fix-up loops** | **13 (41%)** |
| Avg wall time | 64 min/task (n=24, total 1,531 min) |

The 41% re-review loop rate is the B2 pain made visible: reviewer agents get
re-invoked as fixes land, re-reading context each time.

## 4. CI reality check

- Current pipeline: 2 jobs only (ubuntu: validate+pytest+shellcheck; windows:
  validate+pytest), Python 3.12. Adding Ruff + `--junitxml` + artifact upload
  is a small diff. Latency budget ≤ 4 min is realistic.
- `requirements-dev.txt` = 2 deps (PyYAML, pytest) → **pip-audit as a gate:
  confirmed near-zero value** (monthly advisory at most).

## 5. Projected savings vs build effort

| Investment | Effort | Applies to | Projected recurring effect |
|---|---|---|---|
| **R1** QA-elimination (CI evidence + summary.json + gh-read intake) | 1–2 days | **100% of tasks** | In-context re-execution of pytest/validate (observed 3–6× per session) → 0; environment-retry loops → 0 |
| **R2** yellow-collapse (3 agents → 1 scoped review) + B2 regressions | 1 day | **84% of tasks** | ~2 reviewer invocations saved per substantive task; 41% re-review loops shrink to scoped re-checks |
| **R3** GREEN receipt + verifier + authority | ~1 wk | **16% of tasks** (already reduced-chain) | Marginal — near zero |

## 6. R0 gate verdict

**PROCEED with R1 + R2.** Two to three days of build against a recurring
saving on every future task; the invocation baseline above is the before-
picture for the R2 exit metric (3 → 1 per substantive task).
*(Post-decision note: R2 is additionally gated by Review Economy v3 Stage A —
the 3-task ledger supersedes this report's coarser baseline as the R2
before-picture.)*

**DEFER R3 indefinitely.** Measured GREEN rate at the review-unit level (16%,
already cheap tasks) cannot pay back the receipt/verifier/authority machinery.
Revisit only if the work profile shifts toward routine feature code (re-run
this classification — the script is one command).

**Amendment to v2 metrics:** replace "token delta from scorecard.jsonl" with
"reviewer-invocation count + wall-time delta" until token attribution for
Codex sessions exists.

---
*Method: git log --name-status classification against path-based yellow
triggers; scorecard.jsonl parsed programmatically; counts are regex-based on
terse notes and therefore lower bounds.*
