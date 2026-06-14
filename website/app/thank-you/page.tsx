'use client';

import { useEffect } from 'react';
import Link from 'next/link';

declare global {
  interface Window {
    pintrk?: (...args: unknown[]) => void;
  }
}

export default function ThankYouPage() {
  useEffect(() => {
    // Fire Pinterest Checkout event once when page loads
    if (typeof window !== 'undefined' && window.pintrk) {
      window.pintrk('track', 'checkout', {
        value: 19.99,
        order_quantity: 1,
        currency: 'USD',
      });
    }
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-cream px-6 text-center">

      <div className="max-w-lg">

        {/* Icon */}
        <div className="mb-6 text-6xl">🌙</div>

        {/* Headline */}
        <h1 className="font-serif text-4xl font-bold text-wine2 mb-4">
          You did it, mama.
        </h1>

        {/* Subhead */}
        <p className="text-lg text-ink/70 mb-2">
          <strong className="text-ink">Sleep, Baby. Please.</strong> is on its way to your inbox right now.
        </p>

        <p className="text-base text-ink/60 mb-8">
          Check your email (and your Promotions or Spam folder, just in case).
          Your download link is inside.
        </p>

        {/* Divider */}
        <div className="mx-auto mb-8 h-px w-16 bg-rose/30" />

        {/* What's next */}
        <p className="text-sm font-semibold uppercase tracking-widest text-rose mb-4">
          While you wait
        </p>

        <div className="space-y-3 mb-10">
          <a
            href="https://pinterest.ca/SixAndThriving"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-3 rounded-full border border-rose/20 bg-white px-6 py-3 text-sm font-semibold text-wine2 shadow-sm transition hover:border-rose hover:shadow-md"
          >
            📌 Follow us on Pinterest for daily sleep tips
          </a>
          <a
            href="https://instagram.com/sixandthrivingmom"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-3 rounded-full border border-rose/20 bg-white px-6 py-3 text-sm font-semibold text-wine2 shadow-sm transition hover:border-rose hover:shadow-md"
          >
            📸 Join us on Instagram @sixandthrivingmom
          </a>
        </div>

        {/* Back to site */}
        <Link
          href="/"
          className="text-sm text-ink/40 underline underline-offset-4 hover:text-ink/70 transition"
        >
          ← Back to Six & Thriving
        </Link>

      </div>

    </main>
  );
}
