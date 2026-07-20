---
name: read-pack
description: Phase 0B probe that must read a bundled file outside the skills directory.
---

# Materialization probe

Resolve this skill's installed directory, walk exactly two parents to the plugin
root, and use a read-only filesystem tool to read `pack/probe.txt`. Do not infer
the probe value from this instruction: it appears only in that file.

Then attempt to read `pack/does-not-exist.txt` from the same plugin root. Return
exactly two semicolon-separated fields:

`value=<contents of probe.txt>; missing=<the observed failure class>`

Do not run shell commands and do not write files.
