---
name: build-loop
description: >-
  Compatibility alias — the build-loop trigger was renamed to code-loop. Invoke on "run the build loop" or any legacy build-loop phrasing; this stub routes to the code-loop skill, which loads the work-loop engine and the software-dev Domain Pack (six slots: workflow, ground truth, gates, reviewers, deliverables, loop profile). Kept for at least one minor for muscle memory and existing plugin references.
---
<!-- Hand-authored compatibility alias. NOT a registry projection — do not add the generated marker. -->

# build-loop (compatibility alias)

`build-loop` was renamed to `code-loop`. This stub exists only so the old name
keeps working for at least one minor release.

Do exactly what `code-loop` does: resolve domain `software-dev` through the
Registry Catalog, load engine `work-loop/1` and pack `domains/software-dev`, and
run that pack's own deliverable, gate, and reviewer routing. Load the pack's six
semantic slots in its declared order. This alias carries no independent policy of
its own.

Canonical trigger: `skills/code-loop/SKILL.md`.
