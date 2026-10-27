#!/usr/bin/env python3
"""
Script de procesamiento y descarga de la segunda tanda de 100 episodios (123 al 222)
de 'Lasers y Dragones' (Campaña Starfinder: Dead Suns) y catalogación exhaustiva
de todos los especiales, spin-offs y campañas paralelas (HyS, MdO y Spooky Octubre).
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

def clasificar_episodio_123_222(num):
    if 123 <= num <= 135:
        return {
            "libro_starfinder": "Transición hacia Libro 4 / Aventura en el Casino",
            "parte_aventura": "El Casino al fin del Universo y el Rally de la Muerte",
            "volumen_propuesto": "Volumen 10",
            "arco": "El Rally de la Muerte en el Asteroide-Casino",
            "notas_mesa": "Marloc presente como líder y piloto en la carrera mortal."
        }
    elif 136 <= num <= 145:
        return {
            "libro_starfinder": "Arco Canónico Propio: Familia Galway y Nave La Galway",
            "parte_aventura": "Salida de Marloc; Juan Pablo introduce a Zivok; conflicto con los clanes ysoki",
            "volumen_propuesto": "Volumen 11",
            "arco": "La Marcha de Marloc y los Secretos del Clan Galway",
            "notas_mesa": "Juan Pablo da vacaciones a Marloc y juega con Zivok. Roberto gestiona a Marloc como PNJ."
        }
    elif 146 <= num <= 162:
        return {
            "libro_starfinder": "Arco Canónico Propio: La Galway, Gazit y Rumbo a Nejeor",
            "parte_aventura": "Misión con Yolmar, Valentina y Gazit; tensiones de convivencia en el vacío",
            "volumen_propuesto": "Volumen 11",
            "arco": "La Odisea de La Galway y el Camino a las Nubes",
            "notas_mesa": "Marloc ausente de la mesa presencial; tripulación resuelve crisis familiares de Benrey."
        }
    elif 163 <= num <= 175:
        return {
            "libro_starfinder": "Dead Suns Libro 4: The Ruined Clouds (Las Nubes Arruinadas)",
            "parte_aventura": "Retorno de Marloc; Descenso en Nejeor; Llegada a la Ciudadela Flotante de Istamak",
            "volumen_propuesto": "Volumen 12",
            "arco": "El Retorno de Marloc y las Ruinas de Istamak",
            "notas_mesa": "Retorno oficial de Juan Pablo / Marloc (Ep 163). Inicio del Libro 4 de Paizo."
        }
    elif 176 <= num <= 185:
        return {
            "libro_starfinder": "Dead Suns Libro 4: The Ruined Clouds (Las Nubes Arruinadas)",
            "parte_aventura": "El Templo de los Kishalee, Museo de Istamak y Revelación de la Puerta Estelar",
            "volumen_propuesto": "Volumen 12",
            "arco": "El Enigma Kishalee y la Cámara de las Nubes (Clímax Libro 4)",
            "notas_mesa": "Conclusión de la aventura oficial del Libro 4 en Nejeor."
        }
    elif 186 <= num <= 210:
        return {
            "libro_starfinder": "Arco Canónico Propio: Retorno a Apostae / Conspiración Drow",
            "parte_aventura": "Reactivación de la trama de Keiden Ashton; asalto a los dominios drow de la Casa Istrav",
            "volumen_propuesto": "Volumen 13",
            "arco": "La Venganza de las Drow y la Telaraña de Charlotte",
            "notas_mesa": "Trama personal de Triel y confrontación con la jerarquía matriarcal drow."
        }
    elif 211 <= num <= 222:
        return {
            "libro_starfinder": "Arco Canónico Propio: El Rescate de Keiden Ashton",
            "parte_aventura": "Duelo final con la hermana mayor de Triel y el agónico rescate de su padre Keiden Ashton",
            "volumen_propuesto": "Volumen 13",
            "arco": "El Corazón del Padre y la Redención de Apostae",
            "notas_mesa": "Clímax de la búsqueda vital de Triel; resolución del enigma de Keiden Ashton."
        }
    else:
        return {
            "libro_starfinder": "Dead Suns Libro 5: The Thirteenth Gate (La Decimotercera Puerta)",
            "parte_aventura": "La Puerta de los Doce Soles y Mega-Ingeniería Kishalee",
            "volumen_propuesto": "Volumen 14+",
            "arco": "La Decimotercera Puerta",
            "notas_mesa": "Inicio oficial del Libro 5 de Paizo."
        }

def extraer_todo():
    print(">>> 1. Descargando feed RSS completo de Libsyn...")
    rss_url = "https://rss.libsyn.com/shows/241133/destinations/1801772.xml"
    req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req) as resp:
        tree = ET.parse(resp)
    items = tree.getroot().find("channel").findall("item")

    print(">>> 2. Consultando lista de videos de YouTube de 'Lasers y Dragones'...")
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
    
    # Mapas de YouTube
    yt_numbered = {}
    yt_hys = {}
    yt_mdo = {}
    yt_spooky = {}

    for entry in yt_entries:
        t = entry.get("title", "")
        # Numbered mainline
        m_num = re.search(r'^(?:Episodio|Episode)\s+0*(\d+)\b', t.strip(), re.IGNORECASE)
        if m_num:
            yt_numbered[int(m_num.group(1))] = entry
        
        # HyS
        m_hys = re.search(r'HyS\s+Episodio\s+0*(\d+)', t, re.IGNORECASE)
        if m_hys:
            yt_hys[int(m_hys.group(1))] = entry
            
        # MdO
        m_mdo = re.search(r'MdO\s+Episodio\s+0*(\d+)', t, re.IGNORECASE)
        if m_mdo:
            yt_mdo[int(m_mdo.group(1))] = entry
            
        # Spooky
        if "spooky" in t.lower() or "spookie" in t.lower():
            yt_spooky[t.strip()] = entry

    # Catalogar Especiales y Spin-offs
    print(">>> 3. Catalogando Especiales y Campañas Paralelas (HyS, MdO, Spooky)...")
    especiales_catalogados = {
        "campaña_hielo_y_sangre_2020": {
            "nombre": "Hielo y Sangre (HyS)",
            "año": 2020,
            "periodo": "Abril 2020 - Septiembre 2020 (En plena pandemia de COVID-19)",
            "contexto": "Pausa de la campaña de Starfinder entre los Episodios 17 y 18 para jugar a distancia una campaña completa en Discord.",
            "sistema": "Pathfinder 2e",
            "ambientacion": "El Gran Imperio Dreki (Fantasía medieval en tierras heladas y prisioneros en el Peñón de la Pena).",
            "mesa": {
                "director": "Roberto (GM)",
                "jugadores": ["Irene", "Sofía", "Miguel", "Juan Pablo"],
                "jugadores_adicionales": "Mesa regular conectada en remoto por Discord."
            },
            "total_episodios": 22,
            "episodios": []
        },
        "campaña_mundo_de_oscuridad_2022_2023": {
            "nombre": "Mundo de Oscuridad (MdO)",
            "año": "2022-2023",
            "periodo": "Septiembre 2022 - Agosto 2023",
            "contexto": "Pausa de 1 año en Starfinder tras el clímax de Apostae (Episodio 120) hasta el reinicio (Episodio 121).",
            "sistema": "Pathfinder 2e (Aventura oficial de Paizo: 'The Fall of Plaguestone' / 'La Caída de Piedra de Plaga')",
            "ambientacion": "El pueblo de Piedra de Plaga, alquimistas renegados, Vilree y misterios sobrenaturales.",
            "mesa": {
                "director": "Roberto (GM)",
                "jugadores": ["Irene", "Sofía", "Miguel", "Juan Pablo"],
                "jugadores_adicionales": "Mesa regular."
            },
            "total_episodios": 48,
            "episodios": []
        },
        "especiales_halloween_spooky_octubre": {
            "nombre": "Especiales Anuales de Halloween ('Spooky Octubre')",
            "años": [2021, 2025, 2026],
            "ediciones": [
                {
                    "edicion": "Spooky Octubre 2021 (Pesadilla en Viejo Golarion)",
                    "episodios_podcast": "Episodios 073 al 076a",
                    "sistema": "Pathfinder 2e en Viejo Golarion (Simulación virtual neural en Ábsalon)",
                    "mesa": "Roberto (GM), Irene (Monstruo), Miguel (Isopi Flower), Juan Pablo (Valor), Sofía (Pastinaxcel)",
                    "jugadores_adicionales": "Ninguno"
                },
                {
                    "edicion": "Spooky Octubre 2025 (Trilogía de la Muerte)",
                    "episodios_podcast": "Partes 1 a 3 (Visiones de Verano, El Brindis de la Muerte, La Danza de la Muerte)",
                    "sistema": "Shadowdark RPG",
                    "mesa": "Roberto (GM), Irene, Miguel, Juan Pablo, Sofía",
                    "jugadores_adicionales": "Daneris (invitada especial por petición popular)"
                },
                {
                    "edicion": "Spooky Octubre 2026 (La Guardia de Medianoche)",
                    "episodios_podcast": "Episodio 1 en adelante",
                    "sistema": "Aventura especial de terror anual",
                    "mesa": "Roberto (GM), Irene, Miguel, Juan Pablo, Sofía"
                }
            ],
            "episodios": []
        }
    }

    # Recorrer items de RSS para poblar especiales
    for it in items:
        t = it.findtext("title") or ""
        desc = it.findtext("description") or ""
        clean_desc = re.sub(r"<[^>]+>", " ", desc).split("Instagram")[0].strip()
        pub_date = it.findtext("pubDate") or ""
        enclosure = it.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else ""
        link = it.findtext("link") or ""

        # HyS
        m_hys = re.search(r'HyS\s+Episodio\s+0*(\d+)', t, re.IGNORECASE)
        if m_hys:
            num = int(m_hys.group(1))
            yt_info = yt_hys.get(num, {})
            especiales_catalogados["campaña_hielo_y_sangre_2020"]["episodios"].append({
                "numero": num,
                "titulo": t.strip(),
                "fecha": pub_date.strip(),
                "youtube_id": yt_info.get("id", ""),
                "url_audio": audio_url.strip(),
                "url_pagina": link.strip(),
                "sinopsis": clean_desc
            })

        # MdO
        m_mdo = re.search(r'MdO\s+Episodio\s+0*(\d+)', t, re.IGNORECASE)
        if m_mdo:
            num = int(m_mdo.group(1))
            yt_info = yt_mdo.get(num, {})
            especiales_catalogados["campaña_mundo_de_oscuridad_2022_2023"]["episodios"].append({
                "numero": num,
                "titulo": t.strip(),
                "fecha": pub_date.strip(),
                "youtube_id": yt_info.get("id", ""),
                "url_audio": audio_url.strip(),
                "url_pagina": link.strip(),
                "sinopsis": clean_desc
            })

        # Spooky fuera de numeración
        if "spook" in t.lower() and not re.search(r'Episodio\s+0*7[3-6]', t):
            # match with yt
            yt_id = ""
            for k, val in yt_spooky.items():
                if t.lower() in k.lower() or k.lower() in t.lower():
                    yt_id = val.get("id", "")
                    break
            especiales_catalogados["especiales_halloween_spooky_octubre"]["episodios"].append({
                "titulo": t.strip(),
                "fecha": pub_date.strip(),
                "youtube_id": yt_id,
                "url_audio": audio_url.strip(),
                "url_pagina": link.strip(),
                "sinopsis": clean_desc
            })

    # Ordenar episodios de especiales
    especiales_catalogados["campaña_hielo_y_sangre_2020"]["episodios"].sort(key=lambda x: x["numero"])
    especiales_catalogados["campaña_mundo_de_oscuridad_2022_2023"]["episodios"].sort(key=lambda x: x["numero"])

    os.makedirs(META_DIR, exist_ok=True)
    with open(os.path.join(META_DIR, "especiales_y_spinoffs.json"), "w", encoding="utf-8") as f:
        json.dump(especiales_catalogados, f, indent=2, ensure_ascii=False)
    print("  ✓ Guardado: metadatos/especiales_y_spinoffs.json")

    # Catalogar Episodios 123 al 222 (100 episodios de Starfinder)
    print(">>> 4. Extrayendo metadatos de los Episodios 123 al 222 (100 episodios)...")
    episodes_100 = []
    for it in items:
        t = it.findtext("title") or ""
        m = re.search(r'^(?:Episodio|Episode)\s+0*(\d+)\b', t.strip(), re.IGNORECASE)
        if m:
            num = int(m.group(1))
            if 123 <= num <= 222:
                desc = it.findtext("description") or ""
                clean_desc = re.sub(r"<[^>]+>", " ", desc).split("Instagram")[0].strip()
                pub_date = it.findtext("pubDate") or ""
                enclosure = it.find("enclosure")
                audio_url = enclosure.get("url") if enclosure is not None else ""
                link = it.findtext("link") or ""

                yt_info = yt_numbered.get(num, {})
                yt_id = yt_info.get("id", "")

                clasif = clasificar_episodio_123_222(num)

                episodes_100.append({
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

    episodes_100.sort(key=lambda x: x["numero"])

    with open(os.path.join(META_DIR, "episodios_123_222.json"), "w", encoding="utf-8") as f:
        json.dump(episodes_100, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Guardado: metadatos/episodios_123_222.json ({len(episodes_100)} episodios)")

    return episodes_100

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

def descargar_todos(episodes):
    print(f"\n>>> 5. Descargando subtítulos automáticos VTT ({len(episodes)} episodios en paralelo con 6 hilos)...")
    os.makedirs(RAW_DIR, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(descargar_subtitulo, ep): ep for ep in episodes}
        for future in as_completed(futures):
            ep = futures[future]
            num, ok, msg = future.result()
            estado = "✓" if ok else "✗"
            print(f"  [{estado}] Ep {num:03d}: {msg}")

def limpiar_todas(episodes):
    print(f"\n>>> 6. Limpiando y deduplicando transcripciones ({len(episodes)} episodios)...")
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

    print(f"\n>>> Proceso concluido: {exitos}/{len(episodes)} transcripciones limpias ({total_palabras:,} palabras en total).")

def main():
    print("================================================================================")
    print("PROCESAMIENTO DE 100 EPISODIOS (123-222) Y CATALOGACIÓN DE ESPECIALES")
    print("================================================================================")
    episodes = extraer_todo()
    descargar_todos(episodes)
    limpiar_todas(episodes)
    print("================================================================================")
    print("¡PROCESAMIENTO Y DESCARGA COMPLETADOS CON ÉXITO!")
    print("================================================================================")

if __name__ == "__main__":
    main()
