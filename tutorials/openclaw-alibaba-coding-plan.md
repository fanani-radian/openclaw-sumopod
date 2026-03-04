# OpenClaw + Alibaba Cloud Coding Plan: 8 Model AI dengan 1 API Key (Mulai $5/bulan)

Panduan lengkap setup OpenClaw dengan Alibaba Cloud Model Studio Coding Plan untuk akses 8 model AI frontier sekaligus — hemat, fleksibel, dan gampang switch model di tengah sesi.

---

## 🤔 Kenapa Setup Ini?

Kebanyakan orang pakai OpenClaw dengan bayar per provider:
- Z.AI untuk GLM
- Anthropic untuk Claude  
- OpenAI untuk GPT

Tapi ada cara lebih baik: **satu API key, 8 model AI**, flat rate mulai dari $5/bulan.

### 8 Model yang Didapat:

| Model | Kelebihan | Context Window |
|-------|-----------|----------------|
| **GLM-5** | Agentic performance terbaik, tool calling solid | 200K |
| **Qwen3.5-Plus** | All-rounder, support image input | 1M |
| **Qwen3-Max** | Heavy reasoning, "think hard" model | 262K |
| **Qwen3-Coder-Next** | Coding & refactoring | 262K |
| **Qwen3-Coder-Plus** | Coding dengan output panjang | 1M |
| **MiniMax M2.5** | Cepat & murah untuk bulk tasks | 1M |
| **Kimi K2.5** | Multimodal (text + image) | 262K |
| **GLM-4.7** | Fallback solid, ringan | 200K |

**Keunggulan utama:** Bisa ganti model di tengah sesi dengan satu command!

---

## 📋 Step-by-Step Setup

### Step 1 — Dapatkan API Key Coding Plan

1. Buka [Alibaba Cloud Model Studio](https://modelstudio.console.alibabacloud.com) (pilih region Singapore)
2. Register atau login
3. Subscribe ke **Coding Plan** — mulai $5/bulan, sampai 90,000 requests
4. Masuk ke API Keys management → Create new API key
5. Copy API key-nya segera

⚠️ **Catatan Penting:**
- User baru dapat free quota untuk tiap model
- Aktifkan "Stop on Free Quota Exhaustion" di region Singapore biar gak kena charge tiba-tiba

---

### Step 2 — Install OpenClaw

**macOS/Linux:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**Prerequisites:** Node.js v22 atau lebih baru. Cek dengan `node -v`.

**Saat onboarding, pilih:**

| Konfigurasi | Pilihan |
|-------------|---------|
| "Powerful and inherently risky. Continue?" | Yes |
| Onboarding mode | QuickStart |
| Model/auth provider | Skip for now |
| Filter models by provider | All providers |
| Default model | Use defaults |
| Select channel | Skip for now |
| Configure skills? | No |
| Enable hooks? | Spacebar → Enter |
| How to hatch your bot? | Hatch in TUI |

Kita skip model provider karena akan setup manual dengan konfigurasi multi-model lengkap.

---

### Step 3 — Konfigurasi Coding Plan Provider

Buka file konfigurasi:

**Via Web UI:**
```bash
openclaw dashboard
```
Lalu navigasi ke **Config > Raw** di sidebar kiri.

**Via Terminal:**
```bash
nano ~/.openclaw/openclaw.json
```

Tambahkan konfigurasi berikut. **Ganti `YOUR_API_KEY` dengan API key asli kamu:**

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding-intl.dashscope.aliyuncs.com/v1",
        "apiKey": "YOUR_API_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 1000000,
            "maxTokens": 65536
          },
          {
            "id": "qwen3-max-2026-01-23",
            "name": "qwen3-max-2026-01-23",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 262144,
            "maxTokens": 65536
          },
          {
            "id": "qwen3-coder-next",
            "name": "qwen3-coder-next",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 262144,
            "maxTokens": 65536
          },
          {
            "id": "qwen3-coder-plus",
            "name": "qwen3-coder-plus",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 1000000,
            "maxTokens": 65536
          },
          {
            "id": "MiniMax-M2.5",
            "name": "MiniMax-M2.5",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 1000000,
            "maxTokens": 65536
          },
          {
            "id": "glm-5",
            "name": "glm-5",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 202752,
            "maxTokens": 16384
          },
          {
            "id": "glm-4.7",
            "name": "glm-4.7",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 202752,
            "maxTokens": 16384
          },
          {
            "id": "kimi-k2.5",
            "name": "kimi-k2.5",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 262144,
            "maxTokens": 32768
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/glm-5"
      },
      "models": {
        "bailian/qwen3.5-plus": {},
        "bailian/qwen3-max-2026-01-23": {},
        "bailian/qwen3-coder-next": {},
        "bailian/qwen3-coder-plus": {},
        "bailian/MiniMax-M2.5": {},
        "bailian/glm-5": {},
        "bailian/glm-4.7": {},
        "bailian/kimi-k2.5": {}
      }
    }
  },
  "gateway": {
    "mode": "local"
  }
}
```

💡 **Tips:** Primary model di-set ke `glm-5`. Kalau mau ganti default, ubah field `"primary"` ke model lain.

---

### Step 4 — Apply dan Restart

**Via Web UI:**
- Klik **Save** di pojok kanan atas
- Klik **Update**

**Via Terminal:**
```bash
openclaw gateway restart
```

**Verifikasi model terdeteksi:**
```bash
openclaw models list
```

Harusnya muncul semua 8 model di bawah provider `bailian`.

---

### Step 5 — Mulai Pakai

**Web UI:**
```bash
openclaw dashboard
```

**Terminal UI:**
```bash
openclaw tui
```

**Ganti model di tengah sesi:**
```
/model qwen3-coder-next
```

Done! Sekarang kamu punya 8 model AI dalam satu interface. 🎉

---

## ⚠️ Gotchas & Tips Penting

### 1. `"reasoning": false` adalah WAJIB
Jangan set `reasoning: true` — response bakal kosong. Coding Plan endpoint gak support thinking mode.

### 2. Pakai International Endpoint
`baseUrl` harus: `https://coding-intl.dashscope.aliyuncs.com/v1`

Jangan mix region antara API key dan base URL — bakal error autentikasi.

### 3. HTTP 401 Error?
Dua kemungkinan:
- API key salah atau expired
- Config cached dari provider sebelumnya

**Fix:** Hapus `providers.bailian` dari `~/.openclaw/agents/main/agent/models.json`, lalu restart.

### 4. Cost = 0 (Flat Rate)
Semua cost di-set 0 karena Coding Plan flat-rate. OpenClaw gak akan hitung token, tapi quota asli ~90,000 requests/bulan.

### 5. GLM-5 maxTokens Lebih Kecil
Di endpoint ini max 16,384 (native Z.AI bisa lebih). Untuk code generation panjang, pakai Qwen3-Coder-Plus (65,536 tokens).

### 6. Image Input Support
Hanya **Qwen3.5-Plus** dan **Kimi K2.5** yang support image input. Model lain text-only.

### 7. Security: Ganti Default Port
Kalau running di VPS, cek port dengan `openclaw dashboard` dan ganti kalau perlu.

### 8. Troubleshooting
Kalau ada masalah setelah ganti config:
```bash
openclaw gateway stop
# tunggu 3 detik
openclaw gateway start
```
Clean restart fix banyak binding issues.

---

## 🎯 Strategi Rotasi Model (Rekomendasi)

Setelah coba semua 8 model, ini strategi yang works:

| Skenario | Model | Kenapa |
|----------|-------|--------|
| **Daily driver** | `bailian/glm-5` | Agentic performance terbaik, handle 90% task |
| **Heavy coding** | `/model qwen3-coder-next` | Purpose-built, cepat, output clean |
| **Dokumen besar** | `/model qwen3.5-plus` | 1M context window = no problem |
| **Image + text** | `/model kimi-k2.5` | Multimodal solid |
| **Bulk tasks** | `/model MiniMax-M2.5` | Cepat, murah, 1M context |
| **Fallback** | `bailian/glm-4.7` | Battle-tested kalau yang lain error |

---

## 📝 Ringkasan

**Alibaba Cloud Coding Plan** = 8 frontier model (GLM-5, Qwen3.5-Plus, Kimi K2.5, MiniMax M2.5, dll) dengan flat fee mulai $5/bulan.

- Satu API key
- Satu config file
- Switch model dengan `/model`
- JSON config di atas tinggal copy-paste + masukin API key

Ini cara paling cost-effective untuk jalanin OpenClaw dengan variasi model saat ini.

---

## 📚 Referensi

- [Alibaba Cloud Model Studio](https://modelstudio.console.alibababcloud.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)

---

## 🙏 Attribution

> Tutorial ini diadaptasi dari post Reddit r/AIToolsPerformance oleh author anonim dengan modifikasi dan terjemahan oleh **Radit** (OpenClaw Assistant).
> 
> Original post: "OpenClaw + Alibaba Cloud Coding Plan: 8 Frontier Models, One API Key, From $5/month — Full Setup Guide"
> 
> *Thanks to the original author for sharing this gem! 💎*

---

*Last updated: 5 Maret 2026*
