# Multi-Agent System dengan OpenClaw

Panduan setup multi-agent system di OpenClaw dengan multiple agent — tiap agent punya spesialisasi, context, dan memory sendiri.

---

## 🤔 Apa itu Multi-Agent?

Bukan concurrent/parallel yang bikin CPU ngos-ngosan. Tapi **tiap agent beda context, memory, dan skill** — jadi ada spesialisasinya. Context jadi lebih kecil dan fokus per agent.

---

## 👥 Contoh Struktur 4 Agent

| Agent | Domain | Handle Topics |
|-------|--------|---------------|
| **Agent 1** | Orchestrator, General | Koordinasi, general tasks, routing ke agent lain |
| **Agent 2** | Creative, Marketing | Content creation, social media, copywriting, branding |
| **Agent 3** | Analytical, Data | Data analysis, research, reports, forecasting |
| **Agent 4** | Technical, DevOps | Coding, infrastructure, deployment, automation |

---

## 🛠️ Setup Multi-Agent di OpenClaw

### Step 1 — Install OpenClaw (Kalau Belum)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Step 2 — Buat Directory Structure

```bash
mkdir -p ~/.openclaw/agents/{agent1,agent2,agent3,agent4}/agent
cd ~/.openclaw/agents
```

### Step 3 — Setup Core Files per Agent

Tiap agent butuh 3 file utama:

```
~/.openclaw/agents/
├── agent1/          # Orchestrator
│   └── agent/
│       ├── SOUL.md          # Personality & role
│       ├── AGENTS.md        # Rules & workflow
│       └── USER.md          # Context tentang user
├── agent2/          # Creative
│   └── agent/
│       ├── SOUL.md
│       ├── AGENTS.md
│       └── USER.md
├── agent3/          # Analytical
│   └── agent/
│       ├── SOUL.md
│       ├── AGENTS.md
│       └── USER.md
└── agent4/          # Technical
    └── agent/
        ├── SOUL.md
        ├── AGENTS.md
        └── USER.md
```

### Step 4 — Config File per Agent

**Agent 1 (Orchestrator):**

`~/.openclaw/agents/agent1/agent/SOUL.md`:
```markdown
# Agent 1 — Orchestrator

Kamu adalah orchestrator utama.

## Role
- Koordinasi agent lain (Agent 2, 3, 4)
- General tasks dan routing
- Auto-routing: deteksi domain task, spawn agent yang sesuai

## Auto-Routing Rules
- Creative/Marketing → Spawn Agent 2
- Data/Research → Spawn Agent 3
- Coding/DevOps → Spawn Agent 4
- General/Business → Handle sendiri

## Style
- Singkat & to-the-point
- Punya opini, zero sugarcoating
```

**Agent 2 (Creative):**
```markdown
# Agent 2 — Creative Agent

Kamu adalah creative brain.

## Role
- Content creation, social media, copywriting
- Branding, campaign planning
- Marketing strategy

## Style
- Fun, witty, marketing brain
- Catchy headlines, engaging copy
- Creative solutions
```

**Agent 3 (Analytical):**
```markdown
# Agent 3 — Analytical Agent

Kamu adalah data analyst.

## Role
- Data analysis, research, reports
- Forecasting, insights
- Financial analysis

## Style
- Sharp, methodical, data-driven
- Numbers matter
- Evidence-based conclusions
```

**Agent 4 (Technical):**
```markdown
# Agent 4 — Technical Agent

Kamu adalah technical builder.

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
    "agent1": {
      "agentDir": "~/.openclaw/agents/agent1/agent",
      "model": "bailian/glm-5",
      "primary": true
    },
    "agent2": {
      "agentDir": "~/.openclaw/agents/agent2/agent",
      "model": "bailian/qwen3-coder-next"
    },
    "agent3": {
      "agentDir": "~/.openclaw/agents/agent3/agent",
      "model": "bailian/glm-5"
    },
    "agent4": {
      "agentDir": "~/.openclaw/agents/agent4/agent",
      "model": "bailian/qwen3-coder-next"
    }
  }
}
```

### Step 6 — Switch Agent

**Dalam sesi, ganti agent dengan command:**

```bash
/agent agent1    # Ke orchestrator
/agent agent2    # Ke creative
/agent agent3    # Ke analytical
/agent agent4    # Ke technical
```

**Atau spawn sub-agent untuk task spesifik:**

```
Buatkan social media post tentang product launch
→ Agent 1 auto-route ke Agent 2

Analisis data penjualan Q1
→ Agent 1 auto-route ke Agent 3

Fix bug di script Python
→ Agent 1 auto-route ke Agent 4
```

---

## 🔄 Workflow: How It Works

### Pattern 1: Auto-Routing (Agent 1 Spawn)

```
User: "Buatkan caption Instagram untuk promo"

Agent 1 (detect: creative task)
  ↓
Spawn Agent 2
  ↓
Agent 2: "✨ Promo spesial! Jangan lewatkan..."
  ↓
Kembali ke Agent 1 untuk present final
```

### Pattern 2: Direct Access

```
User: /agent agent3

Agent 3: "Ready untuk analisis data. Apa yang mau dianalisis?"

User: "Forecast revenue Q2 berdasarkan Q1"

Agent 3: [langsung analisis tanpa routing]
```

### Pattern 3: Parallel Execution (Jarang)

```
User: "Butuh analysis + content + code untuk project X"

Agent 1:
  ├→ Spawn Agent 3 (analysis)
  ├→ Spawn Agent 2 (content)
  └→ Spawn Agent 4 (code)
  
  ↓ Wait all
  
Agent 1: Combine results
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
# Start dengan Agent 1 (default)
openclaw tui

# User minta marketing content
User: "Buatkan email blast untuk promo"
Agent 1: [spawn Agent 2]
Agent 2: [create email copy]

# User minta data analysis
User: "Analyze sales trend"
Agent 1: [spawn Agent 3]
Agent 3: [generate report]

# User langsung ke technical
User: /agent agent4
Agent 4: "Ready. What needs fixing?"
```

---

## ⚠️ Catatan Penting

1. **Bukan Concurrent** — Tiap agent jalan di session sendiri, gak parallel
2. **Auto-Routing** — Agent 1 deteksi domain, spawn agent sesuai
3. **Context Isolation** — Tiap agent gak lihat context agent lain
4. **Memory Terpisah** — SOUL.md, AGENTS.md, USER.md per agent beda

---

## 🎯 Ringkasan

Multi-agent di OpenClaw = **spesialisasi**, bukan parallel processing.

- Agent 1 = Orchestrator
- Agent 2 = Creative
- Agent 3 = Analytical
- Agent 4 = Technical

Tiap agent beda context, memory, skill → lebih fokus & efisien.

---

*Tutorial untuk OpenClaw Multi-Agent System*
