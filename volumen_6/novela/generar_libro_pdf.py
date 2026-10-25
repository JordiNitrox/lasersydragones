#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: El Fantasma en la Máquina' (Volumen 6)
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
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf")
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
        "sub": "Contexto de producción, el puente de Ukulam a Ábsalon y el canon de la saga"
    },
    {
        "id": "prologo",
        "search_key": "Prólogo: El Resplandor del Pasado",
        "title": "Prólogo: El Resplandor del Pasado",
        "sub": "Despedida del Templo de los Doce Soles, la tormenta en Ukulam y las dudas de Axel"
    },
    {
        "id": "cap_60",
        "search_key": "Capítulo 60: El Principio es el Final es el Principio",
        "title": "Capítulo 60: El Principio es el Final es el Principio",
        "sub": "Basado en el Episodio 60 · Descenso bajo la lluvia torrencial, la doctora Solstarni y el mensaje de Triuno"
    },
    {
        "id": "cap_61",
        "search_key": "Capítulo 61: Sanguijuelas Alucinantes",
        "title": "Capítulo 61: Sanguijuelas Alucinantes",
        "sub": "Basado en el Episodio 61 · Vado del río crecido, la bestia bífida Campin y el asedio viscoso en el islote"
    },
    {
        "id": "cap_62",
        "search_key": "Capítulo 62: Ukulam Standoff",
        "title": "Capítulo 62: Ukulam Standoff",
        "sub": "Basado en el Episodio 62 · Extravío bajo el diluvio, armas en el fango y alianza corsaria con De Bonet"
    },
    {
        "id": "cap_63",
        "search_key": "Capítulo 63: Los Chocopiratas y el Motor del Sabor",
        "title": "Capítulo 63: Los Chocopiratas y el Motor del Sabor",
        "sub": "Basado en el Episodio 63 · Ocho cápsulas de asalto de la Legión y el arrastre del reactor sobre el lodo"
    },
    {
        "id": "cap_64",
        "search_key": "Capítulo 64: ¡Me Lleva la Trampa!",
        "title": "Capítulo 64: ¡Me Lleva la Trampa!",
        "sub": "Basado en el Episodio 64 · Guerra de desgaste: señuelos acústicos, cables trampa y doce horas para La Furia"
    },
    {
        "id": "cap_65",
        "search_key": "Capítulo 65: Una Foto Vale Más que Mil Fantasmas",
        "title": "Capítulo 65: Una Foto Vale Más que Mil Fantasmas",
        "sub": "Basado en el Episodio 65 · Retorno a Qabarat; el misterio de la foto en la Avenida 41 y el pasado de Benray"
    },
    {
        "id": "cap_66",
        "search_key": "Capítulo 66: Necronversaciones en Ábsalon",
        "title": "Capítulo 66: Necronversaciones en Ábsalon",
        "sub": "Basado en el Episodio 66 · Audiencia con el Embajador Gevalarsk Nor y Cheesecake; fondos hacia La Diáspora"
    },
    {
        "id": "cap_67",
        "search_key": "Capítulo 67: Primos, Sobrinos y Productores",
        "title": "Capítulo 67: Primos, Sobrinos y Productores",
        "sub": "Basado en el Episodio 67 · Reencuentro con Bumak Istrav en El Ojo, la pista de Extracciones Astrales y Marcelus"
    },
    {
        "id": "cap_68",
        "search_key": "Capítulo 68: Leguleyos de Espionaje",
        "title": "Capítulo 68: Leguleyos de Espionaje",
        "sub": "Basado en el Episodio 68 · Conspiración en el café Las Lunas; diseño del golpe nocturno a la Torre Prisma"
    },
    {
        "id": "cap_69",
        "search_key": "Capítulo 69: ¡Teme al Espíritu Universitario!",
        "title": "Capítulo 69: ¡Teme al Espíritu Universitario!",
        "sub": "Basado en el Episodio 69 · Infiltración en el Nivel 28; tiroteo de plasma junto al piano de cola contra autómatas"
    },
    {
        "id": "cap_70",
        "search_key": "Capítulo 70: Hack-e Mate",
        "title": "Capítulo 70: Hack-e Mate",
        "sub": "Basado en el Episodio 70 · Despacho de la señorita Joss: fuego automático, sobrecarga de la caja fuerte y captura de datos"
    },
    {
        "id": "cap_71",
        "search_key": "Capítulo 71: Misión Imposible: Protocolo Marcelus",
        "title": "Capítulo 71: Misión Imposible: Protocolo Marcelus",
        "sub": "Basado en el Episodio 71 · Fuga vertical en alas de planeo sobre Ábsalon y localización definitiva del productor"
    },
    {
        "id": "cap_72",
        "search_key": "Capítulo 72: Fantasmeame la Máquina",
        "title": "Capítulo 72: Fantasmeame la Máquina",
        "sub": "Basado en el Episodio 72 · El actor Bordin en el Muelle 22, la pista hacia Eox y el despertar del alma de la nave"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "Ukulam, Extracciones Astrales, los Capitanes Libres, el Fantasma en la Máquina y Héroes de la Saga"
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
<title>Lasers y Dragones: El Fantasma en la Máquina</title>
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
    padding: 3.5px 3px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 9pt;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 8pt;
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
      El Fantasma en la Máquina
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
      VOLUMEN VI · EL FANTASMA EN LA MÁQUINA
    </p>
  </div>

  <!-- 2. NOTA EDITORIAL E INTRODUCCIÓN -->
  <h2 class="section-heading-main" style="margin-top: 5px; margin-bottom: 12px; font-size: 19pt; padding-bottom: 6px;">Nota Editorial e Introducción</h2>
  
  <p style="font-size: 9.5pt; line-height: 1.4; margin-bottom: 6px;">La presente obra constituye el sexto volumen de la novelización de las sesiones reales de juego de rol de mesa (<em>actual play</em>) emitidas en el podcast costarricense <strong>Lasers y Dragones</strong>, correspondiente a los episodios 60 al 72.</p>
  
  <p style="font-size: 9.5pt; line-height: 1.4; margin-bottom: 6px;">Este tomo marca un punto de inflexión decisivo en la saga: la evasión de Ukulam junto a los piratas corsarios de <em>La Furia</em> repeliendo a la Legión del Cielofuego, el misterio mnemónico del alma previa de A.Xel 42, el audaz asalto de espionaje a los archivos de Extracciones Astrales en la Estación Ábsalon y la integración de la conciencia sintética que despierta en la <em>Estrella Errante</em> antes de saltar al cinturón de la Diáspora.</p>
  
  <p style="font-size: 9.5pt; line-height: 1.4; margin-bottom: 6px;">La historia adapta con fidelidad y pulso literario la dirección narrativa del Game Master <strong>Roberto</strong>, junto al elenco original de jugadores:</p>
  
  <div style="margin: 8px auto; max-width: 500px;">
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 6px auto;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 8.5pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 6px 0; text-indent: 0; text-align: center;">
      ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
    </p>
    <p style="margin: 3px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
      <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (y la voz del meca <strong>Gerty</strong>) &nbsp;|&nbsp; <strong style="color: #1a365d;">Miguel:</strong> Benray Galway <em>(Emisario Ysoki)</em>
    </p>
    <p style="margin: 3px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
      <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc Boosmar <em>(Tecnomante)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa)</em>
    </p>
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 6px auto;">
  </div>
  
  <p style="font-size: 9.5pt; line-height: 1.4; margin-bottom: 6px;">El propósito de esta novelización es transformar la espontaneidad de la mesa de rol en una experiencia literaria inmersiva, cinematográfica y coherente, respetando con fidelidad la personalidad de los protagonistas, el tono de comedia y peligro espacial, y la evolución del canon.</p>

  <div style="margin: 10px auto 0 auto; padding: 10px 14px; border: 1px solid #cbd5e0; background-color: #f8fafc; font-size: 7.5pt; color: #4a5568; line-height: 1.35; text-align: justify; border-radius: 4px; page-break-inside: avoid; break-inside: avoid;">
    <p style="margin: 0 0 4px 0; text-indent: 0; font-weight: bold; color: #1a365d; font-size: 8pt; text-transform: uppercase; letter-spacing: 1px; text-align: center;">
      Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución
    </p>
    <p style="margin: 0 0 4px 0; text-indent: 0;">
      Esta obra literaria y sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de <strong>Paizo Inc.</strong>, utilizados bajo la <em>Política de Uso Comunitario de Paizo</em> (<a href="https://paizo.com/communityuse" style="color: #2b6cb0; text-decoration: none;">paizo.com/communityuse</a>). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de <em>Starfinder</em> y <em>Pathfinder</em>, visite <a href="https://paizo.com" style="color: #2b6cb0; text-decoration: none;">paizo.com</a>.
    </p>
    <p style="margin: 0; text-indent: 0;">
      Asimismo, esta novelización constituye un tributo no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense <strong>Lasers y Dragones</strong>. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: <strong>Roberto</strong> (Game Master y Gerty), <strong>Miguel</strong> (Benray Galway), <strong>Irene</strong> (Triel Istrav), <strong>Juan Pablo</strong> (Marloc Boosmar) y <strong>Sofía</strong> (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
    </p>
  </div>

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
    print("=== Compilación de Volumen 6: El Fantasma en la Máquina ===")
    
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
    print(f"\n¡Libro Volumen 6 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
