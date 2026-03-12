# 🌐 Resources & API Providers

Kumpulan resource, panduan, dan daftar provider AI API untuk OpenClaw.

---

## 📚 Panduan OpenClaw

| Resource | Link | Deskripsi |
|----------|------|-----------|
| **Sumopod Dashboard** | https://sumopod.com/dashboard/learn | Panduan lengkap (login required) |
| **GitHub Repository** | https://github.com/fanani-radian/openclaw-sumopod | Kumpulan tutorial dan use cases |
| **Official Docs** | https://docs.openclaw.ai | Dokumentasi resmi OpenClaw |
| **Community Discord** | https://discord.com/invite/clawd | Komunitas pengguna OpenClaw |

---

## 💰 API Murah / Free Tier

Kumpulan provider AI API dengan harga terjangkau atau free tier.

### 🆓 Free Tier

| Provider | Link | Detail |
|----------|------|--------|
| **Sumopod Free Tier** | https://sumopod.com/dashboard/ai/models | Cari model dengan harga $0.00 |
| **OpenRouter Free** | https://openrouter.ai/models?max_price=0 | Model gratis (rate limited) |

### 💵 Budget-Friendly

| Provider | Link | Harga | Models |
|----------|------|-------|--------|
| **BytePlus ModelArk** | https://www.byteplus.com/en/activity/codingplan | $5/bulan pertama | Seed, Kimi, GLM, GPT, DeepSeek |
| **Alibaba Coding Plan** | https://modelstudio.console.alibabacloud.com | $10/bulan | Qwen, GLM, Minimax, Kimi |

### 🎓 Student Discounts

| Provider | Link | Status |
|----------|------|--------|
| **GitHub Student Pack** | https://education.github.com/pack | Apply untuk akses tools gratis |

---

## 🏆 Flagship Models

Provider premium dengan model berkualitas tinggi.

| Provider | Link | Harga | Catatan |
|----------|------|-------|---------|
| **Kimi** | https://kimi.com | $19/bulan | Tool calling excellent |
| **GLM** | https://z.ai | $10/bulan | ByteDance, fast |
| **ChatGPT Plus** | https://chatgpt.com | Rp 349rb/bulan | GPT-4o, o1 |
| **Qwen** | https://modelstudio.console.alibabacloud.com | Per model | Tidak ada paket bulanan |
| **DeepSeek** | https://deepseek.ai/pricing | $0.14/1M tokens | Very cheap |

---

## 🎯 Rekomendasi Berdasarkan Use Case

| Use Case | Rekomendasi | Kenapa |
|----------|-------------|--------|
| **Budget tight** | Sumopod Free + OpenRouter Free | $0 cost |
| **Coding/Development** | BytePlus ModelArk | $5 dapat banyak model |
| **Production** | Kimi atau GLM | Stable, fast tool calling |
| **Experimentation** | Alibaba Coding Plan | $10 untuk test banyak model |
| **High volume** | DeepSeek | $0.14/1M tokens, very cheap |

---

## 📊 Perbandingan Harga (per 1M tokens)

| Model | Input | Output | Provider |
|-------|-------|--------|----------|
| Kimi K2.5 | ~$0.50 | ~$1.50 | Kimi / BytePlus |
| GLM-4.7 | ~$0.30 | ~$0.60 | GLM / Alibaba |
| GPT-4o | ~$2.50 | ~$10.00 | OpenAI |
| DeepSeek V3 | $0.14 | $0.28 | DeepSeek |
| Qwen 2.5 | ~$0.20 | ~$0.60 | Alibaba |

---

## ⚡ Quick Start dengan API Murah

### 1. BytePlus ModelArk (Recommended)

```bash
# Sign up: https://www.byteplus.com/en/activity/codingplan
# Get API key dari dashboard

# Setup di OpenClaw
openclaw config set model.primary "byteplus/seed"
openclaw config set model.fallbacks ["byteplus/kimi","byteplus/glm"]
```

### 2. Alibaba Coding Plan

```bash
# Sign up: https://modelstudio.console.alibabacloud.com
# Enable Coding Plan tab

# Setup di OpenClaw  
openclaw config set model.primary "alibaba/qwen-max"
```

### 3. Sumopod Free

```bash
# Login: https://sumopod.com/dashboard
# Pilih model dengan label "Free"

# Setup di OpenClaw
openclaw config set model.primary "sumopod/llama-3.1-free"
```

---

## 🔗 Useful Links

- **OpenClaw Releases:** https://github.com/openclaw/openclaw/releases
- **OpenClaw Issues:** https://github.com/openclaw/openclaw/issues
- **Model Pricing Comparison:** https://artificialanalysis.ai

---

> **Last Updated:** March 12, 2026  
> **Contributors:** OpenClaw Sumopod Community

---

## 🤝 Berkontribusi

Ada provider API baru atau harga berubah? 
- Fork repo ini
- Update file ini
- Submit Pull Request

**Note:** Harga dan availability dapat berubah sewaktu-waktu. Selalu cek website resmi provider untuk informasi terbaru.
