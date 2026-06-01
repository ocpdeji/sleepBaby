'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Logo from './Logo';
import { site } from '@/lib/site';

export default function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  const isActive = (href: string) =>
    href === '/' ? pathname === '/' : pathname.startsWith(href);

  return (
    <header
      className={`sticky top-0 z-50 transition ${
        scrolled ? 'bg-cream/90 shadow-card backdrop-blur' : 'bg-transparent'
      }`}
    >
      <nav
        className="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8 lg:px-12"
        aria-label="Main navigation"
      >
        <Logo />

        <div className="hidden items-center gap-8 text-sm font-medium text-ink/80 lg:flex">
          {site.nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`relative transition hover:text-wine ${
                isActive(item.href)
                  ? 'text-rose after:absolute after:-bottom-2 after:left-0 after:h-px after:w-full after:bg-rose'
                  : ''
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>

        <Link
          href="/free-sleep-guide"
          className="btn-shine hidden rounded-full bg-wine px-7 py-3.5 text-xs font-extrabold uppercase tracking-[0.18em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2 md:inline-flex"
        >
          Free Sleep Guide
        </Link>

        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="inline-flex items-center justify-center rounded-lg p-2 text-wine2 lg:hidden"
          aria-label="Toggle menu"
          aria-expanded={open}
        >
          <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none">
            {open ? (
              <path d="m6 6 12 12M18 6 6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            ) : (
              <path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            )}
          </svg>
        </button>
      </nav>

      {open && (
        <div className="border-t border-rose/10 bg-cream/95 px-5 py-4 backdrop-blur lg:hidden">
          <div className="flex flex-col gap-1">
            {site.nav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-lg px-3 py-3 text-sm font-medium transition ${
                  isActive(item.href) ? 'bg-blush text-wine2' : 'text-ink/80 hover:bg-blush2'
                }`}
              >
                {item.label}
              </Link>
            ))}
            <Link
              href="/free-sleep-guide"
              className="mt-2 rounded-full bg-wine px-6 py-3.5 text-center text-xs font-extrabold uppercase tracking-[0.18em] text-white"
            >
              Free Sleep Guide
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
