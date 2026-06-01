# couple_sync_planner.py
# We're In This Together — Couples Sleep Planner
# Premium interactive fillable PDF for two parents to coordinate night shifts
# Requires: pip install reportlab

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
import os
import math

# ============================================================
# BRAND / PALETTE  — warm romantic-meets-practical
# ============================================================

PAGE_W, PAGE_H = LETTER
MARGIN = 40

P = {
    "bg":          HexColor("#0C1520"),
    "surface":     HexColor("#162032"),
    "surface2":    HexColor("#1C2B40"),
    "navy":        HexColor("#1A2B45"),
    "navy_light":  HexColor("#223255"),
    "gold":        HexColor("#C9A84C"),
    "gold_light":  HexColor("#E8C97A"),
    "blush":       HexColor("#C97A8A"),
    "blush_light": HexColor("#E8A0B0"),
    "mint":        HexColor("#6ABFA0"),
    "sky":         HexColor("#6A9FBF"),
    "lavender":    HexColor("#9A8ABF"),
    "cream":       HexColor("#F0E8D8"),
    "muted":       HexColor("#8FA0B8"),
    "dim":         HexColor("#4A607A"),
    "rule":        HexColor("#2A3F5A"),
    "input_bg":    HexColor("#0D1720"),
    "input_bd":    HexColor("#2E4A6A"),
    "partner_a":   HexColor("#6A9FBF"),   # sky blue  – Parent A
    "partner_b":   HexColor("#C97A8A"),   # blush pink – Parent B
    "win":         HexColor("#6ABFA0"),   # mint green – celebration
    "warn":        HexColor("#E07A3A"),
    "white":       white,
    "black":       black,
}

# ─── CONTENT ───────────────────────────────────────────────

SHIFT_HOURS = [
    ("7 – 9 PM",   "Bedtime routine window"),
    ("9 – 11 PM",  "First-stretch guard"),
    ("11 PM – 1 AM", "Midnight watch"),
    ("1 – 3 AM",   "Deep-night shift"),
    ("3 – 5 AM",   "Pre-dawn watch"),
    ("5 – 7 AM",   "Early-morning rise"),
]

WIN_PROMPTS = [
    ("First full sleep stretch",   "Record the longest unbroken stretch this week"),
    ("Settled without a feed",     "Baby resettled without needing a feed"),
    ("Partner stepped in",         "Your partner handled it — you slept through"),
    ("Routine nailed",             "Routine completed in correct order every step"),
    ("New record",                 "Personal best for the week — any metric"),
]

CHECKIN_PROMPTS = [
    ("How rested do I feel today? (1–10)", "Be honest. This data matters."),
    ("One thing my partner did brilliantly last night", "Name it. Say it out loud too."),
    ("One thing I need from my partner tonight", "Be specific. Not 'help.' What exactly?"),
    ("My emotional state right now", "Exhausted / OK / Anxious / Hopeful / Other"),
]

CONFLICT_RULES = [
    "No sleep-deprivation decisions after midnight — escalate to morning.",
    "Whoever was on the previous shift speaks first. The other listens completely.",
    "Name feelings before naming problems: 'I feel _ when _.'",
    "If tone escalates — pause 60 seconds. Resume when both are calm.",
    "Disagreements about the method wait until daytime. Night = execute the plan.",
    "One person handles each waking. No double-intervention unless agreed.",
    "Credit out loud: 'You did great last night.' Say it. Mean it.",
]

WEEKLY_GOALS = [
    "Define who owns which shift for every night of this week",
    "Agree on the method and do NOT change it mid-week",
    "Complete at least one Couples Check-In before the week begins",
    "Log every night waking — both parents read the log each morning",
    "Call out one win per day, no matter how small",
]

CELEBRATION_MILESTONES = [
    ("3 consecutive nights", "Both parents slept >4 hours total", "Baby milestone!"),
    ("First 5-hour stretch", "Baby slept 5+ hours in one go", "Gold star night"),
    ("Week 1 complete",     "Survived and tracked the full first week", "You're a team"),
    ("Method is working",   "3+ nights of improvement trend", "Trust the process"),
    ("First full night",    "Baby slept through with zero wakings", "THE DREAM"),
]

NIGHT_WAKING_LOG_LABELS = [
    ("Time", 60), ("Who went?", 140), ("Duration", 240), ("Feed?", 320),
    ("Settle method", 390), ("Notes", 490),
]

AFFIRM_COUPLES = [
    "Sleep deprivation is a team sport. You're in this together.",
    "The plan you agree on tonight protects your relationship at 2 a.m.",
    "Gratitude spoken out loud changes the entire temperature of a hard night.",
    "One of you being rested helps both of you. Sleep shifts are a gift.",
    "You are not fighting each other. You are fighting sleep deprivation. Together.",
    "A plan agreed in daylight survives the dark.",
    "The baby will sleep. Your partnership outlasts every hard night.",
    "Two tired people with a shared plan beat two exhausted people with none.",
    "Name the win. Celebrate the inch. The mile comes later.",
    "You chose each other. You can do this.",
    "A good handoff is an act of love.",
    "The routine is the plan. The plan is the team.",
]

HANDOFF_ITEMS = [
    "Last waking time noted in the log",
    "Baby's current state (asleep / unsettled / just fed)",
    "Time of most recent feed",
    "White noise confirmed on",
    "Room confirmed dark and at correct temp",
    "Monitor charged / positioned",
    "Your partner is briefed — not guessing",
]

METHOD_AGREEMENT = [
    ("Extinction (CIO)", "No returns after crib placement. Hold firm together."),
    ("Ferber / Graduated", "Timed check-ins. Agree on intervals in advance."),
    ("Chair Method", "One parent stays. Move the chair every 2–3 nights."),
    ("Fading", "Gradual reduction. Slow and steady — be patient together."),
    ("Pick Up / Put Down", "Consistent pick-up / calm / put-down. Agree on count."),
]

# ============================================================
# PDF ENGINE
# ============================================================

class CouplePlannerPDF:
    def __init__(self, filename="couple_sync_sleep_planner.pdf"):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.c.setTitle("We're In This Together — Couples Sleep Planner")
        self.c.setAuthor("Six & Thriving")
        self.c.setSubject("Premium couples night-shift coordinator & sleep planner")
        self.c.setCreator("Python + ReportLab")
        self.form = self.c.acroForm
        self.page_num = 0

    # ── Core page helpers ──────────────────────────────────
    def new_page(self, section_title=None, bookmark=None, bg="bg"):
        if self.page_num > 0:
            self.draw_footer()
            self.c.showPage()
        self.page_num += 1
        self.draw_background(P[bg])
        if bookmark:
            self.c.bookmarkPage(bookmark)
            if section_title:
                self.c.addOutlineEntry(section_title, bookmark, level=0, closed=False)

    def draw_background(self, color):
        self.c.setFillColor(color)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    def draw_footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.line(MARGIN, 24, PAGE_W - MARGIN, 24)
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(P["muted"])
        self.c.drawString(MARGIN, 12, "We're In This Together — Couples Sleep Planner")
        self.c.drawRightString(PAGE_W - MARGIN, 12, f"Page {self.page_num}")

    def section_header(self, title, subtitle="", tag=None, title_color="gold_light"):
        y = PAGE_H - 54
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN, y - 52, PAGE_W - 2*MARGIN, 64, 12, fill=1, stroke=0)
        if tag:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 16, y - 8, tag)
        self.c.setFillColor(P[title_color])
        self.c.setFont("Times-Bold", 22)
        self.c.drawString(MARGIN + 16, y + 8, title)
        if subtitle:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 11)
            self.c.drawString(MARGIN + 16, y - 14, subtitle)

    def draw_card(self, x, y, w, h, fill="surface", radius=12, stroke_color=None, stroke_width=1):
        self.c.setFillColor(P[fill])
        if stroke_color:
            self.c.setStrokeColor(P[stroke_color])
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
            self.c.setLineWidth(stroke_width)
        else:
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

    def draw_label(self, x, y, text, size=9, color="muted", font="Helvetica-Bold"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawString(x, y, text)

    def draw_text(self, x, y, text, size=10, color="cream", font="Times-Roman", max_width=None, leading=None):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        leading = leading or (size + 3)
        if not max_width:
            self.c.drawString(x, y, text)
            return y - leading
        lines = simpleSplit(text, font, size, max_width)
        yy = y
        for line in lines:
            self.c.drawString(x, yy, line)
            yy -= leading
        return yy

    def draw_wrapped_bullets(self, x, y, items, width, bullet_color="gold", text_color="cream", size=10):
        yy = y
        for item in items:
            self.c.setFillColor(P[bullet_color])
            self.c.setFont("Helvetica-Bold", size)
            self.c.drawString(x, yy, "•")
            yy = self.draw_text(x + 14, yy, item, size=size, color=text_color, max_width=width - 14)
            yy -= 4
        return yy

    def partner_tag(self, x, y, label, partner="a"):
        color = "partner_a" if partner == "a" else "partner_b"
        self.c.setFillColor(P[color])
        self.c.roundRect(x, y, 72, 16, 8, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 8)
        tw = stringWidth(label, "Helvetica-Bold", 8)
        self.c.drawString(x + (72 - tw)/2, y + 4, label)

    # ── Navigation ─────────────────────────────────────────
    def add_link(self, x, y, w, h, text, dest, fill="surface2", txt="gold_light", size=9):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 10, fill=1, stroke=0)
        self.c.setFillColor(P[txt])
        self.c.setFont("Helvetica-Bold", size)
        tw = stringWidth(text, "Helvetica-Bold", size)
        self.c.drawString(x + (w - tw)/2, y + h/2 - 4, text)
        self.c.linkRect("", dest, (x, y, x + w, y + h), relative=0, thickness=0)

    def top_nav(self, prev_dest=None, next_dest=None, home_dest="cover"):
        y = 34
        if prev_dest:
            self.add_link(MARGIN, y, 90, 18, "◀  Previous", prev_dest, fill="surface2")
        self.add_link(PAGE_W/2 - 45, y, 90, 18, "⌂  Home", home_dest, fill="navy")
        if next_dest:
            self.add_link(PAGE_W - MARGIN - 90, y, 90, 18, "Next  ▶", next_dest, fill="gold", txt="bg")

    # ── Form field helpers ─────────────────────────────────
    def text_field(self, name, x, y, w, h=22, value="", multiline=False,
                   font_size=11, border="input_bd", fill="white", text_color="black", tooltip=None):
        self.form.textfield(
            name=name, tooltip=tooltip or name,
            x=x, y=y, width=w, height=h,
            borderStyle='inset',
            borderColor=P[border],
            fillColor=P[fill],
            textColor=P[text_color],
            forceBorder=True, value=value,
            fontName="Helvetica", fontSize=font_size,
            fieldFlags=('multiline' if multiline else '')
        )

    def checkbox(self, name, x, y, size=15, checked=False, tooltip=None):
        self.form.checkbox(
            name=name, tooltip=tooltip or name,
            x=x, y=y, size=size, checked=checked,
            buttonStyle='check',
            borderColor=P["gold"],
            fillColor=P["white"],
            textColor=P["gold"],
            forceBorder=True
        )

    def radio(self, group, value, x, y, size=15, selected=False, tooltip=None):
        self.form.radio(
            name=group, tooltip=tooltip or group,
            value=value, selected=selected,
            x=x, y=y, buttonStyle='circle',
            borderColor=P["gold"],
            fillColor=P["white"],
            textColor=P["gold"],
            forceBorder=True, size=size
        )

    def labeled_field(self, x, y, w, label, name, h=22, value="", multiline=False,
                      lines=1, label_color="muted", font_size=11):
        self.draw_label(x, y + h + 6, label, size=8, color=label_color)
        field_h = h if not multiline else max(h, 18 * lines)
        self.text_field(name, x, y, w, field_h, value=value,
                        multiline=multiline, font_size=font_size)
        return y - 8

    def partner_field_pair(self, x, y, w, label, base_name, h=22, font_size=11):
        """Two side-by-side partner fields with labels A and B."""
        half = (w - 10) // 2
        self.draw_label(x, y + h + 20, label, size=9, color="gold")
        self.partner_tag(x, y + h + 4, "PARENT A", "a")
        self.text_field(f"{base_name}_a", x, y, half, h, font_size=font_size)
        self.partner_tag(x + half + 10, y + h + 4, "PARENT B", "b")
        self.text_field(f"{base_name}_b", x + half + 10, y, half, h, font_size=font_size)
        return y - 8

    # ── Decorative helpers ─────────────────────────────────
    def star_divider(self, y, color="gold"):
        cx = PAGE_W / 2
        self.c.setFillColor(P[color])
        self.c.setFont("Helvetica", 10)
        self.c.drawCentredString(cx, y, "✦  ✦  ✦")

    def draw_hearts(self, cx, y, color="blush"):
        self.c.setFillColor(P[color])
        self.c.setFont("Helvetica", 14)
        self.c.drawCentredString(cx, y, "♡  ♡  ♡")

    def section_band(self, y, h, label, color="navy"):
        self.c.setFillColor(P[color])
        self.c.rect(0, y, PAGE_W, h, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(MARGIN, y + h/2 - 4, label.upper())

    # ============================================================
    # PAGES
    # ============================================================

    # ── 1. Cover ───────────────────────────────────────────
    def page_cover(self):
        self.new_page("Cover", "cover")

        # large blush accent bar
        self.c.setFillColor(P["blush"])
        self.c.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)
        self.c.setFillColor(P["partner_a"])
        self.c.rect(0, PAGE_H - 14, PAGE_W, 6, fill=1, stroke=0)

        # Subtitle tag
        self.c.setFillColor(P["surface2"])
        self.c.roundRect(MARGIN, PAGE_H - 90, PAGE_W - 2*MARGIN, 30, 8, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 10)
        tag = "SIX & THRIVING  ·  PREMIUM COUPLES EDITION"
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 72, tag)

        # Main title
        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Bold", 38)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 145, "We're In This")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 42)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 193, "Together")

        self.draw_hearts(PAGE_W/2, PAGE_H - 218, color="blush")

        self.c.setFillColor(P["muted"])
        self.c.setFont("Times-Italic", 14)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 240,
                                 "A Couples Sleep Coordination Planner")

        # ─ Partner name banner ─
        self.draw_card(MARGIN, PAGE_H - 330, PAGE_W - 2*MARGIN, 70, fill="navy", radius=14)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 278, "OUR NAMES")

        # Partner A
        self.c.setFillColor(P["partner_a"])
        self.c.roundRect(MARGIN + 12, PAGE_H - 320, 200, 28, 8, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(MARGIN + 22, PAGE_H - 304, "PARENT A")
        self.text_field("cover_name_a", MARGIN + 100, PAGE_H - 318, 108, 22,
                        font_size=12, tooltip="Parent A's name")

        # Partner B
        self.c.setFillColor(P["partner_b"])
        self.c.roundRect(PAGE_W - MARGIN - 212, PAGE_H - 320, 200, 28, 8, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(PAGE_W - MARGIN - 202, PAGE_H - 304, "PARENT B")
        self.text_field("cover_name_b", PAGE_W - MARGIN - 118, PAGE_H - 318, 108, 22,
                        font_size=12, tooltip="Parent B's name")

        # Baby name + start date
        self.draw_card(MARGIN, PAGE_H - 420, PAGE_W - 2*MARGIN, 70, fill="surface", radius=12)
        self.labeled_field(MARGIN + 16, PAGE_H - 412, 220, "Baby's Name", "baby_name_cover",
                           h=24, font_size=12, label_color="gold")
        self.labeled_field(PAGE_W/2 + 20, PAGE_H - 412, 200, "Plan Start Date", "start_date_cover",
                           h=24, font_size=12, label_color="gold")

        # What's inside
        self.draw_card(MARGIN, PAGE_H - 590, PAGE_W - 2*MARGIN, 150, fill="surface2", radius=12)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 11)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 460, "WHAT'S INSIDE THIS PLANNER")
        self.star_divider(PAGE_H - 475, color="dim")

        items = [
            "Partner Profiles — your individual sleep priorities and limits",
            "Shift Scheduler — who handles which hours, every night",
            "Shared Night Log — both parents read the same data each morning",
            "Couples Check-In — daily 2-minute sync to stay aligned",
            "The Conflict Resolution Ground Rules — agreed before night falls",
            "Win Wall — celebrate every milestone together",
            "Weekly Review — reflect, adjust, and recommit as a team",
        ]
        y = PAGE_H - 498
        for item in items:
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(MARGIN + 16, y, "▸")
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 9)
            self.c.drawString(MARGIN + 28, y, item)
            y -= 16

        # Affirm quote
        self.draw_card(MARGIN, PAGE_H - 690, PAGE_W - 2*MARGIN, 76, fill="navy", radius=12)
        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Times-Italic", 12)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 646,
                                 '"You are not fighting each other.')
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 663,
                                 'You are fighting sleep deprivation. Together."')
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 9)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 680, "— Six & Thriving")

        # Nav
        nav_items = [
            ("Partner Profiles", "profiles", MARGIN),
            ("Shift Planner", "shift_week_1", MARGIN + 126),
            ("Night Log", "log_week_1", MARGIN + 252),
            ("Wins & Milestones", "wins", MARGIN + 378),
        ]
        for label, dest, x in nav_items:
            self.add_link(x, 58, 118, 22, label, dest, fill="surface2", txt="gold_light", size=9)

        # bottom accent
        self.c.setFillColor(P["partner_b"])
        self.c.rect(0, 0, PAGE_W, 6, fill=1, stroke=0)
        self.c.setFillColor(P["partner_a"])
        self.c.rect(0, 6, PAGE_W, 4, fill=1, stroke=0)

    # ── 2. Partner Profiles ────────────────────────────────
    def page_profiles(self):
        self.new_page("Partner Profiles", "profiles")
        self.section_header("Partner Profiles",
                            "Before the plan — understand each other's limits and strengths.",
                            tag="FOUNDATION")

        def partner_profile_block(x, y, w, h, partner, color_key, name_key, fields):
            self.draw_card(x, y, w, h, fill="surface", radius=14,
                           stroke_color=color_key, stroke_width=2)
            self.c.setFillColor(P[color_key])
            self.c.roundRect(x, y + h - 28, w, 28, 14, fill=1, stroke=0)
            self.c.rect(x, y + h - 28, w, 14, fill=1, stroke=0)
            self.c.setFillColor(P["white"])
            self.c.setFont("Helvetica-Bold", 11)
            self.c.drawCentredString(x + w/2, y + h - 14, partner.upper())

            yy = y + h - 54
            for label, fname, fh, multi in fields:
                self.draw_label(x + 14, yy + fh + 8, label, size=8, color="muted")
                self.text_field(f"{name_key}_{fname}", x + 14, yy, w - 28, fh,
                                multiline=multi, font_size=10)
                yy -= fh + 22

        fields_a = [
            ("My name", "name", 22, False),
            ("My biggest struggle with sleep deprivation", "struggle", 36, True),
            ("My best time-of-night shift (I handle nights better at...)", "best_shift", 22, False),
            ("My hard limit — hours I absolutely need to function", "limit", 22, False),
            ("My signal that I need relief URGENTLY", "relief_signal", 22, False),
            ("How I best receive support from my partner", "support_style", 36, True),
        ]
        fields_b = [f for f in fields_a]

        partner_profile_block(MARGIN, 120, (PAGE_W - 2*MARGIN - 16)/2, 490,
                              "Parent A", "partner_a", "pa", fields_a)
        partner_profile_block(PAGE_W/2 + 8, 120, (PAGE_W - 2*MARGIN - 16)/2, 490,
                              "Parent B", "partner_b", "pb", fields_b)

        self.star_divider(100, color="dim")
        self.draw_text(MARGIN, 84,
                       "Share your answers with each other before the plan begins. This page is your foundation.",
                       size=9, color="muted", max_width=PAGE_W - 2*MARGIN)

        self.top_nav(prev_dest="cover", next_dest="ground_rules")

    # ── 3. Ground Rules ────────────────────────────────────
    def page_ground_rules(self):
        self.new_page("Ground Rules", "ground_rules")
        self.section_header("Our Conflict-Free Night Rules",
                            "Agreed together, signed together. No amendments after 9 PM.",
                            tag="PARTNERSHIP")

        self.draw_card(MARGIN, 480, PAGE_W - 2*MARGIN, 220, fill="surface", radius=14)
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN, 672, PAGE_W - 2*MARGIN, 30, 14, fill=1, stroke=0)
        self.c.rect(MARGIN, 672, PAGE_W - 2*MARGIN, 14, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawCentredString(PAGE_W/2, 682, "THE SEVEN RULES WE BOTH AGREE TO")

        y = 654
        for i, rule in enumerate(CONFLICT_RULES, 1):
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 14, y, f"{i}.")
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 9)
            self.c.drawString(MARGIN + 30, y, rule)
            y -= 28

        # ADD OUR OWN RULE
        self.draw_card(MARGIN, 370, PAGE_W - 2*MARGIN, 90, fill="surface2", radius=12)
        self.draw_label(MARGIN + 14, 440, "Our Own Rule (add one together)", size=9, color="gold")
        self.text_field("our_rule", MARGIN + 14, 380, PAGE_W - 2*MARGIN - 28, 48,
                        multiline=True, font_size=11,
                        tooltip="Write a custom rule that fits your family")

        # METHOD AGREEMENT
        self.draw_card(MARGIN, 190, PAGE_W - 2*MARGIN, 160, fill="navy", radius=12)
        self.draw_label(MARGIN + 14, 330, "Our Agreed Sleep Method This Week", size=10, color="gold")
        self.draw_label(MARGIN + 14, 314, "Circle one. Do not change it mid-week.", size=8, color="muted")

        y = 292
        for i, (method, principle) in enumerate(METHOD_AGREEMENT):
            rx = MARGIN + 14
            self.radio("method_choice", str(i+1), rx, y - 2, size=13,
                       tooltip=method)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(rx + 18, y + 6, method)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(rx + 18, y - 6, principle)
            y -= 26

        # SIGNATURES
        self.draw_card(MARGIN, 80, PAGE_W - 2*MARGIN, 90, fill="surface", radius=12)
        self.draw_label(MARGIN + 14, 152, "We agree to these rules. Signed:", size=9, color="gold")
        self.draw_label(MARGIN + 14, 132, "Parent A Initials", size=8, color="muted")
        self.text_field("sig_a", MARGIN + 14, 108, 180, 22, font_size=12)
        self.draw_label(PAGE_W/2 + 20, 132, "Parent B Initials", size=8, color="muted")
        self.text_field("sig_b", PAGE_W/2 + 20, 108, 180, 22, font_size=12)
        self.draw_label(PAGE_W - MARGIN - 100, 132, "Date", size=8, color="muted")
        self.text_field("sig_date", PAGE_W - MARGIN - 100, 108, 90, 22, font_size=11)

        self.top_nav(prev_dest="profiles", next_dest="shift_week_1")

    # ── 4. Shift Scheduler (4 weeks) ──────────────────────
    def page_shift_scheduler(self, week):
        dest = f"shift_week_{week}"
        prev = f"ground_rules" if week == 1 else f"log_week_{week-1}_b"
        nxt = f"log_week_{week}"

        self.new_page(f"Week {week} Shift Scheduler", dest)
        self.section_header(f"Week {week} · Night Shift Schedule",
                            "Assign every shift before the week begins. No guessing at midnight.",
                            tag=f"WEEK {week}")

        # Legend
        self.draw_card(MARGIN, 640, PAGE_W - 2*MARGIN, 28, fill="surface2", radius=8)
        self.c.setFillColor(P["partner_a"])
        self.c.roundRect(MARGIN + 12, 646, 60, 16, 6, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawCentredString(MARGIN + 42, 651, "PARENT A")
        self.c.setFillColor(P["partner_b"])
        self.c.roundRect(MARGIN + 82, 646, 60, 16, 6, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.drawCentredString(MARGIN + 112, 651, "PARENT B")
        self.c.setFillColor(P["surface"])
        self.c.roundRect(MARGIN + 152, 646, 60, 16, 6, fill=1, stroke=0)
        self.c.setFillColor(P["muted"])
        self.c.drawCentredString(MARGIN + 182, 651, "TOGETHER")
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 8)
        self.c.drawString(MARGIN + 230, 651,
                          "← Use radio buttons to assign each night's shift owner")

        DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        COL_W = (PAGE_W - 2*MARGIN - 100) / 7
        HEADER_H = 22
        ROW_H = 74
        TABLE_TOP = 626

        # Day headers
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 100, TABLE_TOP - HEADER_H, PAGE_W - 2*MARGIN - 100, HEADER_H, 8, fill=1, stroke=0)
        for d, day in enumerate(DAYS):
            cx = MARGIN + 100 + d * COL_W + COL_W/2
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawCentredString(cx, TABLE_TOP - HEADER_H + 7, day)

        # Shift rows
        for r, (shift, hint) in enumerate(SHIFT_HOURS):
            row_y = TABLE_TOP - HEADER_H - (r + 1) * ROW_H
            fill = "surface" if r % 2 == 0 else "surface2"
            self.draw_card(MARGIN, row_y, PAGE_W - 2*MARGIN, ROW_H, fill=fill, radius=0)

            # Shift label column
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 6, row_y + ROW_H - 16, shift)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7)
            for i2, word in enumerate(hint.split()):
                self.c.drawString(MARGIN + 6, row_y + ROW_H - 28 - i2 * 10, word)

            # Radio cells per day
            for d in range(7):
                cx = MARGIN + 100 + d * COL_W
                rb_x = cx + COL_W/2 - 22
                rb_y = row_y + ROW_H - 24

                # A / B / T radio buttons stacked
                gname = f"w{week}_shift_r{r}_d{d}"
                self.radio(gname, "A", rb_x, rb_y, size=12, tooltip=f"{shift} {DAYS[d]} – Parent A")
                self.c.setFillColor(P["partner_a"])
                self.c.setFont("Helvetica-Bold", 7)
                self.c.drawString(rb_x + 14, rb_y + 2, "A")

                self.radio(gname, "B", rb_x, rb_y - 20, size=12, tooltip=f"{shift} {DAYS[d]} – Parent B")
                self.c.setFillColor(P["partner_b"])
                self.c.drawString(rb_x + 14, rb_y - 18, "B")

                self.radio(gname, "T", rb_x, rb_y - 40, size=12, tooltip=f"{shift} {DAYS[d]} – Together")
                self.c.setFillColor(P["muted"])
                self.c.setFont("Helvetica", 7)
                self.c.drawString(rb_x + 14, rb_y - 38, "Both")

        # Notes section
        bot_y = TABLE_TOP - HEADER_H - len(SHIFT_HOURS) * ROW_H - 10
        self.draw_card(MARGIN, bot_y - 68, PAGE_W - 2*MARGIN, 68, fill="navy", radius=10)
        self.draw_label(MARGIN + 14, bot_y - 14, "Week Notes (method, special circumstances)", size=9, color="gold")
        self.text_field(f"w{week}_shift_notes", MARGIN + 14, bot_y - 58, PAGE_W - 2*MARGIN - 28, 36,
                        multiline=True, font_size=10)

        self.top_nav(prev_dest=prev, next_dest=nxt)

    # ── 5. Night Log (7 nights, 2 pages/week) ─────────────
    def page_night_log(self, week):
        dest = f"log_week_{week}"
        dest_b = f"log_week_{week}_b"
        prev_shift = f"shift_week_{week}"
        nxt_check = f"checkin_week_{week}"

        # PAGE A – nights 1–4
        self.new_page(f"Week {week} Night Log A", dest)
        self.section_header(f"Week {week} · Night Waking Log",
                            "Both parents read this log every morning — no surprises.",
                            tag=f"WEEK {week}")

        for night in range(1, 5):
            self._draw_night_block(week, night, 640 - (night-1) * 136)

        self.top_nav(prev_dest=prev_shift, next_dest=dest_b)

        # PAGE B – nights 5–7
        self.new_page(f"Week {week} Night Log B", dest_b)
        self.section_header(f"Week {week} · Night Waking Log (cont.)",
                            "Patterns emerge by day 3–4. Stick with the method.",
                            tag=f"WEEK {week}")

        for night in range(5, 8):
            self._draw_night_block(week, night, 640 - (night-5) * 160)

        # Weekly totals mini-card
        self.draw_card(MARGIN, 100, PAGE_W - 2*MARGIN, 80, fill="navy", radius=10)
        self.draw_label(MARGIN + 14, 162, "Week Summary Totals", size=10, color="gold")
        mini = [
            ("Total wakings", f"w{week}_total_wakings", 68),
            ("Avg. settle time", f"w{week}_avg_settle", 200),
            ("Longest stretch", f"w{week}_longest", 332),
            ("Best night", f"w{week}_best_night", 464),
        ]
        for label, fname, x in mini:
            self.draw_label(x, 140, label, size=8, color="muted")
            self.text_field(fname, x, 112, 120, 22, font_size=10)

        nxt = f"shift_week_{week+1}" if week < 4 else "wins"
        self.top_nav(prev_dest=dest, next_dest=nxt_check)

    def _draw_night_block(self, week, night, y):
        h = 118
        fill = "surface" if night % 2 else "surface2"
        self.draw_card(MARGIN, y - h, PAGE_W - 2*MARGIN, h, fill=fill, radius=10)

        # Header bar
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN, y - 20, PAGE_W - 2*MARGIN, 20, 10, fill=1, stroke=0)
        self.c.rect(MARGIN, y - 20, PAGE_W - 2*MARGIN, 10, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(MARGIN + 12, y - 13, f"NIGHT {night}")

        # Column headers
        cols = [("Time", 60), ("Who?", 130), ("Duration", 210), ("Feed?", 290),
                ("Method used", 350), ("Notes", 460)]
        for label, cx in cols:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica-Bold", 7)
            self.c.drawString(MARGIN + cx - 40 + 40, y - 34, label)

        # 2 waking rows
        for row in range(2):
            ry = y - 58 - row * 36
            for (label, cx) in cols:
                fw = 58 if cx < 400 else 100
                self.text_field(f"w{week}_n{night}_r{row}_{label.lower().replace(' ','_').replace('?','').strip()}",
                                MARGIN + cx - 5, ry, fw, 22, font_size=9)

        # On-duty badge
        self.c.setFillColor(P["dim"])
        self.c.roundRect(MARGIN + PAGE_W - 2*MARGIN - 120, y - 20, 110, 18, 6, fill=1, stroke=0)
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 7)
        self.c.drawString(MARGIN + PAGE_W - 2*MARGIN - 116, y - 13, "On duty tonight:")
        self.radio(f"w{week}_n{night}_duty", "A",
                   MARGIN + PAGE_W - 2*MARGIN - 116, y - h + 10, size=10, tooltip="Parent A on duty")
        self.c.setFillColor(P["partner_a"])
        self.c.setFont("Helvetica-Bold", 7)
        self.c.drawString(MARGIN + PAGE_W - 2*MARGIN - 104, y - h + 14, "A")
        self.radio(f"w{week}_n{night}_duty", "B",
                   MARGIN + PAGE_W - 2*MARGIN - 80, y - h + 10, size=10, tooltip="Parent B on duty")
        self.c.setFillColor(P["partner_b"])
        self.c.drawString(MARGIN + PAGE_W - 2*MARGIN - 68, y - h + 14, "B")

    # ── 6. Daily Check-In ──────────────────────────────────
    def page_checkin(self, week):
        dest = f"checkin_week_{week}"
        prev = f"log_week_{week}_b"
        nxt = f"shift_week_{week+1}" if week < 4 else "wins"

        self.new_page(f"Week {week} Daily Check-In", dest)
        self.section_header(f"Week {week} · Daily Couples Check-In",
                            "Two minutes every morning. Same time. No phones. Eyes on each other.",
                            tag=f"WEEK {week}")

        for day in range(1, 8):
            day_y = 660 - (day - 1) * 78
            fill = "surface" if day % 2 else "surface2"
            self.draw_card(MARGIN, day_y - 60, PAGE_W - 2*MARGIN, 68, fill=fill, radius=8)

            # Day label
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 10, day_y - 6, f"DAY {day}")

            # How rested? A and B
            self.draw_label(MARGIN + 60, day_y - 6, "Rest score A (1–10)", size=7, color="muted")
            self.text_field(f"w{week}_ci_d{day}_rest_a", MARGIN + 60, day_y - 28, 50, 18, font_size=10)
            self.draw_label(MARGIN + 120, day_y - 6, "Rest score B (1–10)", size=7, color="muted")
            self.text_field(f"w{week}_ci_d{day}_rest_b", MARGIN + 120, day_y - 28, 50, 18, font_size=10)

            # Shoutout
            self.draw_label(MARGIN + 180, day_y - 6, "Today's shoutout to my partner", size=7, color="muted")
            self.text_field(f"w{week}_ci_d{day}_shoutout", MARGIN + 180, day_y - 28, 180, 18, font_size=9)

            # Tonight's on-duty
            self.draw_label(MARGIN + 370, day_y - 6, "Tonight's lead:", size=7, color="muted")
            self.radio(f"w{week}_ci_d{day}_lead", "A", MARGIN + 370, day_y - 28, size=12)
            self.c.setFillColor(P["partner_a"])
            self.c.setFont("Helvetica-Bold", 7)
            self.c.drawString(MARGIN + 384, day_y - 24, "A")
            self.radio(f"w{week}_ci_d{day}_lead", "B", MARGIN + 400, day_y - 28, size=12)
            self.c.setFillColor(P["partner_b"])
            self.c.drawString(MARGIN + 414, day_y - 24, "B")

            # Need tonight
            self.draw_label(MARGIN + 430, day_y - 6, "I need tonight:", size=7, color="muted")
            self.text_field(f"w{week}_ci_d{day}_need", MARGIN + 430, day_y - 28, 100, 18, font_size=9)

        self.star_divider(84, color="dim")
        self.draw_text(MARGIN, 72,
                       "Tip: Do this check-in at the same time each day — morning coffee is ideal. "
                       "Keep it to 2 minutes. No longer.",
                       size=9, color="muted", max_width=PAGE_W - 2*MARGIN)

        self.top_nav(prev_dest=prev, next_dest=nxt)

    # ── 7. Wins & Milestones ───────────────────────────────
    def page_wins(self):
        self.new_page("Wins & Milestones", "wins")
        self.section_header("Win Wall",
                            "Every win celebrated here. No win too small.",
                            tag="CELEBRATE", title_color="win")

        # Milestone checkboxes
        self.draw_card(MARGIN, 520, PAGE_W - 2*MARGIN, 160, fill="surface", radius=12)
        self.draw_label(MARGIN + 14, 660, "Track These Milestones", size=10, color="gold")
        y = 636
        for milestone, desc, badge in CELEBRATION_MILESTONES:
            self.checkbox(f"milestone_{milestone.replace(' ','_')}", MARGIN + 14, y - 4, size=14,
                          tooltip=milestone)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 34, y + 2, milestone)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(MARGIN + 200, y + 2, desc)
            self.c.setFillColor(P["win"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(PAGE_W - MARGIN - 100, y + 2, badge)
            y -= 26

        # Free-form win log
        self.draw_card(MARGIN, 280, PAGE_W - 2*MARGIN, 230, fill="surface2", radius=12)
        self.draw_label(MARGIN + 14, 492, "Our Custom Win Journal", size=10, color="gold")
        self.draw_label(MARGIN + 14, 476, "Write every tiny victory here — they compound.", size=8, color="muted")

        win_y = 456
        for i in range(7):
            self.c.setFillColor(P["win"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 14, win_y, "★")
            self.text_field(f"win_entry_{i+1}", MARGIN + 32, win_y - 4, PAGE_W - 2*MARGIN - 50, 22,
                            font_size=10, tooltip=f"Win #{i+1}")
            win_y -= 30

        # Shoutout wall
        self.draw_card(MARGIN, 100, PAGE_W - 2*MARGIN, 160, fill="navy", radius=12)
        self.draw_label(MARGIN + 14, 242, "Partner Shoutouts — Hall of Fame", size=10, color="blush_light")
        self.draw_label(MARGIN + 14, 226, "Write the specific moments when your partner showed up for you.",
                        size=8, color="muted")
        self.draw_label(MARGIN + 14, 206, "Parent A says about Parent B:", size=8, color="partner_a")
        self.text_field("shoutout_a_to_b", MARGIN + 14, 178, PAGE_W - 2*MARGIN - 28, 24,
                        font_size=10, tooltip="Parent A shoutout")
        self.draw_label(MARGIN + 14, 160, "Parent B says about Parent A:", size=8, color="partner_b")
        self.text_field("shoutout_b_to_a", MARGIN + 14, 132, PAGE_W - 2*MARGIN - 28, 24,
                        font_size=10, tooltip="Parent B shoutout")

        self.top_nav(prev_dest="checkin_week_4", next_dest="weekly_review_w1")

    # ── 8. Weekly Review (shared) ─────────────────────────
    def page_weekly_review(self, week):
        dest = f"weekly_review_w{week}"
        prev = f"wins" if week == 1 else f"weekly_review_w{week-1}"
        nxt = f"weekly_review_w{week+1}" if week < 4 else "handoff"

        self.new_page(f"Week {week} Weekly Review", dest)
        self.section_header(f"Week {week} · Couples Weekly Review",
                            "Sit down together. 10 minutes. Phones away. Eyes on the plan.",
                            tag=f"WEEK {week}")

        # Stats side by side
        self.draw_card(MARGIN, 580, PAGE_W - 2*MARGIN, 110, fill="surface", radius=12)
        self.draw_label(MARGIN + 14, 672, "Weekly Stats", size=10, color="gold")

        stat_fields = [
            ("Total night wakings", "total_wakings"),
            ("Avg. wakings / night", "avg_wakings"),
            ("Longest sleep stretch", "longest_stretch"),
            ("Avg. bedtime achieved", "avg_bedtime"),
            ("Best night #", "best_night"),
            ("Hardest night #", "hardest_night"),
        ]
        x_pos = [MARGIN + 14, MARGIN + 14 + 170, MARGIN + 14 + 340]
        yy = 650
        for i, (label, key) in enumerate(stat_fields):
            xp = x_pos[i % 3]
            if i == 3: yy -= 44
            self.draw_label(xp, yy, label, size=7, color="muted")
            self.text_field(f"w{week}_rev_{key}", xp, yy - 20, 150, 18, font_size=10)

        # Joint reflection questions
        questions = [
            ("What worked best this week?", "worked_best", False, 28),
            ("What we want to do differently next week", "different_next", True, 48),
            ("How are WE doing as a couple — be honest", "couple_health", True, 48),
            ("One thing I appreciate about my partner this week", "appreciate", False, 28),
        ]
        qy = 556
        for label, key, multi, fh in questions:
            self.draw_card(MARGIN, qy - fh - 18, PAGE_W - 2*MARGIN, fh + 28, fill="surface2", radius=8)
            self.draw_label(MARGIN + 14, qy - 4, label, size=9, color="gold_light")
            self.text_field(f"w{week}_rev_{key}", MARGIN + 14, qy - fh - 8,
                            PAGE_W - 2*MARGIN - 28, fh, multiline=multi, font_size=10)
            qy -= fh + 38

        # Weekly goal checklist
        self.draw_card(MARGIN, 100, PAGE_W - 2*MARGIN, 100, fill="navy", radius=10)
        self.draw_label(MARGIN + 14, 182, "Did we hit our weekly goals?", size=9, color="gold")
        gy = 162
        for i, goal in enumerate(WEEKLY_GOALS[:3]):
            self.checkbox(f"w{week}_goal_{i+1}", MARGIN + 14, gy - 4, size=12)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(MARGIN + 30, gy + 2, goal)
            gy -= 20

        # Affirmation
        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Times-Italic", 11)
        self.c.drawCentredString(PAGE_W/2, 82,
                                 f'"{AFFIRM_COUPLES[min(week-1, len(AFFIRM_COUPLES)-1)]}"')

        self.top_nav(prev_dest=prev, next_dest=nxt)

    # ── 9. Handoff Protocol ────────────────────────────────
    def page_handoff(self):
        self.new_page("Handoff Protocol", "handoff")
        self.section_header("The Perfect Handoff Protocol",
                            "A clean shift handoff prevents 3 AM arguments. Use this every time.",
                            tag="OPERATIONS")

        # The 7-point handoff checklist
        self.draw_card(MARGIN, 480, PAGE_W - 2*MARGIN, 200, fill="surface", radius=12)
        self.draw_label(MARGIN + 14, 662, "Before You Hand Over — Check Every Box", size=10, color="gold")

        hy = 636
        for i, item in enumerate(HANDOFF_ITEMS):
            self.checkbox(f"handoff_check_{i+1}", MARGIN + 14, hy - 4, size=14, tooltip=item)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 9)
            self.c.drawString(MARGIN + 34, hy + 2, item)
            hy -= 24

        # Handoff note field (fillable nightly)
        self.draw_card(MARGIN, 330, PAGE_W - 2*MARGIN, 140, fill="surface2", radius=12)
        self.draw_label(MARGIN + 14, 452, "Tonight's Handoff Note", size=10, color="gold")
        self.draw_label(MARGIN + 14, 436, "Leave this for your partner before you sleep.", size=8, color="muted")

        handoff_fields = [
            ("Last waking at:", "handoff_last_wake", 60, 22),
            ("Baby's mood / state:", "handoff_state", 300, 22),
            ("Last fed at:", "handoff_last_fed", 60, 22),
        ]
        hfy = 404
        for label, fname, x, fh in handoff_fields:
            self.draw_label(x + MARGIN + 10, hfy + 4, label, size=8, color="muted")
            self.text_field(fname, x + MARGIN + 10 + stringWidth(label, "Helvetica-Bold", 8) + 6,
                            hfy - 4, 120, fh, font_size=10)
        self.draw_label(MARGIN + 14, 370, "Anything my partner needs to know:", size=8, color="muted")
        self.text_field("handoff_notes", MARGIN + 14, 336, PAGE_W - 2*MARGIN - 28, 28,
                        multiline=True, font_size=10)

        # Communication scripts
        self.draw_card(MARGIN, 140, PAGE_W - 2*MARGIN, 180, fill="navy", radius=12)
        self.draw_label(MARGIN + 14, 304, "What to Say Instead of Fighting", size=10, color="blush_light")
        self.draw_label(MARGIN + 14, 286, "Pre-agreed language for hard moments:", size=8, color="muted")

        scripts = [
            ("Instead of: 'Why didn't you go in?'",
             "Say: 'Can you take the next one? I'm running empty.'"),
            ("Instead of: 'You never help.'",
             "Say: 'I need you to own tonight. I need sleep urgently.'"),
            ("Instead of: 'You're doing it wrong.'",
             "Say: 'Let's check the plan together in the morning.'"),
            ("Instead of: 'I'm so exhausted.'",
             "Say: 'Sleep deprived. I need relief in __ hours. Can you?'"),
        ]
        sy = 264
        for wrong, right in scripts:
            self.c.setFillColor(P["warn"])
            self.c.setFont("Helvetica", 7)
            self.c.drawString(MARGIN + 14, sy, wrong)
            self.c.setFillColor(P["mint"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(MARGIN + 14, sy - 14, right)
            sy -= 34

        self.top_nav(prev_dest="weekly_review_w4", next_dest="sleep_promise")

    # ── 10. Sleep Promise (couples version) ───────────────
    def page_sleep_promise(self):
        self.new_page("Our Sleep Promise", "sleep_promise")
        self.section_header("Our Shared Sleep Promise",
                            "A commitment to your baby — and to each other.",
                            tag="COMMITMENT")

        self.draw_card(MARGIN, 250, PAGE_W - 2*MARGIN, 400, fill="surface", radius=14)
        self.draw_label(MARGIN + 14, 630, "We commit, together:", size=10, color="gold")

        promises = [
            "We will decide the method together and not change it without a daytime conversation.",
            "We will keep the bedtime routine in the same order, every night, no shortcuts.",
            "We will log every night waking so we are both working from the same reality.",
            "We will do the daily 2-minute check-in, even when we're too tired to want to.",
            "We will credit each other out loud — especially on the hard nights.",
            "We will not argue about the method after 9 PM.",
            "We will not wake a sleeping partner unless absolutely necessary.",
            "We will celebrate every win, no matter how small, and write it in the Win Wall.",
            "We will remember: we are not fighting each other. We are fighting sleep deprivation.",
        ]

        py = 604
        for i, promise in enumerate(promises):
            self.checkbox(f"promise_{i+1}", MARGIN + 14, py - 4, size=14)
            py = self.draw_text(MARGIN + 34, py + 2, promise, size=9, color="cream",
                                max_width=PAGE_W - 2*MARGIN - 50)
            py -= 8

        # Dual signature
        self.draw_card(MARGIN, 120, PAGE_W - 2*MARGIN, 115, fill="navy", radius=12)
        self.draw_label(MARGIN + 14, 218, "Signed with love:", size=9, color="gold")

        # A
        self.c.setFillColor(P["partner_a"])
        self.c.roundRect(MARGIN + 14, 150, 220, 56, 10, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(MARGIN + 24, 194, "PARENT A — Signature")
        self.text_field("promise_sig_a", MARGIN + 24, 158, 200, 30, font_size=13)

        # B
        self.c.setFillColor(P["partner_b"])
        self.c.roundRect(PAGE_W - MARGIN - 234, 150, 220, 56, 10, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(PAGE_W - MARGIN - 224, 194, "PARENT B — Signature")
        self.text_field("promise_sig_b", PAGE_W - MARGIN - 224, 158, 200, 30, font_size=13)

        # Date
        self.draw_label(PAGE_W/2 - 40, 148, "Date:", size=8, color="gold")
        self.text_field("promise_date", PAGE_W/2 - 40, 128, 80, 18, font_size=10)

        self.top_nav(prev_dest="handoff", next_dest="cover")

    # ── Table of Contents ──────────────────────────────────
    def page_toc(self):
        self.new_page("Table of Contents", "toc")
        self.section_header("Table of Contents",
                            "Navigate your planner — every section links directly.",
                            tag="NAVIGATION")

        toc_entries = [
            ("Partner Profiles", "profiles", "Set up your individual sleep bios"),
            ("Ground Rules & Method Agreement", "ground_rules", "Agree before nightfall"),
            ("Week 1 Shift Scheduler", "shift_week_1", "Assign every shift for the week"),
            ("Week 1 Night Log", "log_week_1", "Log every waking together"),
            ("Week 1 Daily Check-In", "checkin_week_1", "2-minute morning sync"),
            ("Week 2 Shift Scheduler", "shift_week_2", ""),
            ("Week 2 Night Log", "log_week_2", ""),
            ("Week 2 Daily Check-In", "checkin_week_2", ""),
            ("Week 3 Shift Scheduler", "shift_week_3", ""),
            ("Week 3 Night Log", "log_week_3", ""),
            ("Week 3 Daily Check-In", "checkin_week_3", ""),
            ("Week 4 Shift Scheduler", "shift_week_4", ""),
            ("Week 4 Night Log", "log_week_4", ""),
            ("Week 4 Daily Check-In", "checkin_week_4", ""),
            ("Win Wall & Milestones", "wins", "Celebrate every victory"),
            ("Weekly Reviews (1–4)", "weekly_review_w1", "Reflect and adjust together"),
            ("Handoff Protocol", "handoff", "Clean shift changeover every time"),
            ("Our Shared Sleep Promise", "sleep_promise", "Sign together"),
        ]

        self.draw_card(MARGIN, 84, PAGE_W - 2*MARGIN, 570, fill="surface", radius=12)
        y = 628
        for i, (title, dest, hint) in enumerate(toc_entries):
            fill = "surface2" if i % 2 == 0 else "surface"
            self.draw_card(MARGIN + 8, y - 16, PAGE_W - 2*MARGIN - 16, 24, fill=fill, radius=6)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(MARGIN + 18, y - 8, title)
            if hint:
                self.c.setFillColor(P["muted"])
                self.c.setFont("Helvetica", 8)
                self.c.drawString(MARGIN + 240, y - 8, hint)
            # clickable row
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawRightString(PAGE_W - MARGIN - 18, y - 8, "GO →")
            self.c.linkRect("", dest,
                            (MARGIN + 8, y - 16, PAGE_W - MARGIN - 8, y + 8), relative=0, thickness=0)
            y -= 30

        self.top_nav(prev_dest="cover", next_dest="profiles")

    # ============================================================
    # BUILD
    # ============================================================
    def build(self):
        self.page_cover()
        self.page_toc()
        self.page_profiles()
        self.page_ground_rules()

        for week in range(1, 5):
            self.page_shift_scheduler(week)
            self.page_night_log(week)
            self.page_checkin(week)

        self.page_wins()

        for week in range(1, 5):
            self.page_weekly_review(week)

        self.page_handoff()
        self.page_sleep_promise()

        self.draw_footer()
        self.c.save()
        print(f"✅  Created: {os.path.abspath(self.filename)}")
        print(f"   Pages   : {self.page_num}")


if __name__ == "__main__":
    out = "couple_sync_sleep_planner.pdf"
    CouplePlannerPDF(out).build()
