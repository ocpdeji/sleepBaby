"""
The 2 AM Survival Guide (PowerPoint Premium)
"Sleep, Baby. Please." by Six & Thriving (2026)
─────────────────────────────────────────────────────────────────────
4-page emergency freebie for the moment a mom is at her breaking point.
The most emotionally charged use case in the entire bundle.

Pages:
  1  Cover — "It's 2 AM. Read this NOW."
  2  Letter — "I see you. Six times I sat in this chair."
  3  The 5-step protocol (the lifeline)
  4  "If you caved tonight" recovery + book CTA

Run: python two_am_survival_guide.py
"""

import os
from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from _brand import (
    NAVY, NAVY_MID, NAVY_LITE, GOLD, GOLD_LITE, CREAM, CREAM_MID, WHITE,
    TEAL, SLATE, SLATE_LITE, RUST, GREEN_DK, AMBER, AMBER_LT, BLUE_LT, GREEN_LT,
    RED_LT,
    FONT_HEADING, FONT_BODY, SW, SH,
    bg, shp, txt, mtxt, gbar, header, footer, dark_footer, callout,
    cta_box, cover_decoration,
)

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "2AM_Survival_Guide.pptx")


def p1_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    # Emergency badge — red instead of gold
    shp(slide, Cm(15.5), Cm(2.5), Cm(3.5), Cm(3.5), RUST, MSO_SHAPE.OVAL)
    txt(slide, Cm(15.5), Cm(3.2), Cm(3.5), Cm(0.9),
        "READ", Pt(15), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(15.5), Cm(4.2), Cm(3.5), Cm(0.7),
        "NOW", Pt(11), WHITE, b=True, al=PP_ALIGN.CENTER)

    txt(slide, Cm(2), Cm(4.5), Cm(13), Cm(0.7),
        "AN EMERGENCY GUIDE FROM SIX & THRIVING",
        Pt(9), GOLD, b=True)
    gbar(slide, Cm(2), Cm(5.3), Cm(7))

    txt(slide, Cm(2), Cm(8), Cm(17), Cm(2.5),
        "It's 2 AM.", Pt(48), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(11), Cm(17), Cm(2.5),
        "You're done.", Pt(48), GOLD, b=True, i=True, fn=FONT_HEADING)

    gbar(slide, Cm(2), Cm(14.3), Cm(7))
    shp(slide, Cm(5.3), Cm(14.15), Cm(0.4), Cm(0.4), GOLD, MSO_SHAPE.OVAL)

    mtxt(slide, Cm(2), Cm(15.2), Cm(17), Cm(2.5), [
        {"t": "Take a breath. You're not alone.",
         "sz": Pt(13), "c": CREAM_MID, "sa": Pt(4)},
        {"t": "Here's exactly what to do — in the next 60 seconds.",
         "sz": Pt(13), "c": CREAM_MID},
    ])

    bullets = [
        "✦  The 5 steps that work when nothing else does",
        "✦  What to say to yourself before you go in",
        "✦  How to recover if you caved tonight",
    ]
    paras = [{"t": b, "sz": Pt(11), "c": GOLD_LITE, "sa": Pt(8)} for b in bullets]
    mtxt(slide, Cm(2), Cm(18.5), Cm(17), Cm(5), paras)

    gbar(slide, Cm(2), Cm(24), Cm(7))
    txt(slide, Cm(2), Cm(24.5), Cm(17), Cm(1),
        "SIX  &  THRIVING", Pt(16), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(25.7), Cm(17), Cm(0.8),
        "Mother of Six — Still Here at 3 a.m.",
        Pt(11), GOLD_LITE, i=True)

    txt(slide, Cm(0), Cm(28.5), SW, Cm(0.6),
        "www.sixandthriving.com", Pt(9), GOLD, al=PP_ALIGN.CENTER)


def p2_letter(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "A Letter for Right Now")
    footer(slide, 2)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "BEFORE YOU DO ANYTHING ELSE — READ THIS",
        Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.2), Cm(17), Cm(2.5),
        "I see you.", Pt(36), NAVY, b=True, fn=FONT_HEADING)
    gbar(slide, Cm(2), Cm(7.3), Cm(3))

    body = [
        {"t": "I've sat in this chair too. Six times. With six different babies. At every hour from 11 PM to 5 AM. I have whispered the words 'please, just sleep' into the dark more times than I can count.",
         "sz": Pt(12), "c": SLATE, "sa": Pt(12)},
        {"t": "If you're reading this — your baby is awake. Or just woke. Or hasn't slept in what feels like days.",
         "sz": Pt(12), "c": SLATE, "sa": Pt(12)},
        {"t": "I want you to know three things, right now, before you do anything:",
         "sz": Pt(12), "c": NAVY, "b": True, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(8.3), Cm(17), Cm(8), body)

    # Three big calm-down truths
    truths = [
        ("01", "Your baby is safe.", "If they were not, you would know. Take this breath."),
        ("02", "You are not failing.", "You're exhausted. There is a difference. A huge one."),
        ("03", "This is solvable.", "Not by morning. But by next week. Trust me."),
    ]
    y = Cm(16.5)
    for num, title, sub in truths:
        card = shp(slide, Cm(2), y, Cm(17), Cm(2.5), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = GOLD
        card.line.width = Pt(0.8)
        # Number
        shp(slide, Cm(2.4), y + Cm(0.5), Cm(1.5), Cm(1.5), NAVY, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.4), y + Cm(0.6), Cm(1.5), Cm(1.3),
            num, Pt(13), GOLD, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
            fn=FONT_HEADING)
        txt(slide, Cm(4.3), y + Cm(0.4), Cm(14), Cm(0.7),
            title, Pt(13), NAVY, b=True, fn=FONT_HEADING)
        txt(slide, Cm(4.3), y + Cm(1.3), Cm(14), Cm(1),
            sub, Pt(10.5), SLATE)
        y += Cm(2.7)

    # Tease
    callout(slide, Cm(25),
            "TURN THE PAGE NOW →",
            "The 5-step protocol. Use it in the next 5 minutes.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(2), text_color=NAVY)


def p3_protocol(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "The 5-Step Protocol")
    footer(slide, 3)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "THE LIFELINE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "Do This Right Now",
        Pt(24), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "5 steps. About 3 minutes. Read each one before you act.",
        Pt(11), GOLD, i=True)

    steps = [
        ("1", "PAUSE", "Don't go in yet. Set a timer for 3 minutes. Many sounds at night are sleep cycling — not actual waking. Wait."),
        ("2", "BREATHE", "Take 3 slow breaths. Your nervous system is dysregulated right now. Your baby will feel it. Reset YOURSELF first."),
        ("3", "ASSESS", "After the timer: Are they crying or just rustling? Has it been less than 5 minutes? Is this distress, or is this cycling?"),
        ("4", "RESPOND TO YOUR PLAN", "Use the method you chose BEFORE tonight. Same wait time. Same words. Same approach. If you're winging it — that's the problem."),
        ("5", "REMEMBER", "One bad night doesn't erase progress. Tomorrow is a new night. Your baby will sleep again. So will you."),
    ]
    y = Cm(6.4)
    for num, title, body in steps:
        card = shp(slide, Cm(2), y, Cm(17), Cm(3.3), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        # Number
        shp(slide, Cm(2.4), y + Cm(0.7), Cm(2), Cm(2), NAVY, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.4), y + Cm(0.9), Cm(2), Cm(1.6),
            num, Pt(20), GOLD, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
            fn=FONT_HEADING)
        # Title
        txt(slide, Cm(5), y + Cm(0.5), Cm(13.5), Cm(0.8),
            title, Pt(15), NAVY, b=True, fn=FONT_HEADING)
        gbar(slide, Cm(5), y + Cm(1.4), Cm(2))
        # Body
        txt(slide, Cm(5), y + Cm(1.7), Cm(13.5), Cm(1.5),
            body, Pt(10), SLATE)
        y += Cm(3.5)

    # Bottom note
    callout(slide, Cm(24.5),
            "IF YOUR BABY IS GENUINELY DISTRESSED",
            "Go in. Always. The 5-step protocol is for the rustles, not the screams. You know your baby. Trust that.",
            accent=RUST, bg_clr=RED_LT,
            h=Cm(2.5), text_color=NAVY)


def p4_recovery(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    txt(slide, Cm(2), Cm(3), Cm(17), Cm(0.6),
        "ONE MORE THING — IF YOU CAVED TONIGHT",
        Pt(9), GOLD, b=True, al=PP_ALIGN.CENTER)

    txt(slide, Cm(2), Cm(5.5), Cm(17), Cm(2.5),
        "It's okay.",
        Pt(48), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(8.3), Cm(17), Cm(2.5),
        "It really, really is.",
        Pt(28), GOLD, b=True, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    gbar(slide, Cm(8.5), Cm(11.3), Cm(4))

    body = [
        {"t": "Maybe you brought baby into your bed. Maybe you nursed back to sleep. Maybe you rocked for an hour. Maybe all three.",
         "sz": Pt(11.5), "c": CREAM_MID, "sa": Pt(8), "al": PP_ALIGN.CENTER},
        {"t": "Hear me clearly: ONE NIGHT does not undo a week of progress. It just doesn't. You are tired. You are human. You did what your body told you to do at 3 AM.",
         "sz": Pt(11.5), "c": CREAM_MID, "sa": Pt(8), "al": PP_ALIGN.CENTER},
        {"t": "Tomorrow morning: forgive yourself. Drink the coffee. Read the plan again. Tomorrow night: try again.",
         "sz": Pt(11.5), "c": GOLD_LITE, "i": True, "fn": FONT_HEADING, "al": PP_ALIGN.CENTER},
    ]
    mtxt(slide, Cm(2), Cm(12.5), Cm(17), Cm(7), body)

    cta_box(slide, Cm(20),
            "Stop winging it at 2 AM.",
            "Get the full plan. The book that lives on your nightstand.",
            "GET THE BOOK  →  $19",
            "www.sixandthriving.com")

    txt(slide, Cm(2), Cm(26.7), Cm(17), Cm(0.6),
        "Sleep is coming. For both of you.",
        Pt(11), GOLD_LITE, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(27.4), Cm(17), Cm(0.5),
        "— Six & Thriving",
        Pt(10), GOLD, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    dark_footer(slide, 4)


def build():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH

    print()
    print("  ╔════════════════════════════════════════════════╗")
    print("  ║  The 2 AM Survival Guide — PREMIUM v2 (.pptx)  ║")
    print("  ╚════════════════════════════════════════════════╝")
    print()

    pages = [
        ("Cover — It's 2 AM", p1_cover),
        ("Letter — I see you", p2_letter),
        ("The 5-step protocol", p3_protocol),
        ("Recovery + CTA", p4_recovery),
    ]
    for name, fn in pages:
        print(f"  ✓ {name}")
        fn(prs)

    prs.save(OUTPUT)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print()
    print(f"  ✅ Saved: {OUTPUT}")
    print(f"  📄 Size: {size_kb:.1f} KB  •  4 pages")
    print()


if __name__ == "__main__":
    build()
