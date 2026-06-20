import Link from 'next/link';
import type { Metadata } from 'next';
import CTABanner from '@/components/CTABanner';
import { ArrowRightIcon, HeartIcon } from '@/components/icons';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: 'About Kate',
  description:
    'Meet Kate — mom of three and founder of Six & Thriving. Gentle, no cry-it-out, real-life sleep support for exhausted parents.',
  alternates: { canonical: `${site.url}/about` },
};

const philosophy = [
  {
    title: 'Gentle, never harsh',
    body: 'No baby is left to cry alone against your instincts. Every method in these books keeps connection at the centre.',
  },
  {
    title: 'Real life, real flexibility',
    body: 'Daycare, breastfeeding, single parenting, multiple kids — the plan flexes to your family instead of breaking your spirit.',
  },
  {
    title: 'A plan, not platitudes',
    body: 'Warm encouragement is lovely. But at 2am you need a night-by-night map. You get both.',
  },
];

export default function AboutPage() {
  return (
    <>
      <section className="soft-vignette">
        <div className="mx-auto grid max-w-7xl items-center gap-10 px-5 py-16 sm:px-8 lg:grid-cols-[0.42fr_0.58fr] lg:px-12 lg:py-20">
          <div className="mx-auto w-full max-w-[400px]">
            <div className="overflow-hidden rounded-t-full rounded-b-2xl bg-blush p-2.5 shadow-soft">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/images/kate.jpg"
                alt="Kate, founder of Six & Thriving"
                className="aspect-[0.82] w-full rounded-t-full rounded-b-xl object-cover"
              />
            </div>
          </div>
          <div className="max-w-2xl">
            <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
              Hi, I’m Kate
            </p>
            <h1 className="mt-3 font-serif text-5xl font-semibold leading-[1.02] tracking-[-0.03em] text-wine2 sm:text-6xl">
              Mom of 3. And the village it took to figure this out.
            </h1>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-prose px-5 py-12 sm:px-8">
        <div className="space-y-6 text-lg leading-8 text-ink/80">
          <p>
            I’ve been exactly where you are. Running on empty. Googling sleep advice
            at 2am while holding a baby who would not be put down. Patting, rocking,
            bouncing through songs I didn’t even know I remembered — and still, no
            sleep.
          </p>
          <p>
            I’m a mom of 3. But over the years I’ve also helped raise children
            across my extended family — nieces, nephews, cousins — navigating
            newborn nights, 4-month regressions, and toddler sleep battles across
            more households than I can count.
          </p>
          <p>Baby sleep has been the thread running through all of it.</p>
          <p>
            What I kept noticing, across every baby and every household, is that
            sleep isn’t random. It follows six predictable stages. And once you
            understand which stage you’re actually in — and what your baby
            genuinely needs at that stage — everything shifts.
          </p>
          <p>
            I’m not a sleep clinic. I don’t have a PhD. What I have is years of
            sitting with exhausted parents at 3am — sometimes in my own home,
            sometimes at a sister’s, sometimes on the phone talking a family member
            through a regression they were about to give up on.
          </p>
          <p>
            The desperation in those moments is the same no matter whose baby it is.
          </p>
          <p>
            I wrote <em>Sleep, Baby. Please.</em> for the parent who has already
            Googled everything, tried one thing, watched it fail on Night 3, and
            needs an honest, warm, practical plan that meets them where they
            actually are.
          </p>
          <p>At 2am. In the dark. Wondering if it ever gets better.</p>
          <p>It does. And I’m here to help you get there faster.</p>
          <blockquote className="rounded-2xl border-l-4 border-rose bg-blush2 px-6 py-5 font-serif text-2xl italic text-cocoa">
            “Every single baby I’ve helped through this eventually slept. Every
            single one. And none of them were easy. Yours can too.”
            <footer className="mt-3 text-base font-sans not-italic font-semibold text-rose">
              — Kate, Six &amp; Thriving
            </footer>
          </blockquote>
        </div>
      </section>

      <section className="bg-blush2/40 py-16">
        <div className="mx-auto max-w-7xl px-5 sm:px-8 lg:px-12">
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
              My philosophy
            </p>
            <h2 className="mt-3 font-serif text-4xl font-semibold tracking-[-0.03em] text-wine2 sm:text-5xl">
              Gentle. Flexible. Honest.
            </h2>
          </div>
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {philosophy.map((p) => (
              <div
                key={p.title}
                className="rounded-3xl border border-rose/10 bg-white/85 p-8 shadow-card backdrop-blur"
              >
                <HeartIcon className="h-7 w-7 text-rose" />
                <h3 className="mt-4 font-serif text-2xl font-semibold text-wine2">{p.title}</h3>
                <p className="mt-3 text-sm leading-7 text-ink/70">{p.body}</p>
              </div>
            ))}
          </div>
          <div className="mt-12 text-center">
            <Link
              href="/shop"
              className="btn-shine inline-flex items-center gap-3 rounded-full bg-wine px-8 py-4 text-xs font-extrabold uppercase tracking-[0.16em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2"
            >
              See the books <ArrowRightIcon className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      <CTABanner />
    </>
  );
}
