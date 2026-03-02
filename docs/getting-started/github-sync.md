# 🔄 Sync OpenClaw Memory dengan GitHub

Tutorial lengkap untuk sinkronisasi memory OpenClaw ke GitHub, sehingga bisa berpindah-pindah PC/VPS/device tanpa kehilangan memori.

> 💡 **Kenapa GitHub Sync?**
> - ✅ Portable — pindah device, memori tetap sama
> - ✅ Backup otomatis — riwayat tersimpan di Git
> - ✅ Kolaborasi — bisa share agent dengan tim
> - ✅ Gratis — GitHub private repo gratis

---

## 📋 Persiapan

### 1. Buat Repository GitHub

1. Buka [github.com/new](https://github.com/new)
2. Nama repo: `openclaw-memory` (atau nama lain bebas)
3. Pilih **Private** (recommended, karena berisi data pribadi)
4. Jangan centang "Add README" (kita init dari lokal)
5. Klik **Create repository**

### 2. Ambil Personal Access Token (PAT)

GitHub mengharuskan token untuk autentikasi:

1. Buka [github.com/settings/tokens](https://github.com/settings/tokens)
2. Klik **Generate new token (classic)**
3. Note: `OpenClaw Sync`
4. Expiration: Pilih sesuai kebutuhan (bisa `No expiration`)
5. Centang scope:
   - ✅ `repo` (full control of private repositories)
6. Klik **Generate token**
7. **COPY TOKEN SEKARANG** (hanya muncul sekali!)

---

## 🚀 Setup di OpenClaw

### Struktur Folder yang Akan Di-Sync

```
~/.openclaw/
├── workspace/              ← Folder utama (wajib sync)
│   ├── SOUL.md
│   ├── USER.md
│   ├── MEMORY.md
│   ├── HEARTBEAT.md
│   ├── AGENTS.md
│   ├── TOOLS.md
│   ├── diary/
│   ├── memory/
│   └── skills/             ← Skills custom
├── skills/                 ← Global skills (optional)
└── config/                 ← Konfigurasi (optional)
```

### Step 1: Init Repository Lokal

```bash
# Masuk ke workspace OpenClaw
cd ~/.openclaw/workspace

# Init git repo
git init

# Tambahkan remote (ganti dengan URL repo kamu)
git remote add origin https://github.com/USERNAME/openclaw-memory.git

# Config user (nama dan email kamu)
git config user.name "Nama Kamu"
git config user.email "email@example.com"
```

### Step 2: Buat .gitignore

```bash
cd ~/.openclaw/workspace
cat > .gitignore << 'EOF'
# Secrets - JANGAN DIUPLOAD!
.env
.env.local
*.key
*.pem
credentials.json
n8n-credentials.json

# Cache & Temporary
__pycache__/
*.pyc
.pytest_cache/
node_modules/
.npm
.cache/
*.log
logs/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Large files (optional, bisa diupload kalau perlu)
# *.png
# *.jpg
# *.mp3
# *.mp4
EOF
```

### Step 3: Commit Pertama

```bash
cd ~/.openclaw/workspace

# Tambahkan semua file (kecuali yang di .gitignore)
git add .

# Commit
git commit -m "Initial commit: OpenClaw memory sync

- SOUL.md, USER.md, MEMORY.md
- HEARTBEAT.md, AGENTS.md, TOOLS.md
- Diary dan memory folders
- Custom skills"

# Push ke GitHub
git push -u origin main
```

Masukkan **Personal Access Token** sebagai password ketika diminta.

---

## ⏰ Auto-Sync dengan Cron

### Setup Cron untuk Auto-Push

```bash
# Buka crontab
crontab -e
```

Tambahkan baris berikut:

```bash
# Auto-sync OpenClaw memory ke GitHub setiap 15 menit
*/15 * * * * cd ~/.openclaw/workspace && git add -A && git diff --cached --quiet || (git commit -m "Auto-sync: $(date '+\%Y-\%m-\%d \%H:\%M')" && git push origin main)
```

Penjelasan:
- `*/15 * * * *` → Jalankan tiap 15 menit
- `git add -A` → Stage semua perubahan
- `git diff --cached --quiet` → Cek ada perubahan atau tidak
- Kalau ada perubahan → commit dengan timestamp → push

### Alternatif: Auto-Sync Script (Lebih Robust)

Buat file script:

```bash
mkdir -p ~/.openclaw/scripts
cat > ~/.openclaw/scripts/sync-memory.sh << 'EOF'
#!/bin/bash
# OpenClaw Memory Sync Script

REPO_DIR="$HOME/.openclaw/workspace"
LOG_FILE="$HOME/.openclaw/logs/sync.log"

# Pastikan log directory ada
mkdir -p "$(dirname "$LOG_FILE")"

# Fungsi logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if repo exists
if [ ! -d "$REPO_DIR/.git" ]; then
    log "ERROR: Not a git repository: $REPO_DIR"
    exit 1
fi

cd "$REPO_DIR" || exit 1

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
    log "No changes to sync"
    exit 0
fi

# Sync process
log "Starting sync..."

# Pull first to avoid conflicts
git pull origin main --rebase 2>>"$LOG_FILE"
if [ $? -ne 0 ]; then
    log "ERROR: Pull failed, possible conflict"
    exit 1
fi

# Add all changes
git add -A

# Commit with timestamp
COMMIT_MSG="Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')

Changes:
$(git diff --cached --stat | tail -1)"

git commit -m "$COMMIT_MSG" 2>>"$LOG_FILE"
if [ $? -ne 0 ]; then
    log "ERROR: Commit failed"
    exit 1
fi

# Push to GitHub
git push origin main 2>>"$LOG_FILE"
if [ $? -eq 0 ]; then
    log "SUCCESS: Sync completed"
else
    log "ERROR: Push failed"
    exit 1
fi
EOF

chmod +x ~/.openclaw/scripts/sync-memory.sh
```

Update crontab:

```bash
# Auto-sync tiap 15 menit pakai script
*/15 * * * * /root/.openclaw/scripts/sync-memory.sh
```

---

## 🖥️ Setup di Device Baru (Clone)

Ketika pindah ke PC/VPS baru:

### Step 1: Install OpenClaw

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

### Step 2: Clone Memory Repo

```bash
# Buat folder .openclaw
mkdir -p ~/.openclaw

# Clone repo (ganti dengan URL kamu)
git clone https://github.com/USERNAME/openclaw-memory.git ~/.openclaw/workspace

# Masukkan Personal Access Token sebagai password
```

### Step 3: Setup Git Config

```bash
cd ~/.openclaw/workspace
git config user.name "Nama Kamu"
git config user.email "email@example.com"
```

### Step 4: Setup Auto-Sync (Sama seperti di atas)

```bash
crontab -e
# Tambahkan baris auto-sync
```

**Done!** Sekarang OpenClaw di device baru punya memori yang sama persis.

---

## 🔄 Workflow Sinkronisasi

### Alur Kerja (Multi-Device)

```
Device A (Laptop)
    ↓ (auto-push tiap 15 min)
GitHub Repository
    ↓ (auto-pull saat startup)
Device B (VPS)
    ↓ (auto-push tiap 15 min)
GitHub Repository
    ↓
Device C (PC Kantor)
```

### Manual Sync (Kalau Perlu)

**Push manual:**
```bash
cd ~/.openclaw/workspace
git add -A
git commit -m "Update: deskripsi perubahan"
git push origin main
```

**Pull manual (force refresh):**
```bash
cd ~/.openclaw/workspace
git pull origin main
```

---

## 🛠️ Advanced: Git Credential Helper

Untuk menghindari input token berulang kali:

### Opsi 1: Cache Credential (Lokal)

```bash
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'  # 1 jam
```

### Opsi 2: Store Credential (Permanent)

```bash
git config --global credential.helper store
# Token akan tersimpan di ~/.git-credentials
# ⚠️ Risiko keamanan kalau device shared
```

### Opsi 3: SSH Key (Recommended untuk VPS)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Paste ke GitHub → Settings → SSH and GPG keys → New SSH key

# Update remote URL ke SSH
cd ~/.openclaw/workspace
git remote set-url origin git@github.com:USERNAME/openclaw-memory.git
```

---

## 📁 Struktur Repo yang Baik

Rekomendasi struktur untuk multi-device:

```
openclaw-memory/
├── README.md                 # Dokumentasi repo
├── .gitignore               # File yang diexclude
├── SOUL.md                  # Personality agent
├── USER.md                  # Data user
├── MEMORY.md                # Long-term memory
├── HEARTBEAT.md             # Periodic tasks
├── AGENTS.md                # Agent rules
├── TOOLS.md                 # Tool notes
├── IDENTITY.md              # Identity agent
├── BOOTSTRAP.md             # First-run instructions
├── diary/                   # Daily reflections
│   ├── 2026-03-01.md
│   └── 2026-03-02.md
├── memory/                  # Daily logs
│   ├── 2026-03-01.md
│   └── 2026-03-02.md
├── tasks/                   # Task tracking
│   ├── todo.md
│   └── lessons.md
├── skills/                  # Custom skills
│   └── my-skill/
│       └── SKILL.md
└── scripts/                 # Utility scripts
    └── sync-memory.sh
```

---

## ⚠️ Tips & Troubleshooting

### 1. Merge Conflict

Kalau ada conflict (edit di 2 device sekaligus):

```bash
cd ~/.openclaw/workspace

# Pull dengan rebase
git pull origin main --rebase

# Kalau conflict, edit file yang bermasalah
# Lalu:
git add .
git rebase --continue
git push origin main
```

### 2. File Besar (Large Files)

Kalau ada file besar (>100MB), GitHub akan reject:

```bash
# Cek file besar
cd ~/.openclaw/workspace
git ls-files | xargs -I {} sh -c 'du -h "$1" | grep -E "^[0-9]+M"' _ {}

# Tambahkan ke .gitignore atau gunakan Git LFS
```

### 3. Private Repo vs Public

**Selalu pakai Private Repo** karena berisi:
- Data pribadi (USER.md)
- Token/API keys (meski di .gitignore, mending aman)
- Diary dan memory pribadi

### 4. Backup Berkala

Meski sudah sync, tetap backup ke tempat lain:

```bash
# Export ke ZIP tiap minggu
zip -r ~/backups/openclaw-backup-$(date +%Y%m%d).zip ~/.openclaw/workspace
```

### 5. Multiple Agents (Radit, Raka, Rama, Rafi)

Kalau punya multi-agent, struktur reponya:

```
openclaw-memory/
├── radit/                   # Agent Radit
│   ├── SOUL.md
│   ├── USER.md
│   └── ...
├── raka/                    # Agent Raka
│   ├── SOUL.md
│   └── ...
├── rama/                    # Agent Rama
│   └── ...
└── rafi/                    # Agent Rafi
    └── ...
```

Masing-masing folder di-sync ke workspace agent-nya:

```bash
# Device Radit
cd ~/.openclaw/workspace-radit
git clone https://github.com/USERNAME/openclaw-memory.git temp
cp -r temp/radit/* .
```

---

## 🎯 Checklist Setup

- [ ] Buat repo private di GitHub
- [ ] Generate Personal Access Token
- [ ] Init git di `~/.openclaw/workspace`
- [ ] Buat `.gitignore` untuk exclude secrets
- [ ] Commit dan push pertama
- [ ] Setup cron auto-sync tiap 15 menit
- [ ] Test clone di device kedua
- [ ] Setup credential helper (opsional)

---

## 💬 FAQ

**Q: Apakah ini aman?**
A: Ya, selama repo-nya private dan .gitignore-nya benar. Jangan pernah commit file `.env` atau credentials.

**Q: Berapa lama sync-nya?**
A: Biasanya < 5 detik, tergantung koneksi dan ukuran repo.

**Q: Bisa pakai GitLab/Bitbucket?**
A: Bisa! Workflow-nya sama persis, tinggal ganti URL remote.

**Q: Kalau ada conflict terus?**
A: Hindari edit file yang sama di 2 device bersamaan. Atau pakai strategi: 1 device untuk write, lainnya read-only.

**Q: Skills ikut tersync juga?**
A: Ya, kalau skills-nya di folder `~/.openclaw/workspace/skills/`.

---

## 🔗 Link Terkait

- [GitHub Docs - Create a repo](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [GitHub Docs - Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Git Credential Helper](https://git-scm.com/docs/gitcredentials)

---

Dibuat dengan ❤️ oleh komunitas Sumopod
