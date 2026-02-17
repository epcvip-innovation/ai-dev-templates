#!/bin/bash
# deploy.sh - Complete deployment workflow with verification
#
# Usage: ./deploy.sh
#
# This script:
# 1. Runs tests
# 2. Commits changes
# 3. Pushes to trigger Railway deployment
# 4. Monitors deployment
# 5. Verifies health

set -e  # Exit on error

# Configuration
PROJECT_URL="${PROJECT_URL:-https://your-app-production.up.railway.app}"
TIMEOUT=180  # 3 minutes

echo "=== Railway Deployment Script ==="
echo "Project URL: $PROJECT_URL"
echo ""

# 1. Run tests
echo "▶ Running tests..."
if command -v pytest &> /dev/null; then
  pytest tests/ -v || { echo "❌ Tests failed! Aborting."; exit 1; }
else
  echo "⚠️  pytest not found, skipping tests"
fi

# 2. Check for changes
echo ""
echo "▶ Checking for changes..."
if [[ -z $(git status -s) ]]; then
  echo "No changes to commit."
  exit 0
fi

# 3. Commit changes
echo ""
echo "▶ Committing changes..."
git status -s
read -p "Commit message: " msg
[[ -z "$msg" ]] && echo "❌ Commit message required" && exit 1

git add .
git commit -m "$msg"

# 4. Push to trigger deployment
echo ""
echo "▶ Pushing to GitHub..."
git push origin main

# 5. Monitor deployment
echo ""
echo "▶ Monitoring deployment (Ctrl+C to skip)..."
railway logs --follow &
LOG_PID=$!

# 6. Wait for deployment
echo ""
echo "▶ Waiting for deployment to complete..."
sleep $TIMEOUT

# Stop log monitoring
kill $LOG_PID 2>/dev/null || true
wait $LOG_PID 2>/dev/null || true

# 7. Verify health
echo ""
echo "▶ Verifying deployment..."

if ! health_response=$(curl -s -f "$PROJECT_URL/health" 2>&1); then
  echo "❌ Health check failed to connect"
  echo "Response: $health_response"
  exit 1
fi

health=$(echo "$health_response" | jq -r '.status // "unknown"' 2>/dev/null || echo "unknown")

if [ "$health" = "healthy" ]; then
  echo "✅ Deployment successful!"
  echo ""
  echo "Production URL: $PROJECT_URL"
  exit 0
else
  echo "❌ Deployment failed! Health check returned: $health"
  echo "Response: $health_response"
  echo ""
  echo "Check logs: railway logs --limit 100"
  exit 1
fi
