'use client';

import { useEffect, useState } from 'react';

export interface TocItem {
  id: string;
  text: string;
  level: number;
}

export default function TableOfContents({ items }: { items: TocItem[] }) {
  const [active, setActive] = useState<string>('');

  useEffect(() => {
    if (items.length === 0) return;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setActive(entry.target.id);
        });
      },
      { rootMargin: '-80px 0px -70% 0px', threshold: 0.1 }
    );
    items.forEach((item) => {
      const el = document.getElementById(item.id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, [items]);

  if (items.length === 0) return null;

  return (
    <nav aria-label="Table of contents" className="text-sm">
      <p className="mb-4 text-[11px] font-extrabold uppercase tracking-[0.2em] text-rose">
        In this article
      </p>
      <ul className="space-y-2.5 border-l border-rose/15">
        {items.map((item) => (
          <li key={item.id} style={{ paddingLeft: item.level === 3 ? '1.5rem' : '1rem' }}>
            <a
              href={`#${item.id}`}
              className={`block border-l-2 -ml-px pl-3 transition ${
                active === item.id
                  ? 'border-rose font-semibold text-wine'
                  : 'border-transparent text-ink/60 hover:text-wine'
              }`}
            >
              {item.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
