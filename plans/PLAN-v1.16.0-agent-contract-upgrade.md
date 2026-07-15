# dat-kit v1.16.0 — Agent Contract Fix and Upgrade Plan

**Status:** awaiting implementation approval
**Base:** `v1.15.0` + Phase 0 baseline commit of the current dirty worktree
**Provisional target:** `v1.16.0`
**Plan revision:** v2
**Review history:**

1. Original plan (Codex) — plan review `APPROVE WITH CHANGES`, changes incorporated.
2. Ground-truth audit against the live worktree — Phase 0 and done-in-baseline
   annotations added; auto-migration cut; evidence discriminator specified.
3. Independent plan-reviewer, criterion *multi-runtime portability* —
   `APPROVE WITH CHANGES`: runtime pointer registry, manual-fallback preflight,
   skill-less degradation path, `cursor` in the runtime enum, baseline hygiene.
   All incorporated below.

## Outcome

Eliminate competing instruction sources across Claude Code, Codex, Cursor, and
any future agent runtime. For each dat-kit project, root `AGENTS.md` is the
sole canonical entrypoint — aligned with the emerging cross-tool `AGENTS.md`
convention (Codex and current Cursor read it natively; pointer files are
compatibility for older runtimes) — and routes to:

- `docs/agent-working-rules.md` for project policy, architecture, gates, and traps.
- `docs/agent-workflow.md` for shared execution, preflight, handoff, and adapter rules.

`CLAUDE.md`, `.claude/CLAUDE.md`, and `.cursorrules` remain compatibility
pointers only. Runtime hooks, config, MCP, statuslines, and companion tools are
optional adapters and must not contain shared policy or activate machine-local
routing implicitly. **Portability invariant:** supporting a new runtime must be
a pointer-only operation — one registry entry plus at most one pointer
template, with no other edits (Phase 3).

## Constraints

- Preserve every existing user change in the dirty worktree (Phase 0 commits it).
- Do not overwrite arbitrary brownfield guidance.
- Brownfield conflict detection must occur before any filesystem mutation —
  on every scaffold path, including the manual no-bash fallback.
- Committed scorecard history remains append-only.
- Ignored local settings are reported, not silently edited.
- Release actions require explicit approval after all gates and reviews pass.
- Greenfield scaffolding must keep working with bash alone; Python is required
  for brownfield (`--here`) preflight only.

## Per-phase gate

Every phase ends with the same verification command (pytest applies from
Phase 3 onward):

```text
python scripts/validate.py && pytest scripts/tests && shellcheck scripts/init.sh
```

## Phase 0 — Baseline commit (new)

The dirty worktree already implements a large part of the original Phase 1–2.
Freeze it as an auditable baseline before any further change.

### Work

1. Audit the dirty tree; `python scripts/validate.py` is currently green — keep it green.
2. `git rm --cached scripts/__pycache__/statusline.cpython-310.pyc`; add
   `__pycache__/` to `.gitignore`.
3. Finalize the `.codex/hooks.json` deletion in the index (`git rm`), not only
   in the worktree.
4. Add `.gitattributes` with `* text=auto` (the repo normalizes CRLF in the
   checker but not in git itself).
5. Commit from the native Windows side (or with `core.fileMode=false`) — the
   Linux mount churns mode bits (100644→100755) and would pollute the baseline.
6. Commit everything as one baseline commit and record in its message which
   original-plan items it already delivers (see the annotations below).

### Acceptance

- Clean `git status` after the baseline commit; validator green; no tracked
  pycache; `.codex/hooks.json` gone from the index.

## Phase 1 — Canonical contract and dogfooding

**Done in baseline:** `templates/common/AGENTS.md` (canonical, revision-stamped),
the three pointer templates, `templates/common/docs/agent-workflow.md`,
`templates/common/docs/agent-working-rules.md.tpl`, validator checks for
pointer shape/casing/policy-freedom, CI greenfield+brownfield smoke tests.

### Remaining files

- Add root `AGENTS.md` for maintaining dat-kit itself.
- Add root `docs/agent-working-rules.md`.
- Add root `docs/agent-workflow.md`.

### Remaining work

1. Define the dat-kit maintainer contract separately from generated-project
   templates; neither may accidentally stand in for the other (root docs carry
   no placeholders; templates keep theirs).
2. Make root `AGENTS.md` the single maintainer entrypoint.
3. Keep architecture, gates, workflow, migration, and reporting rules in the
   two linked root docs.
4. Synchronize the canonical contract revision with the release version —
   enforced by the Phase 3 checker, not by convention.

### Acceptance

- Every shared maintainer rule is reachable from root `AGENTS.md`.
- No runtime-specific entrypoint contains an override.
- Generated templates retain placeholders while root maintainer docs do not.

## Phase 2 — Policy-free runtime adapters

**Done in baseline:** `.codex/hooks.json` deletion; `hooks.json` neutral-adapter
shape checks in the validator.

### Files

- `templates/session-bootstrap.txt`
- `.codex/config.toml` (remove from version control)
- `.gitignore`
- `docs/codex.md`

### Work

1. Reduce `templates/session-bootstrap.txt` to one neutral responsibility:
   locate and read root `AGENTS.md`. It must not restate plan, build-loop,
   quality-gate, reporting, or skill-routing policy. **Decision (recorded):**
   one fallback line stays — "no `AGENTS.md` found → suggest
   `/dat-kit:project-init`" — a pointer to adoption, not policy.
2. Keep `hooks.json` as a Claude Code adapter that emits that neutral pointer.
3. Remove tracked `.codex/config.toml`; it sets a machine-local
   `ANTHROPIC_BASE_URL` and therefore activates local routing implicitly.
   Add it to `.gitignore`.
4. Do not edit ignored `.claude/settings.local.json`. Document exact manual
   cleanup and verification for its local Headroom hook.
5. Document that adapter failure is benign by design: if the SessionStart hook
   never fires (e.g., no `node` on PATH), the contract still governs because
   policy lives in `AGENTS.md`, not in the adapter.

### Acceptance

- No tracked Codex runtime file contains a local absolute path, proxy URL, or
  unverified hook schema.
- Claude's SessionStart adapter adds no substantive policy.
- Optional Headroom/MCP configuration remains opt-in and machine-local.

## Phase 3 — Reusable contract checker with runtime pointer registry

### Files

- Add `scripts/contract_check.py` using only the Python standard library.
- Refactor `scripts/validate.py` to call it.
- Wire `scripts/init.sh` brownfield preflight to it.
- Add `scripts/tests/` with pytest fixtures; add `pytest` to
  `requirements-dev.txt`; add a pytest step to CI.

### Runtime pointer registry (single source of truth)

The pointer inventory is currently hardcoded independently in `init.sh`,
`validate.py` (two loops), CI (grep asserts), the `AGENTS.md` template prose,
and `project-init/SKILL.md` — adding a runtime today means five unsynchronized
edits. Fix: define the registry once in `contract_check.py`, e.g.

```python
POINTERS = {
    "claude-code": ["CLAUDE.md", ".claude/CLAUDE.md"],
    "cursor": [".cursorrules"],        # legacy; current Cursor reads AGENTS.md
    "codex": [],                        # reads AGENTS.md natively
}
RUNTIMES = ["claude-code", "codex", "cursor", "other"]  # scorecard enum lives here too
```

Validator checks, `init.sh`'s copy list (checker-verified), and CI smoke
asserts all derive from or are verified against this registry. The
`agent_runtime` enum (Phase 5) is defined here and nowhere else; extending it
is a one-line change.

### Checks

1. Inventory all known instruction entrypoints and runtime configs from the registry.
2. Compare each pointer with its own canonical template after normalizing
   CRLF/LF; do not use raw-byte equality across platforms.
3. Resolve pointer targets and check every path segment with exact casing.
4. Reject missing targets, legacy contract files, substantive duplicate policy,
   and policy-bearing runtime adapters.
5. Recognize legacy dat-kit artifacts (`CLAUDE.md.tpl`-era files,
   `rules/working.rules.md`) with a **named diagnostic** pointing at the manual
   migration doc — recognition without transformation.
6. Reject tracked `.codex/hooks.json` and machine-local `.codex/config.toml`.
7. Validate the contract revision against the version-bearing manifests, named
   explicitly: `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
   `.claude-plugin/marketplace.json` (the Codex marketplace file carries no
   version field).
8. Return stable, testable diagnostic identifiers and a non-zero exit status on
   every violation.

### Acceptance

- Validator, brownfield preflight, and CI use the same detection implementation;
  a detection rule cannot change in one surface without changing all three.
- **Registry proof:** adding a new runtime requires exactly one registry entry
  plus at most one pointer template; a CI test demonstrates this and everything
  stays green with no other edits.
- Windows line-ending differences do not produce false failures.

## Phase 4 — Atomic brownfield migration

### Files

- `scripts/init.sh`
- `skills/project-init/SKILL.md`
- Migration documentation in `README.md`, `HUONG_DAN.vi.md`, and `docs/codex.md`.

### Two-pass flow

1. **Read-only preflight:** inspect the complete destination contract and
   runtime configuration before `mkdir`, `cp`, `sed`, `mv`, or `git init`.
2. **Mutation pass:** create missing files only if the preflight proves the
   existing contract is compatible.

### Interpreter policy

- Brownfield (`--here`) requires the preflight and therefore Python: resolve
  `python3` → `python` → `py` (Windows ships `python`/`py`); if none is found,
  **fail closed** with an actionable message.
- Greenfield into an empty directory has no contract to conflict with and must
  keep working with bash alone.

### Manual-fallback hole (closed)

The `project-init/SKILL.md` no-bash fallback currently performs manual copies
with zero conflict detection — precisely the path non-Claude runtimes hit.
Fix: the fallback must run `contract_check.py --target .` (read-only) before
any copy; if Python is also unavailable, the skill instructs the agent to
perform the checker's inventory manually and **stop on any conflict**.

### Fail-closed conflicts

- Substantive legacy policy in `CLAUDE.md`, `.claude/CLAUDE.md`, or `.cursorrules`.
- Wrong, missing, or wrong-cased pointer targets.
- A competing or incompatible existing `AGENTS.md`.
- Policy-bearing runtime adapters.
- A partial canonical installation whose existing files do not match the
  current contract.
- Path traversal, unsafe symlinks, target escape, or unresolvable containment.

On conflict, exit non-zero with an actionable migration report and make no
filesystem changes. **All legacy migration is manual in this release** — the
original plan's deterministic auto-transformation of recognized old templates
is cut (unmaintainable test matrix for a solo repo); the checker's named
legacy diagnostics (Phase 3, check 5) route users to the manual doc instead.

### Acceptance

- CI snapshots the entire hostile brownfield fixture and proves byte-for-byte
  preservation after a rejected run.
- Compatible partial installs receive only missing files.
- Rerunning against a canonical project is idempotent.
- The documented manual fallback performs the same preflight or stops.

## Phase 5 — Evidence schema v2

### Scorecard schema

New records require:

```json
{
  "schema_version": 2,
  "agent_runtime": "codex",
  "workflow": "build-loop",
  "canonical_contract_revision": "dat-kit 1.16.0",
  "git_state": {
    "branch": "master",
    "head": "<commit>",
    "dirty": true
  }
}
```

`agent_runtime` uses the registry enum from `contract_check.py` —
`claude-code | codex | cursor | other` (Cursor is in scope and must be
attributable; `other` is the escape hatch, and extending the enum is a
registry-only change). `workflow` and `canonical_contract_revision` are
non-empty strings; `none` is the explicit value for a project without a
dat-kit contract. Git fields may be `null` only when the working directory is
not a Git repository.

### Old/new discriminator (file-shape rule)

The validator reads file content, not git history, so the boundary must be
visible in the file itself:

- A record with `schema_version >= 2` is validated strictly — every v2 field
  required, no optional-pair rule.
- A record without `schema_version` is legacy v1 and remains valid.
- **No v1 record may appear after the first v2 record in the file.** This makes
  "new records must be v2" mechanically checkable in an append-only file.

### Files

- `skills/scorecard/SKILL.md`
- `skills/handoff/SKILL.md`
- `scripts/scorecard.py`
- `scripts/validate.py` (via `contract_check.py`)
- `benchmarks/scorecard.jsonl`

### Work

1. Implement the discriminator above; delete the current optional-pair rule.
2. Preserve committed v1 historical lines.
3. Supersede the currently uncommitted 2026-07-15 codex record with an explicit
   v2 superseding record in this phase.
4. Add mandatory `## Workflow` to handoff beside Runtime, Canonical contract,
   and Git state.
5. Preserve provider-safe token enrichment behavior.

### Acceptance

- Negative fixtures fail independently for every missing or invalid v2 field,
  and for a v1 record appended after a v2 record.
- A cold reader can identify runtime, workflow, contract revision, branch,
  commit, and dirty state from both scorecard and handoff evidence.

## Phase 6 — Skills, preflight, reviewers, and documentation

### Files

- `skills/build-loop/SKILL.md`
- `skills/project-init/SKILL.md`
- `skills/handoff/SKILL.md`
- `skills/scorecard/SKILL.md`
- `templates/common/docs/agent-workflow.md`
- Relevant reviewer charters in `agents/`
- `README.md`, `HUONG_DAN.vi.md`, `docs/codex.md`
- `benchmarks/skill-evals.jsonl`
- Roadmap and maintenance sections.

### Work

1. Make all workflow instructions AGENTS-first.
2. Have PREFLIGHT inventory contract entrypoints and runtime adapters (via the
   Phase 3 checker) before feature work.
3. Fail PREFLIGHT on duplicate policy, bad pointers, wrong casing, or live
   dependency on an unverified adapter.
4. **Skill-less runtime degradation path:** add a short section to
   `templates/common/docs/agent-workflow.md` — when dat-kit skills are not
   available in the current runtime, execute the loop steps inline (they are
   listed there) and produce the handoff document manually from its section
   list. The contract must be followable by any runtime that can read
   `AGENTS.md`, plugin or no plugin.
5. Document safe brownfield adoption and explicit manual legacy migration.
6. State that unmigrated brownfield repositories can still drift; reserve the
   no-drift claim for successfully validated canonical installations.
7. Document that installed plugins and active sessions retain old metadata
   until update/reinstall and a fresh session.
8. **Skill-evals authoring rule** (recorded in the maintainer `AGENTS.md`):
   whenever a skill description changes, add or update the corresponding
   positive case in `benchmarks/skill-evals.jsonl` — the validator catches
   removed triggers, but only authoring discipline keeps coverage of new ones.

## Phase 7 — CI and red-before-green verification

### Positive cases

- Fresh greenfield scaffold has the exact canonical structure and no unresolved
  placeholders.
- Canonical rerun is idempotent.
- Compatible partial brownfield receives only missing files.
- Scorecard/handoff v2 examples validate.
- **Registry extension test:** a synthetic runtime added via registry entry +
  pointer template passes the full suite with no other edits.

### Negative cases

- Policy added to any pointer.
- Missing, wrong, or wrong-cased pointer target.
- Legacy duplicate contract (named legacy diagnostic asserted).
- Policy-bearing bootstrap/hook.
- Tracked `.codex/hooks.json` or machine-local `.codex/config.toml`.
- Every individually missing/invalid scorecard v2 field.
- A v1 record appended after a v2 record.
- Hostile brownfield policy conflict.
- Path traversal, destination escape, symlink redirection, and containment
  failures.

Each negative fixture must assert the expected diagnostic identifier and
non-zero exit status before the final green run. Recreate or restore isolated
fixtures after each deliberate failure.

### Final gates

```text
python scripts/validate.py
pytest scripts/tests
bash -n scripts/init.sh
shellcheck scripts/init.sh
greenfield and brownfield scaffold smoke tests
git diff --check
```

## Phase 8 — Independent review and release

1. `qa-agent` runs every declared gate and attacks the migration cases.
2. `code-reviewer` audits the full diff against the canonical contract.
3. `security-reviewer` is mandatory because `init.sh` handles paths and writes
   into arbitrary brownfield repositories. Review traversal, symlink/TOCTOU,
   destination containment, and preservation guarantees.
4. Re-run regression QA after every review fix.
5. Immediately before versioning, check local tags and published/remote state:
   - if `1.16.0` is unpublished, finish as `1.16.0`;
   - if `1.16.0` is published, release the fixes as `1.16.1`.
6. Update all version-bearing manifests and release documentation.
7. Commit, push, verify GitHub Actions, update/reinstall dat-kit in Claude Code
   and Codex, and test from fresh sessions only after explicit user approval.

## Definition of done

- One canonical contract exists per validated project scope.
- All compatibility entrypoints are exact, policy-free pointers derived from a
  single runtime registry; **adding a runtime is a pointer-only operation,
  proven in CI**.
- Runtime adapters contain no shared policy or tracked machine-local activation;
  adapter failure is documented as benign.
- Brownfield conflicts fail before mutation and preserve the complete tree —
  on the scripted path and the manual fallback alike.
- Validator, preflight, and CI share one checker and cannot drift independently.
- Scorecard and handoff contain runtime (including `cursor`), workflow,
  contract revision, and Git state; the v1/v2 boundary is mechanically
  enforced.
- A skill-less runtime can follow the full workflow from `AGENTS.md` alone.
- Every negative fixture goes red with the expected diagnostic; the complete
  final suite is green.
- QA, code review, and security review approve.
- Documentation limits the no-drift claim to validated canonical installations.

## Approval gate

This plan is documentation only. Do not implement it until the user explicitly
approves execution.
