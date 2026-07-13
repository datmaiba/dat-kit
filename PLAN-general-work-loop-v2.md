# dat-kit → General Work-Loop — Plan v3

> Status: **PROPOSAL, not started.** v3 after two independent reviews (v1 sketch 6/10; v2 → "revise by cutting"). Current shipped plugin is v1.7.0 and must keep working. Guiding change in v3: **prove the thesis additively before moving a single file. No structural refactor until it has paid for itself.**
> Date: 2026-07-13 · Owner: Dat (solo maintainer, dev background)

## 1. Goal

Turn dat-kit from a dev-only spec-driven toolkit into a general **"AI-usage support tool per type of work"** — without pretending to know professions the owner doesn't. The invariant is a disciplined working loop; "type of work" becomes a plug-in dimension.

## 2. The one big idea in v3: additive-first, refactor-last (or never)

The whole thesis — *one engine, a Domain × Loop model, loop capability gated by gate quality* — is provable with **additive skills only**, zero folder moves:

- New skill `core/domain-builder` (the mechanism).
- New domain pack `knowledge-work` (the proof it works outside dev).
- A thin `software-dev` pack that **points at the existing `skills/build-loop/`** instead of relocating it.

The v2 plan's structural phases (extracting a shared spine, moving build-loop into `domains/`, folding fable-mode+fable-pro) are the **riskiest, lowest-value** work: they break `validate.py` (which hardcodes `skills/build-loop/SKILL.md` as the reviewer-table source of truth and globs `skills/*/SKILL.md`), put the only dogfooded asset in the blast radius, and deliver **no new user capability**. In v3 they are cut from the critical path and deferred indefinitely — done only *after* the pivot has proven itself, if ever.

## 3. The model (unchanged — this is the part both reviews said to keep)

**One engine, two orthogonal axes.**

- **Domain axis** — *what kind of work*. Declared by a Domain Pack.
- **Loop axis** — *how it's triggered and ended*. Anthropic's 4 loops.

**Capability ladder — loop capability is earned by gate quality:**

| Loop | Trigger | Ends when | Prerequisite | v3 status |
|---|---|---|---|---|
| Turn | user | self-check + user approves | none | **build now** |
| Goal | user | gate green + reviewer pass | gate is measurable **AND** validated | **build now** |
| Time | schedule | gate green each run | automated gate + recurring task | **defer** |
| Proactive | event | until turned off | stable Goal+Time + low risk, else notify-only | **defer** |

A domain unlocks a loop **only** to the degree its gate is measurable *and validated* (§5). High-risk fields (legal/medical/finance) are additionally capped at notify-only for Proactive — but the real danger is an *unnamed* risky field, handled by the validity rule and the honesty scope in §6.

## 4. Domain Pack contract (revised — gates are a list, not a slot)

Every "type of work" plugs into the engine by declaring:

| Slot | File | Meaning |
|---|---|---|
| Ground-truth | `ground-truth.md` | Real sources to check before acting (codebase; ledger; statute; brand assets) |
| Gates | `gates.md` | **One or more** measurable + validated done-criteria, each tagged with the loop ceiling it unlocks. (v2 had a single gate; that under-specifies real domains — `software-dev` already has distinct criteria: build-loop's qa-agent gate vs diagnosing-bugs' repro-test.) |
| Reviewer(s) | `reviewers.md` | Independent checker agent(s) for this domain |
| Deliverables | `deliverables/` | Output templates (code/PR; report; contract; deck) |
| Loop profile | `loop-profile.md` | **Advisory** table: per canonical task, which loop fits + why. Docs only in v3, drives nothing |

## 5. Gate-validity mechanism (the safety core, from review v1/v2 — kept, sharpened)

A *measurable* gate is not a *correct* one. `domain-builder` requires, for every gate:

1. **2–3 real worked cases** where the gate correctly passed and correctly failed.
2. An adversarial **"this gate can be gamed by X"** line.
3. **Practitioner sign-off.**

Interview-authored domains are **capped at Turn/Goal** — an interview alone never unlocks Time/Proactive. A gate that can only be closed by human judgement is a **Turn/Goal, human-run** gate; it never authorizes automation.

## 6. Honesty scope (new in v3 — closes the circular-validation hole)

Both reviews flagged the real unresolved risk: the owner has only vague knowledge of non-dev fields, yet the two domains he'll validate (`software-dev`, `knowledge-work`) are ones he personally practices. The mechanism could pass its own tests and still be useless for an unfamiliar field. v3 resolves this by **stating the boundary instead of hiding it**:

> dat-kit safely supports only domains that **the author, or a supplying practitioner, actually practices**. `domain-builder` assists a real practitioner in encoding *their own* discipline; it does **not** let anyone author a domain they cannot personally judge. This limit is written into `fable-core`'s disclaimers alongside the existing "not your lawyer/doctor/financial advisor" text.

Optional stretch (not required for v3): recruit **one** outside practitioner to run the Phase-B interview once, as the only true test of the mechanism against an unfamiliar field. If that never happens, the honesty scope above is the standing answer.

## 7. Phased delivery — additive, each phase ships green, stays on 1.x until proven

Follow the repo's release discipline: `validate.py` green + version bump in both manifests per phase. **No folder moves anywhere in Phase A–C.**

**Phase 0 — Paper validity check (no code). — do first, today.**
Write `knowledge-work`'s `gates.md` on paper (e.g. gate: "every claim carries a citation to a primary source") and run §5 against it: worked cases + the gaming line ("cite a plausible-but-unsupporting source") + would it need a human to close? If the owner *cannot* produce a valid, non-gameable gate for the one non-dev domain he actually practices, **the pivot premise is in doubt — stop here.** Cost: one markdown file. This is the cheapest possible test of the whole thesis.

**Phase A — Model as docs + advisory metadata (v1.8.0). Additive.**
Write this plan into `spec/`, add `docs/loops.md` (two axes + ladder), and add an **advisory** `loop-profile.md` to the *existing* `skills/build-loop/` (which already is turn-based-with-a-goal-evaluator via qa-agent). No moves, no CI risk.

**Phase B — `domain-builder` skill (v1.9.0). Additive.**
Generalize the ideas in `guardian-builder` into a **new** skill `skills/domain-builder/` (guardian-builder stays untouched). It runs the interview, fills the 5-slot contract, and enforces §5's validity gate + the Turn/Goal cap. Optionally run the one outside-practitioner test here.

**Phase C — `knowledge-work` domain as an additive pack (v1.10.0). Additive.**
Author `skills/knowledge-work/` (a new skill dir under the existing flat `skills/*`, so `validate.py`'s glob still matches) carrying the 5-slot contract; `software-dev` is a thin pack that **references `skills/build-loop/` by path**, not a relocation. Dogfood: use domain-builder to (re)author knowledge-work and confirm the gate from Phase 0 survives. **This proves the entire thesis with zero structural risk.**

**Phase D — Single `2.0.0` cutover, only if C paid off. Structural, deferred.**
*Only now*, if Phases 0–C proved value, do the cosmetic restructure v2 front-loaded: introduce `skills/core/` + `domains/`, extract `core/loop-def.md`, fold fable-mode+fable-pro into `fable-core` (copying the per-profession table + disclaimers **verbatim**), relocate build-loop/diagnosing-bugs/git-worktrees/improve-architecture under `domains/software-dev/`. Rewrite `validate.py` skill-discovery + agent-gate + the eval cases in one pass. This is the one-way door — it happens last, behind an explicit go/no-go.

**(Deferred) Phase E — `runners/` (Time + Proactive).** Only after ≥1 domain has a dogfooded, validated *automated* gate. Time via `create_scheduled_task`; Proactive event-triggered, notify-only default. Out of v3 scope.

## 8. Kill switch / abort criteria (new in v3)

- **After Phase 0:** no valid non-gameable `knowledge-work` gate → the "any type of work" premise fails. Fallback: ship `domain-builder` as a standalone additive skill for practitioners to encode their *own* discipline, and drop the "general tool" framing. dat-kit stays a dev tool that *also* helps others self-encode.
- **Before Phase D:** if the additive domains haven't demonstrably helped a real non-dev task, **do not do the structural refactor.** Everything through Phase C is additive and revertible; Phase D is the only one-way door and is explicitly gated.
- **Version discipline:** stay on **1.x** for all additive phases. Burn `2.0.0` only at the Phase-D cutover, i.e. only on proven value — never on a beta refactor.

## 9. Risks & mitigations

| # | Risk | Mitigation |
|---|---|---|
| R1 | Circular validation — mechanism only tested on domains the owner already knows | §6 honesty scope makes the limit explicit; optional one outside-practitioner test in Phase B |
| R2 | Structural moves break `validate.py` (hardcoded build-loop path, flat skill glob), agent-gate, eval harness | All of Phase 0–C is additive under `skills/*`; the CI rewrite is concentrated in the single, explicitly-gated Phase D |
| R3 | Splitting/moving build-loop regresses the only dogfooded asset | build-loop is never moved before Phase D; `software-dev` pack *points at* it by path |
| R4 | Folding fable-pro drops its professional disclaimers | Phase D copies the per-profession table + disclaimers verbatim into fable-core |
| R5 | Over-engineering / premature runtime | `runners/` deferred; loop-profile advisory; Phase D optional and last |
| R6 | Diluting the dev product that works today | Additive phases leave the v1.7.0 dev experience untouched; the pivot is opt-in until Phase D |
| R7 | `knowledge-work`'s "every claim cited" gate is gameable | Correctly unlocks only Goal (human/reviewer-run), never automation — surfaced in Phase 0 |

## 10. What both reviews said to keep

The capability ladder — **Turn as no-prereq default, Goal needs a measurable+validated gate, Proactive capped to notify-only** — is the spine of the pivot and a faithful, enforceable operationalization of Anthropic's own caveats. Everything else is negotiable; this is not.

## 11. Definition of done

**Minimum viable pivot (end of Phase C, ~v1.10.0), all additive:**
- `domain-builder` skill enforcing gate-validity + Turn/Goal cap.
- `knowledge-work` domain pack, dogfooded, with a validated gate that survived the Phase-0 paper test.
- `software-dev` thin pack referencing the untouched `skills/build-loop/`.
- v1.7.0 dev experience unchanged; `validate.py` green; a fresh session loads cleanly.

**Full cutover (v2.0.0, Phase D) — only if the minimum viable pivot demonstrably helped a real non-dev task.**
