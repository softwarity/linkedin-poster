// LinkedIn poster — Cloudflare Worker.
// Holds the LinkedIn token (never exposed), sends drafts to Slack for approval,
// publishes approved drafts on the owner's personal profile.

const LI_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization";
const LI_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken";
const LI_USERINFO_URL = "https://api.linkedin.com/v2/userinfo";
const LI_POSTS_URL = "https://api.linkedin.com/rest/posts";
const LI_SCOPES = "openid profile w_member_social"; // openid/profile: needed to know the author URN
const LI_MAX_LENGTH = 3000;

const KEY_TOKEN = "linkedin_token";
const KEY_OWNER = "owner_sub"; // first account connected; later connections must match it
const KEY_ORIGIN = "origin"; // Worker public URL, for links sent by the cron
const DRAFT_TTL = 30 * 86400;
const EXPIRY_WARNING_DAYS = 7;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const route = `${request.method} ${url.pathname}`;
    try {
      switch (route) {
        case "GET /authorize":
          return await authorize(url, env);
        case "GET /callback":
          return await callback(url, env);
        case "GET /status":
          return (await isBearerValid(request, env)) ? json(await tokenStatus(env)) : json({ error: "unauthorized" }, 401);
        case "POST /drafts":
          return (await isBearerValid(request, env)) ? await createDraft(request, env) : json({ error: "unauthorized" }, 401);
        case "POST /slack/interactions":
          return await slackInteraction(request, env, ctx);
        default:
          return json({ error: "not_found" }, 404);
      }
    } catch (err) {
      console.error(err);
      return json({ error: "internal_error", message: err.message }, 500);
    }
  },

  async scheduled(_event, env, ctx) {
    ctx.waitUntil(warnIfTokenExpiring(env));
  },
};

// ---------- LinkedIn OAuth ----------

async function authorize(url, env) {
  const state = crypto.randomUUID();
  await env.TOKENS.put(`state:${state}`, "1", { expirationTtl: 600 });
  await env.TOKENS.put(KEY_ORIGIN, url.origin);
  const params = new URLSearchParams({
    response_type: "code",
    client_id: env.LINKEDIN_CLIENT_ID,
    redirect_uri: `${url.origin}/callback`,
    state,
    scope: LI_SCOPES,
  });
  return Response.redirect(`${LI_AUTH_URL}?${params}`, 302);
}

async function callback(url, env) {
  const error = url.searchParams.get("error");
  if (error) return page(`Connexion refusée : ${error} — ${url.searchParams.get("error_description") || ""}`, 400);

  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  if (!code || !state || !(await env.TOKENS.get(`state:${state}`))) {
    return page("Lien expiré ou invalide. Relance /authorize.", 400);
  }
  await env.TOKENS.delete(`state:${state}`);

  const res = await fetch(LI_TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: `${url.origin}/callback`,
      client_id: env.LINKEDIN_CLIENT_ID,
      client_secret: env.LINKEDIN_CLIENT_SECRET,
    }),
  });
  const data = await res.json();
  if (!res.ok || !data.access_token) return page(`Échec de l'échange du code : ${JSON.stringify(data)}`, 502);

  const me = await fetch(LI_USERINFO_URL, { headers: { Authorization: `Bearer ${data.access_token}` } });
  const { sub } = me.ok ? await me.json() : {};
  if (!sub) return page("Impossible de lire le profil LinkedIn : le produit « Sign In with LinkedIn using OpenID Connect » est-il activé sur l'app ?", 502);

  const owner = await env.TOKENS.get(KEY_OWNER);
  if (owner && owner !== sub) return page("Ce compte LinkedIn n'est pas celui du propriétaire de ce Worker.", 403);
  if (!owner) await env.TOKENS.put(KEY_OWNER, sub);

  const record = {
    access_token: data.access_token,
    expires_at: new Date(Date.now() + data.expires_in * 1000).toISOString(),
    person_urn: `urn:li:person:${sub}`,
  };
  await env.TOKENS.put(KEY_TOKEN, JSON.stringify(record), { expirationTtl: data.expires_in });
  return page(`Connecté ✔ — token valable jusqu'au ${record.expires_at.slice(0, 10)}.`);
}

async function tokenStatus(env) {
  const raw = await env.TOKENS.get(KEY_TOKEN);
  if (!raw) return { connected: false };
  const { expires_at, person_urn } = JSON.parse(raw);
  return { connected: true, expires_at, days_left: daysUntil(expires_at), person_urn };
}

// ---------- Drafts & Slack approval ----------

async function createDraft(request, env) {
  const { text, project } = await request.json().catch(() => ({}));
  if (typeof text !== "string" || !text.trim()) return json({ error: "text_required" }, 400);
  if (text.length > LI_MAX_LENGTH) return json({ error: "text_too_long", max: LI_MAX_LENGTH }, 400);

  const draft = { id: crypto.randomUUID(), text, project: project || null, status: "pending", created_at: new Date().toISOString() };
  await saveDraft(env, draft);
  const res = await slackApi(env, "chat.postMessage", {
    channel: env.SLACK_CHANNEL_ID,
    text: `Brouillon LinkedIn${draft.project ? ` — ${draft.project}` : ""}`,
    blocks: draftBlocks(draft),
  });

  const status = await tokenStatus(env);
  return json({ id: draft.id, slack_ts: res.ts, linkedin: status }, 201);
}

async function slackInteraction(request, env, ctx) {
  const body = await request.text();
  if (!(await isSlackSignatureValid(request, body, env))) return json({ error: "invalid_signature" }, 401);

  const payload = JSON.parse(new URLSearchParams(body).get("payload"));
  const action = payload.actions?.[0];
  if (payload.type !== "block_actions" || !action) return new Response("");

  // Slack wants an answer within 3 s: acknowledge now, work in the background.
  ctx.waitUntil(handleAction(env, action, payload).catch((err) => reply(payload.response_url, `⚠️ ${err.message}`)));
  return new Response("");
}

async function handleAction(env, action, payload) {
  const user = payload.user.id;
  const approvers = (env.SLACK_APPROVERS || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (approvers.length && !approvers.includes(user)) return reply(payload.response_url, "Tu n'es pas autorisé à valider les posts.");

  const draft = await loadDraft(env, action.value);
  if (!draft) return reply(payload.response_url, "Brouillon introuvable (expiré ?).");
  if (draft.status !== "pending") return reply(payload.response_url, `Brouillon déjà traité (${draft.status}).`);

  if (action.action_id === "reject") {
    Object.assign(draft, { status: "rejected", decided_by: user });
    await saveDraft(env, draft);
    return replaceMessage(payload.response_url, draft, `❌ Rejeté par <@${user}>`);
  }

  if (action.action_id === "approve") {
    Object.assign(draft, { status: "publishing", decided_by: user });
    await saveDraft(env, draft);
    try {
      draft.post_url = await publishOnLinkedIn(env, draft.text);
      draft.status = "published";
    } catch (err) {
      draft.status = "pending"; // allow a retry once the cause is fixed
      await saveDraft(env, draft);
      return reply(payload.response_url, `⚠️ Publication échouée : ${err.message}`);
    }
    await saveDraft(env, draft);
    return replaceMessage(payload.response_url, draft, `✅ Publié par <@${user}> — <${draft.post_url}|voir le post>`);
  }
}

function draftBlocks(draft, outcome) {
  const blocks = [
    { type: "header", text: { type: "plain_text", text: `Brouillon LinkedIn${draft.project ? ` — ${draft.project}` : ""}` } },
    { type: "section", text: { type: "plain_text", text: draft.text, emoji: true } },
  ];
  if (outcome) {
    blocks.push({ type: "context", elements: [{ type: "mrkdwn", text: outcome }] });
  } else {
    blocks.push({
      type: "actions",
      elements: [
        {
          type: "button",
          action_id: "approve",
          style: "primary",
          text: { type: "plain_text", text: "Publier" },
          value: draft.id,
          confirm: {
            title: { type: "plain_text", text: "Publier sur LinkedIn ?" },
            text: { type: "plain_text", text: "Le post sera publié immédiatement sur ton profil." },
            confirm: { type: "plain_text", text: "Publier" },
            deny: { type: "plain_text", text: "Annuler" },
          },
        },
        { type: "button", action_id: "reject", style: "danger", text: { type: "plain_text", text: "Rejeter" }, value: draft.id },
      ],
    });
  }
  return blocks;
}

async function saveDraft(env, draft) {
  await env.TOKENS.put(`draft:${draft.id}`, JSON.stringify(draft), { expirationTtl: DRAFT_TTL });
}

async function loadDraft(env, id) {
  const raw = await env.TOKENS.get(`draft:${id}`);
  return raw ? JSON.parse(raw) : null;
}

// ---------- LinkedIn publishing ----------

async function publishOnLinkedIn(env, text) {
  const raw = await env.TOKENS.get(KEY_TOKEN);
  if (!raw) throw new Error("pas de token LinkedIn, reconnecte-toi via /authorize");
  const { access_token, person_urn } = JSON.parse(raw);

  const res = await fetch(LI_POSTS_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${access_token}`,
      "LinkedIn-Version": env.LINKEDIN_VERSION,
      "X-Restli-Protocol-Version": "2.0.0",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      author: person_urn,
      commentary: toLittleText(text),
      visibility: "PUBLIC",
      distribution: { feedDistribution: "MAIN_FEED", targetEntities: [], thirdPartyDistributionChannels: [] },
      lifecycleState: "PUBLISHED",
      isReshareDisabledByAuthor: false,
    }),
  });
  if (res.status !== 201) throw new Error(`LinkedIn ${res.status} : ${await res.text()}`);
  return `https://www.linkedin.com/feed/update/${res.headers.get("x-restli-id")}/`;
}

// LinkedIn "little text": reserved characters must be escaped or the post gets truncated.
// A "#" directly followed by a word stays a hashtag.
function toLittleText(text) {
  return text.replace(/[\\|{}@\[\]()<>*_~]/g, "\\$&").replace(/#(?![\p{L}\p{N}])/gu, "\\#");
}

// ---------- Token expiry reminder (cron) ----------

async function warnIfTokenExpiring(env) {
  const status = await tokenStatus(env);
  if (status.connected && status.days_left > EXPIRY_WARNING_DAYS) return;
  const origin = await env.TOKENS.get(KEY_ORIGIN);
  const link = origin ? ` : <${origin}/authorize|se reconnecter>` : "";
  const text = status.connected
    ? `⚠️ Le token LinkedIn expire dans ${status.days_left} j${link}`
    : `⚠️ Aucun token LinkedIn valide, les posts ne peuvent pas être publiés${link}`;
  await slackApi(env, "chat.postMessage", { channel: env.SLACK_CHANNEL_ID, text });
}

// ---------- Slack helpers ----------

async function slackApi(env, method, body) {
  const res = await fetch(`https://slack.com/api/${method}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${env.SLACK_BOT_TOKEN}`, "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!data.ok) throw new Error(`Slack ${method} : ${data.error}`);
  return data;
}

function reply(responseUrl, text) {
  return postJson(responseUrl, { response_type: "ephemeral", replace_original: false, text });
}

function replaceMessage(responseUrl, draft, outcome) {
  return postJson(responseUrl, { replace_original: true, text: outcome, blocks: draftBlocks(draft, outcome) });
}

function postJson(url, body) {
  return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
}

async function isSlackSignatureValid(request, body, env) {
  const timestamp = request.headers.get("X-Slack-Request-Timestamp");
  const signature = request.headers.get("X-Slack-Signature") || "";
  if (!timestamp || Math.abs(Date.now() / 1000 - Number(timestamp)) > 300) return false;
  const key = await crypto.subtle.importKey("raw", encode(env.SLACK_SIGNING_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = await crypto.subtle.sign("HMAC", key, encode(`v0:${timestamp}:${body}`));
  const expected = "v0=" + [...new Uint8Array(mac)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return safeEqual(signature, expected);
}

// ---------- Generic helpers ----------

async function isBearerValid(request, env) {
  const provided = (request.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "");
  return !!env.WORKER_SHARED_SECRET && safeEqual(provided, env.WORKER_SHARED_SECRET);
}

function safeEqual(a, b) {
  const x = encode(a);
  const y = encode(b);
  return x.length === y.length && crypto.subtle.timingSafeEqual(x, y);
}

function encode(s) {
  return new TextEncoder().encode(s);
}

function daysUntil(iso) {
  return Math.floor((Date.parse(iso) - Date.now()) / 86_400_000);
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function page(message, status = 200) {
  const safe = String(message).replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
  return new Response(`<!doctype html><meta charset="utf-8"><title>LinkedIn poster</title><p>${safe}</p>`, {
    status,
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}
