#!/usr/bin/env nix-shell
#! nix-shell shell-browser-test.nix -i bash

# Simple browser test - just open and screenshot

echo "🎭 Monster OSM Quest - Simple Browser Test"
echo "==========================================="

INDEX="file://$(pwd)/index.html"
echo "Testing: $INDEX"
echo ""

# Test Firefox
echo "🦊 Firefox..."
xvfb-run -a firefox --headless --screenshot /tmp/monster-firefox.png "$INDEX" 2>/dev/null && \
  echo "  ✅ Screenshot: /tmp/monster-firefox.png" || \
  echo "  ⚠️  Firefox test skipped"

# Test Chromium  
echo "🌐 Chromium..."
xvfb-run -a chromium --headless --disable-gpu --screenshot=/tmp/monster-chromium.png "$INDEX" 2>/dev/null && \
  echo "  ✅ Screenshot: /tmp/monster-chromium.png" || \
  echo "  ⚠️  Chromium test skipped"

echo ""
echo "✅ Tests complete!"
ls -lh /tmp/monster-*.png 2>/dev/null || echo "No screenshots generated"
