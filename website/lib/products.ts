export interface Product {
  slug: string;
  title: string;
  shortTitle: string;
  price: number;
  compareAt?: number;
  payhipUrl: string;
  payhipId: string;
  tagline: string;
  description: string;
  highlights: string[];
  badge?: string;
  featured?: boolean;
  image: string;
}

/**
 * The 4 live Payhip products. Payhip handles checkout (Stripe + PayPal
 * are connected on the Payhip side — both appear automatically at checkout).
 * `payhipId` is the product code used by the embedded buy button.
 */
export const products: Product[] = [
  {
    slug: 'sleep-baby-please',
    title: 'Sleep, Baby. Please.',
    shortTitle: 'The Book',
    price: 19.99,
    compareAt: 29,
    payhipUrl: 'https://payhip.com/b/m62Yx',
    payhipId: 'm62Yx',
    tagline: 'The complete infant sleep guide',
    description:
      'The evidence-based 7-night plan that gets your baby sleeping through the night — written by a mom of 6 who has been exactly where you are. 59 pages, 15 chapters, every word built to be used at 2am.',
    highlights: [
      'The literal night-by-night 7-night plan',
      'The Extinction Burst — what nobody tells you about Night 3',
      'The Six Sleep Personalities — find your baby in 5 minutes',
      '4 bonus tools: checklist, tracker, awake windows, methods',
    ],
    image: '/images/products/book.jpg',
  },
  {
    slug: 'premium-bundle',
    title: 'Sleep, Baby. Please. — Premium Bundle',
    shortTitle: 'Premium Bundle',
    price: 39.99,
    compareAt: 59,
    payhipUrl: 'https://payhip.com/b/zH6ib',
    payhipId: 'zH6ib',
    tagline: 'The book + every companion tool',
    description:
      'Everything you need to get your baby sleeping — in one download. The book that gives you the knowledge, plus the companion tools that turn it into action.',
    highlights: [
      'The complete 59-page eBook',
      'Bundle Index — Start Here guide',
      '7-Night Sleep Tracker + Routine Builder',
      'Six Sleep Personalities Kit + Reset Protocol',
    ],
    badge: 'Best Value',
    featured: true,
    image: '/images/products/bundle.png',
  },
  {
    slug: 'toddler-bedtime-kit',
    title: 'The Toddler Bedtime Survival Kit',
    shortTitle: 'Toddler Kit',
    price: 12,
    payhipUrl: 'https://payhip.com/b/CgT2K',
    payhipId: 'CgT2K',
    tagline: 'For when bedtime became "negotiable"',
    description:
      'For the parent of an 18-month-to-3-year-old who has discovered bedtime is negotiable. The framework that holds the line — with warmth.',
    highlights: [
      'The Door Rule — resolves bedtime in 3–4 nights',
      'The "One Pass" system for bedtime visitors',
      'Scripts for stalls, 2am visits and bad dreams',
      'The OK-to-Wake setup + the 5am wake fix',
    ],
    image: '/images/products/toddler.png',
  },
  {
    slug: 'newborn-starter-kit',
    title: 'The Newborn Sleep Starter Kit',
    shortTitle: 'Newborn Kit',
    price: 9,
    payhipUrl: 'https://payhip.com/b/Me6L9',
    payhipId: 'Me6L9',
    tagline: 'For the first 8 weeks of surviving',
    description:
      'For the first 8 weeks, when you are not sleep training — you are surviving. Realistic expectations and gentle foundations, without the overwhelm or the guilt.',
    highlights: [
      'What newborn sleep actually looks like',
      'Printable week-by-week awake window tracker',
      'The simple foundation routine for weeks 3–8',
      'Day vs night signals to set the circadian clock',
    ],
    image: '/images/products/newborn.png',
  },
];

export function getProduct(slug: string): Product | undefined {
  return products.find((p) => p.slug === slug);
}

export const featuredProduct = products.find((p) => p.featured) ?? products[1];
