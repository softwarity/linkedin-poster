# Brief : la notion d'app-gateway

**But du post** : faire connaître le mot et l'idée d'**app-gateway**, par opposition à l'API gateway, en présentant Meerkat. Puis ouvrir la discussion avec les lecteurs.

**Le cas d'usage** : une équipe construit une application interne d'entreprise. Très vite, il lui faut des pages de connexion, du SSO et un second facteur, des rôles et des organisations, des règles d'accès par route, des quotas, un journal d'audit, TLS et un coffre à secrets, des tableaux de bord. La réponse habituelle consiste à empiler une API gateway (Kong…), un proxy d'authentification (oauth2-proxy), un fournisseur d'identité (Keycloak), un coffre (Vault), Prometheus et Grafana, un outil d'audit. Soit environ 8 produits, une quarantaine de pods, plusieurs moteurs de stockage, et encore les écrans d'organisation à développer soi-même.

**L'idée à faire passer** : une API gateway sert à exposer des API à des tiers (clés par partenaire, facturation à l'appel). Une **app-gateway** est la porte unique devant **une** application et ses utilisateurs : l'identité, les rôles, les organisations et les pages de connexion font partie du produit. Les services reçoivent des requêtes déjà authentifiées, porteuses d'un JWT signé (identité, rôles, organisation). Ils n'embarquent plus ni page de connexion, ni modèle de rôles, ni table d'utilisateurs.

**Faits utilisables** : tous viennent des sources du site dans `meerkat-ce` (`docs/content/fr/index.md`, `product/what-is-meerkat.md`, `product/features.md` section « Une app-gateway », `product/the-case.md`). Par exemple : une image, aucune dépendance, 70 Mo sur disque, environ 38 pods et 5 systèmes de stockage pour la pile assemblée (`the-case.md`). Ne pas citer de mémoire au repos : le site la calcule à la construction (`{{memory.idle}}`), aucun chiffre fiable dans les sources. Revérifier chaque chiffre avant de l'écrire.

**L'essayer** (juste avant la question) : l'édition d'évaluation, c'est tout Enterprise, gratuite, sans limite de durée, avec seulement une mention affichée ; elle se lance avec la commande `docker run` de `product/editions.md` (image `softwarity/meerkat`). Préciser en une ligne que l'édition Community (`softwarity/meerkat-ce`) est gratuite, production comprise. Pas de « open source » : Meerkat est sous licence FSL, comme plug.

**Fin du post : une vraie question aux lecteurs**, à la place d'une conclusion commerciale. Par exemple : « Vous avez déjà assemblé ce genre de pile pour une appli interne ? C'était pénible, ou ça s'est bien passé ? Une app-gateway tout intégrée vous tenterait, ou vous préférez garder des briques séparées ? » Reformuler librement, mais garder l'intention : recueillir des retours d'expérience honnêtes.

**Image** : `image.gif` dans ce dossier (l'animation « 8 produits → 1 porte »), décrite par `alt.fr.txt`.

**Lien** : https://www.softwarity.io
