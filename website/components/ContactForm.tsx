'use client';

import { useState, type FormEvent } from 'react';
import { ArrowRightIcon, CheckCircleIcon } from './icons';

export default function ContactForm() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus('loading');
    const form = e.currentTarget;
    const data = new FormData(form);

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.get('name'),
          email: data.get('email'),
          message: data.get('message'),
        }),
      });
      if (res.ok) {
        setStatus('success');
        form.reset();
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
      <div className="rounded-3xl border border-rose/10 bg-white/85 p-10 text-center shadow-card">
        <CheckCircleIcon className="mx-auto h-12 w-12 text-rose" />
        <h2 className="mt-4 font-serif text-2xl font-semibold text-wine2">Message sent! 💛</h2>
        <p className="mt-2 text-sm text-ink/70">
          Thanks for reaching out — Kate reads every message and will get back to you soon.
        </p>
      </div>
    );
  }

  const field =
    'w-full rounded-lg border border-rose/15 bg-white px-4 py-3.5 text-sm text-ink shadow-sm outline-none transition placeholder:text-ink/40 focus:border-rose focus:ring-4 focus:ring-rose/15';

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 rounded-3xl border border-rose/10 bg-white/85 p-8 shadow-card backdrop-blur"
    >
      <div>
        <label htmlFor="name" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-cocoa">
          Your name
        </label>
        <input id="name" name="name" required placeholder="Jane Doe" className={field} autoComplete="name" />
      </div>
      <div>
        <label htmlFor="email" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-cocoa">
          Email
        </label>
        <input id="email" name="email" type="email" required placeholder="you@example.com" className={field} autoComplete="email" />
      </div>
      <div>
        <label htmlFor="message" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-cocoa">
          How can we help?
        </label>
        <textarea id="message" name="message" required rows={5} placeholder="Tell us a little about what’s going on…" className={`${field} resize-y`} />
      </div>

      <button
        type="submit"
        disabled={status === 'loading'}
        className="btn-shine flex w-full items-center justify-center gap-3 rounded-full bg-wine px-8 py-4 text-xs font-extrabold uppercase tracking-[0.18em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {status === 'loading' ? 'Sending…' : 'Send message'}
        {status !== 'loading' && <ArrowRightIcon className="h-4 w-4" />}
      </button>

      {status === 'error' && <p className="text-xs text-wine">{message}</p>}
    </form>
  );
}
