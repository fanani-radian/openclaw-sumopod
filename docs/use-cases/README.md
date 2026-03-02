# 💡 Use Cases - Contoh Penggunaan

Kumpulan contoh penggunaan OpenClaw dari komunitas Sumopod.

---

## 📊 Gold Price Monitor with Fallback Chain

**By:** @fanani-radian  
**Use Case:** Track harga emas dengan multiple fallback methods

### Overview
Sistem cek harga emas yang robust dengan **4-layer fallback**. Kalau satu method gagal, otomatis pindah ke method berikutnya:

```
Priority 1: Scrapling (LogamMulia.com) ✅ Most reliable
Priority 2: Python (HargaEmas.com)
Priority 3: Curl (direct fetch)
Priority 4: Smart-search (fallback)
Priority 5: Playwright (last resort)
```

**Why multiple methods?**
- LogamMulia.com punya Cloudflare protection → perlu Scrapling
- HargaEmas.com bisa di-fetch biasa → Python/curl
- Kalau semua gagal → Smart-search sebagai backup

### Tools Used
- **Scrapling** - Bypass Cloudflare Turnstile
- **Python + BeautifulSoup** - HTML parsing
- **Curl** - Direct HTTP fetch
- **Smart-search skill** - Multi-provider search fallback
- **Redis** - Caching (5 min TTL)

### Key Script
```python
# scripts/fetch-gold-scrapling.py
from scrapling import StealthyFetcher

fetcher = StealthyFetcher()
page = fetcher.get('https://www.logammulia.com/id/harga-emas-hari-ini')
price = page.css('td:contains("1 gr")').text
```

```bash
# scripts/quick-gold.sh - Full fallback chain
fetch_scrapling() || fetch_python() || fetch_curl() || fetch_smartsearch() || fetch_playwright()
```

### Cron Schedule
```bash
# Check 4x daily (WITA)
0 7 * * *   /scripts/gold-price-monitor.sh   # 07:00 - Morning
0 8 * * *   /scripts/gold-price-monitor.sh   # 08:00 - Update
10 10 * * * /scripts/gold-price-monitor.sh   # 10:10 - Midday
0 18 * * *  /scripts/gold-price-monitor.sh   # 18:00 - Evening
```

### Output Format
```
📊 ANTAM GOLD PRICE - 02 Mar 2026
💰 IDR 3.135.000/gram
🟢 UP +IDR 50.000 (+1.62%)
🏦 Pegadaian: IDR 3.092.000/gr
📍 Source: LogamMulia.com (Scrapling)
```

### Files
- [fetch-gold-scrapling.py](./examples/gold-monitor/)
- [fetch-gold-python.py](./examples/gold-monitor/)
- [quick-gold.sh](./examples/gold-monitor/)

---

## 🔍 Smart Search Multi-Provider

**By:** @fanani-radian  
**Use Case:** Web search dengan auto-fallback antar provider

### Overview
Skill `smart-search` yang intelligently memilih provider berdasarkan availability dan rate limits. Kalau satu provider fail/down, otomatis switch ke provider lain.

```
Provider Priority:
1. Serper API (Google Search)    - Fastest, most accurate
2. Kimi Web Search               - Good fallback
3. GLM Web Search                - Alternative
4. Perplexity API                - Deep search
5. Tavily API                    - Research-focused
```

### Why Multi-Provider?
| Provider | Strengths | Use Case |
|----------|-----------|----------|
| **Serper** | Real-time Google results | News, current events |
| **Kimi** | Chinese + English sources | Asia-focused queries |
| **Perplexity** | Deep research, citations | Complex questions |
| **Tavily** | AI-optimized extraction | Research tasks |

### Key Config
```yaml
# skills/smart-search/config/providers.yaml
providers:
  serper:
    api_key: ${SERPER_API_KEY}
    priority: 1
    rate_limit: 100/day
    
  kimi:
    api_key: ${MOONSHOT_API_KEY}
    priority: 2
    rate_limit: 1000/day
    
  perplexity:
    api_key: ${PERPLEXITY_API_KEY}
    priority: 3
    rate_limit: 150/day
    
  tavily:
    api_key: ${TAVILY_API_KEY}
    priority: 4
    rate_limit: 1000/month

fallback_chain:
  - serper
  - kimi
  - glm
  - perplexity
  - tavily
```

### Usage
```bash
# Simple search
bash skills/smart-search/scripts/search.sh "harga emas hari ini"

# With provider preference
bash skills/smart-search/scripts/search.sh "berita terkini" --provider serper

# JSON output
bash skills/smart-search/scripts/search.sh "query" --json
```

### Response Format
```json
{
  "query": "harga emas hari ini",
  "provider": "serper",
  "results": [
    {
      "title": "Harga Emas Hari Ini",
      "url": "https://hargaemas.com",
      "snippet": "Harga emas Antam hari ini Rp 3.135.000/gram"
    }
  ],
  "fallback_used": false,
  "latency_ms": 850
}
```

### Cost Optimization
```yaml
# config/smart-search-budget.yaml
tier_1: [serper, kimi]        # Cheap, fast
  max_cost_per_query: $0.001

tier_2: [perplexity]          # Medium cost  
  max_cost_per_query: $0.005
  use_for: [complex_queries]

tier_3: [tavily]              # Higher cost
  max_cost_per_query: $0.01
  use_for: [research_tasks]
```

### Files
- [smart-search.sh](./examples/smart-search/)
- [provider-manager.py](./examples/smart-search/)
- [rate-limiter.js](./examples/smart-search/)

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
