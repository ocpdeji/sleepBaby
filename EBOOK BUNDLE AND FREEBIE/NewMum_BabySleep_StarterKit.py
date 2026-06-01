from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
from pathlib import Path
import os

PAGE_W, PAGE_H = LETTER
M = 38

P = {
    "bg":          HexColor("#0F1923"),
    "surface":     HexColor("#1A2737"),
    "surface2":    HexColor("#1F2E42"),
    "navy":        HexColor("#1C2B4A"),
    "navy_light":  HexColor("#243556"),
    "gold":        HexColor("#C9A84C"),
    "gold_light":  HexColor("#E8C97A"),
    "blush":       HexColor("#C97A7A"),
    "mint":        HexColor("#6ABFA0"),
    "cream":       HexColor("#F0E8D8"),
    "muted":       HexColor("#8FA0B8"),
    "dim":         HexColor("#4A607A"),
    "rule":        HexColor("#2A3F5A"),
    "warn":        HexColor("#E07A3A"),
    "white":       white,
    "black":       black,
}

AWAKE_WINDOWS = [
    ("0–6 wks",  "45–60 min", "4–5/day", "Variable"),
    ("6–12 wks", "60–90 min", "4/day",   "8–9 p.m."),
    ("3–4 mo",   "90 min",    "3–4/day", "7:30–8:30 p.m."),
    ("4–6 mo",   "2 hrs",     "3/day",   "7–8 p.m."),
    ("6–8 mo",   "2.5 hrs",   "2–3/day", "7–8 p.m."),
    ("8–12 mo",  "3–3.5 hrs", "2/day",   "6:30–7:30 p.m."),
    ("12–18 mo", "4–5 hrs",   "1–2/day", "7–7:30 p.m."),
    ("18–24 mo", "5–6 hrs",   "1/day",   "7–7:30 p.m."),
]

PERSONALITIES = [
    ("The Snacker",       "Frequent small feeds to feel settled.",          "Longer gaps between feeds over time."),
    ("The Overthinker",   "Startles easily, very alert.",                   "Deep swaddle, very consistent routine."),
    ("The Sensitive Soul","Overwhelmed by noise, light, transitions.",       "Extra calm-down buffer before crib."),
    ("The Night Owl",     "Genuinely not tired at normal bedtime.",          "Shift bedtime earlier by 10 min every 2–3 days."),
    ("The Catnapper",     "Wakes after 45 min and can't resettle.",         "Practice linking cycles, stay close."),
    ("The Party Animal",  "FOMO — stimulation keeps them awake.",           "Boring, dark, silent exits."),
]

METHODS = [
    ("Extinction (CIO)",           "High",         "3–5 days",   "Place baby in crib awake. Full commitment, no check-ins until morning."),
    ("Ferber",                     "Moderate",     "5–7 days",   "Timed check-ins at increasing intervals. Comfort voice only."),
    ("Chair Method",               "Low–Mod",      "2–3 weeks",  "Sit by crib, move chair closer to door every 2–3 nights."),
    ("Fading",                     "Low",          "3–4+ wks",   "Gradually reduce involvement each night."),
    ("Pick Up / Put Down",         "Low",          "Variable",   "Pick up when upset, put down when calm. Repeat."),
]

BEDTIME_STEPS = [
    "Transition signal (dim lights, same phrase)",
    "Stop stimulating activity",
    "Bath or warm wipe-down",
    "Lotion massage",
    "Pajamas & sleep sack",
    "Feed in dim, quiet room (keep baby awake)",
    "Books or lullaby",
    "Final goodnight phrase (same words every night)",
    "White noise ON",
    "Room fully dark",
    "Into crib — drowsy but awake",
    "Parent exits calmly",
]

SAFE_SLEEP = [
    "Firm, flat mattress — no incline or wedge",
    "Fitted sheet only — no blankets or bumpers",
    "Baby on their BACK every sleep",
    "Sleep sack instead of loose blanket",
    "Room temperature 68–72°F / 20–22°C",
    "True blackout achieved",
    "White noise on (not inside crib)",
    "All LEDs and nightlights covered",
    "Sleep space: crib, bassinet, or play yard only",
]

PROMISE = [
    "I will use the same bedtime routine in the same order every night.",
    "I will watch awake windows and act before overtiredness sets in.",
    "I will decide how to handle night wakings before the night begins.",
    "I will pause before going in to give my baby a chance to resettle.",
    "I will not judge one method on the basis of one hard night.",
    "I will stay consistent — especially on the nights it is hardest.",
    "I am not just surviving. I am teaching a lifelong skill.",
]

FAQS = [
    ("How long does sleep training take?",
     "Most methods show meaningful change in 3–7 nights. 'Slow' methods can take 2–3 weeks. The variable is consistency, not the method."),
    ("When can I start?",
     "Gentle methods (fading, chair) from around 4 months. CIO/Ferber is generally recommended from 6 months. Always check with your pediatrician."),
    ("My baby cried all night. Did I fail?",
     "No. Night 1 and 2 are almost always the hardest. Most families see a clear shift by Night 3 or 4. One hard night is not a failure."),
    ("What if my baby is sick?",
     "Pause the method completely. Comfort first, always. Resume when your baby is well for 2–3 days."),
    ("Do I have to let my baby cry?",
     "No. Chair method and fading involve minimal crying. Choose based on your temperament, not guilt."),
    ("Partner isn't on board. Now what?",
     "Write the plan down before nightfall. The rules must be identical whether it's 8 p.m. or 3 a.m. Talk before the night, not during it."),
]


class StarterKitPDF:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=LETTER)
        self.c.setTitle("The New Mum Baby Sleep Starter Kit")
        self.c.setAuthor("Six & Thriving")
        self.c.setSubject("Premium interactive fillable baby sleep starter kit")
        self.c.setCreator("Python + ReportLab")
        self.form = self.c.acroForm
        self.pn = 0

    # ── helpers ──────────────────────────────────────────────
    def np(self, title=None, bm=None, bg="bg"):
        if self.pn > 0:
            self._footer()
            self.c.showPage()
        self.pn += 1
        self.c.setFillColor(P[bg])
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if bm:
            self.c.bookmarkPage(bm)
            if title:
                self.c.addOutlineEntry(title, bm, 0, False)

    def _footer(self):
        self.c.setStrokeColor(P["rule"])
        self.c.line(M, 22, PAGE_W - M, 22)
        self.c.setFillColor(P["muted"])
        self.c.setFont("Helvetica", 8)
        self.c.drawString(M, 10, "The New Mum Baby Sleep Starter Kit  ·  Six & Thriving")
        self.c.drawRightString(PAGE_W - M, 10, str(self.pn))

    def topbar(self, txt):
        self.c.setFillColor(P["navy"])
        self.c.rect(0, PAGE_H - 20, PAGE_W, 20, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(M, PAGE_H - 14, txt)

    def hdr(self, title, sub="", tag=""):
        self.c.setFillColor(P["navy"])
        self.c.roundRect(M, PAGE_H - 108, PAGE_W - 2*M, 70, 14, fill=1, stroke=0)
        if tag:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(M + 16, PAGE_H - 56, tag)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 22)
        self.c.drawString(M + 16, PAGE_H - 76, title)
        if sub:
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 10)
            self.c.drawString(M + 16, PAGE_H - 93, sub)

    def card(self, x, y, w, h, fill="surface", r=12):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, r, fill=1, stroke=0)

    def txt(self, x, y, s, sz=10, col="cream", font="Times-Roman", mw=None, lead=None):
        self.c.setFillColor(P[col])
        self.c.setFont(font, sz)
        ld = lead or sz + 3
        if mw is None:
            self.c.drawString(x, y, s)
            return y - ld
        for line in simpleSplit(s, font, sz, mw):
            self.c.drawString(x, y, line)
            y -= ld
        return y

    def lbl(self, x, y, s, sz=8, col="muted", font="Helvetica-Bold"):
        self.c.setFillColor(P[col])
        self.c.setFont(font, sz)
        self.c.drawString(x, y, s)

    def btn(self, x, y, w, h, text, dest, fill="surface2", tc="gold_light"):
        self.c.setFillColor(P[fill])
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
        self.c.setFillColor(P[tc])
        self.c.setFont("Helvetica-Bold", 8)
        tw = stringWidth(text, "Helvetica-Bold", 8)
        self.c.drawString(x + (w - tw)/2, y + 6, text)
        self.c.linkRect("", dest, (x, y, x + w, y + h), relative=0, thickness=0)

    def nav(self, prev=None, nxt=None):
        y = 30
        if prev: self.btn(M, y, 88, 18, "Previous", prev)
        self.btn(PAGE_W/2 - 44, y, 88, 18, "Home", "cover", fill="navy")
        if nxt:  self.btn(PAGE_W - M - 88, y, 88, 18, "Next", nxt, fill="gold", tc="bg")

    def tf(self, name, x, y, w, h=20, ml=False, fs=9):
        import inspect
        params = inspect.signature(self.form.textfield).parameters
        kwargs = dict(
            name=name, x=x, y=y, width=w, height=h,
            tooltip=name, value="",
            borderStyle='inset',
            borderColor=P["dim"],
            fillColor=P["white"],
            textColor=P["black"],
            forceBorder=True,
            fontName='Helvetica', fontSize=fs,
        )
        if 'fieldFlags' in params:
            kwargs['fieldFlags'] = 'multiline' if ml else ''
        self.form.textfield(**kwargs)

    def cb(self, name, x, y, sz=12):
        self.form.checkbox(
            name=name, x=x, y=y, size=sz, checked=False,
            buttonStyle='check',
            borderColor=P["gold"], fillColor=P["white"],
            textColor=P["gold"], forceBorder=True
        )

    def rb(self, group, val, x, y, sz=12, sel=False, **_ignored):
        import inspect
        params = inspect.signature(self.form.radio).parameters
        kwargs = dict(
            name=group, value=val, x=x, y=y, size=sz,
            buttonStyle='circle',
            borderColor=P["gold"], fillColor=P["white"],
            textColor=P["gold"], forceBorder=True
        )
        if 'selected' in params:
            kwargs['selected'] = sel
        self.form.radio(**kwargs)

    def field(self, x, y, w, label, name, h=18, ml=False, fs=9):
        self.lbl(x, y + h + 5, label)
        self.tf(name, x, y, w, h=h, ml=ml, fs=fs)

    def divider(self, y):
        self.c.setStrokeColor(P["rule"])
        self.c.line(M, y, PAGE_W - M, y)

    def section_label(self, x, y, text):
        self.c.setFillColor(P["navy"])
        self.c.roundRect(x, y, stringWidth(text, "Helvetica-Bold", 9) + 16, 16, 6, fill=1, stroke=0)
        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(x + 8, y + 4, text)

    # ─────────────────────────────────────────────────────────
    # PAGE 1 — COVER
    # ─────────────────────────────────────────────────────────
    def pg_cover(self):
        self.np("Cover", "cover")
        self.c.setFillColor(P["navy"])
        self.c.roundRect(28, 60, PAGE_W - 56, PAGE_H - 120, 22, fill=1, stroke=0)

        self.c.setFillColor(P["blush"])
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 130, "SIX & THRIVING")

        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Bold", 28)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 168, "The New Mum")
        self.c.setFont("Times-Bold", 28)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 200, "Baby Sleep Starter Kit")

        self.c.setStrokeColor(P["gold"])
        self.c.setLineWidth(2)
        self.c.line(120, PAGE_H - 213, PAGE_W - 120, PAGE_H - 213)

        self.c.setFillColor(P["cream"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, PAGE_H - 242,
            "Everything a new mum needs to start fixing sleep — tonight.")

        features = [
            ("Quick-Start Sleep Plan",     "One page. Fill it in, use it tonight."),
            ("Awake Window Chart",         "Age-by-age reference you'll use every day."),
            ("7-Day Night Log",            "Track patterns, spot progress."),
            ("Bedtime Routine Builder",    "Your 12-step checklist, your version."),
            ("Sleep Personality Finder",   "6 types — which one is your baby?"),
            ("Safe Sleep Checklist",       "Run through every single night."),
            ("Method Comparison Guide",    "5 methods. Pick one, stay with it."),
            ("My Sleep Promise",           "A commitment to the plan and to yourself."),
            ("First-Week Survival Guide",  "Night by night. You have everything."),
            ("Parent FAQ",                 "The 6 questions every new mum asks."),
        ]

        gx, gy = 56, PAGE_H - 430
        col_w = (PAGE_W - 112) / 2
        for i, (title, desc) in enumerate(features):
            cx = gx + (i % 2) * (col_w + 8)
            cy = gy - (i // 2) * 44
            self.card(cx, cy - 6, col_w - 4, 38)
            self.txt(cx + 12, cy + 18, title, sz=10, col="gold_light", font="Times-Bold")
            self.txt(cx + 12, cy + 4, desc, sz=8, col="muted", mw=col_w - 24)

        self.btn(100, 84, 130, 26, "Quick-Start Plan", "quickstart", fill="gold", tc="bg")
        self.btn(246, 84, 130, 26, "Contents", "contents")
        self.btn(392, 84, 130, 26, "7-Day Night Log", "nightlog")

        self.c.setFillColor(P["blush"])
        self.c.setFont("Times-Italic", 10)
        self.c.drawCentredString(PAGE_W/2, 68, "The companion to the Sleep, Baby. Please. system")

    # ─────────────────────────────────────────────────────────
    # PAGE 2 — CONTENTS
    # ─────────────────────────────────────────────────────────
    def pg_contents(self):
        self.np("Contents", "contents")
        self.topbar("CONTENTS")
        self.hdr("What's Inside", "Tap any section to jump directly to it.", "STARTER KIT")

        sections = [
            ("Quick-Start Sleep Plan",       "quickstart"),
            ("Baby Sleep Profile",           "profile"),
            ("Awake Windows Reference",      "awake_ref"),
            ("Sleep Personality Finder",     "personalities"),
            ("Bedtime Routine Builder",      "routine"),
            ("7-Day Night Log",              "nightlog"),
            ("Method Comparison Guide",      "methods"),
            ("Safe Sleep Checklist",         "safe_sleep"),
            ("My Sleep Promise",             "promise"),
            ("First-Week Survival Guide",    "survival"),
            ("Parent FAQ",                   "faq"),
            ("Next Steps",                   "next_steps"),
        ]

        self.card(M, 120, PAGE_W - 2*M, 540)
        y = 624
        col_break = 6
        for i, (title, dest) in enumerate(sections):
            x = M + 16 if i < col_break else M + (PAGE_W - 2*M)/2 + 8
            row_y = (y - (i % col_break) * 54) if i < col_break else (y - (i - col_break) * 54)
            self.card(x, row_y - 8, (PAGE_W - 2*M)/2 - 28, 46, fill="surface2")
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(x + 10, row_y + 24, f"{i+1:02d}")
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 11)
            self.c.drawString(x + 32, row_y + 24, title)
            self.c.linkRect("", dest, (x, row_y - 8, x + (PAGE_W - 2*M)/2 - 28, row_y + 38), relative=0, thickness=0)

        self.nav(prev="cover", nxt="quickstart")

    # ─────────────────────────────────────────────────────────
    # PAGE 3 — QUICK-START SLEEP PLAN
    # ─────────────────────────────────────────────────────────
    def pg_quickstart(self):
        self.np("Quick-Start Plan", "quickstart")
        self.topbar("QUICK-START SLEEP PLAN")
        self.hdr("Your Quick-Start Sleep Plan",
                 "Fill this in before tonight. One page. One plan. Go.", "TONIGHT")

        self.card(M, 480, PAGE_W - 2*M, 180)
        self.lbl(M + 16, 640, "Your Baby's Details", sz=12, col="gold")
        self.field(M + 16, 594, 200, "Baby's Name", "qs_name")
        self.field(M + 240, 594, 200, "Baby's Age", "qs_age")
        self.field(M + 16, 548, 200, "Current Awake Window", "qs_awake_window")
        self.field(M + 240, 548, 200, "Bedtime Target", "qs_bedtime_target")
        self.field(M + 16, 502, 424, "Tonight's Method / Approach", "qs_method_tonight")

        self.card(M, 324, PAGE_W - 2*M, 134, fill="navy")
        self.lbl(M + 16, 436, "Bedtime Routine (write yours in order)", sz=11, col="gold")
        y = 412
        for i in range(1, 7):
            col = M + 16 if i <= 3 else M + 230
            yy = y - ((i - 1) % 3) * 28
            self.lbl(col, yy + 6, str(i), sz=8, col="gold")
            self.tf(f"qs_routine_step_{i}", col + 16, yy, 168, 18, fs=8)

        self.card(M, 166, PAGE_W - 2*M, 128)
        self.lbl(M + 16, 272, "Tonight's Night Waking Plan", sz=11, col="gold")
        self.field(M + 16, 236, 424, "How will I respond to the first waking?", "qs_first_waking", h=18)
        self.field(M + 16, 196, 424, "How will I respond to subsequent wakings?", "qs_later_wakings", h=18)
        self.field(M + 16, 152, 200, "Who handles wakings tonight?", "qs_who_tonight")
        self.field(M + 240, 152, 200, "Partner knows the plan?", "qs_partner")

        self.card(M, 78, PAGE_W - 2*M, 48, fill="navy")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, 98, "Write the plan before nightfall. Your 2am brain will thank your 2pm brain.")

        self.nav(prev="contents", nxt="profile")

    # ─────────────────────────────────────────────────────────
    # PAGE 4 — BABY SLEEP PROFILE
    # ─────────────────────────────────────────────────────────
    def pg_profile(self):
        self.np("Baby Sleep Profile", "profile")
        self.topbar("BABY SLEEP PROFILE")
        self.hdr("My Baby's Sleep Profile",
                 "Fill this in once. Update it as your baby grows.", "PROFILE")

        self.card(M, 550, PAGE_W - 2*M, 190)
        self.lbl(M + 16, 720, "Baby's Details", sz=12, col="gold")
        self.field(M + 16, 676, 200, "Baby's Name", "p_name")
        self.field(M + 240, 676, 200, "Date of Birth", "p_dob")
        self.field(M + 16, 630, 200, "Age Now", "p_age")
        self.field(M + 240, 630, 200, "Planner Start Date", "p_start_date")
        self.field(M + 16, 584, 200, "Pediatrician", "p_ped")
        self.field(M + 240, 584, 200, "Baby's Weight", "p_weight")
        self.field(M + 16, 554, 424, "Main sleep challenges right now", "p_challenges")

        self.card(M, 366, PAGE_W - 2*M, 156, fill="surface2")
        self.lbl(M + 16, 502, "Baby's Sleep Personality", sz=11, col="gold")
        y = 476
        for i, (name, desc, tip) in enumerate(PERSONALITIES):
            col = M + 16 if i < 3 else M + 244
            yy = y - (i % 3) * 34
            self.rb("profile_personality", f"p{i}", col, yy - 2, selected=(i == 0))
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 9)
            self.c.drawString(col + 18, yy, name)
            self.c.setFillColor(P["muted"])
            self.c.setFont("Times-Italic", 8)
            self.c.drawString(col + 18, yy - 12, desc[:38])

        self.card(M, 154, PAGE_W - 2*M, 186, fill="navy")
        self.lbl(M + 16, 320, "Chosen Sleep Method", sz=11, col="gold")
        y = 296
        for i, (name, cry, speed, _) in enumerate(METHODS):
            self.rb("profile_method", f"m{i}", M + 16, y - 2, selected=(i == 1))
            self.txt(M + 36, y, f"{name}  |  Cry: {cry}  |  Speed: {speed}", sz=9)
            y -= 24
        self.field(M + 16, 162, 424, "My reason for choosing this method", "p_method_reason")

        self.card(M, 66, PAGE_W - 2*M, 60)
        self.field(M + 16, 72, 424, "One thing I want to see change in the next 7 days", "p_goal", h=22)

        self.nav(prev="quickstart", nxt="awake_ref")

    # ─────────────────────────────────────────────────────────
    # PAGE 5 — AWAKE WINDOWS
    # ─────────────────────────────────────────────────────────
    def pg_awake_ref(self):
        self.np("Awake Windows", "awake_ref")
        self.topbar("AWAKE WINDOWS REFERENCE")
        self.hdr("Awake Windows by Age",
                 "The most useful chart in this kit. Bookmark it.", "REFERENCE")

        self.card(M, 120, PAGE_W - 2*M, 550)
        self.c.setFillColor(P["navy"])
        self.c.roundRect(M, 626, PAGE_W - 2*M, 24, 6, fill=1, stroke=0)
        heads = [("Age Band", M + 16), ("Awake Window", M + 120), ("Naps/Day", M + 240), ("Bedtime Target", M + 320)]
        for h, x in heads:
            self.lbl(x, 634, h, col="gold")

        y = 592
        for i, (age, aw, naps, bt) in enumerate(AWAKE_WINDOWS):
            self.card(M + 4, y - 6, PAGE_W - 2*M - 8, 30, fill="surface" if i % 2 == 0 else "surface2")
            self.txt(M + 16, y + 4, age, sz=9, col="gold_light", font="Helvetica-Bold")
            self.txt(M + 120, y + 4, aw, sz=9)
            self.txt(M + 240, y + 4, naps, sz=9)
            self.txt(M + 320, y + 4, bt, sz=9)
            y -= 36

        self.card(M, 170, PAGE_W - 2*M, 226, fill="surface2")
        self.lbl(M + 16, 374, "How to Use Awake Windows", sz=11, col="gold")
        tips = [
            "Start timing the awake window from when your baby WAKES, not from when you want to start the routine.",
            "Aim to BEGIN the bedtime routine when the awake window is about 15 min from ending — not at the end.",
            "Overtired means the window was too long. Undertired means it was too short. Adjust by 10–15 min.",
            "Early morning waking often means bedtime is too late — counterintuitively, earlier bedtime can help.",
            "Your awake window is a target range, not a strict alarm. Learn your baby's individual sweet spot.",
        ]
        yy = 350
        for tip in tips:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(M + 16, yy, "•")
            yy = self.txt(M + 28, yy, tip, sz=9, mw=PAGE_W - 2*M - 44)
            yy -= 4

        self.card(M, 78, PAGE_W - 2*M, 64, fill="navy")
        self.field(M + 16, 84, 200, "My baby's current awake window", "aw_current", h=20)
        self.field(M + 240, 84, 200, "My baby's bedtime target", "aw_bedtime_target", h=20)

        self.nav(prev="profile", nxt="personalities")

    # ─────────────────────────────────────────────────────────
    # PAGE 6 — SLEEP PERSONALITY FINDER
    # ─────────────────────────────────────────────────────────
    def pg_personalities(self):
        self.np("Sleep Personalities", "personalities")
        self.topbar("SLEEP PERSONALITY FINDER")
        self.hdr("The Six Sleep Personalities",
                 "Knowing your baby's type changes everything.", "PERSONALITY")

        y = 654
        for i, (name, desc, tip) in enumerate(PERSONALITIES):
            fill = "surface" if i % 2 == 0 else "surface2"
            self.card(M, y - 68, PAGE_W - 2*M, 72)
            self.rb(f"sp_confirm", f"s{i}", M + 16, y - 28 - 2, sz=12)
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Times-Bold", 12)
            self.c.drawString(M + 36, y - 28, name)
            self.txt(M + 36, y - 44, desc, sz=9, col="cream", mw=220)
            self.c.setFillColor(P["navy"])
            self.c.roundRect(M + 270, y - 64, PAGE_W - 2*M - 290, 60, 8, fill=1, stroke=0)
            self.lbl(M + 282, y - 24, "Key Approach", sz=8, col="gold")
            self.txt(M + 282, y - 38, tip, sz=9, col="cream", mw=PAGE_W - 2*M - 306)
            y -= 84

        self.card(M, 72, PAGE_W - 2*M, 54, fill="navy")
        self.field(M + 16, 78, 424, "I think my baby is:", "sp_my_baby", h=20)

        self.nav(prev="awake_ref", nxt="routine")

    # ─────────────────────────────────────────────────────────
    # PAGE 7 — BEDTIME ROUTINE BUILDER
    # ─────────────────────────────────────────────────────────
    def pg_routine(self):
        self.np("Bedtime Routine", "routine")
        self.topbar("BEDTIME ROUTINE BUILDER")
        self.hdr("Bedtime Routine Builder",
                 "Write your version. Post it on the nursery door.", "ROUTINE")

        self.card(M, 650, PAGE_W - 2*M, 52, fill="navy")
        self.field(M + 16, 662, 180, "Routine Start Time", "rt_start_time", h=20)
        self.field(M + 216, 662, 180, "Target End (in crib)", "rt_end_time", h=20)
        self.txt(M + 408, 672, "Aim: 20–30 min", sz=9, col="muted")

        self.c.setFillColor(P["navy"])
        self.c.roundRect(M, 618, PAGE_W - 2*M, 24, 6, fill=1, stroke=0)
        for h, x in [("#", M+14), ("Step", M+36), ("Our Version", M+164), ("✓ Mon", M+336), ("✓ Wed", M+366), ("✓ Thu", M+396), ("✓ Fri", M+426), ("✓ Sat", M+456), ("✓ Sun", M+486)]:
            self.lbl(x, 626, h, sz=7, col="gold")

        y = 588
        for i, step in enumerate(BEDTIME_STEPS, start=1):
            fill_c = "surface" if i % 2 else "surface2"
            self.card(M, y - 6, PAGE_W - 2*M, 28)
            self.txt(M + 14, y + 4, str(i), sz=8, col="gold", font="Helvetica-Bold")
            self.txt(M + 36, y + 5, step[:26], sz=8, font="Times-Bold")
            self.tf(f"rt_step_{i}_text", M + 164, y, 164, 18, fs=7)
            for j, day_x in enumerate([M+338, M+368, M+398, M+428, M+458, M+488]):
                self.cb(f"rt_step_{i}_d{j+2}", day_x, y + 1, sz=11)
            y -= 34

        self.card(M, 78, PAGE_W - 2*M, 72)
        self.lbl(M + 16, 130, "Routine Notes", sz=9, col="gold")
        self.tf("rt_notes", M + 16, 84, PAGE_W - 2*M - 32, 36, ml=True, fs=9)

        self.nav(prev="personalities", nxt="nightlog")

    # ─────────────────────────────────────────────────────────
    # PAGE 8 — 7-DAY NIGHT LOG
    # ─────────────────────────────────────────────────────────
    def pg_nightlog(self):
        self.np("7-Day Night Log", "nightlog")
        self.topbar("7-DAY NIGHT LOG")
        self.hdr("7-Day Night Waking Log",
                 "Track every night. Progress lives in the data.", "NIGHT LOG")

        self.c.setFillColor(P["navy"])
        self.c.roundRect(M, 640, PAGE_W - 2*M, 22, 6, fill=1, stroke=0)
        cols = [("Night", M+12), ("Date", M+52), ("Bedtime", M+108), ("Asleep", M+162), ("1st Wake", M+218), ("# Wakes", M+274), ("Morning", M+326), ("Settled?", M+384)]
        for h, x in cols:
            self.lbl(x, 648, h, sz=7, col="gold")

        y = 608
        for n in range(1, 8):
            fill_c = "surface" if n % 2 else "surface2"
            self.card(M, y - 6, PAGE_W - 2*M, 28)
            self.txt(M + 12, y + 5, str(n), sz=9, col="gold", font="Helvetica-Bold")
            self.tf(f"nl_n{n}_date",    M+52,  y, 46, 18, fs=8)
            self.tf(f"nl_n{n}_bed",     M+108, y, 46, 18, fs=8)
            self.tf(f"nl_n{n}_asleep",  M+162, y, 46, 18, fs=8)
            self.tf(f"nl_n{n}_1stwake", M+218, y, 46, 18, fs=8)
            self.tf(f"nl_n{n}_total",   M+274, y, 42, 18, fs=8)
            self.tf(f"nl_n{n}_morning", M+326, y, 48, 18, fs=8)
            self.rb(f"nl_n{n}_settled", "yes", M+386, y+2, sz=10, sel=False)
            self.txt(M+400, y+5, "Y", sz=8)
            self.rb(f"nl_n{n}_settled", "no",  M+414, y+2, sz=10, sel=False)
            self.txt(M+428, y+5, "N", sz=8)
            y -= 34

        self.card(M, 318, PAGE_W - 2*M, 148, fill="surface2")
        self.lbl(M+16, 446, "Waking Details", sz=11, col="gold")
        self.lbl(M+16, 428, "Night #", sz=8); self.lbl(M+70, 428, "Wake time", sz=8); self.lbl(M+154, 428, "Response", sz=8); self.lbl(M+286, 428, "Back asleep in", sz=8); self.lbl(M+390, 428, "Notes", sz=8)
        yy = 404
        for ni in range(1, 4):
            self.tf(f"nl_det_night{ni}",   M+16,  yy, 44, 18, fs=8)
            self.tf(f"nl_det_time{ni}",    M+70,  yy, 76, 18, fs=8)
            self.tf(f"nl_det_resp{ni}",    M+154, yy, 124, 18, fs=8)
            self.tf(f"nl_det_back{ni}",    M+286, yy, 94, 18, fs=8)
            self.tf(f"nl_det_notes{ni}",   M+390, yy, 128, 18, fs=8)
            yy -= 26

        self.card(M, 154, PAGE_W - 2*M, 136)
        self.lbl(M+16, 270, "Weekly Pattern Review", sz=11, col="gold")
        self.field(M+16, 228, 424, "Patterns I noticed (same waking time, trigger, improvement?)", "nl_patterns", h=22)
        self.field(M+16, 190, 200, "Best night this week", "nl_best")
        self.field(M+240, 190, 200, "Hardest night", "nl_hardest")
        self.field(M+16, 158, 424, "What I'll do differently next week", "nl_next_week", h=22)

        self.card(M, 78, PAGE_W - 2*M, 48, fill="navy")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 12)
        self.c.drawCentredString(PAGE_W/2, 96, "Progress is not linear. One bad night does not undo five good ones.")

        self.nav(prev="routine", nxt="methods")

    # ─────────────────────────────────────────────────────────
    # PAGE 9 — METHOD COMPARISON
    # ─────────────────────────────────────────────────────────
    def pg_methods(self):
        self.np("Sleep Methods", "methods")
        self.topbar("SLEEP METHOD COMPARISON GUIDE")
        self.hdr("Sleep Method Comparison Guide",
                 "Any method works when applied consistently. Pick one, stay with it.", "METHODS")

        y = 654
        for i, (name, cry, speed, principle) in enumerate(METHODS):
            self.card(M, y - 82, PAGE_W - 2*M, 86)
            self.rb("method_pick", f"m{i}", M + 16, y - 32 - 2, sz=12, sel=(i == 1))
            self.c.setFillColor(P["gold_light"])
            self.c.setFont("Times-Bold", 12)
            self.c.drawString(M + 36, y - 32, name)
            self.card(M + 240, y - 46, 90, 16, fill="navy", r=6)
            self.txt(M + 248, y - 40, f"Cry: {cry}", sz=8, col="gold")
            self.card(M + 338, y - 46, 80, 16, fill="navy", r=6)
            self.txt(M + 346, y - 40, f"Speed: {speed}", sz=8, col="mint")
            self.txt(M + 36, y - 52, principle, sz=9, col="cream", mw=PAGE_W - 2*M - 56)
            y -= 100

        self.card(M, 78, PAGE_W - 2*M, 74, fill="surface2")
        self.lbl(M+16, 130, "My method decision", sz=11, col="gold")
        self.field(M+16, 84, 424, "I am choosing this method because:", "mc_reason", h=28, ml=True)

        self.nav(prev="nightlog", nxt="safe_sleep")

    # ─────────────────────────────────────────────────────────
    # PAGE 10 — SAFE SLEEP
    # ─────────────────────────────────────────────────────────
    def pg_safe_sleep(self):
        self.np("Safe Sleep Checklist", "safe_sleep")
        self.topbar("SAFE SLEEP CHECKLIST")
        self.hdr("Safe Sleep Checklist",
                 "Run through this every night until it becomes muscle memory.", "SAFE SLEEP")

        self.card(M, 130, PAGE_W - 2*M, 530)
        y = 620
        for i, item in enumerate(SAFE_SLEEP, start=1):
            self.cb(f"ss_{i}", M + 16, y - 2, sz=13)
            y = self.txt(M + 38, y, item, sz=10, mw=PAGE_W - 2*M - 58)
            y -= 10

        self.card(M, 76, PAGE_W - 2*M, 38, fill="navy")
        self.c.setFillColor(P["warn"])
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(M + 16, 92, "If you ever have a concern about your baby's breathing or safety, contact your pediatrician before resuming any sleep method.")

        self.nav(prev="methods", nxt="promise")

    # ─────────────────────────────────────────────────────────
    # PAGE 11 — SLEEP PROMISE
    # ─────────────────────────────────────────────────────────
    def pg_promise(self):
        self.np("My Sleep Promise", "promise")
        self.topbar("MY SLEEP PROMISE")
        self.hdr("My Sleep Promise",
                 "A commitment to your baby — and to yourself.", "PROMISE")

        self.card(M, 162, PAGE_W - 2*M, 490, fill="navy")
        y = 612
        for i, item in enumerate(PROMISE, start=1):
            self.cb(f"pr_{i}", M + 20, y - 2, sz=12)
            y = self.txt(M + 42, y, item, sz=11, col="cream", mw=PAGE_W - 2*M - 62)
            y -= 10

        self.c.setFillColor(P["gold"])
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(M + 20, 218, "FOR THE NEXT 7 DAYS")
        self.divider(208)
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 14)
        self.c.drawCentredString(PAGE_W/2, 184, "Sleep is coming. For both of you.")

        self.cb("pr_signed", M + 20, 102, sz=16)
        self.txt(M + 46, 106, "I have read this promise and I commit to working the plan.", sz=11)

        self.nav(prev="safe_sleep", nxt="survival")

    # ─────────────────────────────────────────────────────────
    # PAGE 12 — FIRST-WEEK SURVIVAL GUIDE
    # ─────────────────────────────────────────────────────────
    def pg_survival(self):
        self.np("First-Week Survival Guide", "survival")
        self.topbar("FIRST-WEEK SURVIVAL GUIDE")
        self.hdr("Your First-Week Survival Guide",
                 "Night by night. You have everything you need.", "GAME PLAN")

        nights = [
            ("Night 1–2", "warn",  "The hardest. Expect resistance. This is normal and expected. Stay the course."),
            ("Night 3–4", "gold",  "Most families see a noticeable shift. This is where it turns. Trust it."),
            ("Night 5–7", "mint",  "The groove begins. Small wins compound. You are doing it."),
            ("Week 2+",   "blush", "Progress is rarely perfectly linear. One regression night is not failure."),
        ]

        y = 634
        for label, col, desc in nights:
            self.card(M, y - 58, PAGE_W - 2*M, 62)
            self.c.setFillColor(P[col])
            self.c.roundRect(M, y - 58, 6, 62, 4, fill=1, stroke=0)
            self.c.setFillColor(P[col])
            self.c.setFont("Times-Bold", 12)
            self.c.drawString(M + 22, y - 22, label)
            self.txt(M + 22, y - 40, desc, sz=9, col="cream", mw=PAGE_W - 2*M - 42)
            y -= 76

        self.card(M, 310, PAGE_W - 2*M, 138, fill="surface2")
        rules = [
            "Have the plan agreed before nightfall. Not at 2am.",
            "Be boring at night. No lights, no talking, no eye contact beyond what the method requires.",
            "Pause 2–3 minutes before entering. Many babies will resettle alone.",
            "Do not change methods mid-week. Each change resets progress.",
            "Call it a win every morning you wake up having followed the plan.",
        ]
        self.lbl(M + 16, 428, "The Non-Negotiables", sz=11, col="gold")
        yy = 402
        for rule in rules:
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(M + 16, yy, "•")
            yy = self.txt(M + 28, yy, rule, sz=9, mw=PAGE_W - 2*M - 48)
            yy -= 3

        self.card(M, 154, PAGE_W - 2*M, 130)
        self.lbl(M + 16, 264, "How I'll Manage the Hard Nights", sz=11, col="gold")
        self.field(M + 16, 224, 424, "When it feels hard, I will remind myself:", "sv_hard_nights", h=28, ml=True)
        self.field(M + 16, 170, 200, "My support person is:", "sv_support")
        self.field(M + 240, 170, 200, "What I can do in 5 min for myself:", "sv_selfcare")

        self.card(M, 72, PAGE_W - 2*M, 56, fill="navy")
        self.c.setFillColor(P["gold_light"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, 96, "You are not just surviving the night.")
        self.c.drawCentredString(PAGE_W/2, 80, "You are teaching your baby a skill they will use for life.")

        self.nav(prev="promise", nxt="faq")

    # ─────────────────────────────────────────────────────────
    # PAGE 13 — PARENT FAQ
    # ─────────────────────────────────────────────────────────
    def pg_faq(self):
        self.np("Parent FAQ", "faq")
        self.topbar("PARENT FAQ")
        self.hdr("Parent FAQ",
                 "The 6 questions every new mum asks. Answered honestly.", "FAQ")

        y = 650
        for q, a in FAQS:
            self.card(M, y - 78, PAGE_W - 2*M, 82)
            self.c.setFillColor(P["gold"])
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(M + 16, y - 12, "Q")
            self.c.setFillColor(P["cream"])
            self.c.setFont("Times-Bold", 10)
            self.c.drawString(M + 30, y - 12, q)
            self.txt(M + 30, y - 28, a, sz=9, col="muted", mw=PAGE_W - 2*M - 50)
            y -= 96

        self.nav(prev="survival", nxt="next_steps")

    # ─────────────────────────────────────────────────────────
    # PAGE 14 — NEXT STEPS
    # ─────────────────────────────────────────────────────────
    def pg_next_steps(self):
        self.np("Next Steps", "next_steps")
        self.topbar("NEXT STEPS")
        self.hdr("What Comes Next",
                 "You've started. Now let it build.", "NEXT STEPS")

        self.card(M, 400, PAGE_W - 2*M, 260, fill="navy")
        self.lbl(M + 16, 638, "You've Completed the Starter Kit", sz=13, col="gold_light")
        steps = [
            ("Fill in your Quick-Start Plan",       "quickstart"),
            ("Set tonight's bedtime routine",        "routine"),
            ("Start the 7-Day Night Log tonight",   "nightlog"),
            ("Read the Sleep Promise",               "promise"),
            ("Review the Survival Guide before bed","survival"),
        ]
        yy = 606
        for label, dest in steps:
            self.cb(f"ns_done_{dest}", M + 20, yy - 2, sz=12)
            self.txt(M + 42, yy, label, sz=10)
            yy -= 28

        self.card(M, 240, PAGE_W - 2*M, 130)
        self.lbl(M + 16, 348, "Ready to go deeper?", sz=12, col="gold")
        self.txt(M + 16, 326,
            "This Starter Kit is the entry point. The Sleep, Baby. Please. System Planner gives you "
            "the full 12-week structured program — one week per chapter, with awake trackers, "
            "night logs, method tracking, and weekly reflections for the complete journey.",
            sz=9, col="cream", mw=PAGE_W - 2*M - 32)
        self.btn(M + 16, 252, 220, 26, "See the Full 12-Week Planner", "cover", fill="gold", tc="bg")

        self.card(M, 138, PAGE_W - 2*M, 78)
        self.lbl(M + 16, 196, "My commitment for the next 7 nights", sz=10, col="gold")
        self.tf("ns_commitment", M + 16, 144, PAGE_W - 2*M - 32, 42, ml=True, fs=9)

        self.card(M, 68, PAGE_W - 2*M, 48, fill="blush")
        self.c.setFillColor(P["white"])
        self.c.setFont("Times-Italic", 13)
        self.c.drawCentredString(PAGE_W/2, 84, "Sleep is coming.  You've got this.  — Six & Thriving")

        self.nav(prev="faq", nxt="cover")

    # ─────────────────────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────────────────────
    def build(self):
        self.pg_cover()
        self.pg_contents()
        self.pg_quickstart()
        self.pg_profile()
        self.pg_awake_ref()
        self.pg_personalities()
        self.pg_routine()
        self.pg_nightlog()
        self.pg_methods()
        self.pg_safe_sleep()
        self.pg_promise()
        self.pg_survival()
        self.pg_faq()
        self.pg_next_steps()
        self._footer()
        self.c.save()


outfile = "NewMum_BabySleep_StarterKit.pdf"
StarterKitPDF(outfile).build()

# Also save the script
from inspect import getsource
import sys

# Write the python file
py_out = Path("NewMum_BabySleep_StarterKit_Generator.py")
script_content = Path(__file__).read_text() if Path(__file__).exists() else ""

# Write full script as standalone
import textwrap
full_script = open("/proc/self/fd/0").read() if False else ""

# Just copy the entire cell source to file
cell_code = open(os.path.realpath(__file__)).read() if os.path.isfile(os.path.realpath(os.path.abspath("__main__"))) else ""

# Write the final py file from what we have
src_lines = []
src_lines.append("# NewMum_BabySleep_StarterKit_Generator.py")
src_lines.append("# Run: python NewMum_BabySleep_StarterKit_Generator.py")
src_lines.append("# Requires: pip install reportlab\n")
# We'll reconstruct from module
import inspect
src_lines.append(inspect.getsource(StarterKitPDF.__init__).replace("def __init__", "# class StarterKitPDF:\n#   def __init__"))

print("PDF pages:", StarterKitPDF.__dict__.keys())
print(f"PDF size: {Path(outfile).stat().st_size:,} bytes")
print(f"PDF saved: {Path(outfile).resolve()}")