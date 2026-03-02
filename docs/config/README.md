# ⚙️ Config

Kumpulan konfigurasi dan templates untuk OpenClaw.

---

## 📁 Directory Structure

```
config/
├── openclaw/              # Core OpenClaw config
│   ├── openclaw.yaml
│   └── cron-jobs.json
├── model-tiers.yaml       # Model routing
├── brother-routing.yaml   # Multi-agent routing
├── crontab-automation.txt # System cron jobs
└── examples/              # Community configs
    ├── email-automation/
    ├── gold-monitor/
    └── security-monitoring/
```

---

## 🎯 Core Configs

### model-tiers.yaml
```yaml
# Routing berdasarkan task complexity
tiers:
  background:
    models: [ollama/llama3.1, ollama/phi3]
    cost: 0
    use_for:
      - heartbeat
      - simple_fetch
      - log_parsing

  low:
    models: [kimi-coding/k2p5, deepseek-v3]
    cost: low
    use_for:
      - web_search
      - summarize
      - format_data

  medium:
    models: [kimi-k2.5, minimax-m2.5]
    cost: medium
    use_for:
      - analysis
      - coding
      - multi_step_tasks

  heavy:
    models: [claude-opus-4.6, gemini-3-pro]
    cost: high
    use_for:
      - architecture_design
      - complex_debugging
      - critical_decisions

rules:
  - always_start_with: low
  - escalate_on_failure: true
  - report_cost_before_heavy: true
```

### brother-routing.yaml
```yaml
# Multi-agent coordination
agents:
  radit:
    role: orchestrator
    handles: [general, coordination, default]
    priority: 1

  raka:
    role: creative
    handles:
      - content_creation
      - social_media
      - copywriting
      - branding
      - marketing
    keywords: [content, marketing, brand, copy, creative]

  rama:
    role: analytical
    handles:
      - data_analysis
      - research
      - reports
      - forecasting
    keywords: [data, analysis, research, report, forecast]

  rafi:
    role: technical
    handles:
      - coding
      - infrastructure
      - debugging
      - deployment
    keywords: [code, server, deploy, bug, technical]

routing_rules:
  - check_keywords_first: true
  - parallel_if_multiple_domains: true
  - default_to_radit: true
```

---

## ⏰ Cron Templates

### crontab-automation.txt
```bash
# OpenClaw Automation Cron Jobs
# Install: crontab crontab-automation.txt

# Git auto-sync (every 15 min)
*/15 * * * * cd /root/.openclaw/workspace && git pull && git push 2>/dev/null

# Morning briefing (07:00 WITA = 23:00 UTC)
0 23 * * * /root/.openclaw/workspace-radit/skills/morning-briefing/scripts/generate.sh --send

# Gold price check (08:00, 10:10, 18:00 WITA)
0 0,2,10 * * * /root/.openclaw/workspace-radit/scripts/gold-price-monitor.sh

# UNO Attendance (weekdays 08:15 WITA)
15 0 * * 1-5 python3 /root/.openclaw/workspace-radit/automation/uno-attendance.py $(date -u -d '+8 hours' +%Y-%m-%d) | jq -r '.report' | telegram-send

# Night shift janitor (01:00)
0 17 * * * /root/.openclaw/workspace-radit/scripts/night-shift-janitor.sh

# Service health check (every 5 min)
*/5 * * * * /root/.openclaw/workspace-radit/scripts/service-health-check.sh

# SSH login monitor (every minute)
* * * * * /root/.openclaw/workspace-radit/scripts/ssh-login-monitor.sh
```

---

## 🔌 Integration Configs

### n8n-webhooks.yaml
```yaml
# n8n Integration Endpoints
base_url: https://n8n-po9vt01k.sumopod.my
webhooks:
  gmail_read: /webhook/gmail-read
  gmail_send: /webhook/gmail-send
  gdrive_list: /webhook/gdrive-list
  gdrive_create: /webhook/gdrive-create-folder
  gdrive_upload: /webhook/gdrive-upload
  calendar_today: /webhook/calendar-today
  tasks_pending: /webhook/tasks-pending

circuit_breaker:
  enabled: true
  failure_threshold: 3
  cooldown_seconds: 60
```

### telegram-bots.yaml
```yaml
# Multi-agent Telegram bots
bots:
  radit:
    token: ${RADIT_BOT_TOKEN}
    handle: @RaditClaw_bot
    
  raka:
    token: ${RAKA_BOT_TOKEN}
    handle: @RakaClaw_bot
    
  rama:
    token: ${RAMA_BOT_TOKEN}
    handle: @RamaClaw_bot
    
  rafi:
    token: ${RAFI_BOT_TOKEN}
    handle: @RafiClaw_bot

group_settings:
  sumopod_main:
    id: -1001234567890
    bots: [radit, raka, rama, rafi]
```

---

## 📝 Template Files

### SOUL.md Template
```markdown
# Soul

You are [Name] — [role description].

## Personality
- [Trait 1]
- [Trait 2]
- [Trait 3]

## Communication Style
- [Language preference]
- [Tone]
- [Formatting]

## Rules
- [Do this]
- [Don't do this]

## Purpose
[What you're here to do]

## Brothers (if applicable)
| Brother | Domain | Handle Topics |
|---------|--------|---------------|
| [Name] | [Role] | [Topics] |
```

### HEARTBEAT.md Template
```markdown
# HEARTBEAT.md

## Periodic Checks
- **Interval**: 90 minutes minimum
- **Email**: Only if >6h since last check
- **Calendar**: 2x daily (morning & evening)

## Commands
- **/email** → Check unread (top 5)
- **/tasks** → List pending tasks
- **/gold** → Gold price check
- **/server** → Server health

## Auto-Actions
- Compact if idle >30 min
- Push status to dashboard
- Check disk usage (alert if >80%)
```

### USER.md Template
```markdown
# USER.md - About Your Human

- **Name**: [Name]
- **What to call them**: [Preferred name]
- **Timezone**: [Timezone]
- **Pronouns**: [pronouns]

## Emails
- [email@example.com]

## Preferences
- [Preference 1]
- [Preference 2]

## Formatting
[Preferred output style]
```

---

## 🔐 Security Templates

### .env.example
```bash
# API Keys (NEVER commit real values!)
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
MOONSHOT_API_KEY=ms-xxx
DEEPSEEK_API_KEY=ds-xxx

# Telegram
RADIT_BOT_TOKEN=xxx
RAKA_BOT_TOKEN=xxx
RAMA_BOT_TOKEN=xxx
RAFI_BOT_TOKEN=xxx

# n8n
N8N_API_KEY=eyJ...
N8N_BASE_URL=https://n8n.example.com

# WhatsApp
WHATSAPP_API_KEY=xxx
WHATSAPP_SENDER=628xxxx

# Database
REDIS_HOST=localhost
REDIS_PORT=6379

# Other
GOG_KEYRING_PASSWORD=xxx
```

### .gitignore Template
```gitignore
# Secrets
.env
.env.local
.env.*.local
*.key
*.pem
config/credentials.json
n8n-credentials.json

# Cache
__pycache__/
*.pyc
.pytest_cache/
node_modules/
.npm
.cache

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Share Your Config!

Punya konfigurasi yang bisa dishare? [Tambahkan ke examples/](../../tree/main/docs/config/examples/)

---

*Templates by: @fanani-radian*
