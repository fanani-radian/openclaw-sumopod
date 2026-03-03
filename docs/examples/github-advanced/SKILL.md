# GitHub Advanced Automation

Advanced GitHub automation skill untuk OpenClaw — auto-sync, PR review, issue triage, release management, dan backup.

---

## 🚀 Features

| Feature | Deskripsi | Trigger |
|---------|-----------|---------|
| **Auto-Sync** | Auto pull/push tiap 15 menit | Cron / Manual |
| **PR Review** | Auto-comment, merge kalau CI pass | PR opened/updated |
| **Issue Triage** | Auto-label, assign, close stale | Issue opened |
| **Release** | Auto-generate release notes | Tag pushed |
| **Backup** | Auto-archive repo ke zip/cloud | Schedule |
| **Security Scan** | Check secrets, vulnerabilities | Push / Schedule |

---

## 📋 Prerequisites

### 1. Install GitHub CLI (gh)

```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Login
git auth login
```

### 2. Setup GitHub Token

```bash
# Buat token: https://github.com/settings/tokens
# Scopes needed: repo, workflow, admin:org

# Save ke environment
echo "GITHUB_TOKEN=ghp_xxxxxxxx" >> ~/.openclaw/workspace/.env
```

---

## 🔄 Workflow 1: Auto-Sync

Auto pull dari remote dan push local changes.

### Script: `scripts/auto-sync.sh`

```bash
#!/bin/bash
# GitHub Auto-Sync — Pull & Push otomatis
# Usage: github-sync [repo-path]

REPO_PATH="${1:-$PWD}"
LOG_FILE="/var/log/github-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$REPO_PATH" || exit 1

# Check if git repo
if [ ! -d ".git" ]; then
    log "ERROR: Not a git repository: $REPO_PATH"
    exit 1
fi

REPO_NAME=$(basename "$REPO_PATH")
log "Starting sync for: $REPO_NAME"

# Stash local changes (if any)
if [ -n "$(git status --porcelain)" ]; then
    log "Local changes detected, stashing..."
    git stash push -m "auto-sync-$(date +%s)"
    STASHED=1
else
    STASHED=0
fi

# Pull from remote
log "Pulling from remote..."
if git pull --rebase origin main 2>/dev/null || git pull --rebase origin master 2>/dev/null; then
    log "Pull successful"
else
    log "WARNING: Pull failed, may have conflicts"
fi

# Restore stashed changes
if [ "$STASHED" -eq 1 ]; then
    log "Restoring stashed changes..."
    git stash pop
    
    # Add, commit, push
    git add -A
    git commit -m "auto: sync $(date '+%Y-%m-%d %H:%M')" || true
    
    if git push origin HEAD 2>/dev/null; then
        log "Push successful"
    else
        log "ERROR: Push failed"
    fi
else
    # Just push if there are commits to push
    if [ -n "$(git log origin/main..HEAD 2>/dev/null || git log origin/master..HEAD 2>/dev/null)" ]; then
        log "Pushing commits..."
        git push origin HEAD
        log "Push successful"
    else
        log "Nothing to push"
    fi
fi

log "Sync completed for: $REPO_NAME"
```

### Usage

```bash
# Sync current repo
github-sync

# Sync specific repo
github-sync /path/to/repo

# Add to cron (every 15 min)
echo "*/15 * * * * /root/.openclaw/workspace/skills/github-advanced/scripts/auto-sync.sh /path/to/repo >> /var/log/cron-sync.log 2>&1" | crontab -
```

---

## 🔍 Workflow 2: PR Review Automation

Auto-review PRs, comment, dan merge kalau CI pass.

### Script: `scripts/pr-review.sh`

```bash
#!/bin/bash
# GitHub PR Auto-Review
# Usage: github-pr-review owner/repo [pr-number]

REPO="$1"
PR_NUMBER="$2"

if [ -z "$REPO" ]; then
    echo "Usage: github-pr-review owner/repo [pr-number]"
    exit 1
fi

# Get PR info
PR_DATA=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json number,title,author,state,mergeStateStatus,checksState 2>/dev/null)

if [ -z "$PR_DATA" ]; then
    echo "❌ PR #$PR_NUMBER not found in $REPO"
    exit 1
fi

# Parse JSON
PR_STATE=$(echo "$PR_DATA" | jq -r '.state')
CHECKS=$(echo "$PR_DATA" | jq -r '.checksState')
MERGE_STATE=$(echo "$PR_DATA" | jq -r '.mergeStateStatus')

echo "📋 PR #$PR_NUMBER Status:"
echo "   State: $PR_STATE"
echo "   Checks: $CHECKS"
echo "   Mergeable: $MERGE_STATE"

# Auto-merge if CI pass
if [ "$CHECKS" = "SUCCESS" ] && [ "$MERGE_STATE" = "CLEAN" ]; then
    echo "✅ All checks passed! Auto-merging..."
    gh pr merge "$PR_NUMBER" --repo "$REPO" --squash --auto
    echo "✅ PR merged successfully"
elif [ "$CHECKS" = "FAILURE" ]; then
    echo "❌ Checks failed. Commenting..."
    gh pr comment "$PR_NUMBER" --repo "$REPO" --body "⚠️ CI checks failed. Please fix before merging."
else
    echo "⏳ Checks pending or merge conflicts. Waiting..."
fi
```

### Auto-Review All Open PRs

```bash
#!/bin/bash
# Review all open PRs
# Usage: github-review-all owner/repo

REPO="$1"

gh pr list --repo "$REPO" --json number --jq '.[].number' | while read -r pr; do
    echo "Reviewing PR #$pr..."
    github-pr-review "$REPO" "$pr"
done
```

---

## 🏷️ Workflow 3: Issue Triage

Auto-label dan assign issues berdasarkan keyword.

### Script: `scripts/issue-triage.sh`

```bash
#!/bin/bash
# GitHub Issue Triage — Auto-label dan assign
# Usage: github-triage owner/repo

REPO="$1"

if [ -z "$REPO" ]; then
    echo "Usage: github-triage owner/repo"
    exit 1
fi

# Get open issues (no labels)
gh issue list --repo "$REPO" --json number,title,body --search "no:label" | jq -c '.[]' | while read -r issue; do
    NUMBER=$(echo "$issue" | jq -r '.number')
    TITLE=$(echo "$issue" | jq -r '.title')
    BODY=$(echo "$issue" | jq -r '.body')
    
    LABELS=""
    ASSIGNEE=""
    
    # Auto-label based on keywords
    if echo "$TITLE $BODY" | grep -qiE "bug|error|crash|fail"; then
        LABELS="bug"
    elif echo "$TITLE $BODY" | grep -qiE "feature|request|add|implement"; then
        LABELS="enhancement"
    elif echo "$TITLE $BODY" | grep -qiE "doc|documentation|readme"; then
        LABELS="documentation"
    elif echo "$TITLE $BODY" | grep -qiE "security|vuln|exploit|cve"; then
        LABELS="security"
        ASSIGNEE="@admin"  # Auto-assign ke admin untuk security
    fi
    
    # Apply labels
    if [ -n "$LABELS" ]; then
        echo "🏷️  Issue #$NUMBER: Adding label '$LABELS'"
        gh issue edit "$NUMBER" --repo "$REPO" --add-label "$LABELS"
    fi
    
    # Assign if security
    if [ -n "$ASSIGNEE" ]; then
        echo "👤 Issue #$NUMBER: Assigning to $ASSIGNEE"
        gh issue edit "$NUMBER" --repo "$REPO" --add-assignee "$ASSIGNEE"
    fi
done

echo "✅ Triage completed for $REPO"
```

### Close Stale Issues

```bash
#!/bin/bash
# Close stale issues (no activity 30 days)
# Usage: github-close-stale owner/repo [days]

REPO="$1"
DAYS="${2:-30}"

gh issue list --repo "$REPO" --state open --search "updated:<$(date -d "$DAYS days ago" +%Y-%m-%d)" --json number | \
    jq -r '.[].number' | while read -r issue; do
    echo "Closing stale issue #$issue..."
    gh issue close "$issue" --repo "$REPO" --comment "🤖 Auto-closed due to inactivity (${DAYS} days). Please reopen if still relevant."
done
```

---

## 🏷️ Workflow 4: Release Automation

Auto-generate release notes dari commits.

### Script: `scripts/release.sh`

```bash
#!/bin/bash
# GitHub Release Automation
# Usage: github-release owner/repo tag [title]

REPO="$1"
TAG="$2"
TITLE="${3:-Release $TAG}"

if [ -z "$REPO" ] || [ -z "$TAG" ]; then
    echo "Usage: github-release owner/repo tag [title]"
    exit 1
fi

# Get commits since last tag
LAST_TAG=$(gh release view --repo "$REPO" --json tagName --jq '.tagName' 2>/dev/null || echo "")

if [ -n "$LAST_TAG" ]; then
    COMMITS=$(git log "$LAST_TAG..HEAD" --pretty=format:"- %s (%h)" 2>/dev/null || echo "")
else
    COMMITS=$(git log --pretty=format:"- %s (%h)" -20 2>/dev/null || echo "")
fi

# Categorize commits
FEATURES=$(echo "$COMMITS" | grep -iE "^.*(feat|feature|add):" || echo "")
FIXES=$(echo "$COMMITS" | grep -iE "^.*(fix|bug|hotfix):" || echo "")
DOCS=$(echo "$COMMITS" | grep -iE "^.*(doc|docs):" || echo "")
OTHER=$(echo "$COMMITS" | grep -viE "^.*(feat|feature|add|fix|bug|hotfix|doc|docs):" || echo "")

# Build release notes
NOTES="## What's New

"

if [ -n "$FEATURES" ]; then
    NOTES="${NOTES}### ✨ Features
$FEATURES

"
fi

if [ -n "$FIXES" ]; then
    NOTES="${NOTES}### 🐛 Bug Fixes
$FIXES

"
fi

if [ -n "$DOCS" ]; then
    NOTES="${NOTES}### 📚 Documentation
$DOCS

"
fi

if [ -n "$OTHER" ]; then
    NOTES="${NOTES}### 📝 Other Changes
$OTHER

"
fi

NOTES="${NOTES}---
🤖 Auto-generated by OpenClaw"

# Create release
echo "Creating release $TAG..."
gh release create "$TAG" \
    --repo "$REPO" \
    --title "$TITLE" \
    --notes "$NOTES"

echo "✅ Release $TAG created!"
```

---

## 💾 Workflow 5: Backup Automation

Auto-archive repo ke zip atau cloud storage.

### Script: `scripts/backup.sh`

```bash
#!/bin/bash
# GitHub Repo Backup
# Usage: github-backup owner/repo [backup-dir]

REPO="$1"
BACKUP_DIR="${2:-$HOME/backups/github}"

if [ -z "$REPO" ]; then
    echo "Usage: github-backup owner/repo [backup-dir]"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

REPO_NAME=$(basename "$REPO")
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${REPO_NAME}_${DATE}.zip"

echo "📦 Backing up $REPO..."

# Clone bare repo and zip
git clone --bare "https://github.com/$REPO.git" "/tmp/backup_${REPO_NAME}" 2>/dev/null

if [ -d "/tmp/backup_${REPO_NAME}" ]; then
    cd "/tmp/backup_${REPO_NAME}"
    git bundle create "$BACKUP_FILE" --all
    rm -rf "/tmp/backup_${REPO_NAME}"
    
    echo "✅ Backup created: $BACKUP_FILE"
    echo "📊 Size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "❌ Failed to clone $REPO"
    exit 1
fi

# Cleanup old backups (keep last 10)
cd "$BACKUP_DIR"
ls -t "${REPO_NAME}"_*.zip 2>/dev/null | tail -n +11 | xargs -r rm --

echo "🧹 Old backups cleaned up"
```

### Backup All Repos

```bash
#!/bin/bash
# Backup all repos for a user/org
# Usage: github-backup-all username [backup-dir]

USER="$1"
BACKUP_DIR="${2:-$HOME/backups/github}"

gh repo list "$USER" --json nameWithOwner --jq '.[].nameWithOwner' | while read -r repo; do
    github-backup "$repo" "$BACKUP_DIR"
done
```

---

## 🔒 Workflow 6: Security Scan

Check secrets dan vulnerabilities.

### Script: `scripts/security-scan.sh`

```bash
#!/bin/bash
# GitHub Security Scan
# Usage: github-security-scan owner/repo

REPO="$1"

if [ -z "$REPO" ]; then
    echo "Usage: github-security-scan owner/repo"
    exit 1
fi

echo "🔒 Scanning $REPO for security issues..."

# Check for secret scanning alerts
echo "📋 Secret Scanning Alerts:"
gh api "repos/$REPO/secret-scanning/alerts" --jq '.[] | "  - \(.secret_type): \(.location.path)"' 2>/dev/null || echo "  No alerts or not enabled"

# Check for dependabot alerts
echo "📋 Dependency Vulnerabilities:"
gh api "repos/$REPO/dependabot/alerts" --jq '.[] | select(.state == "open") | "  - \(.security_advisory.summary) (Severity: \(.security_advisory.severity))"' 2>/dev/null || echo "  No open alerts"

# Check code scanning (if enabled)
echo "📋 Code Scanning Alerts:"
gh api "repos/$REPO/code-scanning/alerts" --jq '.[] | select(.state == "open") | "  - \(.rule.description) (Severity: \(.rule.severity))"' 2>/dev/null || echo "  No alerts or not enabled"

echo "✅ Security scan completed"
```

---

## 🤖 OpenClaw Integration

### Tambah ke HEARTBEAT.md

```markdown
## GitHub Automation

- [ ] Auto-sync repos (every 15 min)
- [ ] Review open PRs (every hour)
- [ ] Triage issues (every 6 hours)
- [ ] Security scan (daily)
- [ ] Backup repos (weekly)
```

### Commands untuk Telegram/Chat

```
/github sync repo-name
/github pr-review owner/repo
/github triage owner/repo
/github release owner/repo v1.0.0
/github backup owner/repo
/github security-scan owner/repo
```

---

## 📊 Cost Analysis

| Workflow | Frequency | Cost |
|----------|-----------|------|
| Auto-sync | Every 15 min | FREE |
| PR review | On PR event | FREE |
| Issue triage | Every 6 hours | FREE |
| Release | On demand | FREE |
| Backup | Weekly | FREE (storage) |
| Security scan | Daily | FREE |

**Total: FREE!** (kecuali storage backup)

---

## 🔗 API Reference

- GitHub CLI: https://cli.github.com/manual
- GitHub API: https://docs.github.com/en/rest
- gh extension: https://cli.github.com/manual/gh_extension

---

*Skill by: Sumopod Community*
