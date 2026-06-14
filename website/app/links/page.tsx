import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Six & Thriving | Links',
  description: 'Helping exhausted moms finally get some sleep. Free guides, sleep tips, and the Sleep, Baby. Please. eBook.',
};

const mainLinks = [
  {
    emoji: '🌙',
    label: 'Free Baby Sleep Cheat Sheet',
    sublabel: 'Instant download — no fluff, just what works',
    href: 'https://sixandthriving.com/free-sleep-guide',
    highlight: true,
  },
  {
    emoji: '📖',
    label: 'Sleep, Baby. Please.',
    sublabel: 'The 7-night plan — $19.99',
    href: 'https://sixandthriving.com/shop',
    highlight: false,
  },
  {
    emoji: '⏰',
    label: 'Wake Windows by Age — Complete Guide',
    sublabel: 'Birth to 24 months, every stage covered',
    href: 'https://sixandthriving.com/blog/wake-windows-by-age',
    highlight: false,
  },
  {
    emoji: '😴',
    label: '4-Month Sleep Regression Help',
    sublabel: 'Your baby didn\'t break. Here\'s what happened.',
    href: 'https://sixandthriving.com/blog/4-month-sleep-regression',
    highlight: false,
  },
  {
    emoji: '⏸️',
    label: 'The 5-Minute Pause Method',
    sublabel: 'The simplest trick nobody told you',
    href: 'https://sixandthriving.com/blog/5-minute-pause-sleep-trick',
    highlight: false,
  },
  {
    emoji: '🌐',
    label: 'Visit Six & Thriving',
    sublabel: 'Real support for real parents',
    href: 'https://sixandthriving.com',
    highlight: false,
  },
];

const socialLinks = [
  {
    label: 'Instagram',
    href: 'https://www.instagram.com/sixandthrivingmom/',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
      </svg>
    ),
  },
  {
    label: 'Pinterest',
    href: 'https://pinterest.ca/SixAndThriving',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M12 0C5.373 0 0 5.373 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 01.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.632-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0z"/>
      </svg>
    ),
  },
  {
    label: 'TikTok',
    href: 'https://tiktok.com/@sixandthrivin',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/>
      </svg>
    ),
  },
  {
    label: 'YouTube',
    href: 'https://youtube.com/channel/UC97cj6E8VGuXfZ0JDzQrDSA',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
      </svg>
    ),
  },
  {
    label: 'Facebook',
    href: 'https://www.facebook.com/profile.php?id=61590580810773',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
      </svg>
    ),
  },
  {
    label: 'Threads',
    href: 'https://www.threads.com/@sixandthrivingmom',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 013.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.583-1.314-.884-2.371-.899h-.005c-.829 0-1.934.226-2.64 1.149l-1.688-1.239c.903-1.229 2.28-1.913 3.854-1.924.083 0 .166 0 .249.002 1.65.044 2.95.578 3.862 1.587.996 1.104 1.44 2.71 1.32 4.776.082.045.163.091.243.138 1.156.695 1.982 1.647 2.39 2.55.75 1.713.718 4.469-1.587 6.701C17.04 23.24 14.793 23.98 12.186 24zm-3.071-8.757c.071 1.285 1.236 2.037 3.196 1.928 1.139-.062 1.997-.467 2.549-1.202.442-.588.698-1.382.762-2.364a11.765 11.765 0 00-2.656-.208c-.983.057-1.8.307-2.353.725-.522.394-.524.882-.498 1.121z"/>
      </svg>
    ),
  },
  {
    label: 'X / Twitter',
    href: 'https://x.com/SixAndThriving',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.747l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
      </svg>
    ),
  },
  {
    label: 'Bluesky',
    href: 'https://bsky.app/profile/sixandthriving.bsky.social',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
        <path d="M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 01-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.204-.659-.299-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8z"/>
      </svg>
    ),
  },
];

export default function LinksPage() {
  return (
    <main className="min-h-screen bg-cream flex flex-col items-center px-4 py-12 pb-20">

      {/* ── HEADER ── */}
      <div className="flex flex-col items-center mb-10 text-center">
        {/* Logo mark */}
        <div className="mb-4 relative">
          <div className="w-20 h-20 rounded-full bg-wine/10 flex items-center justify-center border-2 border-wine/20">
            <span className="text-3xl">🌙</span>
          </div>
        </div>

        <h1 className="font-serif text-2xl font-bold text-wine2 mb-1 tracking-tight">
          Six & Thriving
        </h1>
        <p className="text-sm text-ink/60 font-medium max-w-xs leading-relaxed">
          Helping exhausted moms finally get some sleep
        </p>

        {/* Mom of 6 badge */}
        <div className="mt-3 inline-flex items-center gap-1.5 bg-wine/8 border border-wine/15 rounded-full px-3 py-1">
          <span className="text-xs font-semibold text-wine2 tracking-wide">
            Mom of 6 · Yes, twins too 👶👶
          </span>
        </div>
      </div>

      {/* ── MAIN LINKS ── */}
      <div className="w-full max-w-sm flex flex-col gap-3 mb-8">
        {mainLinks.map((link) => (
          <a
            key={link.href}
            href={link.href}
            target={link.href.startsWith('https://sixandthriving.com') ? '_self' : '_blank'}
            rel="noopener noreferrer"
            className={`
              group flex items-center gap-4 w-full rounded-2xl px-5 py-4
              transition-all duration-200 hover:-translate-y-0.5
              ${link.highlight
                ? 'bg-wine text-white shadow-lg hover:bg-wine2 hover:shadow-xl'
                : 'bg-white border border-wine/10 text-ink hover:border-wine/30 hover:shadow-md shadow-sm'
              }
            `}
          >
            <span className="text-xl flex-shrink-0">{link.emoji}</span>
            <div className="flex-1 text-left min-w-0">
              <div className={`text-sm font-bold leading-tight truncate ${link.highlight ? 'text-white' : 'text-ink'}`}>
                {link.label}
              </div>
              <div className={`text-xs mt-0.5 truncate ${link.highlight ? 'text-white/75' : 'text-ink/50'}`}>
                {link.sublabel}
              </div>
            </div>
            <svg
              className={`w-4 h-4 flex-shrink-0 transition-transform group-hover:translate-x-0.5 ${link.highlight ? 'text-white/70' : 'text-ink/30'}`}
              fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        ))}
      </div>

      {/* ── DIVIDER ── */}
      <div className="w-full max-w-sm flex items-center gap-3 mb-6">
        <div className="flex-1 h-px bg-wine/10" />
        <span className="text-xs font-semibold text-ink/30 uppercase tracking-widest">Find me here</span>
        <div className="flex-1 h-px bg-wine/10" />
      </div>

      {/* ── SOCIAL ICONS ── */}
      <div className="flex flex-wrap justify-center gap-3 max-w-sm mb-10">
        {socialLinks.map((s) => (
          <a
            key={s.href}
            href={s.href}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={s.label}
            className="w-11 h-11 rounded-full bg-white border border-wine/10 flex items-center justify-center text-wine/60 hover:text-wine hover:border-wine/30 hover:shadow-md transition-all duration-200 shadow-sm"
          >
            {s.icon}
          </a>
        ))}
      </div>

      {/* ── FOOTER ── */}
      <div className="text-center">
        <p className="text-xs text-ink/30 font-medium">
          © Six & Thriving · Real support for real parents
        </p>
        <a
          href="https://sixandthriving.com"
          className="text-xs text-wine/40 hover:text-wine/70 transition-colors mt-1 inline-block"
        >
          sixandthriving.com
        </a>
      </div>

    </main>
  );
}
