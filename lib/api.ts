const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || '';

export async function sendChatMessage(message: string) {
  const res = await fetch(`${baseUrl}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    throw new Error(`Failed to send message: ${res.statusText}`);
  }

  return res.json();
}
