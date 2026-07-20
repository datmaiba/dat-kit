#!/usr/bin/env bash
set -euo pipefail

die() {
  printf 'MANIFEST_INVALID line=%s reason=%s\n' "$1" "$2" >&2
  exit 2
}

safe_path() {
  local value=$1
  [[ "$value" =~ ^[A-Za-z0-9._/-]+$ ]] || return 1
  [[ "$value" != /* ]] || return 1
  [[ ! "$value" =~ ^[A-Za-z]: ]] || return 1
  [[ "/$value/" != *"/../"* ]] || return 1
}

manifest=${1:?usage: parse_manifest.sh MANIFEST}
plan_file=$(mktemp)
trap 'rm -f -- "$plan_file"' EXIT
line_number=0
while IFS=$'\t' read -r source_rel target_rel ownership action introduced_revision lifecycle extra ||
      [[ -n "${source_rel}${target_rel}${ownership}${action}${introduced_revision}${lifecycle}${extra}" ]]; do
  line_number=$((line_number + 1))
  [[ -z "${extra:-}" ]] || die "$line_number" "field-count"
  [[ -n "$source_rel" && -n "$target_rel" && -n "$ownership" && -n "$action" && -n "$introduced_revision" && -n "$lifecycle" ]] ||
    die "$line_number" "field-count"
  safe_path "$source_rel" || die "$line_number" "unsafe-source-path"
  safe_path "$target_rel" || die "$line_number" "unsafe-target-path"
  [[ "$ownership" =~ ^(dat-kit|adapter|user)$ ]] || die "$line_number" "unknown-ownership"
  [[ "$action" =~ ^(copy|render-pointer|preserve)$ ]] || die "$line_number" "unknown-action"
  [[ "$introduced_revision" =~ ^dat-kit\ [0-9]+\.[0-9]+$ ]] || die "$line_number" "invalid-revision"
  [[ "$lifecycle" =~ ^(repo_only|migration_ready|scaffold_active|retired)$ ]] || die "$line_number" "unknown-lifecycle"
  if [[ "$lifecycle" == "scaffold_active" ]]; then
    printf 'MATERIALIZE\t%s\t%s\t%s\n' "$source_rel" "$target_rel" "$action" >> "$plan_file"
  fi
done < "$manifest"

# Publish a materialization plan only after every row has validated.
cat -- "$plan_file"
