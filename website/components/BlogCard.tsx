import Link from 'next/link';
import type { PostMeta } from '@/lib/blog';
import { ClockIcon } from './icons';
import SafeImage from './SafeImage';

function formatDate(date: string) {
  if (!date) return '';
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export default function BlogCard({ post, featured = false }: { post: PostMeta; featured?: boolean }) {
  return (
    <article
      className={`group flex flex-col overflow-hidden rounded-3xl border border-rose/10 bg-white/85 shadow-card backdrop-blur transition duration-300 hover:-translate-y-2 hover:border-rose/30 hover:shadow-soft ${
        featured ? 'lg:col-span-2 lg:flex-row' : ''
      }`}
    >
      <Link
        href={`/blog/${post.slug}`}
        className={`relative block overflow-hidden bg-blush2 ${
          featured ? 'lg:w-1/2' : ''
        }`}
      >
        <div className={`relative ${featured ? 'aspect-[16/10] h-full' : 'aspect-[16/10]'}`}>
          <SafeImage
            src={post.cover}
            alt={post.title}
            className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
          />
          <span className="absolute left-4 top-4 rounded-full bg-cream/90 px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.16em] text-wine backdrop-blur">
            {post.category}
          </span>
        </div>
      </Link>

      <div className={`flex flex-1 flex-col p-7 ${featured ? 'lg:justify-center' : ''}`}>
        <Link href={`/blog/${post.slug}`}>
          <h3
            className={`font-serif font-semibold leading-tight text-wine2 transition group-hover:text-wine ${
              featured ? 'text-3xl' : 'text-xl'
            }`}
          >
            {post.title}
          </h3>
        </Link>
        <p className="mt-3 flex-1 text-sm leading-7 text-ink/70">{post.excerpt}</p>

        <div className="mt-5 flex items-center gap-4 text-xs text-ink/50">
          <span>{formatDate(post.date)}</span>
          <span className="inline-flex items-center gap-1.5">
            <ClockIcon className="h-3.5 w-3.5 text-rose" />
            {post.readingTime}
          </span>
        </div>
      </div>
    </article>
  );
}
