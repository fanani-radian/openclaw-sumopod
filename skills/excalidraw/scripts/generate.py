#!/usr/bin/env python3
"""
Generate Excalidraw diagrams from templates
"""

import json
import sys
import argparse

TEMPLATES = {
    'system-architecture': {
        'width': 900,
        'height': 600,
        'elements': [
            # Main container
            {'type': 'rectangle', 'x': 80, 'y': 80, 'width': 240, 'height': 360,
             'strokeColor': '#1971c2', 'backgroundColor': '#e7f5ff', 'strokeWidth': 2},
            {'type': 'text', 'x': 140, 'y': 95, 'width': 120, 'height': 40,
             'text': '🖥️ VPS Server', 'fontSize': 20, 'strokeColor': '#1971c2'},
            # Services
            {'type': 'rectangle', 'x': 100, 'y': 150, 'width': 200, 'height': 50,
             'strokeColor': '#2f9e44', 'backgroundColor': '#d3f9d8', 'strokeWidth': 2},
            {'type': 'text', 'x': 130, 'y': 165, 'width': 140, 'height': 25,
             'text': '⚡ OpenClaw', 'fontSize': 16, 'strokeColor': '#2f9e44'},
            {'type': 'rectangle', 'x': 100, 'y': 220, 'width': 200, 'height': 50,
             'strokeColor': '#e67700', 'backgroundColor': '#fff9db', 'strokeWidth': 2},
            {'type': 'text', 'x': 135, 'y': 235, 'width': 130, 'height': 25,
             'text': '🔌 n8n', 'fontSize': 16, 'strokeColor': '#e67700'},
            {'type': 'rectangle', 'x': 100, 'y': 290, 'width': 200, 'height': 50,
             'strokeColor': '#1864ab', 'backgroundColor': '#e7f5ff', 'strokeWidth': 2},
            {'type': 'text', 'x': 135, 'y': 305, 'width': 130, 'height': 25,
             'text': '📊 Redis', 'fontSize': 16, 'strokeColor': '#1864ab'},
            # Arrow
            {'type': 'arrow', 'x': 320, 'y': 240, 'points': [[0, 0], [120, 0]],
             'strokeColor': '#e8590c', 'strokeWidth': 3},
            # GitHub
            {'type': 'rectangle', 'x': 460, 'y': 80, 'width': 260, 'height': 360,
             'strokeColor': '#1a1a2e', 'backgroundColor': '#f8f9fa', 'strokeWidth': 2},
            {'type': 'text', 'x': 520, 'y': 95, 'width': 140, 'height': 40,
             'text': '🐙 GitHub', 'fontSize': 20, 'strokeColor': '#1a1a2e'},
            {'type': 'rectangle', 'x': 480, 'y': 150, 'width': 220, 'height': 60,
             'strokeColor': '#495057', 'backgroundColor': '#ffffff', 'strokeWidth': 2},
            {'type': 'text', 'x': 500, 'y': 170, 'width': 180, 'height': 25,
             'text': '📦 radit repo', 'fontSize': 15, 'strokeColor': '#495057'},
        ]
    },
    'memory-sync': {
        'width': 900,
        'height': 600,
        'elements': [
            {'type': 'rectangle', 'x': 80, 'y': 80, 'width': 240, 'height': 360,
             'strokeColor': '#1971c2', 'backgroundColor': '#e7f5ff', 'strokeWidth': 2},
            {'type': 'text', 'x': 140, 'y': 95, 'width': 120, 'height': 40,
             'text': '🤖 RADIT', 'fontSize': 24, 'strokeColor': '#1971c2'},
            {'type': 'rectangle', 'x': 100, 'y': 150, 'width': 200, 'height': 50,
             'strokeColor': '#c92a2a', 'backgroundColor': '#ffe3e3', 'strokeWidth': 2},
            {'type': 'text', 'x': 120, 'y': 165, 'width': 160, 'height': 25,
             'text': '📄 MEMORY.md', 'fontSize': 16, 'strokeColor': '#c92a2a'},
            {'type': 'rectangle', 'x': 100, 'y': 220, 'width': 200, 'height': 50,
             'strokeColor': '#e67700', 'backgroundColor': '#fff9db', 'strokeWidth': 2},
            {'type': 'text', 'x': 115, 'y': 235, 'width': 170, 'height': 25,
             'text': '📝 memory/*.md', 'fontSize': 16, 'strokeColor': '#e67700'},
            {'type': 'rectangle', 'x': 100, 'y': 290, 'width': 200, 'height': 50,
             'strokeColor': '#2f9e44', 'backgroundColor': '#d3f9d8', 'strokeWidth': 2},
            {'type': 'text', 'x': 130, 'y': 305, 'width': 140, 'height': 25,
             'text': '📔 diary/*.md', 'fontSize': 16, 'strokeColor': '#2f9e44'},
            {'type': 'rectangle', 'x': 100, 'y': 360, 'width': 200, 'height': 50,
             'strokeColor': '#1864ab', 'backgroundColor': '#e7f5ff', 'strokeWidth': 2},
            {'type': 'text', 'x': 130, 'y': 375, 'width': 140, 'height': 25,
             'text': '📋 tasks/*.md', 'fontSize': 16, 'strokeColor': '#1864ab'},
            {'type': 'diamond', 'x': 360, 'y': 200, 'width': 100, 'height': 80,
             'strokeColor': '#2f9e44', 'backgroundColor': '#b2f2bb', 'strokeWidth': 3},
            {'type': 'text', 'x': 380, 'y': 225, 'width': 60, 'height': 35,
             'text': '⏰ CRON\n15 min', 'fontSize': 14, 'strokeColor': '#2b8a3e'},
            {'type': 'arrow', 'x': 340, 'y': 240, 'points': [[0, 0], [120, 0]],
             'strokeColor': '#e8590c', 'strokeWidth': 3},
            {'type': 'rectangle', 'x': 460, 'y': 80, 'width': 260, 'height': 360,
             'strokeColor': '#1a1a2e', 'backgroundColor': '#f8f9fa', 'strokeWidth': 2},
            {'type': 'text', 'x': 520, 'y': 95, 'width': 140, 'height': 40,
             'text': '🐙 GITHUB', 'fontSize': 24, 'strokeColor': '#1a1a2e'},
            {'type': 'rectangle', 'x': 480, 'y': 150, 'width': 220, 'height': 60,
             'strokeColor': '#495057', 'backgroundColor': '#ffffff', 'strokeWidth': 2},
            {'type': 'text', 'x': 500, 'y': 170, 'width': 180, 'height': 25,
             'text': '📦 fanani-radian/radit', 'fontSize': 15, 'strokeColor': '#495057'},
            {'type': 'rectangle', 'x': 480, 'y': 230, 'width': 220, 'height': 60,
             'strokeColor': '#495057', 'backgroundColor': '#ffffff', 'strokeWidth': 2},
            {'type': 'text', 'x': 500, 'y': 250, 'width': 180, 'height': 25,
             'text': '📦 radit-dashboard', 'fontSize': 15, 'strokeColor': '#495057'},
            {'type': 'rectangle', 'x': 480, 'y': 310, 'width': 220, 'height': 60,
             'strokeColor': '#495057', 'backgroundColor': '#ffffff', 'strokeWidth': 2},
            {'type': 'text', 'x': 520, 'y': 330, 'width': 140, 'height': 25,
             'text': '📦 simpaw', 'fontSize': 15, 'strokeColor': '#495057'},
        ]
    },
    'quick-note': {
        'width': 600,
        'height': 400,
        'elements': [
            {'type': 'rectangle', 'x': 50, 'y': 50, 'width': 500, 'height': 300,
             'strokeColor': '#e67700', 'backgroundColor': '#fff9db', 'strokeWidth': 3},
            {'type': 'text', 'x': 200, 'y': 70, 'width': 200, 'height': 40,
             'text': '📝 QUICK NOTE', 'fontSize': 24, 'strokeColor': '#e67700'},
            {'type': 'text', 'x': 80, 'y': 130, 'width': 440, 'height': 180,
             'text': '• Point 1\n• Point 2\n• Point 3', 'fontSize': 18, 'strokeColor': '#495057'},
        ]
    }
}

def generate_diagram(template_name, output_file):
    if template_name not in TEMPLATES:
        print(f"Error: Template '{template_name}' not found.")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)
    
    diagram = {
        'type': 'excalidraw',
        'version': 2,
        'source': f'radit-{template_name}',
        'elements': TEMPLATES[template_name]['elements'],
        'appState': {'viewBackgroundColor': '#ffffff'}
    }
    
    with open(output_file, 'w') as f:
        json.dump(diagram, f, indent=2)
    
    print(f"✅ Generated: {output_file}")
    print(f"   Template: {template_name}")
    print(f"   Elements: {len(diagram['elements'])}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Excalidraw diagrams')
    parser.add_argument('--template', '-t', required=True, help='Template name')
    parser.add_argument('--output', '-o', required=True, help='Output filename')
    args = parser.parse_args()
    
    output_file = args.output if args.output.endswith('.excalidraw') else args.output + '.excalidraw'
    generate_diagram(args.template, output_file)
