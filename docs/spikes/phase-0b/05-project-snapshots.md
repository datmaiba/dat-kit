# Spike 05: project-contract snapshots without Git

The probe created a project with no `.git` directory and compared its files to
an immutable descriptor containing relative paths and SHA-256 content hashes.
It classified files as:

```text
AGENTS.md                          exact
docs/agent-workflow.md            exact, then customized after a user edit
docs/agent-working-rules.md       missing
```

Decision: recognized project-contract revisions ship immutable marker and
content-hash descriptors under `registry/snapshots/`. Classification is based
on current bytes, not repository history, timestamps, or a remote tag. An exact
generated file may be replaced only by an approved migration action; a
customized file is preserved and reported as a conflict; a missing file is not
proof that the project is pre-marker.
