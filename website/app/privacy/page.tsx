import type { Metadata } from 'next';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'How Six & Thriving collects, uses, and protects your personal information.',
  alternates: { canonical: `${site.url}/privacy` },
  robots: { index: true, follow: false },
};

export default function PrivacyPage() {
  return (
    <section className="mx-auto max-w-prose px-5 py-16 sm:px-8">
      <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">Legal</p>
      <h1 className="mt-3 font-serif text-5xl font-semibold tracking-[-0.03em] text-wine2">
        Privacy Policy
      </h1>
      <p className="mt-4 text-sm text-ink/55">Last updated: May 2026</p>

      <div className="prose-editorial mt-10">
        <p>
          Six &amp; Thriving (&quot;we&quot;, &quot;us&quot;, &quot;our&quot;) respects your privacy. This
          policy explains what we collect, why, and the rights you have. It is written to comply
          with the EU/UK General Data Protection Regulation (GDPR) and the Canadian Personal
          Information Protection and Electronic Documents Act (PIPEDA).
        </p>

        <h2>What we collect</h2>
        <ul>
          <li><strong>Contact details</strong> you give us — your name and email when you join our newsletter, download the free cheat sheet, or use the contact form.</li>
          <li><strong>Messages</strong> you send through the contact form.</li>
          <li><strong>Usage data</strong> — privacy-friendly, aggregate analytics (via Plausible) and anonymous blog page-view counts. We do not use invasive third-party tracking cookies.</li>
        </ul>

        <h2>How we use it</h2>
        <ul>
          <li>To send you the resources you requested and our email newsletter.</li>
          <li>To respond to your questions and provide support.</li>
          <li>To understand which content is helpful so we can improve the site.</li>
        </ul>
        <p>
          We rely on your <strong>consent</strong> (when you sign up) and our <strong>legitimate
          interest</strong> in running and improving the site as our legal bases for processing.
        </p>

        <h2>Email &amp; payments</h2>
        <p>
          Email is managed by <strong>MailerLite</strong>, which stores your contact details to
          deliver our messages. Purchases are handled entirely by <strong>Payhip</strong> (with
          Stripe and PayPal as payment processors) — we never see or store your full payment card
          details. Each provider maintains its own privacy policy.
        </p>

        <h2>Cookies</h2>
        <p>
          We use only essential cookies needed for the site to function. Our analytics are
          cookieless. We do not sell your data to anyone, ever.
        </p>

        <h2>Your rights</h2>
        <p>
          You can ask us to access, correct, or delete your personal data, or to stop emailing you,
          at any time. Every newsletter includes a one-click unsubscribe link. To make any other
          request, email <a href={`mailto:${site.email}`}>{site.email}</a>.
        </p>

        <h2>Data retention</h2>
        <p>
          We keep your information only as long as needed to provide our services or as required by
          law. If you unsubscribe and request deletion, we remove your details promptly.
        </p>

        <h2>Children</h2>
        <p>
          Our products are for parents and caregivers. The site is not directed at children, and we
          do not knowingly collect data from anyone under 16.
        </p>

        <h2>Changes</h2>
        <p>
          We may update this policy from time to time. The &quot;last updated&quot; date above will
          always reflect the current version.
        </p>

        <h2>Contact</h2>
        <p>
          Questions about your privacy? Email <a href={`mailto:${site.email}`}>{site.email}</a>.
        </p>
      </div>
    </section>
  );
}
