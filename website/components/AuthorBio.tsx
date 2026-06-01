import Link from 'next/link';
import { HeartIcon } from './icons';
import SafeImage from './SafeImage';

export default function AuthorBio() {
  return (
    <aside className="my-12 flex flex-col gap-6 rounded-3xl border border-rose/10 bg-blush2/60 p-7 shadow-card sm:flex-row sm:items-center">
      <div className="mx-auto h-24 w-24 flex-shrink-0 overflow-hidden rounded-full bg-blush ring-2 ring-rose/20 sm:mx-0">
        <SafeImage
          src="/images/kate.jpg"
          alt="Kate, founder of Six & Thriving"
          className="h-full w-full object-cover"
        />
      </div>
      <div>
        <p className="text-[11px] font-extrabold uppercase tracking-[0.2em] text-rose">
          Written by
        </p>
        <h3 className="mt-1 font-serif text-2xl font-semibold text-wine2">Kate</h3>
        <p className="mt-2 text-sm leading-7 text-ink/75">
          Mom of six (including twins) and the founder of Six &amp; Thriving. I write
          for the parent who has already Googled everything — warm, honest, practical
          help that meets you where you are. At 2am. In the dark.
        </p>
        <Link
          href="/about"
          className="mt-3 inline-flex items-center gap-2 text-sm font-semibold text-wine transition hover:text-rose"
        >
          <HeartIcon className="h-4 w-4" /> More about Kate
        </Link>
      </div>
    </aside>
  );
}
