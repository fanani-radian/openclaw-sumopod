# 🎬 AI Video Generation & Editing dengan OpenClaw

Tutorial lengkap generate dan edit video menggunakan AI dengan OpenClaw — low cost, optimized, dan practical!

---

## 🎯 Overview

OpenClaw bisa orkestrasi AI video generation dari berbagai provider. Ada 2 workflow utama:

| Workflow | Use Case | Cost |
|----------|----------|------|
| **Text-to-Video** | Generate video dari prompt/description | $0.01-0.10/5s |
| **Image-to-Video** | Animate foto/gambar jadi video | $0.005-0.05/5s |
| **Video Editing** | Edit existing video (crop, merge, fx) | FREE (local) |

---

## 🏆 Best APIs (Low Cost + Great Results)

### Tier 1: FREE / Ultra Low Cost

| API | Type | Cost | Pros | Cons |
|-----|------|------|------|------|
| **Hedra** | Image-to-Video | FREE | Unlimited free tier | 5s max, watermark |
| **Viggle** | Character Animation | FREE | Great for memes | Limited styles |
| **Stable Video Diffusion** | Image-to-Video | FREE (self-host) | Open source | Requires GPU |
| **Haiper** | Text/Image-to-Video | FREE tier | 10 videos/day free | Lower quality |

### Tier 2: Affordable (Best Value)

| API | Type | Cost | Best For |
|-----|------|------|----------|
| **Kling AI** | Text/Image-to-Video | ~$0.02/5s | Realistic motion |
| **Luma Dream Machine** | Text-to-Video | ~$0.05/5s | Fast, good quality |
| **Runway Gen-2** | Text/Image-to-Video | $0.05-0.10/5s | Professional quality |
| **Pika Labs** | Image-to-Video | $0.03/3s | Artistic styles |

### Tier 3: Video Editing (FREE)

| Tool | Cost | Function |
|------|------|----------|
| **FFmpeg** | FREE | Convert, crop, merge, compress |
| **MoviePy** | FREE | Python video editing |
| **Whisper** | FREE | Auto subtitle generation |

---

## 🛠️ Setup Requirements

### 1. API Keys (Get these)

```bash
# Create .env file
cat > ~/.openclaw/workspace/.env << 'EOF'
# Video Generation APIs
KLING_API_KEY=your_kling_key
LUMA_API_KEY=your_luma_key
RUNWAY_API_KEY=your_runway_key
HEDRA_API_KEY=your_hedra_key  # optional, often free

# For editing (local, no API key needed)
# FFmpeg - install via package manager
EOF
```

### 2. Install FFmpeg (CRITICAL for editing)

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# Mac
brew install ffmpeg

# Windows (via chocolatey)
choco install ffmpeg

# Verify
ffmpeg -version
```

### 3. Install Python deps

```bash
pip install moviepy opencv-python-headless requests
```

---

## 🎬 Workflow 1: Text-to-Video

Generate video dari deskripsi teks.

### Skill: `video-generate`

```bash
# Folder structure
skills/video-generate/
├── SKILL.md
└── scripts/
    ├── generate.sh      # Main generator
    ├── kling-generate.py
    ├── luma-generate.py
    └── runway-generate.py
```

### Script: `generate.sh`

```bash
#!/bin/bash
# AI Video Generator - Low Cost Optimized
# Usage: video-generate "prompt" [--duration 5] [--provider kling|luma|hedra]

PROMPT="$1"
DURATION="${3:-5}"
PROVIDER="${5:-kling}"  # Default: cheapest good option
OUTPUT_DIR="${HOME}/.openclaw/videos"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%s)
OUTPUT_FILE="$OUTPUT_DIR/video_${PROVIDER}_${TIMESTAMP}.mp4"

echo "🎬 Generating video..."
echo "Prompt: $PROMPT"
echo "Provider: $PROVIDER"
echo "Duration: ${DURATION}s"

case $PROVIDER in
    kling)
        python3 skills/video-generate/scripts/kling-generate.py "$PROMPT" "$DURATION" "$OUTPUT_FILE"
        ;;
    luma)
        python3 skills/video-generate/scripts/luma-generate.py "$PROMPT" "$DURATION" "$OUTPUT_FILE"
        ;;
    hedra)
        # FREE option - but need image first
        echo "⚠️ Hedra requires image input. Use image-to-video workflow."
        exit 1
        ;;
    *)
        echo "Unknown provider: $PROVIDER"
        exit 1
        ;;
esac

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ Video saved: $OUTPUT_FILE"
    echo "💰 Estimated cost: \$$(echo "scale=3; $DURATION * 0.004" | bc)"
else
    echo "❌ Generation failed"
    exit 1
fi
```

### Script: `kling-generate.py` (CHEAPEST)

```python
#!/usr/bin/env python3
"""
Kling AI Video Generator
Cost: ~$0.02/5s (cheapest good quality)
"""
import requests
import json
import time
import sys

API_KEY = "your_kling_api_key"
API_URL = "https://api.klingai.com/v1/videos/text2video"

def generate_video(prompt, duration, output_path):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "duration": int(duration),  # 5 or 10 seconds
        "aspect_ratio": "16:9",
        "negative_prompt": "blur, low quality, distorted"
    }
    
    # Submit job
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()
    
    if "job_id" not in data:
        print(f"Error: {data}", file=sys.stderr)
        return False
    
    job_id = data["job_id"]
    print(f"Job submitted: {job_id}")
    
    # Poll for completion
    for i in range(60):  # Max 5 minutes
        time.sleep(5)
        status_resp = requests.get(
            f"{API_URL}/status/{job_id}",
            headers=headers
        )
        status = status_resp.json()
        
        if status.get("status") == "completed":
            video_url = status["video_url"]
            # Download video
            video_data = requests.get(video_url).content
            with open(output_path, 'wb') as f:
                f.write(video_data)
            return True
        elif status.get("status") == "failed":
            print(f"Generation failed: {status}", file=sys.stderr)
            return False
        else:
            print(f"Progress: {status.get('progress', 'unknown')}%")
    
    return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: kling-generate.py 'prompt' duration output.mp4")
        sys.exit(1)
    
    success = generate_video(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0 if success else 1)
```

### Usage dari OpenClaw

```bash
# Generate video via OpenClaw
sessions_spawn runtime="subagent" task="Generate 5-second video of 'sunset over Bali beach with gentle waves'"

# Atau via command
echo "Generate video: golden retriever playing in autumn leaves, 5 seconds"
```

---

## 🖼️ Workflow 2: Image-to-Video (Animate Foto)

Bikin foto jadi video animasi. **LOWEST COST!**

### Option A: Hedra (FREE!)

```bash
#!/bin/bash
# Hedra Image-to-Video (FREE TIER)
# Usage: animate-image image.jpg "description of motion"

IMAGE="$1"
PROMPT="$2"
OUTPUT="${3:-output.mp4}"

curl -X POST "https://api.hedra.com/v1/animate" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@$IMAGE" \
  -F "prompt=$PROMPT" \
  -F "duration=5" \
  --output "$OUTPUT"

echo "✅ Animated video: $OUTPUT"
echo "💰 Cost: FREE"
```

### Option B: Kling Image-to-Video (Better Quality)

```python
#!/usr/bin/env python3
"""
Kling Image-to-Video
Cost: ~$0.015/5s
"""
import requests
import base64

API_KEY = "your_kling_api_key"

def image_to_video(image_path, prompt, output_path):
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "image": f"data:image/jpeg;base64,{image_base64}",
        "prompt": prompt,
        "duration": 5
    }
    
    response = requests.post(
        "https://api.klingai.com/v1/videos/image2video",
        headers=headers,
        json=payload
    )
    
    # Handle response and download...
    # (similar to text2video)
```

---

## ✂️ Workflow 3: Video Editing (FREE!)

Edit video menggunakan FFmpeg - **GRATIS** dan **LOCAL**!

### Skill: `video-edit`

```bash
# skills/video-edit/scripts/edit.sh
#!/bin/bash
# Video Editor using FFmpeg (FREE)
# Usage: video-edit input.mp4 [options]

INPUT="$1"
ACTION="$2"
OUTPUT="${3:-output.mp4}"

case $ACTION in
    compress)
        # Compress for sharing (reduce file size 70%)
        ffmpeg -i "$INPUT" -vcodec h264 -acodec mp2 -crf 28 "$OUTPUT"
        echo "✅ Compressed: $OUTPUT"
        ;;
    
    trim)
        # Trim video (start at 5s, duration 10s)
        START="${4:-0}"
        DURATION="${5:-10}"
        ffmpeg -i "$INPUT" -ss "$START" -t "$DURATION" -c copy "$OUTPUT"
        echo "✅ Trimmed: $OUTPUT"
        ;;
    
    merge)
        # Merge multiple videos
        LIST_FILE="$4"  # File containing list of videos
        ffmpeg -f concat -safe 0 -i "$LIST_FILE" -c copy "$OUTPUT"
        echo "✅ Merged: $OUTPUT"
        ;;
    
    add-subtitle)
        # Add subtitles from SRT file
        SRT="$4"
        ffmpeg -i "$INPUT" -vf "subtitles=$SRT" "$OUTPUT"
        echo "✅ Added subtitles: $OUTPUT"
        ;;
    
    extract-audio)
        # Extract audio from video
        ffmpeg -i "$INPUT" -vn -acodec copy "${OUTPUT}.mp3"
        echo "✅ Audio extracted: ${OUTPUT}.mp3"
        ;;
    
    gif)
        # Convert to GIF (for sharing)
        ffmpeg -i "$INPUT" -vf "fps=10,scale=480:-1:flags=lanczos" "$OUTPUT"
        echo "✅ GIF created: $OUTPUT"
        ;;
    
    *)
        echo "Usage: video-edit input.mp4 [compress|trim|merge|add-subtitle|extract-audio|gif] output"
        exit 1
        ;;
esac
```

### Auto-Generate Subtitles (Whisper - FREE)

```bash
#!/bin/bash
# Auto-generate subtitles dari video (FREE)
# Requires: pip install openai-whisper

VIDEO="$1"

# Extract audio
ffmpeg -i "$VIDEO" -vn -acodec pcm_s16le -ar 16000 -ac 1 "temp.wav"

# Transcribe with Whisper
whisper "temp.wav" --model tiny --language Indonesian --output_format srt

# Cleanup
rm temp.wav

echo "✅ Subtitle generated: temp.srt"
```

---

## 💰 Cost Optimization Strategy

### Best Value Workflow

```
1. Generate Image (FLUX/SDXL)     → $0.001
2. Animate Image (Kling I2V)      → $0.015  
3. Edit/Add Subtitles (FFmpeg)    → FREE
4. Compress (FFmpeg)              → FREE
─────────────────────────────────────────
Total: ~$0.016 for 5s video
```

### vs Direct Text-to-Video

```
Text-to-Video (Runway)            → $0.10
─────────────────────────────────────────
Cost savings: 84%! 🎉
```

---

## 🚀 Practical Use Cases

### Use Case 1: Social Media Content

```bash
# Generate Instagram Reel content
# 1. Generate image
# 2. Animate to 5s video
# 3. Add trending audio
# 4. Compress for upload

video-generate "sunset over Bali temple, cinematic" --provider kling
video-edit output.mp4 compress final.mp4
```

### Use Case 2: Product Showcase

```bash
# Animate product photo
animate-image product.jpg "product rotating 360 degrees, studio lighting"
```

### Use Case 3: Meme Video

```bash
# Use Viggle (FREE) for meme characters
# Upload character image + motion video
viggle-animate character.jpg dance.mp4 output.mp4
```

### Use Case 4: Auto-Subtitle for Podcast

```bash
# Extract audio, transcribe, add subtitles
video-edit podcast.mp4 extract-audio audio.wav
whisper audio.wav --model base --output_format srt
video-edit podcast.mp4 add-subtitle podcast.srt final.mp4
```

---

## 📋 OpenClaw Integration

### Add to HEARTBEAT.md

```markdown
## Video Tasks

- Monitor video generation jobs
- Compress generated videos after 24h
- Cleanup temp files weekly
```

### Create Video Skill

```bash
# Create skill folder
mkdir -p ~/.openclaw/workspace/skills/video-ai
mkdir -p ~/.openclaw/workspace/skills/video-edit

# Copy scripts
cp video-generate.sh ~/.openclaw/workspace/skills/video-ai/scripts/
cp video-edit.sh ~/.openclaw/workspace/skills/video-edit/scripts/

# Create SKILL.md
cat > ~/.openclaw/workspace/skills/video-ai/SKILL.md << 'EOF'
# Video AI Generation

Generate videos using AI APIs.

## APIs Required
- Kling AI (recommended, cheapest)
- or Luma Dream Machine
- or Runway (premium)

## Usage
```bash
video-generate "prompt" --duration 5 --provider kling
```
EOF
```

---

## 🔗 API Signup Links

| API | Link | Free Tier |
|-----|------|-----------|
| Kling AI | https://klingai.com | 50 credits |
| Luma | https://lumalabs.ai/dream-machine | 30 generations |
| Hedra | https://www.hedra.com | Unlimited (watermarked) |
| Haiper | https://haiper.ai | 10 videos/day |
| Runway | https://runwayml.com | 125 credits |

---

## 🎯 Quick Start Checklist

- [ ] Install FFmpeg: `apt install ffmpeg`
- [ ] Get Kling API key (cheapest)
- [ ] Test video generation
- [ ] Setup video output folder
- [ ] Create Telegram/Discord bot for notifications
- [ ] Schedule batch generation via cron

---

## 💡 Pro Tips

1. **Start with Image-to-Video** — 3x cheaper than text-to-video
2. **Use Hedra for testing** — FREE unlimited (with watermark)
3. **Batch processing** — Generate multiple videos in parallel
4. **FFmpeg for everything** — Never pay for simple edits
5. **Compress before sharing** — Reduce file size 70%+ with FFmpeg

---

*Tutorial by: Sumopod Community*
