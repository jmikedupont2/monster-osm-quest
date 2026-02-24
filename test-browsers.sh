#!/usr/bin/env nix-shell
#! nix-shell shell-browser-test.nix -i bash

# Test Monster OSM Quest in multiple browsers

set -e

echo "🎭 Monster OSM Quest - Browser Testing"
echo "======================================"

# Get absolute path
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX="$DIR/index.html"

if [ ! -f "$INDEX" ]; then
    echo "❌ index.html not found"
    exit 1
fi

echo "📄 Testing: $INDEX"
echo ""

# Test Firefox
echo "🦊 Testing Firefox..."
firefox --headless --screenshot /tmp/monster-osm-firefox.png "$INDEX" &
FIREFOX_PID=$!
sleep 5
kill $FIREFOX_PID 2>/dev/null || true

if [ -f /tmp/monster-osm-firefox.png ]; then
    echo "  ✅ Firefox screenshot: /tmp/monster-osm-firefox.png"
    identify /tmp/monster-osm-firefox.png | head -1
else
    echo "  ⚠️  Firefox screenshot failed"
fi

# Test Chromium
echo ""
echo "🌐 Testing Chromium..."
chromium --headless --screenshot=/tmp/monster-osm-chromium.png "$INDEX" 2>/dev/null &
CHROMIUM_PID=$!
sleep 5
kill $CHROMIUM_PID 2>/dev/null || true

if [ -f /tmp/monster-osm-chromium.png ]; then
    echo "  ✅ Chromium screenshot: /tmp/monster-osm-chromium.png"
    identify /tmp/monster-osm-chromium.png | head -1
else
    echo "  ⚠️  Chromium screenshot failed"
fi

# Run Python Selenium tests
echo ""
echo "🧪 Running Selenium tests..."
if command -v python3 &> /dev/null; then
    python3 test-browsers.py
else
    echo "  ⚠️  Python3 not available, skipping Selenium tests"
fi

# Compare screenshots
echo ""
echo "📊 Screenshot Comparison:"
if [ -f /tmp/monster-osm-firefox.png ] && [ -f /tmp/monster-osm-chromium.png ]; then
    echo "  Firefox:  $(identify -format '%wx%h' /tmp/monster-osm-firefox.png)"
    echo "  Chromium: $(identify -format '%wx%h' /tmp/monster-osm-chromium.png)"
    
    # Create comparison
    convert /tmp/monster-osm-firefox.png /tmp/monster-osm-chromium.png +append /tmp/monster-osm-comparison.png
    echo "  ✅ Comparison: /tmp/monster-osm-comparison.png"
fi

echo ""
echo "✅ Browser testing complete!"
echo ""
echo "View screenshots:"
echo "  eog /tmp/monster-osm-*.png"
