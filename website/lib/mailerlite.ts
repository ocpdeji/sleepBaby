const API_BASE = 'https://connect.mailerlite.com/api';

interface SubscribeOptions {
  email: string;
  name?: string;
  groupId?: string;
  fields?: Record<string, string>;
}

interface MailerLiteResult {
  ok: boolean;
  status: number;
  message?: string;
}

/**
 * Subscribe (or upsert) a contact in MailerLite via API v2 (Connect).
 * Used server-side only — never expose MAILERLITE_API_KEY to the client.
 */
export async function subscribe({
  email,
  name,
  groupId,
  fields,
}: SubscribeOptions): Promise<MailerLiteResult> {
  const apiKey = process.env.MAILERLITE_API_KEY;
  if (!apiKey) {
    return { ok: false, status: 500, message: 'MailerLite API key not configured.' };
  }

  const body: Record<string, unknown> = {
    email,
    fields: { ...(name ? { name } : {}), ...(fields ?? {}) },
  };
  if (groupId) body.groups = [groupId];

  try {
    const res = await fetch(`${API_BASE}/subscribers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
    });

    if (res.ok) return { ok: true, status: res.status };

    const data = await res.json().catch(() => ({}));
    return {
      ok: false,
      status: res.status,
      message: data?.message ?? 'Subscription failed. Please try again.',
    };
  } catch {
    return { ok: false, status: 500, message: 'Network error. Please try again.' };
  }
}

export const CHEATSHEET_GROUP_ID = process.env.MAILERLITE_CHEATSHEET_GROUP_ID;
export const WEBSITE_GROUP_ID = process.env.MAILERLITE_WEBSITE_GROUP_ID;
