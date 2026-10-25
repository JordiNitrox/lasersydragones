#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: Las Torres de Qabarat' (Volumen 4)
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
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_4_Las_Torres_de_Qabarat.pdf")
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
        "sub": "Contexto, créditos y canon del podcast original"
    },
    {
        "id": "prologo",
        "search_key": "Prólogo: Las Sombras del Triunfo",
        "title": "Prólogo: Las Sombras del Triunfo",
        "sub": "El eco de la victoria en Absalón, la nueva nave y los enigmas que aguardan en la noche"
    },
    {
        "id": "cap_34",
        "search_key": "Capítulo 34: Historia de Dos Boosmar",
        "title": "Capítulo 34: Historia de Dos Boosmar",
        "sub": "Basado en el Episodio 34 · El Arcanamirium de Absalón, Ambrose Boosmar y el enigma de Aucturn"
    },
    {
        "id": "cap_35",
        "search_key": "Capítulo 35: Evento Horizonte",
        "title": "Capítulo 35: Evento Horizonte",
        "sub": "Basado en el Episodio 35 · El zoco kasatha y el pasado de Axel, el velatorio de Marlene y el concierto de Syd Velch"
    },
    {
        "id": "cap_36",
        "search_key": "Capítulo 36: El Mosh de la Rata",
        "title": "Capítulo 36: El Mosh de la Rata",
        "sub": "Basado en el Episodio 36 · Disonancia psíquica, el mosh pit de Benray y la batalla en la arena"
    },
    {
        "id": "cap_37",
        "search_key": "Capítulo 37: El Muerto al Hoyo",
        "title": "Capítulo 37: El Muerto al Hoyo...",
        "sub": "Basado en el Episodio 37 · El funeral en el Jardín de Cenizas, el dolor de dos mundos y el anillo de Ángela"
    },
    {
        "id": "cap_38",
        "search_key": "Capítulo 38: ...y el Vivo al Bollo",
        "title": "Capítulo 38: ...y el Vivo al Bollo",
        "sub": "Basado en el Episodio 38 · Recepción en Club 13, despedidas en el Muelle 94 y desamarre de la Estrella Errante"
    },
    {
        "id": "cap_39",
        "search_key": "Capítulo 39: Grandes Mentes de Qabarat",
        "title": "Capítulo 39: Grandes Mentes de Qabarat",
        "sub": "Basado en el Episodio 39 · Convivencia en el Drift, la Legión del Fuego en el Cielo y la Ciudad Esmeralda"
    },
    {
        "id": "cap_40",
        "search_key": "Capítulo 40: Mentes Monstruosas",
        "title": "Capítulo 40: Mentes Monstruosas",
        "sub": "Basado en el Episodio 40 · La Universidad de Qabarat, la decana Muhali y el despacho de Solstarni"
    },
    {
        "id": "cap_41",
        "search_key": "Capítulo 41: La Pequeña Cocinita de los Horrores",
        "title": "Capítulo 41: La Pequeña Cocinita de los Horrores",
        "sub": "Basado en el Episodio 41 · La cantina Los Cinco Arcos, Tuwanas En y la emboscada de la Legión"
    },
    {
        "id": "cap_42",
        "search_key": "Capítulo 42: Rápidos y Furiosos",
        "title": "Capítulo 42: Rápidos y Furiosos: Castrovel Drift",
        "sub": "Basado en el Episodio 42 · Persecución urbana a bordo del compacto, desafío en triaxiano y el warwagon"
    },
    {
        "id": "cap_43",
        "search_key": "Capítulo 43: Pobres Piratas en Desgracia",
        "title": "Capítulo 43: Pobres Piratas en Desgracia",
        "sub": "Basado en el Episodio 43 · Refugio corsario con La Venganza, la leyenda de Keiden Ashton y el secreto de Triel"
    },
    {
        "id": "cap_44",
        "search_key": "Capítulo 44: Annabelle y el Conflicto Final",
        "title": "Capítulo 44: Annabelle y el Conflicto Final",
        "sub": "Basado en el Episodio 44 · Contrato con Muhali, el expolio de Annabelle en los archivos y las runas de la roca"
    },
    {
        "id": "cap_45",
        "search_key": "Capítulo 45: Ahora Estás Pensando con Portales",
        "title": "Capítulo 45: Ahora Estás Pensando con Portales",
        "sub": "Basado en el Episodio 45 · El portal de Aiakos, el infierno de Turhalu, Kaeral Waft y los recuerdos de Axel"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "Facciones, Castrovel, la Legión del Fuego en el Cielo, Capitanes Libres y Héroes del Pacto"
    }
]

def generate_html(page_numbers=None):
    if page_numbers is None:
        page_numbers = {item["id"]: 0 for item in TOC_ITEMS}
        
    chapter_files = sorted(glob.glob(os.path.join(CAPS_DIR, "*.md")))
    chapters_data = []
    editorial_html = ""
    
    for f in chapter_files:
        fname = os.path.basename(f)
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            
        if fname == "00_nota_editorial.md":
            # Extraer contenido para la sección editorial previa
            remaining = "\n".join(content.strip().split("\n")[1:])
            editorial_html = md_to_html(remaining, is_glossary=False)
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
<title>Lasers y Dragones: Las Torres de Qabarat</title>
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
    margin: 10px 0;
  }}
  
  .toc-table td {{
    padding: 4px 3px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 9.5pt;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 8.5pt;
    color: #718096;
    font-style: italic;
    line-height: 1.2;
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
      Las Torres de Qabarat
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
      Volumen IV · El Horizonte Esmeralda
    </p>
  </div>

  <!-- 2. NOTA EDITORIAL E INTRODUCCIÓN -->
  <h2 class="section-heading-main" style="margin-bottom: 18px;">Nota Editorial e Introducción</h2>
  
  <p style="margin-bottom: 10px;">La presente obra constituye el cuarto volumen de la novelización de las sesiones reales de juego de rol de mesa (<em>actual play</em>) emitidas en el podcast costarricense <strong>Lasers y Dragones</strong>, correspondiente a los episodios 34 al 45.</p>
  
  <p style="margin-bottom: 10px;">En este volumen se inicia el segundo gran arco argumental de la campaña oficial <strong>Dead Suns (Soles Muertos)</strong> del juego de rol <strong>Starfinder</strong> (creado y publicado por <em>Paizo Inc.</em>), correspondiente a la aventura <em>El Templo de los Doce</em> (<em>Temple of the Twelve</em>). Tras la apoteósica resolución del arbitraje en Absalón, las revelaciones de la Roca del Drift guían a la tripulación hacia el salvaje planeta Castrovel. Antes de zarpar, los aventureros saldan cuentas con su pasado en el Arcanamirium, sobreviven a una noche legendaria de rock espacial con Syd Velch y despiden con honores a Marlene Boosmar. Ya en Castrovel, la expedición se adentrará en las intrigas de la Universidad de Qabarat, persecuciones a toda velocidad en aerodeslizadores y el asedio a las ruinas ancestrales ocultas en la selva lashunta.</p>
  
  <p style="margin-bottom: 10px;">La historia adapta con fidelidad y pulso literario la dirección, giros y modificaciones narrativas del Game Master <strong>Roberto</strong>, junto al elenco original de jugadores:</p>
  
  <div style="margin: 16px auto; max-width: 520px;">
    <hr style="border: none; border-top: 1px solid #b8860b; width: 45%; margin: 8px auto;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 9.5pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 8px 0; text-indent: 0; text-align: center;">
      ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
    </p>
    <p style="margin: 4px 0; text-indent: 0; text-align: center; font-size: 10pt; color: #2d3748;">
      <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (y la voz del meca <strong>Gerty</strong>)
    </p>
    <p style="margin: 4px 0; text-indent: 0; text-align: center; font-size: 10pt; color: #2d3748;">
      <strong style="color: #1a365d;">Miguel:</strong> Benray Galway <em>(Emisario Ysoki)</em>
    </p>
    <p style="margin: 4px 0; text-indent: 0; text-align: center; font-size: 10pt; color: #2d3748;">
      <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em>
    </p>
    <p style="margin: 4px 0; text-indent: 0; text-align: center; font-size: 10pt; color: #2d3748;">
      <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc Boosmar <em>(Tecnomante Humano)</em>
    </p>
    <p style="margin: 4px 0; text-indent: 0; text-align: center; font-size: 10pt; color: #2d3748;">
      <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa Androide)</em>
    </p>
    <hr style="border: none; border-top: 1px solid #b8860b; width: 45%; margin: 8px auto;">
  </div>
  
  <p style="margin-bottom: 10px;">El propósito de esta novelización es transformar la espontaneidad de la mesa de rol en una experiencia literaria inmersiva, cinematográfica y coherente, respetando con fidelidad la personalidad de los protagonistas, el tono de comedia y peligro espacial, y la evolución del canon.</p>

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
    
    # 1. Encontrar la página donde está el Índice de Contenidos
    toc_page = 4
    for idx, page_text in enumerate(pages[:6]):
        if "índice de contenidos" in page_text.lower():
            toc_page = idx + 1
            break
            
    # 2. Nota Editorial siempre está antes del índice (página 2)
    found_pages["nota_editorial"] = 2
    for idx, page_text in enumerate(pages[:toc_page]):
        if "nota editorial e introducción" in page_text.lower():
            found_pages["nota_editorial"] = idx + 1
            break

    # 3. Para el resto de capítulos y anexo, buscamos estrictamente después del índice
    for item in TOC_ITEMS:
        if item["id"] == "nota_editorial":
            continue
        key = item["search_key"].lower().replace("...", "").strip()
        parts = [p.strip() for p in key.split(":") if p.strip()]
        for idx in range(toc_page, len(pages)):
            lines = [l.strip() for l in pages[idx].split("\n") if l.strip()][:8]
            header_text = " ".join(lines).lower().replace("\n", " ")
            if all(p in header_text for p in parts):
                found_pages[item["id"]] = idx + 1
                break
                
    # Fallback
    for item in TOC_ITEMS:
        if item["id"] not in found_pages:
            key = item["search_key"].lower()
            for idx in range(toc_page, len(pages)):
                if key in pages[idx].lower():
                    found_pages[item["id"]] = idx + 1
                    break
                    
    return found_pages

def build_book():
    print("=== Compilación de Volumen 4: Las Torres de Qabarat ===")
    
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
    print(f"\n¡Libro Volumen 4 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
