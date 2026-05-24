"""
Sleep, Baby. Please. — Premium Production PDF
Six & Thriving | 2026
Full-text, production-ready, 10x design quality
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math

W, H = A4  # 595.27 x 841.89 pts

# ── BRAND PALETTE ──────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#0D1B3E")   # Deep navy
NAVY_MID  = colors.HexColor("#162347")
NAVY_LITE = colors.HexColor("#1E2F55")
GOLD      = colors.HexColor("#C9A84C")   # Rich gold
GOLD_LITE = colors.HexColor("#E8C97A")
CREAM     = colors.HexColor("#FAF7F2")   # Warm cream background
CREAM_MID = colors.HexColor("#F0EBE1")
WHITE     = colors.white
TEAL      = colors.HexColor("#2D8A8A")   # Accent teal
SLATE     = colors.HexColor("#4A5568")   # Body text
SLATE_LITE= colors.HexColor("#718096")
RUST      = colors.HexColor("#C0392B")   # Danger/warning accent
GREEN_DK  = colors.HexColor("#276749")
GREEN_LT  = colors.HexColor("#C6F6D5")
AMBER     = colors.HexColor("#D69E2E")
AMBER_LT  = colors.HexColor("#FEFCBF")
RED_LT    = colors.HexColor("#FED7D7")
DIVIDER   = colors.HexColor("#D4B896")
BG_CARD   = colors.HexColor("#FFFFFF")

# ── HELPER: draw filled rounded rect ───────────────────────────────────────────
def rrect(c, x, y, w, h, r=4*mm, fill_color=WHITE, stroke_color=None, lw=0.5):
    c.saveState()
    c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(lw)
    else:
        c.setStrokeColor(colors.transparent)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1 if stroke_color else 0)
    c.restoreState()

def hrule(c, x, y, w, color=DIVIDER, lw=0.75):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x, y, x+w, y)
    c.restoreState()

def gold_bar(c, x, y, w, h=2.5):
    c.setFillColor(GOLD)
    c.rect(x, y, w, h*mm, fill=1, stroke=0)

def label(c, text, x, y, font="Helvetica-Bold", size=7, color=GOLD, tracking=2):
    c.saveState()
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)
    c.restoreState()

def body_text(c, text, x, y, width, size=9.5, color=SLATE, leading=15, font="Helvetica"):
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    style = ParagraphStyle('body', fontName=font, fontSize=size,
                           textColor=color, leading=leading,
                           alignment=TA_JUSTIFY)
    p = Paragraph(text, style)
    p.wrapOn(c, width, 1000)
    p.drawOn(c, x, y - p.height)
    return p.height

def section_heading(c, text, x, y, size=13, color=NAVY):
    c.saveState()
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawString(x, y, text)
    c.restoreState()

def std_header(c, chapter_label, page_num):
    """Standard running header"""
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H-14*mm, W, 14*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H-16*mm, W, 2*mm, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 7.5)
    c.drawString(18*mm, H-9*mm, "Sleep, Baby. Please.")
    c.drawRightString(W-18*mm, H-9*mm, chapter_label)
    c.restoreState()

def std_footer(c, page_num):
    """Standard running footer"""
    c.saveState()
    c.setFillColor(CREAM_MID)
    c.rect(0, 0, W, 14*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 13*mm, W, 0.8*mm, fill=1, stroke=0)
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 7.5)
    c.drawString(18*mm, 4.5*mm, "Six & Thriving  •  sixandthriving.com")
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    # Circle
    cx, cy = W/2, 7*mm
    c.setFillColor(NAVY)
    c.circle(cx, cy, 5*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(cx, cy-2.5, str(page_num))
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 7.5)
    c.drawRightString(W-18*mm, 4.5*mm, "© 2026 Six & Thriving. All rights reserved.")
    c.restoreState()

def chapter_opener(c, num_str, chapter_label, title, subtitle, page_num):
    """Full-bleed dark chapter opener"""
    # Background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Decorative circles
    c.setFillColor(NAVY_LITE)
    c.circle(W+10*mm, H+5*mm, 80*mm, fill=1, stroke=0)
    c.setFillColor(NAVY_MID)
    c.circle(-15*mm, 40*mm, 60*mm, fill=1, stroke=0)
    # Gold bottom bar
    c.setFillColor(GOLD)
    c.rect(0, 0, W, 3*mm, fill=1, stroke=0)
    # Chapter label
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(20*mm, H-30*mm, chapter_label)
    # Big chapter number (ghost)
    c.setFillColor(NAVY_LITE)
    c.setFont("Helvetica-Bold", 100)
    c.drawString(14*mm, H/2 - 20*mm, num_str)
    # Title
    lines = title.split("\n")
    ty = H/2 + 30*mm
    for line in lines:
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 28)
        c.drawString(20*mm, ty, line)
        ty -= 34
    # Gold rule
    c.setFillColor(GOLD)
    c.rect(20*mm, ty - 4*mm, 30*mm, 2, fill=1, stroke=0)
    ty -= 12*mm
    # Subtitle
    if subtitle:
        sub_lines = subtitle.split("\n")
        for sl in sub_lines:
            c.setFillColor(GOLD_LITE)
            c.setFont("Helvetica-Oblique", 10.5)
            c.drawString(20*mm, ty, sl)
            ty -= 14
    # Page number
    std_footer(c, page_num)

def info_card(c, x, y, w, h, title, body, accent=TEAL):
    rrect(c, x, y, w, h, r=3*mm, fill_color=CREAM, stroke_color=CREAM_MID)
    c.setFillColor(accent)
    c.rect(x, y, 3.5, h, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 6*mm, y + h - 7*mm, title)
    style = ParagraphStyle('ic', fontName='Helvetica', fontSize=8.5,
                           textColor=SLATE, leading=13)
    p = Paragraph(body, style)
    p.wrapOn(c, w - 9*mm, h)
    p.drawOn(c, x + 6*mm, y + 4*mm)

def callout_box(c, x, y, w, title, body, bg=CREAM_MID, accent=GOLD, text_color=NAVY):
    style = ParagraphStyle('co', fontName='Helvetica', fontSize=8.5,
                           textColor=SLATE, leading=13.5)
    p = Paragraph(body, style)
    pw, ph = p.wrapOn(c, w - 12*mm, 1000)
    box_h = ph + 20*mm
    rrect(c, x, y - box_h, w, box_h, r=3*mm, fill_color=bg)
    c.setFillColor(accent)
    c.rect(x, y - box_h, 3.5, box_h, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 6*mm, y - 7.5*mm, title.upper())
    p.drawOn(c, x + 6*mm, y - box_h + 4*mm)
    return box_h

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def page_cover(c):
    # Full bleed dark
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Top decorative circle
    c.setFillColor(NAVY_MID)
    c.circle(W + 20*mm, H + 10*mm, 100*mm, fill=1, stroke=0)
    # Bottom gradient suggestion via layered rects
    for i in range(8):
        alpha_color = colors.HexColor("#162347") if i % 2 == 0 else colors.HexColor("#0D1B3E")
        c.setFillColor(alpha_color)
        c.rect(0, i*15, W, 15, fill=1, stroke=0)
    # Gold horizontal stripe
    c.setFillColor(GOLD)
    c.rect(0, H - 5*mm, W, 5*mm, fill=1, stroke=0)
    # Badge — #1 BESTSELLER
    c.setFillColor(GOLD)
    c.circle(W - 30*mm, H - 30*mm, 18*mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W - 30*mm, H - 27*mm, "#1")
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(W - 30*mm, H - 33*mm, "BESTSELLER")
    # Series label
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7.5)
    label_text = "THE HONEST MOM'S GUIDE"
    c.drawCentredString(W/2, H - 22*mm, label_text)
    # Decorative rule
    c.setFillColor(GOLD)
    c.rect(W/2 - 25*mm, H - 24.5*mm, 50*mm, 0.75, fill=1, stroke=0)

    # === MAIN TITLE AREA (lower half) ===
    title_y = H/2 + 30*mm
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 58)
    c.drawString(18*mm, title_y, "Sleep,")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 58)
    c.drawString(18*mm, title_y - 62, "Baby.")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-BoldOblique", 58)
    c.drawString(18*mm, title_y - 124, "Please.")

    # Decorative diamond rule
    c.setFillColor(GOLD)
    c.rect(18*mm, title_y - 140, 70*mm, 1, fill=1, stroke=0)
    c.circle(18*mm + 35*mm, title_y - 140, 2.5, fill=1, stroke=0)

    # Subtitle
    c.setFillColor(CREAM_MID)
    c.setFont("Helvetica", 11)
    c.drawString(18*mm, title_y - 155, "A Mom of 6 Shares the Exact Steps That Got Every")
    c.drawString(18*mm, title_y - 168, "One of Her Babies Sleeping Through the Night")

    # Author block
    c.setFillColor(GOLD)
    c.rect(18*mm, 60*mm, 60*mm, 0.8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(18*mm, 50*mm, "SIX  &  THRIVING")
    c.setFillColor(GOLD_LITE)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(18*mm, 41*mm, "Mother of Six — Still Here at 3 a.m.")
    # Footer
    c.setFillColor(colors.HexColor("#080F24"))
    c.rect(0, 0, W, 20*mm, fill=1, stroke=0)
    c.setFillColor(SLATE_LITE)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W/2, 8*mm, "sixandthriving.com   |   © 2026 Six & Thriving. All Rights Reserved.")


def page_copyright(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Six & Thriving", page_num)
    std_footer(c, page_num)
    y = H - 45*mm
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(20*mm, y, "Sleep, Baby. Please.")
    y -= 10*mm
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(20*mm, y, "The Evidence-Based Roadmap to Restful Nights")
    y -= 18*mm
    hrule(c, 20*mm, y, W - 40*mm, color=DIVIDER)
    y -= 12*mm
    for line in [
        "Copyright © 2026 Six & Thriving. All rights reserved.",
        "",
        "No part of this publication may be reproduced, distributed, or transmitted in",
        "any form or by any means, without the prior written permission of the publisher.",
        "",
        "The information in this eBook is intended for general educational purposes only.",
        "It is not a substitute for professional medical advice, diagnosis, or treatment.",
        "Always consult your paediatrician or qualified health provider with any questions",
        "about your child's sleep, feeding, or wellbeing.",
        "",
        "First published 2026.",
    ]:
        c.setFillColor(SLATE if line else WHITE)
        c.setFont("Helvetica", 9)
        c.drawString(20*mm, y, line)
        y -= 13
    y -= 10*mm
    hrule(c, 20*mm, y, W-40*mm, color=DIVIDER)
    y -= 10*mm
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(20*mm, y, "SIX & THRIVING")
    y -= 11
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 8.5)
    c.drawString(20*mm, y, "Practical parenting resources for the exhausted and the hopeful.")


def page_toc(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Contents", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CONTENTS", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(20*mm, y - 5*mm, "Table of Contents")
    y -= 25*mm
    entries = [
        ("INTRO",    "A Letter to the Exhausted Parent",                       "4"),
        ("CH. ONE",  "Why Your Baby Isn't Sleeping — And It's Not Your Fault", "6"),
        ("CH. TWO",  "The Science: What's Actually Happening in That Little Body","10"),
        ("CH. THREE","Reading Your Baby — Cues, Personalities & Windows",       "14"),
        ("CH. FOUR", "Building the Foundation: Routine, Environment & Feeds",   "18"),
        ("CH. FIVE", "Sleep Training Methods — Choosing What Fits Your Family", "22"),
        ("CH. SIX",  "The Seven Nights: What to Expect, Night by Night",        "25"),
        ("CH. SEVEN","When It's Not Working — Troubleshooting Common Setbacks", "29"),
        ("CH. EIGHT","Toddlers, Big Kids & The Bedtime Stall",                  "31"),
        ("CLOSING",  "My Sleep Promise",                                         "33"),
        ("BONUS",    "Checklists, Trackers & Quick-Reference Tools",             "34"),
    ]
    for tag, title, pg in entries:
        # Divider
        hrule(c, 20*mm, y - 2*mm, W-40*mm, color=CREAM_MID, lw=0.5)
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(20*mm, y + 3*mm, tag)
        c.setFillColor(NAVY)
        c.setFont("Helvetica", 10)
        c.drawString(45*mm, y + 3*mm, title)
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(W-20*mm, y + 3*mm, pg)
        y -= 14.5
    y -= 10*mm
    # How to use note
    rrect(c, 20*mm, y - 18*mm, W-40*mm, 24*mm, r=2.5*mm, fill_color=NAVY)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(26*mm, y - 5*mm, "HOW TO USE THIS BOOK")
    c.setFillColor(CREAM_MID)
    c.setFont("Helvetica", 8.5)
    c.drawString(26*mm, y - 13*mm,
        "Read Chapters One through Three first — they give you the why. Then jump to whatever is most urgent.")
    c.drawString(26*mm, y - 21*mm,
        "The Bonus section is designed to be printed and used on the hard nights.")


def page_intro_letter(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Introduction", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "INTRODUCTION", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(20*mm, y - 8*mm, "A Letter to the")
    c.drawString(20*mm, y - 22*mm, "Exhausted Parent")
    # Gold underline
    c.setFillColor(GOLD)
    c.rect(20*mm, y - 26*mm, 20*mm, 2.5, fill=1, stroke=0)
    y -= 38*mm
    paras = [
        "If you are reading this at 2am, still in your feeding chair, wondering how much longer you can do this - <b>this book is for you.</b>",
        "Sleep deprivation is not a rite of passage. It is a medical condition. It impairs your judgement, erodes your relationship, dims your patience, and quietly strips away the parent you are trying to be. You did not sign up for this part. Nobody really tells you about this part.",
        "Here is what I want you to know before you read another word: <b>your baby is not broken. You are not failing.</b> The situation you are in right now is temporary, it is solvable, and thousands of families who felt exactly as desperate as you do right now have come through it.",
        "I have six children. One set of twins tucked in the middle. I have lived through nearly every sleep scenario described in this book. I have been the mother sitting in the dark at 4am, Googling things I am now embarrassed to have Googled. I have been the one whispering \"please, please just sleep\" to a baby who absolutely would not.",
        "And then - with real, consistent, evidence-backed strategies - <b>every single one of my babies learned to sleep.</b>",
    ]
    col_w = (W - 40*mm) * 0.56
    for txt in paras:
        style = ParagraphStyle('body', fontName='Helvetica', fontSize=10,
                               textColor=SLATE, leading=16, alignment=TA_JUSTIFY)
        p = Paragraph(txt, style)
        pw, ph = p.wrapOn(c, col_w, 1000)
        if y - ph < 20*mm: break
        p.drawOn(c, 20*mm, y - ph)
        y -= ph + 6
    # Quote block
    y -= 6*mm
    c.setFillColor(GOLD)
    c.rect(20*mm, y, 3.5, 28*mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-BoldOblique", 11)
    c.drawString(28*mm, y + 18*mm, 'Sleep is not a gift some babies give their parents.')
    c.drawString(28*mm, y + 9*mm,  "It is a skill - and like every skill, it can be taught.")
    y -= 35*mm
    # Sign-off
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(20*mm, y, "With love and solidarity,")
    y -= 13
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, y, "— Six & Thriving")


def page_fast_track(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Fast-Track: Tonight's Plan", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "FAST-TRACK", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(20*mm, y - 8*mm, "Tonight's Plan")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(20*mm, y - 19*mm, "If you read nothing else, read this page first.")
    y -= 30*mm
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, y, "These six steps are the foundation of everything in this book. Do these tonight.")
    y -= 14*mm
    steps = [
        ("1", "Check the room right now",
         "Pitch black? White noise running? Temperature 68–72°F / 20–22°C? Fix this before anything else."),
        ("2", "Find your baby's awake window",
         "Turn to the Awake Windows table in Ch. 3. Note the max time your baby should be up before the next sleep."),
        ("3", "Write tonight's bedtime routine — in order",
         "Warm bath → lotion → pyjamas → feed (not to sleep) → one song → crib awake. Same sequence every night."),
        ("4", "Decide your response plan before night falls",
         "Choose your method from Ch. 6 right now. Write it down. Your 2 a.m. brain won't make good decisions."),
        ("5", "Pause before you go in",
         "When you hear a sound, wait 2–3 minutes. Many babies cycle through light sleep and will resettle."),
        ("6", "Put them into the crib awake",
         "Drowsy is fine. Already asleep is not. This single skill changes everything."),
    ]
    for num, title, body in steps:
        row_h = 22*mm
        rrect(c, 20*mm, y - row_h, W-40*mm, row_h, r=2.5*mm,
              fill_color=WHITE, stroke_color=CREAM_MID, lw=0.5)
        # Number bubble
        c.setFillColor(NAVY)
        c.circle(31*mm, y - row_h/2, 5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(31*mm, y - row_h/2 - 3, num)
        # Title
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40*mm, y - 8*mm, title)
        # Body
        style = ParagraphStyle('s', fontName='Helvetica', fontSize=8.5,
                               textColor=SLATE, leading=13)
        p = Paragraph(body, style)
        p.wrapOn(c, W - 65*mm, 20*mm)
        p.drawOn(c, 40*mm, y - row_h + 3.5*mm)
        y -= row_h + 3*mm
    # Callout
    y -= 4*mm
    rrect(c, 20*mm, y - 18*mm, W-40*mm, 18*mm, r=2.5*mm, fill_color=AMBER_LT)
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(26*mm, y - 7*mm, "DONE IS BETTER THAN PERFECT")
    c.setFillColor(NAVY)
    c.setFont("Helvetica", 9)
    c.drawString(26*mm, y - 15*mm, "Pick one thing from this list and do it tonight. Progress starts with a single consistent step.")


def page_ch1_opener(c, page_num):
    chapter_opener(c, "01", "CHAPTER ONE",
                   "Why Your Baby\nIsn't Sleeping —\nAnd It's Not\nYour Fault",
                   "Understanding the real reasons behind the night\nwakings, the early mornings, and the 45-minute\nnaps that are slowly breaking you.",
                   page_num)


def page_ch1_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter One", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER ONE", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(20*mm, y - 8*mm, "Why Your Baby Isn't Sleeping")
    y -= 20*mm
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 10.5)
    c.drawString(20*mm, y,
        "Before we fix anything, we need to understand what's actually causing the problem.")
    c.drawString(20*mm, y - 13, "Most sleep struggles come from a surprisingly short list of culprits.")
    y -= 28*mm
    # 5 reasons grid
    reasons = [
        ("Sleep\nAssociations", "Sleep breast and bottle associations"),
        ("Overtiredness", "Difficulty settling due to a cortisol spike"),
        ("Under-\ntiredness", "Resistance to sleep from not enough awake time"),
        ("Environment", "Room too bright, noisy, or uncomfortable temperature"),
        ("Developmental\nLeaps", "Processing new milestones like rolling or crawling"),
    ]
    box_w = (W - 40*mm - 8*mm) / 5
    bx = 20*mm
    for i, (r_title, r_body) in enumerate(reasons):
        bg = [NAVY, colors.HexColor("#2D5016"), AMBER, TEAL, colors.HexColor("#553C9A")][i]
        rrect(c, bx, y - 35*mm, box_w - 1*mm, 35*mm, r=2*mm, fill_color=bg)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        lines = r_title.split("\n")
        ty = y - 10*mm
        for ln in lines:
            c.drawCentredString(bx + box_w/2, ty, ln)
            ty -= 11
        c.setFont("Helvetica", 7.5)
        style = ParagraphStyle('rb', fontName='Helvetica', fontSize=7.5,
                               textColor=WHITE, leading=11, alignment=TA_CENTER)
        p = Paragraph(r_body, style)
        p.wrapOn(c, box_w - 4*mm, 20*mm)
        p.drawOn(c, bx + 2*mm, y - 33*mm)
        bx += box_w + 2

    y -= 48*mm
    section_heading(c, "Sleep Associations: The Hidden Driver", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "A sleep association is anything your baby needs in order to fall asleep — and, critically, to <i>fall back asleep</i> "
        "when they naturally rouse between sleep cycles. If your baby falls asleep while feeding, being rocked, or held, "
        "then wakes at 2am and cannot find those conditions, they will cry until they are recreated.",
        20*mm, y, W - 40*mm)
    y -= 26*mm
    body_text(c,
        "This is not manipulation. It is biology. Your baby is not 'playing you.' They genuinely cannot link sleep cycles "
        "without the tool they learned to use — yet.",
        20*mm, y, W - 40*mm)
    y -= 22*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "The Key Insight",
        "The goal of sleep training is not to make your baby cry. It is to give your baby the one skill they currently lack: "
        "the ability to move between sleep cycles independently, without external assistance.",
        bg=colors.HexColor("#EBF8FF"), accent=TEAL)
    y -= 28*mm
    section_heading(c, "Hunger, Growth & Developmental Leaps", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "Growth spurts, developmental leaps, teething, and illness all temporarily disrupt sleep. During a growth spurt, "
        "your baby genuinely needs more calories. During a developmental leap, their sleep is disrupted by all the brain "
        "processing happening behind the scenes. Most of these pass within one to four weeks.",
        20*mm, y, W - 40*mm)
    y -= 28*mm
    section_heading(c, "Overtiredness: The Parent Trap", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "When babies are overtired, they actually have more trouble sleeping. An overtired baby produces cortisol, which "
        "makes it harder to fall asleep and stay asleep. Keeping them up longer to tire them out is almost always the wrong move.",
        20*mm, y, W - 40*mm)


def page_ch1_content2(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter One", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER ONE", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Environment & Developmental Leaps", 20*mm, y - 8*mm, size=14)
    y -= 22*mm
    body_text(c,
        "A room that is too bright, too warm, or too noisy is working against your baby's sleep biology. A room that is "
        "not dark enough is one of the most common and most fixable problems. True blackout means you cannot see your "
        "hand in front of your face.",
        20*mm, y, W - 40*mm)
    y -= 30*mm
    body_text(c,
        "Developmental leaps — rolling, crawling, pulling to stand — also temporarily disrupt sleep as the brain works "
        "overtime to consolidate new motor programmes. These are normal, expected, and temporary. They are not a sign "
        "to stop what you're doing.",
        20*mm, y, W - 40*mm)
    y -= 30*mm
    # Stats row
    stats = [("45", "Minutes", "A baby's full sleep cycle. Most adults need 90."),
             ("4-6", "Weeks", "Average for sleep habits to become truly stable."),
             ("7", "Nights", "All most families need with a consistent method.")]
    bx = 20*mm; bw = (W - 40*mm - 6*mm)/3
    for val, unit, desc in stats:
        rrect(c, bx, y - 28*mm, bw - 2*mm, 28*mm, r=3*mm, fill_color=NAVY)
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(bx + bw/2, y - 12*mm, val)
        c.setFillColor(CREAM_MID)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(bx + bw/2, y - 19*mm, unit.upper())
        c.setFillColor(SLATE_LITE)
        c.setFont("Helvetica", 7)
        style = ParagraphStyle('s', fontName='Helvetica', fontSize=7,
                               textColor=colors.HexColor("#A0AEC0"), leading=10, alignment=TA_CENTER)
        p = Paragraph(desc, style)
        p.wrapOn(c, bw - 6*mm, 15*mm)
        p.drawOn(c, bx + 3*mm, y - 26*mm)
        bx += bw + 3
    y -= 42*mm
    section_heading(c, "The Two-Week Consistency Rule", 20*mm, y, size=14)
    y -= 8*mm
    body_text(c,
        "The single most common reason sleep training fails is inconsistency. Not the method itself — the application. "
        "Every time you respond differently to the same behaviour, you teach your baby that if they escalate long enough, "
        "the old response will return. This is called intermittent reinforcement, and it makes the crying worse, not better.",
        20*mm, y, W - 40*mm)
    y -= 30*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "What This Chapter Means For You",
        "Identify your main culprit before starting any method. Is it a sleep association? Timing? Environment? "
        "The fix depends entirely on the cause. The rest of this book will help you narrow it down — and then solve it.",
        bg=CREAM_MID, accent=NAVY)


def page_ch2_opener(c, page_num):
    chapter_opener(c, "02", "CHAPTER TWO",
                   "The Science:\nWhat's Actually\nHappening in\nThat Little Body",
                   "Sleep cycles, melatonin, cortisol, circadian rhythms,\nand why your baby's brain works so differently\nfrom yours — and what it means for tonight.",
                   page_num)


def page_ch2_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Two", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER TWO", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "The Science of Baby Sleep", 20*mm, y - 8*mm, size=20)
    y -= 20*mm
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 10.5)
    c.drawString(20*mm, y,
        "Understanding why babies sleep the way they do — and how that differs from adult sleep —")
    c.drawString(20*mm, y - 13, "transforms your frustration into strategy.")
    y -= 30*mm
    section_heading(c, "Sleep Cycles: Shorter Than You Think", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "Adult sleep cycles last roughly 90 minutes. A baby's cycle is only 45 minutes — which is why you see that "
        "signature 45-minute wake at the end of a nap. At the top of every cycle, there is a brief arousal. Adults "
        "pass through these barely noticing. Babies who depend on an external sleep prop cannot — they fully wake "
        "and call for it.",
        20*mm, y, W - 40*mm)
    y -= 30*mm
    # Two-column stats
    col_w = (W - 44*mm)/2
    for col, (badge, title, desc) in enumerate([
        ("45 min", "BABY CYCLES",
         "Short cycles mean more frequent transitions between light and deep sleep — and more opportunities to fully wake if self-settling isn't established."),
        ("90 min", "ADULT CYCLES",
         "Adults pass through cycle transitions unconsciously. This is the skill your baby is currently learning — it just takes a little time and consistency."),
    ]):
        bx = 20*mm + col*(col_w + 4*mm)
        rrect(c, bx, y - 42*mm, col_w, 42*mm, r=3*mm,
              fill_color=NAVY if col==0 else colors.HexColor("#2D4A3E"))
        c.setFillColor(GOLD if col==0 else colors.HexColor("#68D391"))
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(bx + 4*mm, y - 7*mm, title)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(bx + 4*mm, y - 18*mm, badge)
        style = ParagraphStyle('c', fontName='Helvetica', fontSize=8.5,
                               textColor=colors.HexColor("#CBD5E0"), leading=13)
        p = Paragraph(desc, style)
        p.wrapOn(c, col_w - 8*mm, 30*mm)
        p.drawOn(c, bx + 4*mm, y - 40*mm)
    y -= 56*mm
    section_heading(c, "The Sleep Window: Your Most Powerful Tool", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "Timing your baby into the sweet spot — after enough awake time to build sleep pressure, but before the "
        "cortisol zone kicks in — is one of the most impactful things you can do. This window narrows as babies "
        "get overtired: miss it, and you are fighting cortisol.",
        20*mm, y, W-40*mm)
    y -= 28*mm
    section_heading(c, "Melatonin & Circadian Rhythm", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "Babies are not born with a functioning circadian clock. It develops over the first 3–4 months, guided by "
        "light exposure, feed timing, and consistent routines. Melatonin production in newborns comes largely from "
        "their mother's milk. By 3–4 months, your baby's own melatonin system begins to activate — and this is why "
        "sleep becomes more trainable around this age.",
        20*mm, y, W-40*mm)
    y -= 30*mm
    body_text(c,
        "Maximise light exposure in the morning (even five minutes near a window makes a difference), keep the sleep "
        "environment dark during all sleep periods, and anchor bedtime within a 30-minute window every night. "
        "These cues train the circadian clock faster than almost anything else.",
        20*mm, y, W-40*mm)
    y -= 28*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "The Awake Window By Age",
        "How long your baby can comfortably stay awake before needing to sleep changes dramatically across the first "
        "two years. See the full reference table on the next page.",
        bg=colors.HexColor("#EBF8FF"), accent=TEAL)


def page_awake_windows(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Two", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "REFERENCE · CHAPTER TWO", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Baby Sleep Awake Windows: Birth to 18 Months", 20*mm, y - 8*mm, size=16)
    y -= 22*mm
    # Table
    table_data = [
        ["Age", "Awake Window", "Naps/Day", "Target Bedtime", "Notes"],
        ["0–4 weeks",    "45–60 min",       "4–5", "Variable",   "Watch for early cues; windows very short"],
        ["1–2 months",   "60–90 min",       "4–5", "8–9 pm",     "Gradually extending"],
        ["2–3 months",   "75–90 min",       "4",   "8 pm",       "Circadian rhythm starting to emerge"],
        ["3–4 months",   "90 min – 2 hrs",  "3–4", "7:30–8 pm",  "4-month regression often hits here"],
        ["4–6 months",   "2 – 2.5 hrs",     "3",   "7–8 pm",     "More predictable scheduling begins"],
        ["6–8 months",   "2.5–3 hrs",       "2–3", "7–8 pm",     "Transition to 2 naps often starting"],
        ["8–12 months",  "3–4 hrs",         "2",   "6:30–7:30 pm","2-nap schedule solidifies"],
        ["12–18 months", "4–5 hrs",         "1–2", "7–7:30 pm",  "Transitioning to 1 nap"],
        ["18–24 months", "5–6 hrs",         "1",   "7–7:30 pm",  "1 solid nap, longer nights"],
    ]
    col_widths = [28*mm, 32*mm, 22*mm, 32*mm, 53*mm]
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('TEXTCOLOR', (0,1), (-1,-1), SLATE),
        ('BACKGROUND', (0,1), (-1,-1), WHITE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CREAM]),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.3, CREAM_MID),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,1), (0,-1), NAVY),
    ]))
    tw, th = t.wrapOn(c, W-40*mm, 200*mm)
    t.drawOn(c, 20*mm, y - th)
    y -= th + 10*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "The Most Common Timing Mistake",
        "Putting a baby down at a fixed clock time ('we always do 7pm') regardless of when they woke from their last nap. "
        "If the last nap ended at 5:30pm, a 7pm bedtime gives only 90 minutes of awake time — fine for a newborn, "
        "catastrophically early for a 7-month-old whose window is 3.5 hours. Count forward from wake time, not backward from a target.",
        bg=AMBER_LT, accent=AMBER)


def page_ch3_opener(c, page_num):
    chapter_opener(c, "03", "CHAPTER THREE",
                   "Reading Your\nBaby — Cues,\nPersonalities\n& Windows",
                   "How to spot the sleepy sweet spot before it closes,\nidentify your baby's sleep personality,\nand personalise everything that follows.",
                   page_num)


def page_ch3_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Three", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER THREE", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Reading Your Baby", 20*mm, y - 8*mm, size=20)
    y -= 18*mm
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 9.5)
    c.drawString(20*mm, y, "The Three Stages of Tiredness")
    y -= 10*mm
    body_text(c,
        "Think of your baby's readiness to sleep as a traffic light. Most parents only notice Stage 3 — because those "
        "signals are impossible to miss. By then, you're already in damage-control mode.",
        20*mm, y, W-40*mm)
    y -= 22*mm
    # 3-column stage cards
    stages = [
        ("Stage 1", "Green Light", TEAL,
         ["Slowing movements", "Quiet gaze", "Single yawn"], "Start your routine NOW"),
        ("Stage 2", "Yellow Light", AMBER,
         ["Yawning frequently", "Eye rubbing", "Ear pulling", "Fussier"], "Begin routine immediately"),
        ("Stage 3", "Red Light", colors.HexColor("#E53E3E"),
         ["Crying", "Arching back", "Wired and hyper"], "Damage control mode"),
    ]
    col_w = (W - 44*mm)/3
    bx = 20*mm
    for s_title, s_sub, s_color, cues, cta in stages:
        card_h = 70*mm
        rrect(c, bx, y - card_h, col_w - 2*mm, card_h, r=3*mm, fill_color=s_color)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(bx + col_w/2, y - 9*mm, s_title)
        c.setFont("Helvetica", 9)
        c.drawCentredString(bx + col_w/2, y - 17*mm, s_sub)
        cy2 = y - 28*mm
        for cue in cues:
            c.setFont("Helvetica", 8.5)
            c.drawCentredString(bx + col_w/2, cy2, "• " + cue)
            cy2 -= 11
        rrect(c, bx + 3*mm, y - card_h + 3*mm, col_w - 8*mm, 12*mm,
              r=2*mm, fill_color=colors.HexColor("#00000033"))
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(bx + col_w/2, y - card_h + 8.5*mm, cta)
        bx += col_w + 2
    y -= 80*mm
    # Detailed cues table
    section_heading(c, "Stage 1 — Green Light", 20*mm, y, size=11, color=TEAL)
    y -= 8*mm
    cues_left = ["Quieting down, less active", "Gazing away, middle distance",
                 "Slightly slower movements", "Reduced social smiling", "Expression becomes more serious"]
    cues_right = ["Yawning frequently", "Eye rubbing or ear pulling",
                  "Red eyebrows or rimmed eyes", "Losing interest in toys", "Fussiness ramping up"]
    col_w2 = (W - 44*mm)/2
    for i, cue in enumerate(cues_left):
        c.setFillColor(TEAL)
        c.circle(23*mm, y - i*11 + 3, 2, fill=1, stroke=0)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 9)
        c.drawString(26*mm, y - i*11, cue)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(20*mm, y - len(cues_left)*11 - 2, "→ Start routine NOW")
    y -= 10*mm
    section_heading(c, "Stage 2 — Yellow Light", W/2 + 2*mm, y + len(cues_left)*11 + 10*mm, size=11, color=AMBER)
    for i, cue in enumerate(cues_right):
        c.setFillColor(AMBER)
        c.circle(W/2 + 5*mm, y + len(cues_left)*11 + 8*mm - i*11 + 3, 2, fill=1, stroke=0)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 9)
        c.drawString(W/2 + 8*mm, y + len(cues_left)*11 + 8*mm - i*11, cue)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(W/2 + 2*mm, y - 2*mm, "→ Begin routine immediately")
    y -= 18*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "Red-Light Recovery",
        "Dim everything, lower your voice, add extra routine steps. It'll take longer but you can get there. "
        "Tomorrow: aim for Stage 1.",
        bg=RED_LT, accent=colors.HexColor("#E53E3E"), text_color=colors.HexColor("#742A2A"))


def page_ch4_opener(c, page_num):
    chapter_opener(c, "04", "CHAPTER FOUR",
                   "Building the\nFoundation:\nRoutine, Environment\n& Night Feeds",
                   "The bedtime routine is not a suggestion. It is the\nphysiological trigger that prepares your baby's\nbrain and body for sleep — every single night.",
                   page_num)


def page_ch4_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Four", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER FOUR", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Building the Foundation", 20*mm, y - 8*mm, size=20)
    y -= 20*mm
    body_text(c,
        "Before any sleep training method will work, three foundations need to be solid: a consistent routine, "
        "an optimised sleep environment, and a clear understanding of which night feeds are nutritional "
        "and which are habitual.",
        20*mm, y, W - 40*mm)
    y -= 26*mm
    section_heading(c, "The Foundation Bedtime Routine", 20*mm, y, size=13)
    y -= 10*mm
    # Routine steps (visual numbered flow)
    routine = [
        ("1", "Bath or warm wash", "Cleanse and soothe your little one."),
        ("2", "Lotion massage", "Hydrate skin with a gentle massage."),
        ("3", "Pyjamas & sleep sack", "Dress in comfortable layers for sleep."),
        ("4", "Feed", "Provide final nourishment — not to full sleep."),
        ("5", "Wind-down ritual", "One song or book in dim light, then crib awake."),
    ]
    rw = (W - 44*mm)/2 - 2*mm
    rx = 20*mm; ry = y
    for i, (num, title, desc) in enumerate(routine):
        col = i % 2; row = i // 2
        bx = 20*mm + col*(rw + 4*mm)
        by = ry - row * 26*mm
        rrect(c, bx, by - 22*mm, rw, 22*mm, r=2.5*mm, fill_color=WHITE, stroke_color=CREAM_MID, lw=0.5)
        c.setFillColor(NAVY)
        c.circle(bx + 7*mm, by - 11*mm, 5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(bx + 7*mm, by - 13.5*mm, num)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(bx + 14*mm, by - 8*mm, title)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 8)
        c.drawString(bx + 14*mm, by - 17*mm, desc)
    y -= 70*mm
    c.setFillColor(GOLD)
    c.setFont("Helvetica-BoldOblique", 14)
    c.drawCentredString(W/2, y, "Start tonight")
    y -= 14*mm
    body_text(c,
        "The sequence matters as much as the steps themselves. Repetition in the same order, every night, trains the "
        "brain to expect sleep at the end of the sequence. Within 7–10 nights of a consistent routine, most babies will "
        "begin to show settling cues — quieting, slowing — as the routine progresses, even before they are placed in the crib.",
        20*mm, y, W-40*mm)
    y -= 28*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "The Critical Rule About Feeding",
        "Do not let your baby fall asleep during the feed. Feed should come early enough in the routine that they finish "
        "awake, so that the actual sleep-onset happens in the crib, not on the breast or bottle. If your baby is "
        "falling asleep while feeding, move the feed earlier — before the final wind-down steps.",
        bg=AMBER_LT, accent=AMBER)


def page_ch4_environment(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Four", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    section_heading(c, "The Ideal Sleep Environment", 20*mm, y - 8*mm, size=16)
    y -= 22*mm
    # Environment 2-col
    env = [
        ("DARKNESS", NAVY,
         "True blackout is non-negotiable. Even small LED lights from monitors and power sockets can interfere "
         "with melatonin production. Use electrical tape on all lights inside the sleep room."),
        ("SOUND", TEAL,
         "White noise at 65–70dB (about the level of a shower) helps mask household noise that causes partial "
         "arousals. Place the machine across the room, never inside the crib."),
        ("TEMPERATURE", colors.HexColor("#553C9A"),
         "The ideal sleep room temperature is 68–72°F (20–22°C). A baby who is too warm will sleep shorter. "
         "Use a sleep sack appropriate for the room temperature rather than loose blankets."),
        ("THE CRIB", colors.HexColor("#276749"),
         "Firm, flat mattress. Fitted sheet only. No bumpers, pillows, positioners, or stuffed animals. "
         "Every sleep, every time — safe sleep is not negotiable."),
    ]
    col_w = (W - 44*mm)/2
    bx = 20*mm; by = y
    for i, (title, accent, body) in enumerate(env):
        col = i % 2; row = i // 2
        cx = 20*mm + col*(col_w + 4*mm)
        cy = by - row * 45*mm
        rrect(c, cx, cy - 40*mm, col_w, 40*mm, r=3*mm, fill_color=WHITE, stroke_color=CREAM_MID, lw=0.5)
        c.setFillColor(accent)
        c.rect(cx, cy - 40*mm, 3.5, 40*mm, fill=1, stroke=0)
        c.setFillColor(accent)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(cx + 6*mm, cy - 8*mm, title)
        style = ParagraphStyle('e', fontName='Helvetica', fontSize=8.5,
                               textColor=SLATE, leading=13)
        p = Paragraph(body, style)
        p.wrapOn(c, col_w - 10*mm, 35*mm)
        p.drawOn(c, cx + 6*mm, cy - 38*mm)
    y -= 100*mm
    section_heading(c, "Night Feeds by Age: When to Reduce", 20*mm, y, size=14)
    y -= 10*mm
    feed_data = [
        ("0–3 months",  "●●●●", "Not Yet — These Are Nutritional", RUST),
        ("3–4 months",  "●●●",  "Start Reducing Gradually",         AMBER),
        ("4–6 months",  "●●○",  "Start Reducing Gradually",         AMBER),
        ("6–9 months",  "●○",   "Most Babies Can Handle Zero",      TEAL),
        ("9+ months",   "○",    "Most Babies Can Handle Zero",      TEAL),
    ]
    for age, dots, note, dot_color in feed_data:
        hrule(c, 20*mm, y - 1*mm, W-40*mm, color=CREAM_MID, lw=0.3)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20*mm, y + 2*mm, age)
        c.setFillColor(dot_color)
        c.setFont("Helvetica", 12)
        c.drawString(60*mm, y + 2*mm, dots)
        rrect(c, 95*mm, y - 2*mm, 80*mm, 10*mm, r=1.5*mm, fill_color=dot_color)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(135*mm, y + 2*mm, note)
        y -= 12*mm
    y -= 8*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "Habitual vs. Nutritional Feeds",
        "A nutritional feed is one where your baby transfers significant volume and feeds with intent. "
        "A habitual feed is one where they latch briefly, snack, and drift back to sleep. The goal is to eliminate "
        "habitual feeds — not nutritional ones — and you can usually tell the difference by how your baby nurses. "
        "A hungry baby drinks purposefully. A habit-feeder flutters.",
        bg=CREAM_MID, accent=NAVY)


def page_ch5_opener(c, page_num):
    chapter_opener(c, "05", "CHAPTER FIVE",
                   "Sleep Training\nMethods —\nChoosing What\nFits Your Family",
                   "An honest, evidence-based comparison of every major\nsleep training approach — with the data on what\nworks, for whom, and why.",
                   page_num)


def page_ch5_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Five", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER FIVE", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Choosing Your Method", 20*mm, y - 8*mm, size=20)
    y -= 18*mm
    body_text(c,
        "There is no universally \"best\" sleep training method. The best method is the one you will implement "
        "consistently — and consistently is the only thing that matters.",
        20*mm, y, W-40*mm)
    y -= 18*mm
    # Methods table
    table_data = [
        ["Method", "Cry Level", "Speed", "Best For"],
        ["Extinction (CIO)", "High initially", "3–5 nights", "High-sleep-need families; persistent temperaments"],
        ["Ferber / Graduated", "Moderate", "5–7 nights", "Most temperaments; parents who need to do something"],
        ["Chair / Camping Out", "Low–Moderate", "2–3 weeks", "Sensitive babies; parents not ready to step back fully"],
        ["Fading", "Low", "3–4+ weeks", "Gentle approach; highly adaptable babies"],
        ["Pick Up / Put Down", "Low", "Variable", "Babies 3–5 months; high parental support preference"],
    ]
    col_widths = [40*mm, 28*mm, 26*mm, 73*mm]
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,1), (-1,-1), SLATE),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,1), (0,-1), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CREAM]),
        ('ALIGN', (1,0), (2,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.3, CREAM_MID),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    tw, th = t.wrapOn(c, W-40*mm, 100*mm)
    t.drawOn(c, 20*mm, y - th)
    y -= th + 12*mm
    section_heading(c, "The Evidence", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "A 2019 randomised controlled trial in <i>Pediatrics</i> followed children who underwent sleep training up "
        "to age 6 and found no measurable differences in stress levels, emotional development, attachment quality, "
        "or parent-child relationship strength compared to children whose sleep was not trained. The research is "
        "consistent: when implemented appropriately, sleep training is safe.",
        20*mm, y, W-40*mm)
    y -= 30*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "The Truth About Crying",
        "Crying during sleep training is distressing for parents — not harmful to babies. Brief, predictable periods "
        "of infant crying during a structured, consistent sleep training process have not been shown to cause harm in "
        "healthy, full-term babies over 4 months. The science is clear. Your feelings about it are valid. "
        "Both things can be true.",
        bg=colors.HexColor("#EBF8FF"), accent=TEAL)
    y -= 40*mm
    # 7 mistakes
    section_heading(c, "The 7 Mistakes That Sabotage Sleep Training", 20*mm, y, size=12)
    y -= 10*mm
    mistakes = ["Starting & Stopping", "Wrong Age Method", "Too Many Changes",
                "Skipping Daytime", "Responding Fast", "Same Response Always", "Ignoring Yourself"]
    bw = (W - 44*mm) / 7
    bx = 20*mm
    for i, m in enumerate(mistakes):
        rrect(c, bx, y - 22*mm, bw - 1.5*mm, 22*mm, r=2*mm,
              fill_color=NAVY if i % 2 == 0 else NAVY_LITE)
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(bx + bw/2, y - 8*mm, str(i+1))
        style = ParagraphStyle('m', fontName='Helvetica', fontSize=6.5,
                               textColor=WHITE, leading=9, alignment=TA_CENTER)
        p = Paragraph(m, style)
        p.wrapOn(c, bw - 3*mm, 12*mm)
        p.drawOn(c, bx + 1.5*mm, y - 21*mm)
        bx += bw + 2


def page_ch6_opener(c, page_num):
    chapter_opener(c, "06", "CHAPTER SIX",
                   "The Seven Nights:\nWhat to Expect,\nNight by Night",
                   "The night-by-night breakdown every parent needs —\nincluding what the extinction burst is,\nwhy Night 3 is the make-or-break moment.",
                   page_num)


def page_ch6_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Six", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER SIX", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "The Seven Nights", 20*mm, y - 8*mm, size=20)
    y -= 18*mm
    body_text(c,
        "Knowing what to expect each night — before it happens — is what gets families through. Print this page. Refer to it at 3am.",
        20*mm, y, W-40*mm)
    y -= 16*mm
    # Night cards
    nights = [
        ("Night 1", "Hardest", "Foundation Night", RUST,
         "Often the hardest. Your baby doesn't know what's happening yet. Be calm, consistent, predictable."),
        ("Night 2", "Uncertain", "Signal Night", AMBER,
         "Baby's brain is starting to register the new pattern. Hold the line."),
        ("Night 3", "Hold On", "Extinction Burst", colors.HexColor("#6B46C1"),
         "The biggest test: prepare for the last push. This is working. Do NOT give up."),
        ("Night 4", "Turning", "Turning Point", TEAL,
         "Many families see a meaningful shift here. The burst has passed."),
        ("Night 5", "Shifting", "Breakthrough", GREEN_DK,
         "Noticeable improvement. Settling becomes faster."),
        ("Night 6", "Almost", "Reinforcing", colors.HexColor("#2B6CB0"),
         "Reinforce tonight by being exactly as consistent as every other night."),
        ("Night 7", "You Made It", "Success", NAVY,
         "You did it! Look at your log. Compare Night 7 to Night 1. Feel proud of this."),
    ]
    nw = (W - 44*mm) / 7
    nx = 20*mm
    for night, label_tag, sub, color, desc in nights:
        card_h = 55*mm
        is_n3 = night == "Night 3"
        bg = color if is_n3 else colors.HexColor("#F7FAFC")
        stroke = color
        rrect(c, nx, y - card_h, nw - 1.5*mm, card_h, r=2*mm,
              fill_color=bg, stroke_color=stroke, lw=1.2 if is_n3 else 0.5)
        c.setFillColor(WHITE if is_n3 else color)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(nx + nw/2, y - 8*mm, night)
        c.setFillColor(WHITE if is_n3 else GOLD if is_n3 else SLATE_LITE)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(nx + nw/2, y - 16*mm, label_tag)
        c.setFillColor(WHITE if is_n3 else color)
        c.setFont("Helvetica-BoldOblique", 7)
        c.drawCentredString(nx + nw/2, y - 23*mm, sub)
        style = ParagraphStyle('n', fontName='Helvetica', fontSize=6.5,
                               textColor=WHITE if is_n3 else SLATE, leading=9, alignment=TA_CENTER)
        p = Paragraph(desc, style)
        p.wrapOn(c, nw - 4*mm, 25*mm)
        p.drawOn(c, nx + 2*mm, y - card_h + 2*mm)
        nx += nw + 2
    y -= card_h + 10*mm
    body_text(c,
        "<i>Night 3 is the extinction burst — the most important night to hold. Every night after that is measurably easier.</i>",
        20*mm, y, W-40*mm, size=8.5, color=SLATE_LITE)
    y -= 18*mm
    section_heading(c, "The Extinction Burst: Night 3", 20*mm, y, size=13)
    y -= 8*mm
    body_text(c,
        "Night 3 is, counterintuitively, the hardest night of sleep training — not because the method is failing, "
        "but because it is working. When a previously reinforced behaviour (crying until picked up) stops being "
        "rewarded, the behaviour escalates dramatically before it extinguishes. This is called the extinction burst.",
        20*mm, y, W-40*mm)
    y -= 28*mm
    body_text(c,
        "It is the biological equivalent of a toddler tantrum when the iPad is taken away. It is not a red flag. "
        "It is proof the old system is breaking down. Families who push through Night 3 nearly always report a "
        "significant improvement on Night 4.",
        20*mm, y, W-40*mm)
    y -= 25*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "The 3-Night Rule",
        "Three consistent nights of returning to your method will tell you far more than one night of observation. "
        "Most families are pleasantly surprised by how quickly a well-trained baby resets.",
        bg=colors.HexColor("#EBF8FF"), accent=TEAL)


def page_ch7_opener(c, page_num):
    chapter_opener(c, "07", "CHAPTER SEVEN",
                   "When It's Not\nWorking —\nTroubleshooting\nSetbacks",
                   "Illness, regressions, travel, teething, and the other\ncurveballs that derail progress — and the exact\nstrategies to get back on track quickly.",
                   page_num)


def page_ch7_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Seven", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER SEVEN", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Troubleshooting", 20*mm, y - 8*mm, size=20)
    y -= 18*mm
    body_text(c,
        "Every family hits a setback. A night of illness. A trip across time zones. A developmental leap. A regression. "
        "The key is knowing the difference between a blip and a breakdown — and responding accordingly.",
        20*mm, y, W-40*mm)
    y -= 25*mm
    # Three sections side by side
    sections = [
        ("Sleep Regressions", NAVY,
         "Sleep regressions are developmental, not behavioural. They occur when your baby's brain is making a significant "
         "cognitive or motor leap that temporarily disrupts the sleep architecture. Common regression points: 4 months, "
         "8–10 months, 12 months, 18 months, 24 months.\n\n"
         "During a regression, maintain your routine and your consistency. Offer extra daytime connection. Do not introduce "
         "new sleep associations — a habit formed during a regression is harder to break than the regression itself."),
        ("Illness", TEAL,
         "When your baby is genuinely unwell — fever, ear infection, respiratory illness — suspend formal sleep training "
         "and offer whatever comfort they need. You are not undoing your progress. A sick baby needs your presence.\n\n"
         "When illness resolves, return to your method promptly. Most babies who were sleeping well before illness resettle "
         "within 3–5 nights of returning to the method. You are not starting over."),
        ("Travel & Time Zones", GOLD,
         "Shift bedtime by 15–20 minutes per day in the days before travel if crossing more than 2 time zones. "
         "On arrival, prioritise morning light exposure for eastward travel; evening light exposure for westward. "
         "Keep the sleep environment as consistent as possible — travel blackout curtains, portable white noise "
         "machine, familiar sleep sack."),
    ]
    sec_w = (W - 44*mm)/3
    sx = 20*mm
    for title, accent, body in sections:
        rrect(c, sx, y - 100*mm, sec_w - 2*mm, 100*mm, r=3*mm, fill_color=WHITE, stroke_color=CREAM_MID, lw=0.5)
        c.setFillColor(accent)
        c.rect(sx, y - 100*mm, 3.5, 100*mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(sx + 6*mm, y - 8*mm, title)
        style = ParagraphStyle('ts', fontName='Helvetica', fontSize=8.5,
                               textColor=SLATE, leading=13)
        p = Paragraph(body.replace('\n\n', '<br/><br/>'), style)
        p.wrapOn(c, sec_w - 10*mm, 90*mm)
        p.drawOn(c, sx + 6*mm, y - 98*mm)
        sx += sec_w + 2
    y -= 112*mm
    section_heading(c, "Signs You Need a Reset", 20*mm, y, size=13)
    y -= 8*mm
    col_w = (W-44*mm)/2
    warning = ["Bedtime taking noticeably longer than 2 weeks ago",
               "Night wakings increasing in number or duration",
               "New unintended habit has crept back",
               "Routine expanding with additions you didn't plan",
               "You are dreading bedtime before it begins"]
    reset = ["Move bedtime 15–20 min earlier for 3 nights",
             "Return routine to original order — strip all additions",
             "Identify and gradually remove any new sleep association over 3–5 nights",
             "Re-read your night response plan and follow it for 5 consecutive nights",
             "Tighten naps — day sleep drives night sleep"]
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(20*mm, y, "WARNING SIGNS")
    c.setFillColor(TEAL)
    c.drawString(20*mm + col_w + 4*mm, y, "THE FIVE-STEP RESET")
    y -= 8*mm
    for i, (w_item, r_item) in enumerate(zip(warning, reset)):
        c.setFillColor(RUST)
        c.circle(23.5*mm, y + 3, 2, fill=1, stroke=0)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 8.5)
        c.drawString(27*mm, y, w_item)
        # Reset item with number bubble
        c.setFillColor(TEAL)
        c.circle(20*mm + col_w + 7.5*mm, y + 3, 4*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(20*mm + col_w + 7.5*mm, y + 0.5, str(i+1))
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 8.5)
        style = ParagraphStyle('ri', fontName='Helvetica', fontSize=8.5, textColor=SLATE, leading=12)
        p = Paragraph(r_item, style)
        p.wrapOn(c, col_w - 12*mm, 20*mm)
        p.drawOn(c, 20*mm + col_w + 13*mm, y - 5)
        y -= 16*mm
    y -= 4*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "One Slip Does Not Erase the Progress",
        "A single difficult night is not a regression. Three or more consecutive difficult nights with a changing "
        "response pattern is. Know the difference — then act.",
        bg=CREAM_MID, accent=NAVY)


def page_ch8_opener(c, page_num):
    chapter_opener(c, "08", "CHAPTER EIGHT",
                   "Toddlers, Big\nKids & The\nBedtime Stall",
                   "The advanced degree in sleep challenges: everything\nfrom the 'one more story' loop to midnight migrations\nand the art of the firm, loving limit.",
                   page_num)


def page_ch8_content(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Chapter Eight", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CHAPTER EIGHT", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Toddlers & the Bedtime Stall", 20*mm, y - 8*mm, size=18)
    y -= 18*mm
    body_text(c,
        "Toddler sleep resistance is a different beast entirely. Your baby's sleep was largely a biological puzzle. "
        "Your toddler's sleep is a negotiation — and they have been studying you for months.",
        20*mm, y, W-40*mm)
    y -= 20*mm
    section_heading(c, "Why Toddlers Stall", 20*mm, y, size=13, color=NAVY)
    y -= 8*mm
    body_text(c,
        "Toddler sleep challenges are less about biology and more about development. Between 18 months and 3 years, "
        "toddlers are asserting autonomy, testing limits, and developing a powerful will. Common disruptions: the "
        "curtain call, boundary testing, nap refusal, night terrors, and the 5 a.m. wake.",
        20*mm, y, W-40*mm)
    y -= 28*mm
    section_heading(c, "Limits With Warmth: The Toddler Rule Book", 20*mm, y, size=12, color=NAVY)
    y -= 10*mm
    rules = [
        ("One Pass Rule",
         "After bedtime, your toddler gets one pass — one 'get out of bed free' for any reason. After it's used, "
         "they go straight back to bed, every time, same response."),
        ("Consistent Response",
         "'It's sleep time. Back to bed.' Warm, firm, boring. Same words, same tone, every single time."),
        ("The Goodbye Ritual",
         "Something they can count on to mark the real end — a special handshake, a specific song — always the same."),
        ("OK-to-Wake Clock",
         "A clock that glows green when it's okay to get up — game-changing for early risers."),
    ]
    for r_title, r_body in rules:
        c.setFillColor(TEAL)
        c.circle(23.5*mm, y + 3, 2.5, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(27*mm, y, r_title + ":")
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 9)
        style = ParagraphStyle('r', fontName='Helvetica', fontSize=9, textColor=SLATE, leading=13)
        p = Paragraph(r_body, style)
        p.wrapOn(c, W - 50*mm, 20*mm)
        p.drawOn(c, 27*mm, y - 15)
        y -= p.height + 12
    y -= 8*mm
    hrule(c, 20*mm, y, W-40*mm, color=DIVIDER)
    y -= 10*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "The Door Rule",
        "Tell your toddler clearly: 'If you stay in your bed, the door stays open. If you come out, the door closes.' "
        "Follow through every single time. The door being closed is not a punishment — it is a natural consequence "
        "of leaving the safe sleep space. Most toddlers choose the open door within 3–4 nights.",
        bg=NAVY, accent=GOLD, text_color=CREAM)


def page_sleep_promise(c, page_num):
    # Dark full-bleed closing page
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY_MID)
    c.circle(W + 15*mm, H/2, 90*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0, W, 3*mm, fill=1, stroke=0)
    std_footer(c, page_num)
    y = H - 45*mm
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W/2, y, "My Sleep Promise")
    c.setFillColor(GOLD)
    c.rect(W/2 - 15*mm, y - 6*mm, 30*mm, 2, fill=1, stroke=0)
    y -= 22*mm
    promises = [
        "For the next seven days, I will keep bedtime simple and in the same order every night.",
        "I will watch awake windows and act on them — before overtiredness sets in.",
        "I will decide how I will respond to night wakings before the night begins.",
        "I will wait before I go in, and give my baby the chance to resettle independently.",
        "I will not judge the whole plan on the basis of one difficult night.",
        "I will stay consistent — especially on the nights when it is hardest.",
        "I will remember that I am not just surviving the night. I am teaching my baby a skill they will use for the rest of their life.",
        "I will take care of myself — because my baby needs a rested parent, not a perfect one.",
    ]
    for promise in promises:
        c.setFillColor(GOLD)
        c.setFont("Helvetica", 12)
        c.drawString(25*mm, y, "✦")
        style = ParagraphStyle('pr', fontName='Helvetica-Oblique', fontSize=10.5,
                               textColor=CREAM, leading=15)
        p = Paragraph(promise, style)
        p.wrapOn(c, W - 55*mm, 30*mm)
        p.drawOn(c, 33*mm, y - p.height + 10)
        y -= p.height + 4
    y -= 12*mm
    hrule(c, W/2 - 20*mm, y, 40*mm, color=SLATE_LITE)
    y -= 10*mm
    c.setFillColor(SLATE_LITE)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, y, "With love and solidarity,")
    y -= 12
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W/2, y, "Six & Thriving")
    y -= 14
    c.setFillColor(SLATE_LITE)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(W/2, y, "Sleep is coming. For both of you.")


def page_bonus_opener(c, page_num):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold-amber gradient effect
    for i in range(20):
        alpha = i / 20.0
        r = int(0x0D + (0xC9 - 0x0D)*alpha*0.3)
        g = int(0x1B + (0xA8 - 0x1B)*alpha*0.3)
        b = int(0x3E + (0x4C - 0x3E)*alpha*0.1)
        c.setFillColor(colors.Color(r/255, g/255, b/255))
        c.rect(0, i*(H/20), W, H/20+1, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0, W, 3*mm, fill=1, stroke=0)
    std_footer(c, page_num)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(20*mm, H - 28*mm, "BONUS SECTION")
    c.setFillColor(NAVY_LITE)
    c.setFont("Helvetica-Bold", 70)
    c.drawString(14*mm, H/2 - 10*mm, "BONUS")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(20*mm, H/2 - 40*mm, "Quick-Reference")
    c.drawString(20*mm, H/2 - 60*mm, "Checklists &")
    c.drawString(20*mm, H/2 - 80*mm, "Tools")
    c.setFillColor(GOLD_LITE)
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawString(20*mm, H/2 - 96*mm, "Tear-out ready. Print them. Stick them to the fridge.")
    c.drawString(20*mm, H/2 - 109*mm, "Use them on the hard nights when reading feels like too much.")


def page_bonus_checklist(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Bonus One", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "BONUS ONE", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Bedtime Routine Checklist", 20*mm, y - 8*mm, size=18)
    y -= 16*mm
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(20*mm, y, "Run through every night in the same order. Consistency is the method.")
    y -= 14*mm
    checklist = [
        "Transition signal given — lights dimmed, specific phrase spoken (\"OK, it\'s sleep time\")",
        "All screens off and active play ended at least 30 minutes before routine begins",
        "Bath or warm wipe-down completed",
        "Lotion massage — slow, calming strokes (optional but highly effective)",
        "Pyjamas and age-appropriate sleep sack on",
        "Feed given in dim, quiet room — baby must not fall fully asleep during feed",
        "1–3 books or songs in nursing chair — low voice, calm pace",
        "Final goodnight phrase said (same words, every night)",
        "White noise machine on (65–70dB, across the room)",
        "Room fully dark — all LEDs covered, true blackout confirmed",
        "Baby placed in crib drowsy but awake — not fully asleep",
        "Parent exits calmly and consistently",
    ]
    for item in checklist:
        # Checkbox
        c.setStrokeColor(DIVIDER)
        c.setLineWidth(1)
        c.rect(20*mm, y - 2*mm, 4.5*mm, 4.5*mm, fill=0, stroke=1)
        hrule(c, 26*mm, y - 2.5*mm, W-50*mm, color=CREAM_MID, lw=0.3)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 9)
        c.drawString(27*mm, y, item)
        y -= 12.5
    y -= 10*mm
    section_heading(c, "Awake Window Quick Reference", 20*mm, y, size=14)
    y -= 8*mm
    table_data = [
        ["Age", "Awake Window", "Daily Naps", "Target Bedtime"],
        ["0–6 weeks",    "45–60 min",  "4–5", "Variable"],
        ["6–12 weeks",   "60–90 min",  "4",   "8–9 pm"],
        ["3–4 months",   "90 min",     "3–4", "7:30–8:30 pm"],
        ["4–6 months",   "2 hrs",      "3",   "7–8 pm"],
        ["6–8 months",   "2.5 hrs",    "2–3", "7–8 pm"],
        ["8–12 months",  "3–3.5 hrs",  "2",   "6:30–7:30 pm"],
        ["12–18 months", "4–5 hrs",    "1–2", "7–7:30 pm"],
        ["18–24 months", "5–6 hrs",    "1",   "7–7:30 pm"],
    ]
    col_widths = [35*mm, 38*mm, 28*mm, 66*mm]
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR', (0,1), (-1,-1), SLATE),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,1), (0,-1), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CREAM]),
        ('ALIGN', (1,0), (3,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.3, CREAM_MID),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    t.wrapOn(c, W-40*mm, 80*mm)
    t.drawOn(c, 20*mm, y - t._height)


def page_bonus_tracker(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Bonus Two", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "BONUS TWO", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "7-Day Sleep Tracker", 20*mm, y - 8*mm, size=18)
    y -= 16*mm
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(20*mm, y,
        "Fill this in each morning. Patterns will emerge by Day 3–4 and will motivate you through the harder nights.")
    y -= 14*mm
    cols = ["Day", "Last Nap Ended", "Bedtime", "Time to Settle", "Night Wakings", "Wake Time", "Notes"]
    col_ws = [16*mm, 30*mm, 23*mm, 27*mm, 27*mm, 23*mm, 41*mm]
    rows = [cols] + [[f"Day {i}", "", "", "", "", "", ""] for i in range(1,8)]
    t = Table(rows, colWidths=col_ws, rowHeights=[10*mm]+[13*mm]*7)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR', (0,1), (-1,-1), SLATE),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,1), (0,-1), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CREAM]),
        ('GRID', (0,0), (-1,-1), 0.4, DIVIDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    t.wrapOn(c, W-40*mm, 120*mm)
    t.drawOn(c, 20*mm, y - t._height)
    y -= t._height + 14*mm
    section_heading(c, "Safe Sleep Checklist", 20*mm, y, size=14)
    y -= 8*mm
    c.setFillColor(SLATE_LITE)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(20*mm, y, "AAP-aligned. Run through this every night until it is automatic.")
    y -= 14*mm
    col_w = (W-44*mm)/2
    surface = [
        "Firm, flat mattress - no incline, pillow-top, or wedge",
        "Fitted sheet only - no loose blankets, bumpers, or pillows",
        "No stuffed animals or positioners in the crib",
        "Sleep sack used in place of a blanket",
        "Baby placed on their back - every sleep, every time",
        "Crib, bassinet, or play yard only - not swing or car seat",
    ]
    room = [
        "Room temperature 68-72°F / 20-22°C confirmed",
        "Baby's chest warm but not sweaty",
        "True blackout - you cannot see your hand in the room",
        "White noise running at low continuous level",
        "Monitor LEDs covered with electrical tape",
        "No nightlight, or red-spectrum only",
    ]
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(20*mm, y, "SLEEP SURFACE")
    c.drawString(20*mm + col_w + 4*mm, y, "THE ROOM")
    y -= 10*mm
    for i, (s_item, r_item) in enumerate(zip(surface, room)):
        c.setStrokeColor(DIVIDER)
        c.setLineWidth(0.8)
        c.rect(20*mm, y - 2*mm, 4*mm, 4*mm, fill=0, stroke=1)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 8.5)
        style = ParagraphStyle('sl', fontName='Helvetica', fontSize=8.5, textColor=SLATE, leading=12)
        p = Paragraph(s_item, style)
        p.wrapOn(c, col_w - 8*mm, 15*mm)
        p.drawOn(c, 26*mm, y - 4)
        c.rect(20*mm + col_w + 4*mm, y - 2*mm, 4*mm, 4*mm, fill=0, stroke=1)
        p2 = Paragraph(r_item, style)
        p2.wrapOn(c, col_w - 8*mm, 15*mm)
        p2.drawOn(c, 26*mm + col_w + 4*mm, y - 4)
        y -= max(p.height, p2.height) + 6


def page_conclusion(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "Conclusion", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "CONCLUSION", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "What You've Built", 20*mm, y - 8*mm, size=18)
    y -= 18*mm
    takeaways = [
        "Your baby's sleep challenges are not your fault — they're biology, development, and habit.",
        "Sleep science gives you real tools: awake windows, circadian rhythms, sleep pressure, sleep cycles.",
        "Reading cues and responding before overtiredness sets in changes everything.",
        "A consistent bedtime routine is one of the most powerful tools you have.",
        "The sleep environment does active work all night — make sure it's working for you.",
        "Sleep training is not one-size-fits-all — the best method is the one you commit to.",
        "Night wakings can be handled strategically without creating new long-term habits.",
        "Consistency, especially on hard nights, is the bridge between where you are and where you want to be.",
    ]
    for takeaway in takeaways:
        c.setFillColor(TEAL)
        c.circle(23.5*mm, y + 3, 2.5, fill=1, stroke=0)
        style = ParagraphStyle('t', fontName='Helvetica', fontSize=9.5, textColor=SLATE, leading=14)
        p = Paragraph(takeaway, style)
        p.wrapOn(c, W-52*mm, 20*mm)
        p.drawOn(c, 27*mm, y - p.height + 10)
        hrule(c, 27*mm, y - p.height - 2, W-52*mm, color=CREAM_MID, lw=0.3)
        y -= p.height + 8
    y -= 10*mm
    callout_box(c, 20*mm, y, W-40*mm,
        "Hold This Close",
        "When it's hard, remember why you're here. A baby who sleeps well is a baby who thrives. "
        "A parent who sleeps is a parent who's fully present. Sleep is not a luxury — it is a foundation.",
        bg=NAVY, accent=GOLD, text_color=CREAM)
    y -= 38*mm
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(20*mm, y, "Go build that foundation. I'm cheering for you.")
    y -= 14
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "— Six & Thriving")


def page_about(c, page_num):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    std_header(c, "About the Author", page_num)
    std_footer(c, page_num)
    y = H - 38*mm
    label(c, "ABOUT THE AUTHOR", 20*mm, y + 8*mm, color=GOLD)
    hrule(c, 20*mm, y + 5*mm, W-40*mm, color=DIVIDER)
    section_heading(c, "Six & Thriving", 20*mm, y - 8*mm, size=22)
    y -= 20*mm
    body_text(c,
        "Six & Thriving is the pen name of a mother of six who has spent the better part of a decade in the "
        "trenches of infant and toddler sleep. With a set of twins tucked in the middle, a strong-willed "
        "firstborn, and three more uniquely wonderful sleep puzzles, she has lived through nearly every sleep "
        "scenario this book describes.",
        20*mm, y, W-40*mm, size=10)
    y -= 32*mm
    body_text(c,
        "This book was written in the quiet hours — fuelled by cold coffee, hard-won experience, and the "
        "absolute conviction that sleep is possible for every family, with the right approach and the right support.",
        20*mm, y, W-40*mm, size=10)
    y -= 28*mm
    body_text(c,
        "<b>Six & Thriving</b> creates practical, evidence-informed content for exhausted parents who need "
        "real answers, not gentle theory.",
        20*mm, y, W-40*mm, size=10)
    y -= 28*mm
    hrule(c, 20*mm, y, W-40*mm, color=DIVIDER)
    y -= 16*mm
    c.setFillColor(SLATE)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawString(20*mm, y, '"Every single one of my babies learned to sleep.')
    y -= 16
    c.drawString(20*mm, y, 'Every single one."')
    y -= 14
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, y, "— Six & Thriving")
    y -= 30*mm
    rrect(c, 20*mm, y - 26*mm, W-40*mm, 26*mm, r=3*mm, fill_color=NAVY)
    c.setFillColor(CREAM_MID)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, y - 11*mm, "Thank you for trusting Six & Thriving with your baby's sleep journey.")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-BoldOblique", 11)
    c.drawCentredString(W/2, y - 21*mm, "Sleep is coming. For both of you.")
    y -= 38*mm
    hrule(c, W/2 - 30*mm, y, 60*mm, color=DIVIDER)
    y -= 10*mm
    c.setFillColor(SLATE_LITE)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(W/2, y,
        "Disclaimer: This eBook is for educational purposes only and does not constitute medical advice.")
    c.drawCentredString(W/2, y-9,
        "Always consult your paediatrician or qualified health professional about your child's specific needs.")
    y -= 18
    c.setFillColor(SLATE_LITE)
    c.drawCentredString(W/2, y, "Copyright © 2026 Six & Thriving · All rights reserved · sixandthriving.com")


# ═══════════════════════════════════════════════════════════════════════════════
#  ASSEMBLE DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════════

OUT = "SleepBabyPlease_PREMIUM_2026.pdf"

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Sleep, Baby. Please. — Six & Thriving")
c.setAuthor("Six & Thriving")
c.setSubject("The Evidence-Based Roadmap to Restful Nights")
c.setCreator("Six & Thriving Production System 2026")

pages = [
    (page_cover,            None),
    (page_copyright,        2),
    (page_toc,              3),
    (page_intro_letter,     4),
    (page_fast_track,       5),
    (page_ch1_opener,       6),
    (page_ch1_content,      7),
    (page_ch1_content2,     8),
    (page_ch2_opener,       10),
    (page_ch2_content,      11),
    (page_awake_windows,    13),
    (page_ch3_opener,       14),
    (page_ch3_content,      15),
    (page_ch4_opener,       18),
    (page_ch4_content,      19),
    (page_ch4_environment,  20),
    (page_ch5_opener,       22),
    (page_ch5_content,      23),
    (page_ch6_opener,       25),
    (page_ch6_content,      26),
    (page_ch7_opener,       29),
    (page_ch7_content,      30),
    (page_ch8_opener,       31),
    (page_ch8_content,      32),
    (page_sleep_promise,    33),
    (page_bonus_opener,     34),
    (page_bonus_checklist,  35),
    (page_bonus_tracker,    36),
    (page_conclusion,       37),
    (page_about,            38),
]

for fn, pg in pages:
    if pg is None:
        fn(c)
    else:
        fn(c, pg)
    c.showPage()

c.save()
print(f"✅ Done — {len(pages)} pages → {OUT}")
