#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: Sombras sobre Absalón'
Genera un documento HTML con estilos editoriales de libro y lo convierte a PDF.
"""

import os
import re
import glob
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPS_DIR = os.path.join(BASE_DIR, "capitulos")
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_1_Sombras_sobre_Absalon.pdf")
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
            title = line_s[2:].strip()
            html_lines.append(f"<h2 class='chapter-name'>{title}</h2>")
            continue
        elif line_s.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = line_s[3:].strip()
            html_lines.append(f"<h3 class='section-title'>{title}</h3>")
            continue
        elif line_s.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = line_s[4:].strip()
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

def inline_formatting(text):
    text = re.sub(r"\*\*\*([^\*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^\*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"_([^_]+)_", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text

def build_book():
    print("Compilando capítulos de la novela...")
    
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
    with open(glossary_path, "r", encoding="utf-8") as fp:
        glossary_raw = fp.read()
        remaining_glossary = "\n".join(glossary_raw.strip().split("\n")[1:])
        glossary_html = md_to_html(remaining_glossary, is_glossary=True)

    html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Lasers y Dragones: Sombras sobre Absalón</title>
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
    margin: 25px 0;
  }}
  
  .toc-table td {{
    padding: 8px 4px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 10.5pt;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 9.5pt;
    color: #718096;
    font-style: italic;
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
    border-left: 3px solid #cbd5e0;
    margin: 15px 25px;
    padding: 6px 12px;
    font-style: italic;
    color: #4a5568;
  }}
  
</style>
</head>
<body>

  <!-- 1. PORTADA -->
  <div style="text-align: center; padding: 40px 10px; margin: 0 auto; max-width: 500px;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 11pt; letter-spacing: 5px; text-transform: uppercase; color: #2b6cb0; margin: 40px 0 20px 0; text-indent: 0;">
      Ópera Espacial · Universo Starfinder
    </p>
    
    <hr style="border: none; border-top: 2px solid #1a365d; width: 60%; margin: 25px auto;">
    
    <div style="font-size: 30pt; font-weight: bold; color: #0b1a30; margin: 20px 0 10px 0; letter-spacing: 2px; text-align: center;">
      LASERS Y DRAGONES
    </div>
    
    <div style="font-size: 20pt; font-style: italic; color: #b8860b; margin: 10px 0 20px 0; text-align: center;">
      Sombras sobre Absalón
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
      Volumen I · Conspiración en la Espiga
    </p>
  </div>

  <!-- 2. NOTA EDITORIAL E INTRODUCCIÓN -->
  <h2 class="section-heading-main" style="margin-top: 5px; margin-bottom: 12px; font-size: 19pt; padding-bottom: 6px;">Nota Editorial e Introducción</h2>
  
  <p style="font-size: 9.5pt; line-height: 1.4; margin-bottom: 6px;">La presente obra constituye una transposición novelada de las sesiones reales de juego de rol de mesa (<em>actual play</em>) emitidas en el podcast costarricense <strong>Lasers y Dragones</strong>, correspondiente a sus primeros diez episodios transmitidos a comienzos del año 2020.</p>
  
  <p style="font-size: 9.5pt; line-height: 1.4; margin-bottom: 6px;">La historia adapta los acontecimientos de la campaña oficial <strong>Dead Suns (Soles Muertos)</strong> del juego de rol <strong>Starfinder</strong> (creado y publicado por <em>Paizo Inc.</em>), enriquecida con la dirección, giros y modificaciones narrativas del Game Master <strong>Roberto</strong>, junto al elenco original de jugadores:</p>
  
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
    <tr>
      <td>
        <div class="toc-title">Nota Editorial e Introducción</div>
        <div class="toc-sub">Contexto y créditos del podcast original</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">2</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Prólogo: El Fantasma de Golarion</div>
        <div class="toc-sub">La Brecha y la Estación Absalón</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">4</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 1: Senderos hacia la Chatarra</div>
        <div class="toc-sub">Basado en el Episodio 1</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">5</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 2: El Desmayo y el Club 13</div>
        <div class="toc-sub">Basado en el Episodio 2 (Parte 1)</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">12</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 3: La Mesa de los Sospechosos</div>
        <div class="toc-sub">Basado en el Episodio 2 (Parte 2)</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">18</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 4: Emboscada en el Muelle 94</div>
        <div class="toc-sub">Basado en el final del Episodio 2</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">22</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 5: Fuego Cruzado y Chatarra</div>
        <div class="toc-sub">Basado en el Episodio 3 completo</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">25</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 6: Noticias de Última Hora y el Enigma de Chiskisk</div>
        <div class="toc-sub">Basado en los Episodios 4 y 5 · Inversiones Estelares y la Roca del Drift</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">30</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 7: Mano de Seda y Cartas Cuánticas</div>
        <div class="toc-sub">Basado en el Episodio 6 · El rastro de Clara y el Club 13</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">36</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 8: El Laberinto de los Bajos</div>
        <div class="toc-sub">Basado en el Episodio 7</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">41</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 9: La Reina de la Con-Fusión</div>
        <div class="toc-sub">Basado en los Episodios 8 y 9 · Ferani Nadaz y Brock Hilario</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">44</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Capítulo 10: Rumbo a la Deriva</div>
        <div class="toc-sub">Basado en el Episodio 10</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">49</td>
    </tr>
    <tr>
      <td>
        <div class="toc-title">Anexo Especial: Dossier de Personajes y Glosario</div>
        <div class="toc-sub">Fichas de personajes, corporaciones, facciones y el Drift</div>
      </td>
      <td style="text-align: right; vertical-align: bottom; font-weight: bold;">54</td>
    </tr>
  </table>
"""

    # Agregar capítulos: h2 tiene page-break-before: always;
    for i, ch in enumerate(chapters_data):
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

    # Agregar anexo
    html_doc += f"""
  <h2 class="chapter-name">Anexo Especial: <br><span class="chap-sub">Dossier de Personajes y Glosario</span></h2>
  <div class="chapter-body">
    {glossary_html}
  </div>

</body>
</html>
"""

    with open(HTML_OUTPUT, "w", encoding="utf-8") as fp:
        fp.write(html_doc)
    print(f"Documento HTML consolidado creado en: {HTML_OUTPUT}")
    
    # Conversión a PDF mediante LibreOffice
    print("Iniciando renderizado de PDF con LibreOffice...")
    user_prof = f"file://{os.path.join(BASE_DIR, '.libreoffice_profile')}"
    cmd = [
        "libreoffice",
        f"-env:UserInstallation={user_prof}",
        "--headless",
        "--convert-to",
        "pdf",
        HTML_OUTPUT
    ]
    
    res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode == 0:
        gen_pdf = os.path.join(BASE_DIR, "libro_maquetado.pdf")
        if os.path.exists(gen_pdf):
            if os.path.exists(PDF_OUTPUT):
                os.remove(PDF_OUTPUT)
            os.rename(gen_pdf, PDF_OUTPUT)
            print(f"¡PDF generado con éxito en:\n  {PDF_OUTPUT}")
            size_mb = os.path.getsize(PDF_OUTPUT) / (1024 * 1024)
            print(f"Tamaño del archivo: {size_mb:.2f} MB")
        else:
            print("Aviso: No se encontró el archivo PDF generado automáticamente.")
    else:
        print(f"Error al generar PDF: {res.stderr}")

if __name__ == "__main__":
    build_book()
