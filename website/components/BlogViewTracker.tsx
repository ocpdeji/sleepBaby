'use client';

import { useEffect } from 'react';

/**
 * Fire-and-forget page-view ping to Supabase via our API route.
 * Silent by design — analytics should never block or break the read.
 */
export default function BlogViewTracker({ slug }: { slug: string }) {
  useEffect(() => {
    const key = `viewed:${slug}`;
    if (sessionStorage.getItem(key)) return;
    sessionStorage.setItem(key, '1');
    fetch('/api/views', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slug }),
      keepalive: true,
    }).catch(() => {});
  }, [slug]);

  return null;
}
