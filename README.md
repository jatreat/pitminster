# Friends of Pitminster — pitminsterchurchonline.org

A static community site about the church of St Andrew & St Mary, the village of Pitminster, and the families who sailed from it, with a moderated family wall, a contact form, and the family's games.

Running cost: the domain renewal only. Hosting, the database, the spam check and the forms all run on Cloudflare's free tier.

## What is here

```
public/            the website (plain HTML, CSS, JS, images) — this is what gets published
  index.html       front page
  church.html      the church
  village.html     the village
  across.html      the Treats and the village's other American connections
  games.html       the games page
  games/           treatopoly.html, treat-trail.html
  wall.html        the family wall (moderated)
  visit.html       visiting, services, giving
  contact.html     contact form
  about.html       about, sources, photo credits, privacy
  admin.html       editors' desk: approve notes, read messages (needs the editors' key)
  assets/          site.css, site.js, bear.svg, favicon.svg
  images/          photographs (CC BY-SA 2.0; see images/CREDITS.md)
functions/api/     the family wall, contact form and admin API (Cloudflare Pages Functions)
schema.sql         the database tables
wrangler.toml.example  Cloudflare settings for reference (bindings and secrets are set in the dashboard)
tools/build.py     rebuilds the pages from the shared header/footer (optional; the HTML can also be edited directly)
extras/            the 3D game and the untouched original of the trail game, kept out of the site but not thrown away
```

## Deploying, step by step

1. **Put it on GitHub.** Create a repository (for example `jatreat/pitminster`) and push this folder to it.

2. **Create the Cloudflare Pages project.** In the Cloudflare dashboard: Workers & Pages → Create → Pages → Connect to Git → pick the repository. Build settings: no build command; build output directory `public`. Deploy. You get a `*.pages.dev` address straight away.

3. **Create the database.** Workers & Pages → D1 → Create database, named `pitminster`. Open it, go to Console, paste the contents of `schema.sql` and run it. Bind it in the dashboard: Pages project → Settings → Bindings → add D1 binding with variable name `DB`.

4. **Set the editors' key.** Pages project → Settings → Variables and Secrets → add a secret `ADMIN_KEY` with a long random string (a password manager will make one). That string is what you type into `admin.html` to approve notes. Redeploy once after adding bindings and secrets.

5. **Turn on the spam check (optional but worth it).** Turnstile → Add site → domain `pitminsterchurchonline.org` (and `pitminster.pages.dev` while testing) → Managed. Put the site key in `public/assets/site.js` (`TURNSTILE_SITE_KEY`) and the secret key as a Pages secret `TURNSTILE_SECRET`. Without it the forms still work, protected by the honeypot and a rate limit of five posts an hour per address.

6. **Point the domain.** Pages project → Custom domains → add `pitminsterchurchonline.org` and `www.pitminsterchurchonline.org`. The cleanest route is to move the domain's nameservers from GoDaddy to Cloudflare (free; Cloudflare shows the two nameservers to paste into GoDaddy's DNS settings). That also lets you create a free email address such as `friends@pitminsterchurchonline.org` that forwards to your inbox (Email → Email Routing). If you would rather leave DNS at GoDaddy, add the CNAME records Cloudflare shows you instead.

7. **Check GoDaddy is not still billing a lapsed site plan.** Only the domain itself needs to stay.

## Moderating the wall

Open `/admin.html`, enter the editors' key. "Waiting" lists new notes; approve or delete each one. "On the wall" lets you take a note down. "Messages" shows contact-form messages with the sender's email. The page remembers the key only for the browser tab.

Nothing posts to the wall without approval, so there is no rush; check it when you think of it. (A later improvement: an email to you when a note arrives, via Cloudflare Email Workers or Resend's free tier.)

## Updating content

Every page is plain HTML in `public/`. Edit, commit, push; Cloudflare republishes in about a minute. If you edit the shared header or footer, change them in `tools/build.py` and run `python3 tools/build.py` so every page gets it.

Treatopoly's online play uses PeerJS's free public signalling server; if that ever goes away, the game still works on one device.

To swap in your own photographs: replace the files in `public/images/` keeping the same names (640 px wide is plenty), and change the credits in `about.html` and the captions where they appear.

## Still to do before it is "finished"

- Get the parish's online giving link from the PCC and put it in `visit.html` (the box under "Giving to the church").
- Photographs of the Treat brass, the font and the east window (the site has none; Geograph had no interior shots other than the Coles tomb).
- Ask the vicar or a churchwarden to read the church page for errors.

