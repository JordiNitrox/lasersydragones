#!/usr/bin/env python3
"""
Script para descargar los 10 primeros episodios del podcast 'Lasers y Dragones'
a partir de los archivos mensuales de Libsyn (2020/01, 2020/02, 2020/03).
"""

import os
import sys
import time
import json
import re
import urllib.request
import html

EPISODIOS_CONFIG = [
    {
        "numero": 1,
        "titulo": "Episodio 1 - Una Historia: La Llegada",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-1",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio001.mp3",
        "archivo": "LasersYDragonesEpisodio001.mp3",
    },
    {
        "numero": 2,
        "titulo": "Episodio 2 - Aliens y Androides",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-2-aliens-y-androides",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio002.mp3",
        "archivo": "LasersYDragonesEpisodio002.mp3",
    },
    {
        "numero": 3,
        "titulo": "Episodio 3 - Una Dama por la que Mataría",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-3-una-dama-por-la-que-matara",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio003.mp3",
        "archivo": "LasersYDragonesEpisodio003.mp3",
    },
    {
        "numero": 4,
        "titulo": "Episodio 4 - Noticias de Última Hora",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-4-noticias-en-accin",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio004.mp3",
        "archivo": "LasersYDragonesEpisodio004.mp3",
    },
    {
        "numero": 5,
        "titulo": "Episodio 5 - El hombre que no sabía suficiente.",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-5-el-hombre-que-no-saba-suficiente",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio005.mp3",
        "archivo": "LasersYDragonesEpisodio005.mp3",
    },
    {
        "numero": 6,
        "titulo": "Episodio 6 - Maverick Marloc",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-6-maverick-marloc",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio006.mp3",
        "archivo": "LasersYDragonesEpisodio006.mp3",
    },
    {
        "numero": 7,
        "titulo": "Episodio 7 - Tratos por lo bajo",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-7-tratos-por-lo-bajo",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio007.mp3",
        "archivo": "LasersYDragonesEpisodio007.mp3",
    },
    {
        "numero": 8,
        "titulo": "Episodio 8 - La Reina de la Con-Fusión",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-8-la-reina-de-la-kung-fusin",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio008.mp3",
        "archivo": "LasersYDragonesEpisodio008.mp3",
    },
    {
        "numero": 9,
        "titulo": "Episodio 9 - Fear and Loathing in Los Bajos",
        "url_pagina": "https://lasersydragones.libsyn.com/-episodio-9-fear-and-loathing-in-los-bajos",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio009.mp3",
        "archivo": "LasersYDragonesEpisodio009.mp3",
    },
    {
        "numero": 10,
        "titulo": "Episodio 10 - Huyendo del Pasado",
        "url_pagina": "https://lasersydragones.libsyn.com/episodio-10-huyendo-del-pasado",
        "url_audio": "https://traffic.libsyn.com/secure/lasersydragones/LasersYDragonesEpisodio010.mp3",
        "archivo": "LasersYDragonesEpisodio010.mp3",
    },
]

def obtener_detalles_pagina(url_pagina):
    req = urllib.request.Request(url_pagina, headers={"User-Agent": "Mozilla/5.0"})
    try:
        html_content = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
        date_match = re.search(r'<p class=\"date\">([^<]+)</p>', html_content)
        fecha = date_match.group(1).strip() if date_match else ""

        desc_match = re.search(r'<meta name=\"description\" content=\"([^\"]+)\"', html_content)
        descripcion = html.unescape(desc_match.group(1).strip()) if desc_match else ""
        return fecha, descripcion
    except Exception as e:
        print(f"  [Aviso] No se pudo obtener metadatos de {url_pagina}: {e}")
        return "", ""

def descargar_archivo(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        descargado = 0
        bloque = 1024 * 512 # 512 KB
        temp_destino = destino + ".part"
        
        with open(temp_destino, "wb") as f:
            while True:
                chunk = resp.read(bloque)
                if not chunk:
                    break
                f.write(chunk)
                descargado += len(chunk)
                if total > 0:
                    pct = (descargado / total) * 100
                    mb_desc = descargado / (1024 * 1024)
                    mb_tot = total / (1024 * 1024)
                    sys.stdout.write(f"\r  Progreso: {mb_desc:.1f}/{mb_tot:.1f} MB ({pct:.1f}%)")
                    sys.stdout.flush()
        
        if os.path.exists(temp_destino):
            os.replace(temp_destino, destino)
        print()
        return descargado

def main():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    print(f"Descargando los 10 primeros episodios en: {directorio_actual}\n")
    
    metadata = []
    
    for i, ep in enumerate(EPISODIOS_CONFIG, 1):
        num = ep["numero"]
        titulo = ep["titulo"]
        archivo = ep["archivo"]
        ruta_archivo = os.path.join(directorio_actual, archivo)
        
        print(f"[{i}/10] Episodio {num}: {titulo}")
        fecha, desc = obtener_detalles_pagina(ep["url_pagina"])
        
        if os.path.exists(ruta_archivo) and os.path.getsize(ruta_archivo) > 1024 * 1024:
            tam_mb = os.path.getsize(ruta_archivo) / (1024 * 1024)
            print(f"  Archivo ya descargado ({tam_mb:.2f} MB): {archivo}")
            tam_bytes = os.path.getsize(ruta_archivo)
        else:
            print(f"  Descargando desde: {ep['url_audio']}")
            t0 = time.time()
            tam_bytes = descargar_archivo(ep["url_audio"], ruta_archivo)
            dt = time.time() - t0
            velocidad = (tam_bytes / (1024 * 1024)) / (dt if dt > 0 else 1)
            print(f"  Completado en {dt:.1f}s ({velocidad:.2f} MB/s) -> {archivo}")
            
        metadata.append({
            "numero": num,
            "titulo": titulo,
            "archivo": archivo,
            "tamano_mb": round(tam_bytes / (1024 * 1024), 2),
            "tamano_bytes": tam_bytes,
            "fecha": fecha,
            "url_pagina": ep["url_pagina"],
            "url_audio": ep["url_audio"],
            "descripcion": desc
        })
        print()
        
    # Guardar metadata JSON
    json_path = os.path.join(directorio_actual, "episodios.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Metadatos guardados en: {json_path}")
    
    # Guardar README.md
    readme_path = os.path.join(directorio_actual, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Lasers y Dragones - Primeros 10 Episodios\n\n")
        f.write("Episodios descargados desde el sitio oficial de Libsyn (2020/01 a 2020/03).\n\n")
        f.write("| # | Título | Fecha | Tamaño | Archivo |\n")
        f.write("|---|--------|-------|--------|---------|\n")
        for ep in metadata:
            f.write(f"| {ep['numero']} | [{ep['titulo']}]({ep['url_pagina']}) | {ep['fecha']} | {ep['tamano_mb']} MB | `{ep['archivo']}` |\n")
        f.write("\n## Sinopsis de los episodios\n\n")
        for ep in metadata:
            f.write(f"### {ep['titulo']} ({ep['fecha']})\n")
            f.write(f"- **Archivo:** `{ep['archivo']}` ({ep['tamano_mb']} MB)\n")
            f.write(f"- **Enlace:** [{ep['url_pagina']}]({ep['url_pagina']})\n")
            if ep["descripcion"]:
                f.write(f"- **Descripción:** {ep['descripcion']}\n\n")
    print(f"Resumen generado en: {readme_path}")
    print("\n¡Todos los 10 episodios se descargaron exitosamente!")

if __name__ == "__main__":
    main()
