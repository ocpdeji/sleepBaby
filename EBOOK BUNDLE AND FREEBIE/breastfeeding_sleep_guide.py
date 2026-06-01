"""
Breastfeeding & Sleep — The Honest Guide (PowerPoint Premium)
"Sleep, Baby. Please." by Six & Thriving (2026)
─────────────────────────────────────────────────────────────────────
6-page premium freebie targeting breastfeeding moms (the largest buying group).
Same brand DNA as the main ebook. Editable in PowerPoint AND Canva.

Pages:
  1  Cover — premium navy/gold
  2  Letter — "You don't have to choose"
  3  The Drop Schedule (the value)
  4  The Unlatch Technique + Dream Feeds
  5  Q&A — what every breastfeeding mom asks
  6  CTA — Get the full Chapter 13

Run: python breastfeeding_sleep_guide.py
"""

import os
from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from _brand import (
    NAVY, NAVY_MID, NAVY_LITE, GOLD, GOLD_LITE, CREAM, CREAM_MID, WHITE,
    TEAL, SLATE, SLATE_LITE, RUST, GREEN_DK, AMBER, AMBER_LT, BLUE_LT, GREEN_LT,
    FONT_HEADING, FONT_BODY, SW, SH,
    bg, shp, txt, mtxt, gbar, header, footer, dark_footer, callout,
    cta_box, cover_decoration,
)

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "Breastfeeding_and_Sleep_Guide.pptx")


def p1_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    # FREE badge
    shp(slide, Cm(15.5), Cm(2.5), Cm(3.5), Cm(3.5), GOLD, MSO_SHAPE.OVAL)
    txt(slide, Cm(15.5), Cm(3.2), Cm(3.5), Cm(0.9),
        "FREE", Pt(16), NAVY, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(15.5), Cm(4.2), Cm(3.5), Cm(0.7),
        "GUIDE", Pt(9), NAVY, b=True, al=PP_ALIGN.CENTER)

    # Tag
    txt(slide, Cm(2), Cm(4.5), Cm(13), Cm(0.7),
        "FROM CHAPTER 13 OF SLEEP, BABY. PLEASE.",
        Pt(9), GOLD, b=True)
    gbar(slide, Cm(2), Cm(5.3), Cm(7))

    # Title
    txt(slide, Cm(2), Cm(8), Cm(17), Cm(2.5),
        "Breastfeeding", Pt(48), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(11), Cm(17), Cm(2.5),
        "& Sleep", Pt(48), GOLD, b=True, i=True, fn=FONT_HEADING)

    # Diamond rule
    gbar(slide, Cm(2), Cm(14.3), Cm(7))
    shp(slide, Cm(5.3), Cm(14.15), Cm(0.4), Cm(0.4), GOLD, MSO_SHAPE.OVAL)

    # Subtitle
    mtxt(slide, Cm(2), Cm(15.2), Cm(17), Cm(2), [
        {"t": "The honest guide for moms who want to keep nursing",
         "sz": Pt(13), "c": CREAM_MID, "sa": Pt(4)},
        {"t": "AND finally get some sleep.",
         "sz": Pt(13), "c": CREAM_MID},
    ])

    bullets = [
        "✦  Yes, breastfeeding and sleep training ARE compatible",
        "✦  When to drop night feeds — by age",
        "✦  The unlatch technique that changed everything for me",
    ]
    paras = [{"t": b, "sz": Pt(11), "c": GOLD_LITE, "sa": Pt(8)} for b in bullets]
    mtxt(slide, Cm(2), Cm(18), Cm(17), Cm(5), paras)

    gbar(slide, Cm(2), Cm(24), Cm(7))
    txt(slide, Cm(2), Cm(24.5), Cm(17), Cm(1),
        "SIX  &  THRIVING", Pt(16), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(25.7), Cm(17), Cm(0.8),
        "Mother of Six — Including a Set of Twins",
        Pt(11), GOLD_LITE, i=True)

    txt(slide, Cm(0), Cm(28.5), SW, Cm(0.6),
        "www.sixandthriving.com", Pt(9), GOLD, al=PP_ALIGN.CENTER)


def p2_letter(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "A Letter")
    footer(slide, 2)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "TO THE BREASTFEEDING MOM WHO'S BEEN TOLD SHE HAS TO CHOOSE",
        Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.2), Cm(17), Cm(2.5),
        "You don't have\nto choose.",
        Pt(28), NAVY, b=True, fn=FONT_HEADING)
    gbar(slide, Cm(2), Cm(7.2), Cm(3))

    body = [
        {"t": "I've heard it from hundreds of moms: 'I want to keep breastfeeding, but everyone keeps telling me I'll never sleep again unless I wean.'",
         "sz": Pt(11), "c": SLATE, "sa": Pt(10)},
        {"t": "It's not true.",
         "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(10)},
        {"t": "Breastfeeding and independent sleep are completely compatible. I nursed every one of my six babies — including my twins — past 18 months. They all learned to sleep through the night while still breastfeeding.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(10)},
        {"t": "The trick isn't choosing. It's separating the FEED from the FALL-ASLEEP MOMENT.",
         "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(8), Cm(17), Cm(8), body)

    # Pull quote
    shp(slide, Cm(2), Cm(16), Cm(17), Cm(3.5), NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
    shp(slide, Cm(2), Cm(16), Cm(0.2), Cm(3.5), GOLD, MSO_SHAPE.RECTANGLE)
    mtxt(slide, Cm(2.6), Cm(16.3), Cm(16), Cm(3), [
        {"t": '"Your supply will not disappear.', "sz": Pt(15), "c": GOLD_LITE,
         "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(2)},
        {"t": "Your bond will not break.", "sz": Pt(15), "c": GOLD_LITE,
         "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": 'Your baby will still nurse — they will just stop using the breast as a sleep tool."',
         "sz": Pt(11), "c": CREAM, "i": True},
    ])

    closing = [
        {"t": "This guide is the breastfeeding-specific section from my full book. It's the part new moms message me about most.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(10)},
        {"t": "Read it. Try the unlatch technique tonight. Your supply will be fine. Your baby will be fine. You will start sleeping again.",
         "sz": Pt(11), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(20.5), Cm(17), Cm(4), closing)

    # Sign-off
    mtxt(slide, Cm(2), Cm(24.5), Cm(17), Cm(2), [
        {"t": "With love and solidarity,", "sz": Pt(10), "c": SLATE, "i": True, "sa": Pt(4)},
        {"t": "— Six & Thriving", "sz": Pt(11), "c": GOLD, "b": True, "fn": FONT_HEADING},
    ])


def p3_drop_schedule(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Night Feed Schedule")
    footer(slide, 3)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "BY AGE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "When to Drop Night Feeds", Pt(24), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "For breastfed babies — paediatrician approval first.",
        Pt(11), GOLD, i=True)

    # The schedule rows with status badges
    rows = [
        ("0–4 months", "Feed on demand. All night feeds are nutritional.",
         "DON'T DROP", RUST),
        ("4–6 months", "Reduce to 1–2 feeds. Increase daytime calories.",
         "REDUCE", AMBER),
        ("6–9 months", "Most babies can handle 0–1 night feeds.",
         "ALMOST THERE", TEAL),
        ("9+ months", "If weight gain on track, night feeds are habitual.",
         "READY TO DROP", GREEN_DK),
    ]
    y = Cm(6.4)
    for age, desc, badge_text, badge_color in rows:
        # White card
        card = shp(slide, Cm(2), y, Cm(17), Cm(2.3), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        # Badge color stripe on left
        shp(slide, Cm(2), y, Cm(0.25), Cm(2.3), badge_color, MSO_SHAPE.RECTANGLE)
        # Age (bold navy)
        txt(slide, Cm(2.6), y + Cm(0.4), Cm(4), Cm(0.7),
            age, Pt(13), NAVY, b=True, fn=FONT_HEADING)
        # Description
        txt(slide, Cm(2.6), y + Cm(1.3), Cm(11), Cm(0.8),
            desc, Pt(9.5), SLATE)
        # Badge
        shp(slide, Cm(14), y + Cm(0.6), Cm(4.5), Cm(1.1), badge_color, MSO_SHAPE.ROUNDED_RECTANGLE)
        txt(slide, Cm(14), y + Cm(0.7), Cm(4.5), Cm(0.9),
            badge_text, Pt(10), WHITE, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
        y += Cm(2.6)

    # The myth-busting callout
    callout(slide, Cm(17.5),
            "THE MYTH BUSTER",
            "Your supply adjusts to daytime demand within 3–5 days of dropping a night feed. Pump once before bed in the first few days if engorgement is a concern. After that, your body knows what to do.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(3))

    # How to know if it's a habit
    callout(slide, Cm(21),
            "QUICK TEST — IS IT NUTRITIONAL OR HABITUAL?",
            "If your baby feeds for less than 5 minutes and drifts back to sleep — it's habitual. A truly hungry baby drinks purposefully, transferring real volume. Watch tomorrow night.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(3))

    # Tease
    callout(slide, Cm(24.5),
            "TURN THE PAGE →",
            "The unlatch technique. The dream feed. Both will change your nights this week.",
            accent=NAVY, bg_clr=CREAM_MID, h=Cm(2.5), text_color=NAVY)


def p4_techniques(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Two Techniques")
    footer(slide, 4)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "TONIGHT'S TOOLKIT", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "Two Techniques That Change Everything",
        Pt(22), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "Try one tonight. Try both this week.",
        Pt(11), GOLD, i=True)

    # ── TECHNIQUE 1: THE UNLATCH ────────────────────────────────────
    txt(slide, Cm(2), Cm(6.3), Cm(17), Cm(0.8),
        "1.  The Unlatch Technique",
        Pt(16), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(7.3), Cm(17), Cm(0.5),
        "How to gently end a comfort feed without waking baby fully.",
        Pt(10), GOLD, i=True)

    unlatch_steps = [
        ("1", "Watch for the flutter-suck",
         "Slow, gentle, no swallowing. That's the comfort phase, not nutrition."),
        ("2", "Slip your finger in",
         "Gently into the corner of baby's mouth. Break suction softly."),
        ("3", "Sit baby up briefly",
         "Just enough to rouse them to drowsy — NOT fully awake."),
        ("4", "Place in crib awake",
         "A calm phrase. A kiss. Walk out. The feed-to-sleep link breaks here."),
    ]
    y = Cm(8.2)
    for num, ttl, body in unlatch_steps:
        card = shp(slide, Cm(2), y, Cm(17), Cm(1.9), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        # Number badge
        shp(slide, Cm(2.4), y + Cm(0.45), Cm(1), Cm(1), TEAL, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.4), y + Cm(0.5), Cm(1), Cm(0.9), num,
            Pt(11), WHITE, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE,
            fn=FONT_HEADING)
        txt(slide, Cm(3.8), y + Cm(0.3), Cm(15), Cm(0.6),
            ttl, Pt(11), NAVY, b=True)
        txt(slide, Cm(3.8), y + Cm(1), Cm(15), Cm(0.8),
            body, Pt(9.5), SLATE)
        y += Cm(2.05)

    # ── TECHNIQUE 2: THE DREAM FEED ────────────────────────────────
    y = Cm(17)
    txt(slide, Cm(2), y, Cm(17), Cm(0.8),
        "2.  The Dream Feed",
        Pt(16), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), y + Cm(1), Cm(17), Cm(0.5),
        "How to add 1–2 hours to your first stretch tonight.",
        Pt(10), GOLD, i=True)

    # Dream feed in a nice green callout
    df_y = y + Cm(1.8)
    df_h = Cm(7)
    shp(slide, Cm(2), df_y, Cm(17), df_h, GREEN_LT, MSO_SHAPE.ROUNDED_RECTANGLE)
    shp(slide, Cm(2), df_y, Cm(0.25), df_h, GREEN_DK, MSO_SHAPE.RECTANGLE)
    txt(slide, Cm(2.6), df_y + Cm(0.3), Cm(16), Cm(0.5),
        "OFFER AT 10–11 PM, BEFORE YOU GO TO BED",
        Pt(8), GREEN_DK, b=True)

    df_steps = [
        "Lights stay OFF. No talking. No diaper change unless soiled.",
        "Gently lift baby — keep them in a drowsy state.",
        "Latch them. Let them feed for 5–8 minutes.",
        "Place back in crib. They often don't fully wake.",
        "Use it for 2–3 weeks. Drop it when baby is sleeping through.",
    ]
    sy = df_y + Cm(1)
    for step in df_steps:
        txt(slide, Cm(3), sy, Cm(0.4), Cm(0.5),
            "✓", Pt(11), GREEN_DK, b=True)
        txt(slide, Cm(3.5), sy, Cm(15), Cm(0.5),
            step, Pt(10), SLATE)
        sy += Cm(1)

    # Final callout — your supply
    callout(slide, Cm(26.2),
            "REPEAT IF NEEDED",
            "Your supply will adjust within 3–5 days. Your baby will still nurse. You will still bond. You will just be sleeping.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(1.6), text_color=NAVY)


def p5_qa(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Common Questions")
    footer(slide, 5)

    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4),
        "WHAT EVERY BREASTFEEDING MOM ASKS", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))

    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.5),
        "Real Questions, Honest Answers",
        Pt(22), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.6),
        "Asked by hundreds of moms. Answered honestly.",
        Pt(11), GOLD, i=True)

    qa_data = [
        ("Will my supply drop?",
         "No. Your body adjusts to daytime demand within 3–5 days of dropping a night feed. Pump once before bed in the early days if engorgement is a concern."),
        ("Is my baby actually hungry at night?",
         "If they feed for less than 5 minutes and drift back to sleep — it's habitual. A truly hungry baby drinks purposefully and transfers real volume."),
        ("Can I still nurse to sleep for naps?",
         "Ideally no — consistency matters most. But bedtime is the priority. If you're going to break the feed-to-sleep link somewhere, start there."),
        ("My baby refuses bottles from my partner. What now?",
         "Common. Have partner offer the bottle when baby is HUNGRY but not starving — about 15 minutes before usual feed time. Use a slow-flow nipple. Skin-to-skin during the bottle. Try 7–10 days before declaring it 'not working.'"),
        ("Will my baby still bond with me if I stop nursing to sleep?",
         "Yes. The bond is built over thousands of nursing sessions during the day, in your arms, eye-to-eye. Sleep is taught separately. Your bond doesn't depend on how they fall asleep."),
    ]

    y = Cm(6.4)
    for question, answer in qa_data:
        card = shp(slide, Cm(2), y, Cm(17), Cm(3.6), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = GOLD
        card.line.width = Pt(0.8)
        # Q label
        txt(slide, Cm(2.6), y + Cm(0.3), Cm(0.8), Cm(0.6),
            "Q.", Pt(13), GOLD, b=True, fn=FONT_HEADING)
        txt(slide, Cm(3.5), y + Cm(0.35), Cm(15), Cm(0.7),
            question, Pt(11), NAVY, b=True)
        # A
        txt(slide, Cm(2.6), y + Cm(1.4), Cm(0.8), Cm(0.6),
            "A.", Pt(13), TEAL, b=True, fn=FONT_HEADING)
        txt(slide, Cm(3.5), y + Cm(1.45), Cm(15), Cm(2),
            answer, Pt(9.5), SLATE)
        y += Cm(3.8)

    # No room for callout — page is dense, that's OK


def p6_cta(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    cover_decoration(slide)

    txt(slide, Cm(2), Cm(3), Cm(17), Cm(0.6),
        "ONE LAST THING — IF THIS HELPED",
        Pt(9), GOLD, b=True, al=PP_ALIGN.CENTER)

    txt(slide, Cm(2), Cm(5.5), Cm(17), Cm(2.5),
        "This was 1 chapter.", Pt(36), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(8), Cm(17), Cm(2.5),
        "There are 14 more.", Pt(36), GOLD, b=True, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    gbar(slide, Cm(8.5), Cm(11), Cm(4))

    body = [
        {"t": "The full book covers every method (Ferber, extinction, fading, chair, pick-up/put-down) with day-by-day timing charts. Plus the Six Sleep Personalities. Plus the Crib Hour technique nobody else teaches. Plus full chapters on twins, NICU babies, daycare, single parents, and the Reset Protocol if you've tried before.",
         "sz": Pt(11), "c": CREAM_MID, "sa": Pt(8), "al": PP_ALIGN.CENTER},
        {"t": "Everything you need to be sleeping in 7 nights — written by a mom of six who lived every chapter.",
         "sz": Pt(11.5), "c": GOLD_LITE, "i": True, "fn": FONT_HEADING, "al": PP_ALIGN.CENTER},
    ]
    mtxt(slide, Cm(2), Cm(11.8), Cm(17), Cm(7), body)

    cta_box(slide, Cm(19.5),
            "Want the full plan?",
            "Sleep, Baby. Please. — 59 pages. Birth to toddler.",
            "GET THE BOOK  →  $19",
            "www.sixandthriving.com")

    # Sign-off
    txt(slide, Cm(2), Cm(26.5), Cm(17), Cm(0.6),
        "Sleep is coming. For both of you.",
        Pt(11), GOLD_LITE, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(27.2), Cm(17), Cm(0.5),
        "— Six & Thriving",
        Pt(10), GOLD, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)

    dark_footer(slide, 6)


def build():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH

    print()
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║  Breastfeeding & Sleep Guide — PREMIUM v2 (.pptx) ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()

    pages = [
        ("Cover", p1_cover),
        ("Letter — You don't have to choose", p2_letter),
        ("Drop schedule by age", p3_drop_schedule),
        ("Unlatch + Dream Feed", p4_techniques),
        ("Real Q&A", p5_qa),
        ("CTA — Get the full book", p6_cta),
    ]
    for name, fn in pages:
        print(f"  ✓ {name}")
        fn(prs)

    prs.save(OUTPUT)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print()
    print(f"  ✅ Saved: {OUTPUT}")
    print(f"  📄 Size: {size_kb:.1f} KB  •  6 pages")
    print()


if __name__ == "__main__":
    build()
