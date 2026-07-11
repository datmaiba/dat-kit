#!/usr/bin/env bash
# dat-kit project-init — scaffold a spec-driven project.
# Usage:
#   init.sh <project-name> [--profile <name>] [--desc "<one-liner>"]   # greenfield: creates ./<project-name>
#   init.sh --here [--profile <name>] [--desc "<one-liner>"]           # brownfield: current dir, never overwrites
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TPL="$DIR/templates"

NAME="" ; HERE=false ; PROFILE="laravel-react" ; DESC="(fill in: one sentence — what this is and for whom)"
while [ $# -gt 0 ]; do
  case "$1" in
    --here) HERE=true ;;
    --profile) PROFILE="$2"; shift ;;
    --desc) DESC="$2"; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) NAME="$1" ;;
  esac
  shift
done

PROF="$TPL/profiles/$PROFILE"
if [ ! -d "$PROF" ]; then
  echo "✗ Unknown profile '$PROFILE'. Available:"; ls "$TPL/profiles/"; exit 1
fi

if $HERE; then
  TARGET="$(pwd)"; NAME="${NAME:-$(basename "$TARGET")}"
else
  if [ -z "$NAME" ]; then echo "✗ Usage: init.sh <project-name> | init.sh --here"; exit 1; fi
  TARGET="$(pwd)/$NAME"
  if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null)" ]; then
    echo "✗ '$TARGET' exists and is not empty. Use: cd $NAME && init.sh --here"; exit 1
  fi
  mkdir -p "$TARGET"
fi

CREATED=0; SKIPPED=0
copy_if_missing() { # $1 src, $2 dst
  if [ -e "$2" ]; then echo "  skip (exists): ${2#"$TARGET"/}"; SKIPPED=$((SKIPPED+1))
  else mkdir -p "$(dirname "$2")"; cp "$1" "$2"; echo "  + ${2#"$TARGET"/}"; CREATED=$((CREATED+1)); fi
}

fill_name() { # $1 file — replace placeholders in place (portable, no sed -i)
  local tmp; tmp="$(mktemp)"
  # escape sed-special chars in user input (\, &, and the | delimiter)
  local desc_esc; desc_esc=$(printf '%s' "$DESC" | sed -e 's/[\\&|]/\\&/g')
  local name_esc; name_esc=$(printf '%s' "$NAME" | sed -e 's/[\\&/]/\\&/g')
  sed -e "s/{{PROJECT_NAME}}/$name_esc/g" -e "s/{{PROFILE_NAME}}/$PROFILE/g" -e "s|{{PROJECT_DESC}}|$desc_esc|g" "$1" > "$tmp" && mv "$tmp" "$1"
}

echo "Scaffolding '$NAME' (profile: $PROFILE) into $TARGET"

# spec skeleton + lessons + rules
for f in "$TPL"/common/spec/*.md; do copy_if_missing "$f" "$TARGET/spec/$(basename "$f")"; done
copy_if_missing "$TPL/common/lessons-learned/lessons-learned.md" "$TARGET/lessons-learned/lessons-learned.md"
copy_if_missing "$TPL/common/rules/working.rules.md" "$TARGET/.claude/rules/working.rules.md"
[ -e "$TARGET/lessons-learned/lessons-learned.md" ] && fill_name "$TARGET/lessons-learned/lessons-learned.md"

# CLAUDE.md — assemble template + profile sections
if [ -e "$TARGET/CLAUDE.md" ]; then
  echo "  skip (exists): CLAUDE.md  → review $PROF/*.md and merge manually"; SKIPPED=$((SKIPPED+1))
else
  sed -e "/{{PROFILE_ARCHITECTURE}}/r $PROF/architecture.md" -e "/{{PROFILE_ARCHITECTURE}}/d" \
      -e "/{{PROFILE_GATES}}/r $PROF/gates.md"               -e "/{{PROFILE_GATES}}/d" \
      -e "/{{PROFILE_TRAPS}}/r $PROF/traps.md"               -e "/{{PROFILE_TRAPS}}/d" \
      "$TPL/common/CLAUDE.md.tpl" > "$TARGET/CLAUDE.md"
  fill_name "$TARGET/CLAUDE.md"
  echo "  + CLAUDE.md"; CREATED=$((CREATED+1))
fi

# git init (greenfield only, best-effort)
if ! $HERE && command -v git >/dev/null 2>&1 && [ ! -d "$TARGET/.git" ]; then
  (cd "$TARGET" && git init -q) && echo "  + git init" || echo "  ! git init failed (continue manually)"
fi

echo ""
echo "Done: $CREATED created, $SKIPPED skipped (existing files are never overwritten)."
echo "Next steps:"
echo "  1. Fill spec/ in order: 00-vision → 01-features → 02-architecture → 03-db-schema → 04-build-phases"
echo "  2. Review CLAUDE.md (profile: $PROFILE) — adjust gate commands to your compose services"
echo "  3. Start building: open Claude Code and run the dat-kit build-loop (preflight first for autopilot)"
