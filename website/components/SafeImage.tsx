'use client';

import { useState } from 'react';

interface Props {
  src: string;
  alt: string;
  className?: string;
  fallbackClassName?: string;
}

/**
 * A plain <img> that gracefully hides itself if the source fails to load.
 * Used for optional imagery (covers, photos) that may not exist yet locally.
 */
export default function SafeImage({ src, alt, className }: Props) {
  const [failed, setFailed] = useState(false);

  if (failed) {
    return <div className={`${className ?? ''} bg-blush2`} aria-hidden="true" />;
  }

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={src}
      alt={alt}
      className={className}
      loading="lazy"
      onError={() => setFailed(true)}
    />
  );
}
