# Spike 02: deterministic domain-trigger rendering

The stdlib probe rendered the same descriptor with aliases in opposite input
orders. The renderer sorts aliases, uses a fixed field order, encodes UTF-8,
normalizes LF, and writes one terminal newline.

Windows Python 3.12 and Linux Python 3.12 produced the same SHA-256:

```text
c4819f95d42e68ed3caa1c2f15f4f8b11d577eac1197e215708f0ce936846165
```

Decision: descriptor order is not semantic. `render.py domain-trigger` must
emit canonical bytes and `--check` must compare the committed projection
byte-for-byte. A hand edit, missing output, changed descriptor, or changed
engine revision is a failing projection, followed by reinstall and a fresh
host session before acceptance.
