"""
The Twins Sleep Sync Planner (PowerPoint Premium)
"Sleep, Baby. Please." by Six & Thriving (2026)
─────────────────────────────────────────────────────────────────────
5-page premium freebie for twin parents — written by a mom who has twins.

Pages:
  1  Cover — "From a mom who's lived it"
  2  Letter — Twin sleep is different. Here's the truth.
  3  The Golden Rules of Twin Sleep
  4  Today's Schedule planner (Twin A | Twin B side-by-side)
  5  CTA — Get the full Chapter 14

Run: python twins_sync_planner.py
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
                      "Twins_Sync_Planner.pptx")


def p1_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    shp(slide, Cm(15.5), Cm(2.5), Cm(3.5), Cm(3.5), GOLD, MSO_SHAPE.OVAL)
    txt(slide, Cm(15.5), Cm(3.2), Cm(3.5), Cm(0.9),
        "FREE", Pt(16), NAVY, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(15.5), Cm(4.2), Cm(3.5), Cm(0.7),
        "TWINS", Pt(9), NAVY, b=True, al=PP_ALIGN.CENTER)

    txt(slide, Cm(2), Cm(4.5), Cm(13), Cm(0.7),
        "FROM CHAPTER 14 OF SLEEP, BABY. PLEASE.",
        Pt(9), GOLD, b=True)
    gbar(slide, Cm(2), Cm(5.3), Cm(7))

    txt(slide, Cm(2), Cm(8), Cm(17), Cm(2.5),
        "Twin Sleep,", Pt(46), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(11), Cm(17), Cm(2.5),
        "Synchronised.", Pt(46), GOLD, b=True, i=True, fn=FONT_HEADING)

    gbar(slide, Cm(2), Cm(14.3), Cm(7))
    shp(slide, Cm(5.3), Cm(14.15), Cm(0.4), Cm(0.4), GOLD, MSO_SHAPE.OVAL)

    mtxt(slide, Cm(2), Cm(15.2), Cm(17), Cm(2.5), [
        {"t": "From a mom who has twins,",
         "sz": Pt(13), "c": CREAM_MID, "sa": Pt(4)},
        {"t": "and got them on the same schedule by Day 4.",
         "sz": Pt(13), "c": CREAM_MID},
    ])

    bullets = [
        "✦  The Golden Rules of twin sleep (4 of them, that's it)",
        "✦  How to sync feeds and naps from Day 1",
        "✦  Today's printable schedule planner",
    ]
    paras = [{"t": b, "sz": Pt(11), "c": GOLD_LITE, "sa": Pt(8)} for b in bullets]
    mtxt(slide, Cm(2), Cm(18.5), Cm(17), Cm(5), paras)

    gbar(slide, Cm(2), Cm(24), Cm(7))
    txt(slide, Cm(2), Cm(24.5), Cm(17), Cm(1),
        "SIX  &  THRIVING", Pt(16), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(25.7), Cm(17), Cm(0.8),
        "Mother of Six — Twins Tucked in the Middle",
        Pt(11), GOLD_LITE, i=True)

    txt(slide, Cm(0), Cm(28.5), SW, Cm(0.6),
        "www.sixandthriving.com", Pt(9), GOLD, al=PP_ALIGN.CENTER)


def p2_letter(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "A Letter")
    footer(slide, 2)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "FROM ONE TWIN MOM TO ANOTHER",
        Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.2), Cm(17), Cm(2.5),
        "I've been there.\nWith two of them.",
        Pt(28), NAVY, b=True, fn=FONT_HEADING)
    gbar(slide, Cm(2), Cm(7.3), Cm(3))

    body = [
        {"t": "Most sleep books pretend twins don't exist. The ones that do mention them say something useless like 'just follow the same plan.' That's because most sleep authors don't have twins.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(10)},
        {"t": "I do.",
         "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(10)},
        {"t": "My twins were baby #3 and #4. Born 2 minutes apart. Identical temperaments? No. Same sleep needs? Also no. One was a Snacker, the other was a Night Owl. They woke each other up. They synchronised in ways I didn't expect — and didn't synchronise where I expected they would.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(8.3), Cm(17), Cm(8), body)

    # Pull quote
    shp(slide, Cm(2), Cm(16.5), Cm(17), Cm(3.5), NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
    shp(slide, Cm(2), Cm(16.5), Cm(0.2), Cm(3.5), GOLD, MSO_SHAPE.RECTANGLE)
    mtxt(slide, Cm(2.6), Cm(16.8), Cm(16), Cm(3), [
        {"t": '"Twin sleep isn\'t harder.', "sz": Pt(15), "c": GOLD_LITE,
         "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(2)},
        {"t": "It's just different.", "sz": Pt(15), "c": GOLD_LITE,
         "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": 'And once you know the rules, two babies sleep about as easily as one."',
         "sz": Pt(11), "c": CREAM, "i": True},
    ])

    closing = [
        {"t": "I tried to sleep-train my twins on different schedules — feeding one while the other slept, then swapping. It was chaos. By Day 3 I was crying. By Day 5 I was changing the plan.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(10)},
        {"t": "What worked: synchronising EVERYTHING. When one wakes, wake the other. Feed at the same time. Nap at the same time. The Golden Rules on page 3.",
         "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(10)},
        {"t": "By Day 4, they were on the same schedule. They've been on the same schedule ever since.",
         "sz": Pt(11), "c": GOLD, "b": True, "i": True, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(20.5), Cm(17), Cm(7), closing)

    mtxt(slide, Cm(2), Cm(25.5), Cm(17), Cm(1.5), [
        {"t": "With love and solidarity,", "sz": Pt(10), "c": SLATE, "i": True, "sa": Pt(4)},
        {"t": "— Six & Thriving (Mom of twins)", "sz": Pt(11), "c": GOLD, "b": True, "fn": FONT_HEADING},
    ])


def p3_golden_rules(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "The Golden Rules")
    footer(slide, 3)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "FOUR RULES. THAT'S IT.", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "The Golden Rules of Twin Sleep",
        Pt(24), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "If you only remember four things — make them these.",
        Pt(11), GOLD, i=True)

    rules = [
        ("01", "When one wakes, wake the other.",
         "Sounds harsh. Saves your sanity. They will fight you on Day 1. By Day 3 they're synchronised — and YOU are sleeping. Trust this rule above all others."),
        ("02", "Train BOTH simultaneously.",
         "Same method. Same night. Same response time. Yes, even if one is 'easier.' Doing one twin and not the other almost always means failing both."),
        ("03", "Same room is fine.",
         "They habituate to each other's sounds within 3–5 nights — faster than you'd believe. Don't separate them unless one has a medical reason. The white noise machine does the rest."),
        ("04", "Accept they'll progress at different rates.",
         "One will sleep through by Night 5. The other might take Night 8. That's normal. Don't move the slow one to a different method. Hold the line. They'll catch up."),
    ]
    y = Cm(6.4)
    for num, title, body in rules:
        card = shp(slide, Cm(2), y, Cm(17), Cm(4.2), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        # Color stripe (gold)
        shp(slide, Cm(2), y, Cm(0.25), Cm(4.2), GOLD, MSO_SHAPE.RECTANGLE)
        # Number circle
        shp(slide, Cm(2.6), y + Cm(0.7), Cm(2), Cm(2), NAVY, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.6), y + Cm(0.9), Cm(2), Cm(1.6),
            num, Pt(20), GOLD, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
            fn=FONT_HEADING)
        # Title
        txt(slide, Cm(5.2), y + Cm(0.5), Cm(13), Cm(0.8),
            title, Pt(13), NAVY, b=True, fn=FONT_HEADING)
        gbar(slide, Cm(5.2), y + Cm(1.5), Cm(2))
        # Body
        txt(slide, Cm(5.2), y + Cm(1.8), Cm(13.3), Cm(2.2),
            body, Pt(10), SLATE)
        y += Cm(4.4)

    # Bottom callout
    callout(slide, Cm(24.5),
            "ONE TWIN GETS SICK?",
            "Pause for THAT twin only. Continue with the other. Resume the sick twin (3–5 night reset) when they recover.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(2.5), text_color=NAVY)


def p4_schedule(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Today's Schedule")
    footer(slide, 4)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "PRINTABLE PLANNER", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "Today's Synchronised Schedule",
        Pt(22), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "Print this. Fill it in each morning. Stick it on the fridge.",
        Pt(11), GOLD, i=True)

    # Header row
    label_w = Cm(4)
    twin_w = Cm(6.5)
    th_y = Cm(6.4)
    shp(slide, Cm(2), th_y, Cm(17), Cm(1), NAVY, MSO_SHAPE.RECTANGLE)
    txt(slide, Cm(2), th_y + Cm(0.25), label_w, Cm(0.6),
        "Schedule Item", Pt(10), WHITE, b=True, al=PP_ALIGN.CENTER)
    txt(slide, Cm(6), th_y + Cm(0.25), twin_w, Cm(0.6),
        "Twin A", Pt(11), GOLD, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(12.5), th_y + Cm(0.25), twin_w, Cm(0.6),
        "Twin B", Pt(11), GOLD, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    # Rows — schedule items with empty boxes for writing
    items = [
        "Wake Time",
        "Morning Feed",
        "Morning Nap",
        "Midday Feed",
        "Midday Nap",
        "Afternoon Feed",
        "Afternoon Nap",
        "Bedtime Routine",
        "Lights Out",
        "Night Wake 1",
        "Night Wake 2",
    ]
    y = th_y + Cm(1)
    for i, item in enumerate(items):
        bgc = WHITE if i % 2 == 0 else CREAM_MID
        row = shp(slide, Cm(2), y, Cm(17), Cm(1.3), bgc, MSO_SHAPE.RECTANGLE)
        row.line.color.rgb = CREAM_MID
        row.line.width = Pt(0.3)
        # Label
        txt(slide, Cm(2.3), y + Cm(0.35), label_w, Cm(0.6),
            item, Pt(10), NAVY, b=True)
        # Twin A box (gold-bordered, empty for writing)
        ta = shp(slide, Cm(6.2), y + Cm(0.2), Cm(6), Cm(0.9), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        ta.line.color.rgb = GOLD
        ta.line.width = Pt(0.8)
        # Twin B box
        tb = shp(slide, Cm(12.7), y + Cm(0.2), Cm(6), Cm(0.9), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        tb.line.color.rgb = GOLD
        tb.line.width = Pt(0.8)
        y += Cm(1.3)

    # Notes section at bottom
    notes_y = y + Cm(0.3)
    txt(slide, Cm(2), notes_y, Cm(17), Cm(0.6),
        "Notes & observations:",
        Pt(11), NAVY, b=True, fn=FONT_HEADING)
    notes_box = shp(slide, Cm(2), notes_y + Cm(0.7), Cm(17), Cm(2.5),
                    WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
    notes_box.line.color.rgb = GOLD
    notes_box.line.width = Pt(0.8)


def p5_cta(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    txt(slide, Cm(2), Cm(3), Cm(17), Cm(0.6),
        "ONE LAST THING — IF YOU WANT THE FULL TWIN PLAYBOOK",
        Pt(9), GOLD, b=True, al=PP_ALIGN.CENTER)

    txt(slide, Cm(2), Cm(5.5), Cm(17), Cm(2.5),
        "Two babies.",
        Pt(40), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(8), Cm(17), Cm(2.5),
        "One sleep system.",
        Pt(40), GOLD, b=True, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    gbar(slide, Cm(8.5), Cm(11), Cm(4))

    body = [
        {"t": "Chapter 14 of the full book covers the entire twin sleep playbook — including how to handle one twin sick while the other isn't, how to handle different temperaments, the Crib Hour technique for catnappers (very common in twins), and what to do when room-sharing isn't working.",
         "sz": Pt(11), "c": CREAM_MID, "sa": Pt(8), "al": PP_ALIGN.CENTER},
        {"t": "Plus the full 7-night plan that worked for my own twins — and hundreds of other twin families who've used it since.",
         "sz": Pt(11), "c": CREAM_MID, "sa": Pt(8), "al": PP_ALIGN.CENTER},
        {"t": "By a mom who actually has twins.",
         "sz": Pt(13), "c": GOLD_LITE, "i": True, "fn": FONT_HEADING, "al": PP_ALIGN.CENTER},
    ]
    mtxt(slide, Cm(2), Cm(11.8), Cm(17), Cm(7), body)

    cta_box(slide, Cm(19.5),
            "Want the full plan?",
            "Sleep, Baby. Please. — Including a full chapter for twin parents.",
            "GET THE BOOK  →  $19",
            "www.sixandthriving.com")

    txt(slide, Cm(2), Cm(26.5), Cm(17), Cm(0.6),
        "Sleep is coming. For all three of you.",
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
    print("  ║  Twins Sync Planner — PREMIUM v2 (.pptx)       ║")
    print("  ╚════════════════════════════════════════════════╝")
    print()

    pages = [
        ("Cover — From a mom who has twins", p1_cover),
        ("Letter — Twin sleep is different", p2_letter),
        ("The 4 Golden Rules", p3_golden_rules),
        ("Today's Schedule planner", p4_schedule),
        ("CTA — Get Chapter 14", p5_cta),
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
