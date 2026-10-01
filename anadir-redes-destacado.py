#!/usr/bin/env python3
"""
Pone los enlaces de las redes donde SE VEN, y retira el intento anterior.

Recorrido de este asunto, para no repetirlo:
1. `anadir-redes.py` y `anadir-tiktok.py` los pusieron en el pie → pero el pie
   queda al 99 % de la altura de la página (4.718 px de 4.789): invisibles.
2. Un primer intento los subió al bloque final → 94 %. Sigue siendo el fondo.
3. Decisión final: **en el héroe**, debajo de los distintivos. Ahí salen en la
   primera pantalla, que es lo único que se ve sin bajar, y se quedan también en
   el pie, que es lo convencional. La fila del bloque final se retira para no
   repetir la misma línea tres veces en la misma página.

Además, la página de privacidad no tenía ninguno de los cuatro enlaces: se los
añade en su pie.

Idempotente: si ya está en el héroe, no lo repite.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
REDES = [
    ("Instagram", "https://www.instagram.com/wifimonitor.app/"),
    ("Facebook", "https://www.facebook.com/profile.php?id=61594515976679"),
    ("YouTube", "https://www.youtube.com/@wifimonitorapp"),
    ("TikTok", "https://www.tiktok.com/@wifimonitorapp"),
]

# «También en», por idioma: informa, no pide que te sigan.
ETIQUETA = {
    "index.html": "También en:",
    "en/index.html": "Also on:",
    "pt/index.html": "Também em:",
    "fr/index.html": "Aussi sur :",
    "de/index.html": "Auch auf:",
    "it/index.html": "Anche su:",
}


def fila(etiqueta: str, sangria: str = "      ", clase: str = "note") -> str:
    enlaces = " · ".join(f'<a href="{u}" rel="me" target="_blank">{n}</a>' for n, u in REDES)
    return f'{sangria}<p class="{clase}">{etiqueta} {enlaces}</p>\n'


fallos = 0

for ruta, etiqueta in ETIQUETA.items():
    f = RAIZ / ruta
    if not f.exists():
        print(f"FALLO  {ruta}: no existe")
        fallos += 1
        continue
    txt = f.read_text(encoding="utf-8")
    orig = txt

    # --- 1. retirar la fila del bloque final (intento anterior) ------------
    fin = re.search(r'(<section class="final".*?</section>)', txt, re.S)
    if fin and "instagram.com/wifimonitor.app" in fin.group(1):
        bloque = re.sub(r'\n\s*<p class="note">[^\n]*instagram\.com/wifimonitor\.app[^\n]*</p>',
                        "", fin.group(1))
        txt = txt[:fin.start(1)] + bloque + txt[fin.end(1):]
        print(f"OK     {ruta}: retirada la fila del bloque final")

    # --- 2. ponerla en el héroe, debajo de los distintivos -----------------
    hero = re.search(r'(<section class="hero".*?)(<div class="badges">.*?</div>)', txt, re.S)
    if not hero:
        print(f"FALLO  {ruta}: no encuentro los distintivos del héroe")
        fallos += 1
        continue
    seccion_heroe = re.search(r'<section class="hero".*?</section>', txt, re.S)
    if seccion_heroe and "instagram.com/wifimonitor.app" in seccion_heroe.group(0):
        print(f"ya     {ruta}: la fila ya estaba en el héroe")
    else:
        txt = txt[:hero.end(2)] + "\n" + fila(etiqueta) + txt[hero.end(2):]
        print(f"OK     {ruta}: enlaces añadidos al héroe, bajo los distintivos")

    if txt != orig:
        f.write_text(txt, encoding="utf-8")

# --- 3. la página de privacidad: en su pie --------------------------------
priv = RAIZ / "privacidad/index.html"
if priv.exists():
    if "instagram.com/wifimonitor.app" in priv.read_text(encoding="utf-8"):
        print("ya     privacidad/index.html: ya los tenía")
    else:
        txt = priv.read_text(encoding="utf-8")
        m = re.search(r"(<footer>\s*\n\s*<p>.*?</p>)", txt, re.S)
        if not m:
            print("FALLO  privacidad/index.html: no encuentro el pie")
            fallos += 1
        else:
            txt = txt[:m.end(1)] + "\n" + fila("También en:", "    ", "redes") + txt[m.end(1):]
            priv.write_text(txt, encoding="utf-8")
            print("OK     privacidad/index.html: enlaces añadidos al pie")

# --- 4. comprobación: dónde queda la fila --------------------------------
print()
for ruta in list(ETIQUETA) + ["privacidad/index.html"]:
    f = RAIZ / ruta
    if not f.exists():
        continue
    t = f.read_text(encoding="utf-8")
    heroe = re.search(r'<section class="hero".*?</section>', t, re.S)
    fin = re.search(r'<section class="final".*?</section>', t, re.S)
    print(f"  {ruta:<26} héroe: {'sí' if heroe and 'instagram.com' in heroe.group(0) else 'no'}"
          f"  ·  bloque final: {'sí' if fin and 'instagram.com' in fin.group(0) else 'no'}"
          f"  ·  pie: {'sí' if re.search(r'<footer>.*?instagram.com', t, re.S) else 'no'}")

print()
print("FALLOS:", fallos)
raise SystemExit(1 if fallos else 0)
