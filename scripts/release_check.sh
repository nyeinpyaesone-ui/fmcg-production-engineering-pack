#!/bin/sh
# Pre-tag release gate: fails closed unless the tag target is safe to release.
# Usage: sh scripts/release_check.sh vX.Y.Z
# Checks: clean tree, tag format + availability, quality CI green on HEAD.
# Tagging itself still needs explicit human approval (create_release_tag).
set -u

event() {
  printf 'EVENT %s\n' "$1"
}

TAG="${1:-}"
case "$TAG" in
  v[0-9]*.[0-9]*.[0-9]*) ;;
  *) event "bad-tag (want vMAJOR.MINOR.PATCH, got '$TAG')"; exit 1 ;;
esac
event "tag-format-ok $TAG"

if [ -n "$(git status --porcelain)" ]; then
  event "dirty-tree (commit or stash first)"
  exit 1
fi
event "tree-clean"

if git rev-parse "$TAG" >/dev/null 2>&1; then
  event "tag-exists ($TAG already taken)"
  exit 1
fi
event "tag-available"

HEAD_SHA="$(git rev-parse --short HEAD)"
CONCLUSION="$(gh run list --commit "$(git rev-parse HEAD)" --workflow quality.yml \
  --status completed --limit 1 --json conclusion --jq '.[0].conclusion' 2>/dev/null)"
if [ "$CONCLUSION" = "success" ]; then
  event "quality-green $HEAD_SHA"
else
  event "quality-not-green (conclusion: ${CONCLUSION:-none})"
  exit 1
fi

event "release-gate-pass $TAG on $HEAD_SHA (human approval + tag command still required)"
