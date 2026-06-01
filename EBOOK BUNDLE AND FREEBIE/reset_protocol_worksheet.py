"""
The Reset Protocol Worksheet (PowerPoint Premium)
"Sleep, Baby. Please." by Six & Thriving (2026)
─────────────────────────────────────────────────────────────────────
5-page premium freebie for moms who tried before and gave up.

Pages:
  1  Cover — "You're not starting from zero."
  2  Letter — Why most attempts fail (it's not what you think)
  3  Step 1: Diagnose the root cause (5 most common reasons)
  4  Steps 2–5: The full reset + 5-night tracker
  5  CTA — Get the full troubleshooting chapter

Run: python reset_protocol_worksheet.py
"""

import os
from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from _brand import (
    NAVY, NAVY_MID, NAVY_LITE, GOLD, GOLD_LITE, CREAM, CREAM_MID, WHITE,
    TEAL, SLATE, SLATE_LITE, RUST, GREEN_DK, AMBER, AMBER_LT, BLUE_LT, GREEN_LT,
    PURPLE,
    FONT_HEADING, FONT_BODY, SW, SH,
    bg, shp, txt, mtxt, gbar, header, footer, dark_footer, callout,
    cta_box, cover_decoration,
)

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "Reset_Protocol_Worksheet.pptx")


def p1_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    shp(slide, Cm(15.5), Cm(2.5), Cm(3.5), Cm(3.5), GOLD, MSO_SHAPE.OVAL)
    txt(slide, Cm(15.5), Cm(3.2), Cm(3.5), Cm(0.9),
        "FREE", Pt(16), NAVY, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(15.5), Cm(4.2), Cm(3.5), Cm(0.7),
        "RESET", Pt(9), NAVY, b=True, al=PP_ALIGN.CENTER)

    txt(slide, Cm(2), Cm(4.5), Cm(13), Cm(0.7),
        "FROM CHAPTER 7 OF SLEEP, BABY. PLEASE.",
        Pt(9), GOLD, b=True)
    gbar(slide, Cm(2), Cm(5.3), Cm(7))

    txt(slide, Cm(2), Cm(8), Cm(17), Cm(2.5),
        "The Reset", Pt(48), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(11), Cm(17), Cm(2.5),
        "Protocol", Pt(48), GOLD, b=True, i=True, fn=FONT_HEADING)

    gbar(slide, Cm(2), Cm(14.3), Cm(7))
    shp(slide, Cm(5.3), Cm(14.15), Cm(0.4), Cm(0.4), GOLD, MSO_SHAPE.OVAL)

    mtxt(slide, Cm(2), Cm(15.2), Cm(17), Cm(2.5), [
        {"t": "For the mom who tried before",
         "sz": Pt(13), "c": CREAM_MID, "sa": Pt(4)},
        {"t": "and watched it fall apart by Night 4.",
         "sz": Pt(13), "c": CREAM_MID},
    ])

    bullets = [
        "✦  The 5 most common reasons sleep training fails",
        "✦  The diagnostic that tells you which one it was",
        "✦  The 5-step reset + 5-night tracker (printable)",
    ]
    paras = [{"t": b, "sz": Pt(11), "c": GOLD_LITE, "sa": Pt(8)} for b in bullets]
    mtxt(slide, Cm(2), Cm(18.5), Cm(17), Cm(5), paras)

    gbar(slide, Cm(2), Cm(24), Cm(7))
    txt(slide, Cm(2), Cm(24.5), Cm(17), Cm(1),
        "SIX  &  THRIVING", Pt(16), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(25.7), Cm(17), Cm(0.8),
        "Mother of Six — I've Restarted Twice Myself",
        Pt(11), GOLD_LITE, i=True)

    txt(slide, Cm(0), Cm(28.5), SW, Cm(0.6),
        "www.sixandthriving.com", Pt(9), GOLD, al=PP_ALIGN.CENTER)


def p2_letter(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Why It Failed Last Time")
    footer(slide, 2)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "BEFORE WE FIX IT — A FEW WORDS",
        Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.2), Cm(17), Cm(2.5),
        "You're not starting\nfrom zero.",
        Pt(28), NAVY, b=True, fn=FONT_HEADING)
    gbar(slide, Cm(2), Cm(7.2), Cm(3))

    body = [
        {"t": "If you're reading this, you've tried sleep training before. You read a book. You started a method. You held the line for 2 nights, maybe 3. Then something happened — and the wheels came off.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(10)},
        {"t": "Here's what I want you to know first:",
         "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(10)},
        {"t": "You did not fail. The plan failed YOU. There's a difference.",
         "sz": Pt(13), "c": GOLD, "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(8), Cm(17), Cm(7), body)

    # Pull quote
    shp(slide, Cm(2), Cm(15.5), Cm(17), Cm(3.2), NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
    shp(slide, Cm(2), Cm(15.5), Cm(0.2), Cm(3.2), GOLD, MSO_SHAPE.RECTANGLE)
    mtxt(slide, Cm(2.6), Cm(15.8), Cm(16), Cm(2.7), [
        {"t": '"You are not starting from zero.', "sz": Pt(15), "c": GOLD_LITE,
         "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(2)},
        {"t": "You are starting from experience.", "sz": Pt(15), "c": GOLD_LITE,
         "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": 'You know what didn\'t work. That is data. That is power."',
         "sz": Pt(11), "c": CREAM, "i": True},
    ])

    closing = [
        {"t": "I've watched hundreds of moms restart sleep training. The ones who succeed do ONE thing differently:",
         "sz": Pt(11), "c": SLATE, "sa": Pt(10)},
        {"t": "They DIAGNOSE before they fix. They figure out which of the 5 things actually broke last time — and they target THAT one.",
         "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(10)},
        {"t": "That's what this worksheet is. The diagnostic, then the fix. Use it tonight.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(19.5), Cm(17), Cm(6), closing)

    mtxt(slide, Cm(2), Cm(25.5), Cm(17), Cm(1.5), [
        {"t": "With love and solidarity,", "sz": Pt(10), "c": SLATE, "i": True, "sa": Pt(4)},
        {"t": "— Six & Thriving", "sz": Pt(11), "c": GOLD, "b": True, "fn": FONT_HEADING},
    ])


def p3_diagnose(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Step 1: Diagnose")
    footer(slide, 3)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "STEP 1 OF THE PROTOCOL", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "What Actually Broke?", Pt(24), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "Tick the ONE that sounds most like your last attempt.",
        Pt(11), GOLD, i=True)

    # 5 root cause cards — the user can tick by hand on the printed version
    causes = [
        ("01", "Sleep Association",
         "Baby was still falling asleep nursing, rocking, or with a bottle.",
         "If you didn't move feed-to-sleep BEFORE training, this was your culprit.",
         NAVY),
        ("02", "Wrong Timing",
         "Awake windows were too short or too long. Bedtime was off.",
         "Symptom: settling took >30 min. Or 'won't go down at 7pm.'",
         AMBER),
        ("03", "Environment",
         "Room not dark enough. Too warm/cold. Sound machine too quiet/loud.",
         "Symptom: short naps. Wakes between cycles. The 5am party.",
         TEAL),
        ("04", "Inconsistency",
         "You responded one way Monday, another way Wednesday.",
         "The #1 reason sleep training fails. Even gentle methods need 100% consistency.",
         RUST),
        ("05", "Partner Misalignment",
         "One of you held the line. The other caved at 2am.",
         "Baby learns: if I escalate, the other parent comes in. Crying gets WORSE.",
         PURPLE),
    ]
    y = Cm(6.4)
    for num, title, desc, fix_hint, color in causes:
        card = shp(slide, Cm(2), y, Cm(17), Cm(3.6), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        # Color stripe
        shp(slide, Cm(2), y, Cm(0.25), Cm(3.6), color, MSO_SHAPE.RECTANGLE)
        # Number
        shp(slide, Cm(2.6), y + Cm(0.5), Cm(1.5), Cm(1.5), color, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.6), y + Cm(0.6), Cm(1.5), Cm(1.3),
            num, Pt(12), WHITE, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
            fn=FONT_HEADING)
        # Checkbox to tick
        chk = shp(slide, Cm(17), y + Cm(0.7), Cm(1.2), Cm(1.2), WHITE, MSO_SHAPE.RECTANGLE)
        chk.line.color.rgb = color
        chk.line.width = Pt(1.5)
        # Title
        txt(slide, Cm(4.5), y + Cm(0.4), Cm(12.5), Cm(0.6),
            title, Pt(13), NAVY, b=True, fn=FONT_HEADING)
        # Desc
        txt(slide, Cm(4.5), y + Cm(1.2), Cm(12.5), Cm(0.7),
            desc, Pt(10), SLATE, b=True)
        # Fix hint (gold italic)
        txt(slide, Cm(4.5), y + Cm(2.1), Cm(12.5), Cm(1.2),
            fix_hint, Pt(9.5), color, i=True)
        y += Cm(3.8)

    # Bottom note
    callout(slide, Cm(25.5),
            "ONLY ONE.",
            "If you tick more than one — that's normal. But focus on the BIGGEST one. Fix that, and the others often resolve.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(2), text_color=NAVY)


def p4_steps_2_to_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Steps 2–5: The Reset")
    footer(slide, 4)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "THE FULL PROTOCOL", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "Now Fix It — In 5 Nights",
        Pt(24), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "Five steps. Five nights. Targeted at YOUR culprit from page 3.",
        Pt(11), GOLD, i=True)

    steps = [
        ("2", "FIX THE ENVIRONMENT FIRST",
         "Free, fast, no behavior change. Blackout curtains. White noise on. Room at 68–72°F. Do this BEFORE bedtime."),
        ("3", "RESET THE ROUTINE",
         "Same order. Every night. Bath → lotion → pyjamas → feed → song → crib AWAKE. Strip out the 'extras' that crept in last time."),
        ("4", "COMMIT TO 5 NIGHTS",
         "Five consecutive nights. Same response every time. Write your wait time and your script BEFORE the night starts. No deviations."),
        ("5", "TRACK & COMPARE",
         "Note total settle time + number of wakes each morning. By Night 4 you'll see the trend. By Night 5 you'll see the win."),
    ]
    y = Cm(6.4)
    for num, title, body in steps:
        card = shp(slide, Cm(2), y, Cm(17), Cm(2.8), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        shp(slide, Cm(2.4), y + Cm(0.6), Cm(1.6), Cm(1.6), TEAL, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.4), y + Cm(0.7), Cm(1.6), Cm(1.4),
            num, Pt(15), WHITE, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
            fn=FONT_HEADING)
        txt(slide, Cm(4.5), y + Cm(0.4), Cm(14), Cm(0.7),
            title, Pt(11), NAVY, b=True)
        txt(slide, Cm(4.5), y + Cm(1.3), Cm(14), Cm(1.2),
            body, Pt(9.5), SLATE)
        y += Cm(3)

    # 5-Night Tracker (printable grid)
    tracker_y = Cm(18.7)
    txt(slide, Cm(2), tracker_y, Cm(17), Cm(0.7),
        "Your 5-Night Reset Tracker",
        Pt(13), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), tracker_y + Cm(0.8), Cm(17), Cm(0.5),
        "Print this. Fill it in each morning. Keep it on the fridge.",
        Pt(9), GOLD, i=True)

    # Header row
    cols = ["Night", "Date", "Time to Settle", "Number of Wakes", "Notes"]
    col_w = [Cm(2), Cm(2.5), Cm(3.2), Cm(3.3), Cm(6)]
    th_y = tracker_y + Cm(1.7)
    shp(slide, Cm(2), th_y, Cm(17), Cm(0.9), NAVY, MSO_SHAPE.RECTANGLE)
    x = Cm(2)
    for col, w in zip(cols, col_w):
        txt(slide, x, th_y + Cm(0.2), w, Cm(0.6),
            col, Pt(8.5), WHITE, b=True, al=PP_ALIGN.CENTER)
        x += w
    # 5 rows
    ry = th_y + Cm(0.9)
    for n in range(1, 6):
        bgc = WHITE if n % 2 == 1 else CREAM_MID
        row = shp(slide, Cm(2), ry, Cm(17), Cm(1.1), bgc, MSO_SHAPE.RECTANGLE)
        row.line.color.rgb = CREAM_MID
        row.line.width = Pt(0.3)
        # Night column
        txt(slide, Cm(2), ry + Cm(0.3), col_w[0], Cm(0.6),
            f"Night {n}", Pt(9.5), NAVY, b=True, al=PP_ALIGN.CENTER)
        ry += Cm(1.1)


def p5_cta(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    txt(slide, Cm(2), Cm(3), Cm(17), Cm(0.6),
        "ONE LAST THING — IF YOU WANT THE FULL PROTOCOL",
        Pt(9), GOLD, b=True, al=PP_ALIGN.CENTER)

    txt(slide, Cm(2), Cm(5.5), Cm(17), Cm(2.5),
        "This time?",
        Pt(40), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(8), Cm(17), Cm(2.5),
        "Make it stick.",
        Pt(40), GOLD, b=True, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    gbar(slide, Cm(8.5), Cm(11), Cm(4))

    body = [
        {"t": "The full book has the entire troubleshooting chapter — including how to handle illness, regressions, daycare disruption, sleep regressions at 4/8/12/18 months, and the night-by-night roadmap for what to expect during your reset.",
         "sz": Pt(11), "c": CREAM_MID, "sa": Pt(8), "al": PP_ALIGN.CENTER},
        {"t": "Plus the Six Sleep Personalities chapter, so you can match the method to YOUR baby — not the one in someone else's book.",
         "sz": Pt(11), "c": CREAM_MID, "sa": Pt(8), "al": PP_ALIGN.CENTER},
        {"t": "This time, you have the full picture.",
         "sz": Pt(13), "c": GOLD_LITE, "i": True, "fn": FONT_HEADING, "al": PP_ALIGN.CENTER},
    ]
    mtxt(slide, Cm(2), Cm(11.8), Cm(17), Cm(7), body)

    cta_box(slide, Cm(19.5),
            "Want the full plan?",
            "Sleep, Baby. Please. — All 15 chapters. 59 pages. $19.",
            "GET THE BOOK  →  $19",
            "www.sixandthriving.com")

    txt(slide, Cm(2), Cm(26.5), Cm(17), Cm(0.6),
        "Sleep is coming. For both of you.",
        Pt(11), GOLD_LITE, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(27.2), Cm(17), Cm(0.5),
        "— Six & Thriving",
        Pt(10), GOLD, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    dark_footer(slide, 5)


def build():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH

    print()
    print("  ╔════════════════════════════════════════════════╗")
    print("  ║  Reset Protocol Worksheet — PREMIUM v2 (.pptx) ║")
    print("  ╚════════════════════════════════════════════════╝")
    print()

    pages = [
        ("Cover — You're not starting from zero", p1_cover),
        ("Letter — Why it failed last time", p2_letter),
        ("Step 1 — Diagnose the root cause", p3_diagnose),
        ("Steps 2–5 + 5-Night Tracker", p4_steps_2_to_5),
        ("CTA — Get the full chapter", p5_cta),
    ]
    for name, fn in pages:
        print(f"  ✓ {name}")
        fn(prs)

    prs.save(OUTPUT)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print()
    print(f"  ✅ Saved: {OUTPUT}")
    print(f"  📄 Size: {size_kb:.1f} KB  •  5 pages")
    print()


if __name__ == "__main__":
    build()
