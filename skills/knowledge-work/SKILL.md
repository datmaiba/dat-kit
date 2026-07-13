---
name: knowledge-work
description: >-
  The working loop for knowledge work — research, writing, analysis, synthesis,
  and documentation. Invoke when the user wants to write a researched report,
  produce a briefing or memo, do a literature or market review, fact-check a
  document, synthesize sources into an argument, or turn findings into a written
  deliverable. Enforces: ground yourself in primary sources before writing,
  verify every claim against its cited source, and pass the domain's gates
  (citation, source-claim fidelity, source reliability, currency, brief coverage,
  internal consistency) with an independent fact-check before reporting. This
  domain is capped at the Goal loop — its load-bearing quality gate (does the
  source actually support the claim?) needs a human/reviewer to close, so it never
  runs on a schedule or unattended. dat-kit's first non-dev Domain Pack.
---

# knowledge-work — the working loop for research & writing

This is a dat-kit **Domain Pack**: it teaches the working loop what "knowledge work" means. The invariant loop is unchanged — *clarify → decompose → ground-truth → execute → verify → report → harvest* — this pack fills in what each phase means for research and writing. Contract files live beside this one.

## The five-slot contract

| Slot | File | Use it in |
|---|---|---|
| Ground-truth | `ground-truth.md` | phase C — what to read before you write |
| Gates | `gates.md` | phase E — the done-criteria, each with worked cases + how it's gamed |
| Reviewer(s) | `reviewers.md` | phase E — the independent fact-check charter |
| Deliverables | `deliverables/` | phase D — output templates |
| Loop profile | `loop-profile.md` | which loop each task runs at (advisory) |

## Running the loop

**A — Clarify.** Nail the brief before researching: audience, purpose, scope, length, required sources or jurisdiction, deadline. Underspecified research wastes whole runs. State assumptions in one line and proceed.

**B — Decompose.** Any deliverable with 3+ distinct claims or sections gets a visible outline that ends with an explicit **verification step** — the fact-check that deadline pressure deletes first.

**C — Ground truth.** Read `ground-truth.md`. Never write from memory when a source is checkable. Primary over summary, current over remembered, a fresh search for anything time-sensitive.

**D — Execute.** Draft against the outline. Attach a source to every non-trivial factual claim *as you write it*, not afterward — retrofitting citations is how unsupported claims survive. Use the templates in `deliverables/`.

**E — Verify against the gates.** Run every gate in `gates.md`. Then hand the draft to an independent fact-check per `reviewers.md` — you do not grade your own claims. Loop D→E until the gates pass.

**F — Report honestly.** State what was verified and how ("12 claims, all cited; 3 currency-checked against 2026 sources; 1 claim could not be sourced — flagged inline"). Never "fully researched." Surface every claim you could not source rather than hiding it.

**G — Harvest.** A wrong citation caught, a source that looked authoritative but wasn't — each becomes a lessons-learned entry so the next run doesn't repeat it.

## Loop ceiling: Goal (human-run)

See `loop-profile.md`. The gate that carries this domain's real quality — *does the cited source actually support the claim?* — cannot be closed mechanically; it needs a reader. So knowledge-work runs at **Turn** (drafts, brainstorming) or **Goal** (verified deliverables, reviewer-gated) and **never unlocks Time or Proactive automation.** That is the correct outcome of the capability ladder, not a limitation to route around.
