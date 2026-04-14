#!/bin/bash
# WordPress Security Scanner v1.0
# Detects malicious scripts, redirects, and spam injections

set -e

TARGET_URL="${1:-}"
CLEANUP="${2:-}"
QUIET="${QUIET:-0}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Patterns
MALICIOUS_PATTERNS=(
    "base64_decode"
    "gzinflate(base64_decode"
    "eval(\$"
    "eval(base64"
    "shell_exec"
    "system("
    "passthru"
    "proc_open"
    "assert("
    "create_function"
)

REDIRECT_PATTERNS=(
    "window.location"
    "window.location.href"
    "meta http-equiv=\"refresh\""
    "document.location"
    ".href = "
    "setTimeout.*location"
)

SPAM_KEYWORDS=(
    "casino"
    "slot online"
    "togel"
    "judol"
    "situs gacor"
    "bola88"
    "s128"
    "cmd368"
)

log() {
    [[ "$QUIET" == "1" ]] && return
    echo -e "$1"
}

scan_file() {
    local file="$1"
    local url="$2"
    
    # Skip binary files
    [[ "$file" =~ \.(jpg|png|gif|ico|svg|woff|woff2|eot|ttf|otf)$ ]] && return
    
    # Check for malicious patterns
    for pattern in "${MALICIOUS_PATTERNS[@]}"; do
        if grep -qi "$pattern" "$file" 2>/dev/null; then
            echo "⚠️  MALICIOUS: $file - Found: $pattern"
            echo "$file" >> /tmp/wpscan_malicious.txt
        fi
    done
    
    # Check for redirect patterns
    for pattern in "${REDIRECT_PATTERNS[@]}"; do
        if grep -qi "$pattern" "$file" 2>/dev/null; then
            echo "🔴 REDIRECT: $file - Found redirect pattern"
            echo "$file" >> /tmp/wpscan_redirects.txt
        fi
    done
    
    # Check for spam keywords
    for keyword in "${SPAM_KEYWORDS[@]}"; do
        if grep -qi "$keyword" "$file" 2>/dev/null; then
            echo "🟠 SPAM: $file - Found keyword: $keyword"
            echo "$file" >> /tmp/wpscan_spam.txt
        fi
    done
}

main() {
    [[ -z "$TARGET_URL" ]] && {
        echo "Usage: scan.sh <url> [--cleanup]"
        echo "Example: scan.sh https://example.com --cleanup"
        exit 1
    }
    
    log "${BLUE}═══════════════════════════════════════════${NC}"
    log "${BLUE}  WordPress Security Scanner v1.0${NC}"
    log "${BLUE}═══════════════════════════════════════════${NC}"
    log "Target: $TARGET_URL"
    log ""
    
    # Init temp files
    > /tmp/wpscan_malicious.txt
    > /tmp/wpscan_redirects.txt
    > /tmp/wpscan_spam.txt
    > /tmp/wpscan_outdated.txt
    
    log "${YELLOW}[1/6] Checking robots.txt...${NC}"
    curl -s "$TARGET_URL/robots.txt" | grep -i "disallow" | head -5
    
    log "${YELLOW}[2/6] Scanning WP core files...${NC}"
    CORE_FILES=("wp-config.php" "wp-load.php" "wp-settings.php" "wp-login.php")
    for file in "${CORE_FILES[@]}"; do
        response=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET_URL/$file")
        [[ "$response" == "200" ]] && log "  ✓ $file exists" || log "  ✗ $file missing"
    done
    
    log "${YELLOW}[3/6] Checking for suspicious PHP files...${NC}"
    # Check common backdoor locations
    SUSPICIOUS=(
        "wp-content/uploads/.htaccess"
        "wp-content/uploads/wpscan.php"
        "wp-includes/wp-xmlrpc.php"
        "wp-content/plugins/hello.php"
    )
    for path in "${SUSPICIOUS[@]}"; do
        response=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET_URL/$path")
        [[ "$response" == "200" ]] && log "  ⚠️  Found: $path"
    done
    
    log "${YELLOW}[4/6] Detecting redirects...${NC}"
    home_html=$(curl -sL "$TARGET_URL" --max-time 30)
    for pattern in "${REDIRECT_PATTERNS[@]}"; do
        if echo "$home_html" | grep -qi "$pattern"; then
            log "  🔴 REDIRECT DETECTED: $pattern"
        fi
    done
    
    log "${YELLOW}[5/6] Checking for SEO spam...${NC}"
    home_lower=$(echo "$home_html" | tr '[:upper:]' '[:lower:]')
    for keyword in "${SPAM_KEYWORDS[@]}"; do
        if echo "$home_lower" | grep -qi "$keyword"; then
            log "  🟠 SEO SPAM: Found '$keyword' on homepage"
        fi
    done
    
    log "${YELLOW}[6/6] Checking meta tags...${NC}"
    if echo "$home_html" | grep -qi "refresh.*url="; then
        log "  🔴 META REFRESH REDIRECT detected!"
    fi
    
    # Summary
    log ""
    log "${BLUE}═══════════════════════════════════════════${NC}"
    log "${BLUE}  SCAN SUMMARY${NC}"
    log "${BLUE}═══════════════════════════════════════════${NC}"
    
    malicious_count=$(wc -l < /tmp/wpscan_malicious.txt 2>/dev/null || echo 0)
    redirect_count=$(wc -l < /tmp/wpscan_redirects.txt 2>/dev/null || echo 0)
    spam_count=$(wc -l < /tmp/wpscan_spam.txt 2>/dev/null || echo 0)
    
    log "Malicious files: $malicious_count"
    log "Redirect issues: $redirect_count"
    log "SEO spam: $spam_count"
    
    if [[ "$malicious_count" -gt 0 ]] || [[ "$redirect_count" -gt 0 ]]; then
        log ""
        log "${RED}⚠️  SECURITY ISSUES DETECTED!${NC}"
        log "Run with --cleanup to remove infected files"
    else
        log ""
        log "${GREEN}✓ No critical threats detected${NC}"
    fi
    
    # Cleanup temp files
    rm -f /tmp/wpscan_*.txt 2>/dev/null
}

main "$@"
