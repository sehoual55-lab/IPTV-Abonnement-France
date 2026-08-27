# iptvabonnementfrance.store

Site statique en français pour un service d'abonnement IPTV ciblant la France.
HTML / CSS / JS purs — aucun framework, aucune étape de build, aucune dépendance npm.

**25 pages** · **~790 Ko** · [LISEZ-MOI.md](LISEZ-MOI.md) contient la documentation complète
du site (tarifs, WhatsApp, tunnel de commande, SEO).

---

## Déployer sur Vercel

### 1. Pousser sur GitHub

```bash
git init
git add .
git commit -m "Site iptvabonnementfrance.store"
git branch -M main
git remote add origin https://github.com/VOTRE-COMPTE/iptvabonnementfrance.git
git push -u origin main
```

### 2. Importer dans Vercel

Sur [vercel.com/new](https://vercel.com/new), choisissez le dépôt, puis :

| Réglage | Valeur |
|---|---|
| Framework Preset | **Other** |
| Root Directory | `./` |
| Build Command | *(laisser vide)* |
| Output Directory | *(laisser vide)* |
| Install Command | *(laisser vide)* |

C'est un site statique : toute commande de build renverra une erreur. Laissez ces trois champs vides.

### 3. Brancher le domaine

Dans **Settings → Domains**, ajoutez `iptvabonnementfrance.store` **et** `www.iptvabonnementfrance.store`.
Vercel propose alors de rediriger l'un vers l'autre : choisissez `www` → domaine sans `www`,
parce que c'est la version sans `www` qui figure dans les balises canonical et le sitemap.

Chez votre registrar, pointez :

```
A      @      76.76.21.21
CNAME  www    cname.vercel-dns.com
```

Le certificat HTTPS est émis automatiquement.

---

## Ce que fait `vercel.json`

- `cleanUrls` + `trailingSlash` — `/abonnement-iptv/` sert `abonnement-iptv/index.html`,
  et `/abonnement-iptv/index.html` redirige vers l'URL propre. Indispensable pour éviter
  que Google indexe deux URL pour la même page.
- Cache d'un an sur `/assets/`, sauf `config.js` limité à 5 minutes — sinon un changement
  de tarif mettrait des jours à apparaître chez les visiteurs déjà venus.
- HTML jamais mis en cache, pour que vos mises à jour soient visibles tout de suite.
- En-têtes de sécurité : `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`,
  `Permissions-Policy`.
- Les URL de scan WordPress (`/wp-admin`, `/xmlrpc.php`, `/cgi-bin`…) renvoient vers la 404
  au lieu de polluer vos rapports d'erreurs Search Console.

`404.html` est repris automatiquement par Vercel comme page d'erreur.

## Ce que fait `.vercelignore`

`_sources/` (les scripts Python de génération), `_htaccess` et les fichiers d'aperçu restent
dans le dépôt Git mais ne sont **pas** publiés. Sans ce fichier, n'importe qui pourrait
télécharger `_sources/build.py` depuis votre domaine.

---

## Modifier le site

**Contenu commercial** — tarifs, appareils, WhatsApp, moyens de paiement, codes promo :
uniquement `assets/js/config.js`. Un commit, et Vercel redéploie.

**Textes partagés** — footer, mentions légales, sections répétées : ils sont générés.
Éditez `_sources/`, puis :

```bash
cd _sources && python3 build.py && python3 p404.py
```

Les 25 pages sont réécrites. Committez le résultat. Si vous modifiez directement un
`index.html`, la prochaine génération écrasera votre modification.

> **Attention** : `build.py` lit `config.js` pour générer le schéma `Product`/`Offer`.
> Après tout changement de prix, relancez-le, sinon Google continuera d'afficher l'ancien tarif.

---

## Sur GitHub Pages

Possible, mais seulement sur un domaine personnalisé à la racine. Toutes les URL du site sont
absolues (`/assets/…`, `/blog/…`) : sur `votrecompte.github.io/nom-du-depot/`, rien ne se
chargerait. Si vous tenez à Pages, configurez le domaine personnalisé dès le départ.

## Déploiements de prévisualisation

Vercel crée une URL de prévisualisation par branche. Elles reçoivent automatiquement un
en-tête `X-Robots-Tag: noindex` et ne seront pas indexées. Les balises canonical y pointent
quand même vers le domaine de production — c'est voulu.
