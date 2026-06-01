import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

# ============================================================
#  SLEEP, BABY. PLEASE. — 7-Night Sleep Breakthrough Tracker
#  Six & Thriving  |  2026
#  ──────────────────────────────────────────────────────────
#  QUICK START
#  1. pip install reportlab
#  2. Edit TrackerConfig below — everything you need is here
#  3. python sleep_tracker.py
#  4. Open in GoodNotes, Notability, Adobe Acrobat, etc.
# ============================================================


class TrackerConfig:

    # ── Identity ──────────────────────────────────────────────
    BRAND_NAME      = "Six & Thriving"
    TRACKER_TITLE   = "7-Night Sleep Breakthrough Tracker"
    TRACKER_TAGLINE = "One week of data tells you more than six months of guessing."
    EBOOK_TITLE     = "Sleep, Baby. Please."
    TRACKER_YEAR    = 2026

    # ── Output filename ───────────────────────────────────────
    # Leave "" to auto-generate
    OUTPUT_FILENAME = ""

    # ── Page size (landscape iPad / tablet optimised) ─────────
    PAGE_WIDTH  = 1620
    PAGE_HEIGHT = 1215

    # ── Brand palette (from ebook) ────────────────────────────
    # warm cream #FAF6F1 · dark navy #1B2D4F · warm gold #C49A3C
    PALETTE = {
        "C_BG":        "#FAF6F1",   # warm cream background
        "C_NAVY":      "#1B2D4F",   # dark navy — primary ink
        "C_GOLD":      "#C49A3C",   # warm gold — accent
        "C_GOLD_SOFT": "#E8D5A3",   # pale gold — panel tint
        "C_CREAM":     "#F4EEE4",   # deeper cream — panel fill
        "C_CREAM2":    "#EDE5D8",   # card border / subtle divide
        "C_WHITE":     "#FFFFFF",
        "C_MUTED":     "#8A7B68",   # warm grey-brown for secondary text
        "C_BORDER":    "#D9CEBC",   # warm border
        "C_STAR":      "#F0C040",   # mood star fill
        "C_RED_SOFT":  "#E8B4A0",   # gentle coral for alerts
        "C_GREEN":     "#7BAE8A",   # soft green for positive indicators
        "C_NIGHT":     "#0D1B2E",   # very dark navy for cover
    }

    # ── Night labels ──────────────────────────────────────────
    NIGHT_LABELS = [
        "Night 1", "Night 2", "Night 3", "Night 4",
        "Night 5", "Night 6", "Night 7",
    ]

    # ── Nap labels ────────────────────────────────────────────
    NAP_SLOTS = ["Nap 1", "Nap 2", "Nap 3"]

    # ── Bedtime ritual checklist items ────────────────────────
    RITUAL_ITEMS = [
        "Dim lights",
        "Warm bath",
        "White noise on",
        "Feed / nurse",
        "Song / story",
        "Drowsy but awake",
    ]

    # ── Parent mood scale labels ──────────────────────────────
    MOOD_LABELS = ["Wrecked", "Rough", "Okay", "Good", "Thriving"]

    # ── Week-end reflection prompts ───────────────────────────
    REFLECTION_PROMPTS = [
        ("Pattern I Noticed",
         "What happened most nights? What changed by Night 7?"),
        ("What Worked",
         "Which ritual steps, timing, or responses made a difference?"),
        ("What to Adjust",
         "One thing I'll tweak going into next week:"),
        ("Win of the Week",
         "Even a small improvement counts. What was it?"),
    ]

    # ── Tips sidebar ─────────────────────────────────────────
    QUICK_TIPS = [
        ("Watch the Wake Window", "Track the time awake before bed — overtired = harder settle."),
        ("Same Ritual, Same Order", "Consistency cues the brain to expect sleep."),
        ("Drowsy But Awake", "Put down before fully asleep — they need to learn the last bit."),
        ("Night Wakings", "Wait 2 min before responding. They may re-settle."),
        ("Your Mood Matters", "A calmer parent = calmer baby. Track yours too."),
        ("Trust the Data", "7 nights reveals a pattern. Don't quit on Night 3."),
        ("Light Exposure", "Bright morning light + dark room at night resets the clock."),
    ]


# ════════════════════════════════════════════════════════════
#  RESOLVE CONFIG
# ════════════════════════════════════════════════════════════

cfg = TrackerConfig()
p   = cfg.PALETTE

def _hc(key):
    return HexColor(p[key])

C_BG        = _hc("C_BG")
C_NAVY      = _hc("C_NAVY")
C_GOLD      = _hc("C_GOLD")
C_GOLD_SOFT = _hc("C_GOLD_SOFT")
C_CREAM     = _hc("C_CREAM")
C_CREAM2    = _hc("C_CREAM2")
C_WHITE     = _hc("C_WHITE")
C_MUTED     = _hc("C_MUTED")
C_BORDER    = _hc("C_BORDER")
C_STAR      = _hc("C_STAR")
C_RED_SOFT  = _hc("C_RED_SOFT")
C_GREEN     = _hc("C_GREEN")
C_NIGHT     = _hc("C_NIGHT")
C_TRANSPARENT = Color(1, 1, 1, 0)

W  = cfg.PAGE_WIDTH
H  = cfg.PAGE_HEIGHT
MARGIN = 60


# ════════════════════════════════════════════════════════════
#  DRAWING PRIMITIVES  (mirror calm_mind_planner style)
# ════════════════════════════════════════════════════════════

def tf(c, name, x, y, w, h, value="", size=10, font="Helvetica",
       fill=None, border=None, style="underlined"):
    """Interactive AcroForm text field."""
    fill   = fill   if fill   is not None else C_TRANSPARENT
    border = border if border is not None else C_BORDER
    try:
        c.acroForm.textfield(
            name=name, value=value,
            fillColor=fill, borderColor=border,
            textColor=C_NAVY, borderWidth=0.8,
            borderStyle=style,
            width=w, height=h, x=x, y=y,
            tooltip="Tap to write",
            fontName=font, fontSize=size,
        )
    except Exception:
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.8)
        c.line(x, y + 2, x + w, y + 2)


def cb(c, name, x, y, size=16):
    """Interactive AcroForm checkbox."""
    try:
        c.acroForm.checkbox(
            name=name, checked=False,
            buttonStyle="check", shape="square",
            fillColor=C_WHITE, borderColor=C_GOLD,
            textColor=C_GOLD, borderWidth=1.4,
            borderStyle="solid", size=size, x=x, y=y,
            tooltip="Tap to check",
        )
    except Exception:
        c.setStrokeColor(C_GOLD)
        c.setLineWidth(1.4)
        c.setFillColor(C_WHITE)
        c.roundRect(x, y, size, size, 3, fill=1, stroke=1)


def txt(c, text, x, y, font="Helvetica", size=13, color=None, align="left"):
    color = color if color is not None else C_NAVY
    c.setFillColor(color)
    c.setFont(font, size)
    {"left": c.drawString,
     "right": c.drawRightString,
     "center": c.drawCentredString}[align](x, y, text)


def card(c, x, y, w, h, title="", bg=None, stroke=None, radius=12,
         title_color=None, title_size=14):
    bg          = bg          if bg          is not None else C_CREAM
    stroke      = stroke      if stroke      is not None else C_BORDER
    title_color = title_color if title_color is not None else C_NAVY
    c.setFillColor(bg)
    c.setStrokeColor(stroke)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    if title:
        c.setFillColor(title_color)
        c.setFont("Helvetica-Bold", title_size)
        c.drawString(x + 16, y + h - 28, title)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.7)
        c.line(x + 16, y + h - 36, x + w - 16, y + h - 36)


def draw_bg(c):
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def soft_rect(c, x, y, w, h, color, alpha=0.07, radius=8):
    c.setFillColor(Color(color.red, color.green, color.blue, alpha))
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)


def gold_bar(c, x, y, w, h=4, alpha=0.7):
    c.setFillColor(Color(C_GOLD.red, C_GOLD.green, C_GOLD.blue, alpha))
    c.roundRect(x, y, w, h, 2, fill=1, stroke=0)


def draw_moon_icon(c, cx, cy, r=14):
    """Simple crescent moon using two overlapping circles."""
    c.setFillColor(C_GOLD)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(C_BG)
    c.circle(cx + r * 0.5, cy + r * 0.15, r * 0.78, fill=1, stroke=0)


def draw_sun_icon(c, cx, cy, r=10):
    """Simple sun rays."""
    c.setFillColor(C_GOLD)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(2)
    import math
    for i in range(8):
        angle = math.radians(i * 45)
        x1 = cx + math.cos(angle) * (r + 3)
        y1 = cy + math.sin(angle) * (r + 3)
        x2 = cx + math.cos(angle) * (r + 9)
        y2 = cy + math.sin(angle) * (r + 9)
        c.line(x1, y1, x2, y2)


def draw_star(c, cx, cy, r=8, filled=True):
    """5-point star."""
    import math
    pts = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + math.cos(angle) * rr, cy + math.sin(angle) * rr))
    p_path = c.beginPath()
    p_path.moveTo(*pts[0])
    for pt in pts[1:]:
        p_path.lineTo(*pt)
    p_path.close()
    c.setFillColor(C_STAR if filled else C_BORDER)
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(0.6)
    c.drawPath(p_path, fill=1, stroke=1)


# ════════════════════════════════════════════════════════════
#  PAGE 1 — COVER
# ════════════════════════════════════════════════════════════

def draw_cover(c):
    # Deep navy background
    c.setFillColor(C_NIGHT)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Subtle cream texture strip left
    c.setFillColor(Color(C_GOLD.red, C_GOLD.green, C_GOLD.blue, 0.06))
    c.rect(0, 0, 320, H, fill=1, stroke=0)

    # Gold accent strip
    c.setFillColor(C_GOLD)
    c.rect(320, 0, 5, H, fill=1, stroke=0)

    # Decorative circles (stars / planets feel)
    for (cx_, cy_, r_, a_) in [
        (W - 140, H - 100, 220, 0.05),
        (W - 80,  H - 80,  90,  0.08),
        (180,     140,     160, 0.05),
        (260,     H - 60,  80,  0.06),
    ]:
        c.setFillColor(Color(C_GOLD.red, C_GOLD.green, C_GOLD.blue, a_))
        c.circle(cx_, cy_, r_, fill=1, stroke=0)

    # Moon icon centred
    draw_moon_icon(c, W // 2, H - 160, r=55)

    # Ebook title (small, above)
    txt(c, cfg.EBOOK_TITLE.upper(), W // 2, H - 250,
        "Helvetica", 14, C_GOLD, "center")

    # Tracker title
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 52)
    c.drawCentredString(W // 2, H - 330, cfg.TRACKER_TITLE)

    # Gold underline
    gold_bar(c, W // 2 - 280, H - 350, 560, 4)

    # Tagline
    txt(c, f'"{cfg.TRACKER_TAGLINE}"', W // 2, H - 400,
        "Helvetica-Oblique", 18, C_GOLD_SOFT, "center")

    # Description block
    desc_lines = [
        "Track wake times · Naps · Bedtime ritual · Night wakings · Parent mood",
        "Spot the pattern that breaks the exhaustion cycle.",
        "A companion tracker for Sleep, Baby. Please.",
    ]
    for i, line in enumerate(desc_lines):
        txt(c, line, W // 2, H - 470 - i * 36,
            "Helvetica", 15, Color(1, 1, 1, 0.65), "center")

    # What you track — pill chips
    chips = ["Wake Time", "Nap Log", "Bedtime Ritual", "Night Wakings", "Parent Mood"]
    chip_w = 180
    total_w = len(chips) * chip_w + (len(chips) - 1) * 16
    start_x = (W - total_w) // 2
    chip_y = H - 620
    for i, chip in enumerate(chips):
        cx_ = start_x + i * (chip_w + 16)
        c.setFillColor(Color(C_GOLD.red, C_GOLD.green, C_GOLD.blue, 0.18))
        c.setStrokeColor(C_GOLD)
        c.setLineWidth(1)
        c.roundRect(cx_, chip_y, chip_w, 34, 17, fill=1, stroke=1)
        txt(c, chip, cx_ + chip_w // 2, chip_y + 11,
            "Helvetica-Bold", 12, C_GOLD, "center")

    # Stars row
    for i in range(5):
        draw_star(c, W // 2 - 80 + i * 40, H - 690, r=10)

    # Brand footer
    txt(c, cfg.BRAND_NAME, W // 2, 80, "Helvetica-Bold", 16, C_GOLD, "center")
    txt(c, str(cfg.TRACKER_YEAR), W // 2, 56, "Helvetica", 12,
        Color(1, 1, 1, 0.4), "center")


# ════════════════════════════════════════════════════════════
#  PAGE 2 — HOW TO USE
# ════════════════════════════════════════════════════════════

def draw_how_to_use(c):
    draw_bg(c)

    # Header band
    c.setFillColor(C_NAVY)
    c.roundRect(MARGIN, H - 110, W - 2 * MARGIN, 72, 10, fill=1, stroke=0)
    txt(c, "How to Use This Tracker", MARGIN + 30, H - 80,
        "Helvetica-Bold", 22, C_WHITE)
    txt(c, cfg.BRAND_NAME + "  •  " + cfg.TRACKER_TITLE,
        W - MARGIN - 30, H - 80, "Helvetica", 13, C_GOLD_SOFT, "right")

    gold_bar(c, MARGIN, H - 116, W - 2 * MARGIN)

    # Steps
    steps = [
        ("1", "Start on Night 1", "Fill in your baby's actual bedtime, not the target. Honesty in the log = clarity in the pattern."),
        ("2", "Log wake time & naps", "Note morning wake time first. Then log each nap with start time, end time, and quality."),
        ("3", "Check the ritual", "After the bedtime routine, tick off which steps you completed. Consistency is the whole game."),
        ("4", "Track night wakings", "For each waking: time, how long, what you did, and whether it worked. No judgment — just data."),
        ("5", "Rate your mood", "Circle or tap your parent mood rating. Your state affects your baby's state. Track it."),
        ("6", "Read the pattern", "By Night 4 you'll see something. By Night 7 you'll know what to do next."),
    ]

    step_y = H - 160
    for i, (num, title, detail) in enumerate(steps):
        col = i % 2
        row = i // 2
        sx = MARGIN + col * ((W - 2 * MARGIN) // 2 + 10)
        sy = step_y - row * 145

        # Number circle
        c.setFillColor(C_GOLD)
        c.circle(sx + 28, sy - 28, 22, fill=1, stroke=0)
        txt(c, num, sx + 28, sy - 35, "Helvetica-Bold", 16, C_WHITE, "center")

        # Step content
        card(c, sx + 60, sy - 96, (W - 2 * MARGIN) // 2 - 75, 88,
             bg=C_CREAM, stroke=C_BORDER, radius=10)
        txt(c, title, sx + 76, sy - 48, "Helvetica-Bold", 13, C_NAVY)
        txt(c, detail, sx + 76, sy - 68, "Helvetica", 10, C_MUTED)
        # wrap second line if long
        if len(detail) > 70:
            split = detail[:70].rfind(" ")
            txt(c, detail[:split], sx + 76, sy - 68, "Helvetica", 10, C_MUTED)
            txt(c, detail[split+1:], sx + 76, sy - 82, "Helvetica", 10, C_MUTED)

    # Quick tips sidebar strip
    tip_x = MARGIN
    tip_y = H - 600
    card(c, tip_x, tip_y, W - 2 * MARGIN, 200, bg=C_CREAM, stroke=C_BORDER)

    txt(c, "Quick Reference Tips", tip_x + 20, tip_y + 178,
        "Helvetica-Bold", 14, C_NAVY)
    gold_bar(c, tip_x + 20, tip_y + 170, 220, 3)

    col_w = (W - 2 * MARGIN - 40) // 3
    for i, (tip_title, tip_body) in enumerate(cfg.QUICK_TIPS[:6]):
        col = i % 3
        row = i // 3
        tx = tip_x + 20 + col * (col_w + 10)
        ty = tip_y + 148 - row * 80
        soft_rect(c, tx, ty - 52, col_w, 66, C_GOLD, alpha=0.08)
        txt(c, tip_title, tx + 8, ty - 8, "Helvetica-Bold", 10, C_GOLD)
        txt(c, tip_body, tx + 8, ty - 26, "Helvetica", 9, C_MUTED)
        if len(tip_body) > 48:
            sp = tip_body[:48].rfind(" ")
            txt(c, tip_body[:sp], tx + 8, ty - 26, "Helvetica", 9, C_MUTED)
            txt(c, tip_body[sp+1:], tx + 8, ty - 38, "Helvetica", 9, C_MUTED)

    # Footer
    txt(c, f'{cfg.BRAND_NAME}  —  {cfg.EBOOK_TITLE}',
        W // 2, 36, "Helvetica-Oblique", 11, C_MUTED, "center")


# ════════════════════════════════════════════════════════════
#  PAGES 3–9 — NIGHT LOG (one per night)
# ════════════════════════════════════════════════════════════

def draw_night_log(c, night_index):
    night_label = cfg.NIGHT_LABELS[night_index]
    n = night_index + 1

    draw_bg(c)

    # ── Top header strip ──────────────────────────────────────
    c.setFillColor(C_NAVY)
    c.roundRect(MARGIN, H - 102, W - 2 * MARGIN, 64, 10, fill=1, stroke=0)

    # Moon icon
    draw_moon_icon(c, MARGIN + 44, H - 70, r=20)

    txt(c, night_label.upper(), MARGIN + 80, H - 65,
        "Helvetica-Bold", 24, C_WHITE)
    txt(c, cfg.TRACKER_TITLE, MARGIN + 80, H - 84,
        "Helvetica", 11, C_GOLD_SOFT)
    txt(c, f"Night {n} of 7", W - MARGIN - 30, H - 65,
        "Helvetica-Bold", 16, C_GOLD, "right")
    txt(c, "Date: _____ / _____ / _____", W - MARGIN - 30, H - 84,
        "Helvetica", 11, Color(1, 1, 1, 0.55), "right")

    gold_bar(c, MARGIN, H - 106, W - 2 * MARGIN)

    # ── LAYOUT constants ──────────────────────────────────────
    LEFT_W   = 560    # left column width
    RIGHT_W  = W - 2 * MARGIN - LEFT_W - 24
    LEFT_X   = MARGIN
    RIGHT_X  = MARGIN + LEFT_W + 24
    BODY_TOP = H - 126
    BODY_BOT = 80
    BODY_H   = BODY_TOP - BODY_BOT

    # ── LEFT COLUMN ───────────────────────────────────────────

    # 1. WAKE TIME card
    wt_h = 110
    wt_y = BODY_TOP - wt_h
    card(c, LEFT_X, wt_y, LEFT_W, wt_h, bg=C_WHITE, stroke=C_BORDER)
    draw_sun_icon(c, LEFT_X + 28, wt_y + wt_h - 36, r=14)
    txt(c, "Morning Wake Time", LEFT_X + 55, wt_y + wt_h - 28,
        "Helvetica-Bold", 13, C_NAVY)
    txt(c, "What time did baby wake for the day?",
        LEFT_X + 55, wt_y + wt_h - 44, "Helvetica", 10, C_MUTED)
    gold_bar(c, LEFT_X + 16, wt_y + wt_h - 52, LEFT_W - 32)

    txt(c, "Wake time:", LEFT_X + 20, wt_y + 66, "Helvetica", 11, C_MUTED)
    tf(c, f"n{n}_wake_time", LEFT_X + 100, wt_y + 52, 120, 24,
       size=13, font="Helvetica-Bold", style="solid",
       fill=C_CREAM, border=C_GOLD)
    txt(c, "Total sleep (hrs):", LEFT_X + 250, wt_y + 66, "Helvetica", 11, C_MUTED)
    tf(c, f"n{n}_total_sleep", LEFT_X + 380, wt_y + 52, 80, 24,
       size=13, font="Helvetica-Bold", style="solid",
       fill=C_CREAM, border=C_BORDER)

    txt(c, "Notes:", LEFT_X + 20, wt_y + 28, "Helvetica", 10, C_MUTED)
    tf(c, f"n{n}_wake_notes", LEFT_X + 70, wt_y + 14, LEFT_W - 90, 22,
       size=10, style="underlined")

    # 2. NAP LOG card
    nap_h = 200
    nap_y = wt_y - nap_h - 14
    card(c, LEFT_X, nap_y, LEFT_W, nap_h, bg=C_CREAM, stroke=C_BORDER)
    txt(c, "Nap Log", LEFT_X + 16, nap_y + nap_h - 22,
        "Helvetica-Bold", 13, C_NAVY)
    gold_bar(c, LEFT_X + 16, nap_y + nap_h - 32, LEFT_W - 32)

    # Column headers
    col_labels = ["", "Start", "End", "Duration", "Quality"]
    col_xs     = [LEFT_X + 16, LEFT_X + 90, LEFT_X + 200, LEFT_X + 310, LEFT_X + 420]
    for label, cx_ in zip(col_labels, col_xs):
        txt(c, label, cx_, nap_y + nap_h - 52,
            "Helvetica-Bold", 10, C_MUTED)

    for i, nap in enumerate(cfg.NAP_SLOTS):
        row_y = nap_y + nap_h - 90 - i * 48
        soft_rect(c, LEFT_X + 10, row_y - 6, LEFT_W - 20, 38, C_NAVY, alpha=0.03)
        txt(c, nap, LEFT_X + 16, row_y + 10, "Helvetica-Bold", 11, C_GOLD)
        tf(c, f"n{n}_nap{i+1}_start",    LEFT_X + 90,  row_y, 90, 26, size=10)
        tf(c, f"n{n}_nap{i+1}_end",      LEFT_X + 200, row_y, 90, 26, size=10)
        tf(c, f"n{n}_nap{i+1}_duration", LEFT_X + 310, row_y, 90, 26, size=10)
        # Quality: 3 small circles (Good / OK / Poor)
        for qi, (ql, qc) in enumerate([("G", C_GREEN), ("OK", C_GOLD), ("P", C_RED_SOFT)]):
            qx = LEFT_X + 420 + qi * 42
            c.setFillColor(C_WHITE)
            c.setStrokeColor(qc)
            c.setLineWidth(1.2)
            c.circle(qx + 14, row_y + 13, 14, fill=1, stroke=1)
            txt(c, ql, qx + 14, row_y + 8, "Helvetica-Bold", 8, qc, "center")

    # 3. BEDTIME RITUAL card
    rit_h = 198
    rit_y = nap_y - rit_h - 14
    card(c, LEFT_X, rit_y, LEFT_W, rit_h, bg=C_WHITE, stroke=C_BORDER)
    draw_moon_icon(c, LEFT_X + 28, rit_y + rit_h - 30, r=14)
    txt(c, "Bedtime Ritual Checklist", LEFT_X + 52, rit_y + rit_h - 22,
        "Helvetica-Bold", 13, C_NAVY)
    gold_bar(c, LEFT_X + 16, rit_y + rit_h - 36, LEFT_W - 32)

    txt(c, "Target bedtime:", LEFT_X + 20, rit_y + rit_h - 58,
        "Helvetica", 10, C_MUTED)
    tf(c, f"n{n}_target_bed", LEFT_X + 130, rit_y + rit_h - 72, 90, 24,
       size=11, style="solid", fill=C_CREAM, border=C_GOLD)
    txt(c, "Actual:", LEFT_X + 250, rit_y + rit_h - 58, "Helvetica", 10, C_MUTED)
    tf(c, f"n{n}_actual_bed", LEFT_X + 300, rit_y + rit_h - 72, 90, 24,
       size=11, style="solid", fill=C_CREAM, border=C_BORDER)

    # Ritual items — 2 columns
    half = len(cfg.RITUAL_ITEMS) // 2
    for i, item in enumerate(cfg.RITUAL_ITEMS):
        col  = i // half
        row  = i % half
        ix   = LEFT_X + 20 + col * 270
        iy   = rit_y + rit_h - 100 - row * 28
        cb(c, f"n{n}_ritual_{i}", ix, iy, size=16)
        txt(c, item, ix + 22, iy + 3, "Helvetica", 11, C_NAVY)

    # ── RIGHT COLUMN ──────────────────────────────────────────

    # 4. NIGHT WAKINGS card
    nw_h = 380
    nw_y = BODY_TOP - nw_h
    card(c, RIGHT_X, nw_y, RIGHT_W, nw_h, bg=C_CREAM, stroke=C_BORDER)
    txt(c, "Night Wakings Log", RIGHT_X + 16, nw_y + nw_h - 22,
        "Helvetica-Bold", 13, C_NAVY)
    gold_bar(c, RIGHT_X + 16, nw_y + nw_h - 32, RIGHT_W - 32)

    txt(c, "Log each waking below. Patterns will appear.",
        RIGHT_X + 16, nw_y + nw_h - 50, "Helvetica", 10, C_MUTED)

    # Waking headers
    nw_cols = ["#", "Time", "Duration", "Response", "Settled?"]
    nw_xs   = [RIGHT_X + 16, RIGHT_X + 58, RIGHT_X + 160, RIGHT_X + 275, RIGHT_X + 450]
    for label, cx_ in zip(nw_cols, nw_xs):
        txt(c, label, cx_, nw_y + nw_h - 70,
            "Helvetica-Bold", 10, C_MUTED)

    for row in range(5):
        ry = nw_y + nw_h - 110 - row * 52
        soft_rect(c, RIGHT_X + 10, ry - 8, RIGHT_W - 20, 44,
                  C_NAVY, alpha=0.03, radius=6)
        txt(c, str(row + 1), RIGHT_X + 28, ry + 12,
            "Helvetica-Bold", 11, C_GOLD, "center")
        tf(c, f"n{n}_nw{row+1}_time",     RIGHT_X + 58,  ry, 90, 28, size=10)
        tf(c, f"n{n}_nw{row+1}_duration", RIGHT_X + 160, ry, 100, 28, size=10)
        tf(c, f"n{n}_nw{row+1}_response", RIGHT_X + 275, ry, 165, 28, size=10)
        # Settled? Y/N mini choice
        for j, (lbl, col) in enumerate([("Y", C_GREEN), ("N", C_RED_SOFT)]):
            bx = RIGHT_X + 452 + j * 50
            c.setFillColor(C_WHITE)
            c.setStrokeColor(col)
            c.setLineWidth(1.2)
            c.roundRect(bx, ry + 2, 36, 24, 6, fill=1, stroke=1)
            txt(c, lbl, bx + 18, ry + 9, "Helvetica-Bold", 10, col, "center")

    txt(c, "Total wakings:", RIGHT_X + 16, nw_y + 18,
        "Helvetica", 10, C_MUTED)
    tf(c, f"n{n}_total_wakings", RIGHT_X + 120, nw_y + 8, 50, 24,
       size=12, style="solid", fill=C_CREAM, border=C_GOLD)
    txt(c, "Back to sleep in:", RIGHT_X + 200, nw_y + 18,
        "Helvetica", 10, C_MUTED)
    tf(c, f"n{n}_back_to_sleep", RIGHT_X + 330, nw_y + 8, 100, 24,
       size=12, style="solid", fill=C_CREAM, border=C_BORDER)
    txt(c, "min avg", RIGHT_X + 440, nw_y + 18, "Helvetica", 10, C_MUTED)

    # 5. PARENT MOOD card
    mood_h = 130
    mood_y = nw_y - mood_h - 14
    card(c, RIGHT_X, mood_y, RIGHT_W, mood_h, bg=C_WHITE, stroke=C_BORDER)
    txt(c, "Parent Mood & Energy", RIGHT_X + 16, mood_y + mood_h - 22,
        "Helvetica-Bold", 13, C_NAVY)
    gold_bar(c, RIGHT_X + 16, mood_y + mood_h - 32, RIGHT_W - 32)
    txt(c, "Circle your honest state this morning:",
        RIGHT_X + 16, mood_y + mood_h - 50, "Helvetica", 10, C_MUTED)

    mood_spacing = (RIGHT_W - 32) // len(cfg.MOOD_LABELS)
    for i, mood in enumerate(cfg.MOOD_LABELS):
        mx = RIGHT_X + 16 + i * mood_spacing + mood_spacing // 2
        my = mood_y + 50
        # Star rating = i+1 stars (display as dots for print friendliness)
        c.setFillColor(Color(C_GOLD.red, C_GOLD.green, C_GOLD.blue, 0.12))
        c.circle(mx, my, 30, fill=1, stroke=0)
        c.setStrokeColor(C_GOLD)
        c.setLineWidth(1.5)
        c.circle(mx, my, 30, fill=0, stroke=1)
        txt(c, str(i + 1), mx, my + 6, "Helvetica-Bold", 16, C_NAVY, "center")
        txt(c, mood, mx, my - 20, "Helvetica", 9, C_MUTED, "center")

    tf(c, f"n{n}_mood", RIGHT_X + 16, mood_y + 8, 60, 22,
       size=11, style="solid", fill=C_CREAM, border=C_GOLD)
    txt(c, "← write your number",
        RIGHT_X + 84, mood_y + 14, "Helvetica-Oblique", 9, C_MUTED)

    # 6. NOTES / OBSERVATIONS card
    notes_h = H - (BODY_TOP - nw_h - 14) - mood_h - 14 - 14 - BODY_BOT
    notes_y = BODY_BOT
    actual_notes_y = mood_y - notes_h - 14
    if actual_notes_y < BODY_BOT:
        actual_notes_y = BODY_BOT
        notes_h = mood_y - 14 - BODY_BOT

    card(c, RIGHT_X, actual_notes_y, RIGHT_W, notes_h,
         "Tonight's Observations", bg=C_CREAM, stroke=C_BORDER)
    txt(c, "What happened? What worked? What surprised you?",
        RIGHT_X + 16, actual_notes_y + notes_h - 54,
        "Helvetica-Oblique", 10, C_MUTED)

    usable_h = notes_h - 70
    lines = max(3, usable_h // 34)
    for li in range(lines):
        lf_y = actual_notes_y + notes_h - 74 - li * 34
        if lf_y < actual_notes_y + 12:
            break
        tf(c, f"n{n}_obs_{li}", RIGHT_X + 20, lf_y,
           RIGHT_W - 40, 26, size=11, style="underlined")

    # ── Bottom left — KEY METRIC CHIPS ────────────────────────
    # "Total Sleep | Bedtime | Wake Time" summary row
    chip_y = 30
    chips_data = [
        ("Total Night Sleep", f"n{n}_summary_sleep"),
        ("Bedtime",           f"n{n}_summary_bed"),
        ("Final Wake",        f"n{n}_summary_finalwake"),
        ("Wakings",           f"n{n}_summary_wakings"),
    ]
    chip_w = 124
    chip_gap = 14
    for i, (label, fname) in enumerate(chips_data):
        cx_ = LEFT_X + i * (chip_w + chip_gap)
        soft_rect(c, cx_, chip_y, chip_w, 44, C_NAVY, alpha=0.06)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.8)
        c.roundRect(cx_, chip_y, chip_w, 44, 6, fill=0, stroke=1)
        txt(c, label, cx_ + chip_w // 2, chip_y + 32,
            "Helvetica", 8, C_MUTED, "center")
        tf(c, fname, cx_ + 8, chip_y + 8, chip_w - 16, 20,
           size=10, style="solid", fill=C_TRANSPARENT, border=C_TRANSPARENT)

    # Page footer
    txt(c, f"{cfg.BRAND_NAME}  —  {night_label}  of  7",
        W // 2, 10, "Helvetica", 10, C_MUTED, "center")


# ════════════════════════════════════════════════════════════
#  PAGE 10 — PATTERN CHART (7-night overview)
# ════════════════════════════════════════════════════════════

def draw_pattern_chart(c):
    draw_bg(c)
    BODY_BOT = 80

    # Header
    c.setFillColor(C_NAVY)
    c.roundRect(MARGIN, H - 102, W - 2 * MARGIN, 64, 10, fill=1, stroke=0)
    txt(c, "7-Night Pattern Chart", MARGIN + 30, H - 65,
        "Helvetica-Bold", 22, C_WHITE)
    txt(c, "Your data at a glance — spot the trend",
        MARGIN + 30, H - 84, "Helvetica", 12, C_GOLD_SOFT)
    txt(c, cfg.BRAND_NAME, W - MARGIN - 30, H - 73,
        "Helvetica-Bold", 14, C_GOLD, "right")
    gold_bar(c, MARGIN, H - 106, W - 2 * MARGIN)

    # ── Summary table ──────────────────────────────────────────
    col_headers = ["", "Bedtime", "Wake Time", "Total Sleep", "# Wakings", "Mood (1-5)", "Key Note"]
    col_xs = [MARGIN + 10, MARGIN + 120, MARGIN + 280, MARGIN + 430, MARGIN + 580,
              MARGIN + 720, MARGIN + 860]
    col_ws = [100, 145, 135, 135, 125, 130, W - MARGIN - 870]

    table_top = H - 140
    row_h = 58

    # Header row
    c.setFillColor(C_NAVY)
    c.roundRect(MARGIN, table_top - 32, W - 2 * MARGIN, 32, 6, fill=1, stroke=0)
    for label, cx_ in zip(col_headers, col_xs):
        txt(c, label, cx_ + 4, table_top - 20,
            "Helvetica-Bold", 10, C_GOLD)

    # Night rows
    for i, night in enumerate(cfg.NIGHT_LABELS):
        n  = i + 1
        ry = table_top - 36 - i * row_h
        bg = C_WHITE if i % 2 == 0 else C_CREAM
        c.setFillColor(bg)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.7)
        c.roundRect(MARGIN, ry - row_h + 8, W - 2 * MARGIN, row_h, 4, fill=1, stroke=1)

        txt(c, night, col_xs[0] + 4, ry - row_h + 22,
            "Helvetica-Bold", 11, C_GOLD)
        tf(c, f"chart_n{n}_bedtime",    col_xs[1], ry - row_h + 18, 120, 24, size=11)
        tf(c, f"chart_n{n}_waketime",   col_xs[2], ry - row_h + 18, 120, 24, size=11)
        tf(c, f"chart_n{n}_totalsleep", col_xs[3], ry - row_h + 18, 110, 24, size=11)
        tf(c, f"chart_n{n}_wakings",    col_xs[4], ry - row_h + 18, 90,  24, size=11)

        # Mood stars 1-5
        for s in range(5):
            sx = col_xs[5] + s * 22
            draw_star(c, sx + 8, ry - row_h + 30, r=7, filled=False)
        txt(c, "→", col_xs[5] - 14, ry - row_h + 22, "Helvetica", 9, C_MUTED)

        tf(c, f"chart_n{n}_note", col_xs[6], ry - row_h + 18, col_ws[6] - 10, 24, size=10)

    # ── Trend visualiser (bar chart placeholder with fields) ──
    trend_y = table_top - 36 - 7 * row_h - 24
    card(c, MARGIN, BODY_BOT, W - 2 * MARGIN, trend_y - BODY_BOT,
         "Trend Snapshot", bg=C_CREAM, stroke=C_BORDER)

    trend_labels = [
        ("Total wakings going...", "down", C_GREEN, "UP", C_RED_SOFT),
        ("Bedtime consistency...", "consistent", C_GREEN, "shifting", C_GOLD),
        ("Total sleep trending...", "longer", C_GREEN, "shorter", C_RED_SOFT),
        ("Settle time...", "faster", C_GREEN, "slower", C_RED_SOFT),
    ]

    BODY_BOT_AREA = trend_y - BODY_BOT - 50
    item_h = BODY_BOT_AREA // len(trend_labels)

    for i, (label, pos_txt, pos_col, neg_txt, neg_col) in enumerate(trend_labels):
        iy = BODY_BOT + 20 + (len(trend_labels) - 1 - i) * item_h
        ix = MARGIN + 20

        soft_rect(c, ix, iy, W - 2 * MARGIN - 40, item_h - 8, C_NAVY, alpha=0.025)
        txt(c, label, ix + 12, iy + item_h - 28, "Helvetica", 11, C_NAVY)

        # Pos button
        pbx = ix + 380
        c.setFillColor(Color(pos_col.red, pos_col.green, pos_col.blue, 0.15))
        c.setStrokeColor(pos_col)
        c.setLineWidth(1.2)
        c.roundRect(pbx, iy + 6, 110, 28, 8, fill=1, stroke=1)
        txt(c, pos_txt.upper(), pbx + 55, iy + 15, "Helvetica-Bold", 10, pos_col, "center")

        nbx = pbx + 130
        c.setFillColor(Color(neg_col.red, neg_col.green, neg_col.blue, 0.15))
        c.setStrokeColor(neg_col)
        c.roundRect(nbx, iy + 6, 110, 28, 8, fill=1, stroke=1)
        txt(c, neg_txt.upper(), nbx + 55, iy + 15, "Helvetica-Bold", 10, neg_col, "center")

        txt(c, "→ Circle what matches your data",
            nbx + 130, iy + 15, "Helvetica-Oblique", 9, C_MUTED)

    txt(c, f"{cfg.BRAND_NAME}  —  7-Night Pattern Chart",
        W // 2, 10, "Helvetica", 10, C_MUTED, "center")


# ════════════════════════════════════════════════════════════
#  PAGE 11 — WEEK-END REFLECTION
# ════════════════════════════════════════════════════════════

def draw_reflection(c):
    draw_bg(c)

    c.setFillColor(C_NAVY)
    c.roundRect(MARGIN, H - 102, W - 2 * MARGIN, 64, 10, fill=1, stroke=0)
    txt(c, "Week-End Reflection", MARGIN + 30, H - 65,
        "Helvetica-Bold", 22, C_WHITE)
    txt(c, "What the data is telling you — and what to do next",
        MARGIN + 30, H - 84, "Helvetica", 12, C_GOLD_SOFT)
    gold_bar(c, MARGIN, H - 106, W - 2 * MARGIN)

    # Tagline banner
    soft_rect(c, MARGIN, H - 148, W - 2 * MARGIN, 36, C_GOLD, alpha=0.12)
    txt(c, f'"{cfg.TRACKER_TAGLINE}"',
        W // 2, H - 130, "Helvetica-Oblique", 16, C_NAVY, "center")

    # Reflection prompt cards — 2x2 grid
    prompt_w = (W - 2 * MARGIN - 24) // 2
    prompt_h = 210
    prompt_starts = [
        (MARGIN,              H - 190 - prompt_h),
        (MARGIN + prompt_w + 24, H - 190 - prompt_h),
        (MARGIN,              H - 190 - 2 * prompt_h - 24),
        (MARGIN + prompt_w + 24, H - 190 - 2 * prompt_h - 24),
    ]

    for i, (prompt_title, prompt_q) in enumerate(cfg.REFLECTION_PROMPTS):
        px, py = prompt_starts[i]
        card(c, px, py, prompt_w, prompt_h, bg=C_WHITE, stroke=C_BORDER)

        # Gold pill header
        c.setFillColor(C_GOLD)
        c.roundRect(px + 14, py + prompt_h - 38, 14, 14, 7, fill=1, stroke=0)
        txt(c, prompt_title, px + 36, py + prompt_h - 30,
            "Helvetica-Bold", 13, C_NAVY)
        gold_bar(c, px + 14, py + prompt_h - 44, prompt_w - 28)

        txt(c, prompt_q, px + 14, py + prompt_h - 64,
            "Helvetica-Oblique", 10, C_MUTED)

        lines = 4
        for li in range(lines):
            lf_y = py + prompt_h - 94 - li * 34
            if lf_y < py + 10:
                break
            tf(c, f"reflect_{i}_{li}", px + 14, lf_y,
               prompt_w - 28, 26, size=11, style="underlined")

    # Night-2-Week summary strip
    summary_y = H - 190 - 2 * prompt_h - 48 - 130
    if summary_y < 80:
        summary_y = 80
    card(c, MARGIN, summary_y, W - 2 * MARGIN, 110,
         "Your 7-Night Snapshot Numbers", bg=C_CREAM, stroke=C_BORDER)

    summary_fields = [
        "Best night (least wakings):",
        "Hardest night:",
        "Average bedtime:",
        "Average wake time:",
        "Avg nightly sleep:",
        "Avg parent mood:",
    ]
    field_w = (W - 2 * MARGIN - 32) // 3
    for i, label in enumerate(summary_fields):
        col = i % 3
        row = i // 3
        sx = MARGIN + 16 + col * (field_w + 8)
        sy = summary_y + 80 - row * 46
        txt(c, label, sx, sy, "Helvetica", 10, C_MUTED)
        tf(c, f"summary_{i}", sx, sy - 26, field_w - 8, 22,
           size=11, style="underlined")

    # Next week commitment
    commit_y = summary_y - 14 - 100
    if commit_y < 80:
        commit_y = 80
    card(c, MARGIN, commit_y, W - 2 * MARGIN, 100,
         "My Commitment Going Into Week 2", bg=C_NAVY, stroke=C_NAVY, radius=10,
         title_color=C_GOLD)
    txt(c, "One specific thing I will keep consistent:",
        MARGIN + 20, commit_y + 62, "Helvetica-Oblique", 11, C_GOLD_SOFT)
    tf(c, "commit_keep", MARGIN + 20, commit_y + 34, (W - 2 * MARGIN) // 2 - 30, 26,
       size=12, style="underlined", fill=C_TRANSPARENT,
       border=Color(C_GOLD_SOFT.red, C_GOLD_SOFT.green, C_GOLD_SOFT.blue, 0.5))
    txt(c, "One thing I will change:",
        MARGIN + (W - 2 * MARGIN) // 2 + 10, commit_y + 62,
        "Helvetica-Oblique", 11, C_GOLD_SOFT)
    tf(c, "commit_change",
       MARGIN + (W - 2 * MARGIN) // 2 + 10, commit_y + 34,
       (W - 2 * MARGIN) // 2 - 30, 26, size=12, style="underlined",
       fill=C_TRANSPARENT,
       border=Color(C_GOLD_SOFT.red, C_GOLD_SOFT.green, C_GOLD_SOFT.blue, 0.5))

    txt(c, f"{cfg.BRAND_NAME}  —  Sleep, Baby. Please.  —  Week 1 Complete",
        W // 2, 10, "Helvetica", 10, C_MUTED, "center")


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

def main():
    if cfg.OUTPUT_FILENAME.strip():
        out_path = cfg.OUTPUT_FILENAME.strip()
    else:
        out_path = "7_Night_Sleep_Breakthrough_Tracker.pdf"

    # Output to current dir; caller can move it
    print(f"\n{'='*60}")
    print(f"  {cfg.BRAND_NAME}")
    print(f"  {cfg.TRACKER_TITLE}")
    print(f"  Output: {out_path}")
    print(f"{'='*60}\n")

    cv = canvas.Canvas(out_path, pagesize=(W, H))
    cv.setTitle(f"{cfg.TRACKER_TITLE} — {cfg.BRAND_NAME}")
    cv.setAuthor(cfg.BRAND_NAME)
    cv.setSubject("Baby Sleep Tracking Companion for Sleep, Baby. Please.")
    cv.setKeywords("sleep tracker, baby sleep, six and thriving, sleep training")

    print("Generating Cover...")
    draw_cover(cv)
    cv.showPage()

    print("Generating How To Use...")
    draw_how_to_use(cv)
    cv.showPage()

    for i in range(7):
        print(f"Generating {cfg.NIGHT_LABELS[i]}...")
        draw_night_log(cv, i)
        cv.showPage()

    print("Generating Pattern Chart...")
    draw_pattern_chart(cv)
    cv.showPage()

    print("Generating Week-End Reflection...")
    draw_reflection(cv)
    cv.showPage()

    cv.save()
    print(f"\n✓ Done!  Saved: {out_path}")
    print(f"  Pages: 11  (Cover + How-To + 7 Night Logs + Chart + Reflection)\n")


if __name__ == "__main__":
    main()
