import { NextResponse } from 'next/server';
import { createServiceClient, isSupabaseConfigured } from '@/lib/supabase';
import { subscribe, WEBSITE_GROUP_ID } from '@/lib/mailerlite';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(request: Request) {
  let payload: { name?: string; email?: string; message?: string };
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ message: 'Invalid request.' }, { status: 400 });
  }

  const name = (payload.name ?? '').trim();
  const email = (payload.email ?? '').trim().toLowerCase();
  const message = (payload.message ?? '').trim();

  if (!name || !EMAIL_RE.test(email) || message.length < 5) {
    return NextResponse.json(
      { message: 'Please fill in your name, a valid email, and a message.' },
      { status: 422 }
    );
  }

  // Persist to Supabase (best-effort — don't fail the user if DB is down).
  if (isSupabaseConfigured && process.env.SUPABASE_SERVICE_ROLE_KEY) {
    try {
      const supabase = createServiceClient();
      await supabase.from('contacts').insert({ name, email, message });
    } catch {
      // swallow — message still gets emailed via MailerLite below
    }
  }

  // Add to website subscribers + tag for follow-up (auto-reply handled in MailerLite).
  await subscribe({
    email,
    name,
    groupId: WEBSITE_GROUP_ID,
    fields: { source: 'contact-form', last_message: message.slice(0, 250) },
  });

  return NextResponse.json({ ok: true });
}
