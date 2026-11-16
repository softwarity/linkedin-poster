# Brief : vos services reçoivent l'utilisateur tout prêt

**But du post** : montrer la vraie force de Meerkat. Tout ce qui entoure l'utilisateur (connexion, second facteur, passkeys, rôles, tenant) est fait une fois, à la porte. Puis l'identité arrive d'office aux services, sans qu'ils aient rien à faire.

**Le cas d'usage** : dans une application interne en microservices, chaque service finit par refaire sa part d'identité. Il lui faut une session, un contrôle des rôles, parfois une table d'utilisateurs, et le second facteur est géré ailleurs, ou pas du tout. Deux services ne sont jamais d'accord sur ce qu'est un utilisateur.

**Avec Meerkat** :
- **À la porte**, la personne se connecte sur les pages de la gateway, à vos couleurs :
  - comptes locaux, OpenID Connect ou GitHub ;
  - en Enterprise, aussi SAML, LDAP ou Active Directory ;
  - second facteur TOTP, avec codes de secours et navigateurs de confiance ;
  - passkeys comme premier facteur.
- **Le tenant** : avec plusieurs tenants (Enterprise), la personne choisit le sien à la connexion.
- **Le service, lui, reçoit un JWT signé** dans `Authorization: Bearer`. Tout `Authorization` envoyé par le client est d'abord supprimé : personne ne peut en fabriquer un.
  - Le jeton porte `sub` (le compte), plus ce que la route a choisi d'envoyer : nom d'utilisateur, e-mail, rôles, tenant.
  - Il vit deux minutes par défaut.
- **Pour le vérifier**, le service n'a besoin d'aucun secret, d'aucune table de comptes, ni d'aucun rappel vers la gateway. Il lui suffit d'une adresse : le document de découverte, sur le plan interne. C'est la ligne à mettre seule dans le post :

```
http://meerkat:7070/.well-known/openid-configuration
```

  Les bibliothèques courantes la prennent telle quelle (`issuer-uri` chez Spring, `MetadataAddress` en .NET, `openid-client` en Node). Une rotation des clés leur parvient toute seule.
- **Variante sans code** : la route peut envoyer la même identité en en-têtes, pour une application qui lit déjà un en-tête d'utilisateur.

**Le résultat à faire sentir** : les services n'embarquent plus ni page de connexion, ni modèle de rôles, ni table d'utilisateurs. Ils lisent qui appelle, ses rôles et son tenant comme un fait, pas comme un paramètre choisi par l'appelant.

**Sources** (dans `meerkat-ce`, `docs/content/fr/`) :
- `docs/auth/service-jwt.md` : claims, durée, découverte, bibliothèques ;
- `docs/auth/mfa.md` : TOTP, codes de secours, navigateurs de confiance ;
- `docs/auth/passkeys.md` ;
- `product/multi-tenancy.md` (section « Ce que reçoivent vos services ») ;
- `product/what-is-meerkat.md`.

Revérifier chaque détail avant de l'écrire.

**Éditions** : tout ce qui précède est dans l'édition Community, gratuite, production comprise, sauf deux choses qui relèvent d'Enterprise : plusieurs tenants, et SAML/LDAP. Le dire en une ligne. L'édition d'évaluation permet d'essayer Enterprise, avec la commande `docker run` de `product/editions.md`.

**À ne pas écrire** :
- aucun nom de produit tiers d'API gateway ou d'IAM, en dehors des bibliothèques citées ci-dessus ;
- pas de « open source » ;
- ne pas présenter Community comme un produit à part.

**Fin du post** : une question aux lecteurs. Par exemple : « Dans vos services, qui vérifie l'identité aujourd'hui ? Chaque service à sa façon, une bibliothèque commune, ou la gateway ? »

**Image** : `image.png`, la page de connexion de la gateway (avec « Sign in with a passkey »), la même pour toutes les langues. Description : `alt.<langue>.txt`.

**Lien** : https://meerkat.softwarity.dev
