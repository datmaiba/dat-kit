# HANDOFF 2026-07-13 — dat-kit pivot to a general "AI-usage per type of work" toolkit

## Goal
Evolve dat-kit from a dev-only spec-driven toolkit into a general work-discipline toolkit where "type of work" is a plug-in **Domain Pack** and Anthropic's 4 loops (Turn/Goal/Time/Proactive) are an orthogonal axis. Plan lives in `PLAN-general-work-loop-v2.md` (currently at revision v3). This session executed Phase 0 → Phase C — all **additive**, no structural refactor, v1.7.0 behaviour untouched.

## State
- **DONE (uncommitted — nothing committed this session; base commit 95f732a):**
  1. `PLAN-general-work-loop-v2.md` — plan revised through v3 after two independent subagent reviews (v1 6/10; v2 "revise by cutting"). Model = one engine × (Domain axis, Loop axis); capability ladder = loop unlocked by gate quality.
  2. **Phase 0** — `drafts/knowledge-work-gates.draft.md`: paper validity check on knowledge-work gates. Verdict: valid non-gameable gates exist; load-bearing gate is human-run → premise HOLDS.
  3. **Phase A (docs)** — `docs/loops.md` (two-axis model + ladder) and advisory `skills/build-loop/loop-profile.md`.
  4. **Phase B (mechanism)** — new skill `skills/domain-builder/SKILL.md`: interview a practitioner, fill 5-slot contract, enforce gate-validity (worked cases + gaming line + sign-off), cap interview-authored domains at Turn/Goal.
  5. **Phase C (proof)** — full `skills/knowledge-work/` pack (SKILL.md + ground-truth.md + gates.md + reviewers.md + loop-profile.md + deliverables/report.template.md); `docs/domains.md` registry (software-dev referenced in place → build-loop; knowledge-work); 2 eval cases appended to `benchmarks/skill-evals.jsonl`.
  - This completes the plan's **minimum viable pivot** DoD.
- **IN PROGRESS:** none. All files written and validated; nothing half-built.
- **NOT STARTED (deferred by design, in order):**
  1. Release chore for the additive work: bump version in BOTH `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (1.7.0 → 1.8.0), commit, push, confirm CI green. (Manual by design per README.)
  2. **Phase D** — structural cutover (`skills/core/` + `domains/`, extract `loop-def.md`, fold fable-mode+fable-pro → fable-core copying disclaimers verbatim, relocate build-loop). ONE-WAY DOOR — gated: do only if the additive pivot demonstrably helps a real non-dev task. Burns `2.0.0`.
  3. **Phase E** — `runners/` (Time via create_scheduled_task; Proactive notify-only). Only after a domain has a dogfooded automated gate.

## Decisions in effect
No `spec/08-decisions.md` in this repo (it's the plugin repo, not a scaffolded project). Session-local decisions, recorded here:
- **DL-1 Additive-first:** prove the thesis with new skills only; no folder moves until Phase D. (Reason: moving build-loop breaks `validate.py` for zero user benefit.)
- **DL-2 software-dev referenced, not relocated:** its contract lives inside `skills/build-loop/` + its loop-profile.md; registry points at it.
- **DL-3 Gate validity, not just measurability, sets the loop ceiling:** interview alone never unlocks Time/Proactive.
- **DL-4 Honesty scope:** only encode domains the author/a supplying practitioner actually practices.
- **DL-5 Stay on 1.x for all additive phases; burn 2.0.0 only at the Phase-D go/no-go.**

## Files touched (all uncommitted)
- `PLAN-general-work-loop-v2.md` (new) → the v3 plan.
- `drafts/knowledge-work-gates.draft.md` (new) → Phase 0 paper test.
- `docs/loops.md` (new) → two-axis model + ladder.
- `docs/domains.md` (new) → domain registry.
- `skills/build-loop/loop-profile.md` (new) → advisory; SKILL.md NOT modified.
- `skills/domain-builder/SKILL.md` (new) → the mechanism.
- `skills/knowledge-work/` (new, 6 files) → first non-dev pack.
- `benchmarks/skill-evals.jsonl` (modified) → +2 positive cases (`trg-dombuilder-01`, `trg-knowwork-01`).

## Gates
- `python3 scripts/validate.py` → **✓ all checks green** (last run this session, after every phase incl. the eval-case append).
- `skills/domain-builder` description length: 853 chars (limit 1024).
- Eval trigger uniqueness confirmed: `create a domain pack` only in domain-builder; `write a researched report` only in knowledge-work — no collisions.

## Next steps
1. `cd` to repo, run `python3 scripts/validate.py` — confirm still green before touching anything.
2. Decide release: if publishing the additive work, bump `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` to `1.8.0`, then `git add -A && git commit && git push`; watch the GitHub Actions tab go green.
3. Before any Phase D work: run knowledge-work on ONE real non-dev task end-to-end (draft → gates → fact-check → SOURCED). If it doesn't demonstrably help, STOP — do not do the structural cutover (kill-switch, plan §8).
4. Only after step 3 succeeds: open Phase D per `PLAN-general-work-loop-v2.md` §7.

## Traps
- Do NOT move or rename `skills/build-loop/` before Phase D — `validate.py` §3b hardcodes `skills/build-loop/SKILL.md` as the reviewer-table source of truth; the flat glob `skills/*/SKILL.md` also assumes one-level skill dirs.
- Personal-info gate (`validate.py` §5) bans certain strings repo-wide — keep examples generic (the knowledge-work pack uses Vietnam VAT examples, which are fine).
- Adding a new skill silently in scope of an existing trigger risks real-world collision even when `validate.py` passes (it only checks phrases named in eval cases). Chose NOT to make software-dev a triggerable skill for this reason.
- Running plugin sessions use the version loaded at startup — open a NEW session (or `/reload-plugins`) to pick up these skills.

## Glossary
Domain Pack; 5-slot contract (ground-truth, gates, reviewers, deliverables, loop-profile); capability ladder; loop ceiling; gate-validity check (worked cases + gaming line + sign-off); Turn/Goal/Time/Proactive; additive-first; one-way door (Phase D).
