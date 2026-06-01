"""
The 5-email welcome sequence content.
Used by setup_funnel.py to create draft campaigns in MailerLite.

Each email is a tuple: (delay_days, subject, html_body, plain_text_body)
Edit anything you want before running the setup script.
"""


def render_email(body_html: str, *, name: str = "{$name}") -> str:
    """Wrap a body in the brand HTML shell — navy/gold/cream styling."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Sleep, Baby. Please.</title></head>
<body style="margin:0;padding:0;background:#FAF7F2;font-family:Georgia,serif;color:#4A5568;line-height:1.6;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#FAF7F2;">
  <tr><td align="center" style="padding:24px;">
    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border-radius:8px;overflow:hidden;">
      <!-- Navy header -->
      <tr><td style="background:#0D1B3E;padding:18px 28px;">
        <table width="100%"><tr>
          <td style="color:#FAF7F2;font-family:Georgia,serif;font-weight:bold;font-size:14px;">Sleep, Baby. Please.</td>
          <td align="right" style="color:#C9A84C;font-family:Arial,sans-serif;font-size:11px;letter-spacing:1px;">SIX &amp; THRIVING</td>
        </tr></table>
      </td></tr>
      <!-- Gold accent strip -->
      <tr><td style="background:#C9A84C;height:3px;"></td></tr>
      <!-- Body -->
      <tr><td style="padding:36px 32px 28px 32px;font-family:Arial,sans-serif;font-size:15px;color:#4A5568;line-height:1.7;">
        {body_html}
      </td></tr>
      <!-- Footer -->
      <tr><td style="background:#F0EBE1;padding:18px 28px;border-top:1px solid #D4B896;">
        <table width="100%"><tr>
          <td style="color:#718096;font-family:Arial,sans-serif;font-size:11px;">Six &amp; Thriving · <a href="https://www.sixandthriving.com" style="color:#718096;text-decoration:underline;">www.sixandthriving.com</a></td>
          <td align="right" style="color:#718096;font-family:Arial,sans-serif;font-size:11px;">© 2026 Six &amp; Thriving</td>
        </tr></table>
      </td></tr>
    </table>
    <p style="font-family:Arial,sans-serif;font-size:11px;color:#718096;max-width:600px;padding:18px;">
      You're receiving this because you signed up for the Baby Sleep Cheat Sheet.
      <a href="{{$unsubscribe}}" style="color:#718096;">Unsubscribe</a> any time.
    </p>
  </td></tr>
</table>
</body></html>"""


def signoff() -> str:
    return """
<p style="margin-top:28px;color:#4A5568;">With love and solidarity,</p>
<p style="margin-top:4px;color:#C9A84C;font-weight:bold;font-family:Georgia,serif;">— Six &amp; Thriving</p>
"""


# ────────────────────────────────────────────────────────────────────────
# THE 5 EMAILS
# ────────────────────────────────────────────────────────────────────────

EMAIL_1_DAY = 0
EMAIL_1_SUBJECT = "Here's your cheat sheet (and a small confession)"
EMAIL_1_BODY = """
<p>Hi friend,</p>
<p>Your <strong>Baby Sleep Cheat Sheet</strong> is right here:
<a href="{CHEAT_SHEET_URL}" style="color:#0D1B3E;font-weight:bold;">→ Download it again</a></p>
<p>Save it to your phone. Print it. Stick it on the fridge.</p>
<p>But before you go — I want you to know something.</p>
<p>If you're reading this at 2am with a baby in one arm and your phone in the other,
<strong>I see you.</strong> I've been there. Six times.</p>
<p>I'm not a sleep clinic. I don't have a PhD. I'm a mom of six (yes, including a set of twins
tucked in the middle) who spent the better part of a decade in the trenches of infant and toddler sleep.</p>
<p>And here's what I want you to hear before anything else:</p>
<blockquote style="border-left:3px solid #C9A84C;padding:12px 18px;margin:18px 0;background:#FAF7F2;color:#0D1B3E;font-style:italic;">
Your baby is not broken. You are not failing. The situation you're in right now is
<strong>temporary, it is solvable, and you are going to come through it</strong>.
</blockquote>
<p>Tomorrow I'll send you ONE thing you can do tonight to make tomorrow's nights easier.</p>
<p>For now: open the cheat sheet. Find your baby's age. Note the awake window.
That alone changes more nights than you'd believe.</p>
<p style="color:#0D1B3E;font-weight:bold;">Sleep is coming. For both of you.</p>
""" + signoff()

# ────────────────────────────────────────────────────────────────────────

EMAIL_2_DAY = 2
EMAIL_2_SUBJECT = "The 3-minute pause that changes everything"
EMAIL_2_BODY = """
<p>Hi friend,</p>
<p>Today I want to give you ONE quick win. Something you can do tonight, no setup, no equipment.</p>
<p style="font-size:18px;color:#0D1B3E;font-family:Georgia,serif;font-weight:bold;margin-top:24px;">
The 3-Minute Pause.
</p>
<p>Here's what it is: when your baby makes a sound at night, before you do anything — wait 3 minutes.</p>
<p>Set a timer if you have to. Listen carefully. Are they actually crying, or just rustling and making sleep noises?</p>
<p>Most parents go in within 30 seconds because we're terrified of letting our babies cry.
But in those 30 seconds, we accidentally <strong>wake the baby up</strong> who was actually halfway through cycling through a light sleep phase.</p>
<p>The 3-minute pause gives them a chance to resettle on their own — which is the entire skill we're trying to teach.</p>
<p>Try it tonight. Just for one waking. See what happens.</p>
<p>Within 3 days, you'll start hearing the difference between your baby's "I'm cycling" noises and their "I genuinely need you" cry.
That single skill is worth its weight in gold.</p>
<p style="margin-top:18px;font-size:13px;color:#718096;font-style:italic;">
P.S. If your baby is genuinely distressed (escalating cry, signs of pain, fever) — go in. Always. The pause is for the rustles, not the screams.
</p>
""" + signoff()

# ────────────────────────────────────────────────────────────────────────

EMAIL_3_DAY = 4
EMAIL_3_SUBJECT = "Six babies. Six sleep puzzles."
EMAIL_3_BODY = """
<p>I've been thinking about you.</p>
<p>I want to tell you a story I don't share often. It's about my fourth baby.</p>
<p>He was the one who nearly broke me. The other three slept through by 4 months.
He didn't sleep through until 14 weeks — and even then, "sleeping through" meant 5 hours, not 8.</p>
<p>I'd done all the things. The bath. The lavender. The white noise. The schedule.
And he just… wouldn't.</p>
<p>One night around 3am, I sat in the hallway outside his room and cried. Not a polite cry —
the deep, ugly, shoulder-shaking kind. I genuinely thought I was failing him.</p>
<p>Then I did what I'd been resisting: I sat down with everything I'd learned across three previous babies
and just <strong>made a plan</strong>. A real, written-down,
"this is what I'll do at 11pm and this is what I'll do at 2am" plan.</p>
<p>Within 5 nights, he was sleeping through.</p>
<p style="color:#0D1B3E;font-weight:bold;font-family:Georgia,serif;font-size:18px;margin-top:24px;">
That's when I realised: it wasn't the method. It was the plan.
</p>
<p>The decision made before the night started.</p>
<p>If you're winging it at 2am — that's the thing to fix. Not your baby. Not the technique. The plan.</p>
<p>Tomorrow I'll tell you about the night that nearly made me give up on the plan —
<strong>Night 3</strong>. The one nobody warns you about.</p>
""" + signoff()

# ────────────────────────────────────────────────────────────────────────

EMAIL_4_DAY = 6
EMAIL_4_SUBJECT = "Nobody talks about Night 3"
EMAIL_4_BODY = """
<p>I told you I'd come back to talk about Night 3.</p>
<p>Here's what nobody tells you about sleep training:</p>
<p>The first night is hard. The second night might be a little better.
The third night is <strong>a disaster</strong>.</p>
<p>Not because the method is failing.
<strong style="color:#0D1B3E;">Because it's WORKING.</strong></p>
<p>This is called the <strong>extinction burst</strong>. It's a known psychological phenomenon:
when a previously rewarded behaviour (your baby crying until they're picked up) stops being rewarded,
the behaviour <strong>escalates dramatically before it disappears</strong>.</p>
<p>It's the toddler tantrum when the iPad is taken away.
It's the addict's withdrawal symptom right before they break free.
It's the system frantically trying to make the old solution work one more time.</p>
<p>And in the moment, it feels exactly like failure.</p>
<p style="color:#C0392B;font-weight:bold;">This is the night most parents quit.</p>
<p>It's also the night that, if you hold the line, almost always leads to a dramatically better Night 4.</p>
<p>I have lost count of the number of moms who've messaged me after Night 4 saying
<em>"I almost gave up last night. I'm so glad I didn't."</em></p>
<p>If you ever try sleep training: write yourself a note <em>before</em> you start.
Stick it on the fridge.</p>
<blockquote style="border-left:3px solid #C9A84C;padding:12px 18px;margin:18px 0;background:#FAF7F2;color:#0D1B3E;font-style:italic;">
"Night 3 will be the hardest. This is normal. This means it's working. Do not give up."
</blockquote>
<p>That single sentence might be the most important thing in this whole sleep journey.</p>
<p style="margin-top:24px;font-size:13px;color:#718096;">
P.S. I wrote a whole book about this — including a full chapter on Night 3, the methods I've used across all six babies,
and a 7-night plan you can start tonight. If you want it, I'll tell you about it tomorrow.
If not, I'll see you next week with another quick tip. No pressure either way.
</p>
""" + signoff()

# ────────────────────────────────────────────────────────────────────────

EMAIL_5_DAY = 8
EMAIL_5_SUBJECT = "OK — here's what I wrote"
EMAIL_5_BODY = """
<p>Yesterday's email about Night 3 got the most replies of any email I've ever sent.
Mostly variations of: <em>"I needed this six months ago"</em> and <em>"I cried reading it."</em></p>
<p>I wrote it because I needed someone to tell me that, six years ago, with my fourth baby. Nobody did.</p>
<p>So I wrote the book I needed.</p>
<p style="font-size:22px;color:#0D1B3E;font-family:Georgia,serif;font-weight:bold;margin-top:28px;">
Sleep, Baby. Please.
</p>
<p style="color:#C9A84C;font-style:italic;font-family:Georgia,serif;font-size:14px;margin-top:0;">
59 pages. 15 chapters. Built from everything I've learned across six babies.
</p>
<p style="margin-top:18px;">Including:</p>
<ul style="line-height:1.9;">
<li>The full <strong>7-night plan</strong> (with what to expect each night)</li>
<li>Detailed instructions for <strong>every major sleep training method</strong></li>
<li>The <strong>Six Sleep Personalities</strong> (find yours and the strategy that fits)</li>
<li>The <strong>Crib Hour technique</strong> (for 30-minute nappers)</li>
<li>A full <strong>breastfeeding & sleep</strong> chapter</li>
<li>A <strong>twins, NICU, and daycare</strong> chapter</li>
<li>A <strong>partner briefing one-pager</strong></li>
<li>The <strong>Reset Protocol</strong> (for parents who've tried before and failed)</li>
</ul>
<p style="margin-top:24px;">And because you've been here for over a week, you get the founding price:</p>
<p style="margin:24px 0;text-align:center;">
<a href="{BUY_BOOK_URL}" style="display:inline-block;background:#0D1B3E;color:#C9A84C;padding:16px 36px;font-family:Arial,sans-serif;font-weight:bold;font-size:16px;text-decoration:none;border-radius:6px;">
GET THE BOOK &nbsp;&rarr;&nbsp; $19
</a>
</p>
<p style="text-align:center;color:#0D1B3E;font-weight:bold;">
$19 instead of $29 — for the next 48 hours only.
</p>
<p>If now isn't the right time — totally understand. The cheat sheet is yours forever,
and I'll keep showing up here every week with free tips.</p>
<p>If now <em>is</em> the right time — I think it'll change your nights. I really do.</p>
<p>Either way, thank you for being here. You're not alone in this.</p>
<p style="color:#0D1B3E;font-weight:bold;margin-top:24px;">
Sleep is coming. For both of you.
</p>
<p style="margin-top:24px;font-size:13px;color:#718096;">
P.S. The 30% launch discount expires in 48 hours. After that the book goes to $29.
No tricks, no fake countdowns — just a thank-you to my early community.
30-day no-questions-asked refund if it's not for you.
</p>
""" + signoff()


# ────────────────────────────────────────────────────────────────────────

ALL_EMAILS = [
    {"day": EMAIL_1_DAY, "subject": EMAIL_1_SUBJECT, "body": EMAIL_1_BODY,
     "name": "01 — Welcome + Cheat Sheet"},
    {"day": EMAIL_2_DAY, "subject": EMAIL_2_SUBJECT, "body": EMAIL_2_BODY,
     "name": "02 — The 3-Minute Pause"},
    {"day": EMAIL_3_DAY, "subject": EMAIL_3_SUBJECT, "body": EMAIL_3_BODY,
     "name": "03 — Six Babies, Six Puzzles"},
    {"day": EMAIL_4_DAY, "subject": EMAIL_4_SUBJECT, "body": EMAIL_4_BODY,
     "name": "04 — Nobody Talks About Night 3"},
    {"day": EMAIL_5_DAY, "subject": EMAIL_5_SUBJECT, "body": EMAIL_5_BODY,
     "name": "05 — The $19 Launch Pitch"},
]
