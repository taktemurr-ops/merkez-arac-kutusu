#!/usr/bin/env python3
"""Araç Kutusu merkezinin özgün simge, açılış ve mağaza görselleri (Pillow).
Üçüncü taraf görsel kullanılmaz.  pip install pillow && python tool/generate_assets.py"""
import os
from PIL import Image, ImageDraw

BG_TOP, BG_BOTTOM, ACCENT = (18, 58, 79), (7, 22, 34), (79, 209, 197)


def gradient(w, h):
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(BG_TOP[i] * (1 - t) + BG_BOTTOM[i] * t) for i in range(3)))
    return im


def glyph(d, cx, cy, s, color=ACCENT):
    """Anahtar ve tornavida çaprazı: özgün, sade çizim."""
    w = max(2, int(s // 9))
    # tornavida
    d.line([(cx - s * 0.38, cy + s * 0.38), (cx + s * 0.22, cy - s * 0.22)], fill=(236, 239, 241), width=w)
    d.rounded_rectangle([cx + s * 0.16, cy - s * 0.44, cx + s * 0.44, cy - s * 0.16], radius=w, fill=color)
    # anahtar
    d.line([(cx - s * 0.30, cy - s * 0.30), (cx + s * 0.36, cy + s * 0.36)], fill=color, width=w)
    r = s * 0.16
    d.ellipse([cx - s * 0.30 - r, cy - s * 0.30 - r, cx - s * 0.30 + r, cy - s * 0.30 + r], outline=color, width=w)
    d.ellipse([cx + s * 0.36 - r * 0.6, cy + s * 0.36 - r * 0.6, cx + s * 0.36 + r * 0.6, cy + s * 0.36 + r * 0.6], fill=color)


def icon(size=1024):
    im = gradient(size, size)
    glyph(ImageDraw.Draw(im), size / 2, size / 2, size * 0.62)
    return im


def main():
    os.makedirs("assets/branding", exist_ok=True)
    os.makedirs("store", exist_ok=True)
    ic = icon()
    ic.save("assets/branding/icon.png")
    fg = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    glyph(ImageDraw.Draw(fg), 512, 512, 420)
    fg.save("assets/branding/icon_foreground.png")
    sp = Image.new("RGBA", (768, 768), (0, 0, 0, 0))
    glyph(ImageDraw.Draw(sp), 384, 384, 300)
    sp.save("assets/branding/splash.png")
    a12 = Image.new("RGBA", (1152, 1152), (0, 0, 0, 0))
    glyph(ImageDraw.Draw(a12), 576, 576, 380)
    a12.save("assets/branding/splash_android12.png")
    ic.resize((512, 512)).save("store/icon_512.png")
    fe = gradient(1024, 500)
    glyph(ImageDraw.Draw(fe), 512, 250, 300)
    fe.save("store/feature_graphic.png")
    print("assets ok")


if __name__ == "__main__":
    main()
