# Brief : la notion d'app-gateway

**But du post** : faire connaître le mot et l'idée d'**app-gateway**, comme l'évolution naturelle de l'API gateway, en présentant Meerkat. Puis ouvrir la discussion avec les lecteurs.

**Le cas d'usage** : une équipe construit une application interne d'entreprise en microservices. Au départ, une API gateway devant les services suffit. Très vite, il faut des pages de connexion, du SSO et un second facteur, des rôles et des organisations, des règles d'accès par route, des quotas, un journal d'audit, TLS, une documentation OpenAPI par service, un tunnel pour les développeurs, des tableaux de bord. La pile grossit autour de la gateway : un IAM, un proxy d'authentification, des fichiers de configuration partout, chaque brique qui envoie sa propre télémétrie, et les écrans d'organisation à développer soi-même.

**L'idée à faire passer** : l'API gateway a été pensée pour exposer des API à des tiers (clés par partenaire, facturation à l'appel). Une **app-gateway** est la porte unique devant **une** application et ses utilisateurs : l'identité, les rôles, les organisations et les pages de connexion font partie du produit. Comme tout passe par elle, c'est aussi la bonne place pour l'audit, les métriques et les traces. Les services reçoivent des requêtes déjà authentifiées, porteuses de l'identité (un JWT signé ou des en-têtes : utilisateur, rôles, organisation). Ils n'embarquent plus ni page de connexion, ni modèle de rôles, ni table d'utilisateurs.

**À ne pas écrire** :
- aucun nom de produit tiers : parler de catégories (API gateway, IAM, proxy d'authentification…) ;
- ne pas présenter Meerkat comme remplaçant d'un coffre à secrets ou d'une base de données (son coffre sert à ses propres secrets) ;
- pas de nombre de pods ni de produits empilés.

**Faits utilisables** : ils viennent tous des sources du site dans `meerkat-ce` (`docs/content/fr/index.md`, `product/what-is-meerkat.md`, `product/features.md` section « Une app-gateway », `product/microservices.md`). Par exemple : une image, aucune dépendance, 70 Mo sur disque. Ne pas citer de mémoire au repos : le site la calcule à la construction (`{{memory.idle}}`), et les sources ne donnent aucun chiffre fiable. Revérifier chaque chiffre avant de l'écrire.

**L'essayer** (juste avant la question) : l'édition d'évaluation, c'est tout Enterprise, gratuite, sans limite de durée, avec seulement une mention affichée. Elle se lance avec la commande `docker run` de `product/editions.md` (image `softwarity/meerkat`). Préciser en une ligne que l'édition Community (`softwarity/meerkat-ce`) est gratuite, production comprise. Meerkat est un seul produit : ne pas présenter Community comme un produit à part. Pas de « open source » : Meerkat est sous licence FSL, comme plug.

**Fin du post : une vraie question aux lecteurs**, à la place d'une conclusion commerciale. Par exemple : « Vous avez déjà assemblé ce genre de pile autour d'une API gateway ? C'était pénible, ou ça s'est bien passé ? Une app-gateway tout intégrée vous tenterait, ou vous préférez garder des briques séparées ? » Reformuler librement, mais garder l'intention : recueillir des retours d'expérience honnêtes.

**Image** : `image.gif` dans ce dossier, la même pour toutes les langues (aucun texte à traduire). C'est l'animation « API-GATEWAY → APP-GATEWAY » : la pile grossit autour de l'API gateway, qui l'absorbe et devient Meerkat. Le post peut y faire écho (« le I devient un P »). Description : `alt.<langue>.txt`.

**Lien** : https://meerkat.softwarity.dev
