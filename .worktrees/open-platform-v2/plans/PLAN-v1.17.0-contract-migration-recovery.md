# dat-kit v1.17.0 — Contract Migration Recovery Plan

**Status:** Phase 0-5 implemented locally 2026-07-15; release approval pending
**Base:** `v1.16.0` (`7acb595`)
**Target:** `v1.17.0`
**Plan revision:** v2 (independent-review blockers incorporated)
**Incident:** a customized v1.15-era brownfield project is blocked by ten
contract diagnostics after installing v1.16.0.

## Decision

Keep the v1.16 invariant that root `AGENTS.md` is the single canonical
entrypoint. Do not weaken exact static pointers or auto-rewrite user policy.
Instead, make contract evolution independent from package patch releases and
give brownfield projects a deterministic, read-only migration plan that says
which static files require extract-then-replace, which project-owned files
require a semantic merge, and which runtime adapters require manual inspection.

This is a minor release because the read-only migration planner and versioned
JSON schema are new public features. It repairs the v1.16 upgrade path without
introducing a new project-contract layout.

## Evidence and root cause

The incident repro is deterministic:

```powershell
python "<DAT_KIT_ROOT>/scripts/contract_check.py" --target .
```

It exits 1 with:

- one `COMPETING_AGENTS`;
- three `POINTER_MISMATCH` plus three `POINTER_POLICY` diagnostics;
- two `PARTIAL_INSTALL_MISMATCH` diagnostics;
- one `RUNTIME_ADAPTER_CONFLICT`.

Minimal probes also prove that v1.16.0:

1. labels a semantically pointer-only file as `POINTER_POLICY` when its prose
   contains `MUST`;
2. labels any project extension to `docs/agent-workflow.md` as a generic partial
   install mismatch;
3. recognizes `docs/agent-working-rules.md` only through one exact English
   sentence;
4. reports any `.codex/hooks.json` as the same runtime conflict without saying
   whether it is tracked, policy-bearing, machine-local, or merely unknown.

The primary defect is not fail-closed behavior. The defect is that one checker
currently conflates four states:

- a genuinely competing contract;
- a previous dat-kit contract revision requiring migration;
- a safe static-file replacement;
- a user-policy/runtime file requiring manual judgment.

There is a second release-design defect: `CONTRACT_REVISION` is also used as the
expected package manifest version. A v1.16.1 package cannot ship without making
every v1.16.0 project appear stale, even when the project-contract schema is
unchanged.

## Invariants

- All target inspection remains read-only and stdlib-only.
- Brownfield mutation stays fail-closed; `init.sh --here` must not write when an
  unresolved diagnostic exists.
- No tool may move, rewrite, or delete project policy automatically.
- Static compatibility pointers remain exact shipped templates after migration.
- Project-specific policy remains in `AGENTS.md` or linked project-owned docs;
  runtime adapters remain policy-free.
- Existing CLI consumers of `contract_check.py --target <path>` keep working.
- Diagnostic identifiers and machine-readable output are treated as public
  contracts and covered by tests.
- Existing Python consumers of `Report.items` keep the current `(code, message)`
  tuple view throughout v1.x.
- Existing default text diagnostics keep their current codes and one-line
  cardinality. New classifications and grouping are additive in JSON and
  migration-plan output, never silent replacements for legacy codes. Unsafe
  paths are the sole exception: inspection stops at the first unsafe diagnostic
  instead of preserving accidental downstream reads/findings.

## Scope

### In scope

- Contract/package revision separation.
- Typed diagnostics with actionable remediation metadata.
- A read-only migration-plan output mode.
- Better classification of pointer, canonical-layout, static-template, working-
  rules, and runtime-adapter drift.
- Regression fixtures derived from the real incident.
- Documentation and skill routing for manual migration.

### Out of scope

- Editing the affected application repository.
- Automatic policy extraction, merging, replacement, or deletion.
- Changing the canonical v1.16 file layout.
- Supporting arbitrary third-party instruction formats.
- Replacing `init.sh` with a new installer.
- Releasing or pushing without a separate explicit approval.

## Self-Q&A

1. **Should strict pointer equality or the legacy `POINTER_POLICY` diagnostic be
   removed now?** No. Exact static pointers prevent runtime drift, and removing a
   published code would break v1 consumers. Mark `POINTER_POLICY` as a legacy
   compatibility signal: keyword-only evidence cannot drive classification or
   remediation. The migration planner uses the conservative static-file rule
   below; diagnostic removal is deferred to the next major version.
2. **Should customized `agent-workflow.md` become valid?** No for v1.17.0. It is
   intentionally shared/static. The migration plan must explicitly instruct the
   user to relocate project extensions into `agent-working-rules.md` before
   replacing it.
3. **Should working rules become byte-matched?** No. They are project-owned. Add
   a language-neutral machine marker while continuing to accept the v1.16.0
   sentinel during the compatibility window.
4. **Should the tool auto-delete runtime adapters?** No. It may report tracking
   state, detected risk signals, and the manual action, but deletion requires
   human review.
5. **Should v1.17.0 bump the project contract revision?** No. Package version and
   contract revision are separate concepts. v1.17.0 supports the unchanged
   v1.16 contract revision.

## Phase 0 — Lock the incident into red tests

### Files

- `scripts/tests/fixtures/contract-drift-v1/` — add a sanitized, minimal fixture.
- `scripts/tests/test_contract_check.py` — extend unit coverage.
- `scripts/tests/test_contract_migration.py` — add end-to-end plan-output tests.

### Work

1. Capture the load-bearing incident shape only: an older canonical
   `AGENTS.md`, three customized but pointer-shaped runtime files, a static
   workflow with one project extension, localized working rules, and a local
   hook. Copy the fixture into a temporary target for every test; create a
   temporary Git repository only in cases that need tracked/untracked evidence.
2. Snapshot the entire fixture before every migration-plan invocation and prove
   byte-for-byte preservation afterward.
3. Add focused red tests for:
   - package `1.17.0` accepting project contract revision `dat-kit 1.16.0`;
   - stale canonical contract distinguished from a genuinely competing
     `AGENTS.md`;
   - migration-plan grouping consolidates a pointer path without changing its
     legacy diagnostic count;
   - static workflow drift classified as extract-then-replace;
   - localized working rules recognized by a machine marker;
   - tracked, untracked, nested-repository, non-Git, and unavailable-Git runtime
     adapter evidence;
   - deterministic text and JSON output ordering;
   - symlink escape, directory-instead-of-file, unreadable/non-UTF-8 content,
     and invalid targets are never followed or read after classification.
4. Run the narrow suite and preserve the expected failing output in the
   implementation report before changing production code.

### Gate

```text
pytest scripts/tests/test_contract_check.py scripts/tests/test_contract_migration.py
```

The new tests must fail for the intended reasons on `v1.16.0`.

## Phase 1 — Separate package version from contract revision

### Files

- `scripts/contract_check.py`
- `scripts/tests/test_contract_check.py`
- version-bearing manifests during the release phase only

### Work

1. Replace the implicit equality between package SemVer and project-contract
   revision with two explicit concepts:
   - package version, derived from the primary manifest and validated across the
     remaining manifests;
   - supported project-contract revision(s), validated against generated
     projects.
2. Keep `dat-kit 1.16.0` as a supported revision in v1.17.0 because the layout
   is unchanged.
3. Preserve legacy `COMPETING_AGENTS` text diagnostics. Add a structured
   `classification` field (`stale-dat-kit-contract` or `competing-contract`) so
   the planner can distinguish remediation without breaking code consumers.
4. Expose package version, current contract revision, and supported contract
   revisions in `--registry-json`.

### Acceptance

- Bumping manifests from 1.16.0 to 1.17.0 does not invalidate a canonical
  v1.16.0-generated project.
- A true competing `AGENTS.md` still fails closed.
- Revision compatibility has positive and negative tests.

## Phase 2 — Introduce typed, actionable diagnostics

### Files

- `scripts/contract_check.py`
- `scripts/tests/test_contract_check.py`
- `templates/common/docs/agent-working-rules.md.tpl`
- `scripts/tests/test_init_atomicity.py`

### Work

1. Replace tuple-only findings internally with a diagnostic record containing:
   `code`, `path`, `classification`, `summary`, `evidence`, `action`,
   `template`, and `manual_review`.
2. Preserve `Report.items` as a tuple projection and the existing one-line text
   prefix (`CODE: message`) for backward compatibility; add deterministic JSON
   output with an explicit schema version for tooling.
3. Classify remediation into a closed enum:
   - `EXTRACT_THEN_REPLACE` — static canonical file containing project
     extensions;
   - `MERGE_REQUIRED` — project-owned canonical policy;
   - `INSPECT_REMOVE` — runtime adapter/config;
   - `RENAME_REQUIRED` — wrong-cased path;
   - `BLOCKED_UNSAFE` — symlink, escape, invalid target, or unreadable content.
4. Preserve `POINTER_MISMATCH` and `POINTER_POLICY` as separate diagnostics in
   default text, `Report.items`, and JSON. `POINTER_POLICY` is legacy-only:
   keyword matches may add evidence but never choose the classification/action.
   Only the planner's `groups` view may consolidate both codes by path.
5. Add a stable HTML marker to the working-rules template and recognize both
   that marker and the v1.16.0 English sentinel. Do not require English prose in
   project-owned content.
6. Inspect runtime adapters read-only and report Git tracking state plus narrow
   risk signals (shared policy, routing/proxy settings, absolute commands, or
   unknown schema). Do not claim a file is safe merely because no signal matched.
   Resolve tracking state against the target repository, not dat-kit's own Git
   root, and handle non-Git targets explicitly.
7. Use this conservative remediation decision table:

   | File state | Planner action |
   |---|---|
   | Exact current template | no action |
   | Any customized or unknown static pointer/workflow | `EXTRACT_THEN_REPLACE` |
   | `AGENTS.md` or working rules with recognizable dat-kit markers | `MERGE_REQUIRED` |
   | Unrecognized contract/policy content | `MERGE_REQUIRED` |
   | Runtime config/adapter, regardless of content heuristic | `INSPECT_REMOVE` |
   | Unsafe/unreadable path | `BLOCKED_UNSAFE` |

   Keyword/structural heuristics may add bounded evidence labels, but never make
   a static mismatch safe to replace without extraction. Add positive and
   negative fixtures in English and Vietnamese for pointer-only prose, copied
   policy, and unknown content.
8. Use `lstat`/no-follow inspection. Once a path is classified unsafe, invalid,
   a directory, unreadable, or non-UTF-8, short-circuit all content inspection
   for that path. Other safe paths may still be diagnosed.

### Acceptance

- For safe readable paths, default text output, `Report.items`, and JSON
  diagnostics remain code/order/cardinality-compatible with existing fixtures.
  Unsafe paths intentionally stop after their first unsafe diagnostic.
  Migration-plan text and its `groups` array present seven actionable path
  groups for the incident: one canonical entrypoint, three pointers, one static
  workflow, one working-rules file, and one runtime adapter.
- Existing scripts that only check exit status or parse `CODE:` continue to work.
- The checker never prints file contents that may contain secrets.
- A fresh scaffold contains the new marker, while a v1.16 sentinel-only project
  remains valid and idempotent.

## Phase 3 — Add a read-only migration planner

### Files

- `scripts/contract_check.py` or a small sibling module if separation keeps the
  checker deep and testable.
- `scripts/tests/test_contract_migration.py`

### CLI contract

```text
python scripts/contract_check.py --target <path> --migration-plan
python scripts/contract_check.py --target <path> --migration-plan --format json
```

`--format` is `text|json` and defaults to `text`. `--format json` without
`--migration-plan` serializes the target check. Both `--format json` and
`--migration-plan` require `--target`; maintainer-root checking keeps its
existing text interface. Existing `--registry-json` remains backward-compatible:
current fields and values remain, while package/support metadata is additive.
It is mutually exclusive with `--target`, `--migration-plan`, and `--format`.
Argument errors exit 2; a clean check exits 0; any diagnostic or unresolved
migration item exits 1.

The JSON envelope is frozen at schema 1:

```json
{
  "schema_version": 1,
  "mode": "check",
  "target": ".",
  "ok": false,
  "package_version": "1.17.0",
  "contract_revision": "dat-kit 1.16.0",
  "supported_contract_revisions": ["dat-kit 1.16.0"],
  "diagnostics": [
    {
      "code": "POINTER_MISMATCH",
      "path": "CLAUDE.md",
      "classification": "customized-static",
      "summary": "bounded non-secret text",
      "evidence": ["template-mismatch", "policy-keyword"],
      "action": "EXTRACT_THEN_REPLACE",
      "template": "templates/common/CLAUDE.md",
      "manual_review": true
    }
  ],
  "migration_plan": null
}
```

All displayed fields are required. `target` is always `.` rather than an
absolute path; `path`, `template`, and every evidence item are target/package-
relative strings. `migration_plan` is `null` in check mode and an object with
ordered `groups`, `steps`, `preservation`, and `unresolved` arrays in planner
mode. Each group contains `path`, `diagnostic_codes`, `action`, and ordered step
references. Arrays are present even when empty. No config content is serialized.
Top-level scalar types are exactly those shown. Each diagnostic has string
`code`, `path`, `classification`, `summary`, and `action`; string-array
`evidence`; string-or-null `template`; and boolean `manual_review`. Diagnostics
retain legacy emission order. Unknown extra fields are forbidden within schema
1 so consumers can validate the envelope deterministically.

Schema 1 closes the following value sets:

- `mode`: `check` or `migration-plan`.
- `classification`: `stale-dat-kit-contract`, `competing-contract`,
  `current-static`, `customized-static`, `project-owned-policy`,
  `runtime-adapter`, `wrong-case`, `unsafe-path`, or `invalid-content`.
- `action`: `EXTRACT_THEN_REPLACE`, `MERGE_REQUIRED`, `INSPECT_REMOVE`,
  `RENAME_REQUIRED`, or `BLOCKED_UNSAFE`.
- `evidence` items: `template-match`, `template-mismatch`, `policy-keyword`,
  `canonical-marker`, `legacy-sentinel`, `tracked`, `untracked`,
  `not-a-git-repo`, `git-unavailable`, `routing-signal`,
  `absolute-command-signal`, `unknown-schema`, `symlink`, `target-escape`,
  `directory`, `unreadable`, `non-utf8`, `wrong-case`, `legacy-artifact`, or
  `invalid-target`.
- `summary`: a fixed checker-authored message, never source content, limited to
  240 Unicode code points.

`migration_plan` item schemas are also closed:

- `groups[]`: `{path: string, diagnostic_codes: string[], action: action-enum,
  step_ids: string[], manual_review: boolean}`.
- `steps[]`: `{id: string, instruction: instruction-enum, paths: string[],
  depends_on: string[], manual_review: boolean}`. IDs match `^S[0-9]{3}$`.
- `instruction`: `INVENTORY_POLICY`, `EXTRACT_PROJECT_POLICY`,
  `REPLACE_FROM_TEMPLATE`, `MERGE_CANONICAL_POLICY`,
  `INSPECT_RUNTIME_ADAPTER`, `RENAME_PATH`, `RESOLVE_UNSAFE_PATH`, or
  `VERIFY_CONTRACT`.
- `preservation[]`: `{path: string, method: preservation-enum,
  destination: string|null, step_id: string}` where `method` is
  `BYTE_SNAPSHOT`, `POLICY_INVENTORY`, or `MANUAL_INSPECTION`.
- `unresolved[]`: `{path: string, reason: unresolved-enum, step_id: string}`
  where `reason` is `POLICY_DESTINATION`, `UNKNOWN_CONTENT`,
  `RUNTIME_DEPENDENCY`, or `UNSAFE_PATH`.

All item paths are relative; arrays use diagnostic/path/dependency order; every
item field above is required; and schema 1 permits no additional item fields.
Every `step_ids`, `depends_on`, `preservation[].step_id`, and
`unresolved[].step_id` value references an existing step. The dependency graph
is acyclic and `steps` are emitted in stable topological order. Changing any set
or shape requires a new schema version.

### Work

1. Generate a dependency-ordered plan to stdout; never create a plan file inside
   the target automatically.
2. Plan sections must be:
   - baseline command and current diagnostics;
   - policy inventory sources;
   - destination map for project-owned policy;
   - static extract-then-replace steps with exact template sources;
   - manual runtime-adapter inspection;
   - verification commands and expected exit status.
3. Include an explicit preservation table for every affected file and an
   `UNRESOLVED` section whenever human judgment is still required.
4. Return non-zero while unresolved drift exists, including in migration-plan
   mode. A readable plan is not a green contract.
5. Keep the plan deterministic across Windows/Linux path separators and line
   endings.
6. Emit only target-relative paths and bounded evidence labels in migration-plan
   text and all JSON; never serialize config contents or secrets. Legacy default
   check text retains its existing messages, including user-supplied/absolute
   target paths, for v1 compatibility.
7. Keep default check text unchanged. Grouping is exclusive to migration-plan
   text; JSON always uses the frozen per-path envelope above.

### Acceptance

- On the incident fixture, the generated plan instructs the user to preserve
  policy before replacing any static file and to inspect the hook before
  removal.
- The generated plan never says “not mounted” or assumes target access it has
  not tested.
- Re-running produces identical normalized text/JSON and no filesystem diff.

## Phase 4 — Route workflows and documentation to the planner

### Files

- `skills/project-init/SKILL.md`
- `skills/build-loop/SKILL.md`
- `scripts/init.sh`
- `scripts/tests/test_init_atomicity.py`
- `docs/codex.md`
- `README.md`
- `HUONG_DAN.vi.md`
- `benchmarks/skill-evals.jsonl` only if a skill description changes

### Work

1. On brownfield conflict, print the migration-plan command before the generic
   manual-migration documentation link.
2. In build-loop PREFLIGHT, distinguish “contract drift found” from “migration
   performed”; route to the read-only planner and stop until the resulting plan
   is approved and executed separately.
3. Document which files are static dat-kit assets versus project-owned policy.
4. Document the contract-revision compatibility policy: patch releases do not
   force project rewrites; a schema/layout change does.
5. Add a worked, generic v1.15-to-v1.16 example without copying private project
   rules or paths.
6. Do not change `templates/common/docs/agent-workflow.md` in this release: it is
   exact-matched, so changing it would recreate drift in every canonical v1.16
   project. Installed skills and package documentation provide the new route.
7. Extend atomicity tests so every unresolved remediation class aborts before
   `mkdir`, copy, placeholder substitution, or Git initialization, with a full
   before/after byte snapshot.

### Acceptance

- A cold user can move from a named diagnostic to a file-by-file migration plan
  with one documented command.
- No documentation suggests that `init.sh --here` will migrate conflicting
  files automatically.

## Phase 5 — Full verification, review, and release gate

### Red-before-green evidence

- Preserve Phase 0 failing output in the task report.
- Deliberately corrupt one fixture per remediation class and observe the exact
  expected diagnostic before restoring it.

### Required gates

```text
python scripts/validate.py
pytest scripts/tests
bash -n scripts/init.sh
shellcheck scripts/init.sh
git diff --check
```

Also run:

```text
python scripts/contract_check.py --target <incident-fixture> --migration-plan
python scripts/contract_check.py --target <canonical-v1.16-fixture>
```

### Reviews

1. `qa-agent`: full gates plus mutation/snapshot and cross-platform output tests.
2. `code-reviewer`: diagnostic/API compatibility and maintainability review.
3. `security-reviewer`: mandatory because the checker resolves user-controlled
   paths and inspects possible runtime configuration.
4. Regression QA after every review-driven change.

### Release

1. Confirm the source tree is clean except for the approved implementation.
2. Update manifests and release notes to 1.17.0 without changing the supported
   project-contract revision.
3. Re-run all gates.
4. Commit, tag, push, and verify a real GitHub Actions run only after explicit
   release approval.
5. Update/reinstall the plugin and test from a fresh session.

## Definition of done

- A package version bump no longer invalidates an unchanged project-contract
  schema.
- Every drift finding identifies the affected path, evidence class, safe/manual
  action, and template source where applicable.
- Brownfield users can generate a deterministic migration plan without any
  target mutation.
- Static files remain strict, project-owned policy remains customizable, and
  runtime adapters remain manual-review boundaries.
- The captured incident and all remediation classes are regression-tested.
- All repository gates and independent reviews pass.
- The application incident can be repaired from the generated plan, after a
  separate approval, without losing any project-specific rule.

## Approval gate

Implementation of Phase 0-5 was approved on 2026-07-15 and is complete in the
local worktree. The incident repository was inspected read-only and was not
modified. Do not commit, tag, push, publish, or reinstall v1.17.0 until the user
gives separate release approval.
