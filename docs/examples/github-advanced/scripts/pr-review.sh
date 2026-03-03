#!/bin/bash
# GitHub PR Auto-Review
# Usage: pr-review owner/repo [pr-number]

REPO="$1"
PR_NUMBER="$2"

if [ -z "$REPO" ]; then
    echo "Usage: pr-review owner/repo [pr-number]"
    echo "       pr-review owner/repo --all (review all open PRs)"
    exit 1
fi

# Review all open PRs
if [ "$PR_NUMBER" = "--all" ]; then
    echo "🔍 Reviewing all open PRs for $REPO..."
    gh pr list --repo "$REPO" --json number --jq '.[].number' | while read -r pr; do
        echo ""
        echo "═══════════════════════════════════════"
        "$0" "$REPO" "$pr"
    done
    exit 0
fi

# Get PR info
PR_DATA=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json number,title,author,state,mergeStateStatus,checksState,url 2>/dev/null)

if [ -z "$PR_DATA" ]; then
    echo "❌ PR #$PR_NUMBER not found in $REPO"
    exit 1
fi

# Parse JSON
PR_STATE=$(echo "$PR_DATA" | jq -r '.state')
CHECKS=$(echo "$PR_DATA" | jq -r '.checksState')
MERGE_STATE=$(echo "$PR_DATA" | jq -r '.mergeStateStatus')
TITLE=$(echo "$PR_DATA" | jq -r '.title')
AUTHOR=$(echo "$PR_DATA" | jq -r '.author.login')
URL=$(echo "$PR_DATA" | jq -r '.url')

echo "📋 PR #$PR_NUMBER: $TITLE"
echo "   Author: @$AUTHOR"
echo "   URL: $URL"
echo "   State: $PR_STATE"
echo "   Checks: $CHECKS"
echo "   Mergeable: $MERGE_STATE"

# Auto-merge if CI pass
if [ "$CHECKS" = "SUCCESS" ] && [ "$MERGE_STATE" = "CLEAN" ]; then
    echo "✅ All checks passed! Ready to merge."
    echo "   Run: gh pr merge $PR_NUMBER --repo $REPO --squash"
elif [ "$CHECKS" = "FAILURE" ]; then
    echo "❌ Checks failed."
    # Check if already commented
    COMMENTS=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json comments --jq '.comments | length')
    if [ "$COMMENTS" -eq 0 ]; then
        echo "   Commenting on PR..."
        gh pr comment "$PR_NUMBER" --repo "$REPO" --body "⚠️ CI checks failed. Please fix before merging." 2>/dev/null
    fi
elif [ "$CHECKS" = "PENDING" ]; then
    echo "⏳ Checks still running..."
else
    echo "⚠️ Merge conflicts or other issues."
fi
