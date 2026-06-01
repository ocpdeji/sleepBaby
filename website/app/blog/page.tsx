import type { Metadata } from 'next';
import BlogCard from '@/components/BlogCard';
import CTABanner from '@/components/CTABanner';
import { getAllPosts } from '@/lib/blog';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Blog — Gentle Baby Sleep Help',
  description:
    'Practical, gentle baby and toddler sleep articles — wake windows, the 4-month regression, sleep training without crying it out, and more.',
  alternates: { canonical: `${site.url}/blog` },
};

const categories = ['Sleep Training', 'Newborns', 'Toddlers', 'Real Talk'] as const;

export default function BlogIndexPage() {
  const posts = getAllPosts();
  const [featured, ...rest] = posts;

  return (
    <>
      <section className="soft-vignette">
        <div className="mx-auto max-w-3xl px-5 py-16 text-center sm:px-8 lg:py-20">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">The blog</p>
          <h1 className="mt-3 font-serif text-5xl font-semibold leading-[1.02] tracking-[-0.03em] text-wine2 sm:text-6xl">
            Gentle sleep help, one article at a time
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-ink/75">
            Honest, practical guidance for real families. No judgment, no jargon —
            just what actually works.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-2.5">
            {categories.map((c) => (
              <span
                key={c}
                className="rounded-full border border-rose/20 bg-white/70 px-4 py-2 text-xs font-semibold text-wine"
              >
                {c}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-5 pb-8 sm:px-8 lg:px-12">
        {posts.length === 0 ? (
          <p className="py-20 text-center text-ink/60">New articles are on the way.</p>
        ) : (
          <div className="grid gap-7 lg:grid-cols-2">
            {featured && <BlogCard post={featured} featured />}
            {rest.map((post) => (
              <BlogCard key={post.slug} post={post} />
            ))}
          </div>
        )}
      </section>

      <CTABanner />
    </>
  );
}
