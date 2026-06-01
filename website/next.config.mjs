/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'images.unsplash.com' },
      { protocol: 'https', hostname: 'payhip.com' },
      { protocol: 'https', hostname: 'assets.mailerlite.com' },
    ],
    formats: ['image/avif', 'image/webp'],
  },
  async redirects() {
    return [
      { source: '/sleep-guide', destination: '/free-sleep-guide', permanent: true },
    ];
  },
};

export default nextConfig;
