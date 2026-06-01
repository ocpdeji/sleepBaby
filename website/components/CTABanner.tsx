import Link from 'next/link';
import { ArrowRightIcon, HeartIcon } from './icons';

interface Props {
  title?: string;
  subtitle?: string;
  buttonLabel?: string;
  href?: string;
}

export default function CTABanner({
  title = 'A better night could be just one tip away.',
  subtitle = 'Grab your free Baby Sleep Cheat Sheet and start tonight.',
  buttonLabel = 'Get the free cheat sheet',
  href = '/free-sleep-guide',
}: Props) {
  return (
    <section className="mx-auto max-w-7xl px-5 py-12 sm:px-8 lg:px-12">
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blush2 via-[#fbf1ec] to-blush p-8 text-center shadow-soft md:p-14">
        <div className="absolute -left-12 bottom-0 hidden h-64 w-64 rounded-full bg-white/40 blur-2xl md:block" />
        <div className="absolute -right-16 -top-16 h-56 w-56 rounded-full bg-white/50 blur-3xl" />
        <div className="relative mx-auto max-w-2xl">
          <HeartIcon className="mx-auto h-7 w-7 text-rose" />
          <h2 className="mt-4 font-serif text-3xl font-semibold leading-tight tracking-[-0.02em] text-wine2 sm:text-4xl">
            {title}
          </h2>
          <p className="mt-4 text-base leading-7 text-ink/75">{subtitle}</p>
          <Link
            href={href}
            className="btn-shine mt-7 inline-flex items-center justify-center gap-3 rounded-full bg-wine px-8 py-4 text-xs font-extrabold uppercase tracking-[0.16em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2"
          >
            {buttonLabel}
            <ArrowRightIcon className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </section>
  );
}
