import { NextResponse } from 'next/server';
import { subscribe, CHEATSHEET_GROUP_ID, WEBSITE_GROUP_ID } from '@/lib/mailerlite';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(request: Request) {
  let payload: { email?: string; name?: string; source?: string };
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ message: 'Invalid request.' }, { status: 400 });
  }

  const email = (payload.email ?? '').trim().toLowerCase();
  const name = payload.name?.trim();
  const source = payload.source ?? 'website';

  if (!EMAIL_RE.test(email)) {
    return NextResponse.json({ message: 'Please enter a valid email address.' }, { status: 422 });
  }

  // Cheat-sheet sources go to the lead-magnet group; everything else to website.
  const groupId =
    source.includes('cheatsheet') || source.includes('sleep-guide')
      ? CHEATSHEET_GROUP_ID
      : WEBSITE_GROUP_ID;

  const result = await subscribe({
    email,
    name,
    groupId,
    fields: { source },
  });

  if (!result.ok) {
    return NextResponse.json(
      { message: result.message ?? 'Subscription failed.' },
      { status: result.status >= 400 ? result.status : 502 }
    );
  }

  return NextResponse.json({ ok: true });
}
