import { createClient, type SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? '';

/**
 * Browser/client-side Supabase client (anon key, respects RLS).
 * Safe to use in client components and the admin login flow.
 */
export function createBrowserClient(): SupabaseClient {
  return createClient(supabaseUrl, supabaseAnonKey, {
    auth: { persistSession: true, autoRefreshToken: true },
  });
}

/**
 * Server-side admin client (service role key — bypasses RLS).
 * NEVER import this into a client component. Server routes / actions only.
 */
export function createServiceClient(): SupabaseClient {
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY ?? '';
  return createClient(supabaseUrl, serviceKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}

export const isSupabaseConfigured = Boolean(supabaseUrl && supabaseAnonKey);
