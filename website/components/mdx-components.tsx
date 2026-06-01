import type { MDXRemoteProps } from 'next-mdx-remote/rsc';
import InlineCTA from './InlineCTA';

/**
 * Custom React components available inside MDX blog posts.
 * Use <InlineCTA /> anywhere in a post to drop in the cheat-sheet promo.
 */
export const mdxComponents: MDXRemoteProps['components'] = {
  InlineCTA,
};
