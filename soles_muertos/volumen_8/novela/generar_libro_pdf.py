#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: Mundos Fragmentados II: Las Cortes Cadavéricas de Eox' (Volumen 8)
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
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_8_Mundos_Fragmentados_II_Las_Cortes_Cadavericas_de_Eox.pdf")
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
        "sub": "Contexto, créditos de la mesa y canon de Paizo Inc."
    },
    {
        "id": "prologo",
        "search_key": "Prólogo: El Abrazo de la Ceniza",
        "title": "Prólogo: El Abrazo de la Ceniza",
        "sub": "Desde la Diáspora y Ceres X hacia las brumas de la Línea de Vida"
    },
    {
        "id": "cap_1",
        "search_key": "Capítulo 1: Promesas",
        "title": "Capítulo 1: Promesas",
        "sub": "Basado en el Episodio 89 · La clemencia de Radavox en Ceres X y el secreto desgarrador de Marloc"
    },
    {
        "id": "cap_2",
        "search_key": "Capítulo 2: Más Allá de las Estrellas",
        "title": "Capítulo 2: Más Allá de las Estrellas",
        "sub": "Basado en el Episodio 90 · El Ojo de Cuyo para Benrey y el beso cósmico con Ángela en la Deriva"
    },
    {
        "id": "cap_3",
        "search_key": "Capítulo 3: La Máscara de Hueso y la Línea de Vida",
        "title": "Capítulo 3: La Máscara de Hueso y la Línea de Vida",
        "sub": "Basado en el Episodio 91 · Holocinta de Corvis Studios, llegada a Eox y persecución a la Necrópolis de Zano"
    },
    {
        "id": "cap_4",
        "search_key": "Capítulo 4: Trámites Muertocráticos",
        "title": "Capítulo 4: Trámites Muertocráticos",
        "sub": "Basado en el Episodio 92 · La burócrata Waneda Trux, galletas de sombra y la fábrica de carne viva"
    },
    {
        "id": "cap_5",
        "search_key": "Capítulo 5: Antes Muerta que Sencilla",
        "title": "Capítulo 5: Antes Muerta que Sencilla",
        "sub": "Basado en el Episodio 93 · Boutique de Jacqueline, el asalto al apartamento de Greatel y la parálisis de Marloc"
    },
    {
        "id": "cap_6",
        "search_key": "Capítulo 6: La Debilidad de la Carne",
        "title": "Capítulo 6: La Debilidad de la Carne",
        "sub": "Basado en el Episodio 94 · El diario en piel de Harpingdex, la caja fuerte 0212 y la emboscada Nihili"
    },
    {
        "id": "cap_7",
        "search_key": "Capítulo 7: La Pista del Bálsamo y los Salones de los Vivos",
        "title": "Capítulo 7: La Pista del Bálsamo y los Salones de los Vivos",
        "sub": "Basado en el Episodio 95 · La caída del segundo Nihili, la pista del bálsamo CC y la irrupción de Gallito Peligro"
    },
    {
        "id": "cap_8",
        "search_key": "Capítulo 8: El Café Calavera",
        "title": "Capítulo 8: El Café Calavera",
        "sub": "Basado en el Episodio 96 · El show de Gallito, los vampiros Dio y Mircala y el monje lacunar Coin"
    },
    {
        "id": "cap_9",
        "search_key": "Capítulo 9: No Hay Respeto",
        "title": "Capítulo 9: No Hay Respeto",
        "sub": "Basado en el Episodio 97 · El brindis de sangre, el desafío en llamas de Benrey y la entrada a la fosa de Zo!"
    },
    {
        "id": "cap_10",
        "search_key": "Capítulo 10: Como Caído del Cielo",
        "title": "Capítulo 10: Como Caído del Cielo",
        "sub": "Basado en el Episodio 98 · Exterminio de ciber-zombis, el Golem de Neutrones y la nave de asalto furtiva"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial: Dossier de Personajes y Glosario",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "Eox, los Necrovitas, la Flota de Cadáveres, Zo! Media y Héroes de la Saga"
    }
]

def generate_html(page_numbers=None):
    if page_numbers is None:
        page_numbers = {item["id"]: 0 for item in TOC_ITEMS}
        
    chapter_files = sorted(glob.glob(os.path.join(CAPS_DIR, "*.md")))
    chapters_data = []
    
    for f in chapter_files:
        fname = os.path.basename(f)
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            
        if fname == "00_nota_editorial.md":
            continue
            
        first_line = content.strip().split("\n")[0]
        raw_title = first_line.replace("#", "").strip()
        remaining_content = "\n".join(content.strip().split("\n")[1:])
        html_content = md_to_html(remaining_content, is_glossary=False)
        chapters_data.append({
            "file": fname,
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
<title>Lasers y Dragones: Mundos Fragmentados II: Las Cortes Cadavéricas de Eox</title>
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
    margin: 4px 0;
  }}
  
  .toc-table td {{
    padding: 2px 3px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 8.8pt;
    line-height: 1.15;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 7.8pt;
    color: #718096;
    font-style: italic;
    line-height: 1.1;
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
  
  p:first-of-type, .divider + p, .section-title + p, .subsection-title + p, blockquote + p {{
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
  
  code {{
    font-family: 'Liberation Mono', monospace;
    font-size: 9.5pt;
    background: #edf2f7;
    padding: 2px 4px;
    border-radius: 3px;
  }}
</style>
</head>
<body>

<!-- PÁGINA 1: PORTADA EDITORIAL HOMOGÉNEA -->
<div style="text-align: center; padding: 40px 10px; margin: 0 auto; max-width: 500px;">
  <p style="font-family: 'Liberation Sans', sans-serif; font-size: 11pt; letter-spacing: 5px; text-transform: uppercase; color: #2b6cb0; margin: 40px 0 20px 0; text-indent: 0;">
    Ópera Espacial · Universo Starfinder
  </p>
  
  <hr style="border: none; border-top: 2px solid #1a365d; width: 60%; margin: 25px auto;">
  
  <div style="font-size: 30pt; font-weight: bold; color: #0b1a30; margin: 20px 0 10px 0; letter-spacing: 2px; text-align: center;">
    LASERS Y DRAGONES
  </div>
  
  <div style="font-size: 20pt; font-style: italic; color: #b8860b; margin: 10px 0 20px 0; text-align: center;">
    Mundos Fragmentados II
  </div>
  
  <div style="font-size: 13pt; font-weight: bold; color: #2b6cb0; margin: 0 0 20px 0; letter-spacing: 1.5px; text-transform: uppercase; text-align: center;">
    Las Cortes Cadavéricas de Eox
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
    VOLUMEN VIII · EL CAMINO FURIBUNDO: LAS CORTES CADAVÉRICAS DE EOX
  </p>
</div>

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 2 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 2: NOTA EDITORIAL E INTRODUCCIÓN -->
<div style="padding: 10px 0;">
  <h2 class="section-heading-main" style="page-break-before: avoid; break-before: avoid; margin-bottom: 12px; padding-bottom: 6px; font-size: 18pt;">
    Nota Editorial e Introducción
  </h2>
  
  <p style="text-indent: 0; font-size: 9.5pt; line-height: 1.45; margin-bottom: 8px;">
    El presente volumen, <strong>El Camino Furibundo: Las Cortes Cadavéricas de Eox</strong>, constituye la octava entrega de la saga novelada de <em>Lasers y Dragones</em> y adapta de forma integral los acontecimientos narrados en los <strong>Episodios 89 al 98</strong> de la campaña de rol en vivo. Tras la dolorosa victoria en la Diáspora y el asteroide Ceres X, la tripulación de la <em>Estrella Errante</em> viaja a las entrañas del planeta necrótico Eox para seguir la pista de la misteriosa investigadora renegada de la Flota Cadáver y su conexión con la Devoradora de Soles.
  </p>
  
  <p style="text-indent: 0; font-size: 9.5pt; line-height: 1.45; margin-bottom: 8px;">
    Esta obra es un trabajo de adaptación literaria independiente sin fines lucrativos que busca recrear la inmersión, el drama, la tensión táctica y el humor característico surgidos alrededor de la mesa de juego, transformando las sesiones orales en una experiencia narrativa de ópera espacial de ritmo ágil y maduro.
  </p>

  <!-- MESA DE JUEGO ORIGINAL -->
  <div style="margin: 8px auto; max-width: 500px;">
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 6px auto;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 8.5pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 6px 0; text-indent: 0; text-align: center;">
      ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
    </p>
    <p style="margin: 3px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
      <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (y la voz del meca <strong>Gerty</strong>) &nbsp;|&nbsp; <strong style="color: #1a365d;">Miguel:</strong> Benrey Galway <em>(Emisario Ysoki)</em>
    </p>
    <p style="margin: 3px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
      <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc Boosmar <em>(Tecnomante Humano)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa Androide)</em>
    </p>
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 6px auto;">
  </div>

  <!-- AVISO DE PAIZO Y ATRIBUCIÓN -->
  <table style="width: 100%; margin: 10px 0 0 0; border: 1px solid #cbd5e0; background-color: #f8fafc; border-collapse: collapse; page-break-inside: avoid; break-inside: avoid;">
    <tr>
      <td style="padding: 8px 12px; font-size: 7.5pt; color: #4a5568; line-height: 1.35; text-align: justify; border: none;">
        <p style="margin: 0 0 4px 0; text-indent: 0; font-weight: bold; color: #1a365d; font-size: 8pt; text-transform: uppercase; letter-spacing: 1px; text-align: center;">
          Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución
        </p>
        <p style="margin: 0 0 4px 0; text-indent: 0;">
          Esta obra literaria y sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de <strong>Paizo Inc.</strong>, utilizados bajo la <em>Política de Uso Comunitario de Paizo</em> (<a href="https://paizo.com/communityuse" style="color: #2b6cb0; text-decoration: none;">paizo.com/communityuse</a>). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de <em>Starfinder</em> y <em>Pathfinder</em>, visite <a href="https://paizo.com" style="color: #2b6cb0; text-decoration: none;">paizo.com</a>.
        </p>
        <p style="margin: 0; text-indent: 0;">
          Asimismo, esta novelización constituye un tributo no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense <strong>Lasers y Dragones</strong>. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: <strong>Roberto</strong> (Game Master y Gerty), <strong>Miguel</strong> (Benrey Galway), <strong>Irene</strong> (Triel Istrav), <strong>Juan Pablo</strong> (Marloc Boosmar) y <strong>Sofía</strong> (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
        </p>
      </td>
    </tr>
  </table>
</div>

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 3 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 3: ÍNDICE DE CONTENIDOS -->
<div style="padding: 10px 0;">
  <h2 class="section-heading-main" style="page-break-before: avoid; break-before: avoid; margin-bottom: 8px; padding-bottom: 4px; font-size: 16pt;">
    Índice de Contenidos
  </h2>
  
  <table class="toc-table">
{toc_rows_html}
  </table>
</div>

<!-- CONTENIDO PRINCIPAL DEL LIBRO -->
"""

    for ch in chapters_data:
        html_doc += f"""
<div class="chapter-container">
  <h2 class="chapter-name">{ch['raw_title']}</h2>
{ch['html']}
</div>
"""

    if glossary_html:
        html_doc += f"""
<div class="glossary-container">
  <h2 class="chapter-name">Anexo Especial: Dossier de Personajes y Glosario</h2>
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
    print("=== Compilación de Volumen 8: Mundos Fragmentados II: Las Cortes Cadavéricas de Eox ===")
    
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
    
    # Sincronización automática con la biblioteca centralizada si existe
    central_pdf_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "libros_pdf"))
    if os.path.exists(central_pdf_dir):
        central_pdf_path = os.path.join(central_pdf_dir, "08_Lasers_y_Dragones_Volumen_8_Mundos_Fragmentados_II_Las_Cortes_Cadavericas_de_Eox.pdf")
        import shutil
        shutil.copy2(final_pdf, central_pdf_path)
        print(f"Biblioteca centralizada sincronizada: {central_pdf_path}")

    # Validación final de tamaño
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡Libro Volumen 8 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
