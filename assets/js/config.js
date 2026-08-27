/* ==========================================================================
   CONFIGURATION DU SITE — iptvabonnementfrance.store
   --------------------------------------------------------------------------
   C'EST LE SEUL FICHIER À MODIFIER pour changer les tarifs, les appareils,
   les coordonnées et les chiffres affichés sur le site.
   ========================================================================== */

window.CONFIG = {

  devise: "€",

  /* ---------------------------------------------------------------------
     1. REMISE PROGRESSIVE SUR LES CONNEXIONS
     ---------------------------------------------------------------------
     La 1re connexion est au tarif normal. Chaque connexion supplémentaire
     est facturée avec cette remise. 0.15 = 15 % moins cher.
     --------------------------------------------------------------------- */
  remise_connexion: 0.15,
  max_connexions: 5,

  /* ---------------------------------------------------------------------
     2. TARIFS
     ---------------------------------------------------------------------
     prix       : montant de la 1re connexion (ex. 39.99).
                  null = affiche « Tarif sur demande ».
     duree      : durée facturée.
     bonus      : mois offerts en plus ("" pour aucun).
     badge      : texte du ruban ("" pour aucun).
     badge_type : "bleu" ou "vert".
     --------------------------------------------------------------------- */
  offres: [
    {
      id: "bronze",
      nom: "Bronze",
      duree: "12 mois",
      bonus: "",
      prix: 39.99,
      badge: "",
      badge_type: "bleu",
      avantages: [
        "25 000+ chaînes TV",
        "100 000+ films et séries",
        "Qualité 4K / FHD / HD",
        "Chaînes françaises et internationales",
        "Compatible avec tous vos appareils",
        "Guide des programmes (EPG)",
        "Contenus à la demande (VOD)",
        "Serveurs stables et surveillés",
        "Support technique 24/7",
        "Livraison immédiate"
      ]
    },
    {
      id: "gold",
      nom: "Gold",
      duree: "15 mois",
      bonus: "+3 mois offerts",
      prix: 49.99,
      badge: "Le plus populaire",
      badge_type: "bleu",
      avantages: [
        "25 000+ chaînes TV",
        "100 000+ films et séries",
        "Qualité 4K / FHD / HD",
        "Chaînes françaises et internationales",
        "Compatible avec tous vos appareils",
        "Guide des programmes (EPG)",
        "Contenus à la demande (VOD)",
        "Serveurs stables et surveillés",
        "Support technique 24/7",
        "Livraison immédiate"
      ]
    },
    {
      id: "platinum",
      nom: "Platinum",
      duree: "15 mois",
      bonus: "+3 mois offerts",
      prix: 59.99,
      badge: "",
      badge_type: "bleu",
      avantages: [
        "25 000+ chaînes TV",
        "100 000+ films et séries",
        "Qualité 4K / FHD / HD",
        "Chaînes françaises et internationales",
        "Compatible avec tous vos appareils",
        "Guide des programmes (EPG)",
        "Contenus à la demande (VOD)",
        "Serveurs stables et surveillés",
        "Support technique 24/7",
        "Livraison immédiate"
      ]
    },
    {
      id: "exclusif",
      nom: "Exclusif",
      duree: "24 mois",
      bonus: "+3 mois offerts",
      prix: 84.99,
      badge: "Meilleur rapport",
      badge_type: "vert",
      avantages: [
        "130 000+ chaînes TV",
        "140 000+ films et séries",
        "Qualité 4K / FHD / HD",
        "Toutes les chaînes internationales",
        "Compatible avec tous vos appareils",
        "Guide des programmes (EPG)",
        "Contenus à la demande (VOD)",
        "Serveurs stables et surveillés",
        "Support technique 24/7",
        "Livraison immédiate"
      ]
    }
  ],

  /* ---------------------------------------------------------------------
     3. APPAREILS ET PLATEFORMES
     ---------------------------------------------------------------------
     logo : nom du fichier dans /assets/img/marques/ (sans .svg)
     Retirez une ligne pour faire disparaître la marque du site.
     --------------------------------------------------------------------- */
  appareils: [
    { nom: "Samsung TV",  detail: "Tizen",             logo: "samsung" },
    { nom: "LG TV",       detail: "webOS",             logo: "lg" },
    { nom: "Sony TV",     detail: "Google TV",         logo: "sony" },
    { nom: "Android TV",  detail: "Box et TV", logo: "android" },
    { nom: "Apple TV",    detail: "tvOS",              logo: "appletv" },
    { nom: "Amazon",      detail: "Fire TV Stick",     logo: "amazon" },
    { nom: "Chromecast",  detail: "Google TV",         logo: "chromecast" },
    { nom: "Roku",        detail: "Roku OS",           logo: "roku" },
    { nom: "Xbox",        detail: "Console",           logo: "xbox" },
    { nom: "Windows",     detail: "PC et portable",    logo: "windows" },
    { nom: "Apple",       detail: "iPhone, iPad, Mac", logo: "apple" },
    { nom: "Linux",       detail: "Ubuntu, Debian",    logo: "linux" }
  ],

  /* ---------------------------------------------------------------------
     4. CHIFFRES CLÉS (compteurs animés)
     ---------------------------------------------------------------------
     Laissez null pour masquer entièrement la section.
     --------------------------------------------------------------------- */
  chiffres: [
    { valeur: 25000,  suffixe: "+",  libelle: "Chaînes TV" },
    { valeur: 100000, suffixe: "+",  libelle: "Films et séries" },
    { valeur: 12,     suffixe: "",   libelle: "Plateformes compatibles" },
    { valeur: 24,     suffixe: "/7", libelle: "Support technique" }
  ],

  /* ---------------------------------------------------------------------
     5. CONTACT
     ---------------------------------------------------------------------
     whatsapp         : format international SANS "+" ni espaces.
     whatsapp_affiche : version lisible affichée sur le site.
     endpoint         : URL du backend Google Apps Script pour le
                        formulaire. "" = envoi par mailto:.
     --------------------------------------------------------------------- */
  /* ---------------------------------------------------------------------
     MOYENS DE PAIEMENT proposés sur la page de commande.
     Aucun champ de carte bancaire n'est demandé sur le site : le client
     choisit un moyen, vous lui envoyez ensuite le lien ou les coordonnées.
     --------------------------------------------------------------------- */
  moyens_paiement: [
    "Lien de paiement par carte",
    "PayPal",
    "Virement bancaire",
    "À convenir sur WhatsApp"
  ],

  /* ---------------------------------------------------------------------
     CODES PROMO. Clé = code en majuscules, valeur = remise (0.10 = 10 %).
     Laissez l'objet vide {} pour désactiver le champ sur la commande.
     Exemple : codes_promo: { "BIENVENUE10": 0.10, "NOEL": 0.15 }
     --------------------------------------------------------------------- */
  codes_promo: {},

  whatsapp: "16615413954",
  whatsapp_affiche: "+1 (661) 541-3954",
  email: "contact@iptvabonnementfrance.store",
  endpoint: "https://script.google.com/macros/s/AKfycbzqtXNape9QR4xSbp6TGLPixkZjEhIY93Z-aMxbRiLpNDsajbAoPEFglfCQgBbvZwKZ/exec",

  /* ---------------------------------------------------------------------
     6. ENTREPRISE (mentions légales et données structurées)
     --------------------------------------------------------------------- */
  entreprise: {
    nom: "IPTV Abonnement France",
    site: "https://iptvabonnementfrance.store",
    editeur: "À COMPLÉTER — nom du responsable de publication",
    adresse: "À COMPLÉTER — adresse postale",
    siret: "À COMPLÉTER — numéro d'identification",
    hebergeur: "À COMPLÉTER — nom et adresse de l'hébergeur"
  }
};
