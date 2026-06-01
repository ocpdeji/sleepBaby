# sleep_baby_please_pdf_planner_godmode.py
# Premium interactive PDF planner generator for
# "The Sleep, Baby. Please. System Planner"
# Requires: pip install reportlab

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
import os

PAGE_W, PAGE_H = LETTER
MARGIN = 36

P = {
    "bg": HexColor("#0F1923"),
    "surface": HexColor("#1A2737"),
    "surface2": HexColor("#1F2E42"),
    "navy": HexColor("#1C2B4A"),
    "navy_light": HexColor("#243556"),
    "gold": HexColor("#C9A84C"),
    "gold_light": HexColor("#E8C97A"),
    "blush": HexColor("#C97A7A"),
    "mint": HexColor("#6ABFA0"),
    "cream": HexColor("#F0E8D8"),
    "muted": HexColor("#8FA0B8"),
    "dim": HexColor("#4A607A"),
    "rule": HexColor("#2A3F5A"),
    "input_bg": HexColor("#0D1720"),
    "input_bd": HexColor("#2E4A6A"),
    "warn": HexColor("#E07A3A"),
    "white": white,
    "black": black,
}

CHAPTERS = [
    ("1", "Why Your Baby Won't Sleep", "Understanding the 'why' is the first step to sleep.", [
        "Sleep associations are the #1 culprit — what happens at sleep onset will be needed at every waking.",
        "Overtiredness triggers cortisol, making it harder to fall asleep — timing is everything.",
        "Developmental leaps cause temporary regressions — they are normal and they end.",
        "You did not cause this by being a loving, responsive parent.",
    ]),
    ("2", "Sleep Science Every Parent Needs", "Awake windows, cortisol, melatonin — made practical.", [
        "Sleep pressure builds with wake time — hit the sweet spot, not too early or late.",
        "The circadian rhythm is trainable from 6–8 weeks — light is your lever.",
        "Sleeping through is often just a 5–6 hour stretch clinically.",
        "Baby sleep cycles are shorter than adult cycles — transitions matter.",
    ]),
    ("3", "Reading Your Baby's Sleep Cues", "Catch the green light before you hit red.", [
        "Green cues mean start winding down now.",
        "Yellow cues mean go time — get to the crib.",
        "Red cues mean overtiredness is already making things harder.",
        "Use awake windows, not just cues, because cues are easy to miss.",
    ]),
    ("4", "Building a Bedtime Routine", "Same order, every night. This week, lock it in.", [
        "Same sequence every night — the order is the signal.",
        "20–30 minutes is the sweet spot.",
        "Write your actual routine and keep it visible.",
        "Drowsy but awake is the skill you are building.",
    ]),
    ("5", "Setting the Sleep Environment", "Darkness, white noise, temperature — your checklist.", [
        "True blackout matters.",
        "White noise should be steady and safe.",
        "Temperature should be comfortable, not hot.",
        "Cover glowing LEDs and reduce stimulation.",
    ]),
    ("6", "The Sleep Training Debate", "Choose your method. Write it down. Stick to it.", [
        "Consistency matters more than method-hopping.",
        "Choose a method that fits both parent and baby temperament.",
        "Write the plan before nightfall.",
        "Give the method enough nights before judging.",
    ]),
    ("7", "Night Wakings", "Handle them without creating new habits.", [
        "Pause before entering — many babies cycle and resettle.",
        "Avoid rushing in too early.",
        "Feed only when genuinely hungry.",
        "Be boring, calm, and predictable at night.",
    ]),
    ("8", "The Six Sleep Personalities", "Know your baby's type. Work with it, not against it.", [
        "The Snacker needs longer gaps between feeds over time.",
        "The Sensitive Soul needs extra calm-down buffer.",
        "The Night Owl often needs bedtime shifted gradually earlier.",
        "The Catnapper needs practice linking cycles.",
    ]),
    ("9", "Common Mistakes Parents Make", "Awareness is the first step to breaking the cycle.", [
        "Inconsistency is the biggest sleep killer.",
        "Feeding to sleep is the most common sleep association.",
        "Rushing in too quickly can prevent self-settling.",
        "Changing methods mid-week resets progress.",
    ]),
    ("10", "Staying Consistent", "Consistency on hard nights is where progress lives.", [
        "Hard nights are not failed nights.",
        "Partner alignment matters.",
        "Trust the rested plan when you are tired.",
        "Progress is rarely perfectly linear.",
    ]),
    ("11", "Toddler Sleep", "When babies become little negotiators — stay firm.", [
        "One drink, one hug, one question — then goodnight.",
        "The routine still works.",
        "Avoid rewarding bedtime resistance.",
        "Validate feelings without changing boundaries.",
    ]),
    ("12", "Your First-Week Game Plan", "Night-by-night. You have everything you need.", [
        "Night 1–2 are often the hardest.",
        "Night 3–4 often show a shift.",
        "Night 5–7 often begin to groove.",
        "One hard night does not erase progress.",
    ]),
]

PERSONALITIES = [
    ("The Snacker", "Needs frequent small feeds to feel settled.", "Gradually lengthen the gap between feeds. Ensure full feeds during the day."),
    ("The Overthinker", "Startles easily and stays alert.", "Use deep calm, low stimulation, and strong routine consistency."),
    ("The Sensitive Soul", "Gets overwhelmed easily by noise, light, and transitions.", "Use extra-long calm-down time and a slower pre-bed rhythm."),
    ("The Night Owl", "Wired late and genuinely not tired at a typical bedtime.", "Shift bedtime earlier gradually until you find the sweet spot."),
    ("The Catnapper", "Wakes after one short cycle and struggles to resettle.", "Practice linking cycles with consistent settling support."),
    ("The Party Animal", "FOMO drives everything.", "Make bedtime boring, calm, and ultra-predictable."),
]

METHODS = [
    ("Extinction (CIO)", "High", "Fast (3–5 days)", "Persistent babies; high-sleep-need families", "Place baby in crib awake and follow through without checks."),
    ("Ferber / Graduated Extinction", "Moderate", "Medium (5–7 days)", "Most temperaments", "Timed check-ins with increasing intervals."),
    ("Chair Method", "Low–Moderate", "Slower (2–3 weeks)", "Sensitive babies", "Stay nearby and gradually move away over time."),
    ("Fading", "Low", "Slowest (3–4+ weeks)", "Gentle approach", "Reduce support step by step."),
    ("Pick Up / Put Down", "Low", "Variable", "Young babies; high support needs", "Pick up when upset, put down when calm, repeat consistently."),
]

AWAKE_WINDOWS = [
    ("0–6 weeks", "45–60 min", "4–5/day", "Variable", "No routine yet; feed-wake-sleep rhythm."),
    ("6–12 weeks", "60–90 min", "4/day", "8–9 p.m.", "Circadian rhythm is emerging."),
    ("3–4 months", "90 min", "3–4/day", "7:30–8:30 p.m.", "Regression risk and maturing cycles."),
    ("4–6 months", "2 hrs", "3/day", "7–8 p.m.", "A more predictable phase."),
    ("6–8 months", "2.5 hrs", "2–3/day", "7–8 p.m.", "Nap transition zone."),
    ("8–12 months", "3–3.5 hrs", "2/day", "6:30–7:30 p.m.", "Two naps become firmer."),
    ("12–18 months", "4–5 hrs", "1–2/day", "7–7:30 p.m.", "One-nap transition begins."),
    ("18–24 months", "5–6 hrs", "1/day", "7–7:30 p.m.", "One nap is typical."),
]

BEDTIME_STEPS = [
    ("Transition Signal", "e.g. dim lights + same phrase"),
    ("Stop Stimulating Activity", "Screens off, rough play ended, energy lowered"),
    ("Bath or Warm Wipe-Down", "5–10 minutes"),
    ("Lotion Massage", "Slow, gentle strokes"),
    ("Pajamas + Sleep Sack", "Dress for room temperature"),
    ("Feed — Dim, Quiet Room", "Keep baby from fully falling asleep"),
    ("Books or Lullaby", "Same books or same songs helps"),
    ("Final Goodnight Phrase", "Use the same exact wording"),
    ("White Noise ON", "Steady safe volume"),
    ("Room Fully Dark", "Blackout and LEDs covered"),
    ("Into Crib — Drowsy Awake", "This is the key skill"),
    ("Parent Exits Calmly", "Same exit, same energy, no lingering"),
]

ROUTINE_ITEMS = [
    "Bedtime is consistent (within 15 min of target)",
    "Awake window honoured — not over or under",
    "Routine followed in correct order",
    "Feed did not become a sleep association",
    "Baby placed in crib drowsy but awake",
    "White noise confirmed on",
    "Room confirmed fully dark",
    "Parent exited calmly",
]

SAFE_SLEEP = [
    "Firm, flat mattress — no incline, wedge, or pillow-top",
    "Fitted sheet only — no blankets, bumpers, pillows, or positioners",
    "Baby on their back — every sleep, every time",
    "Sleep sack used instead of loose blanket",
    "Room temperature 68–72°F / 20–22°C confirmed",
    "True blackout achieved",
    "White noise running (not inside the crib)",
    "All monitor and device LEDs covered",
    "No nightlight, or red-spectrum only",
    "Sleep space is crib, bassinet, or play yard — not swing or car seat",
]

SLEEP_PROMISE = [
    "I will keep bedtime simple and in the same order every night.",
    "I will watch awake windows and act before overtiredness sets in.",
    "I will decide how to respond to night wakings before the night begins.",
    "I will pause before going in and give my baby the chance to resettle.",
    "I will not judge the whole plan on the basis of one difficult night.",
    "I will stay consistent — especially on the nights when it is hardest.",
    "I am not just surviving the night. I am teaching my baby a lifelong skill.",
]

REFLECTION_PROMPTS = [
    ("What went well this week?", "Even one small win counts."),
    ("What was the hardest moment?", "Name it. Acknowledge it. You survived it."),
    ("What patterns did you notice in the Night Waking Log?", "Look for repeated waking times or repeated triggers."),
    ("What would you do differently next week?", "One specific change only."),
    ("What is your baby teaching you this week?", "About temperament, timing, and needs."),
]

AFFIRM = [
    "You are not just surviving the night. You are teaching your baby a skill they will use for life.",
    "Progress over perfection. Every longer stretch is a victory.",
    "Consistency on hard nights is where progress is actually made.",
    "Sleep is coming — for both of you.",
    "Two steps forward, one step back. You are still moving forward.",
    "The hard nights mean you are in it. Keep going.",
    "You chose a method. You worked the plan. That is what winning looks like.",
    "Know your baby's type. Work with it, not against it.",
    "Awareness breaks the cycle. You are already ahead.",
    "On hard nights: this is temporary. It will not last forever.",
    "The negotiations are real. Stay kind and stay firm.",
    "You have everything you need. This is just the beginning.",
]

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class PlannerPDF:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.form = self.c.acroForm
        self.page_num = 0
        self.c.setTitle("The Sleep, Baby. Please. System Planner")
        self.c.setAuthor("Six & Thriving")
        self.c.setSubject("Premium interactive fillable 12-week PDF planner")
        self.c.setCreator("Python + ReportLab")

    def new_page(self, title=None, bookmark=None, bg="bg"):
        if self.page_num > 0:
            self.footer()
            self.c.showPage()
        self.page_num += 1
        self.c.setFillColor(P[bg])
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if bookmark:
            self.c.bookmarkPage(bookmark)
            if title:
                self.c.addOutlineEntry(title, bookmark, 0, False)

    def footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.line(MARGIN, 22, PAGE_W - MARGIN, 22)
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 8)
        self.c.drawString(MARGIN, 10, "Sleep, Baby. Please. System Planner")
        self.c.drawRightString(PAGE_W - MARGIN, 10, str(self.page_num))

    def topbar(self, section_text):
        self.c.setFillColor(P["navy"])
        self.c.rect(0, PAGE_H - 22, PAGE_W, 22, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(MARGIN, PAGE_H - 15, section_text)

    def section_header(self, title, subtitle="", tag=""):
        self.c.setFillColor(P["navy"])
        self.c.roundRect(MARGIN, PAGE_H - 110, PAGE_W - 2*MARGIN, 72, 14, fill=1, stroke=0)
        if tag:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(MARGIN + 16, PAGE_H - 58, tag)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 22)
        self.c.drawString(MARGIN + 16, PAGE_H - 78, title)
        if subtitle:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 10)
            self.c.drawString(MARGIN + 16, PAGE_H - 94, subtitle)

    def card(self, x, y, w, h, fill="surface", r=12):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, r, fill=1, stroke=0)

    def text(self, x, y, s, size=10, color="cream", font="Times-Roman", max_width=None, leading=None):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        leading = leading or size + 3
        if max_width is None:
            self.c.drawString(x, y, s)
            return y - leading
        lines = simpleSplit(s, font, size, max_width)
        yy = y
        for line in lines:
            self.c.drawString(x, yy, line)
            yy -= leading
        return yy

    def label(self, x, y, s, size=8, color="muted", font="Helvetica-Bold"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawString(x, y, s)

    def link_button(self, x, y, w, h, text, dest, fill="surface2", txt="gold_light"):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
        self.c.setFillColor(P[txt])
        self.c.setFont("Helvetica-Bold", 9)
        tw = stringWidth(text, "Helvetica-Bold", 9)
        self.c.drawString(x + (w - tw)/2, y + 7, text)
        self.c.linkRect("", dest, (x, y, x + w, y + h), relative=0, thickness=0)

    def nav_row(self, prev_dest=None, next_dest=None, home_dest="cover"):
        y = 28
        if prev_dest:
            self.link_button(MARGIN, y, 90, 18, "Previous", prev_dest)
        self.link_button(PAGE_W/2 - 45, y, 90, 18, "Home", home_dest, fill="navy")
        if next_dest:
            self.link_button(PAGE_W - MARGIN - 90, y, 90, 18, "Next", next_dest, fill="gold", txt="bg")

    def text_field(self, name, x, y, w, h=20, value="", multiline=False, fs=10):
        flags = 'multiline' if multiline else ''
        self.form.textfield(
            name=name, x=x, y=y, width=w, height=h,
            tooltip=name, value=value,
            borderStyle='inset',
            borderColor=P["input_bd"],
            fillColor=P["white"],
            textColor=P["black"],
            forceBorder=True,
            fontName='Helvetica',
            fontSize=fs,
            fieldFlags=flags
        )

    def checkbox(self, name, x, y, size=12, checked=False):
        self.form.checkbox(
            name=name, x=x, y=y, size=size, checked=checked,
            buttonStyle='check',
            borderColor=P["gold"], fillColor=P["white"],
            textColor=P["gold"], forceBorder=True
        )

    def radio(self, group, value, x, y, size=12, selected=False):
        self.form.radio(
            name=group, value=value, selected=selected, x=x, y=y, size=size,
            buttonStyle='circle',
            borderColor=P["gold"], fillColor=P["white"],
            textColor=P["gold"], forceBorder=True
        )

    def field(self, x, y, w, label, name, h=18, multiline=False, fs=9):
        self.label(x, y + h + 5, label)
        self.text_field(name, x, y, w, h=h, multiline=multiline, fs=fs)

    def bullets(self, x, y, items, width):
        yy = y
        for item in items:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(x, yy, "•")
            yy = self.text(x + 12, yy, item, size=10, max_width=width - 12)
            yy -= 3
        return yy

    def sidebar_week_tabs(self, week, current_key):
        labels = [
            ("Open", f"week_{week}_open", "open"),
            ("Awake", f"week_{week}_awake", "awake"),
            ("Routine", f"week_{week}_routine", "routine"),
            ("Night", f"week_{week}_night_a", "night"),
            ("Method", f"week_{week}_method", "method"),
            ("Reflect", f"week_{week}_reflect_a", "reflect"),
        ]
        x = PAGE_W - 88
        y = PAGE_H - 150
        for text_label, dest, key in labels:
            fill = "gold" if key == current_key else "surface2"
            txt = "bg" if key == current_key else "gold_light"
            self.link_button(x, y, 52, 16, text_label, dest, fill=fill, txt=txt)
            y -= 22

    def cover(self):
        self.new_page("Cover", "cover")
        self.c.setFillColor(P["navy"])
        self.c.roundRect(30, 64, PAGE_W - 60, PAGE_H - 128, 20, fill=1, stroke=0)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 30)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 150, "Sleep, Baby. Please.")
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 174, "THE 12-WEEK SYSTEM PLANNER")
        self.c.setStrokeColor(P["gold"])
        self.c.setLineWidth(2)
        self.c.line(146, PAGE_H - 185, PAGE_W - 146, PAGE_H - 185)
        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 220, "Finally — a planner built around YOUR baby, not a generic schedule.")
        y = PAGE_H - 264
        for line in [
            "A premium 12-week undated fillable planner covering all 12 chapters.",
            "Awake windows, bedtime routine builder, night waking log, method tracker, and weekly reflection.",
            "The all-in-one companion to the ebook.",
        ]:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 11)
            self.c.drawCentredString(PAGE_W/2, y, line)
            y -= 18
        self.link_button(110, 116, 120, 26, "Start Here", "how_to", fill="gold", txt="bg")
        self.link_button(246, 116, 120, 26, "Baby Profile", "baby_profile")
        self.link_button(382, 116, 120, 26, "Week 1", "week_1_open")
        self.c.setFillColor(P["blush"])
        self.c.setFont("Times-Roman", 11)
        self.c.drawCentredString(PAGE_W/2, 90, "Six & Thriving")

    def contents(self):
        self.new_page("Contents", "contents")
        self.section_header("Planner Navigation", "Tap any section below to jump instantly.", "CONTENTS")
        self.card(48, 110, 240, 560)
        self.card(324, 110, 240, 560)
        self.label(64, 646, "Core Sections", size=11, color="gold")
        yy = 616
        core = [
            ("How to Use", "how_to"),
            ("My Baby's Profile", "baby_profile"),
            ("My Sleep Promise", "sleep_promise"),
            ("Reference: Awake Windows", "ref_awake"),
            ("Reference: Sleep Methods", "ref_methods"),
            ("Reference: Sleep Personalities", "ref_personalities"),
            ("Reference: Safe Sleep", "ref_safe_sleep"),
        ]
        for t, d in core:
            self.link_button(64, yy, 208, 24, t, d)
            yy -= 34
        self.label(340, 646, "12-Week Journey", size=11, color="gold")
        yy = 616
        for i in range(1, 13):
            self.link_button(340, yy, 208, 24, f"Week {i}", f"week_{i}_open")
            yy -= 34
        self.nav_row(prev_dest="cover", next_dest="how_to")

    def how_to(self):
        self.new_page("How to Use", "how_to")
        self.section_header("How to Use This Planner", "One week at a time. Real-life use beats perfect use.", "START HERE")
        self.card(48, 120, PAGE_W - 96, 500)
        steps = [
            ("1", "Read the chapter first", "Each week maps to a chapter. Read, then apply."),
            ("2", "Fill in the pages", "The logs reveal patterns tired brains miss."),
            ("3", "Write your real routine", "The routine page turns ideas into a repeatable order."),
            ("4", "Track nights honestly", "Good nights and hard nights both matter."),
            ("5", "Reflect weekly", "Progress often shows up on paper before it feels obvious."),
        ]
        y = 580
        for num, title, desc in steps:
            self.c.setFillColor(P["gold"])
            self.c.roundRect(68, y - 10, 26, 26, 6, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 12)
            self.c.drawCentredString(81, y + 1, num)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Times-Bold", 12)
            self.c.drawString(108, y + 4, title)
            y = self.text(108, y - 12, desc, size=10, max_width=420)
            y -= 16
        self.link_button(72, 86, 140, 22, "Baby Profile", "baby_profile", fill="gold", txt="bg")
        self.link_button(226, 86, 140, 22, "Sleep Promise", "sleep_promise")
        self.link_button(380, 86, 140, 22, "Go to Week 1", "week_1_open")
        self.nav_row(prev_dest="contents", next_dest="baby_profile")

    def baby_profile(self):
        self.new_page("My Baby's Profile", "baby_profile")
        self.section_header("My Baby's Sleep Profile", "Fill this in before Week 1. Update as your baby grows.", "PROFILE")
        self.card(48, 420, PAGE_W - 96, 230)
        self.label(64, 626, "Baby's Details", size=12, color="gold")
        self.field(64, 574, 220, "Baby's Name", "baby_name")
        self.field(304, 574, 220, "Date of Birth", "baby_dob")
        self.field(64, 530, 220, "Current Age", "baby_age")
        self.field(304, 530, 220, "Planner Start Date", "planner_start_date")
        self.field(64, 486, 460, "Pediatrician / Healthcare Provider", "pediatrician")
        self.field(64, 436, 460, "Current Sleep Challenges", "sleep_challenges")
        self.card(48, 214, PAGE_W - 96, 180, fill="surface2")
        self.label(64, 372, "My Baby's Sleep Personality", size=12, color="gold")
        y = 346
        for i, (name, desc, _) in enumerate(PERSONALITIES):
            self.radio("baby_personality", f"p{i}", 64, y - 4, selected=(i == 0))
            self.text(84, y, name, size=10, font="Times-Bold")
            self.text(200, y, desc[:46], size=8, color="muted")
            y -= 22
        self.card(48, 52, PAGE_W - 96, 136, fill="navy")
        self.label(64, 166, "Chosen Sleep Method", size=12, color="gold")
        y = 142
        for i, (name, cry, speed, _, _) in enumerate(METHODS):
            self.radio("chosen_method", f"m{i}", 64, y - 4, selected=(i == 1))
            self.text(84, y, f"{name} | Cry: {cry} | Speed: {speed}", size=9)
            y -= 18
        self.nav_row(prev_dest="how_to", next_dest="sleep_promise")

    def sleep_promise(self):
        self.new_page("My Sleep Promise", "sleep_promise")
        self.section_header("Your Sleep Promise", "A commitment to your baby — and to yourself.", "PROMISE")
        self.card(48, 140, PAGE_W - 96, 470, fill="navy")
        y = 568
        for i, item in enumerate(SLEEP_PROMISE, start=1):
            self.checkbox(f"promise_{i}", 66, y - 4, size=12)
            y = self.text(86, y, item, size=11, max_width=430)
            y -= 10
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 14)
        self.c.drawCentredString(PAGE_W/2, 176, "Sleep is coming. For both of you.")
        self.checkbox("promise_signed", 68, 108, size=16)
        self.text(94, 112, "I have read this promise and I commit to working the plan.", size=11)
        self.nav_row(prev_dest="baby_profile", next_dest="week_1_open")

    def week_open(self, w, chapter_num, title, subtitle, highlights):
        self.new_page(f"Week {w}", f"week_{w}_open")
        self.topbar(f"WEEK {w:02d} · CHAPTER {chapter_num}")
        self.section_header(f"Week {w} · {title}", subtitle, f"CHAPTER {chapter_num}")
        self.sidebar_week_tabs(w, "open")
        self.card(48, 470, 470, 150)
        self.label(64, 598, "Week Setup", size=12, color="gold")
        self.field(64, 545, 200, "Week Dates", f"w{w}_dates")
        self.field(286, 545, 200, "Baby's Age This Week", f"w{w}_baby_age")
        self.field(64, 500, 200, "Baby's Weight (optional)", f"w{w}_weight")
        self.field(286, 500, 200, "Method This Week", f"w{w}_method_week")
        self.field(64, 452, 422, "This Week's Intention", f"w{w}_intention")
        self.card(48, 200, 470, 240, fill="navy")
        self.label(64, 418, "Key Takeaways", size=12, color="gold")
        self.bullets(68, 392, highlights, 420)
        self.card(48, 88, 470, 88, fill="surface2")
        self.label(64, 152, "Jump to this week's pages", size=9, color="gold")
        buttons = [
            ("Awake", f"week_{w}_awake"),
            ("Routine", f"week_{w}_routine"),
            ("Night A", f"week_{w}_night_a"),
            ("Night B", f"week_{w}_night_b"),
            ("Method", f"week_{w}_method"),
            ("Reflect", f"week_{w}_reflect_a"),
        ]
        bx = 64
        by = 116
        for label, dest in buttons:
            self.link_button(bx, by, 66, 22, label, dest)
            bx += 70
        prev_dest = "sleep_promise" if w == 1 else f"week_{w-1}_reflect_b"
        self.nav_row(prev_dest=prev_dest, next_dest=f"week_{w}_awake")

    def week_awake(self, w):
        self.new_page(f"Week {w} Awake Tracker", f"week_{w}_awake")
        self.topbar(f"WEEK {w:02d} · AWAKE WINDOW TRACKER")
        self.section_header(f"Week {w} · Awake Window Tracker", "Track actual vs target and capture the pattern.", f"WEEK {w}")
        self.sidebar_week_tabs(w, "awake")
        self.card(48, 654, 470, 54, fill="navy")
        ref = " | ".join([f"{a}: {b}" for a, b, _, _, _ in AWAKE_WINDOWS[:4]])
        self.label(64, 686, "Quick reference", size=9, color="gold")
        self.text(64, 670, ref, size=8, max_width=420)
        cols = [("Day", 54), ("Wake", 96), ("Nap 1", 150), ("Nap 2", 208), ("Nap 3", 266), ("Bedtime", 324), ("Settled", 388), ("Actual", 448)]
        self.c.setFillColor(P["navy"])
        self.c.roundRect(48, 624, 470, 24, 6, fill=1, stroke=0)
        for name, x in cols:
            self.label(x, 632, name, size=8, color="gold")
        y = 590
        for day in DAYS:
            self.card(48, y - 6, 470, 30, fill="surface")
            self.text(56, y + 4, day, size=9, color="gold_light", font="Helvetica-Bold")
            positions = [(96, 48, "wake"), (150, 52, "nap1"), (208, 52, "nap2"), (266, 52, "nap3"), (324, 56, "bedtime"), (388, 52, "settled"), (448, 48, "actual")]
            for px, pw, key in positions:
                self.text_field(f"w{w}_{day.lower()}_{key}", px, y, pw, 18, fs=8)
            y -= 38
        self.label(48, 306, "Notes / observations", size=9, color="gold")
        yy = 280
        for day in DAYS:
            self.label(54, yy + 6, day, size=8)
            self.text_field(f"w{w}_{day.lower()}_notes", 86, yy, 432, 18, fs=8)
            yy -= 26
        self.nav_row(prev_dest=f"week_{w}_open", next_dest=f"week_{w}_routine")

    def week_routine(self, w):
        self.new_page(f"Week {w} Routine", f"week_{w}_routine")
        self.topbar(f"WEEK {w:02d} · BEDTIME ROUTINE BUILDER")
        self.section_header(f"Week {w} · Bedtime Routine Builder", "Write it clearly. Repeat it consistently.", f"WEEK {w}")
        self.sidebar_week_tabs(w, "routine")
        self.card(48, 662, 470, 42, fill="navy")
        self.field(64, 674, 180, "Routine Timing", f"w{w}_routine_timing", h=18)
        self.text(262, 682, "Target: 20–30 min", size=9, color="muted")
        self.c.setFillColor(P["navy"])
        self.c.roundRect(48, 632, 470, 24, 6, fill=1, stroke=0)
        headers = [("#", 56), ("Step", 78), ("Our Version", 216), ("Mon", 430), ("Wed", 460), ("Fri", 490)]
        for name, x in headers:
            self.label(x, 640, name, size=8, color="gold")
        y = 598
        for i, (step, _) in enumerate(BEDTIME_STEPS, start=1):
            self.card(48, y - 6, 470, 28, fill="surface" if i % 2 else "surface2")
            self.text(56, y + 4, str(i), size=8, color="gold", font="Helvetica-Bold")
            self.text(78, y + 5, step[:26], size=8, font="Times-Bold")
            self.text_field(f"w{w}_routine_step_{i}_text", 216, y, 200, 18, fs=8)
            self.checkbox(f"w{w}_routine_step_{i}_mon", 432, y + 1, size=11)
            self.checkbox(f"w{w}_routine_step_{i}_wed", 462, y + 1, size=11)
            self.checkbox(f"w{w}_routine_step_{i}_fri", 492, y + 1, size=11)
            y -= 34
        self.card(48, 72, 470, 120)
        self.label(64, 170, "Nightly Checklist", size=10, color="gold")
        for i, item in enumerate(ROUTINE_ITEMS):
            col = 64 if i < 4 else 298
            row = 144 - (i % 4) * 24
            self.checkbox(f"w{w}_checklist_{i+1}", col, row - 2, size=12)
            self.text(col + 18, row, item, size=8, max_width=190)
        self.nav_row(prev_dest=f"week_{w}_awake", next_dest=f"week_{w}_night_a")

    def week_night_a(self, w):
        self.new_page(f"Week {w} Night Log A", f"week_{w}_night_a")
        self.topbar(f"WEEK {w:02d} · NIGHT WAKING LOG")
        self.section_header(f"Week {w} · Night Waking Log", "Nights 1–4. Track every waking clearly.", f"WEEK {w}")
        self.sidebar_week_tabs(w, "night")
        base_y = 650
        for n in range(1, 5):
            top = base_y - (n - 1) * 138
            self.card(48, top - 112, 470, 118)
            self.c.setFillColor(P["navy"])
            self.c.roundRect(48, top - 10, 470, 24, 6, fill=1, stroke=0)
            self.text(60, top - 1, f"Night {n}", size=11, color="gold_light", font="Times-Bold")
            self.field(60, top - 38, 66, "Date", f"w{w}_night{n}_date", h=18, fs=8)
            self.field(136, top - 38, 66, "Bedtime", f"w{w}_night{n}_bedtime", h=18, fs=8)
            self.field(212, top - 38, 66, "Asleep", f"w{w}_night{n}_fell_asleep", h=18, fs=8)
            self.field(288, top - 38, 66, "1st Wake", f"w{w}_night{n}_first_wake", h=18, fs=8)
            self.field(364, top - 38, 66, "Total", f"w{w}_night{n}_total_wakings", h=18, fs=8)
            self.field(440, top - 38, 66, "Morning", f"w{w}_night{n}_morning_wake", h=18, fs=8)
            yy = top - 70
            for wi in range(1, 3):
                self.field(60, yy, 64, f"Wake {wi} time", f"w{w}_night{n}_wake{wi}_time", h=18, fs=7)
                self.field(132, yy, 120, f"Response", f"w{w}_night{n}_wake{wi}_response", h=18, fs=7)
                self.field(260, yy, 80, f"Back asleep", f"w{w}_night{n}_wake{wi}_back_in", h=18, fs=7)
                self.field(348, yy, 158, f"Notes", f"w{w}_night{n}_wake{wi}_notes", h=18, fs=7)
                yy -= 28
        self.nav_row(prev_dest=f"week_{w}_routine", next_dest=f"week_{w}_night_b")

    def week_night_b(self, w):
        self.new_page(f"Week {w} Night Log B", f"week_{w}_night_b")
        self.topbar(f"WEEK {w:02d} · NIGHT WAKING LOG CONTINUED")
        self.section_header(f"Week {w} · Night Waking Log", "Nights 5–7 plus pattern review.", f"WEEK {w}")
        self.sidebar_week_tabs(w, "night")
        base_y = 648
        for n in range(5, 8):
            top = base_y - (n - 5) * 150
            self.card(48, top - 122, 470, 128)
            self.c.setFillColor(P["navy"])
            self.c.roundRect(48, top - 10, 470, 24, 6, fill=1, stroke=0)
            self.text(60, top - 1, f"Night {n}", size=11, color="gold_light", font="Times-Bold")
            self.field(60, top - 38, 66, "Date", f"w{w}_night{n}_date", h=18, fs=8)
            self.field(136, top - 38, 66, "Bedtime", f"w{w}_night{n}_bedtime", h=18, fs=8)
            self.field(212, top - 38, 66, "Asleep", f"w{w}_night{n}_fell_asleep", h=18, fs=8)
            self.field(288, top - 38, 66, "1st Wake", f"w{w}_night{n}_first_wake", h=18, fs=8)
            self.field(364, top - 38, 66, "Total", f"w{w}_night{n}_total_wakings", h=18, fs=8)
            self.field(440, top - 38, 66, "Morning", f"w{w}_night{n}_morning_wake", h=18, fs=8)
            yy = top - 70
            for wi in range(1, 3):
                self.field(60, yy, 64, f"Wake {wi} time", f"w{w}_night{n}_wake{wi}_time", h=18, fs=7)
                self.field(132, yy, 120, f"Response", f"w{w}_night{n}_wake{wi}_response", h=18, fs=7)
                self.field(260, yy, 80, f"Back asleep", f"w{w}_night{n}_wake{wi}_back_in", h=18, fs=7)
                self.field(348, yy, 158, f"Notes", f"w{w}_night{n}_wake{wi}_notes", h=18, fs=7)
                yy -= 28
        self.card(48, 60, 470, 108, fill="surface2")
        self.field(64, 122, 442, "Pattern / trigger you noticed this week", f"w{w}_night_pattern", h=18, fs=8)
        self.field(64, 86, 442, "What response worked best?", f"w{w}_night_best_response", h=18, fs=8)
        self.nav_row(prev_dest=f"week_{w}_night_a", next_dest=f"week_{w}_method")

    def week_method(self, w):
        self.new_page(f"Week {w} Method Tracker", f"week_{w}_method")
        self.topbar(f"WEEK {w:02d} · METHOD TRACKER")
        self.section_header(f"Week {w} · Method Tracker", "Track consistency, challenge points, and confidence.", f"WEEK {w}")
        self.sidebar_week_tabs(w, "method")
        self.c.setFillColor(P["navy"])
        self.c.roundRect(48, 632, 470, 24, 6, fill=1, stroke=0)
        heads = [("Night", 56), ("Method Used", 100), ("Followed?", 228), ("Challenge", 308), ("Different Tomorrow?", 392)]
        for h, x in heads:
            self.label(x, 640, h, size=8, color="gold")
        self.label(460, 640, "1 2 3 4 5", size=8, color="gold")
        y = 594
        for n in range(1, 8):
            self.card(48, y - 8, 470, 32, fill="surface" if n % 2 else "surface2")
            self.text(56, y + 4, str(n), size=9, color="gold_light", font="Helvetica-Bold")
            self.text_field(f"w{w}_method_n{n}_used", 100, y, 116, 18, fs=8)
            self.radio(f"w{w}_method_n{n}_followed", "yes", 232, y + 2, size=10, selected=True)
            self.text(246, y + 4, "Y", size=8)
            self.radio(f"w{w}_method_n{n}_followed", "no", 258, y + 2, size=10)
            self.text(272, y + 4, "N", size=8)
            self.text_field(f"w{w}_method_n{n}_challenge", 308, y, 70, 18, fs=8)
            self.radio(f"w{w}_method_n{n}_different", "yes", 398, y + 2, size=10)
            self.text(412, y + 4, "Y", size=8)
            self.radio(f"w{w}_method_n{n}_different", "no", 424, y + 2, size=10, selected=True)
            self.text(438, y + 4, "N", size=8)
            for s in range(1, 6):
                self.radio(f"w{w}_method_n{n}_confidence", str(s), 460 + (s-1)*11, y + 2, size=9, selected=(s == 3))
            y -= 38
        self.card(48, 136, 470, 90, fill="navy")
        self.label(64, 204, "Method note", size=10, color="gold")
        self.text(64, 186, "Any method can work if it is applied consistently enough to be fairly judged.", size=9, max_width=430)
        self.field(64, 146, 442, "Biggest method lesson this week", f"w{w}_method_lesson", h=18, fs=8)
        self.nav_row(prev_dest=f"week_{w}_night_b", next_dest=f"week_{w}_reflect_a")

    def week_reflect_a(self, w):
        self.new_page(f"Week {w} Reflection A", f"week_{w}_reflect_a")
        self.topbar(f"WEEK {w:02d} · WEEKLY REFLECTION")
        self.section_header(f"Week {w} · Weekly Reflection", "Take five honest minutes. Reflection sharpens progress.", f"WEEK {w}")
        self.sidebar_week_tabs(w, "reflect")
        y = 650
        for i, (q, hint) in enumerate(REFLECTION_PROMPTS, start=1):
            self.card(48, y - 84, 470, 90)
            self.c.setFillColor(P["navy"])
            self.c.roundRect(48, y - 8, 470, 24, 6, fill=1, stroke=0)
            self.label(60, y, f"Q{i}", size=8, color="gold")
            self.text(86, y, q, size=10, font="Times-Bold")
            self.text(60, y - 22, hint, size=8, color="muted", max_width=430)
            self.text_field(f"w{w}_reflection_q{i}", 60, y - 72, 446, 30, multiline=False, fs=9)
            y -= 98
        self.nav_row(prev_dest=f"week_{w}_method", next_dest=f"week_{w}_reflect_b")

    def week_reflect_b(self, w):
        self.new_page(f"Week {w} Reflection B", f"week_{w}_reflect_b")
        self.topbar(f"WEEK {w:02d} · WEEK AT A GLANCE")
        self.section_header(f"Week {w} · Week at a Glance", "Capture the stats and set up next week.", f"WEEK {w}")
        self.sidebar_week_tabs(w, "reflect")
        self.card(48, 406, 470, 244)
        self.label(64, 628, "Sleep Stats", size=12, color="gold")
        stats = [
            ("Best night", "best_night"),
            ("Hardest night", "hardest_night"),
            ("Avg. wakings / night", "avg_wakings"),
            ("Avg. settle time", "avg_settle"),
            ("Longest sleep stretch", "longest_stretch"),
            ("Avg. bedtime", "bedtime_avg"),
            ("Avg. morning wake", "morning_avg"),
        ]
        yy = 584
        for idx, (lab, key) in enumerate(stats):
            x = 64 if idx % 2 == 0 else 296
            if idx % 2 == 0 and idx > 0:
                yy -= 46
            self.field(x, yy, 180, lab, f"w{w}_stats_{key}", h=18, fs=8)
        self.card(48, 238, 470, 136, fill="surface2")
        self.field(64, 306, 442, "Next Week Intention", f"w{w}_next_intention", h=44, multiline=True, fs=9)
        self.card(48, 108, 470, 92, fill="navy")
        aff = AFFIRM[w-1] if w-1 < len(AFFIRM) else AFFIRM[-1]
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 13)
        lines = simpleSplit(aff, "Times-Italic", 13, 420)
        yy = 160
        for line in lines:
            self.c.drawCentredString(PAGE_W/2, yy, line)
            yy -= 16
        next_dest = "ref_awake" if w == 12 else f"week_{w+1}_open"
        self.nav_row(prev_dest=f"week_{w}_reflect_a", next_dest=next_dest)

    def ref_awake(self):
        self.new_page("Reference Awake Windows", "ref_awake")
        self.section_header("Awake Windows — Quick Reference", "Use this whenever wake timing feels off.", "REFERENCE")
        self.card(48, 164, 470, 490)
        self.c.setFillColor(P["navy"])
        self.c.roundRect(48, 624, 470, 24, 6, fill=1, stroke=0)
        headers = [("Age", 64), ("Window", 156), ("Naps", 246), ("Bedtime", 320), ("Notes", 406)]
        for h, x in headers:
            self.label(x, 632, h, size=8, color="gold")
        y = 594
        for age, aw, naps, bedtime, note in AWAKE_WINDOWS:
            self.card(52, y - 8, 462, 30, fill="surface2" if (y // 34) % 2 == 0 else "surface")
            self.text(64, y + 4, age, size=8, color="gold_light")
            self.text(156, y + 4, aw, size=8)
            self.text(246, y + 4, naps, size=8)
            self.text(320, y + 4, bedtime, size=8)
            self.text(406, y + 4, note[:20], size=8, color="muted")
            y -= 34
        self.nav_row(prev_dest="week_12_reflect_b", next_dest="ref_methods")

    def ref_methods(self):
        self.new_page("Reference Sleep Methods", "ref_methods")
        self.section_header("Sleep Methods — Comparison & Guide", "Choose one and stay with it long enough to evaluate fairly.", "REFERENCE")
        y = 648
        for name, cry, speed, best, principle in METHODS:
            self.card(48, y - 84, 470, 90)
            self.text(64, y - 2, name, size=11, color="gold_light", font="Times-Bold")
            self.text(64, y - 20, f"Cry level: {cry} | Speed: {speed} | Best for: {best}", size=8, color="muted", max_width=430)
            self.text(64, y - 42, principle, size=9, max_width=430)
            y -= 100
        self.nav_row(prev_dest="ref_awake", next_dest="ref_personalities")

    def ref_personalities(self):
        self.new_page("Reference Sleep Personalities", "ref_personalities")
        self.section_header("The Six Sleep Personalities", "Work with temperament, not against it.", "REFERENCE")
        positions = [(48, 404), (292, 404), (48, 264), (292, 264), (48, 124), (292, 124)]
        for (name, desc, tip), (x, y) in zip(PERSONALITIES, positions):
            self.card(x, y, 226, 112)
            self.text(x + 14, y + 86, name, size=11, color="gold_light", font="Times-Bold")
            self.text(x + 14, y + 66, desc, size=8, max_width=196)
            self.text(x + 14, y + 34, f"Key approach: {tip}", size=8, color="muted", max_width=196)
        self.nav_row(prev_dest="ref_methods", next_dest="ref_safe_sleep")

    def ref_safe_sleep(self):
        self.new_page("Reference Safe Sleep", "ref_safe_sleep")
        self.section_header("Safe Sleep Checklist", "A practical nightly checklist page.", "REFERENCE")
        self.card(48, 138, 470, 500)
        y = 602
        for i, item in enumerate(SAFE_SLEEP, start=1):
            self.checkbox(f"safe_sleep_{i}", 64, y - 2, size=13)
            y = self.text(84, y, item, size=10, max_width=420)
            y -= 8
        self.link_button(180, 86, 120, 24, "Back Home", "cover")
        self.link_button(316, 86, 120, 24, "Week 1", "week_1_open", fill="gold", txt="bg")
        self.nav_row(prev_dest="ref_personalities", next_dest="cover")

    def build(self):
        self.cover()
        self.contents()
        self.how_to()
        self.baby_profile()
        self.sleep_promise()
        for i, (cn, title, subtitle, highlights) in enumerate(CHAPTERS, start=1):
            self.week_open(i, cn, title, subtitle, highlights)
            self.week_awake(i)
            self.week_routine(i)
            self.week_night_a(i)
            self.week_night_b(i)
            self.week_method(i)
            self.week_reflect_a(i)
            self.week_reflect_b(i)
        self.ref_awake()
        self.ref_methods()
        self.ref_personalities()
        self.ref_safe_sleep()
        self.footer()
        self.c.save()


if __name__ == "__main__":
    out = "sleep_baby_please_pdf_planner_godmode.pdf"
    PlannerPDF(out).build()
    print(os.path.abspath(out))
