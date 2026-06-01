import Link from 'next/link';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { MDXRemote } from 'next-mdx-remote/rsc';
import rehypeSlug from 'rehype-slug';
import remarkGfm from 'remark-gfm';
import TableOfContents from '@/components/TableOfContents';
import AuthorBio from '@/components/AuthorBio';
import BlogCard from '@/components/BlogCard';
import ShareButtons from '@/components/ShareButtons';
import BlogViewTracker from '@/components/BlogViewTracker';
import InlineCTA from '@/components/InlineCTA';
import { mdxComponents } from '@/components/mdx-components';
import { getAllSlugs, getPost, getRelatedPosts } from '@/lib/blog';
import { extractToc } from '@/lib/toc';
import { site } from '@/lib/site';

export const dynamicParams = false;

export function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const post = getPost(params.slug);
  if (!post) return {};
  const url = `${site.url}/blog/${post.slug}`;
  return {
    title: post.title,
    description: post.excerpt,
    keywords: post.keywords,
    alternates: { canonical: url },
    openGraph: {
      type: 'article',
      title: post.title,
      description: post.excerpt,
      url,
      publishedTime: post.date,
      authors: [site.author],
      images: [{ url: post.cover, width: 1200, height: 630, alt: post.title }],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.cover],
    },
  };
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export default function BlogPostPage({ params }: { params: { slug: string } }) {
  const post = getPost(params.slug);
  if (!post) notFound();

  const toc = extractToc(post.content);
  const related = getRelatedPosts(post.slug, post.category);
  const url = `${site.url}/blog/${post.slug}`;

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: `${site.url}${post.cover}`,
    datePublished: post.date,
    author: { '@type': 'Person', name: site.author },
    publisher: {
      '@type': 'Organization',
      name: site.name,
      logo: { '@type': 'ImageObject', url: `${site.url}/images/logo.png` },
    },
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
  };

  return (
    <article>
      <BlogViewTracker slug={post.slug} />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Breadcrumb + hero */}
      <header className="soft-vignette">
        <div className="mx-auto max-w-3xl px-5 pt-12 sm:px-8">
          <nav aria-label="Breadcrumb" className="text-xs text-ink/50">
            <Link href="/" className="hover:text-wine">Home</Link>
            <span className="mx-2">/</span>
            <Link href="/blog" className="hover:text-wine">Blog</Link>
            <span className="mx-2">/</span>
            <span className="text-cocoa">{post.category}</span>
          </nav>
          <p className="mt-6 text-xs font-extrabold uppercase tracking-[0.2em] text-rose">
            {post.category}
          </p>
          <h1 className="mt-3 font-serif text-4xl font-semibold leading-[1.05] tracking-[-0.03em] text-wine2 sm:text-5xl">
            {post.title}
          </h1>
          <div className="mt-5 flex flex-wrap items-center gap-4 text-sm text-ink/55">
            <span>By {site.author}</span>
            <span>•</span>
            <span>{formatDate(post.date)}</span>
            <span>•</span>
            <span>{post.readingTime}</span>
          </div>
        </div>
        <div className="mx-auto mt-8 max-w-4xl px-5 sm:px-8">
          <div className="aspect-[16/8] overflow-hidden rounded-3xl bg-blush2 shadow-soft">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={post.cover} alt={post.title} className="h-full w-full object-cover" />
          </div>
        </div>
      </header>

      {/* Body + sticky TOC */}
      <div className="mx-auto grid max-w-6xl gap-12 px-5 py-14 sm:px-8 lg:grid-cols-[1fr_260px] lg:px-12">
        <div className="mx-auto w-full max-w-prose">
          <div className="prose-editorial">
            <MDXRemote
              source={post.content}
              components={{ ...mdxComponents, InlineCTA }}
              options={{
                mdxOptions: {
                  remarkPlugins: [remarkGfm],
                  rehypePlugins: [rehypeSlug],
                },
              }}
            />
          </div>

          <div className="mt-10 flex items-center justify-between border-t border-rose/10 pt-6">
            <ShareButtons url={url} title={post.title} />
            <Link href="/blog" className="text-sm font-semibold text-wine hover:text-rose">
              ← All articles
            </Link>
          </div>

          <AuthorBio />
        </div>

        <aside className="hidden lg:block">
          <div className="sticky top-24">
            <TableOfContents items={toc} />
          </div>
        </aside>
      </div>

      {related.length > 0 && (
        <section className="bg-blush2/40 py-16">
          <div className="mx-auto max-w-7xl px-5 sm:px-8 lg:px-12">
            <h2 className="mb-8 font-serif text-3xl font-semibold tracking-[-0.02em] text-wine2">
              Keep reading
            </h2>
            <div className="grid gap-6 md:grid-cols-2">
              {related.map((p) => (
                <BlogCard key={p.slug} post={p} />
              ))}
            </div>
          </div>
        </section>
      )}
    </article>
  );
}
