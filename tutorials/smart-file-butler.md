# Smart File Butler

Auto-organize your Downloads folder with AI-powered file management.

## Overview

Your Downloads folder is a mess? Files scattered everywhere with cryptic names like `download (17).pdf`?

This automation:
- Monitors your Downloads folder
- Auto-sorts files by type (Documents, Images, Archives, etc.)
- Renames files with descriptive names using AI
- Archives old files to cloud storage
- Cleans up clutter automatically

**Before:** `download (3).pdf`, `IMG_2024...jpg`, `untitled.zip` scattered randomly  
**After:** Organized folders, descriptive names, auto-archived old files

## Architecture

```
[File downloaded]
      ↓
[Detect file type]
      ↓
[AI analyzes content]
  - Document → Extract title/topic
  - Image → Detect content/scene
  - Archive → List contents
      ↓
[Generate descriptive name]
      ↓
[Move to appropriate folder]
  - Documents/Work/2026/
  - Images/Screenshots/
  - Archives/Software/
      ↓
[Old files → Cloud archive]
      ↓
[Notify user of changes]
```

## Prerequisites

- OpenClaw installed
- Python 3.8+
- `inotifywait` (Linux) or `fswatch` (macOS) for file monitoring
- Google Drive API (for archiving)

## Step 1: Create Directory Structure

```bash
# Create organized folders
mkdir -p ~/Downloads/{Documents,Images,Archives,Media,Software,Data,Other}
mkdir -p ~/Downloads/Documents/{Work,Personal,Invoices,Manuals}
mkdir -p ~/Downloads/Images/{Screenshots,Photos,Designs,Memes}
mkdir -p ~/Downloads/Archives/{Extracted,Keep}
mkdir -p ~/Downloads/Media/{Audio,Video}
```

## Step 2: File Analyzer Script

`scripts/file-butler/analyze-file.py`:

```python
#!/usr/bin/env python3
"""
Analyze file content and generate descriptive name
Usage: python3 analyze-file.py <file_path>
"""

import sys
import os
import mimetypes
from pathlib import Path

def get_file_info(file_path):
    """Get basic file information"""
    stat = os.stat(file_path)
    return {
        "name": os.path.basename(file_path),
        "size": stat.st_size,
        "mime": mimetypes.guess_type(file_path)[0] or "application/octet-stream",
        "ext": Path(file_path).suffix.lower()
    }

def analyze_document(file_path):
    """Extract info from PDF/DOCX/TXT"""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.pdf':
        return analyze_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return analyze_docx(file_path)
    elif ext == '.txt':
        return analyze_txt(file_path)
    else:
        return {"type": "document", "description": "Unknown document"}

def analyze_pdf(file_path):
    """Extract PDF metadata and first page text"""
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            meta = reader.metadata
            
            # Get first page text (limited)
            text = ""
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text()[:500]
            
            return {
                "type": "pdf",
                "title": meta.get('/Title', ''),
                "author": meta.get('/Author', ''),
                "pages": len(reader.pages),
                "preview": text,
                "description": f"PDF: {meta.get('/Title', 'Untitled')} ({len(reader.pages)} pages)"
            }
    except:
        return {"type": "pdf", "description": "PDF document"}

def analyze_image(file_path):
    """Analyze image content using AI vision"""
    # Use AI to describe image
    prompt = "Describe this image in 5-7 words for a filename"
    
    # Implementation depends on your AI setup
    description = call_vision_model(file_path, prompt)
    
    return {
        "type": "image",
        "description": description,
        "dimensions": get_image_dimensions(file_path)
    }

def analyze_archive(file_path):
    """List contents of ZIP/tar files"""
    import zipfile
    import tarfile
    
    ext = Path(file_path).suffix.lower()
    
    try:
        if ext == '.zip':
            with zipfile.ZipFile(file_path, 'r') as zf:
                files = zf.namelist()[:10]  # First 10 files
                return {
                    "type": "zip",
                    "contents": files,
                    "file_count": len(zf.namelist()),
                    "description": f"ZIP archive with {len(zf.namelist())} files"
                }
        elif ext in ['.tar', '.gz', '.bz2']:
            with tarfile.open(file_path, 'r') as tf:
                files = tf.getnames()[:10]
                return {
                    "type": "archive",
                    "contents": files,
                    "description": f"Archive: {', '.join(files[:3])}..."
                }
    except:
        return {"type": "archive", "description": "Compressed archive"}

def generate_filename(file_path, analysis):
    """Generate descriptive filename using AI"""
    
    info = get_file_info(file_path)
    
    prompt = f"""Generate a concise, descriptive filename (2-4 words) for this file:

Original: {info['name']}
Type: {analysis.get('type', 'file')}
Description: {analysis.get('description', 'Unknown')}

Rules:
- Use snake_case (lowercase, underscores)
- Include date if relevant: YYYY-MM-DD
- Be specific but concise
- Max 50 characters

Output only the filename without extension."""

    # Call AI model
    new_name = call_ai_model(prompt)
    
    # Clean up
    new_name = new_name.strip().replace(' ', '_').lower()
    new_name = ''.join(c for c in new_name if c.isalnum() or c in '_-')
    
    # Add date prefix if not present
    if not new_name.startswith('20'):  # No year prefix
        from datetime import datetime
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        new_name = f"{date_prefix}_{new_name}"
    
    return new_name + info['ext']

def determine_folder(file_path, analysis):
    """Determine destination folder based on file type and content"""
    
    info = get_file_info(file_path)
    mime = info['mime']
    
    # By MIME type
    if mime.startswith('image/'):
        if 'screenshot' in analysis.get('description', '').lower():
            return 'Images/Screenshots'
        elif 'design' in analysis.get('description', '').lower():
            return 'Images/Designs'
        return 'Images/Photos'
    
    elif mime.startswith('application/pdf'):
        desc = analysis.get('description', '').lower()
        if any(word in desc for word in ['invoice', 'bill', 'receipt', 'payment']):
            return 'Documents/Invoices'
        elif any(word in desc for word in ['manual', 'guide', 'documentation']):
            return 'Documents/Manuals'
        elif any(word in desc for word in ['report', 'analysis', 'data']):
            return 'Documents/Work'
        return 'Documents'
    
    elif mime.startswith('application/zip') or mime.startswith('application/x-'):
        return 'Archives'
    
    elif mime.startswith('video/'):
        return 'Media/Video'
    
    elif mime.startswith('audio/'):
        return 'Media/Audio'
    
    # By extension
    ext = info['ext']
    if ext in ['.exe', '.dmg', '.pkg', '.deb', '.rpm']:
        return 'Software'
    elif ext in ['.csv', '.json', '.xml', '.sql']:
        return 'Data'
    
    return 'Other'

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze-file.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"🔍 Analyzing: {os.path.basename(file_path)}")
    
    # Analyze based on type
    info = get_file_info(file_path)
    
    if info['mime'].startswith('image/'):
        analysis = analyze_image(file_path)
    elif info['mime'].startswith('application/pdf'):
        analysis = analyze_document(file_path)
    elif info['ext'] in ['.zip', '.tar', '.gz']:
        analysis = analyze_archive(file_path)
    else:
        analysis = {"type": "file", "description": f"{info['ext']} file"}
    
    # Generate new name
    new_filename = generate_filename(file_path, analysis)
    folder = determine_folder(file_path, analysis)
    
    print(f"📁 Destination: {folder}/")
    print(f"📝 New name: {new_filename}")
    
    # Output for script processing
    result = {
        "original": info['name'],
        "new_name": new_filename,
        "folder": folder,
        "analysis": analysis
    }
    
    import json
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

## Step 3: File Organizer Script

`scripts/file-butler/organize.sh`:

```bash
#!/bin/bash
# Smart File Butler - Organize Downloads folder

DOWNLOADS_DIR="$HOME/Downloads"
LOG_FILE="$DOWNLOADS_DIR/.file-butler.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

organize_file() {
    local file_path="$1"
    local filename=$(basename "$file_path")
    
    log "Processing: $filename"
    
    # Skip system files
    if [[ "$filename" == .* ]] || [[ "$filename" == *.tmp ]] || [[ "$filename" == *.crdownload ]]; then
        log "Skipping system file: $filename"
        return
    fi
    
    # Analyze file
    local analysis=$(python3 "$HOME/scripts/file-butler/analyze-file.py" "$file_path")
    local new_name=$(echo "$analysis" | python3 -c "import sys,json; print(json.load(sys.stdin)['new_name'])")
    local folder=$(echo "$analysis" | python3 -c "import sys,json; print(json.load(sys.stdin)['folder'])")
    
    # Create destination path
    local dest_dir="$DOWNLOADS_DIR/$folder"
    mkdir -p "$dest_dir"
    
    # Handle duplicates
    local dest_path="$dest_dir/$new_name"
    local counter=1
    while [ -f "$dest_path" ]; do
        local base="${new_name%.*}"
        local ext="${new_name##*.}"
        dest_path="$dest_dir/${base}_$counter.$ext"
        ((counter++))
    done
    
    # Move file
    mv "$file_path" "$dest_path"
    log "✅ Moved to: $folder/$(basename "$dest_path")"
    
    # Send notification
    notify-user "$filename" "$(basename "$dest_path")" "$folder"
}

notify-user() {
    local original="$1"
    local new_name="$2"
    local folder="$3"
    
    # Telegram notification (optional)
    # curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
    #     -d "chat_id=$CHAT_ID" \
    #     -d "text=📁 File organized:%0A$original → $folder/$new_name"
    
    # Desktop notification
    if command -v notify-send &> /dev/null; then
        notify-send "File Butler" "Organized: $original → $folder/"
    fi
}

# Process single file or watch directory
if [ "$1" == "--watch" ]; then
    log "👀 Watching $DOWNLOADS_DIR for new files..."
    
    # Using inotifywait (Linux)
    inotifywait -m -e create -e moved_to --format '%w%f' "$DOWNLOADS_DIR" | while read file_path; do
        # Wait for file to finish writing
        sleep 2
        if [ -f "$file_path" ]; then
            organize_file "$file_path"
        fi
    done
else
    # Process existing files
    log "🧹 Organizing existing files..."
    
    find "$DOWNLOADS_DIR" -maxdepth 1 -type f | while read file_path; do
        organize_file "$file_path"
    done
    
    log "✅ Organization complete!"
fi
```

Make executable:
```bash
chmod +x scripts/file-butler/organize.sh
```

## Step 4: Auto-Archive Old Files

`scripts/file-butler/archive-old.py`:

```python
#!/usr/bin/env python3
"""
Archive files older than 30 days to Google Drive
Usage: python3 archive-old.py
"""

import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
ARCHIVE_AGE_DAYS = 30
DRIVE_FOLDER_ID = "your-google-drive-folder-id"

def get_file_age(file_path):
    """Get file age in days"""
    stat = os.stat(file_path)
    mtime = datetime.fromtimestamp(stat.st_mtime)
    return (datetime.now() - mtime).days

def upload_to_drive(file_path, folder_id):
    """Upload file to Google Drive using gog CLI"""
    try:
        result = subprocess.run(
            ["gog", "drive", "upload", file_path, "--parent", folder_id],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def archive_file(file_path):
    """Archive single file"""
    rel_path = os.path.relpath(file_path, DOWNLOADS_DIR)
    print(f"📦 Archiving: {rel_path}")
    
    if upload_to_drive(file_path, DRIVE_FOLDER_ID):
        os.remove(file_path)
        print(f"✅ Archived and removed: {rel_path}")
        return True
    else:
        print(f"❌ Failed to archive: {rel_path}")
        return False

def main():
    print("🔍 Scanning for old files...")
    
    archived = 0
    failed = 0
    
    for root, dirs, files in os.walk(DOWNLOADS_DIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip system files
            if file.startswith('.') or file.endswith('.tmp'):
                continue
            
            age = get_file_age(file_path)
            if age > ARCHIVE_AGE_DAYS:
                if archive_file(file_path):
                    archived += 1
                else:
                    failed += 1
    
    print(f"\n📊 Summary: {archived} archived, {failed} failed")
    print(f"💾 Space saved: ~{archived * 5}MB (estimated)")

if __name__ == "__main__":
    main()
```

## Step 5: Systemd Service (Auto-start)

Create `~/.config/systemd/user/file-butler.service`:

```ini
[Unit]
Description=Smart File Butler - Auto-organize Downloads
After=graphical-session.target

[Service]
Type=simple
ExecStart=%h/scripts/file-butler/organize.sh --watch
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

Enable and start:
```bash
systemctl --user daemon-reload
systemctl --user enable file-butler.service
systemctl --user start file-butler.service

# Check status
systemctl --user status file-butler.service
```

## Step 6: Cron Jobs

```bash
# Add to crontab
# Organize existing files daily at 2 AM
0 2 * * * /home/user/scripts/file-butler/organize.sh >> /home/user/.file-butler.log 2>&1

# Archive old files weekly on Sundays
0 3 * * 0 /usr/bin/python3 /home/user/scripts/file-butler/archive-old.py >> /home/user/.file-butler.log 2>&1
```

## Example Output

**Before organization:**
```
Downloads/
├── download (17).pdf
├── IMG_20240308_143022.jpg
├── screenshot_2024-03-08.png
├── presentation_final_v2.pdf
├── software-2.3.1-linux.deb
├── data_export_2024.csv
└── archive.zip
```

**After organization:**
```
Downloads/
├── Documents/
│   ├── Invoices/
│   │   └── 2024-03-08_monthly_invoice_acme.pdf
│   └── Work/
│       └── 2024-03-08_q1_sales_presentation.pdf
├── Images/
│   ├── Screenshots/
│   │   └── 2024-03-08_dashboard_error.png
│   └── Photos/
│       └── 2024-03-08_office_meeting.jpg
├── Software/
│   └── 2024-03-08_developer_tool_linux.deb
├── Data/
│   └── 2024-03-08_customer_export.csv
├── Archives/
│   └── 2024-03-08_project_files.zip
└── .file-butler.log
```

## Advanced Features

### Duplicate Detection

```python
def find_duplicates(directory):
    """Find duplicate files by hash"""
    import hashlib
    
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            
            if file_hash in hashes:
                print(f"Duplicate found: {file_path}")
                # Handle duplicate (delete, move, etc.)
            else:
                hashes[file_hash] = file_path
```

### Content-based Search

```python
def search_by_content(query, directory):
    """Search files by AI-analyzed content"""
    # Build index of file descriptions
    # Search using embeddings or keywords
    pass
```

## Conclusion

You now have an intelligent file management system that:
- ✅ Auto-organizes downloads by type and content
- ✅ Generates descriptive filenames with AI
- ✅ Archives old files to cloud storage
- ✅ Runs continuously in background

**Next Steps:**
- Add file content indexing for search
- Integrate with more cloud providers
- Build web dashboard for file management

---

*Tutorial created for OpenClaw Sumopod*
