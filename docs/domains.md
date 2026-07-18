# Domain registry

The domains dat-kit currently supports. A **Domain Pack** teaches the working loop what one *type of work* means, via the six-slot contract (workflow · ground-truth · gates · reviewers · deliverables · loop-profile — `docs/contracts/domain-pack.md`). New packs are authored with `domain-builder` — and only for a field the author or a supplying practitioner actually practices (`docs/loops.md` scope boundary).

| Domain | Pack location | Loop ceiling | Notes |
|---|---|---|---|
| **software-dev** | `domains/software-dev/` (six slots; generated trigger at `skills/build-loop/SKILL.md`) | Goal | The flagship. The `build-loop` trigger loads this pack + the work-loop engine; its reviewer chain (`qa-agent` → `code-reviewer` → `security-reviewer`) is the gate. |
| **knowledge-work** | `skills/knowledge-work/` | Goal (human-run) | First non-dev pack: research, writing, analysis. Load-bearing gate G2 (source–claim fidelity) is human-run, so no automation. |

## How a domain plugs in

Each pack declares the six slots; the working loop reads them at the relevant phase (ground-truth before acting, gates + reviewers at verify). The loop itself is domain-neutral — the pack supplies the specifics.

`software-dev` cut over to the registry-backed six-slot layout in Phase 4c: the pack lives at `domains/software-dev/`, the `build-loop` trigger is generated from `registry/domains.json` (byte-checked by `render.py --check`), and the engine mechanics live in `engine/work-loop/ENGINE.md`. `knowledge-work` still uses the v1.17 compatibility layout inside `skills/knowledge-work/` until its Phase 4d cutover. [ADR 0001](decisions/0001-open-platform.md) reverses the 2026-07-14 layout freeze and authorizes this staged cutover after its conformance gates pass.

## Adding a domain

Run `domain-builder` with a practitioner of that field. It fills the contract, runs the gate-validity check (worked cases + gaming line + sign-off), and sets the loop ceiling from gate quality. Interview-authored domains are capped at Turn/Goal until a human validates the automatable gates on real cases.
