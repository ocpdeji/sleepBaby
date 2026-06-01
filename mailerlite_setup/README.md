# MailerLite Funnel Setup
## Sleep, Baby. Please. — Six & Thriving | 2026

Provisions your entire MailerLite welcome funnel via the API.

---

## What it does

| Action | API supports? |
|--------|---------------|
| Create the "Sleep Baby Lead Magnet" group | ✅ Automated |
| Create custom fields (signup_source, lead_magnet, ebook_purchased) | ✅ Automated |
| Create 5 prebuilt email campaigns as drafts | ✅ Automated |
| Save all 5 emails as standalone HTML files | ✅ Automated |
| Create a draft automation shell | ✅ Automated |
| **Wire delays + emails into the automation** | ❌ MailerLite API limitation — must be done in UI (10 min) |
| Set automation trigger (joins group) | ❌ UI step |
| Build the signup form | ❌ UI step (MailerLite has a great form builder — easier in UI) |

---

## One-time setup

### 1. Get your MailerLite API key

- Sign in: https://dashboard.mailerlite.com
- Go to: **Account → Integrations → MailerLite API**
- Click **Generate new token**
- Copy the token

### 2. Configure your environment

```powershell
# Copy the template
Copy-Item .env.example .env

# Open .env in your editor and paste your key + URLs
notepad .env
```

Required values:
- `MAILERLITE_API_KEY` — the token from step 1
- `FROM_EMAIL` — your sending email (must be on a verified domain)
- `FROM_NAME` — `Six & Thriving`
- `BUY_BOOK_URL` — where to send buyers (e.g. https://www.sixandthriving.com/buy)
- `CHEAT_SHEET_URL` — where the cheat sheet PDF is hosted

### 3. Install dependencies (once)

```powershell
pip install requests python-dotenv
```

### 4. Run the script

```powershell
cd mailerlite_setup
python setup_funnel.py
```

You'll see output like:

```
═══════════════════════════════════════════
╔ Step 1 / 5: Group ╗
═══════════════════════════════════════════
   ✓ Created group 'Sleep Baby Lead Magnet' (id=...)
...
```

---

## After running — manual UI wiring (10 min)

Log into MailerLite and finish these steps:

### Wire the automation
1. Go to **Automations** → open `Welcome Sequence — 5-Email Funnel`
2. Set the trigger: **Subscriber joins group** → `Sleep Baby Lead Magnet`
3. Add these workflow steps:

   | Step | Type | Delay | Email |
   |------|------|-------|-------|
   | 1 | Email | 0 min (instant) | `01 — Welcome + Cheat Sheet` |
   | 2 | Email | 2 days | `02 — The 3-Minute Pause` |
   | 3 | Email | 2 days | `03 — Six Babies, Six Puzzles` |
   | 4 | Email | 2 days | `04 — Nobody Talks About Night 3` |
   | 5 | Email | 2 days | `05 — The $19 Launch Pitch` |

   For each Email step, choose **Use existing email** and pick the matching draft.

4. Toggle the automation **ON** once your domain is verified.

### Build the signup form
1. Go to **Forms → Embedded form**
2. Connect to group: `Sleep Baby Lead Magnet`
3. Form copy:
   - Headline: **The Baby Sleep Cheat Sheet**
   - Subhead: *Wake windows, nap counts, bedtime targets — free PDF*
   - Button: **Send Me The Cheat Sheet**
4. On success: either redirect to your `CHEAT_SHEET_URL`, or attach the PDF to email 01.
5. Copy the embed code → paste into your landing page.

---

## Files in this folder

```
mailerlite_setup/
├── README.md            ← this file
├── .env.example         ← template (copy to .env)
├── .env                 ← your secrets (gitignored)
├── .gitignore
├── email_content.py     ← all 5 email subjects + bodies (edit me!)
├── mailerlite_client.py ← thin REST wrapper
├── setup_funnel.py      ← the entry point — run this
└── generated_emails/    ← .html backup of every email
```

---

## Re-running

The script is **idempotent** — re-running won't create duplicates of the group
or fields. It WILL create new draft campaigns each time though, so if you re-run
just delete the old drafts in MailerLite first (or rename `email_content.py` names).

---

## Customising

**To change email content:** edit `email_content.py`. The script renders each
email through the brand HTML shell automatically.

**To change the group/automation names:** edit the constants at the top of
`setup_funnel.py`.

**To use different URLs in the emails:** edit `.env` and re-run.

---

## Troubleshooting

**"Missing API key"** → you haven't created `.env` yet, or your key isn't pasted.

**"422 unprocessable entity" on campaign creation** → MailerLite hasn't verified
your sending domain. Wait for the domain to activate, then re-run.

**Domain says "Wait to activate"** → it's processing DNS records (SPF / DKIM).
Usually 1–24 hours after you add the records to your DNS.

**Free MailerLite plan limits** → 1,000 subscribers, 12,000 emails/mo.
Plenty for your launch. Upgrade later when you outgrow it.
