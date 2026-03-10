# ⚠️ JANGAN Update ke OpenClaw 2026.3.7+ — Kimi 2.5 Tool Calling BROKEN!

> **Status:** 🔴 CRITICAL BUG — Affects all Kimi K2.5 users  
> **Affected Versions:** 2026.3.7, 2026.3.8  
> **Last Known Good:** 2026.3.2 ✅  
> **Related Issues:** [#39907](https://github.com/openclaw/openclaw/issues/39907), [#41297](https://github.com/openclaw/openclaw/issues/41297)

---

## 🎯 TL;DR — Quick Summary

```
┌─────────────────────────────────────────────────────────┐
│  ❌ 2026.3.7+  → Tool calling KIMI 2.5 RUSAK           │
│  ✅ 2026.3.2   → STAY — everything works perfectly     │
│                                                         │
│  Command:                                               │
│  pkill -f openclaw; npm install -g openclaw@2026.3.2   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚨 Apa yang Terjadi?

### Sebelum (2026.3.2 ✅)

```
User: "execute ls -la"

Kimi 2.5: [TOOL_CALL] exec({"command": "ls -la"})
         ↓
     [✅ EXECUTED] — Real tool card muncul!
```

### Sesudah (2026.3.7+ ❌)

```
User: "execute ls -la"

Kimi 2.5: "exec({"command": "ls -la"})" 
         ↓
     [❌ FAILED] — Cuma text literal, gak jalan!
         ↓
     Atau looping: "Executing... ⏳" "Running now... ⏳" tanpa henti
```

---

## 🔍 3 Pola Failure yang Terjadi

| Pattern | Deskripsi | Visual |
|---------|-----------|--------|
| **🔄 Looping** | Model bilang "Executing..." "Running now..." tapi gak pernah jalan | `⏳ ⏳ ⏳` infinite loop |
| **📝 Literal Text** | Model output `exec({"command": "..."})` sebagai chat text | `exec({...})` — cuma text, bukan tool call |
| **🎭 Fake Success** | Model bilang "✅ Done! Command executed" padahal gak jalan sama sekali | Tipu-tipu 🎪 |

---

## 🧠 Kenapa Bisa Begini?

### Root Cause Analysis

```
┌──────────────────────────────────────────────────────────┐
│  REQUEST SIDE ✅ (Works fine)                           │
│  OpenClaw → convert tool schema → Kimi API format       │
│  ✓ Payload benar, Kimi nerima dengan baik               │
├──────────────────────────────────────────────────────────┤
│  RESPONSE SIDE ❌ (BROKEN in 2026.3.7+)                 │
│  Kimi API → return tool_use blocks                      │
│  OpenClaw parser → gak recognize format Kimi            │
│  Result → treat as plain text ❌                        │
└──────────────────────────────────────────────────────────┘
```

### Bukti: Kimi API ITU BISA tool calling!

```bash
# Direct test ke Kimi API — TOOL CALLING WORKS! ✅
curl -s https://api.kimi.com/coding/v1/messages \
  -H "x-api-key: $KIMI_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "model": "k2p5",
    "tools": [{"name": "bash", "input_schema": {...}}],
    "messages": [{"role": "user", "content": "Run ls -la"}]
  }'

# Response (correct):
{
  "content": [{
    "type": "tool_use",           ← ✅ Proper tool_use block!
    "name": "bash",
    "input": {"command": "ls -la"}
  }]
}
```

**Conclusion:** Masalahnya di OpenClaw parser (response side), BUKAN di Kimi API! 🎯

---

## 🔧 SOLUSI: Downgrade ke 2026.3.2

### ⚡ Quick Fix (One-Liner)

```bash
pkill -f openclaw; npm install -g openclaw@2026.3.2
```

### 📋 Step-by-Step Detail

```bash
# 1️⃣ Stop gateway yang lagi jalan
pkill -f openclaw

# 2️⃣ Downgrade ke versi yang works
npm install -g openclaw@2026.3.2

# 3️⃣ Reinstall gateway service (kalau pakai systemd)
openclaw gateway install --force

# 4️⃣ Restart gateway
openclaw gateway restart

# 5️⃣ Verify version
openclaw version
# Expected: 2026.3.2 ✅
```

### 🎨 Visual Step-by-Step

```
   ┌──────────┐
   │   🛑     │  1. Stop OpenClaw
   │   Stop   │     pkill -f openclaw
   └────┬─────┘
        ▼
   ┌──────────┐
   │   📦     │  2. Downgrade
   │ Install  │     npm i -g openclaw@2026.3.2
   └────┬─────┘
        ▼
   ┌──────────┐
   │   ⚙️     │  3. Reinstall service
   │  Setup   │     openclaw gateway install --force
   └────┬─────┘
        ▼
   ┌──────────┐
   │   🚀     │  4. Start lagi
   │ Restart  │     openclaw gateway restart
   └────┬─────┘
        ▼
   ┌──────────┐
   │   ✅     │  5. Kimi 2.5 works!
   │ Success  │     Tool calling balik normal
   └──────────┘
```

---

## 🧪 Verifikasi: Cek Tool Calling Works

Setelah downgrade, test dengan command sederhana:

```
User: "execute pwd"

Expected Output:
┌────────────────────────────────────────┐
│  Exec                                  │
│  Command: pwd                          │
│  Status: ✅ Success                    │
│  Output: /home/user/workspace          │
└────────────────────────────────────────┘
```

Kalau muncul **real tool card** → ✅ Berhasil downgrade!

Kalau cuma text `exec({"command": "pwd"})` → ❌ Masih broken, coba ulang step-nya

---

## ⏳ Kapan Bisa Update Lagi?

```
🔴 NOW — 2026.3.7 / 2026.3.8  →  JANGAN UPDATE! Stay di 2026.3.2
🟡 WAIT — Pantau issue #41297   →  Track progress fix
🟢 SAFE — Fix released          →  Bisa update lagi (nanti diumumkan)
```

**Monitor progress:**
- Issue: [#41297](https://github.com/openclaw/openclaw/issues/41297)
- Issue: [#39907](https://github.com/openclaw/openclaw/issues/39907)

---

## 💡 Alternatif Sementara (Kalau Mau Stay 2026.3.7+)

Kalau ada alasan kuat harus stay di 2026.3.7+, ada workaround:

### Option A: Switch ke Model Lain

| Model | Tool Calling Status | Notes |
|-------|---------------------|-------|
| `google/gemini-3-flash` | ✅ Works | Fast, cheap, reliable |
| `zai/glm-4.7` | ✅ Works | ByteDance, good for coding |
| `kimi-coding/k2p5` | ❌ Broken | Avoid in 2026.3.7+ |

```json
// ~/.openclaw/openclaw.json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3-flash",  ← Switch sementara
        "fallbacks": ["zai/glm-4.7"]
      }
    }
  }
}
```

### Option B: Use Sub-Agents dengan Ollama

Kalau tasknya lokal/bukan butuh Kimi specifically:

```bash
# Run local model via Ollama (free, offline)
ollama run llama3.1

# Sub-agent pakai Ollama untuk task simple
# Main agent tetep bisa pakai model lain
```

---

## 📊 Impact Summary

```
┌──────────────────────────────────────────────────────┐
│                  IMPACT ANALYSIS                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  🎯 Affected Users:                                  │
│     • Kimi K2.5 users (kimi-coding/k2p5)            │
│     • Heavy tool users (exec, browser, file ops)    │
│                                                      │
│  📉 Severity: HIGH 🔴                                │
│     • Tool execution unreliable                     │
│     • Bisa kasih fake "success" padahal gak jalan   │
│     • Automation jadi untrustworthy                 │
│                                                      │
│  ✅ Solution:                                        │
│     • Downgrade ke 2026.3.2                         │
│     • Atau switch ke Gemini/GLM sementara           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🎓 Lessons Learned

```
┌─────────────────────────────────────────────────────────┐
│  💡 TAKEAWAYS                                          │
│                                                         │
│  1. Jangan buru-buru update stable release terbaru    │
│     → Wait 1-2 minggu, lihat community feedback       │
│                                                         │
│  2. Kalau tool calling penting buat workflow:         │
│     → Test dulu di dev environment                    │
│     → Backup config sebelum update                    │
│                                                         │
│  3. Know your rollback:                               │
│     → npm install -g openclaw@VERSION                 │
│     → Simpan versi yang works di catatan              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Referensi

| Resource | Link |
|----------|------|
| Original Issue #41297 | https://github.com/openclaw/openclaw/issues/41297 |
| Original Issue #39907 | https://github.com/openclaw/openclaw/issues/39907 |
| Related Issue #40157 | https://github.com/openclaw/openclaw/issues/40157 |
| OpenClaw Releases | https://github.com/openclaw/openclaw/releases |

---

## 🙏 Credits

Thanks to OpenClaw community yang report dan investigate issue ini — especially yang udah trace sampe root cause di response parser! 🎉

---

> **Last Updated:** March 11, 2026  
> **Author:** OpenClaw Sumopod Community  
> **Applies to:** OpenClaw 2026.3.7, 2026.3.8 + kimi-coding/k2p5

---

## 💬 Questions?

Ada pertanyaan atau butuh bantuan downgrade? Join:
- 🌏 OpenClaw Discord: https://discord.com/invite/clawd
- 💬 Tanya di Telegram: @RaditClaw_bot

**Stay safe, stay on 2026.3.2!** 🛡️
