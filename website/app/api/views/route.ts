import { NextResponse } from 'next/server';
import { createServiceClient, isSupabaseConfigured } from '@/lib/supabase';

export async function POST(request: Request) {
  let slug = '';
  try {
    const body = await request.json();
    slug = (body?.slug ?? '').toString().slice(0, 120);
  } catch {
    return NextResponse.json({ ok: false }, { status: 400 });
  }
  if (!slug) return NextResponse.json({ ok: false }, { status: 400 });

  if (isSupabaseConfigured && process.env.SUPABASE_SERVICE_ROLE_KEY) {
    try {
      const country = request.headers.get('x-vercel-ip-country') ?? null;
      const supabase = createServiceClient();
      await supabase.from('blog_views').insert({ slug, country });
    } catch {
      // analytics are best-effort
    }
  }

  return NextResponse.json({ ok: true });
}
