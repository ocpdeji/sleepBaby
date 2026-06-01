import type { Testimonial } from '@/components/TestimonialCard';
import type { FAQItem } from '@/components/FAQAccordion';

export const testimonials: Testimonial[] = [
  {
    name: 'Sara',
    role: 'Mom of 2 · Toronto',
    quote:
      'Kate’s guidance was a total game changer for our family. We went from surviving to thriving — and our toddler is sleeping better than ever.',
    rating: 5,
  },
  {
    name: 'Megan',
    role: 'First-time mom · Calgary',
    quote:
      'I’d tried everything and given up twice. The Night 3 chapter alone explained why. By night 6 my daughter slept through for the first time.',
    rating: 5,
  },
  {
    name: 'Priya',
    role: 'Mom of twins · Vancouver',
    quote:
      'Finally a plan that didn’t pretend twins are the same as one baby. The sync planner saved my sanity. Worth every penny.',
    rating: 5,
  },
];

export const homeFaqs: FAQItem[] = [
  {
    q: 'What age is this for?',
    a: 'Birth to 24 months for active sleep work. The newborn material covers under 8 weeks, and there is a dedicated toddler section for ages 18 months through 3 years.',
  },
  {
    q: 'I’m breastfeeding — is this for me?',
    a: 'Yes. There is a chapter dedicated specifically to breastfeeding moms. Independent sleep and breastfeeding are absolutely compatible — your supply will not disappear and your bond will not break.',
  },
  {
    q: 'Is this just cry-it-out repackaged?',
    a: 'No. Extinction is one of five methods covered. You also get Ferber, Chair Method, Fading, and Pick-Up/Put-Down. You choose what fits your family. The book never tells you to ignore a distressed baby.',
  },
  {
    q: 'I tried sleep training before and it failed. What now?',
    a: 'The Reset Protocol is a step-by-step diagnostic for parents who have already tried. It addresses directly why most attempts fail on Night 3 — and exactly how to fix it.',
  },
  {
    q: 'How long until I see results?',
    a: 'Most families see meaningful change within 7 nights. Some take 10–14. The plan is built to set realistic week-one expectations and stop you quitting on the hardest night.',
  },
];

export const howItWorks = [
  {
    step: '01',
    title: 'Get the free cheat sheet',
    body: 'Start tonight with the simple fixes that make the biggest difference. No fluff — just what works.',
  },
  {
    step: '02',
    title: 'Read the gentle emails',
    body: 'A short series that walks you through the foundations, the mistakes to avoid, and the plan that fits your baby.',
  },
  {
    step: '03',
    title: 'Sleep better — together',
    body: 'Follow the night-by-night plan from the book and watch the breakthrough happen, usually within a week.',
  },
];
