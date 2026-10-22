-- Friends of Pitminster: D1 database schema.
-- Apply once:  npx wrangler d1 execute pitminster --remote --file=schema.sql
-- (or paste into the D1 console in the Cloudflare dashboard)

CREATE TABLE IF NOT EXISTS posts (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  name        TEXT NOT NULL,
  place       TEXT,
  connection  TEXT,
  message     TEXT NOT NULL,
  email       TEXT,
  ip_hash     TEXT,
  status      TEXT NOT NULL DEFAULT 'pending'   -- pending | approved
);
CREATE INDEX IF NOT EXISTS posts_status_created ON posts (status, created_at);
CREATE INDEX IF NOT EXISTS posts_ip_created ON posts (ip_hash, created_at);

CREATE TABLE IF NOT EXISTS messages (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  name        TEXT NOT NULL,
  email       TEXT NOT NULL,
  message     TEXT NOT NULL,
  ip_hash     TEXT
);
CREATE INDEX IF NOT EXISTS messages_ip_created ON messages (ip_hash, created_at);
