# 🖥️ OpenClaw di Windows - Tutorial Lengkap

Panduan komplit install, setup auto-start, dan manage OpenClaw di Windows.

---

## 📋 Prerequisites

- Windows 10/11 (64-bit)
- Node.js 18+ 
- NPM (include saat install Node.js)
- Koneksi internet

### Install Node.js

1. Download dari [nodejs.org](https://nodejs.org) (pilih LTS version)
2. Run installer → Next → Next → Finish
3. Verify:
   ```powershell
   node --version
   npm --version
   ```

---

## 🚀 Step 1: Install OpenClaw

Buka **PowerShell** atau **Command Prompt** (bisa pakai Windows Terminal):

```powershell
# Install OpenClaw globally
npm install -g openclaw@latest

# Verifikasi install
openclaw --version
```

**Kalau ada error permission:**
```powershell
# Run as Administrator
# Atau install di user folder
npm install -g openclaw@latest --prefix "%APPDATA%\npm"
```

---

## ⚙️ Step 2: Setup Pertama (Onboard)

```powershell
# Jalankan wizard setup
openclaw onboard
```

Ikuti instruksi:
1. Pilih AI provider (OpenAI, Claude, Kimi, dll)
2. Masukkan API key
3. Setup workspace folder
4. Pilih channel (Telegram, Discord, dll)

**Workspace location:**
```
C:\Users\[USERNAME]\.openclaw\workspace\
```

---

## 🏃 Step 3: Start Gateway

### Cara Manual (Untuk Test)

```powershell
openclaw gateway start
```

**⚠️ Jangan close PowerShell!** Biarkan jalan di background.

**Check status:**
```powershell
openclaw gateway status
```

Kalau output:
```
Gateway running on ws://127.0.0.1:18789
```
→ ✅ Berhasil!

---

## 🔄 Step 4: Auto-Start (Persistency)

### Opsi A: Windows Service (Recommended untuk Server)

**Catatan:** `openclaw service` command tidak tersedia di Windows. Gunakan alternatif:

#### Menggunakan NSSM (Non-Sucking Service Manager)

```powershell
# Download NSSM
curl -L -o nssm.zip https://nssm.cc/release/nssm-2.24.zip
Expand-Archive nssm.zip -DestinationPath C:\Tools

# Install OpenClaw sebagai service
C:\Tools\nssm-2.24\win64\nssm.exe install OpenClawGateway

# Isi form yang muncul:
# Path: C:\Program Files\nodejs\node.exe
# Arguments: C:\Users\[USERNAME]\AppData\Roaming\npm\node_modules\openclaw\bin\openclaw.js gateway start
# Working directory: C:\Users\[USERNAME]

# Start service
net start OpenClawGateway

# Enable auto-start
sc config OpenClawGateway start= auto
```

#### Menggunakan WinSW (Windows Service Wrapper)

```powershell
# Download WinSW
curl -L -o winsw.exe https://github.com/winsw/winsw/releases/download/v2.12.0/WinSW-x64.exe

# Buat config file
@"<?xml version="1.0" encoding="utf-8" ?>
<service>
  <id>OpenClawGateway</id>
  <name>OpenClaw Gateway</name>
  <description>OpenClaw AI Gateway</description>
  <executable>C:\Program Files\nodejs\node.exe</executable>
  <arguments>C:\Users\[USERNAME]\AppData\Roaming\npm\node_modules\openclaw\bin\openclaw.js gateway start</arguments>
  <loglevel>INFO</loglevel>
</service>
"@ | Out-File -FilePath "winsw.xml" -Encoding utf8

# Install dan start
.\winsw.exe install
.\winsw.exe start
```

### Opsi B: Task Scheduler (Simple)

```powershell
# Create task
schtasks /create /tn "OpenClaw Gateway" /tr "openclaw gateway start" /sc onlogon /rl highest /f

# Run task
schtasks /run /tn "OpenClaw Gateway"
```

**Tapi sering error!** Kalau timeout, gunakan Opsi C.

### Opsi C: Startup Folder (Paling Simple)

```powershell
# Buka startup folder
explorer "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
```

Buat file baru: `start-openclaw.bat`

```batch
@echo off
echo Starting OpenClaw Gateway...
openclaw gateway start
```

Save di folder Startup. Gateway akan auto-start saat login.

### Opsi D: VBScript (Hidden Window)

Buat file: `C:\Tools\start-openclaw.vbs`

```vbscript
Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "C:\Tools\start-openclaw.bat" & Chr(34), 0
Set WshShell = Nothing
```

File `start-openclaw.bat`:
```batch
@echo off
openclaw gateway start > C:\Users\[USERNAME]\.openclaw\gateway.log 2>&1
```

Add shortcut ke Startup folder.

---

## 🛠️ Step 5: Management & Monitoring

### Check Status

```powershell
# Gateway status
openclaw gateway status

# Logs
openclaw logs --follow

# Doctor (check issues)
openclaw doctor
```

### Restart Gateway

```powershell
# Soft restart
openclaw gateway restart

# Hard restart (kalau stuck)
taskkill /F /IM node.exe
openclaw gateway start
```

### Update OpenClaw

```powershell
# Stop gateway dulu
taskkill /F /IM node.exe

# Update
npm install -g openclaw@latest

# Start ulang
openclaw gateway start
```

### Backup & Restore

```powershell
# Backup config dan memory
Compress-Archive -Path "$env:USERPROFILE\.openclaw\workspace" -DestinationPath "openclaw-backup.zip"

# Restore
Expand-Archive -Path "openclaw-backup.zip" -DestinationPath "$env:USERPROFILE\.openclaw"
```

---

## 🔧 Troubleshooting Windows

### Error: "openclaw is not recognized"

```powershell
# Add npm global ke PATH
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";" + $env:APPDATA + "\npm", "User")

# Restart PowerShell
```

### Error: "Port 18789 already in use"

```powershell
# Cek yang pakai port
netstat -ano | findstr "18789"

# Kill process
taskkill /F /PID [PID_NUMBER]

# Atau ganti port
openclaw gateway start --port 18790
```

### Error: Gateway start tapi timeout

```powershell
# Cek log
Get-Content "$env:LOCALAPPDATA\Temp\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log" -Tail 50

# Fix: Jalankan tanpa service
openclaw gateway start
```

### Service tidak mau start

Biasanya karena:
1. Path Node.js salah
2. Permission denied
3. Port conflict

**Solusi:** Gunakan Opsi C (Startup Folder) - paling reliable.

---

## 📱 Integrasi dengan Telegram

### Setup Telegram Bot

1. Chat @BotFather di Telegram
2. Kirim `/newbot`
3. Isi nama dan username bot
4. Copy token

### Config OpenClaw

Edit file: `C:\Users\[USERNAME]\.openclaw\openclaw.json`

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN_HERE"
    }
  }
}
```

Restart gateway:
```powershell
openclaw gateway restart
```

### Test

Kirim pesan ke bot di Telegram → Harusnya langsung respon!

---

## 💡 Tips Windows

### 1. Minimize to Tray

Pakai tool tambahan:
- **RBTray** - Minimize window ke system tray
- **TrayIt!** - Auto-minimize saat start

### 2. Auto-Restart kalau Crash

Buat script: `C:\Tools\monitor-openclaw.bat`

```batch
@echo off
:loop
timeout /t 30 > nul
tasklist | find "node.exe" > nul
if errorlevel 1 (
    echo %date% %time% - Gateway down, restarting...
    openclaw gateway start
)
goto loop
```

Jalankan juga di Startup.

### 3. File Organizer (Downloads)

OpenClaw bisa bersih-bersih PC! Chat ke bot:

```
"Rapikan folder Downloads ku, buat 5 kategori folder"
```

Bot akan auto-organize file:
- Installers (EXE, MSI)
- Documents (PDF, DOCX)
- Images (JPG, PNG)
- Media (MP4, M4A)
- Archives (ZIP, JSON)

---

## 🎯 Checklist Setup Windows

- [ ] Install Node.js
- [ ] Install OpenClaw (`npm install -g openclaw`)
- [ ] Run `openclaw onboard`
- [ ] Test `openclaw gateway start`
- [ ] Setup auto-start (pilih: Service/Task/Startup)
- [ ] Config Telegram bot (optional)
- [ ] Test dari Telegram/HP
- [ ] Backup config ke GitHub (optional)

---

## 🔗 Link Terkait

- [OpenClaw Docs](https://docs.openclaw.ai)
- [Node.js Download](https://nodejs.org)
- [NSSM Service Manager](https://nssm.cc)
- [GitHub - OpenClaw Sumopod](https://github.com/fanani-radian/openclaw-sumopod)

---

*Tutorial by: Sumopod Community*
