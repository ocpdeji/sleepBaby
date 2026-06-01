import type { Metadata } from 'next';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Terms of Service',
  description: 'The terms that apply when you use the Six & Thriving website and buy our digital products.',
  alternates: { canonical: `${site.url}/terms` },
  robots: { index: true, follow: false },
};

export default function TermsPage() {
  return (
    <section className="mx-auto max-w-prose px-5 py-16 sm:px-8">
      <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">Legal</p>
      <h1 className="mt-3 font-serif text-5xl font-semibold tracking-[-0.03em] text-wine2">
        Terms of Service
      </h1>
      <p className="mt-4 text-sm text-ink/55">Last updated: May 2026</p>

      <div className="prose-editorial mt-10">
        <p>
          Welcome to Six &amp; Thriving. By using this website and purchasing our digital products,
          you agree to these terms. Please read them carefully.
        </p>

        <h2>About our products</h2>
        <p>
          We sell <strong>digital products</strong> — ebooks, guides, planners, and printables —
          delivered as instant downloads through Payhip. Once purchased, files are yours to keep and
          use for your own personal, non-commercial purposes.
        </p>

        <h2>Educational content, not medical advice</h2>
        <p>
          Our content is for general educational and informational purposes only. It is <strong>not
          medical advice</strong> and is not a substitute for guidance from your pediatrician or a
          qualified health professional. Always follow safe-sleep guidelines and consult your
          doctor about your child&apos;s specific situation. You use the information at your own
          discretion.
        </p>

        <h2>Refunds &amp; guarantee</h2>
        <p>
          We stand behind our work with a <strong>30-day money-back guarantee</strong>. If a product
          isn&apos;t right for you, email <a href={`mailto:${site.email}`}>{site.email}</a> within 30
          days of purchase for a full refund — no forms, no hassle.
        </p>

        <h2>License &amp; intellectual property</h2>
        <p>
          All content, products, text, and designs are the property of Six &amp; Thriving and
          protected by copyright. When you buy a product, you receive a single-user license. You may
          not resell, redistribute, share, or reproduce our products for others without written
          permission.
        </p>

        <h2>Payments</h2>
        <p>
          Payments are processed securely by Payhip using Stripe and PayPal. Prices are listed in
          USD unless otherwise noted and may change at any time. We do not store your payment card
          information.
        </p>

        <h2>Acceptable use</h2>
        <p>
          You agree not to misuse the site — including attempting to disrupt it, access it
          unlawfully, or use its content in ways these terms don&apos;t allow.
        </p>

        <h2>Limitation of liability</h2>
        <p>
          To the fullest extent permitted by law, Six &amp; Thriving is not liable for any indirect
          or consequential losses arising from your use of the site or products. Our total liability
          is limited to the amount you paid for the product in question.
        </p>

        <h2>Governing law</h2>
        <p>
          These terms are governed by the laws of Canada and the province in which we operate,
          without regard to conflict-of-law principles.
        </p>

        <h2>Contact</h2>
        <p>
          Questions about these terms? Email <a href={`mailto:${site.email}`}>{site.email}</a>.
        </p>
      </div>
    </section>
  );
}
