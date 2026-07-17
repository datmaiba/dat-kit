# Initial Host Adapter facts

Verified 2026-07-18 against primary vendor documentation. These are dated
capability assumptions, not permanent truths; Phase 2 re-verifies them before
activation and Phase 5 re-verifies them before RC.

| Host | Verified fact | Adapter consequence | Primary source |
|---|---|---|---|
| Claude Code | Project `CLAUDE.md` can import `@AGENTS.md`; marketplace plugins are copied to a versioned cache and cannot traverse outside the plugin root; `SessionStart` can inject context. | Keep `CLAUDE.md` as a thin import pointer. Keep engine/packs inside the plugin root. `hooks.json` may remain the Claude-only task-start producer in 2.1. | [Memory and AGENTS import](https://code.claude.com/docs/en/memory), [plugin cache](https://code.claude.com/docs/en/plugins-reference), [SessionStart](https://code.claude.com/docs/en/hooks) |
| Codex | Codex reads `AGENTS.md` once per run; plugins use `.codex-plugin/plugin.json`, bundle skills, can be installed through a local marketplace, and require a new session for newly installed capabilities. | `AGENTS.md` is native and canonical; no duplicate Codex policy file. Plugin descriptor uses `skills: ./skills/`. Reinstall/update plus a fresh run is mandatory smoke evidence. | [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [build plugins](https://learn.chatgpt.com/docs/build-plugins), [use plugins](https://learn.chatgpt.com/docs/plugins) |
| Gemini CLI | Extensions are copied on install, use root `gemini-extension.json`, accept `contextFileName`, and default to root `GEMINI.md`; context files support relative `@file` imports. Extension changes need update/restart unless linked for development. | Repository descriptor remains `repo_only` until a live host is available. A project `GEMINI.md` may be a thin import of `AGENTS.md`; do not duplicate policy. | [Extension reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md), [GEMINI.md context](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md) |
| Cursor | Cursor CLI reads root `AGENTS.md` and `CLAUDE.md`; project rules live in `.cursor/rules`; `.cursorrules` is documented as legacy and deprecated but still supported. | Native `AGENTS.md` is sufficient for the initial pointer. Treat `.cursorrules` as `RETIRE_LEGACY` only through approved migration; do not claim official documentation says Agent mode ignores it. | [CLI project context](https://docs.cursor.com/en/cli/using), [rules and deprecation](https://docs.cursor.com/context/rules-for-ai) |

### Correction to the approved plan's factual footer

The plan stated that Cursor Agent mode ignores `.cursorrules`. The official
rules page supports only “still supported, but deprecated.” Community reports
are not a stable Host Adapter contract. Phase 3 therefore bases retirement on
official deprecation plus migration fixtures, not on an unverified ignored-file
claim.
