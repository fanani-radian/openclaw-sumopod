#!/bin/bash
# GitHub Issue Triage — Auto-label dan assign
# Usage: issue-triage owner/repo

REPO="$1"

if [ -z "$REPO" ]; then
    echo "Usage: issue-triage owner/repo"
    exit 1
fi

echo "🏷️  Triaging issues for $REPO..."

# Get open issues (no labels)
ISSUES=$(gh issue list --repo "$REPO" --state open --json number,title,body --limit 50)

if [ -z "$ISSUES" ] || [ "$ISSUES" = "[]" ]; then
    echo "✅ No open issues to triage"
    exit 0
fi

echo "$ISSUES" | jq -c '.[]' | while read -r issue; do
    NUMBER=$(echo "$issue" | jq -r '.number')
    TITLE=$(echo "$issue" | jq -r '.title' | tr '[:upper:]' '[:lower:]')
    BODY=$(echo "$issue" | jq -r '.body' | tr '[:upper:]' '[:lower:]')
    
    TEXT="$TITLE $BODY"
    LABELS=""
    
    # Auto-label based on keywords
    if echo "$TEXT" | grep -qiE "bug|error|crash|fail|broken|not working"; then
        LABELS="bug"
    elif echo "$TEXT" | grep -qiE "feature|request|enhancement|add|implement|support"; then
        LABELS="enhancement"
    elif echo "$TEXT" | grep -qiE "doc|documentation|readme|wiki|guide|tutorial"; then
        LABELS="documentation"
    elif echo "$TEXT" | grep -qiE "security|vuln|exploit|cve|xss|sql injection"; then
        LABELS="security"
    elif echo "$TEXT" | grep -qiE "performance|slow|speed|optimization|memory|cpu"; then
        LABELS="performance"
    elif echo "$TEXT" | grep -qiE "question|help|how to|what is|clarification"; then
        LABELS="question"
    fi
    
    # Apply labels
    if [ -n "$LABELS" ]; then
        echo "   Issue #$NUMBER: Adding label '$LABELS'"
        gh issue edit "$NUMBER" --repo "$REPO" --add-label "$LABELS" 2>/dev/null || true
    fi
done

echo "✅ Triage completed for $REPO"
