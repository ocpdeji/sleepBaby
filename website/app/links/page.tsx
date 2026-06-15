import type { Metadata } from 'next';
import fs from 'node:fs';
import path from 'node:path';

export const metadata: Metadata = {
  title: 'Six & Thriving | Links',
  description: 'Helping exhausted moms finally get some sleep. Free guides, the Sleep, Baby. Please. eBook, and real support for real parents.',
};

const mainLinks = [
  {
    emoji: '🌙',
    label: 'Free Baby Sleep Cheat Sheet',
    sublabel: 'Instant download — start tonight',
    href: 'https://sixandthriving.com/free-sleep-guide',
    highlight: true,
    badge: 'FREE',
  },
  {
    emoji: '📖',
    label: 'Sleep, Baby. Please.',
    sublabel: 'The 7-night plan · $19.99',
    href: 'https://payhip.com/b/m62Yx',
    highlight: false,
    badge: 'BESTSELLER',
  },
  {
    emoji: '✨',
    label: 'Premium Bundle — Book + All Tools',
    sublabel: 'Everything in one download · $39.99',
    href: 'https://payhip.com/b/zH6ib',
    highlight: false,
    badge: 'BEST VALUE',
  },
  {
    emoji: '🍼',
    label: 'Newborn Sleep Starter Kit',
    sublabel: 'Weeks 0–8 survival guide · $9',
    href: 'https://payhip.com/b/Me6L9',
    highlight: false,
    badge: null,
  },
  {
    emoji: '🧸',
    label: 'Toddler Bedtime Survival Kit',
    sublabel: '18 months–3 years · $12',
    href: 'https://payhip.com/b/CgT2K',
    highlight: false,
    badge: null,
  },
  {
    emoji: '⏰',
    label: 'Wake Windows by Age — Free Guide',
    sublabel: 'Birth to 24 months, every stage',
    href: 'https://sixandthriving.com/blog/wake-windows-by-age',
    highlight: false,
    badge: null,
  },
  {
    emoji: '😴',
    label: '4-Month Sleep Regression Help',
    sublabel: 'Your baby didn\'t break. Here\'s why.',
    href: 'https://sixandthriving.com/blog/4-month-sleep-regression',
    highlight: false,
    badge: null,
  },
  {
    emoji: '🌐',
    label: 'Visit Six & Thriving',
    sublabel: 'sixandthriving.com',
    href: 'https://sixandthriving.com',
    highlight: false,
    badge: null,
  },
];

const socialLinks = [
  { label: 'Instagram', href: 'https://www.instagram.com/sixandthrivingmom/', icon: 'M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z' },
  { label: 'Pinterest', href: 'https://pinterest.ca/SixAndThriving', icon: 'M12 0C5.373 0 0 5.373 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 01.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.632-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0z' },
  { label: 'TikTok', href: 'https://tiktok.com/@sixandthrivin', icon: 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z' },
  { label: 'YouTube', href: 'https://youtube.com/channel/UC97cj6E8VGuXfZ0JDzQrDSA', icon: 'M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z' },
  { label: 'Facebook', href: 'https://www.facebook.com/profile.php?id=61590580810773', icon: 'M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z' },
  { label: 'Threads', href: 'https://www.threads.com/@sixandthrivingmom', icon: 'M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 013.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.583-1.314-.884-2.371-.899h-.005c-.829 0-1.934.226-2.64 1.149l-1.688-1.239c.903-1.229 2.28-1.913 3.854-1.924.083 0 .166 0 .249.002 1.65.044 2.95.578 3.862 1.587.996 1.104 1.44 2.71 1.32 4.776.082.045.163.091.243.138 1.156.695 1.982 1.647 2.39 2.55.75 1.713.718 4.469-1.587 6.701C17.04 23.24 14.793 23.98 12.186 24zm-3.071-8.757c.071 1.285 1.236 2.037 3.196 1.928 1.139-.062 1.997-.467 2.549-1.202.442-.588.698-1.382.762-2.364a11.765 11.765 0 00-2.656-.208c-.983.057-1.8.307-2.353.725-.522.394-.524.882-.498 1.121z' },
  { label: 'X', href: 'https://x.com/SixAndThriving', icon: 'M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.747l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z' },
  { label: 'Bluesky', href: 'https://bsky.app/profile/sixandthriving.bsky.social', icon: 'M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 01-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.204-.659-.299-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8z' },
];

export default function LinksPage() {
  const hasLogo = fs.existsSync(path.join(process.cwd(), 'public', 'images', 'logo.png'));

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500;600;700&display=swap');

        .links-body {
          font-family: 'DM Sans', sans-serif;
          min-height: 100vh;
          background: #faf8f5;
          position: relative;
          overflow-x: hidden;
        }

        /* Animated gradient orbs */
        .orb {
          position: fixed;
          border-radius: 50%;
          filter: blur(80px);
          opacity: 0.35;
          pointer-events: none;
          z-index: 0;
          animation: float 12s ease-in-out infinite;
        }
        .orb-1 {
          width: 400px; height: 400px;
          background: radial-gradient(circle, #c9a0a0 0%, transparent 70%);
          top: -100px; right: -100px;
          animation-delay: 0s;
        }
        .orb-2 {
          width: 300px; height: 300px;
          background: radial-gradient(circle, #b5cfc3 0%, transparent 70%);
          bottom: 100px; left: -80px;
          animation-delay: -4s;
        }
        .orb-3 {
          width: 200px; height: 200px;
          background: radial-gradient(circle, #d4a96a44 0%, transparent 70%);
          top: 50%; left: 50%;
          transform: translate(-50%, -50%);
          animation-delay: -8s;
        }

        @keyframes float {
          0%, 100% { transform: translateY(0px) scale(1); }
          33% { transform: translateY(-20px) scale(1.05); }
          66% { transform: translateY(10px) scale(0.97); }
        }

        /* Stars */
        .stars {
          position: fixed;
          inset: 0;
          pointer-events: none;
          z-index: 0;
        }
        .star {
          position: absolute;
          width: 2px; height: 2px;
          background: #8B1A2B;
          border-radius: 50%;
          opacity: 0;
          animation: twinkle var(--dur) ease-in-out infinite;
          animation-delay: var(--delay);
        }
        @keyframes twinkle {
          0%, 100% { opacity: 0; transform: scale(0.5); }
          50% { opacity: 0.4; transform: scale(1.5); }
        }

        /* Content */
        .links-content {
          position: relative;
          z-index: 1;
          max-width: 420px;
          margin: 0 auto;
          padding: 48px 20px 60px;
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        /* Logo */
        .logo-wrap {
          position: relative;
          margin-bottom: 20px;
          animation: fadeSlideUp 0.6s ease both;
        }
        .logo-ring {
          width: 88px; height: 88px;
          border-radius: 50%;
          background: linear-gradient(135deg, #fff 0%, #f5eded 100%);
          border: 2px solid rgba(139,26,43,0.15);
          display: flex; align-items: center; justify-content: center;
          box-shadow: 0 8px 32px rgba(139,26,43,0.12), 0 2px 8px rgba(0,0,0,0.06);
          animation: breathe 4s ease-in-out infinite;
        }
        @keyframes breathe {
          0%, 100% { box-shadow: 0 8px 32px rgba(139,26,43,0.12), 0 2px 8px rgba(0,0,0,0.06); }
          50% { box-shadow: 0 12px 48px rgba(139,26,43,0.22), 0 4px 16px rgba(0,0,0,0.08); }
        }
        .logo-img {
          width: 56px; height: 56px;
          object-fit: contain;
        }
        .logo-pulse {
          position: absolute;
          inset: -6px;
          border-radius: 50%;
          border: 1.5px solid rgba(139,26,43,0.15);
          animation: pulse-ring 3s ease-in-out infinite;
        }
        .logo-pulse-2 {
          position: absolute;
          inset: -14px;
          border-radius: 50%;
          border: 1px solid rgba(139,26,43,0.08);
          animation: pulse-ring 3s ease-in-out infinite 0.5s;
        }
        @keyframes pulse-ring {
          0% { transform: scale(0.95); opacity: 0.6; }
          70% { transform: scale(1.05); opacity: 0; }
          100% { transform: scale(0.95); opacity: 0; }
        }

        /* Header text */
        .site-name {
          font-family: 'Playfair Display', serif;
          font-size: 28px;
          font-weight: 900;
          color: #5a1020;
          letter-spacing: -0.02em;
          margin-bottom: 6px;
          animation: fadeSlideUp 0.6s ease 0.1s both;
        }
        .site-tagline {
          font-size: 14px;
          color: #6b5b55;
          font-weight: 500;
          margin-bottom: 10px;
          text-align: center;
          animation: fadeSlideUp 0.6s ease 0.15s both;
        }
        .badge {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          background: rgba(139,26,43,0.07);
          border: 1px solid rgba(139,26,43,0.12);
          border-radius: 20px;
          padding: 5px 14px;
          font-size: 12px;
          font-weight: 600;
          color: #8B1A2B;
          margin-bottom: 32px;
          animation: fadeSlideUp 0.6s ease 0.2s both;
        }

        /* Social proof strip */
        .proof-strip {
          display: flex;
          gap: 20px;
          margin-bottom: 28px;
          animation: fadeSlideUp 0.6s ease 0.25s both;
        }
        .proof-item {
          text-align: center;
        }
        .proof-num {
          font-family: 'Playfair Display', serif;
          font-size: 20px;
          font-weight: 700;
          color: #8B1A2B;
          line-height: 1;
        }
        .proof-label {
          font-size: 10px;
          color: #9a8880;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          margin-top: 2px;
        }
        .proof-divider {
          width: 1px;
          background: rgba(139,26,43,0.12);
          align-self: stretch;
        }

        /* Links */
        .links-list {
          width: 100%;
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 28px;
        }

        .link-card {
          display: flex;
          align-items: center;
          gap: 14px;
          width: 100%;
          padding: 14px 18px;
          border-radius: 16px;
          text-decoration: none;
          transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
          position: relative;
          overflow: hidden;
        }
        .link-card:hover {
          transform: translateY(-3px) scale(1.01);
        }
        .link-card::before {
          content: '';
          position: absolute;
          inset: 0;
          opacity: 0;
          transition: opacity 0.2s;
        }
        .link-card:hover::before { opacity: 1; }

        /* Normal card */
        .link-card-normal {
          background: rgba(255,255,255,0.85);
          backdrop-filter: blur(12px);
          border: 1px solid rgba(139,26,43,0.08);
          box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.04);
        }
        .link-card-normal:hover {
          border-color: rgba(139,26,43,0.2);
          box-shadow: 0 8px 32px rgba(139,26,43,0.10), 0 2px 8px rgba(0,0,0,0.06);
        }
        .link-card-normal::before {
          background: linear-gradient(135deg, rgba(139,26,43,0.02) 0%, rgba(212,169,106,0.04) 100%);
        }

        /* Highlight card */
        .link-card-highlight {
          background: linear-gradient(135deg, #8B1A2B 0%, #6b1020 60%, #8B1A2B 100%);
          background-size: 200% 100%;
          border: none;
          box-shadow: 0 6px 24px rgba(139,26,43,0.35), 0 2px 8px rgba(139,26,43,0.2);
          animation: shimmer 3s ease-in-out infinite;
        }
        .link-card-highlight:hover {
          box-shadow: 0 12px 40px rgba(139,26,43,0.45), 0 4px 12px rgba(139,26,43,0.3);
        }
        @keyframes shimmer {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }

        .link-emoji {
          font-size: 22px;
          flex-shrink: 0;
          line-height: 1;
        }
        .link-text { flex: 1; min-width: 0; }
        .link-title {
          font-size: 14px;
          font-weight: 700;
          line-height: 1.3;
          display: block;
        }
        .link-title-dark { color: #2a1510; }
        .link-title-light { color: #fff; }
        .link-sub {
          font-size: 12px;
          font-weight: 500;
          display: block;
          margin-top: 2px;
        }
        .link-sub-dark { color: rgba(42,21,16,0.5); }
        .link-sub-light { color: rgba(255,255,255,0.7); }

        .link-badge {
          font-size: 9px;
          font-weight: 800;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          padding: 3px 8px;
          border-radius: 8px;
          flex-shrink: 0;
        }
        .link-badge-gold {
          background: #D4A96A;
          color: #fff;
        }
        .link-badge-wine {
          background: rgba(255,255,255,0.2);
          color: #fff;
        }
        .link-badge-green {
          background: #6b9e87;
          color: #fff;
        }

        .link-arrow {
          width: 18px; height: 18px;
          flex-shrink: 0;
          transition: transform 0.2s;
        }
        .link-card:hover .link-arrow { transform: translateX(3px); }
        .link-arrow-dark { color: rgba(42,21,16,0.25); }
        .link-arrow-light { color: rgba(255,255,255,0.5); }

        /* Divider */
        .divider {
          width: 100%;
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 20px;
          animation: fadeSlideUp 0.6s ease 0.5s both;
        }
        .divider-line { flex: 1; height: 1px; background: rgba(139,26,43,0.1); }
        .divider-text {
          font-size: 10px;
          font-weight: 700;
          color: rgba(42,21,16,0.3);
          text-transform: uppercase;
          letter-spacing: 0.14em;
          white-space: nowrap;
        }

        /* Social icons */
        .social-grid {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 10px;
          margin-bottom: 36px;
          animation: fadeSlideUp 0.6s ease 0.55s both;
        }
        .social-btn {
          width: 44px; height: 44px;
          border-radius: 12px;
          background: rgba(255,255,255,0.85);
          backdrop-filter: blur(8px);
          border: 1px solid rgba(139,26,43,0.08);
          display: flex; align-items: center; justify-content: center;
          color: rgba(139,26,43,0.5);
          box-shadow: 0 2px 8px rgba(0,0,0,0.05);
          transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
          text-decoration: none;
        }
        .social-btn:hover {
          color: #8B1A2B;
          border-color: rgba(139,26,43,0.25);
          box-shadow: 0 6px 20px rgba(139,26,43,0.15);
          transform: translateY(-3px) scale(1.1);
          background: #fff;
        }

        /* Footer */
        .links-footer {
          text-align: center;
          animation: fadeSlideUp 0.6s ease 0.6s both;
        }
        .footer-copy {
          font-size: 11px;
          color: rgba(42,21,16,0.3);
          font-weight: 500;
        }
        .footer-link {
          font-size: 11px;
          color: rgba(139,26,43,0.35);
          text-decoration: none;
          display: block;
          margin-top: 4px;
          transition: color 0.15s;
        }
        .footer-link:hover { color: #8B1A2B; }

        /* Staggered animations */
        .anim-0 { animation: fadeSlideUp 0.5s ease 0.3s both; }
        .anim-1 { animation: fadeSlideUp 0.5s ease 0.35s both; }
        .anim-2 { animation: fadeSlideUp 0.5s ease 0.4s both; }
        .anim-3 { animation: fadeSlideUp 0.5s ease 0.42s both; }
        .anim-4 { animation: fadeSlideUp 0.5s ease 0.44s both; }
        .anim-5 { animation: fadeSlideUp 0.5s ease 0.46s both; }
        .anim-6 { animation: fadeSlideUp 0.5s ease 0.48s both; }
        .anim-7 { animation: fadeSlideUp 0.5s ease 0.5s both; }

        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(16px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after { animation: none !important; transition: none !important; }
        }
      `}</style>

      <div className="links-body">

        {/* Ambient orbs */}
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />

        {/* Stars */}
        <div className="stars" aria-hidden="true">
          {[
            { top: '8%', left: '12%', dur: '3.2s', delay: '0s' },
            { top: '15%', left: '85%', dur: '4.1s', delay: '0.8s' },
            { top: '25%', left: '5%', dur: '2.8s', delay: '1.4s' },
            { top: '35%', left: '92%', dur: '3.7s', delay: '0.3s' },
            { top: '55%', left: '3%', dur: '4.5s', delay: '2.1s' },
            { top: '65%', left: '88%', dur: '3.1s', delay: '1.7s' },
            { top: '78%', left: '15%', dur: '2.6s', delay: '0.6s' },
            { top: '85%', left: '80%', dur: '4.2s', delay: '1.2s' },
            { top: '92%', left: '45%', dur: '3.4s', delay: '2.5s' },
            { top: '45%', left: '96%', dur: '2.9s', delay: '0.9s' },
          ].map((s, i) => (
            <div
              key={i}
              className="star"
              style={{
                top: s.top, left: s.left,
                ['--dur' as string]: s.dur,
                ['--delay' as string]: s.delay,
              }}
            />
          ))}
        </div>

        <div className="links-content">

          {/* Logo */}
          <div className="logo-wrap">
            <div className="logo-pulse" />
            <div className="logo-pulse-2" />
            <div className="logo-ring">
              {hasLogo ? (
                <img
                  src="/images/logo.png"
                  alt="Six & Thriving"
                  className="logo-img"
                />
              ) : (
                <span style={{ fontSize: 36 }}>🌙</span>
              )}
            </div>
          </div>

          {/* Name + tagline */}
          <h1 className="site-name">Six &amp; Thriving</h1>
          <p className="site-tagline">Helping exhausted moms finally get some sleep</p>
          <div className="badge">Mom of 6 · Yes, twins too 👶👶</div>

          {/* Social proof */}
          <div className="proof-strip">
            <div className="proof-item">
              <div className="proof-num">1,000+</div>
              <div className="proof-label">Parents helped</div>
            </div>
            <div className="proof-divider" />
            <div className="proof-item">
              <div className="proof-num">7</div>
              <div className="proof-label">Nights to results</div>
            </div>
            <div className="proof-divider" />
            <div className="proof-item">
              <div className="proof-num">30</div>
              <div className="proof-label">Day guarantee</div>
            </div>
          </div>

          {/* Main links */}
          <div className="links-list">
            {mainLinks.map((link, i) => (
              <a
                key={link.href}
                href={link.href}
                target={link.href.startsWith('https://sixandthriving.com') ? '_self' : '_blank'}
                rel="noopener noreferrer"
                className={`link-card anim-${i} ${link.highlight ? 'link-card-highlight' : 'link-card-normal'}`}
              >
                <span className="link-emoji">{link.emoji}</span>
                <span className="link-text">
                  <span className={`link-title ${link.highlight ? 'link-title-light' : 'link-title-dark'}`}>
                    {link.label}
                  </span>
                  <span className={`link-sub ${link.highlight ? 'link-sub-light' : 'link-sub-dark'}`}>
                    {link.sublabel}
                  </span>
                </span>
                {link.badge && (
                  <span className={`link-badge ${
                    link.highlight ? 'link-badge-wine' :
                    link.badge === 'BEST VALUE' ? 'link-badge-green' :
                    'link-badge-gold'
                  }`}>
                    {link.badge}
                  </span>
                )}
                <svg className={`link-arrow ${link.highlight ? 'link-arrow-light' : 'link-arrow-dark'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </a>
            ))}
          </div>

          {/* Divider */}
          <div className="divider">
            <div className="divider-line" />
            <span className="divider-text">Find me here</span>
            <div className="divider-line" />
          </div>

          {/* Social icons */}
          <div className="social-grid">
            {socialLinks.map((s) => (
              <a key={s.href} href={s.href} target="_blank" rel="noopener noreferrer" aria-label={s.label} className="social-btn">
                <svg viewBox="0 0 24 24" fill="currentColor" style={{ width: 18, height: 18 }}>
                  <path d={s.icon} />
                </svg>
              </a>
            ))}
          </div>

          {/* Footer */}
          <div className="links-footer">
            <p className="footer-copy">© Six & Thriving · Real support for real parents</p>
            <a href="https://sixandthriving.com" className="footer-link">sixandthriving.com</a>
          </div>

        </div>
      </div>
    </>
  );
}
