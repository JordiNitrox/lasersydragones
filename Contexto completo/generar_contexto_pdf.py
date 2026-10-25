#!/usr/bin/env python3
"""
Compilador del Documento Maestro de Contexto Completo y Guía de Continuidad
de la saga 'Lasers y Dragones' (Campaña Starfinder: Dead Suns).
Genera un HTML con formato editorial y compila el PDF mediante LibreOffice headless,
calculando los números de página exactos en 2 pases con pdftotext.
"""

import os
import re
import subprocess
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_INPUT = os.path.join(BASE_DIR, "CONTEXTO_COMPLETO_SAGA.md")
PDF_OUTPUT = os.path.join(BASE_DIR, "Contexto_Completo_Lasers_y_Dragones.pdf")
HTML_OUTPUT = os.path.join(BASE_DIR, "contexto_completo_maquetado.html")
PROFILE_DIR = os.path.join(BASE_DIR, ".libreoffice_profile")

def inline_formatting(text):
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^\*]+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_([^_]+?)_", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    return text

def md_to_html(text):
    lines = text.strip().split("\n")
    html_lines = []
    in_list = False
    in_table = False
    table_header = True
    
    for line in lines:
        line_s = line.strip()
        
        # Tablas markdown
        if line_s.startswith("|") and line_s.endswith("|"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            
            # Línea divisoria de tabla (ej. |---|---|)
            if re.match(r"^\|(\s*:?-+:?\s*\|)+$", line_s):
                table_header = False
                continue
                
            cells = [c.strip() for c in line_s.strip("|").split("|")]
            if not in_table:
                html_lines.append("<table class='matrix-table' border='1' cellspacing='0' cellpadding='8' style='width: 100%; border-collapse: collapse; border: 1px solid #a0aec0; margin: 20px 0;'>")
                in_table = True
                table_header = True
                
            if table_header:
                th_cells = ""
                col_width = f"width: {100 // len(cells)}%;"
                for idx, c in enumerate(cells):
                    th_cells += f"<th style='background-color: #1a365d; color: #ffffff; padding: 10px 12px; font-weight: bold; border: 1px solid #1a365d; text-align: left; {col_width}'>{inline_formatting(c)}</th>"
                html_lines.append(f"<thead><tr>{th_cells}</tr></thead><tbody>")
            else:
                td_cells = ""
                for idx, c in enumerate(cells):
                    style = "font-weight: bold; color: #0b1a30; background-color: #f7fafc; padding: 8px 10px; border: 1px solid #cbd5e0;" if idx == 0 else "padding: 8px 10px; border: 1px solid #cbd5e0;"
                    td_cells += f"<td style='{style}'>{inline_formatting(c)}</td>"
                html_lines.append(f"<tr>{td_cells}</tr>")
            continue
        else:
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
                table_header = True
                
        # Separadores
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
            continue
        elif line_s.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = inline_formatting(line_s[3:].strip())
            html_lines.append(f"<h2 class='chapter-name'>{title}</h2>")
            continue
        elif line_s.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = inline_formatting(line_s[4:].strip())
            html_lines.append(f"<h3 class='section-title'>{title}</h3>")
            continue
        elif line_s.startswith("#### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = inline_formatting(line_s[5:].strip())
            html_lines.append(f"<h4 class='subsection-title'>{title}</h4>")
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
    if in_table:
        html_lines.append("</tbody></table>")
        
    return "\n".join(html_lines)

CTX_TOC_ITEMS = [
    {
        "id": "presentacion",
        "search_key": "Presentación del Archivo Maestro",
        "title": "Presentación del Archivo Maestro",
        "sub": "Objetivos y uso de la guía de continuidad"
    },
    {
        "id": "sec_1",
        "search_key": "1. Resumen Cronológico de los Volúmenes",
        "title": "1. Resumen Cronológico de los Volúmenes",
        "sub": "Sinopsis argumental y puntos de giro: Volumen 1 al Volumen 6"
    },
    {
        "id": "sec_2",
        "search_key": "2. Índice Maestro de Escenarios y Ubicaciones",
        "title": "2. Índice Maestro de Escenarios y Ubicaciones",
        "sub": "Estación Absalón, Castrovel, Qabarat, Aiakos, Ukulam, La Diáspora y Torre Prisma"
    },
    {
        "id": "sec_3",
        "search_key": "3. Dossier Maestro de Personajes",
        "title": "3. Dossier Maestro de Personajes",
        "sub": "Protagonistas (Nivel 6), aliados, secundarios, corsarios y rivales corporativos"
    },
    {
        "id": "sec_4",
        "search_key": "4. Corporaciones, Facciones e Instituciones",
        "title": "4. Corporaciones, Facciones e Instituciones",
        "sub": "Inversiones Estelares, Hardscrabble, Protectores, Legión, Capitanes Libres y Culto del Devorador"
    },
    {
        "id": "sec_5",
        "search_key": "5. Bestiario y Amenazas Cósmicas",
        "title": "5. Bestiario y Amenazas Cósmicas",
        "sub": "Garaggakal, Driftdead, Akatas, Yaruks, Khasaris, Oshiga, Campin y autómatas de asalto"
    },
    {
        "id": "sec_6",
        "search_key": "6. Matriz de Continuidad y Estado de la Tripulación",
        "title": "6. Matriz de Continuidad y Estado de la Tripulación",
        "sub": "Tabla comparativa de naves, armamento, romances y estado activo (Vol. 1 al 6)"
    }
]

def render_html(page_numbers=None):
    if page_numbers is None:
        page_numbers = {item["id"]: "--" for item in CTX_TOC_ITEMS}
        
    with open(MD_INPUT, "r", encoding="utf-8") as fp:
        raw_md = fp.read()
    body_html = md_to_html(raw_md)
    
    toc_rows = []
    for item in CTX_TOC_ITEMS:
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
<title>Lasers y Dragones: Contexto Completo y Guía de Continuidad</title>
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
  
  h2.chapter-name {{
    page-break-before: always;
    break-before: page;
    font-size: 20pt;
    color: #0b1a30;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 25px;
    line-height: 1.3;
    border-bottom: 2px solid #b8860b;
    padding-bottom: 12px;
  }}
  
  h3.section-title {{
    font-size: 14pt;
    color: #2b6cb0;
    margin-top: 24px;
    margin-bottom: 12px;
    border-bottom: 1px dashed #cbd5e0;
    padding-bottom: 4px;
    font-family: 'Liberation Serif', serif;
  }}
  
  h4.subsection-title {{
    font-size: 12pt;
    color: #1a365d;
    margin-top: 18px;
    margin-bottom: 8px;
    font-family: 'Liberation Sans', sans-serif;
    font-weight: bold;
  }}
  
  p {{
    text-align: justify;
    text-justify: inter-word;
    margin: 0 0 10px 0;
    text-indent: 1.2em;
  }}
  
  p.no-indent {{
    text-indent: 0;
  }}
  
  .divider {{
    text-align: center;
    margin: 25px 0;
    color: #2b6cb0;
    font-size: 11pt;
    letter-spacing: 6px;
  }}
  
  .bullet-list {{
    margin: 10px 0 15px 25px;
    padding: 0;
  }}
  
  .bullet-list li {{
    margin-bottom: 6px;
    text-align: justify;
  }}
  
  .quote {{
    border-left: 3px solid #b8860b;
    background: #f7fafc;
    margin: 15px 20px;
    padding: 8px 15px;
    font-style: italic;
    color: #4a5568;
  }}
  
  .toc-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
  }}
  
  .toc-table td {{
    padding: 7px 4px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 10pt;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 9pt;
    color: #718096;
    font-style: italic;
  }}
  
  .matrix-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0 25px 0;
    font-size: 8.8pt;
    line-height: 1.35;
  }}
  
  .matrix-table th {{
    background: #1a365d;
    color: #ffffff;
    font-weight: bold;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #1a365d;
  }}
  
  .matrix-table td {{
    padding: 8px 10px;
    border: 1px solid #cbd5e0;
    vertical-align: top;
    text-align: left;
  }}
  
  .matrix-table tr:nth-child(even) {{
    background: #f8fafc;
  }}
  
  code {{
    font-family: monospace;
    font-size: 9pt;
    background: #edf2f7;
    padding: 2px 4px;
    border-radius: 3px;
    color: #2b6cb0;
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
      Contexto Completo y Guía de Continuidad
    </div>
    
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 20px auto;">
    
    <div style="font-size: 14pt; color: #2b6cb0; margin: 25px 0;">
      ✦ &nbsp; ◈ &nbsp; ✦
    </div>
    
    <p style="font-size: 11pt; line-height: 1.6; color: #4a5568; margin: 30px auto; max-width: 420px; text-indent: 0; text-align: center;">
      Dossier maestro de escenarios, personajes, facciones, bestiario y resumen cronológico de la saga novelada del podcast <strong>Lasers y Dragones</strong> (Campaña <em>Dead Suns</em>).
    </p>
    
    <hr style="border: none; border-top: 1px solid #cbd5e0; width: 80%; margin: 50px auto 20px auto;">
    
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 10pt; letter-spacing: 3px; text-transform: uppercase; color: #1a365d; margin: 0; text-indent: 0; text-align: center;">
      BIBLIOTECA EDITORIAL · GUÍA DE CANON Y CONTINUIDAD
    </p>
  </div>

  <!-- 2. PRESENTACIÓN EDITORIAL -->
  <h2 class="section-heading-main" style="margin-top: 5px; margin-bottom: 14px; font-size: 19pt; padding-bottom: 6px;">Presentación del Archivo Maestro</h2>
  
  <p style="font-size: 10pt; line-height: 1.45; margin-bottom: 6px;">El presente volumen constituye el <strong>Archivo Maestro de Contexto y Continuidad</strong> de la adaptación novelada de <em>Lasers y Dragones</em>. Su propósito fundamental es doble:</p>
  
  <ul class="bullet-list" style="margin: 6px 0 10px 20px; font-size: 9.5pt; line-height: 1.4;">
    <li style="margin-bottom: 4px;"><strong>Para el lector:</strong> Disponer de un compendio accesible, estructurado y ágil que resuma el viaje de los protagonistas, refresque misterios y organice fichas de personajes y escenarios con indicación de sus apariciones.</li>
    <li><strong>Para el equipo editorial:</strong> Actuar como la <em>Única Fuente de Verdad</em> (Single Source of Truth) para asegurar la coherencia absoluta de las tramas, la evolución del equipo y el estado de las relaciones conforme la saga crece.</li>
  </ul>

  <table style="width: 100%; margin: 10px 0 0 0; border: 1px solid #cbd5e0; background-color: #f8fafc; border-collapse: collapse; page-break-inside: avoid; break-inside: avoid;">
    <tr>
      <td style="padding: 8px 12px; font-size: 7.5pt; color: #4a5568; line-height: 1.35; text-align: justify; border: none;">
        <p style="margin: 0 0 4px 0; text-indent: 0; font-weight: bold; color: #1a365d; font-size: 8pt; text-transform: uppercase; letter-spacing: 1px; text-align: center;">
          Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución
        </p>
        <p style="margin: 0 0 4px 0; text-indent: 0;">
          Esta obra literaria y de documentación sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de <strong>Paizo Inc.</strong>, utilizados bajo la <em>Política de Uso Comunitario de Paizo</em> (<a href="https://paizo.com/communityuse" style="color: #2b6cb0; text-decoration: none;">paizo.com/communityuse</a>). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de <em>Starfinder</em> y <em>Pathfinder</em>, visite <a href="https://paizo.com" style="color: #2b6cb0; text-decoration: none;">paizo.com</a>.
        </p>
        <p style="margin: 0; text-indent: 0;">
          Asimismo, este dossier maestro constituye una recopilación de referencia no oficial y de difusión cultural inspirada en la campaña de rol en vivo del podcast costarricense <strong>Lasers y Dragones</strong>. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: <strong>Roberto</strong> (Game Master y Gerty), <strong>Miguel</strong> (Benray Galway), <strong>Irene</strong> (Triel Istrav), <strong>Juan Pablo</strong> (Marloc Boosmar) y <strong>Sofía</strong> (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
        </p>
      </td>
    </tr>
  </table>
  
  <!-- 3. ÍNDICE DE CONTENIDOS -->
  <h2 class="section-heading-main">Índice del Dossier de Continuidad</h2>
  
  <table class="toc-table">
{toc_rows_html}
  </table>

  <!-- 4. CONTENIDO MAESTRO -->
  {body_html}

</body>
</html>
"""
    with open(HTML_OUTPUT, "w", encoding="utf-8") as fp:
        fp.write(html_doc)
    return HTML_OUTPUT

def execute_libreoffice():
    profile_path = os.path.join(BASE_DIR, ".libreoffice_profile")
    user_prof = "file://" + urllib.parse.quote(profile_path)
    cmd = [
        "libreoffice",
        f"-env:UserInstallation={user_prof}",
        "--headless",
        "--convert-to", "pdf",
        HTML_OUTPUT,
        "--outdir", BASE_DIR
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Error en LibreOffice: {res.stderr}")
    converted_pdf = os.path.join(BASE_DIR, "contexto_completo_maquetado.pdf")
    if os.path.exists(converted_pdf):
        if os.path.exists(PDF_OUTPUT):
            os.remove(PDF_OUTPUT)
        os.rename(converted_pdf, PDF_OUTPUT)
    return PDF_OUTPUT

def extract_context_pages(pdf_path):
    res = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
    pages = res.stdout.split("\x0c")
    found_pages = {}
    
    # Presentación
    for idx, page_text in enumerate(pages[:4]):
        if "presentación del archivo maestro" in page_text.lower():
            found_pages["presentacion"] = idx + 1
            break
            
    # Resto de secciones (buscar encabezados de sección a partir de pág. 4)
    for item in CTX_TOC_ITEMS:
        if item["id"] == "presentacion":
            continue
        key = item["search_key"].lower()
        for idx in range(3, len(pages)):
            lines = [l.strip() for l in pages[idx].split("\n") if l.strip()][:5]
            header = " ".join(lines).lower()
            if key in header:
                found_pages[item["id"]] = idx + 1
                break
                
    return found_pages

def build_pdf():
    print("Compilando Documento Maestro de Contexto Completo...")
    print("Paso 1: Generando HTML preliminar...")
    render_html()
    print("Paso 2: Generando PDF preliminar con LibreOffice...")
    execute_libreoffice()
    
    print("Paso 3: Extrayendo números de página exactos con pdftotext...")
    pages = extract_context_pages(PDF_OUTPUT)
    print("Páginas detectadas en el Dossier:")
    for item in CTX_TOC_ITEMS:
        print(f"  - {item['title']}: pág. {pages.get(item['id'], '??')}")
        
    print("Paso 4: Regenerando HTML con el Índice final...")
    render_html(page_numbers=pages)
    print("Paso 5: Compilando PDF final...")
    final_pdf = execute_libreoffice()
    
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡PDF de Contexto Completo generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")
    return True

if __name__ == "__main__":
    build_pdf()
