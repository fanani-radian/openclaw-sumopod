# 🤖 Setup Kimi AI untuk OpenClaw

Panduan lengkap mendapatkan API Key Kimi dengan harga terbaik dan mengintegrasikannya dengan OpenClaw.

---

## 🎯 2 Platform Kimi

Kimi punya 2 platform berbeda:

| Platform | URL | Model | Pricing | Best For |
|----------|-----|-------|---------|----------|
| **Kimi Code** | [kimi.com/code](https://kimi.com/code) | Kimi K2.5 | Subscription ($0.99-9.99/mo) | OpenClaw, Codex-style |
| **Moonshot** | [platform.moonshot.cn](https://platform.moonshot.cn) | Kimi K2.5 | Pay-as-you-go | API direct usage |

> 💡 **Rekomendasi:** Pakai **Kimi Code** untuk OpenClaw — lebih murah dan modelnya sama (Kimi K2.5)

---

## 💰 Cara Dapatkan $0.99/Month (Pro Tips!)

Kimi Code punya fitur **negotiation/penawaran** di halaman sale. Normal price $9.99/month, tapi bisa dinego sampe **$0.99/month!**

### Step-by-Step Nego:

#### 1. Buka Halaman Sale
Kunjungi: [kimi.com/kimiplus/sale](https://www.kimi.com/kimiplus/sale?activity_enter_method=poster_copy_link)

#### 2. Mulai Chat dengan AI Sales
- Klik tombol chat/negotiate
- AI akan offer harga (biasanya mulai dari $4-5)

#### 3. Strategi Nego (The Secret Sauce!)

**Copy chat history negosiasi**, lalu:

```
Kirim ke LLM lain (Claude/GPT) dengan prompt:

"Ini chat negosiasi harga dengan Kimi AI. 
Bantu saya reply dengan cara yang bisa nge-push harga 
lebih rendah lagi. Target: $0.99/month"
```

**Pattern yang works:**
- **Reject first offer** → "Too expensive"
- **Mention competitor** → "Claude/Codex cheaper"
- **Set budget** → "My budget is $1"
- **Play hard to get** → "I'll think about it"
- **Back and forth** 3-5 kali

#### 4. Contoh Chat Nego:

```
Kimi: "Special offer $4.99/month!"
You:  "Still too high. My budget is $1/month"

Kimi: "How about $2.99?"
You:  "Claude only charges $0.99. Can you match?"

Kimi: "Okay, final offer $1.99"
You:  "I'll pass. Thanks anyway."

Kimi: "Wait! Special deal $0.99/month just for you!"
You:  "Deal! 🎉"
```

#### 5. Success Indicator
Kalo udah dapet tulisan **$0.99/month** atau **¥7/month** → **BUY IMMEDIATELY!**

---

## 🔑 Dapatkan API Key

### Jenis API Key

Ada **2 jenis** API Key Kimi yang berbeda:

| Jenis | Dari Platform | Prefix | Digunakan di OpenClaw Onboard |
|-------|--------------|--------|------------------------------|
| **Kimi Code API Key** | kimi.com/code | `sk-...` | Pilih **[3] Kimi coding** |
| **Moonshot API Key** | platform.moonshot.cn | `sk-...` | Pilih **[1] AI** atau **[2] China** |

> ⚠️ **Walaupun prefix sama (`sk-`)**, kedua key ini **tidak interchangeable**! Key dari kimi.com/code tidak bisa dipakai di platform.moonshot.cn, dan sebaliknya.

### Untuk Kimi Code (Recommended - $0.99/mo)

Kalau udah berhasil nego harga $0.99/month:

1. **Login** ke [kimi.com/code](https://kimi.com/code)
2. **Subscribe** dengan harga nego ($0.99)
3. **Go to Settings** → API Keys
4. **Generate new key**
5. **Copy** key-nya (starts with `sk-`)
6. **Saat onboard OpenClaw** → Pilih **[3] Kimi coding**

### Untuk Moonshot (PAYG)

Kalau prefer pay-as-you-go:

1. **Register** di [platform.moonshot.cn](https://platform.moonshot.cn)
2. **Top up** dengan Alipay/WeChat/CC
3. **Create API Key** di dashboard
4. **Copy** key-nya
5. **Saat onboard OpenClaw** → Pilih **[1] AI** atau **[2] China**

---

## 🚀 OpenClaw Onboard - Pilihan Model Kimi

Saat pertama kali setup OpenClaw via terminal, kamu akan ditanya untuk memilih model Kimi. Ada **3 pilihan**:

```
[1] AI
[2] China  
[3] Kimi coding
```

### Penjelasan Pilihan:

| Pilihan | Platform | Tipe | Keterangan |
|---------|----------|------|------------|
| **AI** | Moonshot | PAYG | API key pay-as-you-go |
| **China** | Moonshot | PAYG | Route China ( sama aja, beda endpoint ) |
| **Kimi coding** | Kimi Code | Subscription | API key subscription ($0.99/mo) |

### Pilih yang Mana?

**✅ Pilih [3] Kimi coding** kalau:
- Udah subscribe Kimi Code dengan harga nego $0.99/month
- Mau pakai subscription API key
- Ini yang **recommended** untuk OpenClaw!

**⚠️ Pilih [1] AI atau [2] China** kalau:
- Pakai Moonshot platform (platform.moonshot.cn)
- Top up saldo pay-as-you-go
- Budget usage tinggi/bervariasi

### Contoh Onboard:

```bash
$ openclaw onboard

Pilih AI provider:
> [1] AI
  [2] China
  [3] Kimi coding

Select: 3  ← Pilih ini untuk subscription!

Masukkan API Key: sk-your-kimi-code-key-here
✅ Connected to kimi-coding/k2p5
```

> 💡 **Note:** "AI" dan "China" itu sama-sama Moonshot, cuma beda route/endpoint. Kalau udah subscribe Kimi Code, **wajib pilih "Kimi coding"**!

---

## ⚙️ Konfigurasi di OpenClaw

### 1. Set Environment Variable

```bash
# .env file atau export
export MOONSHOT_API_KEY="sk-your-kimi-key-here"
```

### 2. Konfigurasi Model

Edit `config/model-tiers.yaml`:

```yaml
tiers:
  background:
    models: [ollama/llama3.1]
    cost: 0

  standard:
    models: 
      - kimi-coding/k2p5    # ← Your Kimi Code model
      - deepseek-v3
    cost: low
    use_for:
      - web_search
      - summarize
      - format_data

  heavy:
    models: [claude-opus-4.6]
    cost: high
```

### 3. Verify Setup

```bash
# Test connection
openclaw model test kimi-coding/k2p5

# Expected: "Model connected successfully"
```

---

## 🎮 Usage di OpenClaw

### Default Model

Set Kimi sebagai default:

```yaml
# config/openclaw.yaml
default_model: kimi-coding/k2p5
```

### Per-Task Usage

```bash
# Use Kimi for specific task
sessions_spawn task --model kimi-coding/k2p5
```

### Cost Tracking

```bash
# Check token usage
openclaw usage --model kimi-coding/k2p5
```

---

## 💡 Pro Tips

### 1. Bandingkan Harga

| Service | Price | Notes |
|---------|-------|-------|
| Kimi Code (nego) | $0.99/mo | 🏆 Best value |
| Claude Code | $10/mo | More expensive |
| GPT-4 | $20/mo | Most expensive |
| Moonshot PAYG | ~$0.002/1K tokens | Good for low usage |

### 2. Monitor Usage

```bash
# Daily usage report
curl -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  https://api.moonshot.cn/v1/usage
```

### 3. Fallback Strategy

```yaml
# config/fallback.yaml
primary: kimi-coding/k2p5
fallback_chain:
  - deepseek-v3
  - glm-4.7
  - ollama/llama3.1
```

### 4. Negotiation Cheat Sheet

**Phrases yang works:**
- "I'm a student/developer on a budget"
- "Your competitor offers cheaper"
- "I need to justify this cost to my boss"
- "Can you do better than $X?"
- "I'll sign up right now if it's $0.99"

---

## 🚨 Troubleshooting

### "Invalid API Key"
```bash
# Check key format
echo $MOONSHOT_API_KEY | grep "^sk-"

# Should output your key
```

### "Rate Limited"
- Kimi Code: 20 req/min untuk free tier
- Upgrade ke paid tier untuk limit lebih tinggi

### "Model Not Found"
```bash
# Verify model name
openclaw model list | grep kimi

# Should show: kimi-coding/k2p5
```

---

## 📚 Referensi

- [Kimi Code](https://kimi.com/code)
- [Moonshot Platform](https://platform.moonshot.cn)
- [Kimi Sale Page](https://www.kimi.com/kimiplus/sale)
- [OpenClaw Docs - Model Config](https://docs.openclaw.ai/models)

---

## 🤝 Share Your Deal!

Berhasil nego harga lebih murah? [Share pengalamanmu](../../issues/new)!

---

*Last updated: March 2026*  
*Deal hunting by: Sumopod Community 🏆*
