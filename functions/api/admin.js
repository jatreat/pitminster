// Editors' desk. Every call carries  Authorization: Bearer <ADMIN_KEY>.
// GET  /api/admin?what=posts&status=pending|approved&limit=100
// GET  /api/admin?what=messages
// POST /api/admin  { action: approve|unapprove|delete|delete-message, id }
import { json } from "../_lib.js";

function authed(request, env) {
  const h = request.headers.get("Authorization") || "";
  const key = h.startsWith("Bearer ") ? h.slice(7).trim() : "";
  if (!env.ADMIN_KEY || !key) return false;
  // constant-time-ish compare
  if (key.length !== env.ADMIN_KEY.length) return false;
  let diff = 0;
  for (let i = 0; i < key.length; i++) diff |= key.charCodeAt(i) ^ env.ADMIN_KEY.charCodeAt(i);
  return diff === 0;
}

export async function onRequestGet({ request, env }) {
  if (!env.DB || !env.ADMIN_KEY) return json({ error: "The desk is not configured (DB binding or ADMIN_KEY missing)." }, 503);
  if (!authed(request, env)) return json({ error: "Not authorised." }, 401);
  const url = new URL(request.url);
  const what = url.searchParams.get("what") || "posts";
  const limit = Math.min(200, Math.max(1, parseInt(url.searchParams.get("limit") || "100", 10) || 100));
  if (what === "messages") {
    const { results } = await env.DB.prepare("SELECT id, created_at, name, email, message FROM messages ORDER BY created_at DESC LIMIT ?1").bind(limit).all();
    return json({ items: results || [] });
  }
  const status = url.searchParams.get("status") === "approved" ? "approved" : "pending";
  const { results } = await env.DB.prepare(
    "SELECT id, created_at, name, place, connection, message, email FROM posts WHERE status = ?1 ORDER BY created_at DESC LIMIT ?2"
  ).bind(status, limit).all();
  return json({ items: results || [] });
}

export async function onRequestPost({ request, env }) {
  if (!env.DB || !env.ADMIN_KEY) return json({ error: "The desk is not configured." }, 503);
  if (!authed(request, env)) return json({ error: "Not authorised." }, 401);
  let body;
  try { body = await request.json(); } catch (e) { return json({ error: "Bad request." }, 400); }
  const id = Number(body.id);
  if (!Number.isInteger(id) || id <= 0) return json({ error: "Bad id." }, 400);
  switch (body.action) {
    case "approve":
      await env.DB.prepare("UPDATE posts SET status = 'approved' WHERE id = ?1").bind(id).run(); break;
    case "unapprove":
      await env.DB.prepare("UPDATE posts SET status = 'pending' WHERE id = ?1").bind(id).run(); break;
    case "delete":
      await env.DB.prepare("DELETE FROM posts WHERE id = ?1").bind(id).run(); break;
    case "delete-message":
      await env.DB.prepare("DELETE FROM messages WHERE id = ?1").bind(id).run(); break;
    default:
      return json({ error: "Unknown action." }, 400);
  }
  return json({ ok: true });
}
