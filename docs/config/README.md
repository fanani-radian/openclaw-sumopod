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

## 🔧 All Config Options Reference

Complete list of what can be configured in OpenClaw.

---

### openclaw.yaml (Main Config)

```yaml
# ~/.openclaw/config/openclaw.yaml

# Gateway Settings
gateway:
  host: "0.0.0.0"
  port: 8080                    # Change if port conflict
  workers: 4                    # Number of worker processes
  timeout: 300                  # Request timeout (seconds)
  max_request_size: "10MB"

# Logging
logging:
  level: "info"                 # debug, info, warn, error
  format: "json"                # json, text
  file: "~/.openclaw/logs/gateway.log"
  max_size: "100MB"
  max_files: 5                  # Keep last N log files

# Models
models:
  default: "kimi-coding/k2p5"
  fallback: "deepseek-v3"
  max_tokens: 8192
  temperature: 0.7
  
# Context Management
context:
  max_context_tokens: 8000
  compress_threshold: 6000      # Auto-compact when reached
  keep_system_prompt: true      # Always keep system prompt
  
# Memory
memory:
  enabled: true
  directory: "~/.openclaw/workspace/memory"
  max_file_size: "1MB"
  auto_archive: true
  archive_after_days: 30

# Channels (Integrations)
channels:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    allowed_chats: []
    
  discord:
    enabled: false
    bot_token: "${DISCORD_BOT_TOKEN}"
    
  slack:
    enabled: false
    bot_token: "${SLACK_BOT_TOKEN}"

# Sub-agents
subagents:
  max_concurrent: 5
  timeout: 120
  default_model: "kimi-coding/k2p5"
  
# Skills
skills:
  directory: "~/.openclaw/workspace/skills"
  auto_reload: true             # Hot reload on change
  allow_untrusted: false        # Scan before loading
  
# Cron
cron:
  enabled: true
  jobs_file: "~/.openclaw/config/cron-jobs.json"
  
# Security
security:
  allowed_hosts: ["localhost", "127.0.0.1"]
  api_key_required: true
  rate_limit:
    enabled: true
    requests_per_minute: 60
```

---

### Environment Variables (.env)

```bash
# API Keys
OPENAI_API_KEY="sk-xxx"
ANTHROPIC_API_KEY="sk-ant-xxx"
MOONSHOT_API_KEY="sk-xxx"
DEEPSEEK_API_KEY="sk-xxx"
GEMINI_API_KEY="xxx"

# Telegram
TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234..."
TELEGRAM_CHAT_ID="123456789"

# Discord
DISCORD_BOT_TOKEN="xxx"

# Database
REDIS_URL="redis://localhost:6379"
POSTGRES_URL="postgresql://user:pass@localhost/db"

# GitHub
GITHUB_TOKEN="ghp_xxx"

# n8n
N8N_BASE_URL="https://n8n.example.com"
N8N_API_KEY="xxx"

# Custom
MY_CUSTOM_VAR="value"
```

---

### Cron Jobs Config

```json
{
  "jobs": [
    {
      "name": "gold-price-check",
      "schedule": "0 8,18 * * *",
      "command": "scripts/gold-price-monitor.sh",
      "enabled": true
    },
    {
      "name": "git-sync",
      "schedule": "*/15 * * * *",
      "command": "git-sync.sh",
      "enabled": true
    },
    {
      "name": "backup",
      "schedule": "0 2 * * *",
      "command": "backup.sh",
      "enabled": true,
      "retry": 3
    }
  ]
}
```

---

### Model Providers Config

```yaml
# ~/.openclaw/config/providers.yaml

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    base_url: "https://api.openai.com/v1"
    models:
      - gpt-4o
      - gpt-4o-mini
      
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    models:
      - claude-3-opus-4.6
      - claude-3-sonnet-4.5
      
  moonshot:
    api_key: "${MOONSHOT_API_KEY}"
    base_url: "https://api.moonshot.cn/v1"
    models:
      - kimi-k2.5
      - kimi-coding/k2p5
      
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
    models:
      - deepseek-chat
      - deepseek-coder
      
  ollama:
    base_url: "http://localhost:11434"
    models:
      - llama3.1
      - phi3
```

---

### Rate Limiting Config

```yaml
# ~/.openclaw/config/rate-limits.yaml

limits:
  # Per IP
  ip:
    requests_per_minute: 60
    burst: 10
    
  # Per user (if authenticated)
  user:
    requests_per_minute: 120
    tokens_per_day: 100000
    
  # Per model
  models:
    "gpt-4o":
      requests_per_minute: 20
    "kimi-coding/k2p5":
      requests_per_minute: 50
```

---

### Notification Templates

```yaml
# ~/.openclaw/config/notifications.yaml

templates:
  error:
    title: "❌ Error Alert"
    color: "#FF0000"
    format: |
      **Error:** {{ message }}
      **Time:** {{ timestamp }}
      **Session:** {{ session_id }}
      
  success:
    title: "✅ Success"
    color: "#00FF00"
    
  warning:
    title: "⚠️ Warning"
    color: "#FFA500"

channels:
  telegram:
    default_chat: "${TELEGRAM_CHAT_ID}"
  
  email:
    smtp_host: "smtp.gmail.com"
    smtp_port: 587
    username: "${EMAIL_USER}"
    password: "${EMAIL_PASS}"
    to: "admin@example.com"
```

---

## Share Your Config!

Punya konfigurasi yang bisa dishare? [Tambahkan ke examples/](../../tree/main/docs/config/examples/)

---

*Templates by: @fanani-radian*
