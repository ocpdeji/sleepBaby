import math
import random
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import simpleSplit

# ============================================================
#  SOFT LIFE PLANNER — Feminine Self-Care Ritual Cards
#  Customisable Configuration
#
#  QUICK START
#  -----------
#  1. pip install reportlab
#  2. Edit the PlannerConfig class below
#  3. Run:  python soft_life_planner.py
#  4. Your PDF is saved to OUTPUT_PATH (or auto-named)
# ============================================================

class PlannerConfig:

    # ── Identity ─────────────────────────────────────────────
    PLANNER_TITLE    = "SOFT LIFE"                    # Cover brand title
    PLANNER_SUBTITLE = "Self-Care Ritual Cards"       # Cover subtitle
    PLANNER_TAGLINE  = "Slow Down · Bloom · Be Held · Live Softly"
    PLANNER_EDITION  = "Feminine Wellness & Ritual Collection"
    PLANNER_YEAR     = 2025

    # ── Output ───────────────────────────────────────────────
    # Leave "" to auto-name, or set a full path e.g. "/Desktop/soft_life.pdf"
    OUTPUT_PATH = ""

    # ── Card Size & Layout ───────────────────────────────────
    # Each card prints as a full page (landscape or portrait)
    # Portrait card — beautiful for printing & cutting
    CARD_WIDTH  = 900    # ~3×5 inch at 300dpi (portrait)
    CARD_HEIGHT = 1260   # adjust to taste

    # Cards per PDF page (arranged as a grid for printable sheet)
    # 1 = one card per page (GoodNotes / digital)
    # 2 = 2-up layout (side by side)
    # 4 = 2×2 grid on an A4/Letter sheet
    CARDS_PER_PAGE = 1

    # ── Theme ────────────────────────────────────────────────
    # Choose ONE of:
    #   "blush_gold"      soft blush + warm gold (default)
    #   "lavender_cream"  lilac + ivory + silver
    #   "sage_linen"      earthy sage + warm cream
    #   "rose_marble"     deep rose + grey marble tones
    #   "peach_glow"      peachy sunset + terracotta
    #   "custom"          use CUSTOM_THEME dict below
    THEME_NAME = "blush_gold"

    # ── Custom Theme ─────────────────────────────────────────
    CUSTOM_THEME = {
        "C_BG":        "#FDF6F0",   # page / card background
        "C_BG2":       "#FAF0EC",   # alternate card bg
        "C_ACCENT":    "#C9896A",   # primary accent (buttons, borders)
        "C_ACCENT2":   "#E8C4A8",   # secondary accent
        "C_GOLD":      "#C9A96E",   # metallic gold details
        "C_INK":       "#3A2820",   # main body text
        "C_SECONDARY": "#7A5C50",   # secondary text
        "C_MUTED":     "#C4A898",   # muted / captions
        "C_BORDER":    "#EDD5C8",   # card border
        "C_PANEL":     "#FDF0E8",   # inner panel
        "C_WHITE":     "#FFFFFF",
        "C_DARK":      "#2A1810",   # deep dark for cover
        "C_FLORAL1":   "#E8B4B8",   # floral decoration 1
        "C_FLORAL2":   "#F5D5A0",   # floral decoration 2
        "C_FLORAL3":   "#B8D4C8",   # floral decoration 3
    }

    # ── Built-in Themes ──────────────────────────────────────
    THEMES = {
        "blush_gold": {
            "C_BG":        "#FDF6F0",
            "C_BG2":       "#FDF0F4",
            "C_ACCENT":    "#C0687A",
            "C_ACCENT2":   "#E8B4BE",
            "C_GOLD":      "#C9A040",
            "C_INK":       "#3A1C24",
            "C_SECONDARY": "#8A5060",
            "C_MUTED":     "#C4989E",
            "C_BORDER":    "#F0C8D0",
            "C_PANEL":     "#FDF4F6",
            "C_WHITE":     "#FFFFFF",
            "C_DARK":      "#2A0E18",
            "C_FLORAL1":   "#F0A8B4",
            "C_FLORAL2":   "#F5D590",
            "C_FLORAL3":   "#B8D8C8",
        },
        "lavender_cream": {
            "C_BG":        "#F9F6FD",
            "C_BG2":       "#F5F0FA",
            "C_ACCENT":    "#8B6BAE",
            "C_ACCENT2":   "#C8B0DC",
            "C_GOLD":      "#B8A060",
            "C_INK":       "#2A1A40",
            "C_SECONDARY": "#6A507A",
            "C_MUTED":     "#B0A0C0",
            "C_BORDER":    "#DDD0EE",
            "C_PANEL":     "#F6F2FC",
            "C_WHITE":     "#FFFFFF",
            "C_DARK":      "#180A30",
            "C_FLORAL1":   "#C8A8DC",
            "C_FLORAL2":   "#F0D898",
            "C_FLORAL3":   "#A8C8C0",
        },
        "sage_linen": {
            "C_BG":        "#F8F5EE",
            "C_BG2":       "#F4F0E8",
            "C_ACCENT":    "#6A8A70",
            "C_ACCENT2":   "#A8C0A8",
            "C_GOLD":      "#B89848",
            "C_INK":       "#1E2A1E",
            "C_SECONDARY": "#506050",
            "C_MUTED":     "#98A898",
            "C_BORDER":    "#C8D8C0",
            "C_PANEL":     "#F2F6EE",
            "C_WHITE":     "#FFFFFF",
            "C_DARK":      "#101A10",
            "C_FLORAL1":   "#D0C0A8",
            "C_FLORAL2":   "#E8D498",
            "C_FLORAL3":   "#A8C8A8",
        },
        "rose_marble": {
            "C_BG":        "#FAF4F4",
            "C_BG2":       "#F8F0F0",
            "C_ACCENT":    "#A84860",
            "C_ACCENT2":   "#D8A0B0",
            "C_GOLD":      "#C09050",
            "C_INK":       "#300818",
            "C_SECONDARY": "#784058",
            "C_MUTED":     "#C09098",
            "C_BORDER":    "#E8C0C8",
            "C_PANEL":     "#FDF6F6",
            "C_WHITE":     "#FFFFFF",
            "C_DARK":      "#200410",
            "C_FLORAL1":   "#E08898",
            "C_FLORAL2":   "#F0D098",
            "C_FLORAL3":   "#C0D0C8",
        },
        "peach_glow": {
            "C_BG":        "#FDF4EE",
            "C_BG2":       "#FCF0E8",
            "C_ACCENT":    "#C87848",
            "C_ACCENT2":   "#E8B890",
            "C_GOLD":      "#C89838",
            "C_INK":       "#381808",
            "C_SECONDARY": "#886040",
            "C_MUTED":     "#C89870",
            "C_BORDER":    "#F0C8A0",
            "C_PANEL":     "#FDF6F0",
            "C_WHITE":     "#FFFFFF",
            "C_DARK":      "#281008",
            "C_FLORAL1":   "#E8A880",
            "C_FLORAL2":   "#F5D090",
            "C_FLORAL3":   "#B8C8A8",
        },
    }

    # ── Cover Style ──────────────────────────────────────────
    # "petals"    — scattered botanical petal shapes
    # "arches"    — layered arch / frame aesthetic
    # "minimal"   — clean typographic cover
    COVER_STYLE = "petals"

    # ── Card Sections ────────────────────────────────────────
    # Each section generates multiple cards.
    # Set to False to skip any section.
    INCLUDE_BEAUTY_RITUALS     = True   # Morning & evening beauty rituals
    INCLUDE_SLOW_LIVING        = True   # Slow morning routines & daily rhythms
    INCLUDE_JOURNALING         = True   # Journaling prompts
    INCLUDE_WELLNESS            = True   # Wellness reminders & body care
    INCLUDE_GRATITUDE          = True   # Gratitude exercises
    INCLUDE_ROMANTICISE_LIFE   = True   # "Romanticise your life" activity cards
    INCLUDE_AFFIRMATIONS       = True   # Feminine affirmation cards
    INCLUDE_SEASONAL_RITUALS   = True   # Season-by-season ritual cards
    INCLUDE_BOUNDARIES_REST    = True   # Rest & boundary cards
    INCLUDE_VISION_DREAMING    = True   # Dream & manifestation cards

    # ── Typography ───────────────────────────────────────────
    # ReportLab built-in fonts only (no TTF needed):
    #   Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique
    #   Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic
    #   Courier, Courier-Bold, Courier-Oblique
    FONT_HEADING  = "Times-Italic"       # Card category / section heading
    FONT_TITLE    = "Times-Bold"         # Card title
    FONT_BODY     = "Times-Roman"        # Card body / prompt text
    FONT_CAPTION  = "Helvetica-Oblique"  # Small captions / labels
    FONT_ACCENT   = "Times-BoldItalic"   # Highlighted pull quotes

    # ── Decorative Elements ──────────────────────────────────
    SHOW_CORNER_ORNAMENTS = True   # Decorative corner flourishes
    SHOW_DIVIDERS         = True   # Thin rule dividers between sections
    SHOW_CARD_NUMBER      = True   # Small card number in corner
    SHOW_SECTION_BADGE    = True   # Category pill on each card


# ═══════════════════════════════════════════════════════════════════
#  CARD CONTENT LIBRARY
# ═══════════════════════════════════════════════════════════════════

BEAUTY_RITUAL_CARDS = [
    {
        "title": "The Golden Hour Cleanse",
        "subtitle": "Evening Beauty Ritual",
        "body": (
            "Light a candle. Fill your basin with warm water and a few drops of rose water. "
            "Cleanse slowly — this is not a chore, it's a ceremony. Pat dry with a soft cloth. "
            "Massage your face upward with two drops of facial oil. You are tending to yourself."
        ),
        "prompt": "What am I releasing from my skin and spirit tonight?",
        "icon": "✿",
    },
    {
        "title": "Silk & Ritual",
        "subtitle": "Morning Skin Awakening",
        "body": (
            "Begin with cool water splashed three times on your face — once for clarity, "
            "once for beauty, once for intention. Apply your serum with upward strokes. "
            "Take one minute to simply look at yourself with kindness. You are enough, exactly as you are."
        ),
        "prompt": "What affirmation will I speak to my reflection today?",
        "icon": "◇",
    },
    {
        "title": "The Petal Bath",
        "subtitle": "Luxe Bathing Ritual",
        "body": (
            "Draw a warm bath. Add Epsom salts, a few drops of lavender oil, and if you have them — "
            "dried rose petals. Play something soft. Stay for at least twenty minutes. "
            "This is your sacred hour. The world will wait."
        ),
        "prompt": "What tension am I soaking away? What feeling do I want to soak in?",
        "icon": "❀",
    },
    {
        "title": "Hair as Crown",
        "subtitle": "Weekly Hair Care Ritual",
        "body": (
            "Warm a small amount of oil between your palms. Work it through your hair from root to end. "
            "Wrap in a warm towel. Put on music that makes you feel like the main character. "
            "Your hair is your crown — tend it like royalty."
        ),
        "prompt": "What does taking care of my hair teach me about patience and devotion?",
        "icon": "✦",
    },
    {
        "title": "Sunday Reset Ritual",
        "subtitle": "Weekly Beauty Ceremony",
        "body": (
            "Exfoliate. Mask. Hydrate. Paint your nails if you wish. "
            "Lay out your favourite scent. Every Sunday is a soft reset — "
            "a chance to arrive at the new week feeling tended, polished, and utterly yourself."
        ),
        "prompt": "How do I want to feel when I step into Monday?",
        "icon": "◯",
    },
    {
        "title": "The Scent of You",
        "subtitle": "Perfume as Ritual",
        "body": (
            "Choose your scent with intention today. Spray it on your wrists, your neck, your collarbone. "
            "Scent is memory, mood, and magic. Wear something that makes you walk differently — "
            "a little taller, a little softer, a little more yours."
        ),
        "prompt": "If my life had a signature scent, what would it smell like and why?",
        "icon": "~",
    },
]

SLOW_LIVING_CARDS = [
    {
        "title": "The Unhurried Morning",
        "subtitle": "Slow Morning Ritual",
        "body": (
            "Wake ten minutes earlier than you think you need to. "
            "Do not reach for your phone. Instead: stretch gently, open a window, "
            "make your drink with care. Let the morning be soft before the world gets loud."
        ),
        "prompt": "What is one thing I can do more slowly this morning?",
        "icon": "☀",
    },
    {
        "title": "The Art of Doing Nothing",
        "subtitle": "Rest as Practice",
        "body": (
            "Schedule fifteen minutes today for nothing. Not scrolling. Not podcasts. "
            "Sit by a window. Watch light move across the floor. Let your mind wander "
            "without guilt. Stillness is not laziness — it is how we hear ourselves."
        ),
        "prompt": "What does my mind travel to when I give it freedom?",
        "icon": "◦",
    },
    {
        "title": "Candlelight Hours",
        "subtitle": "Evening Wind-Down Ritual",
        "body": (
            "One hour before bed, dim every light. Light a candle. "
            "Put your phone in another room. Let your nervous system believe "
            "the day is truly over. You have earned rest. Receive it."
        ),
        "prompt": "What is one thing I'm proud of from today, however small?",
        "icon": "♡",
    },
    {
        "title": "The Slow Cup",
        "subtitle": "Mindful Drinking Ritual",
        "body": (
            "Make your tea or coffee as if it matters — because it does. "
            "Use your favourite mug. Warm it first. Sit down before you drink. "
            "Hold the cup with both hands. One sip at a time. This is your ceremony."
        ),
        "prompt": "What intention do I set as I drink this cup?",
        "icon": "❁",
    },
    {
        "title": "The Weekly Flower",
        "subtitle": "Beauty in the Every Day",
        "body": (
            "Buy yourself flowers — or gather wildflowers, or a single stem from a garden. "
            "Place them where you will see them daily. Beauty is not an indulgence; "
            "it is a necessity for a soft life well-lived."
        ),
        "prompt": "What small beauty am I overlooking in my everyday surroundings?",
        "icon": "✿",
    },
    {
        "title": "The Linen Hour",
        "subtitle": "Slow Sunday Practice",
        "body": (
            "Change your bed linen today. Smooth it carefully. Add a drop of lavender "
            "to your pillowcase. Make your bed as if someone you love is about to sleep in it. "
            "That someone is you."
        ),
        "prompt": "How can I make my rest environment more sacred?",
        "icon": "◇",
    },
]

JOURNALING_CARDS = [
    {
        "title": "The Body Check-In",
        "subtitle": "Somatic Journaling Prompt",
        "body": "Close your eyes. Place one hand on your heart. Ask yourself gently:",
        "prompt": "Where am I holding tension right now? What is my body trying to tell me? What does it need that I haven't given it today?",
        "icon": "✦",
    },
    {
        "title": "Desire Mapping",
        "subtitle": "Deep Longing Prompt",
        "body": "Without editing, without logic — let yourself want freely:",
        "prompt": "What do I truly want my life to feel like? Not look like — feel like. What would I do, be, or have if I knew I couldn't fail?",
        "icon": "◯",
    },
    {
        "title": "The Permission Slip",
        "subtitle": "Self-Authorisation Prompt",
        "body": "Write yourself a permission slip today. Begin with: 'I give myself full permission to...'",
        "prompt": "What have you been waiting for someone else to allow you to do, feel, or be? Give yourself that permission now.",
        "icon": "~",
    },
    {
        "title": "Letters Never Sent",
        "subtitle": "Release Writing Prompt",
        "body": "Write a letter you will never send. Be completely honest:",
        "prompt": "To someone who hurt you. To a younger version of yourself. To the version of you that is coming. What needs to be said?",
        "icon": "❀",
    },
    {
        "title": "The Pleasure List",
        "subtitle": "Joy Mapping Prompt",
        "body": "We often map our pain. Today, map your pleasure:",
        "prompt": "List 20 things that bring you genuine, simple joy. Be specific. Include small things — the smell of rain, a particular song. What do these tell you about who you are?",
        "icon": "♡",
    },
    {
        "title": "Who Am I Becoming?",
        "subtitle": "Identity Journaling Prompt",
        "body": "Growth is not always visible. Look closer:",
        "prompt": "Who was I a year ago? What have I released? What have I grown into? What is one quality I am actively becoming? Write to your future self.",
        "icon": "✿",
    },
    {
        "title": "Shadow & Light",
        "subtitle": "Integration Journaling Prompt",
        "body": "We are whole creatures — light and shadow both:",
        "prompt": "What part of myself have I been hiding or ashamed of? What would it feel like to accept this part fully? What does it need from me?",
        "icon": "◦",
    },
]

WELLNESS_CARDS = [
    {
        "title": "Water is Medicine",
        "subtitle": "Hydration Ritual",
        "body": (
            "Fill a beautiful glass or carafe with water. Add cucumber, mint, or lemon if you like. "
            "Place it where you will see it all day. Your body is mostly water — "
            "tend it like the living, breathing miracle it is."
        ),
        "prompt": "How can I make the basics of self-care feel more luxurious today?",
        "icon": "◇",
    },
    {
        "title": "Move Like You Love Yourself",
        "subtitle": "Joyful Movement Reminder",
        "body": (
            "Forget what exercise is supposed to look like. "
            "What movement brings you joy? Dance in your kitchen. Walk slowly and look at everything. "
            "Stretch on the floor with your cat. Move your body as an act of love, not punishment."
        ),
        "prompt": "What kind of movement makes me feel alive and present?",
        "icon": "✦",
    },
    {
        "title": "The Nourishment Ritual",
        "subtitle": "Conscious Eating Practice",
        "body": (
            "Set the table, even if you're eating alone — especially if you're eating alone. "
            "Use the nice plate. Light a candle. Eat without screens. "
            "You deserve the full experience of being nourished."
        ),
        "prompt": "What does it mean to truly nourish myself — body, mind, and spirit?",
        "icon": "❁",
    },
    {
        "title": "Digital Sunset",
        "subtitle": "Tech Boundaries for Wellness",
        "body": (
            "Choose a time — 8pm, 9pm — and make it your digital sunset. "
            "After that hour, screens go dark. Pick up a book, journal, or simply be. "
            "Your nervous system needs silence to heal."
        ),
        "prompt": "What would I do with my evenings if screens didn't exist?",
        "icon": "◯",
    },
    {
        "title": "Breath as Anchor",
        "subtitle": "Breathwork Wellness Card",
        "body": (
            "Inhale for 4 counts. Hold for 4. Exhale for 6. Hold for 2. Repeat four times. "
            "This is your nervous system reset. You can do this anywhere — "
            "in a meeting, in a queue, in a moment of panic. Your breath is always yours."
        ),
        "prompt": "When do I most need to remember to breathe? What triggers me to hold my breath?",
        "icon": "~",
    },
    {
        "title": "Sleep as Sacred",
        "subtitle": "Sleep Ritual Reminder",
        "body": (
            "Sleep is not laziness — it is when your body repairs, your mind integrates, "
            "and your spirit restores. Protect it fiercely. Create a ritual around it. "
            "The most radical thing you can do for your health is go to sleep."
        ),
        "prompt": "What one change would most improve the quality of my sleep?",
        "icon": "♡",
    },
]

GRATITUDE_CARDS = [
    {
        "title": "The Micro-Gratitude List",
        "subtitle": "Gratitude Practice",
        "body": "Gratitude lives in the smallest things. Look closer:",
        "prompt": "List 10 tiny things you are grateful for right now. Include textures, temperatures, sounds. The weight of your duvet. The smell of morning. The fact that your heart is beating.",
        "icon": "✿",
    },
    {
        "title": "Gratitude for Your Body",
        "subtitle": "Embodied Gratitude Practice",
        "body": "Your body carries you through everything. Today, thank it:",
        "prompt": "Write a love letter to one part of your body you usually criticise. What has it done for you? What does it allow you to experience? What would you say to it if it could hear you?",
        "icon": "❀",
    },
    {
        "title": "Who Made Me?",
        "subtitle": "People Gratitude Practice",
        "body": "We are shaped by those who loved us well — and even those who didn't:",
        "prompt": "Who are three people who believed in you when you didn't believe in yourself? What specific thing did they do or say? Have you told them?",
        "icon": "◦",
    },
    {
        "title": "The Hardship Thank You",
        "subtitle": "Growth Gratitude Practice",
        "body": "Some gifts arrive disguised as loss or pain:",
        "prompt": "What is one difficulty from your past that you are now — even reluctantly — grateful for? What did it teach you? Who did it make you become?",
        "icon": "◇",
    },
    {
        "title": "Present Moment Gratitude",
        "subtitle": "Mindful Gratitude Practice",
        "body": "Right now, in this exact moment:",
        "prompt": "Look up. What do you see? What can you feel — the chair beneath you, the temperature of the air? Name five things that exist around you right now that are beautiful, useful, or kind.",
        "icon": "✦",
    },
]

ROMANTICISE_CARDS = [
    {
        "title": "Main Character Morning",
        "subtitle": "Romanticise Your Life",
        "body": (
            "Today you are the lead in your own film. Your morning routine is a montage. "
            "The light hitting your kitchen is cinematic. Your coffee ritual is a scene. "
            "Narrate your morning internally in third person — she woke slowly, stretched like a cat..."
        ),
        "prompt": "If your life were a film, what genre would it be? What would the soundtrack sound like?",
        "icon": "♡",
    },
    {
        "title": "The Flaneur Walk",
        "subtitle": "Wandering as Practice",
        "body": (
            "Take a walk with no destination and no phone in your hand. "
            "Wander like you have all the time in the world. Notice architecture, light, strangers' shoes. "
            "A flaneur is a city wanderer who finds magic in the mundane — be one today."
        ),
        "prompt": "What did I notice on my walk that I've been walking past without seeing?",
        "icon": "◯",
    },
    {
        "title": "Cook Like You Love Yourself",
        "subtitle": "Romanticise Nourishment",
        "body": (
            "Put on music. Pour yourself something nice. Chop vegetables slowly. "
            "Let cooking be sensory — the sizzle, the steam, the colour of things. "
            "Make something simple and beautiful. Eat by candlelight."
        ),
        "prompt": "What recipe feels like love to me? Who taught me to make it?",
        "icon": "✿",
    },
    {
        "title": "The Reading Nook",
        "subtitle": "Create Your Sanctuary",
        "body": (
            "Choose a corner. Add cushions. Drape a throw. Position a lamp. "
            "Make it the most beautiful seat in your home. "
            "Spend one hour there today — reading, thinking, existing. You deserve a sanctuary."
        ),
        "prompt": "What does my ideal sanctuary look and feel like? What small step can I take toward creating it?",
        "icon": "❁",
    },
    {
        "title": "Dress for the Life You Want",
        "subtitle": "Embody Your Vision",
        "body": (
            "Today, dress as if you are already living your dream life. "
            "Not for anyone else — for the version of you who has arrived. "
            "Wear the perfume. Put on the earrings. You are not waiting. You are here."
        ),
        "prompt": "What would the most expressed, fully-arrived version of me wear today?",
        "icon": "◇",
    },
    {
        "title": "The Long Table",
        "subtitle": "Romanticise Connection",
        "body": (
            "Invite someone for a meal. Lay the table beautifully. "
            "Cook something with your hands. "
            "Connection is the softest luxury — the sharing of food, space, and story."
        ),
        "prompt": "Who in my life deserves more of my unhurried, undivided presence?",
        "icon": "~",
    },
]

AFFIRMATION_CARDS = [
    {
        "title": "You Are Allowed",
        "subtitle": "Permission Affirmation",
        "body": "Read this slowly. Let each line land:",
        "prompt": "I am allowed to take up space.\nI am allowed to change my mind.\nI am allowed to want more.\nI am allowed to rest without earning it.\nI am allowed to be a work in progress and still be worthy of love.",
        "icon": "✿",
    },
    {
        "title": "Soft Is Not Weak",
        "subtitle": "Strength Affirmation",
        "body": "Speak this to yourself as many times as it takes to believe it:",
        "prompt": "My gentleness is not a flaw — it is a gift.\nMy sensitivity allows me to feel deeply.\nMy softness is a form of courage.\nI am strong in the ways that matter most.\nI do not need to harden to survive.",
        "icon": "❀",
    },
    {
        "title": "The Body is Sacred",
        "subtitle": "Body Acceptance Affirmation",
        "body": "Place your hands over your heart and breathe:",
        "prompt": "My body is my home and I choose to love it.\nIt carries me through every experience.\nIt deserves kindness, not criticism.\nI release the need for my body to look a certain way to deserve care.\nI am more than my appearance.",
        "icon": "◦",
    },
    {
        "title": "I Am Becoming",
        "subtitle": "Growth Affirmation",
        "body": "Growth is not always visible. Trust the process:",
        "prompt": "I am exactly where I need to be.\nI trust the pace of my own becoming.\nI don't need to have it all together to be worthy.\nEvery small step is progress.\nI am proud of how far I've come.",
        "icon": "✦",
    },
    {
        "title": "Abundance Is My Birthright",
        "subtitle": "Abundance Affirmation",
        "body": "Say this with your spine tall and your shoulders back:",
        "prompt": "I deserve good things.\nJoy is available to me.\nLove flows toward me easily.\nI am open to receiving.\nAbundance is not selfish — it is my natural state.",
        "icon": "◇",
    },
    {
        "title": "Rest Is Productive",
        "subtitle": "Rest Affirmation",
        "body": "For the one who is always doing, always giving:",
        "prompt": "I do not need to earn my rest.\nBeing is enough — not just doing.\nSlowing down is an act of wisdom.\nMy worth is not tied to my output.\nI give myself full permission to stop.",
        "icon": "♡",
    },
]

SEASONAL_RITUAL_CARDS = [
    {
        "title": "Spring Renewal",
        "subtitle": "Seasonal Ritual · Spring",
        "body": (
            "Open every window. Clear your space. "
            "Write what you are releasing from the last season and burn or bury the paper. "
            "Plant something — a seed, a bulb, an intention. "
            "Spring does not ask permission to bloom. Neither do you."
        ),
        "prompt": "What am I ready to let bloom in this season of my life?",
        "icon": "✿",
    },
    {
        "title": "Summer Abundance",
        "subtitle": "Seasonal Ritual · Summer",
        "body": (
            "Step outside barefoot. Feel the ground. Eat something ripe and in season. "
            "Spend one hour completely unhurried in natural light. "
            "Summer asks you to be fully present — warm, open, generous with your energy."
        ),
        "prompt": "What does full, abundant aliveness feel like in my body right now?",
        "icon": "☀",
    },
    {
        "title": "Autumn Harvest",
        "subtitle": "Seasonal Ritual · Autumn",
        "body": (
            "Audit your life like the trees audit their leaves. "
            "What can you let fall? Make a warm drink. Light a candle. "
            "Write a list of everything you have gathered and grown this year. "
            "Autumn is the season of beautiful, graceful release."
        ),
        "prompt": "What have I harvested this year? What am I ready to release?",
        "icon": "❁",
    },
    {
        "title": "Winter Nesting",
        "subtitle": "Seasonal Ritual · Winter",
        "body": (
            "Honour the dark. Create warmth and softness in your space. "
            "This is the season for going inward — for dreaming, resting, and replenishing. "
            "Nature doesn't apologise for wintering. You don't have to either."
        ),
        "prompt": "What does my soul need in this quieter, darker season?",
        "icon": "◦",
    },
]

BOUNDARY_REST_CARDS = [
    {
        "title": "No Is a Complete Sentence",
        "subtitle": "Boundaries Ritual Card",
        "body": (
            "Practice saying no to something small today — without an explanation. "
            "'No' is a full sentence. You do not owe anyone your energy, time, or presence "
            "simply because they desire it. A soft no now prevents a resentful yes later."
        ),
        "prompt": "What have I been saying yes to that my soul is saying no to?",
        "icon": "◯",
    },
    {
        "title": "The Depletion Check",
        "subtitle": "Energy Audit Card",
        "body": "Sit quietly and ask yourself honestly:",
        "prompt": "Who in my life fills my cup? Who drains it? What activities restore me? What depletes me? Am I giving more energy than I am receiving? What one adjustment could I make this week?",
        "icon": "~",
    },
    {
        "title": "Rest Without Guilt",
        "subtitle": "Sacred Rest Card",
        "body": (
            "Take a rest today that you do not justify, earn, or apologise for. "
            "Lie down in the middle of the day if you can. Read without purpose. "
            "Stare at the ceiling. The world will not end. You will feel better. "
            "Rest is not a reward — it is a right."
        ),
        "prompt": "What story am I telling myself about why I don't deserve to rest?",
        "icon": "♡",
    },
    {
        "title": "Protect Your Peace",
        "subtitle": "Peace Boundaries Card",
        "body": (
            "Your peace is a garden. It needs tending and protecting. "
            "Not everyone deserves access to your inner world. "
            "You can love people and still limit how much of yourself you share with them. "
            "Discernment is not coldness — it is wisdom."
        ),
        "prompt": "What or who is consistently disturbing my peace, and what is one boundary I could set?",
        "icon": "❀",
    },
]

VISION_DREAMING_CARDS = [
    {
        "title": "Dream Without Limits",
        "subtitle": "Vision & Manifestation Card",
        "body": "For the next five minutes, let yourself want without editing:",
        "prompt": "If money, time, and other people's opinions were no obstacle — what would your life look and feel like in five years? Describe your mornings, your home, your work, your relationships, your body, your spirit.",
        "icon": "✦",
    },
    {
        "title": "The Vision Board Letter",
        "subtitle": "Manifestation Writing Card",
        "body": "Write a letter dated one year from today. Begin: 'It has been the most beautiful year...'",
        "prompt": "Describe, in vivid present-tense detail, everything you have called in. Write it as if it has already happened. Feel the feelings as you write.",
        "icon": "◇",
    },
    {
        "title": "Ancestor Dreaming",
        "subtitle": "Lineage & Legacy Card",
        "body": "You carry generations of women before you:",
        "prompt": "What dreams did the women before you not get to live? What freedoms are you living that they could only imagine? How can you honour their sacrifices by living fully, boldly, and softly?",
        "icon": "✿",
    },
    {
        "title": "What Would She Do?",
        "subtitle": "Future Self Card",
        "body": "Connect with the version of you who has already arrived:",
        "prompt": "Close your eyes. See her clearly — the fully healed, fully expressed, fully abundant version of you. What does she look like? How does she carry herself? What decision would she make in your current situation? What would she tell you?",
        "icon": "❁",
    },
]


# ═══════════════════════════════════════════════════════════════════
#  RESOLVE CONFIG
# ═══════════════════════════════════════════════════════════════════

if PlannerConfig.THEME_NAME == "custom":
    theme = PlannerConfig.CUSTOM_THEME
else:
    theme = PlannerConfig.THEMES.get(
        PlannerConfig.THEME_NAME,
        PlannerConfig.THEMES["blush_gold"]
    )

C_BG       = HexColor(theme["C_BG"])
C_BG2      = HexColor(theme["C_BG2"])
C_ACCENT   = HexColor(theme["C_ACCENT"])
C_ACCENT2  = HexColor(theme["C_ACCENT2"])
C_GOLD     = HexColor(theme["C_GOLD"])
C_INK      = HexColor(theme["C_INK"])
C_SECONDARY= HexColor(theme["C_SECONDARY"])
C_MUTED    = HexColor(theme["C_MUTED"])
C_BORDER   = HexColor(theme["C_BORDER"])
C_PANEL    = HexColor(theme["C_PANEL"])
C_WHITE    = HexColor(theme["C_WHITE"])
C_DARK     = HexColor(theme["C_DARK"])
C_FLORAL1  = HexColor(theme["C_FLORAL1"])
C_FLORAL2  = HexColor(theme["C_FLORAL2"])
C_FLORAL3  = HexColor(theme["C_FLORAL3"])

CW = PlannerConfig.CARD_WIDTH
CH = PlannerConfig.CARD_HEIGHT

FONT_HEADING = PlannerConfig.FONT_HEADING
FONT_TITLE   = PlannerConfig.FONT_TITLE
FONT_BODY    = PlannerConfig.FONT_BODY
FONT_CAPTION = PlannerConfig.FONT_CAPTION
FONT_ACCENT  = PlannerConfig.FONT_ACCENT


# ═══════════════════════════════════════════════════════════════════
#  DRAWING HELPERS
# ═══════════════════════════════════════════════════════════════════

def hc(hex_str, alpha=1.0):
    c = HexColor(hex_str)
    if alpha < 1.0:
        return Color(c.red, c.green, c.blue, alpha)
    return c

def col_alpha(c_obj, alpha):
    return Color(c_obj.red, c_obj.green, c_obj.blue, alpha)


def draw_text_wrapped(c, text, x, y, max_width, font, size, color,
                       line_height=None, align="left"):
    """Draw wrapped text, returns y position after last line."""
    if line_height is None:
        line_height = size * 1.55
    c.setFillColor(color)
    c.setFont(font, size)
    lines = simpleSplit(text, font, size, max_width)
    for line in lines:
        if align == "center":
            c.drawCentredString(x + max_width / 2, y, line)
        elif align == "right":
            c.drawRightString(x + max_width, y, line)
        else:
            c.drawString(x, y, line)
        y -= line_height
    return y


def draw_ornament(c, x, y, size=18, color=None):
    """Draw a small botanical-style corner ornament."""
    if color is None:
        color = col_alpha(C_GOLD, 0.55)
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(0.8)
    # Petal cluster
    for angle in [0, 60, 120, 180, 240, 300]:
        rad = math.radians(angle)
        px = x + math.cos(rad) * size * 0.55
        py = y + math.sin(rad) * size * 0.55
        c.circle(px, py, size * 0.22, fill=1, stroke=0)
    c.circle(x, y, size * 0.25, fill=1, stroke=0)


def draw_botanical_sprig(c, x, y, scale=1.0, color=None, angle_deg=0):
    """Draw a minimal botanical leaf sprig."""
    if color is None:
        color = col_alpha(C_FLORAL3, 0.5)
    c.saveState()
    c.translate(x, y)
    c.rotate(angle_deg)
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(0.7 * scale)
    # Stem
    c.line(0, 0, 0, 40 * scale)
    # Leaves
    leaf_positions = [(0, 10, -30), (0, 20, 30), (0, 30, -25), (0, 38, 0)]
    for lx, ly, la in leaf_positions:
        c.saveState()
        c.translate(lx, ly * scale)
        c.rotate(la)
        c.ellipse(-3 * scale, 0, 3 * scale, 12 * scale, fill=1, stroke=0)
        c.restoreState()
    c.restoreState()


def draw_petal_shape(c, cx, cy, rx, ry, color, alpha=0.35, rotation=0):
    """Draw a soft elliptical petal at given position."""
    c.saveState()
    c.translate(cx, cy)
    c.rotate(rotation)
    c.setFillColor(Color(color.red, color.green, color.blue, alpha))
    c.ellipse(-rx, -ry, rx, ry, fill=1, stroke=0)
    c.restoreState()


def draw_thin_rule(c, x, y, w, color=None, alpha=0.4):
    if color is None:
        color = C_GOLD
    c.setStrokeColor(Color(color.red, color.green, color.blue, alpha))
    c.setLineWidth(0.75)
    c.line(x, y, x + w, y)


def draw_double_rule(c, x, y, w, color=None, alpha=0.35):
    if color is None:
        color = C_GOLD
    draw_thin_rule(c, x, y, w, color, alpha)
    draw_thin_rule(c, x, y - 4, w, color, alpha * 0.6)


def draw_section_badge(c, label, cx, y, color=None, text_color=None):
    """Draw a small rounded pill category badge."""
    if color is None:
        color = C_ACCENT
    if text_color is None:
        text_color = C_WHITE
    font = FONT_CAPTION
    font_size = 9
    c.setFont(font, font_size)
    text_w = c.stringWidth(label, font, font_size)
    pw = text_w + 22
    ph = 20
    px = cx - pw / 2
    c.setFillColor(Color(color.red, color.green, color.blue, 0.88))
    c.roundRect(px, y, pw, ph, ph / 2, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.drawCentredString(cx, y + 5.5, label)


def draw_card_number(c, number, total, x, y, color=None):
    if color is None:
        color = col_alpha(C_MUTED, 0.7)
    c.setFillColor(color)
    c.setFont(FONT_CAPTION, 9)
    c.drawString(x, y, f"{number:02d}  /  {total:02d}")


# ═══════════════════════════════════════════════════════════════════
#  BACKGROUND STYLES
# ═══════════════════════════════════════════════════════════════════

def draw_card_bg_petals(c, alt=False):
    """Scattered organic petal shapes background."""
    rng = random.Random(99)
    bg = C_BG2 if alt else C_BG
    c.setFillColor(bg)
    c.rect(0, 0, CW, CH, fill=1, stroke=0)

    petal_configs = [
        # cx_frac, cy_frac, rx, ry, rot, color, alpha
        (0.05, 0.92, 55, 38, 25,  C_FLORAL1, 0.22),
        (0.12, 0.88, 40, 26, -15, C_FLORAL2, 0.18),
        (0.88, 0.92, 60, 42, -30, C_FLORAL1, 0.20),
        (0.95, 0.85, 38, 24,  40, C_FLORAL3, 0.22),
        (0.08, 0.08, 50, 34, -20, C_FLORAL3, 0.18),
        (0.15, 0.12, 32, 20,  35, C_FLORAL2, 0.15),
        (0.85, 0.10, 55, 38,  20, C_FLORAL1, 0.18),
        (0.92, 0.06, 35, 22, -35, C_FLORAL2, 0.16),
        (0.50, 0.96, 45, 28,   0, C_FLORAL3, 0.14),
        (0.50, 0.04, 40, 25,  10, C_FLORAL1, 0.12),
    ]
    for xf, yf, rx, ry, rot, col, alpha in petal_configs:
        draw_petal_shape(c, CW * xf, CH * yf, rx, ry, col, alpha, rot)


def draw_card_bg_arches(c, alt=False):
    """Layered arch / frame background."""
    bg = C_BG2 if alt else C_BG
    c.setFillColor(bg)
    c.rect(0, 0, CW, CH, fill=1, stroke=0)
    # Outer arch (top semi-circle suggestion)
    for i, (aw, alpha) in enumerate([(CW * 0.9, 0.08), (CW * 0.7, 0.06)]):
        c.setFillColor(Color(C_ACCENT.red, C_ACCENT.green, C_ACCENT.blue, alpha))
        ah = aw * 0.55
        ax = (CW - aw) / 2
        ay = CH - ah - 40
        c.ellipse(ax, ay, ax + aw, ay + ah * 2, fill=1, stroke=0)


def draw_card_bg_minimal(c, alt=False):
    """Minimal clean background with subtle texture lines."""
    bg = C_BG2 if alt else C_BG
    c.setFillColor(bg)
    c.rect(0, 0, CW, CH, fill=1, stroke=0)


CARD_BG_STYLES = {
    "petals":  draw_card_bg_petals,
    "arches":  draw_card_bg_arches,
    "minimal": draw_card_bg_minimal,
}


# ═══════════════════════════════════════════════════════════════════
#  CARD BORDER & FRAME
# ═══════════════════════════════════════════════════════════════════

def draw_card_frame(c):
    """Draw the decorative outer border frame."""
    margin = 22
    # Outer border
    c.setStrokeColor(col_alpha(C_BORDER, 0.9))
    c.setLineWidth(1.5)
    c.roundRect(margin, margin, CW - margin * 2, CH - margin * 2, 18, fill=0, stroke=1)
    # Inner hairline
    c.setStrokeColor(col_alpha(C_GOLD, 0.28))
    c.setLineWidth(0.5)
    c.roundRect(margin + 8, margin + 8, CW - (margin + 8) * 2, CH - (margin + 8) * 2,
                14, fill=0, stroke=1)

    # Corner ornaments
    if PlannerConfig.SHOW_CORNER_ORNAMENTS:
        corners = [
            (margin + 18, CH - margin - 18),
            (CW - margin - 18, CH - margin - 18),
            (margin + 18, margin + 18),
            (CW - margin - 18, margin + 18),
        ]
        for cx2, cy2 in corners:
            draw_ornament(c, cx2, cy2, size=14)


# ═══════════════════════════════════════════════════════════════════
#  MAIN CARD RENDERER
# ═══════════════════════════════════════════════════════════════════

def draw_card(c, card_data, card_number, total_cards, section_label,
              alt_bg=False, bookmark=None):
    """
    Render a single self-care ritual card as a full page.
    card_data keys: title, subtitle, body, prompt, icon
    """
    # Background
    bg_fn = CARD_BG_STYLES.get(PlannerConfig.COVER_STYLE, draw_card_bg_petals)
    bg_fn(c, alt=alt_bg)

    # Frame
    draw_card_frame(c)

    if bookmark:
        c.bookmarkPage(bookmark)

    MARGIN = 68
    content_w = CW - MARGIN * 2
    cx = CW / 2

    # ── Top area ──────────────────────────────────────────────
    top_y = CH - MARGIN - 20

    # Section badge
    if PlannerConfig.SHOW_SECTION_BADGE:
        draw_section_badge(c, section_label.upper(), cx, top_y)
        top_y -= 34

    # Large decorative icon
    icon = card_data.get("icon", "✦")
    c.setFillColor(col_alpha(C_ACCENT, 0.25))
    c.setFont(FONT_TITLE, 36)
    icon_w = c.stringWidth(icon, FONT_TITLE, 36)
    c.setFillColor(col_alpha(C_ACCENT, 0.55))
    c.drawCentredString(cx, top_y - 6, icon)
    top_y -= 52

    # Subtitle / category
    c.setFillColor(col_alpha(C_SECONDARY, 0.85))
    c.setFont(FONT_HEADING, 13)
    subtitle = card_data.get("subtitle", "")
    c.drawCentredString(cx, top_y, subtitle)
    top_y -= 22

    # Title
    c.setFillColor(C_INK)
    c.setFont(FONT_TITLE, 30)
    title = card_data.get("title", "")
    title_lines = simpleSplit(title, FONT_TITLE, 30, content_w)
    for tl in title_lines:
        c.drawCentredString(cx, top_y, tl)
        top_y -= 38
    top_y -= 4

    # Gold double rule
    if PlannerConfig.SHOW_DIVIDERS:
        rule_w = min(content_w * 0.55, 300)
        draw_double_rule(c, cx - rule_w / 2, top_y, rule_w)
        top_y -= 22

    # ── Botanical sprigs ──────────────────────────────────────
    draw_botanical_sprig(c, MARGIN + 10, top_y - 80, scale=0.9,
                         color=col_alpha(C_FLORAL3, 0.45), angle_deg=15)
    draw_botanical_sprig(c, CW - MARGIN - 10, top_y - 80, scale=0.9,
                         color=col_alpha(C_FLORAL3, 0.45), angle_deg=-15)

    # ── Body text ─────────────────────────────────────────────
    body = card_data.get("body", "")
    if body:
        body_y = top_y - 8
        c.setFillColor(C_INK)
        body_y = draw_text_wrapped(
            c, body, MARGIN, body_y, content_w,
            FONT_BODY, 15, C_INK, line_height=24, align="center"
        )
        top_y = body_y - 18
    else:
        top_y -= 10

    # ── Prompt panel ──────────────────────────────────────────
    prompt = card_data.get("prompt", "")
    if prompt:
        panel_pad = 24
        panel_inner_w = content_w - panel_pad * 2

        # Estimate prompt panel height
        c.setFont(FONT_ACCENT, 14)
        prompt_lines = simpleSplit(prompt, FONT_ACCENT, 14, panel_inner_w)
        panel_h = len(prompt_lines) * 22 + panel_pad * 2 + 20

        # Anchor panel from top_y downward
        panel_y = top_y - panel_h
        panel_x = MARGIN

        # Panel background
        c.setFillColor(col_alpha(C_ACCENT, 0.06))
        c.setStrokeColor(col_alpha(C_ACCENT2, 0.55))
        c.setLineWidth(1)
        c.roundRect(panel_x, panel_y, content_w, panel_h, 12, fill=1, stroke=1)

        # Gold left accent bar
        c.setFillColor(col_alpha(C_GOLD, 0.65))
        c.roundRect(panel_x + 1, panel_y + 10, 3, panel_h - 20, 2, fill=1, stroke=0)

        # Prompt label
        label_y = panel_y + panel_h - panel_pad - 4
        c.setFillColor(col_alpha(C_ACCENT, 0.75))
        c.setFont(FONT_CAPTION, 10)
        c.drawString(panel_x + panel_pad + 8, label_y, "✦  REFLECTION PROMPT")
        label_y -= 18

        # Prompt text
        draw_text_wrapped(
            c, prompt, panel_x + panel_pad + 8, label_y,
            panel_inner_w - 8, FONT_ACCENT, 14,
            C_INK, line_height=22, align="left"
        )
        bottom_area_y = panel_y - 16
    else:
        bottom_area_y = top_y - 20

    # ── Bottom: Card number + planner name ───────────────────
    if PlannerConfig.SHOW_CARD_NUMBER:
        draw_card_number(c, card_number, total_cards,
                         MARGIN, MARGIN + 28, col_alpha(C_MUTED, 0.65))

    c.setFillColor(col_alpha(C_MUTED, 0.6))
    c.setFont(FONT_CAPTION, 9)
    c.drawCentredString(cx, MARGIN + 28, PlannerConfig.PLANNER_TITLE.upper()
                        + "  ·  " + PlannerConfig.PLANNER_SUBTITLE.upper())

    # Bottom gold rule
    if PlannerConfig.SHOW_DIVIDERS:
        draw_thin_rule(c, MARGIN, MARGIN + 46, content_w, C_GOLD, 0.3)


# ═══════════════════════════════════════════════════════════════════
#  COVER PAGE
# ═══════════════════════════════════════════════════════════════════

def draw_cover(c):
    c.bookmarkPage("Cover")

    # Dark rich background
    c.setFillColor(C_DARK)
    c.rect(0, 0, CW, CH, fill=1, stroke=0)

    # Layered petal blooms — decorative background
    petal_defs = [
        # cx, cy, rx, ry, rot, color hex, alpha
        (CW * 0.12, CH * 0.85, 90, 62,  20, theme["C_FLORAL1"], 0.28),
        (CW * 0.05, CH * 0.90, 60, 40, -10, theme["C_FLORAL2"], 0.22),
        (CW * 0.88, CH * 0.82, 85, 58, -25, theme["C_FLORAL1"], 0.25),
        (CW * 0.95, CH * 0.88, 55, 36,  35, theme["C_FLORAL3"], 0.20),
        (CW * 0.10, CH * 0.15, 75, 50,  15, theme["C_FLORAL3"], 0.22),
        (CW * 0.03, CH * 0.10, 50, 32, -30, theme["C_FLORAL2"], 0.18),
        (CW * 0.90, CH * 0.12, 80, 55,  -20, theme["C_FLORAL1"],0.24),
        (CW * 0.97, CH * 0.18, 48, 30,  40, theme["C_FLORAL2"], 0.18),
        (CW * 0.50, CH * 0.98, 70, 45,   0, theme["C_FLORAL3"], 0.16),
        (CW * 0.50, CH * 0.02, 65, 42,   5, theme["C_FLORAL1"], 0.14),
        # Larger atmospheric blobs
        (CW * 0.15, CH * 0.50, 130, 90,  30, theme["C_ACCENT2"], 0.10),
        (CW * 0.85, CH * 0.50, 120, 85, -30, theme["C_ACCENT2"], 0.10),
    ]
    for xc, yc, rx, ry, rot, chex, alpha in petal_defs:
        pc = HexColor(chex)
        c.saveState()
        c.translate(xc, yc)
        c.rotate(rot)
        c.setFillColor(Color(pc.red, pc.green, pc.blue, alpha))
        c.ellipse(-rx, -ry, rx, ry, fill=1, stroke=0)
        c.restoreState()

    # Floating botanical sprigs
    sprig_positions = [
        (CW * 0.08, CH * 0.70, 1.4, 20),
        (CW * 0.92, CH * 0.68, 1.4, -20),
        (CW * 0.06, CH * 0.30, 1.2, 15),
        (CW * 0.94, CH * 0.28, 1.2, -15),
    ]
    for sx, sy, sc, sa in sprig_positions:
        draw_botanical_sprig(c, sx, sy, scale=sc,
                             color=col_alpha(C_FLORAL3, 0.35), angle_deg=sa)

    # Double border frame
    c.setStrokeColor(col_alpha(C_GOLD, 0.40))
    c.setLineWidth(1.5)
    c.roundRect(24, 24, CW - 48, CH - 48, 20, fill=0, stroke=1)
    c.setStrokeColor(col_alpha(C_GOLD, 0.20))
    c.setLineWidth(0.6)
    c.roundRect(34, 34, CW - 68, CH - 68, 16, fill=0, stroke=1)

    # Corner ornaments
    corners = [
        (44, CH - 44), (CW - 44, CH - 44),
        (44, 44),       (CW - 44, 44),
    ]
    for ox, oy in corners:
        draw_ornament(c, ox, oy, size=16, color=col_alpha(C_GOLD, 0.50))

    cx = CW / 2

    # Edition label
    c.setFillColor(col_alpha(C_FLORAL2, 0.55))
    c.setFont(FONT_CAPTION, 10)
    c.drawCentredString(cx, CH - 82, PlannerConfig.PLANNER_EDITION.upper())

    # Thin rule above title
    draw_thin_rule(c, cx - 160, CH - 98, 320, C_GOLD, 0.35)

    # Main title
    c.setFillColor(C_WHITE)
    c.setFont(FONT_TITLE, 72)
    title_lines = PlannerConfig.PLANNER_TITLE.upper().split()
    ty = CH / 2 + 80
    for tl in title_lines:
        c.drawCentredString(cx, ty, tl)
        ty -= 82

    # Subtitle
    c.setFillColor(col_alpha(HexColor(theme["C_ACCENT2"]), 0.90))
    c.setFont(FONT_HEADING, 20)
    c.drawCentredString(cx, CH / 2 - 25, PlannerConfig.PLANNER_SUBTITLE)

    # Thin rule below subtitle
    draw_double_rule(c, cx - 140, CH / 2 - 48, 280, C_GOLD, 0.35)

    # Tagline
    c.setFillColor(col_alpha(C_WHITE, 0.50))
    c.setFont(FONT_CAPTION, 12)
    c.drawCentredString(cx, CH / 2 - 76, PlannerConfig.PLANNER_TAGLINE)

    # Feature pill row
    features = PlannerConfig.COVER_FEATURE_PILLS if hasattr(PlannerConfig, "COVER_FEATURE_PILLS") else []
    if features:
        pill_font_size = 10
        pill_pad_x = 14
        pill_pad_y = 7
        pill_gap = 10
        pill_h = pill_font_size + pill_pad_y * 2
        c.setFont(FONT_CAPTION, pill_font_size)
        pill_widths = [c.stringWidth(f, FONT_CAPTION, pill_font_size) + pill_pad_x * 2
                       for f in features]
        total_row = sum(pill_widths) + pill_gap * (len(features) - 1)
        pill_sx = cx - total_row / 2
        pill_y = CH / 2 - 130
        for pw, feat in zip(pill_widths, features):
            c.setFillColor(col_alpha(HexColor(theme["C_ACCENT"]), 0.22))
            c.roundRect(pill_sx, pill_y, pw, pill_h, pill_h / 2, fill=1, stroke=0)
            c.setFillColor(col_alpha(C_WHITE, 0.75))
            c.drawCentredString(pill_sx + pw / 2, pill_y + pill_pad_y - 1, feat)
            pill_sx += pw + pill_gap

    # Card count badge
    total = _count_total_cards()
    badge_text = f"{total} RITUAL CARDS INSIDE"
    c.setFont(FONT_CAPTION, 10)
    bw = c.stringWidth(badge_text, FONT_CAPTION, 10) + 28
    bh = 26
    bx = cx - bw / 2
    by = 100
    c.setFillColor(col_alpha(HexColor(theme["C_GOLD"]), 0.25))
    c.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    c.setStrokeColor(col_alpha(HexColor(theme["C_GOLD"]), 0.50))
    c.setLineWidth(0.75)
    c.roundRect(bx, by, bw, bh, bh / 2, fill=0, stroke=1)
    c.setFillColor(col_alpha(HexColor(theme["C_FLORAL2"]), 0.80))
    c.drawCentredString(cx, by + 8, badge_text)

    # Year
    c.setFillColor(col_alpha(C_WHITE, 0.25))
    c.setFont(FONT_CAPTION, 10)
    c.drawCentredString(cx, 68, str(PlannerConfig.PLANNER_YEAR))


# ═══════════════════════════════════════════════════════════════════
#  SECTION DIVIDER PAGE
# ═══════════════════════════════════════════════════════════════════

def draw_section_divider(c, section_title, section_subtitle, section_icon,
                          card_count, bookmark_id=None):
    """Beautiful full-bleed section title card."""
    # Soft background
    bg_fn = CARD_BG_STYLES.get(PlannerConfig.COVER_STYLE, draw_card_bg_petals)
    bg_fn(c, alt=True)

    if bookmark_id:
        c.bookmarkPage(bookmark_id)

    # Accent wash on upper half
    c.setFillColor(col_alpha(C_ACCENT, 0.06))
    c.rect(0, CH * 0.45, CW, CH * 0.55, fill=1, stroke=0)

    draw_card_frame(c)

    cx = CW / 2

    # Large icon
    c.setFont(FONT_TITLE, 52)
    c.setFillColor(col_alpha(C_ACCENT, 0.35))
    c.drawCentredString(cx, CH * 0.60, section_icon)

    # Section label
    c.setFont(FONT_CAPTION, 11)
    c.setFillColor(col_alpha(C_ACCENT, 0.75))
    c.drawCentredString(cx, CH * 0.55, "— SECTION —")

    # Section title
    c.setFont(FONT_TITLE, 42)
    c.setFillColor(C_INK)
    title_lines = simpleSplit(section_title, FONT_TITLE, 42, CW - 120)
    ty = CH * 0.50
    for tl in title_lines:
        c.drawCentredString(cx, ty, tl)
        ty -= 52

    # Subtitle
    c.setFont(FONT_HEADING, 16)
    c.setFillColor(C_SECONDARY)
    c.drawCentredString(cx, ty - 8, section_subtitle)

    draw_double_rule(c, cx - 120, ty - 28, 240, C_GOLD, 0.4)

    # Card count
    c.setFont(FONT_CAPTION, 10)
    c.setFillColor(col_alpha(C_MUTED, 0.8))
    c.drawCentredString(cx, ty - 52, f"{card_count} cards in this section")

    # Bottom ornament cluster
    draw_ornament(c, cx, CH * 0.15, size=20, color=col_alpha(C_GOLD, 0.35))
    draw_ornament(c, cx - 50, CH * 0.12, size=12, color=col_alpha(C_FLORAL1, 0.35))
    draw_ornament(c, cx + 50, CH * 0.12, size=12, color=col_alpha(C_FLORAL2, 0.35))


# ═══════════════════════════════════════════════════════════════════
#  INDEX / TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════

def draw_index(c, sections):
    c.bookmarkPage("Index")
    bg_fn = CARD_BG_STYLES.get(PlannerConfig.COVER_STYLE, draw_card_bg_petals)
    bg_fn(c, alt=False)
    draw_card_frame(c)

    cx = CW / 2
    MARGIN = 68

    # Title
    c.setFont(FONT_TITLE, 32)
    c.setFillColor(C_INK)
    c.drawCentredString(cx, CH - MARGIN - 20, "Contents")
    draw_double_rule(c, cx - 130, CH - MARGIN - 42, 260, C_GOLD, 0.4)

    c.setFont(FONT_CAPTION, 10)
    c.setFillColor(col_alpha(C_SECONDARY, 0.7))
    c.drawCentredString(cx, CH - MARGIN - 62,
                        f"{PlannerConfig.PLANNER_TITLE}  ·  {PlannerConfig.PLANNER_SUBTITLE}")

    # Section list
    item_y = CH - MARGIN - 110
    for i, (bm_id, label, icon, count, start_card) in enumerate(sections):
        # Alternating row tint
        if i % 2 == 0:
            c.setFillColor(col_alpha(C_ACCENT, 0.04))
            c.roundRect(MARGIN, item_y - 8, CW - MARGIN * 2, 38, 6, fill=1, stroke=0)

        # Icon
        c.setFont(FONT_TITLE, 18)
        c.setFillColor(col_alpha(C_ACCENT, 0.60))
        c.drawString(MARGIN + 12, item_y + 10, icon)

        # Section label
        c.setFont(FONT_BODY, 15)
        c.setFillColor(C_INK)
        c.drawString(MARGIN + 44, item_y + 10, label)

        # Dot leader
        c.setFont(FONT_CAPTION, 10)
        c.setFillColor(col_alpha(C_MUTED, 0.5))
        dots_x = MARGIN + 44 + c.stringWidth(label, FONT_BODY, 15) + 8
        dots_end = CW - MARGIN - 100
        dot_gap = 9
        dx = dots_x
        while dx < dots_end:
            c.drawString(dx, item_y + 10, "·")
            dx += dot_gap

        # Card count
        c.setFont(FONT_CAPTION, 10)
        c.setFillColor(col_alpha(C_SECONDARY, 0.70))
        c.drawRightString(CW - MARGIN - 8, item_y + 10,
                          f"{count} cards")

        c.linkAbsolute(bm_id, bm_id,
                       (MARGIN, item_y - 8, CW - MARGIN, item_y + 30),
                       Border="[0 0 0]")
        item_y -= 52

    # Bottom credit
    c.setFont(FONT_CAPTION, 9)
    c.setFillColor(col_alpha(C_MUTED, 0.6))
    c.drawCentredString(cx, MARGIN + 20,
                        f"© {PlannerConfig.PLANNER_YEAR}  ·  {PlannerConfig.PLANNER_EDITION}")


# ═══════════════════════════════════════════════════════════════════
#  UTILITY
# ═══════════════════════════════════════════════════════════════════

def _count_total_cards():
    total = 0
    sections = _build_section_list()
    for _, cards in sections:
        total += len(cards)
    return total


def _build_section_list():
    """Return list of (section_meta, cards_list) tuples respecting config flags."""
    sections = []
    cfg = PlannerConfig

    if cfg.INCLUDE_BEAUTY_RITUALS:
        sections.append((
            ("Section_Beauty", "Beauty Rituals", "✿",
             "Morning & evening beauty ceremonies"),
            BEAUTY_RITUAL_CARDS
        ))
    if cfg.INCLUDE_SLOW_LIVING:
        sections.append((
            ("Section_Slow", "Slow Living", "◦",
             "Daily rhythms & unhurried routines"),
            SLOW_LIVING_CARDS
        ))
    if cfg.INCLUDE_JOURNALING:
        sections.append((
            ("Section_Journal", "Journaling Prompts", "✦",
             "Deep prompts for self-exploration"),
            JOURNALING_CARDS
        ))
    if cfg.INCLUDE_WELLNESS:
        sections.append((
            ("Section_Wellness", "Wellness Reminders", "❁",
             "Body care & nervous system rituals"),
            WELLNESS_CARDS
        ))
    if cfg.INCLUDE_GRATITUDE:
        sections.append((
            ("Section_Gratitude", "Gratitude Practice", "♡",
             "Appreciation & presence exercises"),
            GRATITUDE_CARDS
        ))
    if cfg.INCLUDE_ROMANTICISE_LIFE:
        sections.append((
            ("Section_Romanticise", "Romanticise Your Life", "◇",
             "Finding magic in the everyday"),
            ROMANTICISE_CARDS
        ))
    if cfg.INCLUDE_AFFIRMATIONS:
        sections.append((
            ("Section_Affirmations", "Affirmations", "◯",
             "Words to carry with you"),
            AFFIRMATION_CARDS
        ))
    if cfg.INCLUDE_SEASONAL_RITUALS:
        sections.append((
            ("Section_Seasonal", "Seasonal Rituals", "❀",
             "Living in rhythm with nature"),
            SEASONAL_RITUAL_CARDS
        ))
    if cfg.INCLUDE_BOUNDARIES_REST:
        sections.append((
            ("Section_Boundaries", "Boundaries & Rest", "~",
             "Protecting your peace & energy"),
            BOUNDARY_REST_CARDS
        ))
    if cfg.INCLUDE_VISION_DREAMING:
        sections.append((
            ("Section_Vision", "Vision & Dreaming", "☀",
             "Manifestation & future self work"),
            VISION_DREAMING_CARDS
        ))
    return sections


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    # Resolve output path
    if PlannerConfig.OUTPUT_PATH:
        pdf_filename = PlannerConfig.OUTPUT_PATH
    else:
        safe_title = PlannerConfig.PLANNER_TITLE.replace(" ", "_")
        safe_sub   = PlannerConfig.PLANNER_SUBTITLE.replace(" ", "_").replace("&", "and")
        pdf_filename = f"{safe_title}_{safe_sub}_{PlannerConfig.PLANNER_YEAR}.pdf"

    c = canvas.Canvas(pdf_filename, pagesize=(CW, CH))
    c.setTitle(f"{PlannerConfig.PLANNER_TITLE} — {PlannerConfig.PLANNER_SUBTITLE}")
    c.setAuthor("Soft Life Studio")
    c.setSubject(PlannerConfig.PLANNER_EDITION)

    sections = _build_section_list()

    # Build index metadata (section_id, label, icon, card_count, start_card)
    index_meta = []
    card_counter = 0
    for (sec_id, sec_label, sec_icon, sec_subtitle), cards in sections:
        index_meta.append((sec_id, sec_label, sec_icon, len(cards), card_counter + 1))
        card_counter += len(cards)

    total_cards = sum(len(cards) for _, cards in sections)

    # ── Cover ──────────────────────────────────────────────────
    print("Generating Cover...")
    draw_cover(c)
    c.showPage()

    # ── Index ──────────────────────────────────────────────────
    print("Generating Index...")
    draw_index(c, index_meta)
    c.showPage()

    # ── Sections & Cards ──────────────────────────────────────
    global_card_num = 0
    for section_idx, ((sec_id, sec_label, sec_icon, sec_subtitle), cards) in enumerate(sections):
        print(f"Generating Section: {sec_label} ({len(cards)} cards)...")

        # Section divider
        draw_section_divider(c, sec_label, sec_subtitle, sec_icon,
                             len(cards), bookmark_id=sec_id)
        c.showPage()

        # Cards
        for card_idx, card_data in enumerate(cards):
            global_card_num += 1
            alt = (global_card_num % 2 == 0)
            bm = f"Card_{global_card_num}"
            draw_card(
                c, card_data,
                card_number=global_card_num,
                total_cards=total_cards,
                section_label=sec_label,
                alt_bg=alt,
                bookmark=bm,
            )
            c.showPage()

    c.save()
    print(f"\n✓  Done!  →  {pdf_filename}")
    print(f"   {total_cards} ritual cards across {len(sections)} sections")
    print(f"   Total pages: {2 + len(sections) + total_cards}  (cover + index + dividers + cards)")


if __name__ == "__main__":
    main()
