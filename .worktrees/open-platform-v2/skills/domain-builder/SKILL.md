---
name: domain-builder
description: >-
  Interview a real practitioner and encode THEIR working discipline as a dat-kit
  Domain Pack — the way build-loop encodes software-dev. Invoke when the user says
  "add a domain", "create a domain pack", "make dat-kit work for <profession>",
  "encode my workflow", "build a work-type", or wants dat-kit to support a field
  beyond coding (accounting, law, design, research, ops, teaching, etc.). Produces
  the five-slot contract (ground-truth, gates, reviewers, deliverables, loop-profile)
  and enforces the gate-validity check: every gate needs real worked cases, a stated
  way it can be gamed, and practitioner sign-off. Interview-authored domains are
  capped at Turn/Goal — an interview alone NEVER unlocks Time or Proactive automation.
  Only encodes domains the interviewee actually practices; it does not let anyone
  author a field they cannot personally judge.
---

# domain-builder — encode a practitioner's discipline as a Domain Pack

A **Domain Pack** teaches dat-kit's working loop what one *type of work* means: what to ground yourself in, what "done" is, who checks it, what the deliverable looks like, and which loops are safe. This skill builds one **by interviewing someone who actually does that work.** You are a scribe with a quality bar, not the expert — never invent how a field works; extract it, then pressure-test it.

## Hard rule — who may author a domain

Only encode a domain the interviewee **genuinely practices**. If the user wants a field neither they nor a supplying practitioner works in, stop and say so: dat-kit does not let anyone author a domain they cannot personally judge (see `docs/loops.md` scope boundary). A plausible-looking pack for a field no one in the room understands is worse than none.

## The five-slot contract

Every Domain Pack declares:

| Slot | File | What it captures |
|---|---|---|
| Ground-truth | `ground-truth.md` | The real sources to check before acting — primary over summary, current over remembered |
| Gates | `gates.md` | One or more measurable **and validated** done-criteria, each tagged with the loop ceiling it unlocks |
| Reviewer(s) | `reviewers.md` | Who/what independently checks the work — an agent charter, never the builder grading itself |
| Deliverables | `deliverables/` | Templates for the outputs of this work |
| Loop profile | `loop-profile.md` | Advisory: per canonical task, which loop fits and why (see `docs/loops.md`) |

A pack's own SKILL.md must state **"Contract files live beside this one."** — `validate.py` keys on that sentence to enforce that every declared slot file actually exists beside it.

## Process

### 1. Learn the practitioner and the work (short interview)

Ask only what changes the pack. Two or three natural rounds, not an interrogation:

- **What is the work, and what does a finished deliverable look like?** (report, ledger, brief, mockup, lesson plan, dataset)
- **What do you check *before* you start — and what happens if you skip it?** → this is ground-truth. Push for the actual source ("the signed contract," "the general ledger"), not "my notes."
- **What must be in hand before you start — and when a piece is missing, do you ask, assume, or stop?** → required inputs and the missing-info policy; record both in the pack.
- **How do you know a piece of work is done and correct?** → candidate gates. Chase concreteness: "looks right" is not a gate; "every figure ties back to the source statement" is.
- **What error costs the most here, and who pays?** (money, legal exposure, safety, reputation) → sets default effort and risk caps.
- **Who reviews it in real life, and what do they look for?** → reviewer charter.
- **Show me one real input→output pair — including one that went wrong.** → seeds the gates' worked cases and the deliverable template with reality, not theory.

### 2. Draft the gates — then run the validity check on EACH

A measurable gate is not a correct one. For every gate, the practitioner must supply, and you must record in `gates.md`:

1. **2–3 real worked cases** — a case it should PASS and a case it should FAIL, from real work.
2. **The gaming line** — "this gate can be gamed by X" (e.g. "cite a source that mentions the topic but doesn't state the claim"). Every gate has one; if the practitioner can't name it, you find it.
3. **Human-needed?** — can this gate be closed mechanically, or does it need a person's judgement to close honestly?
4. **Sign-off** — the practitioner confirms the cases and gaming line are real.

A gate that fails to produce worked cases or a gaming line is not ready — mark it draft, don't ship it.

### 3. Set the loop ceiling (the capability ladder)

From the validity results, tag the whole domain:

- Any gate that needs a **human to close** → that gate is **Turn/Goal, human-run**.
- A domain is **capped at Turn/Goal** whenever it was authored by interview — Time/Proactive stay locked until a human has run the automatable gates on real cases and confirmed they hold.
- High-risk fields (legal, medical, finance, anything irreversible or safety-relevant) → Proactive, if ever unlocked, is **notify-only**.

Record the ceiling and the reasoning at the top of `loop-profile.md`. A domain that lands at "Goal, human-run" is a **correct** outcome, not a shortfall — the ladder is doing its job by refusing to automate what can't be safely automated.

### 4. Write the pack

Create `skills/<domain>/` with the five files. Keep each concrete and short — a pack is a working checklist, not documentation. `gates.md` must show, per gate: the criterion, its worked cases, its gaming line, human-needed flag, and unlocked ceiling. Cite the practitioner's real examples throughout; invent nothing.

### 5. Confirm and hand over

Present the pack as numbered findings — each gate with its evidence and ceiling. One confirmation round. Then tell the user: the domain runs through dat-kit's working loop at its ceiling; to raise the ceiling later, a human must validate the automatable gates on real cases (that is the entry condition for the deferred Time/Proactive `runners/`).

## Rules for every pack you generate

- Every gate must be checkable and carry its worked cases + gaming line — no exceptions, no "be thorough."
- Prefer stating *why* a gate exists over a bare rule — future sessions follow understood gates better.
- Never let an interview alone unlock automation. Never encode a field no one present practices.
- If the practitioner cannot produce a single valid, non-gameable gate, say the premise fails for that domain and stop — do not ship a decorative pack.
