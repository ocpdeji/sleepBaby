import type { Metadata } from 'next';
import ProductCard from '@/components/ProductCard';
import CTABanner from '@/components/CTABanner';
import { DownloadIcon, ShieldIcon, CheckCircleIcon } from '@/components/icons';
import { products } from '@/lib/products';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Shop',
  description:
    'The book that gets your baby sleeping — plus the companion kits for newborns, toddlers, and the full premium bundle. Instant download, 30-day guarantee.',
  alternates: { canonical: `${site.url}/shop` },
};

const trustBadges = [
  { icon: DownloadIcon, title: 'Instant download', body: 'Get your files the moment you buy.' },
  { icon: ShieldIcon, title: '30-day guarantee', body: 'No-questions-asked money back.' },
  { icon: CheckCircleIcon, title: 'Secure payment', body: 'Pay with card or PayPal via Payhip.' },
];

export default function ShopPage() {
  return (
    <>
      <section className="soft-vignette">
        <div className="mx-auto max-w-3xl px-5 py-16 text-center sm:px-8 lg:py-20">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">The shop</p>
          <h1 className="mt-3 font-serif text-5xl font-semibold leading-[1.02] tracking-[-0.03em] text-wine2 sm:text-6xl">
            The book that gets your baby sleeping
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-ink/75">
            Written by a mom who has navigated every sleep stage across more
            households than she can count. Choose the book, the full premium
            bundle, or the kit built for your stage.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-5 pb-6 sm:px-8 lg:px-12">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {products.map((product) => (
            <ProductCard key={product.slug} product={product} />
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-5xl px-5 py-12 sm:px-8 lg:px-12">
        <div className="grid gap-5 rounded-3xl border border-rose/10 bg-white/85 p-8 shadow-card backdrop-blur sm:grid-cols-3">
          {trustBadges.map((b) => (
            <div key={b.title} className="flex flex-col items-center gap-3 text-center">
              <span className="flex h-14 w-14 items-center justify-center rounded-full bg-blush2 text-wine">
                <b.icon className="h-7 w-7" />
              </span>
              <div>
                <p className="font-serif text-lg font-semibold text-wine2">{b.title}</p>
                <p className="mt-1 text-sm text-ink/65">{b.body}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <CTABanner
        title="Not sure where to start?"
        subtitle="Grab the free cheat sheet first — it’s the simplest way to see results tonight, no purchase needed."
      />
    </>
  );
}
