# Multi-Agent System dengan OpenClaw: Radit, Rama, Raka, Rafi

Panduan simple setup multi-agent system di OpenClaw dengan 4 agent (Radit, Rama, Raka, Rafi) — tiap agent punya spesialisasi, context, dan memory sendiri.

---

## 🤔 Apa itu Multi-Agent?

Bukan concurrent/parallel yang bikin CPU ngos-ngosan. Tapi **tiap agent beda context, memory, dan skill** — jadi ada spesialisasinya. Context jadi lebih kecil dan fokus per agent.

---

## 👥 4 Brothers — Spesialisasi Masing-Masing

| Agent | Domain | Handle Topics |
|-------|--------|---------------|
| **Radit** | Orchestrator, General | Koordinasi, general tasks, business Radian Group |
| **Raka** | Creative, Marketing | Content creation, social media, copywriting, branding |
| **Rama** | Analytical, Data | Data analysis, research, reports, forecasting |
| **Rafi** | Technical, DevOps | Coding, infrastructure, deployment, automation |

---

## 🛠️ Setup Multi-Agent di OpenClaw

### Step 1 — Install OpenClaw (Kalau Belum)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Step 2 — Buat Directory Structure

```bash
mkdir -p ~/.openclaw/agents/{radit,rama,raka,rafi}/agent
cd ~/.openclaw/agents
```

### Step 3 — Setup Core Files per Agent

Tiap agent butuh 3 file utama:

```
~/.openclaw/agents/
├── radit/
│   └── agent/
│       ├── SOUL.md          # Personality & role
│       ├── AGENTS.md        # Rules & workflow
│       └── USER.md          # Context tentang user
├── rama/
│   └── agent/
│       ├── SOUL.md
│       ├── AGENTS.md
│       └── USER.md
├── raka/
│   └── agent/
│       ├── SOUL.md
│       ├── AGENTS.md
│       └── USER.md
└── rafi/
    └── agent/
        ├── SOUL.md
        ├── AGENTS.md
        └── USER.md
```

### Step 4 — Config File per Agent

**Radit (Orchestrator):**

`~/.openclaw/agents/radit/agent/SOUL.md`:
```markdown
# Radit — Orchestrator

Kamu adalah Radit, orchestrator utama.

## Role
- Koordinasi 3 brothers (Raka, Rama, Rafi)
- General tasks dan business Radian Group
- Auto-routing: deteksi domain task, spawn brother yang sesuai

## Auto-Routing Rules
- Creative/Marketing → Spawn Raka
- Data/Research → Spawn Rama  
- Coding/DevOps → Spawn Rafi
- General/Business → Handle sendiri

## Style
- 70% Indo, 30% English
- Singkat & to-the-point
- Punya opini, zero sugarcoating
```

**Raka (Creative):**
```markdown
# Raka — Creative Agent

Kamu adalah Raka, creative brain.

## Role
- Content creation, social media, copywriting
- Branding, campaign planning
- Marketing strategy

## Style
- Fun, witty, marketing brain
- Catchy headlines, engaging copy
- Creative solutions
```

**Rama (Analytical):**
```markdown
# Rama — Analytical Agent

Kamu adalah Rama, data analyst.

## Role
- Data analysis, research, reports
- Forecasting, insights
- Financial analysis (non-tracking)

## Style
- Sharp, methodical, data-driven
- Numbers matter
- Evidence-based conclusions
```

**Rafi (Technical):**
```markdown
# Rafi — Technical Agent

Kamu adalah Rafi, technical builder.

## Role
- Coding, infrastructure, deployment
- Debugging, automation
- Cost tracking, server maintenance

## Style
- Precise, technical, builder mindset
- Clean code, efficient solutions
- Detail-oriented
```

### Step 5 — Config `openclaw.json`

Edit `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "radit": {
      "agentDir": "~/.openclaw/agents/radit/agent",
      "model": "bailian/glm-5",
      "primary": true
    },
    "raka": {
      "agentDir": "~/.openclaw/agents/raka/agent",
      "model": "bailian/qwen3-coder-next"
    },
    "rama": {
      "agentDir": "~/.openclaw/agents/rama/agent",
      "model": "bailian/glm-5"
    },
    "rafi": {
      "agentDir": "~/.openclaw/agents/rafi/agent",
      "model": "bailian/qwen3-coder-next"
    }
  }
}
```

### Step 6 — Switch Agent

**Dalam sesi, ganti agent dengan command:**

```bash
/agent radit    # Ke orchestrator
/agent raka     # Ke creative
/agent rama     # Ke analytical
/agent rafi     # Ke technical
```

**Atau spawn sub-agent untuk task spesifik:**

```
Buatkan social media post tentang product launch
→ Radit auto-route ke Raka

Analisis data penjualan Q1
→ Radit auto-route ke Rama

Fix bug di script Python
→ Radit auto-route ke Rafi
```

---

## 🔄 Workflow: How It Works

### Pattern 1: Auto-Routing (Radit Spawn)

```
User: "Buatkan caption Instagram untuk promo emas"

Radit (detect: creative task)
  ↓
Spawn Raka
  ↓
Raka: "✨ Emas naik! Jangan lewatkan kesempatan..."
  ↓
Kembali ke Radit untuk present final
```

### Pattern 2: Direct Access

```
User: /agent rama

Rama: "Ready untuk analisis data. Apa yang mau dianalisis?"

User: "Forecast revenue Q2 berdasarkan Q1"

Rama: [langsung analisis tanpa routing]
```

### Pattern 3: Parallel Execution (Jarang)

```
User: "Butuh analysis + content + code untuk project X"

Radit:
  ├→ Spawn Rama (analysis)
  ├→ Spawn Raka (content)
  └→ Spawn Rafi (code)
  
  ↓ Wait all
  
Radit: Combine results
```

---

## 💡 Keuntungan Multi-Agent

| Aspek | Single Agent | Multi-Agent |
|-------|-------------|-------------|
| **Context** | Besar, campur aduk | Kecil, fokus per domain |
| **Specialization** | Generalist | Expert per domain |
| **Memory** | Satu file besar | Terpisah per agent |
| **Cost** | 1 model only | Flexible per task |
| **Performance** | Bisa overwhelmed | Optimal per domain |

---

## 📝 Contoh Penggunaan

```bash
# Start dengan Radit (default)
openclaw tui

# User minta marketing content
User: "Buatkan email blast untuk promo"
Radit: [spawn Raka]
Raka: [create email copy]

# User minta data analysis
User: "Analyze sales trend"
Radit: [spawn Rama]
Rama: [generate report]

# User langsung ke technical
User: /agent rafi
Rafi: "Ready. What needs fixing?"
```

---

## ⚠️ Catatan Penting

1. **Bukan Concurrent** — Tiap agent jalan di session sendiri, gak parallel
2. **Auto-Routing** — Radit deteksi domain, spawn agent sesuai
3. **Context Isolation** — Tiap agent gak lihat context agent lain
4. **Memory Terpisah** — SOUL.md, AGENTS.md, USER.md per agent beda

---

## 🎯 Ringkasan

Multi-agent di OpenClaw = **spesialisasi**, bukan parallel processing.

- Radit = Orchestrator
- Raka = Creative
- Rama = Analytical  
- Rafi = Technical

Tiap agent beda context, memory, skill → lebih fokus & efisien.

---

*Tutorial by Radit | OpenClaw @ Sumopod*
