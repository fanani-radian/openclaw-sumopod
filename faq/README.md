# ❓ FAQ - Frequently Asked Questions

## General

### Q: Apa itu OpenClaw?
**A:** OpenClaw adalah AI agent framework yang memungkinkan kamu membuat personal AI assistant yang bisa mengotomatisasi tugas, mengintegrasikan berbagai tools, dan bekerja secara autonomous.

### Q: Bedanya OpenClaw dengan ChatGPT biasa?
**A:** 
| Feature | ChatGPT | OpenClaw |
|---------|---------|----------|
| Persistent memory | ❌ | ✅ |
| Custom tools | ❌ | ✅ |
| Autonomous execution | ❌ | ✅ |
| Sub-agents | ❌ | ✅ |
| Local/self-hosted | ❌ | ✅ |

### Q: Berapa biaya pakai OpenClaw?
**A:** OpenClaw itself gratis (open source). Biaya tergantung:
- VPS/cloud hosting (jika self-host)
- API usage (OpenAI, Claude, dll)
- Bisa di-minimize pakai local models (Ollama)

---

## Setup & Install

### Q: Error "command not found: openclaw"
**A:**
```bash
# Pastikan global bin di PATH
export PATH="$PATH:$(npm bin -g)"
# atau
npm config set prefix ~/.local
```

### Q: Gateway failed to start
**A:** Check:
1. Port 8080 (atau yang dikonfigurasi) tidak dipakai
2. Environment variables sudah di-set
3. Dependencies terinstall: `npm install`

### Q: Cara update OpenClaw?
**A:**
```bash
npm update -g openclaw
# atau
npm install -g openclaw@latest
```

---

## Configuration

### Q: Dimana simpan API keys?
**A:** Di `.env` file atau secure keyring. Jangan pernah commit ke GitHub!

```bash
# .env
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
```

### Q: Cara ganti model AI?
**A:** Edit `config/openclaw/model.yaml` atau set via env:
```bash
export OPENCLAW_DEFAULT_MODEL=claude-3-opus-20240229
```

### Q: Bisa pakai model local?
**A:** Bisa! Setup Ollama:
```bash
ollama pull llama3.1
# Set di config: model: ollama/llama3.1
```

---

## Usage

### Q: Agent tidak ingat percakapan sebelumnya
**A:** Pastikan:
1. `MEMORY.md` sudah dibuat
2. Di-load di session (otomatis di main session)
3. Jangan delete file memory/*.md

### Q: Cara tambah skill baru?
**A:**
```bash
# Clone dari clawhub
openclaw skills install skill-name

# Atau manual
git clone https://github.com/user/skill-repo skills/skill-name
```

### Q: Skill error / tidak jalan
**A:** Check:
1. Dependencies skill sudah diinstall
2. Permission script: `chmod +x skills/*/scripts/*`
3. Log error: `openclaw logs --skill skill-name`

---

## Troubleshooting

### Q: Memory usage tinggi
**A:** 
- Compact session: `/compact`
- Restart gateway: `openclaw gateway restart`
- Use cheaper models untuk background tasks

### Q: Token usage mahal
**A:**
- Delegate ke sub-agents dengan model lebih murah
- Use local models (Ollama) untuk simple tasks
- Set token limits di config

### Q: Cron jobs tidak jalan
**A:**
```bash
# Check status
openclaw cron status

# Restart cron
openclaw cron restart

# Check logs
openclaw cron logs
```

---

## Contributing

### Q: Cara share config/sendiri?
**A:** Fork repo ini, tambah di folder `docs/config/examples/`, buat PR.

### Q: Bisa share tanpa expose API keys?
**A:** Pastikan `.env` di `.gitignore`. Share only config templates.

---

## Resources

- [OpenClaw Docs](https://docs.openclaw.ai)
- [GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [Discord Community](https://discord.gg/clawd)

---

*Punya pertanyaan lain? [Buat issue](../../issues/new) atau tanya di Discord!*
