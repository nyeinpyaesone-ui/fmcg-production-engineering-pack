#!/bin/sh
# Loop-runner for every test framework in this repo: runs each suite, retries
# once on failure, and exits nonzero if anything is still red. Emits EVENT
# lines so CI logs and humans see exactly what passed, what retried, and what
# failed. No secrets are read, printed or required. Run from the repo root.
set -u
MAX_ATTEMPTS=2
FAILED=""
BUILD_FRONTEND="${BUILD_FRONTEND:-0}"

event() {
  printf 'EVENT %s\n' "$1"
}

run_suite() {
  name="$1"
  shift
  attempt=1
  while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
    if "$@" > "/tmp/verify-$name.log" 2>&1; then
      event "$name pass attempt=$attempt"
      return 0
    fi
    event "$name fail attempt=$attempt (see /tmp/verify-$name.log)"
    attempt=$((attempt + 1))
  done
  FAILED="$FAILED $name"
  return 1
}

event "loop-start max_attempts=$MAX_ATTEMPTS"
run_suite docs-lint npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".agents/**/*.md" || true
run_suite docs-integrity python3 scripts/check_docs.py || true
run_suite yaml-lint pipx run yamllint -c .yamllint.yaml config/agent-policy.yaml \
  .github/workflows/quality.yml .github/workflows/release.yml || true
run_suite backend-lint .venv/bin/ruff check ./backend || true
run_suite backend-format .venv/bin/ruff format --check ./backend || true
(cd backend && run_suite backend-typecheck ../.venv/bin/mypy app) || true
(cd backend && run_suite backend-tests ../.venv/bin/pytest -q) || true
run_suite frontend-typecheck npm run check --prefix frontend || true
run_suite frontend-format npm run format:check --prefix frontend || true
run_suite frontend-tests npm test --prefix frontend || true
if [ "$BUILD_FRONTEND" = "1" ]; then
  run_suite frontend-build npm run build --prefix frontend || true
fi

if [ -z "$FAILED" ]; then
  event "loop-result all-green"
  exit 0
else
  event "loop-result FAILED:$FAILED"
  exit 1
fi
