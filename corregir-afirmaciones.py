#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige en la landing las afirmaciones que la app no cumple.

1. «cada aparato con su consumo y su historial» -> la app muestra fabricante, IP y MAC.
   El consumo y el historial son de la CONEXION (el PC), no de cada aparato.
2. La tarjeta de Historial dice solo «7 días de tráfico»: se aclara que es el tráfico del PC.
3. Meta descripcion, og:description y datos estructurados: mismo matiz.
4. Los nodos del radar llevaban dBm por aparato: la app mide la señal de TU conexion,
   no la de cada dispositivo, asi que se quitan.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

# --- 1. parrafo «la lista del modem»: consumo/historial por aparato -> IP y MAC ---
PARRAFO = {
    "index.html": (
        "Aquí cada aparato sale con su fabricante, su consumo y su historial —",
        "Aquí cada aparato sale con su fabricante, su IP y su MAC —",
    ),
    "en/index.html": (
        "Here every device shows up with its manufacturer, its usage and its history —",
        "Here every device shows up with its manufacturer, its IP and its MAC —",
    ),
    "pt/index.html": (
        "Aqui cada aparelho aparece com o fabricante, o consumo e o histórico —",
        "Aqui cada aparelho aparece com o fabricante, o IP e o MAC —",
    ),
    "fr/index.html": (
        "Ici, chaque appareil apparaît avec son fabricant, sa consommation et son historique —",
        "Ici, chaque appareil apparaît avec son fabricant, son IP et son MAC —",
    ),
    "de/index.html": (
        "Hier erscheint jedes Gerät mit Hersteller, Verbrauch und Verlauf —",
        "Hier erscheint jedes Gerät mit Hersteller, IP und MAC —",
    ),
    "it/index.html": (
        "Qui ogni dispositivo compare con il suo produttore, il suo consumo e la sua cronologia —",
        "Qui ogni dispositivo compare con il suo produttore, l'IP e il MAC —",
    ),
}

# --- 2. tarjeta de Historial: dejar claro que el trafico es el de tu PC ---
TARJETA = {
    "index.html": (
        "<h3>7 días de tráfico</h3><p>Guarda el tráfico enviado y recibido de los últimos siete días para que notes patrones, no solo el momento actual.</p>",
        "<h3>7 días de tu conexión</h3><p>Guarda el tráfico que sube y baja por tu PC en los últimos siete días, junto con la red y la señal de cada medición, para que notes patrones y no solo el momento actual.</p>",
    ),
    "en/index.html": (
        "<h3>7 days of traffic</h3><p>Keeps the sent and received traffic of the last seven days so you can spot patterns, not just the current moment.</p>",
        "<h3>7 days of your connection</h3><p>Keeps the traffic your PC sends and receives over the last seven days, along with the network and signal of each measurement, so you can spot patterns, not just the current moment.</p>",
    ),
    "pt/index.html": (
        "<h3>7 dias de tráfego</h3><p>Guarda o tráfego enviado e recebido dos últimos sete dias para você perceber padrões, não só o momento atual.</p>",
        "<h3>7 dias da sua conexão</h3><p>Guarda o tráfego que sobe e desce pelo seu PC nos últimos sete dias, junto com a rede e o sinal de cada medição, para você perceber padrões e não só o momento atual.</p>",
    ),
    "fr/index.html": (
        "<h3>7 jours de trafic</h3><p>Conserve le trafic envoyé et reçu des sept derniers jours pour repérer des tendances, pas seulement l'instant présent.</p>",
        "<h3>7 jours de votre connexion</h3><p>Conserve le trafic envoyé et reçu par votre PC sur les sept derniers jours, avec le réseau et le signal de chaque mesure, pour repérer des tendances, pas seulement l'instant présent.</p>",
    ),
    "de/index.html": (
        "<h3>7 Tage Datenverkehr</h3><p>Speichert den gesendeten und empfangenen Datenverkehr der letzten sieben Tage, damit du Muster erkennst, nicht nur den aktuellen Moment.</p>",
        "<h3>7 Tage deiner Verbindung</h3><p>Speichert den Datenverkehr, den dein PC in den letzten sieben Tagen sendet und empfängt, zusammen mit Netzwerk und Signal jeder Messung, damit du Muster erkennst, nicht nur den aktuellen Moment.</p>",
    ),
    "it/index.html": (
        "<h3>7 giorni di traffico</h3><p>Conserva il traffico inviato e ricevuto degli ultimi sette giorni per notare gli schemi, non solo il momento attuale.</p>",
        "<h3>7 giorni della tua connessione</h3><p>Conserva il traffico inviato e ricevuto dal tuo PC negli ultimi sette giorni, insieme alla rete e al segnale di ogni misurazione, per notare gli schemi e non solo il momento attuale.</p>",
    ),
}

# --- 3. meta descripcion, og y datos estructurados ---
METAS = {
    "index.html": [
        ("guarda 7 días de tráfico,", "guarda 7 días del tráfico de tu conexión,"),
        ("Dispositivos conectados con fabricante, 7 días de tráfico,", "Dispositivos conectados con fabricante, 7 días del tráfico de tu conexión,"),
        ("guarda 7 días de historial de tráfico,", "guarda 7 días del tráfico de tu conexión,"),
    ],
    "en/index.html": [
        ("keeps 7 days of traffic history,", "keeps 7 days of your connection's traffic history,"),
        ("Connected devices with manufacturer, 7 days of traffic,", "Connected devices with manufacturer, 7 days of your connection's traffic,"),
    ],
    "pt/index.html": [
        ("guarda 7 dias de tráfego,", "guarda 7 dias do tráfego da sua conexão,"),
        ("Dispositivos conectados com fabricante, 7 dias de tráfego,", "Dispositivos conectados com fabricante, 7 dias do tráfego da sua conexão,"),
        ("guarda 7 dias de histórico de tráfego,", "guarda 7 dias do tráfego da sua conexão,"),
    ],
    "fr/index.html": [
        ("conserve 7 jours de trafic,", "conserve 7 jours du trafic de votre connexion,"),
        ("Appareils connectés avec fabricant, 7 jours de trafic,", "Appareils connectés avec fabricant, 7 jours du trafic de votre connexion,"),
        ("conserve 7 jours d'historique de trafic,", "conserve 7 jours du trafic de votre connexion,"),
    ],
    "de/index.html": [
        ("speichert 7 Tage Datenverkehr,", "speichert 7 Tage Datenverkehr deiner Verbindung,"),
        ("Verbundene Geräte mit Hersteller, 7 Tage Datenverkehr,", "Verbundene Geräte mit Hersteller, 7 Tage Datenverkehr deiner Verbindung,"),
    ],
    "it/index.html": [
        ("conserva 7 giorni di traffico,", "conserva 7 giorni del traffico della tua connessione,"),
        ("Dispositivi connessi con produttore, 7 giorni di traffico,", "Dispositivi connessi con produttore, 7 giorni del traffico della tua connessione,"),
        ("conserva 7 giorni di cronologia del traffico,", "conserva 7 giorni del traffico della tua connessione,"),
    ],
}

errores = []
informe = []

for archivo in PARRAFO:
    ruta = RAIZ / archivo
    texto = ruta.read_text(encoding="utf-8")
    original = texto

    # 1. parrafo
    viejo, nuevo = PARRAFO[archivo]
    if viejo not in texto:
        errores.append(f"{archivo}: no encontrado el parrafo «{viejo[:60]}…»")
    else:
        texto = texto.replace(viejo, nuevo)
        informe.append(f"{archivo}: parrafo «consumo e historial por aparato» -> IP y MAC")

    # 2. tarjeta de historial
    viejo, nuevo = TARJETA[archivo]
    if viejo not in texto:
        errores.append(f"{archivo}: no encontrada la tarjeta de historial")
    else:
        texto = texto.replace(viejo, nuevo)
        informe.append(f"{archivo}: tarjeta de historial aclarada (trafico de tu PC)")

    # 3. metas
    for viejo, nuevo in METAS[archivo]:
        if viejo not in texto:
            errores.append(f"{archivo}: no encontrado «{viejo[:60]}…»")
            continue
        texto = texto.replace(viejo, nuevo)
        informe.append(f"{archivo}: meta/datos estructurados «{viejo[:40]}…»")

    # 4. dBm por aparato en el radar
    texto, n = re.subn(r" · -\d+dBm", "", texto)
    if n:
        informe.append(f"{archivo}: quitados {n} dBm por aparato del radar")

    if texto != original:
        ruta.write_text(texto, encoding="utf-8")

print("=== CAMBIOS APLICADOS ===")
for linea in informe:
    print("  " + linea)

if errores:
    print("\n=== NO ENCONTRADO (revisar) ===")
    for e in errores:
        print("  " + e)
    sys.exit(1)

print("\nOK: todo aplicado sin incidencias")
