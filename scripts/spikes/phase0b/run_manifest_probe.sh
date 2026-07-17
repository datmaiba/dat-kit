#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd -- "$scratch"

output=$(bash "$script_dir/parse_manifest.sh" "$script_dir/fixtures/manifest-valid.tsv")
expected=$'MATERIALIZE\ttemplates/common/AGENTS.md\tAGENTS.md\tcopy'
[[ "$output" == "$expected" ]]

for fixture in manifest-injection.tsv manifest-traversal.tsv manifest-unknown-action.tsv manifest-late-invalid.tsv; do
  if bash "$script_dir/parse_manifest.sh" "$script_dir/fixtures/$fixture" >"$scratch/stdout" 2>"$scratch/stderr"; then
    printf 'expected rejection: %s\n' "$fixture" >&2
    exit 1
  fi
  [[ ! -s "$scratch/stdout" ]]
done

[[ ! -e "pwned" ]]
printf 'MANIFEST_PROBE_OK shell=%s valid=1 rejected=4 atomic-reject=1 no-eval=1\n' "${BASH_VERSION}"
