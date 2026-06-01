'use client';

interface Props {
  url: string;
  title: string;
}

export default function ShareButtons({ url, title }: Props) {
  const encodedUrl = encodeURIComponent(url);
  const encodedTitle = encodeURIComponent(title);

  const links = [
    {
      label: 'Share on Facebook',
      href: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
      path: 'M13.5 21v-7h2.3l.4-2.8h-2.7V9.4c0-.8.3-1.4 1.5-1.4h1.3V5.5c-.6-.1-1.4-.2-2.2-.2-2.2 0-3.7 1.3-3.7 3.8v2.1H8.3V14h2.3v7h2.9Z',
    },
    {
      label: 'Share on Pinterest',
      href: `https://pinterest.com/pin/create/button/?url=${encodedUrl}&description=${encodedTitle}`,
      path: 'M12 4.5a7.5 7.5 0 0 0-2.7 14.5c-.06-.6-.11-1.5.02-2.2l.9-3.8s-.23-.46-.23-1.14c0-1.07.62-1.87 1.39-1.87.65 0 .97.49.97 1.08 0 .66-.42 1.64-.64 2.55-.18.77.39 1.4 1.15 1.4 1.38 0 2.43-1.46 2.43-3.56 0-1.86-1.34-3.16-3.25-3.16-2.21 0-3.51 1.66-3.51 3.37 0 .67.26 1.38.58 1.77a.23.23 0 0 1 .05.22l-.22.88c-.03.14-.11.18-.26.11-1-.47-1.62-1.92-1.62-3.09 0-2.52 1.83-4.83 5.27-4.83 2.77 0 4.92 1.97 4.92 4.61 0 2.75-1.73 4.96-4.14 4.96-.81 0-1.57-.42-1.83-.92l-.5 1.9c-.18.69-.66 1.55-.98 2.08A7.5 7.5 0 1 0 12 4.5Z',
    },
  ];

  return (
    <div className="flex items-center gap-3">
      <span className="text-xs font-extrabold uppercase tracking-[0.16em] text-cocoa">Share</span>
      {links.map((l) => (
        <a
          key={l.label}
          href={l.href}
          target="_blank"
          rel="noopener noreferrer"
          aria-label={l.label}
          className="flex h-9 w-9 items-center justify-center rounded-full bg-blush2 text-wine transition hover:bg-rose hover:text-white"
        >
          <svg className="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d={l.path} />
          </svg>
        </a>
      ))}
      <button
        type="button"
        onClick={() => navigator.clipboard?.writeText(url)}
        aria-label="Copy link"
        className="flex h-9 w-9 items-center justify-center rounded-full bg-blush2 text-wine transition hover:bg-rose hover:text-white"
      >
        <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M9 9h10v10H9zM5 15V5h10" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
    </div>
  );
}
