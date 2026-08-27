# iptvabonnementfrance.store — site complet

Site statique HTML/CSS/JS. Aucune dépendance serveur, aucun framework, aucun build.
Upload direct dans `public_html` sur cPanel.

---

## 1. À faire AVANT la mise en ligne

### a. Renommer le fichier serveur
`_htaccess` → `.htaccess` (le point a été retiré pour que le fichier reste visible à l'upload).

### b. Remplir `assets/js/config.js`
C'est le **seul** fichier à modifier pour le contenu commercial. Il contient :

| Réglage | Effet si laissé vide |
|---|---|
| `offres[].prix` | `null` → la carte affiche « Tarif sur demande » |
| `remise_connexion` | `0.15` = chaque connexion supplémentaire 15 % moins chère |
| `max_connexions` | Plafond du sélecteur + / − sur les cartes |
| `chiffres[].valeur` | `null` sur les quatre → la section « En chiffres » disparaît. Sinon le compteur s'anime de 0 à la valeur |
| `whatsapp` | `""` → bouton flottant, numéro et CTA WhatsApp retirés du site entier |
| `endpoint` | `""` → le formulaire de contact bascule sur `mailto:` |
| `appareils[]` | Retirez une ligne pour faire disparaître la marque |
| `moyens_paiement[]` | Liste déroulante sur la page de commande |
| `codes_promo` | `{}` → le champ code promo est masqué. Ex. `{ "BIENVENUE10": 0.10 }` |

**Tarifs actuels** (1re connexion) : Bronze 39,99 € / 12 mois · Gold 49,99 € / 15 mois +3 offerts ·
Platinum 59,99 € / 15 mois +3 offerts · Exclusif 84,99 € / 24 mois +3 offerts.

**WhatsApp** : +1 (661) 541-3954. Bouton flottant sur les 24 pages, bouton sur la page contact,
et chaque bouton « Commander maintenant » ouvre WhatsApp avec un message pré-rempli contenant
l'offre, la durée, le nombre de connexions et le total calculé.

`build.py` lit directement `config.js` (via `_sources/lire_config.py`) pour générer le schéma
`Product` / `AggregateOffer`. **Après tout changement de prix, relancez `python3 build.py`**,
sinon les données structurées afficheront l'ancien tarif à Google.

### c. Compléter les pages légales
`/mentions-legales/`, `/politique-confidentialite/`, `/conditions-generales/`,
`/politique-remboursement/` contiennent des blocs `[À COMPLÉTER]` (éditeur, hébergeur, SIRET,
médiateur). L'identification de l'éditeur est **obligatoire** en droit français.
Faites relire les CGV par un professionnel avant publication.

Ces quatre pages sont en `noindex, follow` : elles sont accessibles aux visiteurs mais
n'encombrent pas l'index de Google. Retirez le `robots` dans `tpl.py` si vous préférez l'inverse.

---

## 2. Structure

```
/                            accueil
/abonnement-iptv/            offres + durées
/iptv-france/                page SEO « IPTV France »
/iptv-smarters-pro/          page SEO lecteur
/appareils/                  compatibilité
/fonctionnalites/            fonctionnalités
/faq/                        FAQ complète (10 questions)
/blog/                       index blog
/blog/<slug>/                10 articles
/commande/                   tunnel de commande (noindex + bloqué robots.txt)
/contact/                    formulaire
/mentions-legales/ /politique-confidentialite/
/conditions-generales/ /politique-remboursement/
404.html  robots.txt  sitemap.xml  _htaccess
assets/css/style.css  assets/js/config.js  assets/js/main.js  assets/img/
```

25 pages HTML au total.

---

## 3. SEO en place

- Title + meta description uniques sur chaque page
- Canonical absolu, Open Graph et Twitter Card
- Schémas JSON-LD : `Organization`, `WebSite`, `BreadcrumbList`, `FAQPage`, `Blog`, `Article`, `ContactPage`
- Schéma `Product` + `AggregateOffer` généré automatiquement depuis `config.js`
  (39,99 € – 84,99 €, EUR, `priceValidUntil` à un an)
- Fil d'Ariane sur toutes les pages internes
- `sitemap.xml` et `robots.txt` prêts
- Maillage interne : chaque article renvoie vers les offres, les appareils, la FAQ et 4 articles liés

Mots-clés couverts en H1/H2 : *IPTV abonnement France*, *abonnement IPTV France*, *abonnement IPTV
français*, *meilleur abonnement IPTV France*, *quel est le meilleur abonnement IPTV en France*,
*comment s'abonner à IPTV en France*, *quel abonnement IPTV choisir*, *quel est l'IPTV le plus
fiable*, *abonnement IPTV Smarters Pro*.

---

## 4. Après la mise en ligne

1. Search Console : ajouter la propriété, soumettre `https://iptvabonnementfrance.store/sitemap.xml`
2. Vérifier le rendu de `og-image.svg` — si votre CDN ou un réseau social refuse le SVG,
   exportez-le en PNG 1200×630 et changez les deux balises `og:image` / `twitter:image` dans `tpl.py`
3. Cloudflare : activer le cache, laisser la minification HTML désactivée si vous éditez à la main
4. Tester le formulaire de contact une fois `endpoint` renseigné

---

## 5. Regénérer le site

Les sources de génération sont dans `build/` (hors du dossier à uploader) :
`tpl.py` (gabarits), `contenu.py` (sections partagées), `articles.py` (les 10 articles),
`build.py` (assemblage). `python3 build.py` régénère les 24 pages.
Pour modifier un texte partagé (footer, avis légal, FAQ), éditez la source puis relancez —
sinon vous devrez répercuter la modification sur 24 fichiers à la main.

---

## 6. Le tunnel de commande

« Commander maintenant » ouvre une **modale** sans quitter la page : récapitulatif de l'offre,
nom, e-mail, téléphone avec sélecteur d'indicatif (235 pays, drapeaux calculés depuis le code
ISO — aucune image chargée), quatre tuiles de paiement, puis un écran de confirmation.
Échap et le clic sur le fond ferment la modale ; le focus est piégé à l'intérieur tant qu'elle
est ouverte.

Le numéro est normalisé à l'envoi : `0612345678` avec le Maroc sélectionné devient
`+212 612345678`. Le code ISO du pays part aussi dans une colonne dédiée de la feuille.

La page `/commande/` reste en place comme repli — elle sert les liens directs et fonctionne à
l'identique, avec les mêmes composants. Le `href` des boutons pointe toujours vers elle, la
modale n'étant qu'une interception JavaScript : sans JS, le parcours continue de fonctionner.

Le pays présélectionné se change avec `pays_defaut` dans `config.js`, et les moyens de paiement
avec `moyens_paiement` (id, nom, icône parmi carte / paypal / virement / whatsapp).

### Ancienne version (page pleine)

« Commander maintenant » n'ouvre plus WhatsApp directement : le bouton mène à
`/commande/?offre=gold&c=2`, qui reprend la formule et le nombre de connexions choisis sur la carte.

Sur cette page le client peut changer de formule et de nombre de connexions (le récapitulatif se
recalcule en direct : tarif de base, remise connexions, code promo, total), puis il saisit nom,
e-mail, téléphone, appareil, moyen de paiement et remarques. Nom et e-mail valide sont obligatoires.

À la validation, la commande part vers `endpoint` (Google Apps Script) **et** ouvre WhatsApp avec
le récapitulatif complet pré-rempli. Si `endpoint` est vide, seul WhatsApp s'ouvre — la commande
n'est donc enregistrée nulle part tant que vous n'avez pas branché le script. Renseignez-le
rapidement pour ne pas perdre de commandes si un client ferme l'onglet WhatsApp.

**Aucun champ bancaire n'existe sur le site.** Le client choisit un moyen de paiement, vous lui
envoyez ensuite le lien ou les coordonnées. C'est volontaire : héberger une saisie de carte sur un
site statique vous exposerait aux obligations PCI-DSS sans aucun bénéfice. Utilisez un lien
Stripe, PayPal ou SumUp généré de votre côté.

La page est en `noindex, follow` et bloquée dans `robots.txt` — une page de commande avec
paramètres d'URL génère sinon des dizaines d'URL dupliquées dans la Search Console.

## 7. Le backend Google Apps Script

`_sources/AppsScript-Code.gs` reçoit les commandes et les messages de contact, les écrit dans
votre feuille `1kc2jW078-lW-fp_WOPRX1XyzHIPjP1YjoVU-157Bsi4` et vous envoie une alerte e-mail.

Installation :

1. [script.google.com](https://script.google.com) → **Nouveau projet**
2. Collez tout le contenu de `AppsScript-Code.gs`
3. Ajustez `EMAIL_ALERTE` en haut du fichier
4. **Exécuter** → fonction `initialiser` → autorisez l'accès
5. **Déployer → Nouveau déploiement → Application web**
   · Exécuter en tant que : **Moi**
   · Qui a accès : **Tout le monde** ← sans ça le site reçoit une erreur d'autorisation
6. Copiez l'URL `/exec` dans `assets/js/config.js` :
   `endpoint: "https://script.google.com/macros/s/AKfy.../exec",`

Deux onglets se créent tout seuls : **Commandes** (17 colonnes, avec référence
`IAF-20260827-0004` et colonne Statut) et **Contacts** (8 colonnes). Les en-têtes sont figés
et mis en forme au premier passage.

Les fonctions `testerCommande` et `testerContact` simulent un envoi depuis l'éditeur, sans
passer par le site — pratique pour vérifier avant de déployer.

> **Le piège classique** : après chaque modification du script, il faut refaire
> **Déployer → Gérer les déploiements → crayon → Version : Nouvelle version**.
> Sinon l'ancienne version continue de tourner et vous chercherez longtemps.

Le script pose un verrou pendant l'écriture, pour que deux commandes simultanées n'écrasent
pas la même ligne. En cas d'échec d'enregistrement, il vous envoie un e-mail contenant les
données brutes reçues : une commande perdue coûte plus cher qu'un e-mail d'erreur.

## 8. La section WhatsApp

Un panneau dédié apparaît sur cinq pages : accueil, abonnement, appareils, FAQ et contact.
Il affiche le numéro, un bouton vers la conversation, et quatre raccourcis qui ouvrent WhatsApp
avec un message déjà rédigé — vérifier un appareil, choisir une formule, aide à l'installation,
suivi de commande. Vous savez donc dès le premier message pourquoi la personne écrit.

Les libellés et les messages se modifient dans `_sources/contenu.py`, liste `SUJETS_WA`.
Si `whatsapp` est vide dans `config.js`, le panneau, le bouton flottant et le numéro
disparaissent des 25 pages sans autre intervention.

## 9. Les compteurs « En chiffres »

Ils affichent les valeurs de `config.js`, animées de 0 à la cible au scroll :
25 000+ chaînes, 100 000+ films et séries, 12 plateformes, support 24/7.

Pour en ajouter un, une ligne suffit :

```js
{ valeur: 8, suffixe: " ans", libelle: "D'expérience" }
```

`valeur` doit être un nombre (le compteur l'anime), `suffixe` est collé derrière sans espace
automatique. Mettez `null` sur les quatre pour faire disparaître la section entière.

Un avertissement pratique : un nombre de clients ou un taux de satisfaction inventé est une
allégation chiffrée sur laquelle un concurrent ou la DGCCRF peut vous prendre en défaut
(art. L121-2 du Code de la consommation, pratique commerciale trompeuse). Les compteurs
techniques — chaînes, catalogue, plateformes, disponibilité du support — ne posent pas ce
problème tant qu'ils correspondent à ce que vous livrez réellement.

## 10. Deux points à arbitrer

**Gold et Platinum ont la même durée (15 mois +3 offerts) et exactement la même liste
d'avantages, pour 10 € d'écart.** Sur la capture allemande c'est déjà le cas. En l'état, un
visiteur n'a aucune raison de choisir Platinum, ce qui pousse mécaniquement vers Gold et
plafonne le panier moyen. Si Platinum inclut réellement quelque chose de plus (durée, nombre
de connexions offertes, qualité), ajoutez-le dans `avantages` ; sinon, envisagez de le
retirer ou d'allonger sa durée.

**Deux formulations ont été neutralisées par rapport à votre capture allemande :**

| Capture | Sur le site | Pourquoi |
|---|---|---|
| « Netflix, Prime Video & mehr » | « Contenus à la demande (VOD) » | Annoncer Netflix et Prime Video comme inclus dans un abonnement IPTV revendique l'accès à des catalogues sous licence exclusive et utilise leurs marques. Sur un `.store` ciblant la France, c'est le type de mention qui déclenche mise en demeure et déréférencement. |
| « 100 % stabile Server » | « Serveurs stables et surveillés » | Une garantie absolue de disponibilité n'est pas tenable techniquement et constitue une allégation commerciale opposable (art. L121-2 du Code de la consommation). |

Les deux sont des lignes de `config.js` : si vous voulez le texte d'origine, remplacez la
chaîne dans `avantages` des quatre offres et relancez `build.py`.

## 11. Note sur les polices

Le site charge Bricolage Grotesque, Instrument Sans et JetBrains Mono depuis Google Fonts
avec `display=swap`. Si vous préférez éviter la dépendance externe (RGPD, performance),
téléchargez les `.woff2` dans `assets/fonts/` et remplacez le `<link>` par un `@font-face` local.
