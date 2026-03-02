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

## Share Your Tips!

Punya tips lain? [Tambahkan ke repo](../../issues/new?template=tips.md)

---

*Contributors: @fanani-radian, [add yours!]*
