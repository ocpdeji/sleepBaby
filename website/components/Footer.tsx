import Link from 'next/link';
import Logo from './Logo';
import EmailSignupForm from './EmailSignupForm';
import { site } from '@/lib/site';

const shopLinks = [
  { label: 'The Book', href: '/shop' },
  { label: 'Premium Bundle', href: '/shop' },
  { label: 'Toddler Kit', href: '/shop' },
  { label: 'Newborn Kit', href: '/shop' },
];

const exploreLinks = [
  { label: 'Blog', href: '/blog' },
  { label: 'About Kate', href: '/about' },
  { label: 'Free Sleep Guide', href: '/free-sleep-guide' },
  { label: 'Contact', href: '/contact' },
];

const legalLinks = [
  { label: 'Privacy Policy', href: '/privacy' },
  { label: 'Terms', href: '/terms' },
];

export default function Footer() {
  return (
    <footer className="relative z-10 mt-10 bg-wine2 text-blush">
      <div className="mx-auto grid max-w-7xl gap-12 px-5 py-16 sm:px-8 lg:grid-cols-[1.4fr_1fr_1fr_1.6fr] lg:px-12">
        <div>
          <Logo light />
          <p className="mt-5 max-w-xs text-sm leading-7 text-blush/75">
            Gentle, practical sleep support for babies, toddlers and the real
            parents loving them through the night.
          </p>
          <div className="mt-6 flex gap-3">
            <SocialLink href={site.social.instagram} label="Instagram">
              <path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Zm5-1.2a.9.9 0 1 0 0 1.8.9.9 0 0 0 0-1.8ZM4.5 8A3.5 3.5 0 0 1 8 4.5h8A3.5 3.5 0 0 1 19.5 8v8a3.5 3.5 0 0 1-3.5 3.5H8A3.5 3.5 0 0 1 4.5 16V8Z" />
            </SocialLink>
            <SocialLink href={site.social.facebook} label="Facebook">
              <path d="M13.5 21v-7h2.3l.4-2.8h-2.7V9.4c0-.8.3-1.4 1.5-1.4h1.3V5.5c-.6-.1-1.4-.2-2.2-.2-2.2 0-3.7 1.3-3.7 3.8v2.1H8.3V14h2.3v7h2.9Z" />
            </SocialLink>
            <SocialLink href={site.social.pinterest} label="Pinterest">
              <path d="M12 4.5a7.5 7.5 0 0 0-2.7 14.5c-.06-.6-.11-1.5.02-2.2l.9-3.8s-.23-.46-.23-1.14c0-1.07.62-1.87 1.39-1.87.65 0 .97.49.97 1.08 0 .66-.42 1.64-.64 2.55-.18.77.39 1.4 1.15 1.4 1.38 0 2.43-1.46 2.43-3.56 0-1.86-1.34-3.16-3.25-3.16-2.21 0-3.51 1.66-3.51 3.37 0 .67.26 1.38.58 1.77a.23.23 0 0 1 .05.22l-.22.88c-.03.14-.11.18-.26.11-1-.47-1.62-1.92-1.62-3.09 0-2.52 1.83-4.83 5.27-4.83 2.77 0 4.92 1.97 4.92 4.61 0 2.75-1.73 4.96-4.14 4.96-.81 0-1.57-.42-1.83-.92l-.5 1.9c-.18.69-.66 1.55-.98 2.08A7.5 7.5 0 1 0 12 4.5Z" />
            </SocialLink>
          </div>
        </div>

        <FooterCol title="Shop" links={shopLinks} />
        <FooterCol title="Explore" links={exploreLinks} />

        <div>
          <h3 className="text-xs font-extrabold uppercase tracking-[0.22em] text-blush">
            A better night, free
          </h3>
          <p className="mt-4 text-sm leading-7 text-blush/75">
            Join the newsletter and get the free Baby Sleep Cheat Sheet.
          </p>
          <div className="mt-5">
            <EmailSignupForm variant="footer" source="footer" />
          </div>
        </div>
      </div>

      <div className="border-t border-blush/15">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-5 py-6 text-xs text-blush/60 sm:flex-row sm:px-8 lg:px-12">
          <p>© {new Date().getFullYear()} Six &amp; Thriving. All rights reserved.</p>
          <div className="flex gap-6">
            {legalLinks.map((l) => (
              <Link key={l.href} href={l.href} className="transition hover:text-blush">
                {l.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}

function FooterCol({ title, links }: { title: string; links: { label: string; href: string }[] }) {
  return (
    <div>
      <h3 className="text-xs font-extrabold uppercase tracking-[0.22em] text-blush">{title}</h3>
      <ul className="mt-4 space-y-3 text-sm text-blush/75">
        {links.map((l) => (
          <li key={l.label}>
            <Link href={l.href} className="transition hover:text-blush">
              {l.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

function SocialLink({
  href,
  label,
  children,
}: {
  href: string;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={label}
      className="flex h-10 w-10 items-center justify-center rounded-full bg-blush/10 text-blush transition hover:bg-blush hover:text-wine2"
    >
      <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        {children}
      </svg>
    </a>
  );
}
