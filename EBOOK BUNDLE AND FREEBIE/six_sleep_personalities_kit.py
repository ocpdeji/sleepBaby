"""
Six Sleep Personalities Discovery Kit — Premium Interactive PDF Planner
Based on "Sleep, Baby. Please." by Six & Thriving
Generates a fully interactive, bookmarked, navigable PDF with
working checkboxes, radio buttons, and text fields.
"""

import random
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

# ============================================================
#  CONFIG
# ============================================================
class Cfg:
    TITLE        = "SLEEP KIT"
    SUBTITLE     = "Six Sleep Personalities Discovery Kit"
    TAGLINE      = "Find your baby's type. Crack the sleep code."
    BRAND        = "Six & Thriving"
    OUTPUT       = "Six_Sleep_Personalities_Kit.pdf"

    # A4 portrait — perfect for print & tablet
    W, H = 595, 842

    # ── Palette: Navy / Gold / Cream ─────────────────────────
    C_DARK    = "#0D1B2A"   # deep navy
    C_ACCENT  = "#1A3A5C"   # mid navy
    C_ACCENT2 = "#C8963C"   # gold
    C_GOLD2   = "#F0C060"   # bright gold highlight
    C_CREAM   = "#FDF8F0"   # warm cream bg
    C_PANEL   = "#F4EDE0"   # card bg
    C_PANEL2  = "#EAF2F8"   # light blue tint card
    C_WHITE   = "#FFFFFF"
    C_INK     = "#1A1A2E"   # near-black
    C_SEC     = "#4A5568"   # secondary text
    C_MUTED   = "#9AA5B4"   # muted
    C_BORDER  = "#DDD0BB"   # warm border
    C_STAR    = "#C8963C"   # star/bullet

    # Personality colours (one per type)
    PERS_COLORS = [
        "#E8734A",  # The Snacker — coral
        "#5B8DB8",  # The Overthinker — steel blue
        "#8E6BAF",  # The Sensitive Soul — lavender
        "#2A9D8F",  # The Night Owl — teal
        "#E9C46A",  # The Catnapper — amber
        "#E76F51",  # The Party Animal — orange-red
    ]

    SECTIONS = [
        ("cover",         "Cover"),
        ("welcome",       "Welcome"),
        ("quiz",          "Personality Quiz"),
        ("snacker",       "The Snacker"),
        ("overthinker",   "The Overthinker"),
        ("sensitive",     "The Sensitive Soul"),
        ("nightowl",      "The Night Owl"),
        ("catnapper",     "The Catnapper"),
        ("party_animal",  "The Party Animal"),
        ("action_plan",   "My Action Plan"),
        ("sleep_tracker", "Sleep Tracker"),
        ("bedtime_builder","Bedtime Builder"),
        ("safe_sleep",    "Safe Sleep"),
        ("promise",       "Sleep Promise"),
    ]

    NAV_SECTIONS = [s for s in SECTIONS if s[0] != "cover"]


# ── Shorthand colour objects ─────────────────────────────────
C = Cfg
CDARK   = HexColor(C.C_DARK)
CA      = HexColor(C.C_ACCENT)
CA2     = HexColor(C.C_ACCENT2)
CGOLD2  = HexColor(C.C_GOLD2)
CCREAM  = HexColor(C.C_CREAM)
CPANEL  = HexColor(C.C_PANEL)
CPANEL2 = HexColor(C.C_PANEL2)
CWHITE  = HexColor(C.C_WHITE)
CINK    = HexColor(C.C_INK)
CSEC    = HexColor(C.C_SEC)
CMUTED  = HexColor(C.C_MUTED)
CBORDER = HexColor(C.C_BORDER)
CTRANS  = Color(1, 1, 1, 0)
W       = C.W
H       = C.H

PERS_HEX = [HexColor(h) for h in C.PERS_COLORS]

# ============================================================
#  PRIMITIVES
# ============================================================

def bg(c, color=None):
    c.setFillColor(color or CCREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def txt(c, text, x, y, font="Helvetica", size=11, color=None, align="left"):
    c.setFillColor(color or CINK)
    c.setFont(font, size)
    fn = {"left": c.drawString, "right": c.drawRightString,
          "center": c.drawCentredString}[align]
    fn(x, y, str(text))

def card(c, x, y, w, h, fill=None, stroke=None, radius=10, lw=1.2):
    c.setFillColor(fill if fill is not None else CPANEL)
    c.setStrokeColor(stroke if stroke is not None else CBORDER)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

def accent_bar(c, x, y, w, h=3, color=None):
    c.setFillColor(color or CA2)
    c.roundRect(x, y, w, h, 2, fill=1, stroke=0)

def divider(c, x, y, w, color=None, lw=0.7):
    c.setStrokeColor(color or CBORDER)
    c.setLineWidth(lw)
    c.line(x, y, x + w, y)

def pill(c, x, y, w, h, fill, text, text_color=None, font="Helvetica-Bold", size=9):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, h / 2, fill=1, stroke=0)
    txt(c, text, x + w / 2, y + (h - size) / 2 + 1, font, size, text_color or CWHITE, "center")


# ── Interactive widgets ──────────────────────────────────────

def tf(c, name, x, y, w, h, size=10, value="", bg_color=None):
    """Fillable text field."""
    try:
        c.acroForm.textfield(
            name=name, value=value,
            fillColor=bg_color or Color(1, 1, 1, 0.6),
            borderColor=CA,
            textColor=CINK, borderWidth=0.9,
            borderStyle="underlined",
            width=w, height=h, x=x, y=y,
            tooltip="Tap to type", fontName="Helvetica", fontSize=size,
        )
    except Exception:
        c.setStrokeColor(CA)
        c.setLineWidth(0.8)
        c.line(x, y + 2, x + w, y + 2)

def tf_box(c, name, x, y, w, h, size=10, value=""):
    """Fillable text field with box border."""
    try:
        c.acroForm.textfield(
            name=name, value=value,
            fillColor=CWHITE,
            borderColor=CBORDER,
            textColor=CINK, borderWidth=1,
            borderStyle="solid",
            width=w, height=h, x=x, y=y,
            tooltip="Tap to type", fontName="Helvetica", fontSize=size,
        )
    except Exception:
        c.setStrokeColor(CBORDER)
        c.setFillColor(CWHITE)
        c.setLineWidth(1)
        c.rect(x, y, w, h, fill=1, stroke=1)

def tf_multi(c, name, x, y, w, h, size=10):
    """Multi-line text area."""
    try:
        c.acroForm.textfield(
            name=name, value="",
            fillColor=CWHITE,
            borderColor=CBORDER,
            textColor=CINK, borderWidth=1,
            borderStyle="solid",
            width=w, height=h, x=x, y=y,
            tooltip="Tap to type notes here",
            fontName="Helvetica", fontSize=size,
            multiline=True,
        )
    except Exception:
        c.setStrokeColor(CBORDER)
        c.setFillColor(CWHITE)
        c.setLineWidth(1)
        c.rect(x, y, w, h, fill=1, stroke=1)

def cb(c, name, x, y, size=14, color=None):
    """Interactive checkbox."""
    try:
        c.acroForm.checkbox(
            name=name, checked=False,
            buttonStyle="check", shape="square",
            fillColor=CWHITE,
            borderColor=color or CA,
            textColor=color or CA,
            borderWidth=1.5,
            borderStyle="solid", size=size, x=x, y=y,
            tooltip="Tap to check",
        )
    except Exception:
        c.setStrokeColor(color or CA)
        c.setFillColor(CWHITE)
        c.setLineWidth(1.5)
        c.roundRect(x, y, size, size, 2, fill=1, stroke=1)

def rb(c, name, value, x, y, size=14, color=None):
    """Interactive radio button."""
    try:
        c.acroForm.radio(
            name=name, value=value,
            selected=False,
            buttonStyle="circle", shape="circle",
            fillColor=CWHITE,
            borderColor=color or CA,
            textColor=color or CA,
            borderWidth=1.5,
            size=size, x=x, y=y,
            tooltip=f"Select: {value}",
        )
    except Exception:
        c.setStrokeColor(color or CA)
        c.setFillColor(CWHITE)
        c.setLineWidth(1.5)
        c.circle(x + size / 2, y + size / 2, size / 2, fill=1, stroke=1)


# ── Navigation helpers ───────────────────────────────────────

def nav_bar(c, active_id):
    """Top navigation strip with clickable section pills."""
    bar_h = 32
    c.setFillColor(CDARK)
    c.rect(0, H - bar_h, W, bar_h, fill=1, stroke=0)

    nav_items = [
        ("welcome", "Welcome"),
        ("quiz", "Quiz"),
        ("action_plan", "Action Plan"),
        ("sleep_tracker", "Tracker"),
        ("bedtime_builder", "Bedtime"),
        ("safe_sleep", "Safe Sleep"),
    ]
    x_start = 8
    for sid, label in nav_items:
        pw = len(label) * 6.2 + 16
        py = H - bar_h + 4
        if sid == active_id:
            c.setFillColor(CA2)
            c.roundRect(x_start, py, pw, 22, 11, fill=1, stroke=0)
            txt(c, label, x_start + pw / 2, py + 7, "Helvetica-Bold", 8, CWHITE, "center")
        else:
            c.setFillColor(Color(1, 1, 1, 0.12))
            c.roundRect(x_start, py, pw, 22, 11, fill=1, stroke=0)
            txt(c, label, x_start + pw / 2, py + 7, "Helvetica", 8,
                Color(1, 1, 1, 0.75), "center")
        c.linkAbsolute(sid, sid, (x_start, py, x_start + pw, py + 22), Border="[0 0 0]")
        x_start += pw + 6

    # Brand right
    txt(c, C.BRAND, W - 10, H - bar_h + 11, "Helvetica-Bold", 9, CA2, "right")

def footer(c, label="", page_note=""):
    c.setFillColor(CMUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(30, 14, f"{C.BRAND}  •  {C.SUBTITLE}")
    if label:
        c.drawCentredString(W / 2, 14, label)
    if page_note:
        c.drawRightString(W - 30, 14, page_note)

def section_header(c, title, subtitle="", color=None, y=None):
    y = y or H - 68
    c.setFillColor(color or CA)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(30, y, title)
    if subtitle:
        txt(c, subtitle, 30, y - 20, "Helvetica-Oblique", 11, CSEC)
    accent_bar(c, 30, y - 28, 280, h=3, color=color or CA2)


# ============================================================
#  COVER
# ============================================================

def draw_cover(c):
    c.bookmarkPage("cover")

    # Deep navy bg
    c.setFillColor(CDARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Star field
    rng = random.Random(42)
    for _ in range(120):
        sx = rng.uniform(0, W)
        sy = rng.uniform(0, H)
        alpha = rng.uniform(0.05, 0.25)
        c.setFillColor(Color(1, 1, 1, alpha))
        c.circle(sx, sy, rng.uniform(0.5, 1.8), fill=1, stroke=0)

    # Moon glow
    c.setFillColor(Color(HexColor(C.C_ACCENT2).red,
                         HexColor(C.C_ACCENT2).green,
                         HexColor(C.C_ACCENT2).blue, 0.12))
    c.circle(W - 60, H - 60, 220, fill=1, stroke=0)
    c.setFillColor(Color(HexColor(C.C_ACCENT2).red,
                         HexColor(C.C_ACCENT2).green,
                         HexColor(C.C_ACCENT2).blue, 0.07))
    c.circle(W - 60, H - 60, 320, fill=1, stroke=0)

    # Bottom wave shape
    c.setFillColor(HexColor(C.C_ACCENT))
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(W, 0)
    p.lineTo(W, 160)
    p.curveTo(W * 0.75, 220, W * 0.25, 130, 0, 190)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Personality emoji icons in a soft arc
    emojis = ["🍼", "🤔", "🌸", "🦉", "😴", "🎉"]
    emoji_labels = ["Snacker", "Overthinker", "Sensitive", "Night Owl", "Catnapper", "Party Animal"]
    num = len(emojis)
    arc_cx, arc_cy, arc_r = W / 2, 310, 210
    import math
    for i, (em, lb) in enumerate(zip(emojis, emoji_labels)):
        angle = math.pi + (math.pi / (num - 1)) * i
        ex = arc_cx + arc_r * math.cos(angle)
        ey = arc_cy + arc_r * math.sin(angle) + 40
        col = PERS_HEX[i]
        c.setFillColor(Color(col.red, col.green, col.blue, 0.2))
        c.circle(ex, ey + 8, 22, fill=1, stroke=0)
        c.setFillColor(Color(col.red, col.green, col.blue, 0.5))
        c.circle(ex, ey + 8, 22, fill=0, stroke=1)
        c.setLineWidth(1.2)
        txt(c, em, ex, ey + 3, "Helvetica", 18, CWHITE, "center")
        txt(c, lb, ex, ey - 14, "Helvetica", 6, Color(1, 1, 1, 0.55), "center")

    # Badge strip
    c.setFillColor(Color(HexColor(C.C_ACCENT2).red,
                         HexColor(C.C_ACCENT2).green,
                         HexColor(C.C_ACCENT2).blue, 0.15))
    c.roundRect(40, H - 115, W - 80, 22, 11, fill=1, stroke=0)
    txt(c, "INTERACTIVE PLANNER  •  FULLY FILLABLE  •  PREMIUM EDITION",
        W / 2, H - 107, "Helvetica", 8, Color(1, 1, 1, 0.55), "center")

    # Main title
    txt(c, "SLEEP,", W / 2, H - 165, "Helvetica-Bold", 72, CWHITE, "center")
    txt(c, "BABY. PLEASE.", W / 2, H - 232, "Helvetica-Bold", 44, CA2, "center")

    # Gold rule
    c.setStrokeColor(CA2)
    c.setLineWidth(1.5)
    c.line(W / 2 - 140, H - 248, W / 2 + 140, H - 248)

    txt(c, C.SUBTITLE, W / 2, H - 268, "Helvetica-Bold", 14, CWHITE, "center")
    txt(c, C.TAGLINE, W / 2, H - 290, "Helvetica-Oblique", 10,
        Color(1, 1, 1, 0.6), "center")

    # CTA button
    bw, bh = 220, 40
    bx, by = W / 2 - bw / 2, 105
    c.setFillColor(CA2)
    c.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    txt(c, "START THE KIT  →", W / 2, by + 14, "Helvetica-Bold", 12, CDARK, "center")
    c.linkAbsolute("welcome", "welcome", (bx, by, bx + bw, by + bh), Border="[0 0 0]")

    # Brand
    txt(c, C.BRAND, W / 2, 70, "Helvetica-Bold", 10, Color(1, 1, 1, 0.45), "center")
    txt(c, "Six & Thriving  ©2026", W / 2, 55, "Helvetica", 8,
        Color(1, 1, 1, 0.3), "center")


# ============================================================
#  WELCOME
# ============================================================

def draw_welcome(c):
    c.bookmarkPage("welcome")
    bg(c)
    nav_bar(c, "welcome")
    footer(c, "Welcome to Your Kit", "Page 2")

    # Decorative left strip
    c.setFillColor(CA)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    section_header(c, "Welcome to the Kit", "Everything you need to crack your baby's sleep code", y=H - 68)

    # Intro card
    card(c, 25, H - 200, W - 50, 106, fill=CPANEL2, stroke=CA, lw=1.5)
    c.setFillColor(CA)
    c.setLineWidth(4)
    c.line(25, H - 200, 25, H - 94)
    txt(c, '"Every baby has a sleep personality. Once you know yours,', 42, H - 126,
        "Helvetica-Oblique", 11, CINK)
    txt(c, 'everything changes."', 42, H - 142, "Helvetica-Oblique", 11, CINK)
    txt(c, "— Six & Thriving", 42, H - 162, "Helvetica", 10, CSEC)

    txt(c, "HOW TO USE THIS KIT", 30, H - 222, "Helvetica-Bold", 13, CA)
    accent_bar(c, 30, H - 228, 200)

    steps = [
        ("01", "Take the Personality Quiz", "Answer questions about YOUR baby's actual behaviours — no guessing."),
        ("02", "Find Your Baby's Type", "Jump to your baby's personality page for tailored strategies."),
        ("03", "Build Your Action Plan", "Use the action plan page to customise your first-week approach."),
        ("04", "Track & Adjust", "Use the Sleep Tracker daily. Patterns emerge by day 3–4."),
        ("05", "Run the Bedtime Builder", "Personalise your exact bedtime sequence and stick it on the door."),
    ]
    for i, (num, title, desc) in enumerate(steps):
        sy = H - 285 - i * 74
        card(c, 25, sy, W - 50, 66, fill=CWHITE, stroke=CBORDER)
        # Number badge
        c.setFillColor(CA)
        c.circle(52, sy + 33, 18, fill=1, stroke=0)
        txt(c, num, 52, sy + 28, "Helvetica-Bold", 10, CWHITE, "center")
        txt(c, title, 78, sy + 42, "Helvetica-Bold", 12, CINK)
        txt(c, desc, 78, sy + 26, "Helvetica", 9.5, CSEC)
        # Jump link arrow
        target_map = {"01": "quiz", "02": "snacker", "03": "action_plan",
                      "04": "sleep_tracker", "05": "bedtime_builder"}
        tid = target_map[num]
        txt(c, "→", W - 48, sy + 28, "Helvetica-Bold", 14, CA2)
        c.linkAbsolute(tid, tid, (W - 60, sy + 18, W - 30, sy + 48), Border="[0 0 0]")

    # Six personalities quick-nav grid
    txt(c, "JUMP TO A PERSONALITY", 30, 148, "Helvetica-Bold", 11, CA)
    accent_bar(c, 30, 144, 180)
    pers_ids  = ["snacker", "overthinker", "sensitive", "nightowl", "catnapper", "party_animal"]
    pers_names = ["The Snacker 🍼", "The Overthinker 🤔", "The Sensitive Soul 🌸",
                  "The Night Owl 🦉", "The Catnapper 😴", "The Party Animal 🎉"]
    col_w = (W - 60) / 3
    for i, (pid, pname) in enumerate(zip(pers_ids, pers_names)):
        col = i % 3
        row = i // 3
        px = 30 + col * col_w
        py = 92 - row * 44
        col_hex = PERS_HEX[i]
        c.setFillColor(Color(col_hex.red, col_hex.green, col_hex.blue, 0.12))
        c.setStrokeColor(col_hex)
        c.setLineWidth(1)
        c.roundRect(px, py, col_w - 8, 36, 8, fill=1, stroke=1)
        txt(c, pname, px + (col_w - 8) / 2, py + 12, "Helvetica-Bold", 9, CINK, "center")
        c.linkAbsolute(pid, pid, (px, py, px + col_w - 8, py + 36), Border="[0 0 0]")


# ============================================================
#  PERSONALITY QUIZ
# ============================================================

def draw_quiz(c):
    c.bookmarkPage("quiz")
    bg(c)
    nav_bar(c, "quiz")
    footer(c, "Personality Quiz", "Page 3")

    c.setFillColor(CA)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    section_header(c, "Baby Sleep Personality Quiz",
                   "Answer each question based on your baby right now. Circle or check the best answer.", y=H - 68)

    txt(c, "Baby's name / nickname:", 30, H - 98, "Helvetica-Bold", 10, CSEC)
    tf(c, "baby_name", 185, H - 104, 160, 18, size=11)
    txt(c, "   Age:", 360, H - 98, "Helvetica-Bold", 10, CSEC)
    tf(c, "baby_age", 392, H - 104, 80, 18, size=11)
    txt(c, "   Date:", 482, H - 98, "Helvetica-Bold", 10, CSEC)
    tf(c, "quiz_date", 514, H - 104, 70, 18, size=11)

    accent_bar(c, 30, H - 112, W - 60)

    questions = [
        {
            "q": "Q1. How does your baby most commonly fall asleep?",
            "opts": [
                ("A", "Nursing or bottle-feeding — every time", "snacker"),
                ("B", "After a long wind-down; they fight it hard", "overthinker"),
                ("C", "Varies — very sensitive to routine changes", "sensitive"),
                ("D", "Rarely tired at the usual bedtime; wants to party", "nightowl"),
            ]
        },
        {
            "q": "Q2. How long are most of your baby's naps?",
            "opts": [
                ("A", "Short — 30–45 min, then wide awake", "catnapper"),
                ("B", "Variable — depends on how many times they fed", "snacker"),
                ("C", "Decent but only if the environment is perfect", "sensitive"),
                ("D", "Long in the day, but then restless at night", "nightowl"),
            ]
        },
        {
            "q": "Q3. What does a night waking look like for your baby?",
            "opts": [
                ("A", "Wants to feed — every single cycle", "snacker"),
                ("B", "Wakes happy, chatty, ready to play at 2 a.m.", "party_animal"),
                ("C", "Hard to resettle; small changes upset them", "sensitive"),
                ("D", "Wakes and stares — curious, won't wind down", "overthinker"),
            ]
        },
        {
            "q": "Q4. How does your baby respond to the sleep environment?",
            "opts": [
                ("A", "Any noise wakes them — very light sleeper", "sensitive"),
                ("B", "Fine until 45 min then up — like clockwork", "catnapper"),
                ("C", "Only settles when fed or rocked completely", "snacker"),
                ("D", "Seems energised at bedtime, not sleepy at all", "nightowl"),
            ]
        },
        {
            "q": "Q5. Which phrase best describes your baby at 7 p.m.?",
            "opts": [
                ("A", '"Wide awake — 7 p.m. is my vibe."', "nightowl"),
                ("B", '"I just woke from my 47-minute nap, refreshed and terrible."', "catnapper"),
                ("C", '"I need to feed to sleep or this is not happening."', "snacker"),
                ("D", '"Everything is interesting. I refuse to miss it."', "overthinker"),
            ]
        },
    ]

    q_y = H - 136
    for qi, q_data in enumerate(questions):
        q_h = 88
        if q_y - q_h < 22:
            break
        card(c, 25, q_y - q_h, W - 50, q_h - 4, fill=CWHITE, stroke=CBORDER)
        txt(c, q_data["q"], 36, q_y - 20, "Helvetica-Bold", 10, CA)

        # Radio buttons in 2 columns
        for oi, (letter, opt_text, pers) in enumerate(q_data["opts"]):
            col = oi % 2
            row = oi // 2
            ox = 36 + col * ((W - 70) / 2)
            oy = q_y - 44 - row * 22
            rb_name = f"q{qi+1}"
            rb(c, rb_name, f"{letter}_{pers}", ox, oy - 2, size=13, color=PERS_HEX[
                ["snacker","overthinker","sensitive","nightowl","catnapper","party_animal"].index(pers)
                if pers in ["snacker","overthinker","sensitive","nightowl","catnapper","party_animal"] else 0
            ])
            txt(c, f"{letter}. {opt_text}", ox + 18, oy + 1, "Helvetica", 8.5, CINK)

        q_y -= q_h + 4

    # Score section at bottom
    if q_y > 80:
        card(c, 25, 22, W - 50, q_y - 30, fill=CPANEL2, stroke=CA2, lw=1.5)
        txt(c, "SCORING YOUR QUIZ", 36, q_y - 10, "Helvetica-Bold", 11, CA)
        txt(c, "Count your most common letter. Mostly A's in Q1–Q3? You have a Snacker.", 36, q_y - 26, "Helvetica", 9, CSEC)
        txt(c, "Multiple letters? Your baby is likely a blend. Read the two closest types.", 36, q_y - 40, "Helvetica", 9, CSEC)
        txt(c, "My baby's primary type:", 36, q_y - 58, "Helvetica-Bold", 10, CINK)
        tf(c, "primary_type", 190, q_y - 64, 170, 18, size=11)
        txt(c, "  Blend type:", 368, q_y - 58, "Helvetica-Bold", 10, CINK)
        tf(c, "blend_type", 435, q_y - 64, 120, 18, size=11)

        # Navigation pills to personality pages
        txt(c, "Jump to your type:", 36, q_y - 86, "Helvetica-Bold", 10, CA)
        pers_ids  = ["snacker","overthinker","sensitive","nightowl","catnapper","party_animal"]
        pers_short= ["Snacker","Overthinker","Sensitive","Night Owl","Catnapper","Party Animal"]
        px_start = 36
        for pi, (pid, psn) in enumerate(zip(pers_ids, pers_short)):
            pw = len(psn) * 6.2 + 14
            col_hex = PERS_HEX[pi]
            c.setFillColor(Color(col_hex.red, col_hex.green, col_hex.blue, 0.2))
            c.setStrokeColor(col_hex)
            c.setLineWidth(1)
            c.roundRect(px_start, q_y - 108, pw, 18, 9, fill=1, stroke=1)
            txt(c, psn, px_start + pw / 2, q_y - 102, "Helvetica-Bold", 7.5, CINK, "center")
            c.linkAbsolute(pid, pid, (px_start, q_y - 108, px_start + pw, q_y - 90),
                           Border="[0 0 0]")
            px_start += pw + 6


# ============================================================
#  PERSONALITY PAGE TEMPLATE
# ============================================================

PERSONALITY_DATA = {
    "snacker": {
        "emoji": "🍼",
        "name": "The Snacker",
        "tagline": "Feeds little and often. The breast or bottle IS the sleep cue.",
        "who": (
            "The Snacker has learned to associate feeding with sleep. They wake "
            "frequently throughout the night — not from hunger, but because nursing "
            "or the bottle is their only way back to sleep. Every sleep cycle = a feed."
        ),
        "signs": [
            "Wakes every 1–2 hours at night, every time",
            "Always falls asleep on the breast or bottle",
            "Short awake windows during the day",
            "Distracted feeder — snacks rather than full feeds",
            "Pacifier or lovey doesn't work (yet)",
        ],
        "strategies": [
            "Consolidate feeds — fewer but larger (gradually)",
            "Feed, then wake slightly, then settle: break the cycle",
            "Introduce a lovey or pacifier as substitute comfort",
            "Move the feed earlier in the bedtime routine",
            "Ensure full feeds during the day (dream feed if needed)",
        ],
        "tip": (
            "Start your bedtime feed 15 minutes earlier so your baby doesn't "
            "fall asleep on the bottle. A drowsy-but-awake transfer to the crib "
            "is your biggest lever."
        ),
        "avoid": "Don't cut feeds cold turkey — gradual consolidation only.",
        "color_idx": 0,
    },
    "overthinker": {
        "emoji": "🤔",
        "name": "The Overthinker",
        "tagline": "Alert, curious, and convinced the world will stop without them.",
        "who": (
            "The Overthinker is fascinating and exhausting in equal measure. They fight "
            "sleep even when obviously tired — because the world is simply too interesting. "
            "Their nervous system runs hot. They need an especially calm, low-stimulus "
            "environment to power down."
        ),
        "signs": [
            "Fights sleep even with clearly tired cues",
            "Hyperalert — tracks movement and sound constantly",
            "Takes very long to settle even when exhausted",
            "Startles awake at the slightest change",
            "Needs a very long, calm wind-down to settle",
        ],
        "strategies": [
            "Earlier bedtime than you think — overtiredness hits them hard",
            "NO mobiles, toys, or screens in the last 30 min",
            "Darkest room you can achieve (blackout + tape over LEDs)",
            "White noise — steady, consistent, from the first minute of wind-down",
            "One caregiver, same voice, same sequence every night",
        ],
        "tip": (
            "The Overthinker's wind-down should feel almost meditative. Dim "
            "lights, low voices, slow movements. Think: 'boring on purpose.'"
        ),
        "avoid": "Avoid any interaction during the last 10 min that sparks engagement.",
        "color_idx": 1,
    },
    "sensitive": {
        "emoji": "🌸",
        "name": "The Sensitive Soul",
        "tagline": "Picks up on everything. Routine is their superpower.",
        "who": (
            "The Sensitive Soul is emotionally attuned and acutely aware of their "
            "environment. A change in your tone, a new smell in the room, a slight "
            "variation in routine — they notice all of it. They're prone to more "
            "frequent waking during household stress or developmental leaps."
        ),
        "signs": [
            "Easily startled and very difficult to resettle",
            "Sleep disrupted by any change in household routine",
            "Very aware of your emotional state — mirrors it",
            "Worsening sleep during developmental leaps",
            "Strong preference for one caregiver at bedtime",
        ],
        "strategies": [
            "Extraordinary routine consistency — same order, every night, forever",
            "Calm and regulated caregiver (hard when exhausted, but essential)",
            "Gentler method: Chair Method or Fading over Extinction",
            "Prepare for leaps — temporarily increase support, then return to plan",
            "Lovey introduced early — a comfort anchor they control",
        ],
        "tip": (
            "Your own nervous system is contagious to the Sensitive Soul. If you're "
            "anxious, they feel it. Take three slow breaths before entering the room."
        ),
        "avoid": "Avoid any abrupt method changes — consistency IS the intervention.",
        "color_idx": 2,
    },
    "nightowl": {
        "emoji": "🦉",
        "name": "The Night Owl",
        "tagline": "Running on a later internal clock. 7 p.m. is not their bedtime.",
        "who": (
            "The Night Owl is genuinely wired to be awake in the evening. Their "
            "circadian rhythm runs late. Putting them down at 7 p.m. results in an "
            "hour of fussing because biologically, they're just not ready. You can "
            "shift this — but it takes weeks, not nights."
        ),
        "signs": [
            "Not tired at 7 p.m. — genuinely wide awake",
            "Easiest to settle between 9 and 11 p.m.",
            "Sleeps well once down, but bedtime is a battle",
            "Wakes later in the morning if allowed",
            "Naps fine but at later-than-expected times",
        ],
        "strategies": [
            "Shift schedule earlier: 10–15 min every 2–3 days over 2–3 weeks",
            "Maximise morning light — outside within 30 min of waking",
            "Cap the last nap earlier to build more sleep pressure by evening",
            "Bright light off at least 90 min before target bedtime",
            "Be patient — circadian shifts take 2–3 weeks of consistent effort",
        ],
        "tip": (
            "Morning light is your strongest lever. Open the blinds, go outside, "
            "use a daylight lamp. This resets the circadian clock faster than anything else."
        ),
        "avoid": "Don't force an early bedtime without first shifting the nap schedule.",
        "color_idx": 3,
    },
    "catnapper": {
        "emoji": "😴",
        "name": "The Catnapper",
        "tagline": "One sleep cycle and done. The 45-minute alarm clock.",
        "who": (
            "The Catnapper surfaces from the first sleep cycle and wakes fully — "
            "45 minutes in, every time. They haven't learned to link sleep cycles. "
            "The result is a baby who's under-rested, a parent with no real break, "
            "and an afternoon of overtired chaos."
        ),
        "signs": [
            "Every nap ends at 35–48 minutes, almost to the minute",
            "Wakes fully — not drowsy, fully awake and often fussy",
            "Three or more naps still needed past 6 months",
            "Seems under-rested despite 'napping'",
            "Night sleep better than day sleep",
        ],
        "strategies": [
            "Be in the room at the 38-min mark — attempt re-settling before full waking",
            "Optimal nap environment: truly dark, white noise running, cool room",
            "Crib naps only (motion sleep doesn't build the same skill)",
            "For under-5 months: 3-nap schedule that works with short naps",
            "Avoid the 4th nap trap — too much sleep fragmentation late in the day",
        ],
        "tip": (
            "Set a timer for 38 minutes from when your baby falls asleep. When it "
            "goes off, put your hand on their chest before they fully surface. "
            "You're trying to push them through the transition."
        ),
        "avoid": "Don't let car or pram be the only nap option — it prevents skill-building.",
        "color_idx": 4,
    },
    "party_animal": {
        "emoji": "🎉",
        "name": "The Party Animal",
        "tagline": "Wakes at 2 a.m. happy, chatty, and ready to go.",
        "who": (
            "The Party Animal is possibly the most disconcerting baby to have: they "
            "wake in the middle of the night genuinely cheerful. Not crying — chatting. "
            "Playing with their feet. Smiling at the ceiling. They're having a great "
            "time. You are not."
        ),
        "signs": [
            "Wakes 1–4 a.m. — happy, alert, not distressed",
            "Plays or babbles in the dark for 30–90 min",
            "Not hungry, not in discomfort — just awake",
            "Falls back asleep eventually, then hard to wake in the morning",
            "Possibly going to bed slightly too early",
        ],
        "strategies": [
            "Check bedtime — try pushing it 15–30 min later to rule out early bedtime",
            "Absolute darkness — any light triggers the circadian 'morning' signal",
            "Do NOT engage during the wakeful window (no lights, no play, no talking)",
            "Make 2 a.m. incredibly boring — flat response, no reward",
            "Ensure the last nap ends early enough to build sleep pressure",
        ],
        "tip": (
            "The Party Animal is often triggered by even tiny amounts of light. "
            "Electrical tape over every LED. True blackout. This alone resolves "
            "many Party Animal wake windows within a week."
        ),
        "avoid": "Never turn a light on, engage with play, or bring them to your bed during this window.",
        "color_idx": 5,
    },
}

def draw_personality(c, pid):
    data = PERSONALITY_DATA[pid]
    c.bookmarkPage(pid)
    bg(c)
    nav_bar(c, "quiz")
    footer(c, data["name"], "Personality Profile")

    col_hex = PERS_HEX[data["color_idx"]]

    # Colour strip left
    c.setFillColor(col_hex)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    # Header band
    c.setFillColor(Color(col_hex.red, col_hex.green, col_hex.blue, 0.1))
    c.rect(8, H - 96, W - 8, 64, fill=1, stroke=0)

    txt(c, data["emoji"] + "  " + data["name"], 22, H - 58,
        "Helvetica-Bold", 24, col_hex)
    txt(c, data["tagline"], 22, H - 78, "Helvetica-Oblique", 10.5, CSEC)
    accent_bar(c, 22, H - 90, 280, h=3, color=col_hex)

    # Back to quiz pill
    c.setFillColor(Color(col_hex.red, col_hex.green, col_hex.blue, 0.15))
    c.roundRect(W - 120, H - 82, 100, 20, 10, fill=1, stroke=0)
    txt(c, "← Back to Quiz", W - 70, H - 77, "Helvetica", 8, col_hex, "center")
    c.linkAbsolute("quiz", "quiz", (W - 120, H - 82, W - 20, H - 62), Border="[0 0 0]")

    # Two-column layout
    col_w = (W - 56) / 2
    lx, rx = 22, 22 + col_w + 12

    # --- LEFT: Who they are + Signs ---
    card(c, lx, H - 278, col_w, 166, fill=CWHITE, stroke=CBORDER)
    txt(c, "WHO THEY ARE", lx + 10, H - 114, "Helvetica-Bold", 10, col_hex)
    accent_bar(c, lx + 10, H - 120, 120, h=2, color=col_hex)

    # Word-wrap "who" text
    who_text = data["who"]
    words = who_text.split()
    lines_who = []
    line = ""
    for w_word in words:
        test = (line + " " + w_word).strip()
        if len(test) * 5.5 < col_w - 22:
            line = test
        else:
            lines_who.append(line)
            line = w_word
    if line:
        lines_who.append(line)
    for li, ln in enumerate(lines_who[:5]):
        txt(c, ln, lx + 10, H - 138 - li * 14, "Helvetica", 9, CINK)

    txt(c, "SIGNS YOUR BABY IS THIS TYPE", lx + 10, H - 228, "Helvetica-Bold", 9, CSEC)
    for si, sign in enumerate(data["signs"]):
        sy = H - 244 - si * 16
        if sy < H - 272:
            break
        c.setFillColor(col_hex)
        c.circle(lx + 17, sy + 5, 3, fill=1, stroke=0)
        txt(c, sign, lx + 25, sy, "Helvetica", 8.5, CINK)

    # --- RIGHT: Strategies ---
    card(c, rx, H - 278, col_w, 166, fill=CWHITE, stroke=CBORDER)
    txt(c, "WHAT WORKS", rx + 10, H - 114, "Helvetica-Bold", 10, col_hex)
    accent_bar(c, rx + 10, H - 120, 120, h=2, color=col_hex)
    for si, strat in enumerate(data["strategies"]):
        sy = H - 138 - si * 24
        if sy < H - 270:
            break
        c.setFillColor(Color(col_hex.red, col_hex.green, col_hex.blue, 0.15))
        c.roundRect(rx + 10, sy - 3, 14, 14, 3, fill=1, stroke=0)
        txt(c, str(si + 1), rx + 17, sy, "Helvetica-Bold", 8, col_hex, "center")
        # Wrap strategy text
        s_words = strat.split()
        s_line = ""
        s_lines = []
        for sw in s_words:
            test = (s_line + " " + sw).strip()
            if len(test) * 5.2 < col_w - 40:
                s_line = test
            else:
                s_lines.append(s_line)
                s_line = sw
        if s_line:
            s_lines.append(s_line)
        for li, sl in enumerate(s_lines[:2]):
            txt(c, sl, rx + 28, sy - li * 12, "Helvetica", 8.5, CINK)

    # --- Tip card (full width) ---
    card(c, 22, H - 370, W - 44, 74, fill=Color(col_hex.red, col_hex.green, col_hex.blue, 0.08),
         stroke=col_hex, lw=1.5)
    c.setFillColor(col_hex)
    c.roundRect(22, H - 318, 70, 18, 9, fill=1, stroke=0)
    txt(c, "PRO TIP", 57, H - 313, "Helvetica-Bold", 8, CWHITE, "center")
    tip_words = data["tip"].split()
    t_line, t_lines = "", []
    for tw in tip_words:
        test = (t_line + " " + tw).strip()
        if len(test) * 5.5 < W - 100:
            t_line = test
        else:
            t_lines.append(t_line)
            t_line = tw
    if t_line:
        t_lines.append(t_line)
    for li, tl in enumerate(t_lines[:3]):
        txt(c, tl, 30, H - 342 - li * 14, "Helvetica-Oblique", 10, CINK)

    c.setFillColor(HexColor("#E74C3C"))
    c.roundRect(22, H - 390, 56, 16, 8, fill=1, stroke=0)
    txt(c, "AVOID", 50, H - 385, "Helvetica-Bold", 7.5, CWHITE, "center")
    txt(c, data["avoid"], 84, H - 385, "Helvetica", 9, CINK)

    # --- Personalisation fields ---
    txt(c, "MY NOTES FOR THIS TYPE", 22, H - 412, "Helvetica-Bold", 10, CA)
    accent_bar(c, 22, H - 418, 200, h=2)

    # Checkboxes for strategies
    txt(c, "Strategies I'm trying:", 22, H - 434, "Helvetica-Bold", 9, CSEC)
    for si, strat in enumerate(data["strategies"][:4]):
        sy = H - 452 - si * 22
        cb(c, f"{pid}_strat_{si}", 22, sy - 2, size=13, color=col_hex)
        txt(c, strat[:65] + ("…" if len(strat) > 65 else ""), 40, sy + 1, "Helvetica", 8.5, CINK)

    txt(c, "What I noticed:", 22, H - 548, "Helvetica-Bold", 9, CSEC)
    tf_multi(c, f"{pid}_notes", 22, H - 630, W - 44, 74, size=9)

    txt(c, "My biggest challenge:", 22, H - 644, "Helvetica-Bold", 9, CSEC)
    tf(c, f"{pid}_challenge", 145, H - 650, W - 170, 18, size=10)

    txt(c, "First thing I'll try tonight:", 22, H - 668, "Helvetica-Bold", 9, CSEC)
    tf(c, f"{pid}_tonight", 175, H - 674, W - 200, 18, size=10)

    # Rating: how confident am I?
    txt(c, "My confidence level (1 = none, 5 = ready):", 22, H - 694, "Helvetica-Bold", 9, CSEC)
    for ri in range(1, 6):
        rb(c, f"{pid}_confidence", str(ri), 22 + (ri - 1) * 38, H - 712, size=14, color=col_hex)
        txt(c, str(ri), 29 + (ri - 1) * 38, H - 726, "Helvetica", 8, CSEC, "center")

    # Next steps nav
    next_map = {
        "snacker": "overthinker", "overthinker": "sensitive",
        "sensitive": "nightowl", "nightowl": "catnapper",
        "catnapper": "party_animal", "party_animal": "action_plan",
    }
    nxt = next_map.get(pid, "action_plan")
    nxt_label = {
        "overthinker": "The Overthinker →", "sensitive": "The Sensitive Soul →",
        "nightowl": "The Night Owl →", "catnapper": "The Catnapper →",
        "party_animal": "The Party Animal →", "action_plan": "My Action Plan →",
    }.get(nxt, "Next →")

    bw, bh = 180, 30
    bx, by = W - bw - 22, 22
    c.setFillColor(col_hex)
    c.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    txt(c, nxt_label, bx + bw / 2, by + 10, "Helvetica-Bold", 9, CWHITE, "center")
    c.linkAbsolute(nxt, nxt, (bx, by, bx + bw, by + bh), Border="[0 0 0]")


# ============================================================
#  ACTION PLAN
# ============================================================

def draw_action_plan(c):
    c.bookmarkPage("action_plan")
    bg(c)
    nav_bar(c, "action_plan")
    footer(c, "My Action Plan", "Page 10")

    c.setFillColor(CA)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    section_header(c, "My 7-Night Action Plan",
                   "Complete this before Night 1 begins. Your 2 a.m. brain will thank you.", y=H - 68)

    # Identity row
    lbl_style = ("Helvetica-Bold", 9, CSEC)
    txt(c, "Baby's name:", 22, H - 98, *lbl_style)
    tf(c, "ap_baby", 105, H - 104, 120, 18, size=11)
    txt(c, "  Age:", 232, H - 98, *lbl_style)
    tf(c, "ap_age", 260, H - 104, 60, 18, size=11)
    txt(c, "  Start date:", 330, H - 98, *lbl_style)
    tf(c, "ap_start", 400, H - 104, 90, 18, size=11)
    txt(c, "  Type:", 500, H - 98, *lbl_style)
    tf(c, "ap_type", 528, H - 104, 52, 18, size=11)
    accent_bar(c, 22, H - 112, W - 44)

    # Three column setup choices
    col_w3 = (W - 56) / 3
    col_headers = ["SLEEP METHOD", "BEDTIME ROUTINE", "MY RESPONSE PLAN"]
    col_subs = [
        "Which method from Chapter 6?",
        "Your exact sequence tonight",
        "What I'll do at each waking",
    ]
    methods = ["Extinction (CIO)", "Ferber Method", "Chair Method", "Fading Method", "Pick Up / Put Down"]
    for ci, (hdr, sub) in enumerate(zip(col_headers, col_subs)):
        cx = 22 + ci * (col_w3 + 6)
        card(c, cx, H - 310, col_w3, 182, fill=CWHITE, stroke=CBORDER)
        c.setFillColor(CA)
        c.roundRect(cx, H - 138, col_w3, 20, 4, fill=1, stroke=0)
        txt(c, hdr, cx + col_w3 / 2, H - 131, "Helvetica-Bold", 9, CWHITE, "center")
        txt(c, sub, cx + 8, H - 150, "Helvetica-Oblique", 8, CSEC)

        if ci == 0:
            for mi, method in enumerate(methods):
                rb(c, "sleep_method", method, cx + 8, H - 170 - mi * 22, size=12, color=CA)
                txt(c, method, cx + 24, H - 167 - mi * 22, "Helvetica", 8.5, CINK)
        elif ci == 1:
            routine_steps = ["Transition signal", "Bath / wipe-down", "Lotion massage",
                             "Pyjamas + sleep sack", "Feed (not to sleep)", "Book or song", "Into crib awake"]
            for ri, step in enumerate(routine_steps):
                sy = H - 166 - ri * 20
                if sy < H - 305:
                    break
                txt(c, f"{ri+1}.", cx + 8, sy, "Helvetica-Bold", 9, CA2)
                tf(c, f"routine_step_{ri}", cx + 22, sy - 4, col_w3 - 30, 16, size=8,
                   value=step)
        else:
            for ri2, label in enumerate(["Waking 1:", "Waking 2:", "Waking 3:", "If distressed:", "My fallback:"]):
                sy = H - 166 - ri2 * 28
                if sy < H - 305:
                    break
                txt(c, label, cx + 8, sy, "Helvetica-Bold", 8.5, CSEC)
                tf(c, f"response_{ri2}", cx + 8, sy - 18, col_w3 - 16, 16, size=8)

    # Environment checklist
    txt(c, "ENVIRONMENT SETUP CHECKLIST", 22, H - 326, "Helvetica-Bold", 10, CA)
    accent_bar(c, 22, H - 332, 260)
    env_items = [
        "True blackout (can't see hand)", "White noise running all night",
        "Room temp 68–72°F / 20–22°C", "All LEDs covered with tape",
        "Firm flat mattress, fitted sheet only", "Sleep sack right tog for temperature",
    ]
    for ei, item in enumerate(env_items):
        col = ei % 3
        row = ei // 3
        ex = 22 + col * ((W - 44) / 3)
        ey = H - 352 - row * 24
        cb(c, f"env_{ei}", ex, ey - 2, size=13)
        txt(c, item, ex + 18, ey + 1, "Helvetica", 8.5, CINK)

    # Night-by-night planner
    txt(c, "NIGHT-BY-NIGHT LOG", 22, H - 422, "Helvetica-Bold", 10, CA)
    accent_bar(c, 22, H - 428, 200)
    nights = ["Night 1", "Night 2", "Night 3", "Night 4", "Night 5", "Night 6", "Night 7"]
    col_w7 = (W - 44) / 7
    for ni, night in enumerate(nights):
        nx = 22 + ni * col_w7
        card(c, nx, H - 540, col_w7 - 4, 102, fill=CWHITE if ni % 2 == 0 else CPANEL,
             stroke=CBORDER, radius=6)
        c.setFillColor(CA if ni < 3 else CA2 if ni < 6 else HexColor("#27AE60"))
        c.roundRect(nx, H - 442, col_w7 - 4, 16, 4, fill=1, stroke=0)
        txt(c, night, nx + (col_w7 - 4) / 2, H - 436,
            "Helvetica-Bold", 7.5, CWHITE, "center")
        txt(c, "Settle time:", nx + 4, H - 460, "Helvetica", 7, CSEC)
        tf(c, f"n{ni}_settle", nx + 4, H - 474, col_w7 - 12, 14, size=7)
        txt(c, "Wakings:", nx + 4, H - 490, "Helvetica", 7, CSEC)
        tf(c, f"n{ni}_wakings", nx + 4, H - 504, col_w7 - 12, 14, size=7)
        txt(c, "Notes:", nx + 4, H - 520, "Helvetica", 7, CSEC)
        tf(c, f"n{ni}_notes", nx + 4, H - 534, col_w7 - 12, 14, size=7)

    # Partner agreement
    card(c, 22, H - 624, W - 44, 72, fill=CPANEL2, stroke=CA, lw=1.5)
    txt(c, "PARTNER AGREEMENT", 34, H - 558, "Helvetica-Bold", 10, CA)
    txt(c, "Who leads Night 1–3:", 34, H - 576, "Helvetica-Bold", 9, CSEC)
    tf(c, "partner_lead_a", 170, H - 582, 140, 16, size=9)
    txt(c, "    Who leads Night 4–7:", 316, H - 576, "Helvetica-Bold", 9, CSEC)
    tf(c, "partner_lead_b", 456, H - 582, 100, 16, size=9)
    txt(c, "If one of us wants to break the plan at 2 a.m.:", 34, H - 600, "Helvetica-Bold", 9, CSEC)
    tf(c, "partner_plan", 270, H - 606, W - 296, 16, size=9)
    txt(c, "Our 'hold the line' signal:", 34, H - 618, "Helvetica-Bold", 9, CSEC)
    tf(c, "partner_signal", 185, H - 624, W - 210, 16, size=9)

    # My why
    txt(c, "MY WHY — what a well-rested family looks like:", 22, H - 644, "Helvetica-Bold", 9, CSEC)
    tf_multi(c, "my_why", 22, H - 700, W - 44, 48, size=10)

    # Nav button
    bw, bh = 160, 28
    bx, by = W - bw - 22, 22
    c.setFillColor(CA2)
    c.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    txt(c, "Sleep Tracker →", bx + bw / 2, by + 9, "Helvetica-Bold", 9, CDARK, "center")
    c.linkAbsolute("sleep_tracker", "sleep_tracker", (bx, by, bx + bw, by + bh), Border="[0 0 0]")


# ============================================================
#  SLEEP TRACKER
# ============================================================

def draw_sleep_tracker(c):
    c.bookmarkPage("sleep_tracker")
    bg(c)
    nav_bar(c, "sleep_tracker")
    footer(c, "7-Day Sleep Tracker", "Page 11")

    c.setFillColor(CA)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    section_header(c, "7-Day Sleep Tracker",
                   "Track daily. Patterns emerge by Day 3–4. Trust the process.", y=H - 68)

    txt(c, "Baby:", 22, H - 92, "Helvetica-Bold", 9, CSEC)
    tf(c, "tracker_baby", 55, H - 98, 120, 16, size=10)
    txt(c, "  Week of:", 184, H - 92, "Helvetica-Bold", 9, CSEC)
    tf(c, "tracker_week", 232, H - 98, 100, 16, size=10)
    accent_bar(c, 22, H - 106, W - 44)

    # Column headers
    cols = ["Day", "Wake Time", "Nap 1", "Nap 2", "Nap 3", "Bedtime", "Wakings", "Total Sleep", "Mood"]
    col_widths = [38, 62, 58, 58, 48, 58, 52, 62, 52]  # must sum to W-44
    # Adjust to fit
    total_cw = sum(col_widths)
    scale = (W - 44) / total_cw
    col_widths = [int(cw * scale) for cw in col_widths]

    hdr_y = H - 120
    cx_pos = 22
    for ci, (col_hdr, cw) in enumerate(zip(cols, col_widths)):
        c.setFillColor(CA)
        c.rect(cx_pos, hdr_y, cw, 20, fill=1, stroke=0)
        txt(c, col_hdr, cx_pos + cw / 2, hdr_y + 6,
            "Helvetica-Bold", 7, CWHITE, "center")
        cx_pos += cw

    # Data rows
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    row_h = 38
    for di, day in enumerate(days):
        ry = hdr_y - (di + 1) * row_h
        cx_pos = 22
        fill_c = CWHITE if di % 2 == 0 else CPANEL
        c.setFillColor(fill_c)
        c.rect(22, ry, W - 44, row_h, fill=1, stroke=0)

        for ci2, cw in enumerate(col_widths):
            c.setStrokeColor(CBORDER)
            c.setLineWidth(0.5)
            c.rect(cx_pos, ry, cw, row_h, fill=0, stroke=1)
            if ci2 == 0:
                # Day + date
                txt(c, day, cx_pos + cw / 2, ry + 22,
                    "Helvetica-Bold", 9, CA, "center")
                tf(c, f"t_{di}_date", cx_pos + 4, ry + 2, cw - 8, 14, size=7)
            elif ci2 == 6:
                # Wakings — radio 0-5+
                txt(c, "count:", cx_pos + 4, ry + 26, "Helvetica", 6, CSEC)
                for wn in range(4):
                    rb(c, f"t_{di}_wake", str(wn), cx_pos + 4 + wn * 12, ry + 12, size=10, color=CA)
                    txt(c, str(wn), cx_pos + 9 + wn * 12, ry + 4, "Helvetica", 6, CSEC, "center")
            elif ci2 == 8:
                # Mood
                for mn, mood in enumerate(["😊", "😐", "😩"]):
                    rb(c, f"t_{di}_mood", mood, cx_pos + 4 + mn * 16, ry + 14, size=12, color=CA2)
                txt(c, "good  ok  hard", cx_pos + 3, ry + 4, "Helvetica", 5.5, CMUTED)
            else:
                tf_box(c, f"t_{di}_col{ci2}", cx_pos + 3, ry + 3, cw - 6, row_h - 6, size=8)
            cx_pos += cw

    # Pattern notes below
    note_y = hdr_y - len(days) * row_h - 16
    txt(c, "PATTERNS & OBSERVATIONS", 22, note_y, "Helvetica-Bold", 10, CA)
    accent_bar(c, 22, note_y - 6, 240)

    obs_labels = ["Best night:", "Hardest night:", "Trend I'm seeing:", "What I'm changing next week:"]
    for oi, label in enumerate(obs_labels):
        oy = note_y - 28 - oi * 34
        txt(c, label, 22, oy, "Helvetica-Bold", 9, CSEC)
        tf(c, f"obs_{oi}", 22 + len(label) * 5.5 + 5, oy - 5, W - 60 - len(label) * 5.5, 18, size=10)

    # Nav
    bw, bh = 180, 28
    c.setFillColor(CA2)
    c.roundRect(W - bw - 22, 22, bw, bh, bh / 2, fill=1, stroke=0)
    txt(c, "Bedtime Builder →", W - bw / 2 - 22, 31, "Helvetica-Bold", 9, CDARK, "center")
    c.linkAbsolute("bedtime_builder", "bedtime_builder",
                   (W - bw - 22, 22, W - 22, 50), Border="[0 0 0]")


# ============================================================
#  BEDTIME BUILDER
# ============================================================

def draw_bedtime_builder(c):
    c.bookmarkPage("bedtime_builder")
    bg(c)
    nav_bar(c, "bedtime_builder")
    footer(c, "Bedtime Builder", "Page 12")

    c.setFillColor(CA)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    section_header(c, "Personalized Bedtime Builder",
                   "Build your exact routine. Same order every night — this IS the signal.", y=H - 68)

    txt(c, "Target bedtime:", 22, H - 92, "Helvetica-Bold", 10, CSEC)
    tf(c, "target_bedtime", 130, H - 98, 80, 18, size=12)
    txt(c, "  Awake window length:", 220, H - 92, "Helvetica-Bold", 10, CSEC)
    tf(c, "awake_window", 360, H - 98, 80, 18, size=12)
    txt(c, " mins  →  Start wind-down at:", 448, H - 92, "Helvetica", 9.5, CSEC)
    tf(c, "winddown_start", W - 82, H - 98, 62, 18, size=12)
    accent_bar(c, 22, H - 108, W - 44)

    # Build the sequence
    txt(c, "MY BEDTIME SEQUENCE", 22, H - 126, "Helvetica-Bold", 11, CA)
    txt(c, "(Fill in each step. Check it off each night.)", 22, H - 140, "Helvetica-Oblique", 9, CSEC)

    default_steps = [
        ("Transition signal", "e.g. 'Lights dim, I say goodnight to the toys'"),
        ("Stop all stimulating activity", "Screens off, active play ended"),
        ("Bath / warm wipe-down", "Duration:"),
        ("Lotion massage", "Optional but signals body-readiness for sleep"),
        ("Pyjamas + sleep sack", "Tog rating for tonight's temp:"),
        ("Feed — NOT to sleep", "Feed in dim room; keep baby awake"),
        ("Books or lullaby", "How many / which song:"),
        ("Goodnight phrase", "Your exact phrase (say this every time):"),
        ("White noise on", "Volume & type:"),
        ("Into crib — drowsy but awake", "The most important step"),
        ("Exit room calmly", "Same, every night"),
    ]

    step_h = 48
    for si, (step_title, hint) in enumerate(default_steps):
        sy = H - 164 - si * step_h
        if sy - step_h < 22:
            break

        # Alternating row bg
        c.setFillColor(CWHITE if si % 2 == 0 else CPANEL)
        c.rect(22, sy - step_h + 4, W - 44, step_h - 2, fill=1, stroke=0)
        c.setStrokeColor(CBORDER)
        c.setLineWidth(0.5)
        c.line(22, sy - step_h + 4, W - 22, sy - step_h + 4)

        # Step number
        c.setFillColor(CA)
        c.circle(40, sy - step_h / 2 + 4, 12, fill=1, stroke=0)
        txt(c, str(si + 1), 40, sy - step_h / 2, "Helvetica-Bold", 9, CWHITE, "center")

        # Checkbox column (7 nights)
        txt(c, "M T W T F S S", W - 100, sy - step_h + 22, "Helvetica", 6.5, CMUTED)
        for ni in range(7):
            cb(c, f"bb_{si}_n{ni}", W - 100 + ni * 12, sy - step_h + 6, size=10, color=CA2)

        # Step name + customisation field
        txt(c, step_title, 58, sy - 8, "Helvetica-Bold", 10, CINK)
        txt(c, hint, 58, sy - step_h + 16, "Helvetica-Oblique", 8, CMUTED)
        tf(c, f"bb_custom_{si}", 58, sy - step_h + 6, W - 180, 14, size=8)

    # Duration + timing note
    if sy - step_h > 60:
        txt(c, "Total routine duration: 20–30 minutes. Shorter = not enough wind-down. Longer = risk of falling asleep IN the routine.",
            22, 50, "Helvetica-Oblique", 8.5, CSEC)

    # Nav
    bw, bh = 160, 28
    c.setFillColor(CA2)
    c.roundRect(W - bw - 22, 22, bw, bh, bh / 2, fill=1, stroke=0)
    txt(c, "Safe Sleep →", W - bw / 2 - 22, 31, "Helvetica-Bold", 9, CDARK, "center")
    c.linkAbsolute("safe_sleep", "safe_sleep", (W - bw - 22, 22, W - 22, 50), Border="[0 0 0]")


# ============================================================
#  SAFE SLEEP
# ============================================================

def draw_safe_sleep(c):
    c.bookmarkPage("safe_sleep")
    bg(c)
    nav_bar(c, "safe_sleep")
    footer(c, "Safe Sleep Checklist", "Page 13")

    c.setFillColor(CA)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    section_header(c, "Safe Sleep Checklist",
                   "AAP-aligned. Run through this every single night until it's muscle memory.", y=H - 68)

    card(c, 22, H - 116, W - 44, 34, fill=Color(0.9, 0.2, 0.2, 0.1),
         stroke=HexColor("#E74C3C"), lw=1.5)
    txt(c, "⚠  If you have any concern about your baby's breathing, weight gain, or comfort, contact your paediatrician BEFORE applying any method.",
        30, H - 98, "Helvetica-Oblique", 8.5, HexColor("#C0392B"))

    sections_data = [
        ("THE SLEEP SURFACE", [
            "Firm, flat mattress — no incline, pillow-top, or wedge",
            "Fitted sheet only — no loose blankets, bumpers, or pillows",
            "No stuffed animals, positioners, or sleep aids inside the crib",
            "Sleep sack used in place of a blanket (correct tog for room temp)",
            "Baby placed on their BACK for every sleep, every time",
            "Crib, bassinet, or play yard only — not swing, car seat, or bouncer",
        ]),
        ("THE ROOM", [
            "Room temperature 68–72°F / 20–22°C confirmed",
            "Baby's chest warm but NOT sweaty",
            "True blackout — cannot see hand in front of face",
            "White noise running at low, continuous level (not inside crib)",
            "Monitor screen and LED indicators covered with electrical tape",
            "No nightlight, or red-spectrum light only",
        ]),
        ("ROOM-SHARING SETUP (if applicable)", [
            "Visual partition between your sleeping area and baby's",
            "Minimal light used during night feeds",
            "Separate sleep surface — not your bed",
            "AAP recommends room-sharing for first 6–12 months",
        ]),
    ]

    col_w2 = (W - 56) / 2
    sy_top = H - 134

    # Layout manually
    # Section 1 + 2 side by side, section 3 full width below
    s1_items = sections_data[0][1]
    s2_items = sections_data[1][1]
    s3_items = sections_data[2][1]

    s12_card_h = max(len(s1_items), len(s2_items)) * 28 + 50
    s12_y = H - 134 - s12_card_h
    s3_card_h = len(s3_items) * 28 + 50
    s3_y = s12_y - s3_card_h - 12

    for ci, (stitle, items) in enumerate([(sections_data[0][0], s1_items), (sections_data[1][0], s2_items)]):
        cx = 22 + ci * (col_w2 + 12)
        card(c, cx, s12_y, col_w2, s12_card_h, fill=CWHITE, stroke=CBORDER)
        c.setFillColor(CA)
        c.roundRect(cx, s12_y + s12_card_h - 26, col_w2, 26, 8, fill=1, stroke=0)
        txt(c, stitle, cx + col_w2 / 2, s12_y + s12_card_h - 14, "Helvetica-Bold", 9, CWHITE, "center")
        for ii, item in enumerate(items):
            iy = s12_y + s12_card_h - 54 - ii * 28
            cb(c, f"safe_{ci}_{ii}", cx + 10, iy - 2, size=14)
            txt(c, item, cx + 28, iy + 1, "Helvetica", 8.5, CINK)

    card(c, 22, s3_y, W - 44, s3_card_h, fill=CPANEL2, stroke=CA, lw=1.5)
    c.setFillColor(CA)
    c.roundRect(22, s3_y + s3_card_h - 26, W - 44, 26, 8, fill=1, stroke=0)
    txt(c, sections_data[2][0], (W) / 2, s3_y + s3_card_h - 14, "Helvetica-Bold", 9, CWHITE, "center")
    for ii, item in enumerate(s3_items):
        iy = s3_y + s3_card_h - 54 - ii * 28
        col = ii % 2
        ix = 22 + col * ((W - 44) / 2)
        cb(c, f"safe_2_{ii}", ix + 10, iy - 2, size=14)
        txt(c, item, ix + 28, iy + 1, "Helvetica", 8.5, CINK)

    # When to call doctor
    doctor_y = s3_y - 60
    card(c, 22, doctor_y, W - 44, 46, fill=Color(0.95, 0.4, 0.3, 0.1),
         stroke=HexColor("#E74C3C"))
    txt(c, "CALL YOUR PAEDIATRICIAN IF:", 34, doctor_y + 32,
        "Helvetica-Bold", 10, HexColor("#C0392B"))
    txt(c, "Fever during sleep training  •  Breathing seems irregular  •  Weight gain concerns  •  Any doubt about physical comfort",
        34, doctor_y + 14, "Helvetica", 9, CINK)

    # Nav
    bw, bh = 160, 28
    c.setFillColor(CA2)
    c.roundRect(W - bw - 22, 22, bw, bh, bh / 2, fill=1, stroke=0)
    txt(c, "Sleep Promise →", W - bw / 2 - 22, 31, "Helvetica-Bold", 9, CDARK, "center")
    c.linkAbsolute("promise", "promise", (W - bw - 22, 22, W - 22, 50), Border="[0 0 0]")


# ============================================================
#  SLEEP PROMISE
# ============================================================

def draw_promise(c):
    c.bookmarkPage("promise")
    bg(c, CDARK)
    nav_bar(c, "safe_sleep")
    footer(c, "", "")

    # Stars
    rng = random.Random(77)
    for _ in range(80):
        sx = rng.uniform(0, W)
        sy_star = rng.uniform(0, H)
        alpha = rng.uniform(0.05, 0.25)
        c.setFillColor(Color(1, 1, 1, alpha))
        c.circle(sx, sy_star, rng.uniform(0.5, 1.5), fill=1, stroke=0)

    # Gold moon glow
    c.setFillColor(Color(CA2.red, CA2.green, CA2.blue, 0.1))
    c.circle(W / 2, H - 60, 280, fill=1, stroke=0)

    txt(c, "Your Sleep Promise", W / 2, H - 72, "Helvetica-Bold", 30, CA2, "center")
    txt(c, "A commitment to your baby — and to yourself.", W / 2, H - 94,
        "Helvetica-Oblique", 11, Color(1, 1, 1, 0.6), "center")
    c.setStrokeColor(CA2)
    c.setLineWidth(1)
    c.line(W / 2 - 160, H - 104, W / 2 + 160, H - 104)

    promises = [
        "For the next seven days, I will keep bedtime simple and in the same order every night.",
        "I will watch awake windows and act on them — before overtiredness sets in.",
        "I will decide how I will respond to night wakings before the night begins.",
        "I will wait before I go in, and give my baby the chance to resettle.",
        "I will not judge the whole plan on the basis of one difficult night.",
        "I will stay consistent — especially on the nights when it is hardest.",
        "I will remember that I am not just surviving the night.",
        "I am teaching my baby a skill they will use for the rest of their life.",
    ]

    p_y = H - 136
    for pi, promise in enumerate(promises):
        cb(c, f"promise_{pi}", 50, p_y - 4, size=15, color=CA2)
        txt(c, promise, 72, p_y, "Helvetica", 10.5, CWHITE)
        p_y -= 42

    # Signature area
    card(c, 50, p_y - 60, W - 100, 88,
         fill=Color(CA2.red, CA2.green, CA2.blue, 0.08),
         stroke=Color(CA2.red, CA2.green, CA2.blue, 0.4))
    txt(c, "Signed:", 70, p_y + 14, "Helvetica-Oblique", 11, Color(1, 1, 1, 0.6))
    tf(c, "signature_parent", 120, p_y + 8, 160, 22, size=13)
    txt(c, "   Date:", 290, p_y + 14, "Helvetica-Oblique", 11, Color(1, 1, 1, 0.6))
    tf(c, "signature_date", 330, p_y + 8, 100, 22, size=13)
    txt(c, "   For:", 440, p_y + 14, "Helvetica-Oblique", 11, Color(1, 1, 1, 0.6))
    tf(c, "signature_baby", 470, p_y + 8, 80, 22, size=13)

    txt(c, '"Sleep is coming. For both of you."', W / 2, p_y - 26,
        "Helvetica-Oblique", 13, CA2, "center")
    txt(c, "— Six & Thriving", W / 2, p_y - 46,
        "Helvetica", 10, Color(1, 1, 1, 0.45), "center")

    # Back to welcome
    bw, bh = 180, 32
    bx, by = W / 2 - bw / 2, 32
    c.setFillColor(CA2)
    c.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    txt(c, "← Back to Welcome", W / 2, by + 11, "Helvetica-Bold", 10, CDARK, "center")
    c.linkAbsolute("welcome", "welcome", (bx, by, bx + bw, by + bh), Border="[0 0 0]")


# ============================================================
#  MAIN
# ============================================================

def main():
    out = C.OUTPUT
    cv = canvas.Canvas(out, pagesize=(W, H))
    cv.setTitle(C.SUBTITLE)
    cv.setAuthor(C.BRAND)
    cv.setSubject("Interactive Baby Sleep Personality Planner")

    pages = [
        ("cover",          draw_cover,          "Cover"),
        ("welcome",        draw_welcome,         "Welcome"),
        ("quiz",           draw_quiz,            "Personality Quiz"),
        ("snacker",        lambda cv: draw_personality(cv, "snacker"),        "The Snacker"),
        ("overthinker",    lambda cv: draw_personality(cv, "overthinker"),    "The Overthinker"),
        ("sensitive",      lambda cv: draw_personality(cv, "sensitive"),      "The Sensitive Soul"),
        ("nightowl",       lambda cv: draw_personality(cv, "nightowl"),       "The Night Owl"),
        ("catnapper",      lambda cv: draw_personality(cv, "catnapper"),      "The Catnapper"),
        ("party_animal",   lambda cv: draw_personality(cv, "party_animal"),   "The Party Animal"),
        ("action_plan",    draw_action_plan,     "Action Plan"),
        ("sleep_tracker",  draw_sleep_tracker,   "Sleep Tracker"),
        ("bedtime_builder",draw_bedtime_builder, "Bedtime Builder"),
        ("safe_sleep",     draw_safe_sleep,      "Safe Sleep"),
        ("promise",        draw_promise,         "Sleep Promise"),
    ]

    for pid, drawer, label in pages:
        print(f"  Drawing: {label}...")
        drawer(cv)
        cv.showPage()

    cv.save()
    print(f"\n✓ Saved → {out}  ({len(pages)} pages)")


if __name__ == "__main__":
    main()
