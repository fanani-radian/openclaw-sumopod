# Excalidraw Integration Skill

Generate beautiful hand-drawn style diagrams programmatically for documentation, reports, and presentations.

## Overview

This skill enables Radit to create Excalidraw-compatible diagrams that can be:
- Exported as PNG/SVG for GitHub, docs, slides
- Opened in excalidraw.com for manual editing
- Embedded in reports and presentations

## Quick Start

```bash
# Generate a simple diagram
python3 skills/excalidraw/scripts/generate.py --template system-architecture --output my-diagram

# Export to PNG for GitHub
python3 skills/excalidraw/scripts/export.py my-diagram.excalidraw my-diagram.png

# Open in browser for editing
python3 skills/excalidraw/scripts/open.py my-diagram.excalidraw
```

## Available Templates

| Template | Description | Use Case |
|----------|-------------|----------|
| `system-architecture` | Server/VPS architecture | Infrastructure docs |
| `memory-sync` | Git sync workflow | Documentation |
| `data-flow` | ETL/data pipeline | Technical specs |
| `decision-tree` | Yes/No decision flow | Process docs |
| `timeline` | Project timeline | Reports |
| `swot` | SWOT analysis | Business docs |
| `mindmap` | Mind mapping | Brainstorming |

## Use Cases

### 1. Technical Documentation (GitHub)
Generate architecture diagrams for README files:
```bash
python3 skills/excalidraw/scripts/generate.py \
  --template system-architecture \
  --vars '{"app_name": "Radit", "services": ["n8n", "Redis", "PostgreSQL"]}' \
  --output radit-arch
```

### 2. Google Docs/Slides Integration
Export as PNG → Insert into Google Docs:
```bash
# Generate and auto-upload to Google Drive
python3 skills/excalidraw/scripts/generate-and-upload.py \
  --template data-flow \
  --output q1-report-diagram \
  --drive-folder "Reports/Q1 2026"
```

### 3. Project Reports
Create visual project timelines:
```bash
python3 skills/excalidraw/scripts/generate.py \
  --template timeline \
  --vars '{"project": "IKN Dashboard", "start": "Jan 2026", "end": "Jun 2026"}' \
  --output ikn-timeline
```

### 4. Business Analysis
SWOT analysis for Radian Group:
```bash
python3 skills/excalidraw/scripts/generate.py \
  --template swot \
  --vars '{"company": "RFM", "strengths": ["Local expertise", "10+ years"]}' \
  --output rfm-swot
```

### 5. Presentation Slides
Export multiple diagrams for slide deck:
```bash
# Generate all slides
for template in system-architecture data-flow timeline; do
  python3 skills/excalidraw/scripts/export.py \
    examples/${template}.excalidraw \
    slides/${template}.png
done
```

### 6. API Documentation
Visualize API flow:
```bash
python3 skills/excalidraw/scripts/generate.py \
  --template api-flow \
  --vars '{"endpoints": ["GET /users", "POST /auth"]}' \
  --output api-diagram
```

### 7. Process Documentation
Decision trees for workflows:
```bash
python3 skills/excalidraw/scripts/generate.py \
  --template decision-tree \
  --vars '{"question": "Deploy to production?", "yes": "Run tests", "no": "Fix bugs"}' \
  --output deploy-process
```

## File Structure

```
skills/excalidraw/
├── SKILL.md              # This file
├── scripts/
│   ├── generate.py       # Main generator
│   ├── export.py         # Export to PNG/SVG
│   ├── open.py           # Open in browser
│   └── upload-drive.py   # Upload to Google Drive
├── templates/
│   ├── system-architecture.json
│   ├── memory-sync.json
│   ├── data-flow.json
│   ├── decision-tree.json
│   ├── timeline.json
│   ├── swot.json
│   └── mindmap.json
└── examples/
    ├── memory-sync-flow.excalidraw
    └── memory-sync-flow.png
```

## Integration with Other Tools

### GitHub
```markdown
![System Architecture](diagrams/architecture.png)
*[Edit in Excalidraw](https://excalidraw.com/#url=https://raw.githubusercontent.com/...)*
```

### Google Docs
1. Generate PNG: `python3 scripts/export.py diagram.excalidraw diagram.png`
2. Upload to Drive automatically or drag-drop to Docs
3. PNG resolution: 900x600 (perfect for docs)

### Notion
1. Export as PNG
2. Upload directly to Notion page
3. Or use Notion API: `scripts/upload-notion.py`

### Slack
```bash
# Generate and post to Slack
python3 skills/excalidraw/scripts/generate.py --template quick-note --output note
python3 skills/excalidraw/scripts/slack-post.py note.png "#general"
```

## API Usage

```python
from skills.excalidraw import Diagram

# Create diagram
diag = Diagram(width=1200, height=800)
diag.add_rectangle(x=100, y=100, width=200, height=100, 
                   fill="#e7f5ff", label="Server")
diag.add_arrow(from=(300, 150), to=(500, 150))
diag.add_rectangle(x=500, y=100, width=200, height=100,
                   fill="#d3f9d8", label="Database")

# Save
diag.save("my-diagram.excalidraw")
diag.export_png("my-diagram.png")
```

## Best Practices

1. **Always save .excalidraw source** — PNG is display-only
2. **Use descriptive filenames** — `radit-arch-v2.excalidraw`
3. **Version control** — Commit both .excalidraw and .png
4. **Consistent colors** — Follow template color schemes
5. **Export resolution** — 900x600 for docs, 1920x1080 for slides

## Color Palette

| Purpose | Color | Hex |
|---------|-------|-----|
| Primary box | Blue | `#e7f5ff` |
| Success/OK | Green | `#d3f9d8` |
| Warning | Yellow | `#fff9db` |
| Error/Alert | Red | `#ffe3e3` |
| Neutral | Gray | `#f8f9fa` |
| Dark text | Dark | `#1a1a2e` |
| Accent | Orange | `#e8590c` |

## Troubleshooting

**Text not rendering?**
- Install fonts: `apt-get install fonts-dejavu`
- Or use export script which bundles fonts

**Colors look different?**
- Use hex codes from palette above
- GitHub displays sRGB, Excalidraw uses same

**PNG blurry?**
- Increase export resolution: `--width 1920 --height 1080`

## Dependencies

```bash
pip install Pillow  # For PNG export
pip install requests  # For API uploads
```

## Changelog

- **2026-03-08** - Initial skill creation with 7 templates
- **2026-03-08** - Added PNG export script
- **2026-03-08** - GitHub integration examples

## References

- [Excalidraw](https://excalidraw.com) - Online editor
- [Excalidraw Libraries](https://libraries.excalidraw.com) - Community shapes
- [Rough.js](https://roughjs.com) - Hand-drawn graphics engine
