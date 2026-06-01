# Six & Thriving — Website

A production-ready **Next.js 14** website for the *Sleep, Baby. Please.* digital book
business. Built with the App Router, Tailwind CSS, Supabase, MailerLite, and an MDX blog.
Payments are handled by Payhip (Stripe + PayPal already connected).

---

## ✨ What's inside

| Area | Details |
| --- | --- |
| **Framework** | Next.js 14 (App Router), TypeScript, React Server Components |
| **Styling** | Tailwind CSS — brand palette baked in (burgundy / wine / blush / cream / rose) |
| **Blog** | MDX files in `content/blog` — 5 SEO articles included, auto TOC + reading time |
| **Email** | MailerLite API v2 via `/api/subscribe` (server-side, key never exposed) |
| **Database** | Supabase — contacts, blog views, waitlist, testimonials (SQL migration included) |
| **Auth** | Supabase Auth protects the `/admin` dashboard |
| **Payments** | Payhip embedded checkout (no Stripe code needed yet) |
| **SEO** | Per-page metadata, Open Graph, JSON-LD article schema, `sitemap.xml`, `robots.txt` |
| **Analytics** | Plausible (privacy-friendly) + anonymous Supabase blog view counts |

---

## 📁 Project structure

```
website/
├── app/
│   ├── layout.tsx              # Root layout: fonts, navbar, footer, analytics
│   ├── page.tsx                # Home
│   ├── globals.css             # Tailwind + editorial prose styles
│   ├── shop/page.tsx
│   ├── about/page.tsx
│   ├── free-sleep-guide/page.tsx
│   ├── contact/page.tsx
│   ├── privacy/page.tsx
│   ├── terms/page.tsx
│   ├── blog/
│   │   ├── page.tsx            # Blog list
│   │   └── [slug]/page.tsx     # Blog post (MDX + TOC + related)
│   ├── admin/page.tsx          # Protected dashboard
│   ├── api/
│   │   ├── subscribe/route.ts  # MailerLite signup
│   │   ├── contact/route.ts    # Contact form → Supabase + MailerLite
│   │   └── views/route.ts      # Blog view tracking
│   ├── sitemap.ts
│   ├── robots.ts
│   └── not-found.tsx
├── components/                 # 10+ reusable components (see below)
├── content/blog/               # 5 MDX articles
├── lib/                        # products, blog loader, supabase, mailerlite, site config
├── supabase/migrations/        # SQL schema + RLS policies
├── public/images/              # Add product covers + photos here
├── .env.example
└── README.md
```

**Components:** Navbar, Footer, ProductCard, BlogCard, TestimonialCard, EmailSignupForm,
FAQAccordion, CTABanner, AuthorBio, TableOfContents — plus ContactForm, ShareButtons,
InlineCTA, BlogViewTracker, and the admin set.

---

## 🚀 Local setup

```bash
cd website
npm install
cp .env.example .env.local   # then fill in your real values
npm run dev
```

Open <http://localhost:3000>.

> The site runs without any env vars — forms and the dashboard simply stay in a graceful
> "not configured" state until you add keys.

---

## 🔑 Environment variables

Copy `.env.example` → `.env.local` and fill in:

| Variable | Where to find it |
| --- | --- |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase → Project Settings → API → Project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase → Project Settings → API → `anon` `public` key |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase → Project Settings → API → `service_role` key (**secret**) |
| `MAILERLITE_API_KEY` | MailerLite → Integrations → API → generate token |
| `MAILERLITE_CHEATSHEET_GROUP_ID` | MailerLite → Subscribers → Groups → open group → ID in URL |
| `MAILERLITE_WEBSITE_GROUP_ID` | Same, for your "Website Subscribers" group |
| `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` | `sixandthriving.com` |
| `NEXT_PUBLIC_SITE_URL` | `https://www.sixandthriving.com` |

> ⚠️ Never commit `.env.local`. Only `.env.example` (with placeholders) is tracked.

---

## 🗄️ Supabase setup

1. Create a project at [supabase.com](https://supabase.com).
2. Open **SQL Editor → New query**, paste the contents of
   `supabase/migrations/0001_init.sql`, and **Run**. This creates the four tables,
   enables Row Level Security, and seeds three starter testimonials.
3. Create your admin login: **Authentication → Users → Add user** (email + password).
   That account is what you'll use at `/admin`.
4. Copy the three Supabase keys into your env vars.

**Security model:** the website writes via the `service_role` key on the server only
(API routes), which bypasses RLS. The browser `anon` key can read only *approved*
testimonials. The `/admin` dashboard requires a logged-in Supabase Auth user.

---

## 📧 MailerLite setup

1. **Integrations → API** → generate a token → set `MAILERLITE_API_KEY`.
2. Create two groups — e.g. *Cheat Sheet Subscribers* and *Website Subscribers* —
   and copy their IDs into the env vars.
3. (Optional) In MailerLite, build an **automation** triggered by joining the cheat-sheet
   group that emails the free PDF. The site adds the subscriber; MailerLite delivers.

The `/api/subscribe` route routes cheat-sheet signups to the cheat-sheet group and all
other signups to the website group automatically.

---

## 🛍️ Products

All product data lives in **`lib/products.ts`** — the single source of truth for the
Home and Shop pages. To change a price, title, or Payhip link, edit that file.

Each `ProductCard` uses Payhip's embedded checkout (`payhip-buy-button` + `data-product`),
so checkout opens in an overlay without leaving the site. Stripe and PayPal both appear
automatically because they're connected on the Payhip side — no code changes needed.

---

## ✍️ Adding a blog post

1. Create `content/blog/your-slug.mdx`.
2. Add front-matter:

```mdx
---
title: "Your Post Title"
excerpt: "One-sentence summary for cards and SEO."
date: "2026-06-01"
category: "Sleep Training"   # or Newborns | Toddlers | Real Talk
cover: "https://...jpg"      # or /images/blog/your-cover.jpg
keywords: ["keyword one", "keyword two"]
---

Write in Markdown. Drop `<InlineCTA />` anywhere to insert the cheat-sheet promo.
```

3. Save. The post is picked up automatically — list page, TOC, reading time, related
   posts, sitemap, and SEO schema all update with no extra work.

---

## 🖼️ Images

Add these to `public/images/` (cards degrade gracefully if missing):

- `products/book.jpg`, `products/bundle.jpg`, `products/toddler.jpg`, `products/newborn.jpg`
- `kate.jpg` — author photo
- `og-default.jpg` — 1200×630 social share image
- `blog/*.jpg` — optional local blog covers (the included posts use Unsplash URLs)

You can reuse the existing covers from the parent project (`payhip_01_bundle_stack.png`,
the ebook cover JPG, etc.).

---

## ☁️ Deploy to Netlify

You're already on Netlify — this is the simplest path.

1. Push the `website/` folder to a Git repo (GitHub/GitLab).
2. At [app.netlify.com](https://app.netlify.com) → **Add new site → Import an existing project** → connect your repo.
   - **Base directory:** `website` (if the repo root is the parent folder)
   - **Build command:** `npm run build` (auto-detected from `netlify.toml`)
   - **Publish directory:** `.next` (auto-detected)
3. **Environment Variables:** Site settings → Environment variables → add every variable from `.env.example` with real values.
4. **Deploy.** Netlify installs `@netlify/plugin-nextjs` automatically from `netlify.toml`.
5. **Domain:** Site settings → Domain management → add `sixandthriving.com` and `www.sixandthriving.com`. Point your DNS as Netlify instructs (usually an `A` record to Netlify's load balancer IP and a `CNAME` for `www`).

After the domain is live, submit `https://www.sixandthriving.com/sitemap.xml` to Google Search Console.

> **Why Netlify works:** The `@netlify/plugin-nextjs` package handles Next.js 14 App Router, Server Components, API routes, and ISR — everything this site uses. No Vercel required.

---

## ✅ Pre-launch checklist

- [ ] Supabase migration run + admin user created
- [ ] All env vars set in Vercel
- [ ] Product images added to `public/images/products/`
- [ ] Author photo + OG image added
- [ ] Test the cheat-sheet form (check MailerLite for the new subscriber)
- [ ] Test the contact form (check the Supabase `contacts` table + `/admin`)
- [ ] Test a Payhip buy button (overlay opens, Stripe + PayPal show)
- [ ] Custom domain connected + SSL active
- [ ] Sitemap submitted to Google Search Console

---

*Sleep is coming. For both of you.* — Six & Thriving
