# Panduan Lengkap Kiro CLI + OpenClaw: Ngoding dari Telegram dengan AI

> **Referensi:** Artikel asli oleh [Rama Aditya — Cara Install Kiro CLI dan Menyuruh OpenClaw Ngoding via Kiro](https://ramadigital.id/blog/cara-install-kiro-cli-dan-menyuruh-openclaw-ngoding-via-kiro-untuk-fix-bug-dan-tambah-fitur.md). Tutorial ini ditulis ulang dengan gaya dan perspektif berbeda, berdasarkan prinsip-prinsip dari artikel referensi tersebut.

---

Bayangkan skenario ini: kamu lagi santai di rumah, tiba-tiba tim laporan ada bug kritis di sistem quotation PT Contoh Engineering. Bukannya harus buka laptop, SSH ke server, baca log, dan ngoding manual — kamu cukup kirim pesan ke OpenClaw di Telegram, dan beberapa menit kemudian bug sudah diperbaiki.

Bukan sihir. Itu kombinasi **Kiro CLI** (AI coding assistant dari terminal) dan **OpenClaw** (AI agent yang nge-orkestrasi semuanya).

Tutorial ini membahas end-to-end: dari install Kiro CLI sampai cara menyuruh OpenClaw ngoding pakai Kiro, termasuk prompt template yang langsung bisa dipakai.

---

## 📐 Arsitektur: Bagaimana OpenClaw dan Kiro Bekerja Sama

Sebelum masuk ke teknis, penting paham flow-nya dulu:

```mermaid
flowchart LR
    A["👤 Developer\n(Telegram/Discord)"] -->| "Instruksi task coding" | B["🤖 OpenClaw\n(Orchestrator)"]
    B -->| "cd ke repo + jalankan kiro-cli" | C["⚙️ Kiro CLI\n(AI Coder)"]
    C -->| "Baca kode, analisis, edit file" | D["📁 Project Repository"]
    C -->| "Return hasil + diff" | B
    B -->| "Laporan perubahan" | A

    subgraph "VPS / Server"
        B
        C
        D
    end

    style A fill:#e3f2fd,stroke:#1565c0
    style B fill:#fff3e0,stroke:#ef6c00
    style C fill:#e8f5e9,stroke:#2e7d32
    style D fill:#f3e5f5,stroke:#7b1fa2
```

**Prinsipnya simpel:** OpenClaw = manajer proyek, Kiro CLI = programmer. Kamu = client yang kasih brief. Masing-masing punya peran jelas, dan nggak saling tumpang tindih.

---

## 📦 Instalasi Kiro CLI

Kiro CLI tersedia untuk macOS dan Linux. Pilih metode yang cocok dengan environment kamu.

### macOS (Cara Paling Cepat)

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

Setelah install, Kiro akan otomatis redirect ke browser untuk autentikasi. Ini jalur paling praktis untuk MacBook atau workstation lokal.

### Linux via AppImage (Portabel, Tanpa Install Sistem)

```bash
# Download
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.appimage

# Jadikan executable
chmod +x kiro-cli.appimage

# Jalankan
./kiro-cli.appimage
```

Cocok kalau mau cepat testing atau di environment yang nggak punya akses `sudo`.

### Linux via Zip Installer (Recommended untuk Server)

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

### Ubuntu/Debian via `.deb`

```bash
# Download
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb

# Install
sudo dpkg -i kiro-cli.deb
sudo apt-get install -f
```

Jalur paling familiar buat user Ubuntu.

### Verifikasi Instalasi

```bash
kiro-cli --version
```

Kalau keluar versi, berarti instalasi berhasil. Catatan penting: command-nya `kiro-cli`, bukan `kiro`.

---

## 🔐 Login ke Kiro CLI

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

### Login dari VPS/Remote Server

Ini bagian yang sering bikin bingung. Ada dua pendekatan:

**1. Device Code Authentication (Recommended untuk VPS)**

AWS Builder ID dan IAM Identity Center mendukung device code — artinya kamu tinggal buka URL di browser lokal, masukkan kode, dan selesai. Nggak perlu tunnel atau konfigurasi tambahan.

**2. Port Forwarding (untuk GitHub/Google Social Login)**

Kalau mau pakai GitHub atau Google login dari VPS, OAuth callback-nya mengarah ke `localhost`. Jadi perlu SSH port forwarding:

```bash
ssh -L 49153:localhost:49153 -N user@server-kamu.com
```

Port `49153` bisa berbeda setiap sesi — sesuaikan dengan yang ditampilkan saat `kiro-cli login`. Jalankan ini di terminal lokal kamu, lalu buka Kiro CLI di sesi SSH server.

### Verifikasi: Health Check

```bash
kiro-cli doctor
```

**Catatan untuk user root:** Kalau kamu menjalankan Kiro CLI sebagai user `root` (umum di VPS), `kiro-cli doctor` mungkin menampilkan warning dan menyarankan flag tambahan:

```bash
kiro-cli doctor --all
```

Ini catatan praktis, bukan pengganti best practice keamanan. Kalau bisa, gunakan non-root user untuk production.

---

## 🚀 Tiga Mode Penggunaan Kiro CLI

### 1. Interactive Mode (Default)

```bash
cd /path/ke/project
kiro-cli
```

Masuk ke sesi chat interaktif. Bisa pakai `/editor` atau `Ctrl+J` untuk multi-line prompt. Cocok untuk eksplorasi dan debugging.

### 2. Resume Mode (Lanjutkan Sesi Sebelumnya)

Kiro menyimpan percakapan berbasis direktori. Jadi kalau tadi ngoding fitur A di repo X, besok bisa lanjut:

```bash
cd /path/ke/project
kiro-cli chat --resume
```

Sangat berguna untuk pengerjaan yang butuh beberapa sesi.

### 3. One-Shot Mode (Non-Interactive)

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

## 🤖 Menyuruh OpenClaw Ngoding via Kiro CLI

Nah, ini bagian inti. Karena Kiro CLI adalah command-line tool, OpenClaw bisa menjalankannya langsung dari `exec`. Kamu cukup kasih instruksi natural language ke OpenClaw.

### Pola Dasar

Berikut contoh instruksi yang bisa kamu kirim ke OpenClaw di Telegram:

> Masuk ke repo `/var/www/company-system`, lalu jalankan Kiro untuk audit dan perbaiki bug login yang return 500. Jangan commit dulu. Setelah selesai, laporkan akar masalah, file yang diubah, dan hasil test.

OpenClaw akan:
1. `cd` ke repo yang ditentukan
2. Menjalankan `kiro-cli` dengan prompt yang tepat
3. Membaca hasilnya
4. Melaporkan balik ke kamu

### Contoh Prompt Template

Berikut template yang bisa langsung dipakai dan dimodifikasi:

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

## 📋 AGENTS.md: Konsistensi Hasil AI Coding

Salah satu masalah umum AI coding: hasilnya kadang bagus, kadang nggak konsisten. Solusinya? `AGENTS.md`.

File ini ditaruh di root directory project dan berisi instruksi yang otomatis dibaca Kiro setiap kali dijalankan di repo tersebut. Isinya bisa berupa:

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

Dengan `AGENTS.md`, setiap kali Kiro (atau AI coding lain) bekerja di repo tersebut, ia sudah punya konteks tentang stack, konvensi, dan batasan. Hasilnya jauh lebih konsisten dan sesuai standar tim.

---

## 🏆 Best Practices

### 1. Mulai dari Task Kecil

Jangan langsung suruh Kiro ngerjain fitur gede. Mulai dari bug fix kecil atau refactor untuk ngeliat bagaimana dia memahami codebase kamu.

### 2. Prompt Spesifik > Prompt Umum

❌ "Tolong perbaiki bug"
✅ "Audit endpoint `/api/login` yang return 500 saat email tidak valid. Cari root cause, perbaiki, dan jalankan test."

### 3. Jangan Langsung Commit

Selalu minta Kiro untuk **jangan commit dulu**. Review hasilnya lewat OpenClaw, kalau sudah OK baru commit manual atau minta Kiro commit di iterasi berikutnya.

### 4. Gunakan Resume untuk Task Bertahap

Fitur besar butuh beberapa iterasi. Pakai `--resume` atau minta OpenClaw menjalankan Kiro di direktori yang sama agar konteks percakapan tetap tersambung.

### 5. `--trust-all-tools` Hanya di Development

Flag ini mematikan semua safety check Kiro. Gunakan **hanya** di environment development, bukan production.

### 6. selalu Ada AGENTS.md

Satu file kecil di root repo bisa bedain hasil Kiro dari "cukup bagus" jadi "sesuai standar tim".

---

## 📚 Link Penting

- [Dokumentasi Kiro CLI](https://docs.kiro.dev)
- [Kiro CLI Install Script](https://cli.kiro.dev/install)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Artikel Referensi — Rama Aditya](https://ramadigital.id/blog/cara-install-kiro-cli-dan-menyuruh-openclaw-ngoding-via-kiro-untuk-fix-bug-dan-tambah-fitur.md)

---

## Penutup

Kombinasi OpenClaw + Kiro CLI itu essentially punya AI programmer yang standby 24/7 di server kamu. Kamu kasih brief lewat chat, dia kerjain. Bug fix, tambah fitur, code review — semua bisa dikerjakan tanpa buka IDE.

Yang perlu diingat: AI coding itu **tool**, bukan pengganti programmer. Dia bagus untuk task yang well-defined dan scope-nya jelas. Untuk architectural decision atau bisnis logic yang kompleks, review manusia tetap wajib.

Mulai dari install, bikin `AGENTS.md`, terus coba task kecil dulu. Dari situ, scale up ke workflow yang lebih kompleks.
