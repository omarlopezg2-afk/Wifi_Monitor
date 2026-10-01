#!/usr/bin/env python3
"""
Añade TikTok a los enlaces del pie de la landing y al `sameAs` de los datos
estructurados, en los 6 idiomas.

Se ejecuta DESPUÉS de `anadir-redes.py` (que puso Instagram, Facebook y YouTube),
por eso va aparte: es un añadido a una lista que ya existe, no una creación.

Datos comprobados el 01-10-2026: el usuario es `@wifimonitorapp` (el dueño lo
cambió desde `wifimonitorapp.wi`; TikTok no deja volver a cambiarlo hasta el
31-10-2026). La cuenta es personal y no tiene campo «Sitio web», así que el
enlace clicable en la bio no existe: la bio dice «Gratis en Microsoft Store» y
con eso basta.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
TIKTOK = "https://www.tiktok.com/@wifimonitorapp"
FICHEROS = ["index.html", "en/index.html", "pt/index.html", "fr/index.html",
            "de/index.html", "it/index.html"]

fallos = 0

for ruta in FICHEROS:
    f = RAIZ / ruta
    if not f.exists():
        print(f"FALLO  {ruta}: no existe")
        fallos += 1
        continue
    txt = f.read_text(encoding="utf-8")
    orig = txt

    # --- 1. el pie: TikTok detrás de YouTube ------------------------------
    if "tiktok.com" in txt:
        print(f"ya     {ruta}: TikTok ya estaba en el pie/sameAs")
    else:
        patron = re.compile(r'(<a href="https://www\.youtube\.com/@wifimonitorapp"[^>]*>YouTube</a>)')
        if not patron.search(txt):
            print(f"FALLO  {ruta}: no encuentro el enlace de YouTube en el pie")
            fallos += 1
            continue
        txt = patron.sub(
            lambda m: m.group(1) + f' · <a href="{TIKTOK}" rel="me" target="_blank">TikTok</a>',
            txt, count=1)
        print(f"OK     {ruta}: TikTok añadido al pie")

    # --- 2. sameAs: TikTok delante de Instagram ---------------------------
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', txt, re.S)
    if not m:
        print(f"FALLO  {ruta}: no encuentro los datos estructurados")
        fallos += 1
        continue
    bloque = m.group(1)
    if "tiktok.com" in bloque:
        print(f"ya     {ruta}: TikTok ya estaba en sameAs")
    else:
        nuevo = bloque.replace('"sameAs":[', '"sameAs":["' + TIKTOK + '",', 1)
        if nuevo == bloque:
            print(f"FALLO  {ruta}: no encuentro el sameAs")
            fallos += 1
            continue
        txt = txt[:m.start(1)] + nuevo + txt[m.end(1):]
        print(f"OK     {ruta}: TikTok añadido al sameAs")

    if txt != orig:
        f.write_text(txt, encoding="utf-8")

    # --- 3. revalidar el JSON-LD de lo escrito ----------------------------
    comp = f.read_text(encoding="utf-8")
    m2 = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', comp, re.S)
    try:
        d = json.loads(m2.group(1))
        cuentas = d.get("sameAs", [])
        print(f"       JSON válido · {len(cuentas)} cuentas · tiktok: {any('tiktok' in u for u in cuentas)}")
    except Exception as e:  # noqa: BLE001
        print(f"FALLO  {ruta}: el JSON-LD quedó inválido: {e}")
        fallos += 1

print()
print("FALLOS:", fallos)
raise SystemExit(1 if fallos else 0)
