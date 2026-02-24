#!/usr/bin/env python3
"""Analyze Monster OSM Quest screenshots with OpenCV and extract game information"""

import cv2
import numpy as np
import json
from pathlib import Path

def analyze_screenshot(image_path):
    """Analyze a screenshot and extract game information"""
    print(f"\n🔬 Analyzing {image_path}...")
    
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"  ❌ Could not load image")
        return None
    
    height, width = img.shape[:2]
    print(f"  📐 Dimensions: {width}x{height}")
    
    # Convert to different color spaces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Detect edges (game elements)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size
    print(f"  🎨 Edge density: {edge_density:.4f}")
    
    # Color analysis
    avg_color = np.mean(img, axis=(0, 1))
    print(f"  🌈 Average BGR: {avg_color.astype(int)}")
    
    # Detect dark background (game uses black #000)
    dark_pixels = np.sum(gray < 30) / gray.size
    print(f"  🌑 Dark pixels: {dark_pixels:.2%}")
    
    # Detect green text (#0f0)
    green_mask = cv2.inRange(hsv, np.array([40, 100, 100]), np.array([80, 255, 255]))
    green_ratio = np.sum(green_mask > 0) / green_mask.size
    print(f"  💚 Green text: {green_ratio:.4%}")
    
    # Detect cyan elements (#0ff)
    cyan_mask = cv2.inRange(hsv, np.array([80, 100, 100]), np.array([100, 255, 255]))
    cyan_ratio = np.sum(cyan_mask > 0) / cyan_mask.size
    print(f"  🔵 Cyan elements: {cyan_ratio:.4%}")
    
    # Find contours (UI elements)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large_contours = [c for c in contours if cv2.contourArea(c) > 100]
    print(f"  📦 UI elements detected: {len(large_contours)}")
    
    # Detect sidebar (right 300px)
    sidebar_region = img[:, -300:]
    sidebar_avg = np.mean(sidebar_region)
    print(f"  📊 Sidebar brightness: {sidebar_avg:.1f}")
    
    # Detect map area (left side)
    map_region = img[:, :-300]
    map_variance = np.var(map_region)
    print(f"  🗺️  Map variance: {map_variance:.1f}")
    
    return {
        "dimensions": {"width": width, "height": height},
        "edge_density": float(edge_density),
        "dark_pixels": float(dark_pixels),
        "green_text_ratio": float(green_ratio),
        "cyan_elements_ratio": float(cyan_ratio),
        "ui_elements": len(large_contours),
        "sidebar_brightness": float(sidebar_avg),
        "map_variance": float(map_variance),
        "avg_color": avg_color.tolist()
    }

def detect_game_elements(image_path):
    """Detect specific game elements using template matching and feature detection"""
    print(f"\n🎮 Detecting game elements in {image_path}...")
    
    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect emoji/unicode characters (high frequency areas)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
    
    # Find bright spots (emojis are typically bright)
    bright_spots = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    emoji_candidates = [c for c in bright_spots if 20 < cv2.contourArea(c) < 2000]
    print(f"  🎭 Emoji candidates: {len(emoji_candidates)}")
    
    # Detect text regions using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    text_regions = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    print(f"  📝 Text regions: {len(text_regions)}")
    
    # Detect grid pattern (map tiles)
    lines = cv2.HoughLinesP(cv2.Canny(gray, 50, 150), 1, np.pi/180, 50, minLineLength=30, maxLineGap=10)
    if lines is not None:
        print(f"  📏 Grid lines detected: {len(lines)}")
    
    # Feature detection (SIFT for unique game elements)
    sift = cv2.SIFT_create()
    keypoints = sift.detect(gray, None)
    print(f"  🔑 Feature keypoints: {len(keypoints)}")
    
    return {
        "emoji_candidates": len(emoji_candidates),
        "text_regions": len(text_regions),
        "grid_lines": len(lines) if lines is not None else 0,
        "feature_keypoints": len(keypoints)
    }

def verify_game_state(analysis):
    """Verify that the screenshot shows a valid game state"""
    print(f"\n✅ Verifying game state...")
    
    checks = {
        "has_dark_background": analysis["dark_pixels"] > 0.3,
        "has_green_text": analysis["green_text_ratio"] > 0.001,
        "has_ui_elements": analysis["ui_elements"] > 5,
        "has_sidebar": analysis["sidebar_brightness"] > 20,
        "has_map_content": analysis["map_variance"] > 100
    }
    
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check.replace('_', ' ').title()}")
    
    return all(checks.values())

def compare_browsers(firefox_data, chromium_data):
    """Compare Firefox and Chromium renderings"""
    print(f"\n🔬 Comparing browser renderings...")
    
    # Compare dimensions
    ff_dims = firefox_data["dimensions"]
    ch_dims = chromium_data["dimensions"]
    dims_match = ff_dims == ch_dims
    print(f"  {'✅' if dims_match else '⚠️ '} Dimensions: FF {ff_dims['width']}x{ff_dims['height']} vs CH {ch_dims['width']}x{ch_dims['height']}")
    
    # Compare color ratios
    green_diff = abs(firefox_data["green_text_ratio"] - chromium_data["green_text_ratio"])
    print(f"  {'✅' if green_diff < 0.01 else '⚠️ '} Green text difference: {green_diff:.4%}")
    
    # Compare UI elements
    ui_diff = abs(firefox_data["ui_elements"] - chromium_data["ui_elements"])
    print(f"  {'✅' if ui_diff < 5 else '⚠️ '} UI elements difference: {ui_diff}")
    
    # Overall similarity
    similarity = 1.0 - (green_diff + ui_diff/100)
    print(f"  📊 Overall similarity: {similarity:.2%}")
    
    return similarity > 0.9

def main():
    print("🎭 Monster OSM Quest - Screenshot Analysis")
    print("=" * 50)
    
    firefox_path = Path("/tmp/monster-firefox.png")
    chromium_path = Path("/tmp/monster-chromium.png")
    
    results = {}
    
    # Analyze Firefox
    if firefox_path.exists():
        ff_analysis = analyze_screenshot(firefox_path)
        ff_elements = detect_game_elements(firefox_path)
        ff_valid = verify_game_state(ff_analysis)
        results["firefox"] = {**ff_analysis, **ff_elements, "valid": ff_valid}
    else:
        print(f"⚠️  Firefox screenshot not found")
        return 1
    
    # Analyze Chromium
    if chromium_path.exists():
        ch_analysis = analyze_screenshot(chromium_path)
        ch_elements = detect_game_elements(chromium_path)
        ch_valid = verify_game_state(ch_analysis)
        results["chromium"] = {**ch_analysis, **ch_elements, "valid": ch_valid}
    else:
        print(f"⚠️  Chromium screenshot not found")
        return 1
    
    # Compare browsers
    browsers_match = compare_browsers(results["firefox"], results["chromium"])
    
    # Save results
    output_path = Path("/tmp/monster-analysis.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Analysis saved to {output_path}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  Firefox: {'✅ VALID' if results['firefox']['valid'] else '❌ INVALID'}")
    print(f"  Chromium: {'✅ VALID' if results['chromium']['valid'] else '❌ INVALID'}")
    print(f"  Browsers match: {'✅ YES' if browsers_match else '❌ NO'}")
    
    all_valid = results['firefox']['valid'] and results['chromium']['valid'] and browsers_match
    print(f"\n{'✅ ALL TESTS PASSED' if all_valid else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
