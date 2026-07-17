# Spike 07: deterministic proposal IDs

The probe canonicalized relative paths to POSIX separators, sorted evidence
records by canonical JSON bytes, serialized UTF-8 with sorted keys and compact
separators, and included the evidence window, policy revision, and governed
owner in identity.

Windows-style paths with reversed record order and POSIX paths produced:

```text
proposal-234e1262e1386ea27425
```

Changing only the evidence window produced:

```text
proposal-4611fdec125470aa6f21
```

Changing only the policy revision and changing only the governed owner each
produced distinct IDs (`proposal-3620a72b402fa66094f9` and
`proposal-0a2ce05a522d9093976d`). Negative cases rejected POSIX absolute paths,
Windows drive-absolute paths, UNC paths, traversal, empty/current-directory
aliases, and Unicode `Cc` control characters (including NUL and C1 controls).

Decision: separator and input-record order are not semantic; evidence window,
normalized record content, policy revision, and governed owner are semantic.
Reject absolute paths, traversal, empty/current-directory aliases, and Unicode
`Cc` controls after canonicalization and before hashing. The 2.2 contract must add
input hashes and policy hash to this canonical payload; the miner cannot choose
an easier identity after seeing an outcome.
