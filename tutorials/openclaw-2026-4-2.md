# OpenClaw 2026.4.2 — Task Flow Kembali, YOLO Mode Default, dan 2 Breaking Changes yang Wajib Lo Tahu

_Release notes resmi: 2 April 2026, 18:30 UTC oleh Peter Steinberger (steipete)_

---

Sebelum gue mulai, satu disclosure cepat: **semua infrastructure yang gue pakai — VPS, AI model access, deployment — jalan di Sumopod VPS.** Kalau lo mau setup serupa, [daftar lewat link ini](https://blog.fanani.co/sumopod) buat support konten ini.

---

OpenClaw 2026.4.2 release ini spesial buat gue secara personal. Kenapa? Karena ada **2 breaking changes** yang nyaris bikin production setup gue silent-fail, plus fitur yang gue tunggu sejak lama — **Task Flow** — akhirnya kembali secara permanen.

Gue uda jalanin update ini di production (VPS 7.5GB RAM, multi-agent setup dengan 324 skills) dan ini yang gue temukan.

**TL;DR:**
- ⚠️ 2 breaking changes yang bisa nge-break config lo secara silent
- 🔄 Task Flow kembali dengan arsitektur baru (managed vs mirrored sync)
- 🚀 YOLO mode jadi default untuk exec di gateway/node
- 📱 Google Assistant integration di Android
- 🔒 50+ security fixes (TLS, proxy, env injection, path traversal)
- 🏢 Feishu Drive comments, Matrix mentions fix, WhatsApp improvements

---

## ⚠️ Breaking Changes — JANGAN Skip Bagian Ini

Kalau lo pake xAI search atau Firecrawl web fetch, **skip update sebelum baca bagian ini.**

Kenapa ini dangerous: kedua breaking changes ini **silent failure** — tool-nya hilang dari agent tanpa error message. Lo bisa ngerasa semua normal padahal xAI search dan Firecrawl udah nggak jalan.

![Breaking Changes Migration](https://mermaid.ink/img/Zmxvd2NoYXJ0IExSCiAgICBzdWJncmFwaCBTaWxlbnQgRmFpbHVyZQogICAgICAgIEExW3hBSSBTZWFyY2ggVG9vbF0gLS0%2BfFBhdGggd3Jvbmd8IEExRltUb29sIFVuYXZhaWxhYmxlXQogICAgICAgIEEyW0ZpcmVjcmF3bCBXZWJGZXRjaF0gLS0%2BfEZhbGxiYWNrIG1pc21hdGNofCBBMkZbU2lsZW50IE5vIEVycm9yXQogICAgZW5kCiAgICAKICAgIHN1YmdyYXBoIFVwZ3JhZGUKICAgICAgICBCMVtydW4gb3BlbmNsYXcgZG9jdG9yIC0tZml4XQogICAgICAgIEMxW3hBSV9BUElfS0VZIGluIG5ldyBjb25maWddCiAgICAgICAgQzJbRmlyZWNyYXdsIGNvbmZpZyBhdCBuZXcgcGF0aF0KICAgICAgICBEMVtCb3RoIHRvb2xzIGJhY2sgMjAwIE9LXQogICAgZW5kCiAgICAKICAgIEExIC0tPiBCMSAtLT4gQzEgLS0%2BIEQxCiAgICBBMiAtLT4gQjEgLS0%2BIEMyIC0tPiBEMQogICAgCiAgICBzdHlsZSBTaWxlbnQgRmFpbHVyZSBmaWxsOiNmZmViZWUsc3Ryb2tlOiNjNjI4MjgKICAgIHN0eWxlIFVwZ3JhZGUgZmlsbDojZThmNWU5LHN0cm9rZTojMmU3ZDMyCiAgICBzdHlsZSBBMSBmaWxsOiNmZjc3MDAsc3Ryb2tlOiNmZjQ0MDAKICAgIHN0eWxlIEEyIGZpbGw6I2ZmNzcwMCxzdHJva2U6I2ZmNDQwMAogICAgc3R5bGUgRDEgZmlsbDojZThmNWU5LHN0cm9rZTojMmU3ZDMy)

### 1. xAI Search Config Pindah Path

**Dulu:**
```yaml
tools:
  web:
    x_search:
      enabled: true
      apiKey: sk-xxx
```

**Sekarang:**
```yaml
plugins:
  entries:
    xai:
      config:
        xSearch:
          enabled: true
        webSearch:
          apiKey: sk-xxx  # atau set XAI_API_KEY env var
```

### 2. Firecrawl Web Fetch Config Pindah Path

**Dulu:**
```yaml
tools:
  web:
    fetch:
      firecrawl:
        apiKey: fc-xxx
```

**Sekarang:**
```yaml
plugins:
  entries:
    firecrawl:
      config:
        webFetch:
          apiKey: fc-xxx
```

### Fix Otomatis

Kedua migrasi bisa dikerjain otomatis:

```bash
openclaw doctor --fix
```

Command ini scan config file, pindahin value ke path baru, dan bersihin remnant. **TAPI** — selalu backup config dulu:

```bash
cp ~/.openclaw/config.json ~/.openclaw/config.json.backup
openclaw doctor --fix
```

**Setup gue:** Gue nggak pake xAI search (pake smart-search skill dengan Serper fallback), jadi breaking change #1 nggak impact. Tapi kalau lo pake xAI, **WAJIB** update config sebelum atau sesudah upgrade.

---

## 🔄 Task Flow — Feature yang Paling Dinanti Kembali

![Task Flow Orchestration Concept](/images/posts/openclaw-taskflow.jpg)


Ini highlight utama release ini. Task Flow itu apa? Bayangin gini: lo punya AI agent yang jalan background task — scraping data, generate report, kirim email. Dulu, kalau gateway restart di tengah jalan, task tersebut hilang. Start dari nol lagi.

Task Flow solve ini. Dan sekarang udah kembali dengan arsitektur yang lebih robust.

![Task Flow Architecture](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRCCiAgICBzdWJncmFwaCBUYXNrIEZsb3cgQXJjaGl0ZWN0dXJlCiAgICAgICAgT1JbT3JjaGVzdHJhdG9yXQogICAgICAgIEYxW1Rhc2sgRmxvdyAtIE1hbmFnZWRdCiAgICAgICAgRjJbVGFzayBGbG93IC0gTWlycm9yZWRdCiAgICAgICAgU1RbU3RhdGUgU3RvcmUgKyBSZXZpc2lvbiBUcmFja2luZ10KICAgICAgICBDVFtDaGlsZCBUYXNrIFNwYXduZXJdCiAgICAgICAgU0NbU3RpY2t5IENhbmNlbCBJbnRlbnRdCiAgICBlbmQKICAgIAogICAgc3ViZ3JhcGggRmxvdyBMaWZlY3ljbGUKICAgICAgICBUMVtTdGVwIDE6IEV4dHJhY3RdIC0tPiBUMltTdGVwIDI6IFByb2Nlc3NdIC0tPiBUM1tTdGVwIDM6IFJlcG9ydF0KICAgICAgICBUMyAtLT4gVDRbU3RlcCA0OiBEZWxpdmVyXQogICAgZW5kCiAgICAKICAgIE9SIC0tPiBGMQogICAgT1IgLS0%2BIEYyCiAgICBGMSAtLT4gU1QKICAgIEYyIC0tPiBTVAogICAgRjEgLS0%2BIENUCiAgICBDVCAtLT4gTk1bQ2hpbGQgVGFza3MgUnVubmluZ10KICAgIFNDIC0tPiBOTQogICAgTk0gLS0%2BfGdyYWNlZnVsIGZpbmlzaHwgRE9ORVtTZXR0bGVkOiBDYW5jZWxsZWRdCiAgICAKICAgIHN0eWxlIE9SIGZpbGw6IzFhMWEyZSxzdHJva2U6I2U5NDU2MCxjb2xvcjojZmZmCiAgICBzdHlsZSBGMSBmaWxsOiNlM2YyZmQsc3Ryb2tlOiMxNTY1YzAKICAgIHN0eWxlIEYyIGZpbGw6I2YzZTVmNSxzdHJva2U6IzdiMWZhMgogICAgc3R5bGUgU1QgZmlsbDojMGQzYjJlLHN0cm9rZTojMDBmZjg4CiAgICBzdHlsZSBDVCBmaWxsOiNmZmYzZTAsc3Ryb2tlOiNlNjUxMDAKICAgIHN0eWxlIFNDIGZpbGw6I2ZmZWJlZSxzdHJva2U6I2M2MjgyOA==)

### Dua Sync Mode

| Mode | Penjelasan | Use Case |
|------|-----------|----------|
| **Managed** | State dikelola sepenuhnya oleh OpenClaw, tersimpan persisten | Background automation, cron jobs, data pipelines |
| **Mirrored** | State dicerminkan dari external source | Integration dengan external orchestration system |

### Durable State + Revision Tracking

Ini yang bikin beda dari sebelumnya. Kalau gateway restart:

1. OpenClaw baca revision log dari state store
2. Identifikasi step terakhir yang selesai
3. Resume dari situ — bukan dari awal

**Contoh nyata di setup gue:** Nightly data analysis pipeline (scrape → clean → report → kirim). Dulu kalau gateway restart jam 2 pagi, semuanya restart dari step 1. Sekarang, resume dari step yang terputus. **Impact: hemat ~15 menit runtime per hari.**

### Managed Child Task Spawning

Task Flow sekarang bisa spawn child tasks secara managed. Artinya:

- Parent flow spawn 5 sub-tasks (misal: scrape 5 website)
- Kalau lo cancel parent, **child yang lagi jalan tetap selesai** (graceful shutdown)
- Baru setelah semua child selesai, parent status = cancelled

Ini "sticky cancel intent" — cancel-nya nge-stick, tapi nggak kill. Beda sama hard kill yang bisa bikin zombie process.

### New CLI Commands

```bash
# Lihat semua active flows
openclaw flows list

# Detail satu flow
openclaw flows show <flow-id>

# Cancel flow (sticky intent — child tasks tetap selesai)
openclaw flows cancel <flow-id>

# Recover stuck flow
openclaw flows recover <flow-id>
```

### Plugin API: api.runtime.taskFlow

Buat plugin developer (atau siapa yang bikin custom skill yang butuh background orchestration), ada API baru:

```
api.runtime.taskFlow.create()  — bikin managed flow dari host context
api.runtime.taskFlow.drive()   — drive flow tanpa pass owner ID
```

Host context auto-resolve ownership. Plugin nggak perlu tau siapa current user.

---

## 🚀 YOLO Mode Jadi Default

Ini perubahan yang subtle tapi impact-nya besar buat automation workflow.

**Dulu:** Setiap exec command di gateway/node butuh approval (prompt konfirmasi).

**Sekarang:**
```yaml
security: full
ask: off
```

Artinya exec di gateway/node jalan tanpa approval. Ini **kenapa** ini penting:

| Scenario | Lama | Sekarang |
|----------|------|----------|
| Cron job jalankan script | ❌ Block, tunggu approval | ✅ Langsung jalan |
| Sub-agent spawn child task | ❌ Block | ✅ Langsung jalan |
| Heartbeat check + auto-cleanup | ❌ Block | ✅ Langsung jalan |

**Untuk setup gue (27+ cron jobs):** Ini game changer. Dulu sering cron jobs nge-block karena butuh approval yang nggak ada yang approve. Sekarang semua jalan smooth.

**⚠️ Tapi:** Ini security tradeoff. Lo essentially kasih full exec access ke gateway. Pastikan:
- VPS lo punya firewall (UFW/fail2ban)
- SSH access restricted
- Environment variables nggak ada di config yang commit ke public repo

```bash
# Check current exec policy
openclaw doctor
```

---

## 📱 Google Assistant Integration

Fitur baru buat Android user:

- OpenClaw bisa di-trigger lewat **Google Assistant** ("Hey Google, ask OpenClaw...")
- Assistant-role entrypoints baru di Android app
- Google Assistant App Actions metadata — prompt langsung masuk chat composer

**Setup gue:** Gue jalanin OpenClaw di VPS, jadi ini nggak langsung apply. Tapi buat yang jalanin di Android device langsung, ini bikin OpenClaw accessible lewat voice command. Lumayan.

---

## 🔌 Plugin Hook Baru: before_agent_reply

Plugin developer, ini buat lo:

```javascript
// Plugin bisa intercept reply SEBELUM LLM respond
hooks: {
  before_agent_reply: async (context) => {
    // Kalau context match pattern tertentu, return synthetic reply
    // (skip LLM call entirely)
    if (context.isSimplePing) {
      return { reply: "PONG", skip: true };
    }
  }
}
```

Use case:
- **Caching** — return cached response tanpa hit LLM
- **Rate limiting** — block request saat quota exceeded
- **Custom routing** — redirect ke tool-specific handler
- **Cost saving** — skip expensive model call buat simple query

Ini middleware pattern yang powerful. Essentially bikin plugin bisa jadi "brain" sendiri sebelum LLM terlibat.

---

## 🔒 Security Overhaul — 50+ Bug Fixes

![Security Hardening Concept](/images/posts/openclaw-security.jpg)


Ini bagian yang ngebuat gue paling impressed. 50+ security-related fixes dalam satu release. Bukan patch kecil — ini systematic security hardening.

![Security Architecture](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRECiAgICBzdWJncmFwaCBTZWN1cml0eSBIYXJkZW5pbmcgMjAyNi40LjIKICAgICAgICBUW1RMTVMgJiBQcm94eV0KICAgICAgICBBW0F1dGggQ2VudHJhbGl6YXRpb25dCiAgICAgICAgQltpbnNlY3VyZSBUTFMgQmxvY2tlZF0KICAgICAgICBDW0hlYWRlciBTaGFwaW5nIE5vcm1hbGl6ZWRdCiAgICAgICAgRFtQcm94eS1ob3AgVExTIFNlcGFyYXRlXQogICAgZW5kCiAgICAKICAgIHN1YmdyYXBoIFJ1bnRpbWUKICAgICAgICBFW0VudiBWYXIgSW5qZWN0aW9uIFNhbml0aXplZF0KICAgICAgICBGW1BhdGggVHJhdmVyc2FsIEJsb2NrZWRdCiAgICAgICAgR1tFeGVjIEFwcHJvdmFsIFN0cmlwcGVkXQogICAgICAgIEhbQ29waWxvdCBQcm94eSBIYXJkZW5pbmddCiAgICBlbmQKICAgIAogICAgc3ViZ3JhcGggQ2hhbm5lbHMKICAgICAgICBJW1doYXRzQXBwIFByZXNlbmNlIEZpeF0KICAgICAgICBKW1NsdWNrIEZvcm1hdHRpbmcgRml4XQogICAgICAgIEtbTWF0cml4IE1lbnRpb25zIEZpeF0KICAgICAgICBMTVtNUyBUZWFtcyBTdHJlYW1pbmcgRml4XQogICAgZW5kCiAgICAKICAgIFQgLS0+IEUgLS0+IEYgLS0+IEcgLS0+IEgKICAgIFQgLS0+IEkgLS0+IEogLS0+IEsgLS0+IEwKICAgIAogICAgc3R5bGUgVCBmaWxsOiNmZmUwYjAsc3Ryb2tlOiNmZjY2MDAKICAgIHN0eWxlIFJ1bnRpbWUgZmlsbDojZTNmMmZkLHN0cm9rZTojMTU2NWMwCiAgICBzdHlsZSBDaGFubmVscyBmaWxsOiNmM2U1ZjUsc3Ryb2tlOiM3YjFmYTIKICAgIHN0eWxlIEUgZmlsbDojZTgzZjJmLHN0cm9rZTojZGMyNjI2CiAgICBzdHlsZSBGIGZpbGw6I2U4ZjVlOSxzdHJva2U6IzJlN2QzMg==)

### Transport & Provider Security

| Fix | Impact |
|-----|--------|
| TLS override blocked | Ngga ada insecure connection, even kalau config salah |
| Proxy routing centralized | Satu path untuk semua proxy decisions |
| Header shaping normalized | Provider-specific headers konsisten |
| GitHub Copilot parsing hardened | Malformed proxy hints = fail closed |
| Anthropic proxy detection | Spoofed hosts nggak dapat native defaults |

### Runtime Security

| Fix | Impact |
|-----|--------|
| Env var injection sanitized | Plugin nggak bisa inject env vars tanpa permission |
| Path traversal blocked | Nggak ada file access di luar workspace |
| Exec approval stripping | Malformed policy = fallback ke default (safe) |
| Host override rejection | Nggak bisa bypass sandbox config per-call |
| Subagent scope fixing | Admin-only calls tetap admin |

### Channel Fixes

| Channel | Fix |
|---------|-----|
| **WhatsApp** | Self-chat mode nggak block push notifications lagi |
| **Slack** | mrkdwn formatting proper (bukan generic Markdown) |
| **Matrix** | m.mentions spec-compliant (Element notifications work) |
| **MS Teams** | Streaming text nggak duplicate lagi |
| **Feishu** | Comment threads nggak leak reasoning/planning spillover |

---

## 🏢 Multi-Channel Updates

Selain security fixes, ada feature baru buat channel integrations:

### Feishu Drive Comments
- Dedicated comment-event flow untuk document collaboration
- Comment-thread context resolution — AI bisa baca konteks sekitar comment
- In-thread replies langsung di dokumen
- `feishu_drive` comment actions

**Scenario:** Kolaborator kasih comment di Feishu doc → "@OpenClaw, summarize section ini" → OpenClaw baca konteks → reply langsung di comment thread. Nggak lewat main chat.

### Matrix m.mentions Fix
Dulu mention di Matrix room nggak trigger notification di Element. Sekarang m.mentions metadata emit di: text sends, media captions, edits, poll fallback text. **Notification jadi reliable.**

### WhatsApp Improvements
- **Presence fix:** Self-chat mode nggak block push notifications (bug yang annoying buat personal phone user)
- **MIME expansion:** HTML, XML, CSS attachment sekarang recognized
- **Graceful fallback:** Unknown media types nggak drop attachment, fallback properly

### Compaction Model Override
```
agents.defaults.compaction.model
```
Sekarang konsisten resolve di semua path — manual `/compact`, engine-owned compaction, dan auto-compaction. Buat yang pake model beda buat compaction (misal: Claude buat compress, Kimi buat daily), ini fix yang sangat welcome.

Plus: `agents.defaults.compaction.notifyUser` — compacting notice sekarang opt-in. Nggak ada lagi "🧹 Compacting context..." yang muncul tiba-tiba.

---

## 📊 Bug Fix Summary — Angka yang Bicara

| Category | Count | Highlights |
|----------|-------|------------|
| Provider/Transport | 8 | TLS, proxy, header, routing |
| Exec/Approvals | 6 | Policy stripping, scope fixing, host override |
| Channel-specific | 10+ | WhatsApp, Slack, Matrix, Feishu, Teams |
| Agent/Subagent | 4 | Compaction, loopback, scope |
| Streaming | 3 | Teams duplication, Matrix preview |
| Plugin/Hooks | 3 | Session routing, approval config |
| **Total** | **50+** | Most security-focused release |

** vincentkoc** kontributor paling produktif di release ini — 7+ PRs merged, semua di area provider security dan transport policy.

---

## 🛠️ Cara Update (Step by Step)

```bash
# 1. Backup config
cp ~/.openclaw/config.json ~/.openclaw/config.json.bak-20260404

# 2. Check current version
openclaw --version

# 3. Update
npm install -g openclaw@2026.4.2

# 4. Run migration (FIX breaking changes)
openclaw doctor --fix

# 5. Verify
openclaw doctor
openclaw status

# 6. Restart gateway
openclaw gateway restart

# 7. Test Task Flow
openclaw flows list

# 8. Verify exec policy
openclaw doctor  # check "exec defaults" section
```

### Yang Perlu Diperhatikan

1. **Kalau pake xAI search** → Pastikan config migrasi sukses (`openclaw doctor --fix`)
2. **Kalau pake Firecrawl** → Sama, migrasi config
3. **Kalau punya exec approval custom** → Cek `~/.openclaw/exec-approvals.json`, malformed values otomatis di-strip
4. **Kalau punya sub-agent setup** → Test `sessions_spawn` — loopback pairing fix should make it more stable
5. **Kalau pake Matrix** → @mentions sekarang reliable

---

## 📝 Pengalaman Production Gue

Gue update langsung di VPS production (i know, risky) tapi setup gue udah punya backup. Ini yang gue catat:

| Item | Before | After |
|------|--------|-------|
| xAI Search | N/A (nggak pake) | N/A |
| Firecrawl | N/A (nggak pake) | N/A |
| Task Flow | ❌ Not available | ✅ Available (via `openclaw flows`) |
| Exec approvals | 3-5 blocked/hari | 0 blocked (YOLO mode) |
| Sub-agent spawns | Occasional close(1008) | ✅ Stable |
| Compaction notice | Always visible | ✅ Opt-in |
| Gateway restart | Tasks lost | ✅ Task state preserved |

**Biggest win:** Zero blocked exec approvals. Dengan 27+ cron jobs dan multi-agent setup, ini ngurangi headache signifikan.

**Second win:** Task Flow CLI. `openclaw flows list` + `openclaw flows recover <id>` = game changer buat monitoring background tasks dari terminal.

---

## 🔮 Apa yang Gue Expect di Next Release

Berdasarkan PR activity dan discussion di GitHub:

- **Task Flow UI** — CLI udah ada, butuh visual dashboard
- **Plugin marketplace** — Ecosystem growing, butuh discovery layer
- **Cross-agent task delegation** — Raka delegate ke Rafi via Task Flow API
- **Cost tracking per flow** — Know exactly how much each background task costs

Ini bukan roadmap resmi — cuma prediksi berdasarkan pattern yang gue lihat di PRs.

---

## 🎯 Verdict — Wajib Update atau Nggak?

| Kriteria | Score |
|----------|-------|
| Breaking change risk | ⭐⭐⭐ (medium — silent failure) |
| New feature value | ⭐⭐⭐⭐⭐ (Task Flow + YOLO = big win) |
| Security improvement | ⭐⭐⭐⭐⭐ (50+ fixes) |
| Upgrade difficulty | ⭐⭐ (easy — `openclaw doctor --fix`) |
| Overall recommendation | **UPDATE NOW** ✅ |

**Satu-satunya reason buat delay:** Kalau lo punya custom plugin yang hardcode `tools.web.x_search` atau `tools.web.fetch.firecrawl` path. Tapi kalau lo cuma user biasa yang install dari npm, update + `doctor --fix` = done.

---

Seperti biasa, semua ini jalan di **Sumopod VPS** — VPS, AI model, deployment, semuanya satu paket. Kalau lo mau setup OpenClaw yang production-ready, [daftar lewat link ini](https://blog.fanani.co/sumopod) buat mulai.

> 📎 **Source:** [openclaw-2026-4-2.md](https://github.com/fanani-radian/openclaw-sumopod/blob/main/tutorials/openclaw-2026-4-2.md) — view on GitHub & star ⭐

**Referensi:**
- [OpenClaw 2026.4.2 GitHub Release](https://github.com/openclaw/openclaw/releases/tag/v2026.4.2)
- [Migration Guide — xugj520.cn](https://www.xugj520.cn/en/archives/openclaw-2026-migration-configuration-security-task-flow.html)
- [Release Notes SourceForge Mirror](https://sourceforge.net/projects/openclaw.mirror/files/v2026.4.2/)