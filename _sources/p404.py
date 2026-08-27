# -*- coding: utf-8 -*-
from tpl import head, header, FOOTER, SCHEMA_ORG, RACINE
import os
corps = """
<section class="section" style="padding-top:60px;min-height:52vh">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow" style="justify-content:center">Erreur 404</p>
      <h1>Cette page n'existe pas</h1>
      <p class="lead" style="margin-inline:auto">Le lien est peut-être ancien ou l'adresse comporte
        une erreur. Voici les pages les plus consultées&nbsp;:</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn btn--primaire" href="/abonnement-iptv/">Voir les abonnements</a>
        <a class="btn btn--fantome" href="/blog/">Lire le blog</a>
        <a class="btn btn--fantome" href="/contact/">Nous contacter</a>
      </div>
    </div>
  </div>
</section>
"""
doc = head("Page introuvable (404) | IPTV Abonnement France",
           "La page demandée n'existe pas ou a été déplacée.",
           "/404.html", schemas=[SCHEMA_ORG], robots="noindex, follow") + header() + corps + FOOTER
open(os.path.join(RACINE, "404.html"), "w", encoding="utf-8").write(doc)
print("404 ok")
