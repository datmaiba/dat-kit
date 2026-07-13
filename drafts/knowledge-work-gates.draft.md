# Phase 0 — `knowledge-work` gates.md (DRAFT) + paper validity check

> Purpose: the cheapest possible test of the pivot premise. If the owner (a dev who does research/writing daily) can articulate valid, non-gameable done-criteria for the one non-dev domain he actually practices, the "any type of work" thesis survives. If not, stop. Cost: this one file, no code.
> Domain: **knowledge-work** — research, writing, analysis, synthesis, documentation.
> Ground-truth for this domain: primary/authoritative sources, the actual brief, the real prior document — never memory or a summary.

---

## Part 1 — The gates (candidate done-criteria)

Each gate is tagged with the **loop ceiling** it can unlock (per the capability ladder: a gate only a human can close is Turn/Goal, never automation).

### G1 — Citation presence
Every non-trivial factual claim carries an inline citation to a locatable source.
- **Measurable?** Yes, structurally (claim without a citation marker = fail).
- **Ceiling:** Goal (a reviewer/linter can flag uncited claims).

### G2 — Source–claim fidelity
Each cited source actually *supports* the specific claim it's attached to.
- **Measurable?** Only semantically — requires reading the source and judging support.
- **Ceiling:** Goal, **human/reviewer-run**. Not automatable.

### G3 — Source reliability
Sources are primary or authoritative for the claim type; not circular, not content-farm, not the deliverable citing itself.
- **Measurable?** Partly (domain allow/deny lists) but the judgement call is human.
- **Ceiling:** Goal, human-run.

### G4 — Currency
Every time-sensitive fact (prices, office-holders, statistics, "latest X") is verified current, with a source date inside an agreed window.
- **Measurable?** Yes — source date present and within window is checkable.
- **Ceiling:** Goal now; **candidate for Time-based later** (a scheduled re-check of a living document), but only after G2/G3 are trusted.

### G5 — Brief coverage
The deliverable answers every item in the agreed brief/outline; nothing silently dropped.
- **Measurable?** Yes, against a checklist of brief items.
- **Ceiling:** Goal.

### G6 — Internal consistency
No two claims contradict; every number reconciles with the figure it's derived from.
- **Measurable?** Numbers: yes (recompute). Prose contradictions: semantic, human-run.
- **Ceiling:** Goal.

---

## Part 2 — Validity check (the §5 mechanism, applied)

For each gate: worked cases where it correctly passes/fails, the adversarial "gamed by X" line, and whether a human must close it.

### G1 — Citation presence
- **Pass case:** "VAT in Vietnam is 10% [Circular 219/2013/TT-BTC]." → marker present → pass.
- **Fail case:** "Most startups fail in year one." No citation → fail.
- **Gamed by X:** attach a citation marker that points nowhere, or to an unrelated source — G1 passes on *presence* alone. → G1 is necessary but weak; it must always run *with* G2.
- **Human needed?** No — automatable. But worthless alone.

### G2 — Source–claim fidelity
- **Pass case:** claim "the standard VAT rate is 10%" cited to the circular's article that states 10% → source read, supports → pass.
- **Fail case:** same claim cited to an article about *filing deadlines* → source doesn't support → fail.
- **Gamed by X:** cite a long, plausible-looking source that *mentions the topic* but doesn't actually state the claim, betting the reviewer won't read it fully. → defeated only by a reviewer who actually reads the cited passage.
- **Human needed?** **Yes.** This is the gate that carries the domain's real quality, and it cannot be automated. → Goal ceiling, human/reviewer-run.

### G3 — Source reliability
- **Pass case:** tax rate cited to the government circular (primary).
- **Fail case:** tax rate cited to a random blog quoting an unnamed "expert."
- **Gamed by X:** cite a source that merely *looks* authoritative (official-sounding name, outdated gov mirror) → passes a shallow check.
- **Human needed?** Mostly yes. Partial automation via allow/deny lists. → Goal, human-run.

### G4 — Currency
- **Pass case:** "As of 2026, the rate is X [source dated 2026]." within window → pass.
- **Fail case:** a 2019 price presented as current → out of window → fail.
- **Gamed by X:** cite a recent source that *restates* an old figure without re-verifying → date is fresh, fact is stale. Defeated only by checking whether the source itself re-verified.
- **Human needed?** Date-in-window: automatable. Stale-restatement: human. → Goal now; Time-based candidate later.

### G5 — Brief coverage
- **Pass case:** brief asked for 3 competitors; all 3 covered → pass.
- **Fail case:** only 2 of 3 covered → fail.
- **Gamed by X:** add a one-line stub for the missing item to tick the box without real coverage. → defeated only by a depth check (human).
- **Human needed?** Presence: automatable. Adequacy: human. → Goal.

### G6 — Internal consistency
- **Pass case:** total in summary equals sum of the parts in the table → pass.
- **Fail case:** intro says "revenue grew," body shows a decline → fail.
- **Gamed by X:** hard to game numerically (recompute catches it); prose contradictions can hide across long documents. → human for prose.
- **Human needed?** Numbers no; prose yes. → Goal.

---

## Part 3 — Verdict

**The pivot premise HOLDS for knowledge-work. Proceed.**

- The owner *can* articulate valid, non-gameable done-criteria for a non-dev domain he practices — six of them, each with real pass/fail cases and a named way it can be gamed. That is exactly what `domain-builder` should be able to elicit from any practitioner.
- The gates split cleanly into **structural (automatable): G1, G4-date, G5-presence, G6-numbers** and **semantic (human/reviewer-run): G2, G3, G4-stale, G5-adequacy, G6-prose**. G2 (source–claim fidelity) is the load-bearing quality gate and is inherently human — exactly the kind of gate the ladder is designed to *cap at Goal*.
- **Loop ceiling for knowledge-work: Goal.** No gate here safely unlocks Time/Proactive automation yet, because the gate that actually protects quality (G2) needs a human/reviewer to close. This is the *correct* outcome — it confirms the capability ladder does its job (it refuses to automate what can't be safely automated), rather than a failure.
- **What this proves about the thesis:** the mechanism produces a truthful, useful result — a usable Goal-level domain plus an honest "no automation" verdict. That is the whole point.

**One caveat, logged honestly (plan §6):** this test was run by the owner on a domain he practices. It shows the mechanism *works when the practitioner genuinely knows the field*. It does **not** prove it's safe for a field the owner can't judge — that still relies on §6's honesty scope (only a real practitioner authors their domain) and the optional one-outside-practitioner test in Phase B.

## Part 4 — Next step

Phase 0 passed → green-light **Phase A** (docs + advisory `loop-profile.md` on the existing build-loop, all additive). This draft becomes the seed of `skills/knowledge-work/gates.md` when Phase C authors the pack.
