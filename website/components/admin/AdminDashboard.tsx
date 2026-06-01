'use client';

import { useEffect, useMemo, useState } from 'react';
import type { Session, SupabaseClient } from '@supabase/supabase-js';
import { createBrowserClient, isSupabaseConfigured } from '@/lib/supabase';
import AdminLogin from './AdminLogin';
import AdminPanel from './AdminPanel';

export default function AdminDashboard() {
  const supabase = useMemo<SupabaseClient | null>(
    () => (isSupabaseConfigured ? createBrowserClient() : null),
    []
  );
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!supabase) {
      setLoading(false);
      return;
    }
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      setLoading(false);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => setSession(s));
    return () => sub.subscription.unsubscribe();
  }, [supabase]);

  if (!supabase) {
    return (
      <div className="mx-auto max-w-md px-5 py-24 text-center">
        <h1 className="font-serif text-3xl font-semibold text-wine2">Admin not configured</h1>
        <p className="mt-3 text-sm text-ink/65">
          Add your Supabase environment variables to enable the dashboard.
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-rose/30 border-t-rose" />
      </div>
    );
  }

  if (!session) {
    return <AdminLogin supabase={supabase} />;
  }

  return <AdminPanel supabase={supabase} email={session.user.email ?? ''} />;
}
