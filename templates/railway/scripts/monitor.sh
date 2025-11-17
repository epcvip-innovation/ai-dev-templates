#!/bin/bash
# monitor.sh - Continuous Railway health monitoring
#
# Usage:
#   ./monitor.sh
#   ./monitor.sh https://your-app.up.railway.app

PROJECT_URL="${1:-https://your-app-production.up.railway.app}"
INTERVAL=60  # Check every 60 seconds

while true; do
  clear
  echo "=== Railway Monitoring Dashboard ==="
  echo "Time: $(date)"
  echo "URL: $PROJECT_URL"
  echo ""

  # Health check
  echo "--- Health Status ---"
  if health_response=$(curl -s -f "$PROJECT_URL/health" 2>&1); then
    health=$(echo "$health_response" | jq -r '.status // "unknown"' 2>/dev/null || echo "unknown")
    if [ "$health" = "healthy" ]; then
      echo "✅ Status: $health"
    else
      echo "❌ Status: $health"
    fi
  else
    echo "❌ Health check failed"
  fi

  # Railway status
  if command -v railway &> /dev/null; then
    echo ""
    echo "--- Railway Status ---"
    railway status 2>/dev/null || echo "Could not fetch Railway status"

    # Recent errors
    echo ""
    echo "--- Error Summary ---"
    error_count=$(railway logs --json --limit 100 2>/dev/null | jq 'select(.level=="error")' | wc -l || echo "0")
    echo "Errors in last 100 logs: $error_count"

    if [ "$error_count" -gt 10 ]; then
      echo "⚠️  High error rate!"
    fi
  fi

  echo ""
  echo "Press Ctrl+C to exit"
  echo "Next refresh in $INTERVAL seconds..."

  sleep $INTERVAL
done
