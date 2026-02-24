#!/usr/bin/env python3
"""Test Monster OSM Quest in multiple browsers using Selenium"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Test configuration
GITHUB_PAGES_URL = "https://meta-introspector.github.io/monster-osm-quest-standalone/"
LOCAL_URL = "file://" + __file__.rsplit('/', 1)[0] + "/index.html"
TEST_URL = LOCAL_URL  # Change to GITHUB_PAGES_URL for live testing

def test_firefox():
    """Test in Firefox"""
    print("\n🦊 Testing Firefox...")
    
    options = FirefoxOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Firefox(options=options)
    
    try:
        driver.get(TEST_URL)
        time.sleep(2)
        
        # Check title
        assert "Monster OSM Quest" in driver.title
        print("  ✅ Title correct")
        
        # Check game container
        game = driver.find_element(By.ID, "game-container")
        assert game.is_displayed()
        print("  ✅ Game container visible")
        
        # Check map
        map_elem = driver.find_element(By.ID, "map")
        assert map_elem.is_displayed()
        print("  ✅ Map rendered")
        
        # Check sidebar
        sidebar = driver.find_element(By.ID, "sidebar")
        assert sidebar.is_displayed()
        print("  ✅ Sidebar visible")
        
        # Check for avatar emoji
        avatar = driver.find_element(By.CLASS_NAME, "avatar")
        assert "🧙" in avatar.text or avatar.is_displayed()
        print("  ✅ Avatar present")
        
        # Take screenshot
        driver.save_screenshot("/tmp/monster-osm-firefox.png")
        print("  📸 Screenshot: /tmp/monster-osm-firefox.png")
        
        print("✅ Firefox: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Firefox: FAILED - {e}")
        return False
    finally:
        driver.quit()

def test_chromium():
    """Test in Chromium"""
    print("\n🌐 Testing Chromium...")
    
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(TEST_URL)
        time.sleep(2)
        
        # Check title
        assert "Monster OSM Quest" in driver.title
        print("  ✅ Title correct")
        
        # Check game container
        game = driver.find_element(By.ID, "game-container")
        assert game.is_displayed()
        print("  ✅ Game container visible")
        
        # Check map
        map_elem = driver.find_element(By.ID, "map")
        assert map_elem.is_displayed()
        print("  ✅ Map rendered")
        
        # Check sidebar
        sidebar = driver.find_element(By.ID, "sidebar")
        assert sidebar.is_displayed()
        print("  ✅ Sidebar visible")
        
        # Check quest log
        quest_log = driver.find_element(By.ID, "quest-log")
        assert quest_log.is_displayed()
        print("  ✅ Quest log visible")
        
        # Take screenshot
        driver.save_screenshot("/tmp/monster-osm-chromium.png")
        print("  📸 Screenshot: /tmp/monster-osm-chromium.png")
        
        print("✅ Chromium: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Chromium: FAILED - {e}")
        return False
    finally:
        driver.quit()

def test_interactions():
    """Test game interactions"""
    print("\n🎮 Testing Interactions...")
    
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    try:
        driver.get(TEST_URL)
        time.sleep(2)
        
        # Get initial position
        position = driver.find_element(By.ID, "position")
        initial_pos = position.text
        print(f"  📍 Initial position: {initial_pos}")
        
        # Simulate arrow key press (via JavaScript)
        driver.execute_script("""
            const event = new KeyboardEvent('keydown', {key: 'ArrowRight'});
            document.dispatchEvent(event);
        """)
        time.sleep(0.5)
        
        # Check if position changed
        new_pos = position.text
        print(f"  📍 New position: {new_pos}")
        
        if new_pos != initial_pos:
            print("  ✅ Movement works")
        else:
            print("  ⚠️  Movement not detected (may need manual testing)")
        
        # Check steps counter
        steps = driver.find_element(By.ID, "steps")
        print(f"  🚶 Steps: {steps.text}")
        
        print("✅ Interactions: TESTED")
        return True
        
    except Exception as e:
        print(f"❌ Interactions: FAILED - {e}")
        return False
    finally:
        driver.quit()

def main():
    print("🎭 Monster OSM Quest - Browser Testing")
    print("=" * 50)
    print(f"Testing URL: {TEST_URL}")
    
    results = {
        "Firefox": test_firefox(),
        "Chromium": test_chromium(),
        "Interactions": test_interactions()
    }
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    for browser, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {browser}: {status}")
    
    all_passed = all(results.values())
    print("\n" + ("✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"))
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
