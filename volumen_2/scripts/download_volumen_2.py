#!/usr/bin/env python3
"""
Script de descarga y procesamiento para el Volumen 2 de 'Lasers y Dragones'
Campaña: Starfinder - Dead Suns (Episodios 11 al 20)
Descarga los audios oficiales de Libsyn, extrae los subtítulos VTT de YouTube y
genera las transcripciones limpias listas para la novelización.
"""

import os
import sys
import json
import subprocess
import urllib.request
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
RAW_DIR = os.path.join(BASE_DIR, "transcripciones", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "transcripciones", "limpias")
META_DIR = os.path.join(BASE_DIR, "metadatos")

CLEANER_SCRIPT = os.path.join(
    os.path.dirname(BASE_DIR),
    ".agents", "skills", "novelizacion-lasers-y-dragones", "scripts", "limpiar_transcripcion.py"
)

EPISODIOS_VOLUMEN_2 = [
    {
        "numero": 11,
        "titulo": "Episodio 11 - Desayuno para Llevar",
        "youtube_id": "LnAF2e4mzM0",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-11-desayuno-para-llevar",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio011.mp3",
        "archivo_audio": "LasersYDragonesEpisodio011.mp3",
        "sinopsis": "Primer desayuno tranquilo interrumpido por los Protectores; dilema entre huir o afrontar la ley."
    },
    {
        "numero": 12,
        "titulo": "Episodio 12 - Regreso a Clases",
        "youtube_id": "sQ5Ca3WnnBk",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-12-regreso-a-clases",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio012.mp3",
        "archivo_audio": "LasersYDragonesEpisodio012.mp3",
        "sinopsis": "Asesoría legal, nuevos recursos y primeros pasos hacia la gran institución del saber."
    },
    {
        "numero": 13,
        "titulo": "Episodio 13 - Arcanatástico!",
        "youtube_id": "I4EBWgPDUS8",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-12-arcanatstico",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio013.mp3",
        "archivo_audio": "LasersYDragonesEpisodio013.mp3",
        "sinopsis": "Infiltración e investigación en el Arcanamirium sobre secretos tecnomágicos de la Brecha."
    },
    {
        "numero": 14,
        "titulo": "Episodio 14 - Propuestas de la Cripta",
        "youtube_id": "yKmENAexQAU",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-14-propuestas-de-la-cripta",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio014.mp3",
        "archivo_audio": "LasersYDragonesEpisodio014.mp3",
        "sinopsis": "Audiencia con el Embajador de Eox y su asistente en la tétrica embajada ósea."
    },
    {
        "numero": 15,
        "titulo": "Episodio 15 - Carnitas Corporativas",
        "youtube_id": "t5iyFIGGnyU",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-15-carnitas-corporativas",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio015.mp3",
        "archivo_audio": "LasersYDragonesEpisodio015.mp3",
        "sinopsis": "Benrey visita a su familia ysoki, recupera su motoneta vespacial y recibe llamadas amenazantes."
    },
    {
        "numero": 16,
        "titulo": "Episodio 16 - El Caballito de Mar",
        "youtube_id": "VfkDJE79aww",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-16-el-caballito-de-mar",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio016.mp3",
        "archivo_audio": "LasersYDragonesEpisodio016.mp3",
        "sinopsis": "Negociaciones con el Colectivo Hardscrabble para asegurar la nave exploradora Hippocampus."
    },
    {
        "numero": 17,
        "titulo": "Episodio 17 - Insinuación Mortal",
        "youtube_id": "usCxwc2UcyU",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-17-insinuacin-mortal",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio017.mp3",
        "archivo_audio": "LasersYDragonesEpisodio017.mp3",
        "sinopsis": "Aprovisionamiento final, calibración de armas y despegue de la estación Absalón rumbo al Acreon."
    },
    {
        "numero": 18,
        "titulo": "Episodio 18 - Aka-Ta el Acreón",
        "youtube_id": "K0S1X8Z63o8",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-018-aka-ta-el-acren",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio018.mp3",
        "archivo_audio": "LasersYDragonesEpisodio018.mp3",
        "sinopsis": "Llegada al pecio fantasma del Acreon en el vacío y primer combate letal contra los Akata."
    },
    {
        "numero": 19,
        "titulo": "Episodio 19 - Hasta la Cocina",
        "youtube_id": "FO_qCT74dDc",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-019-hasta-la-cocina",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio019.mp3",
        "archivo_audio": "LasersYDragonesEpisodio019.mp3",
        "sinopsis": "Exploración de las cubiertas superiores del Acreon y descubrimiento de los restos de la tripulación."
    },
    {
        "numero": 20,
        "titulo": "Episodio 20 - Amigoblins del Espacio",
        "youtube_id": "RqEP45tICIA",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-020-amigoblins-del-espacio",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio020.mp3",
        "archivo_audio": "LasersYDragonesEpisodio020.mp3",
        "sinopsis": "Encuentro caótico con una tribu de goblins espaciales atrincherados en los conductos de carga."
    }
]

def descargar_audios():
    print("=== DESCARGANDO AUDIOS DE LIBSYN (VOLUMEN 2) ===")
    os.makedirs(AUDIOS_DIR, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    
    for ep in EPISODIOS_VOLUMEN_2:
        out_file = os.path.join(AUDIOS_DIR, ep["archivo_audio"])
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000000:
            size_mb = os.path.getsize(out_file) / (1024 * 1024)
            print(f"  [Existente] {ep['archivo_audio']} ({size_mb:.1f} MB)")
            continue
            
        print(f"  Descargando: {ep['archivo_audio']} ...")
        try:
            req = urllib.request.Request(ep["url_audio"], headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp, open(out_file, "wb") as out:
                while True:
                    chunk = resp.read(1024 * 256)
                    if not chunk:
                        break
                    out.write(chunk)
            size_mb = os.path.getsize(out_file) / (1024 * 1024)
            print(f"    ✓ Completado ({size_mb:.1f} MB)")
        except Exception as e:
            print(f"    ✗ Error al descargar {ep['url_audio']}: {e}")

def descargar_subtitulos():
    print("\n=== DESCARGANDO SUBTÍTULOS VTT DE YOUTUBE ===")
    os.makedirs(RAW_DIR, exist_ok=True)
    
    for ep in EPISODIOS_VOLUMEN_2:
        num = ep["numero"]
        vid = ep["youtube_id"]
        vtt_target = os.path.join(RAW_DIR, f"episodio_{num:02d}.es.vtt")
        
        if os.path.exists(vtt_target) and os.path.getsize(vtt_target) > 5000:
            print(f"  [Existente] episodio_{num:02d}.es.vtt")
            continue
            
        print(f"  Descargando subtítulos: Ep {num:02d} ({vid}) ...")
        out_tmpl = os.path.join(RAW_DIR, f"episodio_{num:02d}.%(ext)s")
        cmd = [
            "yt-dlp",
            "--no-warnings",
            "--skip-download",
            "--write-auto-sub",
            "--sub-lang", "es",
            "-o", out_tmpl,
            f"https://www.youtube.com/watch?v={vid}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"    ✓ Subtítulos guardados")
        else:
            print(f"    ✗ Error: {res.stderr.strip()[:100]}")

def limpiar_transcripciones():
    print("\n=== LIMPIANDO Y DEDUPLICANDO TRANSCRIPCIONES ===")
    os.makedirs(CLEAN_DIR, exist_ok=True)
    
    for ep in EPISODIOS_VOLUMEN_2:
        num = ep["numero"]
        raw_file = os.path.join(RAW_DIR, f"episodio_{num:02d}.es.vtt")
        clean_file = os.path.join(CLEAN_DIR, f"episodio_{num:02d}.txt")
        
        if not os.path.exists(raw_file):
            print(f"  [Aviso] Falta archivo raw para Ep {num:02d}")
            continue
            
        print(f"  Procesando Ep {num:02d}...")
        cmd = ["python3", CLEANER_SCRIPT, raw_file, clean_file]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"    ✓ {res.stdout.strip()}")
        else:
            print(f"    ✗ Error al limpiar: {res.stderr}")

def guardar_metadatos():
    print("\n=== GUARDANDO METADATOS DE VOLUMEN 2 ===")
    os.makedirs(META_DIR, exist_ok=True)
    meta_path = os.path.join(META_DIR, "episodios_volumen_2.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(EPISODIOS_VOLUMEN_2, f, indent=2, ensure_ascii=False)
    print(f"  Metadatos guardados en: {meta_path}")

if __name__ == "__main__":
    guardar_metadatos()
    descargar_subtitulos()
    limpiar_transcripciones()
    descargar_audios()
    print("\n¡Todo el lote de Episodios 11 al 20 ha sido procesado con éxito para el Volumen 2!")
