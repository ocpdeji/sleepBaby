'use client';

import { useEffect } from 'react';
import type { Product } from '@/lib/products';
import { ArrowRightIcon, CheckCircleIcon } from './icons';

/**
 * Loads the Payhip embedded checkout script once. The `payhip-buy-button`
 * class + data-product attribute opens checkout in an overlay
 * (Stripe + PayPal both appear automatically).
 */
function usePayhip() {
  useEffect(() => {
    if (document.getElementById('payhip-js')) return;
    const s = document.createElement('script');
    s.id = 'payhip-js';
    s.src = 'https://payhip.com/payhip.js';
    s.async = true;
    document.body.appendChild(s);
  }, []);
}

export default function ProductCard({ product }: { product: Product }) {
  usePayhip();

  return (
    <article
      className={`group relative flex flex-col overflow-hidden rounded-3xl border bg-white/85 shadow-card backdrop-blur transition duration-300 hover:-translate-y-2 hover:shadow-soft ${
        product.featured ? 'border-rose/40 ring-1 ring-rose/20' : 'border-rose/10 hover:border-rose/30'
      }`}
    >
      {product.badge && (
        <span className="absolute right-4 top-4 z-10 rounded-full bg-wine px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.16em] text-white shadow-soft">
          {product.badge}
        </span>
      )}

      <div className="relative aspect-[4/3] overflow-hidden bg-blush2">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={product.image}
          alt={product.title}
          className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
          loading="lazy"
          onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-wine2/15 to-transparent" />
      </div>

      <div className="flex flex-1 flex-col p-7">
        <p className="text-[11px] font-extrabold uppercase tracking-[0.2em] text-rose">
          {product.tagline}
        </p>
        <h3 className="mt-2 font-serif text-2xl font-semibold leading-tight text-wine2">
          {product.title}
        </h3>
        <p className="mt-3 text-sm leading-7 text-ink/70">{product.description}</p>

        <ul className="mt-5 space-y-2.5">
          {product.highlights.map((h) => (
            <li key={h} className="flex items-start gap-2.5 text-sm text-ink/75">
              <CheckCircleIcon className="mt-0.5 h-4 w-4 flex-shrink-0 text-rose" />
              <span>{h}</span>
            </li>
          ))}
        </ul>

        <div className="mt-6 flex items-end gap-3">
          <span className="font-serif text-3xl font-semibold text-wine2">
            ${product.price.toFixed(2).replace(/\.00$/, '')}
          </span>
          {product.compareAt && (
            <span className="mb-1 text-sm text-ink/40 line-through">${product.compareAt}</span>
          )}
        </div>

        <a
          href={product.payhipUrl}
          data-product={product.payhipId}
          className="payhip-buy-button btn-shine mt-5 inline-flex items-center justify-center gap-2.5 rounded-full bg-wine px-7 py-4 text-xs font-extrabold uppercase tracking-[0.16em] text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-wine2"
        >
          Get the Book
          <ArrowRightIcon className="h-4 w-4" />
        </a>

        <p className="mt-3 flex items-center justify-center gap-1.5 text-[11px] text-ink/45">
          <CheckCircleIcon className="h-3.5 w-3.5 text-rose" />
          Instant download • 30-day guarantee
        </p>
      </div>
    </article>
  );
}
