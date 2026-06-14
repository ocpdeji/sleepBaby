'use client';

import { useState, type FormEvent } from 'react';
import { ArrowRightIcon, CheckCircleIcon, MailIcon, UserIcon } from './icons';

declare global {
  interface Window {
    pintrk?: (...args: unknown[]) => void;
  }
}

type Variant = 'card' | 'footer' | 'inline';

interface Props {
  variant?: Variant;
  source?: string;
  withName?: boolean;
  buttonLabel?: string;
}

export default function EmailSignupForm({
  variant = 'card',
  source = 'website',
  withName = true,
  buttonLabel = 'Send it to me',
}: Props) {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const isFooter = variant === 'footer';

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus('loading');
    const form = e.currentTarget;
    const data = new FormData(form);

    try {
      const res = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: data.get('email'),
          name: data.get('name') || undefined,
          source,
        }),
      });
      if (res.ok) {
        setStatus('success');
        form.reset();

        if (typeof window !== 'undefined' && window.pintrk) {
          window.pintrk('track', 'lead', {
            lead_type: source,
          });
        }
      } else {
        const body = await res.json().catch(() => ({}));
        setMessage(body?.message ?? 'Something went wrong. Please try again.');
        setStatus('error');
      }
    } catch {
      setMessage('Network error. Please try again.');
      setStatus('error');
    }
  }

  if (status === 'success') {
    return (
      <div
        className={`rounded-2xl p-6 text-center ${
          isFooter ? 'bg-blush/10 text-blush' : 'bg-white/80 shadow-card'
        }`}
      >
        <CheckCircleIcon className={`mx-auto h-9 w-9 ${isFooter ? 'text-blush' : 'text-rose'}`} />
        <p className={`mt-3 font-serif text-xl font-semibold ${isFooter ? 'text-cream' : 'text-wine2'}`}>
          Your cheat sheet is on its way! 🌙
        </p>
        <p className={`mt-2 text-sm ${isFooter ? 'text-blush/75' : 'text-ink/70'}`}>
          Check your inbox (and the Promotions or Spam folder, just in case).
        </p>
      </div>
    );
  }

  const inputClass = isFooter
    ? 'w-full rounded-lg border border-blush/20 bg-blush/10 px-4 py-3 text-sm text-cream placeholder:text-blush/50 outline-none transition focus:border-blush focus:ring-2 focus:ring-blush/30'
    : 'w-full rounded-lg border border-white/70 bg-white px-12 py-4 text-sm text-ink shadow-sm outline-none transition placeholder:text-ink/40 focus:border-rose focus:ring-4 focus:ring-rose/15';

  return (
    <form onSubmit={handleSubmit} className="space-y-3" aria-label="Email signup">
      {withName && !isFooter && (
        <div className="relative">
          <UserIcon className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-cocoa/45" />
          <input
            type="text"
            name="name"
            placeholder="Your first name"
            className={inputClass}
            autoComplete="given-name"
          />
        </div>
      )}

      <div className="relative">
        {!isFooter && (
          <MailIcon className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-cocoa/45" />
        )}
        <input
          type="email"
          name="email"
          required
          placeholder="Your email address"
          className={inputClass}
          autoComplete="email"
        />
      </div>

      <button
        type="submit"
        disabled={status === 'loading'}
        className={`btn-shine flex w-full items-center justify-center gap-3 rounded-full px-7 py-4 text-xs font-extrabold uppercase tracking-[0.18em] text-white shadow-soft transition hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-70 ${
          isFooter ? 'bg-rose hover:bg-rose/90' : 'bg-wine hover:bg-wine2'
        }`}
      >
        {status === 'loading' ? 'Sending…' : buttonLabel}
        {status !== 'loading' && <ArrowRightIcon className="h-4 w-4" />}
      </button>

      {status === 'error' && (
        <p className={`text-xs ${isFooter ? 'text-blush' : 'text-wine'}`}>{message}</p>
      )}

      <p className={`flex items-center justify-center gap-2 text-xs ${isFooter ? 'text-blush/55' : 'text-ink/50'}`}>
        <CheckCircleIcon className={`h-4 w-4 ${isFooter ? 'text-blush' : 'text-rose'}`} />
        No spam. Unsubscribe anytime.
      </p>
    </form>
  );
}
