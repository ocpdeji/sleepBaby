import Link from 'next/link';
import { ArrowRightIcon, HeartIcon } from './icons';

export default function InlineCTA() {
  return (
    <div className="my-10 rounded-3xl border border-rose/15 bg-blush2/70 p-7 not-prose">
      <HeartIcon className="h-6 w-6 text-rose" />
      <p className="mt-3 font-serif text-2xl font-semibold leading-snug text-wine2">
        Want the simple fixes in one place?
      </p>
      <p className="mt-2 text-sm leading-7 text-ink/75">
        Grab the free Baby Sleep Cheat Sheet — the exact starting points I share with
        every exhausted parent. Yours in seconds.
      </p>
      <Link
        href="/free-sleep-guide"
        className="btn-shine mt-5 inline-flex items-center gap-2.5 rounded-full bg-wine px-7 py-3.5 text-xs font-extrabold uppercase tracking-[0.16em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2"
      >
        Get the free cheat sheet <ArrowRightIcon className="h-4 w-4" />
      </Link>
    </div>
  );
}
