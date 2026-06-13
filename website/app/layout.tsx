import type { Metadata } from 'next';
import { Inter, Fraunces } from 'next/font/google';
import Script from 'next/script';
import './globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { site } from '@/lib/site';
import GoogleAnalytics from '@/components/GoogleAnalytics';
import { Analytics } from '@vercel/analytics/next';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const fraunces = Fraunces({
  subsets: ['latin'],
  variable: '--font-fraunces',
  display: 'swap',
  weight: ['400', '500', '600', '700'],
});

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: `${site.name} | ${site.tagline}`,
    template: `%s | ${site.name}`,
  },
  description: site.description,
  keywords: [
    'baby sleep guide',
    'sleep training gentle',
    'wake windows by age',
    '4 month sleep regression',
    'toddler bedtime routine',
  ],
  authors: [{ name: site.author }],
  openGraph: {
    type: 'website',
    siteName: site.name,
    title: `${site.name} | ${site.tagline}`,
    description: site.description,
    url: site.url,
    images: [{ url: site.ogImage, width: 1200, height: 630, alt: site.name }],
  },
  twitter: {
    card: 'summary_large_image',
    title: `${site.name} | ${site.tagline}`,
    description: site.description,
    images: [site.ogImage],
  },
  alternates: { canonical: site.url },
  robots: { index: true, follow: true },
    verification: {
    google: 'wPhTUGAwhUP17IX9k25SHipaFAODVjAG5tLzci4iMmU',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const plausibleDomain = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN;

return (
  <html lang="en" className={`${inter.variable} ${fraunces.variable}`}>
    <head>
      <Script
        src="https://www.googletagmanager.com/gtag/js?id=G-YHE0Z88VFL"
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-YHE0Z88VFL');
        `}
      </Script>
    </head>
    <body className="bg-cream font-sans antialiased selection:bg-rose selection:text-white">
      <GoogleAnalytics />
        <div className="grain" aria-hidden="true" />
        <Navbar />
        <main className="relative z-10">{children}</main>
        <Footer />
        {plausibleDomain && (
          <Script
            defer
            data-domain={plausibleDomain}
            src="https://plausible.io/js/script.js"
            strategy="afterInteractive"
          />
        )}
        <Analytics />
      </body>
    </html>
  );
}
