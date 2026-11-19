#!/usr/bin/env python3
"""Draw the news-of-the-day poster for 19 November 2026 to /output/entry.png.
A programmatic newspaper front page: masthead names the date, six story
cards across regions and fields, each a headline plus an icon glyph.
Standard library + Pillow only, no network, deterministic."""
import os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

# Fonts from the container's font set.
F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

W = H = 1024
INK = (24, 26, 31)
PAPER = (246, 242, 233)
ACCENTS = [
    (176, 32, 38),    # red
    (18, 84, 158),    # blue
    (196, 128, 16),   # amber
    (34, 120, 74),    # green
    (92, 52, 140),    # purple
    (168, 64, 96),    # crimson
]

# The day's stories, each: headline (max ~2 lines), kicker, region tag, glyph.
STORIES = [
    ("Trump, Xi and Putin\nhold historic APEC\nsummit meeting", "DIPLOMACY  Gyeongju, S. Korea", "SUMMIT"),
    ("Anthropic valued at\n$1.5 trillion in\nrecord AI IPO", "BUSINESS  Wall Street", "IPO"),
    ("Israeli ground op\npushes past Gaza\n'yellow line'", "MIDEAST  Gaza City", "GAZA"),
    ("Iran widens Gulf\nattacks: US base in\nKuwait hit", "SECURITY  Gulf", "GULF"),
    ("US loses measles\nelimination status\namid resurgence", "HEALTH  Atlanta", "MEASLES"),
    ("Van Gogh sells for\nrecord $190.4m after\nNazi-era dispute", "ART  New York", "ART"),
]

def draw_glyph(d, glyph, x, y, s, col):
    """Simple vector glyphs for each story, drawn with shapes."""
    d.setink = col
    if glyph == "SUMMIT":
        # three flags
        for i, h in enumerate((34, 44, 28)):
            fx = x + 10 + i * 18
            d.rectangle([fx, y + 46 - h, fx + 3, y + 46], fill=col)
            d.polygon([(fx + 3, y + 46 - h), (fx + 17, y + 40 - h), (fx + 3, y + 34 - h)], fill=col)
    elif glyph == "IPO":
        # rising chart
        pts = [(x, y + 40), (x + 12, y + 28), (x + 22, y + 33), (x + 36, y + 12)]
        d.line(pts, fill=col, width=4)
        d.polygon([(x + 36, y + 12), (x + 24, y + 12), (x + 36, y + 24)], fill=col)
        d.rectangle([x - 4, y + 44, x + 44, y + 48], fill=col)
    elif glyph == "GAZA":
        d.rectangle([x, y + 18, x + 44, y + 42], fill=col)           # wall
        d.rectangle([x + 14, y + 28, x + 30, y + 42], fill=PAPER)    # door gap
        d.line([(x - 6, y + 12), (x + 50, y + 4)], fill=col, width=4)  # sweep line
    elif glyph == "GULF":
        # radar arcs
        for r in (12, 22, 32):
            d.arc([x + 22 - r, y + 40 - r, x + 22 + r, y + 40 + r], 200, 340, fill=col, width=4)
        d.ellipse([x + 18, y + 36, x + 26, y + 44], fill=col)
    elif glyph == "MEASLES":
        # shield with cross
        d.polygon([(x + 22, y + 6), (x + 44, y + 14), (x + 44, y + 30),
                   (x + 22, y + 46), (x, y + 30), (x, y + 14)], outline=col, width=4)
        d.rectangle([x + 19, y + 16, x + 25, y + 36], fill=col)
        d.rectangle([x + 12, y + 23, x + 32, y + 29], fill=col)
    elif glyph == "ART":
        # framed painting + hammer
        d.rectangle([x, y + 10, x + 34, y + 44], outline=col, width=4)
        d.line([(x + 26, y + 40), (x + 46, y + 4)], fill=col, width=5)

def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead rule lines
    d.rectangle([40, 30, W - 40, 34], fill=INK)
    d.text((40, 46), "THE DAY IN PICTURES", font=font(SERIF_B, 44), fill=INK)
    d.text((W - 40 - 260, 58), "Thursday, 19 November 2026",
           font=font(SANS_B, 20), fill=(90, 90, 96))
    d.rectangle([40, 108, W - 40, 110], fill=INK)

    # Six story cards, 3 x 2
    card_w, card_h, gap = 296, 380, 24
    x0, y0 = 40, 140
    for i, (headline, kicker, glyph) in enumerate(STORIES):
        col = ACCENTS[i]
        r, c = divmod(i, 3)
        x, y = x0 + c * (card_w + gap), y0 + r * (card_h + gap)
        # card
        d.rectangle([x, y, x + card_w, y + card_h], fill=(252, 250, 245), outline=INK, width=2)
        # accent bar + glyph panel
        d.rectangle([x, y, x + card_w, y + 8], fill=col)
        draw_glyph(d, glyph, x + 96, y + 44, 56, col)
        # region kicker
        d.text((x + 16, y + 140), kicker, font=font(SANS_B, 15), fill=col)
        # headline
        yy = y + 170
        for line in headline.split("\n"):
            d.text((x + 16, yy), line, font=font(SERIF_B, 27), fill=INK)
            yy += 40
        # story index numeral
        d.text((x + card_w - 44, y + card_h - 42), f"{i+1}", font=font(SERIF_B, 28), fill=col)
    # footer
    d.rectangle([40, y0 + 2 * card_h + 2 * gap + 10, W - 40, y0 + 2 * card_h + 2 * gap + 12], fill=INK)
    d.text((40, H - 36), "Six stories that moved the world — selected from the day's reporting",
           font=font(SANS, 16), fill=(90, 90, 96))

    img.save(os.path.join(out, "entry.png"), "PNG", optimize=True)

if __name__ == "__main__":
    main()
