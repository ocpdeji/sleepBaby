"""
Sleep, Baby. Please. — MailerLite Funnel Setup
═══════════════════════════════════════════════════════════════════
Provisions everything possible in your MailerLite account via API:
  ✓ The "Sleep Baby Lead Magnet" group
  ✓ Custom fields (signup_source, lead_magnet, ebook_purchased)
  ✓ 5 prebuilt email campaigns ready to drop into your automation
  ✓ A draft automation shell named & ready
  ✓ Saves all 5 emails as standalone .html files (backup)
  ✓ Prints exact UI steps for the manual wiring (10 minutes)

PREREQUISITES:
  1. MailerLite account (free works to start)
  2. Domain verified in MailerLite (you're waiting on this — that's fine,
     the script will still create everything; you can enable later)
  3. Copy .env.example → .env and add your API key

Run:
  cd mailerlite_setup
  python setup_funnel.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env vars from mailerlite_setup/.env
SCRIPT_DIR = Path(__file__).parent
load_dotenv(SCRIPT_DIR / ".env")

# Local imports
sys.path.insert(0, str(SCRIPT_DIR))
from mailerlite_client import MailerLite
from email_content import ALL_EMAILS, render_email


# ────────────────────────────────────────────────────────────────
# CONFIG (read from .env)
# ────────────────────────────────────────────────────────────────
API_KEY = os.getenv("MAILERLITE_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "hello@sixandthriving.com")
FROM_NAME = os.getenv("FROM_NAME", "Six & Thriving")
BUY_BOOK_URL = os.getenv("BUY_BOOK_URL", "https://www.sixandthriving.com/buy")
CHEAT_SHEET_URL = os.getenv("CHEAT_SHEET_URL",
                            "https://www.sixandthriving.com/downloads/cheat-sheet")

GROUP_NAME = "Sleep Baby Lead Magnet"
AUTOMATION_NAME = "Welcome Sequence — 5-Email Funnel"

CUSTOM_FIELDS = [
    ("signup_source", "text"),
    ("lead_magnet", "text"),
    ("ebook_purchased", "text"),
]

# Where to save the HTML email backups
EMAILS_DIR = SCRIPT_DIR / "generated_emails"
EMAILS_DIR.mkdir(exist_ok=True)


def banner(title: str):
    bar = "═" * (len(title) + 4)
    print(f"\n  {bar}")
    print(f"  ╔ {title} ╗")
    print(f"  {bar}")


def main():
    banner("Sleep, Baby. Please. — MailerLite Funnel Setup")

    if not API_KEY or API_KEY == "your_api_key_here":
        print("\n  ❌ Missing API key.")
        print("  Steps to fix:")
        print("     1. cp .env.example .env  (or copy it manually)")
        print("     2. Open .env and paste your MailerLite API key")
        print("     3. Get your key at:")
        print("        https://dashboard.mailerlite.com/integrations/api")
        return

    ml = MailerLite(API_KEY)

    # ────────────────────────────────────────────────
    # 1. GROUP
    # ────────────────────────────────────────────────
    banner("Step 1 / 5: Group")
    group = ml.get_or_create_group(GROUP_NAME)
    group_id = group["id"]

    # ────────────────────────────────────────────────
    # 2. CUSTOM FIELDS
    # ────────────────────────────────────────────────
    banner("Step 2 / 5: Custom fields")
    for fname, ftype in CUSTOM_FIELDS:
        ml.get_or_create_field(fname, ftype)

    # ────────────────────────────────────────────────
    # 3. EMAIL CAMPAIGNS (draft)
    # ────────────────────────────────────────────────
    banner("Step 3 / 5: Email drafts (5 emails)")
    print(f"  From: {FROM_NAME} <{FROM_EMAIL}>")
    print(f"  Group target: {GROUP_NAME} (id={group_id})")
    print()

    created_campaigns = []
    for i, email in enumerate(ALL_EMAILS, start=1):
        # Personalise URL placeholders inside the email body
        body_html = email["body"].format(
            BUY_BOOK_URL=BUY_BOOK_URL,
            CHEAT_SHEET_URL=CHEAT_SHEET_URL,
        )
        html = render_email(body_html)

        # Save the .html backup locally
        safe_name = email["name"].replace(" ", "_").replace("—", "-").replace("/", "_")
        out_path = EMAILS_DIR / f"{safe_name}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  💾 Saved HTML: {out_path.name}")

        # Try to create the draft campaign in MailerLite
        try:
            camp = ml.create_campaign(
                name=email["name"],
                subject=email["subject"],
                from_email=FROM_EMAIL,
                from_name=FROM_NAME,
                content_html=html,
                group_ids=[group_id],
            )
            created_campaigns.append(camp)
            print(f"     ✓ Draft #{i} created in MailerLite")
        except RuntimeError as e:
            print(f"     ⚠ Could not create draft #{i}: {e}")
            print(f"        → use the saved HTML file as a fallback")

        print()

    # ────────────────────────────────────────────────
    # 4. AUTOMATION SHELL (draft) — idempotent
    # ────────────────────────────────────────────────
    banner("Step 4 / 5: Automation shell")
    try:
        automation = ml.get_or_create_automation(AUTOMATION_NAME)
        print(f"  ✓ Automation ready: '{AUTOMATION_NAME}'")
        print(f"     id = {automation['id']}")
    except RuntimeError as e:
        print(f"  ⚠ Could not create automation: {e}")

    # ────────────────────────────────────────────────
    # 5. NEXT STEPS
    # ────────────────────────────────────────────────
    banner("Step 5 / 5: What you need to finish manually (10 min)")
    print("""
  MailerLite's API can create drafts but cannot wire delays + emails
  into an automation. Here's exactly what to click:

  1. Log into MailerLite → Automations
  2. Open '{auto_name}'
  3. Set the trigger:
        Type: 'Subscriber joins group'
        Group: '{group_name}'
  4. Add these workflow steps in order:

        [DELAY: 0 minutes]  → Email: 01 — Welcome + Cheat Sheet
        [DELAY: 2 days]     → Email: 02 — The 3-Minute Pause
        [DELAY: 2 days]     → Email: 03 — Six Babies, Six Puzzles
        [DELAY: 2 days]     → Email: 04 — Nobody Talks About Night 3
        [DELAY: 2 days]     → Email: 05 — The $19 Launch Pitch

  5. For each Email step: 'Use existing email' → pick the matching
     draft from your campaigns (we created them in step 3).
  6. Toggle the automation ON (top right) once domain is verified.

  7. Build a SIGNUP FORM (MailerLite → Forms → Embedded form):
        - Connect to group: '{group_name}'
        - Headline: "The Baby Sleep Cheat Sheet"
        - Subhead:  "Wake windows, nap counts, bedtime targets — free PDF"
        - Button:   "Send Me The Cheat Sheet"
        - Add the form's embed code to your landing page.

  8. Set up the cheat sheet delivery on the form's success message:
        - Either redirect to your hosted PDF URL ({cheat_sheet_url})
        - OR attach the PDF to email 01 directly.

  ⚠ Domain reminder: emails won't actually send until 'sixandthriving.com'
     is verified in MailerLite (Account → Domains). You can do all the
     setup now and toggle live once it's green.
""".format(
        auto_name=AUTOMATION_NAME,
        group_name=GROUP_NAME,
        cheat_sheet_url=CHEAT_SHEET_URL,
    ))

    print(f"  📁 Email HTML backups saved in: {EMAILS_DIR}")
    print()
    print("  ✅ Provisioning complete. Drafts are sitting in your MailerLite.")
    print()


if __name__ == "__main__":
    main()
