---
name: task-loop
description: >-
  Route non-software work to the right Domain Pack. Invoke with "run the task loop", "task-loop", or when the user wants to start non-code work and choose which discipline applies. Lists every registered non-software active pack and routes the chosen one through the work-loop engine and its six slots; a new pack registered via domain-builder appears automatically. Raises no pack's loop ceiling and carries no domain policy of its own.
---
<!-- GENERATED FROM REGISTRY — DO NOT EDIT; source_revision=domains/1 -->

# task-loop

Route non-software work through the Registry Catalog. On a bare
`task-loop`, present the menu below and ask which pack to run. On
`task-loop <domain-id>`, resolve that descriptor through the Catalog, load
its declared engine and the pack's six semantic slots in order, then run
the pack's own deliverable, gate, and reviewer routing.

Registered non-software packs (registry-driven; a new active pack
appears here with no code change):

- `knowledge-work` → trigger `knowledge-work`, pack `domains/knowledge-work`

Registered aliases: `non-code work`, `task loop`.
Fail closed with `DOMAIN_SLOT_MISSING` or `DOMAIN_ENGINE_REVISION_MISMATCH`
before execution when the Catalog, engine, or any slot is unavailable.
Route only through the selected pack; this trigger contains no independent
domain policy.
