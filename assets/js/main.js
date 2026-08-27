/* ==========================================================================
   iptvabonnementfrance.store — script principal
   Dépend de assets/js/config.js (chargé avant ce fichier)
   ========================================================================== */
(function () {
  "use strict";

  var C = window.CONFIG || {};
  var doc = document;
  var $  = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };

  /* ------------------------------------------------------- Header collé -- */
  var header = $(".site-header");
  if (header) {
    var majHeader = function () {
      header.classList.toggle("est-colle", window.scrollY > 8);
    };
    majHeader();
    window.addEventListener("scroll", majHeader, { passive: true });
  }

  /* ------------------------------------------------------ Menu mobile --- */
  var burger = $(".burger");
  var tiroir = $(".tiroir");
  if (burger && tiroir) {
    burger.addEventListener("click", function () {
      var ouvert = tiroir.classList.toggle("est-ouvert");
      burger.setAttribute("aria-expanded", ouvert ? "true" : "false");
      doc.body.style.overflow = ouvert ? "hidden" : "";
    });
    $$("a", tiroir).forEach(function (a) {
      a.addEventListener("click", function () {
        tiroir.classList.remove("est-ouvert");
        burger.setAttribute("aria-expanded", "false");
        doc.body.style.overflow = "";
      });
    });
    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && tiroir.classList.contains("est-ouvert")) burger.click();
    });
  }

  /* -------------------------------------------------- Apparition scroll -- */
  var cibles = $$(".reveal");
  if (cibles.length) {
    if ("IntersectionObserver" in window) {
      var obs = new IntersectionObserver(function (entrees) {
        entrees.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add("vu"); obs.unobserve(e.target); }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      cibles.forEach(function (el) { obs.observe(el); });
    } else {
      cibles.forEach(function (el) { el.classList.add("vu"); });
    }
  }

  /* ------------------------------------------------------------- FAQ ---- */
  $$(".faq-q").forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      var item = bouton.closest(".faq-item");
      var ouvert = item.classList.toggle("est-ouvert");
      bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
    });
  });

  /* ----------------------------------------------------- Lien de commande */
  /* Si aucun numéro WhatsApp n'est configuré, tous les CTA d'achat
     renvoient vers la page contact. Aucun numéro n'est affiché. */
  function lienCommande(offre, connexions) {
    if (offre) {
      return baseUrl() + "commande/?offre=" + encodeURIComponent(offre.id) +
             "&c=" + (connexions || 1);
    }
    return lienWhatsApp(offre, connexions);
  }

  function lienWhatsApp(offre, connexions) {
    if (C.whatsapp) {
      var txt = "Bonjour, je souhaite commander un abonnement IPTV.";
      if (offre) {
        txt += "\n\nOffre : " + offre.nom + " (" + offre.duree +
               (offre.bonus ? " " + offre.bonus : "") + ")";
        txt += "\nConnexions : " + (connexions || 1);
        if (offre.prix !== null && offre.prix !== undefined) {
          txt += "\nTotal : " + fmtPrix(total(offre.prix, connexions || 1)) + " " + (C.devise || "");
        }
      }
      txt += "\n\nMerci de me confirmer la suite.";
      return "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(txt);
    }
    return baseUrl() + "contact/";
  }

  function baseUrl() {
    var b = document.querySelector('meta[name="racine"]');
    return b ? b.content : "/";
  }

  /* Multiplicateur : 1re connexion plein tarif, les suivantes remisées. */
  function multiplicateur(n) {
    var r = (typeof C.remise_connexion === "number") ? C.remise_connexion : 0;
    return 1 + (n - 1) * (1 - r);
  }

  function total(base, n) {
    return Math.round(base * multiplicateur(n) * 100) / 100;
  }

  function fmtPrix(v) {
    return v.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  /* ============================ Briques partagées du tunnel ============== */

  var ICONES_PAIEMENT = {
    carte:    '<rect x="2" y="5" width="20" height="14" rx="2.5"/><path d="M2 10h20"/>',
    paypal:   '<path d="M6.5 20 8.8 5.2h5.4c2.6 0 4.2 1.3 3.8 3.8-.4 2.7-2.4 4.1-5.2 4.1h-2L10 20z"/>',
    virement: '<path d="M3 10 12 4l9 6"/><path d="M5 10v8M12 10v8M19 10v8M3 20h18"/>',
    whatsapp: '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3.5 20.5l1.7-5A8.5 8.5 0 1 1 21 11.5z"/>'
  };

  function svgIcone(d) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" ' +
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>';
  }

  /* Tuiles de choix du moyen de paiement */
  function tuilesPaiement(prefixe) {
    var m = C.moyens_paiement || [];
    return '<div class="paiements" role="radiogroup" aria-label="Mode de paiement">' +
      m.map(function (p, i) {
        return '<button type="button" class="paiement' + (i === 0 ? ' est-choisi' : '') + '" ' +
          'role="radio" aria-checked="' + (i === 0) + '" data-paiement="' + p.nom + '" ' +
          'id="' + prefixe + '-pay-' + p.id + '">' +
          '<span class="paiement-ico">' + svgIcone(ICONES_PAIEMENT[p.icone] || ICONES_PAIEMENT.carte) +
          '</span>' + p.nom + '</button>';
      }).join('') + '</div>';
  }

  function brancherPaiements(racine) {
    var tuiles = $$(".paiement", racine);
    tuiles.forEach(function (t) {
      t.addEventListener("click", function () {
        tuiles.forEach(function (x) {
          x.classList.remove("est-choisi");
          x.setAttribute("aria-checked", "false");
        });
        t.classList.add("est-choisi");
        t.setAttribute("aria-checked", "true");
      });
    });
    return function () {
      var choisi = $(".paiement.est-choisi", racine);
      return choisi ? choisi.getAttribute("data-paiement") : "";
    };
  }

  /* Champ téléphone avec sélecteur d'indicatif international */
  function champTelephone(prefixe) {
    var pays = window.INDICATIFS || [];
    var defaut = C.pays_defaut || "FR";
    var options = pays.map(function (p) {
      return '<option value="' + p.iso + '" data-ind="' + p.ind + '"' +
             (p.iso === defaut ? ' selected' : '') + '>' +
             p.drapeau + ' +' + p.ind + '  ' + p.nom + '</option>';
    }).join('');
    return '<div class="tel-ligne">' +
      '<select class="tel-pays" id="' + prefixe + '-pays" aria-label="Indicatif du pays">' +
        options + '</select>' +
      '<input type="tel" class="tel-num" id="' + prefixe + '-tel" ' +
        'inputmode="tel" autocomplete="tel-national" placeholder="6 12 34 56 78">' +
      '</div>';
  }

  function lireTelephone(prefixe) {
    var sel = $("#" + prefixe + "-pays");
    var num = $("#" + prefixe + "-tel");
    if (!sel || !num) return "";
    var brut = num.value.replace(/[^0-9]/g, "");
    if (!brut) return "";
    var ind = sel.options[sel.selectedIndex].getAttribute("data-ind");
    return "+" + ind + " " + brut.replace(/^0+/, "");
  }

  function paysChoisi(prefixe) {
    var sel = $("#" + prefixe + "-pays");
    return sel ? sel.value : "";
  }

  /* ------------------------------------------------------------ Tarifs -- */
  var zoneTarifs = $("[data-tarifs]");
  if (zoneTarifs && Array.isArray(C.offres)) {
    var maxC = C.max_connexions || 5;
    var pct  = Math.round((C.remise_connexion || 0) * 100);

    zoneTarifs.innerHTML = C.offres.map(function (o, idx) {
      var sansPrix = (o.prix === null || o.prix === undefined || o.prix === "");
      var prixBloc = sansPrix
        ? '<div class="offre-prix" data-vide="1">Tarif sur demande</div>'
        : '<div class="offre-prix"><span data-montant>' + fmtPrix(o.prix) + '</span>' +
          (C.devise || "") + ' <small>/ ' + o.duree + '</small></div>';

      var stepper = sansPrix ? '' : '' +
        '<div class="stepper" data-stepper>' +
          '<button type="button" class="stepper-btn" data-moins aria-label="Retirer une connexion">−</button>' +
          '<span class="stepper-val"><b data-nb>1</b> <span data-mot>connexion</span></span>' +
          '<button type="button" class="stepper-btn" data-plus aria-label="Ajouter une connexion">+</button>' +
        '</div>' +
        '<p class="stepper-note">Première connexion au tarif normal · chaque connexion ' +
        'supplémentaire <b>' + pct + ' % moins chère</b></p>';

      var badge = o.badge
        ? '<span class="ruban ruban--' + (o.badge_type === "vert" ? "vert" : "bleu") + '">' +
          o.badge + '</span>'
        : '';

      var vedette = (o.badge_type === "vert") ? "offre--vert" : (o.badge ? "offre--vedette" : "");

      return '' +
        '<article class="offre reveal ' + vedette + '" data-offre="' + idx + '">' +
          badge +
          '<div class="offre-nom">' + o.nom + '</div>' +
          '<div class="offre-duree">' + o.duree +
            (o.bonus ? ' <em class="offre-bonus">' + o.bonus + '</em>' : '') + '</div>' +
          prixBloc +
          stepper +
          '<ul class="offre-liste">' +
            (o.avantages || []).map(function (a) { return '<li>' + a + '</li>'; }).join('') +
          '</ul>' +
          '<a class="btn ' + (o.badge_type === "vert" ? "btn--vert" :
              (o.badge ? "btn--primaire" : "btn--fantome")) + ' btn--bloc" data-commander ' +
              'href="' + lienCommande(o, 1) + '" data-ouvre-modale>Commander maintenant</a>' +
        '</article>';
    }).join('');

    /* Sélecteur de connexions : met à jour le prix et le lien WhatsApp */
    $$("[data-offre]", zoneTarifs).forEach(function (carte) {
      var o = C.offres[parseInt(carte.getAttribute("data-offre"), 10)];
      if (!o || o.prix === null || o.prix === undefined) return;
      var n = 1;
      var elNb  = $("[data-nb]", carte);
      var elMot = $("[data-mot]", carte);
      var elMt  = $("[data-montant]", carte);
      var lien  = $("[data-commander]", carte);
      var moins = $("[data-moins]", carte);
      var plus  = $("[data-plus]", carte);

      function maj() {
        elNb.textContent = n;
        elMot.textContent = n > 1 ? "connexions" : "connexion";
        elMt.textContent = fmtPrix(total(o.prix, n));
        lien.href = lienCommande(o, n);
        moins.disabled = (n <= 1);
        plus.disabled = (n >= maxC);
      }
      moins.addEventListener("click", function () { if (n > 1) { n--; maj(); } });
      plus.addEventListener("click", function () { if (n < maxC) { n++; maj(); } });
      maj();
    });

    /* Les CTA ouvrent la modale ; le href reste valide en repli sans JS. */
    $$("[data-ouvre-modale]", zoneTarifs).forEach(function (a) {
      a.addEventListener("click", function (e) {
        var carte = a.closest("[data-offre]");
        var o = C.offres[parseInt(carte.getAttribute("data-offre"), 10)];
        var n = parseInt($("[data-nb]", carte) ? $("[data-nb]", carte).textContent : "1", 10) || 1;
        e.preventDefault();
        ouvrirModale(o, n);
      });
    });

    reobserver(zoneTarifs);
  }

  /* --------------------------------------------------------- Appareils -- */
  var zoneApp = $("[data-appareils]");
  if (zoneApp && Array.isArray(C.appareils)) {
    zoneApp.innerHTML = C.appareils.map(function (a) {
      return '' +
        '<div class="appareil reveal">' +
          '<span class="marque-logo" role="img" aria-label="' + a.nom + '" ' +
            'style="--logo:url(/assets/img/marques/' + a.logo + '.svg)"></span>' +
          '<b>' + a.nom + '</b>' +
          '<span>' + (a.detail || "") + '</span>' +
        '</div>';
    }).join('');
    reobserver(zoneApp);
  }

  /* ---------------------------------------------------------- Chiffres -- */
  var zoneChiffres = $("[data-chiffres]");
  if (zoneChiffres) {
    var dispo = (C.chiffres || []).filter(function (c) {
      return c.valeur !== null && c.valeur !== undefined && c.valeur !== "";
    });
    if (!dispo.length) {
      // Aucun chiffre vérifié n'a été renseigné : on masque la section.
      var sec = zoneChiffres.closest("section");
      if (sec) sec.remove(); else zoneChiffres.remove();
    } else {
      zoneChiffres.innerHTML = dispo.map(function (c) {
        return '<div class="chiffre reveal">' +
          '<div class="chiffre-val" data-compteur="' + c.valeur + '" ' +
            'data-suffixe="' + (c.suffixe || '') + '">0' + (c.suffixe || '') + '</div>' +
          '<p>' + c.libelle + '</p></div>';
      }).join('');
      reobserver(zoneChiffres);
      lancerCompteurs();
    }
  }

  function lancerCompteurs() {
    var els = $$("[data-compteur]");
    if (!els.length) return;

    var reduit = window.matchMedia &&
                 window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function ecrire(el, valeur) {
      el.textContent = Math.round(valeur).toLocaleString("fr-FR") +
                       (el.getAttribute("data-suffixe") || "");
    }

    function animer(el) {
      var fin = parseFloat(el.getAttribute("data-compteur")) || 0;
      if (reduit) { ecrire(el, fin); return; }
      var t0 = null, duree = 1600;
      function pas(t) {
        if (t0 === null) t0 = t;
        var p = Math.min((t - t0) / duree, 1);
        ecrire(el, fin * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(pas);
      }
      requestAnimationFrame(pas);
    }

    if (!("IntersectionObserver" in window)) {
      els.forEach(animer);
      return;
    }
    var o = new IntersectionObserver(function (ent) {
      ent.forEach(function (e) {
        if (!e.isIntersecting) return;
        o.unobserve(e.target);
        animer(e.target);
      });
    }, { threshold: 0.35 });
    els.forEach(function (el) { o.observe(el); });
  }

  /* ------------------------------------------- CTA génériques -> commande */
  $$("[data-cta-commande]").forEach(function (a) {
    a.href = baseUrl() + "commande/";
  });

  /* ============================== Modale de commande ==================== */

  var modale = null, modaleEtat = null, focusAvant = null;

  function construireModale() {
    if (modale) return modale;
    modale = doc.createElement("div");
    modale.className = "modale";
    modale.setAttribute("role", "dialog");
    modale.setAttribute("aria-modal", "true");
    modale.setAttribute("aria-labelledby", "modale-titre");
    modale.innerHTML = '' +
      '<div class="modale-fond" data-fermer></div>' +
      '<div class="modale-boite">' +
        '<button type="button" class="modale-croix" data-fermer aria-label="Fermer">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
          'stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>' +
        '</button>' +
        '<div class="modale-corps"></div>' +
      '</div>';
    doc.body.appendChild(modale);

    doc.addEventListener("keydown", function (e) {
      if (!modale.classList.contains("est-ouverte")) return;
      if (e.key === "Escape") fermerModale();
      if (e.key === "Tab") piegerFocus(e);
    });
    return modale;
  }

  function brancherFermeture() {
    $$("[data-fermer]", modale).forEach(function (el) {
      el.addEventListener("click", fermerModale);
    });
  }

  function piegerFocus(e) {
    var f = $$('a[href], button:not([disabled]), input, select, textarea', modale)
      .filter(function (el) { return el.offsetParent !== null; });
    if (!f.length) return;
    var premier = f[0], dernier = f[f.length - 1];
    if (e.shiftKey && doc.activeElement === premier) { e.preventDefault(); dernier.focus(); }
    else if (!e.shiftKey && doc.activeElement === dernier) { e.preventDefault(); premier.focus(); }
  }

  function fermerModale() {
    if (!modale) return;
    modale.classList.remove("est-ouverte");
    doc.body.style.overflow = "";
    if (focusAvant && focusAvant.focus) focusAvant.focus();
  }

  function ouvrirModale(offre, nb) {
    construireModale();
    focusAvant = doc.activeElement;
    modaleEtat = { offre: offre, nb: nb || 1 };

    var sansPrix = (offre.prix === null || offre.prix === undefined);
    var totalTxt = sansPrix ? "Sur demande"
                            : fmtPrix(total(offre.prix, modaleEtat.nb)) + " " + (C.devise || "");
    var pluriel = modaleEtat.nb > 1 ? "s" : "";

    $(".modale-corps", modale).innerHTML = '' +
      '<h2 id="modale-titre">Finalisez votre commande</h2>' +
      '<p class="modale-intro">Vérifiez votre formule et renseignez vos coordonnées pour continuer.</p>' +

      '<div class="modale-recap">' +
        '<div class="mr-ligne"><span>Abonnement</span><b>' + offre.nom + ' — ' + offre.duree +
          (offre.bonus ? ' (' + offre.bonus + ')' : '') + '</b></div>' +
        '<div class="mr-ligne"><span>Connexions</span><b id="m-nb">' + modaleEtat.nb +
          ' connexion' + pluriel + ' simultanée' + pluriel + '</b></div>' +
        '<div class="mr-sep"></div>' +
        '<div class="mr-total"><span>Total à régler</span><b id="m-total">' + totalTxt + '</b></div>' +
      '</div>' +

      '<div class="champ"><label for="m-nom">Nom complet</label>' +
        '<input type="text" id="m-nom" autocomplete="name" placeholder="Jean Dupont" required></div>' +

      '<div class="champ"><label for="m-email">Adresse e-mail</label>' +
        '<input type="email" id="m-email" autocomplete="email" placeholder="jean.dupont@email.fr" required></div>' +

      '<div class="champ"><label for="m-tel">Téléphone</label>' + champTelephone("m") + '</div>' +

      '<div class="champ"><label>Mode de paiement</label>' + tuilesPaiement("m") + '</div>' +

      '<div class="message-form" id="m-msg" role="status" aria-live="polite"></div>' +

      '<button type="button" class="btn btn--primaire btn--bloc modale-valider" id="m-valider">' +
        'Continuer vers le paiement</button>' +

      '<p class="modale-note">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>' +
        "Aucune donnée de carte n'est saisie sur ce site. Après votre commande, nous vous " +
        'envoyons les instructions de paiement sécurisé.</p>' +
      (C.whatsapp ? '<p class="modale-wa">Une question ? <a data-wa-modale href="#">WhatsApp ' +
        (C.whatsapp_affiche || ("+" + C.whatsapp)) + '</a></p>' : '') +
      '<button type="button" class="modale-annuler" data-fermer>Annuler</button>';

    var lirePaiement = brancherPaiements(modale);
    brancherFermeture();

    if (C.whatsapp) {
      $$("[data-wa-modale]", modale).forEach(function (el) {
        el.href = "https://wa.me/" + C.whatsapp;
        el.target = "_blank";
        el.rel = "noopener";
      });
    }

    $("#m-valider", modale).addEventListener("click", function () {
      envoyerDepuisModale(lirePaiement);
    });

    modale.classList.add("est-ouverte");
    doc.body.style.overflow = "hidden";
    setTimeout(function () { var n = $("#m-nom", modale); if (n) n.focus(); }, 60);
  }

  function envoyerDepuisModale(lirePaiement) {
    var msg = $("#m-msg", modale);
    var o = modaleEtat.offre;
    var d = {
      offre: o.nom, duree: o.duree, bonus: o.bonus || "",
      connexions: modaleEtat.nb,
      total: $("#m-total", modale).textContent,
      code_promo: "",
      nom: $("#m-nom", modale).value.trim(),
      email: $("#m-email", modale).value.trim(),
      telephone: lireTelephone("m"),
      pays: paysChoisi("m"),
      appareil: "",
      paiement: lirePaiement(),
      notes: "",
      page: location.href
    };

    if (!d.nom) {
      afficher(msg, "ko", "Merci d'indiquer votre nom.");
      $("#m-nom", modale).focus();
      return;
    }
    if (!d.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) {
      afficher(msg, "ko", "Merci d'indiquer une adresse e-mail valide.");
      $("#m-email", modale).focus();
      return;
    }

    var btn = $("#m-valider", modale);
    btn.disabled = true;
    var ancien = btn.textContent;
    btn.textContent = "Envoi…";

    function terminer() {
      btn.disabled = false;
      btn.textContent = ancien;
      succesModale(d);
    }
    if (!C.endpoint) { terminer(); return; }
    fetch(C.endpoint, {
      method: "POST", mode: "no-cors",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(d)
    }).then(terminer).catch(terminer);
  }

  function succesModale(d) {
    var wa = "";
    if (C.whatsapp) {
      var t = "NOUVELLE COMMANDE\n\n" +
        "Offre : " + d.offre + " (" + d.duree + (d.bonus ? " " + d.bonus : "") + ")\n" +
        "Connexions : " + d.connexions + "\n" +
        "Total : " + d.total + "\n\n" +
        "Nom : " + d.nom + "\n" +
        "E-mail : " + d.email + "\n" +
        (d.telephone ? "Téléphone : " + d.telephone + "\n" : "") +
        "Paiement : " + d.paiement;
      wa = "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(t);
      window.open(wa, "_blank", "noopener");
    }

    $(".modale-corps", modale).innerHTML = '' +
      '<div class="modale-succes">' +
        '<span class="succes-rond">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" ' +
          'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>' +
        '</span>' +
        '<h2 id="modale-titre">Commande enregistrée</h2>' +
        '<p>Merci ' + d.nom.split(" ")[0] + '. Nous vous envoyons les instructions de paiement à ' +
        '<b>' + d.email + '</b>, puis vos accès dès confirmation.</p>' +
        (wa ? '<a class="btn btn--vert btn--bloc" href="' + wa + '" target="_blank" rel="noopener">' +
              'Confirmer sur WhatsApp</a>' : '') +
        '<button type="button" class="modale-annuler" data-fermer>Fermer</button>' +
      '</div>';
    brancherFermeture();
  }

  /* -------------------------------------------------- Bouton WhatsApp --- */
  if (!C.whatsapp) {
    $$("[data-whatsapp]").forEach(function (el) { el.remove(); });
    $$("[data-whatsapp-flottant]").forEach(function (el) { el.remove(); });
    $$("[data-wa-sujet]").forEach(function (el) {
      el.href = "https://wa.me/" + C.whatsapp +
                "?text=" + encodeURIComponent(el.getAttribute("data-wa-sujet"));
      el.target = "_blank";
      el.rel = "noopener";
    });
    $$("[data-numero]").forEach(function (el) { el.remove(); });
  } else {
    var urlWa = "https://wa.me/" + C.whatsapp +
      "?text=" + encodeURIComponent("Bonjour, j'ai une question sur les abonnements IPTV.");
    $$("[data-whatsapp], [data-whatsapp-flottant]").forEach(function (el) {
      el.href = urlWa;
      el.target = "_blank";
      el.rel = "noopener";
    });
    $$("[data-wa-sujet]").forEach(function (el) {
      el.href = "https://wa.me/" + C.whatsapp +
                "?text=" + encodeURIComponent(el.getAttribute("data-wa-sujet"));
      el.target = "_blank";
      el.rel = "noopener";
    });
    $$("[data-numero]").forEach(function (el) {
      el.textContent = C.whatsapp_affiche || ("+" + C.whatsapp);
      if (el.tagName === "A") { el.href = urlWa; el.target = "_blank"; el.rel = "noopener"; }
    });
  }

  /* --------------------------------------------------- E-mail affiché --- */
  $$("[data-email]").forEach(function (el) {
    if (!C.email) { el.remove(); return; }
    el.textContent = C.email;
    if (el.tagName === "A") el.href = "mailto:" + C.email;
  });

  /* ------------------------------------------------------- Page commande --- */
  var zoneCmd = $("[data-commande]");
  if (zoneCmd && Array.isArray(C.offres)) {
    (function () {
      var params = new URLSearchParams(location.search);
      var maxC   = C.max_connexions || 5;
      var promos = C.codes_promo || {};
      var idx = 0;
      C.offres.forEach(function (o, i) { if (o.id === params.get("offre")) idx = i; });
      var nb = Math.min(Math.max(parseInt(params.get("c"), 10) || 1, 1), maxC);
      var remisePromo = 0, codeApplique = "";

      var selOffres = C.offres.map(function (o, i) {
        return '<option value="' + i + '"' + (i === idx ? ' selected' : '') + '>' +
               o.nom + ' — ' + o.duree + (o.bonus ? ' (' + o.bonus + ')' : '') + '</option>';
      }).join('');

      var champPromo = Object.keys(promos).length ? '' +
        '<div class="promo-ligne">' +
          '<input type="text" id="promo" placeholder="Code promo" autocomplete="off">' +
          '<button type="button" class="btn btn--fantome btn--sm" id="promo-btn">Appliquer</button>' +
        '</div>' +
        '<p class="promo-msg" id="promo-msg"></p>' : '';

      zoneCmd.innerHTML = '' +
      '<div class="commande-grille">' +

        '<div class="commande-form">' +
          '<h2 class="commande-titre">1 · Votre abonnement</h2>' +
          '<div class="champ">' +
            '<label for="cmd-offre">Formule</label>' +
            '<select id="cmd-offre">' + selOffres + '</select>' +
          '</div>' +
          '<div class="champ">' +
            '<label>Connexions simultanées</label>' +
            '<div class="stepper" style="margin-top:0">' +
              '<button type="button" class="stepper-btn" id="cmd-moins" aria-label="Retirer une connexion">−</button>' +
              '<span class="stepper-val"><b id="cmd-nb">1</b> <span id="cmd-mot">connexion</span></span>' +
              '<button type="button" class="stepper-btn" id="cmd-plus" aria-label="Ajouter une connexion">+</button>' +
            '</div>' +
            '<p class="stepper-note" style="text-align:left">Une connexion = un appareil qui regarde ' +
            'en même temps. Chaque connexion supplémentaire est ' +
            (Math.round((C.remise_connexion || 0) * 100)) + ' % moins chère.</p>' +
          '</div>' +

          '<h2 class="commande-titre">2 · Vos coordonnées</h2>' +
          '<div class="champ">' +
            '<label for="cmd-nom">Nom et prénom</label>' +
            '<input type="text" id="cmd-nom" autocomplete="name" placeholder="Votre nom" required>' +
          '</div>' +
          '<div class="champ">' +
            '<label for="cmd-email">Adresse e-mail</label>' +
            '<input type="email" id="cmd-email" autocomplete="email" placeholder="vous@exemple.fr" required>' +
            '<p class="tiny" style="margin:0">C\'est à cette adresse que vos informations de configuration seront envoyées.</p>' +
          '</div>' +
          '<div class="champ">' +
            '<label for="cmd-tel">Téléphone ou WhatsApp</label>' + champTelephone("cmd") +
          '</div>' +
          '<div class="champ">' +
            '<label for="cmd-appareil">Appareil utilisé</label>' +
            '<input type="text" id="cmd-appareil" placeholder="Ex. Samsung TV 2021, Fire TV Stick, iPhone…">' +
            '<p class="tiny" style="margin:0">Nous vérifions la compatibilité avant de vous envoyer vos accès.</p>' +
          '</div>' +

          '<h2 class="commande-titre">3 · Paiement</h2>' +
          '<div class="champ">' +
            '<label>Moyen de paiement souhaité</label>' + tuilesPaiement("cmd") +
          '</div>' +
          '<div class="encart" style="margin:0">' +
            '<p style="font-size:.9rem;margin:0">Aucun paiement n\'est demandé sur cette page et ' +
            'aucune donnée bancaire n\'est saisie ici. Après validation, nous vous envoyons le lien ' +
            'ou les coordonnées correspondant au moyen choisi.</p>' +
          '</div>' +
          '<div class="champ" style="margin-top:18px">' +
            '<label for="cmd-notes">Précisions <span style="text-transform:none">(facultatif)</span></label>' +
            '<textarea id="cmd-notes" style="min-height:100px" placeholder="Une question, une demande particulière…"></textarea>' +
          '</div>' +
        '</div>' +

        '<aside class="commande-recap">' +
          '<div class="recap-bloc">' +
            '<h3>Récapitulatif</h3>' +
            '<div class="recap-ligne"><span>Formule</span><b id="r-offre">—</b></div>' +
            '<div class="recap-ligne"><span>Durée</span><b id="r-duree">—</b></div>' +
            '<div class="recap-ligne" id="r-bonus-ligne"><span>Offert</span><b id="r-bonus" class="vert">—</b></div>' +
            '<div class="recap-ligne"><span>Connexions</span><b id="r-nb">1</b></div>' +
            '<div class="recap-sep"></div>' +
            '<div class="recap-ligne"><span>Tarif de base</span><b id="r-base">—</b></div>' +
            '<div class="recap-ligne" id="r-eco-ligne"><span>Remise connexions</span><b id="r-eco" class="vert">—</b></div>' +
            '<div class="recap-ligne" id="r-promo-ligne"><span>Code promo</span><b id="r-promo" class="vert">—</b></div>' +
            champPromo +
            '<div class="recap-sep"></div>' +
            '<div class="recap-total"><span>Total</span><b id="r-total">—</b></div>' +
            '<div class="message-form" id="cmd-msg" role="status" aria-live="polite"></div>' +
            '<button type="button" class="btn btn--primaire btn--bloc" id="cmd-valider" style="margin-top:16px">Confirmer la commande</button>' +
            '<p class="tiny" style="margin-top:14px">En confirmant, vous acceptez nos ' +
            '<a href="/conditions-generales/">conditions générales</a> et notre ' +
            '<a href="/politique-confidentialite/">politique de confidentialité</a>.</p>' +
          '</div>' +
          '<div class="recap-bloc recap-rassurance">' +
            '<p><b>Livraison immédiate</b> — vos accès sont envoyés dès confirmation du paiement.</p>' +
            '<p><b>Support 24/7</b> — nous vous accompagnons pour l\'installation.</p>' +
            '<p><b>Aucune donnée bancaire</b> — rien n\'est saisi sur ce site.</p>' +
          '</div>' +
        '</aside>' +
      '</div>';

      var lirePaiementCmd = brancherPaiements(zoneCmd);

      /* -------- Références -------- */
      var elOffre = $("#cmd-offre"), elNb = $("#cmd-nb"), elMot = $("#cmd-mot");
      var rOffre = $("#r-offre"), rDuree = $("#r-duree"), rBonus = $("#r-bonus");
      var rBonusL = $("#r-bonus-ligne"), rNb = $("#r-nb"), rBase = $("#r-base");
      var rEco = $("#r-eco"), rEcoL = $("#r-eco-ligne"), rPromo = $("#r-promo");
      var rPromoL = $("#r-promo-ligne"), rTotal = $("#r-total");

      function offre() { return C.offres[parseInt(elOffre.value, 10)]; }

      function maj() {
        var o = offre();
        elNb.textContent = nb;
        elMot.textContent = nb > 1 ? "connexions" : "connexion";
        $("#cmd-moins").disabled = (nb <= 1);
        $("#cmd-plus").disabled = (nb >= maxC);

        rOffre.textContent = o.nom;
        rDuree.textContent = o.duree;
        rNb.textContent = nb;
        if (o.bonus) { rBonus.textContent = o.bonus; rBonusL.style.display = ""; }
        else { rBonusL.style.display = "none"; }

        if (o.prix === null || o.prix === undefined) {
          rBase.textContent = "sur demande";
          rEcoL.style.display = "none";
          rPromoL.style.display = "none";
          rTotal.textContent = "Sur demande";
          return;
        }
        var plein  = Math.round(o.prix * nb * 100) / 100;
        var remise = total(o.prix, nb);
        var eco    = Math.round((plein - remise) * 100) / 100;
        var fin    = Math.round(remise * (1 - remisePromo) * 100) / 100;

        rBase.textContent = fmtPrix(plein) + " " + (C.devise || "");
        if (eco > 0) { rEco.textContent = "− " + fmtPrix(eco) + " " + (C.devise || ""); rEcoL.style.display = ""; }
        else { rEcoL.style.display = "none"; }
        if (remisePromo > 0) {
          rPromo.textContent = codeApplique + " · − " +
            fmtPrix(Math.round(remise * remisePromo * 100) / 100) + " " + (C.devise || "");
          rPromoL.style.display = "";
        } else { rPromoL.style.display = "none"; }
        rTotal.textContent = fmtPrix(fin) + " " + (C.devise || "");
      }

      elOffre.addEventListener("change", function () { maj(); histo(); });
      $("#cmd-moins").addEventListener("click", function () { if (nb > 1) { nb--; maj(); histo(); } });
      $("#cmd-plus").addEventListener("click", function () { if (nb < maxC) { nb++; maj(); histo(); } });

      function histo() {
        try {
          history.replaceState(null, "", "?offre=" + offre().id + "&c=" + nb);
        } catch (e) {}
      }

      /* -------- Code promo -------- */
      var btnPromo = $("#promo-btn");
      if (btnPromo) {
        btnPromo.addEventListener("click", function () {
          var code = $("#promo").value.trim().toUpperCase();
          var msg = $("#promo-msg");
          if (promos[code]) {
            remisePromo = promos[code];
            codeApplique = code;
            msg.textContent = "Code appliqué : −" + Math.round(remisePromo * 100) + " %";
            msg.className = "promo-msg ok";
          } else {
            remisePromo = 0; codeApplique = "";
            msg.textContent = "Ce code n'est pas valide.";
            msg.className = "promo-msg ko";
          }
          maj();
        });
      }

      /* -------- Validation et envoi -------- */
      $("#cmd-valider").addEventListener("click", function () {
        var msg = $("#cmd-msg");
        var o = offre();
        var d = {
          offre: o.nom, duree: o.duree, bonus: o.bonus || "",
          connexions: nb,
          total: rTotal.textContent,
          code_promo: codeApplique,
          nom: $("#cmd-nom").value.trim(),
          email: $("#cmd-email").value.trim(),
          telephone: lireTelephone("cmd"),
          pays: paysChoisi("cmd"),
          appareil: $("#cmd-appareil").value.trim(),
          paiement: lirePaiementCmd(),
          notes: $("#cmd-notes").value.trim(),
          page: location.href
        };

        if (!d.nom) { afficher(msg, "ko", "Merci d'indiquer votre nom."); $("#cmd-nom").focus(); return; }
        if (!d.email || d.email.indexOf("@") < 1) {
          afficher(msg, "ko", "Merci d'indiquer une adresse e-mail valide."); $("#cmd-email").focus(); return;
        }

        var btn = $("#cmd-valider");
        btn.disabled = true;
        var ancien = btn.textContent;
        btn.textContent = "Envoi…";

        function terminer() {
          btn.disabled = false;
          btn.textContent = ancien;
          afficher(msg, "ok", "Commande enregistrée. Nous vous contactons pour finaliser le paiement.");
          if (C.whatsapp) {
            var t = "NOUVELLE COMMANDE\n\n" +
              "Offre : " + d.offre + " (" + d.duree + (d.bonus ? " " + d.bonus : "") + ")\n" +
              "Connexions : " + d.connexions + "\n" +
              (d.code_promo ? "Code promo : " + d.code_promo + "\n" : "") +
              "Total : " + d.total + "\n\n" +
              "Nom : " + d.nom + "\n" +
              "E-mail : " + d.email + "\n" +
              (d.telephone ? "Téléphone : " + d.telephone + "\n" : "") +
              (d.appareil ? "Appareil : " + d.appareil + "\n" : "") +
              "Paiement : " + d.paiement +
              (d.notes ? "\n\nPrécisions : " + d.notes : "");
            window.open("https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(t), "_blank", "noopener");
          }
        }

        if (!C.endpoint) { terminer(); return; }
        fetch(C.endpoint, {
          method: "POST", mode: "no-cors",
          headers: { "Content-Type": "text/plain;charset=utf-8" },
          body: JSON.stringify(d)
        }).then(terminer).catch(terminer);
      });

      maj();
    })();
  }

  /* ------------------------------------------------ Formulaire contact -- */
  var form = $("#form-contact");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $("#form-message");
      var btn = $("button[type=submit]", form);
      var data = {
        nom:    form.nom.value.trim(),
        email:  form.email.value.trim(),
        sujet:  form.sujet.value.trim(),
        message: form.message.value.trim(),
        page:   location.href
      };
      if (!data.nom || !data.email || !data.message) {
        afficher(msg, "ko", "Merci de renseigner votre nom, votre e-mail et votre message.");
        return;
      }

      if (!C.endpoint) {
        // Repli sans serveur : ouvre le client mail de l'utilisateur.
        var corps = "Nom : " + data.nom + "\nE-mail : " + data.email + "\n\n" + data.message;
        window.location.href = "mailto:" + (C.email || "") +
          "?subject=" + encodeURIComponent(data.sujet || "Demande depuis le site") +
          "&body=" + encodeURIComponent(corps);
        afficher(msg, "ok", "Votre logiciel de messagerie va s'ouvrir pour finaliser l'envoi.");
        return;
      }

      btn.disabled = true;
      var ancien = btn.textContent;
      btn.textContent = "Envoi…";
      fetch(C.endpoint, {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify(data)
      }).then(function () {
        form.reset();
        afficher(msg, "ok", "Message envoyé. Nous vous répondons dès que possible.");
      }).catch(function () {
        afficher(msg, "ko", "L'envoi a échoué. Réessayez ou écrivez-nous directement par e-mail.");
      }).then(function () {
        btn.disabled = false;
        btn.textContent = ancien;
      });
    });
  }

  function afficher(el, type, texte) {
    if (!el) return;
    el.className = "message-form " + type;
    el.textContent = texte;
  }

  /* --------------------------------------------- Observer les nouveaux -- */
  function reobserver(racine) {
    if (!("IntersectionObserver" in window)) {
      $$(".reveal", racine).forEach(function (el) { el.classList.add("vu"); });
      return;
    }
    var o = new IntersectionObserver(function (ent) {
      ent.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("vu"); o.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    $$(".reveal", racine).forEach(function (el) { o.observe(el); });
  }

  /* --------------------------------------------- Année dans le footer --- */
  $$("[data-annee]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

})();
