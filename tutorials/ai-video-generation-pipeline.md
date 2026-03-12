# 🎬 Auto-Generate Video dengan AI dan Upload ke Cloud Storage

> **Level:** Intermediate  
> **Time:** 20-30 menit  > **Cost:** Varies (AI video generation API)

---

## 📋 Apa yang Akan Kamu Bangun

Di tutorial ini, kita akan membuat **pipeline otomatis** untuk:
1. Generate video menggunakan AI (text-to-video)
2. Upload hasil video ke cloud storage (Google Drive)
3. Dapatkan notifikasi via Telegram saat selesai

**Use cases:**
- Content creator: Batch generate video clips
- Marketing: Auto-generate promo videos
- Education: Generate tutorial videos dari script

**Flow:**
```
Telegram: "/genvideo Sunset over mountains"
           ↓
    [OpenClaw → AI Video API]
           ↓
    Video generated (MP4)
           ↓
    [Upload to Google Drive]
           ↓
    Telegram: "✅ Video ready: [Drive Link]"
```

---

## 🎯 Prerequisites

| Requirement | Status | Notes |
|-------------|--------|-------|
| OpenClaw terinstall | ✅ Wajib | [Install Guide](https://docs.openclaw.ai) |
| AI Video API access | ✅ Wajib | Veo, Runway, atau Pika |
| Google Drive API | ✅ Wajib | Service account |
| Python 3.8+ | ✅ Wajib | `python3 --version` |
| Sufficient API quota | ⭐ Check | Video generation mahal |

---

## 🚀 Step 1: Setup AI Video API

### 1.1 Pilih Provider

| Provider | Pros | Cons | Pricing |
|----------|------|------|---------|
| **Google Veo** | High quality, 8s/clip | Limited access | $0.05-0.20/sec |
| **Runway ML** | Great effects, 4s-16s | Queue times | $0.01-0.05/sec |
| **Pika Labs** | Fast, easy UI | Lower quality | $0.01-0.03/sec |
| **Stable Video** | Open source | Setup complex | Self-hosted |

Untuk tutorial ini, kita pakai pattern yang generic dan bisa adapt ke semua provider.

### 1.2 Dapatkan API Key

**Contoh: Google Veo (via Vertex AI)**

1. Buka [Google Cloud Console](https://console.cloud.google.com)
2. Enable **Vertex AI API**
3. Create service account → Download JSON key
4. Simpan sebagai `~/.config/gcloud/vertex-ai-key.json`

**Contoh: Runway ML**

1. Buka [Runway Dashboard](https://runwayml.com)
2. Settings → API Keys
3. Generate new key
4. Simpan di environment variable: `export RUNWAY_API_KEY="xxx"`

---

## 🔧 Step 2: Setup Google Drive API

### 2.1 Create Service Account

1. Buka [Google Cloud Console](https://console.cloud.google.com)
2. APIs & Services → Credentials
3. Create Credentials → Service Account
4. Grant role: **Drive File Creator**
5. Create Key → Download JSON
6. Simpan sebagai `~/.config/gcloud/drive-service-account.json`

### 2.2 Share Drive Folder

1. Buat folder di Google Drive: `AI-Generated-Videos`
2. Share folder dengan service account email:
   - Klik Share
   - Add: `your-service@project.iam.gserviceaccount.com`
   - Role: Editor
3. Copy **Folder ID** dari URL:
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HERE
   ```

---

## 💻 Step 3: Build Main Script

### 3.1 Buat Project Structure

```bash
mkdir -p ~/ai-video-pipeline/{scripts,output,logs}
cd ~/ai-video-pipeline
```

### 3.2 Video Generation Script

Buat `scripts/generate_video.py`:

```python
#!/usr/bin/env python3
"""
AI Video Generation + Cloud Upload Pipeline
Generate video from text prompt and upload to Google Drive
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime

# 🔧 CONFIG
CONFIG = {
    # AI Video Provider: 'veo', 'runway', 'pika'
    "provider": os.getenv("VIDEO_PROVIDER", "runway"),
    
    # API Keys (use environment variables!)
    "runway_api_key": os.getenv("RUNWAY_API_KEY"),
    "veo_project_id": os.getenv("VEO_PROJECT_ID"),
    
    # Google Drive
    "drive_folder_id": os.getenv("DRIVE_FOLDER_ID"),
    "drive_service_account": os.path.expanduser("~/.config/gcloud/drive-service-account.json"),
    
    # Output
    "output_dir": os.path.expanduser("~/ai-video-pipeline/output"),
    "max_duration": 8,  # seconds
}


def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def generate_video_runway(prompt: str, duration: int = 4) -> str:
    """
    Generate video using Runway ML API
    Returns: video_url or None
    """
    api_key = CONFIG["runway_api_key"]
    if not api_key:
        raise ValueError("RUNWAY_API_KEY not set!")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Create generation task
    payload = {
        "prompt": prompt,
        "duration": duration,  # 4 or 10 seconds
        "ratio": "16:9",  # or "9:16" for vertical
    }
    
    log(f"🎬 Submitting video generation task...")
    log(f"📝 Prompt: {prompt[:60]}...")
    
    response = requests.post(
        "https://api.runwayml.com/v1/generations",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code != 200:
        log(f"❌ Error creating task: {response.text}")
        return None
    
    task_id = response.json().get("id")
    log(f"⏳ Task created: {task_id}")
    
    # Poll for completion (Runway takes 30-120 seconds)
    max_attempts = 60
    for attempt in range(max_attempts):
        time.sleep(5)
        
        status_resp = requests.get(
            f"https://api.runwayml.com/v1/generations/{task_id}",
            headers=headers,
            timeout=30
        )
        
        status_data = status_resp.json()
        status = status_data.get("status")
        
        log(f"   Attempt {attempt+1}/{max_attempts}: {status}")
        
        if status == "succeeded":
            video_url = status_data.get("url")
            log(f"✅ Video generated!")
            return video_url
        elif status == "failed":
            log(f"❌ Generation failed: {status_data.get('error')}")
            return None
    
    log("❌ Timeout waiting for video generation")
    return None


def download_video(url: str, filename: str) -> str:
    """Download video to local storage"""
    output_path = Path(CONFIG["output_dir"]) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    log(f"⬇️  Downloading video...")
    response = requests.get(url, stream=True, timeout=120)
    
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    log(f"✅ Downloaded: {output_path}")
    return str(output_path)


def upload_to_drive(local_path: str, filename: str) -> str:
    """
    Upload video to Google Drive
    Returns: Drive file URL
    """
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    
    # Authenticate
    credentials = service_account.Credentials.from_service_account_file(
        CONFIG["drive_service_account"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    
    service = build("drive", "v3", credentials=credentials)
    
    # Upload file
    file_metadata = {
        "name": filename,
        "parents": [CONFIG["drive_folder_id"]]
    }
    
    media = MediaFileUpload(local_path, resumable=True)
    
    log(f"☁️  Uploading to Google Drive...")
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()
    
    drive_link = file.get("webViewLink")
    log(f"✅ Uploaded: {drive_link}")
    
    # Make publicly viewable (optional)
    service.permissions().create(
        fileId=file.get("id"),
        body={"role": "reader", "type": "anyone"}
    ).execute()
    
    return drive_link


def process_video_generation(prompt: str) -> dict:
    """
    Main pipeline: Generate → Download → Upload
    """
    result = {
        "success": False,
        "prompt": prompt,
        "local_path": None,
        "drive_link": None,
        "error": None
    }
    
    try:
        # 1. Generate video
        video_url = generate_video_runway(prompt)
        if not video_url:
            result["error"] = "Video generation failed"
            return result
        
        # 2. Download
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_video_{timestamp}.mp4"
        local_path = download_video(video_url, filename)
        result["local_path"] = local_path
        
        # 3. Upload to Drive
        drive_link = upload_to_drive(local_path, filename)
        result["drive_link"] = drive_link
        result["success"] = True
        
        log(f"🎉 Pipeline complete!")
        
    except Exception as e:
        log(f"❌ Error: {str(e)}")
        result["error"] = str(e)
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_video.py [prompt]")
        print('Example: python3 generate_video.py "Sunset over mountains"')
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    result = process_video_generation(prompt)
    
    # Output result as JSON for OpenClaw parsing
    print(json.dumps(result, indent=2))
```

### 3.3 Install Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

### 3.4 Test Manual

```bash
export RUNWAY_API_KEY="your_api_key_here"
export DRIVE_FOLDER_ID="your_folder_id_here"

python3 scripts/generate_video.py "Drone flying over beach at sunset"
```

**Expected output:**
```json
{
  "success": true,
  "prompt": "Drone flying over beach at sunset",
  "local_path": "/home/user/ai-video-pipeline/output/ai_video_20240312_143052.mp4",
  "drive_link": "https://drive.google.com/file/d/xxx/view",
  "error": null
}
```

---

## 🔗 Step 4: Integrasi dengan OpenClaw

### 4.1 Buat Command Wrapper

Buat `scripts/video-to-drive.sh`:

```bash
#!/bin/bash
# Telegram command wrapper untuk video generation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$HOME/ai-video-pipeline/output"

# Load environment variables
export RUNWAY_API_KEY="${RUNWAY_API_KEY:-}"
export DRIVE_FOLDER_ID="${DRIVE_FOLDER_ID:-}"

# Validasi input
if [ -z "$1" ]; then
    echo "❌ Usage: /genvideo [description]"
    echo "Example: /genvideo Drone flying over mountains"
    exit 1
fi

PROMPT="$*"

echo "🎬 Starting video generation..."
echo "📝 Prompt: $PROMPT"
echo "⏳ This may take 1-3 minutes..."

# Run generation
RESULT=$(python3 "$SCRIPT_DIR/generate_video.py" "$PROMPT")

# Parse result
SUCCESS=$(echo "$RESULT" | grep -o '"success": true')
DRIVE_LINK=$(echo "$RESULT" | grep -o '"drive_link": "[^"]*' | cut -d'"' -f4)
LOCAL_PATH=$(echo "$RESULT" | grep -o '"local_path": "[^"]*' | cut -d'"' -f4)
ERROR=$(echo "$RESULT" | grep -o '"error": "[^"]*' | cut -d'"' -f4)

if [ -n "$SUCCESS" ]; then
    echo ""
    echo "✅ Video Generated Successfully!"
    echo ""
    echo "📁 Local: $LOCAL_PATH"
    echo "☁️  Drive: $DRIVE_LINK"
    echo ""
    echo "🎬 Prompt: $PROMPT"
else
    echo ""
    echo "❌ Generation Failed"
    echo "Error: ${ERROR:-Unknown error}"
fi
```

Jadikan executable:
```bash
chmod +x scripts/video-to-drive.sh
```

### 4.2 Setup Environment Variables

Buat file `~/.ai-video-env`:

```bash
# AI Video API
export RUNWAY_API_KEY="rk_xxxxxxxxxxxxxxxx"
# export VEO_PROJECT_ID="your-vertex-project"

# Google Drive
export DRIVE_FOLDER_ID="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbsxxxxxxxx"

# Optional: Telegram notification
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
export TELEGRAM_CHAT_ID="123456789"
```

Load saat login:
```bash
echo "source ~/.ai-video-env" >> ~/.bashrc
source ~/.bashrc
```

### 4.3 Integrasi dengan OpenClaw

Update `HEARTBEAT.md` atau commands:

```markdown
### 🎬 AI Video Generation

- **/genvideo [description]** → Generate video dan upload ke Drive
  Execute: `source ~/.ai-video-env && bash ~/ai-video-pipeline/scripts/video-to-drive.sh "[description]"`
  Example: `/genvideo Sunset over mountain range`
  
- **/genvidstatus** → Check recent generations
  Execute: `ls -lt ~/ai-video-pipeline/output | head -5`
```

---

## 🎨 Step 5: Advanced Features

### 5.1 Batch Generation dari File

Buat `scripts/batch_generate.py`:

```python
#!/usr/bin/env python3
"""Batch generate videos dari text file"""

import sys
from generate_video import process_video_generation

def batch_process(prompts_file):
    with open(prompts_file, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"Processing {i}/{len(prompts)}: {prompt[:50]}...")
        print('='*60)
        
        result = process_video_generation(prompt)
        results.append(result)
        
        if result['success']:
            print(f"✅ Done: {result['drive_link']}")
        else:
            print(f"❌ Failed: {result['error']}")
    
    # Summary
    success_count = sum(1 for r in results if r['success'])
    print(f"\n{'='*60}")
    print(f"Batch complete: {success_count}/{len(prompts)} successful")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 batch_generate.py prompts.txt")
        sys.exit(1)
    
    batch_process(sys.argv[1])
```

Buat `prompts.txt`:
```
Drone flying over tropical beach
Time lapse of city traffic at night
Abstract flowing liquid metal
Space nebula with stars
Underwater coral reef scene
```

Run:
```bash
python3 scripts/batch_generate.py prompts.txt
```

### 5.2 Telegram Notification

Tambahkan notifikasi saat selesai:

```python
def notify_telegram(message: str):
    """Send notification to Telegram"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    requests.post(url, json=payload, timeout=10)

# Gunakan di process_video_generation:
if result["success"]:
    notify_telegram(f"🎬 *Video Generated!*\n\n{result['drive_link']}")
```

### 5.3 Video Templates

Buat template system:

```python
TEMPLATES = {
    "nature": "Beautiful {subject} in 4K nature documentary style",
    "urban": "Cinematic shot of {subject}, cyberpunk city aesthetic",
    "abstract": "Fluid abstract visualization of {subject}, vibrant colors",
    "product": "Sleek product showcase of {subject}, studio lighting"
}

def generate_from_template(template_name: str, subject: str):
    template = TEMPLATES.get(template_name, TEMPLATES["nature"])
    prompt = template.format(subject=subject)
    return process_video_generation(prompt)

# Usage: /genvideo template nature waterfall
```

---

## ✅ Step 6: Testing & Troubleshooting

### 6.1 Test Checklist

| Test | Command | Expected Result |
|------|---------|-----------------|
| API connectivity | `curl -H "Authorization: Bearer $RUNWAY_API_KEY" https://api.runwayml.com/v1/health` | 200 OK |
| Drive auth | `python3 -c "from generate_video import upload_to_drive; print('OK')"` | No error |
| Full pipeline | `/genvideo Test video` | Video in Drive |
| Batch mode | `python3 batch_generate.py prompts.txt` | All videos generated |

### 6.2 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "API key invalid" | Wrong key | Check `RUNWAY_API_KEY` env var |
| "Drive permission denied" | Folder not shared | Share Drive folder dengan service account |
| "Timeout waiting" | Long queue | Tunggu atau coba off-peak hours |
| "Video too short" | Duration limit | Check provider limits (Veo max 8s) |
| "Upload failed" | Network issue | Retry atau check Drive API quota |

### 6.3 Cost Monitoring

Tambahkan cost tracking:

```python
COST_PER_SECOND = {
    "runway": 0.05,  # $0.05 per second
    "veo": 0.20,
}

def track_cost(duration: int, provider: str):
    cost = duration * COST_PER_SECOND.get(provider, 0.05)
    log(f"💰 Estimated cost: ${cost:.2f}")
    
    # Save to log file
    with open("logs/costs.txt", "a") as f:
        f.write(f"{datetime.now()},{provider},{duration},{cost}\n")
```

---

## 📊 Usage Examples

### Daily Automation

```bash
# Cron job: Generate daily inspiration video
0 9 * * * source ~/.ai-video-env && python3 ~/ai-video-pipeline/scripts/generate_video.py "Morning inspiration scene"
```

### Social Media Batch

```bash
# Generate 5 videos untuk minggu ini
cat > weekly_prompts.txt << EOF
Monday motivation: Sunrise over mountains
Tuesday tips: Animated data visualization
Wednesday wisdom: Book pages turning
Thursday throwback: Vintage film aesthetic
Friday feels: Celebrating success
EOF

python3 scripts/batch_generate.py weekly_prompts.txt
```

---

## 📚 Referensi

| Resource | Link |
|----------|------|
| Runway ML API | https://docs.runwayml.com/ |
| Google Veo (Vertex AI) | https://cloud.google.com/vertex-ai/generative-ai/docs/video/overview |
| Google Drive API | https://developers.google.com/drive/api/guides/about-sdk |
| OpenClaw Docs | https://docs.openclaw.ai |
| Video Generation Tips | https://help.runwayml.com/hc/en-us/articles/15161264012307-Best-Practices-for-Text-to-Video |

---

## 🎉 Kesimpulan

**Apa yang sudah kita bangun:**

✅ AI video generation pipeline  
✅ Automatic cloud storage upload  
✅ Telegram integration  
✅ Batch processing capability  
✅ Cost tracking & monitoring  

**Ide pengembangan selanjutnya:**
- 🎵 Add background music dari AI
- 📝 Auto-generate prompt dari article/text
- 📅 Scheduled content calendar
- 🔄 Integration dengan video editing APIs
- 📈 Analytics: track which prompts perform best

---

> **Share your creations!**  
> Punya use case menarik atau improvement? Share di komunitas! 🎬

---

**Last Updated:** March 12, 2026  
**Tags:** #ai-video #automation #openclaw #generative-ai #content-creation
