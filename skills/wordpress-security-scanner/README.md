# WordPress Security Scanner - Quick Reference

## Installation
```bash
# Clone skill
cp -r wordpress-security-scanner/ /root/.openclaw/workspace/skills/
chmod +x wordpress-security-scanner/scripts/*.sh
```

## Quick Usage
```bash
# Basic scan
bash skills/wordpress-security-scanner/scripts/scan.sh https://yoursite.com

# Full scan with cleanup
bash skills/wordpress-security-scanner/scripts/scan.sh https://yoursite.com --cleanup

# Hardening only
bash skills/wordpress-security-scanner/scripts/harden.sh https://yoursite.com
```

## Detection Capabilities
| Threat | Patterns |
|--------|----------|
| Backdoors | `base64_decode`, `eval()`, `shell_exec` |
| Redirects | `window.location`, `meta refresh` |
| SEO Spam | `casino`, `slot`, `togel`, `judol` |

## Requirements
- curl, bash, grep, awk
- Optional: wp-cli for deep scans
