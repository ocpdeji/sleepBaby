"""
Sleep, Baby. Please. — BESTSELLER EDITION v4.0
Six & Thriving | 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The Definitive Edition. Built to be:
  • Award-winning quality
  • Zero-refund-rate substance
  • Every mom will refer to other moms
  • Production-ready for Canva import

Combines:
  ✓ All rich content from the OLD edition (Six Sleep Personalities,
    Crib Hour, detailed methods, sample routines by age, night-by-night plan)
  ✓ All audit-driven new chapters (Breastfeeding, Twins/NICU/Daycare,
    First 8 Weeks, Partner Briefing, Reset Protocol)
  ✓ Specific, actionable scripts and decision trees on every page
  ✓ Premium design: navy/gold/cream palette, headers, footers, page numbers
"""

from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── BRAND PALETTE ──────────────────────────────────────────────────────────────
NAVY = RGBColor(0x0D, 0x1B, 0x3E)
NAVY_MID = RGBColor(0x16, 0x23, 0x47)
NAVY_LITE = RGBColor(0x1E, 0x2F, 0x55)
GOLD = RGBColor(0xC9, 0xA8, 0x4C)
GOLD_LITE = RGBColor(0xE8, 0xC9, 0x7A)
CREAM = RGBColor(0xFA, 0xF7, 0xF2)
CREAM_MID = RGBColor(0xF0, 0xEB, 0xE1)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEAL = RGBColor(0x2D, 0x8A, 0x8A)
SLATE = RGBColor(0x4A, 0x55, 0x68)
SLATE_LITE = RGBColor(0x71, 0x80, 0x96)
RUST = RGBColor(0xC0, 0x39, 0x2B)
GREEN_DK = RGBColor(0x27, 0x67, 0x49)
GREEN_LT = RGBColor(0xF0, 0xFD, 0xF4)
AMBER = RGBColor(0xD6, 0x9E, 0x2E)
PURPLE = RGBColor(0x55, 0x3C, 0x9A)
BLUE_LT = RGBColor(0xEB, 0xF8, 0xFF)
AMBER_LT = RGBColor(0xFE, 0xFC, 0xBF)
RED_LT = RGBColor(0xFE, 0xD7, 0xD7)

FONT_HEADING = "Georgia"
FONT_BODY = "Arial"

SW = Cm(21.0)
SH = Cm(29.7)

BASE = os.path.dirname(os.path.abspath(__file__))

IMG = {
    "cover": "1. Sleep_Baby_Please_SixAndThriving_2026 (1)_page-0001.jpg",
    "exhausted_parent": "Warm_editorial_illustration,_exhausted_young_202605112320.jpeg",
    "sleeping_baby": "Soft_editorial_watercolor_illustration,_sleeping_202605112332.jpeg",
    "narrator": "Realistic_AI_female_narrator_in_202605112333.jpeg",
    "timeline": "Clean_horizontal_timeline_infographic,_showing_202605112323.jpeg",
    "bar_chart": "Clean_flat_bar_chart,_showing_202605112332.jpeg",
    "banner": "Clean_flat_infographic_banner,_seven_202605112332.jpeg",
    "diagram": "Clean_flat_infographic_diagram,_two_202605112321.jpeg",
    "editorial": "Clean_premium_editorial_illustration,_full-bleed_202605120011.jpeg",
    "five_step": "Clean_premium_flat_infographic,_five_202605120008.jpeg",
    "horizontal": "Clean_premium_flat_infographic,_horizontal_202605120009.jpeg",
    "seven_info": "Clean_premium_flat_infographic,_seven_202605120011.jpeg",
    "single": "Clean_premium_flat_infographic,_single_202605120010.jpeg",
    "structured": "Clean_premium_flat_infographic,_structured_202605120009.jpeg",
    "designed": "Clean_premium_flat_infographic_designed_202605120010.jpeg",
    "grid": "Clean_premium_flat_infographic_grid,_202605120009.jpeg",
    "styled": "Clean_premium_flat_infographic_styled_202605120011.jpeg",
    "quadrant": "Clean_premium_flat_quadrant_comparison_202605112333.jpeg",
    "poster": "Clean_premium_infographic_poster_design,_202605112323.jpeg",
    "roadmap": "Premium_flat_roadmap_infographic,_horizontal_202605112330.jpeg",
    "vertical": "Premium_flat_infographic,_vertical_5-step_202605112324.jpeg",
    "warm_illust": "Warm_editorial_illustration_of_a_202605112328 (1).jpeg",
    "humorous": "Warm_humorous_editorial_illustration,_small_202605112329.jpeg",
    "breastfeeding": "Ch.9 Breastfeeding.jpeg",
    "twins_nicu": "Ch.10 TwinsNICU.jpeg",
    "partner": "Partner Briefing.jpeg",
}

def imgp(k):
    return os.path.join(BASE, IMG[k])

# ═══════════════════════════════════════════════════════════════════════════════
#  CORE HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def bg(slide, color):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = color

def shp(slide, l, t, w, h, color, st=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = slide.shapes.add_shape(st, l, t, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    return s

def txt(slide, l, t, w, h, text, sz=Pt(10), clr=SLATE, b=False, i=False,
        al=PP_ALIGN.LEFT, fn=FONT_BODY, anc=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anc
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = sz
    p.font.color.rgb = clr
    p.font.bold = b
    p.font.italic = i
    p.font.name = fn
    p.alignment = al
    return tb

def mtxt(slide, l, t, w, h, paras):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, pd in enumerate(paras):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = pd.get("t", "")
        p.font.size = pd.get("sz", Pt(10))
        p.font.color.rgb = pd.get("c", SLATE)
        p.font.bold = pd.get("b", False)
        p.font.italic = pd.get("i", False)
        p.font.name = pd.get("fn", FONT_BODY)
        p.alignment = pd.get("al", PP_ALIGN.LEFT)
        p.space_after = pd.get("sa", Pt(6))
    return tb

def pic(slide, key, l, t, w=None, h=None):
    path = imgp(key)
    if not os.path.exists(path):
        return None
    if w and h:
        return slide.shapes.add_picture(path, l, t, w, h)
    elif w:
        return slide.shapes.add_picture(path, l, t, width=w)
    elif h:
        return slide.shapes.add_picture(path, l, t, height=h)
    return slide.shapes.add_picture(path, l, t)

def gbar(slide, l, t, w):
    return shp(slide, l, t, w, Cm(0.12), GOLD, MSO_SHAPE.RECTANGLE)


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER / FOOTER / PAGE NUMBER SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

def header(slide, chapter="Sleep, Baby. Please."):
    shp(slide, Cm(0), Cm(0), SW, Cm(1.3), NAVY, MSO_SHAPE.RECTANGLE)
    shp(slide, Cm(0), Cm(1.3), SW, Cm(0.12), GOLD, MSO_SHAPE.RECTANGLE)
    txt(slide, Cm(2), Cm(0.3), Cm(8), Cm(0.7), "Sleep, Baby. Please.",
        Pt(7.5), CREAM, fn=FONT_HEADING)
    txt(slide, Cm(11), Cm(0.3), Cm(8), Cm(0.7), chapter,
        Pt(7.5), GOLD_LITE, al=PP_ALIGN.RIGHT, fn=FONT_BODY)

def footer(slide, pg):
    shp(slide, Cm(0), Cm(28.1), SW, Cm(1.6), CREAM_MID, MSO_SHAPE.RECTANGLE)
    shp(slide, Cm(0), Cm(28.0), SW, Cm(0.1), GOLD, MSO_SHAPE.RECTANGLE)
    shp(slide, Cm(9.6), Cm(28.3), Cm(1.3), Cm(1.3), NAVY, MSO_SHAPE.OVAL)
    txt(slide, Cm(9.6), Cm(28.4), Cm(1.3), Cm(1.1), str(pg),
        Pt(9), WHITE, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    txt(slide, Cm(2), Cm(28.4), Cm(7), Cm(0.7),
        "Six & Thriving  •  sixandthriving.com", Pt(7), SLATE_LITE)
    txt(slide, Cm(12.5), Cm(28.4), Cm(6.5), Cm(0.7),
        "© 2026 Six & Thriving", Pt(7), SLATE_LITE, al=PP_ALIGN.RIGHT)

def dark_footer(slide, pg):
    shp(slide, Cm(0), Cm(28.1), SW, Cm(1.6), RGBColor(0x08, 0x0F, 0x24), MSO_SHAPE.RECTANGLE)
    shp(slide, Cm(0), Cm(28.0), SW, Cm(0.1), GOLD, MSO_SHAPE.RECTANGLE)
    shp(slide, Cm(9.6), Cm(28.3), Cm(1.3), Cm(1.3), GOLD, MSO_SHAPE.OVAL)
    txt(slide, Cm(9.6), Cm(28.4), Cm(1.3), Cm(1.1), str(pg),
        Pt(9), NAVY, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
    txt(slide, Cm(2), Cm(28.4), Cm(7), Cm(0.7),
        "Six & Thriving", Pt(7), SLATE_LITE)
    txt(slide, Cm(12.5), Cm(28.4), Cm(6.5), Cm(0.7),
        "© 2026 Six & Thriving", Pt(7), SLATE_LITE, al=PP_ALIGN.RIGHT)

def page_top(slide, label_text, title, chapter_label):
    """Standard content page header — label, gold bar, title."""
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), label_text, Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), title, Pt(20), NAVY, b=True, fn=FONT_HEADING)

def callout(slide, t, w, label, body, accent=TEAL, bg_clr=BLUE_LT, text_color=SLATE,
            label_clr=None, h=Cm(2.5), label_size=Pt(7.5), body_size=Pt(9.5),
            x_left=Cm(2), w_total=Cm(17)):
    """Add a callout box with accent bar."""
    shp(slide, x_left, t, w_total, h, bg_clr, MSO_SHAPE.ROUNDED_RECTANGLE)
    shp(slide, x_left, t, Cm(0.2), h, accent, MSO_SHAPE.RECTANGLE)
    txt(slide, x_left + Cm(0.6), t + Cm(0.2), w_total - Cm(0.8), Cm(0.4),
        label, label_size, label_clr or accent, b=True)
    txt(slide, x_left + Cm(0.6), t + Cm(0.7), w_total - Cm(0.8), h - Cm(0.9),
        body, body_size, text_color)

def ch_opener(prs, num, label, title, subtitle, pg):
    """Dark chapter opener — NO images, clean typography."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    shp(slide, Cm(14), Cm(-3), Cm(12), Cm(12), NAVY_LITE, MSO_SHAPE.OVAL)
    shp(slide, Cm(-4), Cm(20), Cm(8), Cm(8), NAVY_MID, MSO_SHAPE.OVAL)
    shp(slide, Cm(0), Cm(27.5), SW, Cm(0.3), GOLD, MSO_SHAPE.RECTANGLE)
    txt(slide, Cm(2), Cm(4), Cm(10), Cm(0.5), label, Pt(8), GOLD, b=True, fn=FONT_BODY)
    txt(slide, Cm(1.5), Cm(6), Cm(10), Cm(5), num, Pt(100), NAVY_LITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(11), Cm(16), Cm(7), title, Pt(28), WHITE, b=True, fn=FONT_HEADING)
    gbar(slide, Cm(2), Cm(19), Cm(4))
    if subtitle:
        txt(slide, Cm(2), Cm(19.5), Cm(15), Cm(3), subtitle, Pt(11), GOLD_LITE, i=True)
    dark_footer(slide, pg)


# ═══════════════════════════════════════════════════════════════════════════════
#  FRONT MATTER
# ═══════════════════════════════════════════════════════════════════════════════

def p_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    pic(slide, "cover", Cm(0), Cm(0), w=SW, h=SH)

def p_copyright(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Six & Thriving")
    footer(slide, 2)
    txt(slide, Cm(2), Cm(3), Cm(17), Cm(1.2), "Sleep, Baby. Please.",
        Pt(26), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.8),
        "What Actually Worked for All 6 of Mine — Including Twins",
        Pt(12), GOLD, i=True, fn=FONT_HEADING)
    gbar(slide, Cm(2), Cm(5.5), Cm(17))
    paras = [
        {"t": "Copyright © 2026 Six & Thriving. All rights reserved.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "No part of this publication may be reproduced, distributed, or transmitted in any form without prior written permission.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "DISCLAIMER: This book is for informational and educational purposes only. The author is not a licensed medical professional, paediatrician, or certified sleep consultant. Strategies are based on personal experience raising six children and extensive research. Every baby is different, and results will vary. Always consult your paediatrician before making changes to your baby's sleep routine, especially if your baby has any medical conditions.", "sz": Pt(9), "c": SLATE, "sa": Pt(14)},
        {"t": "First Edition. Published 2026.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(20)},
        {"t": "SIX & THRIVING", "sz": Pt(11), "c": GOLD, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Practical parenting resources for the exhausted and the hopeful.", "sz": Pt(9.5), "c": SLATE, "i": True},
    ]
    mtxt(slide, Cm(2), Cm(6.3), Cm(17), Cm(18), paras)

def p_toc(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Contents")
    footer(slide, 3)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CONTENTS", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.2), "Table of Contents",
        Pt(26), NAVY, b=True, fn=FONT_HEADING)
    entries = [
        ("INTRO", "To the Parent Reading This at 3 a.m.", "4"),
        ("FAST-TRACK", "Tonight's Plan — Start Here", "5"),
        ("CH. 1", "Why Your Baby Won't Sleep (And It's Not Your Fault)", "6"),
        ("CH. 2", "The Sleep Science Every Parent Actually Needs", "9"),
        ("CH. 3", "Reading Your Baby's Sleep Cues", "12"),
        ("CH. 4", "Building a Bedtime Routine That Sticks", "16"),
        ("CH. 5", "Setting the Stage — The Sleep Environment", "20"),
        ("CH. 6", "The Big Sleep Training Debate — All Methods", "23"),
        ("CH. 7", "Night Wakings & The Reset Protocol", "28"),
        ("CH. 8", "The Six Sleep Personalities", "32"),
        ("CH. 9", "Common Mistakes (I Made Them All)", "35"),
        ("CH. 10", "Staying Consistent When You're Empty", "38"),
        ("CH. 11", "Toddler Sleep — Little Negotiators", "40"),
        ("CH. 12", "Your First Week — Night-by-Night Plan", "42"),
        ("CH. 13", "Breastfeeding & Sleep — The Honest Guide", "46"),
        ("CH. 14", "Twins, NICU & Daycare", "49"),
        ("CH. 15", "The First 8 Weeks — Newborn Period", "51"),
        ("PARTNER", "The Partner Briefing One-Pager", "53"),
        ("CLOSING", "My Sleep Promise & Conclusion", "54"),
        ("BONUS", "Checklists, Trackers & Quick Reference", "56"),
    ]
    y = Cm(4.6)
    for tag, title, pg in entries:
        shp(slide, Cm(2), y - Cm(0.05), Cm(17), Cm(0.03), CREAM_MID, MSO_SHAPE.RECTANGLE)
        txt(slide, Cm(2), y, Cm(2.8), Cm(0.5), tag, Pt(7), GOLD, b=True)
        txt(slide, Cm(5), y, Cm(11.5), Cm(0.5), title, Pt(9), NAVY)
        txt(slide, Cm(17), y, Cm(2), Cm(0.5), pg, Pt(9), GOLD, b=True, al=PP_ALIGN.RIGHT)
        y += Cm(1.15)

def p_intro(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Introduction")
    footer(slide, 4)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "INTRODUCTION", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(12), Cm(1.8),
        "To the Parent\nReading This at 3 a.m.", Pt(24), NAVY, b=True, fn=FONT_HEADING)
    pic(slide, "exhausted_parent", Cm(13), Cm(2.8), w=Cm(6.5))
    body = [
        {"t": "Let me guess. It's somewhere between midnight and 4 a.m. You're sitting in the dark — probably in a rocking chair, maybe on the nursery floor — holding a baby who should, by every logical measure, be completely exhausted. And yet here you both are.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "You've tried everything. The shushing. The swaddling. Patted, bounced, sung your way through songs you didn't know you remembered. And still — still — this tiny human will not sleep.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "I've been there. Six times.", "sz": Pt(10.5), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "My name is behind the pen name Six & Thriving — and yes, I have six kids. A set of twins tucked into the middle, a strong-willed firstborn, a sensitive soul, an adventurous spirit, and the baby who nearly broke me before finally sleeping through at 14 weeks.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "Every single one came as a unique sleep puzzle. What worked for baby #1 was useless for baby #3. The method that felt wrong with my twins turned out to be exactly right. I read every book, every article, every 2 a.m. forum post. Then I built this system.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(6), Cm(11), Cm(15), body)
    callout(slide, Cm(21.5), w=Cm(17), label="WHO THIS BOOK IS FOR",
            body="Your baby (newborn–24 months) is not sleeping and you have no idea why. You've tried 'just leaving them to cry' and it felt wrong. You're so tired you've Googled 'is it safe to sleep standing up.' You want a real plan from a real parent — not clinical theory.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(3.5), text_color=NAVY, label_clr=AMBER)
    callout(slide, Cm(25.3), w=Cm(17), label="MY PROMISE TO YOU",
            body="By the end of this book, you'll have a step-by-step plan you can start tonight. Sleep is coming — for both of you. I promise.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(2.3), text_color=NAVY, label_clr=TEAL)


def p_fast_track(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Fast-Track")
    footer(slide, 5)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "FAST-TRACK", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Tonight's Plan",
        Pt(22), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.5),
        "If you read nothing else, read this page first.", Pt(10), GOLD, i=True)
    txt(slide, Cm(2), Cm(5), Cm(17), Cm(0.7),
        "These six steps are the foundation of everything in this book. Do these tonight — read the rest when you have twenty quiet minutes.",
        Pt(9.5), SLATE)
    steps = [
        ("1", "Check the room right now",
         "Pitch black? White noise running? Temperature 68–72°F / 20–22°C? Fix it before anything else. This single change can shift the entire night."),
        ("2", "Find your baby's awake window",
         "Turn to the Awake Windows table in Ch. 3. Note the maximum time your baby should be up. Set a timer. Don't let them go past it."),
        ("3", "Write tonight's bedtime routine — in order",
         "Bath → lotion → pyjamas → feed (not to sleep) → song → crib awake. Same sequence every night. Stick it on the door."),
        ("4", "Decide your response plan before night falls",
         "Choose your method from Ch. 6 right NOW. Your 2 a.m. brain won't make good decisions. Write it down."),
        ("5", "Pause before you go in",
         "When you hear a sound, wait 2–3 minutes. Many babies cycle through light sleep and resettle. Rushing in fully wakes them."),
        ("6", "Put them into the crib AWAKE",
         "Drowsy is fine. Already asleep is not. This single skill changes everything. If they always fall asleep in your arms, Ch. 4 is your priority."),
    ]
    y = Cm(6.3)
    for num, title, body in steps:
        card = shp(slide, Cm(2), y, Cm(17), Cm(2.7), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        shp(slide, Cm(2.4), y + Cm(0.5), Cm(1.4), Cm(1.4), NAVY, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.4), y + Cm(0.6), Cm(1.4), Cm(1.2), num,
            Pt(12), WHITE, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
        txt(slide, Cm(4.3), y + Cm(0.3), Cm(14), Cm(0.6), title, Pt(10), NAVY, b=True)
        txt(slide, Cm(4.3), y + Cm(1.2), Cm(14), Cm(1.4), body, Pt(8.5), SLATE)
        y += Cm(2.85)
    callout(slide, Cm(23.5), w=Cm(17), label="DONE IS BETTER THAN PERFECT",
            body="Pick one thing from this list and do it tonight. Progress starts with a single consistent step — not flawless execution of all six at once.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(2), text_color=NAVY, label_clr=AMBER)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 1: WHY YOUR BABY WON'T SLEEP
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch1_open(prs):
    ch_opener(prs, "01", "CHAPTER ONE",
              "Why Your Baby\nWon't Sleep —\nAnd It's Not\nYour Fault",
              "Once you understand the WHY, the WHAT TO DO\nbecomes so much clearer.", 6)

def p_ch1a(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter One")
    footer(slide, 7)
    page_top(slide, "CHAPTER ONE", "Babies Aren't Designed to Sleep Like Adults", "Chapter One")
    body = [
        {"t": "Here's the truth nobody leads with: babies are biologically wired to wake up frequently. This is not a design flaw. It is a survival mechanism. Frequent waking means frequent feeding (essential in early infancy), and lets your baby alert you if something is wrong.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "Adult sleep cycles last roughly 90 minutes. We move through light sleep, deep sleep, and REM. When we hit the light stage, we barely notice — we roll over and drift back. A baby's sleep cycle is much shorter — around 45–50 minutes — and when they hit the light stage, many of them fully wake up and need help getting back down.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "The 5 Most Common Reasons Babies Won't Sleep", "sz": Pt(14), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(10)},
        {"t": "1. Sleep Associations — The Sneaky Culprit", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
        {"t": "Whatever your baby associates with falling asleep, they will need at every wake-up. Always nurses to sleep? They'll need to nurse at 1am, 3am, 5am. This is the #1 reason babies who 'used to sleep great' suddenly start waking constantly — usually around 4 months.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "2. Overtiredness — The Counter-Intuitive Trap", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
        {"t": "You'd think a more tired baby sleeps better. They don't. Overtiredness triggers a cortisol response — the stress hormone — that makes it HARDER to fall and stay asleep. An overtired baby is a wired baby.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "3. Under-tiredness — Yes, This Is Real", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
        {"t": "If bedtime is too early or naps are too long, your baby simply isn't tired enough. I made this mistake with baby #4 — eager to get bedtime moving earlier and ended up with a baby ready to party at 7pm.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.3), Cm(17), Cm(20), body)
    callout(slide, Cm(24.7), w=Cm(17), label="REMEMBER THIS",
            body="A baby waking at night is not failing. A baby waking at night is doing exactly what their biology expects of them. Your job — and this book's job — is to gently teach them a new way.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(2.5), text_color=NAVY, label_clr=TEAL)

def p_ch1b(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter One")
    footer(slide, 8)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER ONE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    body = [
        {"t": "4. Environmental Factors", "sz": Pt(11), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Too much light, too much noise, room too warm or cold — the sleep environment matters more than most parents realize. The room your baby sleeps in is doing quiet work, either FOR you or AGAINST you.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "5. Developmental Leaps & Growth Spurts", "sz": Pt(11), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Just when you crack the code, baby hits a leap and everything goes sideways. This is normal. It is temporary. You haven't broken anything — they're growing. Common leap points: 4 months, 8–10 months, 12 months, 18 months, 24 months.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "And Now — The Part Where I Tell You It's Not Your Fault", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Hear this before we go further: you did not cause this by holding your baby too much, by responding to their cries, or by nursing them to sleep. You responded to your baby's needs. That is parenting. The habits that formed are just habits — and habits can be changed.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "I've met parents who felt crushing guilt over sleep struggles. Parents convinced they had 'done it wrong.' You haven't. You're here, reading this, looking for answers. That IS doing it right.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(3.5), Cm(17), Cm(15), body)
    # Stats
    stats = [("45", "MIN", "Baby's sleep cycle"), ("4–6", "MONTHS", "Earliest training age"), ("7", "NIGHTS", "Most see real change")]
    x = Cm(2)
    for val, unit, desc in stats:
        shp(slide, x, Cm(19), Cm(5.3), Cm(3.3), NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
        txt(slide, x, Cm(19.2), Cm(5.3), Cm(1.3), val, Pt(24), GOLD, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
        txt(slide, x, Cm(20.6), Cm(5.3), Cm(0.5), unit, Pt(8), CREAM_MID, b=True, al=PP_ALIGN.CENTER)
        txt(slide, x, Cm(21.3), Cm(5.3), Cm(0.8), desc, Pt(7.5), SLATE_LITE, al=PP_ALIGN.CENTER)
        x += Cm(5.7)
    # Tried before
    shp(slide, Cm(2), Cm(23), Cm(17), Cm(4), GREEN_LT, MSO_SHAPE.ROUNDED_RECTANGLE)
    shp(slide, Cm(2), Cm(23), Cm(0.2), Cm(4), GREEN_DK, MSO_SHAPE.RECTANGLE)
    txt(slide, Cm(2.6), Cm(23.2), Cm(16), Cm(0.4), "TRIED THIS BEFORE AND IT DIDN'T WORK?", Pt(8), GREEN_DK, b=True)
    mtxt(slide, Cm(2.6), Cm(23.8), Cm(16), Cm(3.5), [
        {"t": "You're not starting from zero — you're starting from experience. Most common reasons it failed:", "sz": Pt(9), "c": SLATE, "sa": Pt(4)},
        {"t": "• Wrong method for baby's temperament  • Inconsistency (especially Night 3)\n• Environment wasn't optimised  • Started during a regression  • Partner not aligned", "sz": Pt(8.5), "c": SLATE, "sa": Pt(6)},
        {"t": "This time, you have the full picture. Keep reading.", "sz": Pt(9), "c": GREEN_DK, "b": True},
    ])


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 2: THE SCIENCE
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch2_open(prs):
    ch_opener(prs, "02", "CHAPTER TWO",
              "The Sleep Science\nEvery Parent\nActually Needs\nto Know",
              "I'm not going to bury you in neuroscience.\nThese are the pieces I wish someone had handed me on day one.", 9)

def p_ch2a(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Two")
    footer(slide, 10)
    page_top(slide, "CHAPTER TWO", "Sleep Pressure & The Sweet Spot", "Chapter Two")
    body = [
        {"t": "Sleep pressure is the building pressure to sleep that accumulates the longer your baby is awake. It's driven by adenosine, a chemical that builds up in the brain. The longer awake, the more adenosine, the more pressure to sleep.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "If you put baby down BEFORE enough sleep pressure has built up — they won't settle. If you wait TOO LONG — cortisol kicks in and you've got an overtired wired baby.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "The sweet spot — where sleep pressure is high enough to make settling easier but cortisol hasn't taken over — is your new best friend.", "sz": Pt(10.5), "c": NAVY, "b": True, "i": True, "sa": Pt(14)},
        {"t": "Cortisol vs. Melatonin: The Two Sides of the Battle", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Melatonin says: SLEEP. Cortisol says: STAY AWAKE. When baby is past their optimal awake window, cortisol rises. That's why an overtired baby seems wired — they literally are. Their body is pumping out a stress hormone to keep them going.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "The Circadian Rhythm — Your Baby Has One Too", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Newborns don't arrive with a set circadian rhythm — it takes 6–8 weeks to develop. By then, you can use light strategically:", "sz": Pt(10), "c": SLATE, "sa": Pt(8)},
        {"t": "• Bright natural light in the morning sets the circadian clock\n• Dimming lights in the hour before bed signals sleep is coming\n• Darkness during the night keeps the clock from resetting too early", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "Melatonin is suppressed by light and released in darkness. A nightlight that seems dim to you may be working against your baby's melatonin release.", "sz": Pt(10), "c": SLATE, "sa": Pt(8)},
    ]
    mtxt(slide, Cm(2), Cm(4.5), Cm(17), Cm(20), body)
    callout(slide, Cm(24.5), w=Cm(17), label="TIMING TIP",
            body="Watch for sleepy cues 10–15 minutes BEFORE the end of the expected awake window and start the wind-down then. Don't wait for yawning and eye-rubbing — by then, cortisol may already be rising.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)

def p_ch2b(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Two")
    footer(slide, 11)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER TWO", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "The 45-Minute Intruder",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.6),
        "Understanding baby sleep cycles — the chart that changed everything for me.", Pt(10), TEAL, i=True)
    # Sleep cycle table
    table_data = [
        ("STAGE", "WHAT'S HAPPENING", "DURATION"),
        ("NREM 1–2 (Light)", "Drowsy, easily woken, may startle or twitch", "10–15 min"),
        ("NREM 3 (Deep)", "Harder to wake, breathing slows, full body relaxation", "15–20 min"),
        ("REM (Active)", "Eyes flutter, facial movements, most dreams occur here", "10–15 min"),
        ("Transition", "Baby surfaces, may fully wake without sleep associations", "~45 min total"),
    ]
    y = Cm(5.4)
    col_widths = [Cm(5.5), Cm(8.5), Cm(3)]
    for i, row in enumerate(table_data):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(0.9), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for j, cell in enumerate(row):
                txt(slide, x + Cm(0.2), y + Cm(0.15), col_widths[j], Cm(0.6),
                    cell, Pt(8.5), WHITE, b=True)
                x += col_widths[j]
            y += Cm(0.9)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(1), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.2), col_widths[j], Cm(0.6),
                    cell, Pt(8.5), color, b=bold)
                x += col_widths[j]
            y += Cm(1)
    body = [
        {"t": "When baby surfaces from a cycle and doesn't know how to resettle, you get the '45-minute nap' — they wake, can't link cycles, end of nap. Teaching a baby to resettle (the core of sleep training) is teaching them to get back through the transition on their own.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "What 'Sleeping Through the Night' Actually Means", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Reset expectations: 'sleeping through' is clinically defined as a 5–6 hour stretch. NOT 7pm to 7am. A 3-month-old doing a 6-hour stretch IS sleeping through the night. That is a win.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "By 6 months: 8–10 hours is achievable. By 9–12 months: 10–12 hours becomes normal. It's a process, not a switch.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Progress over perfection. Every longer stretch is a victory.", "sz": Pt(10.5), "c": GOLD, "b": True, "i": True, "fn": FONT_HEADING},
    ]
    mtxt(slide, Cm(2), Cm(11), Cm(17), Cm(16), body)


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 3: READING SLEEP CUES
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch3_open(prs):
    ch_opener(prs, "03", "CHAPTER THREE",
              "Reading Your\nBaby's Sleep Cues\nBefore It's\nToo Late",
              "If sleep timing were a game, most of us are playing it\non hardest difficulty because we don't know the rules.\nReading cues is learning the rules.", 12)

def p_ch3a(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Three")
    footer(slide, 13)
    page_top(slide, "CHAPTER THREE", "The Sleep Cue Traffic Light", "Chapter Three")
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.6),
        "Think of your baby's readiness to sleep as a traffic light.", Pt(10), TEAL, i=True)
    # 3 stage cards with detailed cues
    stages = [
        ("GREEN", "Early Cues", TEAL,
         ["Quieting down, less active", "Gazing into middle distance", "Slightly slower movements", "Reduced social smiling", "Subtle change in expression"],
         "ACT NOW. Start wind-down.\nThis is your window."),
        ("YELLOW", "Optimal Cues", AMBER,
         ["Yawning (the classic)", "Eye rubbing or ear pulling", "Red eyebrows, red-rimmed eyes", "Losing interest in toys", "Slumping posture, less muscle tone", "Clinginess, fussiness ramping"],
         "GO TIME. Get to crib NOW.\nYou're right on time."),
        ("RED", "Too Late Cues", RUST,
         ["Full crying or wailing", "Back-arching", "Second wind, energized again", "Hysterical, inconsolable"],
         "DAMAGE CONTROL.\nDim everything, slow down."),
    ]
    x = Cm(2)
    for tag, sub, color, cues, cta in stages:
        card_h = Cm(13)
        shp(slide, x, Cm(5.3), Cm(5.3), card_h, color, MSO_SHAPE.ROUNDED_RECTANGLE)
        txt(slide, x, Cm(5.5), Cm(5.3), Cm(0.7), tag, Pt(13), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
        txt(slide, x, Cm(6.3), Cm(5.3), Cm(0.5), sub, Pt(9), WHITE, al=PP_ALIGN.CENTER)
        cue_text = "\n".join(["• " + c for c in cues])
        txt(slide, x + Cm(0.3), Cm(7.4), Cm(4.7), Cm(7.5), cue_text, Pt(8.5), WHITE)
        # CTA box
        shp(slide, x + Cm(0.3), Cm(15.5), Cm(4.7), Cm(2.5), NAVY_MID, MSO_SHAPE.ROUNDED_RECTANGLE)
        txt(slide, x + Cm(0.3), Cm(15.8), Cm(4.7), Cm(2), cta, Pt(8), WHITE, b=True, al=PP_ALIGN.CENTER)
        x += Cm(5.7)
    callout(slide, Cm(19), w=Cm(17), label="RED-LIGHT RECOVERY",
            body="When you hit a red light: dim the lights, lower your voice, add extra steps to the wind-down. It'll take longer but you can still get there. Give yourself and your baby grace. Tomorrow: aim for green.",
            accent=RUST, bg_clr=RED_LT, h=Cm(2.5), text_color=NAVY, label_clr=RUST)
    callout(slide, Cm(22), w=Cm(17), label="THE 7-DAY SLEEP LOG",
            body="Track wake times, sleep times, mood for 5–7 days. You don't need an app — a notebook works. Just note: wake time, nap start/end, bedtime, night wakings, one-word mood. Patterns emerge within a week. Patterns give you power.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(3.2), text_color=NAVY, label_clr=AMBER)

def p_ch3b(prs):
    """Awake Windows by Age Reference."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Three — Reference")
    footer(slide, 14)
    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4), "REFERENCE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Awake Windows by Age",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.3), Cm(17), Cm(0.5),
        "These are averages. Your baby may run 15 minutes either side. The shape is what matters.",
        Pt(9), SLATE, i=True)
    # Table
    rows = [
        ("AGE", "AWAKE WINDOW", "NAPS/DAY", "NOTES"),
        ("0–4 weeks", "45–60 min", "4–5", "Watch for early cues; very short windows"),
        ("1–2 months", "60–90 min", "4–5", "Gradually extending"),
        ("2–3 months", "75–90 min", "4", "Circadian rhythm starting"),
        ("3–4 months", "90 min – 2 hrs", "3–4", "4-month regression often hits here"),
        ("4–6 months", "2 – 2.5 hrs", "3", "More predictable scheduling begins"),
        ("6–8 months", "2.5 – 3 hrs", "2–3", "Transition to 2 naps often starting"),
        ("8–10 months", "3 – 3.5 hrs", "2", "2-nap schedule solidifies"),
        ("10–12 months", "3.5 – 4 hrs", "2", "Approaching toddler territory"),
        ("12–18 months", "4 – 5 hrs", "1–2", "Transitioning to 1 nap"),
        ("18–24 months", "5 – 6 hrs", "1", "1 solid nap, longer nights"),
    ]
    y = Cm(5.2)
    col_widths = [Cm(2.8), Cm(3.5), Cm(2.2), Cm(8.5)]
    for i, row in enumerate(rows):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(0.9), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for j, cell in enumerate(row):
                txt(slide, x + Cm(0.2), y + Cm(0.15), col_widths[j], Cm(0.6),
                    cell, Pt(8.5), WHITE, b=True)
                x += col_widths[j]
            y += Cm(0.9)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(0.9), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.2), col_widths[j], Cm(0.5),
                    cell, Pt(8), color, b=bold)
                x += col_widths[j]
            y += Cm(0.9)
    callout(slide, Cm(15), w=Cm(17), label="THE MOST COMMON TIMING MISTAKE",
            body="Putting baby down at a fixed clock time regardless of when they woke from their last nap. Count FORWARD from wake time, not BACKWARD from a target. 'We always do 7pm' will fail you.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(2.7), text_color=NAVY, label_clr=AMBER)

def p_ch3c(prs):
    """The Crib Hour."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Three — The Crib Hour")
    footer(slide, 15)
    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4), "TECHNIQUE · CHAPTER THREE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "The Crib Hour",
        Pt(20), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.5),
        "The nap technique that teaches sleep-cycle linking.", Pt(10), GOLD, i=True)
    body = [
        {"t": "If your baby consistently wakes after 30–45 minutes of every nap and cannot resettle — they are a one-cycle napper. Their brain is surfacing from the first sleep cycle and does not yet know how to link into the next one. The Crib Hour teaches them.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "What it is", "sz": Pt(12), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "After your baby goes down for a nap, give them ONE FULL HOUR in the crib — regardless of when they wake. If they surface at 28 minutes, leave them (as long as they're not in distress) until 60 minutes have passed from when they first went down. Do not collect them at the first sound.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "Why it works", "sz": Pt(12), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "A baby left in a calm, dark, white-noise environment after waking will often resettle from boredom within 5–10 minutes — linking naturally into a second cycle. Each time, the brain practices independent cycle-linking. Within ONE WEEK of consistent practice, many 30-minute nappers become 60–90 minute nappers.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(12)},
    ]
    mtxt(slide, Cm(2), Cm(5.2), Cm(17), Cm(13), body)
    # Rules table
    txt(slide, Cm(2), Cm(17), Cm(17), Cm(0.6), "The Rules at a Glance",
        Pt(13), NAVY, b=True, fn=FONT_HEADING)
    rules = [
        ("Calm or intermittent sounds", "Leave them. Self-settling is in progress."),
        ("Escalating, distressed cry", "Go in, offer minimal comfort, resettle and leave."),
        ("After 60 minutes", "Always go in. End the nap regardless."),
        ("Environment required", "Same as night: full blackout, white noise running."),
        ("Age to begin", "From around 4 months, when sleep cycles mature."),
    ]
    y = Cm(17.8)
    for situation, response in rules:
        row = shp(slide, Cm(2), y, Cm(17), Cm(0.9), WHITE, MSO_SHAPE.RECTANGLE)
        row.line.color.rgb = CREAM_MID
        row.line.width = Pt(0.3)
        txt(slide, Cm(2.2), y + Cm(0.2), Cm(6), Cm(0.6), situation, Pt(8.5), NAVY, b=True)
        txt(slide, Cm(8.5), y + Cm(0.2), Cm(10.3), Cm(0.6), response, Pt(8.5), SLATE)
        y += Cm(0.9)
    callout(slide, Cm(23), w=Cm(17), label="THE CRIB HOUR IS NOT CRY-IT-OUT",
            body="You are not ignoring your baby. You are giving them the space to practice a skill. Watch and listen throughout. If something feels wrong, always go in.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(2.5), text_color=NAVY, label_clr=TEAL)


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 4: BEDTIME ROUTINE
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch4_open(prs):
    ch_opener(prs, "04", "CHAPTER FOUR",
              "Building a Bedtime\nRoutine That\nActually Sticks",
              "A bedtime routine is not just cute events before sleep.\nIt is a neurological signal. Done consistently, the routine\nitself triggers the brain's sleep response.", 16)

def p_ch4a(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Four")
    footer(slide, 17)
    page_top(slide, "CHAPTER FOUR", "The Pavlov Effect for Babies", "Chapter Four")
    body = [
        {"t": "Pavlov's dogs learned to salivate at a bell because the bell reliably predicted food. Your baby can learn to feel sleepy at the sight of a bath or sound of a lullaby — because those things reliably predict sleep.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "The key word is CONSISTENT. The routine doesn't need to be elaborate. It doesn't need lavender wash or a $300 sound machine. It needs to be the SAME, in the SAME ORDER, every single night.", "sz": Pt(10), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "The Four Components of an Effective Bedtime Routine", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(10)},
        {"t": "1. The Transition Signal", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
        {"t": "Marks the beginning of wind-down. Turning off TV, closing blinds, saying a phrase like 'Okay, it's sleepy time!' Tells the brain: the active part of the evening is over.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "2. The Wind-Down Activity", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
        {"t": "Lower stimulation actively. A warm bath is the gold standard — not because of the lavender, but because immersion in warm water raises body temperature, and the subsequent COOLING after the bath triggers the sleep drive. AVOID: screens, bright lights, rough play, exciting visitors.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "3. The Feeding or Comfort Step", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
        {"t": "Feed them here — but here's the critical piece: do NOT let them fall asleep during the feed. If they always fall asleep at breast or bottle, the feed BECOMES a sleep association. Feed enough to be satisfied, then move to the sleep space. Goal: drowsy but awake.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "4. The Sleep Trigger", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
        {"t": "The last thing before you leave the room. A specific song (sung live, not a device), a brief cuddle in the crib, a phrase like 'I love you, goodnight, sleep well.' The final cue. Keep it short. Keep it warm. Keep it the SAME.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(24.5), w=Cm(17), label="ROUTINE TIMING",
            body="The whole routine should take 20–30 minutes. Much shorter and it's not long enough to wind down. Much longer and you risk baby falling asleep DURING the routine instead of in the crib.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)

def p_ch4b(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Four")
    footer(slide, 18)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER FOUR", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Sample Routines by Age",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    # 3 columns - one per age range
    routines = [
        ("Newborn–3 Months", NAVY, [
            "Dim lights 30 min before sleep",
            "Sponge bath or wipe-down",
            "Feed in quiet dim room",
            "Swaddle while still calm/awake",
            "Hold & rock briefly with shushing",
            "Place in crib drowsy but awake",
            "Hand on chest briefly, then leave",
        ]),
        ("3–6 Months", TEAL, [
            "Transition signal: lights dim",
            "Warm bath (5–10 min)",
            "Lotion massage (5 min)",
            "Pyjamas and sleep sack",
            "Feed in dim room — keep awake",
            "1–2 short songs",
            "Into crib drowsy but awake",
        ]),
        ("6–18 Months", PURPLE, [
            "Clean-up cue ('toys to bed!')",
            "Bath",
            "Pyjamas and sleep sack",
            "2–3 short books in chair",
            "Feed/milk (not to sleep)",
            "Goodnight phrase",
            "Into crib, white noise on",
        ]),
    ]
    x = Cm(2)
    for title, color, steps in routines:
        card_h = Cm(15)
        shp(slide, x, Cm(4.7), Cm(5.3), card_h, WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        # Color header
        shp(slide, x, Cm(4.7), Cm(5.3), Cm(1.2), color, MSO_SHAPE.ROUNDED_RECTANGLE)
        shp(slide, x, Cm(5.7), Cm(5.3), Cm(0.3), color, MSO_SHAPE.RECTANGLE)
        txt(slide, x, Cm(4.9), Cm(5.3), Cm(0.8), title, Pt(11), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
        # Steps
        sy = Cm(6.2)
        for i, step in enumerate(steps):
            txt(slide, x + Cm(0.3), sy, Cm(0.5), Cm(0.5), str(i+1) + ".", Pt(8.5), color, b=True)
            txt(slide, x + Cm(0.8), sy, Cm(4.3), Cm(1.2), step, Pt(8), SLATE)
            sy += Cm(1.2)
        x += Cm(5.7)
    body = [
        {"t": "The Most Important Rule: Same Order. Every Night.", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Rotate the songs. Switch the books. But the ORDER stays the same. The order is the signal. Once your baby's brain maps it, each step starts to turn down their alertness. By the last step, they're already halfway to sleep.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "Give it 7 days of consistency before evaluating. You're building a neural pathway, and that takes repetition.", "sz": Pt(10), "c": GOLD, "b": True, "i": True},
    ]
    mtxt(slide, Cm(2), Cm(20), Cm(17), Cm(7), body)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 5: ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch5_open(prs):
    ch_opener(prs, "05", "CHAPTER FIVE",
              "Setting the Stage:\nThe Sleep\nEnvironment",
              "You can have the perfect routine and the perfect timing —\nand still have a rough night if the environment\nis working against you.", 20)

def p_ch5a(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Five")
    footer(slide, 21)
    page_top(slide, "CHAPTER FIVE", "Darkness, Sound & Temperature", "Chapter Five")
    body = [
        {"t": "Darkness: The Non-Negotiable", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "TRUE darkness — where you genuinely cannot see your hand in front of your face — is the single most impactful environmental change most families can make. Melatonin is significantly reduced by even low-level light. That little nightlight that seems harmless? If your baby can see it, it's working against their sleep hormone.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "• Use blackout curtains or blinds — not 'room darkening' — true blackout\n• Cover any glowing LEDs on monitors with electrical tape\n• If you need a nightlight for safety during feeds, use a RED-spectrum light\n• The hallway light coming under the door matters — use a draft stopper", "sz": Pt(9), "c": SLATE, "sa": Pt(14)},
        {"t": "White Noise: Your Baby's Sleep Soundtrack", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "The womb is loud. Really loud — about 80–85 decibels, similar to a vacuum cleaner. So the perfectly silent nursery that feels peaceful to YOU actually feels startlingly quiet to a newborn.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "White noise helps two ways: recreates a familiar sound environment, AND masks household sounds (dog barking, sibling running, delivery at the door) that wake babies in light sleep.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Temperature: The Goldilocks Factor", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Ideal room temperature: 68–72°F (20–22°C). Too warm and babies rouse easily. Too cold and they can't maintain comfortable sleep. Babies can't regulate body temperature like adults — dress them based on the ROOM TEMP, not what feels comfortable to you.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Rule of thumb: dress your baby in ONE more layer than you'd wear comfortably to sleep.", "sz": Pt(9.5), "c": NAVY, "b": True},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(25), w=Cm(17), label="WHITE NOISE SETUP",
            body="Play at 60–65 decibels — similar to shower noise — measured where baby's head will be. Don't put the machine in the crib or right next to the ear. A few feet away, running ALL night, is the goal. Fan, static, rain, brown noise — all work. Pick one and stick with it.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(2.5), text_color=NAVY, label_clr=TEAL)


def p_ch5b(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Five")
    footer(slide, 22)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER FIVE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "The Crib & The Room",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    body = [
        {"t": "The Crib Setup: Safe and Sleep-Inducing", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "AAP guidelines: firm flat mattress, fitted sheet, NOTHING ELSE. No bumpers, pillows, stuffed animals, or positioners. This isn't just about safety — a clear, simple sleep space is also better for sleep. Babies don't need stimulation in their sleep environment.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "After 12 months (when SIDS risk drops significantly), you can introduce a comfort object — a small lovey or stuffed animal. Many babies form genuine attachments that help them resettle at night.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "The 'Away From the Action' Principle", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "If possible, baby's sleep space should feel removed from the busyness of the house. This doesn't mean silent — ambient household noise is fine and helps babies habituate. But a nursery right next to the kitchen where dishes are clattering, or adjacent to a loud playroom, is a harder environment.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Small space? White noise becomes more critical. Room-sharing? Use a partition or curtain to create visual separation, and keep light minimal during night feeds.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Room-Sharing Note", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "The AAP recommends ROOM-sharing — but NOT bed-sharing — for the first 6–12 months. This reduces SIDS risk while keeping baby in a safe, separate sleep surface. When transitioning out of your room, do it during a stable period — not during illness, travel, or a regression.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(24.5), w=Cm(17), label="THE BOTTOM LINE",
            body="The room doesn't need to be perfect. It needs to be CONSISTENTLY set up for sleep. Done is better than perfect here. Make the changes you can make tonight. Plan the rest for this weekend.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 6: SLEEP TRAINING METHODS (DETAILED)
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch6_open(prs):
    ch_opener(prs, "06", "CHAPTER SIX",
              "The Big Sleep\nTraining Debate:\nFinding What Fits\nYOUR Baby",
              "I've used almost every method across my six kids.\nSome worked beautifully. Some didn't fit my baby's temperament.\nHere's the full picture.", 23)

def p_ch6a(prs):
    """Methods 1 & 2: Extinction + Ferber"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Six")
    footer(slide, 24)
    page_top(slide, "CHAPTER SIX", "Method 1: Extinction (Cry It Out)", "Chapter Six")
    body = [
        {"t": "What it is: You put baby down awake and don't return until morning (or a pre-set feeding time). No checks, no response unless there's genuine concern.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "The research: Multiple studies show extinction does NOT cause long-term harm to emotional development, cortisol levels, or attachment when done after appropriate age (4–6+ months). Tends to produce results fastest — often 3–5 days.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Who it fits: Families struggling severely and needing fast results. Babies who are highly persistent — who actually escalate MORE with parental check-ins. Parents who can stay consistent without exception.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "The honest truth: It is hard. Even knowing the research, sitting in another room while your baby cries is one of the hardest things you'll do. Make sure both partners are aligned BEFORE starting. Have a plan for the first few nights.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Method 2: Ferber (Graduated Extinction)", "sz": Pt(14), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "What it is: Check on baby at gradually increasing intervals — 3 min, 5 min, 10 min, 15 min (cap there) — without picking up. Verbal reassurance only.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Day-by-Day Ferber Schedule:", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(4)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(13), body)
    # Ferber day chart
    ferber = [
        ("DAY", "1ST WAIT", "2ND WAIT", "3RD WAIT", "MAX WAIT"),
        ("Day 1", "3 min", "5 min", "10 min", "10 min"),
        ("Day 2", "5 min", "10 min", "12 min", "12 min"),
        ("Day 3", "10 min", "12 min", "15 min", "15 min"),
        ("Day 4+", "12 min", "15 min", "17 min", "17 min"),
    ]
    y = Cm(17.3)
    col_w = Cm(3.4)
    for i, row in enumerate(ferber):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(0.8), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for cell in row:
                txt(slide, x + Cm(0.2), y + Cm(0.15), col_w, Cm(0.5), cell, Pt(8), WHITE, b=True, al=PP_ALIGN.CENTER)
                x += col_w
            y += Cm(0.8)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(0.8), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.2), col_w, Cm(0.5), cell, Pt(8.5), color, b=bold, al=PP_ALIGN.CENTER)
                x += col_w
            y += Cm(0.8)
    callout(slide, Cm(21.5), w=Cm(17), label="WHEN FERBER ISN'T A FIT",
            body="If your baby ESCALATES with each check-in instead of calming between them — Ferber may not be right. They see you, you leave again, they're more upset. Switch to extinction or Chair Method.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)
    callout(slide, Cm(24.5), w=Cm(17), label="DURING CHECK-INS",
            body="Stay 30 seconds max. Pat their back briefly. Say a calm phrase: 'I love you. It's sleep time.' Do NOT pick up. Do NOT turn on lights. Do NOT engage. Then leave.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(2.5), text_color=NAVY, label_clr=TEAL)


def p_ch6b(prs):
    """Methods 3, 4, 5: Chair, Fading, Pick Up/Put Down"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Six")
    footer(slide, 25)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER SIX", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "The Gentler Methods",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    body = [
        {"t": "Method 3: Chair Method (Sleep Lady Shuffle)", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "What it is: Sit next to the crib until baby falls asleep. Every few nights, move your chair progressively further from the crib until you're out of the room.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "Week 1: Chair beside crib. You're there but not engaging. Brief shushing/reassurance only.\nWeek 2: Chair halfway across the room.\nWeek 3: Chair at the doorway.\nWeek 4: Chair just outside, door open.\nWeek 5: Out of sight, door open.\nWeek 6: Door closed.", "sz": Pt(9), "c": SLATE, "sa": Pt(8)},
        {"t": "Best for: Sensitive babies who need parental presence. Parents not ready to step back fully. Slower (2–4 weeks) but gentler.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Method 4: Fading", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "What it is: Gradually reduce your involvement over time. Less rocking each night, less nursing, less of the current sleep association — until baby is independent.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "Example: If you currently rock for 20 min — Night 1: 18 min. Night 2: 16 min. Night 3: 14 min. Continue reducing by 2 min each night until you're rocking for 0.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "Best for: Gentlest method. Adaptable babies tolerant of gradual change. Parents who want low/no crying. Easier to stall out — full removal of association required.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Method 5: Pick Up / Put Down", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "What it is: Put baby down. If they cry, pick up to calm. Put down again. Repeat until they fall asleep.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "Best for: Younger babies (3–5 months) needing high support. Parents who can't tolerate extended crying. Can take a long time per night with older or more persistent babies.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(22), body)
    callout(slide, Cm(25), w=Cm(17), label="THE TRUTH ABOUT METHODS",
            body="There is NO universally 'best' method. The best one is the one you can commit to consistently. A gentle method done inconsistently is LESS effective — and harder on baby — than a stricter method done with unwavering consistency.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)

def p_ch6c(prs):
    """Method comparison table + when to start"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Six")
    footer(slide, 26)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER SIX", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Choose Your Method",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.3), Cm(17), Cm(0.5),
        "Direct comparison — pick what fits your family.", Pt(10), GOLD, i=True)
    # Comparison table
    methods = [
        ("METHOD", "CRY LEVEL", "SPEED", "BEST FOR"),
        ("Extinction (CIO)", "High", "3–5 days", "Persistent babies; severe sleep deprivation"),
        ("Ferber", "Moderate", "5–7 days", "Most temperaments; parents wanting to do something"),
        ("Chair Method", "Low–Mod", "2–4 weeks", "Sensitive babies; gradual approach"),
        ("Fading", "Low", "3–4+ weeks", "Gentlest; adaptable babies; no-cry priority"),
        ("Pick Up/Put Down", "Low", "Variable", "3–5 month olds; high-support preference"),
    ]
    y = Cm(5.3)
    col_w = [Cm(4.5), Cm(2.7), Cm(2.7), Cm(7.1)]
    for i, row in enumerate(methods):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(0.9), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for j, cell in enumerate(row):
                txt(slide, x + Cm(0.2), y + Cm(0.2), col_w[j], Cm(0.5), cell, Pt(8.5), WHITE, b=True)
                x += col_w[j]
            y += Cm(0.9)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(1.1), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.3), col_w[j], Cm(0.6), cell, Pt(8.5), color, b=bold)
                x += col_w[j]
            y += Cm(1.1)
    body = [
        {"t": "When to Start Sleep Training", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Most paediatricians and consultants agree 4–6 months is the earliest most babies are developmentally ready. Before that, night feeding is often genuinely necessary and the nervous system isn't mature enough for independent settling.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "Do NOT start during: illness, teething peaks, a move, travel, or a developmental leap. Wait for a stable 2-week window with no major disruptions ahead.", "sz": Pt(10), "c": SLATE, "sa": Pt(10)},
        {"t": "Pick your method. Pick your start date. Commit. Consistency is everything.", "sz": Pt(11), "c": GOLD, "b": True, "i": True},
    ]
    mtxt(slide, Cm(2), Cm(13), Cm(17), Cm(11), body)
    callout(slide, Cm(24.5), w=Cm(17), label="DECISION SHORTCUT",
            body="If you need fast results AND can stay consistent → Extinction. If you need 'something to do' during crying → Ferber. If your baby is very sensitive → Chair Method. If you want zero crying → Fading. Pick one TONIGHT. Don't second-guess.",
            accent=TEAL, bg_clr=BLUE_LT, h=Cm(2.5), text_color=NAVY, label_clr=TEAL)


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 7: NIGHT WAKINGS & RESET PROTOCOL
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch7_open(prs):
    ch_opener(prs, "07", "CHAPTER SEVEN",
              "Night Wakings\n& The Reset\nProtocol",
              "How you handle wakings makes the difference between\nwaking that's gradually shrinking and waking\nthat stays stubbornly in place for months.", 28)

def p_ch7a(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Seven")
    footer(slide, 29)
    page_top(slide, "CHAPTER SEVEN", "The Wait-Before-You-Go Principle", "Chapter Seven")
    body = [
        {"t": "This is hard when every instinct says GO. But here's what I've learned: many babies who wake and make noise at night are NOT fully awake. They're cycling through a light sleep phase. If you go in immediately, you fully wake them. If you wait 2–3 minutes, there's a real chance they'll settle on their own.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "This doesn't mean letting your baby scream while you count seconds. It means PAUSING before acting — listening for whether sounds are escalating or quieting. Within days, you'll know the difference between 'I'm cycling' noises and 'I genuinely need you' cry.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "The Lovey Strategy", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "A lovey is a small soft comfort object — stuffed animal or small blanket with soft toy. When introduced consistently, many babies transfer their comfort-seeking from a parent (or breast/bottle) to the lovey.", "sz": Pt(10), "c": SLATE, "sa": Pt(8)},
        {"t": "How to build the association: Keep the lovey near your body or the nursing area during daytime feeds so it picks up your scent. Introduce at bedtime and naps. Once associated, baby can find and hold the lovey at 3am without needing you. APPROPRIATE FROM AROUND 12 MONTHS.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "Night Feeding: Nutritional vs. Habitual", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(15), body)
    # Night feed table
    feed_table = [
        ("AGE", "TYPICAL NIGHT FEEDS", "GUIDANCE"),
        ("0–3 months", "2–4 per night", "Not yet — these are nutritional"),
        ("3–4 months", "1–3 per night", "Work on timing & drowsy-but-awake first"),
        ("4–6 months", "1–2 per night", "Begin gradual reduction if weight is good"),
        ("6–9 months", "0–1 per night", "Most babies can handle 0 with paed OK"),
        ("9+ months", "0 in most cases", "Any waking is likely habitual or comfort"),
    ]
    y = Cm(20.2)
    col_w = [Cm(3.5), Cm(5), Cm(8.5)]
    for i, row in enumerate(feed_table):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(0.8), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for j, cell in enumerate(row):
                txt(slide, x + Cm(0.2), y + Cm(0.15), col_w[j], Cm(0.5), cell, Pt(8), WHITE, b=True)
                x += col_w[j]
            y += Cm(0.8)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(0.9), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.2), col_w[j], Cm(0.6), cell, Pt(8.5), color, b=bold)
                x += col_w[j]
            y += Cm(0.9)

def p_ch7b(prs):
    """Reducing night feeds + habits to avoid"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Seven")
    footer(slide, 30)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER SEVEN", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Reducing Night Feeds & Avoiding Sleep Debt Traps",
        Pt(16), NAVY, b=True, fn=FONT_HEADING)
    body = [
        {"t": "How to Reduce a Night Feed Without Going Cold Turkey", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "BOTTLE FEEDING: Reduce the amount offered at the target waking by 1 oz every 2–3 nights. Your baby gradually stops waking for a feed that isn't worth the effort.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "BREASTFEEDING: Gradually reduce feeding TIME at the target waking — by about 1 minute every 2–3 nights. So if currently 8 min, go to 7, then 6, etc. As the feed becomes less substantial, the waking often disappears.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Always check with your paediatrician before reducing night feeds, especially under 6 months or with weight concerns.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "Habits to Avoid After the First Few Months", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "I call these 'sleep debt traps' — patterns that feel like solutions in the moment but create harder problems over time:", "sz": Pt(10), "c": SLATE, "sa": Pt(8)},
        {"t": "• Feeding to sleep after 4 months — every waking will require a feed to resettle\n• Rocking fully to sleep — they'll need rocking back at every cycle\n• Bringing baby into your bed as a rescue — this becomes expected very quickly\n• Motion sleep for all naps — car, pram, swing sleep doesn't build same sleep pressure", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "None of these make you a bad parent. They make you a HUMAN parent who did what was necessary to survive. Now let's gently undo them.", "sz": Pt(10), "c": GOLD, "b": True, "i": True},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)

def p_ch7c(prs):
    """The Reset Protocol"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Seven — Reset Protocol")
    footer(slide, 31)
    txt(slide, Cm(2), Cm(2.2), Cm(15), Cm(0.4), "PROTOCOL · CHAPTER SEVEN", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "The Reset Protocol",
        Pt(20), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.5),
        "When everything has slipped — start here. The 5-step rescue plan.", Pt(10), TEAL, i=True)
    # 5 steps
    resets = [
        ("1", "Diagnose the root cause",
         "Is it sleep association? Timing? Environment? Partner inconsistency? Regression? Pick ONE primary culprit before fixing anything."),
        ("2", "Fix the environment first",
         "Blackout, white noise, temperature 68–72°F. These are FREE and IMMEDIATE wins. Do this tonight before anything else."),
        ("3", "Reset the routine to original order",
         "Strip back any steps that have crept in. Bath → lotion → pyjamas → feed → song → crib. Print it. Stick it on the door."),
        ("4", "Commit to 5 consecutive nights",
         "Same method, same response, no exceptions. Five consecutive consistent nights resolves most slides completely. No deviations."),
        ("5", "Track and compare",
         "Use the 7-Day Tracker. Compare Night 5 to Night 1. Time to settle, number of wakings, total sleep. The data motivates you when memory fails."),
    ]
    y = Cm(5.3)
    for num, title, body in resets:
        card = shp(slide, Cm(2), y, Cm(17), Cm(2.8), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        card.line.color.rgb = CREAM_MID
        card.line.width = Pt(0.5)
        shp(slide, Cm(2.4), y + Cm(0.6), Cm(1.5), Cm(1.5), TEAL, MSO_SHAPE.OVAL)
        txt(slide, Cm(2.4), y + Cm(0.7), Cm(1.5), Cm(1.3), num, Pt(13), WHITE, b=True, al=PP_ALIGN.CENTER, anc=MSO_ANCHOR.MIDDLE)
        txt(slide, Cm(4.5), y + Cm(0.3), Cm(14), Cm(0.6), title, Pt(11), NAVY, b=True)
        txt(slide, Cm(4.5), y + Cm(1.2), Cm(14), Cm(1.5), body, Pt(9), SLATE)
        y += Cm(2.95)
    callout(slide, Cm(20.5), w=Cm(17), label="ONE SLIP DOES NOT ERASE PROGRESS",
            body="A single difficult night is NOT a regression. Three or more consecutive difficult nights with a CHANGING response pattern is. Know the difference. Then act.",
            accent=NAVY, bg_clr=CREAM_MID, h=Cm(2.5), text_color=NAVY, label_clr=NAVY)
    callout(slide, Cm(23.5), w=Cm(17), label="REGRESSION REFERENCE",
            body="• 4 months: circadian shift  • 8–10 months: separation anxiety  • 12 months: walking  • 18 months: autonomy  • 24 months: imagination. Hold the line during regressions — they pass within 1–4 weeks.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(3), text_color=NAVY, label_clr=AMBER)


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 8: THE SIX SLEEP PERSONALITIES
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch8_open(prs):
    ch_opener(prs, "08", "CHAPTER EIGHT",
              "The Six Sleep\nPersonalities\n(And How I\nCracked Each One)",
              "Six babies. Six completely different little humans.\nSee if your baby recognizes themselves\nin one of these.", 32)

def p_ch8a(prs):
    """Personalities 1, 2, 3"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Eight")
    footer(slide, 33)
    page_top(slide, "CHAPTER EIGHT", "Personalities 1–3", "Chapter Eight")
    body = [
        {"t": "1. The Snacker", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Who they are: Feeds little and often. Has learned to associate feeding with sleep. Wakes frequently throughout the night — not from hunger, but because the breast or bottle is their sleep cue.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "What works: Gradually consolidate feeds (fewer but larger). Use the 'feed, then wake slightly, then settle' sequence at bedtime to break feed-to-sleep association. Introduce a pacifier or lovey as a substitute comfort.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "2. The Overthinker", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Who they are: Alert, curious, deeply interested in everything happening around them. They don't want to miss anything. Fights sleep even when clearly exhausted because the world is too interesting.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "What works: An EARLIER bedtime than you'd think necessary. Extremely low-stimulation wind-down (no mobiles, toys, interactive anything during the last 30 minutes). Often a darker, quieter room than average.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "3. The Sensitive Soul", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Who they are: Picks up on everything — change in your tone, a slightly different bedtime, a new smell in the room. Easily startled, emotionally attuned, prone to more frequent waking during periods of change or stress.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "What works: Extraordinary routine consistency. A calm, regulated caregiver (hard when you're exhausted). A gentler sleep training approach (Fading or Chair over Extinction). Especially mindful of developmental leaps.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    # Image
    pic(slide, "warm_illust", Cm(2), Cm(24.5), w=Cm(17))

def p_ch8b(prs):
    """Personalities 4, 5, 6"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Eight")
    footer(slide, 34)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER EIGHT", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Personalities 4–6",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    body = [
        {"t": "4. The Night Owl", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Who they are: Genuinely seems to be running on a later circadian schedule. Not tired at 7pm — tired at 9 or 10pm — and they'll let you know if you try to put them down before they're ready.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "What works: Gradually shift the schedule earlier over 2–3 weeks (15 min every 2–3 days). Maximize MORNING light exposure immediately upon waking. Shorten the LAST nap of the day to build more sleep pressure by evening.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "5. The Catnapper", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Who they are: Never naps for more than 30–45 minutes. Surfaces from the first sleep cycle and wakes fully — leaving you with a baby who's not fully rested and a window of time too short for anything.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "What works: USE THE CRIB HOUR (Chapter 3). Be in the room at the 40-minute mark to attempt resettling before they fully wake. Optimize the sleep environment — darkness and white noise matter enormously for naps. For some Catnappers, accept a 3-nap schedule that accounts for shorter individual naps.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "6. The Party Animal", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Who they are: Wakes between 1–4am ready to go. Not crying — happy. Chatting. Playing with their feet. They're having a great time. You are not.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "What works: Rule out an early bedtime CAUSING the early waking (sometimes moving bedtime LATER by 15–30 min solves this). Absolute darkness to prevent circadian clock triggering. Do NOT engage with the wakeful period — no lights, no play, no stimulation. Make 2am incredibly boring.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(24.5), w=Cm(17), label="COMBINING THE TYPES",
            body="Most babies are a BLEND of two personalities. You might have an Overthinker who's also a Sensitive Soul, or a Snacker who's also a Party Animal (baby #5 — she's in college now and still stays up too late). Use the combination to tailor your approach.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 9: COMMON MISTAKES
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch9_open(prs):
    ch_opener(prs, "09", "CHAPTER NINE",
              "Common Mistakes\nExhausted Parents\nMake (I Made\nThem All)",
              "There's no shame in this chapter. These are mistakes\nborn from desperation and love. I made every single\none across my six kids.", 35)

def p_ch9a(prs):
    """Mistakes 1-4"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Nine")
    footer(slide, 36)
    page_top(slide, "CHAPTER NINE", "Mistakes 1–4", "Chapter Nine")
    body = [
        {"t": "Mistake 1: The Moving Goalpost", "sz": Pt(12), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "You start a method. Night 2 feels awful, you go in and rock to sleep. Feel guilty, try again. By Day 5 you've tried 3 approaches and your baby has no idea what's coming.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(4)},
        {"t": "THE FIX: Pick a method and commit for at least 5–7 consecutive nights. Even the hard ones. Inconsistency is more confusing and distressing than a firm, predictable approach.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(12)},
        {"t": "Mistake 2: Skipping the Wake Window", "sz": Pt(12), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Desperate to get them down. Put them in the crib at the first yawn. They don't settle. You try for 45 min. They're not actually tired enough yet.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(4)},
        {"t": "THE FIX: Track awake windows and TRUST them. A baby who isn't tired enough yet will tell you. Don't fight it — work with their biology.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(12)},
        {"t": "Mistake 3: The Nap Trap", "sz": Pt(12), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Long afternoon naps sound wonderful. But a baby who naps 2 hours at 4pm may not be ready for sleep at 7pm. Too much daytime sleep STEALS from the night.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(4)},
        {"t": "THE FIX: Cap afternoon naps based on schedule needs. For most babies over 3 months, the LAST nap should END at least 2 hours before bedtime, and shouldn't be the longest nap of the day.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(12)},
        {"t": "Mistake 4: Rescuing Too Fast", "sz": Pt(12), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Baby stirs at 11pm. You're in there in 30 seconds because you don't want them to fully wake up. But in those 30 seconds you've INTERRUPTED a resettling process that was just beginning.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(4)},
        {"t": "THE FIX: Wait 2–5 minutes before going in for wakings without crying. Listen carefully. Give them the chance to surprise you.", "sz": Pt(9.5), "c": NAVY, "b": True},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(22), body)

def p_ch9b(prs):
    """Mistakes 5-7"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Nine")
    footer(slide, 37)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER NINE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Mistakes 5–7",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    body = [
        {"t": "Mistake 5: Treating Weekends Differently", "sz": Pt(12), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Weekends = flexibility. Kids up later, schedule slides. For ADULTS this is fine. For a baby in active sleep training, a 90-min schedule shift on Saturday can UNDO 5 days of progress.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(4)},
        {"t": "THE FIX: Hold the schedule 7 days a week during active training. After 2–3 weeks of consistent independent sleep, you have more room for occasional flexibility.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "Mistake 6: Waiting for Perfect Conditions", "sz": Pt(12), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Always something. Trip next month. Holiday. Tooth that might be coming. There's NEVER a perfect time. There will always be a leap, a holiday, a cold season approaching.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(4)},
        {"t": "THE FIX: Pick a 2-week window with no major events or travel and START. Done is infinitely better than theoretically perfect.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "Mistake 7: Giving Up at the Extinction Burst", "sz": Pt(12), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "This is the sneaky one. First few nights get better. Then on Night 4 or 5, it suddenly gets WORSE. This is the EXTINCTION BURST — behavior intensifying ONE LAST TIME before it fades.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(4)},
        {"t": "THE FIX: Know the burst is coming and PLAN for it. Write a note. Tell your partner. Put it on the fridge. 'Night 4–5 might be hard. This is normal. Do not give up.' Forewarned is forearmed.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "If you've made these mistakes — including all of them — you're not failing. You're parenting. Now you have the playbook.", "sz": Pt(11), "c": GOLD, "b": True, "i": True, "fn": FONT_HEADING},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(22), body)
    callout(slide, Cm(25), w=Cm(17), label="THE EXTINCTION BURST IN ONE SENTENCE",
            body="When something stops working (your baby's old strategy of crying-until-rescued), they try harder before they give up. Hold the line on Night 3.",
            accent=NAVY, bg_clr=CREAM_MID, h=Cm(2), text_color=NAVY, label_clr=NAVY)


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 10: STAYING CONSISTENT
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch10_open(prs):
    ch_opener(prs, "10", "CHAPTER TEN",
              "Staying Consistent\nWhen You're\nRunning on Empty",
              "Strategy only gets you so far.\nImplementation is where sleep training\nactually lives.", 38)

def p_ch10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Ten")
    footer(slide, 39)
    page_top(slide, "CHAPTER TEN", "Surviving the Hard Nights", "Chapter Ten")
    body = [
        {"t": "Before You Start: Non-Negotiable Conversations", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "If you have a co-parent or anyone in nighttime care, you need to be FULLY aligned before starting. Not mostly. Fully. Sleep training done by one parent and undone by another isn't just ineffective — it's HARDER on baby than either approach done consistently.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Decide in advance: if one parent is struggling at 2am, the other holds the line. Take turns being the strong one.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "The Night-by-Night Survival Plan", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Here is how I survived the hard nights — practically:", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "• EAR PROTECTION: If you're not the responding parent, ear plugs or headphones playing something take the physical edge off. Sounds counterintuitive — makes you significantly more capable of staying consistent.\n\n• THE 'WRITE IT DOWN' RULE: Before you go in, write down the time, how long they've been crying, whether it's escalating. Gives your rational brain something to do — and often reveals the crying is shorter than it feels.\n\n• THE 'GO OUTSIDE' RULE: If you're staying back and can't take it, go outside for 60 seconds. Fresh air, brief physical separation, a moment to breathe. Helps more than you'd think.\n\n• THE JOURNAL: Track each night's progress. Seeing Night 1 was 47 minutes, Night 3 was 22, Night 5 was 8 — incredibly motivating when Night 4 feels endless.", "sz": Pt(9), "c": SLATE, "sa": Pt(14)},
        {"t": "When You Slip Up", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "You will slip. You'll have a night where you crack and bring them into bed, or rock them fully to sleep because everyone is beyond their limit. This is human. This is parenting. This does not mean starting over from scratch.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "If you slip: acknowledge it, don't catastrophize, get back on plan the very next night. ONE night doesn't undo a week. THREE nights of deviation in a row might require a restart. Be honest.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(25), w=Cm(17), label="WHEN IT GETS HARD",
            body="Remember your WHY specifically. Picture in detail: a well-rested family. The hours you'll get back. The patience you'll have for your toddler. The conversations with your partner. The shower you'll take. It's coming. Keep going.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 11: TODDLER SLEEP
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch11_open(prs):
    ch_opener(prs, "11", "CHAPTER ELEVEN",
              "Toddler Sleep —\nWhen Babies Become\nLittle Negotiators",
              "Your baby has become a tiny, extremely opinionated,\nsurprisingly persuasive toddler who has discovered\nthat bedtime is negotiable. It is not.", 40)

def p_ch11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Eleven")
    footer(slide, 41)
    page_top(slide, "CHAPTER ELEVEN", "The Toddler Rule Book", "Chapter Eleven")
    body = [
        {"t": "Why Toddler Sleep Is Different", "sz": Pt(12), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Toddler challenges are less about biology, more about development. Between 18 months and 3 years: asserting autonomy, developing theory of mind, discovering they have power. Beautiful developmentally, difficult practically.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(12)},
        {"t": "Common disruptions: the curtain call (one more thing — water, hug, question, fear), boundary testing, nap refusal, night terrors, the 5am wake.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Limits With Warmth: The Rules", "sz": Pt(12), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "Toddlers need limits. Not because you're controlling — predictable limits create SAFETY and reduce anxiety.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "ONE PASS RULE", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(2)},
        {"t": "After bedtime, your toddler gets ONE pass — one 'get out of bed free' for any reason. After it's used, they stay in bed. Hang an actual visual pass on the door for under-3s.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "CONSISTENT RESPONSE", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(2)},
        {"t": "Every time they call out or come out after the pass, the SAME response: 'It's sleep time. Back to bed.' Warm, firm, boring. Same words every time.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "THE GOODBYE RITUAL", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(2)},
        {"t": "Something they can count on to mark the end — special handshake, specific song. Always the same. Signals: this is actually the end, not a negotiating position.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
        {"t": "OK-TO-WAKE CLOCK", "sz": Pt(11), "c": NAVY, "b": True, "sa": Pt(2)},
        {"t": "A clock that glows green when it's okay to get up. Game-changing for early risers.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(24), w=Cm(17), label="THE DOOR RULE",
            body="'If you stay in bed, the door stays open. If you come out, the door closes.' Follow through every single time. Not a punishment — a natural consequence. Most toddlers choose the open door within 3–4 nights.",
            accent=NAVY, bg_clr=CREAM_MID, h=Cm(3), text_color=NAVY, label_clr=NAVY)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 12: NIGHT-BY-NIGHT PLAN
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch12_open(prs):
    ch_opener(prs, "12", "CHAPTER TWELVE",
              "Your First Week:\nA Night-by-Night\nGame Plan",
              "All right. You've got the knowledge.\nLet's put it together into an actual plan\nyou can use starting tonight.", 42)

def p_ch12a(prs):
    """Pre-week setup + Nights 1-3"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Twelve")
    footer(slide, 43)
    page_top(slide, "CHAPTER TWELVE", "Pre-Week Setup", "Chapter Twelve")
    body = [
        {"t": "The Day Before You Start", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "1. Set up the room: blackout curtains, white noise positioned and tested, temperature 68–72°F.\n2. Write out your bedtime routine steps in order. Put them somewhere visible.\n3. Decide bedtime target. For most babies: 7–8pm.\n4. Set up a simple sleep log: date, awake times, nap times, night wakings.\n5. Tell your partner / family / anyone helping. Get full alignment.\n6. Do a 'nap day' — watch awake windows closely and feel out your baby's natural rhythm.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(8), body)
    # Nights 1-3 cards
    nights = [
        ("NIGHT 1", "Foundation Night", NAVY,
         "Start the routine at your target time. Calm. Consistent. Predictable. This will likely be the hardest — your baby doesn't know what's happening yet. Stay the course with your chosen method. Log everything. Tonight you're planting the seed. Expect it to take longer. Give yourself grace."),
        ("NIGHT 2", "Signal Night", TEAL,
         "Your baby is starting to notice the pattern. Settling may still take a while, but you'll likely notice shorter periods before they start to quiet. Night wakings may be similar to Night 1. This is normal. Don't evaluate yet — the data isn't in. Stay consistent."),
        ("NIGHT 3", "Turning Point (Maybe) — OR THE EXTINCTION BURST", RUST,
         "Many families see a meaningful shift on Night 3. The routine has started to register. Some babies begin settling significantly faster. BUT this is also when the EXTINCTION BURST may appear — things suddenly getting WORSE before they get better. THIS IS NOT FAILURE. It is proof the old system is breaking down. Hold the line. Tomorrow will be different."),
    ]
    y = Cm(13)
    for tag, sub, color, body_text in nights:
        card_h = Cm(4.3)
        shp(slide, Cm(2), y, Cm(17), card_h, WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        shp(slide, Cm(2), y, Cm(0.3), card_h, color, MSO_SHAPE.RECTANGLE)
        txt(slide, Cm(2.6), y + Cm(0.2), Cm(4), Cm(0.5), tag, Pt(10), color, b=True)
        txt(slide, Cm(7), y + Cm(0.2), Cm(11.5), Cm(0.5), sub, Pt(10), NAVY, b=True)
        txt(slide, Cm(2.6), y + Cm(0.9), Cm(15.8), Cm(3.3), body_text, Pt(8.5), SLATE)
        y += Cm(4.6)

def p_ch12b(prs):
    """Nights 4-7"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Twelve")
    footer(slide, 44)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER TWELVE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Nights 4–7",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    nights = [
        ("NIGHT 4", "The Possible Dip", AMBER,
         "If tonight is harder than Nights 2 and 3, check the note you wrote. The extinction burst is expected. It is temporary. DO NOT change methods tonight. Stay consistent."),
        ("NIGHT 5", "The Breakthrough", TEAL,
         "For many babies, this is the night you realize you haven't heard anything since 7:30pm. If this is you — congratulations. Write it down. Celebrate quietly. If not yet — still normal. Some babies take 7–10 days, especially Sensitive Souls."),
        ("NIGHT 6", "Reinforcement Night", PURPLE,
         "Whatever gains you've made, REINFORCE them tonight by being exactly as consistent as before. NOT the night to relax the routine or push boundaries. Pattern is forming. Protect it."),
        ("NIGHT 7", "Evaluation Night", GREEN_DK,
         "Look at your sleep log. Compare Night 7 to Night 1. What's changed? How much faster is settling? How many fewer/shorter wakings? Even if not where you hoped, there will be progress. Use the data to decide: continue same method, or adjust for week 2."),
    ]
    y = Cm(4.5)
    for tag, sub, color, body_text in nights:
        card_h = Cm(4.5)
        shp(slide, Cm(2), y, Cm(17), card_h, WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
        shp(slide, Cm(2), y, Cm(0.3), card_h, color, MSO_SHAPE.RECTANGLE)
        txt(slide, Cm(2.6), y + Cm(0.2), Cm(4), Cm(0.5), tag, Pt(10), color, b=True)
        txt(slide, Cm(7), y + Cm(0.2), Cm(11.5), Cm(0.5), sub, Pt(10), NAVY, b=True)
        txt(slide, Cm(2.6), y + Cm(0.9), Cm(15.8), Cm(3.5), body_text, Pt(8.5), SLATE)
        y += Cm(4.7)
    callout(slide, Cm(24), w=Cm(17), label="AFTER WEEK ONE",
            body="Most babies show significant improvement within 7–14 days. If at 2 weeks with minimal progress: is the method right for your baby's personality? Are you TRULY consistent? Medical factors to rule out (reflux, ear infections, allergies)? A consult with a paediatric sleep consultant can help. There's no shame in asking for help.",
            accent=GOLD, bg_clr=AMBER_LT, h=Cm(3), text_color=NAVY, label_clr=AMBER)


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 13: BREASTFEEDING & SLEEP
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch13_open(prs):
    ch_opener(prs, "13", "CHAPTER THIRTEEN",
              "Breastfeeding\n& Sleep —\nThe Honest Guide",
              "The intersection of breastfeeding and sleep training\nis the most Googled topic in this space.\nHere's the truth.", 46)

def p_ch13a(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Thirteen")
    footer(slide, 47)
    page_top(slide, "CHAPTER THIRTEEN", "Breastfeeding & Independent Sleep ARE Compatible", "Chapter Thirteen")
    body = [
        {"t": "This is the #1 fear driving purchase hesitation in breastfeeding communities. Address directly: you do NOT have to choose between breastfeeding and sleep training. They work TOGETHER.", "sz": Pt(10), "c": TEAL, "b": True, "sa": Pt(14)},
        {"t": "Nursing-to-Sleep: Association vs. Nutrition", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "A NUTRITIONAL FEED: Baby drinks purposefully, transfers significant volume, feeds with intent. This is real hunger.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "A COMFORT FEED: Brief latch, flutter-sucking, drifts back to sleep. Baby is using the breast as a sleep prop, not eating.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "The goal is to separate the nutritional feeds from the sleep-onset moment. Eliminate the comfort/habit feeds — keep the nutritional ones.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(14)},
        {"t": "How to Gently End a Comfort Feed (The Unlatch Technique)", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "1. Watch for the flutter-suck (slow, gentle, no swallowing)\n2. Slip your finger gently into the corner of baby's mouth\n3. Break the suction softly — they will release\n4. Sit baby up briefly. Rouse them just enough to be drowsy-not-asleep.\n5. Place in crib awake. Calm phrase. Leave.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Dream Feeds for Breastfed Babies", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "A dream feed (10–11pm, without fully waking baby) can extend the first stretch of night sleep by 1–2 hours. Offer for 2–3 weeks, then gradually drop once baby is sleeping through.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "How: Lights off. No talking. Gently lift baby. Latch them while they remain drowsy. Let them feed for 5–8 minutes. Place back in crib. They often don't fully wake.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(22), body)
    # Image
    pic(slide, "breastfeeding", Cm(2), Cm(26), w=Cm(17))

def p_ch13b(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Thirteen")
    footer(slide, 48)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "CHAPTER THIRTEEN", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "When to Drop Night Feeds (Breastfed)",
        Pt(16), NAVY, b=True, fn=FONT_HEADING)
    # Table
    feed_data = [
        ("AGE", "GUIDANCE", "STATUS"),
        ("0–4 months", "Feed on demand. All nutritional.", "DON'T DROP"),
        ("4–6 months", "Reduce to 1–2 feeds. Increase daytime calories.", "REDUCE GRADUALLY"),
        ("6–9 months", "Most can handle 0–1 night feeds.", "ALMOST THERE"),
        ("9+ months", "If weight gain on track, night feeds are habitual.", "READY TO DROP"),
    ]
    y = Cm(4.4)
    col_w = [Cm(3), Cm(9), Cm(5)]
    for i, row in enumerate(feed_data):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(0.9), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for j, cell in enumerate(row):
                txt(slide, x + Cm(0.2), y + Cm(0.2), col_w[j], Cm(0.5), cell, Pt(8.5), WHITE, b=True)
                x += col_w[j]
            y += Cm(0.9)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(1), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.25), col_w[j], Cm(0.6), cell, Pt(8.5), color, b=bold)
                x += col_w[j]
            y += Cm(1)
    body = [
        {"t": "Your Supply Will NOT Disappear", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Your body adjusts to daytime demand within 3–5 days of dropping a night feed. Pump once before bed in the first few days if concerned about engorgement.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "Common Q&A", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Q: Will my supply drop?", "sz": Pt(10), "c": GOLD, "b": True, "sa": Pt(2)},
        {"t": "A: No. Your body adjusts within 3–5 days.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Q: Is my baby actually hungry at night?", "sz": Pt(10), "c": GOLD, "b": True, "sa": Pt(2)},
        {"t": "A: If they feed for less than 5 min and drift off, it's habitual.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Q: Can I still nurse to sleep for naps?", "sz": Pt(10), "c": GOLD, "b": True, "sa": Pt(2)},
        {"t": "A: Ideally no — consistency matters. But bedtime is the priority. Naps can be a transition zone.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "Q: My baby refuses bottles from my partner — what now?", "sz": Pt(10), "c": GOLD, "b": True, "sa": Pt(2)},
        {"t": "A: Common. Have partner offer bottle when baby is HUNGRY but NOT starving (15 min before usual feed). Use a slow-flow nipple. Skin-to-skin during the bottle. Try for 7–10 days before declaring it 'not working.'", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
    ]
    mtxt(slide, Cm(2), Cm(10), Cm(17), Cm(17), body)


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 14: TWINS, NICU, DAYCARE
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch14_open(prs):
    ch_opener(prs, "14", "CHAPTER FOURTEEN",
              "Twins, NICU\n& Daycare —\nSpecial Situations",
              "I have twins. I know this section is overdue.\nThis chapter is for the parents standard\nguides ignore.", 49)

def p_ch14(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Fourteen")
    footer(slide, 50)
    page_top(slide, "CHAPTER FOURTEEN", "Twins, Premature Babies & Daycare", "Chapter Fourteen")
    body = [
        {"t": "Sleep Training Twins", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "The Golden Rule for Twins: When one wakes, wake the other. Synchronize feeds and sleep from Day 1. Train SIMULTANEOUSLY — same method, same night, same response.", "sz": Pt(10), "c": SLATE, "sa": Pt(8)},
        {"t": "Same room? YES. Babies habituate to each other's sounds faster than you'd expect. Separate rooms isn't necessary unless one has a medical condition.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "Accept that one twin will progress faster. That's normal — they have different temperaments. Use the same method for both, and let each one's pace be their pace.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(6)},
        {"t": "If one is sick, pause for THAT twin only. Continue with the other. Resume the sick twin when they recover (3–5 nights to reset).", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Premature & NICU Babies", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "USE CORRECTED AGE for all sleep milestones. A baby born 6 weeks early at 4 months calendar age is developmentally 2.5 months — and their awake windows, sleep needs, and readiness for training reflect that.", "sz": Pt(10), "c": SLATE, "sa": Pt(8)},
        {"t": "Corrected age = calendar age − weeks early. Don't sleep-train until corrected age is 4–6 months at minimum, and your paediatrician confirms baby is ready.", "sz": Pt(9.5), "c": NAVY, "b": True, "sa": Pt(8)},
        {"t": "NICU families carry fear, hypervigilance, and guilt into the sleep journey. That is VALID. You are not being overprotective — you are being a parent who has been through something hard. Honor that. Move at your pace.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Daycare & Nursery Schedules", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "ASK YOUR NURSERY: What time is the last nap? How long? This drives your bedtime.\nACCEPT: Daycare naps are often shorter — compensate with an EARLIER bedtime (sometimes 30 min earlier on daycare days).\nWEEKENDS: Keep the SAME schedule. Consistency across all 7 days matters more than weekend rest.\nGIVE: A one-page summary to your provider (use the Partner Briefing format in Chapter 15).", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    # Image
    pic(slide, "twins_nicu", Cm(2), Cm(24.5), w=Cm(17))

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAPTER 15: FIRST 8 WEEKS
# ═══════════════════════════════════════════════════════════════════════════════

def p_ch15_open(prs):
    ch_opener(prs, "15", "CHAPTER FIFTEEN",
              "The First\n8 Weeks —\nNewborn Period",
              "Sleep training starts at 4 months.\nUntil then, here is what you are building.\nYou are not behind.", 51)

def p_ch15(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Chapter Fifteen")
    footer(slide, 52)
    page_top(slide, "CHAPTER FIFTEEN", "What Newborn Sleep Actually Looks Like", "Chapter Fifteen")
    body = [
        {"t": "What Normal Newborn Sleep Looks Like", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "• 14–17 hours of sleep in 24 hours, in 2–4 hour chunks\n• NO circadian rhythm yet — day and night are meaningless to them\n• Frequent feeding is biologically necessary and expected\n• 'Sleeping through' is NOT a realistic goal before 3–4 months", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "What You CAN Do Now (Foundation Building)", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "• Expose baby to natural light during the day (10–15 min near a window)\n• Keep night feeds DARK, QUIET, and BORING — no eye contact, no talking\n• Start a simple bedtime routine from week 3–4 (bath → feed → swaddle → crib)\n• Practice ONE crib nap per day (even if it's short)\n• Distinguish between active sleep sounds and actual waking — many newborn 'wake' sounds are just sleep cycling", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "The SNOO & Swaddle Question", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Swaddles are appropriate UNTIL baby shows signs of rolling (typically 3–4 months). Stop swaddling immediately when rolling starts — it becomes a SIDS risk.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
        {"t": "The SNOO is a tool, not a crutch — but plan your transition off it BEFORE 5 months to avoid creating a motion dependency that's harder to undo later.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "Common Newborn Sleep Mistakes", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "• Trying to sleep-train before 4 months (too early)\n• Keeping nights bright/loud (delays circadian development)\n• Not feeding frequently enough (leads to overtiredness AND undernutrition)\n• Comparing your newborn to other babies (every newborn is different)\n• Dropping naps early (newborns need 4–5 naps; cutting them = overtiredness)", "sz": Pt(9.5), "c": SLATE, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(24.5), w=Cm(17), label="HOLD THIS CLOSE",
            body="You are not behind. You are not failing. You are building the foundation that makes everything else possible. Some of the most important sleep work in the first 8 weeks looks like 'just feeding and surviving.' That IS the work.",
            accent=GREEN_DK, bg_clr=GREEN_LT, h=Cm(2.5), text_color=NAVY, label_clr=GREEN_DK)

# ═══════════════════════════════════════════════════════════════════════════════
#  PARTNER BRIEFING
# ═══════════════════════════════════════════════════════════════════════════════

def p_partner(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Partner Briefing")
    footer(slide, 53)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "PARTNER BRIEFING", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.6),
        "The One-Pager for the\nPerson Who Hasn't Read the Book",
        Pt(20), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(5.2), Cm(17), Cm(0.6),
        "Print this. Give it to your partner. Consistency requires two people.",
        Pt(10), TEAL, i=True)
    body = [
        {"t": "THE PLAN (in 60 seconds):", "sz": Pt(11), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "1. Bedtime routine: same steps, same order, every night\n2. Baby goes into crib drowsy but awake\n3. When baby cries: we wait [X] minutes before responding\n4. Our response method is: ____________________\n5. We do the SAME thing every time — no exceptions for 7 nights", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "WHY THIS MATTERS:", "sz": Pt(11), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "If one of us holds firm and the other caves at 2am, we teach baby that escalating works. This makes the crying WORSE, not better. Consistency between both of us is the single biggest predictor of success.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "NIGHT 3 WARNING:", "sz": Pt(11), "c": RUST, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Night 3 will be the hardest. This is the EXTINCTION BURST — it means the method is WORKING, not failing. DO NOT change the plan on Night 3. Night 4 is almost always dramatically better.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(14)},
        {"t": "IF YOU'RE DOING THIS ALONE:", "sz": Pt(11), "c": TEAL, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Single parents carrying this weight alone: you are doing something extraordinary. Write your plan down. Read it at 2am when your resolve wavers. You are both parents in one — and that is enough.", "sz": Pt(9.5), "c": SLATE, "sa": Pt(8)},
    ]
    mtxt(slide, Cm(2), Cm(6.2), Cm(17), Cm(18), body)
    pic(slide, "partner", Cm(2), Cm(24.5), w=Cm(17))


# ═══════════════════════════════════════════════════════════════════════════════
#  CLOSING & CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════

def p_promise(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    shp(slide, Cm(15), Cm(8), Cm(12), Cm(12), NAVY_MID, MSO_SHAPE.OVAL)
    shp(slide, Cm(-3), Cm(22), Cm(8), Cm(8), NAVY_LITE, MSO_SHAPE.OVAL)
    txt(slide, Cm(2), Cm(3), Cm(17), Cm(1.5), "My Sleep Promise",
        Pt(28), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    gbar(slide, Cm(8), Cm(4.8), Cm(5))
    promises = [
        "For the next seven days, I will keep bedtime simple and in the same order.",
        "I will watch awake windows and act on them before overtiredness sets in.",
        "I will decide my response plan before the night begins.",
        "I will pause before I go in — and give my baby the chance to resettle.",
        "I will not judge the whole plan on one difficult night.",
        "I will stay consistent — especially when it is hardest.",
        "I will remember I am teaching a skill they will use for life.",
        "I will take care of myself — my baby needs a rested parent, not a perfect one.",
    ]
    paras = [{"t": "✦  " + p, "sz": Pt(11), "c": CREAM, "i": True, "sa": Pt(11), "fn": FONT_HEADING} for p in promises]
    mtxt(slide, Cm(2.5), Cm(6), Cm(16), Cm(18), paras)
    mtxt(slide, Cm(2), Cm(25), Cm(17), Cm(2.5), [
        {"t": "With love and solidarity,", "sz": Pt(9), "c": SLATE_LITE, "al": PP_ALIGN.CENTER, "sa": Pt(4)},
        {"t": "Six & Thriving", "sz": Pt(13), "c": GOLD, "b": True, "al": PP_ALIGN.CENTER, "fn": FONT_HEADING, "sa": Pt(4)},
        {"t": "Sleep is coming. For both of you.", "sz": Pt(10), "c": SLATE_LITE, "i": True, "al": PP_ALIGN.CENTER},
    ])
    dark_footer(slide, 54)

def p_conclusion(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Conclusion")
    footer(slide, 55)
    page_top(slide, "CONCLUSION", "You've Got This — And Your Baby Will Sleep", "Conclusion")
    body = [
        {"t": "We started this book in the dark. Maybe literally. Maybe you were in that rocking chair, or sitting in the hallway listening, or lying in bed staring at the ceiling waiting for the next waking. And we end here, with a plan in your hands and a little more understanding in your heart.", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "What You've Learned", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "•  Your baby's sleep challenges are biology, development, and habit — NOT your fault\n•  Sleep science gives you real tools: awake windows, circadian rhythms, sleep pressure\n•  Reading cues before overtiredness changes everything\n•  A consistent routine is one of the most powerful sleep tools you have\n•  The environment is doing work all night — make sure it's working FOR you\n•  The best method is the one you can commit to consistently\n•  Night 3 is the extinction burst — and it means the method is working\n•  Knowing your baby's sleep personality helps you tailor your approach\n•  Common mistakes are avoidable once you know what they are\n•  Consistency on hard nights is the bridge between where you are and where you want to be", "sz": Pt(9), "c": SLATE, "sa": Pt(14)},
        {"t": "The Most Important Thing I Can Tell You", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "Across six children, across the exhausted nights and the mornings that felt impossible — every single one of them learned to sleep. Every single one. The stubborn ones. The sensitive ones. The ones who seemed physiologically opposed to sleep. They all got there.", "sz": Pt(10), "c": SLATE, "sa": Pt(8)},
        {"t": "And so will yours.", "sz": Pt(13), "c": GOLD, "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(10)},
    ]
    mtxt(slide, Cm(2), Cm(4.4), Cm(17), Cm(20), body)
    callout(slide, Cm(24), w=Cm(17), label="HOLD THIS CLOSE",
            body="A baby who sleeps well is a baby who thrives. A parent who sleeps is a parent who's fully present. Sleep is not a luxury — it is a foundation. Go build that foundation. I'm cheering for you.",
            accent=GOLD, bg_clr=NAVY, h=Cm(3), text_color=CREAM, label_clr=GOLD)

# ═══════════════════════════════════════════════════════════════════════════════
#  BONUS SECTION
# ═══════════════════════════════════════════════════════════════════════════════

def p_bonus_open(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    txt(slide, Cm(2), Cm(3), Cm(10), Cm(0.5), "BONUS SECTION", Pt(8), GOLD, b=True)
    txt(slide, Cm(1.5), Cm(7), Cm(18), Cm(4), "BONUS", Pt(70), NAVY_LITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(13), Cm(16), Cm(5), "Quick-Reference\nChecklists & Tools",
        Pt(28), WHITE, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(20), Cm(16), Cm(2),
        "Tear-out ready. Print them. Stick them to the fridge.\nUse them on the hard nights when reading feels like too much.",
        Pt(10.5), GOLD_LITE, i=True)
    pic(slide, "banner", Cm(1.5), Cm(23), w=Cm(18))
    dark_footer(slide, 56)

def p_bonus_checklist(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Bonus 1: Routine Checklist")
    footer(slide, 57)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "BONUS ONE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Bedtime Routine Checklist",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.5),
        "Same order. Every night. Consistency IS the method.", Pt(10), GOLD, i=True)
    items = [
        "Transition signal — lights dimmed, specific phrase spoken",
        "Stimulating activities stopped — screens off, active play ended",
        "Bath or warm wipe-down completed",
        "Lotion massage — slow, calming strokes",
        "Pyjamas and sleep sack on",
        "Feed in dim, quiet room — baby must NOT fall fully asleep",
        "1–3 books or songs in nursing chair / glider",
        "Final goodnight phrase (same words every night)",
        "White noise on (60–70dB, across the room)",
        "Room fully dark — all LEDs covered, true blackout",
        "Baby placed in crib drowsy but awake",
        "Parent exits calmly and consistently",
    ]
    y = Cm(5.3)
    for item in items:
        box = shp(slide, Cm(2), y, Cm(0.5), Cm(0.5), WHITE, MSO_SHAPE.RECTANGLE)
        box.line.color.rgb = GOLD
        box.line.width = Pt(1.2)
        txt(slide, Cm(2.8), y - Cm(0.05), Cm(16), Cm(0.6), item, Pt(9.5), SLATE)
        y += Cm(1.5)
    pic(slide, "designed", Cm(2), Cm(24.5), w=Cm(17))


def p_bonus_tracker(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Bonus 2: 7-Day Tracker")
    footer(slide, 58)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "BONUS TWO", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "7-Day Sleep Tracker",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.5),
        "Fill in each morning. Patterns emerge by Day 3–4.", Pt(10), GOLD, i=True)
    # Table
    shp(slide, Cm(1.5), Cm(5.3), Cm(18), Cm(1.1), NAVY, MSO_SHAPE.RECTANGLE)
    cols = ["Day", "Last Nap", "Bedtime", "Settle", "Wakes", "Up", "Notes"]
    widths = [Cm(2.2), Cm(2.5), Cm(2.2), Cm(2.3), Cm(2.3), Cm(2.2), Cm(4.3)]
    x = Cm(1.5)
    for col, w in zip(cols, widths):
        txt(slide, x, Cm(5.4), w, Cm(0.9), col, Pt(8), WHITE, b=True, al=PP_ALIGN.CENTER)
        x += w
    y = Cm(6.6)
    for day in range(1, 8):
        c = WHITE if day % 2 == 1 else CREAM
        row = shp(slide, Cm(1.5), y, Cm(18), Cm(1.6), c, MSO_SHAPE.RECTANGLE)
        row.line.color.rgb = CREAM_MID
        row.line.width = Pt(0.3)
        txt(slide, Cm(1.5), y + Cm(0.4), Cm(2.2), Cm(0.8), f"Day {day}", Pt(9), NAVY, b=True, al=PP_ALIGN.CENTER)
        y += Cm(1.6)
    # Safe sleep section
    y += Cm(0.6)
    txt(slide, Cm(2), y, Cm(16), Cm(0.7), "Safe Sleep Checklist (AAP-Aligned)",
        Pt(13), NAVY, b=True, fn=FONT_HEADING)
    y += Cm(1)
    left = ["Firm flat mattress", "Fitted sheet only", "No toys, bumpers, positioners", "Sleep sack used", "Back to sleep — every time", "Crib/bassinet only"]
    right = ["Room 68–72°F", "Chest warm not sweaty", "True blackout", "White noise running", "Monitor LEDs covered", "No nightlight, or red only"]
    txt(slide, Cm(2), y, Cm(4), Cm(0.4), "SURFACE", Pt(8), NAVY, b=True)
    txt(slide, Cm(11), y, Cm(4), Cm(0.4), "ROOM", Pt(8), NAVY, b=True)
    y += Cm(0.7)
    for l, r in zip(left, right):
        txt(slide, Cm(2.5), y, Cm(7.5), Cm(0.4), "☐  " + l, Pt(9), SLATE)
        txt(slide, Cm(11.5), y, Cm(7.5), Cm(0.4), "☐  " + r, Pt(9), SLATE)
        y += Cm(0.8)

def p_bonus_awake(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Bonus 3: Awake Windows")
    footer(slide, 59)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "BONUS THREE", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Awake Window Quick Reference",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.5),
        "Pull this out when you need it.", Pt(10), GOLD, i=True)
    rows = [
        ("AGE", "AWAKE WINDOW", "MAX NAPS", "BEDTIME TARGET"),
        ("0–6 weeks", "45–60 min", "4–5/day", "Variable"),
        ("6–12 weeks", "60–90 min", "4/day", "8–9 pm"),
        ("3–4 months", "90 min", "3–4/day", "7:30–8:30 pm"),
        ("4–6 months", "2 hrs", "3/day", "7–8 pm"),
        ("6–8 months", "2.5 hrs", "2–3/day", "7–8 pm"),
        ("8–12 months", "3–3.5 hrs", "2/day", "6:30–7:30 pm"),
        ("12–18 months", "4–5 hrs", "1–2/day", "7–7:30 pm"),
        ("18–24 months", "5–6 hrs", "1/day", "7–7:30 pm"),
    ]
    y = Cm(5.3)
    col_w = [Cm(3.5), Cm(4.5), Cm(3.5), Cm(5.5)]
    for i, row in enumerate(rows):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(1), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for j, cell in enumerate(row):
                txt(slide, x + Cm(0.2), y + Cm(0.25), col_w[j], Cm(0.6), cell, Pt(9), WHITE, b=True, al=PP_ALIGN.CENTER)
                x += col_w[j]
            y += Cm(1)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(1), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.3), col_w[j], Cm(0.5), cell, Pt(9), color, b=bold, al=PP_ALIGN.CENTER)
                x += col_w[j]
            y += Cm(1)
    callout(slide, Cm(15.5), w=Cm(17), label="ONE LAST REMINDER",
            body="Count FORWARD from wake time, not BACKWARD from a target. If your baby's last nap ended at 5pm and the awake window is 3 hours, bedtime is 8pm — even if 'we always do 7'.",
            accent=AMBER, bg_clr=AMBER_LT, h=Cm(2.5), text_color=NAVY, label_clr=AMBER)

def p_bonus_method(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "Bonus 4: Method Comparison")
    footer(slide, 60)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "BONUS FOUR", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(17), Cm(1.1), "Method Comparison Card",
        Pt(18), NAVY, b=True, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(4.4), Cm(17), Cm(0.5),
        "Which Method Fits Your Family? Choose. Commit. Don't second-guess.", Pt(10), GOLD, i=True)
    methods = [
        ("METHOD", "CRY", "SPEED", "BEST FOR"),
        ("Extinction (CIO)", "High", "3–5 days", "High-need families; persistent babies; need fast results"),
        ("Ferber", "Moderate", "5–7 days", "Most temperaments; parents wanting to do something"),
        ("Chair Method", "Low–Mod", "2–4 weeks", "Sensitive babies; parents not ready to step back"),
        ("Fading", "Low", "3–4+ wks", "Gentlest; adaptable babies; no-cry priority"),
        ("Pick Up/Put Down", "Low", "Variable", "3–5 month olds; high-support preference"),
    ]
    y = Cm(5.3)
    col_w = [Cm(4.5), Cm(2.5), Cm(2.7), Cm(7.3)]
    for i, row in enumerate(methods):
        if i == 0:
            shp(slide, Cm(2), y, Cm(17), Cm(1), NAVY, MSO_SHAPE.RECTANGLE)
            x = Cm(2)
            for j, cell in enumerate(row):
                txt(slide, x + Cm(0.2), y + Cm(0.25), col_w[j], Cm(0.6), cell, Pt(9), WHITE, b=True)
                x += col_w[j]
            y += Cm(1)
        else:
            row_color = WHITE if i % 2 == 1 else CREAM
            row_bg = shp(slide, Cm(2), y, Cm(17), Cm(1.2), row_color, MSO_SHAPE.RECTANGLE)
            row_bg.line.color.rgb = CREAM_MID
            row_bg.line.width = Pt(0.3)
            x = Cm(2)
            for j, cell in enumerate(row):
                color = NAVY if j == 0 else SLATE
                bold = j == 0
                txt(slide, x + Cm(0.2), y + Cm(0.35), col_w[j], Cm(0.6), cell, Pt(9), color, b=bold)
                x += col_w[j]
            y += Cm(1.2)
    body = [
        {"t": "The Decision Shortcut", "sz": Pt(13), "c": NAVY, "b": True, "fn": FONT_HEADING, "sa": Pt(8)},
        {"t": "If you need fast results AND can stay consistent → Extinction\nIf you need 'something to do' during crying → Ferber\nIf your baby is very sensitive → Chair Method\nIf you want zero crying → Fading\nIf baby is 3–5 months → Pick Up / Put Down", "sz": Pt(10), "c": SLATE, "sa": Pt(14)},
        {"t": "Pick ONE method. Commit. Stick to it for 7 nights minimum before evaluating. The method matters less than the consistency.", "sz": Pt(11), "c": GOLD, "b": True, "i": True, "fn": FONT_HEADING},
    ]
    mtxt(slide, Cm(2), Cm(13), Cm(17), Cm(10), body)

def p_about(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    header(slide, "About the Author")
    footer(slide, 61)
    txt(slide, Cm(2), Cm(2.2), Cm(10), Cm(0.4), "ABOUT THE AUTHOR", Pt(7), GOLD, b=True)
    gbar(slide, Cm(2), Cm(2.7), Cm(17))
    txt(slide, Cm(2), Cm(3.1), Cm(16), Cm(1), "Six & Thriving",
        Pt(24), NAVY, b=True, fn=FONT_HEADING)
    pic(slide, "narrator", Cm(13.5), Cm(4), w=Cm(5.5))
    bio = [
        {"t": "Six & Thriving is the pen name of a mother of six — including twins — who has spent a decade in the trenches of infant and toddler sleep.", "sz": Pt(10), "c": SLATE, "sa": Pt(12)},
        {"t": "This book was written in the quiet hours, fueled by cold coffee, hard-won experience, and the conviction that sleep is possible for every family.", "sz": Pt(10), "c": SLATE, "sa": Pt(12)},
        {"t": "Six & Thriving creates practical, evidence-informed content for exhausted parents who need real answers, not gentle theory.", "sz": Pt(10), "c": SLATE, "b": True, "sa": Pt(18)},
        {"t": '"Every single one of my babies learned to sleep. Every single one."', "sz": Pt(13), "c": SLATE, "b": True, "i": True, "fn": FONT_HEADING, "sa": Pt(6)},
        {"t": "— Six & Thriving", "sz": Pt(11), "c": GOLD, "b": True, "fn": FONT_HEADING},
    ]
    mtxt(slide, Cm(2), Cm(4.5), Cm(11), Cm(14), bio)
    shp(slide, Cm(2), Cm(20), Cm(17), Cm(2.8), NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(slide, Cm(2.5), Cm(20.4), Cm(16), Cm(0.7),
        "Thank you for trusting Six & Thriving with your baby's sleep journey.",
        Pt(10), CREAM_MID, al=PP_ALIGN.CENTER)
    txt(slide, Cm(2.5), Cm(21.5), Cm(16), Cm(0.8),
        "Sleep is coming. For both of you.",
        Pt(13), GOLD, b=True, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    mtxt(slide, Cm(2), Cm(24), Cm(17), Cm(2.5), [
        {"t": "Disclaimer: Educational purposes only. Not medical advice. Consult your paediatrician.", "sz": Pt(7.5), "c": SLATE_LITE, "al": PP_ALIGN.CENTER, "sa": Pt(4)},
        {"t": "© 2026 Six & Thriving · All rights reserved · sixandthriving.com", "sz": Pt(7.5), "c": SLATE_LITE, "al": PP_ALIGN.CENTER},
    ])

def p_back(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    shp(slide, Cm(14), Cm(-2), Cm(12), Cm(12), NAVY_MID, MSO_SHAPE.OVAL)
    shp(slide, Cm(-3), Cm(22), Cm(10), Cm(10), NAVY_LITE, MSO_SHAPE.OVAL)
    shp(slide, Cm(0), Cm(0), SW, Cm(0.4), GOLD, MSO_SHAPE.RECTANGLE)
    shp(slide, Cm(0), Cm(29.3), SW, Cm(0.4), GOLD, MSO_SHAPE.RECTANGLE)
    txt(slide, Cm(2), Cm(7), Cm(17), Cm(2), "Sleep, Baby. Please.",
        Pt(36), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    gbar(slide, Cm(7.5), Cm(9.5), Cm(6))
    txt(slide, Cm(3), Cm(10.5), Cm(15), Cm(1.5),
        "What Actually Worked for All 6 of Mine — Including Twins",
        Pt(12), GOLD_LITE, i=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    points = [
        "15 chapters of evidence-based, actionable strategies",
        "The Six Sleep Personalities — find yours, fix yours",
        "The Crib Hour technique nobody else teaches",
        "Detailed scripts for every major sleep training method",
        "Full Reset Protocol for parents who've tried before",
        "Breastfeeding, twins, NICU, daycare — all covered",
        "Partner Briefing one-pager included",
        "Written by a mother of six who's been where you are",
    ]
    paras = [{"t": "✦  " + p, "sz": Pt(10), "c": CREAM, "sa": Pt(10), "al": PP_ALIGN.CENTER} for p in points]
    mtxt(slide, Cm(3), Cm(13), Cm(15), Cm(11), paras)
    txt(slide, Cm(2), Cm(24), Cm(17), Cm(0.7), "SIX & THRIVING", Pt(13), WHITE, b=True, al=PP_ALIGN.CENTER, fn=FONT_HEADING)
    txt(slide, Cm(2), Cm(25), Cm(17), Cm(0.5), "sixandthriving.com", Pt(10), GOLD, al=PP_ALIGN.CENTER)
    txt(slide, Cm(2), Cm(27.5), Cm(17), Cm(0.5), "© 2026 Six & Thriving. All Rights Reserved.", Pt(7.5), SLATE_LITE, al=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH

    print()
    print("  ╔════════════════════════════════════════════════════════════════╗")
    print("  ║  Sleep, Baby. Please. — BESTSELLER EDITION v4.0               ║")
    print("  ║  The Definitive, Award-Quality, Zero-Refund Edition           ║")
    print("  ║  Six & Thriving | 2026                                        ║")
    print("  ╚════════════════════════════════════════════════════════════════╝")
    print()

    pages = [
        ("Cover", p_cover),
        ("Copyright", p_copyright),
        ("Table of Contents", p_toc),
        ("Introduction — Letter to the Parent", p_intro),
        ("Fast-Track: Tonight's Plan", p_fast_track),
        ("Ch.1 Opener", p_ch1_open),
        ("Ch.1a — Why Babies Don't Sleep Like Adults", p_ch1a),
        ("Ch.1b — Stats & Tried-Before", p_ch1b),
        ("Ch.2 Opener", p_ch2_open),
        ("Ch.2a — Sleep Pressure & Cortisol", p_ch2a),
        ("Ch.2b — The 45-Minute Intruder", p_ch2b),
        ("Ch.3 Opener", p_ch3_open),
        ("Ch.3a — Sleep Cue Traffic Light", p_ch3a),
        ("Ch.3b — Awake Windows Reference", p_ch3b),
        ("Ch.3c — The Crib Hour", p_ch3c),
        ("Ch.4 Opener", p_ch4_open),
        ("Ch.4a — Pavlov Effect & 4 Components", p_ch4a),
        ("Ch.4b — Sample Routines by Age", p_ch4b),
        ("Ch.5 Opener", p_ch5_open),
        ("Ch.5a — Darkness, Sound, Temperature", p_ch5a),
        ("Ch.5b — Crib & Room", p_ch5b),
        ("Ch.6 Opener", p_ch6_open),
        ("Ch.6a — Extinction & Ferber", p_ch6a),
        ("Ch.6b — Chair, Fading, Pick-Up", p_ch6b),
        ("Ch.6c — Comparison & When to Start", p_ch6c),
        ("Ch.7 Opener", p_ch7_open),
        ("Ch.7a — Wait Principle & Lovey", p_ch7a),
        ("Ch.7b — Reducing Night Feeds", p_ch7b),
        ("Ch.7c — The Reset Protocol", p_ch7c),
        ("Ch.8 Opener", p_ch8_open),
        ("Ch.8a — Personalities 1–3", p_ch8a),
        ("Ch.8b — Personalities 4–6", p_ch8b),
        ("Ch.9 Opener", p_ch9_open),
        ("Ch.9a — Mistakes 1–4", p_ch9a),
        ("Ch.9b — Mistakes 5–7", p_ch9b),
        ("Ch.10 Opener", p_ch10_open),
        ("Ch.10 — Staying Consistent", p_ch10),
        ("Ch.11 Opener", p_ch11_open),
        ("Ch.11 — Toddler Rule Book", p_ch11),
        ("Ch.12 Opener", p_ch12_open),
        ("Ch.12a — Pre-Week & Nights 1–3", p_ch12a),
        ("Ch.12b — Nights 4–7", p_ch12b),
        ("Ch.13 Opener — Breastfeeding", p_ch13_open),
        ("Ch.13a — Compatibility & Unlatch", p_ch13a),
        ("Ch.13b — Drop Schedule & Q&A", p_ch13b),
        ("Ch.14 Opener — Twins/NICU/Daycare", p_ch14_open),
        ("Ch.14 — Special Situations", p_ch14),
        ("Ch.15 Opener — First 8 Weeks", p_ch15_open),
        ("Ch.15 — Newborn Period", p_ch15),
        ("Partner Briefing One-Pager", p_partner),
        ("My Sleep Promise", p_promise),
        ("Conclusion", p_conclusion),
        ("Bonus Opener", p_bonus_open),
        ("Bonus 1 — Routine Checklist", p_bonus_checklist),
        ("Bonus 2 — 7-Day Tracker + Safe Sleep", p_bonus_tracker),
        ("Bonus 3 — Awake Windows Reference", p_bonus_awake),
        ("Bonus 4 — Method Comparison Card", p_bonus_method),
        ("About the Author", p_about),
        ("Back Cover", p_back),
    ]

    for name, fn in pages:
        print(f"  ✓ {name}")
        fn(prs)

    out = os.path.join(BASE, "SleepBabyPlease_BESTSELLER_2026.pptx")
    prs.save(out)

    print()
    print("  ════════════════════════════════════════════════════════════════")
    print(f"  ✅ DONE — {len(pages)} pages of premium, actionable content")
    print(f"  📄 {out}")
    print()
    print("  🏆 BESTSELLER FEATURES:")
    print("     ✓ 15 chapters (vs. 11 in previous version)")
    print("     ✓ Specific scripts and decision trees on every page")
    print("     ✓ Full method instructions: Extinction, Ferber, Chair, Fading, PUPD")
    print("     ✓ Day-by-day Ferber timing chart")
    print("     ✓ Sample routines by age (newborn, 3-6mo, 6-18mo)")
    print("     ✓ The Six Sleep Personalities with custom strategies")
    print("     ✓ The Crib Hour technique (unique differentiator)")
    print("     ✓ 7 Common Mistakes with exact fixes")
    print("     ✓ Full night-by-night plan (Nights 1-7)")
    print("     ✓ The Reset Protocol for failed-before parents")
    print("     ✓ Breastfeeding chapter (unlatch technique, dream feeds, Q&A)")
    print("     ✓ Twins, NICU, daycare — all covered properly")
    print("     ✓ First 8 Weeks newborn chapter")
    print("     ✓ Partner Briefing one-pager")
    print("     ✓ 4 bonus tools: checklist, tracker, awake reference, methods")
    print()
    print("  📋 CANVA IMPORT:")
    print("     1. canva.com → Create → Import file")
    print("     2. Upload the .pptx")
    print("     3. Every element fully editable")
    print()

if __name__ == "__main__":
    build()
