# night_waking_response_planner.py
# Premium Interactive PDF — Night Waking Response Planner
# Based on Chapter 7: Sleep, Baby. Please.
# Requires: pip install reportlab

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
import os

PAGE_W, PAGE_H = LETTER
M = 44  # margin

# ─────────────────────────── PALETTE ───────────────────────────────────────

P = {
    "bg":         HexColor("#0C1220"),   # near-black indigo
    "bg2":        HexColor("#101828"),   # slightly lighter bg
    "card":       HexColor("#16213A"),   # card surface
    "card2":      HexColor("#1A2848"),   # alternate card
    "card3":      HexColor("#1E2F52"),   # highlight card
    "navy":       HexColor("#1C3160"),   # deep navy
    "navy_l":     HexColor("#243A70"),   # lighter navy accent
    "gold":       HexColor("#C8943A"),   # warm gold
    "gold_l":     HexColor("#E8B86D"),   # light gold
    "gold_dim":   HexColor("#7A5A22"),   # muted gold
    "amber":      HexColor("#D4773C"),   # amber/warm orange
    "blush":      HexColor("#B87070"),   # soft blush rose
    "mint":       HexColor("#5AADA8"),   # teal mint
    "lavender":   HexColor("#8878C8"),   # soft purple
    "cream":      HexColor("#EDE5D4"),   # warm cream
    "cream_dim":  HexColor("#C4B89A"),   # dimmed cream
    "muted":      HexColor("#7A90B0"),   # muted blue-grey
    "dim":        HexColor("#3A5070"),   # dim text
    "rule":       HexColor("#253550"),   # divider
    "input_bg":   HexColor("#F8F6F2"),   # input background (light)
    "input_bd":   HexColor("#C8943A"),   # input border
    "white":      white,
    "black":      black,
}

# ─────────────────────────── CONTENT ───────────────────────────────────────

WAKING_TYPES = [
    {
        "id": "hunger",
        "icon": "🍼",
        "label": "Hunger / Nutritional Waking",
        "desc": "Baby genuinely needs a feed. Usually before 6–9 months.",
        "cues": [
            "Rhythmic, escalating cry — not easily soothed",
            "Rooting reflex / mouthing movements",
            "Short time since last feed relative to age",
            "Under 6 months or post-growth-spurt",
        ],
        "plan_prompt": "My response plan for hunger wakings:",
        "plan_hint": "e.g. Feed fully in dim room. No stimulation. Back down drowsy-awake.",
        "key": "hunger",
    },
    {
        "id": "habit",
        "icon": "🔁",
        "label": "Habit / Association Waking",
        "desc": "Baby wakes expecting the same conditions they fell asleep with.",
        "cues": [
            "Waking at predictable, regular intervals (often ~45 min or 90 min)",
            "Calms immediately when the association is offered",
            "Old enough that hunger is unlikely (6+ months)",
            "Fed or rocked to sleep at bedtime",
        ],
        "plan_prompt": "My response plan for habit/association wakings:",
        "plan_hint": "e.g. Wait 3 min. Do not feed. Use chosen method to resettle.",
        "key": "habit",
    },
    {
        "id": "comfort",
        "icon": "🤗",
        "label": "Comfort / Connection Waking",
        "desc": "Baby wants closeness, not food or a specific habit.",
        "cues": [
            "Quiets with touch or voice — not specific feed/rock",
            "More common during developmental leaps or illness",
            "May have been a well-settled sleeper before this",
            "Calms with brief reassurance then re-settles",
        ],
        "plan_prompt": "My response plan for comfort wakings:",
        "plan_hint": "e.g. Pat/shush in crib. 2 min voice only. Exit once calm.",
        "key": "comfort",
    },
    {
        "id": "developmental",
        "icon": "🧠",
        "label": "Developmental / Leap Waking",
        "desc": "Temporary regression tied to a growth or brain leap.",
        "cues": [
            "Sudden return of waking after a settled period",
            "Increased fussiness or clingyness during the day",
            "Near a known leap window (4 mo, 6 mo, 8–10 mo, 12 mo…)",
            "Lasts 1–3 weeks then resolves",
        ],
        "plan_prompt": "My response plan for developmental wakings:",
        "plan_hint": "e.g. Offer extra comfort. Maintain routine. Ride it out 1–2 weeks.",
        "key": "developmental",
    },
    {
        "id": "environment",
        "icon": "🌡️",
        "label": "Environmental Waking",
        "desc": "External factor woke or kept the baby awake.",
        "cues": [
            "Woke at an unusual time / not their pattern",
            "Room too hot, too cold, or too light",
            "External noise — traffic, sibling, alarm",
            "White noise failed or isn't loud enough",
        ],
        "plan_prompt": "My response plan for environmental wakings:",
        "plan_hint": "e.g. Check room temp, white noise. Resettle with minimal interaction.",
        "key": "environmental",
    },
    {
        "id": "overtired",
        "icon": "😩",
        "label": "Overtired / Undertired Waking",
        "desc": "Sleep timing is off — too much or too little sleep pressure.",
        "cues": [
            "Overtired: hard to settle, wakes shortly after going down",
            "Undertired: wakes after a full cycle and can't go back",
            "Awake windows not matching baby's current developmental stage",
            "Nap timing or length is off",
        ],
        "plan_prompt": "My response plan for timing-related wakings:",
        "plan_hint": "e.g. Review awake windows. Adjust bedtime by 15 min tomorrow.",
        "key": "timing",
    },
    {
        "id": "pain",
        "icon": "😢",
        "label": "Pain / Illness / Discomfort",
        "desc": "Physical cause that needs to be ruled out first.",
        "cues": [
            "Inconsolable cry — nothing helps",
            "Signs of illness (fever, congestion, rash)",
            "Teething symptoms (drool, gum rubbing)",
            "Unusual body language — pulling ears, arching",
        ],
        "plan_prompt": "My response plan for pain/illness wakings:",
        "plan_hint": "e.g. Comfort fully. Address medical needs. Resume routine once recovered.",
        "key": "pain",
    },
]

WAIT_OPTIONS = [
    ("0–1 min", "Respond quickly — we're early in training"),
    ("2–3 min", "Standard pause — give self-settling a chance"),
    ("3–5 min", "Extended pause — well-established sleeper"),
    ("5+ min", "Following graduated method strictly"),
]

METHODS = [
    ("Extinction (CIO)",       "No check-ins. Go in only for morning or planned feed."),
    ("Ferber (Graduated)",     "Timed check-ins at increasing intervals."),
    ("Chair Method",           "Sit near crib. Move chair further every 2–3 nights."),
    ("Fading",                 "Gradually reduce involvement each night."),
    ("Pick Up / Put Down",     "Lift when crying; place down when calm. Repeat."),
]

REVIEW_QUESTIONS = [
    ("Which wakings self-settled without my help?",
     "Note the type and time — this reveals what they can already do."),
    ("Which wakings genuinely needed intervention?",
     "Hunger and pain always do. Habit/comfort often don't."),
    ("Did I respond consistently with my written plan?",
     "Yes/No. If No — what changed, and why?"),
    ("What pattern am I seeing across multiple nights?",
     "Same time every night? Same type? This shapes tomorrow's plan."),
    ("One thing to adjust in my plan based on this week:",
     "Small, specific change only. One lever at a time."),
]

NIGHT_LOG_FIELDS = [
    ("Time Woke",   "time_woke"),
    ("Duration",    "duration"),
    ("Waking Type", "type_guess"),
    ("My Response", "response"),
    ("Self-Settled?","settled_alone"),
    ("Time Back",   "time_back"),
]

AFFIRMATIONS = [
    "You wrote the plan in daylight so your exhausted brain doesn't have to decide at 2 a.m.",
    "A consistent response — even an imperfect one — is infinitely better than a different one every night.",
    "Pause before you go. Many wakings resolve in 2–3 minutes on their own.",
    "You are not failing your baby. You are teaching them the most important sleep skill of their life.",
    "Progress is not a straight line. One hard night does not erase five good ones.",
    "The goal isn't a perfect night. It's a more predictable, more confident response to whatever comes.",
    "Sleep is coming. For both of you.",
]

# ─────────────────────────── PDF ENGINE ────────────────────────────────────

class NightWakingPDF:
    def __init__(self, filename="night_waking_response_planner.pdf"):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.c.setTitle("Night Waking Response Planner")
        self.c.setAuthor("Sleep, Baby. Please. — Chapter 7 Companion")
        self.c.setSubject("Pre-write your night response plan. Break the habit cycle.")
        self.form = self.c.acroForm
        self.page_num = 0
        self._field_counter = 0

    # ─────────── unique field name helper ───────────
    def _uid(self, base):
        self._field_counter += 1
        return f"{base}_{self._field_counter}"

    # ─────────── page management ───────────
    def new_page(self, section_title=None, bookmark=None):
        if self.page_num > 0:
            self._draw_footer()
            self.c.showPage()
        self.page_num += 1
        # full dark background
        self.c.setFillColor(P["bg"])
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        # subtle top accent stripe
        self.c.setFillColor(P["navy"])
        self.c.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)

        if bookmark:
            self.c.bookmarkPage(bookmark)
            if section_title:
                self.c.addOutlineEntry(section_title, bookmark, level=0, closed=False)

    def _draw_footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.setLineWidth(0.5)
        self.c.line(M, 28, PAGE_W - M, 28)
        self.c.setFillColor(P["dim"])
        self.c.setFont("Helvetica", 7.5)
        self.c.drawString(M, 16, "Night Waking Response Planner  ·  Chapter 7 Companion  ·  Sleep, Baby. Please.")
        self.c.setFillColor(P["gold_dim"])
        self.c.setFont("Helvetica-Bold", 7.5)
        self.c.drawRightString(PAGE_W - M, 16, f"— {self.page_num} —")

    # ─────────── drawing primitives ───────────
    def _bg_rect(self, x, y, w, h, fill="card", radius=10, stroke_col=None, stroke_w=0.8):
        self.c.setFillColor(P[fill])
        if stroke_col:
            self.c.setStrokeColor(stroke_col)
            self.c.setLineWidth(stroke_w)
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
        else:
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

    def _label(self, x, y, text, size=8.5, color="muted", font="Helvetica-Bold"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawString(x, y, text)

    def _text(self, x, y, text, size=10, color="cream", font="Times-Roman", max_w=None, leading=None):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        leading = leading or (size * 1.4)
        if not max_w:
            self.c.drawString(x, y, text)
            return y - leading
        lines = simpleSplit(text, font, size, max_w)
        yy = y
        for ln in lines:
            self.c.drawString(x, yy, ln)
            yy -= leading
        return yy

    def _centered(self, y, text, size=12, color="cream", font="Times-Roman"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawCentredString(PAGE_W / 2, y, text)

    def _rule(self, y, x1=None, x2=None, color="rule", w=0.5):
        self.c.setStrokeColor(P[color] if isinstance(P[color], Color) else P[color])
        self.c.setLineWidth(w)
        self.c.line(x1 or M, y, x2 or PAGE_W - M, y)

    def _gold_pill(self, x, y, text, size=8):
        tw = stringWidth(text, "Helvetica-Bold", size)
        pw, ph = tw + 14, 16
        self.c.setFillColor(P["gold_dim"])
        self.c.roundRect(x, y - 2, pw, ph, 5, fill=1, stroke=0)
        self.c.setFillColor(P["gold_l"])
        self.c.setFont("Helvetica-Bold", size)
        self.c.drawString(x + 7, y + 5, text)

    def _section_header(self, title, subtitle="", tag=None, y_top=None):
        y = y_top or (PAGE_H - 52)
        self._bg_rect(M, y - 44, PAGE_W - 2*M, 58, fill="navy", radius=12)
        # left gold accent bar
        self.c.setFillColor(P["gold"])
        self.c.roundRect(M, y - 44, 5, 58, 3, fill=1, stroke=0)
        if tag:
            self._gold_pill(M + 20, y + 2, tag)
        self.c.setFillColor(P["gold_l"])
        self.c.setFont("Times-Bold", 20)
        self.c.drawString(M + 20, y - 14, title)
        if subtitle:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 10)
            self.c.drawString(M + 20, y - 30, subtitle)

    # ─────────── nav buttons ───────────
    def _nav_btn(self, x, y, w, h, text, dest, fill="card2", txt="gold_l", size=9):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
        self.c.setFillColor(P[txt])
        self.c.setFont("Helvetica-Bold", size)
        tw = stringWidth(text, "Helvetica-Bold", size)
        self.c.drawString(x + (w - tw) / 2, y + h / 2 - 3.5, text)
        self.c.linkRect("", dest, (x, y, x + w, y + h), relative=0, thickness=0)

    def _top_nav(self, prev=None, nxt=None, home="cover"):
        y = 42
        if prev:
            self._nav_btn(M, y, 100, 20, "◀  Previous", prev, fill="card2")
        self._nav_btn(PAGE_W/2 - 50, y, 100, 20, "⌂  Home", home, fill="navy")
        if nxt:
            self._nav_btn(PAGE_W - M - 100, y, 100, 20, "Next  ▶", nxt, fill="gold", txt="bg")

    # ─────────── form helpers ───────────
    def _field(self, name, x, y, w, h=20, multiline=False, font_size=10, value="", tooltip=None):
        self.form.textfield(
            name=name, tooltip=tooltip or name,
            x=x, y=y, width=w, height=h,
            borderStyle='inset',
            borderColor=P["input_bd"],
            fillColor=P["input_bg"],
            textColor=P["black"],
            forceBorder=True,
            value=value,
            fontName="Helvetica",
            fontSize=font_size,
            fieldFlags='multiline' if multiline else '',
        )

    def _checkbox(self, name, x, y, size=14, checked=False, tooltip=None):
        self.form.checkbox(
            name=name, tooltip=tooltip or name,
            x=x, y=y, size=size, checked=checked,
            buttonStyle='check',
            borderColor=P["gold"],
            fillColor=P["input_bg"],
            textColor=P["gold"],
            forceBorder=True,
        )

    def _radio(self, group, value, x, y, size=13, selected=False, tooltip=None):
        self.form.radio(
            name=group, tooltip=tooltip or group,
            value=value, selected=selected,
            x=x, y=y, buttonStyle='circle',
            borderColor=P["gold"],
            fillColor=P["input_bg"],
            textColor=P["gold"],
            forceBorder=True,
            size=size,
        )

    def _labeled_field(self, x, y, w, label, name, h=22, multiline=False, font_size=10, tooltip=None):
        self._label(x, y + h + 5, label, size=8)
        fh = h if not multiline else h
        self._field(name, x, y, w, fh, multiline=multiline, font_size=font_size, tooltip=tooltip)

    def _check_row(self, x, y, name, label, size=13, label_color="cream", label_size=10, max_w=440):
        self._checkbox(name, x, y - 1, size=size)
        self._text(x + size + 8, y + 1, label, size=label_size, color=label_color, max_w=max_w)
        return y - 22

    # ═══════════════════════════════════════════════════════════
    # PAGE: COVER
    # ═══════════════════════════════════════════════════════════
    def page_cover(self):
        self.new_page("Cover", "cover")

        # diagonal ambient glow — top right
        self.c.setFillColor(HexColor("#1C3160"))
        self.c.ellipse(350, PAGE_H - 80, PAGE_W + 80, PAGE_H + 100, fill=1, stroke=0)

        # moon circle decoration
        self.c.setFillColor(HexColor("#1A2848"))
        self.c.circle(PAGE_W - 90, PAGE_H - 110, 80, fill=1, stroke=0)
        self.c.setFillColor(P["bg"])
        self.c.circle(PAGE_W - 60, PAGE_H - 100, 76, fill=1, stroke=0)

        # stars (small gold dots)
        import random
        random.seed(42)
        for _ in range(28):
            sx = random.randint(40, int(PAGE_W) - 40)
            sy = random.randint(int(PAGE_H) - 280, int(PAGE_H) - 30)
            sr = random.uniform(0.8, 2.0)
            alpha_factor = random.uniform(0.3, 1.0)
            star_col = HexColor("#C8943A") if alpha_factor > 0.6 else HexColor("#3A5070")
            self.c.setFillColor(star_col)
            self.c.circle(sx, sy, sr, fill=1, stroke=0)

        # main title card
        self._bg_rect(M, PAGE_H - 380, PAGE_W - 2*M, 300, fill="navy", radius=16)
        self.c.setFillColor(P["gold"])
        self.c.roundRect(M, PAGE_H - 380, 6, 300, 4, fill=1, stroke=0)

        # CHAPTER 7 tag
        self._gold_pill(M + 24, PAGE_H - 118, "CHAPTER 7  ·  SLEEP, BABY. PLEASE.", size=8.5)

        self.c.setFillColor(P["gold_l"])
        self.c.setFont("Times-Bold", 32)
        self.c.drawString(M + 24, PAGE_H - 158, "Night Waking")

        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Bold", 32)
        self.c.drawString(M + 24, PAGE_H - 196, "Response Planner")

        self._rule(PAGE_H - 210, M + 24, PAGE_W - M - 24, color="gold_dim", w=1.2)

        self.c.setFillColor(P["muted"])
        self.c.setFont("Times-Italic", 12)
        tagline = "Pre-write your plan. Your tired brain just has to follow it."
        self.c.drawString(M + 24, PAGE_H - 232, tagline)

        desc_lines = [
            "7 waking types  ·  Response scripts  ·  7-night log",
            "Self-settling tracker  ·  Weekly review  ·  Pattern finder",
        ]
        y = PAGE_H - 260
        for ln in desc_lines:
            self.c.setFillColor(P["cream_dim"])
            self.c.setFont("Helvetica", 10)
            self.c.drawString(M + 24, y, ln)
            y -= 18

        # quick nav buttons
        btns = [
            ("How to Use", "how_to"),
            ("My Plan Overview", "plan_overview"),
            ("Night 1 Log", "night_log_1"),
            ("Weekly Review", "week_review"),
        ]
        bx = M + 24
        btn_y = PAGE_H - 400
        for label, dest in btns:
            self._nav_btn(bx, btn_y, 110, 24, label, dest,
                         fill="card3" if label != "How to Use" else "gold",
                         txt="bg" if label == "How to Use" else "gold_l")
            bx += 118

        # bottom card — key insight
        self._bg_rect(M, 100, PAGE_W - 2*M, 80, fill="card", radius=12,
                     stroke_col=P["gold_dim"])
        self.c.setFillColor(P["gold"])
        self.c.setFont("Times-Italic", 11)
        self.c.drawCentredString(PAGE_W/2, 162, "\"The plan you write at 2 p.m. is the one your 2 a.m. brain will thank you for.\"")
        self.c.setFillColor(P["dim"])
        self.c.setFont("Helvetica", 8.5)
        self.c.drawCentredString(PAGE_W/2, 142, "— Sleep, Baby. Please. · Chapter 7")

        self.c.setFillColor(P["blush"])
        self.c.setFont("Times-Roman", 10)
        self.c.drawCentredString(PAGE_W/2, 74, "Six & Thriving  ·  sleepbabyplease.com")

    # ═══════════════════════════════════════════════════════════
    # PAGE: HOW TO USE
    # ═══════════════════════════════════════════════════════════
    def page_how_to(self):
        self.new_page("How to Use", "how_to")
        self._section_header(
            "How to Use This Planner",
            "A plan written before the night beats decisions made in the dark.",
            tag="START HERE"
        )

        self._bg_rect(M, 120, PAGE_W - 2*M, 500, fill="card", radius=12)

        steps = [
            ("1", "Read Chapter 7 first",
             "This planner is the hands-on companion. The chapter explains the why; this planner captures your what."),
            ("2", "Identify your baby's waking types",
             "Pages 3–9 walk through each type. Read the cues. Check off what applies."),
            ("3", "Write your response plan — in daylight",
             "For each waking type, write exactly what you will do. Specific, step-by-step."),
            ("4", "Log every night for 7 nights",
             "Pages 10–16 give you a full log for each night. Patterns only appear with data."),
            ("5", "Review on Day 7",
             "The weekly review (page 17) separates genuine needs from habit wakings."),
        ]

        y = 580
        for num, title, desc in steps:
            # number badge
            self.c.setFillColor(P["gold"])
            self.c.roundRect(M + 18, y - 8, 26, 26, 6, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 13)
            self.c.drawCentredString(M + 31, y + 4, num)

            self.c.setFillColor(P["gold_l"])
            self.c.setFont("Times-Bold", 12)
            self.c.drawString(M + 56, y + 6, title)

            y = self._text(M + 56, y - 10, desc, size=10, color="cream_dim",
                          font="Times-Roman", max_w=PAGE_W - 2*M - 80)
            y -= 18

        # key principles box
        self._bg_rect(M, 50, PAGE_W - 2*M, 62, fill="card3", radius=10,
                     stroke_col=P["navy_l"])
        self._label(M + 18, 100, "The two rules this planner is built on:", size=9.5, color="gold_l")
        self._text(M + 18, 84, "① Pause 2–3 minutes before going in. Many wakings self-resolve.", size=10, color="cream")
        self._text(M + 18, 66, "② Decide your response before the waking happens — not during it.", size=10, color="cream")

        self._top_nav(prev="cover", nxt="plan_overview")

    # ═══════════════════════════════════════════════════════════
    # PAGE: PLAN OVERVIEW (baby + method setup)
    # ═══════════════════════════════════════════════════════════
    def page_plan_overview(self):
        self.new_page("My Plan Overview", "plan_overview")
        self._section_header(
            "My Night Response Plan — Setup",
            "Fill this before the first night. Post it where you can see it.",
            tag="PLAN SETUP"
        )

        # ── Baby details ──
        self._bg_rect(M, 570, PAGE_W - 2*M, 120, fill="card", radius=12)
        self._label(M + 18, 672, "Baby's Details", size=11, color="gold_l")
        self._labeled_field(M + 18, 620, 180, "Baby's Name", "overview_baby_name")
        self._labeled_field(M + 218, 620, 130, "Age Right Now", "overview_baby_age")
        self._labeled_field(M + 368, 620, 120, "Planner Start Date", "overview_start_date")
        self._labeled_field(M + 18, 578, 200, "Current Sleep Challenge (one line)", "overview_challenge",
                           tooltip="What's the main sleep issue you're trying to solve?")
        self._labeled_field(M + 238, 578, 250, "Biggest Habit to Break", "overview_habit",
                           tooltip="e.g. fed to sleep, rocked fully to sleep, brought to bed")

        # ── Wait policy ──
        self._bg_rect(M, 470, PAGE_W - 2*M, 90, fill="card2", radius=12)
        self._label(M + 18, 548, "My Wait-Before-I-Go Policy", size=11, color="gold_l")
        self._text(M + 18, 532, "How long will I pause before entering the room when I hear a sound?",
                  size=9.5, color="muted", max_w=430)
        x = M + 18
        for i, (label, desc) in enumerate(WAIT_OPTIONS):
            self._radio("wait_policy", f"w{i}", x, 490, selected=(i == 1))
            self._text(x + 18, 494, label, size=9.5, color="gold_l")
            self._text(x + 18, 482, desc, size=8, color="cream_dim")
            x += 128

        # ── Chosen method ──
        self._bg_rect(M, 370, PAGE_W - 2*M, 90, fill="card", radius=12)
        self._label(M + 18, 448, "My Chosen Sleep Method (from Chapter 6)", size=11, color="gold_l")
        x = M + 18
        for i, (name, principle) in enumerate(METHODS):
            col_x = M + 18 + (i % 3) * 172
            row_y = 420 if i < 3 else 395
            self._radio("chosen_method", f"m{i}", col_x, row_y, selected=(i == 1))
            self._text(col_x + 18, row_y + 2, name, size=9, color="cream")

        self._label(M + 18, 378, "Method note:", size=8, color="muted")
        self._field("overview_method_note", M + 90, 372, 380, 18, font_size=9)

        # ── What I will NOT do ──
        self._bg_rect(M, 240, PAGE_W - 2*M, 122, fill="navy", radius=12)
        self._label(M + 18, 350, "Sleep Debt Traps I Am Actively Avoiding", size=11, color="amber")
        self._text(M + 18, 334, "Check what you're committing to avoid (after the first few months):",
                  size=9.5, color="cream_dim")
        traps = [
            "Feeding to sleep at bedtime",
            "Rocking fully to sleep at bedtime",
            "Bringing baby to our bed as a night rescue",
            "Rushing in before the wait window",
            "Switching methods mid-week",
            "Using motion sleep (swing/pram) for all naps",
        ]
        y = 314
        for i, trap in enumerate(traps):
            col_x = M + 18 if i % 2 == 0 else M + 258
            row_y = y - (i // 2) * 24
            self._checkbox(f"trap_{i}", col_x, row_y - 1, size=12,
                          tooltip=f"Avoiding: {trap}")
            self._text(col_x + 18, row_y + 1, trap, size=9, color="cream")

        # ── Partner sync ──
        self._bg_rect(M, 120, PAGE_W - 2*M, 112, fill="card2", radius=12)
        self._label(M + 18, 220, "Partner / Co-Parent Sync", size=11, color="gold_l")
        self._labeled_field(M + 18, 174, 200, "Who handles odd nights?", "partner_odd")
        self._labeled_field(M + 238, 174, 260, "Who handles even nights?", "partner_even")
        self._labeled_field(M + 18, 130, 480, "One agreed rule we both follow if the other deviates:", "partner_rule",
                           tooltip="e.g. Text before going in. Never rock past 5 minutes.")

        self._top_nav(prev="how_to", nxt="waking_type_1")

    # ═══════════════════════════════════════════════════════════
    # PAGES: WAKING TYPE RESPONSE PLANS (7 types)
    # ═══════════════════════════════════════════════════════════
    def page_waking_type(self, idx, data, prev_dest, next_dest):
        bookmark = f"waking_type_{idx+1}"
        self.new_page(data["label"], bookmark)

        # colored top accent for this type
        accent_colors = ["mint", "lavender", "blush", "gold", "amber", "gold_l", "cream_dim"]
        accent = P.get(accent_colors[idx % len(accent_colors)], P["gold"])

        self._section_header(
            data["label"],
            data["desc"],
            tag=f"WAKING TYPE {idx+1} OF {len(WAKING_TYPES)}"
        )

        # ── Cue recognition card ──
        self._bg_rect(M, 500, PAGE_W - 2*M, 148, fill="card", radius=12)
        self._label(M + 18, 636, "How to Recognise This Waking", size=11, color="gold_l")
        self._text(M + 18, 619, "Check all cues that apply to your baby right now:", size=9.5, color="muted")

        y = 598
        for i, cue in enumerate(data["cues"]):
            self._checkbox(f"wt{idx}_cue_{i}", M + 18, y - 2, size=12, tooltip=cue)
            y = self._text(M + 38, y, cue, size=10, color="cream", max_w=440)
            y -= 6

        # applies badge
        self._label(M + 18, 510, "Does this type apply to my baby currently?", size=9, color="muted")
        self._radio(f"wt{idx}_applies", "yes", M + 280, 508, size=13, selected=True)
        self._text(M + 298, 511, "Yes — I need a plan for this", size=9, color="cream")
        self._radio(f"wt{idx}_applies", "no", M + 420, 508, size=13)
        self._text(M + 438, 511, "Not yet", size=9, color="muted")

        # ── Response plan card ──
        self._bg_rect(M, 310, PAGE_W - 2*M, 182, fill="card2", radius=12,
                     stroke_col=accent, stroke_w=0.6)
        self._label(M + 18, 480, data["plan_prompt"], size=11, color="gold_l")
        self._text(M + 18, 463, "Write your step-by-step response. Be specific. Your tired brain will follow this exactly.",
                  size=9.5, color="muted")

        # step-by-step fields
        steps_label = ["Step 1 — First action (in room or out?):",
                       "Step 2 — If not settled after wait window:",
                       "Step 3 — If still not settled after 10 min:"]
        sy = 438
        for si, slabel in enumerate(steps_label):
            self._label(M + 18, sy, slabel, size=8.5, color="cream_dim")
            self._field(f"wt{idx}_step_{si+1}", M + 18, sy - 26, PAGE_W - 2*M - 36, 22,
                       font_size=10, tooltip=slabel)
            sy -= 52

        # hint
        self.c.setFillColor(P["dim"])
        self.c.setFont("Times-Italic", 9)
        self.c.drawString(M + 18, 318, f"Hint: {data['plan_hint']}")

        # ── When to escalate card ──
        self._bg_rect(M, 200, PAGE_W - 2*M, 102, fill="card", radius=12)
        self._label(M + 18, 290, "When This Waking Gets Flagged for Review", size=10.5, color="gold_l")
        self._text(M + 18, 272,
                  "I will escalate / reassess if this waking type occurs more than:",
                  size=9.5, color="muted", max_w=300)
        self._radio(f"wt{idx}_escalate", "2", M + 320, 270, size=12, selected=True)
        self._text(M + 337, 273, "2×/night", size=9)
        self._radio(f"wt{idx}_escalate", "3", M + 390, 270, size=12)
        self._text(M + 407, 273, "3×/night", size=9)
        self._radio(f"wt{idx}_escalate", "4", M + 455, 270, size=12)
        self._text(M + 472, 273, "4+×/night", size=9)

        self._label(M + 18, 244, "If this waking type persists unchanged for more than 7 days, I will:", size=8.5, color="muted")
        self._field(f"wt{idx}_escalate_plan", M + 18, 212, PAGE_W - 2*M - 36, 22,
                   font_size=10, tooltip="What will you do if this waking type persists?")

        # ── Affirmation strip ──
        self._bg_rect(M, 88, PAGE_W - 2*M, 44, fill="navy", radius=8)
        aff = AFFIRMATIONS[idx % len(AFFIRMATIONS)]
        self.c.setFillColor(P["gold_l"])
        self.c.setFont("Times-Italic", 10)
        self.c.drawCentredString(PAGE_W/2, 108, '201c' + aff + '201d')

        self._top_nav(prev=prev_dest, nxt=next_dest)

    # ═══════════════════════════════════════════════════════════
    # PAGES: NIGHT LOG (7 nights)
    # ═══════════════════════════════════════════════════════════
    def page_night_log(self, night_num, prev_dest, next_dest):
        bookmark = f"night_log_{night_num}"
        self.new_page(f"Night {night_num} Log", bookmark)
        self._section_header(
            f"Night {night_num} — Waking Log",
            f"Record every waking. Honest data reveals the pattern.",
            tag=f"NIGHT {night_num} OF 7"
        )

        n = night_num

        # ── Night setup ──
        self._bg_rect(M, 580, PAGE_W - 2*M, 80, fill="card", radius=12)
        self._label(M + 18, 648, "Night Setup", size=11, color="gold_l")
        self._labeled_field(M + 18, 596, 120, "Date", f"n{n}_date")
        self._labeled_field(M + 158, 596, 100, "Bedtime", f"n{n}_bedtime")
        self._labeled_field(M + 278, 596, 100, "Time Asleep", f"n{n}_asleep")
        self._labeled_field(M + 398, 596, 100, "Morning Wake", f"n{n}_morning")

        # ── Waking log rows ──
        self._bg_rect(M, 194, PAGE_W - 2*M, 378, fill="card2", radius=12)
        self._label(M + 18, 560, "Waking Log", size=11, color="gold_l")

        # header row
        self.c.setFillColor(P["navy"])
        self.c.roundRect(M + 10, 540, PAGE_W - 2*M - 20, 18, 4, fill=1, stroke=0)
        headers = [("Time", M+20), ("Type", M+72), ("My Response", M+180),
                   ("Self-Settled?", M+355), ("Back Down", M+436), ("Duration", M+502)]
        for h, hx in headers:
            self._label(hx, 543, h, size=7.5, color="gold_l")

        row_y = 520
        for w in range(1, 7):
            fill_key = "card" if w % 2 else "bg2"
            self._bg_rect(M + 10, row_y - 16, PAGE_W - 2*M - 20, 26, fill=fill_key, radius=4)

            self._label(M + 18, row_y - 6, f"#{w}", size=8, color="gold_dim")
            self._field(f"n{n}_w{w}_time",    M + 32,  row_y - 14, 38, 18, font_size=8.5)
            self._field(f"n{n}_w{w}_type",    M + 72,  row_y - 14, 102, 18, font_size=8.5,
                       tooltip="e.g. Habit, Hunger, Comfort, Developmental…")
            self._field(f"n{n}_w{w}_response",M + 176, row_y - 14, 174, 18, font_size=8.5,
                       tooltip="What exactly did you do?")

            self._radio(f"n{n}_w{w}_settled", "yes", M + 355, row_y - 12, size=11, selected=False)
            self._label(M + 370, row_y - 8, "Y", size=8.5, color="mint")
            self._radio(f"n{n}_w{w}_settled", "no", M + 388, row_y - 12, size=11)
            self._label(M + 403, row_y - 8, "N", size=8.5, color="blush")
            self._radio(f"n{n}_w{w}_settled", "partial", M + 416, row_y - 12, size=11)
            self._label(M + 431, row_y - 8, "P", size=8.5, color="amber")

            self._field(f"n{n}_w{w}_back",     M + 450, row_y - 14, 48, 18, font_size=8.5)
            self._field(f"n{n}_w{w}_duration", M + 502, row_y - 14, 44, 18, font_size=8.5)

            row_y -= 34

        # ── Followed my plan? ──
        self._label(M + 18, 202, "Did I follow my written response plan tonight?", size=9.5, color="muted")
        self._radio(f"n{n}_followed_plan", "fully", M + 260, 200, size=13, selected=True)
        self._label(M + 278, 204, "Fully", size=9.5, color="mint")
        self._radio(f"n{n}_followed_plan", "mostly", M + 320, 200, size=13)
        self._label(M + 338, 204, "Mostly", size=9.5, color="gold_l")
        self._radio(f"n{n}_followed_plan", "deviated", M + 385, 200, size=13)
        self._label(M + 403, 204, "Deviated", size=9.5, color="blush")

        # ── Notes ──
        self._bg_rect(M, 48, PAGE_W - 2*M, 90, fill="card", radius=12)
        self._label(M + 18, 128, "Night Notes", size=10, color="gold_l")
        self._text(M + 18, 111, "Anything that affected this night (illness, travel, deviation from plan):", size=9, color="muted")
        self._field(f"n{n}_notes", M + 18, 58, PAGE_W - 2*M - 36, 46, multiline=True, font_size=9.5,
                   tooltip="Night notes — anything unusual or relevant")

        self._top_nav(prev=prev_dest, nxt=next_dest)

    # ═══════════════════════════════════════════════════════════
    # PAGE: WEEKLY REVIEW
    # ═══════════════════════════════════════════════════════════
    def page_weekly_review(self):
        self.new_page("Weekly Review", "week_review")
        self._section_header(
            "7-Night Review — Pattern Finder",
            "Look at the data. Separate genuine needs from habit. Adjust one lever.",
            tag="WEEKLY REVIEW"
        )

        # ── Stats summary ──
        self._bg_rect(M, 556, PAGE_W - 2*M, 108, fill="card", radius=12)
        self._label(M + 18, 652, "7-Night Sleep Stats", size=11, color="gold_l")
        stat_fields = [
            ("Best night (fewest wakings)", "stat_best", M + 18, 612),
            ("Hardest night (most wakings)", "stat_hardest", M + 258, 612),
            ("Avg wakings / night", "stat_avg_wakings", M + 18, 570),
            ("Most common waking type", "stat_common_type", M + 258, 570),
            ("Longest uninterrupted stretch", "stat_longest_stretch", M + 458, 570),
        ]
        for label, fname, fx, fy in stat_fields:
            self._labeled_field(fx, fy, 190, label, fname, h=20, font_size=9.5)

        # ── Self-settling tracker ──
        self._bg_rect(M, 428, PAGE_W - 2*M, 120, fill="card2", radius=12)
        self._label(M + 18, 536, "Self-Settling Tracker", size=11, color="gold_l")
        self._text(M + 18, 518,
                  "For each night, mark how many wakings self-resolved (S) vs needed intervention (I):",
                  size=9.5, color="muted")

        days = ["N1", "N2", "N3", "N4", "N5", "N6", "N7"]
        dx = M + 18
        for i, day in enumerate(days):
            self._label(dx, 498, day, size=9, color="gold_l")
            self._label(dx, 484, "S:", size=8, color="muted")
            self._field(f"settle_s_{i+1}", dx + 14, 476, 38, 18, font_size=9)
            self._label(dx, 460, "I:", size=8, color="muted")
            self._field(f"settle_i_{i+1}", dx + 14, 452, 38, 18, font_size=9)
            dx += 72

        self._text(M + 18, 436, "Total self-settled across week:", size=9.5, color="muted")
        self._field("settle_total_s", M + 240, 430, 60, 18, font_size=10)
        self._text(M + 310, 436, "Total interventions:", size=9.5, color="muted")
        self._field("settle_total_i", M + 440, 430, 60, 18, font_size=10)

        # ── Review questions ──
        self._bg_rect(M, 50, PAGE_W - 2*M, 372, fill="card", radius=12)
        self._label(M + 18, 410, "Review Questions", size=11, color="gold_l")

        qy = 388
        for qi, (q, hint) in enumerate(REVIEW_QUESTIONS, start=1):
            self._bg_rect(M + 10, qy - 54, PAGE_W - 2*M - 20, 60, fill="card2", radius=8)
            self.c.setFillColor(P["gold_dim"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(M + 18, qy - 4, f"Q{qi}")
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 10)
            self.c.drawString(M + 36, qy - 4, q)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 9)
            self.c.drawString(M + 36, qy - 20, hint)
            self._field(f"review_q{qi}", M + 36, qy - 50, PAGE_W - 2*M - 60, 22, font_size=10,
                       tooltip=q)
            qy -= 68

        self._top_nav(prev="night_log_7", nxt="plan_v2")

    # ═══════════════════════════════════════════════════════════
    # PAGE: REVISED PLAN (v2 after review)
    # ═══════════════════════════════════════════════════════════
    def page_plan_v2(self):
        self.new_page("Revised Plan (Week 2)", "plan_v2")
        self._section_header(
            "Revised Response Plan — Week 2",
            "One plan, adjusted by evidence. Small changes. Committed execution.",
            tag="PLAN v2"
        )

        # ── What changed ──
        self._bg_rect(M, 530, PAGE_W - 2*M, 130, fill="card", radius=12)
        self._label(M + 18, 648, "What I'm Changing (and Why)", size=11, color="gold_l")
        self._text(M + 18, 630, "Only change things the data showed. One lever at a time.",
                  size=9.5, color="muted")

        change_fields = [
            ("Change to wait window (if any)", "v2_wait_change"),
            ("Change to method (if any)", "v2_method_change"),
            ("Waking type with biggest improvement last week", "v2_improved"),
            ("Waking type still needing the most work", "v2_still_hard"),
        ]
        fy = 610
        for i, (label, fname) in enumerate(change_fields):
            fx = M + 18 if i % 2 == 0 else M + 268
            row_y = fy if i < 2 else fy - 50
            self._labeled_field(fx, row_y, 230, label, fname, h=20, font_size=9.5)

        # ── Revised plans per type ──
        self._bg_rect(M, 130, PAGE_W - 2*M, 390, fill="card2", radius=12)
        self._label(M + 18, 508, "Revised Response Plan by Waking Type", size=11, color="gold_l")
        self._text(M + 18, 490,
                  "Update any type where last week's plan wasn't working. Leave blank if plan is unchanged.",
                  size=9.5, color="muted")

        compact_types = [
            ("Hunger / Nutritional", "rv_hunger"),
            ("Habit / Association", "rv_habit"),
            ("Comfort / Connection", "rv_comfort"),
            ("Developmental / Leap", "rv_developmental"),
            ("Environmental", "rv_environmental"),
            ("Timing / Over-Undertired", "rv_timing"),
            ("Pain / Illness", "rv_pain"),
        ]
        ty = 468
        for i, (label, fname) in enumerate(compact_types):
            col_x = M + 18 if i % 2 == 0 else M + 268
            row_y = ty - (i // 2) * 46
            self._label(col_x, row_y, label, size=8.5, color="cream_dim")
            self._field(fname, col_x, row_y - 26, 230, 22, font_size=9.5, tooltip=f"Revised plan: {label}")

        # ── Commitment strip ──
        self._bg_rect(M, 50, PAGE_W - 2*M, 72, fill="navy", radius=12,
                     stroke_col=P["gold_dim"])
        self._checkbox("v2_committed", M + 18, 94, size=16,
                      tooltip="I have re-read and committed to this plan")
        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Italic", 11)
        self.c.drawString(M + 44, 102, "I have updated this plan based on what I observed. I commit to 5 more consistent nights.")
        self._labeled_field(PAGE_W - M - 160, 58, 148, "Week 2 Start Date", "v2_start_date", h=18)

        self._top_nav(prev="week_review", nxt="quick_ref")

    # ═══════════════════════════════════════════════════════════
    # PAGE: QUICK REFERENCE CARD
    # ═══════════════════════════════════════════════════════════
    def page_quick_ref(self):
        self.new_page("Quick Reference Card", "quick_ref")
        self._section_header(
            "Quick Reference — Print & Post",
            "One page. Everything you need at 2 a.m.",
            tag="REFERENCE"
        )

        # ── Wait rule ──
        self._bg_rect(M, 588, PAGE_W - 2*M, 70, fill="navy", radius=12)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Times-Bold", 14)
        self.c.drawCentredString(PAGE_W/2, 640, "Rule #1 — Wait Before You Go")
        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Roman", 11)
        self.c.drawCentredString(PAGE_W/2, 618,
            "Hear a sound → pause 2–3 min → listen → is it escalating? → then decide.")
        self._field("qr_wait_note", M + 18, 596, PAGE_W - 2*M - 36, 16, font_size=9,
                   tooltip="My personal wait rule this week")

        # ── Waking type quick map ──
        self._bg_rect(M, 330, PAGE_W - 2*M, 250, fill="card", radius=12)
        self._label(M + 18, 568, "Waking Type → My Response (Summary)", size=11, color="gold_l")

        types_short = [
            ("🍼 Hunger",       "qr_hunger_resp",    "Under 6 mo: likely yes. Over 9 mo: likely habit."),
            ("🔁 Habit",         "qr_habit_resp",     "Don't offer the association. Use your method."),
            ("🤗 Comfort",       "qr_comfort_resp",   "Brief reassurance. Don't linger. Exit calmly."),
            ("🧠 Developmental", "qr_dev_resp",       "Temporary. Extra comfort OK. Hold the routine."),
            ("🌡️ Environmental", "qr_env_resp",       "Check room. Fix the cause. Resettle."),
            ("😩 Timing",        "qr_timing_resp",    "Note the time. Adjust tomorrow. Don't feed."),
            ("😢 Pain/Illness",  "qr_pain_resp",      "Comfort fully. Medical need first. Resume after."),
        ]

        ty = 544
        for i, (type_name, fname, hint) in enumerate(types_short):
            fill_k = "card2" if i % 2 == 0 else "bg2"
            self._bg_rect(M + 10, ty - 24, PAGE_W - 2*M - 20, 28, fill=fill_k, radius=4)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 9.5)
            self.c.drawString(M + 18, ty - 10, type_name)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7.5)
            self.c.drawString(M + 128, ty - 10, hint)
            self._field(fname, M + 340, ty - 20, PAGE_W - 2*M - 360, 18, font_size=9,
                       tooltip=f"My response for: {type_name}")
            ty -= 32

        # ── Night feeding by age ──
        self._bg_rect(M, 170, PAGE_W - 2*M, 152, fill="card2", radius=12)
        self._label(M + 18, 310, "Night Feeding — Is It Hunger or Habit?", size=11, color="gold_l")

        feed_rows = [
            ("0–3 months", "2–4 feeds expected", "Do not reduce — nutritional"),
            ("3–4 months", "1–3 feeds",          "Focus on drowsy-awake first"),
            ("4–6 months", "1–2 feeds",           "Begin gradual reduction if weight good"),
            ("6–9 months", "0–1 feed",            "Most can handle 0 with pediatric OK"),
            ("9+ months",  "0 in most cases",     "Likely habit — follow your method"),
        ]

        self.c.setFillColor(P["navy"])
        self.c.roundRect(M + 10, 284, PAGE_W - 2*M - 20, 18, 4, fill=1, stroke=0)
        for h, hx in [("Age", M+18), ("Expected Feeds", M+108), ("Guidance", M+230)]:
            self._label(hx, 288, h, size=7.5, color="gold_l")

        ry = 268
        for age, feeds, guidance in feed_rows:
            fill_k = "card" if ry % 2 == 0 else "bg2"
            self._bg_rect(M + 10, ry - 10, PAGE_W - 2*M - 20, 18, fill=fill_k, radius=3)
            self._text(M + 18, ry - 2, age, size=8.5, color="cream")
            self._text(M + 108, ry - 2, feeds, size=8.5, color="gold_l")
            self._text(M + 230, ry - 2, guidance, size=8, color="cream_dim")
            ry -= 22

        # ── Affirmation ──
        self._bg_rect(M, 50, PAGE_W - 2*M, 52, fill="navy", radius=8)
        self.c.setFillColor(P["gold_l"])
        self.c.setFont("Times-Italic", 11)
        self.c.drawCentredString(PAGE_W/2, 85,
            "\"Consistency on hard nights is where progress is made. You're in it. Keep going.\"")
        self.c.setFillColor(P["dim"])
        self.c.setFont("Helvetica", 8)
        self.c.drawCentredString(PAGE_W/2, 62, "— Sleep, Baby. Please. · Chapter 7")

        self._top_nav(prev="plan_v2", nxt="cover")

    # ═══════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════════════
    def page_toc(self):
        self.new_page("Table of Contents", "toc")
        self._section_header(
            "Planner Contents",
            "Tap any item to jump directly to that page.",
            tag="CONTENTS"
        )

        toc_items = [
            ("How to Use This Planner",    "how_to"),
            ("My Plan — Setup",            "plan_overview"),
        ] + [
            (f"Waking Type {i+1}: {wt['label']}", f"waking_type_{i+1}")
            for i, wt in enumerate(WAKING_TYPES)
        ] + [
            (f"Night {n} Log", f"night_log_{n}") for n in range(1, 8)
        ] + [
            ("Weekly Review — Pattern Finder", "week_review"),
            ("Revised Plan — Week 2",          "plan_v2"),
            ("Quick Reference Card",            "quick_ref"),
        ]

        self._bg_rect(M, 100, PAGE_W - 2*M, 530, fill="card", radius=12)

        # two columns
        mid = len(toc_items) // 2
        left_items = toc_items[:mid]
        right_items = toc_items[mid:]

        for col_idx, items in enumerate([left_items, right_items]):
            col_x = M + 18 if col_idx == 0 else PAGE_W/2 + 10
            yy = 600
            for label, dest in items:
                self._nav_btn(col_x, yy, 234, 22, label[:40], dest, fill="card2", size=9)
                yy -= 30

        self._top_nav(prev="cover", nxt="how_to")

    # ═══════════════════════════════════════════════════════════
    # BUILD
    # ═══════════════════════════════════════════════════════════
    def build(self):
        # Cover
        self.page_cover()
        # TOC
        self.page_toc()
        # How to use
        self.page_how_to()
        # Plan overview / setup
        self.page_plan_overview()

        # 7 waking type pages
        for i, wt in enumerate(WAKING_TYPES):
            prev = "plan_overview" if i == 0 else f"waking_type_{i}"
            nxt = f"waking_type_{i+2}" if i < len(WAKING_TYPES) - 1 else "night_log_1"
            self.page_waking_type(i, wt, prev, nxt)

        # 7 night log pages
        for n in range(1, 8):
            prev = f"waking_type_{len(WAKING_TYPES)}" if n == 1 else f"night_log_{n-1}"
            nxt = f"night_log_{n+1}" if n < 7 else "week_review"
            self.page_night_log(n, prev, nxt)

        # Weekly review
        self.page_weekly_review()

        # Revised plan v2
        self.page_plan_v2()

        # Quick reference
        self.page_quick_ref()

        # finalize
        self._draw_footer()
        self.c.save()
        return self.filename


# ─────────────────────────── ENTRY POINT ───────────────────────────────────

if __name__ == "__main__":
    out = "night_waking_response_planner.pdf"
    print("Building Night Waking Response Planner...")
    NightWakingPDF(out).build()
    print(f"✓  Created: {os.path.abspath(out)}")
    size_kb = os.path.getsize(out) // 1024
    print(f"   File size: {size_kb} KB")
