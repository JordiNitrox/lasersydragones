#!/usr/bin/env python3
"""
Script de descarga y procesamiento para la tanda de 50 episodios (73 al 122)
de 'Lasers y Dragones' (Campaña Starfinder: Dead Suns).

Extrae metadatos oficiales de Libsyn y YouTube, descarga subtítulos automáticos en VTT
y genera las transcripciones limpias deduplicadas para la planificación de los
Volúmenes 7, 8, 9 y siguientes.
"""

import os
import sys
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
META_DIR = os.path.join(BASE_DIR, "metadatos")
RAW_DIR = os.path.join(BASE_DIR, "transcripciones", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "transcripciones", "limpias")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

CLEANER_SCRIPT = os.path.join(
    PROJECT_ROOT,
    ".agents", "skills", "novelizacion-lasers-y-dragones", "scripts", "limpiar_transcripcion.py"
)

# Mapeo narrativo de correspondencia con Starfinder Dead Suns Adventure Path
def clasificar_episodio(num):
    if 73 <= num <= 75:
        return {
            "libro_starfinder": "Especial de Halloween / Meta-Rol en Viejo Golarion (Pathfinder 2e)",
            "parte_aventura": "Simulación Virtual de Rol en Estación Ábsalon ('Spooky Octubre')",
            "volumen_propuesto": "Volumen Especial Extra (Spooky Octubre)",
            "arco": "Spooky Octubre: Pesadilla en el Viejo Golarion"
        }
    elif num == 76:
        return {
            "libro_starfinder": "Bisagra: Fin Especial Spooky Octubre / Despertar en Ábsalon",
            "parte_aventura": "Victoria virtual contra Damien / Despertar en Ábsalon y Asalto Armado de Gnolls del Culto",
            "volumen_propuesto": "Volumen Especial Extra / Volumen 7 (Bisagra)",
            "arco": "Despertar de la Emboscada y Visión Cósmica"
        }
    elif 77 <= num <= 78:
        return {
            "libro_starfinder": "Transición entre Libro 2 y Libro 3",
            "parte_aventura": "Interrogatorio a Null-9, Conspiración y Salto al Drift",
            "volumen_propuesto": "Volumen 7",
            "arco": "Preparativos y Rumbo a la Diáspora"
        }
    elif 79 <= num <= 86:
        return {
            "libro_starfinder": "Dead Suns Libro 3: Splintered Worlds (Mundos Fragmentados)",
            "parte_aventura": "Parte 1: La Diáspora (Cinturón de Asteroides y Base Sarcesiana del Culto del Devorador)",
            "volumen_propuesto": "Volumen 7",
            "arco": "La Diáspora de Asteroides y el Templo del Devorador"
        }
    elif 87 <= num <= 90:
        return {
            "libro_starfinder": "Dead Suns Libro 3: Splintered Worlds (Mundos Fragmentados)",
            "parte_aventura": "Transición: Batalla contra la Flota de los Cuerpos, Memorias de Axel y Rumbo a Eox",
            "volumen_propuesto": "Volumen 7 / Volumen 8 (Bisagra)",
            "arco": "Flota de los Cuerpos y Fantasmas del Pasado"
        }
    elif 91 <= num <= 97:
        return {
            "libro_starfinder": "Dead Suns Libro 3: Splintered Worlds (Mundos Fragmentados)",
            "parte_aventura": "Parte 2A: Eox (El Planeta de los Muertos, Sabios Óseos, Asesinos Nihili y Café Calavera)",
            "volumen_propuesto": "Volumen 8",
            "arco": "Llegada a Eox y Trámites con los No-Muertos"
        }
    elif 98 <= num <= 105:
        return {
            "libro_starfinder": "Dead Suns Libro 3: Splintered Worlds (Mundos Fragmentados)",
            "parte_aventura": "Parte 2B: El Reality Show Mortal de Zo! (Coliseo, Golem de Neutrones, El Camino Furibundo)",
            "volumen_propuesto": "Volumen 8",
            "arco": "El Show Macabro de Zo!"
        }
    elif 106 <= num <= 110:
        return {
            "libro_starfinder": "Dead Suns Libro 3: Splintered Worlds (Mundos Fragmentados)",
            "parte_aventura": "Parte 2C: Asalto a la Necrogarganta, Guardián Ellicoth, Derrota de Xerantha Zatus y Huida",
            "volumen_propuesto": "Volumen 8",
            "arco": "La Caída de Xerantha Zatus (Clímax Libro 3)"
        }
    elif 111 <= num <= 113:
        return {
            "libro_starfinder": "Arco Canónico Propio de la Mesa: Inversiones Estelares S.C.",
            "parte_aventura": "Aparición de Marcelus en Persona, Revelación Corporativa y Destino Apostae",
            "volumen_propuesto": "Volumen 9",
            "arco": "El Rostro de Marcelus"
        }
    elif 114 <= num <= 120:
        return {
            "libro_starfinder": "Arco Canónico Propio de la Mesa: La Casa Istrav en Apostae",
            "parte_aventura": "Infiltración en la Fortaleza Drow, Secretos de la Madre de Triel, Keiden Ashton y Combate contra Jhidel",
            "volumen_propuesto": "Volumen 9",
            "arco": "La Sombra de la Casa Istrav y Duelo Fratricida"
        }
    elif 121 <= num <= 122:
        return {
            "libro_starfinder": "Arco Canónico Propio de la Mesa: Epílogo de Apostae y Reanudación",
            "parte_aventura": "Huida de Apostae, Secuelas del Duelo de Triel y el Valor de Axel",
            "volumen_propuesto": "Volumen 9",
            "arco": "Epílogo en Thanox y Secuelas"
        }
    else:
        return {
            "libro_starfinder": "Dead Suns Libro 4: The Ruined Clouds (Las Nubes Arruinadas)",
            "parte_aventura": "El Casino Espacial, Rally de la Muerte y Rumbo a Nejeor / Istamak",
            "volumen_propuesto": "Volumen 10",
            "arco": "Transición hacia Nejeor"
        }

def extraer_metadatos():
    print(">>> 1. Descargando feed RSS de Libsyn...")
    rss_url = "https://rss.libsyn.com/shows/241133/destinations/1801772.xml"
    req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req) as resp:
        tree = ET.parse(resp)
    items = tree.getroot().find("channel").findall("item")

    print(">>> 2. Consultando lista de videos del canal de YouTube de 'Lasers y Dragones'...")
    yt_cmd = [
        "yt-dlp", "--no-update", "--flat-playlist", "-J",
        "https://www.youtube.com/channel/UCPZQdWughRVDyd3LNFkIExw/videos"
    ]
    res = subprocess.run(yt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error consultando YouTube: {res.stderr}")
        sys.exit(1)

    yt_data = json.loads(res.stdout)
    yt_map = {}
    for entry in yt_data.get("entries", []):
        t = entry.get("title", "")
        m = re.search(r"(?:Episodio|Episode)\s+0*(\d+)", t, re.IGNORECASE)
        if m:
            yt_map[int(m.group(1))] = entry

    print(">>> 3. Estructurando metadatos de los 50 episodios (73 al 122)...")
    episodes = []
    for it in items:
        title = it.findtext("title") or ""
        m = re.search(r"Episodio\s+0*(\d+)", title, re.IGNORECASE)
        if m:
            num = int(m.group(1))
            if 73 <= num <= 122:
                enclosure = it.find("enclosure")
                audio_url = enclosure.get("url") if enclosure is not None else ""
                link = it.findtext("link") or ""
                desc = it.findtext("description") or ""
                
                # Limpiar texto de sinopsis (remover HTML y redes sociales estándar)
                clean_desc = re.sub(r"<[^>]+>", " ", desc)
                clean_desc = clean_desc.split("Instagram:")[0].split("Facebook:")[0].split("En Twitter")[0].strip()
                pub_date = it.findtext("pubDate") or ""
                
                yt_info = yt_map.get(num, {})
                yt_id = yt_info.get("id", "")
                
                clasif = clasificar_episodio(num)
                
                episodes.append({
                    "numero": num,
                    "titulo": title.strip(),
                    "youtube_id": yt_id,
                    "youtube_url": f"https://www.youtube.com/watch?v={yt_id}" if yt_id else "",
                    "url_pagina": link.strip(),
                    "url_audio": audio_url.strip(),
                    "archivo_audio": f"LasersYDragonesEpisodio{num:03d}.mp3",
                    "fecha_publicacion": pub_date.strip(),
                    "libro_starfinder": clasif["libro_starfinder"],
                    "parte_aventura": clasif["parte_aventura"],
                    "volumen_propuesto": clasif["volumen_propuesto"],
                    "arco_narrativo": clasif["arco"],
                    "sinopsis": clean_desc
                })

    episodes.sort(key=lambda x: x["numero"])
    
    os.makedirs(META_DIR, exist_ok=True)
    meta_path = os.path.join(META_DIR, "episodios_73_122.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(episodes, f, indent=2, ensure_ascii=False)
        
    print(f"  ✓ Metadatos guardados con éxito ({len(episodes)} episodios) en:\n    {meta_path}")
    return episodes

def descargar_subtitulo(ep):
    num = ep["numero"]
    yt_id = ep["youtube_id"]
    if not yt_id:
        return num, False, "No YouTube ID"

    out_pattern = os.path.join(RAW_DIR, f"episodio_{num:02d}.%(ext)s")
    target_vtt = os.path.join(RAW_DIR, f"episodio_{num:02d}.es.vtt")

    if os.path.exists(target_vtt):
        return num, True, "Ya existía"

    cmd = [
        "yt-dlp",
        "--no-update",
        "--write-auto-sub",
        "--sub-lang", "es",
        "--skip-download",
        "--no-warnings",
        "-o", out_pattern,
        f"https://www.youtube.com/watch?v={yt_id}"
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if os.path.exists(target_vtt):
        return num, True, "Descargado"
    else:
        return num, False, res.stderr[:100]

def descargar_todos_subtitulos(episodes):
    print(f"\n>>> 4. Descargando subtítulos automáticos VTT ({len(episodes)} episodios en paralelo)...")
    os.makedirs(RAW_DIR, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(descargar_subtitulo, ep): ep for ep in episodes}
        for future in as_completed(futures):
            ep = futures[future]
            num, ok, msg = future.result()
            estado = "✓" if ok else "✗"
            print(f"  [{estado}] Ep {num:03d} ({ep['titulo'][:35]}...): {msg}")

def limpiar_transcripciones(episodes):
    print(f"\n>>> 5. Limpiando y deduplicando transcripciones a texto corrido...")
    os.makedirs(CLEAN_DIR, exist_ok=True)

    sys.path.insert(0, os.path.dirname(CLEANER_SCRIPT))
    from limpiar_transcripcion import limpiar_vtt

    exitos = 0
    total_palabras = 0

    for ep in episodes:
        num = ep["numero"]
        vtt_file = os.path.join(RAW_DIR, f"episodio_{num:02d}.es.vtt")
        clean_file = os.path.join(CLEAN_DIR, f"episodio_{num:02d}.txt")

        if not os.path.exists(vtt_file):
            print(f"  [Aviso] No se encontró VTT para Ep {num}")
            continue

        limpiar_vtt(vtt_file, clean_file)
        if os.path.exists(clean_file):
            with open(clean_file, "r", encoding="utf-8") as f:
                content = f.read()
            palabras = len(content.split())
            total_palabras += palabras
            exitos += 1
            print(f"  ✓ Ep {num:03d}: {os.path.basename(clean_file)} ({palabras:,} palabras)")

    print(f"\n>>> Proceso concluido: {exitos}/{len(episodes)} transcripciones limpias ({total_palabras:,} palabras en total).")

def main():
    print("================================================================================")
    print("PROCESAMIENTO Y PLANIFICACIÓN DE EPISODIOS 73 AL 122 - LASERS Y DRAGONES")
    print("================================================================================")
    episodes = extraer_metadatos()
    descargar_todos_subtitulos(episodes)
    limpiar_transcripciones(episodes)
    print("================================================================================")
    print("¡DESCARGA Y PROCESAMIENTO COMPLETADOS CON ÉXITO!")
    print("================================================================================")

if __name__ == "__main__":
    main()
