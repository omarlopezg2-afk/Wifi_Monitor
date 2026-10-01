#!/usr/bin/env python3
"""
Añade a la landing los enlaces a las redes del producto y los declara en los
datos estructurados (`sameAs`), que es lo que hace que Google y Bing asocien
las cuentas a la marca.

- El enlace del pie dice «También en:», no «Síguenos»: informa, no pide. Es la
  misma regla del contenido de los vídeos.
- El `sameAs` va dentro del bloque JSON-LD que ya existe (`SoftwareApplication`),
  y el bloque se revalida con `json.loads` después de tocarlo: unos datos
  estructurados rotos son peores que no tenerlos.

Idempotente: si ya está, no lo repite.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

REDES = [
    ("Instagram", "https://www.instagram.com/wifimonitor.app/"),
    # Comprobado el 1-oct-2026 con la sesión del dueño: este es el id *vigente* de
    # la Página «WiFi Monitor» (el viejo 1413800131809489 redirige aquí). El nombre
    # corto facebook.com/wifimonitorapp NO existe («contenido no disponible»), así
    # que aquí va la URL por id, que funciona siempre. Si algún día se le pone
    # nombre de usuario a la Página, se puede cambiar por el bonito.
    ("Facebook", "https://www.facebook.com/profile.php?id=61594515976679"),
    ("YouTube", "https://www.youtube.com/@wifimonitorapp"),
]
URLS = [u for _, u in REDES]

# «También en», por idioma (informar, no pedir que te sigan)
ETIQUETA = {
    "index.html": "También en:",
    "en/index.html": "Also on:",
    "pt/index.html": "Também em:",
    "fr/index.html": "Aussi sur :",
    "de/index.html": "Auch auf:",
    "it/index.html": "Anche su:",
}

fallos = 0

for ruta, etiqueta in ETIQUETA.items():
    f = RAIZ / ruta
    if not f.exists():
        print(f"FALLO  {ruta}: no existe")
        fallos += 1
        continue
    txt = f.read_text(encoding="utf-8")
    orig = txt

    # --- 1. el enlace del pie, una sola vez -------------------------------
    if 'class="redes"' in txt:
        print(f"ya     {ruta}: el pie ya tenía las redes")
    else:
        fila = (f'    <p class="redes">{etiqueta} ' +
                " · ".join(f'<a href="{u}" rel="me" target="_blank">{n}</a>' for n, u in REDES) +
                "</p>\n")
        # se inserta al final del contenedor del pie, antes de cerrarlo
        patron = re.compile(r"(\n\s*</div>\s*\n</footer>)")
        if not patron.search(txt):
            print(f"FALLO  {ruta}: no encuentro el cierre del pie")
            fallos += 1
            continue
        txt = patron.sub("\n" + fila + r"\1", txt, count=1)
        print(f"OK     {ruta}: enlaces añadidos al pie")

    # --- 2. sameAs dentro del JSON-LD -------------------------------------
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', txt, re.S)
    if not m:
        print(f"FALLO  {ruta}: no encuentro el bloque de datos estructurados")
        fallos += 1
        continue
    bloque = m.group(1)
    if '"sameAs"' in bloque:
        print(f"ya     {ruta}: sameAs ya estaba")
    else:
        lista = ",".join(f'"{u}"' for u in URLS)
        nuevo = re.sub(r'("url"\s*:\s*"[^"]*",)',
                       lambda mm: mm.group(1) + f'\n  "sameAs":[{lista}],',
                       bloque, count=1)
        if nuevo == bloque:
            print(f"FALLO  {ruta}: no encuentro dónde insertar sameAs")
            fallos += 1
            continue
        txt = txt[:m.start(1)] + nuevo + txt[m.end(1):]
        print(f"OK     {ruta}: sameAs añadido")

    if txt != orig:
        f.write_text(txt, encoding="utf-8")

    # --- 3. revalidar el JSON-LD de lo que acabamos de escribir -----------
    comp = (RAIZ / ruta).read_text(encoding="utf-8")
    m2 = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', comp, re.S)
    try:
        datos = json.loads(m2.group(1))
        print(f"       JSON válido · sameAs → {datos.get('sameAs')}")
    except Exception as e:  # noqa: BLE001
        print(f"FALLO  {ruta}: el JSON-LD quedó inválido: {e}")
        fallos += 1

print()
print("FALLOS:", fallos)
raise SystemExit(1 if fallos else 0)
