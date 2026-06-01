import { StarIcon } from './icons';

export interface Testimonial {
  name: string;
  role?: string;
  quote: string;
  rating?: number;
}

export default function TestimonialCard({ testimonial }: { testimonial: Testimonial }) {
  const rating = testimonial.rating ?? 5;
  return (
    <figure className="flex h-full flex-col rounded-3xl border border-rose/10 bg-white/85 p-8 shadow-card backdrop-blur transition duration-300 hover:-translate-y-1 hover:shadow-soft">
      <div className="flex gap-1 text-rose" aria-label={`${rating} out of 5 stars`}>
        {Array.from({ length: rating }).map((_, i) => (
          <StarIcon key={i} className="h-5 w-5" />
        ))}
      </div>
      <blockquote className="mt-5 flex-1 text-[15px] leading-7 text-ink/80">
        “{testimonial.quote}”
      </blockquote>
      <figcaption className="mt-6 border-t border-rose/10 pt-5">
        <p className="font-serif text-lg font-semibold text-wine2">{testimonial.name}</p>
        {testimonial.role && <p className="text-xs text-ink/55">{testimonial.role}</p>}
      </figcaption>
    </figure>
  );
}
