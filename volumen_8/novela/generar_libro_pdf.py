#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: Mundos Fragmentados II: Las Cortes Cadavéricas de Eox' (Volumen 8)
Genera un documento HTML con estilos editoriales de libro y lo convierte a PDF
siguiendo las directrices técnicas del skill para garantizar marcadores PDF correctos.
"""

import os
import re
import glob
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPS_DIR = os.path.join(BASE_DIR, "capitulos")
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_8_Mundos_Fragmentados_II_Las_Cortes_Cadavericas_de_Eox.pdf")
HTML_OUTPUT = os.path.join(BASE_DIR, "libro_maquetado.html")

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
        if line_s.startswith("* ") or line_s.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item_text = inline_formatting(line_s[2:].strip())
            html_lines.append(f"<li>{item_text}</li>")
            continue
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
                
        # Citas / Blockquotes
        if line_s.startswith("> "):
            quote_text = inline_formatting(line_s[2:].strip())
            html_lines.append(f"<blockquote><p>{quote_text}</p></blockquote>")
            continue
            
        # Línea vacía
        if not line_s:
            continue
            
        # Párrafos normales
        p_text = inline_formatting(line_s)
        html_lines.append(f"<p>{p_text}</p>")
        
    if in_list:
        html_lines.append("</ul>")
        
    return "\n".join(html_lines)

def inline_formatting(text):
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    return text

def build_html():
    cap_files = sorted(glob.glob(os.path.join(CAPS_DIR, "*.md")))
    glosario_file = os.path.join(BASE_DIR, "GLOSARIO_Y_PERSONAJES.md")
    
    html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Lasers y Dragones · Volumen VIII · Mundos Fragmentados II: Las Cortes Cadavéricas de Eox</title>
<style>
  @page {
    size: 152.4mm 228.6mm; /* 6x9 pulgadas */
    margin-top: 20mm;
    margin-bottom: 20mm;
    margin-left: 20mm;
    margin-right: 20mm;
    @bottom-center {
      content: counter(page);
      font-family: 'Liberation Serif', Georgia, serif;
      font-size: 9pt;
      color: #4a5568;
    }
  }

  body {
    font-family: 'Liberation Serif', Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1a202c;
    margin: 0;
    padding: 0;
    text-align: justify;
    text-justify: inter-word;
  }

  .cover-page {
    page-break-after: always;
    text-align: center;
    padding-top: 45mm;
  }
  .cover-series {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 12pt;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #718096;
    margin-bottom: 8mm;
  }
  .cover-title {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 24pt;
    font-weight: 700;
    line-height: 1.2;
    color: #0f172a;
    margin-bottom: 5mm;
  }
  .cover-sub {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 14pt;
    font-weight: 400;
    color: #2b6cb0;
    letter-spacing: 1.5px;
    margin-bottom: 25mm;
  }
  .cover-footer {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 9.5pt;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #1a365d;
    margin-top: 35mm;
  }

  .chapter {
    page-break-before: always;
    padding-top: 15mm;
  }
  
  h2.chapter-name {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 16pt;
    font-weight: 700;
    text-align: center;
    color: #0f172a;
    margin-bottom: 8mm;
    page-break-after: avoid;
  }

  h3.subsection-title {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    color: #2b6cb0;
    margin-top: 7mm;
    margin-bottom: 4mm;
    page-break-after: avoid;
  }

  h3.section-title {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #1a365d;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 2mm;
    margin-top: 8mm;
    margin-bottom: 4mm;
    page-break-after: avoid;
  }

  h4.subsection-title {
    font-family: 'Liberation Sans', sans-serif;
    font-size: 10.5pt;
    font-weight: 700;
    color: #2d3748;
    margin-top: 5mm;
    margin-bottom: 2mm;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-indent: 5mm;
  }

  h2.chapter-name + p,
  h3.subsection-title + p,
  h3.section-title + p,
  .divider + p,
  blockquote + p {
    text-indent: 0;
  }

  .divider {
    text-align: center;
    font-size: 11pt;
    color: #a0aec0;
    margin-top: 5mm;
    margin-bottom: 5mm;
    page-break-inside: avoid;
  }

  blockquote {
    border-left: 3px solid #2b6cb0;
    background-color: #f8fafc;
    padding: 3mm 5mm;
    margin: 4mm 0;
    font-style: italic;
    color: #4a5568;
    text-indent: 0;
  }
  blockquote p {
    text-indent: 0;
    margin-bottom: 0;
  }

  ul {
    margin-top: 0;
    margin-bottom: 4mm;
    padding-left: 6mm;
  }

  li {
    margin-bottom: 2mm;
  }
</style>
</head>
<body>

<!-- PORTADA -->
<div class="cover-page">
  <div class="cover-series">Lasers y Dragones · Saga Principal</div>
  <div class="cover-title">MUNDOS FRAGMENTADOS II</div>
  <div class="cover-sub">Las Cortes Cadavéricas de Eox</div>
  <div class="divider">✦ &nbsp; ◈ &nbsp; ✦</div>
  <div class="cover-footer">VOLUMEN VIII · MUNDOS FRAGMENTADOS II: LAS CORTES CADAVÉRICAS DE EOX</div>
</div>

"""
    for fpath in cap_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        cap_html = md_to_html(content, is_glossary=False)
        html += f"<div class='chapter'>\n{cap_html}\n</div>\n"
        
    if os.path.exists(glosario_file):
        with open(glosario_file, "r", encoding="utf-8") as f:
            g_content = f.read()
        g_html = md_to_html(g_content, is_glossary=True)
        html += f"<div class='chapter glossary'>\n{g_html}\n</div>\n"
        
    html += "</body>\n</html>"
    
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"HTML generado exitosamente: {HTML_OUTPUT}")

def convert_to_pdf():
    user_prof = f"file://{BASE_DIR}/.libreoffice_profile"
    cmd = [
        "libreoffice",
        f"-env:UserInstallation={user_prof}",
        "--headless",
        "--convert-to",
        "pdf:writer_pdf_Export",
        HTML_OUTPUT
    ]
    print("Compilando PDF con LibreOffice en modo headless...")
    res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode == 0:
        src_pdf = os.path.join(BASE_DIR, "libro_maquetado.pdf")
        if os.path.exists(src_pdf):
            os.replace(src_pdf, PDF_OUTPUT)
            print(f"PDF generado exitosamente: {PDF_OUTPUT}")
        elif os.path.exists(PDF_OUTPUT):
            print(f"PDF generado: {PDF_OUTPUT}")
        else:
            print("Error: No se encontró el archivo PDF generado.")
    else:
        print(f"Error en LibreOffice: {res.stderr}")

if __name__ == "__main__":
    build_html()
    convert_to_pdf()
