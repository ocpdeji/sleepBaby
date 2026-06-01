"""
Product Cover Image Generator
══════════════════════════════════════════════════════════════════
Creates a premium 1500x1500 cover image for each standalone Payhip product.

Outputs:
  cover_03_toddler_kit.png       — The Toddler Bedtime Survival Kit
  cover_04_exhausted_mum.png     — The Exhausted Mum's Survival Journal
  cover_05_newborn_kit.png       — The Newborn Sleep Starter Kit
  cover_06_seven_night_tracker.png — The 7-Night Sleep Tracker
  cover_07_self_care_cards.png   — Self-Care Ritual Cards
  cover_08_couple_sync.png       — Couple Sync Sleep Planner

Run: python generate_product_covers.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ── BRAND ────────────────────────────────────────────────────
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
GREEN_DK = "#276749"
PURPLE = "#553C9A"
AMBER = "#D69E2E"

W, H = 1500, 1500
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_font(size, bold=False, italic=False):
    if bold and italic:
        candidates = ["georgiaz.ttf", "arialbi.ttf"]
    elif bold:
        candidates = ["georgiab.ttf", "arialbd.ttf"]
    elif italic:
        candidates = ["georgiai.ttf", "ariali.ttf"]
    else:
        candidates = ["georgia.ttf", "arial.ttf"]
    for fn in candidates:
        try:
            return ImageFont.truetype(fn, size)
        except (OSError, IOError):
            try:
                return ImageFont.truetype(rf"C:\Windows\Fonts\{fn}", size)
            except (OSError, IOError):
                continue
    return ImageFont.load_default()


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered(draw, text, y, font, color, x_center=W // 2):
    w, _ = text_size(draw, text, font)
    draw.text((x_center - w // 2, y), text, font=font, fill=color)


def gold_bar(draw, x, y, w, h=4, color=GOLD):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=color)


def make_cover(filename, *, tag, title_lines, subtitle_lines, badge_text,
               accent_color=GOLD, dominant=NAVY):
    """Create a generic premium product cover.

    tag           — small uppercase label at top, gold (e.g. 'TODDLER EDITION')
    title_lines   — list of lines for the main title (italic last line)
    subtitle_lines— description below gold rule
    badge_text    — round badge text e.g. '$12'
    accent_color  — color for badge + accents (defaults gold)
    dominant      — background color
    """
    img = Image.new("RGB", (W, H), dominant)
    draw = ImageDraw.Draw(img)

    # Decorative circles
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o = ImageDraw.Draw(overlay)
    o.ellipse((W - 200, -200, W + 400, 400), fill=(30, 47, 85, 255))
    o.ellipse((-200, H - 350, 350, H + 100), fill=(22, 35, 71, 255))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Gold strips
    draw.rectangle((0, 0, W, 16), fill=GOLD)
    draw.rectangle((0, H - 16, W, H), fill=GOLD)

    # Price/value badge top-right
    bx, by, br = W - 200, 200, 130
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=GOLD)
    f_badge = get_font(58, bold=True)
    bw, _ = text_size(draw, badge_text, f_badge)
    draw.text((bx - bw // 2, by - 36), badge_text,
              font=f_badge, fill=NAVY)

    # Tag
    f_tag = get_font(28, bold=True)
    draw_centered(draw, tag.upper(), 220, f_tag, GOLD)

    # Decorative gold rule below tag
    gold_bar(draw, W // 2 - 140, 270, 280, 3)

    # Title — up to 3 lines, last in italic gold for contrast
    f_title = get_font(110, bold=True)
    f_title_i = get_font(110, bold=True, italic=True)

    title_y = 380
    for i, line in enumerate(title_lines):
        if i == len(title_lines) - 1:
            # Last line italic + gold
            draw_centered(draw, line, title_y, f_title_i, GOLD)
        else:
            draw_centered(draw, line, title_y, f_title, WHITE)
        title_y += 130

    # Diamond rule below title
    rule_y = title_y + 20
    gold_bar(draw, W // 2 - 100, rule_y, 200, 4)
    # Center diamond
    diamond_size = 14
    cx = W // 2
    cy = rule_y + 2
    draw.polygon(
        [(cx, cy - diamond_size), (cx + diamond_size, cy),
         (cx, cy + diamond_size), (cx - diamond_size, cy)],
        fill=GOLD,
    )

    # Subtitle — up to 3 lines
    f_sub = get_font(32, italic=True)
    sub_y = rule_y + 60
    for line in subtitle_lines:
        draw_centered(draw, line, sub_y, f_sub, GOLD_LITE)
        sub_y += 50

    # Author block at bottom
    gold_bar(draw, W // 2 - 200, 1280, 400, 3)
    f_brand = get_font(44, bold=True)
    draw_centered(draw, "SIX  &  THRIVING", 1310, f_brand, WHITE)
    f_brand_s = get_font(24, italic=True)
    draw_centered(draw, "Mother of Six — Including Twins",
                  1380, f_brand_s, GOLD_LITE)

    # Bottom URL
    f_url = get_font(22, bold=True)
    draw_centered(draw, "www.sixandthriving.com", 1450, f_url, GOLD)

    out = os.path.join(SCRIPT_DIR, filename)
    img.save(out, optimize=True)
    print(f"  ✓ {out}")


# ════════════════════════════════════════════════════════════
# THE 6 COVERS
# ════════════════════════════════════════════════════════════

def build_all():
    print()
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║  PRODUCT COVER GENERATOR — 6 covers           ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print()

    # 03 — Toddler Bedtime Survival Kit
    make_cover(
        "cover_03_toddler_kit.png",
        tag="TODDLER EDITION",
        title_lines=["The Toddler", "Bedtime", "Survival Kit"],
        subtitle_lines=[
            "For the parent of an 18-month-to-3-year-old",
            "who's discovered bedtime is 'negotiable.'",
        ],
        badge_text="$12",
    )

    # 04 — The Exhausted Mum's Survival Journal
    make_cover(
        "cover_04_exhausted_mum.png",
        tag="MUM SELF-CARE",
        title_lines=["The Exhausted", "Mum's", "Survival Journal"],
        subtitle_lines=[
            "Daily reset rituals, mindset prompts,",
            "and reminders that you are doing enough.",
        ],
        badge_text="$14",
    )

    # 05 — The Newborn Sleep Starter Kit
    make_cover(
        "cover_05_newborn_kit.png",
        tag="FIRST 8 WEEKS",
        title_lines=["The Newborn", "Sleep", "Starter Kit"],
        subtitle_lines=[
            "Realistic expectations, foundation habits,",
            "and the awake window tracker for weeks 0–8.",
        ],
        badge_text="$9",
    )

    # 06 — 7-Night Sleep Tracker
    make_cover(
        "cover_06_seven_night_tracker.png",
        tag="ACTION TOOL",
        title_lines=["The 7-Night", "Sleep", "Tracker"],
        subtitle_lines=[
            "Print it. Fill it in each morning.",
            "See the breakthrough by Day 4.",
        ],
        badge_text="$7",
    )

    # 07 — Self-Care Ritual Cards
    make_cover(
        "cover_07_self_care_cards.png",
        tag="MUM RECOVERY",
        title_lines=["Self-Care", "Ritual", "Cards"],
        subtitle_lines=[
            "30 printable rituals for the mum",
            "who's been pouring from an empty cup.",
        ],
        badge_text="$9",
    )

    # 08 — Couple Sync Sleep Planner
    make_cover(
        "cover_08_couple_sync.png",
        tag="FOR PARTNERS",
        title_lines=["The Couple", "Sync Sleep", "Planner"],
        subtitle_lines=[
            "Get on the same page in 60 seconds.",
            "Because consistency requires two people.",
        ],
        badge_text="$9",
    )

    print()
    print("  ✅ 6 covers generated.")
    print()


if __name__ == "__main__":
    build_all()
