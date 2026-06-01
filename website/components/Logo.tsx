import Link from 'next/link';

export default function Logo({ light = false }: { light?: boolean }) {
  return (
    <Link
      href="/"
      className="group inline-flex flex-col leading-none"
      aria-label="Six and Thriving home"
    >
      <span className={`relative mb-1 h-5 w-12 ${light ? 'text-blush' : 'text-rose'}`}>
        <svg viewBox="0 0 110 40" fill="none" className="h-full w-full" aria-hidden="true">
          <path d="M9 30C29 14 49 9 75 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          <path d="M31 16C25 7 17 5 8 8C14 18 21 22 31 16Z" stroke="currentColor" strokeWidth="2" />
          <path d="M53 12C47 3 38 1 29 5C36 15 43 18 53 12Z" stroke="currentColor" strokeWidth="2" />
          <path d="M75 15C69 5 60 3 51 7C58 17 66 21 75 15Z" stroke="currentColor" strokeWidth="2" />
        </svg>
      </span>
      <span
        className={`font-serif text-2xl font-semibold tracking-tight ${
          light ? 'text-cream' : 'text-wine2'
        } sm:text-[1.7rem]`}
      >
        Six &amp; Thriving
      </span>
      <span
        className={`mt-1 text-[9px] font-bold uppercase tracking-[0.28em] ${
          light ? 'text-blush/70' : 'text-cocoa/70'
        }`}
      >
        Real support for real parents
      </span>
    </Link>
  );
}
