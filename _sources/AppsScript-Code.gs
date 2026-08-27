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
var EMAIL_ALERTE = 'imadamhine@gmail.com';   // ← destinataire des alertes
var SITE         = 'iptvabonnementfrance.store';
var FUSEAU       = 'Europe/Paris';
var PREFIXE_REF  = 'IAF';                    // préfixe des références de commande

var ONGLET_COMMANDES = 'Commandes';
var ONGLET_CONTACTS  = 'Contacts';

var COLONNES_COMMANDES = [
  'Date', 'Référence', 'Statut', 'Offre', 'Durée', 'Bonus', 'Connexions',
  'Total', 'Code promo', 'Nom', 'E-mail', 'Téléphone', 'Appareil',
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
  var feuille = onglet_(ONGLET_COMMANDES, COLONNES_COMMANDES);
  var ref = reference_(feuille);

  feuille.appendRow([
    horodatage_(),
    ref,
    'Nouvelle',
    txt_(d.offre),
    txt_(d.duree),
    txt_(d.bonus),
    txt_(d.connexions),
    txt_(d.total),
    txt_(d.code_promo),
    txt_(d.nom),
    txt_(d.email),
    txt_(d.telephone),
    txt_(d.appareil),
    txt_(d.paiement),
    txt_(d.notes),
    txt_(d.page),
    navigateur_(e)
  ]);

  finaliser_(feuille, COLONNES_COMMANDES.length);
  return ref;
}

function enregistrerContact_(d, e) {
  var feuille = onglet_(ONGLET_CONTACTS, COLONNES_CONTACTS);
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
 * Récupère l'onglet, le crée avec ses en-têtes s'il n'existe pas encore.
 */
function onglet_(nom, colonnes) {
  var classeur = SpreadsheetApp.openById(SHEET_ID);
  var feuille = classeur.getSheetByName(nom);

  if (!feuille) {
    feuille = classeur.insertSheet(nom);
    feuille.appendRow(colonnes);
    var entete = feuille.getRange(1, 1, 1, colonnes.length);
    entete.setFontWeight('bold')
          .setBackground('#1E4FD8')
          .setFontColor('#FFFFFF')
          .setVerticalAlignment('middle');
    feuille.setRowHeight(1, 34);
    feuille.setFrozenRows(1);
  }
  return feuille;
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
  onglet_(ONGLET_COMMANDES, COLONNES_COMMANDES);
  onglet_(ONGLET_CONTACTS, COLONNES_CONTACTS);
  Logger.log('Onglets prêts dans : ' +
             SpreadsheetApp.openById(SHEET_ID).getName());
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
        telephone: '+33 6 12 34 56 78', appareil: 'Samsung TV 2021',
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
