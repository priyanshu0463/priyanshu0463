#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG with animated reveal."""

import os
from pathlib import Path

def make_info_card(output_path: str = "info-card.svg"):
    # Edit your info here
    info = {
        "Now": "Full-stack + AI/ML + DevOps",
        "Prev": "2 IEEE publications, SmartMeter Core",
        "Stack": "React, Node, Python, Docker, AWS",
        "Highlights": "Ships code & breaks prod (pentesting)",
    }
    
    static = os.getenv("STATIC") == "1"
    
    width = 490
    height = 280
    
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<style>',
        'text { font-family: monospace; font-size: 14px; }',
        '.title { fill: #58a6ff; font-weight: bold; font-size: 18px; }',
        '.key { fill: #7ee787; }',
        '.value { fill: #e6edf3; }',
        '</style>',
        '<rect width="100%" height="100%" fill="#0d1117" rx="6"/>',
    ]
    
    # Title
    y = 40
    if static:
        lines.append(f'<text x="20" y="{y}" class="title">priyanshu@github</text>')
    else:
        lines.append(
            f'<text x="20" y="{y}" class="title" opacity="0">'
            f'priyanshu@github'
            f'<animate attributeName="opacity" from="0" to="1" begin="0s" dur="0.3s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-20 0" to="0 0" begin="0s" dur="0.3s" fill="freeze"/>'
            f'</text>'
        )
    
    # Separator
    y += 20
    lines.append(f'<line x1="20" y1="{y}" x2="{width-20}" y2="{y}" stroke="#30363d" stroke-width="1"/>')
    
    # Info rows
    y += 30
    row_height = 28
    for i, (key, val) in enumerate(info.items()):
        delay = 0.1 + i * 0.15
        
        if static:
            lines.append(f'<text x="20" y="{y}" class="key">{key}:</text>')
            lines.append(f'<text x="140" y="{y}" class="value">{val}</text>')
        else:
            lines.append(
                f'<g opacity="0">'
                f'<text x="20" y="{y}" class="key">{key}:</text>'
                f'<text x="140" y="{y}" class="value">{val}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" begin="{delay}s" dur="0.3s" fill="freeze"/>'
                f'</g>'
            )
        
        y += row_height
    
    lines.append('</svg>')
    
    Path(output_path).write_text('\n'.join(lines))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    make_info_card()
