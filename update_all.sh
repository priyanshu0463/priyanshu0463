#!/bin/bash
# Regenerate all profile art (run this locally when you change your photo or info)

set -e

echo "🔄 Activating Python environment..."
source .venv/bin/activate

echo "📸 Prepping photo (if source-prepped.png is missing or you have a new photo)..."
if [ ! -f "source-prepped.png" ] || [ "$1" = "photo" ]; then
    if [ -f "asset/WhatsApp Image 2026-07-14 at 11.28.41 AM.jpeg" ]; then
        python scripts/prep_photo.py "asset/WhatsApp Image 2026-07-14 at 11.28.41 AM.jpeg"
    else
        echo "⚠️  Photo not found. Place your photo in asset/ and run:"
        echo "    python scripts/prep_photo.py asset/your-photo.jpg"
    fi
fi

echo "🎨 Generating ASCII art..."
python scripts/make_ascii_svg.py

echo "📇 Generating info card..."
python scripts/make_info_card.py

echo "📊 Fetching contributions..."
python scripts/fetch_contributions.py

echo "🗺️  Rendering heatmap..."
python scripts/render_heatmap_svg.py

echo "✅ All done! Your profile is ready."
echo ""
echo "Next steps:"
echo "  1. Review the generated SVGs"
echo "  2. Customize scripts/make_info_card.py with your details"
echo "  3. Commit and push to GitHub"
echo "  4. The heatmap will auto-update daily via GitHub Actions"
