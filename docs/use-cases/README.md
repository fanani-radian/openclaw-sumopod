# 💡 Use Cases - Contoh Penggunaan

Kumpulan contoh penggunaan OpenClaw dari komunitas Sumopod.

---

## 📧 Email Automation

**By:** @fanani-radian  
**Use Case:** Auto-process email masuk, classify, dan buat tasks

### Overview
Agent membaca Gmail setiap 5 menit, classify email (invoice, support, general), dan otomatis:
- Forward invoice ke finance
- Extract data ke Google Sheets
- Buat tasks di Google Tasks
- Draft reply dengan ghostwriter persona

### Tools Used
- Gmail (read/send)
- Google Drive
- Google Sheets
- Google Tasks

### Key Config
```yaml
# config/email-automation.yaml
scan_interval: 5m
classifiers:
  - invoice: ["invoice", "tagihan", "payment"]
  - support: ["help", "issue", "error"]
  - general: ["default"]
actions:
  invoice:
    - forward_to: finance@company.com
    - extract_to_sheets: true
    - upload_to_drive: true
```

### Files
- [email-processor.js](./examples/email-automation/)
- [invoice-extractor.py](./examples/email-automation/)

---

## 🏢 UNO Attendance Report

**By:** @fanani-radian  
**Use Case:** Daily attendance report otomatis

### Overview
Setiap weekday jam 8:15 AM, agent:
1. Fetch data absensi dari sistem UNO
2. Generate report (who's in, late, absent)
3. Kirim ke Telegram group

### Tools Used
- Internal UNO API
- Telegram Bot API
- Cron scheduler

### Key Script
```bash
# scripts/uno-attendance.sh
python3 uno-attendance.py $(date +%Y-%m-%d) | \
  jq -r '.report' | \
  telegram-send --format markdown
```

---

## 📊 Gold Price Monitor

**By:** @fanani-radian  
**Use Case:** Track harga emas real-time

### Overview
- Fetch harga Antam dari LogamMulia.com
- Cache dengan TTL 5 menit
- Alert kalau perubahan > 2%
- Auto-share ke WhatsApp/Telegram

### Tools Used
- Scrapling (bypass Cloudflare)
- Redis cache
- WhatsApp API
- Telegram Bot

### Key Config
```python
# config/gold-monitor.yaml
sources:
  - logammulia:
      url: "https://www.logammulia.com/id/harga-emas-hari-ini"
      method: "scrapling"
  - hargaemas:
      url: "https://hargaemas.com"
      method: "fetch"
cache_ttl: 300  # 5 minutes
alert_threshold: 0.02  # 2%
notifications:
  - whatsapp
  - telegram
```

---

## 🌅 Morning Briefing

**By:** @fanani-radian  
**Use Case:** Daily summary otomatis

### Overview
Setiap pagi jam 7 AM WITA, kirim briefing:
- 📧 Unread emails summary
- 📅 Calendar events hari ini
- 📋 Pending tasks
- 💰 Gold price
- 🖥️ Server health
- 🏢 UNO attendance (weekdays)

### Tools Used
- Gmail API
- Google Calendar
- Google Tasks
- Custom gold/attendance scripts

---

## 🔒 Security Monitoring

**By:** @fanani-radian  
**Use Case:** 24/7 server monitoring

### Overview
- Brute force detection (SSH failed logins)
- SSL certificate expiry check
- Service health monitoring (auto-restart if down)
- SSH login monitoring (alert new IPs)

### Tools Used
- fail2ban
- UFW firewall
- Systemd service checks
- Telegram alerts

### Key Scripts
```bash
# cron jobs
*/15 * * * * /scripts/brute-force-monitor.sh
*/5 * * * *  /scripts/service-health-check.sh
* * * * *    /scripts/ssh-login-monitor.sh
```

---

## 🤖 Multi-Agent Coordination

**By:** @fanani-radian  
**Use Case:** 4 agents dengan spesialisasi berbeda

### Overview
| Agent | Role | Tasks |
|-------|------|-------|
| **Radit** | Main | Orchestration, general tasks |
| **Raka** | Creative | Content, marketing, copywriting |
| **Rama** | Analytical | Data analysis, research |
| **Rafi** | Technical | Coding, infrastructure |

### Routing Logic
```yaml
# config/brother-routing.yaml
routes:
  creative: ["content", "marketing", "social media", "copy"]
  analytical: ["data", "research", "report", "analysis"]
  technical: ["code", "deploy", "server", "bug"]
  default: "radit"
```

---

## Share Your Use Case!

Punya use case menarik? [Tambahkan ke repo ini](../../issues/new?template=use-case.md) dengan format:

```markdown
## [Nama Use Case]
**By:** @username
**Use Case:** [Deskripsi singkat]

### Overview
[Penjelasan detail]

### Tools Used
- [tool1]
- [tool2]

### Key Config
[config atau code snippet]

### Files
- [link ke script/config]
```

---

*Last updated: March 2026*
