# sleep_environment_planner.py
# The Perfect Sleep Environment Checklist Planner
# "Get the room right once. Then it works every night."
# Premium fillable PDF — Six & Thriving
# Requires: pip install reportlab

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
import os

# ============================================================
# BRAND / PALETTE  — warm nursery meets premium editorial
# ============================================================

PAGE_W, PAGE_H = LETTER
MARGIN = 40

P = {
    "bg":           HexColor("#0C1A20"),
    "surface":      HexColor("#152430"),
    "surface2":     HexColor("#1C2E3C"),
    "surface3":     HexColor("#223344"),
    "navy":         HexColor("#1A3245"),
    "navy_light":   HexColor("#224460"),
    "gold":         HexColor("#C9A84C"),
    "gold_light":   HexColor("#E8C97A"),
    "gold_dim":     HexColor("#9E7A30"),
    "sage":         HexColor("#6BA68C"),        # safe/green
    "amber":        HexColor("#D4894A"),        # warmth/caution accent
    "blush":        HexColor("#C97A7A"),        # danger/red accent
    "sky":          HexColor("#5C9FBF"),        # light/blue accent
    "cream":        HexColor("#F0E8D8"),
    "muted":        HexColor("#8FA0B8"),
    "dim":          HexColor("#4A607A"),
    "rule":         HexColor("#2A3F5A"),
    "white":        white,
    "black":        black,
}

# ============================================================
# CONTENT
# ============================================================

# ---- ONE-TIME SETUP ITEMS (room-by-room) ----

SETUP_DARKNESS = [
    ("True blackout curtains or blinds installed",
     "Not 'room-darkening' — hold a phone torch behind the fabric. Zero light through = pass.",
     "critical"),
    ("All monitor/device LEDs covered with electrical tape",
     "Even a single dim indicator light can suppress melatonin. Tape every LED.",
     "critical"),
    ("Door gap light sealed (draft stopper or blackout panel)",
     "Hallway light under the door counts. Use a door-bottom draft seal.",
     "high"),
    ("Nightlight removed OR replaced with red-spectrum only",
     "White/blue nightlights disrupt melatonin. Red-spectrum: acceptable if needed.",
     "high"),
    ("Window frame light leaks identified and sealed",
     "Use blackout tape or foam strips on frame gaps. Check at midday.",
     "medium"),
]

SETUP_WHITE_NOISE = [
    ("White noise machine purchased and positioned",
     "Place 3–6 feet from crib, never inside or right against it.",
     "critical"),
    ("Volume calibrated to 60–65 dB at crib head level",
     "Use a free dB meter app. Similar to shower noise. Not a whisper, not a jet engine.",
     "critical"),
    ("Sound type selected and set to run all night",
     "White/brown/pink noise or rain. Consistent is better than varied.",
     "high"),
    ("Extension cord / power supply confirmed stable",
     "Machine must not cut out mid-night. Test for 48 hours before relying on it.",
     "medium"),
    ("Machine not placed inside the crib or against the crib rail",
     "Distance protects hearing. A few feet away is ideal.",
     "critical"),
]

SETUP_TEMPERATURE = [
    ("Room thermometer installed at crib level",
     "Not a wall thermostat — measure where baby actually sleeps.",
     "critical"),
    ("Room confirmed 68–72°F / 20–22°C at crib height",
     "Too warm = more rousing. Too cold = disrupted sleep. Goldilocks zone is critical.",
     "critical"),
    ("Central heating/cooling set to maintain target overnight",
     "Set it and test for 2 nights. Note if it overshoots in early morning.",
     "high"),
    ("Sleep sack tog rating matched to room temperature",
     "0.5 tog: 24°C+. 1.0 tog: 20–23°C. 2.5 tog: 16–20°C. 3.5 tog: below 16°C.",
     "high"),
    ("Baby's chest warm but not sweaty — test regularly",
     "Check the chest/back of neck, not hands or feet (always cooler on babies).",
     "high"),
    ("No direct heating/cooling vent blowing on crib",
     "Drafts and direct airflow disrupt sleep and create uneven temperature.",
     "medium"),
]

SETUP_CRIB = [
    ("Firm, flat mattress — no incline, wedge, or pillow-top",
     "AAP guideline. A firm surface that does not indent under baby's weight.",
     "critical"),
    ("Fitted sheet only on mattress — nothing else",
     "No loose blankets, bumpers, pillows, positioners, or stuffed animals.",
     "critical"),
    ("Mattress fits snugly — no gaps between mattress and crib sides",
     "Gaps larger than 2 fingers are a safety concern. Replace mattress if needed.",
     "critical"),
    ("Baby placed on back — every sleep, every time, without exception",
     "Back-sleeping until baby can roll both ways independently.",
     "critical"),
    ("Sleep sack used instead of blanket",
     "Choose size and tog for current weight and room temperature.",
     "critical"),
    ("No stuffed animals, positioners, or wedges in sleep space",
     "Safe from birth. Comfort object (lovey) appropriate from 12 months.",
     "critical"),
    ("Crib slat spacing confirmed safe (under 2.375 inches / 6 cm)",
     "Older cribs may not meet current standards. Verify if using second-hand crib.",
     "high"),
    ("Crib positioned away from windows, cords, and curtains",
     "Strangulation and temperature risk. Minimum 3 feet from all window coverings.",
     "high"),
    ("All window blind/curtain cords looped up and out of reach",
     "Cord strangulation is a leading cause of accidental death. Cordless blinds preferred.",
     "critical"),
    ("Crib hardware checked and all bolts confirmed tight",
     "Check monthly. Rattling hardware can startle baby during light sleep.",
     "medium"),
]

SETUP_MONITOR = [
    ("Baby monitor positioned correctly — not inside crib",
     "Monitor should view the whole crib. Minimum 3 feet from baby.",
     "critical"),
    ("Monitor screen brightness set to lowest possible",
     "If monitor screen is in your bedroom, face it away or cover when not checking.",
     "high"),
    ("Monitor alert volume tested — audible from parent bedroom",
     "Test at actual distance with door closed. Ensure it can wake a sleeping adult.",
     "high"),
    ("WiFi/Bluetooth monitor security reviewed",
     "Change default passwords. Enable two-factor if available.",
     "medium"),
]

SETUP_ROOM_SHARING = [
    ("Visual partition between baby sleep space and parent area",
     "A curtain, room divider, or crib placement that creates visual separation.",
     "high"),
    ("Parent phone and device screens dimmed for night feeds",
     "Keep phone brightness to minimum. No scrolling bright screens during feeds.",
     "high"),
    ("Bedside lamp on red-spectrum or dimmest warm setting",
     "Or use a small red-spectrum clip light for feeding only.",
     "high"),
    ("Bedsharing NOT occurring as default — crib/bassinet used",
     "AAP: room-sharing yes, bed-sharing no. If bedsharing intentionally, follow safe bedsharing guidelines.",
     "critical"),
]

SETUP_GENERAL_ENV = [
    ("Nursery door hardware confirmed silent (no squeaking)",
     "Oil hinges. Replace squeaking hardware. A noisy exit wakes babies.",
     "medium"),
    ("Rocking chair / glider stable and not squeaking",
     "Test before use. Squeaks during feeds can create light-sleep arousal.",
     "medium"),
    ("Phone on silent (not vibrate) during baby's sleep hours",
     "Vibrate on a hard surface is audible. Full silent during naps and bedtime.",
     "medium"),
    ("Household noise pattern understood and managed",
     "Sibling play, TV, kitchen — white noise masks most. Plan for peak noise periods.",
     "medium"),
    ("Nightlight location confirmed (or confirmed absent)",
     "If using, place near door not near crib. Red spectrum only.",
     "high"),
]

# Priority colors
PRIORITY_COLORS = {
    "critical": "blush",
    "high":     "amber",
    "medium":   "sage",
}
PRIORITY_LABELS = {
    "critical": "CRITICAL",
    "high":     "IMPORTANT",
    "medium":   "RECOMMENDED",
}

# ---- NIGHTLY CONDITION LOG ----
NIGHTLY_CONDITIONS = [
    ("Room Temp (°F/°C)",   "temp"),
    ("Blackout confirmed",  "dark"),
    ("White noise ON",      "wn"),
    ("Sleep sack tog",      "tog"),
    ("Crib clear",          "crib"),
    ("All LEDs covered",    "leds"),
]

# ---- SCIENCE REFERENCE ----
SCIENCE_CARDS = [
    ("Darkness & Melatonin",
     "sky",
     "Melatonin production begins when the retina detects darkness. Even 10 lux — a dim nightlight — can suppress melatonin by up to 50% in infants. True blackout means zero detectable light. If you can see your hand, it is too bright."),
    ("White Noise Science",
     "sage",
     "The womb measures 80–85 dB — similar to a vacuum cleaner. A silent nursery is jarring to a newborn's nervous system. White noise at 60–65 dB masks startling household sounds and recreates the familiar womb environment. Never exceed 65 dB at crib level."),
    ("Temperature & Sleep Architecture",
     "amber",
     "Core body temperature must drop 1–2°F to initiate sleep. Rooms above 72°F / 22°C prevent this drop and cause more frequent arousal. Too cold (below 65°F / 18°C) causes the same effect. 68–72°F is the evidence-based sweet spot."),
    ("Tog Ratings Explained",
     "gold",
     "Tog measures thermal insulation. 0.5 tog: 24°C+ rooms. 1.0 tog: 20–23°C. 2.5 tog: 16–20°C. 3.5 tog: below 16°C. Overdressing is a greater risk than underdressing. When in doubt, go lower tog and layer underneath."),
    ("The LED Problem",
     "blush",
     "Monitor screens, power indicator LEDs, smoke detector lights, charging cables — all emit light. Research shows blue/white light exposure at night shifts the circadian clock and disrupts infant sleep. Cover every LED with electrical tape before the first night."),
    ("Room-Sharing vs Bed-Sharing",
     "muted",
     "The AAP recommends room-sharing for 6–12 months — it reduces SIDS risk by up to 50%. Bed-sharing is a separate and higher-risk practice. Room-sharing means the baby sleeps in their own safe sleep surface within arm's reach, not in the parent's bed."),
]

# ---- TEMPERATURE / LIGHT LOG (30-night tracker) ----
MONTHS = ["Week 1", "Week 2", "Week 3", "Week 4"]

# ---- TOG QUICK REFERENCE ----
TOG_GUIDE = [
    ("Below 16°C / 61°F", "3.5 tog", "Long-sleeve bodysuit + 3.5 tog sleep sack"),
    ("16–20°C / 61–68°F", "2.5 tog", "Long-sleeve bodysuit + 2.5 tog sleep sack"),
    ("20–23°C / 68–73°F", "1.0 tog", "Short-sleeve bodysuit + 1.0 tog sleep sack"),
    ("24°C+ / 75°F+",     "0.5 tog", "Nappy/short-sleeve only + 0.5 tog sleep sack"),
]

# ---- QUICK WIN CHECKLIST (tonight) ----
QUICK_WINS = [
    "Walk into the nursery right now — can you see anything with lights off?",
    "Is the white noise on and audible at crib level?",
    "Check the room thermometer — is it in the 68–72°F / 20–22°C range?",
    "Cover every LED in the room with electrical tape right now.",
    "Check the sleep sack tog rating against the room temperature.",
    "Confirm the crib has nothing in it except baby + fitted sheet + sleep sack.",
    "Check the monitor is not inside or against the crib.",
    "Look at the door gap — is light coming under it from the hallway?",
]

# ---- TROUBLESHOOTING ----
TROUBLESHOOT = [
    ("Baby wakes 45 min into every nap",
     "Classic sleep cycle transition. Ensure darkness and white noise are optimal for naps too. "
     "Check if any light enters at midday (sun angle changes). Be in the room at the 40-min mark "
     "to attempt resettling before full waking."),
    ("Baby wakes with every household sound",
     "White noise volume may be too low, or machine may be too far from crib. "
     "Increase volume slightly (max 65 dB at crib head). Ensure it runs continuously — "
     "some machines auto-off after 30–60 min."),
    ("Baby is sweaty but room is within target temperature",
     "Sleep sack tog is too high. Drop one tog level. Check if central heating is spiking "
     "in early morning. A chest that is warm but not sweaty is the target."),
    ("Baby seems cold despite appropriate tog",
     "Add a short-sleeve onesie under the sleep sack before increasing tog. "
     "Check for drafts from vents, windows, or fans blowing directly on crib."),
    ("Early morning waking (4–5am)",
     "Most common cause: light entering room at sunrise. Check east-facing windows especially. "
     "Add blackout tape to any frame gaps. A second layer of blackout curtain often solves this."),
    ("Baby startles awake when parent enters or exits",
     "Door hinges need oiling. Practice the exit sequence in daylight. "
     "Ensure white noise is running before entry. Move slowly and without sudden movements."),
    ("Room temperature varies significantly overnight",
     "Thermostat may be on a schedule. Set to 'hold' at 20°C/68°F overnight. "
     "Consider a secondary programmable plug-in heater/cooler for the nursery only."),
]

# ============================================================
# PDF ENGINE
# ============================================================

class EnvironmentPlannerPDF:
    def __init__(self, filename="sleep_environment_planner.pdf"):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.c.setTitle("The Perfect Sleep Environment Checklist Planner")
        self.c.setAuthor("Six & Thriving")
        self.c.setSubject("Premium nursery setup and nightly condition tracker")
        self.c.setCreator("Python + ReportLab")
        self.form = self.c.acroForm
        self.page_num = 0

    # --------------------------------------------------------
    # Core helpers
    # --------------------------------------------------------
    def new_page(self, title=None, bookmark=None, bg="bg"):
        if self.page_num > 0:
            self._footer()
            self.c.showPage()
        self.page_num += 1
        self.c.setFillColor(P[bg])
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if bookmark:
            self.c.bookmarkPage(bookmark)
            if title:
                self.c.addOutlineEntry(title, bookmark, level=0, closed=False)

    def _footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.line(MARGIN, 24, PAGE_W - MARGIN, 24)
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(P["muted"])
        self.c.drawString(MARGIN, 12, "Perfect Sleep Environment Planner  |  Six & Thriving")
        self.c.drawRightString(PAGE_W - MARGIN, 12, str(self.page_num))

    def section_header(self, title, subtitle="", tag=None, tag_color="amber"):
        y = PAGE_H - 54
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN, y - 52, PAGE_W - 2*MARGIN, 64, 12, fill=1, stroke=0)
        if tag:
            self.c.setFillColor(P[tag_color])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 16, y - 8, tag)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 22)
        self.c.drawString(MARGIN + 16, y + 8, title)
        if subtitle:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 11)
            self.c.drawString(MARGIN + 16, y - 14, subtitle)

    def card(self, x, y, w, h, fill="surface", radius=10):
        self.c.setFillColor(P[fill])
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
        for ln in lines:
            self.c.drawString(x, yy, ln)
            yy -= ld
        return yy

    def bullets(self, x, y, items, width, bc="gold", tc="cream", size=9):
        yy = y
        for item in items:
            self.c.setFillColor(P[bc])
            self.c.setFont("Helvetica-Bold", size + 1)
            self.c.drawString(x, yy, "•")
            yy = self.text(x + 14, yy, item, size=size, color=tc, max_w=width - 14)
            yy -= 3
        return yy

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------
    def link_btn(self, x, y, w, h, lbl, dest, fill="surface2", txt="gold_light", size=9):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 10, fill=1, stroke=0)
        self.c.setFillColor(P[txt])
        self.c.setFont("Helvetica-Bold", size)
        tw = stringWidth(lbl, "Helvetica-Bold", size)
        self.c.drawString(x + (w - tw)/2, y + h/2 - 3, lbl)
        self.c.linkRect("", dest, (x, y, x + w, y + h), relative=0, thickness=0)

    def nav(self, prev=None, nxt=None, home="cover"):
        y = 32
        if prev:
            self.link_btn(MARGIN, y, 96, 18, "< Previous", prev, fill="surface2")
        self.link_btn(PAGE_W/2 - 45, y, 90, 18, "Home", home, fill="navy")
        if nxt:
            self.link_btn(PAGE_W - MARGIN - 96, y, 96, 18, "Next >", nxt, fill="gold", txt="bg")

    # --------------------------------------------------------
    # Form helpers
    # --------------------------------------------------------
    def tf(self, name, x, y, w, h=20, multiline=False, fs=10, value="", tooltip=None):
        self.form.textfield(
            name=name, tooltip=tooltip or name,
            x=x, y=y, width=w, height=h,
            borderStyle='inset',
            borderColor=P["gold"],
            fillColor=P["white"],
            textColor=P["black"],
            forceBorder=True, value=value,
            fontName="Helvetica", fontSize=fs,
            fieldFlags=('multiline' if multiline else '')
        )

    def cb(self, name, x, y, size=14, checked=False, tooltip=None):
        self.form.checkbox(
            name=name, tooltip=tooltip or name,
            x=x, y=y, size=size, checked=checked,
            buttonStyle='check',
            borderColor=P["gold"],
            fillColor=P["white"],
            textColor=P["gold"],
            forceBorder=True
        )

    def radio(self, group, value, x, y, size=13, selected=False):
        self.form.radio(
            name=group, value=value, selected=selected,
            x=x, y=y, buttonStyle='circle',
            borderColor=P["gold"],
            fillColor=P["white"],
            textColor=P["gold"],
            forceBorder=True, size=size
        )

    def lf(self, x, y, w, lbl, name, h=20, fs=10):
        self.label(x, y + h + 5, lbl, size=8)
        self.tf(name, x, y, w, h, fs=fs)

    # --------------------------------------------------------
    # Priority badge
    # --------------------------------------------------------
    def priority_badge(self, x, y, priority):
        color = PRIORITY_COLORS[priority]
        lbl = PRIORITY_LABELS[priority]
        bw = stringWidth(lbl, "Helvetica-Bold", 7) + 10
        self.c.setFillColor(P[color])
        self.c.roundRect(x, y, bw, 12, 3, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 7)
        self.c.drawString(x + 5, y + 3, lbl)
        return bw

    # ========================================================
    # PAGES
    # ========================================================

    def page_cover(self):
        self.new_page("Cover", "cover")

        # Background decorative band
        self.c.setFillColor(P["navy"])
        self.c.roundRect(34, 72, PAGE_W - 68, PAGE_H - 144, 22, fill=1, stroke=0)

        # Amber top accent
        self.c.setFillColor(P["amber"])
        self.c.roundRect(34, PAGE_H - 160, PAGE_W - 68, 6, 3, fill=1, stroke=0)

        # Title block
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 28)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 174, "The Perfect Sleep")

        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 28)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 204, "Environment")

        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 228, "CHECKLIST PLANNER")

        self.c.setStrokeColor(P["gold"])
        self.c.setLineWidth(1.5)
        self.c.line(130, PAGE_H - 240, PAGE_W - 130, PAGE_H - 240)

        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 266,
                                 "Get the room right once.")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 284, "Then it works every night.")

        # 4 pillar cards
        pillars = [
            ("One-Time\nSetup",     "setup_darkness",  "sage"),
            ("Safe Sleep\nBible",   "safe_sleep",      "blush"),
            ("Nightly\nLog",        "nightly_log",     "gold"),
            ("Troubleshoot",        "troubleshoot",    "amber"),
        ]
        px = 60
        for lbl, dest, col in pillars:
            self.card(px, PAGE_H - 398, 104, 68, fill="surface2")
            self.c.setFillColor(P[col])
            self.c.roundRect(px, PAGE_H - 336, 104, 6, 3, fill=1, stroke=0)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Helvetica-Bold", 8.5)
            lines = lbl.split("\n")
            for i, ln in enumerate(lines):
                tw = stringWidth(ln, "Helvetica-Bold", 8.5)
                self.c.drawString(px + (104 - tw)/2, PAGE_H - 370 + i*14, ln)
            self.c.linkRect("", dest, (px, PAGE_H - 398, px + 104, PAGE_H - 330),
                            relative=0, thickness=0)
            px += 112

        desc_lines = [
            "Room-by-room setup tracker · Safe Sleep (Bonus 5) · Chapter 5 environment",
            "Darkness · White Noise · Temperature · Crib · Monitor · Room-sharing",
            "Nightly condition log · Tog guide · Science reference · Troubleshooting",
        ]
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 9)
        y = PAGE_H - 424
        for ln in desc_lines:
            self.c.drawCentredString(PAGE_W/2, y, ln)
            y -= 16

        # Quick CTA buttons
        self.link_btn(80,  160, 132, 26, "Quick Start Tonight",   "quick_start", fill="amber", txt="white")
        self.link_btn(228, 160, 120, 26, "Safe Sleep Checklist",  "safe_sleep",  fill="blush", txt="white")
        self.link_btn(364, 160, 108, 26, "Nightly Log",           "nightly_log", fill="gold",  txt="bg")

        self.c.setFillColor(P["blush"])
        self.c.setFont("Times-Roman", 11)
        self.c.drawCentredString(PAGE_W/2, 110, "Six & Thriving")
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 9)
        self.c.drawCentredString(PAGE_W/2, 94,
                                 "Companion to Sleep, Baby. Please. — Chapter 5 + Bonus 5")

    def page_toc(self):
        self.new_page("Contents", "contents")
        self.section_header("Planner Navigation",
                            "Tap any section to jump directly to that page.",
                            "CONTENTS", "gold")

        left_items = [
            ("Quick Start — Tonight",           "quick_start"),
            ("Room Setup Guide",                "setup_guide_intro"),
            ("Safe Sleep Checklist (Bonus 5)",  "safe_sleep"),
            ("Tog Rating Quick Guide",          "tog_guide"),
            ("Sleep Science Reference",         "science_ref"),
            ("Troubleshooting Guide",           "troubleshoot"),
        ]
        right_items = [
            ("Darkness Setup Checklist",        "setup_darkness"),
            ("White Noise Setup Checklist",     "setup_wn"),
            ("Temperature Setup Checklist",     "setup_temp"),
            ("Crib & Sleep Surface Checklist",  "setup_crib"),
            ("Monitor Setup Checklist",         "setup_monitor"),
            ("Room-Sharing Checklist",          "setup_roomshare"),
            ("General Environment Checklist",   "setup_general"),
            ("28-Night Condition Log",          "nightly_log"),
            ("My Room Settings Record",         "room_record"),
        ]

        lx, rx = 54, PAGE_W/2 + 8
        self.card(lx, 100, 244, 572, fill="surface")
        self.card(rx, 100, 244, 572, fill="surface")

        self.label(lx + 14, 656, "Core Sections", size=11, color="gold")
        yy = 628
        for lbl, dest in left_items:
            self.link_btn(lx + 14, yy, 216, 24, lbl, dest)
            yy -= 34

        self.label(rx + 14, 656, "Setup Checklists", size=11, color="gold")
        yy = 628
        for lbl, dest in right_items:
            self.link_btn(rx + 14, yy, 216, 24, lbl, dest)
            yy -= 32

        self.nav(prev="cover", nxt="quick_start")

    def page_quick_start(self):
        self.new_page("Quick Start — Tonight", "quick_start")
        self.section_header("Quick Start — Do This Tonight",
                            "If you do nothing else, do these 8 things before the next sleep.",
                            "TONIGHT", "amber")

        self.card(48, 120, PAGE_W - 96, 534, fill="surface")

        y = 616
        for i, item in enumerate(QUICK_WINS, start=1):
            row_fill = "surface2" if i % 2 == 0 else "navy"
            self.card(56, y - 8, PAGE_W - 112, 32, fill=row_fill)
            self.c.setFillColor(P["amber"])
            self.c.roundRect(56, y - 8, 26, 32, 4, fill=1, stroke=0)
            self.c.setFillColor(P["white"])
            self.c.setFont("Helvetica-Bold", 11)
            self.c.drawCentredString(69, y + 4, str(i))
            self.cb(f"qs_{i}", 90, y - 1, size=14)
            self.text(112, y + 6, item, size=9.5, color="cream", max_w=400)
            y -= 40

        self.card(48, 55, PAGE_W - 96, 58, fill="navy")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 12)
        self.c.drawCentredString(PAGE_W/2, 88,
                                 "Done is better than perfect.")
        self.c.setFillColor(P["muted"])
        self.c.setFont("Times-Roman", 10)
        self.c.drawCentredString(PAGE_W/2, 70,
                                 "Fix one thing right now, then work through the full room checklist when it's daylight.")

        self.nav(prev="contents", nxt="setup_guide_intro")

    def page_setup_guide_intro(self):
        self.new_page("Room Setup Guide", "setup_guide_intro")
        self.section_header("The Room Setup System",
                            "Work through each section once. Tick everything off. Then rely on the nightly log.",
                            "SETUP GUIDE", "sage")

        # Section navigator
        self.card(48, 530, PAGE_W - 96, 180, fill="surface")
        self.label(64, 692, "Jump to any setup section", size=11, color="gold")

        sections = [
            ("1. Darkness",         "setup_darkness",  "sky"),
            ("2. White Noise",      "setup_wn",        "sage"),
            ("3. Temperature",      "setup_temp",      "amber"),
            ("4. Crib & Surface",   "setup_crib",      "blush"),
            ("5. Monitor",          "setup_monitor",   "muted"),
            ("6. Room-Sharing",     "setup_roomshare", "gold"),
            ("7. General Env.",     "setup_general",   "gold_dim"),
        ]
        bx, by = 64, 652
        for i, (lbl, dest, col) in enumerate(sections):
            if i == 4:
                bx = 64
                by = 612
            self.link_btn(bx, by, 130, 24, lbl, dest, fill="navy")
            bx += 136

        # Priority legend
        self.card(48, 380, PAGE_W - 96, 130, fill="surface2")
        self.label(64, 492, "Priority Legend", size=11, color="gold")
        legend = [
            ("CRITICAL",    "blush",  "AAP safe sleep guideline or direct safety risk. Must be complete before baby sleeps in this room."),
            ("IMPORTANT",   "amber",  "Significantly impacts sleep quality. Complete within the first week."),
            ("RECOMMENDED", "sage",   "Evidence-based optimisation. Complete when you can — worth doing."),
        ]
        ly = 470
        for lbl, col, desc in legend:
            bw = stringWidth(lbl, "Helvetica-Bold", 7) + 10
            self.c.setFillColor(P[col])
            self.c.roundRect(64, ly, bw, 12, 3, fill=1, stroke=0)
            self.c.setFillColor(P["white"])
            self.c.setFont("Helvetica-Bold", 7)
            self.c.drawString(69, ly + 3, lbl)
            self.text(64 + bw + 8, ly + 3, desc, size=8.5, color="cream", max_w=380)
            ly -= 28

        # Mindset card
        self.card(48, 190, PAGE_W - 96, 172, fill="navy")
        self.label(64, 344, "The Setup Philosophy", size=11, color="gold")
        paras = [
            ("The room works for you or against you every single night. "
             "Most sleep problems that persist after a good routine is in place are environment problems "
             "in disguise — usually light, usually temperature. The one-time setup investment pays back "
             "hundreds of times.", "cream"),
            ("You do not need a perfect nursery. You need a dark, temperature-controlled, "
             "noise-masked sleep space. That's it. This planner gets you there systematically.", "muted"),
        ]
        py = 318
        for para, col in paras:
            py = self.text(64, py, para, size=9.5, color=col, max_w=462)
            py -= 10

        # My setup progress
        self.card(48, 56, PAGE_W - 96, 116, fill="surface")
        self.label(64, 154, "My Setup Progress", size=10, color="gold")
        self.lf(64, 110, 180, "Setup Start Date", "setup_start_date", h=20)
        self.lf(264, 110, 120, "Baby's Name", "setup_baby_name", h=20)
        self.lf(64, 76, 200, "Room Type", "setup_room_type", h=20)
        self.lf(284, 76, 180, "Target Bedtime", "setup_target_bedtime", h=20)

        self.nav(prev="quick_start", nxt="setup_darkness")

    def _setup_checklist_page(self, title, subtitle, tag, bookmark,
                              items, prev_dest, next_dest, tag_color="sage",
                              notes_key=None):
        """Generic room setup checklist page."""
        self.new_page(title, bookmark)
        self.section_header(title, subtitle, tag, tag_color)

        # Overall completion radio
        self.card(48, 655, PAGE_W - 96, 36, fill="navy")
        self.label(64, 681, "Section status:", size=9, color="gold")
        statuses = [("Not started", "none"), ("In progress", "progress"),
                    ("Complete", "done"), ("N/A for us", "na")]
        sx = 168
        for lbl, val in statuses:
            self.radio(f"{bookmark}_status", val, sx, 662, size=11, selected=(val == "none"))
            self.text(sx + 15, 666, lbl, size=8.5, color="cream")
            sx += 108

        y = 636
        for i, (item_text, note_text, priority) in enumerate(items, start=1):
            # Row height depends on text wrap
            row_h = 54
            self.card(48, y - row_h + 8, PAGE_W - 96, row_h, fill="surface" if i % 2 else "surface2")

            # Priority badge
            bw = self.priority_badge(56, y - row_h + 22, priority)

            # Checkbox
            self.cb(f"{bookmark}_item_{i}", 56, y - 6, size=14)

            # Item text
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 10)
            self.c.drawString(76, y, item_text)

            # Note text
            self.text(76, y - 16, note_text, size=8, color="muted", max_w=448)

            y -= row_h + 4
            if y < 160:
                break

        # Notes field
        if notes_key:
            self.card(48, 68, PAGE_W - 96, 96, fill="navy")
            self.label(64, 152, "Notes / what I ordered / still to do", size=9, color="gold")
            self.tf(notes_key, 64, 76, 462, 64, multiline=True, fs=9)

        self.nav(prev=prev_dest, nxt=next_dest)

    def page_setup_darkness(self):
        self._setup_checklist_page(
            "Darkness — Room Setup",
            "The single highest-impact change. True blackout before anything else.",
            "SECTION 1 · DARKNESS", "setup_darkness",
            SETUP_DARKNESS, "setup_guide_intro", "setup_wn",
            tag_color="sky", notes_key="notes_darkness"
        )

    def page_setup_wn(self):
        self._setup_checklist_page(
            "White Noise — Room Setup",
            "Mask household sounds. Recreate the familiar womb environment.",
            "SECTION 2 · WHITE NOISE", "setup_wn",
            SETUP_WHITE_NOISE, "setup_darkness", "setup_temp",
            tag_color="sage", notes_key="notes_wn"
        )

    def page_setup_temp(self):
        self._setup_checklist_page(
            "Temperature — Room Setup",
            "68–72°F / 20–22°C at crib height. Measured, not assumed.",
            "SECTION 3 · TEMPERATURE", "setup_temp",
            SETUP_TEMPERATURE, "setup_wn", "setup_crib",
            tag_color="amber", notes_key="notes_temp"
        )

    def page_setup_crib(self):
        """Crib page has 10 items — needs two pages."""
        self.new_page("Crib & Sleep Surface", "setup_crib")
        self.section_header("Crib & Sleep Surface — Setup",
                            "The sleep surface is the foundation. Every item here is non-negotiable.",
                            "SECTION 4 · CRIB & SURFACE", "blush")

        self.card(48, 655, PAGE_W - 96, 36, fill="navy")
        self.label(64, 681, "Section status:", size=9, color="gold")
        statuses = [("Not started", "none"), ("In progress", "progress"),
                    ("Complete", "done"), ("N/A", "na")]
        sx = 168
        for lbl, val in statuses:
            self.radio("setup_crib_status", val, sx, 662, size=11, selected=(val=="none"))
            self.text(sx + 15, 666, lbl, size=8.5)
            sx += 108

        y = 636
        for i, (item_text, note_text, priority) in enumerate(SETUP_CRIB[:8], start=1):
            row_h = 54
            self.card(48, y - row_h + 8, PAGE_W - 96, row_h,
                      fill="surface" if i % 2 else "surface2")
            self.priority_badge(56, y - row_h + 22, priority)
            self.cb(f"setup_crib_item_{i}", 56, y - 6, size=14)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 10)
            self.c.drawString(76, y, item_text)
            self.text(76, y - 16, note_text, size=8, color="muted", max_w=448)
            y -= row_h + 4

        self.nav(prev="setup_temp", nxt="setup_crib_b")

        # Page 2 — remaining items
        self.new_page("Crib Setup Continued", "setup_crib_b")
        self.section_header("Crib & Sleep Surface — Continued",
                            "Finishing the 10-point crib safety checklist.",
                            "SECTION 4 · CONTINUED", "blush")

        y = 636
        for i, (item_text, note_text, priority) in enumerate(SETUP_CRIB[8:], start=9):
            row_h = 54
            self.card(48, y - row_h + 8, PAGE_W - 96, row_h,
                      fill="surface" if i % 2 else "surface2")
            self.priority_badge(56, y - row_h + 22, priority)
            self.cb(f"setup_crib_item_{i}", 56, y - 6, size=14)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 10)
            self.c.drawString(76, y, item_text)
            self.text(76, y - 16, note_text, size=8, color="muted", max_w=448)
            y -= row_h + 4

        self.card(48, 68, PAGE_W - 96, 128, fill="navy")
        self.label(64, 180, "Notes / what I ordered / still to do", size=9, color="gold")
        self.tf("notes_crib", 64, 76, 462, 90, multiline=True, fs=9)

        self.nav(prev="setup_crib", nxt="setup_monitor")

    def page_setup_monitor(self):
        self._setup_checklist_page(
            "Monitor — Room Setup",
            "Positioned correctly, dimmed, tested. Not inside the crib.",
            "SECTION 5 · MONITOR", "setup_monitor",
            SETUP_MONITOR, "setup_crib_b", "setup_roomshare",
            tag_color="muted", notes_key="notes_monitor"
        )

    def page_setup_roomshare(self):
        self._setup_checklist_page(
            "Room-Sharing — Setup",
            "AAP recommends room-sharing for 6–12 months. Here's how to do it right.",
            "SECTION 6 · ROOM-SHARING", "setup_roomshare",
            SETUP_ROOM_SHARING, "setup_monitor", "setup_general",
            tag_color="gold", notes_key="notes_roomshare"
        )

    def page_setup_general(self):
        self._setup_checklist_page(
            "General Environment — Setup",
            "The finishing details that prevent surprise disruptions.",
            "SECTION 7 · GENERAL", "setup_general",
            SETUP_GENERAL_ENV, "setup_roomshare", "safe_sleep",
            tag_color="gold_dim", notes_key="notes_general"
        )

    def page_safe_sleep(self):
        self.new_page("Safe Sleep Checklist", "safe_sleep")
        self.section_header("Safe Sleep Checklist — Bonus 5",
                            "AAP-aligned guidelines. Run through this every night until it is muscle memory.",
                            "SAFE SLEEP · BONUS 5", "blush")

        # Sleep surface section
        self.card(48, 400, PAGE_W - 96, 250, fill="surface")
        self.card(48, 618, PAGE_W - 96, 26, fill="blush", radius=8)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(64, 626, "THE SLEEP SURFACE")

        surface_items = [
            "Firm, flat mattress — no incline, pillow-top, or wedge",
            "Fitted sheet only — no loose blankets, bumpers, or pillows",
            "No stuffed animals, positioners, or sleep aids inside the crib",
            "Sleep sack used in place of a blanket — tog matched to room temperature",
            "Baby placed on their back — every sleep, every time, without exception",
            "Crib, bassinet, or play yard only — not a swing, car seat, or bouncer",
        ]
        y = 596
        for i, item in enumerate(surface_items, start=1):
            self.cb(f"safe_surface_{i}", 60, y - 3, size=13)
            self.text(80, y, item, size=9.5, color="cream", max_w=448)
            y -= 22

        # Room section
        self.card(48, 158, PAGE_W - 96, 226, fill="surface2")
        self.card(48, 362, PAGE_W - 96, 26, fill="navy", radius=8)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(64, 370, "THE ROOM")

        room_items = [
            "Room temperature confirmed between 68–72°F / 20–22°C",
            "Baby's chest feels warm but not sweaty — adjust tog if needed",
            "True blackout achieved — if you can see your hand, it is too bright",
            "White noise running at a continuous low level — not inside the crib",
            "Monitor screen and indicator LEDs covered with electrical tape",
            "No nightlight in use, or red-spectrum light only",
        ]
        y = 342
        for i, item in enumerate(room_items, start=1):
            self.cb(f"safe_room_{i}", 60, y - 3, size=13)
            self.text(80, y, item, size=9.5, color="cream", max_w=448)
            y -= 22

        # Room-sharing note
        self.card(48, 68, PAGE_W - 96, 80, fill="navy")
        self.label(64, 134, "Room-Sharing Note (AAP)", size=9, color="gold")
        self.text(64, 118,
                  "Room-sharing — not bed-sharing — for the first 6–12 months reduces SIDS risk by up to 50%. "
                  "Baby sleeps in their own safe surface within arm's reach. Chapter 5 covers full setup.",
                  size=9, color="muted", max_w=462)

        self.nav(prev="setup_general", nxt="tog_guide")

    def page_tog_guide(self):
        self.new_page("Tog Rating Guide", "tog_guide")
        self.section_header("Tog Rating Quick Guide",
                            "Match the sleep sack to the room temperature. Print and post in the nursery.",
                            "TOG REFERENCE", "amber")

        # Big table
        self.card(48, 390, PAGE_W - 96, 280, fill="surface")
        self.card(48, 642, PAGE_W - 96, 26, fill="navy", radius=8)
        for txt, x in [("Room Temperature", 64), ("Tog Rating", 248), ("Dressing Guide", 360)]:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(x, 650, txt)

        y = 616
        row_colors = ["surface2", "surface", "surface2", "surface"]
        for (temp, tog, dressing), fill in zip(TOG_GUIDE, row_colors):
            self.card(52, y - 20, PAGE_W - 104, 46, fill=fill)
            self.text(64,  y, temp,     size=10, color="gold_light", font="Times-Bold")
            self.text(248, y, tog,      size=13, color="amber", font="Helvetica-Bold")
            self.text(360, y, dressing, size=9,  color="cream", max_w=210)
            y -= 56

        # My room settings
        self.card(48, 214, PAGE_W - 96, 162, fill="surface2")
        self.label(64, 360, "My Nursery Settings", size=11, color="gold")
        self.lf(64,  306, 180, "Normal room temp (°C/°F)",   "my_room_temp",    h=22)
        self.lf(264, 306, 180, "Sleep sack we use",           "my_sleep_sack",   h=22)
        self.lf(64,  262, 180, "Tog rating we use",           "my_tog",          h=22)
        self.lf(264, 262, 180, "Dressing underneath",         "my_dressing",     h=22)
        self.lf(64,  218, 380, "Notes / brand / size",        "my_tog_notes",    h=22)

        # Handy note
        self.card(48, 88, PAGE_W - 96, 110, fill="navy")
        self.label(64, 182, "The Rule of Thumb", size=10, color="gold")
        self.text(64, 164,
                  "Dress your baby in one more layer than you would wear comfortably in the same room. "
                  "A chest that is warm (not hot) and a back of the neck that is slightly warm (not sweaty) "
                  "means the tog is right. Hands and feet are always cooler — don't judge by them.",
                  size=9.5, color="cream", max_w=462)

        self.nav(prev="safe_sleep", nxt="science_ref")

    def page_science_ref(self):
        self.new_page("Sleep Science Reference", "science_ref")
        self.section_header("Sleep Environment Science — Why It Matters",
                            "The evidence behind each room setup decision.",
                            "SCIENCE REFERENCE", "sky")

        positions = [
            (48, 396, 244, 160),
            (316, 396, 244, 160),
            (48, 224, 244, 160),
            (316, 224, 244, 160),
            (48, 52, 244, 160),
            (316, 52, 244, 160),
        ]
        for (sc_title, sc_color, sc_body), (x, y, w, h) in zip(SCIENCE_CARDS, positions):
            self.card(x, y, w, h, fill="surface")
            self.c.setFillColor(P[sc_color])
            self.c.roundRect(x, y + h - 20, w, 20, 6, fill=1, stroke=0)
            self.c.setFillColor(P["white"])
            self.c.setFont("Helvetica-Bold", 8.5)
            tw = stringWidth(sc_title, "Helvetica-Bold", 8.5)
            self.c.drawString(x + (w - tw)/2, y + h - 13, sc_title)
            self.text(x + 10, y + h - 34, sc_body, size=8, color="cream", max_w=w - 20)

        self.nav(prev="tog_guide", nxt="troubleshoot")

    def page_troubleshoot(self):
        self.new_page("Troubleshooting Guide", "troubleshoot")
        self.section_header("Environment Troubleshooting",
                            "Persistent sleep problems after setup? Start here.",
                            "TROUBLESHOOT", "amber")

        y = 640
        for i, (problem, solution) in enumerate(TROUBLESHOOT, start=1):
            row_h = 72
            self.card(48, y - row_h + 8, PAGE_W - 96, row_h,
                      fill="surface" if i % 2 else "surface2")
            self.c.setFillColor(P["amber"])
            self.c.roundRect(48, y + 6, PAGE_W - 96, 18, 4, fill=1, stroke=0)
            self.c.setFillColor(P["white"])
            self.c.setFont("Times-Bold", 9.5)
            self.c.drawString(62, y + 10, problem)
            self.text(62, y - 8, solution, size=8.5, color="cream", max_w=462)
            y -= row_h + 8

        self.nav(prev="science_ref", nxt="nightly_log")

    def page_nightly_log(self):
        """28-night condition log — 4 pages of 7 nights each."""
        week_nav = [
            ("nightly_log",   "nightly_log_w2", "Log: Week 1"),
            ("nightly_log_w2","nightly_log_w3", "Log: Week 2"),
            ("nightly_log_w3","nightly_log_w4", "Log: Week 3"),
            ("nightly_log_w4","room_record",    "Log: Week 4"),
        ]
        prev_sources = ["troubleshoot", "nightly_log", "nightly_log_w2", "nightly_log_w3"]

        for w_idx, (bookmark, nxt_dest, wk_label) in enumerate(week_nav):
            self.new_page(wk_label, bookmark)
            self.section_header(f"Nightly Condition Log — {wk_label.split(': ')[1]}",
                                "Log these 6 conditions each night. Patterns emerge by night 3.",
                                "NIGHTLY LOG", "gold")

            # Column headers
            self.card(48, 630, PAGE_W - 96, 24, fill="navy")
            cols = [
                ("Night",     52),
                ("Date",     100),
                ("Temp °F/°C",163),
                ("Blackout?", 235),
                ("W.Noise?",  305),
                ("Tog",       370),
                ("Crib OK?",  430),
                ("LEDs?",     490),
                ("Notes",     540),
            ]
            for h, x in cols:
                self.c.setFillColor(P["gold"])
                self.c.setFont("Helvetica-Bold", 8)
                self.c.drawString(x, 638, h)

            row_y = 596
            for n in range(1, 8):
                night_num = w_idx * 7 + n
                fill = "surface" if n % 2 else "surface2"
                self.card(48, row_y - 8, PAGE_W - 96, 30, fill=fill)
                self.c.setFillColor(P["gold_light"])
                self.c.setFont("Helvetica-Bold", 9)
                self.c.drawString(56, row_y + 4, str(night_num))
                # Date
                self.tf(f"log_n{night_num}_date",  100, row_y - 2, 54, 18, fs=8)
                # Temp
                self.tf(f"log_n{night_num}_temp",  163, row_y - 2, 64, 18, fs=8)
                # Yes/No radio pairs
                for key, x0 in [("dark", 235), ("wn", 305), ("crib", 430), ("leds", 490)]:
                    self.radio(f"log_n{night_num}_{key}", "Y", x0,     row_y - 1, size=11, selected=True)
                    self.c.setFillColor(P["muted"])
                    self.c.setFont("Helvetica", 7)
                    self.c.drawString(x0 + 13, row_y + 3, "Y")
                    self.radio(f"log_n{night_num}_{key}", "N", x0 + 28, row_y - 1, size=11)
                    self.c.drawString(x0 + 41, row_y + 3, "N")
                # Tog
                self.tf(f"log_n{night_num}_tog",    370, row_y - 2, 50, 18, fs=8)
                # Notes
                self.tf(f"log_n{night_num}_notes",  540, row_y - 2, 120, 18, fs=8)
                row_y -= 38

            # Week summary section
            self.card(48, 120, PAGE_W - 96, 110, fill="surface2")
            self.label(64, 214, f"Week {w_idx + 1} Summary", size=10, color="gold")
            self.lf(64,  160, 160, "Most common issue this week",    f"w{w_idx+1}_issue",   h=18, fs=9)
            self.lf(244, 160, 120, "Average room temp",              f"w{w_idx+1}_avgtemp", h=18, fs=9)
            self.lf(384, 160, 120, "Tog used most nights",           f"w{w_idx+1}_tog",     h=18, fs=9)
            self.lf(64,  128, 440, "What I adjusted this week",      f"w{w_idx+1}_adjust",  h=18, fs=9)

            self.nav(prev=prev_sources[w_idx], nxt=nxt_dest)

    def page_room_record(self):
        self.new_page("My Room Settings Record", "room_record")
        self.section_header("My Room Settings — Permanent Record",
                            "Fill this in once the room is dialled in. Post on the nursery wall or inside the door.",
                            "ROOM RECORD", "sage")

        # Big settings card
        self.card(48, 290, PAGE_W - 96, 390, fill="surface")
        self.label(64, 664, "Final Confirmed Settings", size=12, color="gold")

        # Darkness
        self.card(56, 620, PAGE_W - 112, 36, fill="navy")
        self.label(68, 642, "DARKNESS", size=8, color="sky")
        self.lf(170, 624, 180, "Blackout curtain brand/model", "rec_curtain", h=18, fs=9)
        self.lf(370, 624, 160, "LED tape used?", "rec_led_tape", h=18, fs=9)

        # White noise
        self.card(56, 576, PAGE_W - 112, 36, fill="surface2")
        self.label(68, 598, "WHITE NOISE", size=8, color="sage")
        self.lf(170, 580, 130, "Machine brand/model", "rec_wn_brand",  h=18, fs=9)
        self.lf(314, 580, 80,  "Volume (dB)",         "rec_wn_db",     h=18, fs=9)
        self.lf(408, 580, 120, "Sound type",          "rec_wn_sound",  h=18, fs=9)

        # Temperature
        self.card(56, 532, PAGE_W - 112, 36, fill="navy")
        self.label(68, 554, "TEMPERATURE", size=8, color="amber")
        self.lf(170, 536, 130, "Target temp (°C/°F)",  "rec_temp_target",  h=18, fs=9)
        self.lf(314, 536, 130, "Thermostat setting",   "rec_thermostat",   h=18, fs=9)
        self.lf(458, 536, 70,  "Confirmed OK?",        "rec_temp_ok",      h=18, fs=9)

        # Sleep sack
        self.card(56, 488, PAGE_W - 112, 36, fill="surface2")
        self.label(68, 510, "SLEEP SACK", size=8, color="gold")
        self.lf(170, 492, 120, "Brand/model",          "rec_sack_brand",   h=18, fs=9)
        self.lf(304, 492, 60,  "Current tog",          "rec_sack_tog",     h=18, fs=9)
        self.lf(378, 492, 80,  "Size",                 "rec_sack_size",    h=18, fs=9)
        self.lf(472, 492, 56,  "Dressing under",       "rec_dressing",     h=18, fs=9)

        # Monitor
        self.card(56, 444, PAGE_W - 112, 36, fill="navy")
        self.label(68, 466, "MONITOR", size=8, color="muted")
        self.lf(170, 448, 180, "Monitor brand/model",  "rec_monitor",      h=18, fs=9)
        self.lf(364, 448, 100, "Position from crib",   "rec_monitor_pos",  h=18, fs=9)
        self.lf(478, 448, 50,  "Brightness",           "rec_monitor_br",   h=18, fs=9)

        # Nightlight
        self.card(56, 298, PAGE_W - 112, 36, fill="surface2")
        self.label(68, 320, "NIGHTLIGHT", size=8, color="gold_dim")
        self.lf(170, 302, 160, "Type (red/none/other)", "rec_nightlight",   h=18, fs=9)
        self.lf(344, 302, 180, "Position in room",      "rec_nightlight_pos",h=18, fs=9)

        # Room dimensions / notes
        self.card(48, 120, PAGE_W - 96, 160, fill="surface2")
        self.label(64, 264, "Additional Setup Notes", size=10, color="gold")
        self.tf("rec_notes", 64, 128, 462, 124, multiline=True, fs=9)

        # Nightly checklist card to print
        self.card(48, 56, PAGE_W - 96, 58, fill="navy")
        self.label(64, 104, "Print & Post — Nightly 30-Second Check:", size=9, color="gold")
        nightly_txt = "  ✓ Temp in range   ✓ Blackout confirmed   ✓ White noise ON   ✓ Tog correct   ✓ Crib clear   ✓ LEDs covered"
        self.text(64, 84, nightly_txt, size=9, color="cream")

        self.nav(prev="nightly_log_w4", nxt="safe_sleep")

    # ========================================================
    # BUILD
    # ========================================================
    def build(self):
        self.page_cover()
        self.page_toc()
        self.page_quick_start()
        self.page_setup_guide_intro()
        self.page_setup_darkness()
        self.page_setup_wn()
        self.page_setup_temp()
        self.page_setup_crib()    # 2 pages
        self.page_setup_monitor()
        self.page_setup_roomshare()
        self.page_setup_general()
        self.page_safe_sleep()
        self.page_tog_guide()
        self.page_science_ref()
        self.page_troubleshoot()
        self.page_nightly_log()   # 4 pages
        self.page_room_record()

        self._footer()
        self.c.save()


if __name__ == "__main__":
    out = "sleep_environment_planner.pdf"
    print("Building Perfect Sleep Environment Checklist Planner...")
    EnvironmentPlannerPDF(out).build()
    print(f"Done: {os.path.abspath(out)}")
