import type { MetadataRoute } from 'next';
import { getAllPosts } from '@/lib/blog';
import { site } from '@/lib/site';

export default function sitemap(): MetadataRoute.Sitemap {
  const staticPaths = ['', '/shop', '/about', '/blog', '/free-sleep-guide', '/contact', '/privacy', '/terms'];

  const staticEntries: MetadataRoute.Sitemap = staticPaths.map((path) => ({
    url: `${site.url}${path}`,
    lastModified: new Date(),
    changeFrequency: path === '' ? 'weekly' : 'monthly',
    priority: path === '' ? 1 : 0.7,
  }));

  const postEntries: MetadataRoute.Sitemap = getAllPosts().map((post) => ({
    url: `${site.url}/blog/${post.slug}`,
    lastModified: post.date ? new Date(post.date) : new Date(),
    changeFrequency: 'monthly',
    priority: 0.6,
  }));

  return [...staticEntries, ...postEntries];
}
