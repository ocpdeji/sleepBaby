import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import readingTime from 'reading-time';
import type { BlogCategory } from './site';

const BLOG_DIR = path.join(process.cwd(), 'content', 'blog');

export interface PostMeta {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  category: BlogCategory;
  cover: string;
  keywords: string[];
  readingTime: string;
}

export interface Post extends PostMeta {
  content: string;
}

function readPostFile(slug: string): Post | null {
  const fullPath = path.join(BLOG_DIR, `${slug}.mdx`);
  if (!fs.existsSync(fullPath)) return null;

  const raw = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(raw);
  const stats = readingTime(content);

  return {
    slug,
    title: data.title ?? slug,
    excerpt: data.excerpt ?? '',
    date: data.date ?? '',
    category: (data.category ?? 'Real Talk') as BlogCategory,
    cover: data.cover ?? '/images/blog/default.jpg',
    keywords: data.keywords ?? [],
    readingTime: stats.text,
    content,
  };
}

export function getAllSlugs(): string[] {
  if (!fs.existsSync(BLOG_DIR)) return [];
  return fs
    .readdirSync(BLOG_DIR)
    .filter((f) => f.endsWith('.mdx'))
    .map((f) => f.replace(/\.mdx$/, ''));
}

export function getPost(slug: string): Post | null {
  return readPostFile(slug);
}

export function getAllPosts(): PostMeta[] {
  return getAllSlugs()
    .map((slug) => readPostFile(slug))
    .filter((p): p is Post => Boolean(p))
    .sort((a, b) => (a.date < b.date ? 1 : -1))
    .map(({ content, ...meta }) => meta);
}

export function getRelatedPosts(slug: string, category: BlogCategory, limit = 2): PostMeta[] {
  const all = getAllPosts().filter((p) => p.slug !== slug);
  const sameCategory = all.filter((p) => p.category === category);
  const others = all.filter((p) => p.category !== category);
  return [...sameCategory, ...others].slice(0, limit);
}
