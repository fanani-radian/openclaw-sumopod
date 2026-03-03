# 🔧 Install Gog CLI di OpenClaw

Tutorial simpel setup Google Workspace CLI (gog) untuk akses Gmail, Calendar, Drive, dll.

---

## 📋 Apa itu Gog?

**Gog** = Google Workspace CLI  
Akses Gmail, Calendar, Drive, Contacts, Docs, Sheets dari terminal!

---

## Step 1: Install Gog

```bash
# Download latest release
curl -fsSL https://github.com/rubiojr/gog/releases/latest/download/gog-linux-amd64 -o /usr/local/bin/gog

# Beri permission execute
chmod +x /usr/local/bin/gog

# Verify install
gog --version
```

---

## Step 2: Buat Project di Google Cloud Console

### 2.1 Buka Google Cloud Console
1. Kunjungi: https://console.cloud.google.com
2. Login dengan akun Google kamu
3. Klik **"Select a project"** → **"New Project"**
4. Nama project: `openclaw-gog` (bebas)
5. Klik **"Create"**

### 2.2 Enable APIs
1. Menu sidebar → **"APIs & Services"** → **"Library"**
2. Cari dan enable satu per satu:
   - ✅ Gmail API
   - ✅ Google Calendar API
   - ✅ Google Drive API
   - ✅ Google Docs API
   - ✅ Google Sheets API
   - ✅ People API (untuk Contacts)

### 2.3 Buat OAuth Credentials
1. Menu sidebar → **"APIs & Services"** → **"Credentials"**
2. Klik **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Klik **"Configure consent screen"** (kalau belum)
   - User Type: **External**
   - App name: `OpenClaw Gog`
   - User support email: (email kamu)
   - Developer contact: (email kamu)
   - Klik **"Save and Continue"** 3x
   - Klik **"Back to Dashboard"**

4. Kembali ke **"Credentials"** → **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
   - Application type: **Desktop app**
   - Name: `OpenClaw Desktop`
   - Klik **"Create"**

5. **Download JSON** → simpan sebagai `client_secret.json`

---

## Step 3: Setup Gog

### 3.1 Pindahkan credentials
```bash
# Buat folder config
mkdir -p ~/.config/gog

# Pindahkan file credentials
cp /path/to/client_secret.json ~/.config/gog/client_secret.json
```

### 3.2 Login
```bash
# Jalankan login
gog auth login
```

**Proses:**
1. Browser akan terbuka otomatis
2. Pilih akun Google kamu
3. Klik **"Allow"** untuk semua permission
4. Copy **authorization code**
5. Paste di terminal
6. Done! ✅

---

## Step 4: Test Gog

```bash
# Cek akun
gog auth status

# List email Gmail
gog gmail list --max=5

# List event Calendar hari ini
gog calendar events list --today

# List file di Drive
gog drive list --max=10

# Search contact
gog contacts search "nama"
```

---

## Step 5: Integrasi ke OpenClaw

### 5.1 Simpan credentials ke environment
```bash
# Tambahkan ke ~/.bashrc atau ~/.zshrc
echo 'export GOG_ACCOUNT="email-kamu@gmail.com"' >> ~/.bashrc
echo 'export GOG_KEYRING_PASSWORD="password-aman-mu"' >> ~/.bashrc

# Reload
source ~/.bashrc
```

### 5.2 Test dari OpenClaw
```bash
# Di terminal OpenClaw
gog gmail search "is:unread" --max=5
```

---

## 🔧 Troubleshooting

### Error: "Token has been expired or revoked"
```bash
# Re-login
gog auth logout
gog auth login
```

### Error: "unauthorized_client"
- Pastikan **Desktop app** dipilih (bukan Web app)
- Download ulang `client_secret.json`

### Browser tidak terbuka
```bash
# Copy URL yang muncul di terminal
# Buka manual di browser
# Paste authorization code
```

---

## 💡 Tips Penggunaan

```bash
# Gmail: Mark as read
gog gmail modify --ids=MESSAGE_ID --read

# Gmail: Kirim email
gog gmail send --to="target@email.com" --subject="Hello" --body="Pesan"

# Calendar: Buat event
gog calendar events create --summary="Meeting" --start="2026-03-05T10:00:00" --end="2026-03-05T11:00:00"

# Drive: Upload file
gog drive upload --file=/path/to/file.pdf --folder="MyFolder"

# Docs: Baca document
gog docs get --id=DOCUMENT_ID
```

---

## 📚 Resources

- Gog GitHub: https://github.com/rubiojr/gog
- Google Cloud Console: https://console.cloud.google.com
- OpenClaw Docs: https://docs.openclaw.ai

---

*Tutorial by: OpenClaw Sumopod Community*
