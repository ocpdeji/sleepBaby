"""
Mom Referral Card — "From One Exhausted Mom to Another"
"Sleep, Baby. Please." by Six & Thriving (2026)

A premium 1-page shareable referral card. Designed to be screenshotted,
texted to friends, and shared on social. Introduces the book in 60 seconds.

Run: python mom_referral_card.py
Requires: reportlab (pip install reportlab)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# === BRAND PALETTE ===
NAVY = HexColor("#0D1B3E")
GOLD = HexColor("#C9A84C")
CREAM = HexColor("#FAF7F2")
TEAL = HexColor("#2D8A8A")
SLATE = HexColor("#4A5568")
WHITE = HexColor("#FFFFFF")
SOFT_GRAY = HexColor("#E2E8F0")

# === PAGE SETUP ===
PAGE_W, PAGE_H = letter  # 612 x 792
MARGIN = 36
CONTENT_W = PAGE_W - 2 * MARGIN


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------
def draw_rounded_rect(c, x, y, w, h, radius=8, fill_color=None,
                      stroke_color=None, stroke_width=0.5):
    """Draw a rounded rectangle with optional fill and stroke."""
    c.saveState()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    if fill_color and stroke_color:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    else:
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()


def draw_wrapped_text(c, text, x, y, max_width, font_name, font_size,
                      color, line_height=None, leading_factor=1.25):
    """Draw text wrapped to max_width. Returns the y position after drawing."""
    if line_height is None:
        line_height = font_size * leading_factor
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    cur_y = y
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font_name, font_size) <= max_width:
            line = test
        else:
            if line:
                c.drawString(x, cur_y, line)
                cur_y -= line_height
            line = word
    if line:
        c.drawString(x, cur_y, line)
        cur_y -= line_height
    return cur_y


def draw_moon_icon(c, cx, cy, r, color):
    """Tiny crescent moon — for 'mom on Night 47' style bullets."""
    c.saveState()
    c.setFillColor(color)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.circle(cx + r * 0.45, cy + r * 0.15, r * 0.85, fill=1, stroke=0)
    c.restoreState()


def draw_heart_icon(c, cx, cy, size, color):
    """Tiny heart shape using two circles + a triangle."""
    c.saveState()
    c.setFillColor(color)
    r = size * 0.32
    # Two top lobes
    c.circle(cx - r * 0.85, cy + r * 0.15, r, fill=1, stroke=0)
    c.circle(cx + r * 0.85, cy + r * 0.15, r, fill=1, stroke=0)
    # Bottom triangle
    p = c.beginPath()
    p.moveTo(cx - size * 0.55, cy + r * 0.25)
    p.lineTo(cx + size * 0.55, cy + r * 0.25)
    p.lineTo(cx, cy - size * 0.55)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def draw_zzz_icon(c, cx, cy, size, color):
    """Three little Zs descending."""
    c.saveState()
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size * 1.1)
    c.drawString(cx - size * 0.6, cy - size * 0.1, "z")
    c.setFont("Helvetica-Bold", size * 0.85)
    c.drawString(cx - size * 0.05, cy + size * 0.15, "z")
    c.setFont("Helvetica-Bold", size * 0.65)
    c.drawString(cx + size * 0.4, cy + size * 0.4, "z")
    c.restoreState()


def draw_phone_icon(c, cx, cy, size, color):
    """Tiny phone outline — for the '2am googling' mom."""
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    w = size * 0.55
    h = size * 0.95
    c.roundRect(cx - w / 2, cy - h / 2, w, h, 2, fill=0, stroke=1)
    c.setLineWidth(1.2)
    # Speaker line at top
    c.line(cx - w * 0.18, cy + h * 0.38, cx + w * 0.18, cy + h * 0.38)
    # Home dot at bottom
    c.circle(cx, cy - h * 0.38, 1.1, fill=1, stroke=0)
    c.restoreState()


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------
def generate_referral_card():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "Mom_Referral_Card.pdf")

    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle("Mom Referral Card — Sleep, Baby. Please.")
    c.setAuthor("Six & Thriving")
    c.setSubject("Share this with another exhausted mom")

    # === CREAM BACKGROUND ===
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    y = PAGE_H

    # =========================================================
    # 1. HEADER BAR
    # =========================================================
    header_h = 38
    y -= header_h
    c.setFillColor(NAVY)
    c.rect(0, y, PAGE_W, header_h, fill=1, stroke=0)

    # Tiny gold square accent left of brand name
    c.setFillColor(GOLD)
    c.rect(MARGIN, y + header_h / 2 - 4, 8, 8, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 14, y + header_h / 2 - 4, "Sleep, Baby. Please.")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(PAGE_W - MARGIN, y + header_h / 2 - 3,
                      "FOR A FRIEND WHO NEEDS THIS")

    # Gold accent line
    y -= 3
    c.setFillColor(GOLD)
    c.rect(0, y, PAGE_W, 3, fill=1, stroke=0)

    # =========================================================
    # 2. TITLE & SUBTITLE
    # =========================================================
    y -= 32
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_W / 2, y, "From One Exhausted Mom")

    y -= 26
    c.drawCentredString(PAGE_W / 2, y, "to Another")

    # Decorative gold underline (centered)
    y -= 10
    line_w = 70
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(PAGE_W / 2 - line_w / 2, y, PAGE_W / 2 + line_w / 2, y)

    y -= 14
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawCentredString(
        PAGE_W / 2, y,
        "If you know a mom struggling with baby sleep \u2014 share this."
    )

    # =========================================================
    # 3. WHAT THIS BOOK IS — White card, gold border
    # =========================================================
    y -= 18
    card_h = 96
    card_y = y - card_h
    draw_rounded_rect(c, MARGIN, card_y, CONTENT_W, card_h, radius=10,
                      fill_color=WHITE, stroke_color=GOLD, stroke_width=1.5)

    # Section label inside the card
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 18, card_y + card_h - 18, "WHAT THIS BOOK IS")

    # Tiny gold accent under label
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MARGIN + 18, card_y + card_h - 22,
           MARGIN + 18 + 32, card_y + card_h - 22)

    bullets = [
        "Written by a real mom of 6 (including twins) \u2014 not a sleep clinic.",
        "The exact 7-night plan that worked for every one of her babies.",
        "Honest, warm, and addresses what nobody else does \u2014 Night 3, "
        "breastfeeding, twins, single parents.",
    ]

    bullet_y = card_y + card_h - 38
    for b in bullets:
        # Gold dot
        c.setFillColor(GOLD)
        c.circle(MARGIN + 22, bullet_y + 3, 2.2, fill=1, stroke=0)
        # Body text
        new_y = draw_wrapped_text(
            c, b, MARGIN + 32, bullet_y,
            CONTENT_W - 50, "Helvetica", 9.5, SLATE,
            line_height=12,
        )
        bullet_y = new_y - 3

    y = card_y - 14

    # =========================================================
    # 4. WHO IT'S FOR — Icon grid (2x2)
    # =========================================================
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "WHO IT'S FOR")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MARGIN, y - 4, MARGIN + 32, y - 4)

    y -= 14

    grid_h = 88
    grid_y = y - grid_h
    draw_rounded_rect(c, MARGIN, grid_y, CONTENT_W, grid_h, radius=10,
                      fill_color=WHITE, stroke_color=SOFT_GRAY,
                      stroke_width=0.8)

    # Faint gold left rail
    c.setFillColor(GOLD)
    c.rect(MARGIN, grid_y, 3, grid_h, fill=1, stroke=0)

    # 4 entries — 2 columns x 2 rows
    entries = [
        ("moon",  "The mom on Night 47 of 45-minute naps."),
        ("zzz",   "The mom whose baby will only sleep on her chest."),
        ("heart", "The mom who tried sleep training before and gave up."),
        ("phone", "The mom who's googling \u201cis it safe to sleep "
                  "standing up\u201d at 2am."),
    ]

    col_w = (CONTENT_W - 16) / 2
    row_h = grid_h / 2
    icon_pad = 22

    for i, (icon, text) in enumerate(entries):
        col = i % 2
        row = i // 2
        cx = MARGIN + 12 + col * (col_w + 4)
        cy_top = grid_y + grid_h - row * row_h
        center_y = cy_top - row_h / 2

        # Icon circle background
        ic_x = cx + 12
        ic_y = center_y
        c.setFillColor(CREAM)
        c.circle(ic_x, ic_y, 12, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.circle(ic_x, ic_y, 12, fill=0, stroke=1)

        if icon == "moon":
            draw_moon_icon(c, ic_x + 1, ic_y, 6, NAVY)
        elif icon == "heart":
            draw_heart_icon(c, ic_x, ic_y, 14, TEAL)
        elif icon == "zzz":
            draw_zzz_icon(c, ic_x - 4, ic_y - 3, 9, NAVY)
        elif icon == "phone":
            draw_phone_icon(c, ic_x, ic_y, 16, NAVY)

        # Text to the right of the icon
        text_x = ic_x + icon_pad
        text_top = center_y + 8
        draw_wrapped_text(
            c, text, text_x, text_top,
            col_w - icon_pad - 18, "Helvetica", 9, SLATE,
            line_height=11.5,
        )

    y = grid_y - 16

    # =========================================================
    # 5. WHAT MAKES IT DIFFERENT — 3 columns
    # =========================================================
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "WHAT MAKES IT DIFFERENT")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(MARGIN, y - 4, MARGIN + 32, y - 4)

    y -= 12

    diff_h = 100
    col_gap = 10
    col_count = 3
    col_w3 = (CONTENT_W - col_gap * (col_count - 1)) / col_count
    diff_y = y - diff_h

    columns = [
        ("THE 7-NIGHT PLAN",
         "Day-by-day what to expect \u2014 so you know it's working before "
         "it feels like it's working.",
         NAVY),
        ("THE EXTINCTION BURST",
         "Nobody talks about Night 3. We do. The night most parents quit \u2014 "
         "and why you shouldn't.",
         TEAL),
        ("BUILT FOR REAL FAMILIES",
         "Twins, NICU graduates, breastfeeding moms, single parents. "
         "Real life, real plans.",
         GOLD),
    ]

    for i, (title, body, accent) in enumerate(columns):
        cx = MARGIN + i * (col_w3 + col_gap)
        # Card
        draw_rounded_rect(c, cx, diff_y, col_w3, diff_h, radius=10,
                          fill_color=WHITE, stroke_color=SOFT_GRAY,
                          stroke_width=0.8)
        # Top accent strip
        c.setFillColor(accent)
        c.rect(cx, diff_y + diff_h - 5, col_w3, 5, fill=1, stroke=0)

        # Number badge
        num_r = 11
        num_cx = cx + 16
        num_cy = diff_y + diff_h - 22
        c.setFillColor(accent)
        c.circle(num_cx, num_cy, num_r, fill=1, stroke=0)
        c.setFillColor(WHITE if accent != GOLD else NAVY)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(num_cx, num_cy - 3.5, str(i + 1))

        # Title
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(cx + 32, num_cy - 3, title)

        # Body
        body_top = num_cy - num_r - 8
        draw_wrapped_text(
            c, body, cx + 12, body_top,
            col_w3 - 24, "Helvetica", 8.5, SLATE,
            line_height=11,
        )

    y = diff_y - 16

    # =========================================================
    # 6. CALL-TO-ACTION BOX (navy)
    # =========================================================
    cta_h = 102
    cta_y = y - cta_h
    draw_rounded_rect(c, MARGIN, cta_y, CONTENT_W, cta_h, radius=12,
                      fill_color=NAVY)

    # Gold corner accents
    c.setFillColor(GOLD)
    c.rect(MARGIN + 12, cta_y + cta_h - 16, 30, 3, fill=1, stroke=0)
    c.rect(PAGE_W - MARGIN - 42, cta_y + 13, 30, 3, fill=1, stroke=0)

    # Book title — large gold
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(PAGE_W / 2, cta_y + cta_h - 32,
                        "Sleep, Baby. Please.")

    # By Six & Thriving
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_W / 2, cta_y + cta_h - 48,
                        "By Six & Thriving")

    # Tiny separator
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W / 2 - 40, cta_y + cta_h - 56,
           PAGE_W / 2 + 40, cta_y + cta_h - 56)

    # URL — gold
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_W / 2, cta_y + cta_h - 72,
                        "sixandthriving.com")

    # Tag — cream
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(PAGE_W / 2, cta_y + cta_h - 88,
                        "Get the full guide and free tools.")

    y = cta_y - 14

    # =========================================================
    # 7. FOOTER
    # =========================================================
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)

    y -= 12
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(
        PAGE_W / 2, y,
        "Forwarded with love by a friend who's been there."
    )

    y -= 11
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(
        PAGE_W / 2, y,
        "Six & Thriving \u2022 Evidence-based parenting tools for the "
        "first 2,190 days"
    )

    # === SAVE ===
    c.save()
    print(f"\n\u2705 Referral card generated: {output_path}")
    print(f"   File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    generate_referral_card()
