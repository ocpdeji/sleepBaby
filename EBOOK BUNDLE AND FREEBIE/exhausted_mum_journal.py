# exhausted_mum_survival_journal.py
# The Exhausted Mum Survival Journal — Premium Interactive PDF
# "You're not failing. You're figuring it out. Track both."
# Requires: pip install reportlab

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
import os

# ============================================================
#  PALETTE — Warm Navy · Blush · Gold · Cream
# ============================================================

PAGE_W, PAGE_H = LETTER   # 612 x 792
M = 40  # margin

P = {
    "bg":         HexColor("#0D1720"),
    "surface":    HexColor("#1A2737"),
    "surface2":   HexColor("#1E2E42"),
    "navy":       HexColor("#1C2B4A"),
    "navy_light": HexColor("#243556"),
    "gold":       HexColor("#C9A84C"),
    "gold_light": HexColor("#E8C97A"),
    "blush":      HexColor("#C97A8A"),
    "blush_light":HexColor("#E8A0AF"),
    "blush_pale": HexColor("#3A2030"),
    "lavender":   HexColor("#8B80B0"),
    "lav_pale":   HexColor("#1E1A2E"),
    "mint":       HexColor("#6ABFA0"),
    "cream":      HexColor("#F0E8D8"),
    "muted":      HexColor("#8FA0B8"),
    "dim":        HexColor("#4A607A"),
    "rule":       HexColor("#2A3F5A"),
    "input_bg":   HexColor("#F8F4EE"),
    "input_bd":   HexColor("#C9A84C"),
    "warn":       HexColor("#E07A3A"),
    "white":      white,
    "black":      black,
    "heart":      HexColor("#C97A8A"),
}

# ============================================================
#  CONTENT DATA
# ============================================================

AWAKE_WINDOWS = [
    ("0–6 weeks",   "45–60 min", "4–5/day", "Variable",     "Feed-wake-sleep. No set routine yet."),
    ("6–12 weeks",  "60–90 min", "4/day",   "8–9 pm",       "Circadian rhythm begins forming."),
    ("3–4 months",  "90 min",    "3–4/day", "7:30–8:30 pm", "4-month regression risk period."),
    ("4–6 months",  "2 hrs",     "3/day",   "7–8 pm",       "Good time to start a method."),
    ("6–8 months",  "2.5 hrs",   "2–3/day", "7–8 pm",       "2-nap transition zone."),
    ("8–12 months", "3–3.5 hrs", "2/day",   "6:30–7:30 pm", "2 naps firm."),
    ("12–18 mths",  "4–5 hrs",   "1–2/day", "7–7:30 pm",    "1-nap transition begins."),
    ("18–24 mths",  "5–6 hrs",   "1/day",   "7–7:30 pm",    "Nap drop approaching."),
]

PERSONALITIES = [
    ("The Snacker",       "Frequent small feeds, not fully settling between.",
     "Gradually lengthen gaps. Ensure full feeds in the day."),
    ("The Overthinker",   "Alert, startles easily, environment-sensitive.",
     "Deep swaddle, consistent routine, minimal stimulation."),
    ("The Sensitive Soul", "Overwhelmed by noise, light, transitions.",
     "Long calm-down buffer, dimmer, quieter, slower everything."),
    ("The Night Owl",     "Not tired at normal bedtime, genuinely wired late.",
     "Shift bedtime earlier by 10 min every 2–3 days."),
    ("The Catnapper",     "Wakes after 45 min and cannot link cycles.",
     "Practice settling at cycle transitions. Don't rescue too fast."),
    ("The Party Animal",  "FOMO-driven — stimulation equals awake.",
     "Boring, dark, silent exits. Sleep = least interesting option."),
]

METHODS = [
    ("Extinction (CIO)",          "High",       "Fast (3–5 days)",    "Persistent babies; exhausted families"),
    ("Ferber / Graduated Ext.",   "Moderate",   "Medium (5–7 days)",  "Most temperaments; parents who need to act"),
    ("Chair Method",              "Low–Mod",    "Slower (2–3 wks)",   "Sensitive babies; anxious parents"),
    ("Fading",                    "Low",        "Slowest (3–4+ wks)", "Gentle; adaptable babies"),
    ("Pick Up / Put Down",        "Low",        "Variable",           "Young babies 3–5 months; high support needs"),
]

BEDTIME_STEPS = [
    "Transition signal (dim lights + phrase)",
    "Screens off — stimulating activities ended",
    "Bath or warm wipe-down",
    "Lotion massage (slow, calm)",
    "Pyjamas + sleep sack on",
    "Feed in dim, quiet room (no falling asleep)",
    "1–3 books or lullaby",
    "Final goodnight phrase (same words, every night)",
    "White noise ON",
    "Room fully dark (LEDs covered)",
    "Into crib — drowsy but awake",
    "Parent exits calmly and consistently",
]

SAFE_SLEEP = [
    "Firm, flat mattress — no wedge, incline, or pillow-top",
    "Fitted sheet only — no blankets, bumpers, or pillows",
    "Baby on back — every sleep, every time",
    "Sleep sack instead of a loose blanket",
    "Room temperature confirmed 68–72°F / 20–22°C",
    "True blackout achieved (can't see your hand)",
    "White noise running (not inside the crib)",
    "All monitor and device LEDs covered",
    "No nightlight, or red-spectrum only",
    "Sleep space is crib/bassinet/play yard only",
]

DAILY_AFFIRM = [
    "You are not failing. You are figuring it out. That is exactly what love looks like at 3am.",
    "The fact that you're still going — still trying — means more than you know.",
    "A baby who is loved is already thriving. You are the proof of that.",
    "Hard nights don't make you a bad mum. They make you an exhausted one. That's allowed.",
    "You will sleep again. You will feel like yourself again. This is temporary.",
    "Every small thing you do for your baby today matters more than you realise.",
    "You are not alone in this. Thousands of mums are in the dark with you right now.",
    "Asking for help is not failing. It is the most courageous thing you can do.",
    "You don't have to be perfect. You just have to be there. And you are.",
    "The guilt means you care. But guilt without action is just noise. Let it go.",
    "Tomorrow is another chance. Tonight, you just have to get through tonight.",
    "Your baby doesn't need a perfect mother. They need you. Just you.",
    "Crying in the bathroom counts as self-care if it means you got 90 seconds alone.",
    "You fed them. You held them. You showed up. That is everything.",
    "Progress on hard nights is invisible. It still counts.",
    "You are building something. Sleep is coming — for both of you.",
    "Grace over perfection. Every single time.",
    "One more night. You have survived every hard night so far. This one too.",
    "Your love for this child is evident in every single page of this journal.",
    "It's okay to not be okay. Write it here. Feel it. Then keep going.",
    "The version of you doing this right now is stronger than you think.",
    "Reaching for this journal at the end of a hard day is an act of courage.",
    "Consistency matters more than perfection. You are still consistent.",
    "Two steps forward, one step back. You are still ahead of where you started.",
    "You are allowed to grieve the sleep you've lost and still love this baby fiercely.",
    "The nights that break you a little are the same nights that build you.",
    "Messy progress is still progress. Look how far you've come.",
    "You will remember these nights. Not with bitterness — with pride.",
    "You gave everything today. That is enough. That has always been enough.",
    "Sleep is coming. For both of you. Keep the faith.",
]

THREE_AM_PROMPTS = [
    "Right now, thousands of other mums are awake in the dark with you. You are not the only one holding a baby in a quiet house at this hour.",
    "This is the hardest part. Not the lack of sleep — the silence around you at 3am. But you are seen. And this season will end.",
    "If you could write a letter to yourself from six months from now, what would she want you to know tonight?",
    "What is one thing you did today — however small — that was good? Hold that. You did that.",
    "The love that is keeping you awake right now will be the same love that makes you a great mum long after sleep returns.",
    "Name one thing you're grateful for in this exact moment. Even if it is tiny. Even if it is just that your baby is safe.",
    "What does the version of you who got through this look like? She exists. She is coming.",
    "You don't have to figure out the whole plan tonight. You only have to get through tonight.",
    "It's okay to feel resentment and fierce love at exactly the same time. Both things are real. Both things are allowed.",
    "This baby chose you. Of all the people in the world — they chose you.",
    "What do you need to hear right now? Write it in the notes below. Say it to yourself.",
    "The mum who is awake at 3am because she loves her baby too much to stop showing up — that is who you are.",
    "Breathe. You are doing the hardest job there is. And you are still here.",
    "The morning will come. It always does. You just have to get there.",
    "What would you say to a friend who was sitting where you are sitting right now?",
    "You are not behind. You are not broken. You are in the thick of it. Keep going.",
    "Every long night has an end. You have proof of this from every previous night you have survived.",
    "The version of you reading this in a year will not believe she made it through — but she did. You will.",
    "This love you feel — even exhausted, even overwhelmed — is extraordinary.",
    "Tomorrow's plan matters. Tonight's survival matters more.",
    "There is nothing wrong with you. There is nothing wrong with your baby. This is just the beginning.",
    "The quiet house can feel so lonely. But somewhere in that silence is also peace — the baby is breathing, and you are here.",
    "You have everything your baby needs. You are enough.",
    "Even on the nights you feel like you're failing — the fact that you're still in the room proves you're not.",
    "Hard nights are not permanent. They are part of the bridge between where you are and where you're going.",
    "The patience you've shown today — even the exhausted, imperfect version of it — is a gift to your child.",
    "What you are doing at 3am in the dark, alone and tired — that is love in its purest form.",
    "You have survived 100% of your hardest nights so far. That record holds tonight.",
    "Your baby will not remember this night. But you will — as the night you didn't quit.",
    "Sleep is coming. For both of you. I promise.",
]

WEEK_THEMES = [
    ("Week 1", "The First Seven Days", "Establishing, surviving, beginning to see.",
     "blush", "blush_pale"),
    ("Week 2", "Patterns Start to Emerge", "What the data is already starting to tell you.",
     "gold", "navy"),
    ("Week 3", "Finding Your Footing", "Confidence is built in the details. You're building it.",
     "mint", "surface"),
    ("Week 4", "You Made It a Month", "A month in. Look how far you've come.",
     "lavender", "lav_pale"),
]

WEEK_REFLECT_Q = [
    ("How many nights felt hard?", "Be honest. Hard nights are data, not failure."),
    ("What pattern did you notice in the sleep log?", "Repeated wake times, settle methods that worked, etc."),
    ("What was the biggest win this week?", "Even if tiny — write it. It happened."),
    ("What was the hardest moment?", "Name it. You survived it. It counts."),
    ("How did YOU feel this week — honestly?", "Not as a mother. As a person."),
    ("What would you do differently next week?", "One thing only."),
    ("What did your baby teach you about themselves this week?", "Every week reveals something."),
]

MUM_PROMISE = [
    "I will track my sleep — and my feelings — without judgment.",
    "I will name my hard moments instead of burying them.",
    "I will celebrate small wins, even when the night felt like a loss.",
    "I will ask for help before I reach breaking point.",
    "I will remember that my emotional health is my baby's emotional health.",
    "I will not compare myself to mothers online or in my mother's group.",
    "I will rest when I can, eat when I can, and drink the water.",
    "I will hold the guilt loosely — I am learning, not failing.",
    "I will be honest in these pages. This journal sees the whole truth.",
    "I will remember: I am not just surviving the night. I am becoming her mother.",
]


# ============================================================
#  PDF ENGINE
# ============================================================

class MumJournalPDF:
    def __init__(self, filename="Exhausted_Mum_Survival_Journal.pdf"):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.c.setTitle("The Exhausted Mum Survival Journal")
        self.c.setAuthor("Six & Thriving")
        self.c.setSubject("Premium sleep tracker and emotional check-in journal for new mothers")
        self.form = self.c.acroForm
        self.page_num = 0

    # ──────────────────────────────────────────────
    # Core page / layout helpers
    # ──────────────────────────────────────────────

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
                self.c.addOutlineEntry(title, bookmark, level=0, closed=True)

    def _footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.line(M, 20, PAGE_W - M, 20)
        self.c.setFont("Helvetica", 7)
        self.c.setFillColor(P["muted"])
        self.c.drawString(M, 8, "The Exhausted Mum Survival Journal  ·  Six & Thriving")
        self.c.drawRightString(PAGE_W - M, 8, f"p. {self.page_num}")

    def section_header(self, title, subtitle="", tag=None, tag_color="blush"):
        y = PAGE_H - 52
        self.c.setFillColor(P["navy"])
        self.c.roundRect(M, y - 52, PAGE_W - 2*M, 66, 12, fill=1, stroke=0)
        if tag:
            self.c.setFillColor(P[tag_color])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(M + 16, y - 8, tag)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 21)
        self.c.drawString(M + 16, y + 8, title)
        if subtitle:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 10)
            self.c.drawString(M + 16, y - 14, subtitle)

    def card(self, x, y, w, h, fill="surface", radius=10, stroke_color=None, lw=0):
        self.c.setFillColor(P[fill])
        if stroke_color:
            self.c.setStrokeColor(P[stroke_color])
            self.c.setLineWidth(lw or 1)
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
        else:
            self.c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

    def label(self, x, y, text, size=8, color="muted", font="Helvetica-Bold"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        self.c.drawString(x, y, text)

    def txt(self, x, y, text, size=10, color="cream", font="Times-Roman",
            max_w=None, leading=None, align="left"):
        self.c.setFillColor(P[color])
        self.c.setFont(font, size)
        lead = leading or (size + 3)
        if align == "center":
            if max_w:
                lines = simpleSplit(text, font, size, max_w)
                for ln in lines:
                    self.c.drawCentredString(x + max_w/2, y, ln)
                    y -= lead
            else:
                self.c.drawCentredString(x, y, text)
            return y
        if not max_w:
            self.c.drawString(x, y, text)
            return y - lead
        lines = simpleSplit(text, font, size, max_w)
        for ln in lines:
            self.c.drawString(x, y, ln)
            y -= lead
        return y

    def hline(self, x1, y, x2, color="rule", lw=0.5):
        self.c.setStrokeColor(P[color])
        self.c.setLineWidth(lw)
        self.c.line(x1, y, x2, y)

    def col_hdr(self, x, y, w, text, bg="navy", fg="gold"):
        self.c.setFillColor(P[bg])
        self.c.rect(x, y, w, 18, fill=1, stroke=0)
        self.c.setFillColor(P[fg])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawCentredString(x + w/2, y + 5, text)

    # ──────────────────────────────────────────────
    # Navigation
    # ──────────────────────────────────────────────

    def nav(self, prev=None, nxt=None, home="cover"):
        y = 28
        if prev:
            self._navbtn(M, y, 88, 16, "← Previous", prev, "surface2", "muted")
        self._navbtn(PAGE_W/2 - 42, y, 84, 16, "❤ Home", home, "blush_pale", "blush_light")
        if nxt:
            self._navbtn(PAGE_W - M - 88, y, 88, 16, "Next →", nxt, "gold", "bg")

    def _navbtn(self, x, y, w, h, text, dest, fill, fg, size=8):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 6, fill=1, stroke=0)
        self.c.setFillColor(P[fg])
        self.c.setFont("Helvetica-Bold", size)
        tw = stringWidth(text, "Helvetica-Bold", size)
        self.c.drawString(x + (w - tw)/2, y + h/2 - 3, text)
        self.c.linkRect("", dest, (x, y, x+w, y+h), relative=0, thickness=0)

    def link_pill(self, x, y, w, h, text, dest, fill="navy", fg="gold_light", size=9):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
        self.c.setFillColor(P[fg])
        self.c.setFont("Helvetica-Bold", size)
        tw = stringWidth(text, "Helvetica-Bold", size)
        self.c.drawString(x + (w - tw)/2, y + h/2 - 3, text)
        self.c.linkRect("", dest, (x, y, x+w, y+h), relative=0, thickness=0)

    # ──────────────────────────────────────────────
    # Form fields
    # ──────────────────────────────────────────────

    def tf(self, name, x, y, w, h=20, value="", multi=False, size=10, tooltip=None):
        self.form.textfield(
            name=name, tooltip=tooltip or name,
            x=x, y=y, width=w, height=h,
            borderStyle="inset", borderColor=P["input_bd"],
            fillColor=P["input_bg"], textColor=P["black"],
            forceBorder=True, value=value,
            fontName="Helvetica", fontSize=size,
            fieldFlags=("multiline" if multi else ""),
        )

    def cb(self, name, x, y, size=13, checked=False, tooltip=None):
        self.form.checkbox(
            name=name, tooltip=tooltip or name,
            x=x, y=y, size=size, checked=checked,
            buttonStyle="check", borderColor=P["gold"],
            fillColor=P["white"], textColor=P["gold"],
            forceBorder=True,
        )

    def rb(self, group, value, x, y, size=12, selected=False, tooltip=None):
        self.form.radio(
            name=group, tooltip=tooltip or value,
            value=value, selected=selected,
            x=x, y=y, buttonStyle="circle",
            borderColor=P["blush"], fillColor=P["white"],
            textColor=P["blush"], forceBorder=True, size=size,
        )

    def lf(self, x, y, w, lbl, name, h=20, size=10, multi=False, lines=1):
        """Labeled text field."""
        fh = h if not multi else max(h, 16 * lines)
        self.label(x, y + fh + 5, lbl, size=8)
        self.tf(name, x, y, w, fh, size=size, multi=multi)

    # ──────────────────────────────────────────────
    # Shared reusable layouts
    # ──────────────────────────────────────────────

    def mood_row(self, prefix, x, y, group_suffix, bar_color="blush",
                 labels=None, title="Mood", rb_color="blush"):
        """5-point radio scale row with labels."""
        if labels is None:
            labels = ["1","2","3","4","5"]
        self.label(x, y + 18, title, size=8, color=bar_color)
        spacing = 82
        for i, lbl in enumerate(labels):
            rx = x + i * spacing
            self.rb(f"{prefix}_{group_suffix}", str(i+1), rx, y, size=13,
                    selected=(i == 2), tooltip=lbl)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7)
            self.c.drawString(rx + 16, y + 3, lbl[:12])

    def nap_block(self, prefix, x, y, n):
        """Single nap row."""
        label = f"Nap {n}" if n <= 3 else "Extra"
        self.label(x, y + 6, label, size=8, color="gold")
        self.tf(f"{prefix}_nap{n}_start", x + 32, y, 48, 18, size=9, tooltip=f"Nap {n} start")
        self.label(x + 84, y + 3, "–", size=9, color="muted")
        self.tf(f"{prefix}_nap{n}_end",   x + 92, y, 48, 18, size=9, tooltip=f"Nap {n} end")
        self.label(x + 144, y + 3, "=", size=9, color="muted")
        self.tf(f"{prefix}_nap{n}_total", x + 154, y, 38, 18, size=9, tooltip="total")
        # quality
        self.label(x + 196, y + 6, "Quality:", size=7, color="muted")
        for qi, qv in enumerate(["Easy","Medium","Hard"]):
            self.rb(f"{prefix}_nap{n}_q", qv, x + 234 + qi * 52, y + 2, size=10,
                    selected=(qi == 0), tooltip=qv)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7)
            self.c.drawString(x + 248 + qi * 52, y + 4, qv)

    # ──────────────────────────────────────────────
    # PAGES
    # ──────────────────────────────────────────────

    # ─── COVER ────────────────────────────────────

    def page_cover(self):
        self.new_page("Cover", "cover", bg="bg")

        # large blush glow blobs
        self.c.setFillColor(Color(0.79, 0.48, 0.54, 0.12))
        self.c.circle(PAGE_W - 60, PAGE_H - 60, 200, fill=1, stroke=0)
        self.c.circle(80, 120, 160, fill=1, stroke=0)

        # Inner card
        self.card(30, 60, PAGE_W - 60, PAGE_H - 120, "navy", 20)

        # Decorative top accent bar
        self.c.setFillColor(P["blush"])
        self.c.roundRect(30, PAGE_H - 90, PAGE_W - 60, 8, 4, fill=1, stroke=0)

        # Brand
        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 116, "SIX & THRIVING")

        # Main title
        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Bold", 13)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 154, "THE")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 36)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 194, "Exhausted Mum")
        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Times-Bold", 28)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 228, "Survival Journal")

        # Rule
        self.c.setStrokeColor(P["gold"])
        self.c.setLineWidth(1.5)
        self.c.line(130, PAGE_H - 244, PAGE_W - 130, PAGE_H - 244)

        # Tagline
        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Italic", 14)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 270,
            "Track your baby's sleep. Track your own heart.")

        # Feature pills
        pills = ["30 Days", "Baby Sleep Log", "Mum's Emotional Check-In",
                 "Weekly Reflection", "3am Prompts", "Safe Sleep Guide"]
        pw = 86
        gap = 8
        total = len(pills) * pw + (len(pills)-1) * gap
        px = (PAGE_W - total) / 2
        py = PAGE_H - 330
        for i, pill in enumerate(pills):
            fc = "blush_pale" if i % 2 == 0 else "lav_pale"
            tc = "blush_light" if i % 2 == 0 else "lavender"
            self.c.setFillColor(P[fc])
            self.c.roundRect(px, py, pw, 20, 6, fill=1, stroke=0)
            self.c.setFillColor(P[tc])
            self.c.setFont("Helvetica-Bold", 7)
            tw = stringWidth(pill, "Helvetica-Bold", 7)
            self.c.drawString(px + (pw - tw)/2, py + 6, pill)
            px += pw + gap

        # Central emotional copy block
        self.card(56, PAGE_H - 550, PAGE_W - 112, 190, "surface2", 12)
        self.c.setFillColor(P["blush"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 386, "A NOTE BEFORE YOU BEGIN")
        lines = [
            "You picked up this journal at the right moment. Whether it's 3pm",
            "or 3am — whether you're holding a sleeping baby or a screaming one —",
            "you are exactly where you need to be.",
            "",
            "This journal holds two things at once: your baby's sleep data, and",
            "your own emotional truth. Because both of those matter.",
            "",
            "You're not failing. You're figuring it out.",
        ]
        yy = PAGE_H - 410
        for ln in lines:
            if ln == "":
                yy -= 6
                continue
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Italic" if "failing" in ln else "Times-Roman", 10)
            self.c.drawCentredString(PAGE_W/2, yy, ln)
            yy -= 15

        # CTA buttons
        self.link_pill(70, 92, 130, 26, "Begin →", "toc", "gold", "bg")
        self.link_pill(214, 92, 130, 26, "My Profile", "profile", "surface2", "gold_light")
        self.link_pill(358, 92, 130, 26, "Day 1", "d1_sleep", "blush_pale", "blush_light")

        # Bottom credit
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 8)
        self.c.drawCentredString(PAGE_W/2, 72,
            "Sleep, Baby. Please. · The Companion Journal · Six & Thriving")

    # ─── TABLE OF CONTENTS ────────────────────────

    def page_toc(self):
        self.new_page("Contents", "toc")
        self.section_header("Journal Navigation",
            "Tap any entry to jump directly to that page.", "CONTENTS", "blush")

        # Two column layout
        lx, rx = 52, PAGE_W/2 + 8
        cw = PAGE_W/2 - 60

        self.card(lx, 100, cw, 568, "surface")
        self.card(rx, 100, cw, 568, "surface")

        # Left col — core sections
        self.label(lx+14, 648, "Journal Foundations", size=11, color="gold")
        core = [
            ("How to Use This Journal", "how_to"),
            ("My Profile & Baby Details", "profile"),
            ("My Promise to Myself", "promise"),
            ("Reference: Awake Windows", "ref_awake"),
            ("Reference: Sleep Methods", "ref_methods"),
            ("Reference: Sleep Personalities", "ref_personalities"),
            ("Safe Sleep Checklist", "safe_sleep"),
            ("Letter to Future Self", "letter_self"),
            ("Notes Pages", "notes"),
        ]
        yy = 622
        for lbl, dest in core:
            self.link_pill(lx+14, yy, cw-28, 22, lbl, dest, "navy", "cream", 8)
            yy -= 30

        # Left bottom: weekly reflections
        self.label(lx+14, yy-4, "Weekly Reflections", size=9, color="blush_light")
        yy -= 26
        for i in range(1, 5):
            self.link_pill(lx+14, yy, cw-28, 20, f"Week {i} Reflection", f"w{i}_reflect",
                           "blush_pale", "blush_light", 8)
            yy -= 27

        # Right col — 30 daily pages
        self.label(rx+14, 648, "30 Days — Sleep + Heart", size=11, color="gold")
        yy2 = 622
        for d in range(1, 31):
            self.link_pill(rx+14, yy2, (cw-36)/2 - 2, 18,
                           f"Day {d} Sleep", f"d{d}_sleep", "surface2", "gold_light", 7)
            self.link_pill(rx+14 + (cw-36)/2 + 4, yy2, (cw-36)/2 - 2, 18,
                           f"Day {d} Heart", f"d{d}_heart", "blush_pale", "blush_light", 7)
            yy2 -= 20

        self.nav(prev="cover", nxt="how_to")

    # ─── HOW TO USE ───────────────────────────────

    def page_how_to(self):
        self.new_page("How to Use", "how_to")
        self.section_header("How to Use This Journal",
            "Simple. Honest. Daily. Even on the worst nights.", "START HERE", "blush")

        self.card(M, 100, PAGE_W - 2*M, 580, "surface")

        steps = [
            ("❤", "Track both baby and yourself, every day",
             "Each day has two pages: your baby's sleep log, and your own emotional check-in. "
             "Both pages matter equally. Neither is optional."),
            ("✦", "Be honest — this journal is just for you",
             "No one is grading this. Write the real feelings. Name the hard moments. "
             "The only wrong way to use this journal is to perform positivity you don't feel."),
            ("✓", "Fill in the baby log first, then your heart page",
             "Start with the facts (times, wakings, nap data) — then move to how you actually feel. "
             "The baby log grounds you. The heart page releases you."),
            ("◆", "Use the 3am prompt when you can't sleep",
             "Every heart page has a rotating prompt designed for the quiet hours. "
             "You don't have to write much. Even one sentence is enough."),
            ("★", "Do the weekly reflections — they change everything",
             "Patterns only emerge when you look back. The weekly pages turn daily data "
             "into insight. 10 minutes on a Sunday can shift the whole next week."),
            ("◯", "Grace over perfection, every single time",
             "Missed a day? Start from today. Forgot to track a nap? Leave it blank. "
             "An imperfect journal used daily is more valuable than a perfect journal used once."),
        ]
        yy = 640
        for icon, title, desc in steps:
            self.c.setFillColor(P["blush"])
            self.c.roundRect(64, yy - 8, 26, 26, 6, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 12)
            self.c.drawCentredString(77, yy + 3, icon)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Times-Bold", 11)
            self.c.drawString(100, yy + 4, title)
            yy = self.txt(100, yy - 10, desc, size=9, color="muted", max_w=430)
            yy -= 12

        self.link_pill(64, 118, 140, 24, "My Profile →", "profile", "gold", "bg")
        self.link_pill(218, 118, 140, 24, "My Promise →", "promise", "blush_pale", "blush_light")
        self.link_pill(372, 118, 140, 24, "Start Day 1 →", "d1_sleep", "navy", "gold_light")
        self.nav(prev="toc", nxt="profile")

    # ─── PROFILE ──────────────────────────────────

    def page_profile(self):
        self.new_page("My Profile", "profile")
        self.section_header("My Profile — Baby & Mum",
            "Fill this in before Day 1. Update it as you grow.", "MY DETAILS", "gold")

        # Baby card
        self.card(M, 470, PAGE_W - 2*M, 220, "surface")
        self.label(56, 668, "Baby's Details", size=12, color="gold")

        self.lf(56,  622, 200, "Baby's Name",               "baby_name")
        self.lf(270, 622, 200, "Date of Birth",              "baby_dob")
        self.lf(56,  576, 200, "Current Age / Stage",        "baby_age")
        self.lf(270, 576, 200, "Journal Start Date",         "start_date")
        self.lf(56,  530, 414, "Pediatrician / GP Contact",  "pediatrician")
        self.lf(56,  484, 414, "Current sleep challenge (in your words)", "challenge", h=30)

        # Personality selector
        self.card(M, 290, PAGE_W - 2*M, 160, "surface2")
        self.label(56, 432, "Baby's Sleep Personality (Circle One)", size=11, color="gold")
        self.txt(56, 416, "You can update this any time — babies change.", size=8, color="muted")
        yp = 394
        for idx, (name, desc, _) in enumerate(PERSONALITIES):
            self.rb("baby_personality", f"p{idx}", 56, yp - 4, size=11, selected=(idx == 0))
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 10)
            self.c.drawString(73, yp, name)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 8)
            self.c.drawString(192, yp, desc[:56])
            if idx == 2:
                yp = 394 - 26
                yp -= 26
            else:
                yp -= 22

        # Mum's wellbeing starting point
        self.card(M, 104, PAGE_W - 2*M, 168, "blush_pale")
        self.label(56, 252, "Mum — My Starting Point", size=12, color="blush_light")
        self.lf(56,  206, 414, "How I would describe my mental health right now",
                "mum_mental", h=26)
        self.lf(56,  162, 200, "Biggest fear about this process", "mum_fear")
        self.lf(270, 162, 200, "One thing I know about myself as a mum", "mum_strength")

        self.nav(prev="how_to", nxt="promise")

    # ─── MUM'S PROMISE ────────────────────────────

    def page_promise(self):
        self.new_page("My Promise", "promise")
        self.section_header("My Promise to Myself",
            "Not a promise to be perfect. A promise to be honest.", "THE COMMITMENT", "blush")

        self.card(M, 148, PAGE_W - 2*M, 540, "navy")

        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Times-Italic", 12)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 160,
            "I open this journal because I believe that seeing the truth")
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 178,
            "is the first step toward living it differently.")

        self.hline(80, PAGE_H - 192, PAGE_W - 80, "rule", 0.5)

        yy = PAGE_H - 218
        for i, item in enumerate(MUM_PROMISE):
            self.cb(f"promise_{i}", 60, yy - 4, size=13)
            yy = self.txt(82, yy, item, size=10, color="cream", max_w=436)
            yy -= 8

        self.c.setFillColor(P["gold"])
        self.c.setFont("Times-Italic", 14)
        self.c.drawCentredString(PAGE_W/2, 230,
            "\"You're not failing. You're figuring it out.\"")

        self.hline(80, 218, PAGE_W - 80, "gold", 0.8)

        self.label(60, 200, "Signed:", size=9, color="muted")
        self.tf("promise_sig",  110, 185, 220, 20, size=10, tooltip="Your name")
        self.label(342, 200, "Date:", size=9, color="muted")
        self.tf("promise_date", 376, 185, 140, 20, size=10, tooltip="Today's date")

        self.cb("promise_committed", 60, 160, size=14)
        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Roman", 10)
        self.c.drawString(82, 164, "I have read this promise. I commit to showing up for myself — even imperfectly.")

        self.nav(prev="profile", nxt="d1_sleep")

    # ─── DAILY PAGES (30 × 2) ─────────────────────

    def day_sleep_page(self, d):
        """Page A: Baby's Night — sleep tracking."""
        week = min((d - 1) // 7 + 1, 4)
        prev = f"d{d-1}_heart" if d > 1 else "promise"
        nxt  = f"d{d}_heart"
        bk   = f"d{d}_sleep"

        self.new_page(f"Day {d} — Sleep Log", bk)
        self.section_header(
            f"Day {d}  ·  Baby's Night",
            f"Week {week}  ·  Track every waking. Patterns emerge from the data.",
            f"SLEEP LOG · DAY {d}", "gold"
        )

        # Quick jump row
        self.c.setFillColor(P["surface2"])
        self.c.roundRect(M, PAGE_H - 138, PAGE_W - 2*M, 26, 6, fill=1, stroke=0)
        self.link_pill(M + 4, PAGE_H - 136, 110, 22,
                       f"Day {d} Heart →", f"d{d}_heart", "blush_pale", "blush_light", 8)
        self.link_pill(PAGE_W - M - 114, PAGE_H - 136, 110, 22,
                       f"Week {week} Reflect", f"w{week}_reflect", "navy", "gold_light", 8)

        # ── Night overview fields ──
        self.card(M, 596, PAGE_W - 2*M, 64, "surface")
        self.label(56, 645, "Night Overview", size=10, color="gold")
        self.lf(56,  606, 80,  "Date",         f"d{d}_date",    h=18, size=9)
        self.lf(148, 606, 80,  "Bedtime",      f"d{d}_bedtime", h=18, size=9)
        self.lf(240, 606, 80,  "Fell Asleep",  f"d{d}_asleep",  h=18, size=9)
        self.lf(332, 606, 80,  "Morning Wake", f"d{d}_wake",    h=18, size=9)
        self.lf(424, 606, 80,  "Total Sleep",  f"d{d}_total",   h=18, size=9)

        # ── Night Wakings Table ──
        self.card(M, 420, PAGE_W - 2*M, 166, "surface2")
        self.label(56, 568, "Night Wakings Log", size=10, color="gold")
        # Table headers
        col_x = [56, 126, 196, 290, 390, 480]
        col_w = [62,  62,  90,  92,  88,  52]
        hdrs  = ["Time Up","Settled","Duration","How I Settled","Method","Fed?"]
        self.c.setFillColor(P["navy"])
        self.c.roundRect(M+2, 546, PAGE_W - 2*M - 4, 18, 4, fill=1, stroke=0)
        for hdr, cx, cw in zip(hdrs, col_x, col_w):
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 7)
            self.c.drawString(cx, 551, hdr)

        # 5 waking rows
        for r in range(5):
            ry = 526 - r * 24
            bg = "surface" if r % 2 == 0 else "surface2"
            self.card(M+2, ry - 4, PAGE_W - 2*M - 4, 22, bg, 4)
            self.tf(f"d{d}_w{r}_time",   col_x[0], ry, col_w[0]-4, 16, size=8)
            self.tf(f"d{d}_w{r}_settled",col_x[1], ry, col_w[1]-4, 16, size=8)
            self.tf(f"d{d}_w{r}_dur",    col_x[2], ry, col_w[2]-4, 16, size=8)
            self.tf(f"d{d}_w{r}_how",    col_x[3], ry, col_w[3]-4, 16, size=8)
            # method radio
            for mi, mv in enumerate(["SS","Pt","Feed","Rock"]):
                self.rb(f"d{d}_w{r}_method", mv, col_x[4]+mi*22, ry+2, size=9,
                        selected=(mi==0), tooltip=mv)
                self.c.setFillColor(P["muted"])
                self.c.setFont("Helvetica", 6)
                self.c.drawString(col_x[4]+mi*22+11, ry+4, mv)
            # fed
            self.rb(f"d{d}_w{r}_fed", "Y", col_x[5],    ry+2, size=9, selected=False, tooltip="Yes")
            self.rb(f"d{d}_w{r}_fed", "N", col_x[5]+20, ry+2, size=9, selected=True,  tooltip="No")
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 6)
            self.c.drawString(col_x[5]+11, ry+4, "Y")
            self.c.drawString(col_x[5]+31, ry+4, "N")

        # ── Nap Tracker ──
        self.card(M, 264, PAGE_W - 2*M, 148, "surface")
        self.label(56, 394, "Today's Nap Tracker", size=10, color="gold")
        self.txt(200, 396, "Start — End = Total  |  Quality: Easy / Medium / Hard",
                 size=8, color="muted")
        for n in range(1, 4):
            self.nap_block(f"d{d}", 56, 382 - n * 36, n)

        # ── Tonight's Method & Environment ──
        self.card(M, 108, PAGE_W - 2*M, 148, "navy")
        self.label(56, 238, "Tonight's Setup", size=10, color="gold")

        # Method radio
        self.label(56, 224, "Sleep method used:", size=8, color="muted")
        mnames = ["CIO","Ferber","Chair","Fading","PUPD","Own"]
        for mi, mn in enumerate(mnames):
            self.rb(f"d{d}_method", mn, 56 + mi * 84, 206, size=11,
                    selected=(mi==1), tooltip=mn)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(56 + mi * 84 + 14, 208, mn)

        # Environment checks
        self.label(56, 192, "Environment:", size=8, color="muted")
        env_items = [
            ("Room pitch dark", f"d{d}_env_dark"),
            ("White noise on",   f"d{d}_env_wn"),
            ("Temp 68–72°F",    f"d{d}_env_temp"),
            ("No LEDs visible",  f"d{d}_env_led"),
            ("On back in crib",  f"d{d}_env_back"),
            ("Drowsy not asleep",f"d{d}_env_drowsy"),
        ]
        for ei, (elbl, ename) in enumerate(env_items):
            ex = 56 + (ei % 3) * 172
            ey = 174 - (ei // 3) * 22
            self.cb(ename, ex, ey, size=11)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(ex + 14, ey + 2, elbl)

        # Follow plan?
        self.label(56, 130, "Followed the plan tonight?", size=8, color="muted")
        for ri, rv in enumerate(["Yes — fully","Mostly","Struggled","No"]):
            self.rb(f"d{d}_plan", rv, 56 + ri * 120, 114, size=11, selected=(ri==0), tooltip=rv)
            self.c.setFillColor(P["cream"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(56 + ri * 120 + 14, 116, rv)

        self.nav(prev=prev, nxt=nxt)

    def day_heart_page(self, d):
        """Page B: Mum's Heart — emotional check-in."""
        week  = min((d - 1) // 7 + 1, 4)
        prev  = f"d{d}_sleep"
        nxt   = f"d{d+1}_sleep" if d < 30 else f"w4_reflect"
        # Insert weekly reflection links after days 7, 14, 21
        if d in (7, 14, 21):
            nxt = f"w{d//7}_reflect"
        bk = f"d{d}_heart"
        affirm = DAILY_AFFIRM[(d - 1) % len(DAILY_AFFIRM)]
        prompt = THREE_AM_PROMPTS[(d - 1) % len(THREE_AM_PROMPTS)]

        self.new_page(f"Day {d} — Mum's Heart", bk)

        # Full blush tint overlay for heart pages
        self.c.setFillColor(Color(0.29, 0.15, 0.19, 0.18))
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

        self.section_header(
            f"Day {d}  ·  Mum's Heart",
            "This page is for you. Honest. Private. Yours.",
            f"EMOTIONAL CHECK-IN · DAY {d}", "blush"
        )

        # Quick jump
        self.c.setFillColor(P["blush_pale"])
        self.c.roundRect(M, PAGE_H - 138, PAGE_W - 2*M, 26, 6, fill=1, stroke=0)
        self.link_pill(M + 4, PAGE_H - 136, 110, 22,
                       f"← Day {d} Sleep", f"d{d}_sleep", "surface2", "gold_light", 8)
        if d < 30:
            self.link_pill(PAGE_W - M - 114, PAGE_H - 136, 110, 22,
                           f"Day {d+1} →", f"d{d+1}_sleep", "navy", "gold_light", 8)

        # ── Mood / Energy / Anxiety scales ──
        self.card(M, 600, PAGE_W - 2*M, 86, "surface")
        self.label(56, 670, "How am I feeling right now?", size=10, color="blush_light")

        mood_labels  = ["Barely\nhere","Struggling","Getting\nby","Actually\nokay","Thriving"]
        energy_labels= ["Empty","Low","Some","Good","Full"]
        anxiety_lbls = ["Calm","Mild","Moderate","High","Very high"]

        # Mood row
        self.label(56, 657, "Mood", size=8, color="blush")
        for i, lbl in enumerate(mood_labels):
            self.rb(f"d{d}_mood", str(i+1), 56 + i*86, 638, size=13,
                    selected=(i==2), tooltip=lbl.replace("\n"," "))
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 6)
            self.c.drawString(56 + i*86 + 15, 641, lbl.split("\n")[0])

        # Energy row
        self.label(56, 625, "Energy", size=8, color="gold")
        for i, lbl in enumerate(energy_labels):
            self.rb(f"d{d}_energy", str(i+1), 56 + i*86, 606, size=13,
                    selected=(i==2), tooltip=lbl)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 6)
            self.c.drawString(56 + i*86 + 15, 609, lbl)

        # ── Guilt + self-care row ──
        self.card(M, 526, PAGE_W - 2*M, 66, "blush_pale")
        self.label(56, 576, "Guilt check:", size=9, color="blush_light")
        self.txt(128, 578,
                 "Guilt is information — not verdict. Name it without judgment.",
                 size=8, color="muted", max_w=380)
        guilt_opts = ["None right now","A little","Quite a bit","A lot — let's talk"]
        for gi, go in enumerate(guilt_opts):
            self.rb(f"d{d}_guilt", go, 56 + gi * 126, 538, size=12,
                    selected=(gi==0), tooltip=go)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7)
            self.c.drawString(56 + gi * 126 + 15, 541, go[:16])

        # Self-care quick checks
        self.label(56, 524, "Self-care today:", size=8, color="muted")
        sc_items = [("Ate a meal",f"d{d}_sc_eat"), ("Drank water",f"d{d}_sc_water"),
                    ("Showered",  f"d{d}_sc_shower"), ("Asked for help",f"d{d}_sc_help"),
                    ("5 min alone",f"d{d}_sc_alone"),("Got outside",f"d{d}_sc_out")]
        for si, (slbl, sname) in enumerate(sc_items):
            sx = 56 + (si % 3) * 168
            sy = 508 - (si // 3) * 18
            self.cb(sname, sx, sy - 2, size=10)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 7)
            self.c.drawString(sx + 13, sy, slbl)

        # ── WIN of the day ──
        self.card(M, 418, PAGE_W - 2*M, 100, "surface")
        self.c.setFillColor(P["gold"])
        self.c.roundRect(M + 2, 494, 130, 20, 4, fill=1, stroke=0)
        self.c.setFillColor(P["bg"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawCentredString(M + 67, 499, "★  MY WIN TODAY")
        self.txt(56, 476,
                 "Something went right. Something you did. Even tiny. Write it.",
                 size=8, color="muted", max_w=486)
        self.tf(f"d{d}_win", 56, 428, 490, 42, size=10, multi=True,
                tooltip="My win today was...")

        # ── Hard moment ──
        self.card(M, 322, PAGE_W - 2*M, 90, "surface2")
        self.c.setFillColor(P["blush"])
        self.c.roundRect(M + 2, 390, 130, 20, 4, fill=1, stroke=0)
        self.c.setFillColor(P["white"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawCentredString(M + 67, 395, "♡  THE HARD MOMENT")
        self.txt(56, 374,
                 "Name it. You don't have to fix it. Just name it.",
                 size=8, color="muted", max_w=486)
        self.tf(f"d{d}_hard", 56, 332, 490, 36, size=10, multi=True,
                tooltip="The hardest moment today was...")

        # ── 3am prompt ──
        self.card(M, 198, PAGE_W - 2*M, 118, "lav_pale")
        self.c.setFillColor(P["lavender"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(56, 298, "3AM PROMPT")
        # Prompt text
        wrap = simpleSplit(f"\"{prompt}\"", "Times-Italic", 9, 486)
        yp = 282
        for ln in wrap[:3]:
            self.c.setFillColor(P["blush_light"])
            self.c.setFont("Times-Italic", 9)
            self.c.drawString(56, yp, ln)
            yp -= 13
        self.tf(f"d{d}_3am", 56, 208, 490, 38, size=9, multi=True,
                tooltip="Your thoughts at 3am...")

        # ── What I need ──
        self.card(M, 108, PAGE_W - 2*M, 84, "surface")
        self.label(56, 176, "What I need from MYSELF tomorrow:", size=8, color="gold")
        self.tf(f"d{d}_need_self", 56, 154, 486, 18, size=9)
        self.label(56, 146, "What I need from SOMEONE ELSE:", size=8, color="blush_light")
        self.tf(f"d{d}_need_other", 56, 118, 486, 22, size=9, multi=True)

        # ── Affirmation footer ──
        self.c.setFillColor(P["blush_pale"])
        self.c.roundRect(M, 52, PAGE_W - 2*M, 50, 8, fill=1, stroke=0)
        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Times-Italic", 10)
        wrap_a = simpleSplit(affirm, "Times-Italic", 10, PAGE_W - 2*M - 40)
        ya = 89 - (len(wrap_a)-1) * 6
        for ln in wrap_a:
            self.c.drawCentredString(PAGE_W/2, ya, ln)
            ya -= 13

        self.nav(prev=prev, nxt=nxt)

    # ─── WEEKLY REFLECTIONS ───────────────────────

    def page_weekly_reflect(self, week):
        theme_title, theme_sub, theme_desc, hdr_color, bg_fill = WEEK_THEMES[week - 1]
        bk = f"w{week}_reflect"
        prev_day = week * 7
        if week < 4:
            nxt = f"d{week*7+1}_sleep"
        else:
            nxt = "progress"

        # ── Page A: Reflection prompts ──
        self.new_page(f"Week {week} Reflection", bk)
        self.section_header(
            f"Week {week} Reflection  ·  {theme_title}",
            theme_desc, f"WEEKLY REFLECTION · WEEK {week}", hdr_color
        )

        self.card(M, 100, PAGE_W - 2*M, 568, "surface")

        self.c.setFillColor(P[hdr_color])
        self.c.setFont("Times-Bold", 11)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 162, f"\"{theme_sub}\"")
        self.hline(60, PAGE_H - 174, PAGE_W - 60, "rule")

        yy = PAGE_H - 198
        for i, (q, hint) in enumerate(WEEK_REFLECT_Q):
            self.card(M+6, yy - 72, PAGE_W - 2*M - 12, 80, "surface2", 8)
            self.c.setFillColor(P[hdr_color])
            self.c.roundRect(M+6, yy - 6, PAGE_W - 2*M - 12, 18, 4, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(M+16, yy, f"Q{i+1}  {q}")
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 8)
            self.c.drawString(M+16, yy - 16, hint)
            self.tf(f"w{week}_q{i}", M+16, yy - 60, PAGE_W - 2*M - 32, 36,
                    size=9, multi=True)
            yy -= 82

        self.nav(prev=f"d{prev_day}_heart", nxt=f"w{week}_reflect_b")

        # ── Page B: Sleep stats + Letter ──
        self.new_page(f"Week {week} Stats", f"w{week}_reflect_b")
        self.section_header(
            f"Week {week}  ·  By the Numbers",
            "Patterns only appear when you look back. Look back.",
            f"WEEK {week} STATS", "gold"
        )

        # Sleep stats grid
        self.card(M, 504, PAGE_W - 2*M, 190, "surface")
        self.label(56, 676, "This Week's Sleep Data", size=11, color="gold")
        stats = [
            ("Best night",          f"w{week}_best"),
            ("Hardest night",       f"w{week}_hardest"),
            ("Avg wakings/night",   f"w{week}_avg_wake"),
            ("Avg settle time",     f"w{week}_settle"),
            ("Longest stretch",     f"w{week}_longest"),
            ("Avg bedtime",         f"w{week}_avg_bed"),
            ("Avg morning wake",    f"w{week}_avg_morning"),
            ("Total nap avg/day",   f"w{week}_nap_avg"),
        ]
        sy = 648
        for i, (lbl, name) in enumerate(stats):
            sx = 56 if i % 2 == 0 else 310
            if i % 2 == 0 and i > 0:
                sy -= 44
            self.lf(sx, sy, 200, lbl, name, h=18, size=9)

        # Mum's emotional summary
        self.card(M, 330, PAGE_W - 2*M, 166, "blush_pale")
        self.label(56, 480, "Mum — This Week's Emotional Summary", size=11, color="blush_light")
        emo_qs = [
            ("How did I feel overall this week?",     f"w{week}_emo_overall"),
            ("Moment I felt most like myself:",        f"w{week}_emo_myself"),
            ("What kept me going on hard days?",       f"w{week}_emo_kept"),
        ]
        ey = 454
        for elbl, ename in emo_qs:
            self.label(56, ey, elbl, size=8, color="muted")
            self.tf(ename, 56, ey - 22, 490, 18, size=9)
            ey -= 44

        # Letter to baby
        self.card(M, 108, PAGE_W - 2*M, 214, "lav_pale")
        self.c.setFillColor(P["lavender"])
        self.c.setFont("Times-Bold", 12)
        self.c.drawString(56, 304, f"Dear Baby — Week {week}")
        self.txt(56, 288,
                 "What do you want to tell them about this week? Write it here.",
                 size=8, color="muted")
        self.tf(f"w{week}_letter_baby", 56, 118, 490, 164, size=10, multi=True,
                tooltip="Dear baby...")

        # Affirmation
        affirm_w = AFFIRM_WEEK[week - 1]
        self.c.setFillColor(P["gold"])
        self.c.setFont("Times-Italic", 11)
        self.c.drawCentredString(PAGE_W/2, 88, f"\"{affirm_w}\"")

        self.nav(prev=f"w{week}_reflect", nxt=nxt)

    # ─── PROGRESS DASHBOARD ───────────────────────

    def page_progress(self):
        self.new_page("Progress Dashboard", "progress")
        self.section_header("30-Day Progress Dashboard",
            "You made it through 30 days. Look at this.", "PROGRESS", "gold")

        # Stat boxes
        stat_labels = [
            "Total nights tracked", "Nights that felt hard", "Best sleep stretch",
            "Avg wakings (final week)", "Days I felt good", "Days I asked for help",
        ]
        sx0, sy0, sw, sh = M, PAGE_H - 310, 152, 72
        for i, sl in enumerate(stat_labels):
            sx = sx0 + (i % 4) * (sw + 10)
            sy = sy0 - (i // 4) * (sh + 12)
            self.card(sx, sy, sw, sh, "navy", 10,
                      stroke_color="gold" if i < 4 else "blush", lw=0.8)
            self.label(sx + 8, sy + sh - 16, sl, size=7, color="muted")
            self.tf(f"prog_stat_{i}", sx + 8, sy + 8, sw - 16, 36, size=18, tooltip=sl)

        # Wins wall
        self.card(M, 138, 246, 258, "surface")
        self.label(56, 378, "My Biggest Wins", size=11, color="gold")
        for i in range(7):
            wy = 356 - i * 32
            self.c.setFillColor(P["gold"])
            self.c.circle(62, wy + 6, 7, fill=1, stroke=0)
            self.c.setFillColor(P["bg"])
            self.c.setFont("Helvetica-Bold", 7)
            self.c.drawCentredString(62, wy + 3, str(i+1))
            self.tf(f"prog_win_{i}", 76, wy - 2, 198, 18, size=8)

        # Emotional journey summary
        self.card(M + 258, 138, 284, 258, "blush_pale")
        self.label(M + 274, 378, "Mum's Emotional Journey", size=11, color="blush_light")
        ej_qs = [
            ("How I felt on Day 1:",   "prog_ej_d1"),
            ("How I feel on Day 30:",  "prog_ej_d30"),
            ("What surprised me most:","prog_ej_surprise"),
            ("What I'd tell Day-1-me:","prog_ej_advice"),
        ]
        ey2 = 354
        for elbl, ename in ej_qs:
            self.label(M+274, ey2, elbl, size=8, color="muted")
            self.tf(ename, M+274, ey2-22, 250, 18, size=9)
            ey2 -= 46

        # Next steps
        self.card(M + 554, 138, 0, 0, "surface2")  # skip — use lf
        self.card(M + 554, 138, PAGE_W - 2*M - 554, 258, "surface2")
        self.label(M + 570, 378, "What's Next", size=11, color="lavender")
        nxt_qs = [
            ("My sleep method going forward:", "prog_nxt_method"),
            ("One thing I'll keep doing:",     "prog_nxt_keep"),
            ("One thing I'll change:",         "prog_nxt_change"),
            ("My word for the next 30 days:",  "prog_nxt_word"),
        ]
        ny = 354
        for nlbl, nname in nxt_qs:
            self.label(M+570, ny, nlbl, size=8, color="muted")
            self.tf(nname, M+570, ny-22, 198, 18, size=9)
            ny -= 46

        # Bottom gold quote
        self.c.setFillColor(P["gold"])
        self.c.roundRect(M, 102, PAGE_W - 2*M, 30, 6, fill=1, stroke=0)
        self.c.setFillColor(P["bg"])
        self.c.setFont("Times-Bold", 12)
        self.c.drawCentredString(PAGE_W/2, 112,
            "You showed up for 30 days. That is not nothing. That is everything.")

        self.nav(prev="w4_reflect_b", nxt="ref_awake")

    # ─── REFERENCE PAGES ──────────────────────────

    def page_ref_awake(self):
        self.new_page("Reference: Awake Windows", "ref_awake")
        self.section_header("Awake Windows — Quick Reference",
            "Use this whenever wake timing feels off.", "REFERENCE", "gold")

        self.card(M, 100, PAGE_W - 2*M, 564, "surface")

        # header row
        self.c.setFillColor(P["navy"])
        self.c.roundRect(M+2, 634, PAGE_W - 2*M - 4, 22, 4, fill=1, stroke=0)
        cols = [("Baby's Age",56), ("Awake Window",154), ("Max Naps",252),
                ("Bedtime Target",330), ("Notes",430)]
        for h, cx in cols:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawString(cx, 641, h)

        y = 614
        for i, (age, aw, naps, bt, note) in enumerate(AWAKE_WINDOWS):
            self.card(M+2, y-6, PAGE_W-2*M-4, 26, "surface2" if i%2 else "surface", 4)
            self.txt(56, y+4, age,  size=9, color="gold_light")
            self.txt(154,y+4, aw,   size=9, color="cream")
            self.txt(252,y+4, naps, size=9, color="cream")
            self.txt(330,y+4, bt,   size=9, color="cream")
            self.txt(430,y+4, note, size=8, color="muted")
            y -= 32

        self.c.setFillColor(P["blush_pale"])
        self.c.roundRect(M+2, 108, PAGE_W-2*M-4, 48, 6, fill=1, stroke=0)
        self.txt(PAGE_W/2, 140, "Always set a timer — don't rely on cues alone.",
                 size=10, color="blush_light", font="Times-Italic", align="center")
        self.txt(PAGE_W/2, 122,
                 "Awake windows are the single most powerful lever in early sleep.",
                 size=9, color="muted", align="center")

        self.nav(prev="progress", nxt="ref_methods")

    def page_ref_methods(self):
        self.new_page("Reference: Sleep Methods", "ref_methods")
        self.section_header("Sleep Methods — Comparison",
            "Choose one. Write it down. Give it 7 consistent nights.", "REFERENCE", "gold")

        y = 636
        for name, cry, speed, best in METHODS:
            self.card(M, y - 80, PAGE_W - 2*M, 88, "surface")
            self.c.setFillColor(P["navy"])
            self.c.roundRect(M+2, y - 4, PAGE_W - 2*M - 4, 18, 4, fill=1, stroke=0)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Times-Bold", 11)
            self.c.drawString(56, y, name)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Helvetica", 8)
            self.c.drawString(56, y - 18, f"Cry level: {cry}  ·  Speed: {speed}")
            self.c.drawString(56, y - 32, f"Best for: {best}")
            self.label(56, y - 50, "My notes:", size=8)
            self.tf(f"method_notes_{name[:4]}", 110, y - 68, 410, 16, size=8)
            y -= 100

        self.nav(prev="ref_awake", nxt="ref_personalities")

    def page_ref_personalities(self):
        self.new_page("Reference: Sleep Personalities", "ref_personalities")
        self.section_header("The Six Sleep Personalities",
            "Work with your baby's temperament — not against it.", "REFERENCE", "blush")

        positions = [(M, 400), (PAGE_W//2+4, 400),
                     (M, 264), (PAGE_W//2+4, 264),
                     (M, 128), (PAGE_W//2+4, 128)]
        cw = PAGE_W//2 - M - 8

        for (name, desc, tip), (px, py) in zip(PERSONALITIES, positions):
            self.card(px, py, cw, 118, "surface", 10, stroke_color="blush", lw=0.5)
            self.c.setFillColor(P["blush"])
            self.c.roundRect(px+2, py+90, cw-4, 22, 4, fill=1, stroke=0)
            self.c.setFillColor(P["white"])
            self.c.setFont("Times-Bold", 10)
            self.c.drawString(px+12, py+95, name)
            self.txt(px+12, py+78, desc, size=9, color="muted", max_w=cw-24)
            self.txt(px+12, py+52, f"Approach: {tip}", size=8, color="cream", max_w=cw-24)
            self.label(px+12, py+12, "My observation:", size=7, color="dim")
            self.tf(f"pers_note_{name[:4]}", px+12, py+2, cw-24, 14, size=7)

        self.nav(prev="ref_methods", nxt="safe_sleep")

    def page_safe_sleep(self):
        self.new_page("Safe Sleep Checklist", "safe_sleep")
        self.section_header("Safe Sleep Checklist",
            "Run through this every night until it's muscle memory.", "SAFE SLEEP", "mint")

        self.card(M, 108, PAGE_W - 2*M, 560, "surface")

        self.c.setFillColor(P["blush_pale"])
        self.c.roundRect(M+2, 638, PAGE_W-2*M-4, 24, 6, fill=1, stroke=0)
        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Times-Italic", 10)
        self.c.drawCentredString(PAGE_W/2, 644,
            "Safe sleep is always the first priority — before any method.")

        yy = 616
        for i, item in enumerate(SAFE_SLEEP):
            self.cb(f"safe_{i}", 56, yy - 2, size=13)
            yy = self.txt(76, yy, item, size=10, color="cream", max_w=440)
            yy -= 10

        self.c.setFillColor(P["warn"])
        self.c.roundRect(M+2, 116, PAGE_W-2*M-4, 48, 6, fill=1, stroke=0)
        self.txt(PAGE_W/2, 148,
                 "Call your pediatrician if: baby has a fever, breathing seems irregular,",
                 size=9, color="cream", align="center")
        self.txt(PAGE_W/2, 132,
                 "weight gain is a concern, or you have any doubt about physical comfort.",
                 size=9, color="cream", align="center")

        self.nav(prev="ref_personalities", nxt="letter_self")

    def page_letter_self(self):
        self.new_page("Letter to Future Self", "letter_self")
        self.section_header("A Letter to Your Future Self",
            "Write it on Day 1. Read it on Day 30. You'll be surprised.", "LETTER", "lavender")

        self.card(M, 108, PAGE_W - 2*M, 556, "lav_pale")

        self.c.setFillColor(P["lavender"])
        self.c.setFont("Times-Italic", 12)
        self.c.drawString(56, PAGE_H - 174, "Dear Me — 30 days from now...")

        self.hline(56, PAGE_H - 186, PAGE_W - 56, "rule", 0.5)

        self.tf("letter_self_body", 56, 226, 490, 310, size=11, multi=True,
                tooltip="Write whatever you need your future self to know...")

        self.hline(56, 218, PAGE_W - 56, "rule", 0.5)
        self.label(56, 206, "Signed:", size=9, color="muted")
        self.tf("letter_sig",  110, 192, 200, 18, size=10)
        self.label(322, 206, "Today's date:", size=9, color="muted")
        self.tf("letter_date", 408, 192, 140, 18, size=10)

        self.c.setFillColor(P["blush_light"])
        self.c.setFont("Times-Italic", 9)
        self.c.drawCentredString(PAGE_W/2, 152,
            "Come back and read this on Day 30. The woman writing it needed you to.")

        self.nav(prev="safe_sleep", nxt="notes")

    def page_notes(self):
        for pi in range(2):
            bk = "notes" if pi == 0 else "notes_2"
            ttl = "Notes" if pi == 0 else "Notes (continued)"
            prv = "letter_self" if pi == 0 else "notes"
            nxt = "notes_2"    if pi == 0 else "cover"

            self.new_page(ttl, bk)
            self.section_header(ttl,
                "Your thoughts. Your patterns. Your observations.",
                "NOTES", "muted")

            self.card(M, 100, PAGE_W - 2*M, 560, "surface")
            yy = PAGE_H - 182
            for i in range(20):
                self.hline(56, yy, PAGE_W - 56, "rule", 0.4)
                self.tf(f"notes_{pi}_{i}", 56, yy - 18, PAGE_W - 112, 16, size=10)
                yy -= 26

            self.nav(prev=prv, nxt=nxt if pi == 0 else None)

    # ──────────────────────────────────────────────
    # BUILD
    # ──────────────────────────────────────────────

    def build(self):
        print("  Cover & front matter...")
        self.page_cover()
        self.page_toc()
        self.page_how_to()
        self.page_profile()
        self.page_promise()

        print("  30 daily spreads (60 pages)...")
        for d in range(1, 31):
            if d % 5 == 0:
                print(f"    Day {d}/30...")
            self.day_sleep_page(d)
            self.day_heart_page(d)
            # Insert weekly reflection after days 7, 14, 21, 30
            if d in (7, 14, 21, 30):
                week = d // 7
                print(f"  Week {week} reflection...")
                self.page_weekly_reflect(week)

        print("  Progress + reference pages...")
        self.page_progress()
        self.page_ref_awake()
        self.page_ref_methods()
        self.page_ref_personalities()
        self.page_safe_sleep()
        self.page_letter_self()
        self.page_notes()

        self._footer()
        self.c.save()
        print(f"\n  Saved → {os.path.abspath(self.filename)}")
        print(f"  Pages: {self.page_num}")


# ============================================================
#  AFFIRM_WEEK — one per weekly reflection
# ============================================================

AFFIRM_WEEK = [
    "The first seven days are always the hardest. You did them. They are done.",
    "Patterns are emerging. Trust what the data is showing you.",
    "Three weeks in. This is not luck. This is consistency. This is you.",
    "A month. You held this together for a whole month. That is extraordinary.",
]

# ============================================================
#  ENTRY POINT
# ============================================================

if __name__ == "__main__":
    output = "Exhausted_Mum_Survival_Journal.pdf"
    print(f"\nBuilding: {output}")
    print("=" * 48)
    MumJournalPDF(output).build()
    print("=" * 48)
    print("Done. Open the PDF in Adobe Acrobat, GoodNotes, or any")
    print("fillable-PDF viewer to use all interactive fields.")
