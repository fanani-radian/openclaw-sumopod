# 🚀 Getting Started

## Instalasi OpenClaw

### Prerequisites

- Node.js 18+ / Python 3.10+
- Git
- (Optional) Docker

### Install via npm

```bash
npm install -g openclaw
```

### 📊 Installation Flowchart

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e3f2fd', 'primaryTextColor': '#1565c0', 'primaryBorderColor': '#1976d2', 'lineColor': '#424242', 'secondaryColor': '#c8e6c9', 'tertiaryColor': '#fff3e0'}}}%%
flowchart TD
    A[🖥️ Check Prerequisites] --> B{✅ Node 18+?}
    B -->|Yes| C[📦 Install OpenClaw]
    B -->|No| D[⬆️ Upgrade Node.js]
    D --> C
    C --> E[📁 Clone Workspace]
    E --> F[📥 Install Dependencies]
    F --> G[⚙️ Configure .env]
    G --> H[🚀 Start Gateway]
    H --> I{✨ Running?}
    I -->|Yes| J[🎉 Ready to Use!]
    I -->|No| K[🔧 Troubleshoot]
    K --> H
    
    style A fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style B fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style C fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    style J fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    style K fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
```

### Setup Pertama

1. **Clone workspace template:**
   ```bash
   git clone https://github.com/openclaw/workspace-template my-workspace
   cd my-workspace
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env dengan API keys yang diperlukan
   ```

4. **Start OpenClaw:**
   ```bash
   openclaw gateway start
   ```

---

## 📂 Workspace Structure Diagram

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f3e5f5', 'primaryTextColor': '#7b1fa2', 'primaryBorderColor': '#9c27b0'}}}%%
flowchart TB
    subgraph WS["📁 my-workspace/"]
        direction TB
        
        subgraph Core["⚡ Core Files"]
            AGENTS["👤 AGENTS.md<br/>Tentang agent"]
            USER["👥 USER.md<br/>Profil user"]
            SOUL["🎭 SOUL.md<br/>Personality"]
            MEMORY["🧠 MEMORY.md<br/>Long-term memory"]
        end
        
        subgraph Config["⚙️ Configuration"]
            TOOLS["🛠️ TOOLS.md<br/>Available tools"]
            HB["💓 HEARTBEAT.md<br/>Periodic tasks"]
            ENV["🔐 .env<br/>Environment vars"]
        end
        
        subgraph Dirs["📂 Directories"]
            CFG["config/"]
            SKILLS["skills/"]
            MEM["memory/"]
            SCRIPTS["scripts/"]
        end
    end
    
    AGENTS --> TOOLS
    USER --> MEMORY
    SOUL --> HB
    
    style Core fill:#e3f2fd,stroke:#1976d2
    style Config fill:#fff3e0,stroke:#f57c00
    style Dirs fill:#c8e6c9,stroke:#388e3c
    style WS fill:#fafafa,stroke:#424242,stroke-width:3px
```

---

## Struktur Workspace

```
my-workspace/
├── AGENTS.md          # Tentang agent kamu
├── USER.md            # Profil user
├── SOUL.md            # Personality agent
├── MEMORY.md          # Memori jangka panjang
├── TOOLS.md           # Tools yang tersedia
├── HEARTBEAT.md       # Task periodic
├── config/            # Konfigurasi
├── skills/            # Custom skills
├── memory/            # Daily logs
└── scripts/           # Automation scripts
```

---

## Konsep Dasar

### 1. Skills
Skills adalah kemampuan spesifik yang bisa dipelajari agent.

Contoh struktur skill:
```
skills/my-skill/
├── SKILL.md           # Dokumentasi skill
├── README.md          # Cara pakai
└── scripts/
    └── run.sh         # Entry point
```

### 2. Memory System

- **MEMORY.md** - Memori jangka panjang (loaded di main session)
- **memory/YYYY-MM-DD.md** - Daily logs
- **HEARTBEAT.md** - Task yang dicek secara periodic

### 3. Sub-agents

Untuk tugas kompleks, spawn sub-agents:

```bash
# Contoh dari dalam session
sessions_spawn with runtime="subagent" untuk parallel execution
```

---

## 🔄 Memory & Skills Flow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e8f5e9', 'primaryTextColor': '#2e7d32', 'primaryBorderColor': '#4caf50'}}}%%
flowchart LR
    subgraph User["👤 User Interaction"]
        Q["❓ Ask Question"]
        A["✅ Get Answer"]
    end
    
    subgraph Agent["🤖 OpenClaw Agent"]
        M["🧠 Load MEMORY.md"]
        S["📚 Check Skills"]
        P["⚡ Process"]
    end
    
    subgraph Storage["💾 Persistent Storage"]
        MEM[("🗄️ MEMORY.md<br/>Long-term facts")]
        DAILY[("📅 memory/YYYY-MM-DD.md<br/>Daily logs")]
        SK[("🛠️ skills/<br/>Custom capabilities")]
    end
    
    Q --> M
    M --> MEM
    M --> DAILY
    S --> SK
    M --> P
    S --> P
    P --> A
    
    style User fill:#e3f2fd,stroke:#1976d2
    style Agent fill:#fff3e0,stroke:#f57c00
    style Storage fill:#f3e5f5,stroke:#9c27b0
```

---

## Next Steps

- [🤖 Setup Kimi AI](./kimi-setup.md) - Dapatkan API Key Kimi dengan harga $0.99/month!
- [🔧 Setup Gog CLI](./gog-setup.md) - Integrasi Google Workspace (Gmail, Calendar, Drive)!
- [📱 Setup Telegram Bot](./telegram-setup.md) - Hubungkan OpenClaw dengan Telegram!
- [🖥️ Install di Windows](./windows-install.md) - Tutorial lengkap Windows install + auto-start + management!
- [🔄 Sync Memory ke GitHub](./github-sync.md) - Sinkronisasi memory antar device/PC/VPS!
- [Konfigurasi Skills](../config/README.md)
- [Contoh Use Cases](../use-cases/README.md)
- [Tips & Tricks](../tips-tricks/README.md)
