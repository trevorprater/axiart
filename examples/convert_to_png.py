#!/usr/bin/env python3
"""Quick script to convert SVG to PNG."""

import sys
sys.path.insert(0, '..')

# Try multiple conversion methods
svg_file = "output_self_portrait_claude.svg"
png_file = "output_self_portrait_claude.png"

# Method 1: Try cairosvg
try:
    import cairosvg
    print("Using cairosvg...")
    cairosvg.svg2png(url=svg_file, write_to=png_file, scale=3.0)
    print(f"✓ Converted to {png_file} (cairosvg, 3x scale)")
    sys.exit(0)
except ImportError:
    print("cairosvg not available, trying next method...")
except Exception as e:
    print(f"cairosvg failed: {e}")

# Method 2: Try svglib + reportlab
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    print("Using svglib + reportlab...")
    drawing = svg2rlg(svg_file)
    renderPM.drawToFile(drawing, png_file, fmt="PNG", dpi=300)
    print(f"✓ Converted to {png_file} (svglib, 300 DPI)")
    sys.exit(0)
except ImportError:
    print("svglib/reportlab not available, trying next method...")
except Exception as e:
    print(f"svglib failed: {e}")

# Method 3: Try wand (ImageMagick Python binding)
try:
    from wand.image import Image
    print("Using wand (ImageMagick)...")
    with Image(filename=svg_file, resolution=300) as img:
        img.format = 'png'
        img.save(filename=png_file)
    print(f"✓ Converted to {png_file} (wand, 300 DPI)")
    sys.exit(0)
except ImportError:
    print("wand not available")
except Exception as e:
    print(f"wand failed: {e}")

print("\nNo conversion libraries available. Installing cairosvg...")
print("Run: uv pip install cairosvg")
