'use client';

import { useState, type FormEvent } from 'react';
import type { SupabaseClient } from '@supabase/supabase-js';
import Logo from '@/components/Logo';
import { ArrowRightIcon } from '@/components/icons';

export default function AdminLogin({ supabase }: { supabase: SupabaseClient }) {
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');
  const [error, setError] = useState('');

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus('loading');
    setError('');
    const data = new FormData(e.currentTarget);
    const { error } = await supabase.auth.signInWithPassword({
      email: String(data.get('email')),
      password: String(data.get('password')),
    });
    if (error) {
      setError(error.message);
      setStatus('error');
    }
  }

  const field =
    'w-full rounded-lg border border-rose/15 bg-white px-4 py-3.5 text-sm text-ink shadow-sm outline-none transition placeholder:text-ink/40 focus:border-rose focus:ring-4 focus:ring-rose/15';

  return (
    <div className="flex min-h-[70vh] items-center justify-center px-5 py-16">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex justify-center">
          <Logo />
        </div>
        <form
          onSubmit={handleSubmit}
          className="space-y-4 rounded-3xl border border-rose/10 bg-white/85 p-8 shadow-soft backdrop-blur"
        >
          <h1 className="text-center font-serif text-2xl font-semibold text-wine2">
            Dashboard login
          </h1>
          <div>
            <label htmlFor="email" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-cocoa">
              Email
            </label>
            <input id="email" name="email" type="email" required className={field} autoComplete="email" />
          </div>
          <div>
            <label htmlFor="password" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-cocoa">
              Password
            </label>
            <input id="password" name="password" type="password" required className={field} autoComplete="current-password" />
          </div>
          <button
            type="submit"
            disabled={status === 'loading'}
            className="btn-shine flex w-full items-center justify-center gap-3 rounded-full bg-wine px-8 py-3.5 text-xs font-extrabold uppercase tracking-[0.18em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2 disabled:opacity-70"
          >
            {status === 'loading' ? 'Signing in…' : 'Sign in'}
            {status !== 'loading' && <ArrowRightIcon className="h-4 w-4" />}
          </button>
          {status === 'error' && <p className="text-center text-xs text-wine">{error}</p>}
        </form>
        <p className="mt-4 text-center text-xs text-ink/45">
          Access is restricted to Six &amp; Thriving administrators.
        </p>
      </div>
    </div>
  );
}
