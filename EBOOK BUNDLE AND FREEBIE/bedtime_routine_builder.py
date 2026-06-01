"""
╔══════════════════════════════════════════════════════════════════╗
║   BEDTIME ROUTINE BUILDER PAD  —  Sleep, Baby. Please.          ║
║   Based on the Six & Thriving ebook bedtime checklist system     ║
║   Premium fillable PDF · Interactive fields · Nursery-ready      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import math
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.pagesizes import letter

# ============================================================
#  CONFIG
# ============================================================
OUTPUT_FILENAME = "Bedtime_Routine_Builder_Pad.pdf"

W, H = letter  # 612 × 792 pt  — standard US Letter (portrait)

# ── Palette: warm navy / gold / cream ─────────────────────
NAVY    = HexColor("#1A2E4A")
NAVY2   = HexColor("#243D60")
GOLD    = HexColor("#C9963A")
GOLD2   = HexColor("#E8B96A")
CREAM   = HexColor("#FFF8EE")
CREAM2  = HexColor("#FFF1D6")
BLUSH   = HexColor("#FAE8D8")
ROSE    = HexColor("#D4756A")
SAGE    = HexColor("#6B9E8A")
SAGE2   = HexColor("#A8CCBE")
SILVER  = HexColor("#B8C4CC")
INK     = HexColor("#1A1A2E")
MUTED   = HexColor("#7A8CA0")
BORDER  = HexColor("#D9C9B4")
PANEL   = HexColor("#FEFBF6")
CTRANS  = Color(1, 1, 1, 0)

STAR    = "★"
MOON    = "☽"
ZZZ     = "z"

CHECKLIST_ITEMS = [
    ("transition",  "Transition signal given",          "e.g. 'lights are going dim, sleep time soon'"),
    ("screens",     "Screens & stimulation off",         "TV, tablets, bright lights — all off"),
    ("bath",        "Bath or warm wipe-down",            "Warm water relaxes the nervous system"),
    ("lotion",      "Lotion massage",                    "Optional but calming — lavender works beautifully"),
    ("pyjamas",     "Pyjamas & sleep sack on",           "Check tog rating for room temperature"),
    ("feed",        "Feed given (not to sleep)",         "Dim, quiet room — drowsy is the goal, not asleep"),
    ("books",       "1–3 books or songs",                "Rocking chair / glider; keep it soft and slow"),
    ("phrase",      "Final goodnight phrase said",       "Same words every night — baby learns the cue"),
    ("whitenoise",  "White noise turned on",             "Continuous, low level — not inside the crib"),
    ("dark",        "Room fully dark",                   "Blackout curtains + cover monitor LEDs"),
    ("crib",        "Baby placed in crib DROWSY but AWAKE", "The single most important skill in this book"),
    ("exit",        "Parent exits calmly & consistently","Same every night — consistency is the magic"),
]

SAFE_SLEEP = [
    "Firm, flat mattress · fitted sheet only",
    "No loose blankets, bumpers, or stuffed animals",
    "Baby on back · every sleep · every time",
    "Room temp 68–72°F / 20–22°C",
    "True blackout achieved",
]

AWAKE_WINDOWS = [
    ("0–6 wks",    "45–60 min",  "4–5/day", "Variable"),
    ("6–12 wks",   "60–90 min",  "4/day",   "8–9 pm"),
    ("3–4 mo",     "90 min",     "3–4/day", "7:30–8:30 pm"),
    ("4–6 mo",     "2 hrs",      "3/day",   "7–8 pm"),
    ("6–8 mo",     "2.5 hrs",    "2–3/day", "7–8 pm"),
    ("8–12 mo",    "3–3.5 hrs",  "2/day",   "6:30–7:30 pm"),
    ("12–18 mo",   "4–5 hrs",    "1–2/day", "7–7:30 pm"),
    ("18–24 mo",   "5–6 hrs",    "1/day",   "7–7:30 pm"),
]

# ============================================================
#  DRAWING PRIMITIVES
# ============================================================

def bg(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def card(c, x, y, w, h, fill=PANEL, stroke=BORDER, radius=8, lw=0.8):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def txt(c, text, x, y, font="Helvetica", size=11, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, text)
    elif align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)


def accent_bar(c, x, y, w, h=3, color=GOLD):
    c.setFillColor(color)
    c.setStrokeColor(CTRANS)
    c.roundRect(x, y, w, h, 1.5, fill=1, stroke=0)


def star_row(c, x, y, count=5, size=9, color=GOLD2):
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    for i in range(count):
        c.drawString(x + i * (size + 3), y, STAR)


def moon_deco(c, x, y, size=18, color=NAVY):
    """Draw a crescent moon decoration."""
    c.setFillColor(color)
    c.setFont("ZapfDingbats", size)
    # Use circle approach for crescent
    c.setFillColor(color)
    c.circle(x, y, size * 0.5, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.circle(x + size * 0.18, y + size * 0.08, size * 0.42, fill=1, stroke=0)


def draw_checkbox(c, name, x, y, size=14, checked=False):
    """Draw a styled interactive checkbox."""
    # Shadow
    c.setFillColor(HexColor("#C9963A30"))
    c.roundRect(x + 1, y - 1, size, size, 3, fill=1, stroke=0)
    # Box
    c.setFillColor(PANEL)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.roundRect(x, y, size, size, 3, fill=1, stroke=1)
    # Interactive field
    from reportlab.pdfbase.pdfdoc import PDFName
    c.acroForm.checkbox(
        name=name,
        tooltip=name.replace("_", " ").title(),
        x=x, y=y,
        size=size,
        buttonStyle="check",
        borderColor=NAVY,
        fillColor=PANEL,
        textColor=GOLD,
        forceBorder=True,
    )


def draw_textfield(c, name, x, y, w, h, size=11, tooltip="", placeholder="",
                   bg_color=None, border_color=None, multiline=False):
    """Draw a styled interactive text field."""
    bg_c = bg_color or PANEL
    bc   = border_color or BORDER

    # Subtle field background
    c.setFillColor(bg_c)
    c.setStrokeColor(bc)
    c.setLineWidth(0.6)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)

    flags = "multiline" if multiline else ""
    c.acroForm.textfield(
        name=name,
        tooltip=tooltip or name.replace("_", " ").title(),
        x=x + 2, y=y + 2,
        width=w - 4,
        height=h - 4,
        fontSize=size,
        textColor=INK,
        fillColor=bg_c,
        borderColor=bc,
        borderWidth=0,
        value=placeholder,
        forceBorder=False,
        fieldFlags=flags,
    )


def draw_radio(c, group, value, x, y, size=13):
    """Draw a styled radio button."""
    c.setFillColor(PANEL)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.circle(x + size / 2, y + size / 2, size / 2, fill=1, stroke=1)
    c.acroForm.radio(
        name=group,
        tooltip=value,
        value=value,
        x=x, y=y,
        size=size,
        buttonStyle="circle",
        borderColor=NAVY,
        fillColor=PANEL,
        textColor=GOLD,
        forceBorder=True,
    )


def section_divider(c, y, label="", color=NAVY):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.line(36, y, W - 36, y)
    if label:
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(W / 2, y + 3, f"  {label}  ")


def dotted_line(c, x1, y, x2, dash=3, gap=4, color=BORDER):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.setDash(dash, gap)
    c.line(x1, y, x2, y)
    c.setDash()


# ============================================================
#  PAGE 1  —  COVER
# ============================================================

def draw_cover(c):
    c.bookmarkPage("cover")
    bg(c)

    # Full bleed header block
    c.setFillColor(NAVY)
    c.rect(0, H - 200, W, 200, fill=1, stroke=0)

    # Decorative arch / wave
    p = c.beginPath()
    p.moveTo(0, H - 200)
    p.curveTo(W * 0.25, H - 175, W * 0.75, H - 225, W, H - 200)
    p.lineTo(W, H - 200)
    p.lineTo(0, H - 200)
    p.close()
    c.setFillColor(NAVY2)
    c.drawPath(p, fill=1, stroke=0)

    # Stars sprinkled in header
    for sx, sy in [(50, H-50), (120, H-30), (200, H-70), (280, H-20),
                   (380, H-55), (450, H-25), (530, H-65), (580, H-40)]:
        c.setFillColor(GOLD2)
        c.setFont("Helvetica", 8)
        c.drawString(sx, sy, STAR)

    # Brand pill
    pill_w, pill_h = 200, 28
    pill_x = (W - pill_w) / 2
    c.setFillColor(GOLD)
    c.roundRect(pill_x, H - 52, pill_w, pill_h, 14, fill=1, stroke=0)
    txt(c, "SLEEP, BABY. PLEASE.", W / 2, H - 33, "Helvetica-Bold", 10, NAVY, "center")

    # Main title
    txt(c, "Bedtime Routine", W / 2, H - 95, "Helvetica-Bold", 38, CREAM, "center")
    txt(c, "Builder Pad", W / 2, H - 135, "Helvetica-Bold", 38, GOLD, "center")

    # Tagline
    txt(c, "Stick it on the nursery door.", W / 2, H - 170,
        "Helvetica-Oblique", 13, CREAM2, "center")
    txt(c, "Your 2am brain will thank you.", W / 2, H - 188,
        "Helvetica-Oblique", 13, SAGE2, "center")

    # Moon decoration
    moon_deco(c, 52, H - 145, 30, GOLD2)
    moon_deco(c, W - 52, H - 145, 30, GOLD2)

    # ── Baby name / date card ──────────────────────────────
    card(c, 36, H - 310, W - 72, 90, fill=CREAM2, stroke=GOLD, radius=10, lw=1.5)
    txt(c, "TONIGHT'S PAD", 56, H - 230, "Helvetica-Bold", 9, GOLD)
    accent_bar(c, 56, H - 238, 120, color=GOLD)

    col1 = 56
    col2 = W / 2 + 20
    field_h = 24

    txt(c, "Baby's Name:", col1, H - 262, "Helvetica-Bold", 10, MUTED)
    draw_textfield(c, "cover_baby_name", col1 + 88, H - 270, 165, field_h,
                   size=12, tooltip="Baby's name", bg_color=CREAM)

    txt(c, "Date:", col2, H - 262, "Helvetica-Bold", 10, MUTED)
    draw_textfield(c, "cover_date", col2 + 38, H - 270,
                   W - col2 - 52 - 38, field_h, size=12,
                   tooltip="Tonight's date", placeholder=datetime.date.today().strftime("%B %d, %Y"),
                   bg_color=CREAM)

    txt(c, "Baby's Age:", col1, H - 296, "Helvetica-Bold", 10, MUTED)
    draw_textfield(c, "cover_age", col1 + 83, H - 304, 100, field_h,
                   size=12, tooltip="Age in weeks/months", bg_color=CREAM)

    txt(c, "Awake Window:", col2, H - 296, "Helvetica-Bold", 10, MUTED)
    draw_textfield(c, "cover_awake_window", col2 + 108, H - 304,
                   W - col2 - 52 - 108, field_h, size=12,
                   tooltip="Max awake time before bed", bg_color=CREAM)

    # ── Awake Window quick ref ─────────────────────────────
    card(c, 36, H - 460, W - 72, 130, fill=NAVY, stroke=NAVY, radius=10)
    txt(c, "⏱  AWAKE WINDOW QUICK REFERENCE", W / 2, H - 348,
        "Helvetica-Bold", 11, GOLD, "center")
    accent_bar(c, (W - 200) / 2, H - 356, 200, color=GOLD2)

    cols = [("AGE", 0.08), ("AWAKE", 0.25), ("NAPS", 0.47), ("BEDTIME", 0.65)]
    col_xs = [36 + (W - 72) * f for _, f in cols]
    for i, (label, _) in enumerate(cols):
        txt(c, label, col_xs[i] + 4, H - 373, "Helvetica-Bold", 8, GOLD)

    row_h = 10.5
    for ri, (age, aw, naps, bt) in enumerate(AWAKE_WINDOWS):
        ry = H - 387 - ri * row_h
        if ri % 2 == 0:
            c.setFillColor(HexColor("#FFFFFF18"))
            c.roundRect(38, ry - 1, W - 76, row_h, 2, fill=1, stroke=0)
        row_data = [age, aw, naps, bt]
        for ci, val in enumerate(row_data):
            color = CREAM2 if ci == 0 else SILVER
            txt(c, val, col_xs[ci] + 4, ry + 1, "Helvetica", 8, color)

    # ── Tonight's method selector ──────────────────────────
    card(c, 36, H - 570, W - 72, 90, fill=BLUSH, stroke=ROSE, radius=8, lw=1)
    txt(c, "TONIGHT'S RESPONSE METHOD", 56, H - 490,
        "Helvetica-Bold", 10, NAVY)
    txt(c, "Decide before night falls — your 2pm brain makes better decisions than your 2am brain.",
        56, H - 505, "Helvetica-Oblique", 8, MUTED)

    methods = ["Ferber", "Chair", "Fading", "CIO", "Pick Up/Put Down", "Our Own Plan"]
    mx = 56
    for mi, method in enumerate(methods):
        draw_radio(c, "tonight_method", method, mx, H - 542, 12)
        txt(c, method, mx + 17, H - 539, "Helvetica", 9, INK)
        mx += 90 if mi < 2 else 85
        if mi == 2:
            mx = 56
            break
    # second row
    mx = 56
    for mi, method in enumerate(methods[3:]):
        draw_radio(c, "tonight_method", method, mx, H - 558, 12)
        txt(c, method, mx + 17, H - 555, "Helvetica", 9, INK)
        mx += 105

    # ── Page nav footer ────────────────────────────────────
    pages = [("Cover & Setup", "cover"), ("Tonight's Routine", "routine"),
             ("Night Log", "log"), ("Safe Sleep", "safe"), ("Notes", "notes")]
    nav_y = 30
    nav_w = (W - 72) / len(pages)
    for pi, (label, anchor) in enumerate(pages):
        nx = 36 + pi * nav_w
        is_first = pi == 0
        c.setFillColor(NAVY if is_first else CREAM2)
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.8)
        c.roundRect(nx + 2, nav_y, nav_w - 4, 22, 4, fill=1, stroke=1)
        txt(c, label, nx + nav_w / 2, nav_y + 7,
            "Helvetica-Bold" if is_first else "Helvetica",
            8, CREAM if is_first else NAVY, "center")
        if not is_first:
            c.linkAbsolute(label, anchor,
                           Rect=(nx + 2, nav_y, nx + nav_w - 2, nav_y + 22))

    star_row(c, W / 2 - 30, 18, 5, 8, GOLD2)


# ============================================================
#  PAGE 2  —  TONIGHT'S ROUTINE BUILDER
# ============================================================

def draw_routine_page(c):
    c.bookmarkPage("routine")
    bg(c)

    # Header band
    c.setFillColor(NAVY)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    p = c.beginPath()
    p.moveTo(0, H - 80)
    p.curveTo(W * 0.3, H - 65, W * 0.7, H - 95, W, H - 80)
    p.lineTo(W, H - 80)
    p.lineTo(0, H - 80)
    p.close()
    c.setFillColor(NAVY2)
    c.drawPath(p, fill=1, stroke=0)

    txt(c, "Tonight's Routine", W / 2, H - 35, "Helvetica-Bold", 24, CREAM, "center")
    txt(c, "Check off each step in order · Add your own timing · Note what worked",
        W / 2, H - 58, "Helvetica-Oblique", 9, SAGE2, "center")

    # Quick-fill bar
    card(c, 36, H - 118, W - 72, 30, fill=CREAM2, stroke=GOLD, radius=6, lw=1)
    field_labels = [("Baby:", 50, 78), ("Date:", 180, 60), ("Bedtime target:", 320, 90), ("Actual in-crib:", 490, 80)]
    fx = 44
    for label, lw_px, fw in field_labels:
        txt(c, label, fx, H - 99, "Helvetica-Bold", 9, MUTED)
        draw_textfield(c, f"qf_{label.lower().replace(':', '').replace(' ', '_')}",
                       fx + lw_px - 22, H - 107, fw - lw_px - 5, 20, size=10,
                       bg_color=CREAM)
        fx += fw

    # ── CHECKLIST ─────────────────────────────────────────
    section_y = H - 135
    cb_size = 16
    row_h = 46
    pad_l = 36
    pad_r = W - 36

    for i, (key, label, hint) in enumerate(CHECKLIST_ITEMS):
        ry = section_y - i * row_h

        # Alternating row backgrounds
        bg_fill = PANEL if i % 2 == 0 else CREAM2
        c.setFillColor(bg_fill)
        c.setStrokeColor(CTRANS)
        c.roundRect(pad_l, ry - row_h + 8, pad_r - pad_l, row_h - 2, 5, fill=1, stroke=0)

        # Step number badge
        badge_x = pad_l + 6
        badge_y = ry - row_h + 18
        c.setFillColor(NAVY)
        c.circle(badge_x + 10, badge_y + 9, 11, fill=1, stroke=0)
        txt(c, str(i + 1), badge_x + 10, badge_y + 5, "Helvetica-Bold", 10, GOLD, "center")

        # Checkbox
        cb_x = badge_x + 28
        draw_checkbox(c, f"check_{key}", cb_x, badge_y, cb_size)

        # Label & hint
        txt(c, label, cb_x + cb_size + 10, ry - row_h + 31, "Helvetica-Bold", 11, INK)
        txt(c, hint, cb_x + cb_size + 10, ry - row_h + 18, "Helvetica-Oblique", 8, MUTED)

        # Time field
        txt(c, "Time:", pad_r - 145, ry - row_h + 29, "Helvetica", 8, MUTED)
        draw_textfield(c, f"time_{key}", pad_r - 110, ry - row_h + 15, 72, 20,
                       size=10, tooltip=f"Time for: {label}", bg_color=CREAM2)

    # ── ROUTINE ORDER BUILDER ─────────────────────────────
    section_divider(c, section_y - len(CHECKLIST_ITEMS) * row_h - 2,
                    "YOUR CUSTOM ROUTINE SEQUENCE", NAVY)

    builder_y = section_y - len(CHECKLIST_ITEMS) * row_h - 20
    card(c, 36, builder_y - 60, W - 72, 65, fill=NAVY, stroke=NAVY, radius=8)
    txt(c, "MY ROUTINE ORDER TONIGHT", W / 2, builder_y - 14,
        "Helvetica-Bold", 10, GOLD, "center")
    txt(c, "Write your steps in the exact order you do them. Same sequence every night.",
        W / 2, builder_y - 30, "Helvetica-Oblique", 8, SAGE2, "center")

    cols_n = 6
    box_w = (W - 72 - (cols_n - 1) * 6) / cols_n
    for bi in range(cols_n):
        bx = 36 + bi * (box_w + 6)
        by = builder_y - 58
        c.setFillColor(GOLD)
        c.circle(bx + 16, by + 24, 12, fill=1, stroke=0)
        txt(c, str(bi + 1), bx + 16, by + 20, "Helvetica-Bold", 10, NAVY, "center")
        draw_textfield(c, f"order_{bi + 1}", bx + 30, by + 6, box_w - 34, 22,
                       size=9, tooltip=f"Step {bi + 1}", bg_color=CREAM)

    # ── NOTES / WHAT WORKED ───────────────────────────────
    notes_y = builder_y - 80
    card(c, 36, notes_y - 80, (W - 80) / 2 - 2, 82, fill=BLUSH, stroke=ROSE, radius=8, lw=1)
    txt(c, "🌙  WHAT WORKED TONIGHT", 52, notes_y - 12, "Helvetica-Bold", 10, NAVY)
    draw_textfield(c, "what_worked", 52, notes_y - 74, (W - 80) / 2 - 34, 58,
                   size=10, tooltip="What worked well", multiline=True, bg_color=CREAM)

    rx = 36 + (W - 80) / 2 + 6
    card(c, rx, notes_y - 80, (W - 80) / 2 - 2, 82, fill=CREAM2, stroke=GOLD, radius=8, lw=1)
    txt(c, "✏️  ADJUST TOMORROW", rx + 16, notes_y - 12, "Helvetica-Bold", 10, NAVY)
    draw_textfield(c, "adjust_tomorrow", rx + 16, notes_y - 74, (W - 80) / 2 - 34, 58,
                   size=10, tooltip="What to adjust tomorrow", multiline=True, bg_color=CREAM)

    # ── Mood / settling quality rating ────────────────────
    rate_y = notes_y - 100
    card(c, 36, rate_y - 30, W - 72, 32, fill=NAVY, stroke=NAVY, radius=8)
    txt(c, "SETTLING QUALITY:", 56, rate_y - 11, "Helvetica-Bold", 10, GOLD)

    ratings = ["😴 Out cold", "😌 Settled well", "😕 A few hiccups", "😤 Tough night", "🌪 Send help"]
    rx2 = 210
    for ri, rating in enumerate(ratings):
        draw_radio(c, "settling_quality", rating, rx2, rate_y - 22, 12)
        txt(c, rating, rx2 + 16, rate_y - 18, "Helvetica", 9, CREAM)
        rx2 += 80

    # Footer nav
    _draw_footer_nav(c, "routine")


# ============================================================
#  PAGE 3  —  NIGHT WAKING LOG
# ============================================================

def draw_night_log(c):
    c.bookmarkPage("log")
    bg(c)

    c.setFillColor(NAVY2)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    txt(c, "Night Waking Log", W / 2, H - 35, "Helvetica-Bold", 24, CREAM, "center")
    txt(c, "Track every wake · Spot patterns · Celebrate the wins",
        W / 2, H - 58, "Helvetica-Oblique", 9, SAGE2, "center")

    # Quick-fill bar
    card(c, 36, H - 118, W - 72, 30, fill=CREAM2, stroke=GOLD, radius=6, lw=1)
    txt(c, "Baby:", 50, H - 99, "Helvetica-Bold", 9, MUTED)
    draw_textfield(c, "log_baby", 88, H - 107, 100, 20, size=10, bg_color=CREAM)
    txt(c, "Night of:", 210, H - 99, "Helvetica-Bold", 9, MUTED)
    draw_textfield(c, "log_date", 260, H - 107, 120, 20, size=10, bg_color=CREAM,
                   placeholder=datetime.date.today().strftime("%b %d, %Y"))
    txt(c, "Sleep method:", 406, H - 99, "Helvetica-Bold", 9, MUTED)
    draw_textfield(c, "log_method", 494, H - 107, 110, 20, size=10, bg_color=CREAM)

    # ── Waking entry table ────────────────────────────────
    table_y = H - 138
    headers = ["#", "Wake time", "Duration awake", "How resolved", "Resettled by", "Notes"]
    col_ws  = [26, 78, 90, 120, 90, W - 72 - 26 - 78 - 90 - 120 - 90 - 8]
    col_xs  = [36]
    for cw in col_ws[:-1]:
        col_xs.append(col_xs[-1] + cw)

    # Header row
    c.setFillColor(NAVY)
    c.roundRect(36, table_y - 22, W - 72, 22, 4, fill=1, stroke=0)
    for hi, hdr in enumerate(headers):
        cx = col_xs[hi] + col_ws[hi] / 2
        txt(c, hdr, cx, table_y - 14, "Helvetica-Bold", 8, GOLD, "center")

    row_h = 36
    n_rows = 10
    for ri in range(n_rows):
        ry = table_y - 22 - (ri + 1) * row_h
        bg_fill = PANEL if ri % 2 == 0 else CREAM2
        c.setFillColor(bg_fill)
        c.roundRect(36, ry, W - 72, row_h - 2, 3, fill=1, stroke=0)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.4)
        c.roundRect(36, ry, W - 72, row_h - 2, 3, fill=0, stroke=1)

        # Row number
        txt(c, str(ri + 1), col_xs[0] + col_ws[0] / 2, ry + 12,
            "Helvetica-Bold", 9, MUTED, "center")

        # Text fields for each column except the number
        field_names = ["wake_time", "duration", "resolved", "resettled", "notes"]
        for ci, fname in enumerate(field_names):
            fx = col_xs[ci + 1] + 3
            fw = col_ws[ci + 1] - 6
            draw_textfield(c, f"row{ri}_{fname}", fx, ry + 4, fw, row_h - 10,
                           size=9, bg_color=bg_fill)

    # ── Overnight summary ─────────────────────────────────
    sum_y = table_y - 22 - (n_rows + 1) * row_h - 10
    card(c, 36, sum_y - 80, W - 72, 82, fill=NAVY, stroke=NAVY, radius=8)
    txt(c, "OVERNIGHT SUMMARY", W / 2, sum_y - 12, "Helvetica-Bold", 11, GOLD, "center")

    fields = [
        ("Total wake count:", "total_wakes", 50, 90),
        ("Longest sleep stretch:", "longest_stretch", 220, 100),
        ("Total sleep time:", "total_sleep", 430, 90),
        ("Wake-up time:", "wakeup_time", 600, 80),
    ]
    fx = 50
    for label, name, lw_px, fw in fields:
        txt(c, label, fx, sum_y - 38, "Helvetica-Bold", 9, GOLD)
        draw_textfield(c, name, fx, sum_y - 68, fw - 10, 22, size=11, bg_color=CREAM2)
        fx += fw

    # Overall night rating
    rate_y = sum_y - 90
    card(c, 36, rate_y - 28, W - 72, 30, fill=BLUSH, stroke=ROSE, radius=6, lw=1)
    txt(c, "TONIGHT OVERALL:", 52, rate_y - 9, "Helvetica-Bold", 9, NAVY)
    stars = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    sx = 200
    for si, s in enumerate(stars):
        draw_radio(c, "night_rating", s, sx, rate_y - 22, 12)
        txt(c, s, sx + 15, rate_y - 19, "Helvetica", 9, GOLD)
        sx += 72

    # Notes
    note_y = rate_y - 48
    card(c, 36, note_y - 60, W - 72, 62, fill=CREAM2, stroke=GOLD, radius=8, lw=1)
    txt(c, "NOTES & OBSERVATIONS:", 52, note_y - 12, "Helvetica-Bold", 10, NAVY)
    draw_textfield(c, "night_notes", 52, note_y - 54, W - 104, 38,
                   size=10, multiline=True, bg_color=CREAM)

    _draw_footer_nav(c, "log")


# ============================================================
#  PAGE 4  —  SAFE SLEEP CHECKLIST
# ============================================================

def draw_safe_sleep(c):
    c.bookmarkPage("safe")
    bg(c)

    c.setFillColor(SAGE)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    txt(c, "Safe Sleep Checklist", W / 2, H - 35, "Helvetica-Bold", 24, CREAM, "center")
    txt(c, "AAP-aligned guidelines · Run through this every night · Non-negotiable",
        W / 2, H - 58, "Helvetica-Oblique", 9, CREAM2, "center")

    # Disclaimer banner
    card(c, 36, H - 118, W - 72, 30, fill=BLUSH, stroke=ROSE, radius=6, lw=1)
    txt(c, ("⚠  If you have concerns about your baby's sleep or breathing, "
            "always contact your paediatrician first."),
        W / 2, H - 100, "Helvetica-Oblique", 8.5, ROSE, "center")

    # ── Sleep surface checklist ───────────────────────────
    sections = [
        ("THE SLEEP SURFACE", SAGE, [
            ("surf_firm",    "Firm, flat mattress · no incline, pillow-top, or wedge"),
            ("surf_sheet",   "Fitted sheet only — no loose blankets, bumpers, or pillows"),
            ("surf_nostuffy","No stuffed animals, positioners, or sleep aids inside crib"),
            ("surf_sack",    "Sleep sack used in place of blanket — correct tog for temp"),
            ("surf_back",    "Baby placed on back · every sleep · every time · no exceptions"),
            ("surf_crib",    "Crib / bassinet / play yard ONLY (not swing, car seat, bouncer)"),
        ]),
        ("THE ROOM", NAVY, [
            ("room_temp",    "Room temp confirmed between 68–72°F / 20–22°C"),
            ("room_warm",    "Baby's chest warm but not sweaty — adjust tog if needed"),
            ("room_dark",    "True blackout achieved — if you can see your hand, too bright"),
            ("room_noise",   "White noise running at low continuous level — not in crib"),
            ("room_monitor", "Monitor LEDs covered with electrical tape"),
            ("room_light",   "No nightlight in use (or red-spectrum light only)"),
        ]),
        ("BEFORE YOU LEAVE THE ROOM", GOLD, [
            ("exit_check1",  "Transition signal completed? (e.g. goodnight phrase said)"),
            ("exit_check2",  "Baby is drowsy but awake — NOT already asleep"),
            ("exit_check3",  "Door cracked / monitor positioned and working"),
            ("exit_check4",  "You've decided how you'll respond to first cry"),
        ]),
    ]

    sy = H - 138
    for sec_label, sec_color, items in sections:
        # Section header
        c.setFillColor(sec_color)
        c.roundRect(36, sy - 22, W - 72, 22, 5, fill=1, stroke=0)
        txt(c, sec_label, W / 2, sy - 11, "Helvetica-Bold", 10, CREAM, "center")
        sy -= 22

        for key, label in items:
            row_h2 = 30
            bg_fi = PANEL if items.index((key, label)) % 2 == 0 else CREAM2
            c.setFillColor(bg_fi)
            c.roundRect(36, sy - row_h2, W - 72, row_h2 - 1, 4, fill=1, stroke=0)

            draw_checkbox(c, key, 50, sy - row_h2 + 7, 16)
            txt(c, label, 74, sy - row_h2 + 13, "Helvetica", 10, INK)
            sy -= row_h2

        sy -= 8  # gap between sections

    # ── Sleep Promise ─────────────────────────────────────
    promise_h = 140
    sy -= 8
    card(c, 36, sy - promise_h, W - 72, promise_h, fill=NAVY, stroke=GOLD, radius=10, lw=2)
    txt(c, "✦  YOUR SLEEP PROMISE  ✦", W / 2, sy - 18, "Helvetica-Bold", 12, GOLD, "center")
    accent_bar(c, (W - 200) / 2, sy - 28, 200, color=GOLD)

    promises = [
        "I will keep bedtime simple and in the same order every night.",
        "I will watch awake windows and act on them before overtiredness sets in.",
        "I will decide how I respond to night wakings before the night begins.",
        "I will wait before I go in — and give my baby the chance to resettle.",
        "I will stay consistent, especially on the nights when it is hardest.",
        "I am not just surviving the night — I am teaching my baby a life skill.",
    ]
    for pi, promise in enumerate(promises):
        py = sy - 52 - pi * 14
        c.setFillColor(GOLD2)
        c.circle(52, py + 4, 3, fill=1, stroke=0)
        txt(c, promise, 62, py, "Helvetica-Oblique", 8.5, CREAM)

    txt(c, "Sleep is coming. For both of you.  — Six & Thriving",
        W / 2, sy - promise_h + 14, "Helvetica-BoldOblique", 9, SAGE2, "center")

    _draw_footer_nav(c, "safe")


# ============================================================
#  PAGE 5  —  NOTES & PATTERNS
# ============================================================

def draw_notes_page(c):
    c.bookmarkPage("notes")
    bg(c)

    c.setFillColor(ROSE)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    txt(c, "Notes & Patterns", W / 2, H - 35, "Helvetica-Bold", 24, CREAM, "center")
    txt(c, "Get it out of your head · spot what's working · celebrate every win",
        W / 2, H - 58, "Helvetica-Oblique", 9, CREAM2, "center")

    pad = 36
    gutter = 14
    half_w = (W - pad * 2 - gutter) / 2

    # ── Left column ───────────────────────────────────────
    lx = pad
    ly = H - 100

    # Brain dump block
    card(c, lx, ly - 120, half_w, 122, fill=CREAM2, stroke=ROSE, radius=8, lw=1)
    txt(c, "BRAIN DUMP", lx + 14, ly - 18, "Helvetica-Bold", 11, NAVY)
    txt(c, "Everything on your mind — no filter", lx + 14, ly - 33,
        "Helvetica-Oblique", 8, MUTED)
    accent_bar(c, lx + 14, ly - 40, 130, color=ROSE)
    draw_textfield(c, "brain_dump", lx + 14, ly - 112, half_w - 28, 68,
                   size=10, multiline=True, bg_color=CREAM)

    # What I notice block
    ly2 = ly - 140
    card(c, lx, ly2 - 140, half_w, 142, fill=PANEL, stroke=BORDER, radius=8, lw=1)
    txt(c, "PATTERNS I NOTICE", lx + 14, ly2 - 18, "Helvetica-Bold", 11, NAVY)
    accent_bar(c, lx + 14, ly2 - 28, 150, color=SAGE)
    lines_y = ly2 - 44
    for li in range(7):
        lly = lines_y - li * 18
        dotted_line(c, lx + 14, lly, lx + half_w - 14)
        draw_textfield(c, f"pattern_{li}", lx + 14, lly - 14, half_w - 28, 16,
                       size=9, bg_color=PANEL)

    # Questions to ask paed
    ly3 = ly2 - 160
    card(c, lx, ly3 - 110, half_w, 112, fill=BLUSH, stroke=ROSE, radius=8, lw=1)
    txt(c, "QUESTIONS FOR PAEDIATRICIAN", lx + 14, ly3 - 18, "Helvetica-Bold", 10, NAVY)
    accent_bar(c, lx + 14, ly3 - 28, 200, color=ROSE)
    for qi in range(5):
        qy = ly3 - 48 - qi * 18
        c.setFillColor(ROSE)
        c.circle(lx + 22, qy + 5, 4, fill=1, stroke=0)
        draw_textfield(c, f"paed_q_{qi}", lx + 30, qy - 2, half_w - 48, 16,
                       size=9, bg_color=BLUSH)

    # ── Right column ──────────────────────────────────────
    rx = pad + half_w + gutter
    ry = H - 100

    # WIN LOG
    card(c, rx, ry - 200, half_w, 202, fill=NAVY, stroke=NAVY, radius=8)
    txt(c, "WIN LOG", rx + 14, ry - 18, "Helvetica-Bold", 12, GOLD)
    txt(c, "Every win counts — big AND small", rx + 14, ry - 33,
        "Helvetica-Oblique", 8, SAGE2)
    accent_bar(c, rx + 14, ry - 40, 120, color=GOLD)
    for wi in range(8):
        wy = ry - 58 - wi * 19
        c.setFillColor(GOLD)
        c.circle(rx + 24, wy + 5, 6, fill=1, stroke=0)
        txt(c, str(wi + 1), rx + 24, wy + 1, "Helvetica-Bold", 7, NAVY, "center")
        draw_textfield(c, f"win_{wi}", rx + 36, wy - 2, half_w - 52, 16,
                       size=9, bg_color=HexColor("#FFFFFF18"), border_color=HexColor("#FFFFFF30"))

    # Mantra / affirmation
    ry2 = ry - 220
    card(c, rx, ry2 - 80, half_w, 82, fill=GOLD, stroke=GOLD, radius=8)
    txt(c, "MY MANTRA FOR TONIGHT", rx + 14, ry2 - 16, "Helvetica-Bold", 10, NAVY)
    txt(c, "(write it. say it before you go in.)", rx + 14, ry2 - 30,
        "Helvetica-Oblique", 8, NAVY2)
    draw_textfield(c, "mantra", rx + 14, ry2 - 72, half_w - 28, 38,
                   size=11, multiline=True, bg_color=CREAM2)

    # This week's goal
    ry3 = ry2 - 100
    card(c, rx, ry3 - 80, half_w, 82, fill=SAGE, stroke=SAGE, radius=8)
    txt(c, "THIS WEEK'S SLEEP GOAL", rx + 14, ry3 - 16, "Helvetica-Bold", 10, CREAM)
    accent_bar(c, rx + 14, ry3 - 26, 160, color=CREAM2)
    draw_textfield(c, "week_goal", rx + 14, ry3 - 72, half_w - 28, 42,
                   size=10, multiline=True, bg_color=HexColor("#FFFFFF30"),
                   border_color=CREAM2)

    # Free notes
    ry4 = ry3 - 100
    avail = ry4 - 70
    if avail > 40:
        card(c, rx, 60, half_w, avail, fill=CREAM2, stroke=BORDER, radius=8, lw=1)
        txt(c, "FREE NOTES", rx + 14, 60 + avail - 18, "Helvetica-Bold", 10, NAVY)
        draw_textfield(c, "free_notes", rx + 14, 66, half_w - 28, avail - 28,
                       size=10, multiline=True, bg_color=CREAM)

    # ── Quote footer ──────────────────────────────────────
    card(c, 36, 34, W - 72, 28, fill=NAVY, stroke=NAVY, radius=6)
    txt(c, ('"Done is better than perfect. Pick one thing and do it tonight." '
            '— Six & Thriving'),
        W / 2, 45, "Helvetica-Oblique", 9, GOLD, "center")

    _draw_footer_nav(c, "notes")


# ============================================================
#  SHARED FOOTER NAV
# ============================================================

def _draw_footer_nav(c, active_page):
    pages = [
        ("Cover & Setup", "cover"),
        ("Tonight's Routine", "routine"),
        ("Night Log", "log"),
        ("Safe Sleep", "safe"),
        ("Notes", "notes"),
    ]
    nav_h = 22
    nav_y = 8
    nav_w = (W - 72) / len(pages)

    for pi, (label, anchor) in enumerate(pages):
        nx = 36 + pi * nav_w
        is_active = anchor == active_page
        fill = NAVY if is_active else CREAM2
        stroke = NAVY
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.setLineWidth(0.8)
        c.roundRect(nx + 1, nav_y, nav_w - 2, nav_h, 4, fill=1, stroke=1)
        txt(c, label, nx + nav_w / 2, nav_y + 7,
            "Helvetica-Bold" if is_active else "Helvetica",
            7.5, CREAM if is_active else NAVY, "center")
        if not is_active:
            c.linkAbsolute(label, anchor,
                           Rect=(nx + 1, nav_y, nx + nav_w - 1, nav_y + nav_h))


# ============================================================
#  MAIN
# ============================================================

def main():
    out = OUTPUT_FILENAME
    cv = canvas.Canvas(out, pagesize=(W, H))
    cv.setTitle("Bedtime Routine Builder Pad — Sleep, Baby. Please.")
    cv.setAuthor("Six & Thriving")
    cv.setSubject("Nightly bedtime routine tracker & safe sleep checklist")

    print("Generating Cover & Setup page...")
    draw_cover(cv)
    cv.showPage()

    print("Generating Tonight's Routine page...")
    draw_routine_page(cv)
    cv.showPage()

    print("Generating Night Waking Log page...")
    draw_night_log(cv)
    cv.showPage()

    print("Generating Safe Sleep Checklist page...")
    draw_safe_sleep(cv)
    cv.showPage()

    print("Generating Notes & Patterns page...")
    draw_notes_page(cv)
    cv.showPage()

    cv.save()
    print(f"\n✓  Done!  Saved → {out}")
    print(f"   5 interactive pages · {len(CHECKLIST_ITEMS)} checklist items")
    print("   Open in Adobe Acrobat or any PDF reader that supports AcroForms")


if __name__ == "__main__":
    main()
