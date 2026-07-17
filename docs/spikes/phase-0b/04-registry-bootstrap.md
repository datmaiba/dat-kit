# Spike 04: registry bootstrap diagnostics

A stdlib-only loader was exercised with missing, malformed, and future-format
bootstrap files. The future fixture referenced a missing child on purpose.

Both Windows and Linux returned:

```text
missing                   REGISTRY_BOOTSTRAP_MISSING
malformed                 REGISTRY_BOOTSTRAP_MALFORMED
future-with-missing-child REGISTRY_FORMAT_UNSUPPORTED actual=2 supported=1
```

The future-format diagnostic occurred before child loading. Decision:
`registry/platform.json` is the only hardcoded bootstrap filename; the running
code checks the top-level format before reading any child. Unknown, old,
future, or wrong-typed revisions fail atomically with a path-aware diagnostic.
Mixed code/data revisions must use `REGISTRY_ATOMIC_UPGRADE_REQUIRED`, never
partial best-effort loading. Validation uses `json` and other Python standard
library modules only and does not claim JSON Schema compliance.
