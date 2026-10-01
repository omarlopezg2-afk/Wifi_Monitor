#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Añade la ventaja del navegador a la landing y quita una afirmación falsa.

1. NUEVA PREGUNTA (6 idiomas): si al PC le falta el complemento de las ventanas
   (WebView2), la app no se queda en blanco: avisa y se abre en el navegador con
   las mismas funciones. Verificado el 1-oct-2026 sobre la copia de la Store.

2. CORRECCIÓN (en, pt, fr, it): la respuesta sobre recursos decía «se ejecuta en
   segundo plano». Es FALSO —la app no corre de fondo, y la pregunta siguiente
   dice justo lo contrario— y es la frase prohibida por la regla de promesas.
   Se quita la parte falsa y se deja lo que sí es cierto: el escaneo es liviano.
   (Español y alemán ya estaban bien.)
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

# --- 1. la afirmación falsa del "segundo plano" (solo donde está) -------------
FALSAS = {
    "en/index.html": (
        "No. It runs in the background and the device scan is lightweight.",
        "No. The device scan is lightweight.",
    ),
    "pt/index.html": (
        "Não. Ele roda em segundo plano e o escaneamento de dispositivos é leve.",
        "Não. O escaneamento de dispositivos é leve.",
    ),
    "fr/index.html": (
        "Non. Elle tourne en arrière-plan et l'analyse des appareils est légère.",
        "Non. L'analyse des appareils est légère.",
    ),
    "it/index.html": (
        "No. Funziona in background e la scansione dei dispositivi è leggera.",
        "No. La scansione dei dispositivi è leggera.",
    ),
}

# --- 2. la pregunta nueva, insertada tras la de recursos ----------------------
RECURSOS = {
    "index.html": "¿Consume muchos recursos del PC?",
    "en/index.html": "Does it use a lot of PC resources?",
    "pt/index.html": "Consome muitos recursos do PC?",
    "fr/index.html": "Est-ce qu'elle consomme beaucoup de ressources du PC ?",
    "de/index.html": "Braucht sie viele PC-Ressourcen?",
    "it/index.html": "Consuma molte risorse del PC?",
}

NUEVA = {
    "index.html": '<details><summary>¿Y si mi PC es viejo o le falta algún complemento de Windows?</summary><p>Funciona igual. La ventana la dibuja un complemento de Microsoft (WebView2); si tu equipo no lo tiene —pasa en Windows antiguos o recién instalados—, la app no se queda en blanco: te avisa y se abre sola en tu navegador, con las mismas funciones. Si luego instalas el complemento, vuelve a su propia ventana.</p></details>',
    "en/index.html": '<details><summary>What if my PC is old or missing a Windows component?</summary><p>It works anyway. The window is drawn by a Microsoft component (WebView2); if your computer doesn\'t have it —common on older or freshly installed Windows—, the app doesn\'t go blank: it tells you and opens by itself in your browser, with the same features. Install the component later and it goes back to its own window.</p></details>',
    "pt/index.html": '<details><summary>E se meu PC for antigo ou faltar algum componente do Windows?</summary><p>Funciona igual. A janela é desenhada por um componente da Microsoft (WebView2); se o seu computador não o tiver —acontece em Windows antigos ou recém-instalados—, o app não fica em branco: avisa você e abre sozinho no seu navegador, com as mesmas funções. Se depois instalar o componente, volta para a própria janela.</p></details>',
    "fr/index.html": '<details><summary>Et si mon PC est ancien ou qu\'il manque un composant Windows ?</summary><p>Elle fonctionne quand même. La fenêtre est dessinée par un composant Microsoft (WebView2) ; si votre ordinateur ne l\'a pas —c\'est courant sur les Windows anciens ou fraîchement installés—, l\'application ne reste pas blanche : elle vous prévient et s\'ouvre toute seule dans votre navigateur, avec les mêmes fonctions. Si vous installez le composant plus tard, elle retrouve sa propre fenêtre.</p></details>',
    "de/index.html": '<details><summary>Und wenn mein PC alt ist oder eine Windows-Komponente fehlt?</summary><p>Sie funktioniert trotzdem. Das Fenster zeichnet eine Microsoft-Komponente (WebView2); fehlt sie auf deinem Rechner —das passiert bei alten oder frisch installierten Windows-Versionen—, bleibt die App nicht weiß: sie sagt es dir und öffnet sich von selbst in deinem Browser, mit denselben Funktionen. Installierst du die Komponente später, kehrt sie in ihr eigenes Fenster zurück.</p></details>',
    "it/index.html": '<details><summary>E se il mio PC è vecchio o manca un componente di Windows?</summary><p>Funziona lo stesso. La finestra la disegna un componente Microsoft (WebView2); se il tuo computer non ce l\'ha —succede con Windows vecchi o appena installati—, l\'app non resta bianca: ti avvisa e si apre da sola nel tuo browser, con le stesse funzioni. Se poi installi il componente, torna nella sua finestra.</p></details>',
}

# --- 3. el distintivo del hero: fuera «tiempo real» (6 idiomas) ---------------
# Es una de las tres palabras prohibidas por la regla de promesas, y además es
# falso: la app escanea cuando la usas, no de forma continua. El sustituto dice
# lo que la app hace de verdad.
DISTINTIVO = {
    "index.html": ("Monitoreo en tiempo real", "Detección de dispositivos"),
    "en/index.html": ("Real-time monitoring", "Device detection"),
    "pt/index.html": ("Monitoramento em tempo real", "Detecção de dispositivos"),
    "fr/index.html": ("Surveillance en temps réel", "Détection des appareils"),
    "de/index.html": ("Überwachung in Echtzeit", "Geräteerkennung"),
    "it/index.html": ("Monitoraggio in tempo reale", "Rilevamento dei dispositivi"),
}

fallos = 0

for ruta, (viejo, nuevo) in DISTINTIVO.items():
    f = RAIZ / ruta
    txt = f.read_text(encoding="utf-8")
    if viejo not in txt:
        print(f"AVISO  {ruta}: no encuentro el distintivo «{viejo}»")
        continue
    f.write_text(txt.replace(viejo, nuevo, 1), encoding="utf-8")
    print(f"OK     {ruta}: distintivo -> «{nuevo}»")

for ruta, (viejo, nuevo) in FALSAS.items():
    f = RAIZ / ruta
    txt = f.read_text(encoding="utf-8")
    if viejo not in txt:
        print(f"AVISO  {ruta}: no encuentro la frase del «segundo plano» (¿ya corregida?)")
        continue
    f.write_text(txt.replace(viejo, nuevo, 1), encoding="utf-8")
    print(f"OK     {ruta}: quitada la afirmación de «segundo plano»")

for ruta, pregunta in RECURSOS.items():
    f = RAIZ / ruta
    txt = f.read_text(encoding="utf-8")
    # se inserta la pregunta nueva justo después del bloque de recursos
    marca = None
    for linea in txt.splitlines():
        if pregunta in linea and linea.strip().startswith("<details>"):
            marca = linea
            break
    if marca is None:
        print(f"FALLO  {ruta}: no encuentro el bloque de recursos")
        fallos += 1
        continue
    if NUEVA[ruta][:40] in txt:
        print(f"AVISO  {ruta}: la pregunta nueva ya estaba")
        continue
    txt = txt.replace(marca, marca + "\n    " + NUEVA[ruta], 1)
    f.write_text(txt, encoding="utf-8")
    print(f"OK     {ruta}: añadida la pregunta de la ventaja")

print()
print("FALLOS:", fallos)
sys.exit(1 if fallos else 0)
