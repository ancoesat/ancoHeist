"""Render a specimen image (specimen.png) from the built TTF."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF = os.path.join(ROOT, "fonts", "ttf", "AncoHeist-Black.ttf")

LINES = [
    (150, "ANCO HEIST"),
    (96, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    (96, "abcdefghijklmnopqrstuvwxyz"),
    (96, "0123456789 $₺%#!?.,:;'\"()[]+=*/"),
    (96, "ÇĞİÖŞÜ çğıöşü Çömlekçi"),
    (110, "WASTED  BUSTED  $1,250"),
    (80, "The quick brown fox jumps over the lazy dog."),
]


def main(out=os.path.join(ROOT, "specimen.png"), bg="#101010", fg="#f2f2f2"):
    pad = 60
    W = 2600
    H = pad * 2 + sum(int(s * 1.35) for s, _ in LINES)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    y = pad
    for size, text in LINES:
        f = ImageFont.truetype(TTF, size)
        d.text((pad, y), text, font=f, fill=fg)
        y += int(size * 1.35)
    img.save(out)
    print("saved", out)


if __name__ == "__main__":
    main()
