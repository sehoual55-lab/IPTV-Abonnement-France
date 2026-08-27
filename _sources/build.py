# -*- coding: utf-8 -*-
import os, datetime
from tpl import (page, ecrire, RACINE, DOMAINE, MARQUE, SCHEMA_ORG, SCHEMA_SITE,
                 schema_faq, faq_html, CTA_FINAL)
import contenu as C
from articles import ARTICLES
from lire_config import charger

CFG = charger()

def schema_offres():
    """Product/Offer généré depuis config.js — n'inclut que les prix réellement définis."""
    offres = []
    for o in CFG.get("offres", []):
        if o.get("prix") in (None, ""):
            continue
        offres.append({
            "@type": "Offer",
            "name": "%s — %s" % (o["nom"], o["duree"]),
            "price": "%.2f" % float(o["prix"]),
            "priceCurrency": "EUR",
            "availability": "https://schema.org/InStock",
            "url": DOMAINE + "/abonnement-iptv/",
            "priceValidUntil": str(datetime.date.today().replace(year=datetime.date.today().year + 1)),
        })
    if not offres:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Abonnement IPTV France",
        "description": "Abonnement IPTV pour la France, compatible Smart TV, Android, Apple, "
                       "Fire TV, Roku, Xbox, PC et mobile. Installation guidée et support en français.",
        "brand": {"@type": "Brand", "name": MARQUE},
        "category": "Abonnement IPTV",
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "EUR",
            "lowPrice": "%.2f" % min(float(o["prix"]) for o in CFG["offres"] if o.get("prix")),
            "highPrice": "%.2f" % max(float(o["prix"]) for o in CFG["offres"] if o.get("prix")),
            "offerCount": len(offres),
            "offers": offres,
        },
    }

SCHEMA_PRODUIT = schema_offres()

AUJ = datetime.date.today().isoformat()
URLS = []


def enr(chemin, prio, freq="monthly"):
    URLS.append((chemin, prio, freq))


# ============================================================== ACCUEIL =====
hero = f"""
<section class="hero">
  <div class="wrap hero-grille">
    <div class="hero-texte">
      <span class="badge-direct"><span class="pastille"></span>Service disponible en France</span>
      <h1>IPTV Abonnement France <em>Profitez de la TV en streaming</em></h1>
      <p class="lead">Découvrez une solution IPTV moderne pour regarder vos chaînes, films, séries
        et programmes préférés sur vos appareils. Mise en service guidée, assistance en français.</p>
      <div class="btn-row">
        <a class="btn btn--primaire" href="/abonnement-iptv/">Voir nos abonnements</a>
        <a class="btn btn--fantome" href="/iptv-france/">Découvrir IPTV</a>
      </div>
      <p class="ligne-confiance">Compatible Smart TV • Fire TV • Android • Apple • PC • Smartphone</p>
    </div>
    {C.TV_VISUEL}
  </div>
</section>
"""

intro_abo = """
<section class="section section--line">
  <div class="wrap grille-2" style="gap:56px;align-items:start">
    <div class="reveal">
      <p class="eyebrow">Le service</p>
      <h2>Abonnement IPTV France</h2>
      <p>Un <strong>abonnement IPTV France</strong> vous donne accès à un service de télévision
        diffusé par votre connexion Internet, sans antenne ni parabole. Après votre commande, vous
        recevez des informations de configuration à saisir dans une application de lecture compatible :
        votre téléviseur, votre boîtier ou votre mobile affiche alors les contenus auxquels votre
        abonnement vous donne accès.</p>
      <p>Le principe est le même quel que soit l'appareil. Un lecteur IPTV se connecte au serveur,
        récupère la liste des contenus disponibles et les affiche dans une interface organisée par
        catégories, avec un guide des programmes. C'est ce qui rend l'<strong>abonnement IPTV
        français</strong> aussi simple à mettre en place sur un téléviseur récent que sur un ordinateur.</p>
      <div class="btn-row"><a class="btn btn--primaire" href="/abonnement-iptv/">Choisir mon abonnement</a></div>
    </div>
    <div class="reveal">
      <div class="carte" style="margin-bottom:16px">
        <h3>Une installation en trois gestes</h3>
        <p>Installer un lecteur compatible, saisir vos informations de connexion, laisser la liste se
          charger. Notre guide détaille chaque étape selon votre appareil, et notre équipe prend le
          relais si vous bloquez.</p>
      </div>
      <div class="carte" style="margin-bottom:16px">
        <h3>Des appareils que vous avez déjà</h3>
        <p>Téléviseur connecté, boîtier Android TV, clé HDMI, ordinateur, smartphone ou tablette :
          si un lecteur IPTV peut y être installé, votre abonnement s'y utilise.</p>
      </div>
      <div class="carte">
        <h3>Une assistance qui répond</h3>
        <p>Avant la commande pour vérifier la compatibilité de votre modèle, pendant l'installation,
          et ensuite si vous changez d'appareil. En français, par écrit.</p>
      </div>
    </div>
  </div>
</section>
"""

chiffres = """
<section class="section section--line">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">En chiffres</p>
      <h2>Notre service en quelques repères</h2>
    </div>
    <div class="grille-4" data-chiffres></div>
  </div>
</section>
"""

smarters_court = """
<section class="section section--line">
  <div class="wrap grille-2" style="gap:56px;align-items:center">
    <div class="reveal">
      <p class="eyebrow">Lecteurs compatibles</p>
      <h2>IPTV Smarters Pro : une solution simple pour votre streaming</h2>
      <p>Les lecteurs IPTV comme <strong>IPTV Smarters Pro</strong> servent d'interface entre votre
        abonnement et votre écran. L'application ne fournit aucune chaîne par elle-même : elle affiche
        uniquement le contenu auquel votre service autorisé vous donne accès, une fois vos informations
        de connexion saisies.</p>
      <p>C'est ce fonctionnement qui rend l'installation aussi rapide : vous téléchargez le lecteur
        depuis la boutique officielle de votre appareil, vous renseignez vos accès, et la liste se
        charge.</p>
      <div class="btn-row"><a class="btn btn--fantome" href="/iptv-smarters-pro/">Découvrir la compatibilité</a></div>
    </div>
    <div class="carte reveal">
      <h3>Ce que fait un lecteur IPTV</h3>
      <ul class="offre-liste" style="border-top:0;padding-top:0;margin-bottom:0">
        <li>Il se connecte au service auquel vous êtes abonné</li>
        <li>Il charge la liste des contenus disponibles</li>
        <li>Il décode et affiche le flux vidéo sur votre écran</li>
        <li>Il gère les favoris et le guide des programmes</li>
        <li>Il ne diffuse aucun contenu de son propre chef</li>
      </ul>
    </div>
  </div>
</section>
"""

seo_meilleur = """
<section class="section section--line section--surface">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Bien choisir</p>
      <h2>Quel est le meilleur abonnement IPTV en France ?</h2>
    </div>
    <div class="prose reveal">
      <p>La question revient à chaque recherche, et elle mérite une réponse honnête : il n'existe pas
      de <strong>meilleur abonnement IPTV France</strong> universel. Le service qui convient à un
      utilisateur équipé d'un boîtier Android récent et d'une connexion fibre ne donnera pas le même
      résultat sur un téléviseur de 2016 relié en Wi-Fi. La bonne façon de se poser la question est
      donc : quel abonnement fonctionne le mieux avec mon matériel et mes usages ?</p>

      <h3>La compatibilité passe avant le prix</h3>
      <p>Vérifiez d'abord qu'un lecteur IPTV est installable sur votre appareil. Sur les téléviseurs
      plus anciens, la boutique intégrée ne propose parfois plus rien : une clé HDMI ou un boîtier
      Android TV règle la question pour un budget modeste, et vous évite un abonnement inutilisable.</p>

      <h3>La fiabilité se vérifie à l'usage</h3>
      <p>Un flux fluide en journée ne présage pas de son comportement un soir de forte affluence.
      C'est précisément pourquoi commencer par une durée courte a du sens : vous testez le service au
      moment où vous l'utilisez réellement. Ceux qui se demandent <em>quel est l'IPTV le plus fiable</em>
      trouveront rarement la réponse dans un classement — mais toujours dans quelques soirées d'essai.</p>

      <h3>Le support est un critère, pas un bonus</h3>
      <p>Posez une question technique précise avant de payer. Le délai et la qualité de la réponse
      vous renseignent mieux que n'importe quel argument commercial sur ce qui vous attend le jour où
      quelque chose ne fonctionnera pas.</p>

      <h3>L'installation doit être documentée</h3>
      <p>Un service sérieux fournit des instructions adaptées à votre appareil, pas un texte générique.
      Si la documentation est confuse avant l'achat, elle ne le sera pas moins après.</p>

      <h3>Le tarif se juge sur la durée</h3>
      <p>Ramenez chaque offre à un coût mensuel, puis intégrez le risque : une durée longue chez un
      prestataire jamais testé n'est pas une économie, c'est un pari. La progression raisonnable
      consiste à valider d'abord, s'engager ensuite.</p>

      <h3>Les fonctionnalités doivent correspondre à vos usages</h3>
      <p>Nombre d'écrans simultanés, présence d'un guide des programmes, contenus à la demande,
      gestion des favoris : la question <em>quel abonnement IPTV France</em> choisir se règle en
      confrontant cette liste à ce que vous regardez vraiment, plutôt qu'à ce qui est le plus mis en avant.</p>

      <div class="encart"><p>Un dernier repère : un prestataire qui explique clairement les
      responsabilités de l'utilisateur et le cadre légal applicable en France ne cherche pas à masquer
      le sujet. C'est un bon signe sur son sérieux général.</p></div>
    </div>
  </div>
</section>
"""

# 3 derniers articles pour l'accueil
def cartes_blog(liste):
    out = []
    for a in liste:
        out.append(f"""
<article class="article-carte reveal">
  <a href="/blog/{a['slug']}/" aria-label="{a['h1']}">
    <div class="article-visuel" style="--a1:{a['c1']};--a2:{a['c2']}"><span>{a['cat']}</span></div>
  </a>
  <div class="article-corps">
    <h3><a href="/blog/{a['slug']}/">{a['h1']}</a></h3>
    <p>{a['resume']}</p>
    <a class="article-lien" href="/blog/{a['slug']}/">Lire l'article →</a>
  </div>
</article>""")
    return "".join(out)


blog_accueil = f"""
<section class="section section--line">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Blog</p>
      <h2>Guides et conseils IPTV</h2>
      <p class="lead">Des articles pratiques pour choisir, installer et régler votre service, sans jargon inutile.</p>
    </div>
    <div class="grille-blog">{cartes_blog(ARTICLES[:3])}</div>
    <div class="btn-row"><a class="btn btn--fantome" href="/blog/">Tous les articles</a></div>
  </div>
</section>
"""

page(
    "/",
    "IPTV Abonnement France | Abonnement IPTV français premium",
    "IPTV abonnement France : profitez de la TV en streaming sur Smart TV, Fire TV, "
    "Android, Apple, PC et smartphone. Installation simple et assistance en français.",
    hero + C.bandeau_confiance() + intro_abo + C.section_tarifs() + C.section_fonctionnalites()
    + C.section_appareils() + smarters_court + C.section_pourquoi() + C.section_etapes()
    + seo_meilleur + chiffres + C.section_faq(C.FAQ_PRINCIPALE[:6]) + blog_accueil
    + C.section_whatsapp() + CTA_FINAL,
    actif="/",
    schemas=[x for x in [SCHEMA_ORG, SCHEMA_SITE, SCHEMA_PRODUIT,
                         schema_faq(C.FAQ_PRINCIPALE[:6])] if x],
)
enr("/", "1.0", "weekly")


# ====================================================== ABONNEMENT IPTV =====
ar = [("Accueil", "/"), ("Abonnement IPTV", None)]
corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Nos offres</p>
      <h1>Abonnement IPTV France : nos formules</h1>
      <p class="lead">Quatre durées, la même mise en service et la même assistance. Choisissez la
        période qui correspond à votre usage — et si vous découvrez l'IPTV, commencez court.</p>
    </div>
  </div>
</section>
{C.section_tarifs("Choisissez la durée de votre abonnement", "Les tarifs affichés correspondent à une connexion. Chaque connexion supplémentaire est facturée 15 % moins cher — ajustez le compteur sur la carte de votre choix.")}
{C.section_etapes("Comment se passe la souscription ?")}
<section class="section section--line section--surface">
  <div class="wrap prose reveal">
    <h2>Quelle durée choisir pour votre abonnement IPTV ?</h2>
    <p>Le choix de la durée dépend surtout de trois éléments : le nombre d'écrans utilisés en même
    temps dans votre foyer, votre régularité d'utilisation, et ce que vous savez déjà du service.</p>
    <h3>Vous découvrez l'IPTV</h3>
    <p>Prenez une durée courte. Elle coûte plus cher au mois, mais elle achète une information qui
    vaut largement la différence : est-ce que le service fonctionne bien avec votre téléviseur et
    votre connexion, à vos heures d'utilisation ?</p>
    <h3>Vous utilisez déjà le service</h3>
    <p>Une durée plus longue réduit nettement le coût mensuel. Elle suppose simplement que vous ayez
    déjà validé la compatibilité de votre matériel et la réactivité du support.</p>
    <h3>Plusieurs personnes regardent en même temps</h3>
    <p>Vérifiez le nombre de connexions simultanées <em>avant</em> de vous intéresser à la durée.
    C'est la première cause de déception quand le point n'a pas été clarifié à la commande.</p>
    <div class="encart"><p>Un doute sur la formule adaptée à votre foyer ?
    <a href="/contact/">Écrivez-nous</a> en précisant le nombre d'écrans et vos appareils :
    nous vous orienterons sans vous vendre plus que nécessaire.</p></div>
  </div>
</section>
{C.section_appareils("Vérifiez la compatibilité de votre appareil")}
{C.section_faq(C.FAQ_PRINCIPALE[3:8], "Questions sur nos abonnements")}
{C.section_whatsapp("Un doute sur la formule ? Demandez-nous")}
{CTA_FINAL}
"""
page("/abonnement-iptv/",
     "Abonnement IPTV France : formules 1, 6, 12 et 24 mois | Tarifs",
     "Découvrez nos formules d'abonnement IPTV France : 1, 6, 12 ou 24 mois. "
     "Installation guidée, appareils compatibles et assistance en français.",
     corps, ar, actif="/abonnement-iptv/",
     schemas=[x for x in [SCHEMA_ORG, SCHEMA_PRODUIT,
                          schema_faq(C.FAQ_PRINCIPALE[3:8])] if x])
enr("/abonnement-iptv/", "0.9", "weekly")


# =========================================================== IPTV FRANCE ====
ar = [("Accueil", "/"), ("IPTV France", None)]
corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Comprendre</p>
      <h1>IPTV France : comment ça marche et à quoi s'attendre</h1>
      <p class="lead">Le fonctionnement, le matériel nécessaire, la question de la connexion et le
        cadre légal applicable en France — expliqués simplement.</p>
    </div>
    <div class="prose reveal">
      <h2>Qu'est-ce que l'IPTV, concrètement ?</h2>
      <p>IPTV signifie « télévision sur protocole Internet ». Au lieu de recevoir un signal par une
      antenne, une parabole ou le câble, votre appareil se connecte à un serveur qui lui transmet un
      flux vidéo par votre connexion Internet. Un lecteur installé sur votre appareil décode ce flux
      et l'affiche à l'écran.</p>
      <p>Trois maillons interviennent donc : le service auquel vous êtes abonné, votre connexion
      Internet, et l'appareil qui décode. Cette distinction est utile au quotidien : lorsqu'une image
      saccade, la cause peut se situer à n'importe lequel de ces trois niveaux, et le réflexe le plus
      efficace consiste à tester sur un second appareil pour isoler l'origine.</p>

      <h2>Ce dont vous avez besoin</h2>
      <ul>
        <li><strong>Un appareil compatible</strong> — téléviseur connecté, boîtier Android TV, clé
        HDMI, ordinateur, smartphone ou tablette.</li>
        <li><strong>Une connexion stable</strong> — la régularité compte davantage que le débit brut.</li>
        <li><strong>Un lecteur IPTV</strong> — installé depuis la boutique officielle de votre appareil.</li>
        <li><strong>Vos informations de connexion</strong> — transmises après votre commande.</li>
      </ul>

      <h2>Quelle connexion Internet faut-il en France ?</h2>
      <p>Une fibre confortable est un plus, mais une bonne connexion ADSL stable donne souvent de
      meilleurs résultats qu'une fibre saturée par d'autres usages simultanés. Deux gestes simples
      améliorent nettement le confort : relier l'appareil en Ethernet lorsque la prise est accessible,
      et éviter de lancer un téléchargement volumineux pendant la lecture.</p>

      <h2>Le cadre légal en France</h2>
      <p>En France, la diffusion et l'accès aux contenus audiovisuels sont encadrés par le Code de la
      propriété intellectuelle. Un prestataire technique ne transfère pas cette responsabilité à sa
      place : il appartient à chaque utilisateur de s'assurer qu'il dispose des droits nécessaires pour
      accéder aux contenus qu'il consulte, et de n'utiliser un service de diffusion qu'avec des
      contenus autorisés.</p>
      <p>Nous préférons afficher cette information clairement plutôt que de la contourner. Un service
      qui n'aborde jamais le sujet ne vous rend pas service, quelle que soit la qualité de sa page d'accueil.</p>

      <h2>Les erreurs les plus fréquentes</h2>
      <ul>
        <li>S'engager sur une longue durée chez un prestataire jamais testé.</li>
        <li>Ne pas vérifier la compatibilité de son téléviseur avant de payer.</li>
        <li>Ignorer le nombre d'écrans simultanés prévu par l'offre.</li>
        <li>Partager ses identifiants, ce qui entraîne coupures et blocages.</li>
        <li>Attribuer au service des problèmes venant d'un Wi-Fi saturé.</li>
      </ul>
    </div>
  </div>
</section>
{C.section_pourquoi()}
{C.section_appareils()}
{C.section_faq(C.FAQ_PRINCIPALE[:5], "Questions fréquentes sur l'IPTV en France")}
{CTA_FINAL}
"""
page("/iptv-france/",
     "IPTV France : fonctionnement, matériel et cadre légal | Guide",
     "IPTV France : comment fonctionne la télévision par Internet, quel matériel prévoir, "
     "quelle connexion et quelles sont vos responsabilités légales.",
     corps, ar, schemas=[SCHEMA_ORG, schema_faq(C.FAQ_PRINCIPALE[:5])])
enr("/iptv-france/", "0.8")


# ====================================================== IPTV SMARTERS PRO ===
ar = [("Accueil", "/"), ("IPTV Smarters Pro", None)]
faq_sm = [
    ("IPTV Smarters Pro fournit-il des chaînes ?",
     "Non. C'est une application de lecture. Elle n'héberge, ne produit et ne diffuse aucun contenu : "
     "elle affiche uniquement ce à quoi votre service autorisé vous donne accès, une fois vos "
     "informations de connexion saisies."),
    ("Sur quels appareils peut-on l'installer ?",
     "Le lecteur existe sur Android et Android TV, iOS et Apple TV, ainsi que sur ordinateur Windows "
     "et macOS. Sur certains téléviseurs connectés, il est également disponible dans la boutique "
     "intégrée selon la marque et l'année du modèle."),
    ("Où faut-il télécharger l'application ?",
     "Uniquement depuis la boutique officielle de votre appareil. Les versions modifiées qui circulent "
     "sur des sites tiers peuvent contenir du code indésirable et compromettre vos identifiants."),
    ("Que faire si mes identifiants sont refusés ?",
     "Ressaisissez-les caractère par caractère en surveillant les confusions classiques entre le "
     "chiffre zéro et la lettre O, ou entre le chiffre un et la lettre l minuscule. Vérifiez aussi "
     "l'absence d'espace en fin de champ."),
    ("Peut-on utiliser un autre lecteur ?",
     "Oui. Plusieurs lecteurs IPTV fonctionnent selon le même principe. Le choix dépend surtout de ce "
     "qui est disponible sur votre appareil et de l'interface que vous préférez."),
]
corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Lecteurs compatibles</p>
      <h1>IPTV Smarters Pro : une solution simple pour votre streaming</h1>
      <p class="lead">Comment fonctionne un lecteur IPTV, ce qu'il fait — et surtout ce qu'il ne fait
        pas — et comment le configurer avec votre abonnement.</p>
    </div>
    <div class="prose reveal">
      <h2>Un lecteur, pas un fournisseur de contenu</h2>
      <p>C'est le point le plus important et le plus souvent mal compris. Une application comme
      <strong>IPTV Smarters Pro</strong> est un lecteur : un logiciel qui se connecte à un service
      auquel vous êtes abonné, récupère la liste des contenus autorisés et les affiche. L'application
      elle-même ne fournit aucune chaîne, aucun film et aucune série.</p>
      <p>Concrètement, installer le lecteur sans abonnement actif ne donne accès à rien du tout.
      C'est la même logique qu'un navigateur web : l'outil affiche, il ne produit pas.</p>

      <h2>Installer le lecteur</h2>
      <p>Le téléchargement se fait exclusivement depuis la boutique officielle de votre appareil :
      Play Store sur Android et Android TV, App Store sur iOS et Apple TV, boutique intégrée sur
      certains téléviseurs. Une version de bureau existe également pour Windows et macOS.</p>
      <p>Évitez systématiquement les fichiers d'installation proposés par des sites tiers. Les versions
      modifiées qui circulent peuvent embarquer du code indésirable, et vos identifiants y sont exposés.</p>

      <h2>Configurer votre abonnement</h2>
      <p>Au premier lancement, le lecteur propose d'ajouter un utilisateur. Selon les informations
      transmises par votre fournisseur, vous saisissez soit un nom d'utilisateur, un mot de passe et
      une adresse de serveur, soit l'adresse d'une liste à charger. Dans les deux cas, la saisie doit
      être exacte : la casse compte, et un espace en trop suffit à faire échouer la connexion.</p>
      <p>Le lecteur télécharge ensuite la liste des contenus. Selon le volume, cela prend de quelques
      secondes à deux minutes. Ne quittez pas l'application pendant cette étape.</p>

      <h2>Les réglages qui améliorent le confort</h2>
      <ul>
        <li><strong>Tampon de lecture</strong> — à augmenter en cas de micro-coupures régulières.</li>
        <li><strong>Moteur de décodage</strong> — plusieurs sont proposés ; en essayer un autre règle
        la plupart des contenus qui refusent de se lancer.</li>
        <li><strong>Guide des programmes</strong> — à activer pour afficher les horaires dans l'interface.</li>
        <li><strong>Favoris</strong> — à organiser dès le départ si la liste de chaînes est longue.</li>
      </ul>

      <h2>Utilisation responsable</h2>
      <p>Un lecteur IPTV est un outil neutre, largement utilisé par des services parfaitement légaux.
      Sa légitimité dépend donc entièrement du service auquel vous le connectez. Assurez-vous de
      disposer des droits nécessaires pour accéder aux contenus que vous consultez et n'utilisez le
      lecteur qu'avec des services et des contenus autorisés.</p>

      <div class="btn-row"><a class="btn btn--primaire" href="/appareils/">Découvrir la compatibilité</a></div>
    </div>
  </div>
</section>
{C.section_appareils("Sur quels appareils installer votre lecteur ?")}
{C.section_faq(faq_sm, "Questions fréquentes sur IPTV Smarters Pro")}
{CTA_FINAL}
"""
page("/iptv-smarters-pro/",
     "Abonnement IPTV Smarters Pro : configuration et compatibilité",
     "IPTV Smarters Pro : comment fonctionne ce lecteur IPTV, sur quels appareils l'installer "
     "et comment le configurer avec votre abonnement IPTV.",
     corps, ar, schemas=[SCHEMA_ORG, schema_faq(faq_sm)])
enr("/iptv-smarters-pro/", "0.8")


# ============================================================= APPAREILS ====
ar = [("Accueil", "/"), ("Appareils", None)]
faq_app = [
    ("Mon téléviseur est ancien, puis-je quand même utiliser l'IPTV ?",
     "Oui, dans la quasi-totalité des cas. Une clé HDMI ou un boîtier Android TV branché sur une prise "
     "HDMI libre remplace la partie applicative du téléviseur, qui redevient un simple écran."),
    ("Combien d'appareils puis-je utiliser ?",
     "Cela dépend du nombre de connexions simultanées prévu par votre offre. Contactez-nous avant la "
     "commande si plusieurs personnes regardent en même temps chez vous."),
    ("Le Wi-Fi suffit-il ?",
     "Le Wi-Fi fonctionne, mais une liaison Ethernet reste nettement plus stable, surtout pour les "
     "contenus en haute définition et aux heures de forte affluence."),
]
corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Compatibilité</p>
      <h1>Regardez votre contenu sur vos appareils préférés</h1>
      <p class="lead">Une expérience adaptée à votre écran. Voici les appareils sur lesquels un lecteur
        IPTV compatible peut être installé — et quoi faire quand le vôtre n'en propose aucun.</p>
    </div>
  </div>
</section>
{C.section_appareils("Appareils pris en charge", "h2")}
<section class="section section--line section--surface">
  <div class="wrap prose reveal">
    <h2>Ce qui change d'un système à l'autre</h2>
    <h3>Samsung (Tizen) et LG (webOS)</h3>
    <p>Les boutiques intégrées de ces deux marques proposent des lecteurs compatibles, avec une réserve
    importante : la disponibilité varie selon l'année du modèle et la région. Sur des téléviseurs plus
    anciens, certaines applications ont été retirées du catalogue et ne réapparaîtront pas.</p>
    <h3>Android TV et Google TV</h3>
    <p>C'est le terrain le plus confortable : large choix de lecteurs, mises à jour régulières, bonne
    réactivité. Si vous avez le choix à l'achat d'un boîtier, c'est l'option qui pose le moins de questions.</p>
    <h3>Apple TV</h3>
    <p>L'écosystème est plus fermé, mais les lecteurs disponibles sont bien suivis et l'expérience
    reste fluide. Un bon choix si vous êtes déjà équipé chez Apple.</p>
    <h3>Ordinateurs, mobiles et tablettes</h3>
    <p>Windows, macOS, Android et iOS disposent tous de lecteurs compatibles. Le fonctionnement est
    identique : installation, saisie des identifiants, chargement de la liste.</p>

    <h2>Quand votre téléviseur ne propose rien</h2>
    <p>C'est une situation courante et facile à résoudre. Trois options, par ordre de budget :</p>
    <ul>
      <li><strong>Clé HDMI</strong> — compacte et économique, suffisante pour un usage courant.</li>
      <li><strong>Boîtier Android TV</strong> — plus polyvalent et généralement plus réactif.</li>
      <li><strong>Apple TV</strong> — le plus fluide, pertinent si vous êtes dans l'écosystème Apple.</li>
    </ul>

    <div class="encart"><p>Avant de commander, indiquez-nous la marque, le modèle et l'année de votre
    appareil. Nous vérifions ensemble qu'un lecteur compatible existe pour lui — plutôt que de vous
    laisser le découvrir après l'achat.</p></div>
  </div>
</section>
{C.section_faq(faq_app, "Questions sur la compatibilité")}
{C.section_whatsapp("Envoyez-nous le modèle de votre appareil")}
{CTA_FINAL}
"""
page("/appareils/",
     "Appareils compatibles IPTV : Smart TV, Fire TV, Android, Apple, PC",
     "Quels appareils sont compatibles avec un abonnement IPTV ? Smart TV Samsung et LG, "
     "Fire TV Stick, Android TV, Apple TV, smartphone, tablette et ordinateur.",
     corps, ar, actif="/appareils/", schemas=[SCHEMA_ORG, schema_faq(faq_app)])
enr("/appareils/", "0.8")


# ======================================================== FONCTIONNALITÉS ===
ar = [("Accueil", "/"), ("Fonctionnalités", None)]
corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Fonctionnalités</p>
      <h1>Pourquoi choisir notre abonnement IPTV France ?</h1>
      <p class="lead">Ce que vous retrouvez concrètement une fois votre abonnement activé et votre
        lecteur configuré — sans promesse invérifiable.</p>
    </div>
  </div>
</section>
{C.section_fonctionnalites("Les fonctionnalités du service", "h2")}
{C.section_pourquoi("Nos quatre engagements", "h2")}
<section class="section section--line">
  <div class="wrap prose reveal">
    <h2>Ce que nous ne promettons pas</h2>
    <p>Aucun service diffusé par Internet ne peut garantir un fonctionnement parfait en permanence :
    la qualité dépend de la source, de votre connexion et de votre appareil, et ces trois éléments
    varient. Nous préférons l'écrire plutôt que d'afficher une garantie que personne ne peut tenir.</p>
    <p>Ce que nous pouvons vous engager, en revanche : une installation documentée, un support qui
    répond en français, des conditions écrites et accessibles, et une information honnête sur la
    compatibilité de votre matériel avant que vous ne commandiez.</p>
    <div class="encart"><p>Une question sur une fonctionnalité précise avant de vous décider ?
    <a href="/contact/">Posez-la nous</a> — une réponse claire avant l'achat vaut mieux qu'une
    déception après.</p></div>
  </div>
</section>
{C.section_etapes()}
{CTA_FINAL}
"""
page("/fonctionnalites/",
     "Fonctionnalités de notre abonnement IPTV France | Le service en détail",
     "Les fonctionnalités de notre abonnement IPTV France : compatibilité multi-appareils, "
     "contenus à la demande, guide des programmes, installation simple et assistance.",
     corps, ar, actif="/fonctionnalites/", schemas=[SCHEMA_ORG])
enr("/fonctionnalites/", "0.7")


# =================================================================== FAQ ====
ar = [("Accueil", "/"), ("FAQ", None)]
corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Aide</p>
      <h1>Questions fréquentes sur l'abonnement IPTV</h1>
      <p class="lead">Les réponses aux questions que l'on nous pose le plus souvent, du fonctionnement
        de l'IPTV à la configuration de votre appareil.</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">{faq_html(C.FAQ_PRINCIPALE)}</div>
</section>
<section class="section section--line section--surface">
  <div class="wrap prose reveal">
    <h2>Vous n'avez pas trouvé votre réponse ?</h2>
    <p>Écrivez-nous en précisant votre appareil, le lecteur utilisé et la description exacte du
    problème rencontré. Plus votre message est précis, plus notre réponse le sera : c'est la façon la
    plus rapide d'avancer.</p>
    <div class="btn-row"><a class="btn btn--primaire" href="/contact/">Contacter le support</a></div>
  </div>
</section>
{C.section_whatsapp("Posez votre question directement sur WhatsApp")}
{CTA_FINAL}
"""
page("/faq/",
     "FAQ IPTV : réponses aux questions fréquentes | IPTV Abonnement France",
     "Toutes les réponses sur l'abonnement IPTV en France : fonctionnement, souscription, "
     "appareils compatibles, installation d'un lecteur et contact du support.",
     corps, ar, actif="/faq/", schemas=[SCHEMA_ORG, schema_faq(C.FAQ_PRINCIPALE)])
enr("/faq/", "0.8")


# ================================================================= BLOG =====
ar = [("Accueil", "/"), ("Blog", None)]
corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Blog</p>
      <h1>Guides et conseils sur l'IPTV en France</h1>
      <p class="lead">Choisir son abonnement, installer un lecteur, régler les problèmes courants :
        des articles pratiques, écrits pour être utiles plutôt que pour remplir une page.</p>
    </div>
    <div class="grille-blog">{cartes_blog(ARTICLES)}</div>
  </div>
</section>
{CTA_FINAL}
"""
page("/blog/",
     "Blog IPTV France : guides, comparatifs et tutoriels",
     "Le blog IPTV Abonnement France : guides pour choisir un abonnement IPTV, tutoriels "
     "d'installation, comparatifs et conseils de configuration.",
     corps, ar, actif="/blog/",
     schemas=[SCHEMA_ORG, {
         "@context": "https://schema.org", "@type": "Blog",
         "name": "Blog " + MARQUE, "url": DOMAINE + "/blog/", "inLanguage": "fr-FR",
         "publisher": {"@id": DOMAINE + "/#organisation"}}])
enr("/blog/", "0.8", "weekly")


# ------------------------------------------------------- Articles de blog ---
for i, a in enumerate(ARTICLES):
    autres = [x for x in ARTICLES if x["slug"] != a["slug"]][:4]
    lies = "".join('<li><a href="/blog/%s/">%s</a></li>' % (x["slug"], x["h1"]) for x in autres)
    cartes_liees = cartes_blog([ARTICLES[(i + 1) % len(ARTICLES)],
                                ARTICLES[(i + 2) % len(ARTICLES)],
                                ARTICLES[(i + 3) % len(ARTICLES)]])
    bloc_faq = ""
    schemas_art = []
    if a.get("faq"):
        bloc_faq = ('<h2>Questions fréquentes</h2>' + faq_html(a["faq"], False))
        schemas_art.append(schema_faq(a["faq"]))

    article_schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["h1"],
        "description": a["desc"],
        "inLanguage": "fr-FR",
        "mainEntityOfPage": {"@type": "WebPage", "@id": DOMAINE + "/blog/" + a["slug"] + "/"},
        "author": {"@type": "Organization", "name": MARQUE, "url": DOMAINE + "/"},
        "publisher": {"@id": DOMAINE + "/#organisation"},
        "articleSection": a["cat"],
    }
    schemas_art.insert(0, article_schema)

    ar_a = [("Accueil", "/"), ("Blog", "/blog/"), (a["h1"], None)]
    corps = f"""
<article class="section" style="padding-top:30px">
  <div class="wrap">
    <div class="section-head reveal" style="max-width:76ch">
      <p class="eyebrow">{a['cat']} · {a['temps']} de lecture</p>
      <h1>{a['h1']}</h1>
      <p class="lead">{a['resume']}</p>
    </div>
    <div class="mise-en-page-article">
      <div class="prose reveal">
        {a['corps']}
        {bloc_faq}
        <h2>Aller plus loin</h2>
        <p>Vous pouvez consulter nos <a href="/abonnement-iptv/">formules d'abonnement</a>, vérifier la
        <a href="/appareils/">compatibilité de votre appareil</a> ou parcourir la
        <a href="/faq/">foire aux questions</a>. Une question précise ?
        <a href="/contact/">Écrivez-nous</a>.</p>
      </div>
      <aside class="aside-sticky">
        <div class="aside-bloc">
          <h4>Voir les abonnements</h4>
          <p class="tiny" style="margin-bottom:14px">Quatre durées, une mise en service identique et
            une assistance en français.</p>
          <a class="btn btn--primaire btn--bloc btn--sm" href="/abonnement-iptv/">Découvrir les offres</a>
        </div>
        <div class="aside-bloc">
          <h4>Articles liés</h4>
          <ul>{lies}</ul>
        </div>
        <div class="aside-bloc">
          <h4>Besoin d'aide ?</h4>
          <p class="tiny" style="margin-bottom:14px">Indiquez-nous votre appareil et le point qui
            vous bloque : nous répondons avec la bonne procédure.</p>
          <a class="btn btn--fantome btn--bloc btn--sm" href="/contact/">Nous contacter</a>
        </div>
      </aside>
    </div>
  </div>
</article>
<section class="section section--line section--surface">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">À lire aussi</p>
      <h2>Articles similaires</h2>
    </div>
    <div class="grille-blog">{cartes_liees}</div>
  </div>
</section>
{CTA_FINAL}
"""
    page("/blog/%s/" % a["slug"], a["titre"], a["desc"], corps, ar_a,
         actif="/blog/", schemas=[SCHEMA_ORG] + schemas_art, og_type="article")
    enr("/blog/%s/" % a["slug"], "0.7")


# ============================================================== CONTACT =====
ar = [("Accueil", "/"), ("Contact", None)]
corps = """
<section class="section" style="padding-top:34px">
  <div class="wrap grille-2" style="gap:56px;align-items:start">
    <div class="reveal">
      <p class="eyebrow">Contact</p>
      <h1>Besoin d'aide ?</h1>
      <p class="lead">Notre équipe est disponible pour répondre à vos questions. Avant la commande
        pour vérifier la compatibilité de votre appareil, pendant l'installation, ou ensuite si vous
        rencontrez un problème.</p>

      <div class="carte" style="margin-top:26px">
        <h3>Pour une réponse plus rapide</h3>
        <p>Précisez dans votre message : la marque et le modèle de votre appareil, le lecteur IPTV
          utilisé, et le message d'erreur exact si vous en voyez un. Ces trois informations nous
          évitent un aller-retour et nous permettent de vous répondre directement avec la procédure adaptée.</p>
      </div>

      <div class="carte" style="margin-top:16px">
        <h3>Par e-mail</h3>
        <p>Vous pouvez également nous écrire directement à
          <a href="#" data-email style="color:var(--bleu-clair)">notre adresse de contact</a>.</p>
        <p style="margin-top:14px">WhatsApp : <a data-numero href="#" style="color:var(--vert-clair);font-family:var(--mono)">—</a></p>
        <p style="margin-top:12px"><a class="btn btn--vert btn--sm" data-whatsapp href="#">Écrire sur WhatsApp</a></p>
      </div>
    </div>

    <div class="carte reveal">
      <h2 style="font-size:1.3rem;margin-bottom:20px">Envoyez-nous un message</h2>
      <form class="formulaire" id="form-contact" novalidate>
        <div class="champ">
          <label for="nom">Nom</label>
          <input type="text" id="nom" name="nom" autocomplete="name" placeholder="Votre nom" required>
        </div>
        <div class="champ">
          <label for="email">E-mail</label>
          <input type="email" id="email" name="email" autocomplete="email" placeholder="vous@exemple.fr" required>
        </div>
        <div class="champ">
          <label for="sujet">Sujet</label>
          <input type="text" id="sujet" name="sujet" placeholder="Question sur un abonnement, installation…">
        </div>
        <div class="champ">
          <label for="message">Message</label>
          <textarea id="message" name="message" placeholder="Décrivez votre question ou le problème rencontré." required></textarea>
        </div>
        <div class="message-form" id="form-message" role="status" aria-live="polite"></div>
        <button class="btn btn--primaire btn--bloc" type="submit">Envoyer le message</button>
        <p class="tiny">En envoyant ce formulaire, vous acceptez que vos coordonnées soient utilisées
          uniquement pour répondre à votre demande. Consultez notre
          <a href="/politique-confidentialite/" style="color:var(--bleu-clair)">politique de confidentialité</a>.</p>
      </form>
    </div>
  </div>
</section>
"""
corps = C.section_whatsapp("Le plus rapide : WhatsApp") + corps

page("/contact/",
     "Contact | IPTV Abonnement France",
     "Une question sur votre abonnement IPTV, la compatibilité de votre appareil ou "
     "l'installation d'un lecteur ? Contactez notre équipe en français.",
     corps, ar, actif="/contact/",
     schemas=[SCHEMA_ORG, {"@context": "https://schema.org", "@type": "ContactPage",
                           "name": "Contact — " + MARQUE, "url": DOMAINE + "/contact/",
                           "inLanguage": "fr-FR"}])
enr("/contact/", "0.7")


# =============================================================== LÉGAL ======
def page_legale(chemin, h1, titre, desc, corps_html, nom_ariane):
    ar = [("Accueil", "/"), (nom_ariane, None)]
    corps = f"""
<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="section-head reveal" style="max-width:76ch">
      <p class="eyebrow">Informations légales</p>
      <h1>{h1}</h1>
      <p class="tiny">Dernière mise à jour : {AUJ}</p>
    </div>
    <div class="prose reveal">{corps_html}</div>
  </div>
</section>
"""
    page(chemin, titre, desc, corps, ar, schemas=[SCHEMA_ORG], robots="noindex, follow")
    enr(chemin, "0.3", "yearly")


page_legale(
    "/mentions-legales/", "Mentions légales",
    "Mentions légales | IPTV Abonnement France",
    "Mentions légales du site iptvabonnementfrance.store : éditeur, hébergeur, propriété intellectuelle et responsabilité.",
    """
<div class="encart"><p><strong>À compléter avant mise en ligne.</strong> Les champs signalés
ci-dessous doivent être renseignés avec vos informations réelles : la loi française impose
l'identification de l'éditeur d'un site accessible au public.</p></div>

<h2>Éditeur du site</h2>
<p>Site : iptvabonnementfrance.store<br>
Éditeur : <em>[À COMPLÉTER — nom ou raison sociale]</em><br>
Forme juridique et capital social : <em>[À COMPLÉTER]</em><br>
Adresse : <em>[À COMPLÉTER]</em><br>
Numéro d'identification (SIRET / RCS) : <em>[À COMPLÉTER]</em><br>
Numéro de TVA intracommunautaire : <em>[À COMPLÉTER le cas échéant]</em><br>
Directeur de la publication : <em>[À COMPLÉTER]</em><br>
Contact : voir la <a href="/contact/">page de contact</a>.</p>

<h2>Hébergeur</h2>
<p>Nom de l'hébergeur : <em>[À COMPLÉTER]</em><br>
Adresse : <em>[À COMPLÉTER]</em><br>
Téléphone : <em>[À COMPLÉTER]</em></p>

<h2>Propriété intellectuelle</h2>
<p>La structure du site, les textes, les éléments graphiques et le code qui le composent sont
protégés par le droit de la propriété intellectuelle. Toute reproduction ou représentation, totale ou
partielle, sans autorisation écrite préalable est interdite.</p>
<p>Les marques, logos et noms de produits mentionnés sur ce site (notamment les marques de fabricants
d'appareils et de lecteurs multimédias) appartiennent à leurs titulaires respectifs. Leur mention est
faite à titre purement informatif, dans un but de compatibilité technique, et n'implique aucun
partenariat, affiliation ou approbation de leur part.</p>

<h2>Nature du service et responsabilité</h2>
<p>Le service proposé consiste en la fourniture d'un accès technique à un service de diffusion et
des informations de configuration associées. L'éditeur n'héberge, ne produit, n'édite et ne contrôle
aucun contenu audiovisuel.</p>
<p>Il appartient à chaque utilisateur de s'assurer qu'il dispose des droits nécessaires pour accéder
aux contenus qu'il consulte et de n'utiliser le service qu'avec des contenus autorisés, dans le
respect du Code de la propriété intellectuelle et de la réglementation française et européenne en
vigueur. Toute utilisation contraire à ces règles relève de la seule responsabilité de l'utilisateur.</p>

<h2>Liens externes</h2>
<p>Ce site peut renvoyer vers des sites tiers (boutiques d'applications, éditeurs de lecteurs).
L'éditeur n'exerce aucun contrôle sur leur contenu et décline toute responsabilité à leur égard.</p>

<h2>Droit applicable</h2>
<p>Le présent site est soumis au droit français. Tout litige relatif à son utilisation relève de la
compétence des juridictions françaises.</p>
""", "Mentions légales")


page_legale(
    "/politique-confidentialite/", "Politique de confidentialité",
    "Politique de confidentialité (RGPD) | IPTV Abonnement France",
    "Politique de confidentialité du site : données collectées, finalités, durée de conservation et vos droits au titre du RGPD.",
    """
<div class="encart"><p><strong>À adapter avant mise en ligne</strong> en fonction des outils
réellement utilisés (formulaire, mesure d'audience, paiement) et de l'identité du responsable de
traitement.</p></div>

<h2>Responsable du traitement</h2>
<p>Le responsable du traitement est <em>[À COMPLÉTER — éditeur du site]</em>. Pour toute question
relative à vos données, utilisez la <a href="/contact/">page de contact</a>.</p>

<h2>Données collectées</h2>
<p>Nous collectons uniquement les données que vous nous transmettez volontairement :</p>
<ul>
  <li><strong>Via le formulaire de contact</strong> : nom, adresse e-mail, sujet et contenu du message.</li>
  <li><strong>Lors d'une commande</strong> : les informations nécessaires au traitement de votre
  demande et à la mise en service de votre abonnement.</li>
  <li><strong>Données techniques</strong> : le cas échéant, données de connexion générées automatiquement
  par l'hébergeur (adresse IP, horodatage) à des fins de sécurité.</li>
</ul>

<h2>Finalités et bases légales</h2>
<ul>
  <li>Répondre à vos demandes — base légale : votre consentement.</li>
  <li>Exécuter la prestation commandée — base légale : l'exécution du contrat.</li>
  <li>Assurer la sécurité du site — base légale : l'intérêt légitime du responsable de traitement.</li>
</ul>

<h2>Durée de conservation</h2>
<p>Les messages reçus via le formulaire sont conservés le temps nécessaire au traitement de la
demande, puis archivés ou supprimés. Les données liées à une commande sont conservées conformément
aux obligations légales de conservation applicables.</p>

<h2>Destinataires</h2>
<p>Vos données ne sont ni vendues ni louées. Elles peuvent être traitées par nos prestataires
techniques (hébergement, messagerie) agissant sur instruction et pour la seule exécution du service.</p>

<h2>Cookies</h2>
<p>Ce site fonctionne sans cookie publicitaire ni cookie de suivi tiers. Si un outil de mesure
d'audience est ajouté ultérieurement, un bandeau de consentement conforme sera mis en place et cette
section mise à jour.</p>

<h2>Vos droits</h2>
<p>Conformément au Règlement général sur la protection des données (RGPD) et à la loi Informatique
et Libertés, vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation,
d'opposition et de portabilité de vos données. Vous pouvez exercer ces droits via la
<a href="/contact/">page de contact</a>.</p>
<p>Vous pouvez également introduire une réclamation auprès de la Commission nationale de
l'informatique et des libertés (CNIL), 3 place de Fontenoy, TSA 80715, 75334 Paris Cedex 07.</p>

<h2>Sécurité</h2>
<p>Nous mettons en œuvre des mesures techniques et organisationnelles raisonnables pour protéger vos
données contre la perte, l'usage abusif et l'accès non autorisé.</p>
""", "Politique de confidentialité")


page_legale(
    "/conditions-generales/", "Conditions générales de vente et d'utilisation",
    "Conditions générales | IPTV Abonnement France",
    "Conditions générales de vente et d'utilisation du service : objet, commande, obligations de l'utilisateur, responsabilité et droit applicable.",
    """
<div class="encart"><p><strong>Document type à faire valider</strong> par un professionnel du droit
avant mise en ligne, et à compléter avec l'identité de l'éditeur et vos conditions commerciales réelles.</p></div>

<h2>1. Objet</h2>
<p>Les présentes conditions régissent la fourniture, par l'éditeur du site, d'un accès technique à un
service de diffusion par Internet ainsi que des informations de configuration associées, et
l'utilisation du site iptvabonnementfrance.store.</p>

<h2>2. Nature du service</h2>
<p>L'éditeur n'héberge, ne produit, n'édite et ne contrôle aucun contenu audiovisuel. Le service
fourni est de nature technique. Les applications de lecture mentionnées sur le site sont éditées par
des tiers indépendants et ne fournissent elles-mêmes aucun contenu.</p>

<h2>3. Commande et mise en service</h2>
<p>Toute commande suppose l'acceptation préalable des présentes conditions. Les informations
nécessaires à la configuration sont transmises après validation de la commande. Ces informations sont
strictement personnelles et ne doivent pas être partagées, revendues ou publiées.</p>

<h2>4. Tarifs</h2>
<p>Les tarifs applicables sont ceux communiqués au moment de la commande. Les offres et tarifs
peuvent être modifiés à tout moment, sans effet rétroactif sur les abonnements déjà souscrits.</p>

<h2>5. Obligations de l'utilisateur</h2>
<p>L'utilisateur s'engage à :</p>
<ul>
  <li>utiliser le service exclusivement avec des contenus qu'il est légalement autorisé à consulter ;</li>
  <li>ne pas partager, revendre ni rediffuser ses informations de connexion ou les flux reçus ;</li>
  <li>respecter le Code de la propriété intellectuelle et l'ensemble de la réglementation applicable ;</li>
  <li>disposer d'un équipement et d'une connexion Internet adaptés.</li>
</ul>
<p>Le non-respect de ces obligations peut entraîner la suspension immédiate de l'accès, sans remboursement.</p>

<h2>6. Disponibilité</h2>
<p>Le service est fourni dans le cadre d'une obligation de moyens. Des interruptions peuvent survenir
du fait de la maintenance, d'incidents techniques, du réseau de l'utilisateur ou d'un cas de force
majeure. L'éditeur ne saurait garantir une disponibilité ininterrompue.</p>

<h2>7. Responsabilité</h2>
<p>L'éditeur ne peut être tenu responsable des dommages résultant d'une utilisation du service
contraire aux présentes conditions ou à la réglementation applicable, d'une défaillance de la
connexion Internet de l'utilisateur, ou d'une incompatibilité de son matériel non signalée avant la
commande.</p>

<h2>8. Droit de rétractation</h2>
<p>Les modalités applicables sont détaillées dans notre
<a href="/politique-remboursement/">politique de remboursement</a>.</p>

<h2>9. Données personnelles</h2>
<p>Le traitement des données est décrit dans la
<a href="/politique-confidentialite/">politique de confidentialité</a>.</p>

<h2>10. Modification des conditions</h2>
<p>L'éditeur peut modifier les présentes conditions. La version applicable est celle en vigueur à la
date de la commande.</p>

<h2>11. Droit applicable et litiges</h2>
<p>Les présentes conditions sont soumises au droit français. En cas de litige, une solution amiable
sera recherchée en priorité. À défaut, les juridictions françaises sont compétentes. Conformément à
la réglementation, le consommateur peut recourir gratuitement à un médiateur de la consommation
<em>[À COMPLÉTER — coordonnées du médiateur retenu]</em>.</p>
""", "Conditions générales")


page_legale(
    "/politique-remboursement/", "Politique de remboursement",
    "Politique de remboursement | IPTV Abonnement France",
    "Politique de remboursement et droit de rétractation applicables aux abonnements souscrits sur iptvabonnementfrance.store.",
    """
<div class="encart"><p><strong>À adapter</strong> à votre pratique commerciale réelle avant mise en
ligne. Ne publiez pas une garantie que vous n'appliquez pas : une politique non respectée est une
source de litige et de réclamation.</p></div>

<h2>Principe général</h2>
<p>Nous cherchons d'abord à résoudre les difficultés techniques. Avant toute demande de remboursement,
contactez notre support : une grande partie des problèmes rencontrés relèvent d'un réglage du lecteur,
d'une saisie d'identifiants ou de la connexion locale, et se règlent en quelques échanges.</p>

<h2>Droit de rétractation et contenu numérique</h2>
<p>Conformément aux articles L221-18 et suivants du Code de la consommation, le consommateur dispose
en principe d'un délai de quatorze jours pour exercer son droit de rétractation.</p>
<p>Toutefois, l'article L221-28 prévoit que ce droit ne peut être exercé pour la fourniture d'un
contenu numérique non fourni sur support matériel dont l'exécution a commencé après accord préalable
exprès du consommateur et renoncement exprès à son droit de rétractation. Lors de la commande, il vous
est donc demandé de confirmer expressément votre demande d'exécution immédiate.</p>

<h2>Cas donnant lieu à examen d'un remboursement</h2>
<ul>
  <li>Le service n'a jamais été activé du fait de l'éditeur.</li>
  <li>Une incompatibilité technique confirmée, signalée avant la commande et non résolue.</li>
  <li>Une erreur de facturation ou un double paiement.</li>
</ul>

<h2>Cas n'ouvrant pas droit à remboursement</h2>
<ul>
  <li>Partage, revente ou rediffusion des informations de connexion.</li>
  <li>Utilisation du service en contradiction avec les conditions générales ou la réglementation applicable.</li>
  <li>Difficultés liées à la connexion Internet ou au matériel de l'utilisateur, après diagnostic.</li>
  <li>Changement d'avis après une période d'utilisation significative du service.</li>
</ul>

<h2>Comment formuler une demande</h2>
<p>Adressez votre demande via la <a href="/contact/">page de contact</a> en précisant la référence de
votre commande, la date, l'appareil utilisé et la description du problème ainsi que les démarches déjà
effectuées avec le support. Nous accusons réception et vous indiquons la suite donnée.</p>

<h2>Délai de traitement</h2>
<p>Lorsqu'un remboursement est accordé, il est effectué par le même moyen de paiement que celui utilisé
lors de la commande, dans les délais prévus par la réglementation applicable.</p>
""", "Politique de remboursement")


# ============================================================= COMMANDE =====
ar = [("Accueil", "/"), ("Abonnement IPTV", "/abonnement-iptv/"), ("Commande", None)]
corps = """
<section class="section" style="padding-top:30px">
  <div class="wrap">
    <div class="section-head reveal" style="max-width:70ch">
      <p class="eyebrow">Commande</p>
      <h1>Finaliser votre abonnement</h1>
      <p class="lead">Vérifiez votre formule, indiquez vos coordonnées et choisissez votre moyen
        de paiement. Nous revenons vers vous pour finaliser, puis vos accès sont envoyés.</p>
    </div>
    <div data-commande></div>
  </div>
</section>
<section class="section section--line section--surface">
  <div class="wrap prose reveal">
    <h2>Ce qui se passe après votre commande</h2>
    <ol>
      <li><strong>Nous vérifions votre appareil.</strong> Si le modèle indiqué ne permet pas
      d'installer un lecteur IPTV, nous vous le disons avant tout paiement et nous vous proposons
      une alternative.</li>
      <li><strong>Nous vous envoyons le moyen de paiement choisi.</strong> Aucune donnée bancaire
      n'est saisie sur ce site : vous recevez un lien ou des coordonnées par e-mail ou WhatsApp.</li>
      <li><strong>Vos accès arrivent par e-mail</strong> dès confirmation du paiement, accompagnés
      du guide d'installation correspondant à votre appareil.</li>
      <li><strong>Nous restons disponibles</strong> pendant l'installation et ensuite, si vous
      changez d'appareil ou rencontrez un souci.</li>
    </ol>
    <div class="encart"><p>Une question avant de commander ? Écrivez-nous sur WhatsApp au
    <a data-numero href="#">—</a> ou via la <a href="/contact/">page de contact</a>.</p></div>
  </div>
</section>
"""
page("/commande/",
     "Commander votre abonnement IPTV | IPTV Abonnement France",
     "Finalisez votre commande d'abonnement IPTV : formule, connexions simultanées, "
     "coordonnées et moyen de paiement. Accès envoyés après confirmation.",
     corps, ar, actif="/abonnement-iptv/",
     schemas=[SCHEMA_ORG], robots="noindex, follow")


# ============================================================ SITEMAP =======
lignes = "\n".join(
    "  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>"
    % (DOMAINE, u, AUJ, f, p) for u, p, f in URLS
)
ecrire_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">
</urlset>"""
with open(os.path.join(RACINE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + lignes + "\n</urlset>\n")

# ============================================================= ROBOTS =======
with open(os.path.join(RACINE, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("""User-agent: *
Allow: /

# Pages légales : accessibles mais non indexées (voir meta robots)
Disallow: /assets/js/config.js
Disallow: /commande/

Sitemap: %s/sitemap.xml
""" % DOMAINE)

print("Pages générées :", len(URLS))
