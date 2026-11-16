# Brief : développer un service à la place de celui du cluster, et que tout le monde le sache

**But du post** : relier Meerkat et plug. Le mode développement permet à un développeur de faire tourner un service sur sa machine à la place du service déployé. La gateway sait qui le fait et l'annonce à tous. Public : développeurs et tech leads.

**Le cas d'usage** : le cluster contient tous les services et toutes les données. Reconstruire cela sur un portable est difficile, parfois interdit. Et quand quelqu'un branche son poste à la place d'un service partagé, les autres ne le savent pas : « pourquoi checkout répond bizarrement ? ».

**Avec Meerkat** :
- **Préparation** : un administrateur marque l'utilisateur comme développeur. Le développeur ajoute sa clé SSH publique à son compte Meerkat (Profil, Développeur).
- **La commande**, exacte, sur sa propre ligne :

```
plug -p <gateway-host> -s user-mng-service:8080:3000 npm run start
```

- **Ce qui se passe** :
  - le service local appelle les autres services par leur nom, comme s'il tournait dans le cluster ;
  - le trafic destiné à `user-mng-service` part vers sa machine, et toutes les routes qui l'utilisent suivent d'elles-mêmes ;
  - quand il arrête le processus, le service déployé revient.
- **La différence avec un tunnel seul** : chaque développeur a sa propre clé, donc la substitution est nommée (« checkout, par Alice »). Une page le dit à la connexion, et un bandeau le rappelle sur chaque page, en direct.
  - Retirer la clé ou le rôle de développeur ferme le tunnel en quelques secondes.
  - Le journal d'audit garde l'ouverture et la fin de chaque session.
- **En une ligne, en complément** : le Swagger des développeurs, `/meerkat/apidocs`. Toutes les API au même endroit, appelées à travers la gateway. *Try it out* peut agir sous un utilisateur, des groupes ou des rôles donnés : « que répond cette API à quelqu'un qui n'a que ce rôle ? ». Ce Swagger est dans toutes les éditions.

**Sources** (dans `meerkat-ce`, `docs/content/fr/`) :
- `product/dev-mode.md` ;
- `docs/operations/plug.md`.

Pour plug lui-même : https://plug.softwarity.dev.

**Éditions** :
- plug est gratuit et tourne à côté de n'importe quelle stack ;
- plug intégré à Meerkat (une clé par développeur, substitution nommée et annoncée) relève des éditions Team et Enterprise ; l'édition d'évaluation permet de l'essayer gratuitement, avec la commande `docker run` de `product/editions.md` ;
- le Swagger des développeurs est dans toutes les éditions, Community comprise.

**À ne pas écrire** :
- pas de nom d'outil tiers de tunnel ;
- pas de « open source » (Meerkat et plug sont sous licence FSL) ;
- ne pas présenter Community comme un produit à part.

**Fin du post** : une question aux lecteurs. Par exemple : « Comment testez-vous un service contre les vraies données du cluster aujourd'hui ? Et comment vos collègues savent-ils que c'est votre version qui répond ? »

**Image** : `image.png`, la page Plug de la console avec les étapes pour brancher le poste d'un développeur, la même pour toutes les langues. Description : `alt.<langue>.txt`.

**Liens** : https://meerkat.softwarity.dev et https://plug.softwarity.dev
