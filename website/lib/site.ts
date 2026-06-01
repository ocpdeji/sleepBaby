export const site = {
  name: 'Six & Thriving',
  tagline: 'Gentle sleep support for real families',
  description:
    'Gentle, practical sleep support for babies and toddlers — designed for real life and real parents. Free baby sleep cheat sheet, blog, and the book that gets your baby sleeping.',
  url: process.env.NEXT_PUBLIC_SITE_URL || 'https://www.sixandthriving.com',
  email: 'info@sixandthriving.com',
  author: 'Kate',
  ogImage: '/images/og-default.jpg',
  social: {
    instagram: 'https://instagram.com/sixandthriving',
    facebook: 'https://facebook.com/sixandthriving',
    pinterest: 'https://pinterest.com/sixandthriving',
  },
  nav: [
    { label: 'Home', href: '/' },
    { label: 'Shop', href: '/shop' },
    { label: 'Blog', href: '/blog' },
    { label: 'About', href: '/about' },
    { label: 'Contact', href: '/contact' },
  ],
};

export type BlogCategory = 'Sleep Training' | 'Newborns' | 'Toddlers' | 'Real Talk';
