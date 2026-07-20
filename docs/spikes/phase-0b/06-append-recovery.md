# Spike 06: append and recovery across operating systems

Phase 0B reused the released 1.17.1 append primitive rather than creating a
second JSONL writer. Targeted `test_scorecard_append.py` results:

```text
Windows Python 3.12   18 passed, 2 skipped
Linux Python 3.12     19 passed, 1 skipped
```

The suite covers append-only prefix preservation, concurrent locking,
short-write rollback, malformed history, strict schema-v2 input, path swaps,
hardlinks, symlinks where the OS permits them, and report-time enrichment that
does not persist.

Decision for the future telemetry writer: reuse a shared append primitive with
record-boundary locking, `O_APPEND`, exact positive write counts, rollback
under the same lock, UTF-8 JSON lines, and replacement-aware path checks.
Single-writer interrupted recovery is required for 2.1; multi-writer telemetry
is not claimed until delegated writers actually need it. Corrections append a
new record and never rewrite history.
