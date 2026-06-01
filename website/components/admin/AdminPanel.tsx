'use client';

import { useCallback, useEffect, useState } from 'react';
import type { SupabaseClient } from '@supabase/supabase-js';

interface Contact {
  id: string;
  name: string;
  email: string;
  message: string;
  created_at: string;
  replied: boolean;
}

interface Testimonial {
  id: string;
  name: string;
  role: string | null;
  quote: string;
  rating: number;
  approved: boolean;
}

export default function AdminPanel({
  supabase,
  email,
}: {
  supabase: SupabaseClient;
  email: string;
}) {
  const [tab, setTab] = useState<'contacts' | 'testimonials'>('contacts');
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [testimonials, setTestimonials] = useState<Testimonial[]>([]);
  const [views, setViews] = useState<number>(0);
  const [subs, setSubs] = useState<number>(0);

  const load = useCallback(async () => {
    const [c, t, v] = await Promise.all([
      supabase.from('contacts').select('*').order('created_at', { ascending: false }),
      supabase.from('testimonials').select('*').order('created_at', { ascending: false }),
      supabase.from('blog_views').select('id', { count: 'exact', head: true }),
    ]);
    setContacts((c.data as Contact[]) ?? []);
    setTestimonials((t.data as Testimonial[]) ?? []);
    setViews(v.count ?? 0);
    setSubs(((c.data as Contact[]) ?? []).length);
  }, [supabase]);

  useEffect(() => {
    load();
  }, [load]);

  async function toggleApproved(id: string, approved: boolean) {
    await supabase.from('testimonials').update({ approved: !approved }).eq('id', id);
    load();
  }

  async function toggleReplied(id: string, replied: boolean) {
    await supabase.from('contacts').update({ replied: !replied }).eq('id', id);
    load();
  }

  return (
    <div className="mx-auto max-w-6xl px-5 py-12 sm:px-8 lg:px-12">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="font-serif text-4xl font-semibold text-wine2">Dashboard</h1>
          <p className="mt-1 text-sm text-ink/55">Signed in as {email}</p>
        </div>
        <button
          onClick={() => supabase.auth.signOut()}
          className="rounded-full border border-rose/20 px-5 py-2.5 text-xs font-extrabold uppercase tracking-[0.16em] text-wine transition hover:bg-blush2"
        >
          Sign out
        </button>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        <StatCard label="Contact messages" value={subs} />
        <StatCard label="Blog views" value={views} />
        <StatCard label="Testimonials" value={testimonials.length} />
      </div>

      <div className="mt-10 flex gap-2">
        <TabButton active={tab === 'contacts'} onClick={() => setTab('contacts')}>
          Contacts
        </TabButton>
        <TabButton active={tab === 'testimonials'} onClick={() => setTab('testimonials')}>
          Testimonials
        </TabButton>
      </div>

      <div className="mt-6 space-y-4">
        {tab === 'contacts' &&
          (contacts.length === 0 ? (
            <Empty>No contact messages yet.</Empty>
          ) : (
            contacts.map((c) => (
              <div key={c.id} className="rounded-2xl border border-rose/10 bg-white/85 p-6 shadow-card">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-serif text-lg font-semibold text-wine2">{c.name}</p>
                    <a href={`mailto:${c.email}`} className="text-sm text-wine hover:underline">
                      {c.email}
                    </a>
                  </div>
                  <button
                    onClick={() => toggleReplied(c.id, c.replied)}
                    className={`rounded-full px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.14em] ${
                      c.replied ? 'bg-blush2 text-cocoa' : 'bg-wine text-white'
                    }`}
                  >
                    {c.replied ? 'Replied' : 'Mark replied'}
                  </button>
                </div>
                <p className="mt-3 text-sm leading-7 text-ink/75">{c.message}</p>
                <p className="mt-3 text-xs text-ink/40">
                  {new Date(c.created_at).toLocaleString()}
                </p>
              </div>
            ))
          ))}

        {tab === 'testimonials' &&
          (testimonials.length === 0 ? (
            <Empty>No testimonials yet.</Empty>
          ) : (
            testimonials.map((t) => (
              <div key={t.id} className="rounded-2xl border border-rose/10 bg-white/85 p-6 shadow-card">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-serif text-lg font-semibold text-wine2">{t.name}</p>
                    {t.role && <p className="text-xs text-ink/55">{t.role}</p>}
                  </div>
                  <button
                    onClick={() => toggleApproved(t.id, t.approved)}
                    className={`rounded-full px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.14em] ${
                      t.approved ? 'bg-wine text-white' : 'bg-blush2 text-cocoa'
                    }`}
                  >
                    {t.approved ? 'Approved' : 'Approve'}
                  </button>
                </div>
                <p className="mt-3 text-sm leading-7 text-ink/75">“{t.quote}”</p>
              </div>
            ))
          ))}
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl border border-rose/10 bg-white/85 p-6 shadow-card">
      <p className="font-serif text-4xl font-semibold text-wine2">{value}</p>
      <p className="mt-1 text-xs font-medium uppercase tracking-[0.12em] text-cocoa/70">{label}</p>
    </div>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`rounded-full px-5 py-2.5 text-xs font-extrabold uppercase tracking-[0.16em] transition ${
        active ? 'bg-wine text-white shadow-soft' : 'border border-rose/20 text-wine hover:bg-blush2'
      }`}
    >
      {children}
    </button>
  );
}

function Empty({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-2xl border border-dashed border-rose/20 bg-white/50 p-12 text-center text-sm text-ink/50">
      {children}
    </div>
  );
}
