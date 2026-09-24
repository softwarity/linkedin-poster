# Ligne éditoriale LinkedIn

Consignes de la tâche qui rédige les posts du profil de François Achache, sous la marque Softwarity. Chaque post passe par la validation de François dans Slack avant publication.

## Rythme et rotation

Un passage le mardi et le jeudi, **un seul post par passage**. Chaque sujet sort en trois langues, une par passage, dans cet ordre : `fr`, puis `en`, puis `he`. Ensuite, un nouveau sujet commence, et le projet alterne à chaque nouveau sujet : plug, puis Meerkat, puis plug…

Pour savoir quoi écrire, on lit l'état du dépôt (en incluant les branches `claude/*`, où un passage précédent a pu pousser) :

```bash
git fetch origin '+refs/heads/claude/*:refs/remotes/origin/claude/*'
for ref in HEAD $(git for-each-ref --format='%(refname)' refs/remotes/origin/claude); do
  git ls-tree -r --name-only "$ref" -- posts | grep -E '/[a-z]{2}\.txt$'
done | sort -u
```

- Si le sujet le plus récent (celui dont le `fr.txt` a été ajouté en dernier : `git log --diff-filter=A --format=%as -- <fichier>`) n'a pas encore son `en.txt`, écrire `en.txt`. S'il a son `en.txt` mais pas son `he.txt`, écrire `he.txt`.
- Sinon, commencer un nouveau sujet en `fr`, sur l'autre projet que le dernier sujet, dans `posts/<projet>/<AAAA-MM-JJ>-<slug>/fr.txt`.

## Projets et sources autorisées

Ne rien affirmer qui ne figure pas dans ces sources publiques : pas de chiffres, de clients, de benchmarks ni de fonctionnalités inventés.

- **plug** : https://github.com/softwarity/plug (README) et https://softwarity.github.io/plug/, y compris sa page de comparaison. Liens à mettre dans le post : le dépôt GitHub et la doc. Pour la licence, écrire « le code source est sur GitHub », **jamais « open source »** (plug est sous licence FSL).
- **Meerkat** : **uniquement** https://www.softwarity.io/. Le dépôt de Meerkat est privé : même s'il est accessible, n'en rien citer. Le produit est en construction : ne présenter que ce que le site donne comme disponible. Lien à mettre dans le post : www.softwarity.io.

Si le site de Meerkat est injoignable, traiter un nouveau sujet plug à la place.

Pistes de sujets pour plug, un angle par post : reprendre un service déjà déployé (mis de côté puis restauré) en héritant de ses variables d'environnement ; le port local choisi automatiquement, pour deux branches côte à côte ; plusieurs clusters en parallèle ; le serveur MCP pour les agents IA de code ; l'installation en une commande ssh servie par le cluster ; Swarm sans modification du réseau ; Windows. Les sujets déjà traités sont dans `posts/`.

## Style

- Écrire à la première personne, au nom de François ; vouvoyer le lecteur.
- Écrire concret et factuel, comme un développeur qui parle à des développeurs : partir d'une douleur réelle, puis montrer la commande.
- Pas de superlatifs ni de ton marketing, et pas de paragraphe sur les limites face aux concurrents. Citer les concurrents (mirrord, Telepresence…) seulement pour situer l'approche, sans les dénigrer.
- Faire tenir l'accroche dans les deux premières lignes (LinkedIn coupe ensuite).
- Viser 900 à 1 800 caractères, sans jamais dépasser 3 000.
- Écrire en texte brut, car LinkedIn n'interprète pas le Markdown. Utiliser → et • pour les listes, et mettre les commandes sur une ligne à part.
- Terminer par 3 à 5 hashtags en anglais.
- Pour `en` et `he`, adapter le post plutôt que le traduire mot à mot : garder le fond, retravailler l'accroche.
- Pour `he`, écrire un hébreu naturel. Laisser en caractères latins les commandes, les noms de produits et les termes techniques usuels (Kubernetes, Docker, CLI…), et garder chaque commande sur sa propre ligne pour ne pas casser l'affichage de droite à gauche.

## Image

- Une traduction réutilise l'`image.*` de son dossier : écrire seulement `alt.<langue>.txt`, la description de l'image dans la langue du post.
- Un nouveau sujet peut avoir une image, facultative : `image.png`, `image.gif` ou `image.jpg`, 8 Mo au plus, prise sur les sources publiques ci-dessus. Écrire alors `alt.fr.txt`. Ne jamais fabriquer de capture d'écran ; sans image pertinente, publier le texte seul.

## Livraison

- Un commit par passage, avec pour message `post: <projet>/<sujet> (<langue>)`.
- **Jamais de `[skip ci]`** : c'est le push qui envoie le brouillon dans Slack.
- Jamais de trailer `Co-Authored-By` mentionnant Claude ou Anthropic.
- Pousser sur `main`. Si c'est refusé, pousser sur une branche `claude/linkedin-<AAAA-MM-JJ>` : le brouillon part aussi.
- Ne modifier aucun fichier en dehors de `posts/`.
