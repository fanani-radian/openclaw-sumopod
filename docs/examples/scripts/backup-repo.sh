#!/bin/bash
# GitHub Repo Backup
# Usage: backup-repo owner/repo [backup-dir]

REPO="$1"
BACKUP_DIR="${2:-$HOME/backups/github}"

if [ -z "$REPO" ]; then
    echo "Usage: backup-repo owner/repo [backup-dir]"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

REPO_NAME=$(basename "$REPO")
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${REPO_NAME}_${DATE}.bundle"

echo "📦 Backing up $REPO..."

# Clone bare repo
tmp_dir="/tmp/github_backup_$$"
if git clone --bare "https://github.com/$REPO.git" "$tmp_dir" 2>/dev/null; then
    cd "$tmp_dir" || exit 1
    
    # Create bundle
    git bundle create "$BACKUP_FILE" --all
    
    # Cleanup
    rm -rf "$tmp_dir"
    
    if [ -f "$BACKUP_FILE" ]; then
        echo "✅ Backup created: $BACKUP_FILE"
        echo "📊 Size: $(du -h "$BACKUP_FILE" | cut -f1)"
        
        # Cleanup old backups (keep last 10)
        cd "$BACKUP_DIR"
        ls -t "${REPO_NAME}"_*.bundle 2>/dev/null | tail -n +11 | xargs -r rm --
        echo "🧹 Old backups cleaned up (kept last 10)"
    else
        echo "❌ Failed to create bundle"
        exit 1
    fi
else
    echo "❌ Failed to clone $REPO"
    exit 1
fi
