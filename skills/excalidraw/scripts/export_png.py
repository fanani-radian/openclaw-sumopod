#!/usr/bin/env python3
"""
Export Excalidraw to PNG using Pillow
Simple renderer for clean diagrams
"""

import json
from PIL import Image, ImageDraw, ImageFont
import sys

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
    angle = 0.5  # radians
    import math
    dx, dy = x2 - x1, y2 - y1
    arrow_len = 15
    line_angle = math.atan2(dy, dx)
    
    ax1 = x2 - arrow_len * math.cos(line_angle - angle)
    ay1 = y2 - arrow_len * math.sin(line_angle - angle)
    ax2 = x2 - arrow_len * math.cos(line_angle + angle)
    ay2 = y2 - arrow_len * math.sin(line_angle + angle)
    
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=fill)

def render_excalidraw(input_file, output_file):
    # Load data
    with open(input_file) as f:
        data = json.load(f)
    
    # Create image
    img = Image.new('RGB', (900, 600), '#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Try to load font
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Color mapping
    colors = {
        '#e7f5ff': '#e7f5ff',  # Light blue
        '#ffe3e3': '#ffe3e3',  # Light red
        '#fff9db': '#fff9db',  # Light yellow
        '#d3f9d8': '#d3f9d8',  # Light green
        '#b2f2bb': '#b2f2bb',  # Green
        '#ffffff': '#ffffff',  # White
        '#f8f9fa': '#f8f9fa',  # Light gray
        '#1971c2': '#1971c2',  # Blue
        '#c92a2a': '#c92a2a',  # Red
        '#e67700': '#e67700',  # Orange
        '#2f9e44': '#2f9e44',  # Green
        '#1864ab': '#1864ab',  # Dark blue
        '#e8590c': '#e8590c',  # Orange
        '#1a1a2e': '#1a1a2e',  # Dark
        '#495057': '#495057',  # Gray
        '#ffffff': '#ffffff',  # White
    }
    
    # Draw elements
    for el in data.get('elements', []):
        el_type = el.get('type')
        
        if el_type == 'rectangle':
            x, y = el.get('x', 0), el.get('y', 0)
            w, h = el.get('width', 0), el.get('height', 0)
            fill = colors.get(el.get('backgroundColor', '#ffffff'), '#ffffff')
            outline = colors.get(el.get('strokeColor', '#000000'), '#000000')
            width = el.get('strokeWidth', 1)
            draw_rounded_rect(draw, [x, y, x+w, y+h], fill, outline, width)
            
        elif el_type == 'diamond':
            x, y = el.get('x', 0), el.get('y', 0)
            w, h = el.get('width', 0), el.get('height', 0)
            fill = colors.get(el.get('backgroundColor', '#ffffff'), '#ffffff')
            outline = colors.get(el.get('strokeColor', '#000000'), '#000000')
            width = el.get('strokeWidth', 1)
            draw_diamond(draw, x, y, w, h, fill, outline, width)
            
        elif el_type == 'arrow':
            x, y = el.get('x', 0), el.get('y', 0)
            points = el.get('points', [[0,0], [0,0]])
            x2, y2 = x + points[1][0], y + points[1][1]
            fill = colors.get(el.get('strokeColor', '#000000'), '#000000')
            width = el.get('strokeWidth', 1)
            draw_arrow(draw, x, y, x2, y2, fill, width)
            
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
            
            # Center text
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
    print(f"Saved: {output_file}")

if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'memory-sync-flow-v2.excalidraw'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'memory-sync-flow.png'
    render_excalidraw(input_file, output_file)
