"""
Payhip Product Image Generator
══════════════════════════════════════════════════════════════════
Generates 4 premium marketing images for the Payhip product page:

  1. payhip_01_bundle_stack.png       — "Look at all you get" mockup
  2. payhip_02_what_youll_get.png     — Feature grid with checkmarks
  3. payhip_03_who_its_for.png        — "This is for you if..."
  4. payhip_04_proof.png              — Author credibility / quote card

Run: python generate_payhip_images.py

Requires: Pillow (pip install Pillow)
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ── BRAND COLORS ─────────────────────────────────────────────
NAVY = "#0D1B3E"
NAVY_MID = "#162347"
NAVY_LITE = "#1E2F55"
GOLD = "#C9A84C"
GOLD_LITE = "#E8C97A"
CREAM = "#FAF7F2"
CREAM_MID = "#F0EBE1"
WHITE = "#FFFFFF"
TEAL = "#2D8A8A"
SLATE = "#4A5568"
SLATE_LITE = "#718096"
RUST = "#C0392B"
GOLD_RGBA = (201, 168, 76, 255)
NAVY_RGBA = (13, 27, 62, 255)

# ── CANVAS ───────────────────────────────────────────────────
W, H = 1500, 1500   # Square — perfect for Payhip / Etsy / Pinterest
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_font(size, bold=False, italic=False):
    """Try Georgia / Arial system fonts. Fall back to default."""
    candidates_bold = ["georgiab.ttf", "Georgia-Bold.ttf", "arialbd.ttf"]
    candidates_italic = ["georgiai.ttf", "ariali.ttf"]
    candidates_regular = ["georgia.ttf", "arial.ttf"]

    if bold and italic:
        candidates = ["georgiaz.ttf", "arialbi.ttf"] + candidates_bold
    elif bold:
        candidates = candidates_bold
    elif italic:
        candidates = candidates_italic
    else:
        candidates = candidates_regular

    for fn in candidates:
        try:
            return ImageFont.truetype(fn, size)
        except (OSError, IOError):
            continue
    # Try Windows full path
    for path in [
        r"C:\Windows\Fonts\georgiab.ttf",
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def text_size(draw, text, font):
    """Measure text dimensions."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered(draw, text, y, font, color, x_center=W // 2):
    w, _ = text_size(draw, text, font)
    draw.text((x_center - w // 2, y), text, font=font, fill=color)


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Pillow's rounded rect with optional outline."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def gold_bar(draw, x, y, w, h=4, color=GOLD):
    rounded_rect(draw, (x, y, x + w, y + h), radius=h // 2, fill=color)


# ════════════════════════════════════════════════════════════
# IMAGE 1 — BUNDLE STACK ("look at all you get")
# ════════════════════════════════════════════════════════════

def img_01_bundle_stack():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Decorative circles
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    o_draw.ellipse((W - 200, -200, W + 400, 400), fill=(30, 47, 85, 255))
    o_draw.ellipse((-200, H - 350, 350, H + 100), fill=(22, 35, 71, 255))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Gold top + bottom strips
    draw.rectangle((0, 0, W, 12), fill=GOLD)
    draw.rectangle((0, H - 12, W, H), fill=GOLD)

    # Top tag
    f_tag = get_font(28, bold=True)
    draw_centered(draw, "THE PREMIUM SLEEP BUNDLE", 80, f_tag, GOLD_LITE)

    # Big title
    f_title = get_font(110, bold=True)
    draw_centered(draw, "Everything", 160, f_title, WHITE)
    draw_centered(draw, "You Need.", 290, f_title, GOLD)

    # Gold rule
    gold_bar(draw, W // 2 - 100, 430, 200, 5)

    # Subtitle
    f_sub = get_font(36, italic=True)
    draw_centered(draw, "The book + 6 companion tools.", 470, f_sub, GOLD_LITE)
    draw_centered(draw, "One ZIP. One purchase. One sleeping baby.", 520, f_sub, GOLD_LITE)

    # ── BOOK STACK — center hero book + 6 fanned behind ────
    # Hero book (the eBook) — large in the center
    hero_w, hero_h = 380, 520
    hero_x = (W - hero_w) // 2
    hero_y = 620

    # Six smaller "companion tools" arranged 3-on-each-side, fanned
    side_w, side_h = 220, 300
    f_book_t = get_font(34, bold=True)
    f_book_s = get_font(20, bold=True)
    f_side_t = get_font(22, bold=True)

    # Companion books (left side, then right side)
    companions_left = [
        ("7-Night\nTracker", "#C5D8F5", NAVY),
        ("Routine\nBuilder", "#A8E0DD", NAVY),
        ("Six\nPersonalities", "#D6BFEF", NAVY),
    ]
    companions_right = [
        ("Reset\nProtocol", "#FBE5C2", NAVY),
        ("Mom\nReferral", "#F5C9C0", NAVY),
        ("Start Here\nGuide", CREAM_MID, NAVY),
    ]

    # Helper to draw a book card with shadow + spine + label
    def draw_book(cx, cy, bw, bh, fill_color, text_color, label,
                  rotation_offset=0, font_t=None):
        # Shadow first
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.rounded_rectangle((cx + 8, cy + 12, cx + bw + 8, cy + bh + 12),
                             radius=8, fill=(0, 0, 0, 100))
        nonlocal img
        img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
        d = ImageDraw.Draw(img)
        # Book body
        d.rounded_rectangle((cx, cy, cx + bw, cy + bh), radius=8, fill=fill_color)
        # Spine (dark line on left edge)
        d.rectangle((cx, cy, cx + 8, cy + bh), fill=NAVY)
        # Top accent bar
        accent = NAVY if fill_color != NAVY_LITE else GOLD
        d.rectangle((cx + 8, cy, cx + bw, cy + 8), fill=accent)
        # Label centered
        if font_t is None:
            font_t = f_side_t
        lines = label.split("\n")
        total_h = len(lines) * 28
        ly = cy + bh // 2 - total_h // 2
        for line in lines:
            lw, _ = text_size(d, line, font_t)
            d.text((cx + bw // 2 - lw // 2, ly), line,
                   font=font_t, fill=text_color)
            ly += 28
        return d

    # Left fan — 3 books stacked diagonally going up-right
    left_x_start = hero_x - 280
    for i, (label, fill, tc) in enumerate(companions_left):
        cx = left_x_start - i * 50
        cy = hero_y + 50 - i * 30
        draw = draw_book(cx, cy, side_w, side_h, fill, tc, label)

    # Right fan — 3 books stacked diagonally going up-left
    right_x_start = hero_x + hero_w + 60
    for i, (label, fill, tc) in enumerate(companions_right):
        cx = right_x_start + i * 50
        cy = hero_y + 50 - i * 30
        draw = draw_book(cx, cy, side_w, side_h, fill, tc, label)

    # Hero book LAST so it's on top
    # Shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((hero_x + 12, hero_y + 18, hero_x + hero_w + 12, hero_y + hero_h + 18),
                         radius=10, fill=(0, 0, 0, 130))
    img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
    draw = ImageDraw.Draw(img)
    # Hero body
    draw.rounded_rectangle((hero_x, hero_y, hero_x + hero_w, hero_y + hero_h),
                            radius=10, fill=NAVY_LITE)
    # Spine
    draw.rectangle((hero_x, hero_y, hero_x + 12, hero_y + hero_h), fill=NAVY)
    # Gold top accent
    draw.rectangle((hero_x + 12, hero_y, hero_x + hero_w, hero_y + 10), fill=GOLD)
    # Hero label
    f_hero_tag = get_font(20, bold=True)
    f_hero_title = get_font(46, bold=True)
    f_hero_sub = get_font(22, italic=True)
    # Inset content
    draw_centered(draw, "THE EBOOK", hero_y + 80, f_hero_tag, GOLD)
    # Wrap title on 3 lines
    title_y = hero_y + 180
    for line in ["Sleep,", "Baby.", "Please."]:
        draw_centered(draw, line, title_y, f_hero_title, WHITE)
        title_y += 56
    # Gold rule
    gold_bar(draw, hero_x + hero_w // 2 - 40, hero_y + 380, 80, 3)
    # Subtitle
    draw_centered(draw, "59 pages", hero_y + 410, f_hero_sub, GOLD_LITE)
    draw_centered(draw, "15 chapters", hero_y + 445, f_hero_sub, GOLD_LITE)

    # Bottom callout — price pill (more breathing room)
    rounded_rect(draw, (W // 2 - 380, 1330, W // 2 + 380, 1410),
                 radius=40, fill=GOLD)
    f_price = get_font(38, bold=True)
    draw_centered(draw, "INSTANT DOWNLOAD  •  $39", 1352, f_price, NAVY)

    # Author below price (with proper spacing from gold strip)
    f_brand = get_font(22, bold=True)
    draw_centered(draw, "SIX & THRIVING", 1455, f_brand, GOLD_LITE)

    out = os.path.join(SCRIPT_DIR, "payhip_01_bundle_stack.png")
    img.save(out, optimize=True)
    print(f"  ✓ {out}")


# ════════════════════════════════════════════════════════════
# IMAGE 2 — WHAT YOU'LL GET (feature grid)
# ════════════════════════════════════════════════════════════

def img_02_what_youll_get():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header band
    draw.rectangle((0, 0, W, 100), fill=NAVY)
    draw.rectangle((0, 100, W, 108), fill=GOLD)

    f_brand = get_font(28, bold=True)
    draw.text((60, 36), "Sleep, Baby. Please.", font=f_brand, fill=CREAM)
    f_brand_r = get_font(20, bold=True)
    text_w, _ = text_size(draw, "WHAT YOU'LL GET", f_brand_r)
    draw.text((W - text_w - 60, 40), "WHAT YOU'LL GET", font=f_brand_r, fill=GOLD)

    # Title
    f_title = get_font(76, bold=True)
    draw_centered(draw, "What You'll Get", 200, f_title, NAVY)

    # Subtitle
    f_sub = get_font(32, italic=True)
    draw_centered(draw, "7 premium files. Each one earns its place.", 310, f_sub, GOLD)
    gold_bar(draw, W // 2 - 80, 360, 160, 4)

    # 7 feature cards in 2 columns (4 left, 3 right)
    features = [
        ("01", "The Main eBook", "59 pages. 15 chapters. The full 7-night plan.", NAVY),
        ("02", "7-Night Sleep Tracker", "Fill it in each morning. See the wins by Day 4.", TEAL),
        ("03", "Bedtime Routine Builder", "Same routine every night. Stick it on the door.", "#553C9A"),
        ("04", "Six Sleep Personalities Kit", "Find YOUR baby's type in 5 minutes.", "#276749"),
        ("05", "Reset Protocol Worksheet", "For parents who tried before. Start here.", "#D69E2E"),
        ("06", "Mom Referral Card", "Share with a friend who needs this.", RUST),
        ("07", "Start Here Guide", "Tells you what to open first based on YOUR situation.", NAVY),
    ]

    # 2 columns, 4 rows on left, 3 rows on right
    col_x = [80, W // 2 + 20]
    card_w = (W // 2) - 100
    card_h = 200
    row_y_start = 410
    gap = 30

    f_num = get_font(38, bold=True)
    f_card_t = get_font(34, bold=True)
    f_card_s = get_font(22)

    for i, (num, title, sub, color) in enumerate(features):
        col = 0 if i < 4 else 1
        row = i if col == 0 else i - 4
        x = col_x[col]
        y = row_y_start + row * (card_h + gap)

        # Card bg
        rounded_rect(draw, (x, y, x + card_w, y + card_h), radius=18, fill=WHITE,
                     outline=CREAM_MID, width=2)
        # Color accent stripe (left edge)
        draw.rectangle((x, y, x + 8, y + card_h), fill=color)

        # Number badge
        bx, by = x + 60, y + 60
        draw.ellipse((bx - 35, by - 35, bx + 35, by + 35), fill=color)
        nw, _ = text_size(draw, num, f_num)
        draw.text((bx - nw // 2, by - 26), num, font=f_num, fill=WHITE)

        # Title
        draw.text((x + 110, y + 35), title, font=f_card_t, fill=NAVY)

        # Subtitle
        draw.text((x + 110, y + 100), sub, font=f_card_s, fill=SLATE)

    # Footer
    draw.rectangle((0, H - 80, W, H), fill=NAVY)
    f_foot = get_font(22)
    draw_centered(draw, "Six & Thriving  •  www.sixandthriving.com  •  $39 instant download",
                  H - 50, f_foot, GOLD_LITE)

    out = os.path.join(SCRIPT_DIR, "payhip_02_what_youll_get.png")
    img.save(out, optimize=True)
    print(f"  ✓ {out}")


# ════════════════════════════════════════════════════════════
# IMAGE 3 — WHO IT'S FOR (emotional connection)
# ════════════════════════════════════════════════════════════

def img_03_who_its_for():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Top navy band
    draw.rectangle((0, 0, W, 100), fill=NAVY)
    draw.rectangle((0, 100, W, 108), fill=GOLD)

    f_brand = get_font(28, bold=True)
    draw.text((60, 36), "Sleep, Baby. Please.", font=f_brand, fill=CREAM)
    f_brand_r = get_font(20, bold=True)
    text_w, _ = text_size(draw, "WHO IT'S FOR", f_brand_r)
    draw.text((W - text_w - 60, 40), "WHO IT'S FOR", font=f_brand_r, fill=GOLD)

    # Title
    f_title = get_font(80, bold=True)
    draw_centered(draw, "If you're reading", 220, f_title, NAVY)
    draw_centered(draw, "this at 2am...", 320, f_title, GOLD)

    # Sub
    f_sub = get_font(32, italic=True)
    draw_centered(draw, "this is for you.", 440, f_sub, SLATE)
    gold_bar(draw, W // 2 - 60, 490, 120, 4)

    # The 6 "you are" statements
    statements = [
        "You're on Night 47 of 45-minute naps",
        "Your baby will only sleep on your chest",
        "You tried sleep training before — and gave up on Night 3",
        "You're breastfeeding and everyone says you'll never sleep again",
        "You have twins and every guide pretends you don't exist",
        'You\'ve Googled "is it safe to sleep standing up"',
    ]

    f_stmt = get_font(30)
    f_check = get_font(40, bold=True)
    y = 580
    line_h = 90

    for stmt in statements:
        # Check icon — gold circle with check
        cx_icon = 180
        cy_icon = y + 18
        draw.ellipse((cx_icon - 25, cy_icon - 25, cx_icon + 25, cy_icon + 25),
                     fill=GOLD)
        # Draw a simple checkmark
        draw.line(
            [(cx_icon - 12, cy_icon + 2), (cx_icon - 4, cy_icon + 12),
             (cx_icon + 13, cy_icon - 10)],
            fill=NAVY, width=5,
        )
        # Statement
        draw.text((230, y), stmt, font=f_stmt, fill=NAVY)
        y += line_h

    # CTA box at bottom
    rounded_rect(draw, (100, 1230, W - 100, 1380), radius=24, fill=NAVY)
    f_cta = get_font(40, bold=True)
    draw_centered(draw, "I see you. I've been there. Six times.",
                  1255, f_cta, GOLD)
    f_cta_sub = get_font(26, italic=True)
    draw_centered(draw, "— Six & Thriving, mother of six (including twins)",
                  1320, f_cta_sub, GOLD_LITE)

    # Footer
    draw.rectangle((0, H - 80, W, H), fill=NAVY)
    f_foot = get_font(22)
    draw_centered(draw, "Sleep is coming. For both of you.",
                  H - 50, f_foot, GOLD_LITE)

    out = os.path.join(SCRIPT_DIR, "payhip_03_who_its_for.png")
    img.save(out, optimize=True)
    print(f"  ✓ {out}")


# ════════════════════════════════════════════════════════════
# IMAGE 4 — PROOF / AUTHOR CREDIBILITY
# ════════════════════════════════════════════════════════════

def img_04_proof():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Decorative
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    o_draw.ellipse((W - 250, -250, W + 350, 350), fill=(30, 47, 85, 255))
    o_draw.ellipse((-300, H - 300, 300, H + 200), fill=(22, 35, 71, 255))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Gold strips
    draw.rectangle((0, 0, W, 12), fill=GOLD)
    draw.rectangle((0, H - 12, W, H), fill=GOLD)

    # Top tag
    f_tag = get_font(28, bold=True)
    draw_centered(draw, "WRITTEN BY A MOM WHO LIVED IT", 100, f_tag, GOLD_LITE)
    gold_bar(draw, W // 2 - 200, 150, 400, 4)

    # Stats row — 3 big numbers
    stats = [
        ("6", "Babies", "Including a set of twins"),
        ("10+", "Years", "In the trenches of infant sleep"),
        ("100%", "Success", "Every one of mine learned to sleep"),
    ]

    f_num = get_font(180, bold=True)
    f_unit = get_font(32, bold=True)
    f_desc = get_font(24)

    col_w = W // 3
    for i, (num, unit, desc) in enumerate(stats):
        cx = col_w * i + col_w // 2
        # Number
        nw, _ = text_size(draw, num, f_num)
        draw.text((cx - nw // 2, 230), num, font=f_num, fill=GOLD)
        # Unit
        uw, _ = text_size(draw, unit, f_unit)
        draw.text((cx - uw // 2, 460), unit.upper(), font=f_unit, fill=WHITE)
        # Description
        dw, _ = text_size(draw, desc, f_desc)
        draw.text((cx - dw // 2, 510), desc, font=f_desc, fill=GOLD_LITE)

    # Big quote
    f_quote = get_font(52, bold=True, italic=True)
    quote_lines = [
        '"Every single one of my babies',
        'learned to sleep.',
        'Every single one."',
    ]
    qy = 700
    for line in quote_lines:
        draw_centered(draw, line, qy, f_quote, WHITE)
        qy += 70

    # Attribution
    f_attr = get_font(28, italic=True)
    draw_centered(draw, "— Six & Thriving", 920, f_attr, GOLD)

    # Bottom badge
    rounded_rect(draw, (W // 2 - 400, 1100, W // 2 + 400, 1280),
                 radius=24, fill=CREAM)
    f_promise_t = get_font(40, bold=True)
    draw_centered(draw, "30-Day Money-Back Guarantee", 1130, f_promise_t, NAVY)
    f_promise_s = get_font(24)
    draw_centered(draw, "If it doesn't work, email me. Full refund. No questions.",
                  1190, f_promise_s, SLATE)
    f_brand_p = get_font(20, bold=True)
    draw_centered(draw, "www.sixandthriving.com", 1230, f_brand_p, GOLD)

    # Footer
    f_foot = get_font(22)
    draw_centered(draw, "Sleep is coming. For both of you.",
                  H - 60, f_foot, GOLD_LITE)

    out = os.path.join(SCRIPT_DIR, "payhip_04_proof.png")
    img.save(out, optimize=True)
    print(f"  ✓ {out}")


# ════════════════════════════════════════════════════════════
# BUILD ALL
# ════════════════════════════════════════════════════════════

def build():
    print()
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║  PAYHIP PRODUCT IMAGE GENERATOR               ║")
    print("  ║  Six & Thriving | 2026                        ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print()
    print("  Generating 4 marketing images for Payhip...\n")

    img_01_bundle_stack()
    img_02_what_youll_get()
    img_03_who_its_for()
    img_04_proof()

    print()
    print("  ✅ All 4 images generated.")
    print()
    print("  📋 UPLOAD ORDER ON PAYHIP:")
    print("     1. Your existing cover JPG (the navy/gold cover image)")
    print("     2. payhip_01_bundle_stack.png    — what you get visualization")
    print("     3. payhip_02_what_youll_get.png  — feature breakdown")
    print("     4. payhip_03_who_its_for.png     — emotional connection")
    print("     5. payhip_04_proof.png           — author credibility + guarantee")
    print()


if __name__ == "__main__":
    build()
