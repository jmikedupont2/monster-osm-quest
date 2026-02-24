{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "monster-osm-browser-test";
  
  buildInputs = with pkgs; [
    # Browsers
    firefox
    chromium
    
    # Headless X server
    xvfb-run
    xorg.xorgserver
    
    # VNC (optional)
    tigervnc
    
    # Testing tools
    python3
    python3Packages.selenium
    python3Packages.requests
    
    # Drivers
    geckodriver
    chromedriver
    
    # Screenshot tools
    imagemagick
  ];
  
  shellHook = ''
    echo "🎭 Monster OSM Quest - Browser Testing"
    echo "======================================"
    echo ""
    echo "Available browsers:"
    echo "  - firefox (headless)"
    echo "  - chromium (headless)"
    echo ""
    echo "Test commands:"
    echo "  xvfb-run ./test-browsers.sh"
    echo "  xvfb-run python3 test-browsers.py"
    echo ""
    echo "With VNC (for viewing):"
    echo "  vncserver :1"
    echo "  DISPLAY=:1 firefox index.html"
    echo ""
  '';
}
