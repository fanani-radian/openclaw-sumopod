#!/bin/bash
# GitHub Security Scan
# Usage: security-scan owner/repo

REPO="$1"

if [ -z "$REPO" ]; then
    echo "Usage: security-scan owner/repo"
    exit 1
fi

echo "🔒 Security Scan for $REPO"
echo "═══════════════════════════════════════"

# Check for secret scanning alerts
echo ""
echo "📋 Secret Scanning Alerts:"
SECRETS=$(gh api "repos/$REPO/secret-scanning/alerts" --jq '.[] | "  ⚠️  \(.secret_type): \(.location.path)"' 2>/dev/null)
if [ -n "$SECRETS" ]; then
    echo "$SECRETS"
else
    echo "  ✅ No secret alerts (or not enabled)"
fi

# Check for dependabot alerts
echo ""
echo "📋 Dependency Vulnerabilities:"
DEPS=$(gh api "repos/$REPO/dependabot/alerts" --jq '.[] | select(.state == "open") | "  ⚠️  \(.security_advisory.summary) (\(.security_advisory.severity))"' 2>/dev/null)
if [ -n "$DEPS" ]; then
    echo "$DEPS"
else
    echo "  ✅ No open dependency alerts"
fi

# Check code scanning (if enabled)
echo ""
echo "📋 Code Scanning Alerts:"
CODE=$(gh api "repos/$REPO/code-scanning/alerts" --jq '.[] | select(.state == "open") | "  ⚠️  \(.rule.description) (\(.rule.severity))"' 2>/dev/null)
if [ -n "$CODE" ]; then
    echo "$CODE"
else
    echo "  ✅ No code scanning alerts (or not enabled)"
fi

# Check branch protection
echo ""
echo "📋 Branch Protection:"
DEFAULT_BRANCH=$(gh api "repos/$REPO" --jq '.default_branch' 2>/dev/null)
PROTECTION=$(gh api "repos/$REPO/branches/$DEFAULT_BRANCH/protection" 2>/dev/null)
if [ -n "$PROTECTION" ]; then
    echo "  ✅ Branch protection enabled on $DEFAULT_BRANCH"
else
    echo "  ⚠️  No branch protection on $DEFAULT_BRANCH"
fi

echo ""
echo "✅ Security scan completed"
