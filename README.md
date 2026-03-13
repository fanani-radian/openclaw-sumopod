# 🤖 OpenClaw Sumopod

Repositori komunitas untuk belajar, berbagi, dan berkolaborasi tentang [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework yang powerful dan fleksibel.

> **Sumopod Server**: Komunitas pengguna OpenClaw di Indonesia 🌏

---

## 🏗️ OpenClaw Architecture

```svg
<svg width="100%" viewBox="0 0 680 440">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  
  <rect x="20" y="20" width="640" height="400" rx="16" fill="var(--color-background-secondary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="40" y="45" class="th" font-size="16" fill="var(--color-text-primary)">🤖 OpenClaw System Architecture</text>
  
  <!-- User Interface Layer -->
  <rect x="40" y="60" width="600" height="70" rx="10" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="50" y="80" font-size="12" font-weight="500" fill="var(--color-text-primary)">👤 User Interfaces</text>
  
  <g class="node c-blue" onclick="sendPrompt('Tell me about Telegram integration with OpenClaw')">
    <rect x="60" y="95" width="100" height="26" rx="4" stroke-width="0.5"/>
    <text x="110" y="108" text-anchor="middle" dominant-baseline="central" font-size="11">Telegram</text>
  </g>
  
  <g class="node c-green" onclick="sendPrompt('Tell me about Discord integration with OpenClaw')">
    <rect x="175" y="95" width="100" height="26" rx="4" stroke-width="0.5"/>
    <text x="225" y="108" text-anchor="middle" dominant-baseline="central" font-size="11">Discord</text>
  </g>
  
  <g class="node c-purple" onclick="sendPrompt('Tell me about web interface in OpenClaw')">
    <rect x="290" y="95" width="100" height="26" rx="4" stroke-width="0.5"/>
    <text x="340" y="108" text-anchor="middle" dominant-baseline="central" font-size="11">Web UI</text>
  </g>
  
  <g class="node c-coral" onclick="sendPrompt('Tell me about CLI in OpenClaw')">
    <rect x="405" y="95" width="100" height="26" rx="4" stroke-width="0.5"/>
    <text x="455" y="108" text-anchor="middle" dominant-baseline="central" font-size="11">CLI</text>
  </g>
  
  <g class="node c-teal" onclick="sendPrompt('Tell me about API access in OpenClaw')">
    <rect x="520" y="95" width="100" height="26" rx="4" stroke-width="0.5"/>
    <text x="570" y="108" text-anchor="middle" dominant-baseline="central" font-size="11">API</text>
  </g>
  
  <!-- OpenClaw Core -->
  <rect x="40" y="145" width="280" height="120" rx="12" fill="var(--color-background-info)" stroke="var(--color-border-primary)" stroke-width="0.5"/>
  <text x="50" y="170" font-size="13" font-weight="500" fill="var(--color-text-primary)">⚙️ OpenClaw Core</text>
  
  <g class="node c-purple" onclick="sendPrompt('How does session management work in OpenClaw?')">
    <rect x="60" y="185" width="90" height="30" rx="4" stroke-width="0.5"/>
    <text x="105" y="200" text-anchor="middle" dominant-baseline="central" font-size="10">Session Mgr</text>
  </g>
  
  <g class="node c-teal" onclick="sendPrompt('How does tool routing work in OpenClaw?')">
    <rect x="160" y="185" width="70" height="30" rx="4" stroke-width="0.5"/>
    <text x="195" y="200" text-anchor="middle" dominant-baseline="central" font-size="10">Tools</text>
  </g>
  
  <g class="node c-coral" onclick="sendPrompt('How does skill management work in OpenClaw?')">
    <rect x="240" y="185" width="70" height="30" rx="4" stroke-width="0.5"/>
    <text x="275" y="200" text-anchor="middle" dominant-baseline="central" font-size="10">Skills</text>
  </g>
  
  <g class="node c-blue" onclick="sendPrompt('How does memory work in OpenClaw?')">
    <rect x="60" y="225" width="70" height="30" rx="4" stroke-width="0.5"/>
    <text x="95" y="240" text-anchor="middle" dominant-baseline="central" font-size="10">Memory</text>
  </g>
  
  <g class="node c-green" onclick="sendPrompt('How do subagents work in OpenClaw?')">
    <rect x="140" y="225" width="80" height="30" rx="4" stroke-width="0.5"/>
    <text x="180" y="240" text-anchor="middle" dominant-baseline="central" font-size="10">Subagents</text>
  </g>
  
  <g class="node c-amber" onclick="sendPrompt('How does model routing work in OpenClaw?')">
    <rect x="230" y="225" width="80" height="30" rx="4" stroke-width="0.5"/>
    <text x="270" y="240" text-anchor="middle" dominant-baseline="central" font-size="10">Models</text>
  </g>
  
  <!-- AI Models -->
  <rect x="340" y="145" width="140" height="120" rx="12" fill="var(--color-background-tertiary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="350" y="170" font-size="13" font-weight="500" fill="var(--color-text-primary)">🧠 AI Models</text>
  
  <g class="node c-purple" onclick="sendPrompt('Tell me about Kimi K2.5 in OpenClaw')">
    <rect x="355" y="185" width="110" height="24" rx="4" stroke-width="0.5"/>
    <text x="410" y="197" text-anchor="middle" dominant-baseline="central" font-size="10">Kimi K2.5</text>
  </g>
  
  <g class="node c-teal" onclick="sendPrompt('Tell me about Claude models in OpenClaw')">
    <rect x="355" y="215" width="110" height="24" rx="4" stroke-width="0.5"/>
    <text x="410" y="227" text-anchor="middle" dominant-baseline="central" font-size="10">Claude 3.5</text>
  </g>
  
  <g class="node c-gray" onclick="sendPrompt('Tell me about Gemini models in OpenClaw')">
    <rect x="355" y="245" width="110" height="24" rx="4" stroke-width="0.5"/>
    <text x="410" y="257" text-anchor="middle" dominant-baseline="central" font-size="10">Gemini Pro</text>
  </g>
  
  <!-- Integrations -->
  <rect x="500" y="145" width="140" height="120" rx="12" fill="var(--color-background-tertiary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="510" y="170" font-size="13" font-weight="500" fill="var(--color-text-primary)">🔌 Integrations</text>
  
  <g class="node c-blue" onclick="sendPrompt('How does GitHub integration work in OpenClaw?')">
    <rect x="515" y="185" width="110" height="24" rx="4" stroke-width="0.5"/>
    <text x="570" y="197" text-anchor="middle" dominant-baseline="central" font-size="10">GitHub</text>
  </g>
  
  <g class="node c-green" onclick="sendPrompt('How does Gmail integration work in OpenClaw?')">
    <rect x="515" y="215" width="110" height="24" rx="4" stroke-width="0.5"/>
    <text x="570" y="227" text-anchor="middle" dominant-baseline="central" font-size="10">Gmail</text>
  </g>
  
  <g class="node c-coral" onclick="sendPrompt('How do webhooks work in OpenClaw?')">
    <rect x="515" y="245" width="110" height="24" rx="4" stroke-width="0.5"/>
    <text x="570" y="257" text-anchor="middle" dominant-baseline="central" font-size="10">Webhooks</text>
  </g>
  
  <!-- Skills Ecosystem -->
  <rect x="40" y="280" width="600" height="120" rx="12" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="50" y="305" font-size="13" font-weight="500" fill="var(--color-text-primary)">🧩 Skills Ecosystem (200+ Skills)</text>
  
  <g class="node c-purple" onclick="sendPrompt('List popular automation skills in OpenClaw')">
    <rect x="60" y="325" width="80" height="26" rx="4" stroke-width="0.5"/>
    <text x="100" y="338" text-anchor="middle" dominant-baseline="central" font-size="10">Automation</text>
  </g>
  
  <g class="node c-teal" onclick="sendPrompt('List popular content creation skills in OpenClaw')">
    <rect x="150" y="325" width="80" height="26" rx="4" stroke-width="0.5"/>
    <text x="190" y="338" text-anchor="middle" dominant-baseline="central" font-size="10">Content</text>
  </g>
  
  <g class="node c-coral" onclick="sendPrompt('List popular data skills in OpenClaw')">
    <rect x="240" y="325" width="80" height="26" rx="4" stroke-width="0.5"/>
    <text x="280" y="338" text-anchor="middle" dominant-baseline="central" font-size="10">Data & Research</text>
  </g>
  
  <g class="node c-blue" onclick="sendPrompt('List popular monitoring skills in OpenClaw')">
    <rect x="330" y="325" width="80" height="26" rx="4" stroke-width="0.5"/>
    <text x="370" y="338" text-anchor="middle" dominant-baseline="central" font-size="10">Monitoring</text>
  </g>
  
  <g class="node c-green" onclick="sendPrompt('List popular AI skills in OpenClaw')">
    <rect x="420" y="325" width="80" height="26" rx="4" stroke-width="0.5"/>
    <text x="460" y="338" text-anchor="middle" dominant-baseline="central" font-size="10">AI Generation</text>
  </g>
  
  <g class="node c-amber" onclick="sendPrompt('List popular utility skills in OpenClaw')">
    <rect x="510" y="325" width="80" height="26" rx="4" stroke-width="0.5"/>
    <text x="550" y="338" text-anchor="middle" dominant-baseline="central" font-size="10">Utilities</text>
  </g>
  
  <!-- Skill Details -->
  <g class="node c-gray" onclick="sendPrompt('How to install skills in OpenClaw?')">
    <rect x="60" y="360" width="100" height="24" rx="4" stroke-width="0.5"/>
    <text x="110" y="372" text-anchor="middle" dominant-baseline="central" font-size="9">ClawHub Store</text>
  </g>
  
  <g class="node c-pink" onclick="sendPrompt('How to create custom skills in OpenClaw?')">
    <rect x="175" y="360" width="100" height="24" rx="4" stroke-width="0.5"/>
    <text x="225" y="372" text-anchor="middle" dominant-baseline="central" font-size="9">Custom Skills</text>
  </g>
  
  <g class="node c-teal" onclick="sendPrompt('How does skill hot-reload work?')">
    <rect x="290" y="360" width="100" height="24" rx="4" stroke-width="0.5"/>
    <text x="340" y="372" text-anchor="middle" dominant-baseline="central" font-size="9">Hot Reload</text>
  </g>
  
  <g class="node c-coral" onclick="sendPrompt('How does skill validation work?')">
    <rect x="405" y="360" width="100" height="24" rx="4" stroke-width="0.5"/>
    <text x="455" y="372" text-anchor="middle" dominant-baseline="central" font-size="9">Validation</text>
  </g>
  
  <g class="node c-blue" onclick="sendPrompt('How to share skills in OpenClaw?')">
    <rect x="520" y="360" width="100" height="24" rx="4" stroke-width="0.5"/>
    <text x="570" y="372" text-anchor="middle" dominant-baseline="central" font-size="9">Community Share</text>
  </g>
  
  <!-- Connection Arrows -->
  <path d="M340 130 L340 145" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow)"/>
  <path d="M180 130 L180 145" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow)"/>
  <path d="M500 130 L500 145" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow)"/>
</svg>
```

---

## ✅ UPDATE: Kimi 2.5 Fixed di OpenClaw 2026.3.11!

```
┌──────────────────────────────────────────────────────────┐
│  ✅ GOOD NEWS: OpenClaw 2026.3.11 FIXES KIMI 2.5!       │
│                                                          │
│  🎉 Tool calling BERFUNGSI kembali                      │
│  🎉 Infinite loop issue RESOLVED                        │
│  🎉 Kimi K2.5 bisa dipakai lagi                         │
│                                                          │
│  ✅ UPDATE: npm i -g openclaw@latest                    │
│  📖 Release: https://github.com/openclaw/openclaw/      │
│              releases/tag/v2026.3.11                    │
│                                                          │
│  ⚠️  NOTE: Versi 2026.3.7 - 2026.3.10 masih buggy       │
│       Skip langsung ke 2026.3.11 atau lebih baru        │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started Flowchart

```svg
<svg width="100%" viewBox="0 0 680 500">
  <defs>
    <marker id="arrow2" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  
  <rect x="20" y="20" width="640" height="460" rx="16" fill="var(--color-background-secondary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="40" y="45" class="th" font-size="16" fill="var(--color-text-primary)">🚀 Getting Started with OpenClaw</text>
  
  <!-- Step 1 -->
  <g class="node c-purple" onclick="sendPrompt('How to install OpenClaw?')">
    <rect x="280" y="70" width="120" height="50" rx="8" stroke-width="0.5"/>
    <text x="340" y="88" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500">1. Install</text>
    <text x="340" y="106" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--color-text-secondary)">npm i -g openclaw</text>
  </g>
  
  <!-- Step 2 -->
  <g class="node c-teal" onclick="sendPrompt('How to configure OpenClaw?')">
    <rect x="280" y="140" width="120" height="50" rx="8" stroke-width="0.5"/>
    <text x="340" y="158" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500">2. Configure</text>
    <text x="340" y="176" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--color-text-secondary)">API Keys + Models</text>
  </g>
  
  <!-- Decision: Platform -->
  <polygon points="340,220 390,245 340,270 290,245" fill="var(--color-background-warning)" stroke="var(--color-border-primary)" stroke-width="0.5"/>
  <text x="340" y="240" text-anchor="middle" dominant-baseline="central" font-size="11" font-weight="500">Platform?</text>
  <text x="340" y="255" text-anchor="middle" dominant-baseline="central" font-size="9" fill="var(--color-text-secondary)">Windows/Mac/Linux</text>
  
  <!-- Windows Path -->
  <g class="node c-blue" onclick="sendPrompt('Windows installation guide for OpenClaw')">
    <rect x="60" y="300" width="100" height="50" rx="8" stroke-width="0.5"/>
    <text x="110" y="318" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="500">Windows</text>
    <text x="110" y="336" text-anchor="middle" dominant-baseline="central" font-size="9" fill="var(--color-text-secondary)">WSL + Auto-start</text>
  </g>
  
  <!-- Mac Path -->
  <g class="node c-coral" onclick="sendPrompt('Mac installation guide for OpenClaw')">
    <rect x="190" y="300" width="100" height="50" rx="8" stroke-width="0.5"/>
    <text x="240" y="318" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="500">Mac</text>
    <text x="240" y="336" text-anchor="middle" dominant-baseline="central" font-size="9" fill="var(--color-text-secondary)">Homebrew</text>
  </g>
  
  <!-- Linux Path -->
  <g class="node c-green" onclick="sendPrompt('Linux installation guide for OpenClaw')">
    <rect x="320" y="300" width="100" height="50" rx="8" stroke-width="0.5"/>
    <text x="370" y="318" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="500">Linux</text>
    <text x="370" y="336" text-anchor="middle" dominant-baseline="central" font-size="9" fill="var(--color-text-secondary)">Docker/Native</text>
  </g>
  
  <!-- Cloud Path -->
  <g class="node c-amber" onclick="sendPrompt('Cloud installation guide for OpenClaw')">
    <rect x="450" y="300" width="100" height="50" rx="8" stroke-width="0.5"/>
    <text x="500" y="318" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="500">Cloud</text>
    <text x="500" y="336" text-anchor="middle" dominant-baseline="central" font-size="9" fill="var(--color-text-secondary)">VPS/Cloud</text>
  </g>
  
  <!-- Step 4: Setup Workspace -->
  <g class="node c-pink" onclick="sendPrompt('How to setup OpenClaw workspace?')">
    <rect x="280" y="380" width="120" height="50" rx="8" stroke-width="0.5"/>
    <text x="340" y="398" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500">4. Setup Workspace</text>
    <text x="340" y="416" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--color-text-secondary)">Git Clone + Config</text>
  </g>
  
  <!-- Step 5: First Skill -->
  <g class="node c-green" onclick="sendPrompt('What is the first skill to try in OpenClaw?')">
    <rect x="500" y="380" width="120" height="50" rx="8" stroke-width="0.5"/>
    <text x="560" y="398" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500">5. First Skill! 🎉</text>
    <text x="560" y="416" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--color-text-secondary)">Try hello-world</text>
  </g>
  
  <!-- Arrows -->
  <path d="M340 120 L340 140" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
  <path d="M340 190 L340 220" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
  
  <!-- Platform arrows -->
  <path d="M290 245 L240 245 L240 270 L160 300" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
  <path d="M290 245 L240 300" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
  <path d="M340 270 L370 300" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
  <path d="M390 245 L440 245 L440 270 L500 300" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
  
  <!-- To setup workspace -->
  <path d="M110 350 L110 365 L340 365 L340 380" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
  <path d="M240 350 L240 365" fill="none" class="arr" stroke="var(--color-border-secondary)"/>
  <path d="M370 350 L370 365" fill="none" class="arr" stroke="var(--color-border-secondary)"/>
  <path d="M500 350 L500 365 L400 380" fill="none" class="arr" stroke="var(--color-border-secondary)"/>
  
  <!-- To first skill -->
  <path d="M400 405 L500 405" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow2)"/>
</svg>
```

---

## 📚 Navigasi Cepat

| Section | Deskripsi |
|---------|-----------|
| [🚀 Getting Started](./docs/getting-started/README.md) | Panduan instalasi dan setup pertama |
| [🖥️ Windows Install](./docs/getting-started/windows-install.md) | Tutorial lengkap Windows + auto-start + management |
| [🔄 Sync Memory ke GitHub](./docs/getting-started/github-sync.md) | Sinkronisasi memory antar device/PC/VPS |
| [📖 Tutorials](#-tutorials) | Kumpulan tutorial praktis OpenClaw |
| [💡 Use Cases](#-use-cases) | Contoh penggunaan real-world |
| [🎯 Tips & Tricks](#-tips--tricks) | Trik optimize OpenClaw |
| [❓ FAQ](./faq/README.md) | Pertanyaan yang sering ditanyakan |
| [⚙️ Config](./docs/config/README.md) | Konfigurasi dan templates |
| [🎥 Resources](./resources/README.md) | Video, link, dan referensi |
| [💰 API Providers](./resources/api-providers.md) | Daftar provider AI API murah & free tier |

---

## 📖 Tutorials

Kumpulan tutorial praktis untuk membangun automation dengan OpenClaw.

### 🎓 Getting Started
| Tutorial | Deskripsi | Level |
|----------|-----------|-------|
| [☁️ Alibaba Cloud Coding Plan](./tutorials/openclaw-alibaba-coding-plan.md) | 8 model AI dengan 1 API key mulai $5/bulan | Beginner |
| [🖥️ Windows Install](./docs/getting-started/windows-install.md) | Instalasi lengkap Windows + auto-start | Beginner |
| [⚠️ OpenClaw Version Guide](./tutorials/avoid-openclaw-2026-3-7-kimi-bug.md) | Update guide: Kimi 2.5 fixed in 2026.3.11 | **CRITICAL** |

### 🤖 AI Automation
| Tutorial | Deskripsi | Level |
|----------|-----------|-------|
| [📝 Auto-Post ke Website](./tutorials/auto-post-website.md) | Foto → AI content → Auto-post ke website | Intermediate |
| [🎙️ Voice Memo to Action](./tutorials/voice-memo-to-action.md) | WhatsApp voice → Whisper → Tasks | Intermediate |
| [📧 Smart Email Forward PDF](./tutorials/smart-email-forward-pdf.md) | Forward email + extract PDF data otomatis | Intermediate |
| [🏷️ Gmail Auto-Label Triage](./tutorials/gmail-auto-label-triage.md) | Auto-classify emails dengan 7 label | Intermediate |
| [📰 Multi-Agent System](./tutorials/openclaw-multi-agent-system.md) | Setup brothers (Radit, Raka, Rama, Rafi) | Advanced |
| [🧠 Multi-Agent Shared Memory](./tutorials/multi-agent-shared-memory.md) | Multiple agents sharing knowledge via GitHub | Advanced |

### 📊 Data & Monitoring
| Tutorial | Deskripsi | Level |
|----------|-----------|-------|
| [📊 Visual Data Alert](./tutorials/visual-data-alert.md) | Spreadsheet → Charts → Telegram | Intermediate |
| [📧 Smart Email Triage](./tutorials/smart-email-triage.md) | AI classify inbox + auto-actions | Intermediate |
| [🗂️ Smart File Butler](./tutorials/smart-file-butler.md) | Auto-organize Downloads dengan AI | Beginner |
| [⚡ Redis Caching Pattern](./tutorials/redis-caching-pattern.md) | Speed up 20x dengan Redis cache | Beginner |
| [🏥 Service Health Dashboard](./tutorials/service-health-dashboard.md) | Monitor services + auto-retry alerts | Intermediate |

### ☁️ Integrations
| Tutorial | Deskripsi | Level |
|----------|-----------|-------|
| [🔍 gog CLI Google Workspace](./tutorials/gog-cli-google-workspace.md) | Gmail, Drive, Docs, Sheets via CLI | Intermediate |
| [⚡ n8n Integration](./tutorials/n8n-integration.md) | Workflow automation dengan n8n | Intermediate |
| [🚀 Deployment Butler](./tutorials/deployment-butler.md) | GitHub webhook → Auto-deploy + rollback | Advanced |
| [🧵 Repliz Threads Automation](./tutorials/repliz-threads-automation.md) | Auto-post ke Threads via Telegram | Intermediate |

### 🎨 Content Creation
| Tutorial | Deskripsi | Level |
|----------|-----------|-------|
| [🎨 Excalidraw Diagram Generation](./tutorials/excalidraw-diagram-generation.md) | Generate diagram dari teks | Beginner |
| [🎬 AI Video Generation Pipeline](./tutorials/ai-video-generation-pipeline.md) | Generate video AI → Upload ke Drive | Intermediate |

---

## 💡 Use Cases

```svg
<svg width="100%" viewBox="0 0 680 350">
  <defs>
    <marker id="arrow3" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  
  <rect x="20" y="20" width="640" height="310" rx="16" fill="var(--color-background-secondary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="40" y="45" class="th" font-size="16" fill="var(--color-text-primary)">💡 Real-World Use Cases</text>
  
  <!-- Use Case 1: Content Automation -->
  <g onclick="sendPrompt('Tell me about content automation use case')">
    <rect x="50" y="70" width="280" height="110" rx="10" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    <text x="70" y="95" font-size="14" font-weight="500" fill="var(--color-text-primary)">📝 Content Automation</text>
    
    <g class="node c-purple">
      <rect x="70" y="110" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="95" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">RSS Feed</text>
    </g>
    
    <g class="node c-teal">
      <rect x="130" y="110" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="155" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">AI Rewrite</text>
    </g>
    
    <g class="node c-green">
      <rect x="190" y="110" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="215" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">Schedule</text>
    </g>
    
    <g class="node c-coral">
      <rect x="250" y="110" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="280" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">Multi-Platform</text>
    </g>
    
    <text x="70" y="150" font-size="10" fill="var(--color-text-secondary)">Auto-curate news → AI rewrite →</text>
    <text x="70" y="165" font-size="10" fill="var(--color-text-secondary)">Schedule posts → Publish everywhere</text>
  </g>
  
  <!-- Use Case 2: Data Pipeline -->
  <g onclick="sendPrompt('Tell me about data pipeline use case')">
    <rect x="350" y="70" width="290" height="110" rx="10" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    <text x="370" y="95" font-size="14" font-weight="500" fill="var(--color-text-primary)">📊 Data Pipeline</text>
    
    <g class="node c-blue">
      <rect x="370" y="110" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="395" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">Scrape</text>
    </g>
    
    <g class="node c-amber">
      <rect x="430" y="110" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="455" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">Clean</text>
    </g>
    
    <g class="node c-pink">
      <rect x="490" y="110" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="515" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">Analyze</text>
    </g>
    
    <g class="node c-purple">
      <rect x="550" y="110" width="70" height="22" rx="4" stroke-width="0.5"/>
      <text x="585" y="121" text-anchor="middle" dominant-baseline="central" font-size="9">Dashboard</text>
    </g>
    
    <text x="370" y="150" font-size="10" fill="var(--color-text-secondary)">Scrape multiple sources → Clean data →</text>
    <text x="370" y="165" font-size="10" fill="var(--color-text-secondary)">AI analysis → Visual dashboard + alerts</text>
  </g>
  
  <!-- Use Case 3: Customer Support -->
  <g onclick="sendPrompt('Tell me about customer support automation use case')">
    <rect x="50" y="200" width="280" height="110" rx="10" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    <text x="70" y="225" font-size="14" font-weight="500" fill="var(--color-text-primary)">🎧 Customer Support</text>
    
    <g class="node c-teal">
      <rect x="70" y="240" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="95" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Ingest</text>
    </g>
    
    <g class="node c-coral">
      <rect x="130" y="240" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="155" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Classify</text>
    </g>
    
    <g class="node c-green">
      <rect x="190" y="240" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="215" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Route</text>
    </g>
    
    <g class="node c-blue">
      <rect x="250" y="240" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="280" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Respond</text>
    </g>
    
    <text x="70" y="280" font-size="10" fill="var(--color-text-secondary)">Monitor channels → AI classify → Route to</text>
    <text x="70" y="295" font-size="10" fill="var(--color-text-secondary)">agent/skill → Auto-respond or escalate</text>
  </g>
  
  <!-- Use Case 4: DevOps -->
  <g onclick="sendPrompt('Tell me about DevOps automation use case')">
    <rect x="350" y="200" width="290" height="110" rx="10" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    <text x="370" y="225" font-size="14" font-weight="500" fill="var(--color-text-primary)">🚀 DevOps Automation</text>
    
    <g class="node c-amber">
      <rect x="370" y="240" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="395" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Monitor</text>
    </g>
    
    <g class="node c-red">
      <rect x="430" y="240" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="455" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Detect</text>
    </g>
    
    <g class="node c-purple">
      <rect x="490" y="240" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="515" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Deploy</text>
    </g>
    
    <g class="node c-teal">
      <rect x="550" y="240" width="70" height="22" rx="4" stroke-width="0.5"/>
      <text x="585" y="251" text-anchor="middle" dominant-baseline="central" font-size="9">Notify</text>
    </g>
    
    <text x="370" y="280" font-size="10" fill="var(--color-text-secondary)">GitHub webhook → Auto-test → Deploy →</text>
    <text x="370" y="295" font-size="10" fill="var(--color-text-secondary)">Health check → Rollback if needed</text>
  </g>
</svg>
```

| Use Case | Deskripsi | Link |
|----------|-----------|------|
| [🎬 AI Video Generation](./docs/use-cases/ai-video-generation.md) | Otomatisasi pembuatan video dengan AI | [Read](./docs/use-cases/ai-video-generation.md) |
| [📰 News Aggregator](./docs/use-cases/news-aggregator.md) | Aggregasi berita otomatis dengan AI | [Read](./docs/use-cases/news-aggregator.md) |

---

## 🔗 Integration Patterns

```svg
<svg width="100%" viewBox="0 0 680 300">
  <defs>
    <marker id="arrow4" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  
  <rect x="20" y="20" width="640" height="260" rx="16" fill="var(--color-background-secondary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
  <text x="40" y="45" class="th" font-size="16" fill="var(--color-text-primary)">🔗 Common Integration Patterns</text>
  
  <!-- Pattern 1: Webhook Trigger -->
  <g onclick="sendPrompt('Explain webhook trigger pattern in OpenClaw')">
    <rect x="50" y="70" width="180" height="90" rx="8" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    
    <g class="node c-coral">
      <rect x="65" y="85" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="95" y="96" text-anchor="middle" dominant-baseline="central" font-size="9">Webhook</text>
    </g>
    
    <path d="M125 96 L145 96" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-teal">
      <rect x="155" y="85" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="185" y="96" text-anchor="middle" dominant-baseline="central" font-size="9">Process</text>
    </g>
    
    <text x="65" y="125" font-size="10" font-weight="500" fill="var(--color-text-primary)">Webhook Trigger</text>
    <text x="65" y="142" font-size="9" fill="var(--color-text-secondary)">GitHub, Stripe, etc.</text>
  </g>
  
  <!-- Pattern 2: Scheduled Job -->
  <g onclick="sendPrompt('Explain scheduled job pattern in OpenClaw')">
    <rect x="250" y="70" width="180" height="90" rx="8" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    
    <g class="node c-amber">
      <rect x="265" y="85" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="290" y="96" text-anchor="middle" dominant-baseline="central" font-size="9">Cron</text>
    </g>
    
    <path d="M315 96 L335 96" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-blue">
      <rect x="345" y="85" width="70" height="22" rx="4" stroke-width="0.5"/>
      <text x="380" y="96" text-anchor="middle" dominant-baseline="central" font-size="9">Execute</text>
    </g>
    
    <text x="265" y="125" font-size="10" font-weight="500" fill="var(--color-text-primary)">Scheduled Job</text>
    <text x="265" y="142" font-size="9" fill="var(--color-text-secondary)">Daily/hourly tasks</text>
  </g>
  
  <!-- Pattern 3: Event Stream -->
  <g onclick="sendPrompt('Explain event stream pattern in OpenClaw')">
    <rect x="450" y="70" width="190" height="90" rx="8" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    
    <g class="node c-green">
      <rect x="465" y="85" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="490" y="96" text-anchor="middle" dominant-baseline="central" font-size="9">Event</text>
    </g>
    
    <path d="M515 96 L535 96" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-purple">
      <rect x="545" y="85" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="570" y="96" text-anchor="middle" dominant-baseline="central" font-size="9">Route</text>
    </g>
    
    <path d="M595 96 L615 96" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-pink">
      <rect x="625" y="85" width="0" height="0"/>
      <text x="625" y="85" text-anchor="middle" font-size="0"></text>
    </g>
    
    <text x="465" y="125" font-size="10" font-weight="500" fill="var(--color-text-primary)">Event Stream</text>
    <text x="465" y="142" font-size="9" fill="var(--color-text-secondary)">Real-time processing</text>
  </g>
  
  <!-- Pattern 4: API Gateway -->
  <g onclick="sendPrompt('Explain API gateway pattern in OpenClaw')">
    <rect x="50" y="180" width="180" height="90" rx="8" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    
    <g class="node c-blue">
      <rect x="65" y="195" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="95" y="206" text-anchor="middle" dominant-baseline="central" font-size="9">Request</text>
    </g>
    
    <path d="M125 206 L145 206" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-teal">
      <rect x="155" y="195" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="185" y="206" text-anchor="middle" dominant-baseline="central" font-size="9">Handler</text>
    </g>
    
    <text x="65" y="235" font-size="10" font-weight="500" fill="var(--color-text-primary)">API Gateway</text>
    <text x="65" y="252" font-size="9" fill="var(--color-text-secondary)">REST/GraphQL endpoint</text>
  </g>
  
  <!-- Pattern 5: Queue Worker -->
  <g onclick="sendPrompt('Explain queue worker pattern in OpenClaw')">
    <rect x="250" y="180" width="180" height="90" rx="8" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    
    <g class="node c-purple">
      <rect x="265" y="195" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="290" y="206" text-anchor="middle" dominant-baseline="central" font-size="9">Queue</text>
    </g>
    
    <path d="M315 206 L335 206" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-green">
      <rect x="345" y="195" width="70" height="22" rx="4" stroke-width="0.5"/>
      <text x="380" y="206" text-anchor="middle" dominant-baseline="central" font-size="9">Worker</text>
    </g>
    
    <text x="265" y="235" font-size="10" font-weight="500" fill="var(--color-text-primary)">Queue Worker</text>
    <text x="265" y="252" font-size="9" fill="var(--color-text-secondary)">Async processing</text>
  </g>
  
  <!-- Pattern 6: Pub/Sub -->
  <g onclick="sendPrompt('Explain pub/sub pattern in OpenClaw')">
    <rect x="450" y="180" width="190" height="90" rx="8" fill="var(--color-background-primary)" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
    
    <g class="node c-coral">
      <rect x="465" y="195" width="50" height="22" rx="4" stroke-width="0.5"/>
      <text x="490" y="206" text-anchor="middle" dominant-baseline="central" font-size="9">Pub</text>
    </g>
    
    <path d="M515 206 L555 206" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-amber">
      <rect x="565" y="195" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="595" y="206" text-anchor="middle" dominant-baseline="central" font-size="9">Sub A</text>
    </g>
    
    <path d="M535 210 L535 230 L555 230" fill="none" class="arr" stroke="var(--color-border-secondary)" marker-end="url(#arrow4)"/>
    
    <g class="node c-blue">
      <rect x="565" y="220" width="60" height="22" rx="4" stroke-width="0.5"/>
      <text x="595" y="231" text-anchor="middle" dominant-baseline="central" font-size="9">Sub B</text>
    </g>
    
    <text x="465" y="255" font-size="10" font-weight="500" fill="var(--color-text-primary)">Pub/Sub</text>
    <text x="465" y="270" font-size="9" fill="var(--color-text-secondary)">Multi-consumer</text>
  </g>
</svg>
```

---

## 🎯 Tips & Tricks

Trik dan best practices untuk optimize OpenClaw.

| Topic | Deskripsi | Link |
|-------|-----------|------|
| [🚀 Performance Optimization](./docs/tips-tricks/README.md) | Best practices untuk speed dan efisiensi | [Read](./docs/tips-tricks/README.md) |

---

## 🎬 YouTube Playlist

- 📺 [OpenClaw Tutorial Series](#) - *Coming soon*
- 📺 [Sumopod Community Showcase](#) - *Coming soon*

---

## 🤝 Cara Berkontribusi

1. **Fork** repo ini
2. **Clone** ke lokal: `git clone https://github.com/fanani-radian/openclaw-sumopod.git`
3. Buat **branch baru**: `git checkout -b feature/nama-fitur`
4. **Commit** perubahan: `git commit -m "Add: deskripsi singkat"`
5. **Push** ke branch: `git push origin feature/nama-fitur`
6. Buat **Pull Request**

### Kontribusi yang Diterima

- ✅ Tips & tricks baru
- ✅ Use cases dari pengalaman nyata
- ✅ Konfigurasi yang bisa dishare
- ✅ Jawaban untuk FAQ
- ✅ Translation (Bahasa Indonesia / English)
- ✅ Video tutorials

---

## 💬 Join Komunitas

- **Discord**: [Sumopod OpenClaw](#)
- **Telegram**: [@sumopod](#)

---

## 📄 Lisensi

Konten repo ini dilisensikan under [MIT License](./LICENSE).

---

<p align="center">
  <sub>Dibuat dengan ❤️ oleh komunitas Sumopod</sub>
</p>
