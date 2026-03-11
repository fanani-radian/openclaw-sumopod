# ⚡ Redis Caching Pattern for Speed

> **Speed up 20x dengan Redis cache — dari 1 detik jadi 50ms!** 🚀

```
┌─────────────────────────────────────────────────────────────────┐
│                    ⚡ SPEED COMPARISON ⚡                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   WITHOUT CACHE                    WITH CACHE                   │
│   ─────────────                    ──────────                   │
│                                                                 │
│   🐌 1000ms                         ⚡ 50ms                      │
│   ████████████████████████████      █░                          │
│   1.0 second                        0.05 second                 │
│                                                                 │
│   ❌ API call every time           ✅ Cache hit 95%             │
│   ❌ Rate limit risk               ✅ Protect API               │
│   ❌ Slow user experience          ✅ Instant response          │
│                                                                 │
│   Speedup: 20x faster! 🚀                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Kenapa Caching Penting?

### Real Example: Gold Price Checker

| Metric | Without Cache | With Cache | Improvement |
|--------|--------------|------------|-------------|
| Response Time | 1000ms | 50ms | **20x faster** 🚀 |
| API Calls/Hour | 60 | 4 | **15x less** 📉 |
| Rate Limit Risk | ⚠️ High | ✅ Low | Protected |
| User Experience | 😴 Slow | ⚡ Instant | Happy! |

### When to Cache?

```
✅ GOOD for Caching:
   • Data yang jarang berubah (harga, cuaca, rates)
   • API calls mahal/limited
   • Data yang sering di-request
   • Computation-heavy results

❌ BAD for Caching:
   • Real-time critical data
   • User-specific sensitive data
   • Data yang berubah tiap detik
   • Financial transactions
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         REQUEST FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User Request                                                  │
│       │                                                         │
│       ▼                                                         │
│   ┌──────────────┐                                              │
│   │ Check Cache? │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│    ┌─────┴─────┐                                                │
│    ▼           ▼                                                │
│  HIT ❌      MISS ✅                                            │
│    │           │                                                │
│    │           ▼                                                │
│    │    ┌─────────────┐                                         │
│    │    │ Fetch from  │                                         │
│    │    │ API/Source  │                                         │
│    │    └──────┬──────┘                                         │
│    │           │                                                │
│    │           ▼                                                │
│    │    ┌─────────────┐                                         │
│    │    │ Store to    │                                         │
│    │    │ Redis       │                                         │
│    │    │ (TTL: 5min) │                                         │
│    │    └─────────────┘                                         │
│    │           │                                                │
│    └───────────┘                                                │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │ Return Data  │                                              │
│   └──────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup Redis

### Step 1: Install Redis

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y redis-server

# macOS
brew install redis
brew services start redis

# Docker
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### Step 2: Verify Installation

```bash
# Test connection
redis-cli ping

# Expected output: PONG ✅
```

### Step 3: Check Status

```bash
# Redis info
redis-cli info server | grep version

# Output: redis_version:7.2.7
```

---

## 📜 Helper Script

**File:** `redis-utils.sh`

```bash
#!/bin/bash

# ⚡ Redis Helper Functions
# Source this file: source redis-utils.sh

REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"

# ─────────────────────────────────────────────────────────────

redis_set() {
    local key="$1"
    local value="$2"
    local ttl="${3:-300}"  # Default 5 minutes
    
    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" SETEX "$key" "$ttl" "$value"
    echo "✅ Cached: $key (TTL: ${ttl}s)"
}

redis_get() {
    local key="$1"
    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" GET "$key"
}

redis_delete() {
    local key="$1"
    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" DEL "$key"
    echo "🗑️  Deleted: $key"
}

redis_exists() {
    local key="$1"
    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" EXISTS "$key"
}

redis_ttl() {
    local key="$1"
    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" TTL "$key"
}

redis_keys() {
    local pattern="${1:-*}"
    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" KEYS "$pattern"
}

# ─────────────────────────────────────────────────────────────
# Use Case Functions

redis_cache_weather() {
    local city="$1"
    local data="$2"
    redis_set "weather:$city" "$data" 1800  # 30 min TTL
}

redis_cache_price() {
    local item="$1"
    local price="$2"
    redis_set "price:$item" "$price" 300   # 5 min TTL
}

redis_cache_api_response() {
    local endpoint="$1"
    local response="$2"
    redis_set "api:$endpoint" "$response" 600  # 10 min TTL
}
```

```bash
chmod +x redis-utils.sh
```

---

## 💡 Implementation Examples

### Example 1: Weather Cache

```bash
#!/bin/bash
source redis-utils.sh

get_weather() {
    local city="$1"
    local cache_key="weather:$city"
    
    # Check cache
    cached=$(redis_get "$cache_key")
    
    if [ -n "$cached" ] && [ "$cached" != "nil" ]; then
        echo "⚡ Cache HIT: Weather for $city"
        echo "$cached"
        return
    fi
    
    # Cache miss - fetch from API
    echo "🌐 Cache MISS: Fetching weather for $city..."
    weather_data=$(curl -s "https://api.weather.com/v1/current?city=$city")
    
    # Store to cache (30 min TTL)
    redis_cache_weather "$city" "$weather_data"
    
    echo "$weather_data"
}

# Usage
get_weather "Jakarta"
get_weather "Jakarta"  # Second call = cache hit!
```

### Example 2: Price Checker with Cache

```bash
#!/bin/bash
source redis-utils.sh

get_gold_price() {
    local cache_key="gold:price"
    
    # Check cache
    cached=$(redis_get "$cache_key")
    
    if [ -n "$cached" ] && [ "$cached" != "nil" ]; then
        echo "💰 Cache HIT: Rp $cached"
        echo "⏱️  TTL: $(redis_ttl $cache_key) seconds left"
        return
    fi
    
    # Fetch fresh data
    echo "🌐 Fetching fresh price..."
    price=$(curl -s "https://hargaemas.com/api/price" | jq -r '.antam_1gr')
    
    # Cache for 5 minutes
    redis_cache_price "gold" "$price"
    
    echo "💰 Fresh: Rp $price"
}

# Benchmark
echo "First call (cache miss):"
time get_gold_price

echo ""
echo "Second call (cache hit):"
time get_gold_price
```

### Example 3: API Response Cache

```bash
#!/bin/bash
source redis-utils.sh

api_call_with_cache() {
    local endpoint="$1"
    local cache_key="api:$endpoint"
    local ttl="${2:-600}"  # Default 10 min
    
    # Try cache
    cached=$(redis_get "$cache_key")
    
    if [ -n "$cached" ] && [ "$cached" != "nil" ]; then
        echo '{"cached":true,"data":'"$cached"'}'
        return
    fi
    
    # Call API
    response=$(curl -s -w "\n%{http_code}" "https://api.example.com/$endpoint")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        # Cache successful response
        redis_set "$cache_key" "$body" "$ttl"
        echo '{"cached":false,"data":'"$body"'}'
    else
        echo '{"error":"API failed","code":'"$http_code"'}'
    fi
}

# Usage
api_call_with_cache "users/list" 300      # Cache 5 min
api_call_with_cache "config/app" 3600     # Cache 1 hour
```

---

## 🧪 Performance Testing

**File:** `cache-benchmark.sh`

```bash
#!/bin/bash
source redis-utils.sh

echo "🧪 CACHE BENCHMARK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TEST_KEY="benchmark:test"

# Clear cache
redis_delete "$TEST_KEY" 2>/dev/null

echo ""
echo "1️⃣ Cache MISS (API call simulation):"
echo "─────────────────────────────────────"

start=$(date +%s%N)
result=$(redis_get "$TEST_KEY")

if [ -z "$result" ] || [ "$result" = "nil" ]; then
    # Simulate API call
    sleep 1
    redis_set "$TEST_KEY" "test_data" 300
fi

end=$(date +%s%N)
duration_ms=$(( (end - start) / 1000000 ))

echo "   Time: ${duration_ms}ms (includes 1s API simulation)"

echo ""
echo "2️⃣ Cache HIT (Redis only):"
echo "─────────────────────────────────────"

start=$(date +%s%N)
result=$(redis_get "$TEST_KEY")
end=$(date +%s%N)
duration_ms=$(( (end - start) / 1000000 ))

echo "   Time: ${duration_ms}ms"
echo "   Data: $result"

echo ""
echo "📊 RESULT:"
echo "   Speedup: $((1000 / duration_ms))x faster!"

# Cleanup
redis_delete "$TEST_KEY" 2>/dev/null
```

**Run benchmark:**
```bash
chmod +x cache-benchmark.sh
./cache-benchmark.sh

# Output:
# 🧪 CACHE BENCHMARK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 1️⃣ Cache MISS (API call simulation):
# ─────────────────────────────────────
#    Time: 1005ms
#
# 2️⃣ Cache HIT (Redis only):
# ─────────────────────────────────────
#    Time: 3ms
#    Data: test_data
#
# 📊 RESULT:
#    Speedup: 335x faster! 🚀
```

---

## 📊 Cache Statistics

Check cache performance:

```bash
#!/bin/bash

echo "📊 CACHE STATISTICS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "🗝️  Total Keys:"
redis-cli DBSIZE

echo ""
echo "📁 Key Prefixes:"
redis-cli KEYS "*" | cut -d: -f1 | sort | uniq -c | sort -rn | head -10

echo ""
echo "⏱️  Memory Usage:"
redis-cli INFO memory | grep used_memory_human

echo ""
echo "🔑 Sample Keys:"
redis-cli KEYS "*" | head -10
```

---

## 🎯 Best Practices

### TTL Guidelines

```
Data Type              Recommended TTL
─────────────────────────────────────────
Weather               30 minutes (1800s)
Gold/Stock Prices     5 minutes (300s)
API Responses         10 minutes (600s)
User Sessions         1 hour (3600s)
Config/Settings       1 day (86400s)
Static Content        1 day (86400s)
```

### Key Naming Convention

```
format:   category:subcategory:id

examples:
  weather:jakarta
  price:gold:antam
  api:users:list
  session:user:12345
  config:app:theme
```

### Error Handling

```bash
redis_safe_get() {
    local key="$1"
    local default="${2:-null}"
    
    # Check Redis connection
    if ! redis-cli ping > /dev/null 2>&1; then
        echo "⚠️  Redis down, returning default"
        echo "$default"
        return 1
    fi
    
    result=$(redis_get "$key")
    
    if [ -z "$result" ] || [ "$result" = "nil" ]; then
        echo "$default"
        return 1
    fi
    
    echo "$result"
}
```

---

## 🔧 Troubleshooting

### Redis Connection Failed

```bash
# Check if Redis running
sudo systemctl status redis

# Restart Redis
sudo systemctl restart redis

# Check port
sudo netstat -tlnp | grep 6379
```

### Cache Not Working

```bash
# Debug: Manual test
redis-cli SET testkey "hello" EX 60
redis-cli GET testkey
redis-cli TTL testkey
```

### Memory Full

```bash
# Check memory
redis-cli INFO memory

# Clear old keys
redis-cli --eval clear-old-keys.lua

# Or set maxmemory policy in redis.conf
maxmemory-policy allkeys-lru
```

---

## 🚀 Production Tips

### 1. Redis Persistence

```bash
# Enable RDB snapshot in redis.conf
save 900 1      # Save if 1+ keys changed in 15 min
save 300 10     # Save if 10+ keys changed in 5 min
save 60 10000   # Save if 10000+ keys changed in 1 min
```

### 2. Monitoring

```bash
# Log slow queries
redis-cli SLOWLOG GET 10

# Monitor commands (dev only!)
redis-cli MONITOR
```

### 3. Backup

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backup/redis"
mkdir -p "$BACKUP_DIR"
cp /var/lib/redis/dump.rdb "$BACKUP_DIR/dump-$(date +%Y%m%d).rdb"
```

---

## 📚 Referensi

| Command | Description |
|---------|-------------|
| `SETEX key ttl value` | Set dengan TTL |
| `GET key` | Get value |
| `DEL key` | Delete key |
| `TTL key` | Check remaining TTL |
| `EXISTS key` | Check if exists |
| `KEYS pattern` | Find keys |
| `FLUSHALL` | Clear all (⚠️ DANGER) |

---

**Selamat!** Aplikasi-mu sekarang ⚡ **20x lebih cepat** dengan Redis cache! 🎉

---

*Tutorial ini dibuat untuk OpenClaw Sumopod Community*
