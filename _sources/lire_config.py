# -*- coding: utf-8 -*-
"""Lit assets/js/config.js pour que build.py et le site partagent la même source de tarifs."""
import re, json, os
from tpl import RACINE

def charger():
    src = open(os.path.join(RACINE, "assets/js/config.js"), encoding="utf-8").read()
    src = src[src.index("window.CONFIG = {") + len("window.CONFIG = "):]
    src = src[:src.rindex("};") + 1]
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)      # commentaires
    src = re.sub(r"(?m)^\s*//.*$", "", src)
    src = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', src)  # clés
    src = re.sub(r",(\s*[}\]])", r"\1", src)             # virgules finales
    return json.loads(src)
