# 📱 Setup Telegram Bot

Panduan lengkap menghubungkan OpenClaw dengan Telegram Bot.

---

## 🎯 Overview

Telegram Bot memungkinkan kamu:
- ✅ Chat dengan AI agent dari HP
- ✅ Terima notifikasi otomatis (gold price, server alert, dll)
- ✅ Kirim commands (/gold, /server, /email)
- ✅ Integrasi dengan group chat

---

## 📝 Step 1: Buat Bot di Telegram

### Via @BotFather

1. **Buka Telegram** → Search "@BotFather"
2. **Start chat** → Klik `/start`
3. **Buat bot baru** → Kirim `/newbot`
4. **Isi nama bot**:
   - **Name**: My OpenClaw Bot (boleh pakai spasi)
   - **Username**: myopenclaw_bot (harus unik, diakhiri _bot)
5. **Copy Bot Token** → Simpan dengan aman!

```
🔐 Contoh token:
123456789:ABCdefGHIjklMNOpqrSTUvwxyz
```

> ⚠️ **Jangan pernah share token ini!** Kalau bocor, bikin ulang via /revoke

---

## ⚙️ Step 2: Konfigurasi di OpenClaw

### 1. Set Environment Variable

```bash
# .env file
TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrSTUvwxyz"
```

### 2. Konfigurasi Channel

Edit `config/openclaw.yaml`:

```yaml
channels:
  telegram:
    enabled: true
    bot_token: ${TELEGRAM_BOT_TOKEN}
    default_chat_id: "${TELEGRAM_CHAT_ID}"  # Optional
    allowed_chats:
      - "${MY_CHAT_ID}"
      - "${GROUP_CHAT_ID}"
```

### 3. Dapatkan Chat ID

**Cara 1: Via Bot**
```
1. Start chat dengan bot kamu
2. Kirim pesan apa saja
3. Buka: https://api.telegram.org/bot<TOKEN>/getUpdates
4. Cari "chat":{"id":123456789
```

**Cara 2: Via @userinfobot**
```
1. Search "@userinfobot" di Telegram
2. Start → Dapat ID kamu
3. Untuk group: Add bot ke group → Kirim /getgroupid@userinfobot
```

---

## 🚀 Step 3: Test Connection

### Start Gateway

```bash
openclaw gateway start
```

### Test dari Telegram

```
/start        → Bot reply dengan welcome message
/help         → List available commands
/status       → Cek gateway status
```

### Test dari Terminal

```bash
# Kirim test message
openclaw message send \
  --channel telegram \
  --to "${CHAT_ID}" \
  --text "🎉 Hello from OpenClaw!"
```

---

## 🎨 Custom Commands

### Tambah Commands ke BotFather

1. Kirim `/setcommands` ke @BotFather
2. Pilih bot kamu
3. Kirim daftar commands:

```
gold - Cek harga emas hari ini
server - Cek status server
email - Cek email terbaru
tasks - List pending tasks
weather - Cek cuaca
compact - Compact session memory
```

### Handle Commands di OpenClaw

Edit `HEARTBEAT.md` atau buat skill:

```yaml
# config/telegram-commands.yaml
commands:
  /gold:
    action: run_script
    script: scripts/quick-gold.sh
    
  /server:
    action: run_script
    script: scripts/server-health-check.sh
    
  /email:
    action: run_script
    script: scripts/quick-email.sh
    
  /compact:
    action: compact_session
```

---

## 👥 Setup Group Chat

### 1. Add Bot ke Group

1. Buka group → Add member
2. Search username bot → Add
3. Jadikan admin (optional, untuk delete messages)

### 2. Dapatkan Group Chat ID

```bash
# Cara 1: Via getUpdates
https://api.telegram.org/bot<TOKEN>/getUpdates
# Cari: "chat":{"id":-1001234567890

# Cara 2: Via bot
/getgroupid@userinfobot
```

> 💡 **Group ID selalu diawali -100**

### 3. Update Config

```yaml
channels:
  telegram:
    allowed_chats:
      - "${MY_CHAT_ID}"       # Personal chat
      - "-1001234567890"      # Group chat (note the -100)
```

---

## 🔔 Notifikasi Otomatis

### Contoh: Gold Price Alert

```bash
# scripts/gold-alert.sh
PRICE=$(fetch_gold_price)
if [ "$PRICE" -gt 3200000 ]; then
  openclaw message send \
    --channel telegram \
    --to "${CHAT_ID}" \
    --text "🚀 Gold price spike! Rp $PRICE/gr"
fi
```

### Cron Schedule

```bash
# Cron setiap 1 jam
0 * * * * /scripts/gold-alert.sh
```

---

## 🔒 Security Best Practices

### 1. Restrict Bot Access

```yaml
channels:
  telegram:
    # Hanya terima dari chat yang diizinkan
    allowed_chats_only: true
    allowed_chats:
      - "123456789"           # Kamu
      - "-1001234567890"      # Group kerja
```

### 2. Validasi Commands

```bash
# Validasi user sebelum eksekusi sensitive commands
if [ "$USER_ID" != "123456789" ]; then
  echo "⛔ Unauthorized"
  exit 1
fi
```

### 3. Log Semua Interaksi

```bash
# Log commands
log_info "Telegram command" "{\"user\":\"$USER_ID\",\"cmd\":\"$COMMAND\"}"
```

---

## 🐛 Troubleshooting

### "Bot not responding"

```bash
# Check gateway status
openclaw gateway status

# Restart if needed
openclaw gateway restart

# Check logs
openclaw logs --channel telegram
```

### "Chat not found"

- Pastikan Chat ID benar (personal: angka, group: -100...)
- Bot harus sudah start chat dengan user
- Untuk group: bot harus member group

### "Message not delivered"

```bash
# Test dengan curl langsung
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>" \
  -d "text=Test message"
```

### "Token invalid"

```
1. Buka @BotFather
2. Kirim /revoke
3. Pilih bot → Token lama dicabut
4. Buat token baru dengan /token
5. Update .env dengan token baru
```

---

## 📱 Formatting Tips

### Markdown Support

Telegram support Markdown:

```markdown
*bold text*
_italic text_
`inline code`
[link text](URL)
```

### Code Blocks

````
```bash
echo "Hello World"
```
````

### Emojis

```bash
# Status icons
✅ Success
❌ Error
⚠️ Warning
🔄 Processing
📊 Data
🚀 Deployed
```

---

## 🔗 Integrasi dengan Use Cases

| Use Case | Telegram Feature |
|----------|-----------------|
| Gold Price Monitor | Daily price update |
| Server Health | Alert on downtime |
| Email Automation | New email notification |
| Security Monitoring | Intrusion alerts |
| Morning Briefing | Daily summary |

---

## 📚 Referensi

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots#6-botfather)
- [OpenClaw Telegram Channel](https://docs.openclaw.ai/channels/telegram)

---

*Last updated: March 2026*
