# Use Case: Building a Smart News Aggregator with OpenClaw

> **Tutorial Level**: Intermediate  
> **Estimated Time**: 45 minutes  
> **Prerequisites**: OpenClaw installed, Telegram bot configured

## Overview

This tutorial walks you through building a personalized news aggregator that fetches stories from multiple sources, deduplicates them, and delivers witty, emoji-rich updates to Telegram on scheduled intervals.

## What You'll Build

A multi-category news system with:
- **5 news categories** with different refresh intervals
- **Redis-based deduplication** (no repeat stories)
- **Witty, human-like formatting** with emojis
- **Automatic cron scheduling**
- **Telegram integration**

## Architecture

```
skills/my-news/
├── config/
│   └── sources.json          # RSS/API endpoints
├── scripts/
│   ├── fetcher.py           # Generic RSS/API fetcher
│   ├── dedup.py             # Redis deduplication
│   ├── formatter.py         # Emoji + witty comments
│   ├── sender.sh            # Telegram delivery
│   └── fetch-*.sh           # Category wrappers
└── logs/
    └── news.log
```

## Step 1: Project Setup

Create the skill structure:

```bash
mkdir -p skills/my-news/{scripts,config,logs}
touch skills/my-news/SKILL.md
touch skills/my-news/config/sources.json
```

## Step 2: Define Your Sources

Create `config/sources.json` with sample sources:

```json
{
  "categories": {
    "tech": {
      "interval": "3h",
      "ttl": 259200,
      "emoji": ["🚀", "💻", "🔥", "✨"],
      "sources": [
        {"name": "Tech News Site", "type": "rss", "url": "https://example.com/feed", "limit": 5},
        {"name": "Dev Community", "type": "rss", "url": "https://dev.to/feed", "limit": 5}
      ]
    },
    "finance": {
      "interval": "2h",
      "ttl": 172800,
      "emoji": ["💰", "📈", "📉", "💵"],
      "sources": [
        {"name": "Markets", "type": "rss", "url": "https://example.com/markets.rss", "limit": 5}
      ]
    },
    "sports": {
      "interval": "8h",
      "ttl": 604800,
      "emoji": ["⚽", "🏆", "🔥", "⚡"],
      "sources": [
        {"name": "ESPN", "type": "rss", "url": "https://example.com/sports.rss", "limit": 5}
      ]
    }
  }
}
```

**TTL Strategy**: Higher TTL for slower-updating categories:
- Fast (finance): 48 hours
- Medium (tech): 72 hours  
- Slow (sports): 7 days

## Step 3: Build the Fetcher

Create `scripts/fetcher.py`:

```python
#!/usr/bin/env python3
import json
import feedparser
import requests

def fetch_rss(url, limit=5):
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:limit]:
            items.append({
                "title": entry.get('title', 'No title'),
                "url": entry.get('link', ''),
                "source": feed.feed.get('title', 'RSS'),
                "published": entry.get('published', 'now')
            })
        return items
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print(json.dumps(fetch_rss(url, limit), indent=2))
```

## Step 4: Deduplication System

Create `scripts/dedup.py`:

```python
#!/usr/bin/env python3
import redis
import hashlib
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_key(category):
    return f"news:{category}:seen"

def is_seen(url, category):
    key = get_key(category)
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return r.sismember(key, url_hash)

def mark_seen(url, category, ttl=86400):
    key = get_key(category)
    url_hash = hashlib.md5(url.encode()).hexdigest()
    r.sadd(key, url_hash)
    r.expire(key, ttl)

def filter_new(items, category, ttl=86400):
    new_items = []
    for item in items:
        if not is_seen(item['url'], category):
            new_items.append(item)
            mark_seen(item['url'], category, ttl)
    return new_items

if __name__ == "__main__":
    # Read items from stdin
    items = json.load(sys.stdin)
    category = sys.argv[1]
    new_items = filter_new(items, category)
    print(json.dumps(new_items, indent=2))
```

## Step 5: Witty Formatter

Create `scripts/formatter.py`:

```python
#!/usr/bin/env python3
import json
import random

WITTY_COMMENTS = {
    "tech": [
        "Another framework to learn! 🔥",
        "The cloud is just someone else's computer ☁️",
        "Have you tried turning it off and on again? 🔄"
    ],
    "finance": [
        "Stonks! 📈",
        "Money printer go brrr? 🖨️",
        "Buy the dip! 💎"
    ],
    "sports": [
        "What a match! 🔥",
        "Title race getting spicy 🌶️",
        "VAR doing its thing again 📺"
    ]
}

def format_news(items, category):
    if not items:
        return None
    
    witty = random.choice(WITTY_COMMENTS.get(category, ["Fresh news! 📰"]))
    emojis = {"tech": "🚀", "finance": "💰", "sports": "⚽"}
    
    lines = [f"{emojis.get(category, '📰')} *{category.upper()} NEWS*"]
    lines.append(f"_{witty}_\n")
    
    for i, item in enumerate(items[:5], 1):
        lines.append(f"{i}. *{item['title']}*")
        lines.append(f"📎 [{item['source']}]({item['url']})\n")
    
    lines.append("━━━━━━━━━━━━")
    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    items = json.load(sys.stdin)
    category = sys.argv[1]
    print(format_news(items, category))
```

## Step 6: Telegram Sender

Create `scripts/sender.sh`:

```bash
#!/bin/bash
TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID}"

message=$(cat)

curl -s -X POST \
  "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{
    \"chat_id\": \"${CHAT_ID}\",
    \"text\": $(echo "$message" | jq -Rs .),
    \"parse_mode\": \"Markdown\",
    \"disable_web_page_preview\": true
  }"
```

## Step 7: Category Wrapper

Create `scripts/fetch-tech.sh`:

```bash
#!/bin/bash
CATEGORY="tech"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Fetch
news=$(python3 "$SCRIPT_DIR/fetcher.py" "https://dev.to/feed" 5)

# Deduplicate
new_news=$(echo "$news" | python3 "$SCRIPT_DIR/dedup.py" "$CATEGORY")

# Format and send
if [ "$(echo "$new_news" | jq length)" -gt 0 ]; then
    echo "$new_news" | python3 "$SCRIPT_DIR/formatter.py" "$CATEGORY" | bash "$SCRIPT_DIR/sender.sh"
fi
```

Make it executable:
```bash
chmod +x scripts/*.sh scripts/*.py
```

## Step 8: Cron Setup

Add to your crontab:

```bash
# Tech news every 3 hours
0 */3 * * * /path/to/skills/my-news/scripts/fetch-tech.sh

# Finance every 2 hours
0 */2 * * * /path/to/skills/my-news/scripts/fetch-finance.sh

# Sports every 8 hours
0 */8 * * * /path/to/skills/my-news/scripts/fetch-sports.sh
```

## Step 9: Testing

Test manually before cron:
```bash
# Test fetcher
python3 scripts/fetcher.py "https://dev.to/feed" 3

# Test full pipeline
bash scripts/fetch-tech.sh
```

## Advanced Features

### Smart Search Fallback
When RSS fails, use smart-search:

```python
def fetch_with_fallback(url, query):
    try:
        return fetch_rss(url)
    except:
        # Fallback to smart-search
        import subprocess
        result = subprocess.run(
            ["bash", "skills/smart-search/scripts/search.sh", query],
            capture_output=True, text=True
        )
        return parse_search_results(result.stdout)
```

### Scrapling for Protected Sites
For sites with anti-bot protection:

```python
from scrapling import Fetcher

def fetch_protected(url):
    fetcher = Fetcher()
    page = fetcher.get(url)
    return parse_html(page.text)
```

### Multi-Source Aggregation
Combine multiple sources per category:

```bash
# Fetch from 3 sources
news1=$(python3 fetcher.py "source1.com/feed" 3)
news2=$(python3 fetcher.py "source2.com/rss" 3)
news3=$(python3 fetcher.py "source3.com/api" 3)

# Merge and dedupe
all_news=$(echo "[$news1, $news2, $news3]" | jq 'add | unique_by(.url)')
```

## Troubleshooting

**No messages sent?**
- Check Redis: `redis-cli ping`
- Check logs: `tail -f logs/news.log`
- Verify Telegram token: `echo $TELEGRAM_BOT_TOKEN`

**Duplicate news?**
- Clear Redis: `redis-cli del news:tech:seen`
- Check TTL: `redis-cli ttl news:tech:seen`

**RSS parsing errors?**
- Test feed: `curl -s https://example.com/feed | head -20`
- Try feedparser directly in Python

## Conclusion

You've built a fully automated news aggregator that:
- ✅ Fetches from multiple sources
- ✅ Prevents duplicates with Redis
- ✅ Formats with personality
- ✅ Delivers to Telegram
- ✅ Runs on autopilot via cron

**Next steps:**
- Add more categories (local news, weather, crypto)
- Implement keyword filtering
- Add sentiment analysis
- Create web dashboard with Supabase

---

*Built with OpenClaw 🦞*  
*For more use cases, visit: github.com/openclaw/openclaw/docs*
