# Host Adapter — Codex

Registry descriptor: `registry/adapters.json#adapter_id=codex`. Lifecycle:
`repo_only` (no project artifact exists or is emitted). Contract:
`docs/contracts/host-adapter.md`.

## Pointer semantics

Codex reads `AGENTS.md` natively — the canonical contract needs no pointer
file, so this adapter owns **zero** project artifacts. Missing `AGENTS.md`
degrades to documented host-default behavior (`documented-degradation`).

## Repository artifacts

`.agents/plugins/marketplace.json` and `.codex-plugin/plugin.json`
(host-mandated, repo root; `skills: ./skills/`).

## Official facts (dated; re-verify before the affected RC)

See descriptor `official_facts`: native AGENTS.md discovery (verified
2026-07-18, learn.chatgpt.com/docs/agent-configuration/agents-md); plugins
install via local marketplace and need a fresh session after install/update.
Phase 0B live spike on Codex CLI 0.144.4: installed plugin materialized and
read a file outside `skills/` (decision 0001) — the previously UNVERIFIED
claim in the plan's factual footer is now verified evidence.

## Conformance

- Fixture `ADAPTER-CODEX-01` + `test_adapter_conformance.py`: no project
  artifacts, no duplicate policy surface, rollback owns only the two
  manifests.
- Host smoke (host available to maintainer): reinstall plugin, fresh
  `codex exec` run, invoke thin trigger, confirm pack read.

## Rollback

Remove the two manifests only; project trees are untouched by definition.
