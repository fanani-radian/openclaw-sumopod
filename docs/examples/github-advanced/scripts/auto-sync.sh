#!/bin/bash
# GitHub Auto-Sync — Pull & Push otomatis
# Usage: auto-sync [repo-path]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/github-helpers.sh"

REPO_PATH="${1:-$PWD}"
LOG_FILE="${GITHUB_LOG:-/var/log/github-sync.log}"

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

# Detect default branch
DEFAULT_BRANCH=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}')
[ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH="main"

# Pull from remote
log "Pulling from origin/$DEFAULT_BRANCH..."
if git pull --rebase origin "$DEFAULT_BRANCH" 2>/dev/null; then
    log "Pull successful"
else
    log "WARNING: Pull failed, may have conflicts"
fi

# Restore stashed changes
if [ "$STASHED" -eq 1 ]; then
    log "Restoring stashed changes..."
    git stash pop || log "WARNING: Failed to pop stash"
    
    # Add, commit, push
    git add -A
    if git commit -m "auto: sync $(date '+%Y-%m-%d %H:%M')" 2>/dev/null; then
        log "Changes committed"
    fi
    
    if git push origin HEAD 2>/dev/null; then
        log "Push successful"
    else
        log "ERROR: Push failed"
    fi
else
    # Just push if there are commits to push
    if [ -n "$(git log origin/$DEFAULT_BRANCH..HEAD 2>/dev/null)" ]; then
        log "Pushing commits..."
        git push origin HEAD
        log "Push successful"
    else
        log "Nothing to push"
    fi
fi

log "Sync completed for: $REPO_NAME"
