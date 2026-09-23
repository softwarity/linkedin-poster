# linkedin-poster

Publie des posts sur le profil LinkedIn personnel de François Achache pour faire connaître les projets Softwarity (plug, Meerkat, Halcyon…), **après validation dans Slack**.

```
Tâche Claude hebdo ──POST /drafts──▶ Worker ──▶ Slack #linkedin-posts  [Publier] [Rejeter]
                                        │                   │
                                        │◀── clic Publier ──┘
                                        └──▶ LinkedIn (profil perso)
```

Le Worker Cloudflare garde le token LinkedIn et ne le transmet jamais. Il ne publie qu'un brouillon validé dans Slack.

## Routes

| Route | Accès | Rôle |
| --- | --- | --- |
| `GET /authorize` | navigateur | Connexion (ou reconnexion) à LinkedIn |
| `GET /callback` | LinkedIn | Retour OAuth, enregistre le token |
| `POST /drafts` | `Authorization: Bearer <WORKER_SHARED_SECRET>` | Envoie un brouillon `{"text": "...", "project": "plug"}` dans Slack |
| `GET /status` | `Authorization: Bearer <WORKER_SHARED_SECRET>` | État du token (`connected`, `days_left`) |
| `POST /slack/interactions` | Slack (requête signée) | Boutons Publier / Rejeter |

Seuls les utilisateurs Slack listés dans `SLACK_APPROVERS` (`wrangler.toml`) peuvent publier.

## ⚠️ Reconnexion tous les 60 jours

LinkedIn ne fournit pas de refresh token aux apps self-serve : **le token expire au bout de 60 jours**. Il faut alors rouvrir `<WORKER_URL>/authorize` dans un navigateur. Tant que ce n'est pas fait, les posts approuvés ne partent pas.

Pour ne pas oublier, le Worker poste chaque jour un rappel dans `#linkedin-posts`, avec le lien, dès qu'il reste 7 jours ou moins.

## Installation

### 1. App LinkedIn (developer.linkedin.com → app « Softwarity »)

- **Products** : activer *Share on LinkedIn* et *Sign In with LinkedIn using OpenID Connect* (sans lui, le Worker ne peut pas identifier le profil auteur).
- **Auth → Authorized redirect URLs** : `<WORKER_URL>/callback`

### 2. App Slack

Créer l'app depuis [`slack-manifest.yml`](slack-manifest.yml) en remplaçant `<WORKER_URL>`, puis l'installer dans le workspace.

### 3. Secrets Cloudflare

```bash
npm install
npx wrangler login
npx wrangler secret put LINKEDIN_CLIENT_ID       # app LinkedIn → Auth
npx wrangler secret put LINKEDIN_CLIENT_SECRET   # app LinkedIn → Auth
npx wrangler secret put SLACK_BOT_TOKEN          # app Slack → OAuth & Permissions (xoxb-…)
npx wrangler secret put SLACK_SIGNING_SECRET     # app Slack → Basic Information
openssl rand -hex 32 | tee /dev/stderr | npx wrangler secret put WORKER_SHARED_SECRET
```

Garder `WORKER_SHARED_SECRET` dans le coffre de mots de passe : c'est lui qui permet d'envoyer des brouillons.

### 4. Déploiement

- À la main : `npm run deploy`
- Automatique : à chaque push sur `main` (GitHub Actions). Il faut les secrets de dépôt `CLOUDFLARE_API_TOKEN` (token Cloudflare créé avec le modèle *Edit Cloudflare Workers*) et `CLOUDFLARE_ACCOUNT_ID`.

### 5. Première connexion

Ouvrir `<WORKER_URL>/authorize` et accepter. Le premier compte LinkedIn connecté devient le propriétaire : aucun autre compte ne pourra ensuite prendre sa place. Pour changer de propriétaire, supprimer la clé `owner_sub` du KV `linkedin-softwarity-tokens`.

## Tester

```bash
curl -X POST "$WORKER_URL/drafts" \
  -H "Authorization: Bearer $WORKER_SHARED_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"project": "plug", "text": "Test de publication #plug"}'
```

Le brouillon apparaît dans `#linkedin-posts`. `npm run logs` affiche les logs du Worker en direct.

## Maintenance

`LINKEDIN_VERSION` (`wrangler.toml`) est la version de l'API LinkedIn. Chaque version reste supportée environ un an : à mettre à jour si LinkedIn répond qu'elle a été retirée.
