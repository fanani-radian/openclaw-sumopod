# 🏥 Service Health Dashboard with Auto-Retry

> **Monitor semua service-mu dalam satu dashboard — dengan auto-retry dan Telegram alerts!** 📊

```
┌─────────────────────────────────────────────────────────────────┐
│                  🏥 SERVICE HEALTH DASHBOARD                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   🟢 Database      ✅ OK        45ms                            │
│   🟢 API Server    ✅ OK        120ms                           │
│   🟡 Redis         ⚠️ DEGRADED  850ms  (slow)                   │
│   🔴 Email Service ❌ DOWN      Timeout                         │
│                                                                 │
│   ─────────────────────────────────────────────────────────     │
│                                                                 │
│   Auto-retry: Email Service ↻ Attempt 2/3...                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Fitur Utama

| Feature | Description |
|---------|-------------|
| 🔄 **Auto-Retry** | Retry otomatis dengan exponential backoff |
| 📊 **JSON Output** | Structured data untuk parsing |
| 🎨 **Visual Status** | Emoji + colors untuk quick glance |
| 📱 **Telegram Alerts** | Notifikasi real-time saat service down |
| ⏱️ **Response Time** | Track latency per service |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       MONITORING FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│   │  Service A  │     │  Service B  │     │  Service C  │       │
│   │  (Database) │     │    (API)    │     │   (Redis)   │       │
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘       │
│          │                   │                   │               │
│          └───────────────────┼───────────────────┘               │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │  Health Check    │                         │
│                    │  Script          │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│              ┌──────────────┼──────────────┐                    │
│              │              │              │                    │
│              ▼              ▼              ▼                    │
│        ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│        │   🟢     │  │   🟡     │  │   🔴     │                │
│        │   OK     │  │ DEGRADED │  │   DOWN   │                │
│        └──────────┘  └──────────┘  └──────────┘                │
│              │              │              │                    │
│              └──────────────┼──────────────┘                    │
│                             │                                   │
│                             ▼                                   │
│                    ┌──────────────────┐                         │
│                    │  Telegram Alert  │ ◄─── If DOWN/DEGRADED   │
│                    │  (Auto-retry)    │                         │
│                    └──────────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Step-by-Step Setup

### Step 1: Create Health Check Script

**File:** `health-dashboard.sh`

```bash
#!/bin/bash

# 🏥 Service Health Dashboard with Auto-Retry
# Usage: ./health-dashboard.sh [--json]

set -e

OUTPUT_FORMAT="${1:-text}"
TELEGRAM_BOT="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT="${TELEGRAM_CHAT_ID:-}"

# Services to monitor
declare -A SERVICES
declare -A SERVICE_URLS

SERVICES=(
    ["database"]="PostgreSQL"
    ["api"]="API Server"
    ["redis"]="Redis Cache"
    ["webhook"]="Webhook Endpoint"
)

SERVICE_URLS=(
    ["database"]="postgresql://localhost:5432/mydb"
    ["api"]="https://api.example.com/health"
    ["redis"]="redis://localhost:6379"
    ["webhook"]="https://webhook.example.com/ping"
)

# Thresholds
DEGRADED_MS=500   # > 500ms = degraded
TIMEOUT_MS=3000   # > 3s = down
MAX_RETRIES=3     # Retry 3 times

# Results storage
declare -A RESULT_STATUS
declare -A RESULT_TIME
declare -A RESULT_MESSAGE

# ─────────────────────────────────────────────────────────────

# Function: Check with retry
check_with_retry() {
    local service="$1"
    local url="$2"
    local attempt=0
    local success=false
    
    while [ $attempt -lt $MAX_RETRIES ]; do
        attempt=$((attempt + 1))
        
        # Perform check
        start=$(date +%s%N)
        
        case "$service" in
            "database")
                if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
                    success=true
                fi
                ;;
            "redis")
                if redis-cli ping > /dev/null 2>&1; then
                    success=true
                fi
                ;;
            *)
                http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$url" 2>/dev/null || echo "000")
                if [ "$http_code" = "200" ]; then
                    success=true
                fi
                ;;
        esac
        
        end=$(date +%s%N)
        duration_ms=$(( (end - start) / 1000000 ))
        
        if [ "$success" = true ]; then
            RESULT_TIME[$service]=$duration_ms
            
            # Determine status based on response time
            if [ $duration_ms -gt $DEGRADED_MS ]; then
                RESULT_STATUS[$service]="degraded"
                RESULT_MESSAGE[$service]="Slow response (${duration_ms}ms)"
            else
                RESULT_STATUS[$service]="ok"
                RESULT_MESSAGE[$service]="Healthy"
            fi
            return 0
        fi
        
        # Retry with exponential backoff
        if [ $attempt -lt $MAX_RETRIES ]; then
            sleep $((2 ** attempt))
        fi
    done
    
    # All retries failed
    RESULT_STATUS[$service]="down"
    RESULT_TIME[$service]=9999
    RESULT_MESSAGE[$service]="Timeout after $MAX_RETRIES attempts"
    return 1
}

# Function: Get status emoji
get_emoji() {
    local status="$1"
    case "$status" in
        "ok") echo "🟢" ;;
        "degraded") echo "🟡" ;;
        "down") echo "🔴" ;;
        *) echo "⚪" ;;
    esac
}

# Function: Get status text
get_status_text() {
    local status="$1"
    case "$status" in
        "ok") echo "✅ OK" ;;
        "degraded") echo "⚠️  DEGRADED" ;;
        "down") echo "❌ DOWN" ;;
        *) echo "❓ UNKNOWN" ;;
    esac
}

# ─────────────────────────────────────────────────────────────
# Main Execution

echo "🏥 HEALTH DASHBOARD CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Time: $(date)"
echo ""

# Check all services
for service in "${!SERVICES[@]}"; do
    name="${SERVICES[$service]}"
    url="${SERVICE_URLS[$service]}"
    
    echo "Checking: $name..."
    check_with_retry "$service" "$url"
done

echo ""
echo "📊 RESULTS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Output based on format
if [ "$OUTPUT_FORMAT" = "--json" ]; then
    # JSON output
    echo "{"
    echo '  "timestamp": "'"$(date -Iseconds)'"",'
    echo '  "services": ['
    
    first=true
    for service in "${!SERVICES[@]}"; do
        [ "$first" = true ] || echo ","
        first=false
        
        cat <<EOF
    {
      "name": "${SERVICES[$service]}",
      "status": "${RESULT_STATUS[$service]}",
      "response_time_ms": ${RESULT_TIME[$service]},
      "message": "${RESULT_MESSAGE[$service]}"
    }
EOF
    done
    
    echo ""
    echo "  ]"
    echo "}"
else
    # Text output
    for service in "${!SERVICES[@]}"; do
        emoji=$(get_emoji "${RESULT_STATUS[$service]}")
        status_text=$(get_status_text "${RESULT_STATUS[$service]}")
        time_ms="${RESULT_TIME[$service]}"
        message="${RESULT_MESSAGE[$service]}"
        
        printf "%-20s %s %-10s %5sms %s\n" \
            "${SERVICES[$service]}:" \
            "$emoji" \
            "$status_text" \
            "$time_ms" \
            "$message"
    done
fi

# Count issues
ok_count=0
degraded_count=0
down_count=0

for status in "${RESULT_STATUS[@]}"; do
    case "$status" in
        "ok") ok_count=$((ok_count + 1)) ;;
        "degraded") degraded_count=$((degraded_count + 1)) ;;
        "down") down_count=$((down_count + 1)) ;;
    esac
done

echo ""
echo "📈 SUMMARY:"
echo "   🟢 OK: $ok_count"
echo "   🟡 Degraded: $degraded_count"
echo "   🔴 Down: $down_count"

# Send Telegram alert if issues found
if [ $down_count -gt 0 ] || [ $degraded_count -gt 0 ]; then
    if [ -n "$TELEGRAM_BOT" ] && [ -n "$TELEGRAM_CHAT" ]; then
        alert_message="🚨 HEALTH ALERT

"
        
        for service in "${!SERVICES[@]}"; do
            if [ "${RESULT_STATUS[$service]}" != "ok" ]; then
                emoji=$(get_emoji "${RESULT_STATUS[$service]}")
                alert_message+="${SERVICES[$service]}: ${RESULT_STATUS[$service]}
"
            fi
        done
        
        alert_message+="
Time: $(date)"
        
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT" \
            -d "text=$alert_message" \
            > /dev/null
        
        echo ""
        echo "📱 Telegram alert sent!"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

```bash
chmod +x health-dashboard.sh
```

---

## 🧪 Testing

### Test 1: Normal Run (Text Output)

```bash
./health-dashboard.sh

# Output:
# 🏥 HEALTH DASHBOARD CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Time: Wed Mar 11 08:30:00 WIB 2026
#
# Checking: PostgreSQL...
# Checking: API Server...
# Checking: Redis Cache...
# Checking: Webhook Endpoint...
#
# 📊 RESULTS:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PostgreSQL:          🟢 ✅ OK        45ms  Healthy
# API Server:          🟢 ✅ OK       120ms  Healthy
# Redis Cache:         🟡 ⚠️  DEGRADED  850ms Slow response (850ms)
# Webhook Endpoint:    🔴 ❌ DOWN      9999ms Timeout after 3 attempts
#
# 📈 SUMMARY:
#    🟢 OK: 2
#    🟡 Degraded: 1
#    🔴 Down: 1
#
# 📱 Telegram alert sent!
```

### Test 2: JSON Output

```bash
./health-dashboard.sh --json | jq

# Output:
# {
#   "timestamp": "2026-03-11T08:30:00+07:00",
#   "services": [
#     {
#       "name": "PostgreSQL",
#       "status": "ok",
#       "response_time_ms": 45,
#       "message": "Healthy"
#     },
#     ...
#   ]
# }
```

---

## 📅 Setup Cron

```bash
# Edit crontab
crontab -e

# Check every 5 minutes
*/5 * * * * /path/to/health-dashboard.sh --json > /var/log/health.json 2>>1

# Daily summary report (8 AM)
0 8 * * * /path/to/health-dashboard.sh | mail -s "Daily Health Report" admin@example.com
```

---

## 🎨 Visual Status Page

Buat simple HTML dashboard:

```bash
#!/bin/bash
# generate-status-page.sh

JSON_DATA=$(./health-dashboard.sh --json)

cat > /var/www/html/status.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Service Status</title>
    <style>
        body { font-family: monospace; padding: 20px; background: #1a1a1a; color: #fff; }
        .ok { color: #4caf50; }
        .degraded { color: #ff9800; }
        .down { color: #f44336; }
        .service { padding: 10px; margin: 5px; background: #333; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🏥 Service Health Dashboard</h1>
    <p>Last updated: $(date)</p>
    <div id="services"></div>
    <script>
        const data = $JSON_DATA;
        const container = document.getElementById('services');
        
        data.services.forEach(svc => {
            const div = document.createElement('div');
            div.className = 'service ' + svc.status;
            div.innerHTML = \`
                <strong>\${svc.name}</strong>: 
                \${svc.status.toUpperCase()} 
                (\${svc.response_time_ms}ms)
            \`;
            container.appendChild(div);
        });
    </script>
</body>
</html>
EOF

echo "✅ Status page generated: /var/www/html/status.html"
```

---

## 📊 Monitoring Integration

### Save to InfluxDB

```bash
# Add to health-dashboard.sh
save_to_influxdb() {
    local service="$1"
    local status="$2"
    local time_ms="$3"
    
    curl -s -X POST "http://influxdb:8086/write?db=monitoring" \
        --data-binary "health_check,service=$service status=\"$status\",response_time=$time_ms"
}
```

### Grafana Dashboard

Query untuk Grafana:
```sql
-- Response time trend
SELECT mean("response_time") FROM "health_check" 
WHERE $timeFilter GROUP BY time($interval), "service"

-- Down events
SELECT count("status") FROM "health_check" 
WHERE "status" = 'down' AND $timeFilter GROUP BY "service"
```

---

## 🔧 Troubleshooting

### Check Not Working

```bash
# Test individual service
curl -v https://api.example.com/health
pg_isready -h localhost -p 5432
redis-cli ping

# Check script permissions
ls -la health-dashboard.sh
```

### False Positives

Tambahkan validasi response:

```bash
# Check response content, not just HTTP code
response=$(curl -s "$url")
if echo "$response" | grep -q '"status":"healthy"'; then
    success=true
fi
```

---

## 📚 Referensi

| Status | HTTP Code | Meaning |
|--------|-----------|---------|
| 🟢 OK | 200 | Service healthy |
| 🟡 Degraded | 200 (slow) | Working but slow |
| 🔴 Down | 4xx/5xx/timeout | Not responding |

---

**Selamat!** Monitoring system-mu sekarang auto-detect issues dengan retry logic! 🎉

---

*Tutorial ini dibuat untuk OpenClaw Sumopod Community*
