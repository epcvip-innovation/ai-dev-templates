#!/bin/bash
# audit-variables.sh - Check required Railway environment variables
#
# Usage: ./audit-variables.sh

# Define required variables for your project
REQUIRED_VARS=(
  "DATABASE_PATH"
  "JWT_SECRET_KEY"
  "ENVIRONMENT"
)

# Add your project-specific variables here
# REQUIRED_VARS+=(
#   "AWS_ACCESS_KEY_ID"
#   "AWS_SECRET_ACCESS_KEY"
# )

echo "=== Railway Variable Audit ==="
echo ""

missing=0
found=0

for var in "${REQUIRED_VARS[@]}"; do
  if railway variables 2>/dev/null | grep -q "^$var="; then
    echo "✅ $var"
    found=$((found + 1))
  else
    echo "❌ $var (MISSING)"
    missing=$((missing + 1))
  fi
done

echo ""
echo "Summary: $found found, $missing missing"

if [ $missing -gt 0 ]; then
  echo ""
  echo "Set missing variables with:"
  echo "  railway variables set VARIABLE_NAME=value"
  exit 1
else
  echo ""
  echo "✅ All required variables are set"
fi
