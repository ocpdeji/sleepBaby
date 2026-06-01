-- ════════════════════════════════════════════════════════════
-- Six & Thriving — initial schema
-- Run in Supabase: SQL Editor → New query → paste → Run
-- ════════════════════════════════════════════════════════════

-- ── Contact form submissions ────────────────────────────────
create table if not exists public.contacts (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  email text not null,
  message text not null,
  created_at timestamptz default now(),
  replied boolean default false
);

-- ── Blog post analytics (page views) ────────────────────────
create table if not exists public.blog_views (
  id uuid default gen_random_uuid() primary key,
  slug text not null,
  viewed_at timestamptz default now(),
  country text
);
create index if not exists blog_views_slug_idx on public.blog_views (slug);

-- ── Waitlist for future products ────────────────────────────
create table if not exists public.waitlist (
  id uuid default gen_random_uuid() primary key,
  email text not null unique,
  product_interest text,
  created_at timestamptz default now()
);

-- ── Testimonials (managed from the dashboard) ───────────────
create table if not exists public.testimonials (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  role text,
  quote text not null,
  rating integer default 5,
  approved boolean default false,
  created_at timestamptz default now()
);

-- ════════════════════════════════════════════════════════════
-- Row Level Security
-- The website writes via the SERVICE ROLE key (server-side only),
-- which bypasses RLS. We enable RLS so nothing is publicly readable
-- or writable with the anon key, except approved testimonials.
-- ════════════════════════════════════════════════════════════

alter table public.contacts      enable row level security;
alter table public.blog_views    enable row level security;
alter table public.waitlist      enable row level security;
alter table public.testimonials  enable row level security;

-- Public can read ONLY approved testimonials (if you ever fetch them client-side).
drop policy if exists "approved testimonials are public" on public.testimonials;
create policy "approved testimonials are public"
  on public.testimonials for select
  using (approved = true);

-- Authenticated admins (logged-in Supabase Auth users) can read/manage everything.
drop policy if exists "admins manage contacts" on public.contacts;
create policy "admins manage contacts"
  on public.contacts for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

drop policy if exists "admins read views" on public.blog_views;
create policy "admins read views"
  on public.blog_views for select
  using (auth.role() = 'authenticated');

drop policy if exists "admins manage testimonials" on public.testimonials;
create policy "admins manage testimonials"
  on public.testimonials for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

drop policy if exists "admins manage waitlist" on public.waitlist;
create policy "admins manage waitlist"
  on public.waitlist for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

-- ════════════════════════════════════════════════════════════
-- Optional seed: a few starter testimonials (already approved)
-- ════════════════════════════════════════════════════════════
insert into public.testimonials (name, role, quote, rating, approved) values
  ('Sara',  'Mom of 2 · Toronto',        'Kate''s guidance was a total game changer for our family. We went from surviving to thriving.', 5, true),
  ('Megan', 'First-time mom · Calgary',  'I''d tried everything and given up twice. By night 6 my daughter slept through for the first time.', 5, true),
  ('Priya', 'Mom of twins · Vancouver',  'Finally a plan that didn''t pretend twins are the same as one baby. Worth every penny.', 5, true)
on conflict do nothing;
