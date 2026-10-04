# Ligne éditoriale LinkedIn

Consignes de la tâche qui rédige les posts du profil de François Achache, sous la marque Softwarity. François valide la version française de chaque sujet dans Slack ; les traductions de ce sujet sont ensuite publiées sans nouvelle validation. Personne ne les relit : elles doivent être irréprochables.

## Rythme et rotation

Un passage chaque jour du lundi au vendredi, **un seul post par passage**. Un sujet par semaine, qui sort en cinq langues, une par jour, dans cet ordre : `fr` (lundi), `en`, `es`, `pt`, `de` (vendredi). Le projet alterne à chaque nouveau sujet : plug, puis Meerkat, puis plug…

Pour savoir quoi écrire, on lit l'état du dépôt (en incluant les branches `claude/*`, où un passage précédent a pu pousser) :

```bash
git fetch origin '+refs/heads/claude/*:refs/remotes/origin/claude/*'
for ref in HEAD $(git for-each-ref --format='%(refname)' refs/remotes/origin/claude); do
  git ls-tree -r --name-only "$ref" -- posts | grep -E '/[a-z]{2}\.txt$'
done | sort -u
```

- Si le sujet le plus récent (celui dont le `fr.txt` a été ajouté en dernier : `git log --diff-filter=A --format=%as -- <fichier>`) n'a pas toutes ses langues, écrire la première qui manque dans l'ordre `en`, `es`, `pt`, `de`. Toujours finir un sujet avant d'en commencer un autre.
- Si le sujet le plus récent est complet et que l'on **n'est pas lundi**, ne rien écrire : terminer sans commit, en le disant dans le résumé. Un nouveau sujet ne commence que le lundi.
- Si l'on est lundi, commencer un nouveau sujet en `fr` :
  1. **D'abord un sujet planifié**, s'il y en a un pour un projet qui n'est pas en pause : un dossier qui contient un `brief.md` mais pas de `fr.txt`, le plus ancien d'abord (date du dossier). Écrire son `fr.txt` en suivant le brief, qui prime sur les consignes générales.
  2. Sinon, un nouveau sujet sur l'autre projet que le dernier sujet, s'il n'est pas en pause (sinon, sur le même projet), dans `posts/<projet>/<AAAA-MM-JJ>-<slug>/fr.txt`.

**Projets en pause** : **Meerkat**, jusqu'à ce que François le relance (la version d'évaluation est en cours de finalisation). N'écrire aucun post sur Meerkat, même planifié, tant qu'il figure ici.

## Projets et sources autorisées

Ne rien affirmer qui ne figure pas dans ces sources publiques : pas de chiffres, de clients, de benchmarks ni de fonctionnalités inventés.

- **plug** : https://github.com/softwarity/plug (README) et https://softwarity.github.io/plug/, y compris sa page de comparaison. Liens à mettre dans le post : le dépôt GitHub et la doc. Pour la licence, écrire « le code source est sur GitHub », **jamais « open source »** (plug est sous licence FSL).
- **Meerkat** : **uniquement** le dépôt public https://github.com/softwarity/meerkat-ce, et dans ce dépôt, les sources du site `docs/content/fr/**` et `docs/content/en/**`, plus le `README.md`. Le site https://www.softwarity.io est une application monopage : un WebFetch n'y voit que le titre, il faut donc lire ces sources. Ne rien tirer d'un autre dépôt (le dépôt `meerkat` est privé), ni des autres fichiers de `meerkat-ce` (`FEATURES.md`, `memory.md`, `CLAUDE.md`…), qui sont des notes de travail. Le produit est en construction : ne présenter que ce que le site donne comme livré. Lien à mettre dans le post : https://www.softwarity.io.

Pistes de cas d'usage pour plug, un par post :
- ouvrir une base du cluster (MongoDB, Postgres…) avec un outil graphique (Compass, DBeaver) sans exposer de port (`plug -c`) ;
- développer un service déjà déployé : plug met la version déployée de côté, votre process local prend sa place et hérite de ses variables d'environnement (`plug -s`) ;
- faire tourner deux branches du même service côte à côte, avec un port local choisi automatiquement ;
- tester une image Docker comme membre du cluster avant de la déployer (`--dockerrun`) ;
- lancer un script ponctuel avec les identifiants d'un service (`--env-of`) ;
- travailler sur plusieurs clusters en parallèle (prod et staging) ;
- laisser un agent IA de code interroger le cluster (`plug mcp`).

Les sujets déjà traités sont dans `posts/`.

## Format d'un post : le projet en bref, puis un cas d'usage

Chaque post suit ce schéma :

1. **Le projet en une ou deux lignes** : ce que c'est, pour qui.
2. **Un cas d'usage concret**, raconté comme une situation vécue :
   - la situation (« J'ai mon cluster avec MongoDB dedans… ») ;
   - le blocage (« …et aucun port exposé pour m'y connecter. ») ;
   - la commande, **exacte**, vérifiée dans la doc, sur sa propre ligne ;
   - le résultat (« Compass tourne sur mon Mac, mais il est vu comme à l'intérieur du cluster, et il atteint la base par son nom. »).
3. Les liens, puis les hashtags.

Un seul cas d'usage par post. Le lecteur doit pouvoir se dire « ça, c'est moi », puis copier la commande.

Exemple de référence, pour plug :

> plug fait tourner un process local comme s'il était dans votre cluster Docker, Swarm ou Kubernetes.
>
> Cas vécu : mon cluster contient un MongoDB, mais aucun port n'est exposé. Pour l'explorer avec Compass, il faudrait un port-forward, ou modifier la stack.
>
> Avec plug, sur mon Mac :
> plug -c open -a Compass
>
> Compass se connecte à mongodb:27017, par son nom, comme n'importe quel service du cluster. Je ferme Compass : tout est comme avant.

Une commande doit être exacte au caractère près : la tirer de la doc, jamais de mémoire. Exception connue : la doc affirme que `open -a` ne fonctionne pas avec `plug -c` sur macOS, alors que François a vérifié que si (2026-09-24). Pour lancer une app macOS, écrire donc `plug -c open -a <App>`.

## Style

- Écrire à la première personne, au nom de François ; vouvoyer le lecteur.
- Écrire concret et factuel, comme un développeur qui parle à des développeurs : partir d'une douleur réelle, puis montrer la commande.
- Pas de superlatifs ni de ton marketing, et pas de paragraphe sur les limites face aux concurrents. Citer les concurrents (mirrord, Telepresence…) seulement pour situer l'approche, sans les dénigrer.
- Faire tenir l'accroche dans les deux premières lignes (LinkedIn coupe ensuite).
- Viser 900 à 1 800 caractères, sans jamais dépasser 3 000.
- Écrire en texte brut, car LinkedIn n'interprète pas le Markdown. Utiliser → et • pour les listes, et mettre les commandes sur une ligne à part.
- Terminer par 3 à 5 hashtags en anglais.
- Pour les traductions, adapter le post plutôt que le traduire mot à mot : garder le fond et les faits, retravailler l'accroche pour qu'elle sonne naturelle.
- Écrire dans la variante qui porte le plus loin : `es` en espagnol neutre, compris en Espagne comme en Amérique latine ; `pt` en portugais du Brésil ; `de` en allemand, en vouvoyant (« Sie »). Laisser tels quels les commandes, les noms de produits et les termes techniques que les développeurs de ce pays emploient en anglais (Kubernetes, Docker, gateway, CLI…).
- Relire chaque traduction comme un locuteur natif : orthographe, accents, accords, tournures. Aucune relecture humaine n'aura lieu.

## Image

- Une traduction réutilise l'image de son dossier : `image.<langue>.*` s'il existe (image dont le texte est dans cette langue), sinon `image.*`. Écrire seulement `alt.<langue>.txt`, la description de l'image dans la langue du post.
- Un nouveau sujet peut avoir une image, facultative : `image.png`, `image.gif` ou `image.jpg`, 8 Mo au plus, prise sur les sources publiques ci-dessus. Écrire alors `alt.fr.txt`. Ne jamais fabriquer de capture d'écran ; sans image pertinente, publier le texte seul.

## Livraison

- Commiter sous l'identité de François : `git config user.name hhfrancois` et `git config user.email francois.achache@gmail.com`.
- Un commit par passage, avec pour message `post: <projet>/<sujet> (<langue>)`.
- **Jamais de `[skip ci]`** : c'est le push qui envoie le brouillon dans Slack.
- Jamais de trailer `Co-Authored-By` mentionnant Claude ou Anthropic.
- Pousser sur `main`. Si c'est refusé, pousser sur une branche `claude/linkedin-<AAAA-MM-JJ>` : le brouillon part aussi.
- Ne modifier aucun fichier en dehors de `posts/`, et ne jamais modifier un `brief.md`.
