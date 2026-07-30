#!/usr/bin/env python3
"""Convert prepped grayscale image to animated ASCII art SVG."""

import sys
from pathlib import Path
from PIL import Image

# Density ramp: space (brightest) to @ (darkest)
RAMP = " .:-=+*#%@"

def brightness_to_char(brightness: int) -> str:
    """Map 0-255 brightness to ASCII character."""
    # Invert and boost contrast
    adjusted = max(0, min(255, int((brightness - 100) * 1.5 + 100)))
    index = int((1 - adjusted / 255.0) * (len(RAMP) - 1))
    return RAMP[index]

def make_ascii_svg(
    source_path: str = "source-prepped.png",
    output_path: str = "avi-ascii.svg",
    char_width: int = 100,
):
    print(f"Loading {source_path}...")
    img = Image.open(source_path).convert('L')
    
    # Calculate char height to maintain aspect ratio
    aspect = img.height / img.width
    char_height = int(char_width * aspect * 0.5)  # 0.5 corrects for char aspect ratio
    
    # Downsample to character grid
    print(f"Downsampling to {char_width}×{char_height} grid...")
    img_small = img.resize((char_width, char_height), Image.Resampling.LANCZOS)
    
    # Convert to ASCII
    print("Converting to ASCII...")
    lines = []
    for y in range(char_height):
        line = ""
        for x in range(char_width):
            brightness = img_small.getpixel((x, y))
            line += brightness_to_char(brightness)
        lines.append(line)
    
    # Build SVG with animation
    print(f"Building SVG to {output_path}...")
    
    font_size = 10
    char_w = font_size * 0.6
    char_h = font_size * 1.2
    
    svg_width = char_width * char_w
    svg_height = char_height * char_h
    
    # Animation timing
    row_duration = 0.03  # seconds per row
    total_duration = char_height * row_duration
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}">',
        '<style>',
        f'text {{ font-family: monospace; font-size: {font_size}px; fill: #8b949e; }}',
        '.cursor { fill: #58a6ff; }',
        '</style>',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
    ]
    
    for i, line in enumerate(lines):
        y = (i + 1) * char_h
        delay = i * row_duration
        
        # Escape XML entities
        escaped_line = (line
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))
        
        # Each row has a clip-path that wipes left-to-right
        clip_id = f"clip{i}"
        svg_lines.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="{y - char_h}" width="0" height="{char_h}">'
            f'<animate attributeName="width" from="0" to="{svg_width}" '
            f'begin="{delay}s" dur="{row_duration}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        
        svg_lines.append(
            f'<text x="0" y="{y}" clip-path="url(#{clip_id})">{escaped_line}</text>'
        )
        
        # Typing cursor (small block that follows the wipe)
        svg_lines.append(
            f'<rect class="cursor" x="0" y="{y - char_h}" width="{char_w}" height="{char_h}">'
            f'<animate attributeName="x" from="0" to="{svg_width}" '
            f'begin="{delay}s" dur="{row_duration}s" fill="freeze"/>'
            f'<animate attributeName="opacity" from="1" to="0" '
            f'begin="{delay + row_duration}s" dur="0.1s" fill="freeze"/>'
            f'</rect>'
        )
    
    svg_lines.append('</svg>')
    
    Path(output_path).write_text('\n'.join(svg_lines))
    print("Done!")

if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    output = sys.argv[2] if len(sys.argv) > 2 else "avi-ascii.svg"
    make_ascii_svg(source, output)
