# 🎯 Tips & Tricks

Kumpulan tips untuk optimize OpenClaw dari pengalaman komunitas Sumopod.

---

## 💰 Cost Optimization

### 1. Model Tiering
**Save up to 80% on API costs**

```yaml
# config/model-tiers.yaml
tiers:
  background:
    model: ollama/llama3.1  # $0
    use_for: [heartbeat, simple-fetch]
  
  standard:
    model: kimi-coding/k2p5  # ~$0.002
    use_for: [general-tasks, search]
  
  premium:
    model: claude-3-opus-4.6  # $0.01+
    use_for: [complex-coding, architecture]
```

### 2. Token Budgeting
```javascript
// Set max tokens per session type
const BUDGETS = {
  heartbeat: 5000,
  quick_task: 10000,
  deep_work: 50000
};
```

### 3. Caching Strategy
```bash
# Cache expensive operations
redis_set "gold:price" "$DATA" 300  # 5 min TTL
redis_set "weather:$CITY" "$DATA" 600  # 10 min TTL
```

---

## ⚡ Performance

### 1. Sub-agent Parallelization
```bash
# DON'T: Sequential
for task in tasks; do
  process $task
done

# DO: Parallel
sessions_spawn task1 &
sessions_spawn task2 &
sessions_spawn task3 &
wait
```

### 2. JIT Context Loading
```yaml
# Hanya load context yang diperlukan
context:
  main_session: ["SOUL.md", "USER.md", "MEMORY.md"]
  heartbeat: ["HEARTBEAT.md"]
  sub_agent: []  # Minimal context
```

### 3. Compact Regularly
```bash
# Add to HEARTBEAT.md
- Run /compact if idle > 30 min
- Auto-compact saves 40-60% tokens
```

---

## 🛠️ Developer Experience

### 1. Skill Hot Reload
```bash
# Watcher auto-test skills on change
scripts/skill-hot-reload.sh --watch
```

### 2. Structured Logging
```bash
# Use structured logger untuk debug
source scripts/structured-logger.sh
log_info "Task completed" '{"duration": 120}'
```

### 3. Circuit Breaker Pattern
```bash
# Auto-failover kalau service down
./scripts/n8n-circuit-breaker.sh --status
```

---

## 🔒 Security Best Practices

### 1. Never Commit Secrets
```bash
# .gitignore
.env
*.key
*.pem
config/credentials.json
```

### 2. Use Keyring for API Keys
```bash
# Gog CLI example
gog auth login --store-keyring
```

### 3. Scan Skills Before Use
```bash
# Check for dangerous patterns
openclaw skills scan skills/suspicious-skill/

# Remove if flagged
rm -rf skills/flagged-skill
```

---

## 📝 Memory Management

### 1. Daily → Long-term
```bash
# Cron: Daily 23:30
scripts/auto-diary-memory.sh
# Auto-generates diary + memory entries
```

### 2. Archive Old Logs
```bash
# Archive logs >30 days
find memory/ -name "*.md" -mtime +30 -exec gzip {} \;
```

### 3. Memory Search
```bash
# Search prior decisions
memory_search "git config change"
```

---

## 🔄 Automation Patterns

### 1. Cron with Circuit Breaker
```bash
# scripts/cron-wrapper.sh
if ! ./scripts/n8n-call.sh "$@"; then
  ./scripts/fallback.sh "$@"
fi
```

### 2. Health Check Pattern
```bash
# Every 5 minutes
if ! curl -sf "$HEALTH_URL"; then
  systemctl restart openclaw-gateway
  telegram-send "Service restarted"
fi
```

### 3. Backup Pattern
```bash
# Daily backup
rsync -avz workspace/ backup/
git add -A && git commit -m "auto: $(date)"
git push origin main
```

---

## 🎨 Prompt Engineering

### 1. System Prompt Optimization
```markdown
# SOUL.md - Keep it concise
- Personality: [brief]
- Rules: [bullet points]
- Format: [examples]
```

### 2. Task-specific Instructions
```markdown
# Add to task prompt
## Constraints
- Max 3 sentences
- Use bullet points
- No filler words
```

### 3. Chain of Thought
```markdown
# For complex tasks
1. Plan → Write to plan.md
2. Execute → Step by step
3. Verify → Check results
4. Report → Summary only
```

---

## 🔧 Debugging

### 1. Verbose Mode
```bash
OPENCLAW_DEBUG=1 openclaw gateway start
```

### 2. Session Logs
```bash
# Check session history
sessions_history $SESSION_KEY --limit 50
```

### 3. Tool Inspection
```bash
# List available tools
openclaw tools list

# Test specific tool
openclaw tools test web_search
```

---

## 🔧 OpenClaw.json Repair & Troubleshooting

Tips untuk memperbaiki masalah umum di OpenClaw, terutama yang berhubungan dengan config dan state.

---

### 1. OpenClaw.json Corrupted

**Symptoms:**
- Gateway failed to start
- Error: "Invalid JSON in openclaw.json"
- Config tidak tersimpan

**Fix:**

```bash
# 1. Backup corrupted file
cp ~/.openclaw/config/openclaw.json ~/.openclaw/config/openclaw.json.bak.$(date +%Y%m%d)

# 2. Validate JSON
python3 -m json.tool ~/.openclaw/config/openclaw.json > /dev/null

# 3. Kalau invalid, restore dari backup terakhir
cp ~/.openclaw/config/openclaw.json.bak ~/.openclaw/config/openclaw.json

# 4. Atau reset ke default
openclaw config reset --force

# 5. Reconfigure
openclaw onboard
```

---

### 2. Session Freeze / Not Responding

**Symptoms:**
- Agent tidak reply
- Command hang
- "Session locked"

**Fix:**

```bash
# Method 1: Compact session
/compact

# Method 2: Restart gateway
openclaw gateway restart

# Method 3: Clear session cache
rm -rf ~/.openclaw/cache/sessions/*

# Method 4: Full restart
openclaw gateway stop
sleep 5
openclaw gateway start
```

---

### 3. Gateway Won't Start

**Symptoms:**
- `openclaw gateway start` failed
- Port already in use
- Error logs muncul

**Fix:**

```bash
# Check what's using port 8080 (default)
sudo lsof -i :8080

# Kill process yang pakai port
sudo kill -9 $(sudo lsof -t -i:8080)

# Atau ganti port di config
# Edit: ~/.openclaw/config/openclaw.yaml
port: 8081  # Ganti ke port lain

# Start ulang
openclaw gateway start --port 8081
```

---

### 4. Skills Not Loading

**Symptoms:**
- Skill tidak dikenali
- "Skill not found" error
- Permission denied

**Fix:**

```bash
# 1. Check skill structure
ls -la skills/my-skill/
# Harus ada: SKILL.md, scripts/

# 2. Fix permissions
chmod +x skills/*/scripts/*.sh

# 3. Re-index skills
openclaw skills index --reload

# 4. Check SKILL.md valid
openclaw skills validate skills/my-skill/
```

---

### 5. Memory/Context Too Large

**Symptoms:**
- Token usage tinggi
- Slow response
- Out of memory error

**Fix:**

```bash
# 1. Compact session segera
/compact

# 2. Archive old memory
mkdir -p memory/archive
mv memory/2026-01-*.md memory/archive/  # Archive bulan lalu
gzip memory/archive/*.md

# 3. Trim MEMORY.md
# Hapus entry lama yang tidak relevan

# 4. Set context limit di config
# config/openclaw.yaml
context:
  max_tokens: 8000
  compress_threshold: 6000
```

---

### 6. API Key Errors

**Symptoms:**
- "Invalid API key"
- "Rate limit exceeded"
- Model tidak merespon

**Fix:**

```bash
# 1. Check API key format
echo $OPENAI_API_KEY | grep "^sk-"

# 2. Test API key langsung
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# 3. Kalau expired, update .env
nano .env
# Update key baru

# 4. Reload config
source .env
openclaw gateway restart
```

---

### 7. Git Sync Failed

**Symptoms:**
- "Failed to sync with GitHub"
- Changes tidak tersimpan
- Conflict errors

**Fix:**

```bash
# 1. Check git status
cd ~/.openclaw/workspace
git status

# 2. Resolve conflicts (kalau ada)
git pull origin main --rebase

# 3. Atau force sync (HATI-HATI!)
git fetch origin
git reset --hard origin/main

# 4. Auto-sync script
# Tambah ke cron setiap 15 menit:
*/15 * * * * cd ~/.openclaw/workspace && git pull && git push 2>/dev/null
```

---

### 8. Reset Everything (Nuclear Option)

**KALAU SEMUA GAGAL:**

```bash
# 1. Backup dulu!
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/

# 2. Stop gateway
openclaw gateway stop

# 3. Reset config
rm -rf ~/.openclaw/config/
openclaw config init

# 4. Re-onboard
openclaw onboard

# 5. Restore data penting (jika perlu)
# MEMORY.md, SOUL.md, skills/, scripts/
```

---

### 9. Debug Mode

```bash
# Enable verbose logging
OPENCLAW_DEBUG=1 openclaw gateway start

# Check logs realtime
tail -f ~/.openclaw/logs/gateway.log

# Check specific session logs
openclaw logs --session $SESSION_ID
```

---

### 10. Common Error Codes

| Error | Meaning | Fix |
|-------|---------|-----|
| `ECONNREFUSED` | Gateway tidak jalan | Start gateway |
| `EADDRINUSE` | Port dipakai | Ganti port atau kill process |
| `ETIMEDOUT` | Timeout | Check internet/API status |
| `ENOENT` | File tidak ada | Check path/file |
| `EPERM` | Permission denied | Fix permissions atau sudo |

---

## Share Your Tips!

Punya tips lain? [Tambahkan ke repo](../../issues/new?template=tips.md)

---

*Contributors: Sumopod Community*
