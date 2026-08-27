/**
 * ============================================================================
 *  iptvabonnementfrance.store — backend Google Apps Script
 * ============================================================================
 *  Reçoit les commandes (/commande/) et les messages (/contact/),
 *  les enregistre dans Google Sheets et vous envoie une alerte e-mail.
 *
 *  INSTALLATION (5 minutes) :
 *   1. https://script.google.com  →  Nouveau projet
 *   2. Collez ce fichier entier à la place du contenu par défaut
 *   3. Ajustez EMAIL_ALERTE ci-dessous
 *   4. Exécuter → choisir « initialiser » → Exécuter → autoriser l'accès
 *   5. Déployer → Nouveau déploiement → type « Application web »
 *        Exécuter en tant que  : Moi
 *        Qui a accès           : Tout le monde        ← indispensable
 *   6. Copiez l'URL /exec obtenue et collez-la dans assets/js/config.js :
 *        endpoint: "https://script.google.com/macros/s/AKfy.../exec",
 *
 *  IMPORTANT — à chaque modification de ce script, il faut refaire
 *  « Déployer → Gérer les déploiements → crayon → Version : Nouvelle version ».
 *  Sans ça, l'ancienne version continue de tourner.
 * ============================================================================
 */

/* --------------------------------------------------------------- Réglages */

var SHEET_ID     = '1kc2jW078-lW-fp_WOPRX1XyzHIPjP1YjoVU-157Bsi4';
var EMAIL_ALERTE = 'xyz905391@gmail.com';    // ← destinataire des alertes
var SITE         = 'iptvabonnementfrance.store';
var FUSEAU       = 'Europe/Paris';
var PREFIXE_REF  = 'IAF';                    // préfixe des références de commande

var ONGLET_COMMANDES = 'Commandes';
var ONGLET_CONTACTS  = 'Contacts';

var COLONNES_COMMANDES = [
  'Date', 'Référence', 'Statut', 'Offre', 'Durée', 'Bonus', 'Connexions',
  'Total', 'Code promo', 'Nom', 'E-mail', 'Téléphone', 'Pays', 'Appareil',
  'Paiement', 'Précisions', 'Page', 'Navigateur'
];

var COLONNES_CONTACTS = [
  'Date', 'Statut', 'Nom', 'E-mail', 'Sujet', 'Message', 'Page', 'Navigateur'
];

/* ------------------------------------------------------------ Point d'entrée */

function doPost(e) {
  // Un verrou évite que deux commandes simultanées écrivent sur la même ligne.
  var verrou = LockService.getScriptLock();
  try {
    verrou.waitLock(20000);
  } catch (err) {
    return reponse_(false, 'Serveur occupé, réessayez.');
  }

  try {
    var data = lireCorps_(e);
    if (!data) return reponse_(false, 'Requête vide ou illisible.');

    // Le formulaire de commande envoie un champ "offre" : c'est ce qui
    // distingue une commande d'un simple message de contact.
    var estCommande = !!(data.offre || data.connexions);

    if (estCommande) {
      var ref = enregistrerCommande_(data, e);
      alerteCommande_(data, ref);
      return reponse_(true, 'Commande enregistrée', { reference: ref });
    } else {
      enregistrerContact_(data, e);
      alerteContact_(data);
      return reponse_(true, 'Message enregistré');
    }
  } catch (err) {
    // On journalise et on prévient : une commande perdue coûte plus cher
    // qu'un e-mail d'erreur.
    console.error(err);
    alerteErreur_(err, e);
    return reponse_(false, String(err));
  } finally {
    verrou.releaseLock();
  }
}

function doGet() {
  return ContentService
    .createTextOutput('OK — backend ' + SITE + ' actif (' + horodatage_() + ')')
    .setMimeType(ContentService.MimeType.TEXT);
}

/* ------------------------------------------------------------- Lecture JSON */

function lireCorps_(e) {
  if (!e || !e.postData || !e.postData.contents) {
    // Repli : certaines requêtes arrivent en paramètres de formulaire.
    if (e && e.parameter && Object.keys(e.parameter).length) return e.parameter;
    return null;
  }
  try {
    return JSON.parse(e.postData.contents);
  } catch (err) {
    return e.parameter && Object.keys(e.parameter).length ? e.parameter : null;
  }
}

/* ------------------------------------------------------------- Écriture ---- */

function enregistrerCommande_(d, e) {
  var feuille = ongletCommandes_();
  var ref = reference_(feuille);

  ecrireParEntetes_(feuille, {
    date:       horodatage_(),
    reference:  ref,
    statut:     'Nouvelle',
    offre:      txt_(d.offre),
    duree:      txt_(d.duree),
    bonus:      txt_(d.bonus),
    connexions: txt_(d.connexions),
    total:      txt_(d.total),
    promo:      txt_(d.code_promo),
    nom:        txt_(d.nom),
    email:      txt_(d.email),
    telephone:  txt_(d.telephone),
    pays:       txt_(d.pays),
    appareil:   txt_(d.appareil),
    paiement:   txt_(d.paiement),
    notes:      txt_(d.notes),
    page:       txt_(d.page),
    navigateur: navigateur_(e)
  });

  return ref;
}

function enregistrerContact_(d, e) {
  var feuille = ongletContacts_();
  feuille.appendRow([
    horodatage_(),
    'Non traité',
    txt_(d.nom),
    txt_(d.email),
    txt_(d.sujet),
    txt_(d.message),
    txt_(d.page),
    navigateur_(e)
  ]);
  finaliser_(feuille, COLONNES_CONTACTS.length);
}

/**
 * Récupère l'onglet des commandes.
 * Priorité : (1) un onglet nommé ONGLET_COMMANDES, (2) le premier onglet du
 * classeur s'il a déjà une ligne d'en-têtes que vous avez saisie à la main,
 * (3) sinon on le crée. Objectif : écrire dans VOTRE feuille, pas à côté.
 */
function ongletCommandes_() {
  var classeur = SpreadsheetApp.openById(SHEET_ID);
  var feuille = classeur.getSheetByName(ONGLET_COMMANDES);
  if (feuille) return feuille;

  var premier = classeur.getSheets()[0];
  if (premier && premier.getLastRow() >= 1 && premier.getLastColumn() >= 2) {
    // Le premier onglet a déjà des en-têtes : on s'en sert.
    return premier;
  }
  return creerOnglet_(classeur, ONGLET_COMMANDES, COLONNES_COMMANDES);
}

function ongletContacts_() {
  var classeur = SpreadsheetApp.openById(SHEET_ID);
  return classeur.getSheetByName(ONGLET_CONTACTS) ||
         creerOnglet_(classeur, ONGLET_CONTACTS, COLONNES_CONTACTS);
}

function creerOnglet_(classeur, nom, colonnes) {
  var feuille = classeur.insertSheet(nom);
  feuille.appendRow(colonnes);
  feuille.getRange(1, 1, 1, colonnes.length)
         .setFontWeight('bold')
         .setBackground('#1E4FD8')
         .setFontColor('#FFFFFF')
         .setVerticalAlignment('middle');
  feuille.setRowHeight(1, 34);
  feuille.setFrozenRows(1);
  return feuille;
}

/**
 * Écrit une ligne en faisant correspondre les valeurs aux EN-TÊTES EXISTANTS.
 * Vous pouvez donc renommer, réordonner ou supprimer des colonnes dans la
 * feuille : le script suit, au lieu de décaler tout d'une case.
 * Les valeurs sans en-tête correspondant sont simplement ignorées.
 */
function ecrireParEntetes_(feuille, valeurs) {
  var nbCol = Math.max(feuille.getLastColumn(), 1);
  var entetes = feuille.getRange(1, 1, 1, nbCol).getValues()[0];

  var ligne = new Array(nbCol).fill('');
  var placee = false;

  for (var c = 0; c < nbCol; c++) {
    var cle = normaliser_(entetes[c]);
    if (!cle) continue;
    for (var nom in valeurs) {
      if (ALIAS_[nom] && ALIAS_[nom].indexOf(cle) !== -1) {
        ligne[c] = valeurs[nom];
        placee = true;
        break;
      }
    }
  }

  // Aucune correspondance : la feuille n'a pas d'en-têtes exploitables,
  // on écrit dans l'ordre par défaut plutôt que de perdre la commande.
  if (!placee) {
    feuille.appendRow(COLONNES_COMMANDES.map(function (c) {
      var cle = normaliser_(c);
      for (var nom in valeurs) {
        if (ALIAS_[nom] && ALIAS_[nom].indexOf(cle) !== -1) return valeurs[nom];
      }
      return '';
    }));
    return;
  }
  feuille.appendRow(ligne);
}

/** Noms d'en-têtes acceptés pour chaque donnée (accents et casse ignorés). */
var ALIAS_ = {
  date:       ['date', 'horodatage', 'timestamp', 'recule', 'datedecommande'],
  reference:  ['reference', 'ref', 'nocommande', 'numerodecommande'],
  statut:     ['statut', 'status', 'etat'],
  offre:      ['formule', 'offre', 'abonnement', 'plan', 'pack'],
  duree:      ['duree', 'periode'],
  bonus:      ['bonus', 'moisofferts', 'offert'],
  connexions: ['connexions', 'connexion', 'nbconnexions', 'ecrans'],
  total:      ['prix', 'prixe', 'total', 'montant', 'totalareger', 'totalaregler'],
  promo:      ['codepromo', 'promo', 'coupon'],
  nom:        ['nom', 'nomcomplet', 'client', 'nomprenom'],
  email:      ['email', 'mail', 'adresseemail', 'courriel'],
  telephone:  ['telephone', 'tel', 'mobile', 'whatsapp', 'numero'],
  pays:       ['pays', 'country', 'indicatif'],
  appareil:   ['appareil', 'device', 'materiel'],
  paiement:   ['paiement', 'modedepaiement', 'moyendepaiement', 'payment'],
  notes:      ['precisions', 'notes', 'remarques', 'commentaire', 'message'],
  page:       ['page', 'url', 'source'],
  navigateur: ['navigateur', 'useragent', 'ua']
};

function normaliser_(v) {
  return String(v == null ? '' : v)
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]/g, '');
}

/**
 * Référence lisible : IAF-20260827-0004
 */
function reference_(feuille) {
  var jour = Utilities.formatDate(new Date(), FUSEAU, 'yyyyMMdd');
  var numero = Math.max(feuille.getLastRow(), 1); // ligne 1 = en-têtes
  return PREFIXE_REF + '-' + jour + '-' + ('0000' + numero).slice(-4);
}

/**
 * Ajuste les colonnes et met la dernière ligne en évidence.
 */
function finaliser_(feuille, nbColonnes) {
  try {
    var derniere = feuille.getLastRow();
    feuille.getRange(derniere, 1, 1, nbColonnes)
           .setVerticalAlignment('top')
           .setWrap(false);
    if (derniere <= 3) feuille.autoResizeColumns(1, nbColonnes);
  } catch (err) {
    // Purement cosmétique : ne doit jamais faire échouer l'enregistrement.
    console.warn(err);
  }
}

/* ------------------------------------------------------------- Alertes ----- */

function alerteCommande_(d, ref) {
  if (!EMAIL_ALERTE) return;

  var sujet = '🛒 Commande ' + ref + ' — ' + txt_(d.offre) + ' — ' + txt_(d.total);

  var lignes = [
    ['Référence',   ref],
    ['Offre',       txt_(d.offre) + ' (' + txt_(d.duree) +
                    (d.bonus ? ' ' + d.bonus : '') + ')'],
    ['Connexions',  txt_(d.connexions)],
    ['Code promo',  txt_(d.code_promo) || '—'],
    ['Total',       txt_(d.total)],
    ['Nom',         txt_(d.nom)],
    ['E-mail',      txt_(d.email)],
    ['Téléphone',   txt_(d.telephone) || '—'],
    ['Pays',        txt_(d.pays) || '—'],
    ['Appareil',    txt_(d.appareil) || '—'],
    ['Paiement',    txt_(d.paiement)],
    ['Précisions',  txt_(d.notes) || '—'],
    ['Reçue le',    horodatage_()]
  ];

  MailApp.sendEmail({
    to: EMAIL_ALERTE,
    subject: sujet,
    replyTo: estEmail_(d.email) ? d.email : undefined,
    htmlBody: gabarit_('Nouvelle commande', lignes,
      'Répondez directement à cet e-mail pour joindre le client.')
  });
}

function alerteContact_(d) {
  if (!EMAIL_ALERTE) return;

  var lignes = [
    ['Nom',      txt_(d.nom)],
    ['E-mail',   txt_(d.email)],
    ['Sujet',    txt_(d.sujet) || '—'],
    ['Message',  txt_(d.message)],
    ['Page',     txt_(d.page)],
    ['Reçu le',  horodatage_()]
  ];

  MailApp.sendEmail({
    to: EMAIL_ALERTE,
    subject: '✉️ Message de ' + (txt_(d.nom) || 'un visiteur') + ' — ' + SITE,
    replyTo: estEmail_(d.email) ? d.email : undefined,
    htmlBody: gabarit_('Nouveau message', lignes,
      'Répondez directement à cet e-mail pour joindre l\'expéditeur.')
  });
}

function alerteErreur_(err, e) {
  if (!EMAIL_ALERTE) return;
  try {
    MailApp.sendEmail({
      to: EMAIL_ALERTE,
      subject: '⚠️ Erreur backend ' + SITE,
      body: 'Une soumission n\'a pas pu être enregistrée.\n\n' +
            'Erreur : ' + err + '\n\n' +
            'Données reçues :\n' +
            (e && e.postData ? e.postData.contents : '(aucune)') + '\n\n' +
            horodatage_()
    });
  } catch (ignore) {}
}

function gabarit_(titre, lignes, pied) {
  var html = '<div style="font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;' +
             'max-width:600px;color:#111">' +
             '<div style="background:#1E4FD8;color:#fff;padding:18px 22px;border-radius:10px 10px 0 0">' +
             '<div style="font-size:12px;letter-spacing:.12em;text-transform:uppercase;opacity:.8">' +
             SITE + '</div>' +
             '<div style="font-size:20px;font-weight:700;margin-top:4px">' + titre + '</div></div>' +
             '<table style="width:100%;border-collapse:collapse;border:1px solid #E3E6EC;' +
             'border-top:0;border-radius:0 0 10px 10px">';

  for (var i = 0; i < lignes.length; i++) {
    var fond = (i % 2 === 0) ? '#FFFFFF' : '#F7F8FA';
    html += '<tr style="background:' + fond + '">' +
            '<td style="padding:11px 16px;font-size:13px;color:#5C6274;width:34%;' +
            'border-bottom:1px solid #EDEFF3;vertical-align:top">' + lignes[i][0] + '</td>' +
            '<td style="padding:11px 16px;font-size:14px;font-weight:600;' +
            'border-bottom:1px solid #EDEFF3;vertical-align:top">' +
            echapper_(lignes[i][1]) + '</td></tr>';
  }

  html += '</table>' +
          '<p style="font-size:12px;color:#8C93A4;margin-top:14px">' + pied + '<br>' +
          '<a href="https://docs.google.com/spreadsheets/d/' + SHEET_ID + '" ' +
          'style="color:#1E4FD8">Ouvrir la feuille de suivi</a></p></div>';
  return html;
}

/* ------------------------------------------------------------- Utilitaires - */

function txt_(v) {
  if (v === null || v === undefined) return '';
  return String(v).trim();
}

function echapper_(v) {
  return txt_(v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>');
}

function estEmail_(v) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(txt_(v));
}

function horodatage_() {
  return Utilities.formatDate(new Date(), FUSEAU, 'dd/MM/yyyy HH:mm:ss');
}

function navigateur_(e) {
  try {
    return (e && e.parameter && e.parameter.ua) ? e.parameter.ua : '';
  } catch (err) {
    return '';
  }
}

function reponse_(ok, message, extra) {
  var corps = { ok: ok, message: message };
  if (extra) for (var k in extra) corps[k] = extra[k];
  return ContentService
    .createTextOutput(JSON.stringify(corps))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ------------------------------------------------------------- Tests ------- */

/**
 * À exécuter UNE FOIS depuis l'éditeur pour créer les onglets
 * et déclencher la demande d'autorisation Google.
 */
function initialiser() {
  var classeur = SpreadsheetApp.openById(SHEET_ID);
  var cmd = ongletCommandes_();
  var ct  = ongletContacts_();
  Logger.log('Classeur : ' + classeur.getName());
  Logger.log('Commandes -> onglet « ' + cmd.getName() + ' »');
  Logger.log('Contacts  -> onglet « ' + ct.getName() + ' »');
  Logger.log('En-têtes détectés : ' +
    cmd.getRange(1, 1, 1, Math.max(cmd.getLastColumn(), 1)).getValues()[0].join(' | '));
}

/**
 * Simule une commande sans passer par le site. Vérifiez ensuite
 * la feuille et votre boîte mail.
 */
function testerCommande() {
  var faux = {
    postData: {
      contents: JSON.stringify({
        offre: 'Gold', duree: '15 mois', bonus: '+3 mois offerts',
        connexions: 2, total: '92,48 €', code_promo: '',
        nom: 'Test Dupont', email: 'test@exemple.fr',
        telephone: '+212 612345678', pays: 'MA', appareil: 'Samsung TV 2021',
        paiement: 'PayPal', notes: 'Ceci est un test.',
        page: 'https://' + SITE + '/commande/?offre=gold&c=2'
      })
    }
  };
  Logger.log(doPost(faux).getContent());
}

/**
 * Simule un message du formulaire de contact.
 */
function testerContact() {
  var faux = {
    postData: {
      contents: JSON.stringify({
        nom: 'Test Martin', email: 'martin@exemple.fr',
        sujet: 'Compatibilité', message: 'Mon téléviseur est-il compatible ?',
        page: 'https://' + SITE + '/contact/'
      })
    }
  };
  Logger.log(doPost(faux).getContent());
}
