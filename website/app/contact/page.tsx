import type { Metadata } from 'next';
import ContactForm from '@/components/ContactForm';
import { HeartIcon, MailIcon, ClockIcon } from '@/components/icons';
import { site } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Contact',
  description:
    'Questions about baby sleep, the books, or your download? Send Kate a message — she reads every one.',
  alternates: { canonical: `${site.url}/contact` },
};

export default function ContactPage() {
  return (
    <section className="soft-vignette">
      <div className="mx-auto grid max-w-7xl gap-12 px-5 py-16 sm:px-8 lg:grid-cols-[0.45fr_0.55fr] lg:px-12 lg:py-20">
        <div className="max-w-lg">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-rose">Contact</p>
          <h1 className="mt-3 font-serif text-5xl font-semibold leading-[1.02] tracking-[-0.03em] text-wine2 sm:text-6xl">
            Let’s talk
          </h1>
          <p className="mt-6 text-lg leading-8 text-ink/80">
            Whether it’s a question about the books, a hiccup with your download, or
            you just need a little reassurance at 2am — I’m here.
          </p>

          <div className="mt-8 space-y-4">
            <InfoRow icon={MailIcon} title="Email">
              <a href={`mailto:${site.email}`} className="text-wine underline-offset-2 hover:underline">
                {site.email}
              </a>
            </InfoRow>
            <InfoRow icon={ClockIcon} title="Response time">
              Usually within 1–2 business days.
            </InfoRow>
            <InfoRow icon={HeartIcon} title="A note from Kate">
              I read every message myself. You’re not bothering me — that’s what I’m here for.
            </InfoRow>
          </div>
        </div>

        <ContactForm />
      </div>
    </section>
  );
}

function InfoRow({
  icon: Icon,
  title,
  children,
}: {
  icon: (props: { className?: string }) => JSX.Element;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-start gap-4 rounded-2xl border border-rose/10 bg-white/70 p-5 shadow-card backdrop-blur">
      <span className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-full bg-blush2 text-wine">
        <Icon className="h-5 w-5" />
      </span>
      <div>
        <p className="text-xs font-extrabold uppercase tracking-[0.16em] text-cocoa">{title}</p>
        <p className="mt-1 text-sm text-ink/75">{children}</p>
      </div>
    </div>
  );
}
