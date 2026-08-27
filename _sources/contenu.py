# -*- coding: utf-8 -*-
"""Blocs de contenu français réutilisables."""

# --------------------------------------------------------------- Visuel TV --
TV_VISUEL = """
<div class="tv reveal" aria-hidden="true">
  <div class="tv-cadre">
    <div class="tv-ecran">
      <div class="ecran-haut">
        <span class="pastille"></span><span>En direct</span><span>Grille des programmes</span>
      </div>
      <div class="ecran-vedette">
        <div class="vedette-txt">
          <small>À la une</small>
          <b>Votre sélection du soir</b>
        </div>
      </div>
      <div class="ecran-rail">
        <div class="tuile"></div><div class="tuile"></div><div class="tuile"></div>
        <div class="tuile"></div><div class="tuile"></div>
      </div>
      <div class="ecran-epg">
        <div class="epg-regle"><span>20:00</span><span>20:45</span><span>21:30</span><span>22:15</span></div>
        <div class="epg-barres"><i></i><i class="actif"></i><i></i><i></i><i class="actif"></i><i></i><i></i></div>
        <div class="epg-curseur"></div>
      </div>
    </div>
  </div>
  <div class="tv-socle"></div>
</div>
"""

# ---------------------------------------------------------- Barre confiance --
def bandeau_confiance():
    items = [
        ("check", "Installation simple",
         "Un guide clair, étape par étape, pour configurer votre appareil."),
        ("devices", "Multi-appareils",
         "Smart TV, box, mobile, tablette ou ordinateur compatibles."),
        ("flow", "Streaming fluide",
         "Une lecture pensée pour rester confortable au quotidien."),
        ("support", "Support client",
         "Une équipe francophone joignable en cas de question."),
    ]
    icones = {
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "devices": '<rect x="2" y="4" width="14" height="10" rx="2"/><rect x="17" y="9" width="5" height="11" rx="1.5"/>',
        "flow": '<path d="M13 2 4.5 13H11l-1 9 8.5-11H12l1-9z"/>',
        "support": '<path d="M21 15a2 2 0 0 1-2 2H8l-4 4V6a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/>',
    }
    cartes = "".join(
        '<div class="confiance-item">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
        '<div><b>%s</b><p>%s</p></div></div>' % (icones[i], t, d)
        for i, t, d in items
    )
    return ('<section class="bandeau-confiance"><div class="wrap">'
            '<div class="confiance-grille">%s</div></div></section>' % cartes)


# --------------------------------------------------------------- Tarifs -----
def section_tarifs(titre="Nos formules d'abonnement IPTV", intro=None, niveau="h2"):
    intro = intro or ("Quatre formules, la même mise en service immédiate. Ajustez le nombre "
                      "de connexions simultanées avec les boutons + et − : le tarif se met à "
                      "jour automatiquement.")
    return f"""
<section class="section section--line" id="abonnements">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Abonnements</p>
      <{niveau}>{titre}</{niveau}>
      <p class="lead" style="margin-inline:auto">{intro}</p>
    </div>
    <div class="grille-tarifs" data-tarifs></div>
    <p class="note-tarifs">Les offres et tarifs peuvent être modifiés à tout moment.</p>
  </div>
</section>
"""


# ------------------------------------------------------------ Appareils -----
def section_appareils(titre="Regardez votre contenu sur vos appareils préférés", niveau="h2"):
    return f"""
<section class="section section--line" id="appareils">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Compatibilité</p>
      <{niveau}>{titre}</{niveau}>
      <p class="lead" style="margin-inline:auto">Une expérience adaptée à votre écran.
        La liste ci-dessous reprend les appareils sur lesquels un lecteur IPTV compatible
        peut être installé.</p>
    </div>
    <div class="grille-appareils" data-appareils></div>
    <p class="note-tarifs">Avant de commander, vérifiez avec nous la compatibilité de votre
      modèle précis : les applications disponibles varient d'une marque et d'une année à l'autre.</p>
  </div>
</section>
"""


# ------------------------------------------------------- Fonctionnalités ----
FONCTIONNALITES = [
    ("📺", "Compatible avec vos appareils",
     "Votre abonnement s'utilise avec les lecteurs IPTV installés sur un téléviseur, une box ou un mobile."),
    ("⚡", "Streaming fluide",
     "Une configuration soignée et une connexion stable sont les deux clés d'une lecture confortable."),
    ("🎬", "Films et séries",
     "Un catalogue à la demande consultable directement depuis l'interface de votre lecteur."),
    ("📡", "Chaînes TV",
     "Des chaînes organisées par thématiques et accompagnées d'un guide des programmes."),
    ("📱", "Compatible mobile",
     "Regardez depuis un smartphone ou une tablette lorsque vous n'êtes pas devant la télévision."),
    ("💻", "Compatible ordinateur",
     "Un lecteur compatible sous Windows ou macOS permet d'utiliser le service sur PC et Mac."),
    ("🔧", "Installation simple",
     "Vous recevez les informations de configuration et un guide pour les saisir dans votre lecteur."),
    ("💬", "Assistance client",
     "Une question sur la mise en route ? Notre équipe répond en français."),
]


def section_fonctionnalites(titre="Pourquoi choisir notre abonnement IPTV France ?", niveau="h2"):
    cartes = "".join(
        '<article class="carte reveal"><div class="icone-carte">%s</div>'
        '<h3>%s</h3><p>%s</p></article>' % (i, t, d)
        for i, t, d in FONCTIONNALITES
    )
    return f"""
<section class="section section--line section--surface" id="fonctionnalites">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">Fonctionnalités</p>
      <{niveau}>{titre}</{niveau}>
      <p class="lead" style="margin-inline:auto">Ce que vous retrouvez concrètement une fois
        votre abonnement activé et votre lecteur configuré.</p>
    </div>
    <div class="grille-4">{cartes}</div>
  </div>
</section>
"""


# --------------------------------------------------------------- Étapes -----
ETAPES = [
    ("01", "Choisissez votre abonnement",
     "Comparez les offres et sélectionnez celle qui vous convient."),
    ("02", "Recevez vos informations",
     "Après votre commande, recevez les informations nécessaires à la configuration."),
    ("03", "Configurez votre appareil",
     "Suivez notre guide d'installation et commencez à utiliser votre service."),
]


def section_etapes(titre="Comment s'abonner à notre IPTV en France ?", niveau="h2"):
    et = "".join(
        '<div class="etape reveal"><div class="etape-num">%s</div><h3>%s</h3><p>%s</p></div>'
        % (n, t, d) for n, t, d in ETAPES
    )
    return f"""
<section class="section section--line">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Mise en route</p>
      <{niveau}>{titre}</{niveau}>
      <p class="lead">Trois étapes, et la même logique quel que soit l'appareil :
        on choisit une durée, on reçoit ses accès, on les saisit dans un lecteur compatible.</p>
    </div>
    <div class="etapes">{et}</div>
    <div class="btn-row"><a class="btn btn--primaire" href="/abonnement-iptv/">Choisir mon abonnement</a></div>
  </div>
</section>
"""


# ------------------------------------------------------------ Pourquoi nous --
POURQUOI = [
    ("Qualité", "Une expérience pensée pour un streaming confortable.",
     "La qualité perçue dépend autant de la source que de votre installation. "
     "Nous vous aidons à régler les paramètres de votre lecteur pour obtenir le meilleur "
     "rendu possible sur votre écran et votre connexion."),
    ("Simplicité", "Une installation claire et accessible.",
     "Pas de manipulation technique compliquée : un lecteur compatible, les informations "
     "que nous vous transmettons, et le service est prêt en quelques minutes."),
    ("Compatibilité", "Utilisez vos appareils compatibles préférés.",
     "Téléviseur connecté, boîtier Android, clé HDMI, mobile ou ordinateur : le même "
     "abonnement s'utilise sur les appareils sur lesquels un lecteur compatible peut être installé."),
    ("Support", "Une équipe disponible pour vous accompagner.",
     "Avant la commande pour vérifier votre matériel, pendant l'installation, et ensuite "
     "si vous changez d'appareil. En français."),
]


def section_pourquoi(titre="Pourquoi choisir notre IPTV en France ?", niveau="h2"):
    cartes = "".join(
        '<article class="carte reveal"><h3>%s</h3>'
        '<p style="color:var(--blanc);margin-bottom:10px;font-size:.97rem">%s</p>'
        '<p>%s</p></article>' % (t, a, d)
        for t, a, d in POURQUOI
    )
    return f"""
<section class="section section--line section--surface">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Nos engagements</p>
      <{niveau}>{titre}</{niveau}>
    </div>
    <div class="grille-2">{cartes}</div>
  </div>
</section>
"""


# ------------------------------------------------------------------ FAQ -----
FAQ_PRINCIPALE = [
    ("Qu'est-ce qu'un abonnement IPTV ?",
     "IPTV signifie « télévision sur protocole Internet ». Un abonnement IPTV donne accès à un "
     "flux de télévision et de contenus à la demande transmis via votre connexion Internet, au lieu "
     "d'une antenne, du satellite ou du câble. Concrètement, vous recevez des informations de connexion "
     "que vous saisissez dans une application de lecture compatible installée sur votre appareil."),

    ("Comment s'abonner à IPTV en France ?",
     "Le parcours tient en trois étapes : vous choisissez une durée d'abonnement, vous validez votre "
     "commande, puis vous recevez les informations de configuration à saisir dans votre lecteur. "
     "Notre guide d'installation détaille la marche à suivre selon l'appareil utilisé, et notre équipe "
     "peut vous accompagner si vous bloquez sur une étape."),

    ("Quel est le meilleur abonnement IPTV en France ?",
     "Il n'existe pas de réponse unique : le meilleur abonnement IPTV en France est celui qui fonctionne "
     "sur votre appareil, qui correspond à ce que vous regardez réellement et dont le service client "
     "répond quand vous en avez besoin. Regardez la compatibilité, la stabilité, la clarté de "
     "l'installation, la qualité de l'assistance et la transparence des conditions avant de comparer les prix."),

    ("Quel abonnement IPTV choisir ?",
     "Si vous découvrez l'IPTV, une courte durée permet de vérifier que le service fonctionne bien avec "
     "votre matériel et votre connexion. Si l'usage est déjà installé chez vous, une durée plus longue "
     "revient généralement moins cher au mois. Le choix dépend surtout du nombre d'écrans utilisés "
     "et de votre régularité d'usage."),

    ("Quel est l'IPTV le plus fiable ?",
     "La fiabilité se mesure à l'usage plutôt qu'aux promesses affichées : régularité du flux aux heures "
     "de forte affluence, rapidité de réponse du support, absence de coupures inexpliquées et clarté des "
     "conditions de service. Méfiez-vous des offres qui annoncent des chiffres spectaculaires sans "
     "aucune information sur l'entreprise ou sur les conditions d'utilisation."),

    ("Quels appareils sont compatibles ?",
     "L'IPTV s'utilise sur tout appareil capable d'installer un lecteur compatible : téléviseurs connectés, "
     "boîtiers Android TV, clés HDMI, ordinateurs Windows et macOS, smartphones et tablettes. Les "
     "applications disponibles varient selon la marque et l'année du modèle : n'hésitez pas à nous "
     "indiquer votre appareil avant de commander pour que nous vérifiions ensemble."),

    ("Comment installer un lecteur IPTV ?",
     "Vous installez d'abord une application de lecture compatible depuis la boutique d'applications de "
     "votre appareil. Vous ouvrez ensuite l'application et vous saisissez les informations de connexion "
     "que nous vous avons transmises. Le lecteur charge alors la liste des contenus auxquels votre "
     "abonnement vous donne accès."),

    ("Puis-je regarder l'IPTV sur Smart TV ?",
     "Oui, dès lors que votre téléviseur permet d'installer une application de lecture IPTV depuis sa "
     "boutique intégrée. Si ce n'est pas le cas — c'est fréquent sur les modèles plus anciens — un "
     "boîtier Android TV ou une clé HDMI branchée sur une prise HDMI libre permet d'obtenir le même résultat."),

    ("Puis-je utiliser IPTV sur smartphone ?",
     "Oui. Plusieurs lecteurs IPTV existent sur Android et iOS. Le fonctionnement est identique à celui "
     "d'un téléviseur : vous installez l'application, vous saisissez vos informations de connexion et vous "
     "accédez à votre service. En déplacement, privilégiez le Wi-Fi ou une connexion mobile stable."),

    ("Comment contacter le support ?",
     "Vous pouvez nous écrire à tout moment via le formulaire de la page Contact. Précisez votre appareil, "
     "le lecteur utilisé et la description du problème rencontré : cela nous permet de vous répondre "
     "directement avec la bonne procédure."),
]


def section_faq(paires, titre="Questions fréquentes sur l'abonnement IPTV", niveau="h2"):
    from tpl import faq_html
    return f"""
<section class="section section--line" id="faq">
  <div class="wrap">
    <div class="section-head center reveal">
      <p class="eyebrow">FAQ</p>
      <{niveau}>{titre}</{niveau}>
    </div>
    {faq_html(paires)}
  </div>
</section>
"""


# ------------------------------------------------------------- WhatsApp -----
SUJETS_WA = [
    ("Vérifier mon appareil",
     "Bonjour, je voudrais vérifier si mon appareil est compatible. Mon modèle est : "),
    ("Choisir une formule",
     "Bonjour, j'hésite entre plusieurs formules d'abonnement. Pouvez-vous me conseiller ?"),
    ("Aide à l'installation",
     "Bonjour, j'ai besoin d'aide pour installer mon lecteur IPTV. Mon appareil est : "),
    ("Suivi de ma commande",
     "Bonjour, je souhaite avoir des nouvelles de ma commande. Mon adresse e-mail est : "),
]

LOGO_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967'
           '-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.174.199-.347.223-.644.075-.297-.15-1.255-.463'
           '-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149'
           '-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5'
           '-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 '
           '1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.625.712.227 1.36.195 '
           '1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347'
           'm-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 '
           '0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.82 9.82 0 0 1 6.988 2.896 9.825 9.825 0 0 1 2.893 '
           '6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335'
           '.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c'
           '6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0 0 20.465 3.49"/></svg>')


def section_whatsapp(titre="Une question ? Écrivez-nous sur WhatsApp", niveau="h2"):
    puces = "".join(
        '<a class="wa-sujet" href="#" data-wa-sujet="%s">%s</a>' % (msg, lib)
        for lib, msg in SUJETS_WA
    )
    return f"""
<section class="section section--line" data-section-whatsapp>
  <div class="wrap">
    <div class="wa-panneau reveal">
      <div class="wa-panneau-texte">
        <span class="wa-marque">{LOGO_WA}<span>WhatsApp</span></span>
        <{niveau}>{titre}</{niveau}>
        <p>Le moyen le plus rapide de nous joindre. Compatibilité de votre téléviseur, choix
          d'une formule, aide à l'installation ou suivi d'une commande : on répond directement,
          en français.</p>
        <a class="wa-numero" data-numero href="#">—</a>
        <div class="btn-row" style="margin-top:22px">
          <a class="btn btn--vert" data-whatsapp href="#">{LOGO_WA}Ouvrir la conversation</a>
          <a class="btn btn--fantome" href="/contact/">Écrire par e-mail</a>
        </div>
      </div>
      <div class="wa-panneau-sujets">
        <p class="wa-sujets-titre">Message pré-rempli selon votre besoin</p>
        {puces}
      </div>
    </div>
  </div>
</section>
"""
