# WordPress Security Scanner Skill

## Overview
Automated security scanning and cleanup for WordPress websites. Detects malicious scripts, redirects (judol/gambling), spam injections, and restores site health.

## What It Does
- **Scan** WordPress sites for malicious scripts, hidden redirects, spam SEO links
- **Detect** PHP backdoors, base64 encoded payloads, suspicious eval()
- **Clean** infected files and restore clean versions
- **Harden** wp-config.php, .htaccess, file permissions
- **Report** detailed findings with severity levels

## Architecture

```mermaid
flowchart TD
    subgraph Scan["🔍 WordPress Security Scanner"]
        A[Target URL Input] --> B[robots.txt Check]
        B --> C[WP Core Scan]
        C --> D[Plugin/Theme Scan]
        D --> E[Database Scan]
        E --> F[Redirect Detection]
        F --> G[Malicious Script Detection]
        G --> H[SEO Spam Check]
        H --> I[Report Generation]
    end
    
    subgraph Detection["🎯 Detection Engine"]
        I --> J[Base64 Decode]
        J --> K[eval() Pattern Match]
        K --> L[Redirect Loop Detect]
        L --> M[Hidden Content Find]
        M --> N[SEO Link Analysis]
    end
    
    subgraph Cleanup["🧹 Cleanup Actions"]
        N --> O[Quarantine Infected]
        O --> P[Restore Clean Backup]
        P --> Q[Remove Spam Links]
        Q --> R[Fix Permissions]
        R --> S[Harden Config]
    end
```

## Files
```
wordpress-security-scanner/
├── SKILL.md              # This file
├── scripts/
│   ├── scan.sh           # Main scanner script
│   ├── cleanup.sh        # Cleanup infected files
│   └── harden.sh         # Security hardening
└── README.md             # Quick reference
```

## Usage

### Quick Scan
```bash
bash skills/wordpress-security-scanner/scripts/scan.sh https://example.com
```

### Full Scan + Cleanup
```bash
bash skills/wordpress-security-scanner/scripts/scan.sh https://example.com --cleanup
```

### Hardening Only
```bash
bash skills/wordpress-security-scanner/scripts/harden.sh https://example.com
```

## Detection Patterns

| Threat Type | Patterns Detected |
|-------------|-------------------|
| Base64 Backdoor | `base64_decode(`, `gzinflate(base64_decode(` |
| eval() Injection | `eval($`, `eval(base64` |
| Hidden Redirects | `window.location`, `meta http-equiv="refresh"` |
| SEO Spam | `casino`, `slot`, `togel`, `judol` links |
| PHP Mailer | `mail(`, `mb_send_mail(` spam scripts |
| Suspicious Files | `.php.txt`, `.jpg.php`, `wp-xmlrpc.php` |

## Severity Levels
- 🔴 **CRITICAL**: Active backdoor, shell upload
- 🟠 **HIGH**: Malicious redirect, SEO spam injection
- 🟡 **MEDIUM**: Outdated plugin, weak permissions
- 🟢 **LOW**: Minor configuration issue

## Requirements
- Bash, curl, grep, awk
- WordPress site with read access
- Optional: wp-cli for deeper scans

## Skill Triggers
- "scan wordpress security"
- "cek keamanan wordpress"
- "bersihkan web wordpress"
- "wordpress malware scan"
