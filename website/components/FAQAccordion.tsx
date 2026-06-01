'use client';

import { useState } from 'react';
import { ChevronDownIcon } from './icons';

export interface FAQItem {
  q: string;
  a: string;
}

export default function FAQAccordion({ items }: { items: FAQItem[] }) {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <div className="mx-auto max-w-3xl divide-y divide-rose/10 overflow-hidden rounded-3xl border border-rose/10 bg-white/85 shadow-card backdrop-blur">
      {items.map((item, i) => {
        const isOpen = open === i;
        return (
          <div key={item.q}>
            <button
              type="button"
              onClick={() => setOpen(isOpen ? null : i)}
              className="flex w-full items-center justify-between gap-4 px-6 py-5 text-left transition hover:bg-blush2/50"
              aria-expanded={isOpen}
            >
              <span className="font-serif text-lg font-semibold text-wine2">{item.q}</span>
              <ChevronDownIcon
                className={`h-5 w-5 flex-shrink-0 text-rose transition-transform duration-300 ${
                  isOpen ? 'rotate-180' : ''
                }`}
              />
            </button>
            <div
              className={`grid transition-all duration-300 ease-in-out ${
                isOpen ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'
              }`}
            >
              <div className="overflow-hidden">
                <p className="px-6 pb-6 text-sm leading-7 text-ink/75">{item.a}</p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
