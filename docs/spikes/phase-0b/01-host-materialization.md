# Spike 01: live host materialization

## Question

Can a fresh installed-host session load a skill under `skills/` and read a
bundled file elsewhere inside the plugin root?

## Fixture

Disposable plugin `materialization-probe` 0.1.0, retained as the non-public
fixture `scripts/spikes/phase0b/fixtures/host-materialization/`:

```text
skills/read-pack/SKILL.md
pack/probe.txt                     # rotate to an unpublished nonce per run
```

Immediately before the final 2026-07-18 rerun, the committed marker was
replaced with a new nonce that occurred only in `pack/probe.txt`: it was absent
from the prompt, skill, reports, and other repository files available to each
fresh session. Both returned the exact nonce; its file-byte SHA-256 was
`336a4366ccc8d73480972aca7be83a1fd7adf9f78a393ce0a80fef9c546f7bf6`.
The report records the hash rather than publishing the oracle. The retained
fixture restores a non-evidence marker and its README requires a fresh nonce
and empty working directory for every future live run. The skill also attempted
`pack/does-not-exist.txt` so failure behavior was observable.

## Claude Code 2.1.211

- Existing dat-kit 1.17.1 install: enabled from the `release/1.x` marketplace
  route; installed versions are under
  `~/.claude/plugins/cache/dat-kit/dat-kit/<version>`.
- Probe loading: `claude --plugin-dir <probe-root> -p ... --allowedTools Read`
  in a new, non-persistent session.
- Final fresh result: exact nonce match; `missing=file not found`.
- Resolution: two parents above the skill file reached the plugin root; the
  file outside `skills/` was readable. `--plugin-dir` used the development
  directory in place; marketplace installs use the versioned cache.

## Codex CLI 0.144.4

- Existing dat-kit 1.17.1 install: enabled from the `release/1.x` marketplace
  route.
- Probe installation: a local marketplace with `source: local`, followed by
  `codex plugin add materialization-probe@phase0b-probe`.
- Observed cache:
  `~/.codex/plugins/cache/phase0b-probe/materialization-probe/0.1.0`, including
  both `skills/read-pack/SKILL.md` and `pack/probe.txt`.
- Fresh run: `codex exec --ephemeral -s read-only ...`.
- Final fresh ephemeral/read-only result: exact nonce match; `missing=ENOENT`.
- The probe plugin and marketplace, disposable installed copy, and exact empty
  `phase0b-probe` cache namespace were removed after evidence capture.

## Decision

Select Option A. Both tested hosts copied/resolved content outside `skills/`
when it remained inside the plugin root. This does not authorize traversal
outside the plugin root. Every installed conformance smoke must reinstall or
update the plugin and start a new session; cached or already-open sessions are
not evidence for a changed trigger or pack.

Official constraints: [Claude plugin cache and root boundary](https://code.claude.com/docs/en/plugins-reference),
[Codex local marketplace and plugin layout](https://learn.chatgpt.com/docs/build-plugins),
and [Codex new-session requirement](https://learn.chatgpt.com/docs/plugins).
