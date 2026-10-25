#!/usr/bin/env python3
"""
Script de procesamiento, descarga y limpieza del tramo final de episodios (223 al 272)
de 'Lasers y Dragones' (Campaña Starfinder: Dead Suns - Libros 5 y 6)
y el especial en emisión Spooky Octubre 2026 (Episodio 1).
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

def clasificar_episodio_223_272(num):
    if 223 <= num <= 233:
        return {
            "libro_starfinder": "Dead Suns Libro 5: The Thirteenth Gate (Parte 1)",
            "parte_aventura": "Consecuencias de Apostae, rumbo a los Doce Soles y secretos de Axel-42",
            "volumen_propuesto": "Volumen 14",
            "arco": "El Misterio de los Doce Soles y el Chasis de Axel",
            "notas_mesa": "Mesa completa; revelaciones del pasado mecánico de Axel-42 y amenazas residuales."
        }
    elif 234 <= num <= 244:
        return {
            "libro_starfinder": "Dead Suns Libro 5: The Thirteenth Gate (Parte 2)",
            "parte_aventura": "Mega-estructura de los Doce Soles, estaciones de control y laboratorios Kishalee",
            "volumen_propuesto": "Volumen 14",
            "arco": "La Ciudadela de los Doce Soles",
            "notas_mesa": "Exploración de la mega-ingeniería Kishalee y combate contra bestias ancestrales."
        }
    elif 245 <= num <= 249:
        return {
            "libro_starfinder": "Dead Suns Libro 5: The Thirteenth Gate (Clímax)",
            "parte_aventura": "Duelo final contra Null-9, la IA Eltreth y apertura de La Decimotercera Puerta",
            "volumen_propuesto": "Volumen 14",
            "arco": "La Decimotercera Puerta (Clímax Libro 5)",
            "notas_mesa": "Caída de Null-9 y activación del portal interdimensional hacia el Devastador Estelar."
        }
    elif 250 <= num <= 254:
        return {
            "libro_starfinder": "Dead Suns Libro 6: Empire of Bones (Parte 1)",
            "parte_aventura": "Llegada del dreadnought 'Imperio de los Huesos', emboscada de marines no-muertos y contraataque",
            "volumen_propuesto": "Volumen 15 (En Curso)",
            "arco": "La Invasión de la Flota de los Cuerpos (Atómicos Assemble)",
            "notas_mesa": "Inicio oficial del Libro 6 de Paizo. Guerra total contra la armada no-muerta de Eox."
        }
    elif 255 <= num <= 269:
        return {
            "libro_starfinder": "Dead Suns Libro 6: Empire of Bones (Parte 2: Infiltración)",
            "parte_aventura": "Incursión en el Imperio de los Huesos: hangares, calabozos, duelo con Malakar y persecución en tren de la muerte",
            "volumen_propuesto": "Volumen 15 (En Curso)",
            "arco": "Infiltración en el Imperio de los Huesos y el Tren de la Muerte",
            "notas_mesa": "Tensión táctica máxima; combate vehicular tren contra tren y acecho de baykoks."
        }
    else: # 270 <= num <= 272+
        return {
            "libro_starfinder": "Dead Suns Libro 6: Empire of Bones (Parte 3: Núcleo y Sangromancia)",
            "parte_aventura": "Sección de motores, visiones sangrientas de Marloc y combate contra la tejedora de sangre Anasi",
            "volumen_propuesto": "Volumen 15 (En Curso)",
            "arco": "El Velo de la Sangre y la Marcha hacia el Almirante",
            "notas_mesa": "Historia en emisión; Marloc frente a visiones arcanas. ¡Campaña en curso en mesa!"
        }

def extraer_datos():
    print(">>> 1. Descargando feed RSS completo...")
    rss_url = "https://rss.libsyn.com/shows/241133/destinations/1801772.xml"
    req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        tree = ET.parse(resp)
    items = tree.getroot().find("channel").findall("item")

    print(">>> 2. Consultando lista completa de videos de YouTube...")
    yt_cmd = [
        "yt-dlp", "--no-update", "--flat-playlist", "-J",
        "https://www.youtube.com/channel/UCPZQdWughRVDyd3LNFkIExw/videos"
    ]
    res = subprocess.run(yt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error consultando YouTube: {res.stderr}")
        sys.exit(1)

    yt_data = json.loads(res.stdout)
    yt_entries = yt_data.get("entries", [])
    
    yt_numbered = {}
    yt_spooky_2026 = None

    for entry in yt_entries:
        t = entry.get("title", "")
        m_num = re.search(r'^(?:Episodio|Episode)\s+0*(\d+)\b', t.strip(), re.IGNORECASE)
        if m_num:
            yt_numbered[int(m_num.group(1))] = entry
        if ("spooky" in t.lower() or "spookie" in t.lower()) and "2026" in t:
            yt_spooky_2026 = entry

    print(">>> 3. Extrayendo metadatos de los Episodios 223 al 272 (50 episodios)...")
    episodes_finales = []
    spooky_2026_data = None

    for it in items:
        t = it.findtext("title") or ""
        m = re.search(r'^(?:Episodio|Episode)\s+0*(\d+)\b', t.strip(), re.IGNORECASE)
        desc = it.findtext("description") or ""
        clean_desc = re.sub(r"<[^>]+>", " ", desc).split("Instagram")[0].strip()
        pub_date = it.findtext("pubDate") or ""
        enclosure = it.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else ""
        link = it.findtext("link") or ""

        if m:
            num = int(m.group(1))
            if 223 <= num <= 272:
                yt_info = yt_numbered.get(num, {})
                yt_id = yt_info.get("id", "")
                clasif = clasificar_episodio_223_272(num)

                episodes_finales.append({
                    "numero": num,
                    "titulo": t.strip(),
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
                    "notas_mesa": clasif["notas_mesa"],
                    "sinopsis": clean_desc
                })
        elif ("spooky" in t.lower() or "spookie" in t.lower()) and "2026" in t:
            spooky_2026_data = {
                "identificador": "spooky_octubre_2026_ep01",
                "titulo": t.strip(),
                "fecha_publicacion": pub_date.strip(),
                "youtube_id": yt_spooky_2026.get("id", "") if yt_spooky_2026 else "",
                "youtube_url": f"https://www.youtube.com/watch?v={yt_spooky_2026.get('id', '')}" if yt_spooky_2026 else "",
                "url_audio": audio_url.strip(),
                "url_pagina": link.strip(),
                "archivo_audio": "SpookyOctubre2026Ep01.mp3",
                "sinopsis": clean_desc,
                "estado": "En emisión / Halloween 2026 en curso"
            }

    episodes_finales.sort(key=lambda x: x["numero"])

    # Guardar metadatos del lote 223_272
    with open(os.path.join(META_DIR, "episodios_starfinder_223_272.json"), "w", encoding="utf-8") as f:
        json.dump(episodes_finales, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Guardado: metadatos/episodios_starfinder_223_272.json ({len(episodes_finales)} episodios)")

    # Actualizar especiales_y_spinoffs.json con Spooky 2026
    esp_path = os.path.join(META_DIR, "especiales_y_spinoffs.json")
    if os.path.exists(esp_path):
        with open(esp_path, "r", encoding="utf-8") as f:
            esp_data = json.load(f)
        
        # Actualizar edicion Spooky 2026
        ediciones = esp_data["especiales_halloween_spooky_octubre"].get("ediciones", [])
        for ed in ediciones:
            if "2026" in ed.get("edicion", ""):
                ed["estado"] = "En emisión / No terminado"
                ed["episodios_disponibles"] = ["Episodio 1: La Guardia de Medianoche (21 Oct 2026)"]
                ed["nota"] = "El podcast continúa emitiendo la temporada de Halloween."
        
        # Agregar episodio a lista si no está
        ep_list = esp_data["especiales_halloween_spooky_octubre"].setdefault("episodios", [])
        ya_existe = any("2026" in item.get("titulo", "") for item in ep_list)
        if not ya_existe and spooky_2026_data:
            ep_list.append(spooky_2026_data)

        with open(esp_path, "w", encoding="utf-8") as f:
            json.dump(esp_data, f, indent=2, ensure_ascii=False)
        print("  ✓ Actualizado: metadatos/especiales_y_spinoffs.json (con Spooky 2026)")

    # Consolidar metadatos maestros: episodios_starfinder_73_272.json (200 episodios)
    with open(os.path.join(META_DIR, "episodios_starfinder_73_122.json"), "r", encoding="utf-8") as f:
        lote_1 = json.load(f)
    with open(os.path.join(META_DIR, "episodios_starfinder_123_222.json"), "r", encoding="utf-8") as f:
        lote_2 = json.load(f)
    
    maestro_200 = lote_1 + lote_2 + episodes_finales
    maestro_200.sort(key=lambda x: x["numero"])
    
    with open(os.path.join(META_DIR, "episodios_starfinder_73_272.json"), "w", encoding="utf-8") as f:
        json.dump(maestro_200, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Guardado: metadatos/episodios_starfinder_73_272.json ({len(maestro_200)} episodios acumulados)")

    return episodes_finales, spooky_2026_data

def descargar_subtitulo(item, is_special=False):
    if is_special:
        identificador = item["identificador"]
        yt_id = item["youtube_id"]
        out_pattern = os.path.join(RAW_DIR, f"{identificador}.%(ext)s")
        target_vtt = os.path.join(RAW_DIR, f"{identificador}.es.vtt")
    else:
        num = item["numero"]
        identificador = f"Ep {num:03d}"
        yt_id = item["youtube_id"]
        out_pattern = os.path.join(RAW_DIR, f"episodio_{num:02d}.%(ext)s")
        target_vtt = os.path.join(RAW_DIR, f"episodio_{num:02d}.es.vtt")

    if not yt_id:
        return identificador, False, "No YouTube ID"

    if os.path.exists(target_vtt):
        return identificador, True, "Ya existía"

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
        return identificador, True, "Descargado"
    else:
        return identificador, False, res.stderr[:100]

def descargar_todos(episodes, spooky_data):
    items_to_download = [(ep, False) for ep in episodes]
    if spooky_data:
        items_to_download.append((spooky_data, True))

    print(f"\n>>> 4. Descargando subtítulos automáticos VTT ({len(items_to_download)} elementos en paralelo)...")
    os.makedirs(RAW_DIR, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(descargar_subtitulo, item, is_sp): item for item, is_sp in items_to_download}
        for future in as_completed(futures):
            identificador, ok, msg = future.result()
            estado = "✓" if ok else "✗"
            print(f"  [{estado}] {identificador}: {msg}")

def limpiar_todas(episodes, spooky_data):
    print(f"\n>>> 5. Limpiando y deduplicando transcripciones...")
    os.makedirs(CLEAN_DIR, exist_ok=True)

    sys.path.insert(0, os.path.dirname(CLEANER_SCRIPT))
    from limpiar_transcripcion import limpiar_vtt

    exitos = 0
    total_palabras = 0

    items_to_clean = [(f"episodio_{ep['numero']:02d}", f"Ep {ep['numero']:03d}") for ep in episodes]
    if spooky_data:
        items_to_clean.append((spooky_data["identificador"], "Spooky Octubre 2026 Ep 1"))

    for base_name, label in items_to_clean:
        vtt_file = os.path.join(RAW_DIR, f"{base_name}.es.vtt")
        clean_file = os.path.join(CLEAN_DIR, f"{base_name}.txt")

        if not os.path.exists(vtt_file):
            print(f"  [Aviso] No se encontró VTT para {label}")
            continue

        limpiar_vtt(vtt_file, clean_file)
        if os.path.exists(clean_file):
            with open(clean_file, "r", encoding="utf-8") as f:
                content = f.read()
            palabras = len(content.split())
            total_palabras += palabras
            exitos += 1

    print(f"\n>>> Proceso concluido: {exitos}/{len(items_to_clean)} transcripciones limpias ({total_palabras:,} palabras en este lote).")

def main():
    print("================================================================================")
    print("PROCESAMIENTO FINAL: EPISODIOS 223 AL 272 + SPOOKY OCTUBRE 2026")
    print("================================================================================")
    episodes, spooky_data = extraer_datos()
    descargar_todos(episodes, spooky_data)
    limpiar_todas(episodes, spooky_data)
    print("================================================================================")
    print("¡DESCARGA Y PROCESAMIENTO COMPLETADOS CON ÉXITO!")
    print("================================================================================")

if __name__ == "__main__":
    main()
