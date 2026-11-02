#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/actualizar_wiki.py
Generador y sincronizador automático del Wiki de GitHub para 'Lasers y Dragones: La Novela'.
Convierte todos los capítulos, prólogos, notas editoriales, glosarios y compendios
a páginas planas de GitHub Wiki con navegación diegética cruzada (anterior/siguiente),
índice lateral (_Sidebar.md), pie de página (_Footer.md) y portada principal (Home.md).
"""

import os
import sys
import re
import glob
import argparse
import shutil
from pathlib import Path

# Catálogo canónico de títulos y subtítulos de volúmenes
METADATOS_VOLUMENES = {
    1: {"titulo": "Sombras sobre Absalón", "subtitulo": "Conspiración en la Espiga", "episodios": "Episodios 1 al 10"},
    2: {"titulo": "El Misterio del Acreon", "subtitulo": "Los Secretos del Vacío", "episodios": "Episodios 11 al 22"},
    3: {"titulo": "La Roca del Drift", "subtitulo": "El Enigma Ancestral", "episodios": "Episodios 23 al 33"},
    4: {"titulo": "Las Torres de Qabarat", "subtitulo": "El Horizonte Esmeralda", "episodios": "Episodios 34 al 45"},
    5: {"titulo": "El Templo de los Doce Soles", "subtitulo": "El Enigma de Castrovel", "episodios": "Episodios 46 al 59"},
    6: {"titulo": "El Fantasma en la Máquina", "subtitulo": "Intriga en la Ciudadela", "episodios": "Episodios 60 al 72"},
    7: {"titulo": "Mundos Fragmentados I: El Rastro hacia Eox", "subtitulo": "El Rastro hacia Eox", "episodios": "Episodios 76 al 88"},
    8: {"titulo": "Mundos Fragmentados II: Las Cortes Cadavéricas de Eox", "subtitulo": "El Camino Furibundo de Zo!", "episodios": "Episodios 89 al 98"},
    9: {"titulo": "Mundos Fragmentados III: La Necrogarganta de Eox", "subtitulo": "La Necrogarganta de Eox", "episodios": "Episodios 99 al 110"},
    10: {"titulo": "Lazos de Sangre: La Sombra de Apostae", "subtitulo": "La Sombra de Apostae", "episodios": "Episodios 111 al 122"},
    11: {"titulo": "El Rally de la Muerte", "subtitulo": "El Rally de la Muerte en el Asteroide-Casino", "episodios": "Episodios 123 al 135"},
    12: {"titulo": "El Pecio de la Oscuridad", "subtitulo": "La Odisea de La Galway I: El Pecio de la Oscuridad", "episodios": "Episodios 136 al 147"},
    13: {"titulo": "El Laberinto de los Lovelorn", "subtitulo": "La Odisea de La Galway II: El Laberinto de los Lovelorn", "episodios": "Episodios 148 al 162"},
    14: {"titulo": "La Ciudadela de Istamak", "subtitulo": "Las Nubes Arruinadas I: La Ciudadela de Istamak", "episodios": "Episodios 163 al 173"},
    15: {"titulo": "La Forja Kishalee", "subtitulo": "Las Nubes Arruinadas II: La Forja Kishalee", "episodios": "Episodios 174 al 185"},
    16: {"titulo": "El Secreto de la Deriva", "subtitulo": "Las Nubes Arruinadas III: El Secreto de la Deriva", "episodios": "Episodios 186 al 201"},
    17: {"titulo": "La Nave de Besmara", "subtitulo": "La Conexión de los Doce Soles I", "episodios": "Episodios 202 a 222"},
    18: {"titulo": "Los Doce Soles", "subtitulo": "La Conexión de los Doce Soles II", "episodios": "Episodios 223 al 235"},
    19: {"titulo": "La Decimotercera Puerta", "subtitulo": "Hacia el Núcleo Estelar", "episodios": "Episodios 236 al 249"},
    20: {"titulo": "El Imperio de los Huesos", "subtitulo": "El Asalto Final", "episodios": "Episodios 250 al 272"}
}

COMPENDIO_SECCIONES = [
    ("01_resumen_cronologico_volumenes.md", "Compendio-Cronologia-Volumenes", "📅 Cronología de los Volúmenes"),
    ("02_indice_maestro_escenarios.md", "Compendio-Indice-Escenarios", "🪐 Índice de Escenarios"),
    ("03_dossier_maestro_personajes.md", "Compendio-Dossier-Personajes", "👥 Dossier de Personajes"),
    ("04_corporaciones_facciones.md", "Compendio-Corporaciones-Facciones", "🏢 Corporaciones y Facciones"),
    ("05_bestiario_y_amenazas.md", "Compendio-Bestiario-Amenazas", "👾 Bestiario y Amenazas"),
    ("06_matriz_continuidad.md", "Compendio-Matriz-Continuidad", "📐 Matriz de Continuidad")
]


def limpiar_enlaces_markdown(contenido: str, vol_num: int) -> str:
    """Adapta enlaces relativos locales a enlaces compatibles con GitHub Wiki."""
    # Enlaces a glosario local
    contenido = re.sub(r'\[([^\]]+)\]\(GLOSARIO_Y_PERSONAJES\.md\)', rf'[\1](Volumen-{vol_num:02d}-Glosario)', contenido)
    # Enlaces a capitulos tipo capitulos/01_capitulo_...md
    def repl_cap(match):
        texto = match.group(1)
        target = match.group(2)
        if "prologo" in target:
            return f"[{texto}](Volumen-{vol_num:02d}-Prologo)"
        if "nota_editorial" in target:
            return f"[{texto}](Volumen-{vol_num:02d}-Nota-Editorial)"
        m = re.search(r'capitulo_(\d+)', target)
        if m:
            num = int(m.group(1))
            return f"[{texto}](Volumen-{vol_num:02d}-Capitulo-{num:02d})"
        return match.group(0)

    contenido = re.sub(r'\[([^\]]+)\]\(capitulos/([^\)]+)\)', repl_cap, contenido)
    contenido = re.sub(r'\[([^\]]+)\]\(([0-9]+_[^\)]+\.md)\)', repl_cap, contenido)
    return contenido


def extraer_titulo_archivo(ruta_archivo: str) -> str:
    """Extrae el primer título H1 (# ...) de un archivo markdown."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            for line in f:
                line_str = line.strip()
                if line_str.startswith('# '):
                    return line_str.replace('# ', '').strip()
    except Exception:
        pass
    base = os.path.basename(ruta_archivo)
    return base.replace('.md', '').replace('_', ' ').title()


def construir_barra_navegacion(anterior: dict, indice: dict, siguiente: dict) -> str:
    """Genera la barra de navegación entre capítulos para la lectura fluida."""
    partes = []
    if anterior:
        partes.append(f"[⬅️ **{anterior['label']}**]({anterior['page']})")
    else:
        partes.append(f"[🏠 **Biblioteca (Home)**](Home)")

    partes.append(f"[📚 **{indice['label']}**]({indice['page']})")

    if siguiente:
        partes.append(f"[**{siguiente['label']}** ➡️]({siguiente['page']})")
    else:
        partes.append(f"[🏠 **Biblioteca (Home)**](Home)")

    nav_text = " &nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp; ".join(partes)
    return f"\n\n---\n\n<div align=\"center\">\n\n{nav_text}\n\n</div>\n\n---\n\n"



def procesar_volumen(vol_dir: str, vol_num: int):
    """Procesa un volumen específico retornando su lista de páginas ordenadas y metadata."""
    meta = METADATOS_VOLUMENES.get(vol_num, {
        "titulo": f"Volumen {vol_num}",
        "subtitulo": f"Soles Muertos - Volumen {vol_num}",
        "episodios": ""
    })

    novela_dir = os.path.join(vol_dir, "novela")
    capitulos_dir = os.path.join(novela_dir, "capitulos")
    glosario_path = os.path.join(novela_dir, "GLOSARIO_Y_PERSONAJES.md")

    paginas = []

    # 1. Nota Editorial
    nota_path = os.path.join(capitulos_dir, "00_nota_editorial.md")
    if os.path.exists(nota_path):
        paginas.append({
            "tipo": "nota_editorial",
            "page": f"Volumen-{vol_num:02d}-Nota-Editorial",
            "label": "Nota Editorial",
            "titulo": extraer_titulo_archivo(nota_path),
            "ruta": nota_path
        })

    # 2. Prólogo
    prologo_path = os.path.join(capitulos_dir, "00_prologo.md")
    if os.path.exists(prologo_path):
        paginas.append({
            "tipo": "prologo",
            "page": f"Volumen-{vol_num:02d}-Prologo",
            "label": "Prólogo",
            "titulo": extraer_titulo_archivo(prologo_path),
            "ruta": prologo_path
        })

    # 3. Capítulos numerados
    cap_files = sorted(glob.glob(os.path.join(capitulos_dir, "[0-9][0-9]_capitulo_*.md")))
    for cap_idx, c_path in enumerate(cap_files, start=1):
        titulo_cap = extraer_titulo_archivo(c_path)
        # Extraer número canónico del capítulo si es posible
        m = re.search(r'capitulo_([0-9]+)', os.path.basename(c_path))
        num_cap_canon = int(m.group(1)) if m else cap_idx

        paginas.append({
            "tipo": "capitulo",
            "numero_vol": cap_idx,
            "numero_canon": num_cap_canon,
            "page": f"Volumen-{vol_num:02d}-Capitulo-{cap_idx:02d}",
            "label": f"Capítulo {cap_idx}",
            "titulo": titulo_cap,
            "ruta": c_path
        })

    # 4. Glosario
    if os.path.exists(glosario_path):
        paginas.append({
            "tipo": "glosario",
            "page": f"Volumen-{vol_num:02d}-Glosario",
            "label": "Glosario y Personajes",
            "titulo": f"Glosario y Personajes - Volumen {vol_num}",
            "ruta": glosario_path
        })

    return meta, paginas


def generar_wiki(repo_dir: str, wiki_dir: str):
    """Genera todas las páginas del wiki en wiki_dir a partir del repo."""
    os.makedirs(wiki_dir, exist_ok=True)
    repo_path = Path(repo_dir)

    volumenes_info = []

    # Localizar volúmenes de 1 a 20
    for v_num in range(1, 21):
        v_dir = repo_path / "soles_muertos" / f"volumen_{v_num}"
        if not v_dir.exists():
            continue

        meta, paginas = procesar_volumen(str(v_dir), v_num)
        volumenes_info.append({
            "numero": v_num,
            "meta": meta,
            "paginas": paginas,
            "dir": str(v_dir)
        })

    print(f"[*] Procesando {len(volumenes_info)} volúmenes...")

    # Generar páginas de capítulos con barras de navegación
    total_paginas_escritas = 0

    for vol in volumenes_info:
        v_num = vol["numero"]
        meta = vol["meta"]
        paginas = vol["paginas"]

        indice_info = {
            "page": f"Volumen-{v_num:02d}",
            "label": f"Volumen {v_num}"
        }

        # Generar cada página individual del volumen
        for idx, item in enumerate(paginas):
            anterior = paginas[idx - 1] if idx > 0 else None
            siguiente = paginas[idx + 1] if idx < len(paginas) - 1 else None

            # Si es el último capítulo del volumen y no hay glosario, enlazar con el siguiente volumen si existe
            if not siguiente and v_num < len(volumenes_info):
                next_vol = volumenes_info[v_num]  # v_num es 1-based, index v_num es volumen v_num + 1
                if next_vol["paginas"]:
                    primera_siguiente = next_vol["paginas"][0]
                    siguiente = {
                        "page": primera_siguiente["page"],
                        "label": f"Vol {next_vol['numero']} ({primera_siguiente['label']})"
                    }

            nav_bar = construir_barra_navegacion(anterior, indice_info, siguiente)

            # Leer contenido original
            with open(item["ruta"], 'r', encoding='utf-8') as f:
                raw_content = f.read()

            contenido_limpio = limpiar_enlaces_markdown(raw_content, v_num)

            # Encabezado del volumen y navegación
            subhead = f"<div align=\"center\">\n\n### 📖 *Lasers y Dragones · Volumen {v_num}: {meta['titulo']}*\n*{meta['subtitulo']}*\n\n</div>\n\n"

            pagina_final = f"{nav_bar}{subhead}{contenido_limpio}\n\n{nav_bar}"

            out_path = os.path.join(wiki_dir, f"{item['page']}.md")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(pagina_final)
            total_paginas_escritas += 1

        # Generar Índice del Volumen (Volumen-XX.md)
        generar_indice_volumen(wiki_dir, vol)
        total_paginas_escritas += 1

    # Generar Páginas de Compendio Maestro
    compendio_dir = repo_path / "Contexto completo" / "secciones"
    if compendio_dir.exists():
        for archivo, wiki_slug, label in COMPENDIO_SECCIONES:
            src = compendio_dir / archivo
            if src.exists():
                with open(src, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Reescribir referencias a otros archivos del compendio
                for a_ref, s_ref, _ in COMPENDIO_SECCIONES:
                    content = content.replace(f"secciones/{a_ref}", s_ref)
                    content = content.replace(a_ref, s_ref)

                nav_compendio = "\n\n---\n\n<div align=\"center\">\n\n[🏠 **Inicio Wiki**](Home) &nbsp;•&nbsp; [👥 **Personajes**](Compendio-Dossier-Personajes) &nbsp;•&nbsp; [🪐 **Escenarios**](Compendio-Indice-Escenarios) &nbsp;•&nbsp; [🏢 **Facciones**](Compendio-Corporaciones-Facciones) &nbsp;•&nbsp; [📅 **Cronología**](Compendio-Cronologia-Volumenes)\n\n</div>\n\n---\n\n"

                out_comp = os.path.join(wiki_dir, f"{wiki_slug}.md")
                with open(out_comp, 'w', encoding='utf-8') as f:
                    f.write(f"{nav_compendio}{content}\n\n{nav_compendio}")
                total_paginas_escritas += 1

    # Generar Home.md
    generar_home(wiki_dir, volumenes_info)
    total_paginas_escritas += 1

    # Generar _Sidebar.md
    generar_sidebar(wiki_dir, volumenes_info)
    total_paginas_escritas += 1

    # Generar _Footer.md
    generar_footer(wiki_dir)
    total_paginas_escritas += 1

    print(f"[✓] Generación completada con éxito. Total de páginas escritas: {total_paginas_escritas}")


def generar_indice_volumen(wiki_dir: str, vol: dict):
    """Genera la página índice de un volumen específico (Volumen-XX.md)."""
    v_num = vol["numero"]
    meta = vol["meta"]
    paginas = vol["paginas"]

    primer_cap = None
    for p in paginas:
        if p["tipo"] in ("prologo", "capitulo"):
            primer_cap = p
            break

    leer_primero_btn = f"[▶️ **Comenzar a leer este volumen ({primer_cap['label']})**]({primer_cap['page']})" if primer_cap else ""

    md = [
        f"# 📖 Volumen {v_num}: {meta['titulo']}",
        f"### *{meta['subtitulo']}*",
        f"**Correspondencia:** {meta['episodios']}  ",
        "",
        "---",
        "",
        leer_primero_btn,
        "",
        "## 📑 Índice de Capítulos",
        ""
    ]

    for p in paginas:
        icono = "📝" if p["tipo"] == "nota_editorial" else ("🌌" if p["tipo"] == "prologo" else ("📜" if p["tipo"] == "glosario" else "🔹"))
        md.append(f"* {icono} **[{p['titulo']}]({p['page']})** ({p['label']})")

    md.extend([
        "",
        "---",
        "",
        "## 📥 Edición Editorial en PDF",
        f"Puedes descargar la versión maquetada oficial con portada A4, tipografía editorial e índice interactivo desde el repositorio:",
        f"👉 [**Descargar PDF en carpeta del proyecto**](https://github.com/JordiNitrox/lasersydragones/tree/main/soles_muertos/libros_pdf)",
        "",
        "---",
        "<div align=\"center\">\n\n[🏠 **Volver a la Portada de la Biblioteca**](Home)\n\n</div>"
    ])

    out_path = os.path.join(wiki_dir, f"Volumen-{v_num:02d}.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))


def generar_home(wiki_dir: str, volumenes_info: list):
    """Genera la página principal del Wiki (Home.md)."""
    md = [
        "# 🚀 Lasers y Dragones: La Novela",
        "### *Saga Completa de Soles Muertos (Dead Suns)*",
        "",
        "> Bienvenido a la biblioteca digital online de **Lasers y Dragones: La Novela**, una ambiciosa adaptación literaria diegética de la campaña de rol de ciencia ficción espacial *Starfinder: Dead Suns*, emitida originalmente en el podcast costarricense homónimo.",
        "",
        "---",
        "",
        "## 🧭 Guía de Lectura Rápida",
        "",
        "Para disfrutar de la historia, puedes avanzar capítulo a capítulo directamente desde el navegador con la barra lateral o mediante los botones de navegación al inicio y final de cada página:",
        "",
        "* 🌟 **[Comenzar desde el inicio (Volumen 1: Prólogo)](Volumen-01-Prologo)**: Descubre el misterio de la Estación Absalón y el primer encuentro de la tripulación.",
        "* 👥 **[Dossier de Personajes de la Saga](Compendio-Dossier-Personajes)**: Conoce a Benrey Galway, Triel Istrav, Gerty, Marloc Boosmar y A.Xel 42.",
        "* 🪐 **[Atlas de Escenarios](Compendio-Indice-Escenarios)**: Desde la Espiga de Absalón hasta Eox, Apostae y las Nubes Arruinadas.",
        "* 📥 **[Descarga de Libros en PDF Maquetados](https://github.com/JordiNitrox/lasersydragones/tree/main/soles_muertos/libros_pdf)**: Versiones editoriales preparadas para imprenta o lectura en tablet.",
        "",
        "---",
        "",
        "## 📚 Índice General de Volúmenes",
        "",
        "| Vol. | Título de la Novela | Subtítulo / Arco | Episodios | Leer Online |",
        "| :---: | :--- | :--- | :---: | :---: |"
    ]

    for vol in volumenes_info:
        v_num = vol["numero"]
        meta = vol["meta"]
        paginas = vol["paginas"]

        # Enlace al primer capítulo
        primer = None
        for p in paginas:
            if p["tipo"] in ("prologo", "capitulo"):
                primer = p
                break

        enlace_leer = f"[Leer ▶️]({primer['page']})" if primer else "-"
        md.append(f"| **{v_num:02d}** | **[{meta['titulo']}](Volumen-{v_num:02d})** | *{meta['subtitulo']}* | {meta['episodios']} | {enlace_leer} |")

    md.extend([
        "",
        "---",
        "",
        "## 🌌 Compendio Maestro y Guía de Continuidad",
        "",
        "El universo de *Lasers y Dragones* cuenta con una densa red de relaciones corporativas, tecnología, amenazas alienígenas y saltos en el Drift:",
        "",
        "* 📅 **[Cronología Detallada de los 20 Volúmenes](Compendio-Cronologia-Volumenes)**",
        "* 👥 **[Dossier Completo de Personajes y Aliados](Compendio-Dossier-Personajes)**",
        "* 🪐 **[Índice Maestro de Escenarios y Estaciones](Compendio-Indice-Escenarios)**",
        "* 🏢 **[Corporaciones, Casas Nobles y Facciones](Compendio-Corporaciones-Facciones)**",
        "* 👾 **[Bestiario Estelar y Amenazas Biológicas](Compendio-Bestiario-Amenazas)**",
        "* 📐 **[Matriz de Continuidad y Líneas Temporales](Compendio-Matriz-Continuidad)**",
        "",
        "---",
        "",
        "<p align=\"center\"><i>Adaptación literaria comunitaria sin fines comerciales. Todas las marcas registradas de Starfinder pertenecen a Paizo Inc.</i></p>"
    ])

    out_path = os.path.join(wiki_dir, "Home.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))


def generar_sidebar(wiki_dir: str, volumenes_info: list):
    """Genera la barra lateral interactiva desplegable (_Sidebar.md)."""
    md = [
        "### 🚀 [Biblioteca Online](Home)",
        "",
        "---",
        "",
        "### 📚 Volúmenes de la Novela",
        ""
    ]

    for vol in volumenes_info:
        v_num = vol["numero"]
        meta = vol["meta"]
        paginas = vol["paginas"]

        md.append(f"<details>")
        md.append(f"<summary><b>Volumen {v_num}: {meta['titulo']}</b></summary>\n")
        md.append(f"* 📖 **[Índice del Volumen](Volumen-{v_num:02d})**")

        for p in paginas:
            icono = "📝" if p["tipo"] == "nota_editorial" else ("🌌" if p["tipo"] == "prologo" else ("📜" if p["tipo"] == "glosario" else "🔹"))
            md.append(f"* {icono} [{p['label']}]({p['page']})")

        md.append("</details>\n")

    md.extend([
        "---",
        "",
        "### 🌌 Compendio Maestro",
        "* 📅 [Cronología General](Compendio-Cronologia-Volumenes)",
        "* 👥 [Dossier de Personajes](Compendio-Dossier-Personajes)",
        "* 🪐 [Atlas de Escenarios](Compendio-Indice-Escenarios)",
        "* 🏢 [Facciones y Corporaciones](Compendio-Corporaciones-Facciones)",
        "* 👾 [Bestiario y Amenazas](Compendio-Bestiario-Amenazas)",
        "* 📐 [Matriz de Continuidad](Compendio-Matriz-Continuidad)",
        "",
        "---",
        "",
        "### 📥 Recursos",
        "* [📁 Libros PDF Maquetados](https://github.com/JordiNitrox/lasersydragones/tree/main/soles_muertos/libros_pdf)",
        "* [💻 Repositorio del Proyecto](https://github.com/JordiNitrox/lasersydragones)"
    ])

    out_path = os.path.join(wiki_dir, "_Sidebar.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))


def generar_footer(wiki_dir: str):
    """Genera el pie de página permanente del Wiki (_Footer.md)."""
    md = [
        "---",
        "<p align=\"center\">",
        "  <b>Lasers y Dragones: La Novela</b> · Adaptación literaria fan sin ánimo de lucro de la campaña <i>Dead Suns</i> (Starfinder / Paizo Inc.)<br>",
        "  Basada en las sesiones de rol de Roberto, Miguel, Irene, Juan Pablo y Sofía · Sincronizado automáticamente desde <a href=\"https://github.com/JordiNitrox/lasersydragones\">JordiNitrox/lasersydragones</a>",
        "</p>"
    ]
    out_path = os.path.join(wiki_dir, "_Footer.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))


def sincronizar_localmente(repo_dir: str):
    """Clona el repositorio wiki en un directorio temporal, lo actualiza y lo sube con credenciales locales."""
    import tempfile
    import subprocess

    wiki_url = "https://github.com/JordiNitrox/lasersydragones.wiki.git"
    print(f"[*] Modo local: Clonando repositorio wiki ({wiki_url})...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        clone_cmd = ["git", "clone", wiki_url, tmp_dir]
        res = subprocess.run(clone_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[!] Error al clonar el wiki: {res.stderr}")
            print("[!] Asegúrate de que el wiki está inicializado en GitHub y tienes permisos de escritura.")
            sys.exit(1)

        print("[*] Generando archivos del wiki...")
        generar_wiki(repo_dir, tmp_dir)

        # Comprobar cambios
        status = subprocess.run(["git", "status", "--porcelain"], cwd=tmp_dir, capture_output=True, text=True)
        if not status.stdout.strip():
            print("[✓] La wiki ya está al día. No hay cambios que subir.")
            return

        print("[*] Añadiendo y enviando cambios al wiki...")
        subprocess.run(["git", "add", "-A"], cwd=tmp_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Actualización automática de capítulos y compendio de la novela"], cwd=tmp_dir, check=True)
        push_res = subprocess.run(["git", "push"], cwd=tmp_dir, capture_output=True, text=True)
        if push_res.returncode == 0:
            print("[✓] ¡Wiki sincronizado y publicado con éxito en GitHub!")
        else:
            print(f"[!] Error al hacer push al wiki: {push_res.stderr}")


def main():
    parser = argparse.ArgumentParser(description="Actualizador del Wiki de GitHub para Lasers y Dragones")
    parser.add_argument("--wiki-dir", default="wiki_dist", help="Directorio destino para los archivos del wiki")
    parser.add_argument("--repo-dir", default=".", help="Ruta al repositorio principal de lasersydragones")
    parser.add_argument("--sync-local", action="store_true", help="Clona el wiki, genera los archivos y sube los cambios usando tus credenciales locales de git")
    args = parser.parse_args()

    repo_abs = os.path.abspath(args.repo_dir)

    if args.sync_local:
        sincronizar_localmente(repo_abs)
    else:
        generar_wiki(repo_abs, os.path.abspath(args.wiki_dir))


if __name__ == "__main__":
    main()

