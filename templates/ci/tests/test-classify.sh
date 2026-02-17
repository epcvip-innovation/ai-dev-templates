#!/usr/bin/env bash
# test-classify.sh — Fixture tests for classify-pr.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLASSIFY="$SCRIPT_DIR/scripts/classify-pr.sh"
POLICY="$SCRIPT_DIR/risk-policy.json.template"
PASS=0; FAIL=0
TMPDIR_TEST=$(mktemp -d)
trap 'rm -rf "$TMPDIR_TEST"' EXIT

assert_tier() {
  local desc="$1" expected="$2" actual_tier
  shift 2
  actual_tier=$("$@" 2>/dev/null | jq -r '.tier') || true
  if [[ "$actual_tier" == "$expected" ]]; then
    echo "  PASS: $desc"
    ((++PASS))
  else
    echo "  FAIL: $desc (expected=$expected actual=$actual_tier)"
    ((++FAIL))
  fi
}

assert_fails() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "  FAIL: $desc (expected failure, got success)"
    ((++FAIL))
  else
    echo "  PASS: $desc"
    ((++PASS))
  fi
}

echo "=== Tier classification ==="
assert_tier "auth path → critical" "critical" \
  bash "$CLASSIFY" "$POLICY" "src/auth/login.ts"
assert_tier "API path → high" "high" \
  bash "$CLASSIFY" "$POLICY" "src/api/users.ts"
assert_tier "src path → standard" "standard" \
  bash "$CLASSIFY" "$POLICY" "src/utils/format.ts"
assert_tier "markdown → low" "low" \
  bash "$CLASSIFY" "$POLICY" "README.md"
assert_tier "docs dir → low" "low" \
  bash "$CLASSIFY" "$POLICY" "docs/guide.md"

echo "=== Mixed files (highest wins) ==="
assert_tier "critical + low → critical" "critical" \
  bash "$CLASSIFY" "$POLICY" "src/auth/login.ts" "README.md"

echo "=== CI infrastructure → critical ==="
assert_tier "workflow file → critical" "critical" \
  bash "$CLASSIFY" "$POLICY" ".github/workflows/ci.yml"
assert_tier "classifier script → critical" "critical" \
  bash "$CLASSIFY" "$POLICY" ".github/scripts/classify-pr.sh"
assert_tier "risk policy → critical" "critical" \
  bash "$CLASSIFY" "$POLICY" ".github/risk-policy.json"

echo "=== Stdin input ==="
assert_tier "stdin with spaces in filename" "standard" \
  bash -c "echo 'src/my file.ts' | bash '$CLASSIFY' '$POLICY'"
assert_tier "stdin with empty lines" "low" \
  bash -c "printf '\nREADME.md\n\n' | bash '$CLASSIFY' '$POLICY'"

echo "=== Escape hatch ==="
assert_tier "SKIP_RISK_GATE=1 → low" "low" \
  env SKIP_RISK_GATE=1 bash "$CLASSIFY" "$POLICY" "src/auth/login.ts"

echo "=== Policy validation ==="

cat > "$TMPDIR_TEST/bad-default.json" <<'JSON'
{"tiers":{"low":{"required_checks":[]}},"path_rules":[],"default_tier":"nope"}
JSON
assert_fails "invalid default_tier reference fails" \
  bash "$CLASSIFY" "$TMPDIR_TEST/bad-default.json"

cat > "$TMPDIR_TEST/bad-rule.json" <<'JSON'
{"tiers":{"low":{"required_checks":[]}},"path_rules":[{"pattern":"**","tier":"typo"}],"default_tier":"low"}
JSON
assert_fails "undefined tier in path_rules fails" \
  bash "$CLASSIFY" "$TMPDIR_TEST/bad-rule.json"

cat > "$TMPDIR_TEST/no-default.json" <<'JSON'
{"tiers":{"low":{"required_checks":[]}},"path_rules":[]}
JSON
assert_fails "missing default_tier field fails" \
  bash "$CLASSIFY" "$TMPDIR_TEST/no-default.json"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
