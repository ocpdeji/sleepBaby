import type { Metadata } from 'next';
import EmailSignupForm from '@/components/EmailSignupForm';
import { CheckCircleIcon, HeartIcon, MailIcon } from '@/components/icons';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Free Baby Sleep Cheat Sheet',
  description:
    'Download the free Baby Sleep Cheat Sheet — simple, practical fixes for better nights and calmer days. No spam, unsubscribe anytime.',
  alternates: { canonical: `${site.url}/free-sleep-guide` },
};

const insideItems = [
  'The awake windows table by age (birth to 24 months)',
  'The 3-Minute Pause — the simplest trick nobody told you',
  'A calm-down bedtime routine you can start tonight',
  'The 3 most common sleep mistakes (and easy fixes)',
  'What to do at 2am — a simple decision guide',
];

const afterSteps = [
  { title: 'Check your inbox', body: 'Your cheat sheet arrives within a minute or two.' },
  { title: 'Peek in Promotions / Spam', body: 'If you don’t see it, look there and drag it to Primary.' },
  { title: 'Start tonight', body: 'Pick one tip and try it at the next bedtime. Small wins add up.' },
];

export default function FreeSleepGuidePage() {
  return (
    <>
      <section className="soft-vignette">
        <div className="mx-auto grid max-w-7xl items-center gap-12 px-5 py-16 sm:px-8 lg:grid-cols-2 lg:px-12 lg:py-20">
          <div className="max-w-xl">
            <p className="inline-flex items-center gap-2 rounded-full bg-blush px-4 py-2 text-[11px] font-extrabold uppercase tracking-[0.18em] text-wine">
              <HeartIcon className="h-4 w-4 text-rose" /> Free download
            </p>
            <h1 className="mt-5 font-serif text-5xl font-semibold leading-[1.0] tracking-[-0.03em] text-wine2 sm:text-6xl">
              The Baby Sleep Cheat Sheet
            </h1>
            <p className="mt-6 text-lg leading-8 text-ink/80">
              Simple fixes for better nights and calmer days. The exact starting
              points I share with every exhausted parent — free, and yours in seconds.
            </p>
            <ul className="mt-8 space-y-3">
              {insideItems.map((item) => (
                <li key={item} className="flex items-start gap-3 text-[15px] text-ink/80">
                  <CheckCircleIcon className="mt-0.5 h-5 w-5 flex-shrink-0 text-rose" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-3xl border border-rose/10 bg-white/80 p-8 shadow-soft backdrop-blur">
            <h2 className="font-serif text-2xl font-semibold text-wine2">
              Where should we send it?
            </h2>
            <p className="mt-2 text-sm text-ink/65">
              Enter your details and we’ll email your cheat sheet right away.
            </p>
            <div className="mt-6">
              <EmailSignupForm source="free-sleep-guide" buttonLabel="Send my cheat sheet" />
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-5 py-16 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">
            What happens next
          </p>
          <h2 className="mt-3 font-serif text-4xl font-semibold tracking-[-0.03em] text-wine2 sm:text-5xl">
            After you sign up
          </h2>
        </div>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {afterSteps.map((s, i) => (
            <div
              key={s.title}
              className="rounded-3xl border border-rose/10 bg-white/85 p-8 text-center shadow-card backdrop-blur"
            >
              <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-blush2 font-serif text-xl font-semibold text-wine">
                {i + 1}
              </span>
              <h3 className="mt-4 font-serif text-xl font-semibold text-wine2">{s.title}</h3>
              <p className="mt-2 text-sm leading-7 text-ink/70">{s.body}</p>
            </div>
          ))}
        </div>
        <p className="mt-10 flex items-center justify-center gap-2 text-sm text-ink/55">
          <MailIcon className="h-5 w-5 text-rose" />
          Questions? Email {site.email}
        </p>
      </section>
    </>
  );
}
