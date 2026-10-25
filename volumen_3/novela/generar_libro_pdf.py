#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: La Roca del Drift' (Volumen 3)
Genera un documento HTML con estilos editoriales de libro y lo convierte a PDF
siguiendo las directrices técnicas del skill para garantizar marcadores PDF correctos
y números de página exactos en el Índice de Contenidos.
"""

import os
import re
import glob
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPS_DIR = os.path.join(BASE_DIR, "capitulos")
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_3_La_Roca_del_Drift.pdf")
HTML_OUTPUT = os.path.join(BASE_DIR, "libro_maquetado.html")
PROFILE_DIR = os.path.join(BASE_DIR, ".libreoffice_profile")

def inline_formatting(text):
    text = re.sub(r"\*\*\*([^\*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^\*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"_([^_]+)_", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text

def md_to_html(text, is_glossary=False):
    lines = text.strip().split("\n")
    html_lines = []
    in_list = False
    
    for line in lines:
        line_s = line.strip()
        
        # Saltos o separadores
        if line_s == "***" or line_s == "---":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<div class='divider'>✦ &nbsp; ◈ &nbsp; ✦</div>")
            continue
            
        # Encabezados
        if line_s.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = inline_formatting(line_s[2:].strip())
            html_lines.append(f"<h2 class='chapter-name'>{title}</h2>")
            continue
        elif line_s.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = inline_formatting(line_s[3:].strip())
            html_lines.append(f"<h3 class='section-title'>{title}</h3>")
            continue
        elif line_s.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = inline_formatting(line_s[4:].strip())
            if is_glossary:
                html_lines.append(f"<h4 class='subsection-title'>{title}</h4>")
            else:
                html_lines.append(f"<h3 class='subsection-title'>{title}</h3>")
            continue
            
        # Listas
        if line_s.startswith("- ") or line_s.startswith("* "):
            if not in_list:
                html_lines.append("<ul class='bullet-list'>")
                in_list = True
            item_text = line_s[2:].strip()
            item_html = inline_formatting(item_text)
            html_lines.append(f"<li>{item_html}</li>")
            continue
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
                
        # Citas
        if line_s.startswith("> "):
            quote_text = inline_formatting(line_s[2:].strip())
            html_lines.append(f"<blockquote class='quote'>{quote_text}</blockquote>")
            continue
            
        # Párrafos normales
        if line_s:
            p_html = inline_formatting(line_s)
            html_lines.append(f"<p>{p_html}</p>")
            
    if in_list:
        html_lines.append("</ul>")
        
    return "\n".join(html_lines)

# Metadata de capítulos para el índice
TOC_ITEMS = [
    {
        "id": "nota_editorial",
        "search_key": "Nota Editorial e Introducción",
        "title": "Nota Editorial e Introducción",
        "sub": "Contexto y créditos del podcast original"
    },
    {
        "id": "prologo",
        "search_key": "Prólogo: El Abismo del Asteroide",
        "title": "Prólogo: El Abismo del Asteroide",
        "sub": "Transición desde el Acreon y descenso al pozo vertical"
    },
    {
        "id": "cap_23",
        "search_key": "Capítulo 23: Cuentas Claras",
        "title": "Capítulo 23: Cuentas Claras",
        "sub": "Basado en el Episodio 23 · Descenso en gravedad cero, la emboscada de Clara-247 y la caída de la mercenaria"
    },
    {
        "id": "cap_24",
        "search_key": "Capítulo 24: Problemas Tentaculares",
        "title": "Capítulo 24: Problemas Tentaculares",
        "sub": "Basado en el Episodio 24 · Placas luminosas alienígenas, el primer oficial Aravat zombi del vacío y trompos en gravedad cero"
    },
    {
        "id": "cap_25",
        "search_key": "Capítulo 25: Voces en la Oscuridad",
        "title": "Capítulo 25: Voces en la Oscuridad",
        "sub": "Basado en el Episodio 25 · Los zombis del vacío de Orin y la capitana Alhana, el portal pre-Brecha y los susurros de la roca"
    },
    {
        "id": "cap_26",
        "search_key": "Capítulo 26: La Redención del Mago",
        "title": "Capítulo 26: La Redención del Mago",
        "sub": "Basado en el Episodio 26 · El Driftdead de Moriko Nash, los proyectiles mágicos de Marloc y el acertijo de los guijarros"
    },
    {
        "id": "cap_27",
        "search_key": "Capítulo 27: Arqueología de Combate",
        "title": "Capítulo 27: Arqueología de Combate",
        "sub": "Basado en el Episodio 27 · El autómata ancestral de seguridad, el dron centinela y la momia de Moriko Nash"
    },
    {
        "id": "cap_28",
        "search_key": "Capítulo 28: La Última Voluntad",
        "title": "Capítulo 28: La Última Voluntad",
        "sub": "Basado en el Episodio 28 · El testamento de Moriko Nash, el hangar de la Estrella Errante y el despertar del Garaggakal"
    },
    {
        "id": "cap_29",
        "search_key": "Capítulo 29: El Coleccionista",
        "title": "Capítulo 29: El Coleccionista: La Bestia del Drift",
        "sub": "Basado en el Episodio 29 · Clímax contra el Garaggakal, el disparo letal de Axel y la sala de trofeos óseos"
    },
    {
        "id": "cap_30",
        "search_key": "Capítulo 30: Locademia de Pilotos",
        "title": "Capítulo 30: Locademia de Pilotos: El Núcleo Revelado",
        "sub": "Basado en el Episodio 30 · La IA de la Estrella Errante, huida al espacio real y la emboscada de la Flota de los Cuerpos"
    },
    {
        "id": "cap_31",
        "search_key": "Capítulo 31: El Precio de la Fama",
        "title": "Capítulo 31: El Precio de la Fama",
        "sub": "Basado en el Episodio 31 · Llegada triunfal al Muelle 94, entrevista de Carne Yac, fiesta en Las Lunas y mensajes del corazón"
    },
    {
        "id": "cap_32",
        "search_key": "Capítulo 32: Padres, Hermanas y Productores",
        "title": "Capítulo 32: Padres, Hermanas y Productores",
        "sub": "Basado en el Episodio 32 · Presiones familiares y productores de Benray, el secreto del pirata Keiden Ashton y el legado de Ambrose Boosmar"
    },
    {
        "id": "cap_33",
        "search_key": "Capítulo 33: ¡Piedra para Todos!",
        "title": "Capítulo 33: ¡Piedra para Todos!: La Gran Resolución",
        "sub": "Basado en el Episodio 33 · El arbitraje del tribunal kasatha, victoria de Hardscrabble, homenaje en El Pulmón Negro y un nuevo horizonte"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "Facciones, la Roca del Drift, la Flota de los Cuerpos, Bestiario y Héroes de Absalón"
    }
]

def generate_html(page_numbers=None):
    if page_numbers is None:
        page_numbers = {item["id"]: 0 for item in TOC_ITEMS}
        
    chapter_files = sorted(glob.glob(os.path.join(CAPS_DIR, "*.md")))
    chapters_data = []
    
    for f in chapter_files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            first_line = content.strip().split("\n")[0]
            raw_title = first_line.replace("#", "").strip()
            remaining_content = "\n".join(content.strip().split("\n")[1:])
            html_content = md_to_html(remaining_content, is_glossary=False)
            chapters_data.append({
                "file": os.path.basename(f),
                "raw_title": raw_title,
                "html": html_content
            })
            
    # Leer anexo de personajes
    glossary_path = os.path.join(BASE_DIR, "GLOSARIO_Y_PERSONAJES.md")
    glossary_html = ""
    if os.path.exists(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as fp:
            glossary_raw = fp.read()
            remaining_glossary = "\n".join(glossary_raw.strip().split("\n")[1:])
            glossary_html = md_to_html(remaining_glossary, is_glossary=True)

    # Filas de la tabla de contenidos
    toc_rows = []
    for item in TOC_ITEMS:
        pg = page_numbers.get(item["id"], "--")
        toc_rows.append(f"""    <tr>
      <td>
        <div class="toc-title">{item['title']}</div>
        <div class="toc-sub">{item['sub']}</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">{pg}</td>
    </tr>""")
    toc_rows_html = "\n".join(toc_rows)

    html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Lasers y Dragones: La Roca del Drift</title>
<style>
  @page {{
    size: A4;
    margin: 25mm 22mm 25mm 22mm;
  }}
  
  body {{
    font-family: 'Liberation Serif', 'Georgia', 'Palatino Linotype', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}
  
  .section-heading-main {{
    font-size: 22pt;
    text-align: center;
    color: #0b1a30;
    margin-top: 0;
    margin-bottom: 25px;
    border-bottom: 2px solid #b8860b;
    padding-bottom: 10px;
    page-break-before: always;
    break-before: page;
  }}

  /* Índice de contenidos */
  .toc-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
  }}
  
  .toc-table td {{
    padding: 5px 3px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 10pt;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 8.8pt;
    color: #718096;
    font-style: italic;
    line-height: 1.25;
  }}
  
  /* Título de Capítulo con salto de página infalible en LibreOffice */
  h2.chapter-name {{
    page-break-before: always;
    break-before: page;
    font-size: 22pt;
    color: #0b1a30;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 25px;
    line-height: 1.3;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 15px;
  }}
  
  .chap-sub {{
    font-size: 18pt;
    font-style: italic;
    color: #2b6cb0;
    font-weight: normal;
  }}
  
  h3.section-title {{
    font-size: 14pt;
    color: #2b6cb0;
    margin-top: 25px;
    margin-bottom: 12px;
    border-bottom: 1px dashed #e2e8f0;
    padding-bottom: 4px;
    font-family: 'Liberation Serif', serif;
  }}
  
  h3.subsection-title {{
    font-size: 12.5pt;
    color: #2d3748;
    margin-top: 20px;
    margin-bottom: 10px;
    font-family: 'Liberation Serif', serif;
  }}

  h4.subsection-title {{
    font-size: 11.5pt;
    color: #1a365d;
    margin-top: 16px;
    margin-bottom: 6px;
    font-weight: bold;
    font-family: 'Liberation Serif', serif;
  }}
  
  p {{
    text-align: justify;
    text-justify: inter-word;
    margin: 0 0 12px 0;
    text-indent: 1.5em;
  }}
  
  p:first-of-type, .divider + p, .section-title + p, .subsection-title + p {{
    text-indent: 0;
  }}
  
  .divider {{
    text-align: center;
    margin: 25px 0;
    color: #a0aec0;
    font-size: 10pt;
    letter-spacing: 6px;
  }}
  
  .bullet-list {{
    margin: 12px 0 15px 25px;
    padding: 0;
  }}
  
  .bullet-list li {{
    margin-bottom: 6px;
    text-align: justify;
  }}
  
  .quote {{
    margin: 18px 25px;
    padding: 10px 18px;
    border-left: 3px solid #b8860b;
    background: #f7fafc;
    font-style: italic;
    color: #4a5568;
  }}
</style>
</head>
<body>

  <!-- 1. PORTADA EDITORIAL HOMOGÉNEA -->
  <div style="text-align: center; padding: 40px 10px; margin: 0 auto; max-width: 500px;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 11pt; letter-spacing: 5px; text-transform: uppercase; color: #2b6cb0; margin: 40px 0 20px 0; text-indent: 0;">
      Ópera Espacial · Universo Starfinder
    </p>
    
    <hr style="border: none; border-top: 2px solid #1a365d; width: 60%; margin: 25px auto;">
    
    <div style="font-size: 30pt; font-weight: bold; color: #0b1a30; margin: 20px 0 10px 0; letter-spacing: 2px; text-align: center;">
      LASERS Y DRAGONES
    </div>
    
    <div style="font-size: 20pt; font-style: italic; color: #b8860b; margin: 10px 0 20px 0; text-align: center;">
      La Roca del Drift
    </div>
    
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 20px auto;">
    
    <div style="font-size: 14pt; color: #2b6cb0; margin: 25px 0;">
      ✦ &nbsp; ◈ &nbsp; ✦
    </div>
    
    <p style="font-size: 11pt; line-height: 1.6; color: #4a5568; margin: 30px auto; max-width: 420px; text-indent: 0; text-align: center;">
      Una adaptación novelada de la campaña oficial <em>Dead Suns</em> (Soles Muertos), inspirada en las sesiones de rol en vivo del podcast <strong>Lasers y Dragones</strong>.
    </p>
    
    <hr style="border: none; border-top: 1px solid #cbd5e0; width: 80%; margin: 50px auto 20px auto;">
    
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 10pt; letter-spacing: 3px; text-transform: uppercase; color: #1a365d; margin: 0; text-indent: 0; text-align: center;">
      Volumen III · El Enigma Ancestral
    </p>
  </div>

  <!-- 2. NOTA EDITORIAL E INTRODUCCIÓN -->
  <h2 class="section-heading-main" style="margin-top: 5px; margin-bottom: 12px; font-size: 19pt; padding-bottom: 6px;">Nota Editorial e Introducción</h2>
  
  <p style="font-size: 9pt; line-height: 1.35; margin-bottom: 5px;">La presente obra constituye el tercer volumen de la novelización de las sesiones reales de juego de rol de mesa (<em>actual play</em>) emitidas en el podcast costarricense <strong>Lasers y Dragones</strong>, correspondiente a los episodios 23 al 33.</p>
  
  <p style="font-size: 9pt; line-height: 1.35; margin-bottom: 5px;">Con este volumen culmina el primer gran arco argumental de la campaña oficial <strong>Dead Suns (Soles Muertos)</strong> de <strong>Starfinder</strong> (publicado por <em>Paizo Inc.</em>), correspondiente a la aventura <em>Incidente en la Estación Absalón</em>. Narra el descenso a la Roca del Drift, el hallazgo de una civilización anterior a la Brecha, la lucha contra el vampírico <em>Garaggakal</em>, el legado de Moriko Nash y el apoteósico triunfo judicial en Absalón.</p>
  
  <div style="margin: 6px auto; max-width: 500px;">
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 5px auto;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 8.5pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 5px 0; text-indent: 0; text-align: center;">
      ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
      <strong style="color: #1a365d;">Roberto:</strong> GM / Gerty &nbsp;|&nbsp; <strong style="color: #1a365d;">Miguel:</strong> Benray Galway <em>(Emisario)</em>
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
      <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc <em>(Tecnomante)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa)</em>
    </p>
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 5px auto;">
  </div>
  
  <p style="font-size: 9pt; line-height: 1.35; margin-bottom: 5px;">El propósito de esta novelización es transformar la espontaneidad de la mesa de rol en una experiencia literaria inmersiva, cinematográfica y coherente, respetando con fidelidad a los protagonistas, el humor espacial y la evolución del canon.</p>

  <table style="width: 100%; margin: 8px 0 0 0; border: 1px solid #cbd5e0; background-color: #f8fafc; border-collapse: collapse; page-break-inside: avoid; break-inside: avoid;">
    <tr>
      <td style="padding: 8px 12px; font-size: 7.5pt; color: #4a5568; line-height: 1.35; text-align: justify; border: none;">
        <p style="margin: 0 0 4px 0; text-indent: 0; font-weight: bold; color: #1a365d; font-size: 8pt; text-transform: uppercase; letter-spacing: 1px; text-align: center;">
          Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución
        </p>
        <p style="margin: 0 0 4px 0; text-indent: 0;">
          Esta obra literaria y sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de <strong>Paizo Inc.</strong>, utilizados bajo la <em>Política de Uso Comunitario de Paizo</em> (<a href="https://paizo.com/communityuse" style="color: #2b6cb0; text-decoration: none;">paizo.com/communityuse</a>). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de <em>Starfinder</em> y <em>Pathfinder</em>, visite <a href="https://paizo.com" style="color: #2b6cb0; text-decoration: none;">paizo.com</a>.
        </p>
        <p style="margin: 0; text-indent: 0;">
          Asimismo, esta novelización constituye un tributo no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense <strong>Lasers y Dragones</strong>. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: <strong>Roberto</strong> (Game Master y Gerty), <strong>Miguel</strong> (Benray Galway), <strong>Irene</strong> (Triel Istrav), <strong>Juan Pablo</strong> (Marloc Boosmar) y <strong>Sofía</strong> (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
        </p>
      </td>
    </tr>
  </table>

  <!-- 3. ÍNDICE DE CONTENIDOS -->
  <h2 class="section-heading-main">Índice de Contenidos</h2>
  
  <table class="toc-table">
{toc_rows_html}
  </table>
"""

    # Agregar capítulos
    for ch in chapters_data:
        raw = ch['raw_title']
        if ":" in raw:
            prefix, subtitle = raw.split(":", 1)
            header_html = f"{prefix.strip()}: <br><span class=\"chap-sub\">{subtitle.strip()}</span>"
        else:
            header_html = raw
        html_doc += f"""
  <h2 class="chapter-name">{header_html}</h2>
  <div class="chapter-body">
    {ch['html']}
  </div>
"""

    # Agregar anexo si existe
    if glossary_html:
        html_doc += f"""
  <h2 class="chapter-name">Anexo Especial: <br><span class="chap-sub">Dossier de Personajes y Glosario</span></h2>
  <div class="chapter-body">
    {glossary_html}
  </div>
"""

    html_doc += """
</body>
</html>
"""
    with open(HTML_OUTPUT, "w", encoding="utf-8") as fp:
        fp.write(html_doc)
    return HTML_OUTPUT

def run_libreoffice():
    user_prof = f"file://{PROFILE_DIR}"
    cmd = [
        "libreoffice",
        f"-env:UserInstallation={user_prof}",
        "--headless",
        "--convert-to",
        "pdf",
        HTML_OUTPUT
    ]
    res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Error al compilar con LibreOffice: {res.stderr}")
    gen_pdf = os.path.join(BASE_DIR, "libro_maquetado.pdf")
    if os.path.exists(gen_pdf):
        if os.path.exists(PDF_OUTPUT):
            os.remove(PDF_OUTPUT)
        os.rename(gen_pdf, PDF_OUTPUT)
    return PDF_OUTPUT

def extract_page_numbers_from_pdf(pdf_path):
    """
    Usa pdftotext para encontrar en qué página física aparece cada h2.chapter-name
    evitando falsos positivos dentro de la propia tabla del índice de contenidos.
    """
    res = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
    pages = res.stdout.split("\x0c") # Form feed separa páginas
    
    found_pages = {}
    
    # Nota Editorial siempre está antes del índice (página 2)
    for idx, page_text in enumerate(pages[:3]):
        if "nota editorial e introducción" in page_text.lower():
            found_pages["nota_editorial"] = idx + 1
            break
            
    # Para el resto de capítulos y anexo, buscamos desde la página donde terminan los preliminares
    # buscando que el título aparezca en el encabezado de la página (primeras 6 líneas)
    for item in TOC_ITEMS:
        if item["id"] == "nota_editorial":
            continue
        key = item["search_key"].lower()
        # Buscar desde la página 4 en adelante (índice está en pág. 3)
        for idx in range(3, len(pages)):
            lines = [l.strip() for l in pages[idx].split("\n") if l.strip()][:6]
            header_text = " ".join(lines).lower()
            if key in header_text:
                found_pages[item["id"]] = idx + 1
                break
                
    # Fallback si alguno no fue detectado en las primeras líneas
    for item in TOC_ITEMS:
        if item["id"] not in found_pages:
            key = item["search_key"].lower()
            for idx in range(3, len(pages)):
                if key in pages[idx].lower():
                    found_pages[item["id"]] = idx + 1
                    break
                    
    return found_pages

def build_book():
    print("=== Compilación de Volumen 3: La Roca del Drift ===")
    
    # Pase 1: Generación preliminar para calcular páginas reales
    print("Paso 1: Generando HTML preliminar...")
    generate_html()
    print("Paso 2: Compilando PDF preliminar con LibreOffice...")
    run_libreoffice()
    
    print("Paso 3: Extrayendo paginación real de capítulos con pdftotext...")
    pages = extract_page_numbers_from_pdf(PDF_OUTPUT)
    print("Páginas detectadas:")
    for item in TOC_ITEMS:
        print(f"  - {item['title']}: pág. {pages.get(item['id'], '??')}")
        
    # Pase 2: Regeneración con la tabla de contenidos exacta
    print("Paso 4: Regenerando HTML con el Índice de Contenidos final...")
    generate_html(page_numbers=pages)
    
    print("Paso 5: Compilación final del PDF...")
    final_pdf = run_libreoffice()
    
    # Validación final de tamaño
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡Libro Volumen 3 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
