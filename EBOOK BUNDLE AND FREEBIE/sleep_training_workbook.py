# sleep_training_method_workbook.py
# Sleep Training Method Workbook — Decision support + personalised plan + nightly log
# Requires: pip install reportlab
# "Decided before dark. Consistent after midnight."

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
import os

# ============================================================
# BRAND / PALETTE
# ============================================================

PAGE_W, PAGE_H = LETTER
MARGIN = 40

P = {
    "bg":         HexColor("#0B1520"),
    "surface":    HexColor("#162030"),
    "surface2":   HexColor("#1C2D42"),
    "navy":       HexColor("#1A2A45"),
    "navy_light": HexColor("#22375A"),
    "gold":       HexColor("#C9A84C"),
    "gold_light": HexColor("#E8C97A"),
    "blush":      HexColor("#C97A7A"),
    "mint":       HexColor("#6ABFA0"),
    "teal":       HexColor("#4AA8A0"),
    "lavender":   HexColor("#9B8EC4"),
    "cream":      HexColor("#F0E8D8"),
    "muted":      HexColor("#8FA0B8"),
    "dim":        HexColor("#4A607A"),
    "rule":       HexColor("#2A3F5A"),
    "input_bg":   HexColor("#0D1720"),
    "input_bd":   HexColor("#3A5575"),
    "warn":       HexColor("#E07A3A"),
    "green":      HexColor("#5AB87A"),
    "white":      white,
    "black":      black,
}

# ============================================================
# CONTENT
# ============================================================

METHODS_FULL = [
    {
        "id": "cio",
        "name": "Extinction (CIO)",
        "subtitle": "Cry It Out",
        "cry": "High",
        "speed": "Fast — 3 to 5 days",
        "best_for": "Persistent babies; exhausted families who need fast results",
        "not_for": "Highly sensitive babies; parents who struggle with extended crying",
        "principle": "Place baby in crib awake. Do not return until morning or a planned feed. Baby learns to self-settle with full opportunity.",
        "consistency_key": "No returns except pre-planned feeds. Even one intervention resets progress.",
        "cry_icon": "●●●●●",
        "speed_icon": "▶▶▶▶▶",
        "color": "blush",
    },
    {
        "id": "ferber",
        "name": "Ferber / Graduated",
        "subtitle": "Timed Check-ins",
        "cry": "Moderate",
        "speed": "Medium — 5 to 7 days",
        "best_for": "Most temperaments; parents who need to do something during crying",
        "not_for": "Babies who escalate at check-ins; parents who can't keep to the schedule",
        "principle": "Check in at increasing timed intervals. Comfort with voice only — no picking up. Intervals increase each night.",
        "consistency_key": "Stick to the interval schedule. Picking up resets the lesson.",
        "cry_icon": "●●●○○",
        "speed_icon": "▶▶▶▶○",
        "color": "gold",
    },
    {
        "id": "chair",
        "name": "Chair Method",
        "subtitle": "Sleep Lady Shuffle",
        "cry": "Low to Moderate",
        "speed": "Slower — 2 to 3 weeks",
        "best_for": "Sensitive babies; parents not ready to leave the room",
        "not_for": "Babies who are stimulated by parental presence",
        "principle": "Sit in a chair by the crib. Move chair farther away every 2 to 3 nights. Your presence fades gradually.",
        "consistency_key": "Move the chair on schedule. Staying too long in one position extends the process.",
        "cry_icon": "●●○○○",
        "speed_icon": "▶▶○○○",
        "color": "mint",
    },
    {
        "id": "fading",
        "name": "Fading Method",
        "subtitle": "Gradual Withdrawal",
        "cry": "Low",
        "speed": "Slowest — 3 to 4 plus weeks",
        "best_for": "Gentle approach; adaptable babies; parents who want no cry",
        "not_for": "Families who need faster results; inconsistent schedules",
        "principle": "Gradually reduce your involvement at sleep onset over time. Each night slightly less help than the last.",
        "consistency_key": "Reduce involvement on schedule. Adding back support undoes progress.",
        "cry_icon": "●○○○○",
        "speed_icon": "▶○○○○",
        "color": "lavender",
    },
    {
        "id": "pupd",
        "name": "Pick Up / Put Down",
        "subtitle": "PUPD",
        "cry": "Low",
        "speed": "Variable — depends on baby",
        "best_for": "Young babies 3 to 5 months; high-support-need families",
        "not_for": "Older babies who are stimulated by being picked up",
        "principle": "Pick up when crying peaks. Put down when calm. Repeat until asleep. Your presence is the safety net.",
        "consistency_key": "Put down even if baby protests immediately. The ritual itself is the signal.",
        "cry_icon": "●○○○○",
        "speed_icon": "▶▶○○○",
        "color": "teal",
    },
]

DECISION_QUESTIONS = [
    {
        "id": "tolerance",
        "question": "How do you feel about hearing your baby cry?",
        "tag": "EMOTIONAL TOLERANCE",
        "options": [
            ("a", "I can manage extended crying if it means faster results", ["cio", "ferber"]),
            ("b", "I need to do something — check-ins help me cope", ["ferber", "chair"]),
            ("c", "Crying feels wrong to me — I want minimal distress", ["chair", "fading", "pupd"]),
            ("d", "Any crying longer than a few minutes is not possible for me", ["fading", "pupd"]),
        ]
    },
    {
        "id": "urgency",
        "question": "How urgently do you need results?",
        "tag": "TIMELINE",
        "options": [
            ("a", "Crisis level — I need change within the week", ["cio", "ferber"]),
            ("b", "Soon — ideally within two weeks", ["ferber", "chair"]),
            ("c", "Patient — I'll take three to four weeks if it's gentler", ["chair", "fading"]),
            ("d", "No rush — baby's comfort is the priority", ["fading", "pupd"]),
        ]
    },
    {
        "id": "baby_age",
        "question": "How old is your baby right now?",
        "tag": "BABY'S AGE",
        "options": [
            ("a", "Under 4 months (newborn stage)", ["pupd", "fading"]),
            ("b", "4 to 6 months (prime sleep training window)", ["ferber", "cio", "fading"]),
            ("c", "6 to 12 months", ["cio", "ferber", "chair"]),
            ("d", "12 months and older / toddler", ["ferber", "chair", "fading"]),
        ]
    },
    {
        "id": "temperament",
        "question": "How would you describe your baby's temperament?",
        "tag": "BABY'S TEMPERAMENT",
        "options": [
            ("a", "Easy-going and adaptable", ["cio", "ferber", "fading"]),
            ("b", "Persistent and strong-willed", ["cio", "ferber"]),
            ("c", "Sensitive and easily overwhelmed", ["chair", "fading", "pupd"]),
            ("d", "High energy — stimulated by attention", ["cio", "ferber"]),
        ]
    },
    {
        "id": "consistency",
        "question": "How consistent can you realistically be?",
        "tag": "YOUR CONSISTENCY",
        "options": [
            ("a", "Very — once I commit I don't waver", ["cio", "ferber"]),
            ("b", "Mostly — I may need a check-in to feel confident", ["ferber", "chair"]),
            ("c", "Variable — life is unpredictable right now", ["fading", "chair"]),
            ("d", "Uncertain — I may need to adjust as I go", ["pupd", "fading"]),
        ]
    },
]

FERBER_INTERVALS = [
    ("Night 1", "3 min", "5 min", "10 min", "10 min"),
    ("Night 2", "5 min", "10 min", "12 min", "12 min"),
    ("Night 3", "10 min", "12 min", "15 min", "15 min"),
    ("Night 4+", "12 min", "15 min", "17 min", "17 min"),
    ("Night 6+", "15 min", "17 min", "20 min", "20 min"),
]

NIGHT_LOG_PROMPTS = [
    ("Bedtime", "What time did you put baby down?", 90),
    ("Settle time", "How long until they fell asleep?", 60),
    ("Night waking 1", "Time + how you responded", 80),
    ("Night waking 2", "Time + how you responded", 80),
    ("Night waking 3", "Time + how you responded", 80),
    ("Morning wake", "What time did baby wake for the day?", 60),
    ("Total sleep estimate", "Rough total overnight hours", 50),
    ("Method adherence", "Did you stick to the plan? Any deviations?", 90),
    ("Emotional check", "How are you doing? One honest sentence.", 80),
]

PLAN_SECTIONS = [
    ("Method Chosen", "method_chosen", 22, False),
    ("Why I Chose This Method", "method_why", 40, True),
    ("My Baby's Sleep Personality", "personality_chosen", 22, False),
    ("Planned Bedtime", "planned_bedtime", 22, False),
    ("Planned Response to Night Wakings", "night_response", 40, True),
    ("Planned Feed Window (if any)", "feed_window", 22, False),
    ("Partner / Co-parent Briefing", "partner_brief", 40, True),
    ("My Non-Negotiable Rule", "non_negotiable", 30, True),
]

CONSISTENCY_CHECKS = [
    "I followed the method without deviation",
    "I waited before entering at night wakings",
    "I did not feed to sleep",
    "I used the same bedtime routine in the same order",
    "I kept the room dark and white noise on",
    "I kept bedtime within 15 minutes of target",
    "I placed baby drowsy but awake",
    "I exited the room calmly after the routine",
]

AFFIRM = [
    "Decided before dark. Consistent after midnight.",
    "Your 2am brain will thank your 2pm brain.",
    "Consistency on hard nights is where progress lives.",
    "One bad night does not undo five good ones.",
    "You chose a method. You worked the plan. That is winning.",
    "Progress is often messy before it sticks.",
    "The hard nights are not failed nights.",
    "Sleep is coming — for both of you.",
    "Two steps forward, one step back. You are still moving forward.",
    "Awareness breaks the cycle. You are already ahead.",
    "Stay kind. Stay firm. Stay consistent.",
    "Your baby is learning a skill for life. Keep going.",
    "You do not need perfection. You need direction.",
    "Hard nights are evidence you are in it.",
    "The plan was made in calm. Trust it at midnight.",
    "Even one longer stretch is a victory worth recording.",
    "Show up again tonight. That is the whole job.",
    "You are the constant. Be the constant.",
    "Grace for tonight. Plan for tomorrow.",
    "This is temporary. Keep your eyes on the horizon.",
    "Strong families make decisions before the hard moment arrives.",
]

PERSONALITY_TIPS = {
    "Snacker":    "Gradually lengthen feed gaps during the day. Ensure full feeds so night hunger is genuine.",
    "Overthinker":"Deep firm swaddle. Highly consistent routine. Minimal stimulation in the 30 min before bed.",
    "Sensitive":  "Extra long calm-down buffer before crib. Dimmer, quieter, slower — everything turned down.",
    "Night Owl":  "Push bedtime earlier by 10 minutes every 2 to 3 days until you hit the sweet spot.",
    "Catnapper":  "Practice settling at the 40-minute cycle mark. Stay close but do not rescue immediately.",
    "Party Animal":"Boring, dark, silent exits. Make sleep the least interesting option in the house.",
}

# ============================================================
# PDF ENGINE
# ============================================================

class WorkbookPDF:
    def __init__(self, filename="sleep_training_method_workbook.pdf"):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.c.setTitle("Sleep Training Method Workbook")
        self.c.setAuthor("Six & Thriving")
        self.c.setSubject("Decision support · Personalised plan · Nightly training log")
        self.c.setCreator("Python + ReportLab")
        self.form = self.c.acroForm
        self.page_num = 0
        self._affirm_idx = 0

    # ----------------------------------------------------------
    # Core helpers
    # ----------------------------------------------------------
    def new_page(self, section_title=None, bookmark=None, bg="bg"):
        if self.page_num > 0:
            self._draw_footer()
            self.c.showPage()
        self.page_num += 1
        self.c.setFillColor(P[bg])
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if bookmark:
            self.c.bookmarkPage(bookmark)
            if section_title:
                self.c.addOutlineEntry(section_title, bookmark, level=0, closed=False)

    def _draw_footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN, 26, PAGE_W - MARGIN, 26)
        self.c.setFont("Helvetica", 7.5)
        self.c.setFillColor(P["muted"])
        self.c.drawString(MARGIN, 14, "Sleep Training Method Workbook  ·  Six & Thriving")
        self.c.drawRightString(PAGE_W - MARGIN, 14, f"{self.page_num}")

    def section_header(self, title, subtitle="", tag=None, tag_color="gold"):
        y = PAGE_H - 52
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN, y - 54, PAGE_W - 2*MARGIN, 68, 14, fill=1, stroke=0)
        # accent bar
        self.c.setFillColor(P[tag_color])
        self.c.roundRect(MARGIN, y + 10, 6, 48, 3, fill=1, stroke=0)
        if tag:
            self.c.setFillColor(P[tag_color])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(MARGIN + 18, y + 6, tag)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 20)
        self.c.drawString(MARGIN + 18, y - 10, title)
        if subtitle:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 10)
            self.c.drawString(MARGIN + 18, y - 28, subtitle)

    def card(self, x, y, w, h, fill="surface", r=10, stroke_color=None, stroke_w=0.5):
        self.c.setFillColor(P[fill])
        if stroke_color:
            self.c.setStrokeColor(P[stroke_color])
            self.c.setLineWidth(stroke_w)
            self.c.roundRect(x, y, w, h, r, fill=1, stroke=1)
        else:
            self.c.roundRect(x, y, w, h, r, fill=1, stroke=0)

    def label(self, x, y, text, size=9, color="muted", font="Helvetica-Bold"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawString(x, y, text)

    def text(self, x, y, txt, size=10, color="cream", font="Times-Roman", max_w=None, leading=None):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        lh = leading or (size + 3)
        if not max_w:
            self.c.drawString(x, y, txt)
            return y - lh
        lines = simpleSplit(txt, font, size, max_w)
        yy = y
        for line in lines:
            self.c.drawString(x, yy, line)
            yy -= lh
        return yy

    def bullets(self, x, y, items, width, bullet="gold", txt_color="cream", size=10):
        yy = y
        for item in items:
            self.c.setFillColor(P[bullet])
            self.c.setFont("Helvetica-Bold", size)
            self.c.drawString(x, yy, "•")
            yy = self.text(x + 14, yy, item, size=size, color=txt_color, max_w=width - 14)
            yy -= 4
        return yy

    # ----------------------------------------------------------
    # Nav helpers
    # ----------------------------------------------------------
    def btn(self, x, y, w, h, text, dest, fill="surface2", txt="gold_light", size=9):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
        self.c.setFillColor(P[txt])
        self.c.setFont("Helvetica-Bold", size)
        tw = stringWidth(text, "Helvetica-Bold", size)
        self.c.drawString(x + (w - tw)/2, y + h/2 - 3.5, text)
        self.c.linkRect("", dest, (x, y, x + w, y + h), relative=0, thickness=0)

    def nav(self, prev=None, nxt=None, home="cover"):
        y = 36
        if prev:
            self.btn(MARGIN, y, 88, 18, "◀  Previous", prev, fill="surface2")
        self.btn(PAGE_W/2 - 44, y, 88, 18, "⌂  Home", home, fill="navy")
        if nxt:
            self.btn(PAGE_W - MARGIN - 88, y, 88, 18, "Next  ▶", nxt, fill="gold", txt="bg")

    # ----------------------------------------------------------
    # Form field helpers  (white bg, legible, generous size)
    # ----------------------------------------------------------
    def field(self, name, x, y, w, h=22, value="", multiline=False, fsize=10, tooltip=None):
        self.form.textfield(
            name=name,
            tooltip=tooltip or name.replace("_", " "),
            x=x, y=y, width=w, height=h,
            borderStyle='inset',
            borderColor=P["input_bd"],
            fillColor=white,
            textColor=black,
            forceBorder=True,
            value=value,
            fontName="Helvetica",
            fontSize=fsize,
            fieldFlags=('multiline' if multiline else '')
        )

    def lfield(self, x, y, w, lbl, name, h=22, multiline=False, fsize=10):
        """Labeled field: label above, field below."""
        self.label(x, y + h + 6, lbl, size=8)
        self.field(name, x, y, w, h, multiline=multiline, fsize=fsize)

    def chk(self, name, x, y, size=13, tooltip=None):
        self.form.checkbox(
            name=name,
            tooltip=tooltip or name.replace("_", " "),
            x=x, y=y, size=size,
            checked=False,
            buttonStyle='check',
            borderColor=P["gold"],
            fillColor=white,
            textColor=P["gold"],
            forceBorder=True,
        )

    def radio_btn(self, group, value, x, y, size=14, selected=False, tooltip=None):
        self.form.radio(
            name=group,
            tooltip=tooltip or group,
            value=value,
            selected=selected,
            x=x, y=y, buttonStyle='circle',
            borderColor=P["gold"],
            fillColor=white,
            textColor=P["gold"],
            forceBorder=True,
            size=size,
        )

    def affirm(self, idx=None):
        """Draw centered italic affirmation near bottom of page."""
        i = idx if idx is not None else (self._affirm_idx % len(AFFIRM))
        self._affirm_idx += 1
        self.c.setFillColor(P["dim"])
        self.c.roundRect(MARGIN, 60, PAGE_W - 2*MARGIN, 22, 8, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Times-Italic", 10)
        self.c.drawCentredString(PAGE_W/2, 67, f'"{AFFIRM[i]}"')

    # ----------------------------------------------------------
    # ========================================================
    # PAGES
    # ========================================================
    # ----------------------------------------------------------

    # ── COVER ─────────────────────────────────────────────────
    def page_cover(self):
        self.new_page("Cover", "cover", bg="bg")

        # outer glow frame
        self.c.setFillColor(P["navy"])
        self.c.roundRect(28, 60, PAGE_W - 56, PAGE_H - 120, 20, fill=1, stroke=0)
        self.c.setStrokeColor(P["gold"])
        self.c.setLineWidth(1.5)
        self.c.roundRect(28, 60, PAGE_W - 56, PAGE_H - 120, 20, fill=0, stroke=1)

        # eyebrow
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 118, "SIX & THRIVING  ·  COMPANION WORKBOOK")

        # rule
        self.c.setStrokeColor(P["gold"])
        self.c.setLineWidth(1)
        self.c.line(100, PAGE_H - 128, PAGE_W - 100, PAGE_H - 128)

        # main title
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 36)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 170, "Sleep Training")

        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Italic", 22)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 196, "Method Workbook")

        # rule
        self.c.setStrokeColor(P["dim"])
        self.c.line(120, PAGE_H - 210, PAGE_W - 120, PAGE_H - 210)

        # tagline
        self.c.setFillColor(P["muted"])
        self.c.setFont("Times-Italic", 12)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 236,
            "Choose your method · Build your plan · Log every night")

        # 3-pillar cards
        card_y = PAGE_H - 400
        card_h = 130
        card_w = 148
        pillars = [
            ("DECIDE", "gold", "Compare all 5 methods. Answer 5 questions. Get a clear recommendation before tonight."),
            ("PLAN", "mint", "Build your complete personalised plan. Write it. Post it. Trust it at 2am."),
            ("LOG", "lavender", "Objective nightly logs for every night of training. No panic. Just data."),
        ]
        xstart = 52
        for pname, pcolor, pdesc in pillars:
            self.c.setFillColor(P["surface2"])
            self.c.roundRect(xstart, card_y, card_w, card_h, 12, fill=1, stroke=0)
            self.c.setFillColor(P[pcolor])
            self.c.roundRect(xstart, card_y + card_h - 28, card_w, 28, 12, fill=1, stroke=0)
            self.c.roundRect(xstart, card_y + card_h - 14, card_w, 14, 0, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 11)
            tw = stringWidth(pname, "Helvetica-Bold", 11)
            self.c.drawString(xstart + (card_w - tw)/2, card_y + card_h - 18, pname)
            self.text(xstart + 10, card_y + card_h - 44, pdesc, size=8.5, color="cream",
                      max_w=card_w - 20)
            xstart += card_w + 12

        # quote box
        self.c.setFillColor(P["surface"])
        self.c.roundRect(52, card_y - 80, PAGE_W - 104, 64, 10, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawCentredString(PAGE_W/2, card_y - 26, "DECIDED BEFORE DARK. CONSISTENT AFTER MIDNIGHT.")
        self.c.setFillColor(P["muted"])
        self.c.setFont("Times-Italic", 9)
        self.c.drawCentredString(PAGE_W/2, card_y - 44,
            "Write your method down before tonight. Your 2am brain will thank your 2pm brain.")

        # feature chips
        chips = ["Interactive form fields", "Method comparison", "Personalised plan",
                 "21 nightly log pages", "Ferber interval guide", "Weekly summaries"]
        cx = 52
        cy = card_y - 106
        for chip in chips:
            cw = stringWidth(chip, "Helvetica", 8) + 18
            self.c.setFillColor(P["navy_light"])
            self.c.roundRect(cx, cy, cw, 16, 8, fill=1, stroke=0)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(cx + 9, cy + 4, chip)
            cx += cw + 8
            if cx > PAGE_W - 100:
                cx = 52
                cy -= 22

        # nav buttons
        self.btn(90, 80, 130, 26, "Start Decision Guide", "decide_intro", fill="gold", txt="bg", size=9)
        self.btn(236, 80, 110, 26, "My Plan", "my_plan", fill="surface2", size=9)
        self.btn(362, 80, 110, 26, "Night 1 Log", "night_1", fill="surface2", size=9)

        # byline
        self.c.setFillColor(P["blush"])
        self.c.setFont("Times-Italic", 10)
        self.c.drawCentredString(PAGE_W/2, 68, "Six & Thriving")

    # ── CONTENTS ──────────────────────────────────────────────
    def page_contents(self):
        self.new_page("Contents", "contents")
        self.section_header("Workbook Navigation",
                            "Tap any entry below to jump directly to that section.", "CONTENTS")

        self.card(MARGIN, 90, PAGE_W - 2*MARGIN, 580, fill="surface")

        sections_left = [
            ("Decision Guide — Intro", "decide_intro"),
            ("Method Comparison Cards", "method_cards"),
            ("5 Decision Questions", "decide_q1"),
            ("Your Recommendation", "decide_result"),
            ("Ferber Interval Guide", "ferber_guide"),
            ("Chair Method Schedule", "chair_schedule"),
            ("My Personalised Plan", "my_plan"),
            ("Safe Sleep Checklist", "safe_sleep"),
        ]
        sections_right = [(f"Night {n} Training Log", f"night_{n}") for n in range(1, 22)]

        left_x = MARGIN + 16
        right_x = PAGE_W/2 + 8

        self.label(left_x, 648, "Core Sections", size=11, color="gold")
        self.label(right_x, 648, "21-Night Training Log", size=11, color="gold")

        yy = 622
        for lbl, dest in sections_left:
            self.btn(left_x, yy, 218, 22, lbl, dest)
            yy -= 30

        yy = 622
        for lbl, dest in sections_right:
            self.btn(right_x, yy - 4, 218, 18, lbl, dest, size=8)
            yy -= 24

        self.nav(prev="cover", nxt="decide_intro")

    # ── DECISION INTRO ────────────────────────────────────────
    def page_decide_intro(self):
        self.new_page("Decision Guide — Intro", "decide_intro")
        self.section_header("The Decision Guide",
                            "Five questions. One clear recommendation. Done before dark.",
                            "STEP 1 — DECIDE", tag_color="gold")

        self.card(MARGIN, 490, PAGE_W - 2*MARGIN, 170, fill="surface")
        self.label(MARGIN + 16, 640, "Why this matters", size=11, color="gold")
        body = ("Any sleep training method can work if — and only if — it is applied consistently. "
                "The method you half-heartedly try is worse than the gentle method you actually follow every night. "
                "This guide helps you choose not the 'best' method in the abstract, but the method that best fits "
                "your temperament, your baby's temperament, and your family's current reality.")
        self.text(MARGIN + 16, 618, body, size=10, color="cream", max_w=PAGE_W - 2*MARGIN - 32)

        self.card(MARGIN, 300, PAGE_W - 2*MARGIN, 170, fill="navy")
        self.label(MARGIN + 16, 450, "How to use this section", size=11, color="gold")
        steps = [
            ("1", "Read the 5 Method Cards on the next page — one for each training approach."),
            ("2", "Answer the 5 Decision Questions honestly. Circle your answer."),
            ("3", "Tally your method scores on the Recommendation page."),
            ("4", "Confirm your choice and copy it to your Personalised Plan."),
        ]
        yy = 426
        for num, step_text in steps:
            self.c.setFillColor(P["gold"])
            self.c.roundRect(MARGIN + 16, yy - 8, 22, 22, 5, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawCentredString(MARGIN + 27, yy + 1, num)
            yy = self.text(MARGIN + 46, yy + 1, step_text, size=10, color="cream",
                           max_w=PAGE_W - 2*MARGIN - 62)
            yy -= 8

        self.card(MARGIN, 100, PAGE_W - 2*MARGIN, 180, fill="surface2")
        self.label(MARGIN + 16, 260, "The 5 Methods at a Glance", size=11, color="gold")
        cols = [("Method", 60), ("Cry Level", 200), ("Speed", 300), ("Best For", 390)]
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 8, 230, PAGE_W - 2*MARGIN - 16, 18, 4, fill=1, stroke=0)
        for hdr, hx in cols:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(hx, 235, hdr)

        yy = 216
        for m in METHODS_FULL:
            self.c.setFillColor(P[m["color"]])
            self.c.circle(MARGIN + 20, yy + 5, 4, fill=1, stroke=0)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Roman", 9)
            self.c.drawString(60, yy, m["name"])
            self.c.drawString(200, yy, m["cry"])
            self.c.drawString(300, yy, m["speed"][:22])
            self.c.drawString(390, yy, m["best_for"][:28])
            yy -= 18

        self.affirm(0)
        self.nav(prev="contents", nxt="method_cards")

    # ── METHOD COMPARISON CARDS ───────────────────────────────
    def page_method_cards(self):
        self.new_page("Method Comparison Cards", "method_cards")
        self.section_header("The 5 Methods — Comparison Cards",
                            "Read each card. Note which resonates. Then answer the decision questions.",
                            "STEP 1 · COMPARE", tag_color="gold")

        card_h = 110
        card_y = 640
        for m in METHODS_FULL:
            self.card(MARGIN, card_y, PAGE_W - 2*MARGIN, card_h, fill="surface",
                      stroke_color=m["color"], stroke_w=1.2)
            # colour badge
            self.c.setFillColor(P[m["color"]])
            self.c.roundRect(MARGIN, card_y + card_h - 22, 100, 22, 8, fill=1, stroke=0)
            self.c.roundRect(MARGIN, card_y + card_h - 11, 100, 11, 0, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 8, card_y + card_h - 14, m["name"])

            # cry / speed dots
            x_dots = PAGE_W - MARGIN - 180
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7)
            self.c.drawString(x_dots, card_y + card_h - 10, f"Cry:  {m['cry_icon']}")
            self.c.drawString(x_dots + 90, card_y + card_h - 10, f"Speed: {m['speed_icon']}")

            # principle
            self.text(MARGIN + 12, card_y + card_h - 34, m["principle"],
                      size=9, color="cream", max_w=PAGE_W - 2*MARGIN - 24)
            # tags
            self.label(MARGIN + 12, card_y + 22, f"✓ Best for: {m['best_for'][:55]}", size=8, color="mint")
            self.label(MARGIN + 12, card_y + 8, f"✗ Not ideal: {m['not_for'][:55]}", size=8, color="blush")

            card_y -= card_h + 10

        self.affirm(1)
        self.nav(prev="decide_intro", nxt="decide_q1")

    # ── DECISION QUESTIONS ────────────────────────────────────
    def _decision_page_a(self):
        """Questions 1-3 on first page."""
        self.new_page("Decision Questions 1-3", "decide_q1")
        self.section_header("5 Decision Questions",
                            "Circle or tick the answer that honestly fits your situation right now.",
                            "STEP 2 · CHOOSE", tag_color="gold")

        y = 640
        for q_data in DECISION_QUESTIONS[:3]:
            q_h = 115
            self.card(MARGIN, y - q_h, PAGE_W - 2*MARGIN, q_h, fill="surface")
            self.c.setFillColor(P["navy"])
            self.c.roundRect(MARGIN, y - 22, PAGE_W - 2*MARGIN, 22, 8, fill=1, stroke=0)
            self.c.roundRect(MARGIN, y - 11, PAGE_W - 2*MARGIN, 11, 0, fill=1, stroke=0)
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(MARGIN + 12, y - 16, q_data["tag"])
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 11)
            self.c.drawString(MARGIN + 100, y - 16, q_data["question"])

            yy = y - 36
            for val, lbl, methods in q_data["options"]:
                self.radio_btn(f"decision_{q_data['id']}", val, MARGIN + 16, yy - 4, size=12)
                # method tags
                tag_str = "  →  " + "  /  ".join([m.upper()[:7] for m in methods])
                self.c.setFillColor(P["cream"])
                self.c.setFont("Times-Roman", 9.5)
                self.c.drawString(MARGIN + 34, yy, lbl)
                self.c.setFillColor(P["dim"])
                self.c.setFont("Helvetica", 7.5)
                self.c.drawString(MARGIN + 34 + stringWidth(lbl, "Times-Roman", 9.5) + 4, yy, tag_str)
                yy -= 17

            y -= q_h + 12

        self.affirm(2)
        self.nav(prev="method_cards", nxt="decide_q2")

    def _decision_page_b(self):
        """Questions 4-5 on second page."""
        self.new_page("Decision Questions 4-5", "decide_q2")
        self.section_header("5 Decision Questions — continued",
                            "Two more questions then tally your scores on the next page.",
                            "STEP 2 · CHOOSE", tag_color="gold")

        y = 620
        for q_data in DECISION_QUESTIONS[3:]:
            q_h = 115
            self.card(MARGIN, y - q_h, PAGE_W - 2*MARGIN, q_h, fill="surface")
            self.c.setFillColor(P["navy"])
            self.c.roundRect(MARGIN, y - 22, PAGE_W - 2*MARGIN, 22, 8, fill=1, stroke=0)
            self.c.roundRect(MARGIN, y - 11, PAGE_W - 2*MARGIN, 11, 0, fill=1, stroke=0)
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(MARGIN + 12, y - 16, q_data["tag"])
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 11)
            self.c.drawString(MARGIN + 100, y - 16, q_data["question"])

            yy = y - 36
            for val, lbl, methods in q_data["options"]:
                self.radio_btn(f"decision_{q_data['id']}", val, MARGIN + 16, yy - 4, size=12)
                tag_str = "  →  " + "  /  ".join([m.upper()[:7] for m in methods])
                self.c.setFillColor(P["cream"])
                self.c.setFont("Times-Roman", 9.5)
                self.c.drawString(MARGIN + 34, yy, lbl)
                self.c.setFillColor(P["dim"])
                self.c.setFont("Helvetica", 7.5)
                self.c.drawString(MARGIN + 34 + stringWidth(lbl, "Times-Roman", 9.5) + 4, yy, tag_str)
                yy -= 17

            y -= q_h + 12

        # tally explainer
        self.card(MARGIN, 120, PAGE_W - 2*MARGIN, 130, fill="navy")
        self.label(MARGIN + 16, 230, "How to tally your scores", size=11, color="gold")
        self.text(MARGIN + 16, 212,
                  "Each answer above shows which method(s) it points toward. "
                  "Count how many times each method appears across all 5 questions. "
                  "The method with the highest count is your recommended starting point. "
                  "Record your tally on the next page.", size=9.5, color="cream",
                  max_w=PAGE_W - 2*MARGIN - 32)

        self.affirm(3)
        self.nav(prev="decide_q1", nxt="decide_result")

    # ── RECOMMENDATION PAGE ───────────────────────────────────
    def page_decide_result(self):
        self.new_page("Your Method Recommendation", "decide_result")
        self.section_header("Your Recommendation",
                            "Tally your answers and confirm your method. Write it before tonight.",
                            "STEP 3 · CONFIRM", tag_color="gold")

        # tally grid
        self.card(MARGIN, 530, PAGE_W - 2*MARGIN, 190, fill="surface")
        self.label(MARGIN + 16, 700, "Score Tally", size=12, color="gold")
        self.text(MARGIN + 16, 684, "Count how many decision questions pointed to each method. Circle the winner.",
                  size=9, color="muted", max_w=480)

        col_w = (PAGE_W - 2*MARGIN - 32) / 5
        hx = MARGIN + 16
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 8, 655, PAGE_W - 2*MARGIN - 16, 22, 5, fill=1, stroke=0)
        for m in METHODS_FULL:
            self.c.setFillColor(P[m["color"]])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(hx, 662, m["name"][:14])
            hx += col_w

        hx = MARGIN + 16
        for m in METHODS_FULL:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7)
            self.c.drawString(hx, 642, "Tally marks:")
            self.field(f"tally_{m['id']}", hx, 600, int(col_w) - 8, h=36, fsize=18,
                       tooltip=f"Score tally for {m['name']}")
            hx += col_w

        # confirmed method
        self.card(MARGIN, 390, PAGE_W - 2*MARGIN, 124, fill="navy",
                  stroke_color="gold", stroke_w=1.5)
        self.label(MARGIN + 16, 494, "My Confirmed Method", size=12, color="gold")
        self.text(MARGIN + 16, 476,
                  "Write the method name below. This is your method. You chose it in calm. "
                  "Trust it at midnight.", size=9, color="muted", max_w=480)
        self.field("confirmed_method", MARGIN + 16, 408, PAGE_W - 2*MARGIN - 32, h=42,
                   fsize=16, tooltip="Write your confirmed sleep training method here")

        # why this fits
        self.card(MARGIN, 220, PAGE_W - 2*MARGIN, 150, fill="surface")
        self.label(MARGIN + 16, 350, "Why this method fits my family", size=11, color="gold")
        self.field("method_fit_reason", MARGIN + 16, 236, PAGE_W - 2*MARGIN - 32, h=88,
                   multiline=True, fsize=10,
                   tooltip="Why does this method fit your baby's temperament and your own?")

        # method links
        self.card(MARGIN, 100, PAGE_W - 2*MARGIN, 100, fill="surface2")
        self.label(MARGIN + 16, 180, "Method-specific guides in this workbook", size=9, color="muted")
        self.btn(MARGIN + 16, 118, 130, 20, "Ferber Intervals", "ferber_guide", fill="navy")
        self.btn(MARGIN + 160, 118, 130, 20, "Chair Schedule", "chair_schedule", fill="navy")
        self.btn(MARGIN + 304, 118, 130, 20, "My Plan", "my_plan", fill="gold", txt="bg")

        self.affirm(4)
        self.nav(prev="decide_q2", nxt="ferber_guide")

    # ── FERBER INTERVAL GUIDE ─────────────────────────────────
    def page_ferber_guide(self):
        self.new_page("Ferber Interval Guide", "ferber_guide")
        self.section_header("Ferber Interval Guide",
                            "Timed check-ins at increasing intervals. Comfort with voice only — never pick up.",
                            "FERBER / GRADUATED", tag_color="gold")

        # interval table
        self.card(MARGIN, 380, PAGE_W - 2*MARGIN, 300, fill="surface")
        self.label(MARGIN + 16, 660, "Check-in Interval Schedule", size=12, color="gold")
        self.text(MARGIN + 16, 643,
                  "Wait these intervals before entering. At each check-in: speak calmly, no lights, no picking up. "
                  "Immediately leave and restart the timer.", size=9, color="muted", max_w=480)

        cols = [("", 55), ("Wait 1", 180), ("Wait 2", 270), ("Wait 3", 360), ("Each After", 450)]
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 8, 610, PAGE_W - 2*MARGIN - 16, 22, 5, fill=1, stroke=0)
        for h, hx in cols:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(hx, 618, h)
        self.c.drawString(55, 618, "Night")

        yy = 596
        for row in FERBER_INTERVALS:
            bg = "surface2" if (FERBER_INTERVALS.index(row) % 2 == 0) else "surface"
            self.card(MARGIN + 8, yy - 2, PAGE_W - 2*MARGIN - 16, 20, fill=bg, r=4)
            vals = [row[0]] + list(row[1:])
            xs = [55, 180, 270, 360, 450]
            for val, xx in zip(vals, xs):
                color = "gold_light" if xx == 55 else "cream"
                self.c.setFillColor(P[color])
                self.c.setFont("Times-Roman" if xx > 55 else "Times-Bold", 9)
                self.c.drawString(xx, yy + 4, val)
            yy -= 22

        # rules card
        self.card(MARGIN, 200, PAGE_W - 2*MARGIN, 162, fill="navy")
        self.label(MARGIN + 16, 342, "The Non-Negotiable Rules", size=11, color="gold")
        rules = [
            "Never pick baby up during a check-in. Voice and presence only.",
            "Leave the room immediately after a check-in — even if crying resumes.",
            "Reset the timer from the moment you leave the room.",
            "If baby falls asleep during a check-in cycle, do not restart if they briefly stir.",
            "Stay on the scheduled night's interval — do not shorten because it feels hard.",
        ]
        self.bullets(MARGIN + 16, 320, rules, PAGE_W - 2*MARGIN - 32, size=9)

        # log field
        self.card(MARGIN, 90, PAGE_W - 2*MARGIN, 94, fill="surface2")
        self.label(MARGIN + 16, 164, "My interval plan for tonight", size=9, color="muted")
        self.field("ferber_tonight_plan", MARGIN + 16, 100, PAGE_W - 2*MARGIN - 32, h=50,
                   multiline=True, fsize=10, tooltip="Write tonight's intervals and your response plan")

        self.affirm(5)
        self.nav(prev="decide_result", nxt="chair_schedule")

    # ── CHAIR METHOD SCHEDULE ─────────────────────────────────
    def page_chair_schedule(self):
        self.new_page("Chair Method Schedule", "chair_schedule")
        self.section_header("Chair Method — Position Schedule",
                            "Move the chair every 2 to 3 nights. Do not rush. Do not stay too long.",
                            "CHAIR METHOD", tag_color="mint")

        self.card(MARGIN, 430, PAGE_W - 2*MARGIN, 290, fill="surface")
        self.label(MARGIN + 16, 700, "Chair Position Guide", size=12, color="mint")

        chair_rows = [
            ("Nights 1–2", "Next to the crib", "Sit close. Gentle shush. No eye contact."),
            ("Nights 3–4", "Halfway to the door", "Presence only. Very minimal verbal reassurance."),
            ("Nights 5–6", "Near the door (inside)", "Silent presence. No interaction."),
            ("Nights 7–8", "Just outside the door", "Occasional very soft shush if needed."),
            ("Nights 9+", "Chair removed", "Baby settles independently. Method complete."),
        ]
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 8, 672, PAGE_W - 2*MARGIN - 16, 22, 5, fill=1, stroke=0)
        headers_c = [("Nights", 55), ("Chair Position", 160), ("Your Role", 340)]
        for h, hx in headers_c:
            self.c.setFillColor(P["mint"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(hx, 680, h)

        yy = 658
        for nights, pos, role in chair_rows:
            self.card(MARGIN + 8, yy - 4, PAGE_W - 2*MARGIN - 16, 22, fill="surface2", r=4)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Times-Bold", 9)
            self.c.drawString(55, yy + 5, nights)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Roman", 9)
            self.c.drawString(160, yy + 5, pos)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 8.5)
            self.c.drawString(340, yy + 5, role)
            yy -= 26

        # rules
        self.card(MARGIN, 260, PAGE_W - 2*MARGIN, 154, fill="navy")
        self.label(MARGIN + 16, 394, "Chair Method Rules", size=11, color="mint")
        chair_rules = [
            "Move the chair on the scheduled night — even if the previous night was rough.",
            "Do not make eye contact after the first 2 nights.",
            "No patting, stroking, or picking up after position 1.",
            "If baby climbs out, return them calmly with zero interaction.",
            "Some babies are stimulated by presence — switch methods if escalating after night 4.",
        ]
        self.bullets(MARGIN + 16, 372, chair_rules, PAGE_W - 2*MARGIN - 32, bullet="mint", size=9)

        # my schedule card
        self.card(MARGIN, 90, PAGE_W - 2*MARGIN, 150, fill="surface2")
        self.label(MARGIN + 16, 220, "My Chair Schedule", size=11, color="mint")
        self.label(MARGIN + 16, 204, "Record tonight's position and any notes:", size=8)

        row_y = 184
        for idx, (nights, pos, _) in enumerate(chair_rows):
            self.chk(f"chair_check_{idx}", MARGIN + 16, row_y - 4, size=12)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Roman", 9)
            self.c.drawString(MARGIN + 34, row_y, f"{nights}  —  {pos}")
            row_y -= 18

        self.affirm(6)
        self.nav(prev="ferber_guide", nxt="my_plan")

    # ── MY PERSONALISED PLAN ──────────────────────────────────
    def page_my_plan(self):
        self.new_page("My Personalised Sleep Training Plan", "my_plan")
        self.section_header("My Personalised Plan",
                            "Fill this in once. Post it where both parents can see it. Trust it tonight.",
                            "STEP 4 — PLAN", tag_color="teal")

        # baby details block
        self.card(MARGIN, 570, PAGE_W - 2*MARGIN, 140, fill="surface")
        self.label(MARGIN + 16, 690, "Baby & Family Details", size=11, color="gold")
        self.lfield(MARGIN + 16, 620, 200, "Baby's Name", "plan_baby_name")
        self.lfield(310, 620, 200, "Date of Birth", "plan_dob")
        self.lfield(MARGIN + 16, 580, 200, "Current Age", "plan_age")
        self.lfield(310, 580, 200, "Training Start Date", "plan_start")

        # method + personality
        self.card(MARGIN, 430, PAGE_W - 2*MARGIN, 122, fill="navy")
        self.label(MARGIN + 16, 532, "Method & Personality", size=11, color="gold")

        self.label(MARGIN + 16, 516, "Chosen Method:", size=8)
        # radio buttons for method
        rx = MARGIN + 16
        for m in METHODS_FULL:
            self.radio_btn("plan_method", m["id"], rx, 490, size=12)
            self.c.setFillColor(P[m["color"]])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(rx + 16, 494, m["name"][:10])
            rx += 102

        self.label(MARGIN + 16, 478, "Baby's Sleep Personality:", size=8)
        personalities = ["Snacker", "Overthinker", "Sensitive", "Night Owl", "Catnapper", "Party Animal"]
        rx = MARGIN + 16
        for idx, pname in enumerate(personalities):
            self.radio_btn("plan_personality", pname, rx, 452, size=12)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(rx + 16, 456, pname)
            rx += 86

        # timing block
        self.card(MARGIN, 320, PAGE_W - 2*MARGIN, 94, fill="surface")
        self.label(MARGIN + 16, 394, "Timing", size=11, color="gold")
        self.lfield(MARGIN + 16, 334, 130, "Target Bedtime", "plan_bedtime")
        self.lfield(190, 334, 130, "Awake Window", "plan_awake_w")
        self.lfield(364, 334, 130, "Planned Feed (if any)", "plan_feed_time")

        # response plan
        self.card(MARGIN, 170, PAGE_W - 2*MARGIN, 134, fill="surface2")
        self.label(MARGIN + 16, 284, "My Night Waking Response Plan", size=11, color="gold")
        self.text(MARGIN + 16, 268,
                  "Write exactly what you will do when baby wakes. Be specific. This is your 2am script.",
                  size=8.5, color="muted", max_w=480)
        self.field("plan_response", MARGIN + 16, 182, PAGE_W - 2*MARGIN - 32, h=72,
                   multiline=True, fsize=10,
                   tooltip="Write your exact response plan for night wakings")

        # partner agreement
        self.card(MARGIN, 90, PAGE_W - 2*MARGIN, 64, fill="navy")
        self.label(MARGIN + 16, 136, "Partner briefed and in agreement?", size=9, color="muted")
        self.radio_btn("plan_partner_agree", "yes", MARGIN + 16, 104, size=12)
        self.c.setFillColor(P["cream"]); self.c.setFont("Helvetica", 9)
        self.c.drawString(MARGIN + 34, 108, "Yes — we are aligned")
        self.radio_btn("plan_partner_agree", "solo", MARGIN + 200, 104, size=12)
        self.c.drawString(MARGIN + 218, 108, "Solo parent / single decision-maker")

        self.nav(prev="decide_result", nxt="plan_p2")

    def page_my_plan_p2(self):
        self.new_page("My Plan — Routine & Commitment", "plan_p2")
        self.section_header("My Plan — Bedtime Routine & Commitment",
                            "Lock in the routine order now. Post it on the nursery door.",
                            "STEP 4 — PLAN", tag_color="teal")

        # bedtime routine builder
        self.card(MARGIN, 430, PAGE_W - 2*MARGIN, 290, fill="surface")
        self.label(MARGIN + 16, 700, "My Bedtime Routine — In Order", size=12, color="gold")
        self.text(MARGIN + 16, 684,
                  "Fill in the time for each step. Check when completed. This is the sequence — same every night.",
                  size=9, color="muted", max_w=480)

        routine_defaults = [
            "Dim lights / transition signal",
            "Stop stimulating activity — screens off",
            "Bath or warm wipe-down",
            "Lotion massage",
            "Pajamas and sleep sack on",
            "Feed — dim quiet room (baby not asleep)",
            "1 to 3 books or songs",
            "Final goodnight phrase (same words)",
            "White noise on",
            "Room fully dark",
            "Into crib — drowsy but awake",
            "Parent exits calmly",
        ]
        ry = 668
        for idx, step in enumerate(routine_defaults):
            self.chk(f"routine_chk_{idx}", MARGIN + 16, ry - 3, size=11)
            self.field(f"routine_time_{idx}", MARGIN + 34, ry - 2, 52, h=14, fsize=8,
                       tooltip=f"Time for: {step}")
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Roman", 9)
            self.c.drawString(MARGIN + 94, ry + 2, step)
            # custom override field
            self.field(f"routine_custom_{idx}", PAGE_W - MARGIN - 118, ry - 2, 110, h=14, fsize=8,
                       tooltip="Custom note for this step")
            ry -= 18

        # personality tip
        self.card(MARGIN, 290, PAGE_W - 2*MARGIN, 122, fill="navy")
        self.label(MARGIN + 16, 392, "Personality-Specific Tip", size=11, color="gold")
        self.text(MARGIN + 16, 376,
                  "Refer to your baby's sleep personality (from your plan page) and write the key adjustment below.",
                  size=9, color="muted", max_w=480)
        self.label(MARGIN + 16, 356, "My baby's type:", size=8)
        self.field("p2_personality_note", MARGIN + 110, 346, 350, h=20, fsize=10,
                   tooltip="Note your baby's personality and key approach")
        self.label(MARGIN + 16, 332, "Key adjustment for this type:", size=8)
        self.field("p2_personality_tip", MARGIN + 16, 302, PAGE_W - 2*MARGIN - 32, h=28,
                   multiline=True, fsize=10, tooltip="Write the specific adjustment for your baby's personality")

        # sleep promise checklist
        self.card(MARGIN, 100, PAGE_W - 2*MARGIN, 172, fill="surface2")
        self.label(MARGIN + 16, 252, "My Sleep Training Commitment", size=11, color="gold")
        promise_items = [
            "I chose this method deliberately. I will work it consistently.",
            "I will not change methods mid-week. Five nights minimum.",
            "I will decide my response before every night begins.",
            "I will wait before going in at night wakings.",
            "I will not judge the whole plan on one hard night.",
            "I will communicate the plan to everyone in the house.",
        ]
        cy = 234
        for i, item in enumerate(promise_items):
            self.chk(f"commit_{i}", MARGIN + 16, cy - 2, size=11)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Roman", 9.5)
            self.c.drawString(MARGIN + 34, cy + 2, item)
            cy -= 18

        self.affirm(7)
        self.nav(prev="my_plan", nxt="safe_sleep")

    # ── SAFE SLEEP CHECKLIST ──────────────────────────────────
    def page_safe_sleep(self):
        self.new_page("Safe Sleep Checklist", "safe_sleep")
        self.section_header("Safe Sleep Checklist",
                            "Run through this every night before you start the training routine.",
                            "SAFETY FIRST", tag_color="mint")

        self.card(MARGIN, 120, PAGE_W - 2*MARGIN, 560, fill="surface")
        self.label(MARGIN + 16, 660, "AAP-Aligned Safe Sleep Checklist", size=12, color="mint")
        self.text(MARGIN + 16, 644,
                  "Check every item before training begins. If any box cannot be checked, resolve it first.",
                  size=9, color="muted", max_w=480)

        safe_items = [
            ("sleep_surface", "THE SLEEP SURFACE", [
                "Firm flat mattress — no incline, wedge, or pillow-top",
                "Fitted sheet only — no loose blankets, bumpers, pillows, or positioners",
                "Baby placed on their back — every sleep, every time",
                "Sleep sack used instead of a loose blanket (correct tog for room temp)",
                "Sleep space is crib, bassinet, or play yard — not a swing or car seat",
            ]),
            ("room_env", "THE ROOM", [
                "Room temperature between 68 and 72 degrees F / 20 to 22 degrees C",
                "True blackout achieved — hand invisible in front of face",
                "White noise running at low continuous level — not inside the crib",
                "All monitor and device LEDs covered with tape",
                "No nightlight, or red-spectrum only",
            ]),
        ]

        yy = 622
        for section_id, section_title, items in safe_items:
            self.c.setFillColor(P["navy"])
            self.c.roundRect(MARGIN + 8, yy - 4, PAGE_W - 2*MARGIN - 16, 20, 4, fill=1, stroke=0)
            self.c.setFillColor(P["mint"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 16, yy + 2, section_title)
            yy -= 24
            for i, item in enumerate(items):
                self.chk(f"{section_id}_{i}", MARGIN + 16, yy - 2, size=12)
                self.c.setFillColor(P["cream"])
                self.c.setFont("Times-Roman", 10)
                self.c.drawString(MARGIN + 34, yy + 2, item)
                yy -= 20
            yy -= 8

        self.affirm(8)
        self.nav(prev="plan_p2", nxt="night_1")

    # ── NIGHTLY LOG ───────────────────────────────────────────
    def page_night_log(self, n):
        dest = f"night_{n}"
        prev_dest = "safe_sleep" if n == 1 else f"night_{n-1}"
        next_dest = f"night_{n+1}" if n < 21 else "weekly_summary_1"
        week_num = ((n - 1) // 7) + 1
        week_dest = f"weekly_summary_{week_num}"

        self.new_page(f"Night {n} Training Log", dest)

        # header with night/week indicator
        self.section_header(
            f"Night {n} — Training Log",
            f"Week {week_num} · Night {((n-1) % 7) + 1} of 7  ·  Objective notes only. No panic-decisions here.",
            f"NIGHT {n}", tag_color="lavender"
        )

        # top row: date, method reminder, baby mood
        self.card(MARGIN, 580, PAGE_W - 2*MARGIN, 78, fill="surface")
        self.lfield(MARGIN + 16, 600, 150, "Date", f"n{n}_date")
        self.lfield(210, 600, 150, "Method Used Tonight", f"n{n}_method")
        self.lfield(410, 600, 100, "Baby Mood at Bedtime", f"n{n}_mood")

        # main log fields
        self.card(MARGIN, 90, PAGE_W - 2*MARGIN, 476, fill="navy")
        self.label(MARGIN + 16, 548, "Night Log", size=12, color="lavender")

        yy = 532
        for label, hint, field_h in NIGHT_LOG_PROMPTS:
            self.label(MARGIN + 16, yy, label, size=8.5, color="gold")
            self.text(MARGIN + 16, yy - 12, hint, size=8, color="dim", max_w=200)
            self.field(f"n{n}_{label.lower().replace(' ', '_').replace('.','')[:20]}",
                       MARGIN + 220, yy - field_h + 10, PAGE_W - 2*MARGIN - 236, h=field_h - 8,
                       multiline=(field_h > 60), fsize=9,
                       tooltip=f"Night {n}: {label}")
            yy -= field_h + 4

        # consistency checklist
        self.card(MARGIN, 370, PAGE_W/2 - MARGIN/2 - 6, 160, fill="surface2") if False else None  # skip separate card
        # inline consistency mini-card
        self.card(MARGIN, 58, PAGE_W/2 - MARGIN - 4, 124, fill="surface2")
        self.label(MARGIN + 12, 162, "Consistency Check", size=9, color="lavender")
        mini_checks = CONSISTENCY_CHECKS[:5]
        cy = 148
        for i, item in enumerate(mini_checks):
            self.chk(f"n{n}_cons_{i}", MARGIN + 12, cy - 2, size=10)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 7.5)
            self.c.drawString(MARGIN + 28, cy + 1, item[:45])
            cy -= 18

        # tomorrow reminder card
        self.card(PAGE_W/2 + 6, 58, PAGE_W/2 - MARGIN - 4, 124, fill="surface")
        self.label(PAGE_W/2 + 20, 162, "Tomorrow's Reminder", size=9, color="gold")
        self.text(PAGE_W/2 + 20, 146,
                  "Write one thing you'll do differently or keep the same tonight.",
                  size=8, color="muted", max_w=195)
        self.field(f"n{n}_tomorrow", PAGE_W/2 + 20, 68, PAGE_W/2 - MARGIN - 30, h=64,
                   multiline=True, fsize=9,
                   tooltip=f"Night {n}: note for tomorrow")

        # affirm + nav
        self.affirm(n % len(AFFIRM))
        # week summary jump
        self.btn(PAGE_W/2 - 55, 36, 110, 18, f"Week {week_num} Summary", week_dest,
                 fill="surface2", size=8)
        self.nav(prev=prev_dest, nxt=next_dest)

    # ── WEEKLY SUMMARY ────────────────────────────────────────
    def page_weekly_summary(self, week_num):
        dest = f"weekly_summary_{week_num}"
        start_night = (week_num - 1) * 7 + 1
        end_night = min(week_num * 7, 21)
        prev_dest = f"night_{start_night}" if week_num == 1 else f"weekly_summary_{week_num - 1}"
        next_dest = f"weekly_summary_{week_num + 1}" if week_num < 3 else "cover"

        self.new_page(f"Week {week_num} Summary", dest)
        self.section_header(
            f"Week {week_num} Summary",
            f"Nights {start_night}–{end_night} · Honest reflection drives better decisions next week.",
            f"WEEK {week_num} REVIEW", tag_color="teal"
        )

        # stats grid
        self.card(MARGIN, 510, PAGE_W - 2*MARGIN, 190, fill="surface")
        self.label(MARGIN + 16, 680, "Sleep Stats This Week", size=12, color="gold")
        stats = [
            ("Best night", f"w{week_num}_best_night"),
            ("Hardest night", f"w{week_num}_hardest_night"),
            ("Avg. wakings / night", f"w{week_num}_avg_wakings"),
            ("Avg. settle time", f"w{week_num}_avg_settle"),
            ("Longest sleep stretch", f"w{week_num}_longest_stretch"),
            ("Consistency rating (1-10)", f"w{week_num}_consistency"),
        ]
        sx = MARGIN + 16
        sy = 660
        for i, (lbl, key) in enumerate(stats):
            if i % 2 == 0 and i > 0:
                sy -= 46
            xx = sx if i % 2 == 0 else sx + 240
            self.lfield(xx, sy, 200, lbl, key, h=20)

        # reflection questions
        self.card(MARGIN, 290, PAGE_W - 2*MARGIN, 204, fill="navy")
        self.label(MARGIN + 16, 474, "Weekly Reflection", size=12, color="gold")
        qs = [
            ("What went well?", f"w{week_num}_went_well"),
            ("What was the hardest moment?", f"w{week_num}_hardest"),
            ("What pattern did you notice?", f"w{week_num}_pattern"),
            ("One change for next week?", f"w{week_num}_change"),
        ]
        qy = 456
        for qlbl, qkey in qs:
            self.label(MARGIN + 16, qy, qlbl, size=8.5, color="gold")
            self.field(qkey, MARGIN + 16, qy - 30, PAGE_W - 2*MARGIN - 32, h=24,
                       multiline=False, fsize=10, tooltip=qlbl)
            qy -= 50

        # method check
        self.card(MARGIN, 120, PAGE_W - 2*MARGIN, 154, fill="surface2")
        self.label(MARGIN + 16, 254, "Method Assessment", size=11, color="gold")
        self.label(MARGIN + 16, 238, "Is your current method still right for your baby?", size=9, color="muted")

        options = [
            ("yes", "Yes — staying with it. Progress is happening."),
            ("adjust", "Mostly yes — small adjustment needed."),
            ("switch", "No — considering a switch (discuss with your partner first)."),
        ]
        oy = 220
        for val, lbl in options:
            self.radio_btn(f"w{week_num}_method_check", val, MARGIN + 16, oy - 4, size=12)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Roman", 9.5)
            self.c.drawString(MARGIN + 34, oy, lbl)
            oy -= 20

        self.label(MARGIN + 16, 140, "Notes on method assessment:", size=8)
        self.field(f"w{week_num}_method_notes", MARGIN + 16, 122, PAGE_W - 2*MARGIN - 32, h=16,
                   fsize=9, tooltip="Method assessment notes")

        self.affirm((week_num + 10) % len(AFFIRM))
        self.nav(prev=prev_dest, nxt=next_dest)

    # ========================================================
    # BUILD
    # ========================================================
    def build(self):
        self.page_cover()
        self.page_contents()
        self.page_decide_intro()
        self.page_method_cards()
        self._decision_page_a()
        self._decision_page_b()
        self.page_decide_result()
        self.page_ferber_guide()
        self.page_chair_schedule()
        self.page_my_plan()
        self.page_my_plan_p2()
        self.page_safe_sleep()

        for n in range(1, 22):
            self.page_night_log(n)

        for w in range(1, 4):
            self.page_weekly_summary(w)

        self._draw_footer()
        self.c.save()
        print(f"\n✓  Created: {os.path.abspath(self.filename)}")
        print(f"   Pages: {self.page_num}")
        print(f"   Sections: Cover · Contents · Decision Guide (6pp) · My Plan (2pp) · Safe Sleep · 21 Night Logs · 3 Weekly Summaries")


if __name__ == "__main__":
    WorkbookPDF("sleep_training_method_workbook.pdf").build()
