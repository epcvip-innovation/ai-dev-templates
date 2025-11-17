#!/bin/bash
# health-check.sh - Verify Railway deployment health
#
# Usage:
#   ./health-check.sh
#   ./health-check.sh https://your-app.up.railway.app

PROJECT_URL="${1:-https://your-app-production.up.railway.app}"

echo "=== Railway Health Check ==="
echo "Checking: $PROJECT_URL"
echo ""

# Health endpoint check
echo "▶ Checking health endpoint..."
if ! health_response=$(curl -s -f "$PROJECT_URL/health" 2>&1); then
  echo "❌ Health endpoint failed"
  echo "Response: $health_response"
  exit 1
fi

health=$(echo "$health_response" | jq -r '.status // "unknown"' 2>/dev/null || echo "unknown")

if [ "$health" = "healthy" ]; then
  echo "✅ Health: $health"
else
  echo "❌ Health: $health"
  echo "Response: $health_response"
  exit 1
fi

# Check Railway logs for errors
echo ""
echo "▶ Checking logs for errors..."
if command -v railway &> /dev/null; then
  error_count=$(railway logs --json --limit 100 2>/dev/null | jq 'select(.level=="error")' | wc -l || echo "0")
  echo "Errors in last 100 logs: $error_count"

  if [ "$error_count" -gt 10 ]; then
    echo "⚠️  High error count!"
    exit 1
  fi
else
  echo "⚠️  Railway CLI not found, skipping log check"
fi

# Response time check
echo ""
echo "▶ Checking response time..."
response_time=$(( $(date +%s%N) ))
curl -s "$PROJECT_URL/health" > /dev/null
response_time=$(( ($(date +%s%N) - response_time) / 1000000 ))
echo "Response time: ${response_time}ms"

if [ "$response_time" -gt 3000 ]; then
  echo "⚠️  Slow response time"
fi

echo ""
echo "✅ All health checks passed"
