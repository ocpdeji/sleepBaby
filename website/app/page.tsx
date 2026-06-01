import Link from 'next/link';
import type { Metadata } from 'next';
import ProductCard from '@/components/ProductCard';
import TestimonialCard from '@/components/TestimonialCard';
import FAQAccordion from '@/components/FAQAccordion';
import EmailSignupForm from '@/components/EmailSignupForm';
import { ArrowRightIcon, CheckCircleIcon, HeartIcon } from '@/components/icons';
import { products } from '@/lib/products';
import { testimonials, homeFaqs, howItWorks } from '@/lib/content';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: `${site.name} | ${site.tagline}`,
  description: site.description,
  alternates: { canonical: site.url },
};

export default function HomePage() {
  return (
    <>
      {/* ───────── HERO ───────── */}
      <section className="soft-vignette relative">
        <div className="mx-auto grid max-w-7xl items-center gap-8 px-5 pb-10 pt-6 sm:px-8 md:min-h-[640px] lg:grid-cols-[0.94fr_1.06fr] lg:px-12">
          <div className="relative z-10 max-w-2xl animate-fade-up">
            <h1 className="font-serif text-5xl font-semibold leading-[0.96] tracking-[-0.04em] text-wine2 sm:text-6xl lg:text-7xl">
              You’re not failing.
              <span className="block pt-2 italic text-rose">You’re just exhausted.</span>
            </h1>
            <HeartIcon className="my-7 h-6 w-6 text-rose" />
            <p className="max-w-xl text-lg leading-8 text-ink/80">
              Gentle, practical sleep support for babies and toddlers — designed for
              real life and real parents.
            </p>
            <div className="mt-9 flex flex-col gap-4 sm:flex-row sm:items-center">
              <Link
                href="/free-sleep-guide"
                className="btn-shine inline-flex items-center justify-center gap-3 rounded-full bg-wine px-8 py-5 text-xs font-extrabold uppercase tracking-[0.14em] text-white shadow-soft transition hover:-translate-y-1 hover:bg-wine2"
              >
                Get your free sleep cheat sheet
                <ArrowRightIcon className="h-4 w-4" />
              </Link>
              <Link
                href="/shop"
                className="inline-flex items-center justify-center gap-2 rounded-full border border-rose/30 px-7 py-5 text-xs font-extrabold uppercase tracking-[0.14em] text-wine transition hover:border-rose hover:bg-blush2"
              >
                Shop the books
              </Link>
            </div>
            <p className="mt-5 inline-flex items-center gap-2 text-xs font-medium text-ink/55">
              <CheckCircleIcon className="h-5 w-5 text-rose" />
              No spam. Unsubscribe anytime.
            </p>
          </div>

          <div className="relative min-h-[360px] animate-fade-in md:min-h-[540px] lg:min-h-[640px]">
            <div className="absolute inset-x-[-1.25rem] bottom-0 top-0 overflow-hidden rounded-[2rem] lg:-right-12 lg:left-[-8%] lg:rounded-none">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/images/hero.jpg"
                alt="Gentle sleep support for real families — Six & Thriving"
                className="h-full w-full object-cover object-center opacity-95"
              />
              <div className="absolute inset-0 bg-gradient-to-r from-cream via-cream/35 to-transparent lg:from-cream lg:via-cream/10" />
              <div className="absolute inset-0 bg-gradient-to-t from-cream via-transparent to-transparent" />
            </div>
            <div className="animate-float-badge absolute bottom-8 right-4 z-10 flex h-32 w-32 items-center justify-center rounded-full bg-rose text-center text-white shadow-soft sm:bottom-14 sm:right-8 sm:h-40 sm:w-40">
              <div>
                <HeartIcon className="mx-auto mb-2 h-5 w-5" />
                <p className="text-[11px] font-extrabold uppercase leading-4 tracking-[0.16em]">
                  Sleep
                  <br />
                  is possible.
                  <br />
                  You deserve
                  <br />
                  it too.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ───────── SOCIAL PROOF BAR ───────── */}
      <section className="border-y border-rose/10 bg-blush2/60">
        <div className="mx-auto grid max-w-7xl grid-cols-2 gap-6 px-5 py-8 text-center sm:px-8 md:grid-cols-4 lg:px-12">
          <Stat value="1,000+" label="Exhausted parents helped" />
          <Stat value="7 nights" label="To the breakthrough" />
          <Stat value="6 babies" label="Tested across (incl. twins)" />
          <Stat value="30 days" label="Money-back guarantee" />
        </div>
      </section>

      {/* ───────── HOW IT WORKS ───────── */}
      <section className="mx-auto max-w-7xl px-5 py-16 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
            How it works
          </p>
          <h2 className="mt-3 font-serif text-4xl font-semibold tracking-[-0.03em] text-wine2 sm:text-5xl">
            Three steps to calmer nights
          </h2>
        </div>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {howItWorks.map((s) => (
            <div
              key={s.step}
              className="relative rounded-3xl border border-rose/10 bg-white/85 p-8 shadow-card backdrop-blur transition hover:-translate-y-1 hover:shadow-soft"
            >
              <span className="font-serif text-5xl font-semibold text-blush">{s.step}</span>
              <h3 className="mt-4 font-serif text-2xl font-semibold text-wine2">{s.title}</h3>
              <p className="mt-3 text-sm leading-7 text-ink/70">{s.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ───────── PRODUCTS PREVIEW ───────── */}
      <section className="bg-blush2/40 py-16">
        <div className="mx-auto max-w-7xl px-5 sm:px-8 lg:px-12">
          <div className="flex flex-col items-end justify-between gap-4 sm:flex-row">
            <div className="max-w-xl">
              <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
                The books
              </p>
              <h2 className="mt-3 font-serif text-4xl font-semibold tracking-[-0.03em] text-wine2 sm:text-5xl">
                Pick the plan that fits your family
              </h2>
            </div>
            <Link
              href="/shop"
              className="inline-flex items-center gap-2 text-sm font-semibold text-wine transition hover:text-rose"
            >
              View all <ArrowRightIcon className="h-4 w-4" />
            </Link>
          </div>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {products.map((product) => (
              <ProductCard key={product.slug} product={product} />
            ))}
          </div>
        </div>
      </section>

      {/* ───────── TESTIMONIALS ───────── */}
      <section className="mx-auto max-w-7xl px-5 py-16 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
            Real families
          </p>
          <h2 className="mt-3 font-serif text-4xl font-semibold tracking-[-0.03em] text-wine2 sm:text-5xl">
            From surviving to thriving
          </h2>
        </div>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {testimonials.map((t) => (
            <TestimonialCard key={t.name} testimonial={t} />
          ))}
        </div>
      </section>

      {/* ───────── ABOUT KATE PREVIEW ───────── */}
      <section className="bg-blush2/40 py-16">
        <div className="mx-auto grid max-w-7xl items-center gap-10 px-5 sm:px-8 lg:grid-cols-[0.4fr_0.6fr] lg:px-12">
          <div className="mx-auto w-full max-w-[360px]">
            <div className="overflow-hidden rounded-t-full rounded-b-xl bg-blush p-2 shadow-card">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/images/kate.jpg"
                alt="Kate, baby sleep support specialist and founder of Six & Thriving"
                className="aspect-[0.82] w-full rounded-t-full rounded-b-lg object-cover"
              />
            </div>
          </div>
          <div className="max-w-xl">
            <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
              Meet Kate
            </p>
            <h2 className="mt-3 font-serif text-4xl font-semibold tracking-[-0.03em] text-wine2 sm:text-5xl">
              Mom of six. Including twins.
            </h2>
            <div className="mt-6 space-y-4 text-base leading-8 text-ink/80">
              <p>
                I’ve been where you are — running on empty, googling at 2am, wondering
                if it will ever get better. After years of trial, error and a lot of
                coffee, I learned what actually works.
              </p>
              <p>
                Now I help overwhelmed parents create calmer nights and happier days —
                without the guilt or the judgment.
              </p>
            </div>
            <Link
              href="/about"
              className="btn-shine mt-7 inline-flex items-center gap-2 rounded-full bg-wine px-8 py-4 text-xs font-extrabold uppercase tracking-[0.16em] text-white shadow-card transition hover:-translate-y-0.5 hover:bg-wine2"
            >
              Read my story <ArrowRightIcon className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* ───────── EMAIL SIGNUP ───────── */}
      <section id="cheatsheet" className="mx-auto max-w-7xl px-5 py-16 sm:px-8 lg:px-12">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blush2 via-[#fbf1ec] to-blush p-8 shadow-soft md:p-12">
          <div className="absolute -right-16 -top-16 h-56 w-56 rounded-full bg-white/50 blur-3xl" />
          <div className="relative grid items-center gap-10 lg:grid-cols-2">
            <div>
              <h2 className="font-serif text-4xl font-semibold leading-tight tracking-[-0.03em] text-wine2 sm:text-5xl">
                A better night could be just one tip away.
              </h2>
              <p className="mt-5 text-base leading-7 text-ink/75">
                Grab your free Baby Sleep Cheat Sheet and start tonight. Short.
                Practical. Mom-approved.
              </p>
              <p className="mt-5 inline-flex items-center gap-2 text-sm font-medium text-cocoa">
                <HeartIcon className="h-5 w-5 text-rose" />
                Join 1,000+ parents getting gentle sleep support.
              </p>
            </div>
            <div className="rounded-2xl bg-white/70 p-6 shadow-card backdrop-blur">
              <EmailSignupForm source="home-cheatsheet" />
            </div>
          </div>
        </div>
      </section>

      {/* ───────── FAQ ───────── */}
      <section className="mx-auto max-w-7xl px-5 pb-20 sm:px-8 lg:px-12">
        <div className="mx-auto mb-12 max-w-2xl text-center">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
            Questions
          </p>
          <h2 className="mt-3 font-serif text-4xl font-semibold tracking-[-0.03em] text-wine2 sm:text-5xl">
            The things parents ask first
          </h2>
        </div>
        <FAQAccordion items={homeFaqs} />
      </section>
    </>
  );
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div>
      <p className="font-serif text-3xl font-semibold text-wine2 sm:text-4xl">{value}</p>
      <p className="mt-1 text-xs font-medium uppercase tracking-[0.12em] text-cocoa/70">{label}</p>
    </div>
  );
}
