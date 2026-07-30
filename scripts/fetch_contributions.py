#!/usr/bin/env python3
"""Fetch GitHub contribution data from public HTML (no token needed)."""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# Set your GitHub username here
GITHUB_USERNAME = "priyanshu0463"

def fetch_contributions():
    url = f"https://github.com/users/{GITHUB_USERNAME}/contributions"
    print(f"Fetching contributions from {url}...")
    
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Parse contribution cells
    days = []
    for cell in soup.select('td.ContributionCalendar-day'):
        date = cell.get('data-date')
        level = cell.get('data-level', '0')
        count_match = re.search(r'(\d+) contribution', cell.get('data-title', ''))
        count = int(count_match.group(1)) if count_match else 0
        
        days.append({
            'date': date,
            'count': count,
            'level': int(level)
        })
    
    print(f"Found {len(days)} days of contributions")
    
    # Calculate stats
    total = sum(d['count'] for d in days)
    best_day = max(days, key=lambda d: d['count'])
    
    # Current streak
    current_streak = 0
    for day in reversed(days):
        if day['count'] > 0:
            current_streak += 1
        else:
            break
    
    # Longest streak
    longest_streak = 0
    streak = 0
    for day in days:
        if day['count'] > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0
    
    # Monthly totals (last 12 months)
    monthly = {}
    for day in days:
        month = day['date'][:7]  # YYYY-MM
        monthly[month] = monthly.get(month, 0) + day['count']
    
    data = {
        'username': GITHUB_USERNAME,
        'fetched_at': datetime.utcnow().isoformat(),
        'days': days,
        'stats': {
            'total': total,
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'best_day': best_day,
            'monthly': monthly
        }
    }
    
    # Save to file
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'contributions.json'
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved to {output_path}")
    print(f"Total contributions: {total}")
    print(f"Current streak: {current_streak} days")
    print(f"Longest streak: {longest_streak} days")
    print(f"Best day: {best_day['date']} ({best_day['count']} contributions)")

if __name__ == "__main__":
    fetch_contributions()
