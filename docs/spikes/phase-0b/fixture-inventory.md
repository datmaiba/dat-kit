# Fixture inventory

## Present at Phase 0B exit

| Fixture/test | Owner | What it proves |
|---|---|---|
| `scripts/tests/fixtures/contract-drift-v1/` | project-contract migration | Known drift is detected from files on disk. |
| `scripts/tests/test_contract_check.py` | project-contract checker | Pointer, path-swap, link, revision, and evidence behavior. |
| `scripts/tests/test_contract_migration.py` | migration planner | Inspection and migration plans do not silently mutate projects. |
| `scripts/tests/test_init_atomicity.py` | greenfield launcher | Failed init leaves target snapshots unchanged. |
| `scripts/tests/test_scorecard_append.py` | append primitive | Append-only, locking, rollback, schema, and path safety. |
| `scripts/spikes/phase0b/fixtures/manifest-valid.tsv` | scaffold projection | One active row materializes and one `repo_only` row does not. |
| `manifest-injection.tsv` | scaffold projection security | Shell metacharacters are rejected without evaluation. |
| `manifest-traversal.tsv` | scaffold projection security | Relative traversal is rejected. |
| `manifest-unknown-action.tsv` | scaffold projection compatibility | Unknown action enum fails closed. |
| `manifest-late-invalid.tsv` | scaffold projection atomicity | A valid actionable prefix plus invalid tail publishes no partial plan. |
| `scripts/spikes/phase0b/probe.py` | Phase 0B decisions | Cross-platform trigger, bootstrap, snapshot, and proposal-ID evidence. |
| `scripts/spikes/phase0b/fixtures/host-materialization/` | host materialization | Reproducible Claude/Codex plugin-root read and missing-file probe; replace the oracle with a fresh nonce before each live run; not part of the public plugin. |

## Required before dependent phase exit

| ID | Phase | Planned fixture |
|---|---|---|
| REG-EXT-01 | 1B | Synthetic registry-only domain passes without production Python edits. |
| ADAPTER-EXT-01 | 1B/2 | Synthetic Host Adapter descriptor and template render without shell/validator edits. |
| REG-FIELD-01 | 1B | Unknown descriptor field returns a path-aware diagnostic. |
| REG-BOOT-01 | 1B | Missing, malformed, old, future, and mixed bootstrap formats fail atomically. |
| PROJ-STALE-01 | 1B | Deleted descriptor referenced by a projection fails byte-exact check. |
| EVOLVE-ORPHAN-01 | 1B | New governed product path fails `EVOLUTION_ORPHAN_PATH`. |
| ADAPTER-CLAUDE-01 | 2 | Claude pointer and plugin-root conformance, official fact date recorded. |
| ADAPTER-CODEX-01 | 2 | Codex native AGENTS, plugin cache, and fresh-session conformance. |
| ADAPTER-GEMINI-01 | 2 | Repo-only GEMINI import pointer and documented degradation if host unavailable. |
| ADAPTER-CURSOR-01 | 2 | Native AGENTS plus `.cursor/rules` behavior; legacy file inventoried. |
| MIG-CLEAN-116 | 3 | Clean v1.16 is recognized but nonzero migration-required. |
| MIG-CUSTOM-116 | 3 | Customized v1.16 preserves user content and reports conflicts. |
| MIG-PARTIAL-20 | 3 | Partially migrated project fails with a named diagnostic. |
| MIG-UNKNOWN | 3 | Unknown/pre-marker revision is inspect-only and never mutated. |
| PACK-SOFTWARE-BEFORE/AFTER | 4 | Normal, autopilot, delegated, security, recovery, and harvest behavior parity. |
| PACK-KNOWLEDGE-BEFORE/AFTER | 4 | Report and fact-check paths retain gate behavior. |
| PACK-SYNTHETIC-01 | 4 | A non-software pack composes through all six slots without engine edits. |
| TRIGGER-LOAD-01 | 4 | Installed Claude/Codex trigger loads actual pack files, not only names. |
