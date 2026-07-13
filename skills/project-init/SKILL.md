---
name: project-init
description: >-
  Scaffold a spec-driven project the dat-kit way — CLAUDE.md assembled from a stack
  profile, a spec/ skeleton (00-vision through 08-decisions), working rules, and a
  lessons-learned file. Invoke when the user wants to start a new project ("init a
  project", "scaffold my-app", "set up a new repo the dat-kit way") or adopt the
  structure in an existing repo ("adopt dat-kit here", "add a spec structure to this
  project"). Greenfield creates a fresh directory; brownfield (--here) only adds
  missing files and never overwrites. After scaffolding, guide the user to fill the
  spec and hand off to the build-loop skill.
---

# project-init — scaffold a spec-driven project

## 1. Gather inputs (ask only what's missing)

- **Project name** (directory-safe).
- **One-line description** — what it is, for whom.
- **Stack profile** — list what exists in `${CLAUDE_PLUGIN_ROOT}/templates/profiles/` and let the user pick; default `laravel-react`. If their stack has no profile yet, say so plainly: scaffold with `common/` only and tell them the architecture section of CLAUDE.md must be written by hand (offer to draft it from their description — but mark it unproven, unlike a battle-tested profile).
- **Greenfield or brownfield** — new directory, or `--here` into the current repo.

## 2. Run the scaffold

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/init.sh" <name> --profile <profile> --desc "<one-liner>"
# or, inside an existing repo:
bash "${CLAUDE_PLUGIN_ROOT}/scripts/init.sh" --here --profile <profile>
```

Brownfield guarantees: existing files are never overwritten — the script prints `skip (exists)` per conflict. If `CLAUDE.md` already exists, the profile sections are NOT merged automatically; read the profile files and propose a manual merge as a diff for approval.

If the script cannot run (no bash, permissions), do the same work manually from `${CLAUDE_PLUGIN_ROOT}/templates/`: copy `common/spec/`, `common/lessons-learned/`, `common/rules/`, `common/CONTEXT.md`, then assemble `CLAUDE.md` from `CLAUDE.md.tpl` by replacing `{{PROJECT_NAME}}`, `{{PROJECT_DESC}}`, `{{PROFILE_NAME}}` and splicing the profile's `architecture.md`, `gates.md`, `traps.md` into the three `{{PROFILE_*}}` markers.

## 3. After scaffolding — the part that actually matters

An empty spec skeleton has zero value until filled. Walk the user through it in this order, one file at a time, drafting content from their answers:

1. `spec/00-vision.md` — what, for whom, success, non-goals (non-goals are the highest-value 5 minutes of the whole setup).
2. `spec/01-features.md` — feature list with P0/P1/P2.
3. `spec/02-architecture.md` + `03-db-schema.md` — topology and data. Probe real constraints; don't let placeholders survive.
4. `spec/04-build-phases.md` — slice P0 features into phases with Scope + Demo each.
5. Skim `05`–`07` — fill what's known, leave honest TODOs for what isn't.
6. `CONTEXT.md` — seed the glossary with 3–5 domain terms that came up while filling the spec (one line each). It grows during build phases; it must not start empty of the terms you already used.

Adjust the gate commands in `CLAUDE.md` to the project's real service names before the first build phase.

## 4. Suggest companion tools (detect, don't install)

dat-kit is a methodology, not a package manager — it never installs anything for the user. But two optional, independent, local-first tools pair well with the build loop, and a fresh repo is the natural moment to point them out. **Detect, then suggest the exact command — never run a privileged install yourself.**

- **CodeGraph** (semantic code index → far fewer tool calls when exploring a repo). Two checks:
  - `command -v codegraph` missing → suggest it once with the one-time, per-machine install command (`npm install -g @colbymchenry/codegraph`; note a user npm prefix or `sudo` may be needed if the global dir isn't writable), then stop.
  - CLI present but the repo has no `.codegraph/` → suggest `codegraph init -i` to index this project.
  - Always remind: add `.codegraph/` to the user's global gitignore (`~/.gitignore_global`), never the repo's tracked `.gitignore`.
- **Headroom** (local context compression → fewer tokens). Optional. If `command -v headroom` is missing, mention it once with `pip install "headroom-ai[all]"` and stop. Its failure-mining (`headroom learn`) only pays off once the repo has real session history, so don't push it on a fresh repo.
- **caveman** (output compression → ~65% fewer *output* tokens, MIT). Optional. Orthogonal to dat-kit: dat-kit governs how the agent *works*, caveman governs how it *talks*. If the user wants the full ecosystem (multi-level incl. `wenyan`, `/caveman-commit`, `/caveman-review`, lifetime-savings badge), mention the installer once (`curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash`) and stop. **First point them at dat-kit's own `terse-mode` skill** — zero dependency, no second SessionStart hook, no statusline contention, and it already carves out evidence/gates/approval stops. Only suggest caveman if they want more than terse-mode gives. Whichever they pick, run one, not both.
- **cavemem** (cross-agent memory, sibling of caveman). Optional and also orthogonal; mention only if the user raises cross-session memory. **Do NOT suggest `cavekit`** — it is a competing spec-driven build loop that overlaps dat-kit's own build-loop; pulling it in creates two rival disciplines in one repo.

Rules: suggest each tool at most once per repo; if the user declines, or the tool is already set up, say nothing further. Never run `npm` / `pip` / `sudo` on the user's behalf — print the command and let them decide. These are independent projects with their own release cycles; dat-kit only points at them, it does not wrap or version them.

## 5. Hand off

Tell the user: run the **build-loop** skill for phase 0 (or "autopilot from phase 0" — PREFLIGHT will batch every open decision into one questionnaire, recorded in `spec/08-decisions.md`). The scaffold is done when `claude` opened in the project reads CLAUDE.md and can recite the rules on "verify rules".

