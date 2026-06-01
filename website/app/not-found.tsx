import Link from 'next/link';
import { ArrowRightIcon, HeartIcon } from '@/components/icons';

export default function NotFound() {
  return (
    <section className="soft-vignette flex min-h-[70vh] items-center justify-center px-5 py-20 text-center">
      <div className="max-w-md">
        <HeartIcon className="mx-auto h-10 w-10 text-rose" />
        <p className="mt-6 font-serif text-7xl font-semibold text-wine2">404</p>
        <h1 className="mt-3 font-serif text-3xl font-semibold text-wine2">
          This page is fast asleep
        </h1>
        <p className="mt-4 text-base leading-7 text-ink/70">
          We couldn’t find the page you were looking for. Let’s get you back to
          somewhere restful.
        </p>
        <Link
          href="/"
          className="btn-shine mt-8 inline-flex items-center gap-3 rounded-full bg-wine px-8 py-4 text-xs font-extrabold uppercase tracking-[0.16em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2"
        >
          Back home <ArrowRightIcon className="h-4 w-4" />
        </Link>
      </div>
    </section>
  );
}
