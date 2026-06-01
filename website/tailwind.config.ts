import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './content/**/*.{md,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        cream: '#FBF7F2',
        cream2: '#FFFAF6',
        blush: '#F4E5DF',
        blush2: '#F9EEEA',
        rose: '#B65D68',
        wine: '#951238',
        wine2: '#7B0F2E',
        ink: '#2B2022',
        cocoa: '#6E3A42',
        taupe: '#B9928F',
      },
      fontFamily: {
        serif: ['var(--font-fraunces)', 'Georgia', 'Cormorant Garamond', 'serif'],
        sans: ['var(--font-inter)', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 20px 60px rgba(80, 34, 42, 0.10)',
        card: '0 14px 40px rgba(80, 34, 42, 0.08)',
      },
      maxWidth: {
        prose: '46rem',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        floatBadge: {
          '0%,100%': { transform: 'translateY(0) rotate(-2deg)' },
          '50%': { transform: 'translateY(-10px) rotate(2deg)' },
        },
      },
      animation: {
        'fade-up': 'fadeUp .9s ease both',
        'fade-in': 'fadeIn 1.1s ease both',
        'float-badge': 'floatBadge 4.8s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};

export default config;
