# Examples

This folder contains example diagrams generated with the Excalidraw skill.

## Files

| File | Description |
|------|-------------|
| `memory-sync-flow.excalidraw` | Editable source file |
| `memory-sync-flow.png` | PNG export for GitHub/docs |

## Viewing

### Open in Excalidraw (Editable)
1. Go to https://excalidraw.com
2. File → Open → Select `.excalidraw` file
3. Edit as needed

### View PNG (Static)
Open `memory-sync-flow.png` directly in any image viewer.

## Preview

![Memory Sync Flow](memory-sync-flow.png)

## Creating Your Own

```bash
# From workspace root
cd skills/excalidraw

# Generate from template
python3 scripts/generate.py --template memory-sync --output my-diagram

# Export to PNG
python3 scripts/export.py my-diagram.excalidraw my-diagram.png
```
