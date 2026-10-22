// POST /api/contact -> stores a message for the editors
import { json, clean, ipHash, verifyTurnstile, tooMany } from "../_lib.js";

export async function onRequestPost({ request, env }) {
  if (!env.DB) return json({ error: "The contact form's database is not set up yet." }, 503);
  let body;
  try { body = await request.json(); } catch (e) { return json({ error: "Bad request." }, 400); }
  if (clean(body.website, 10)) return json({ ok: true });

  const name = clean(body.name, 80);
  const email = clean(body.email, 120);
  const message = clean(body.message, 3000);
  if (!name || !email || !message) return json({ error: "Name, email and a message are all needed." }, 400);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ error: "That email address does not look right." }, 400);

  if (!(await verifyTurnstile(env, body.token, request))) return json({ error: "The spam check did not pass. Reload the page and try again." }, 400);

  const hash = await ipHash(request);
  if (await tooMany(env, "messages", hash, 5)) return json({ error: "Too many messages from this connection. Try again later." }, 429);

  await env.DB.prepare("INSERT INTO messages (name, email, message, ip_hash) VALUES (?1, ?2, ?3, ?4)")
    .bind(name, email, message, hash).run();

  return json({ ok: true }, 201);
}
