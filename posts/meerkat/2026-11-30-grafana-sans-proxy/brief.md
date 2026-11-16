# Brief : Grafana derrière la gateway, sans proxy d'authentification

**But du post** : un cas concret qu'un tech lead reconnaît tout de suite. Un outil interne sans connexion à lui est protégé par un proxy d'authentification. On le remplace par une route Meerkat, et on gagne au passage les rôles, la règle d'accès et l'audit.

**Le cas d'usage** : Grafana est protégé par un proxy d'authentification, ou par une règle de forward-auth dans le reverse proxy. Le proxy connecte la personne et passe son nom dans un en-tête. Mais les rôles Grafana (Viewer, Editor, Admin) se gèrent à part, il y a un proxy par outil, et rien n'est au même endroit.

**Avec Meerkat**, la recette « Grafana, par en-têtes » de `docs/auth/connect-an-application.md` :
- **Côté Grafana**, quelques variables d'environnement. En citer deux ou trois telles quelles, sur leur propre ligne :

```
GF_AUTH_PROXY_ENABLED=true
GF_AUTH_PROXY_HEADER_NAME=X-WEBAUTH-USER
GF_AUTH_PROXY_HEADERS=Email:X-WEBAUTH-EMAIL Name:X-WEBAUTH-NAME Role:X-WEBAUTH-ROLE
```

- **Côté Meerkat**, une route sur `/grafana/**`. Dans **Identity**, chaque information va sous le nom d'en-tête que Grafana lit, avec le mécanisme **Headers**.
- **Le rôle Grafana est calculé à la porte** à partir des rôles de la personne. C'est le détail qui fait la différence ; le citer tel quel :

```
{{if .Roles | .Keep "ROLE_ADMIN" "grafana-admin"}}Admin{{else if .Roles | .Keep "grafana-editor"}}Editor{{else}}Viewer{{end}}
```

- **Sécurité** : les en-têtes que pose Meerkat sont d'abord retirés de la requête entrante, donc un appelant ne peut pas les falsifier. Grafana ne doit être joignable que par la gateway (pas de port publié, pas d'ingress à lui).

**Le résultat** : Grafana lit les mêmes en-têtes qu'avant, rien ne change pour lui. Autour, sa règle d'accès, ses rôles et son trafic sont dans la console avec ceux des autres applications, et chaque modification est dans le journal d'audit. La même recette existe pour d'autres outils (`connect-an-application.md`).

Grafana est l'application cible : on peut la nommer. Ne pas nommer de proxy d'authentification ni de reverse proxy : écrire « un proxy d'authentification » ou « une règle de forward-auth ».

**Sources** (dans `meerkat-ce`, `docs/content/fr/`) :
- `docs/auth/connect-an-application.md` (section Grafana) ;
- `product/replace-an-auth-proxy.md` : correspondances et étapes ;
- `docs/auth/service-jwt.md` (section « La forme des rôles »).

Recopier variables et expression au caractère près.

**Éditions** : tout cela est dans l'édition Community, gratuite, production comprise. Pour l'essayer : l'image `softwarity/meerkat-ce` ; la doc d'installation (`docs/start/install.md`) donne un fichier compose. Ne pas inventer de commande `docker run` pour Community : les commandes de ce post sont déjà la config Grafana et l'expression.

**À ne pas écrire** : pas de « open source », et ne pas présenter Community comme un produit à part.

**Fin du post** : une question aux lecteurs. Par exemple : « Combien d'outils internes avez-vous derrière un proxy d'authentification ? Et où gérez-vous leurs rôles ? »

**Image** : `image.png`, l'éditeur de route sur l'onglet Security (qui peut passer), la même pour toutes les langues. Description : `alt.<langue>.txt`.

**Lien** : https://meerkat.softwarity.dev
