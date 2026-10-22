/* Friends of Pitminster — page behaviour
   The wall and the contact form talk to /api/* (Cloudflare Pages Functions).
   When the API is not there (a local preview, or a static host), the pages
   still read correctly: example notes stay, and forms explain themselves. */
(function () {
  "use strict";

  // Set this to your Turnstile site key once Turnstile is configured in Cloudflare.
  // Leave it empty and no challenge is shown (the server then relies on the
  // honeypot and rate limit only).
  var TURNSTILE_SITE_KEY = "";

  var API = "api";

  function $(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function fmtDate(iso) {
    try {
      var d = new Date(iso);
      if (isNaN(d.getTime())) return "";
      return d.toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
    } catch (e) { return ""; }
  }

  function renderPost(p) {
    var meta = [];
    if (p.place) meta.push(esc(p.place));
    var when = fmtDate(p.created_at);
    if (when) meta.push(when);
    return '<article class="post">' +
      '<header><b>' + esc(p.name) + '</b>' + (meta.length ? '<span>' + meta.join(" · ") + '</span>' : "") + '</header>' +
      (p.connection ? '<p class="small muted" style="margin-bottom:.4rem">' + esc(p.connection) + '</p>' : "") +
      '<p>' + esc(p.message) + '</p>' +
      '</article>';
  }

  function notice(el, kind, text) {
    if (!el) return;
    el.className = "notice " + kind;
    el.textContent = text;
    el.hidden = false;
  }

  function turnstileToken(container) {
    if (!container || !TURNSTILE_SITE_KEY || !window.turnstile) return null;
    var inp = container.querySelector('input[name="cf-turnstile-response"]');
    return inp ? inp.value : null;
  }

  function mountTurnstile(container) {
    if (!container || !TURNSTILE_SITE_KEY) return;
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async = true;
    s.onload = function () {
      try { window.turnstile.render(container, { sitekey: TURNSTILE_SITE_KEY }); } catch (e) { /* no widget */ }
    };
    document.head.appendChild(s);
  }

  // ---------------------------------------------------------------- the wall
  function loadWall(listEl, emptyEl, limit) {
    if (!listEl) return;
    fetch(API + "/posts?limit=" + (limit || 50), { headers: { Accept: "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error("api"); return r.json(); })
      .then(function (data) {
        var posts = (data && data.posts) || [];
        if (!posts.length) {
          if (emptyEl) { listEl.innerHTML = ""; emptyEl.hidden = false; }
          return; // on the home page the examples stay
        }
        listEl.innerHTML = posts.map(renderPost).join("");
        if (emptyEl) emptyEl.hidden = true;
      })
      .catch(function () { /* preview or static host: examples stay */ });
  }

  function wireWallForm() {
    var form = $("wall-form");
    if (!form) return;
    mountTurnstile($("w-turnstile"));
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var n = $("w-notice");
      var name = $("w-name").value.trim(), msg = $("w-msg").value.trim();
      if (!name || !msg) { notice(n, "err", "A name and a note are both needed."); return; }
      var body = {
        name: name, place: $("w-place").value.trim(), connection: $("w-conn").value.trim(),
        message: msg, email: $("w-email").value.trim(), website: $("w-web").value,
        token: turnstileToken($("w-turnstile"))
      };
      $("w-submit").disabled = true;
      fetch(API + "/posts", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); })
        .then(function (res) {
          if (res.ok) {
            notice(n, "ok", "Thank you. Your note is in the queue and will appear once an editor has read it.");
            form.reset();
          } else {
            notice(n, "err", (res.j && res.j.error) || "The note could not be posted. Try again in a few minutes.");
          }
        })
        .catch(function () {
          notice(n, "err", "Posting is not switched on in this preview. It works once the site is live at pitminsterchurchonline.org.");
        })
        .then(function () { $("w-submit").disabled = false; });
    });
  }

  // ------------------------------------------------------------- contact form
  function wireContactForm() {
    var form = $("contact-form");
    if (!form) return;
    mountTurnstile($("c-turnstile"));
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var n = $("c-notice");
      var name = $("c-name").value.trim(), email = $("c-email").value.trim(), msg = $("c-msg").value.trim();
      if (!name || !email || !msg) { notice(n, "err", "Name, email and a message are all needed."); return; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { notice(n, "err", "That email address does not look right."); return; }
      $("c-submit").disabled = true;
      fetch(API + "/contact", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, email: email, message: msg, website: $("c-web").value, token: turnstileToken($("c-turnstile")) }) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok) { notice(n, "ok", "Sent. The editors will reply to the address you gave."); form.reset(); }
          else notice(n, "err", (res.j && res.j.error) || "The message could not be sent. Try again in a few minutes.");
        })
        .catch(function () {
          notice(n, "err", "Sending is not switched on in this preview. It works once the site is live at pitminsterchurchonline.org.");
        })
        .then(function () { $("c-submit").disabled = false; });
    });
  }

  // ------------------------------------------------------------------ admin
  function wireAdmin() {
    var login = $("admin-login");
    if (!login) return;
    var desk = $("admin-desk"), list = $("admin-list"), n = $("a-notice");
    var key = "";
    try { key = sessionStorage.getItem("pit-editor-key") || ""; } catch (e) { key = ""; }
    var tab = "pending";

    function api(method, params, body) {
      var url = API + "/admin" + (params ? "?" + params : "");
      return fetch(url, { method: method, headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" }, body: body ? JSON.stringify(body) : undefined })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); });
    }

    function row(item, kind) {
      var acts = "";
      if (kind === "pending") acts = '<button data-act="approve" data-id="' + item.id + '">Approve</button><button data-act="delete" data-id="' + item.id + '">Delete</button>';
      else if (kind === "approved") acts = '<button data-act="unapprove" data-id="' + item.id + '">Take down</button><button data-act="delete" data-id="' + item.id + '">Delete</button>';
      else acts = '<button data-act="delete-message" data-id="' + item.id + '">Delete</button>';
      var head = '<b>' + esc(item.name) + '</b> <span class="muted small">' + esc(item.place || "") + (item.email ? " · " + esc(item.email) : "") + " · " + esc(fmtDate(item.created_at)) + '</span>' +
        (item.connection ? '<div class="small muted">' + esc(item.connection) + '</div>' : "");
      return '<div class="admin-row"><div>' + head + '<p style="white-space:pre-line;overflow-wrap:anywhere">' + esc(item.message) + '</p></div><div class="acts">' + acts + '</div></div>';
    }

    function load() {
      var params = tab === "messages" ? "what=messages" : "what=posts&status=" + tab;
      list.innerHTML = '<p class="muted">Loading…</p>';
      api("GET", params).then(function (res) {
        if (!res.ok) { throw new Error(res.j && res.j.error ? res.j.error : "Could not load"); }
        var items = res.j.items || [];
        if (!items.length) { list.innerHTML = '<p class="muted">Nothing here.</p>'; return; }
        list.innerHTML = items.map(function (it) { return row(it, tab); }).join("");
      }).catch(function (e) {
        list.innerHTML = '<p class="notice err">' + esc(e.message) + '</p>';
      });
    }

    function open() {
      login.hidden = true; desk.hidden = false; load();
    }

    login.addEventListener("submit", function (ev) {
      ev.preventDefault();
      key = $("a-key").value.trim();
      if (!key) { notice(n, "err", "Enter the editors' key."); return; }
      api("GET", "what=posts&status=pending&limit=1").then(function (res) {
        if (res.ok) {
          try { sessionStorage.setItem("pit-editor-key", key); } catch (e) { /* fine */ }
          open();
        } else if (res.status === 401) notice(n, "err", "That key was not accepted.");
        else notice(n, "err", "The desk is not switched on in this preview. It works once the site is live with its database.");
      }).catch(function () {
        notice(n, "err", "The desk is not switched on in this preview. It works once the site is live with its database.");
      });
    });

    desk.querySelector(".tabs").addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-tab]");
      if (!b) return;
      tab = b.getAttribute("data-tab");
      desk.querySelectorAll(".tabs button").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
      load();
    });

    list.addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-act]");
      if (!b) return;
      var act = b.getAttribute("data-act"), id = Number(b.getAttribute("data-id"));
      if (act.indexOf("delete") === 0 && b.textContent !== "Really delete") { b.textContent = "Really delete"; return; }
      b.disabled = true;
      api("POST", null, { action: act, id: id }).then(function (res) {
        if (!res.ok) throw new Error(res.j && res.j.error ? res.j.error : "Failed");
        load();
      }).catch(function (e) { list.insertAdjacentHTML("afterbegin", '<p class="notice err">' + esc(e.message) + '</p>'); b.disabled = false; });
    });

    $("a-logout").addEventListener("click", function () {
      key = ""; try { sessionStorage.removeItem("pit-editor-key"); } catch (e) { /* fine */ }
      desk.hidden = true; login.hidden = false; $("a-key").value = "";
    });

    if (key) open();
  }

  document.addEventListener("DOMContentLoaded", function () {
    loadWall($("wall"), $("wall-empty"), 50);
    loadWall($("home-wall"), null, 3);
    wireWallForm();
    wireContactForm();
    wireAdmin();
  });
})();
