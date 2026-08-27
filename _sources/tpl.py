# -*- coding: utf-8 -*-
"""Templates partagés pour iptvabonnementfrance.store"""
import os, json, html

# Racine du site = dossier parent de _sources/ (fonctionne quelle que soit la machine)
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINE = "https://iptvabonnementfrance.store"
MARQUE = "IPTV Abonnement France"

NAV = [
    ("Accueil", "/"),
    ("Abonnement IPTV", "/abonnement-iptv/"),
    ("Fonctionnalités", "/fonctionnalites/"),
    ("Appareils", "/appareils/"),
    ("FAQ", "/faq/"),
    ("Blog", "/blog/"),
    ("Contact", "/contact/"),
]

LOGO_SVG = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<circle cx="12" cy="12" r="10.2" stroke="currentColor" stroke-width="1.9"/>'
            '<path d="M10 8.4 16 12l-6 3.6z" fill="currentColor"/></svg>')

LOGO_MARQUE = ('<a class="logo" href="/" aria-label="' + MARQUE + ' — accueil">'
               '<span class="logo-pastille">' + LOGO_SVG + '</span>'
               '<span class="logo-mot"><b>IPTV</b> Abonnement <em>France</em></span>'
               '</a>')


def head(titre, description, chemin, og_type="website", schemas=None, robots=None):
    canonical = DOMAINE + chemin
    s = ""
    for sc in (schemas or []):
        s += ('\n  <script type="application/ld+json">'
              + json.dumps(sc, ensure_ascii=False, separators=(",", ":"))
              + "</script>")
    rb = robots or "index, follow, max-image-preview:large, max-snippet:-1"
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titre)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="robots" content="{rb}">
  <meta name="racine" content="/">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#08090B">
  <meta name="author" content="{MARQUE}">

  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{MARQUE}">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="{html.escape(titre)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAINE}/assets/img/og-image.svg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(titre)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{DOMAINE}/assets/img/og-image.svg">

  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/img/favicon.svg">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
  <link rel="stylesheet" href="/assets/css/style.css">{s}
</head>
<body>
"""


def header(actif=""):
    cur = ' aria-current="page"'
    liens = "".join(
        '<a href="%s"%s>%s</a>' % (u, cur if u == actif else "", n) for n, u in NAV
    )
    liens_mobile = liens
    return f"""<a class="btn btn--primaire" href="#contenu" style="position:absolute;left:-9999px;top:0"
   onfocus="this.style.left='12px';this.style.top='12px';this.style.zIndex='99'"
   onblur="this.style.left='-9999px'">Aller au contenu</a>

<header class="site-header">
  <div class="wrap barre-nav">
    {LOGO_MARQUE}
    <nav class="nav-liens" aria-label="Navigation principale">{liens}</nav>
    <div class="nav-actions">
      <a class="btn btn--fantome btn--sm" href="/contact/">Nous contacter</a>
      <a class="btn btn--primaire btn--sm" href="/abonnement-iptv/">Voir les abonnements</a>
      <button class="burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu-mobile">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<div class="tiroir" id="menu-mobile">
  {liens_mobile}
  <a class="btn btn--primaire" href="/abonnement-iptv/">Voir les abonnements</a>
  <a class="btn btn--fantome" href="/contact/">Nous contacter</a>
</div>

<main id="contenu">
"""


FOOTER = f"""</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grille">
      <div class="footer-col footer-intro">
        {LOGO_MARQUE}
        <p>Un service d'abonnement IPTV pensé pour les utilisateurs en France :
           installation claire, appareils compatibles, assistance en français.</p>
      </div>
      <div class="footer-col">
        <h4>Le service</h4>
        <ul>
          <li><a href="/abonnement-iptv/">Abonnement IPTV</a></li>
          <li><a href="/iptv-france/">IPTV France</a></li>
          <li><a href="/fonctionnalites/">Fonctionnalités</a></li>
          <li><a href="/appareils/">Appareils compatibles</a></li>
          <li><a href="/iptv-smarters-pro/">IPTV Smarters Pro</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Aide</h4>
        <ul>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="#" data-email>contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Informations légales</h4>
        <ul>
          <li><a href="/mentions-legales/">Mentions légales</a></li>
          <li><a href="/politique-confidentialite/">Politique de confidentialité</a></li>
          <li><a href="/conditions-generales/">Conditions générales</a></li>
          <li><a href="/politique-remboursement/">Politique de remboursement</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
    </div>

    <div class="avis-legal">
      <p><b>Utilisation responsable.</b> {MARQUE} fournit un accès à un service
      de diffusion et des informations de configuration. Nous n'hébergeons, ne produisons
      et ne contrôlons aucun contenu audiovisuel. Il appartient à chaque utilisateur de
      s'assurer qu'il dispose des droits nécessaires pour accéder aux contenus qu'il
      consulte et de n'utiliser le service qu'avec des contenus autorisés, dans le respect
      de la législation française et européenne en vigueur, notamment le Code de la
      propriété intellectuelle. Toute utilisation contraire relève de la seule
      responsabilité de l'utilisateur.</p>
    </div>

    <div class="footer-bas">
      <span>© <span data-annee>2026</span> {MARQUE} — iptvabonnementfrance.store</span>
      <span class="tricolore" aria-hidden="true"><i></i><i></i><i></i></span>
    </div>
  </div>
</footer>

<a class="wa-flottant" data-whatsapp-flottant href="#" aria-label="Nous écrire sur WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.174.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.82 9.82 0 0 1 6.988 2.896 9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0 0 20.465 3.49"/></svg>
</a>
<span class="wa-bulle">Une question ? Écrivez-nous sur WhatsApp</span>

<script src="/assets/js/indicatifs.js"></script>
<script src="/assets/js/config.js"></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def ariane(items):
    """items : liste de (libellé, url|None)"""
    li = []
    for nom, url in items:
        li.append(f'<li><a href="{url}">{nom}</a></li>' if url else f"<li>{nom}</li>")
    return ('<nav class="ariane wrap" aria-label="Fil d\'Ariane"><ol>'
            + "".join(li) + "</ol></nav>")


def schema_ariane(items):
    el = []
    for i, (nom, url) in enumerate(items, 1):
        e = {"@type": "ListItem", "position": i, "name": nom}
        if url:
            e["item"] = DOMAINE + url
        el.append(e)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}


SCHEMA_ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": DOMAINE + "/#organisation",
    "name": MARQUE,
    "url": DOMAINE + "/",
    "logo": DOMAINE + "/assets/img/favicon.svg",
    "areaServed": {"@type": "Country", "name": "France"},
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "service client",
        "telephone": "+16615413954",
        "availableLanguage": ["fr", "en"],
        "url": DOMAINE + "/contact/",
    },
}

SCHEMA_SITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": DOMAINE + "/#site",
    "name": MARQUE,
    "url": DOMAINE + "/",
    "inLanguage": "fr-FR",
    "publisher": {"@id": DOMAINE + "/#organisation"},
}


def schema_faq(paires):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": r}}
            for q, r in paires
        ],
    }


def faq_html(paires, ouvrir_premier=True):
    out = ['<div class="faq">']
    for i, (q, r) in enumerate(paires):
        ouvert = ouvrir_premier and i == 0
        out.append(
            f'<div class="faq-item{" est-ouvert" if ouvert else ""}">'
            f'<button class="faq-q" type="button" aria-expanded="{"true" if ouvert else "false"}">{q}</button>'
            f'<div class="faq-r"><div><p>{r}</p></div></div></div>'
        )
    out.append("</div>")
    return "".join(out)


CTA_FINAL = """
<section class="section">
  <div class="wrap">
    <div class="cta-final reveal">
      <p class="eyebrow" style="justify-content:center">Prêt à commencer</p>
      <h2>Choisissez l'abonnement IPTV qui correspond à vos usages</h2>
      <p>Comparez les durées, vérifiez la compatibilité de votre appareil et lancez-vous.
         Notre équipe reste disponible si vous avez la moindre question.</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn btn--primaire" href="/abonnement-iptv/">Voir nos abonnements</a>
        <a class="btn btn--fantome" href="/contact/">Poser une question</a>
      </div>
    </div>
  </div>
</section>
"""


def ecrire(chemin, contenu):
    """chemin : '/abonnement-iptv/' -> site/abonnement-iptv/index.html"""
    if chemin == "/":
        dest = os.path.join(RACINE, "index.html")
    else:
        d = os.path.join(RACINE, chemin.strip("/"))
        os.makedirs(d, exist_ok=True)
        dest = os.path.join(d, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(contenu)
    return dest


def page(chemin, titre, description, corps, ariane_items=None, actif="",
         schemas=None, og_type="website", robots=None):
    sch = list(schemas or [])
    fil = ""
    if ariane_items:
        sch.append(schema_ariane(ariane_items))
        fil = ariane(ariane_items)
    doc = head(titre, description, chemin, og_type, sch, robots) + header(actif) + fil + corps + FOOTER
    return ecrire(chemin, doc)
