#!/usr/bin/env python3
"""Render contribution heatmap SVG from fetched data."""

import json
from pathlib import Path
from datetime import datetime, timedelta

# GitHub green palette
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def level_to_color(level: int) -> str:
    """Map contribution level (0-4+) to color."""
    return PALETTE[min(level, len(PALETTE) - 1)]

def render_heatmap_svg(output_path: str = "contrib-heatmap.svg"):
    # Load data
    data_path = Path('data/contributions.json')
    with open(data_path) as f:
        data = json.load(f)
    
    days = data['days']
    stats = data['stats']
    
    # Build 53-week grid (7 rows × 53 cols)
    cell_size = 11
    cell_gap = 3
    margin = 20
    
    weeks = 53
    days_per_week = 7
    
    grid_width = weeks * (cell_size + cell_gap)
    grid_height = days_per_week * (cell_size + cell_gap)
    
    svg_width = grid_width + margin * 2
    svg_height = grid_height + margin * 2 + 60  # Extra space for legend and stats
    
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">',
        '<style>',
        'text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 12px; fill: #8b949e; }',
        '.legend { font-size: 10px; }',
        '.stats { font-size: 11px; fill: #e6edf3; }',
        f'.cell {{ rx: 2; }}',
        '</style>',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
    ]
    
    # Organize days by week
    weeks_data = []
    week = []
    for day in days:
        week.append(day)
        if len(week) == 7:
            weeks_data.append(week)
            week = []
    if week:
        weeks_data.append(week)
    
    # Render cells with staggered animation
    for week_idx, week in enumerate(weeks_data[:weeks]):
        for day_idx, day in enumerate(week):
            x = margin + week_idx * (cell_size + cell_gap)
            y = margin + day_idx * (cell_size + cell_gap)
            color = level_to_color(day['level'])
            
            # Diagonal stagger animation
            delay = (week_idx + day_idx) * 0.01
            
            lines.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                f'fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.2s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 -5" to="0 0" begin="{delay}s" dur="0.2s" fill="freeze"/>'
                f'<title>{day["date"]}: {day["count"]} contributions</title>'
                f'</rect>'
            )
    
    # Legend
    legend_y = margin + grid_height + 30
    lines.append(f'<text x="{margin}" y="{legend_y}" class="legend">Less</text>')
    
    legend_x = margin + 35
    for i, color in enumerate(PALETTE):
        lines.append(
            f'<rect x="{legend_x + i * (cell_size + cell_gap)}" y="{legend_y - 10}" '
            f'width="{cell_size}" height="{cell_size}" fill="{color}" rx="2"/>'
        )
    
    lines.append(f'<text x="{legend_x + len(PALETTE) * (cell_size + cell_gap) + 5}" y="{legend_y}" class="legend">More</text>')
    
    # Stats footer
    stats_y = legend_y + 25
    stats_text = f"{stats['total']:,} contributions in the last year"
    lines.append(f'<text x="{svg_width // 2}" y="{stats_y}" class="stats" text-anchor="middle">{stats_text}</text>')
    
    lines.append('</svg>')
    
    Path(output_path).write_text('\n'.join(lines))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    render_heatmap_svg()
