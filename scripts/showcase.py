"""Render the README images into images/ from the built TTF.

Run after ./scripts/build.sh:  python scripts/showcase.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF = os.path.join(ROOT, "fonts", "ttf", "AncoHeist-Black.ttf")
OUT = os.path.join(ROOT, "images")
os.makedirs(OUT, exist_ok=True)

INK = (238, 236, 230)
DIM = (150, 148, 142)
GOLD = (233, 196, 82)
RED = (178, 34, 34)
GREEN = (96, 170, 84)


def font(size):
    return ImageFont.truetype(TTF, size)


def gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return img


def vignette(img, strength=0.55):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((-w * 0.25, -h * 0.35, w * 1.25, h * 1.35), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) // 6))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(img, Image.blend(img, dark, strength), mask)


def grain(img, amount=10):
    """Light dithered texture, kept small so the PNGs stay small."""
    return img.quantize(256, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")


def shadow_text(img, xy, text, f, fill, blur=10, offset=(6, 8), alpha=170, anchor="la", stroke=0):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((xy[0] + offset[0], xy[1] + offset[1]), text, font=f,
                               fill=(0, 0, 0, alpha), anchor=anchor, stroke_width=stroke)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.paste(layer, (0, 0), layer)
    ImageDraw.Draw(img).text(xy, text, font=f, fill=fill, anchor=anchor,
                             stroke_width=stroke, stroke_fill=(10, 10, 10))


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path, optimize=True)
    print("saved", path)


def hero():
    W, H = 2400, 1000
    img = gradient(W, H, (44, 46, 50), (14, 15, 17))
    img = vignette(img)
    shadow_text(img, (W // 2, 430), "ANCO HEIST", font(300), INK, blur=18, offset=(10, 14), anchor="mm")
    d = ImageDraw.Draw(img)
    d.rectangle((W // 2 - 520, 600, W // 2 + 520, 612), fill=GOLD)
    d.text((W // 2, 700), "A HEAVY DISPLAY TYPEFACE", font=font(70), fill=DIM, anchor="mm")
    d.text((W // 2, 830), "FREE AND OPEN SOURCE  /  SIL OFL 1.1", font=font(46), fill=(110, 108, 104), anchor="mm")
    save(grain(img), "hero.png")


def charset():
    W, H = 2400, 1350
    img = gradient(W, H, (226, 221, 208), (205, 199, 184))
    d = ImageDraw.Draw(img)
    ink = (24, 24, 26)
    x = 110
    d.text((x, 90), "CHARACTER SET", font=font(52), fill=(130, 124, 110))
    rows = [
        (150, "ABCDEFGHIJKLM"), (150, "NOPQRSTUVWXYZ"),
        (150, "abcdefghijklm"), (150, "nopqrstuvwxyz"),
        (150, "0123456789"), (120, "$ ₺ % # ! ? . , : ; ' \" ( ) [ ] + = * /"),
    ]
    y = 190
    for size, text in rows:
        d.text((x, y), text, font=font(size), fill=ink)
        y += int(size * 1.18)
    save(grain(img, 8), "charset.png")


def hud():
    W, H = 2400, 1200
    img = gradient(W, H, (92, 96, 104), (38, 40, 44))
    d = ImageDraw.Draw(img)
    # fake skyline silhouette for depth
    import random
    random.seed(4)
    x = 0
    while x < W:
        bw = random.randint(80, 220)
        bh = random.randint(250, 640)
        d.rectangle((x, H - bh, x + bw, H), fill=(30, 32, 36))
        for wy in range(H - bh + 30, H - 20, 46):
            for wx in range(x + 18, x + bw - 18, 40):
                if random.random() < 0.18:
                    d.rectangle((wx, wy, wx + 14, wy + 20), fill=(196, 170, 110))
        x += bw + random.randint(4, 30)
    img = Image.blend(img, Image.new("RGB", (W, H), (60, 60, 60)), 0.35)  # desaturated, washed look
    img = vignette(img, 0.65)
    shadow_text(img, (W - 90, 90), "$1,250", font(130), GREEN, blur=4, offset=(4, 5), anchor="ra", stroke=6)
    shadow_text(img, (W // 2, H // 2 - 20), "WASTED", font(330), RED, blur=16, offset=(8, 12), anchor="mm", stroke=4)
    d = ImageDraw.Draw(img)
    d.text((W // 2, H - 150), "Not the best day in the city.", font=font(64), fill=INK,
           anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    save(grain(img, 12), "hud.png")


def turkish():
    W, H = 2400, 900
    img = gradient(W, H, (28, 30, 34), (16, 17, 19))
    img = vignette(img, 0.4)
    d = ImageDraw.Draw(img)
    d.text((110, 90), "TÜRKÇE KARAKTERLER", font=font(52), fill=(120, 118, 112))
    d.text((110, 190), "ÇĞİÖŞÜ  çğıöşü", font=font(200), fill=GOLD)
    d.text((110, 470), "Pijamalı hasta yağız", font=font(130), fill=INK)
    d.text((110, 640), "şoföre çabucak güvendi.", font=font(130), fill=INK)
    save(grain(img), "turkish.png")


def waterfall():
    W, H = 2400, 1300
    img = Image.new("RGB", (W, H), (240, 237, 229))
    d = ImageDraw.Draw(img)
    y = 70
    for size in (36, 56, 84, 120, 160, 220):
        d.text((110, y + size * 0.1), f"{size}", font=font(34), fill=(150, 146, 136))
        d.text((260, y), "Heist at the harbor", font=font(size), fill=(24, 24, 26))
        y += int(size * 1.25) + 30
    save(img, "waterfall.png")


if __name__ == "__main__":
    hero()
    charset()
    hud()
    turkish()
    waterfall()
