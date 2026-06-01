import type { TocItem } from '@/components/TableOfContents';

/** Slugify heading text to match rehype-slug's default behaviour. */
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

/** Extract h2/h3 headings from raw MDX content for the table of contents. */
export function extractToc(content: string): TocItem[] {
  const lines = content.split('\n');
  const items: TocItem[] = [];
  let inCodeBlock = false;

  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) continue;

    const match = /^(#{2,3})\s+(.*)$/.exec(line.trim());
    if (match) {
      const level = match[1].length;
      const text = match[2].replace(/[*_`]/g, '').trim();
      items.push({ id: slugify(text), text, level });
    }
  }
  return items;
}
