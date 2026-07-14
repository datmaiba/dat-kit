# Domain registry

The domains dat-kit currently supports. A **Domain Pack** teaches the working loop what one *type of work* means, via the five-slot contract (ground-truth · gates · reviewers · deliverables · loop-profile). New packs are authored with `domain-builder` — and only for a field the author or a supplying practitioner actually practices (`docs/loops.md` scope boundary).

| Domain | Pack location | Loop ceiling | Notes |
|---|---|---|---|
| **software-dev** | `skills/build-loop/` (+ `skills/build-loop/loop-profile.md`) | Goal | The flagship. `build-loop` *is* this domain's loop; its reviewer chain (`qa-agent` → `code-reviewer` → `security-reviewer`) is the gate. Not relocated — referenced in place. |
| **knowledge-work** | `skills/knowledge-work/` | Goal (human-run) | First non-dev pack: research, writing, analysis. Load-bearing gate G2 (source–claim fidelity) is human-run, so no automation. |

## How a domain plugs in

Each pack declares the five slots; the working loop reads them at the relevant phase (ground-truth before acting, gates + reviewers at verify). The loop itself is domain-neutral — the pack supplies the specifics.

`software-dev` predates the contract, so its slots are expressed inside `build-loop` rather than as separate files: ground-truth = the spec + codebase, gates = the reviewer verdicts, reviewers = the three subagents, deliverables = code/PR, loop-profile = `skills/build-loop/loop-profile.md`. It is listed here by **reference**, deliberately not moved — moving it would break `scripts/validate.py` (which treats `skills/build-loop/SKILL.md` as the single source of truth for the reviewer table) for zero user benefit. This layout is **permanent**: the structural cutover once sketched in `PLAN-general-work-loop-v2.md` was cancelled (plan v5, 2026-07-14) — domains-by-reference under flat `skills/*` is the final shape.

## Adding a domain

Run `domain-builder` with a practitioner of that field. It fills the contract, runs the gate-validity check (worked cases + gaming line + sign-off), and sets the loop ceiling from gate quality. Interview-authored domains are capped at Turn/Goal until a human validates the automatable gates on real cases.
