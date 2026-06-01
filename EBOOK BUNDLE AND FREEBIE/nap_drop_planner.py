# nap_drop_planner.py
# The Nap Drop Planner — Premium Fillable PDF
# Covers: 4→3, 3→2, 2→1 nap transitions, week-by-week
# Requires: pip install reportlab

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
import os

# ============================================================
# BRAND / PALETTE  (warm navy + gold + sage — premium nursery)
# ============================================================

PAGE_W, PAGE_H = LETTER
MARGIN = 40

P = {
    "bg":         HexColor("#0C1821"),
    "surface":    HexColor("#162233"),
    "surface2":   HexColor("#1C2D42"),
    "navy":       HexColor("#1A2E4A"),
    "navy_light": HexColor("#243A5E"),
    "gold":       HexColor("#C9A84C"),
    "gold_light": HexColor("#E8C97A"),
    "sage":       HexColor("#7AAF90"),
    "blush":      HexColor("#C98080"),
    "cream":      HexColor("#F0E8D8"),
    "muted":      HexColor("#8FA0B8"),
    "dim":        HexColor("#4A607A"),
    "rule":       HexColor("#2A3F5A"),
    "input_bg":   HexColor("#0D1720"),
    "input_bd":   HexColor("#3A5A7A"),
    "warn":       HexColor("#E07A3A"),
    "white":      white,
    "black":      black,
    "tag_4to3":   HexColor("#5A7FA8"),
    "tag_3to2":   HexColor("#7A9A6A"),
    "tag_2to1":   HexColor("#A07850"),
}

# ============================================================
# CONTENT
# ============================================================

TRANSITIONS = [
    {
        "id":    "4to3",
        "label": "4 → 3 Naps",
        "age":   "6–8 Weeks",
        "color": "tag_4to3",
        "badge": "TRANSITION 1",
        "tagline": "The first major schedule shift. Rhythm begins here.",
        "signs": [
            "Takes 20+ minutes to fall asleep for the 4th nap",
            "Fights or skips the last nap of the day entirely",
            "Awake window feels too short — baby seems alert, not tired",
            "Night sleep is disrupted by over-napping in the day",
            "Bedtime push needed — currently too late or too chaotic",
        ],
        "new_schedule": [
            ("Wake", "6:30–7:00 a.m."),
            ("Nap 1", "~8:00–9:00 a.m.  (90 min awake window)"),
            ("Nap 2", "~11:00 a.m.–12:30 p.m."),
            ("Nap 3 (bridge)", "~2:30–3:30 p.m."),
            ("Bedtime", "7:00–7:30 p.m."),
        ],
        "caution": "The 3rd nap is a bridge nap — keep it short (30–45 min). Its job is to get baby to bedtime without overtiredness, not to be a full sleep.",
        "weeks": 4,
    },
    {
        "id":    "3to2",
        "label": "3 → 2 Naps",
        "age":   "6–8 Months",
        "color": "tag_3to2",
        "badge": "TRANSITION 2",
        "tagline": "The biggest daytime shift. Give it a full month.",
        "signs": [
            "Consistently fights the 3rd nap — takes 30+ min to settle",
            "3rd nap pushes bedtime past 8:30 p.m.",
            "Night wakings increase despite good naps",
            "First two naps stretch longer — baby consolidating naturally",
            "Two full naps leave baby happy and unbothered",
        ],
        "new_schedule": [
            ("Wake", "6:30–7:00 a.m."),
            ("Nap 1", "~9:00–10:30 a.m.  (2–2.5 hr awake window)"),
            ("Nap 2", "~1:00–3:00 p.m.  (2.5 hr awake window)"),
            ("Bedtime", "6:30–7:30 p.m."),
        ],
        "caution": "Early bedtime is not a mistake during 3→2. A 6:30 p.m. bedtime is protective, not too early. It prevents overtiredness from tanking the whole transition.",
        "weeks": 6,
    },
    {
        "id":    "2to1",
        "label": "2 → 1 Nap",
        "age":   "12–18 Months",
        "color": "tag_2to1",
        "badge": "TRANSITION 3",
        "tagline": "The long one. Expect 4–6 weeks of messiness.",
        "signs": [
            "Consistently fights the morning nap or second nap",
            "Takes 45+ min to fall asleep for one of the naps",
            "One nap causes the other to be skipped or very short",
            "Night sleep extends — baby banking more overnight hours",
            "Clearly tired at 11 a.m. but fights the afternoon nap",
        ],
        "new_schedule": [
            ("Wake", "6:30–7:00 a.m."),
            ("Nap (midday)", "~12:00–12:30 p.m. start  (5–6 hr awake window)"),
            ("Nap duration", "1.5–3 hours — let them lead"),
            ("Quiet rest", "If nap is short, offer 20 min quiet rest on floor"),
            ("Bedtime", "6:30–7:30 p.m."),
        ],
        "caution": "Do NOT drop the nap on a bad day. The 2→1 transition takes 4–6 weeks. Expect \"disaster days\" weeks 2 and 3. This is normal. Stay the course.",
        "weeks": 6,
    },
]

WEEK_THEMES = {
    "4to3": [
        ("Drop & Observe", "Pull the 4th nap. Watch for signals. Don't rescue with a car nap."),
        ("Lock in Timing", "Set firm nap start times. Push back if baby woke early."),
        ("Bedtime Calibration", "Adjust bedtime 10–15 min earlier if needed."),
        ("The New Normal", "Routine is taking hold. Log patterns, note wins."),
    ],
    "3to2": [
        ("Pull the 3rd", "Drop the 3rd nap fully. Early bedtime is your safety net."),
        ("Ride the Chaos", "Expect some tough afternoons. This is normal — don't add back."),
        ("Extend Window 1", "Push Nap 1 start 15 min later to lengthen awake windows."),
        ("Extend Window 2", "Push Nap 2 start 15 min later. Watch bedtime stays consistent."),
        ("Mid-Point Check", "Two full naps settling? Log consistency."),
        ("Solidify", "Nap times feel predictable. Fine-tune bedtime."),
    ],
    "2to1": [
        ("Trial Week", "Drop the morning nap or the second. Pick one, stay consistent."),
        ("The Hard Week", "Most families hit a wall. Protect bedtime above all else."),
        ("Push the Nap", "Move midday nap start 15 min later than last week."),
        ("Extend the Nap", "Try to extend nap — blackout, white noise, no early rescues."),
        ("Stabilize", "Watch the nap settling reliably? Night sleep usually improves."),
        ("The New Groove", "Routine is yours now. Log the final schedule that works."),
    ],
}

NAP_SIGNS_READINESS = [
    ("✦ Ready to drop", "Fights this nap 4+ days out of 7"),
    ("✦ Borderline", "Fights this nap 2–3 days out of 7 — watch another week"),
    ("✦ Keep it", "Settles for this nap easily — not time yet"),
    ("✦ Check environment", "Fighting nap but may be environmental, not readiness"),
]

TROUBLESHOOT = [
    ("Early waking", "Usually caused by: too much daytime sleep, first nap too early, or overtiredness. Try capping total nap time and pushing first nap 15 min later."),
    ("Catnapping", "Baby wakes at 30–45 min mark. Practice re-settle: pause, wait, offer a pat — don't immediately feed or remove from crib."),
    ("Short nap throws off schedule", "Use the 'floating nap' rescue: brief 20-min top-up if needed. Don't let it become a habit — 3 days max."),
    ("Bedtime resistance", "Nap is too late, total sleep too high, or stimulation too high pre-bed. Pull bedtime 15–30 min earlier for a week."),
    ("Overtiredness spiral", "Signs: wired but won't sleep, crying hard, won't settle. Push bedtime to 6 p.m. for 2–3 days to reset."),
    ("Regression during transition", "Normal. Transitions rarely land clean. Hold the new schedule even on bad days — reverting resets the clock."),
]

AFFIRM = [
    "Transitions are messy by design. Messy means it's working.",
    "One bad nap day does not undo a week of progress.",
    "Your baby's body is learning a new rhythm. Give it time.",
    "The transition takes as long as it takes. Consistent > Perfect.",
    "You pulled the nap. That was the hard part. Hold the line.",
    "Some days the new schedule works beautifully. Some don't. Keep going.",
    "Sleep science says: 5–7 consistent days before you can judge a change.",
    "The log is your data. The data is your ally.",
    "You're not failing — you're transitioning. There's a difference.",
    "When in doubt: earlier bedtime, consistent schedule, patience.",
]

DAILY_LOG_COLS = ["Nap 1 Start", "Nap 1 End", "Nap 2 Start", "Nap 2 End", "Bedtime", "Night Wakes"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

TOC_ENTRIES = [
    ("How to Use This Planner", "how_to", None),
    ("Baby Profile", "baby_profile", None),
    ("— TRANSITION 1: 4 → 3 Naps —", None, "4to3"),
    ("  Signs It's Time", "4to3_signs", "4to3"),
    ("  New Schedule Guide", "4to3_sched", "4to3"),
    ("  Week-by-Week Planner (Weeks 1–4)", "4to3_w1", "4to3"),
    ("— TRANSITION 2: 3 → 2 Naps —", None, "3to2"),
    ("  Signs It's Time", "3to2_signs", "3to2"),
    ("  New Schedule Guide", "3to2_sched", "3to2"),
    ("  Week-by-Week Planner (Weeks 1–6)", "3to2_w1", "3to2"),
    ("— TRANSITION 3: 2 → 1 Nap —", None, "2to1"),
    ("  Signs It's Time", "2to1_signs", "2to1"),
    ("  New Schedule Guide", "2to1_sched", "2to1"),
    ("  Week-by-Week Planner (Weeks 1–6)", "2to1_w1", "2to1"),
    ("Troubleshooting Guide", "troubleshoot", None),
    ("Quick Reference & Resources", "quickref", None),
]


# ============================================================
# PDF ENGINE
# ============================================================

class NapDropPDF:
    def __init__(self, filename="nap_drop_planner.pdf"):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.c.setTitle("The Nap Drop Planner")
        self.c.setAuthor("Six & Thriving")
        self.c.setSubject("Premium fillable nap transition planner — 4→3, 3→2, 2→1")
        self.c.setCreator("Python + ReportLab")
        self.form = self.c.acroForm
        self.page_num = 0
        self._field_id = 0

    def _uid(self, prefix="fld"):
        self._field_id += 1
        return f"{prefix}_{self._field_id:04d}"

    # ─────────────────────────────────────────────────────────
    # Core page helpers
    # ─────────────────────────────────────────────────────────
    def new_page(self, section_title=None, bookmark=None, bg="bg"):
        if self.page_num > 0:
            self._draw_footer()
            self.c.showPage()
        self.page_num += 1
        self._draw_bg(P[bg])
        if bookmark:
            self.c.bookmarkPage(bookmark)
            if section_title:
                self.c.addOutlineEntry(section_title, bookmark, level=0, closed=False)

    def _draw_bg(self, color):
        self.c.setFillColor(color)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    def _draw_footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.line(MARGIN, 22, PAGE_W - MARGIN, 22)
        self.c.setFont("Helvetica", 7)
        self.c.setFillColor(P["muted"])
        self.c.drawString(MARGIN, 11, "The Nap Drop Planner  ·  Six & Thriving")
        self.c.drawRightString(PAGE_W - MARGIN, 11, str(self.page_num))

    # ─────────────────────────────────────────────────────────
    # Drawing helpers
    # ─────────────────────────────────────────────────────────
    def card(self, x, y, w, h, fill="surface", radius=10, stroke_color=None, stroke_w=0.5):
        self.c.setFillColor(P[fill])
        if stroke_color:
            self.c.setStrokeColor(P[stroke_color])
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
            self.c.setLineWidth(stroke_w)
        else:
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

    def label(self, x, y, text, size=9, color="muted", font="Helvetica-Bold"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawString(x, y, text)

    def text(self, x, y, txt, size=10, color="cream", font="Times-Roman", max_w=None, leading=None):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        ld = leading or (size + 3)
        if not max_w:
            self.c.drawString(x, y, txt)
            return y - ld
        lines = simpleSplit(txt, font, size, max_w)
        yy = y
        for line in lines:
            self.c.drawString(x, yy, line)
            yy -= ld
        return yy

    def ctext(self, cx, y, txt, size=12, color="gold_light", font="Times-Bold"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawCentredString(cx, y, txt)

    def section_header(self, title, subtitle="", tag=None, tag_color="gold"):
        y = PAGE_H - 54
        self.card(MARGIN, y - 54, PAGE_W - 2*MARGIN, 68, fill="navy")
        if tag:
            self.c.setFillColor(P[tag_color])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(MARGIN + 14, y - 10, tag)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 20)
        self.c.drawString(MARGIN + 14, y + 6, title)
        if subtitle:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 10)
            self.c.drawString(MARGIN + 14, y - 24, subtitle)

    def divider(self, y, color="rule"):
        self.c.setStrokeColor(P[color])
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN, y, PAGE_W - MARGIN, y)

    # ─────────────────────────────────────────────────────────
    # Navigation
    # ─────────────────────────────────────────────────────────
    def nav_btn(self, x, y, w, h, text, dest, fill="surface2", txt="gold_light", size=9):
        self.card(x, y, w, h, fill=fill, radius=8)
        self.c.setFillColor(P[txt])
        self.c.setFont("Helvetica-Bold", size)
        tw = stringWidth(text, "Helvetica-Bold", size)
        self.c.drawString(x + (w - tw)/2, y + h/2 - 3, text)
        self.c.linkRect("", dest, (x, y, x+w, y+h), relative=0, thickness=0)

    def top_nav(self, prev=None, nxt=None, home="cover"):
        y = 34
        if prev:
            self.nav_btn(MARGIN, y, 90, 20, "◀  Prev", prev, fill="surface2")
        self.nav_btn(PAGE_W/2 - 40, y, 80, 20, "⌂  Home", home, fill="navy")
        if nxt:
            self.nav_btn(PAGE_W - MARGIN - 90, y, 90, 20, "Next  ▶", nxt, fill="gold", txt="bg")

    # ─────────────────────────────────────────────────────────
    # Form field helpers
    # ─────────────────────────────────────────────────────────
    def tf(self, name, x, y, w, h=22, value="", multiline=False, fsize=10, tip=None):
        self.form.textfield(
            name=name,
            tooltip=tip or name,
            x=x, y=y, width=w, height=h,
            borderStyle="inset",
            borderColor=P["input_bd"],
            fillColor=white,
            textColor=black,
            forceBorder=True,
            value=value,
            fontName="Helvetica",
            fontSize=fsize,
            fieldFlags=("multiline" if multiline else ""),
        )

    def cb(self, name, x, y, size=14, checked=False, tip=None):
        self.form.checkbox(
            name=name, tooltip=tip or name,
            x=x, y=y, size=size,
            checked=checked,
            buttonStyle="check",
            borderColor=P["gold"],
            fillColor=white,
            textColor=P["gold"],
            forceBorder=True,
        )

    def rb(self, group, value, x, y, size=13, selected=False, tip=None):
        self.form.radio(
            name=group, tooltip=tip or group,
            value=value, selected=selected,
            x=x, y=y, size=size,
            buttonStyle="circle",
            borderColor=P["gold"],
            fillColor=white,
            textColor=P["gold"],
            forceBorder=True,
        )

    def labeled_tf(self, x, y, w, lbl, name, h=22, multiline=False, fsize=10):
        self.label(x, y + h + 5, lbl, size=8)
        self.tf(name, x, y, w, h, multiline=multiline, fsize=fsize)

    def pill_badge(self, x, y, text, fill="gold", txt="bg", w=None):
        fw = w or (stringWidth(text, "Helvetica-Bold", 8) + 16)
        self.card(x, y, fw, 16, fill=fill, radius=8)
        self.c.setFillColor(P[txt])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawCentredString(x + fw/2, y + 4, text)

    # ─────────────────────────────────────────────────────────
    # COVER
    # ─────────────────────────────────────────────────────────
    def page_cover(self):
        self.new_page("Cover", "cover")

        # Gradient-like layered background
        for i, (yfrac, col) in enumerate([
            (0.65, HexColor("#0C1821")),
            (0.3,  HexColor("#0F2035")),
            (0.0,  HexColor("#0C1821")),
        ]):
            self.c.setFillColor(col)
            self.c.rect(0, PAGE_H * yfrac, PAGE_W, PAGE_H * (1 - yfrac), fill=1, stroke=0)

        # Decorative arc rings
        self.c.setStrokeColor(HexColor("#C9A84C22"))
        self.c.setLineWidth(1.2)
        for r in [180, 230, 285]:
            self.c.circle(PAGE_W/2, PAGE_H - 120, r, fill=0, stroke=1)

        # Moon icon top centre
        self.c.setFillColor(P["gold"])
        self.c.circle(PAGE_W/2, PAGE_H - 100, 28, fill=1, stroke=0)
        self.c.setFillColor(P["bg"])
        self.c.circle(PAGE_W/2 + 14, PAGE_H - 110, 22, fill=1, stroke=0)

        # Brand tag
        self.pill_badge(PAGE_W/2 - 55, PAGE_H - 190, "SIX & THRIVING  ·  PREMIUM PLANNER", fill="navy_light", txt="gold", w=220)

        # Title block
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 38)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 250, "The Nap Drop")
        self.c.setFillColor(white)
        self.c.setFont("Times-Bold", 38)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 295, "Planner")

        self.c.setFillColor(P["gold"])
        self.c.setLineWidth(1.5)
        self.c.line(PAGE_W/2 - 90, PAGE_H - 310, PAGE_W/2 + 90, PAGE_H - 310)

        self.c.setFillColor(P["muted"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 328, "Navigate every nap transition with confidence.")
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 344, "4→3 · 3→2 · 2→1  Week-by-week, fully logged.")

        # Three transition cards
        cards = [
            ("4 → 3 Naps", "6–8 weeks", "tag_4to3", "4to3_signs"),
            ("3 → 2 Naps", "6–8 months", "tag_3to2", "3to2_signs"),
            ("2 → 1 Nap",  "12–18 months", "tag_2to1", "2to1_signs"),
        ]
        card_w, card_h = 140, 72
        gap = (PAGE_W - 2*MARGIN - 3*card_w) / 2
        cx = MARGIN
        for name, age, col, dest in cards:
            self.card(cx, PAGE_H - 450, card_w, card_h, fill="surface", stroke_color=col)
            self.c.setFillColor(P[col])
            self.c.setFont("Times-Bold", 14)
            self.c.drawCentredString(cx + card_w/2, PAGE_H - 400, name)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 9)
            self.c.drawCentredString(cx + card_w/2, PAGE_H - 418, age)
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawCentredString(cx + card_w/2, PAGE_H - 434, "Tap to start ›")
            self.c.linkRect("", dest, (cx, PAGE_H-450, cx+card_w, PAGE_H-378), relative=0, thickness=0)
            cx += card_w + gap

        # Navigation row
        nav = [
            ("How to Use", "how_to"),
            ("Baby Profile", "baby_profile"),
            ("Troubleshooting", "troubleshoot"),
            ("Quick Ref", "quickref"),
        ]
        btn_w = 110
        bx = MARGIN
        by = 110
        gap2 = (PAGE_W - 2*MARGIN - 4*btn_w) / 3
        for lbl, dest in nav:
            self.nav_btn(bx, by, btn_w, 26, lbl, dest, fill="navy_light", txt="gold_light", size=9)
            bx += btn_w + gap2

        # Footer tagline
        self.c.setFillColor(P["dim"])
        self.c.setFont("Helvetica", 8)
        self.c.drawCentredString(PAGE_W/2, 72, "Nap transitions derail progress. This keeps you on track.")

    # ─────────────────────────────────────────────────────────
    # HOW TO USE
    # ─────────────────────────────────────────────────────────
    def page_how_to(self):
        self.new_page("How to Use This Planner", "how_to")
        self.section_header(
            "How to Use This Planner",
            "Read this once. It'll save you confusion at 2 a.m.",
            tag="GETTING STARTED"
        )

        tips = [
            ("Start at the right transition",
             "Go to the transition that matches your baby's current age and situation. Don't read ahead — each section assumes you're actively in that transition."),
            ("Work week by week",
             "Each transition has a week-by-week planner. Fill in each week's schedule, log daily nap times, and mark signs of progress before moving to the next week."),
            ("Use the Signs It's Time page first",
             "Before starting a transition, review the signs checklist. If fewer than 3 signs are checked, wait. Rushing a transition adds weeks, not saves them."),
            ("Log every day — even bad ones",
             "The daily log is your data. Patterns only show up after 5–7 days. One bad day means nothing; a pattern of bad days means something."),
            ("Troubleshoot before backtracking",
             "If things feel off in week 2 or 3, go to the Troubleshooting Guide before dropping back to the old schedule. Most issues are fixable without reverting."),
            ("Checkboxes are decisions, not decorations",
             "Every checklist item in this planner represents something that has worked across hundreds of babies. When things aren't working, re-check the basics."),
        ]

        y = 600
        for i, (title, body) in enumerate(tips):
            self.card(MARGIN, y - 56, PAGE_W - 2*MARGIN, 68, fill="surface")
            self.pill_badge(MARGIN + 10, y + 2, f"0{i+1}", fill="gold", txt="bg", w=24)
            self.label(MARGIN + 42, y + 4, title, size=11, color="gold_light", font="Times-Bold")
            self.text(MARGIN + 14, y - 18, body, size=9, color="cream", max_w=PAGE_W - 2*MARGIN - 28, leading=13)
            y -= 78

        self.top_nav(prev="cover", nxt="baby_profile")

    # ─────────────────────────────────────────────────────────
    # BABY PROFILE
    # ─────────────────────────────────────────────────────────
    def page_baby_profile(self):
        self.new_page("Baby Profile", "baby_profile")
        self.section_header(
            "Baby Profile",
            "Fill this in once. Reference it throughout.",
            tag="YOUR BABY"
        )

        self.card(MARGIN, 530, PAGE_W - 2*MARGIN, 120, fill="surface")
        self.label(MARGIN + 14, 634, "Baby's Name & Nickname", size=9, color="gold")
        self.labeled_tf(MARGIN + 14, 566, 200, "Full name", "bp_name")
        self.labeled_tf(268, 566, 120, "Nickname", "bp_nick")
        self.labeled_tf(420, 566, 100, "DOB", "bp_dob")

        self.card(MARGIN, 420, PAGE_W - 2*MARGIN, 98, fill="surface2")
        self.label(MARGIN + 14, 504, "Current Sleep Snapshot  (fill in before starting)", size=9, color="gold")
        self.labeled_tf(MARGIN + 14, 454, 110, "Age right now", "bp_age")
        self.labeled_tf(160, 454, 110, "Current # of naps", "bp_naps")
        self.labeled_tf(306, 454, 110, "Avg night sleep (hrs)", "bp_night")
        self.labeled_tf(452, 454, 98, "Current bedtime", "bp_bt")

        self.card(MARGIN, 290, PAGE_W - 2*MARGIN, 110, fill="surface")
        self.label(MARGIN + 14, 386, "Sleep Personality  (circle one)", size=9, color="gold")
        personalities = [
            ("Snacker", "bp_pers"), ("Overthinker", "bp_pers"), ("Sensitive Soul", "bp_pers"),
            ("Night Owl", "bp_pers"), ("Catnapper", "bp_pers"), ("Party Animal", "bp_pers"),
        ]
        px = MARGIN + 14
        py = 352
        for i, (pname, group) in enumerate(personalities):
            if i == 3:
                px = MARGIN + 14
                py = 322
            self.rb(group, pname, px, py, size=11, tip=f"Sleep personality: {pname}")
            self.label(px + 14, py + 1, pname, size=9, color="cream")
            px += 135 if i < 2 else (138 if i == 2 else 135)

        self.card(MARGIN, 170, PAGE_W - 2*MARGIN, 100, fill="surface2")
        self.label(MARGIN + 14, 256, "Which transitions apply to this baby?  (check all)", size=9, color="gold")
        transitions_check = [
            ("4 → 3 Naps  (6–8 weeks)", "bp_t1", MARGIN + 14, 224),
            ("3 → 2 Naps  (6–8 months)", "bp_t2", MARGIN + 14, 200),
            ("2 → 1 Nap  (12–18 months)", "bp_t3", MARGIN + 14, 176),
        ]
        for lbl, name, cx, cy in transitions_check:
            self.cb(name, cx, cy, size=13)
            self.label(cx + 16, cy + 1, lbl, size=10, color="cream")

        self.card(MARGIN, 70, PAGE_W - 2*MARGIN, 80, fill="navy")
        self.label(MARGIN + 14, 134, "Notes / anything important about this baby's sleep so far:", size=9, color="gold")
        self.tf("bp_notes", MARGIN + 14, 78, PAGE_W - 2*MARGIN - 28, 40, multiline=True, fsize=9)

        self.top_nav(prev="how_to", nxt="4to3_signs")

    # ─────────────────────────────────────────────────────────
    # TRANSITION OPENING — Signs & Schedule (shared pattern)
    # ─────────────────────────────────────────────────────────
    def page_transition_signs(self, t):
        tid = t["id"]
        first_week_dest = f"{tid}_w1"
        self.new_page(f"{t['label']} — Signs It's Time", f"{tid}_signs")

        # Colour strip
        self.c.setFillColor(P[t["color"]])
        self.c.rect(0, PAGE_H - 12, PAGE_W, 12, fill=1, stroke=0)

        self.section_header(
            f"{t['label']}  ·  Signs It's Time",
            f"Age range: {t['age']}  ·  {t['tagline']}",
            tag=t["badge"],
            tag_color=t["color"]
        )

        # Readiness status radio
        self.card(MARGIN, 620, PAGE_W - 2*MARGIN, 50, fill="navy")
        self.label(MARGIN + 14, 656, "Overall Readiness Assessment:", size=10, color="gold")
        statuses = ["Ready to transition", "Almost ready — watch 1 more week", "Not ready yet — hold the schedule"]
        rx = MARGIN + 170
        for i, s in enumerate(statuses):
            self.rb(f"{tid}_readiness", s, rx, 628, size=11, tip=s)
            self.label(rx + 14, 630, s, size=8, color="cream")
            rx += 145

        # Signs checklist
        self.card(MARGIN, 390, PAGE_W - 2*MARGIN, 214, fill="surface")
        self.label(MARGIN + 14, 590, "Check the signs you are seeing consistently (4+ days/week):", size=9, color="gold")
        sy = 564
        for i, sign in enumerate(t["signs"]):
            self.cb(f"{tid}_sign_{i}", MARGIN + 14, sy - 2, size=13, tip=sign)
            self.text(MARGIN + 32, sy, sign, size=10, color="cream", max_w=470)
            sy -= 34

        # Score interpretation
        self.label(MARGIN + 14, 408, "3–4 checked = ready.  1–2 checked = watch another week.  0 checked = not yet.", size=8, color="muted")

        # Notes
        self.card(MARGIN, 250, PAGE_W - 2*MARGIN, 120, fill="surface2")
        self.label(MARGIN + 14, 356, "Observation Notes  (what are you seeing day-to-day?):", size=9, color="gold")
        self.tf(f"{tid}_obs_notes", MARGIN + 14, 258, PAGE_W - 2*MARGIN - 28, 84, multiline=True, fsize=9)

        # Date logged
        self.card(MARGIN, 150, PAGE_W - 2*MARGIN, 80, fill="navy")
        self.labeled_tf(MARGIN + 14, 162, 130, "Date assessed", f"{tid}_assess_date")
        self.labeled_tf(180, 162, 130, "Baby's current age", f"{tid}_assess_age")
        self.labeled_tf(346, 162, 200, "Decision  (transition now / wait / not yet)", f"{tid}_decision", h=22)

        # Determine previous destination
        prev_map = {"4to3": "baby_profile", "3to2": "4to3_reflect_4", "2to1": "3to2_reflect_6"}
        self.top_nav(prev=prev_map[tid], nxt=f"{tid}_sched")

    def page_transition_schedule(self, t):
        tid = t["id"]
        self.new_page(f"{t['label']} — New Schedule", f"{tid}_sched")

        self.c.setFillColor(P[t["color"]])
        self.c.rect(0, PAGE_H - 12, PAGE_W, 12, fill=1, stroke=0)

        self.section_header(
            f"{t['label']}  ·  New Schedule Guide",
            "This is your target. It doesn't have to happen perfectly on day 1.",
            tag=t["badge"],
            tag_color=t["color"]
        )

        # Schedule table
        self.card(MARGIN, 490, PAGE_W - 2*MARGIN, 180, fill="surface")
        self.label(MARGIN + 14, 658, "Target Schedule", size=11, color="gold")

        # Header bar
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 6, 640, PAGE_W - 2*MARGIN - 12, 18, 4, fill=1, stroke=0)
        self.label(MARGIN + 18, 644, "Time Anchor", size=9, color="gold")
        self.label(280, 644, "Target Time  (edit to your baby's rhythm)", size=9, color="gold")

        sy = 618
        for i, (slot, time_hint) in enumerate(t["new_schedule"]):
            fill_key = "surface2" if i % 2 == 0 else "surface"
            self.card(MARGIN + 6, sy - 8, PAGE_W - 2*MARGIN - 12, 28, fill=fill_key, radius=4)
            self.label(MARGIN + 18, sy + 4, slot, size=10, color="cream")
            self.label(160, sy + 4, time_hint, size=9, color="muted")
            # Editable field
            self.tf(f"{tid}_sched_{i}", 390, sy - 4, 150, 20, value="", fsize=9,
                    tip=f"Your baby's actual {slot} time")
            sy -= 30

        # Caution card
        self.card(MARGIN, 360, PAGE_W - 2*MARGIN, 106, fill="navy", stroke_color="warn")
        self.c.setFillColor(P["warn"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(MARGIN + 14, 450, "⚠  KEY NOTE")
        self.text(MARGIN + 14, 430, t["caution"], size=9.5, color="cream", max_w=490, leading=14)

        # Adjust Plan (my version)
        self.card(MARGIN, 200, PAGE_W - 2*MARGIN, 140, fill="surface2")
        self.label(MARGIN + 14, 326, "My Adjusted Plan  (personalise this schedule for our home):", size=9, color="gold")
        self.tf(f"{tid}_my_plan", MARGIN + 14, 208, PAGE_W - 2*MARGIN - 28, 106, multiline=True, fsize=9)

        # Start date
        self.card(MARGIN, 110, PAGE_W - 2*MARGIN, 72, fill="navy")
        self.labeled_tf(MARGIN + 14, 120, 140, "Planned transition start date", f"{tid}_start_date")
        self.labeled_tf(190, 120, 140, "Baby's age at start", f"{tid}_start_age")
        self.labeled_tf(366, 120, 150, "Support person / partner aware?", f"{tid}_partner")

        self.top_nav(prev=f"{tid}_signs", nxt=f"{tid}_w1")

    # ─────────────────────────────────────────────────────────
    # WEEKLY PLANNER (shared)
    # ─────────────────────────────────────────────────────────
    def page_week_planner(self, t, week_num):
        tid = t["id"]
        themes = WEEK_THEMES[tid]
        theme_title, theme_desc = themes[week_num - 1] if week_num - 1 < len(themes) else (f"Week {week_num}", "Stay consistent.")
        total_weeks = t["weeks"]
        bm = f"{tid}_w{week_num}"

        self.new_page(f"{t['label']} Week {week_num}", bm)

        # Colour strip + badge
        self.c.setFillColor(P[t["color"]])
        self.c.rect(0, PAGE_H - 10, PAGE_W, 10, fill=1, stroke=0)

        self.section_header(
            f"{t['label']}  ·  Week {week_num}  —  {theme_title}",
            theme_desc,
            tag=f"WEEK {week_num} OF {total_weeks}",
            tag_color=t["color"]
        )

        # ── This week's schedule targets ──
        self.card(MARGIN, 580, PAGE_W - 2*MARGIN, 78, fill="surface")
        self.label(MARGIN + 14, 644, "This Week's Schedule Targets  (copy from schedule page or adjust here):", size=9, color="gold")
        fields = [("Wake time", f"{bm}_wake"), ("Nap 1 start", f"{bm}_n1start"),
                  ("Nap 2 start", f"{bm}_n2start"), ("Bedtime target", f"{bm}_bt")]
        fx = MARGIN + 14
        for lbl, fname in fields:
            self.labeled_tf(fx, 588, 108, lbl, fname, h=20, fsize=9)
            fx += 122

        # ── Daily log table ──
        self.card(MARGIN, 310, PAGE_W - 2*MARGIN, 252, fill="surface2")
        self.label(MARGIN + 14, 548, "Daily Nap Log", size=11, color="gold")

        # Column headers
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 6, 530, PAGE_W - 2*MARGIN - 12, 18, 4, fill=1, stroke=0)

        col_xs = [MARGIN + 14, 108, 173, 238, 303, 376, 455]
        col_heads = ["Day", "Nap 1\nStart", "Nap 1\nEnd", "Nap 2\nStart", "Nap 2\nEnd", "Bedtime", "Night\nWakes"]
        for cx, ch in zip(col_xs, col_heads):
            h_lbl = ch.replace("\n", " ")
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 7)
            self.c.drawString(cx, 535, h_lbl)

        dy = 510
        for di, day in enumerate(DAYS):
            row_fill = "surface" if di % 2 == 0 else "surface2"
            self.card(MARGIN + 6, dy - 8, PAGE_W - 2*MARGIN - 12, 22, fill=row_fill, radius=3)
            self.label(col_xs[0], dy + 4, day[:3], size=8, color="muted")
            col_widths = [58, 58, 58, 58, 66, 66]
            for ci, (cx, cw) in enumerate(zip(col_xs[1:], col_widths)):
                fn = f"{bm}_d{di+1}_c{ci+1}"
                self.tf(fn, cx, dy - 6, cw, 18, fsize=8, tip=f"{day} — {col_heads[ci+1].replace(chr(10),' ')}")
            dy -= 26

        # ── Focus checklist ──
        self.card(MARGIN, 170, PAGE_W - 2*MARGIN, 122, fill="surface")
        self.label(MARGIN + 14, 278, f"Week {week_num} Focus Checklist  (mark each day you nailed it):", size=9, color="gold")
        checks = [
            (f"Nap 1 started within 15 min of target", f"{bm}_chk_n1"),
            (f"Nap 2 started within 15 min of target", f"{bm}_chk_n2"),
            (f"No rescue nap added (no car nap / contact nap bail-out)", f"{bm}_chk_no_rescue"),
            (f"Bedtime hit the target window", f"{bm}_chk_bt"),
        ]
        cy2 = 254
        for lbl, name in checks:
            self.cb(name, MARGIN + 14, cy2 - 2, size=12, tip=lbl)
            self.label(MARGIN + 30, cy2, lbl, size=9, color="cream")
            cy2 -= 22

        # ── Affirmation ──
        affirm_idx = (week_num - 1) % len(AFFIRM)
        self.card(MARGIN, 74, PAGE_W - 2*MARGIN, 74, fill="navy")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 10)
        self.c.drawCentredString(PAGE_W/2, 120, f'"{AFFIRM[affirm_idx]}"')
        self.c.setFillColor(P["dim"])
        self.c.setFont("Helvetica", 7)
        self.c.drawCentredString(PAGE_W/2, 100, "— Six & Thriving")

        # Navigation
        if week_num == 1:
            prev_dest = f"{tid}_sched"
        else:
            prev_dest = f"{tid}_reflect_{week_num - 1}"
        if week_num < total_weeks:
            nxt_dest = f"{tid}_reflect_{week_num}"
        else:
            nxt_dest = f"{tid}_reflect_{week_num}"

        self.top_nav(prev=prev_dest, nxt=nxt_dest)

    # ─────────────────────────────────────────────────────────
    # WEEKLY REFLECTION
    # ─────────────────────────────────────────────────────────
    def page_week_reflect(self, t, week_num):
        tid = t["id"]
        total_weeks = t["weeks"]
        bm = f"{tid}_reflect_{week_num}"

        self.new_page(f"{t['label']} Week {week_num} Reflection", bm)

        self.c.setFillColor(P[t["color"]])
        self.c.rect(0, PAGE_H - 10, PAGE_W, 10, fill=1, stroke=0)

        self.section_header(
            f"{t['label']}  ·  Week {week_num} Reflection",
            "Fill this out at the end of the week — before starting the next.",
            tag=f"WEEK {week_num} REVIEW",
            tag_color=t["color"]
        )

        # Stats row
        self.card(MARGIN, 568, PAGE_W - 2*MARGIN, 84, fill="surface")
        self.label(MARGIN + 14, 638, "Week at a Glance", size=11, color="gold")
        stats = [
            ("Best nap day", f"{bm}_best_day"),
            ("Hardest day", f"{bm}_hard_day"),
            ("Avg nap 1 length", f"{bm}_avg_n1"),
            ("Avg nap 2 length", f"{bm}_avg_n2"),
        ]
        sx = MARGIN + 14
        for lbl, name in stats:
            self.labeled_tf(sx, 576, 118, lbl, name, h=20, fsize=8)
            sx += 130

        # Reflection questions
        questions = [
            ("What went well?", "Even one small win counts — write it down.", f"{bm}_q1"),
            ("What was the hardest part?", "Name it specifically. Vague problems stay stuck.", f"{bm}_q2"),
            ("Patterns in the nap log?", "Repeated short naps? Consistent fighting? Specific days?", f"{bm}_q3"),
            ("One adjustment for next week:", "One thing only. Small + specific.", f"{bm}_q4"),
        ]
        qy = 548
        for qtitle, qhint, qname in questions:
            self.card(MARGIN, qy - 74, PAGE_W - 2*MARGIN, 84, fill="surface2")
            self.c.setFillColor(P["navy"])
            self.c.roundRect(MARGIN + 6, qy, PAGE_W - 2*MARGIN - 12, 18, 4, fill=1, stroke=0)
            self.label(MARGIN + 18, qy + 4, qtitle, size=10, color="gold_light", font="Times-Bold")
            self.label(MARGIN + 18, qy - 14, qhint, size=8, color="muted")
            self.tf(qname, MARGIN + 14, qy - 64, PAGE_W - 2*MARGIN - 28, 38, multiline=True, fsize=9)
            qy -= 90

        # Transition progress indicator
        self.card(MARGIN, 118, PAGE_W - 2*MARGIN, 56, fill="navy")
        self.label(MARGIN + 14, 160, "Transition Progress", size=9, color="gold")
        progress_options = ["Settling well — on track", "Still adjusting — hold this week's schedule", "Struggling — see troubleshooting guide"]
        px = MARGIN + 14
        for po in progress_options:
            self.rb(f"{bm}_progress", po, px, 126, size=11, tip=po)
            self.label(px + 14, 128, po, size=8, color="cream")
            px += 175

        # Next / prev
        nxt_dest = f"{tid}_w{week_num + 1}" if week_num < total_weeks else self._next_after_transition(tid)
        self.top_nav(prev=f"{tid}_w{week_num}", nxt=nxt_dest)

    def _next_after_transition(self, tid):
        mapping = {"4to3": "3to2_signs", "3to2": "2to1_signs", "2to1": "troubleshoot"}
        return mapping[tid]

    # ─────────────────────────────────────────────────────────
    # TROUBLESHOOTING
    # ─────────────────────────────────────────────────────────
    def page_troubleshoot(self):
        self.new_page("Troubleshooting Guide", "troubleshoot")
        self.section_header(
            "Troubleshooting Guide",
            "Something's off? Start here before reverting to the old schedule.",
            tag="PROBLEM SOLVER"
        )

        y = 628
        for i, (problem, fix) in enumerate(TROUBLESHOOT):
            fill = "surface" if i % 2 == 0 else "surface2"
            self.card(MARGIN, y - 68, PAGE_W - 2*MARGIN, 80, fill=fill)
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(MARGIN + 14, y + 4, f"⚑  {problem}")
            self.text(MARGIN + 14, y - 16, fix, size=9.5, color="cream", max_w=490, leading=13)
            y -= 90

        self.top_nav(prev="2to1_reflect_6", nxt="quickref")

    # ─────────────────────────────────────────────────────────
    # QUICK REFERENCE
    # ─────────────────────────────────────────────────────────
    def page_quickref(self):
        self.new_page("Quick Reference", "quickref")
        self.section_header(
            "Quick Reference  ·  Nap Readiness by Age",
            "Use this as a sanity check throughout all three transitions.",
            tag="REFERENCE"
        )

        ref_data = [
            ("6–8 weeks",    "3",   "45–75 min",   "4→3 transition zone"),
            ("3–4 months",   "3",   "75–90 min",   "Bridge nap still needed"),
            ("5–6 months",   "3",   "90 min",      "3 firm naps for most"),
            ("6–8 months",   "2–3", "2–2.5 hrs",   "3→2 transition zone"),
            ("8–12 months",  "2",   "2.5–3.5 hrs", "2 naps solidly"),
            ("12–15 months", "1–2", "4–5 hrs",     "2→1 transition zone"),
            ("15–24 months", "1",   "5–6 hrs",     "1 nap, midday"),
            ("2–3 years",    "1",   "6 hrs+",      "Nap may drop ~3 yrs"),
        ]

        self.card(MARGIN, 360, PAGE_W - 2*MARGIN, 270, fill="surface")
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN + 6, 608, PAGE_W - 2*MARGIN - 12, 20, 4, fill=1, stroke=0)
        hcols = [("Age", MARGIN + 16), ("# Naps", 165), ("Awake Window", 248), ("Notes", 360)]
        for h, hx in hcols:
            self.label(hx, 612, h, size=9, color="gold")

        ry = 586
        for age, naps, aw, note in ref_data:
            fill = "surface2" if int(ry) % 2 == 0 else "surface"
            self.card(MARGIN + 6, ry - 6, PAGE_W - 2*MARGIN - 12, 22, fill=fill, radius=3)
            self.label(MARGIN + 16, ry + 6, age, size=9, color="gold_light")
            self.label(165, ry + 6, naps, size=9)
            self.label(248, ry + 6, aw, size=9)
            self.label(360, ry + 6, note, size=8, color="muted")
            ry -= 28

        # Personal notes section
        self.card(MARGIN, 180, PAGE_W - 2*MARGIN, 158, fill="surface2")
        self.label(MARGIN + 14, 324, "My Personal Notes & Reminders:", size=10, color="gold")
        self.tf("qr_notes", MARGIN + 14, 188, PAGE_W - 2*MARGIN - 28, 122, multiline=True, fsize=10)

        # Navigation home
        self.card(MARGIN, 110, PAGE_W - 2*MARGIN, 46, fill="navy")
        self.nav_btn(PAGE_W/2 - 80, 120, 160, 26, "⌂  Return to Cover", "cover", fill="gold", txt="bg")

        self.top_nav(prev="troubleshoot", nxt="cover")

    # ─────────────────────────────────────────────────────────
    # TABLE OF CONTENTS
    # ─────────────────────────────────────────────────────────
    def page_toc(self):
        self.new_page("Table of Contents", "toc")
        self.section_header(
            "Contents",
            "Jump directly to any section. All links are active.",
            tag="NAVIGATION"
        )

        y = 616
        for entry, dest, tid in TOC_ENTRIES:
            is_section_head = dest is None
            if is_section_head:
                self.c.setFillColor(P[TRANSITIONS[[t["id"] for t in TRANSITIONS].index(tid)]["color"]] if tid else P["gold"])
                self.c.setFont("Helvetica-Bold", 9)
                self.c.drawString(MARGIN + 14, y, entry)
                y -= 20
                continue

            fill = "navy" if y % 40 < 20 else "surface"
            self.card(MARGIN, y - 8, PAGE_W - 2*MARGIN, 22, fill="surface", radius=4)
            self.label(MARGIN + 28, y + 4, entry, size=9, color="cream")

            # Dotted leader + page link indicator
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawRightString(PAGE_W - MARGIN - 12, y + 4, "›")
            self.c.linkRect("", dest, (MARGIN, y - 8, PAGE_W - MARGIN, y + 14), relative=0, thickness=0)
            y -= 26

        self.top_nav(nxt="how_to", home="cover")

    # ─────────────────────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────────────────────
    def build(self):
        self.page_cover()
        self.page_toc()
        self.page_how_to()
        self.page_baby_profile()

        for t in TRANSITIONS:
            self.page_transition_signs(t)
            self.page_transition_schedule(t)
            for w in range(1, t["weeks"] + 1):
                self.page_week_planner(t, w)
                self.page_week_reflect(t, w)

        self.page_troubleshoot()
        self.page_quickref()

        self._draw_footer()
        self.c.save()
        print(f"\n✓  Created: {os.path.abspath(self.filename)}")
        print(f"   Pages: {self.page_num}")


# ── entry point ──────────────────────────────────────────────
if __name__ == "__main__":
    out = "nap_drop_planner.pdf"
    NapDropPDF(out).build()
