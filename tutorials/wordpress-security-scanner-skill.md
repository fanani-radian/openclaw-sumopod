# 🔒 WordPress Security Scanner — Auto-Deteksi & Bersihkan Malware

![WordPress Security](https://img.shields.io/badge/WordPress-Security_Scanner-blue?style=for-the-badge)
![Bash](https://img.shields.io/badge/Bash-Script-green?style=for-the-badge)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange?style=for-the-badge)

> **Bahasa Indonesia & English** — Tutorial ini tersedia dalam dua bahasa untuk kemudahan pemahaman.

---

## 📌 Apa Ini?

Tool scanner otomatis buat WordPress yang:
- 🔍 **Deteksi** malware, backdoor, dan script jahat
- 🧹 **Bersihkan** file yang terinfeksi
- 🛡️ **Harden** konfigurasi keamanan
- 📊 **Report** temuan dengan severity level

Cocok buat kamu yang punya WordPress site dan suspect "kenapa ranking turun?" atau " ada redirect aneh ke situs lain?"

---

## 🎯 Kapan Butuh?

Waspadai gejala-gejala ini:

| Gejala | Kemungkinan Penyebab |
|--------|---------------------|
| Redirect ke situs judol/slot | 🔴 Malware injection |
| Ranking SEO turun drastis | 🟠 SEO spam injection |
| File unknown di uploads/ | 🟠 Backdoor upload |
| Login tidak bisa | 🟡 Brute force bot |
| Site jadi lambat | 🟡 Suspicious script |

---

## 🏗️ Architecture

```mermaid
flowchart LR
    subgraph Input["📥 Input"]
        A[WordPress URL]
    end
    
    subgraph Scan["🔍 Security Scanner"]
        B[robots.txt Check]
        C[Core Files Scan]
        D[Plugin Scan]
        E[Redirect Detection]
        F[Malicious Pattern Match]
        G[SEO Spam Check]
    end
    
    subgraph Output["📤 Output"]
        H[Security Report]
        I[Cleanup Actions]
        J[Hardening Steps]
    end
    
    A --> B --> C --> D --> E --> F --> G --> H
    H --> I
    H --> J
    
    style Input fill:#e3f2fd
    style Scan fill:#fff3e0
    style Output fill:#e8f5e9
```

---

## 🔧 Installation

```bash
# Clone ke workspace
git clone https://github.com/fanani-radian/openclaw-sumopod.git
cd openclaw-sumopod

# Atau copy langsung skillnya
cp -r skills/wordpress-security-scanner /root/.openclaw/workspace/skills/
chmod +x skills/wordpress-security-scanner/scripts/*.sh
```

---

## 📖 Cara Pakai

### 1️⃣ Basic Scan — Cek Malware

```bash
bash skills/wordpress-security-scanner/scripts/scan.sh https://yoursite.com
```

**Output contoh:**
```
═══════════════════════════════════════════
  WordPress Security Scanner v1.0
═══════════════════════════════════════════
Target: https://yoursite.com

[1/6] Checking robots.txt...
[2/6] Scanning WP core files...
  ✓ wp-config.php exists
  ✓ wp-login.php exists
[3/6] Checking for suspicious PHP files...
  ⚠️  Found: wp-content/uploads/.htaccess
[4/6] Detecting redirects...
[5/6] Checking for SEO spam...
  🟠 SEO SPAM: Found 'slot' on homepage
[6/6] Checking meta tags...

═══════════════════════════════════════════
  SCAN SUMMARY
═══════════════════════════════════════════
Malicious files: 0
Redirect issues: 0
SEO spam: 1

⚠️  SEO SPAM DETECTED!
Run with --cleanup to remove infected files
```

### 2️⃣ Full Scan + Auto Cleanup

```bash
bash skills/wordpress-security-scanner/scripts/scan.sh https://yoursite.com --cleanup
```

⚠️ **Warning:** Backup dulu sebelum cleanup!

### 3️⃣ Hardening Saja

```bash
bash skills/wordpress-security-scanner/scripts/harden.sh https://yoursite.com
```

---

## 🎨 Mermaid Diagram — Alur Deteksi

```mermaid
flowchart TD
    A[Start: Masukkan URL] --> B{robots.txt ada?}
    B -->|Yes| C[Parse disallowed paths]
    B -->|No| D[Skip robots check]
    
    C --> E[Scan WP Core Files]
    D --> E
    
    E --> F{Core files lengkap?}
    F -->|Yes| G[✓ Clean]
    F -->|No| H[⚠️ Missing files]
    
    G --> I[Check suspicious paths]
    H --> I
    
    I --> J{Find backdoor?}
    J -->|Yes| K[🔴 CRITICAL]
    J -->|No| L[✓ No backdoor]
    
    K --> M[Check redirects]
    L --> M
    
    M --> N{Redirect detected?}
    N -->|Yes| O[🔴 HIGH]
    N -->|No| P[✓ No redirect]
    
    O --> Q[Check SEO spam]
    P --> Q
    
    Q --> R{Spam keywords found?}
    R -->|Yes| S[🟠 MEDIUM]
    R -->|No| T[✓ Clean]
    
    S --> U[Generate Report]
    T --> U
    H --> U
    K --> U
    O --> U
    
    U --> V[📊 Severity Report]
    
    style K fill:#ffcdd2
    style O fill:#ffcdd2
    style S fill:#fff9c4
    style G fill:#c8e6c9
    style T fill:#c8e6c9
```

---

## 🛡️ Pattern Yang Dideteksi

### Malware/Backdoor Patterns

| Pattern | Severity | Keterangan |
|---------|----------|------------|
| `base64_decode(` | 🔴 CRITICAL | Base64 encoded payload |
| `eval($` | 🔴 CRITICAL | Dynamic code execution |
| `shell_exec` | 🔴 CRITICAL | Remote command execution |
| `gzinflate(base64_decode` | 🔴 CRITICAL | Compressed malware |
| `system(` | 🔴 CRITICAL | System command injection |

### Redirect Patterns

| Pattern | Severity | Keterangan |
|---------|----------|------------|
| `window.location` | 🔴 HIGH | JavaScript redirect |
| `meta http-equiv="refresh"` | 🔴 HIGH | Meta tag redirect |
| `.href = ` | 🟠 MEDIUM | Location change |
| `setTimeout.*location` | 🟠 MEDIUM | Delayed redirect |

### SEO Spam Keywords

```
casino, slot online, poker, domino99
togel, judol, gambling
situs gacor, bola88, s128
cmd368, mix parlay
```

---

## 📁 File Structure

```
wordpress-security-scanner/
├── SKILL.md              # Skill definition (OpenClaw)
├── README.md             # Quick reference
├── scripts/
│   ├── scan.sh           # Main scanner
│   ├── cleanup.sh        # Auto cleanup
│   └── harden.sh         # Security hardening
└── docs/
    └── DIAGRAM.md        # Architecture diagrams
```

---

## 🔄 Integration with OpenClaw

### Trigger Keywords
```
"scan wordpress"
"cek keamanan wordpress"
"bersihkan web wordpress"
"wordpress malware scan"
"scan wp security"
```

### Example Conversation

```
User: scan wordpress security untuk websitename.com
Radit: 🔍 Starting WordPress security scan...
       Target: websitename.com
       
       [1/6] robots.txt... ✓
       [2/6] Core files... ✓ wp-config.php, wp-login.php
       [3/6] Suspicious paths... ⚠️ Found backdoor!
       [4/6] Redirect detection... 🔴 DETECTED
       [5/6] SEO spam... 🟠 Found 'casino'
       [6/6] Meta tags... OK
       
       📊 SUMMARY:
       🔴 CRITICAL: 1 backdoor detected
       🔴 HIGH: Redirect injection found
       🟠 MEDIUM: SEO spam present
       
       ⚡ Mau cleanup sekarang?
```

---

## ⚠️ Warning & Best Practices

### Sebelum Scan
1. ✅ **Backup database** — `wp db export`
2. ✅ **Backup files** — `tar -czf backup.tar.gz wp-content/`
3. ✅ **Catat timestamp** — biar tau kapan infeksi terjadi

### Setelah Cleanup
1. ✅ **Update semua plugin & theme**
2. ✅ **Ganti semua password** (WP, DB, FTP)
3. ✅ **Install security plugin** (Wordfence, Sucuri)
4. ✅ **Monitor regularly** — weekly/monthly scan

---

## 📊 Sample Report

```
═══════════════════════════════════════════════════════════════
  WORDPRESS SECURITY SCAN REPORT
  Target: websitename.com
  Date: 2026-04-14 08:00 WITA
═══════════════════════════════════════════════════════════════

🔴 CRITICAL (1)
  └─ wp-content/uploads/2024/01/.htaccess
     └─ Malicious .htaccess redirect rules

🔴 HIGH (2)
  └─ wp-includes/js/jquery/jquery.min.php
     └─ Injected script tag
  └─ wp-content/themes/theme404/footer.php
     └─ Hidden iframe to external domain

🟠 MEDIUM (3)
  └─ wp-content/plugins/hello.php
     └─ Suspicious mail() function
  └─ wp-content/uploads/2024/03/
     └─ SEO spam links detected
  └─ wp-login.php
     └─ Brute force protection needed

🟢 CLEAN (15)
  └─ All core WordPress files verified
  └─ wp-config.php secure
  └─ No database injection detected

═══════════════════════════════════════════════════════════════
  RECOMMENDATIONS
═══════════════════════════════════════════════════════════════
1. Remove infected .htaccess immediately
2. Replace footer.php with clean version
3. Update WordPress to latest version
4. Install Wordfence Security plugin
5. Enable 2FA for admin login

SCORE: 45/100 ⚠️ NEEDS ATTENTION
```

---

## 🎓 Learn More

| Resource | Link |
|----------|------|
| WordPress Security | [wordfence.com](https://www.wordfence.com) |
| Sucuri Security | [sucuri.net](https://sucuri.net) |
| OWASP Top 10 | [owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten/) |
| WP CLI | [wp-cli.org](https://wp-cli.org) |

---

## 🙏 Credits

**Skill ini bagian dari OpenClaw Sumopod — Tutorial Hub komunitas Indonesia**

- 🧠 **Idea:** Ari Eko Prasethio Sumopod
- 🔧 **Built with:** OpenClaw + Bash
- 📝 **Contributing:** PRs welcome!

---

<div align="center">

![Star History](https://api.star-history.com/svg?repos=fanani-radian/openclaw-sumopod&type=Timeline)

**OpenClaw Sumopod** — Tutorial Hub for Indonesian Dev Community

</div>
