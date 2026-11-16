# Brief : plusieurs clients sur la même application, séparés à la porte

**But du post** : présenter la multi-tenance, une fonction Enterprise, avec un appel à l'essayer par l'édition d'évaluation. Public : architectes et tech leads qui servent plusieurs clients, filiales ou services avec les mêmes applications internes.

**Le cas d'usage** : la même application sert plusieurs clients, ou plusieurs filiales, qui ne doivent pas se voir. D'habitude, chaque service reçoit un identifiant de client en paramètre et doit le vérifier. Il suffit d'un oubli pour qu'un client voie les données d'un autre.

**Avec Meerkat** :
- **Chaque client est un tenant**, avec ses membres (administrateurs ou utilisateurs), ses groupes qui donnent des rôles, son propriétaire et ses réglages (durée de session…).
- **Un administrateur de tenant** gère ses membres, ses groupes et ses règles depuis la console, et rien en dehors.
- **À la connexion** : avec une seule appartenance, la personne entre directement. Avec plusieurs, elle choisit, et peut changer ensuite depuis le bouton utilisateur.
- **Le point clé** : le tenant voyage avec la requête, à côté de l'identité et des rôles, dans le JWT signé ou les en-têtes. Les règles de route et par endpoint sont jugées dans ce tenant. Le service apprend dans quel tenant travaille l'appelant **comme un fait, pas comme un paramètre choisi par l'appelant**. C'est la phrase à faire passer.
- **En une ligne** : en Enterprise, une règle de groupe peut faire d'un groupe d'annuaire, d'une équipe GitHub ou d'un claim OpenID Connect une appartenance, à chaque connexion.

**Sources** (dans `meerkat-ce`, `docs/content/fr/`) :
- `product/multi-tenancy.md` ;
- `docs/access/tenants.md`.

**Éditions** : plusieurs tenants relèvent d'Enterprise ; l'édition Community sert un seul tenant. Pour essayer : l'édition d'évaluation, c'est tout Enterprise, gratuit, sans limite de durée, avec seulement une mention affichée. La commande à mettre sur sa propre ligne est le `docker run` de `product/editions.md` (image `softwarity/meerkat`).

**À ne pas écrire** :
- pas de prix ;
- pas de « open source » ;
- ne pas présenter Community comme un produit à part.

**Fin du post** : une question aux lecteurs. Par exemple : « Chez vous, l'isolation entre clients se joue dans chaque service, ou en amont ? »

**Image** : `image.png`, la console d'une administratrice de tenant (« Acme Corp » : ses membres et leurs groupes, aucun autre tenant), la même pour toutes les langues. Description : `alt.<langue>.txt`.

**Lien** : https://meerkat.softwarity.dev
