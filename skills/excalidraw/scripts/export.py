#!/usr/bin/env python3
"""
Excalidraw to PNG Export Script
Renders .excalidraw files to clean PNG images
"""

import json
import sys
from PIL import Image, ImageDraw, ImageFont
import math

def draw_rounded_rect(draw, xy, fill, outline, width, radius=10):
    """Draw rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_diamond(draw, x, y, w, h, fill, outline, width):
    """Draw diamond shape"""
    cx, cy = x + w//2, y + h//2
    points = [(cx, y), (x + w, cy), (cx, y + h), (x, cy)]
    draw.polygon(points, fill=fill, outline=outline)

def draw_arrow(draw, x1, y1, x2, y2, fill, width):
    """Draw arrow with arrowhead"""
    draw.line([(x1, y1), (x2, y2)], fill=fill, width=width)
    # Arrowhead
    angle = 0.5
    dx, dy = x2 - x1, y2 - y1
    arrow_len = 15
    line_angle = math.atan2(dy, dx)
    
    ax1 = x2 - arrow_len * math.cos(line_angle - angle)
    ay1 = y2 - arrow_len * math.sin(line_angle - angle)
    ax2 = x2 - arrow_len * math.cos(line_angle + angle)
    ay2 = y2 - arrow_len * math.sin(line_angle + angle)
    
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=fill)

def render_excalidraw(input_file, output_file, width=900, height=600):
    with open(input_file) as f:
        data = json.load(f)
    
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    colors = {
        '#e7f5ff': '#e7f5ff',
        '#ffe3e3': '#ffe3e3',
        '#fff9db': '#fff9db',
        '#d3f9d8': '#d3f9d8',
        '#b2f2bb': '#b2f2bb',
        '#ffffff': '#ffffff',
        '#f8f9fa': '#f8f9fa',
        '#1971c2': '#1971c2',
        '#c92a2a': '#c92a2a',
        '#e67700': '#e67700',
        '#2f9e44': '#2f9e44',
        '#1864ab': '#1864ab',
        '#e8590c': '#e8590c',
        '#1a1a2e': '#1a1a2e',
        '#495057': '#495057',
        '#2b8a3e': '#2b8a3e',
    }
    
    for el in data.get('elements', []):
        el_type = el.get('type')
        
        if el_type == 'rectangle':
            x, y = el.get('x', 0), el.get('y', 0)
            w, h = el.get('width', 0), el.get('height', 0)
            fill = colors.get(el.get('backgroundColor', '#ffffff'), '#ffffff')
            outline = colors.get(el.get('strokeColor', '#000000'), '#000000')
            stroke_width = el.get('strokeWidth', 1)
            draw_rounded_rect(draw, [x, y, x+w, y+h], fill, outline, stroke_width)
            
        elif el_type == 'diamond':
            x, y = el.get('x', 0), el.get('y', 0)
            w, h = el.get('width', 0), el.get('height', 0)
            fill = colors.get(el.get('backgroundColor', '#ffffff'), '#ffffff')
            outline = colors.get(el.get('strokeColor', '#000000'), '#000000')
            stroke_width = el.get('strokeWidth', 1)
            draw_diamond(draw, x, y, w, h, fill, outline, stroke_width)
            
        elif el_type == 'arrow':
            x, y = el.get('x', 0), el.get('y', 0)
            points = el.get('points', [[0,0], [0,0]])
            x2, y2 = x + points[1][0], y + points[1][1]
            fill = colors.get(el.get('strokeColor', '#000000'), '#000000')
            stroke_width = el.get('strokeWidth', 1)
            draw_arrow(draw, x, y, x2, y2, fill, stroke_width)
            
        elif el_type == 'text':
            x, y = el.get('x', 0), el.get('y', 0)
            w, h = el.get('width', 0), el.get('height', 0)
            text = el.get('text', '')
            color = colors.get(el.get('strokeColor', '#000000'), '#000000')
            size = el.get('fontSize', 14)
            
            if size >= 20:
                font = font_large
            elif size >= 15:
                font = font_medium
            else:
                font = font_small
            
            lines = text.split('\n')
            line_height = size + 4
            total_height = len(lines) * line_height
            start_y = y + (h - total_height) // 2
            
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                text_w = bbox[2] - bbox[0]
                text_x = x + (w - text_w) // 2
                text_y = start_y + i * line_height
                draw.text((text_x, text_y), line, fill=color, font=font)
    
    img.save(output_file, 'PNG')
    print(f"✅ Exported: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: export.py <input.excalidraw> [output.png] [width] [height]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.excalidraw', '.png')
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 900
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    
    render_excalidraw(input_file, output_file, width, height)
