// GET  /api/posts?limit=50   -> approved notes, newest first
// POST /api/posts            -> a new note, held for moderation
import { json, clean, ipHash, verifyTurnstile, tooMany } from "../_lib.js";

export async function onRequestGet({ request, env }) {
  if (!env.DB) return json({ error: "The wall's database is not set up yet." }, 503);
  const url = new URL(request.url);
  const limit = Math.min(100, Math.max(1, parseInt(url.searchParams.get("limit") || "50", 10) || 50));
  const { results } = await env.DB.prepare(
    "SELECT id, created_at, name, place, connection, message FROM posts WHERE status = 'approved' ORDER BY created_at DESC LIMIT ?1"
  ).bind(limit).all();
  return json({ posts: results || [] }, 200, { "Cache-Control": "public, max-age=60" });
}

export async function onRequestPost({ request, env }) {
  if (!env.DB) return json({ error: "The wall's database is not set up yet." }, 503);
  let body;
  try { body = await request.json(); } catch (e) { return json({ error: "Bad request." }, 400); }

  // Honeypot: real people never fill the hidden field.
  if (clean(body.website, 10)) return json({ ok: true, queued: true });

  const name = clean(body.name, 80);
  const place = clean(body.place, 80);
  const connection = clean(body.connection, 120);
  const message = clean(body.message, 1200);
  const email = clean(body.email, 120);
  if (!name || !message) return json({ error: "A name and a note are both needed." }, 400);
  if (message.length < 3) return json({ error: "The note is too short." }, 400);
  if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ error: "That email address does not look right." }, 400);
  if ((message.match(/https?:\/\//g) || []).length > 2) return json({ error: "Please keep links to a minimum." }, 400);

  if (!(await verifyTurnstile(env, body.token, request))) return json({ error: "The spam check did not pass. Reload the page and try again." }, 400);

  const hash = await ipHash(request);
  if (await tooMany(env, "posts", hash, 5)) return json({ error: "Too many notes from this connection. Try again later." }, 429);

  await env.DB.prepare(
    "INSERT INTO posts (name, place, connection, message, email, ip_hash, status) VALUES (?1, ?2, ?3, ?4, ?5, ?6, 'pending')"
  ).bind(name, place, connection, message, email, hash).run();

  return json({ ok: true, queued: true }, 201);
}
