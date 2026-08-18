#!/usr/bin/env python3
"""
Generate a demo PNG screenshot of the terminal output for the telemetry project.
If Pillow is not installed, the script will print the ASCII demo to stdout.

Usage:
    python tools/generate_demo_screenshot.py --out demo.png

"""
import sys
import argparse


DEMO_TEXT = (
    "==============================================\n"
    "   FORZA HORIZON 6 TELEMETRY  (demo)\n"
    "==============================================\n\n"
    "Vites:  3 | Hız: 128.3 km/h | RPM: 5300 | Max RPM: 7000\n\n"
    "[DEBUG] packet(64): 01000000aabbccddeeff00112233445566778899aabbccddeeff0011223344\n"
    "[DEBUG] gear_raw=3 gear=3 speed=128.30 RPM=5300\n"
)


def generate_png(text: str, out_path: str):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        print("Pillow is not installed. Install it with: pip install pillow")
        return False

    # choose a monospace font; default to PIL's built-in if not available
    font = ImageFont.load_default()
    # estimate image size using ImageDraw.textsize for compatibility
    lines = text.splitlines()
    tmp_img = Image.new("RGB", (1, 1))
    tmp_draw = ImageDraw.Draw(tmp_img)

    def measure(line):
        # Try multiple APIs for compatibility across Pillow versions
        try:
            bbox = tmp_draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            return w, h
        except Exception:
            pass
        try:
            size = tmp_draw.textsize(line, font=font)
            return size[0], size[1]
        except Exception:
            pass
        try:
            bbox = font.getbbox(line)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            return w, h
        except Exception:
            pass
        # fallback
        mask = font.getmask(line)
        return mask.size

    widths = [measure(line)[0] for line in lines]
    heights = [measure(line)[1] for line in lines]
    max_width = max(widths) if widths else 0
    line_height = max(heights) if heights else 10
    img = Image.new("RGB", (max_width + 20, line_height * len(lines) + 20), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    y = 10
    for line in lines:
        draw.text((10, y), line, font=font, fill=(220, 220, 220))
        y += line_height
    img.save(out_path)
    return True


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="demo.png", help="Output PNG path")
    args = p.parse_args(argv)

    ok = generate_png(DEMO_TEXT, args.out)
    if ok:
        print(f"Generated demo image: {args.out}")
    else:
        print(DEMO_TEXT)


if __name__ == "__main__":
    main(sys.argv[1:])
