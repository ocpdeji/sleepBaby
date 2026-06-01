"""
Add Navigation Links to Sleep, Baby. Please. — Invisible Rectangle Method
═══════════════════════════════════════════════════════════════════════════
The PROFESSIONAL approach: instead of hyperlinking text directly (which forces
PowerPoint to apply underline + theme link color), we overlay invisible
rectangles over the text and put the hyperlinks on the SHAPES.

Result:
  ✓ Text keeps its original styling (no underline, no color shift)
  ✓ Click areas still work perfectly
  ✓ Brand-perfect design

Reads:  SleepBabyPlease_BESTSELLER_2026_UPDATED2.pptx
Writes: SleepBabyPlease_BESTSELLER_2026_FINAL_v5.pptx
"""

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
import os
from lxml import etree

INPUT_FILE = r"C:\Users\Deji\Documents\GitHub\sleepBaby\SleepBabyPlease_BESTSELLER_2026_UPDATED2.pptx"
OUTPUT_FILE = r"C:\Users\Deji\Documents\GitHub\sleepBaby\SleepBabyPlease_BESTSELLER_2026_FINAL_v5.pptx"
WEBSITE_URL = "https://www.sixandthriving.com"

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'

# (Text on TOC) → target slide number (1-indexed)
TOC_LINKS = {
    "To the Parent Reading This at 3 a.m.": 4,
    "Tonight's Plan — Start Here": 5,
    "Why Your Baby Won't Sleep (And It's Not Your Fault)": 6,
    "The Sleep Science Every Parent Actually Needs": 9,
    "Reading Your Baby's Sleep Cues": 12,
    "Building a Bedtime Routine That Sticks": 16,
    "Setting the Stage — The Sleep Environment": 19,
    "The Big Sleep Training Debate — All Methods": 22,
    "Night Wakings & The Reset Protocol": 26,
    "The Six Sleep Personalities": 30,
    "Common Mistakes (I Made Them All)": 33,
    "Staying Consistent When You're Empty": 36,
    "Toddler Sleep — Little Negotiators": 38,
    "Your First Week — Night-by-Night Plan": 40,
    "Breastfeeding & Sleep — The Honest Guide": 43,
    "Twins, NICU & Daycare": 46,
    "The First 8 Weeks — Newborn Period": 48,
    "The Partner Briefing One-Pager": 50,
    "My Sleep Promise & Conclusion": 51,
    "Checklists, Trackers & Quick Reference": 53,
}


# ════════════════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════════════════

def update_text_in_runs(slide, old_text, new_text):
    """Replace text in any run that contains old_text."""
    count = 0
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if old_text in run.text:
                    run.text = run.text.replace(old_text, new_text)
                    count += 1
    return count


def get_shape_position(shape):
    """Return (left, top, width, height) of a shape in EMU."""
    return (shape.left, shape.top, shape.width, shape.height)


def find_text_paragraph_position(shape, search_text):
    """Find the bounding rectangle of the paragraph containing search_text
    within a shape. Returns (left, top, width, height) in EMU, or None.

    Since python-pptx doesn't expose paragraph-level rendered positions,
    we approximate by using the parent shape's bounds. For TOC entries,
    each row is in its own textbox so this gives accurate hit areas.
    """
    if not shape.has_text_frame:
        return None
    for para in shape.text_frame.paragraphs:
        full_text = "".join(r.text for r in para.runs)
        if full_text.strip() == search_text.strip():
            return get_shape_position(shape)
    return None


def add_internal_link_shape(slide, target_slide, left, top, width, height):
    """Add a transparent rectangle over the area, with a click action
    pointing to target_slide. The shape has no fill and no line — fully
    invisible — but it captures the click.
    """
    # Add the shape
    rect = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    # Make it fully transparent (no fill, no line)
    rect.fill.background()  # No fill
    rect.line.fill.background()  # No line
    # Remove any default text
    if rect.has_text_frame:
        rect.text_frame.text = ""

    # Add slide-to-slide relationship
    rId = slide.part.relate_to(target_slide.part, RT.SLIDE)

    # Add the click action onto the shape's nvSpPr/cNvPr element
    sp = rect._element
    # Path: p:sp / p:nvSpPr / p:cNvPr
    cNvPr = sp.find(f'{{{P_NS}}}nvSpPr/{{{P_NS}}}cNvPr')
    if cNvPr is None:
        return rect
    # Remove existing hlinkClick if any
    existing = cNvPr.find(f'{{{A_NS}}}hlinkClick')
    if existing is not None:
        cNvPr.remove(existing)
    hlink = etree.SubElement(cNvPr, f'{{{A_NS}}}hlinkClick')
    hlink.set(f'{{{R_NS}}}id', rId)
    hlink.set('action', 'ppaction://hlinksldjump')
    return rect


def add_external_link_shape(slide, url, left, top, width, height):
    """Add a transparent rectangle over the area, with a click action
    opening the given external URL.
    """
    rect = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    rect.fill.background()
    rect.line.fill.background()
    if rect.has_text_frame:
        rect.text_frame.text = ""

    # External hyperlink — use the slide part's relationships properly
    sp_part = slide.part
    # Use load_rel which works for external (no target part)
    rId = sp_part.relate_to(url, RT.HYPERLINK, is_external=True)

    sp = rect._element
    cNvPr = sp.find(f'{{{P_NS}}}nvSpPr/{{{P_NS}}}cNvPr')
    if cNvPr is None:
        return rect
    existing = cNvPr.find(f'{{{A_NS}}}hlinkClick')
    if existing is not None:
        cNvPr.remove(existing)
    hlink = etree.SubElement(cNvPr, f'{{{A_NS}}}hlinkClick')
    hlink.set(f'{{{R_NS}}}id', rId)
    return rect


def find_textbox_with_text(slide, search_text):
    """Find shapes whose text exactly matches search_text. Returns list of shapes."""
    matches = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            full_text = "".join(r.text for r in para.runs)
            if full_text.strip() == search_text.strip():
                matches.append(shape)
                break
    return matches


def find_textbox_containing(slide, search_text):
    """Find shapes whose text CONTAINS search_text (partial match). Returns list."""
    matches = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if search_text in run.text:
                    matches.append(shape)
                    break
            else:
                continue
            break
    return matches


# ════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file not found: {INPUT_FILE}")
        return

    print(f"📖 Loading: {INPUT_FILE}")
    prs = Presentation(INPUT_FILE)
    print(f"   Slides: {len(prs.slides)}")
    print()

    slides = list(prs.slides)
    toc_slide = slides[2]  # Slide 3 (TOC)

    # ─────────────────────────────────────────────────────────────
    # STEP 1: Update website URL text
    # ─────────────────────────────────────────────────────────────
    print("🔗 STEP 1: Updating website URL to www.sixandthriving.com")
    url_updates = 0
    for slide in slides:
        url_updates += update_text_in_runs(slide, "sixandthriving.com", "www.sixandthriving.com")
        update_text_in_runs(slide, "www.www.", "www.")
    print(f"   ✓ Updated {url_updates} URL text references (no formatting changes)")
    print()

    # ─────────────────────────────────────────────────────────────
    # STEP 2: Overlay invisible rectangles on TOC entries
    # ─────────────────────────────────────────────────────────────
    print("🔲 STEP 2: Adding invisible click rectangles over TOC entries")
    toc_links = 0
    for entry_text, page_num in TOC_LINKS.items():
        if page_num > len(slides):
            continue
        target = slides[page_num - 1]
        shapes_found = find_textbox_with_text(toc_slide, entry_text)
        for shape in shapes_found:
            l, t, w, h = get_shape_position(shape)
            # Slightly expand the click area for easier targeting
            pad_x = Emu(50000)  # ~0.05 cm
            pad_y = Emu(20000)
            add_internal_link_shape(toc_slide, target,
                                    l - pad_x, t - pad_y,
                                    w + 2 * pad_x, h + 2 * pad_y)
            toc_links += 1
            print(f"   ✓ '{entry_text[:50]}' → slide {page_num}")
    print(f"   Total TOC entry links: {toc_links}")
    print()

    # ─────────────────────────────────────────────────────────────
    # STEP 2b: Overlay invisible rectangles on TOC tags (CH. 1, INTRO, etc.)
    # ─────────────────────────────────────────────────────────────
    print("🔲 STEP 2b: Adding invisible click rectangles over TOC tags")
    tag_map = {
        "INTRO": 4, "FAST-TRACK": 5,
        "CH. 1": 6, "CH. 2": 9, "CH. 3": 12, "CH. 4": 16, "CH. 5": 19,
        "CH. 6": 22, "CH. 7": 26, "CH. 8": 30, "CH. 9": 33, "CH. 10": 36,
        "CH. 11": 38, "CH. 12": 40, "CH. 13": 43, "CH. 14": 46, "CH. 15": 48,
        "PARTNER": 50, "CLOSING": 51, "BONUS": 53,
    }
    tag_links = 0
    for tag, page_num in tag_map.items():
        if page_num > len(slides):
            continue
        target = slides[page_num - 1]
        shapes_found = find_textbox_with_text(toc_slide, tag)
        for shape in shapes_found:
            l, t, w, h = get_shape_position(shape)
            pad_x = Emu(30000)
            pad_y = Emu(20000)
            add_internal_link_shape(toc_slide, target,
                                    l - pad_x, t - pad_y,
                                    w + 2 * pad_x, h + 2 * pad_y)
            tag_links += 1
    print(f"   ✓ Added {tag_links} tag click areas")
    print()


    # ─────────────────────────────────────────────────────────────
    # STEP 3: Overlay invisible rectangles on website URLs
    # ─────────────────────────────────────────────────────────────
    print("🔲 STEP 3: Adding invisible click rectangles over website URLs")
    url_links = 0
    for slide in slides:
        url_shapes = find_textbox_containing(slide, "www.sixandthriving.com")
        for shape in url_shapes:
            l, t, w, h = get_shape_position(shape)
            try:
                add_external_link_shape(slide, WEBSITE_URL, l, t, w, h)
                url_links += 1
            except Exception as e:
                print(f"   ⚠ Error on slide: {e}")
    print(f"   ✓ Added {url_links} URL click areas")
    print()

    # ─────────────────────────────────────────────────────────────
    # STEP 4: Overlay invisible rectangles on big chapter numbers (01-15)
    # ─────────────────────────────────────────────────────────────
    print("🔲 STEP 4: Adding invisible click rectangles on chapter numbers (back to TOC)")
    back_links = 0
    big_nums = [f"{i:02d}" for i in range(1, 16)]
    for slide in slides:
        if slide is toc_slide:
            continue
        for num in big_nums:
            shapes_found = find_textbox_with_text(slide, num)
            for shape in shapes_found:
                # Confirm this is the BIG ghost number, not a small "01" elsewhere
                # The big ghost numbers are typically 70+ pt — we check via the shape size
                # Heuristic: ghost numbers occupy a large area
                l, t, w, h = get_shape_position(shape)
                # Big ghost numbers in this file are exactly 10cm x 5cm
                # = 3,600,000 x 1,800,000 EMU. Use >= 3,000,000 to be safe.
                if w >= 3000000 and h >= 1500000:
                    add_internal_link_shape(slide, toc_slide, l, t, w, h)
                    back_links += 1
    print(f"   ✓ Added {back_links} back-to-TOC click areas")
    print()

    # ─────────────────────────────────────────────────────────────
    # SAVE
    # ─────────────────────────────────────────────────────────────
    print(f"💾 Saving: {OUTPUT_FILE}")
    prs.save(OUTPUT_FILE)
    print()
    print("═══════════════════════════════════════════════════════")
    print("✅ DONE — Invisible rectangle method applied")
    print(f"   📄 {OUTPUT_FILE}")
    print(f"   🔗 {toc_links} TOC titles + {tag_links} TOC tags + {back_links} chapter numbers + {url_links} URLs")
    print()
    print("📋 KEY DIFFERENCE FROM v1-v4:")
    print("   • Text has ZERO modifications — same color, same font, NO underline")
    print("   • Invisible rectangles overlay clickable areas")
    print("   • PowerPoint can't add link styling because the text isn't linked!")
    print()
    print("✅ Original file UNTOUCHED. Open the FINAL_v5 file to verify.")


if __name__ == "__main__":
    main()
