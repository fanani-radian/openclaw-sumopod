# Panduan Lengkap AI Coding CLI untuk OpenClaw: Kiro CLI & Trae Agent

> **Referensi:** Artikel Kiro oleh [Rama Aditya — Cara Install Kiro CLI dan Menyuruh OpenClaw Ngoding via Kiro](https://ramadigital.id/blog/cara-install-kiro-cli-dan-menyuruh-openclaw-ngoding-via-kiro-untuk-fix-bug-dan-tambah-fitur.md). Informasi Trae Agent berdasarkan riset via Perplexity AI. Tutorial ini ditulis ulang dengan gaya dan perspektif berbeda.

---

Bayangkan skenario ini: kamu lagi santai di rumah, tiba-tiba tim laporan ada bug kritis di sistem quotation PT Contoh Engineering. Bukannya harus buka laptop, SSH ke server, baca log, dan ngoding manual — kamu cukup kirim pesan ke OpenClaw di Telegram, dan beberapa menit kemudian bug sudah diperbaiki.

Bukan sihir. Itu kombinasi **AI Coding CLI** (asisten coding dari terminal) dan **OpenClaw** (AI agent yang nge-orkestrasi semuanya).

Tutorial ini membahas dua tool utama — **Kiro CLI** (dari AWS) dan **Trae Agent** (dari ByteDance) — end-to-end: dari instalasi sampai cara menyuruh OpenClaw ngoding pakai keduanya, termasuk prompt template yang langsung bisa dipakai.

---

## 📐 Arsitektur: OpenClaw sebagai Orchestrator AI Coding

```mermaid
flowchart TB
    USER["👤 Developer\n(Telegram/Discord)"] -->| "Instruksi task coding" | OC["🤖 OpenClaw\n(Orchestrator)"]

    OC -->| "Task routing" | KIRO["⚙️ Kiro CLI — AI Coder AWS"]
    OC -->| "Task routing" | TRAE["🔧 Trae Agent — AI Coder ByteDance"]

    KIRO -->| "Baca, analisis, edit kode" | REPO["📁 Project Repository"]
    TRAE -->| "Baca, analisis, edit kode" | REPO

    KIRO -->| "Return hasil + diff" | OC
    TRAE -->| "Return hasil + diff" | OC
    OC -->| "Laporan perubahan" | USER

    subgraph VPS_Server["VPS / Server"]
        OC
        KIRO
        TRAE
        REPO
    end

    style USER fill:#e3f2fd,stroke:#1565c0
    style OC fill:#fff3e0,stroke:#ef6c00
    style KIRO fill:#e8f5e9,stroke:#2e7d32
    style TRAE fill:#fce4ec,stroke:#c62828
    style REPO fill:#f3e5f5,stroke:#7b1fa2
```

**Prinsipnya simpel:** OpenClaw = manajer proyek, AI Coding CLI = programmer. Kamu = client yang kasih brief. Masing-masing punya peran jelas, dan nggak saling tumpang tindih.

---

## 🆚 Perbandingan: Kiro CLI vs Trae Agent

| Aspek | Kiro CLI | Trae Agent |
|-------|----------|------------|
| **Pengembang** | AWS / Amazon | ByteDance |
| **Lisensi** | Proprietary | MIT (Open Source) |
| **GitHub** | [kiro.dev](https://kiro.dev) | [github.com/bytedance/trae-agent](https://github.com/bytedance/trae-agent) |
| **Model AI** | Claude (Anthropic), Amazon Nova | OpenAI, Anthropic (Claude) |
| **Instalasi** | Binary/AppImage/deb (official) | Clone repo + install deps |
| **Auth** | AWS Builder ID, GitHub, Google | API key (env var / config) |
| **Mode** | Interactive, One-shot, Resume | Interactive, Non-interactive |
| **Built-in Tools** | File edit, bash, search | File edit, bash, structured problem-solving |
| **Kompatibilitas** | macOS, Linux | macOS, Linux, Windows |
| **Cocok Untuk** | Ekosistem AWS, enterprise | Open source enthusiast, fleksibel model |

---

## ══════════════════════════════════════
## 🔵 KIRO CLI
## ══════════════════════════════════════

### Instalasi Kiro CLI

Kiro CLI tersedia untuk macOS dan Linux. Pilih metode yang cocok dengan environment kamu.

#### macOS (Cara Paling Cepat)

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

Setelah install, Kiro akan otomatis redirect ke browser untuk autentikasi. Ini jalur paling praktis untuk MacBook atau workstation lokal.

#### Linux via AppImage (Portabel, Tanpa Install Sistem)

```bash
# Download
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.appimage

# Jadikan executable
chmod +x kiro-cli.appimage

# Jalankan
./kiro-cli.appimage
```

Cocok kalau mau cepat testing atau di environment yang nggak punya akses `sudo`.

#### Linux via Zip Installer (Recommended untuk Server)

Pertama, cek versi glibc:

```bash
ldd --version
```

- **glibc 2.34+** → pakai paket standar
- **glibc < 2.34** → pakai paket **musl**

Lalu download sesuai arsitektur:

```bash
# x86_64, glibc 2.34+
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-x86_64-linux.zip' \
  -o 'kirocli.zip'

# Ekstrak dan install
unzip kirocli.zip
./kirocli/install.sh
```

Secara default, binary dipasang ke `~/.local/bin`. Pastikan direktori itu ada di `PATH` kamu.

Varian lain: `kirocli-aarch64-linux.zip` (ARM64), `kirocli-x86_64-linux-musl.zip` (glibc lama), `kirocli-aarch64-linux-musl.zip` (ARM64 + glibc lama).

#### Ubuntu/Debian via `.deb`

```bash
# Download
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb

# Install
sudo dpkg -i kiro-cli.deb
sudo apt-get install -f
```

Jalur paling familiar buat user Ubuntu.

#### Verifikasi Instalasi

```bash
kiro-cli --version
```

Kalau keluar versi, berarti instalasi berhasil. Catatan penting: command-nya `kiro-cli`, bukan `kiro`.

---

### 🔐 Login ke Kiro CLI

Setelah install, jalankan:

```bash
kiro-cli
# atau
kiro-cli login
```

Kiro CLI mendukung beberapa metode autentikasi:
- GitHub
- Google
- AWS Builder ID
- AWS IAM Identity Center
- Identity provider eksternal (Okta, Microsoft Entra ID)

#### Login dari VPS/Remote Server

Ini bagian yang sering bikin bingung. Ada dua pendekatan:

**1. Device Code Authentication (Recommended untuk VPS)**

AWS Builder ID dan IAM Identity Center mendukung device code — artinya kamu tinggal buka URL di browser lokal, masukkan kode, dan selesai. Nggak perlu tunnel atau konfigurasi tambahan.

**2. Port Forwarding (untuk GitHub/Google Social Login)**

Kalau mau pakai GitHub atau Google login dari VPS, OAuth callback-nya mengarah ke `localhost`. Jadi perlu SSH port forwarding:

```bash
ssh -L 49153:localhost:49153 -N user@server-kamu.com
```

Port `49153` bisa berbeda setiap sesi — sesuaikan dengan yang ditampilkan saat `kiro-cli login`. Jalankan ini di terminal lokal kamu, lalu buka Kiro CLI di sesi SSH server.

#### Verifikasi: Health Check

```bash
kiro-cli doctor
```

**Catatan untuk user root:** Kalau kamu menjalankan Kiro CLI sebagai user `root` (umum di VPS), `kiro-cli doctor` mungkin menampilkan warning dan menyarankan flag tambahan:

```bash
kiro-cli doctor --all
```

---

### 🚀 Tiga Mode Penggunaan Kiro CLI

#### 1. Interactive Mode (Default)

```bash
cd /path/ke/project
kiro-cli
```

Masuk ke sesi chat interaktif. Bisa pakai `/editor` atau `Ctrl+J` untuk multi-line prompt. Cocok untuk eksplorasi dan debugging.

#### 2. Resume Mode (Lanjutkan Sesi Sebelumnya)

Kiro menyimpan percakapan berbasis direktori. Jadi kalau tadi ngoding fitur A di repo X, besok bisa lanjut:

```bash
cd /path/ke/project
kiro-cli chat --resume
```

Sangat berguna untuk pengerjaan yang butuh beberapa sesi.

#### 3. One-Shot Mode (Non-Interactive)

Ini mode yang paling sering dipakai bareng OpenClaw:

```bash
kiro-cli chat --model "claude-opus-4.6" \
  --no-interactive \
  --trust-all-tools \
  "Prompt task kamu di sini"
```

**Penjelasan flag:**

| Flag | Fungsi |
|------|--------|
| `--no-interactive` | Eksekusi satu kali jalan, tanpa sesi chat. Output langsung return. |
| `--trust-all-tools` | Izinkan Kiro menjalankan semua tool tanpa konfirmasi per-item. **Hati-hati:** tingkatkan risiko. Jangan pakai di production. |
| `--model` | Pilih model AI yang digunakan. Sesuaikan dengan kapabilitas dan budget. |

---

### 🤖 Menyuruh OpenClaw Ngoding via Kiro CLI

OpenClaw bisa menjalankan Kiro CLI langsung dari `exec`. Kamu cukup kasih instruksi natural language.

#### Contoh Prompt Template

**🔍 Bug Fix — Pendekatan Root Cause**

```
Masuk ke repo /var/www/app, jalankan Kiro non-interaktif untuk:
1. Audit bug upload gambar yang gagal tanpa pesan error
2. Cari root cause, jangan cuma patch symptom
3. Perbaiki implementasinya
4. Jalankan test yang relevan
5. Ringkas: file diubah, risiko tersisa, dan apa yang belum ter-cover

Jangan commit. Berikan full diff di laporan.
```

**➕ Tambah Fitur — Pendekatan Minimum Viable**

```
Masuk ke repo /var/www/app, pakai Kiro untuk menambahkan fitur export PDF di halaman quotation.
Ikuti pola komponen yang sudah ada di project.
Implementasi minimum yang usable dulu, jangan over-engineer.
Kalau perlu helper/util, pastikan penamaan konsisten.
Jelaskan: alur fitur, file yang berubah, dan cara test-nya.
```

**📝 Code Review**

```
Masuk ke repo /var/www/app, jalankan Kiro untuk review kode di folder src/modules/invoice/.
Fokus ke: error handling, security vulnerability, dan performance issue.
Berikan rekomendasi per prioritas (critical/warning/info).
```

**🔄 Iterasi Revisi**

```
Lanjutkan kerja Kiro di repo /var/www/app yang sama tadi.
Sekarang rapikan edge case untuk filter invoice saat query kosong dan saat status tidak valid.
```

**✅ Fix + Validasi Build**

```
Masuk ke repo /var/www/app, jalankan Kiro untuk:
1. Tambah fitur export CSV di halaman order
2. Jalankan build atau test suite
3. Kalau ada error, perbaiki sampai lolos
4. Kasih ringkasan final: apa yang ditambah, apa yang di-fix, dan status build
```

---

## ══════════════════════════════════════
## 🔴 TRAE AGENT (ByteDance)
## ══════════════════════════════════════

### Apa itu Trae Agent?

**Trae Agent** adalah AI coding assistant open source dari ByteDance (perusahaan di balik TikTok/Douyin). Berbeda dengan Kiro CLI yang proprietary, Trae Agent sepenuhnya open source di bawah lisensi **MIT** — artinya bisa digunakan, dimodifikasi, dan didistribusikan secara bebas.

Repo: [github.com/bytedance/trae-agent](https://github.com/bytedance/trae-agent)

Trae Agent punya dua bentuk:

| Command | Fungsi |
|---------|--------|
| `trae` | Membuka IDE Trae (full editor, GUI) |
| `trae-agent` | CLI coding assistant di terminal (mode yang relevan untuk OpenClaw) |

Trae Agent mendukung model dari **OpenAI** (GPT-4o, dll) dan **Anthropic** (Claude). Kamu bisa memilih model sesuai kebutuhan dan budget.

### Fitur Utama Trae Agent

- **File editing** — baca, buat, dan edit file kode secara otomatis
- **Bash execution** — jalankan perintah shell untuk testing, build, dll
- **Structured problem-solving** — pendekatan terstruktur untuk menganalisis dan memecahkan masalah coding
- **Interactive mode** — sesi chat untuk eksplorasi dan iterasi
- **Non-interactive mode** — one-shot execution, cocok untuk automasi via OpenClaw

---

### 📦 Instalasi Trae Agent

#### Prasyarat

- Git
- Node.js (v18+)
- npm atau pnpm

#### Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/bytedance/trae-agent.git
cd trae-agent

# 2. Install dependencies
npm install
# atau
pnpm install

# 3. Konfigurasi API key
# Pilih salah satu (atau keduanya):

# OpenAI
export OPENAI_API_KEY="sk-your-openai-key"

# Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"

# 4. Build (jika diperlukan)
npm run build
```

#### Verifikasi Instalasi

```bash
# Cek apakah trae-agent bisa dijalankan
npx trae-agent --help
# atau setelah global install:
trae-agent --help
```

Untuk kemudahan, kamu bisa meng-install secara global:

```bash
cd trae-agent
npm link
# Sekarang bisa langsung:
trae-agent --help
```

#### Konfigurasi Model

Trae Agent mendukung beberapa model. Tentukan model yang ingin digunakan melalui environment variable atau konfigurasi:

```bash
# Default model selection
export TRAE_MODEL="claude-sonnet-4-20250514"  # Anthropic Claude
# atau
export TRAE_MODEL="gpt-4o"                     # OpenAI GPT-4o
```

---

### 🚀 Mode Penggunaan Trae Agent

#### 1. Interactive Mode

```bash
cd /path/ke/project
trae-agent
```

Masuk ke sesi chat interaktif. Cocok untuk eksplorasi, debugging, dan iterasi kompleks.

#### 2. Non-Interactive / One-Shot Mode

Mode ini paling cocok digunakan bersama OpenClaw:

```bash
trae-agent --no-interactive "Audit dan perbaiki bug login yang return 500"
```

Atau dengan model spesifik:

```bash
trae-agent --model "claude-sonnet-4-20250514" --no-interactive "Task description here"
```

---

### 🤖 Menyuruh OpenClaw Ngoding via Trae Agent

Sama seperti Kiro CLI, OpenClaw bisa menjalankan Trae Agent langsung dari `exec`. Polanya identik — OpenClaw jadi orchestrator, Trae Agent jadi coder.

#### Contoh Prompt Template

**🔍 Bug Fix via Trae**

```
Masuk ke repo /var/www/app, jalankan trae-agent non-interaktif untuk:
1. Analisis endpoint /api/invoices yang response time-nya > 5 detik
2. Cari bottleneck (N+1 query, missing index, dll)
3. Perbaiki performa
4. Benchmark sebelum dan sesudah fix
5. Ringkas: apa yang diubah, improvement yang didapat

Jangan commit. Berikan detail perubahan.
```

**➕ Tambah Fitur via Trae**

```
Masuk ke repo /var/www/app, pakai trae-agent untuk menambahkan fitur dark mode.
Gunakan CSS variables yang sudah ada di project.
Pastikan toggle state tersimpan di localStorage.
Jelaskan: file yang diubah, alur implementasi, dan cara test-nya.
```

**📝 Code Review via Trae**

```
Masuk ke repo /var/www/app, jalankan trae-agent untuk review kode di folder src/utils/.
Fokus ke: error handling, edge case, dan code duplication.
Berikan rekomendasi per prioritas (critical/warning/info).
```

**🔄 Debug + Fix via Trae**

```
Masuk ke repo /var/www/app, jalankan trae-agent untuk:
1. Reproduce error "Cannot read property of undefined" di halaman dashboard
2. Trace stack trace dan identifikasi root cause
3. Perbaiki bug beserta edge case terkait
4. Jalankan test yang relevan
5. Kasih ringkasan: root cause, fix yang diterapkan, dan cara prevent ke depannya
```

**✅ Refactor via Trae**

```
Masuk ke repo /var/www/app, jalankan trae-agent untuk:
1. Refactor modul auth/ — pisahkan logic validation, token management, dan session handling
2. Pastikan tidak ada breaking change pada API yang sudah exist
3. Tambah unit test untuk fungsi yang di-refactor
4. Jalankan full test suite
```

---

## 📋 AGENTS.md: Konsistensi Hasil AI Coding

**Berlaku untuk Kiro CLI maupun Trae Agent.** File `AGENTS.md` ditaruh di root directory project dan berisi instruksi yang otomatis dibaca AI coding setiap kali dijalankan di repo tersebut.

```markdown
# AGENTS.md — PT Contoh Engineering Backend

## Stack
- Framework: Next.js 14 (App Router)
- Database: PostgreSQL via Prisma
- Styling: Tailwind CSS
- Testing: Vitest + React Testing Library

## Konvensi Kode
- Gunakan TypeScript strict mode
- Komponen naming: PascalCase
- Utility function di folder src/lib/
- Database query selalu melalui Prisma client
- Error handling pakai try-catch dengan custom error class

## Aturan Penting
- JANGAN pernah commit tanpa running test
- JANGAN ubah file migration yang sudah exist
- Selalu buat backward-compatible change
- Gunakan existing patterns, jangan introduce pattern baru tanpa alasan kuat
```

Dengan `AGENTS.md`, hasil coding AI jauh lebih konsisten dan sesuai standar tim — baik pakai Kiro CLI maupun Trae Agent.

---

## 🏆 Best Practices

### 1. Mulai dari Task Kecil

Jangan langsung suruh AI ngerjain fitur gede. Mulai dari bug fix kecil atau refactor untuk ngeliat bagaimana dia memahami codebase kamu.

### 2. Prompt Spesifik > Prompt Umum

❌ "Tolong perbaiki bug"
✅ "Audit endpoint `/api/login` yang return 500 saat email tidak valid. Cari root cause, perbaiki, dan jalankan test."

### 3. Jangan Langsung Commit

Selalu minta AI untuk **jangan commit dulu**. Review hasilnya lewat OpenClaw, kalau sudah OK baru commit manual.

### 4. Pilih Tool yang Tepat

- **Kiro CLI** → Kalau kamu sudah di ekosistem AWS, atau butuh enterprise-grade support
- **Trae Agent** → Kalau kamu mau open source, fleksibel pilih model, atau customize behavior

### 5. `--trust-all-tools` Hanya di Development

Flag ini mematikan semua safety check. Gunakan **hanya** di environment development.

### 6. Selalu Ada AGENTS.md

Satu file kecil di root repo bisa bedain hasil AI coding dari "cukup bagus" jadi "sesuai standar tim".

---

## 📚 Link Penting

### Kiro CLI
- [Dokumentasi Kiro CLI](https://docs.kiro.dev)
- [Kiro CLI Install Script](https://cli.kiro.dev/install)
- [Artikel Referensi — Rama Aditya](https://ramadigital.id/blog/cara-install-kiro-cli-dan-menyuruh-openclaw-ngoding-via-kiro-untuk-fix-bug-dan-tambah-fitur.md)

### Trae Agent
- [GitHub — Trae Agent](https://github.com/bytedance/trae-agent)
- [ByteDance Open Source](https://opensource.bytedance.com)

### OpenClaw
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

---

## Penutup

Dengan dua opsi AI Coding CLI — **Kiro CLI** dan **Trae Agent** — OpenClaw punya fleksibilitas lebih besar sebagai orchestrator. Pilih tool berdasarkan kebutuhanmu: enterprise AWS ecosystem (Kiro) atau open source flexibility (Trae).

Yang perlu diingat: AI coding itu **tool**, bukan pengganti programmer. Dia bagus untuk task yang well-defined dan scope-nya jelas. Untuk architectural decision atau bisnis logic yang kompleks, review manusia tetap wajib.

Mulai dari install salah satu (atau keduanya), bikin `AGENTS.md`, terus coba task kecil dulu. Dari situ, scale up ke workflow yang lebih kompleks.
