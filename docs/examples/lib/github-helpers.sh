#!/bin/bash
# GitHub Advanced Helpers
# Common functions for GitHub automation

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if gh CLI is installed
check_gh_cli() {
    if ! command -v gh > /dev/null 2>&1; then
        log_error "GitHub CLI (gh) not installed"
        echo "Install: https://cli.github.com"
        exit 1
    fi
    
    if ! gh auth status > /dev/null 2>&1; then
        log_error "Not authenticated with GitHub"
        echo "Run: gh auth login"
        exit 1
    fi
}

# Get repository info
get_repo_info() {
    local repo="$1"
    gh api "repos/$repo" --jq '{name: .name, owner: .owner.login, private: .private, default_branch: .default_branch}' 2>/dev/null
}

# Check if user has write access
check_write_access() {
    local repo="$1"
    gh api "repos/$repo" --jq '.permissions.push' 2>/dev/null | grep -q "true"
}

# Send notification (Telegram/Discord)
send_notification() {
    local message="$1"
    local channel="${2:-telegram}"
    
    # Add your notification logic here
    # Example: Telegram bot
    # curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    #     -d "chat_id=$TELEGRAM_CHAT_ID" \
    #     -d "text=$message"
    
    echo "$message"
}

# Format size (bytes to human readable)
format_size() {
    local size="$1"
    local units=("B" "KB" "MB" "GB")
    local unit_index=0
    
    while [ "$size" -ge 1024 ] && [ "$unit_index" -lt 3 ]; do
        size=$((size / 1024))
        unit_index=$((unit_index + 1))
    done
    
    echo "${size}${units[$unit_index]}"
}

# Validate repo format (owner/repo)
validate_repo() {
    local repo="$1"
    if [[ ! "$repo" =~ ^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$ ]]; then
        log_error "Invalid repo format: $repo"
        echo "Expected: owner/repo"
        return 1
    fi
    return 0
}
