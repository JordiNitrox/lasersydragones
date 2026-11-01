#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: La Sombra de Apostae' (Volumen 10)
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
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_10_La_Sombra_de_Apostae.pdf")
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
        "id": "cap_1",
        "search_key": "Capítulo 1: It's Morbin Time",
        "title": "Capítulo 1: It's Morbin Time",
        "sub": "Basado en el Episodio 111 · El fin de Marcellus, cenizas con arroz y el gatillo del muerto"
    },
    {
        "id": "cap_2",
        "search_key": "Capítulo 2: ¿Quién es el Jefe?",
        "title": "Capítulo 2: ¿Quién es el Jefe?",
        "sub": "Basado en el Episodio 112 · El barman de los Doce Soles, la sede de Inversiones Estelares y la carta de Marloc"
    },
    {
        "id": "cap_3",
        "search_key": "Capítulo 3: Juego de Niños",
        "title": "Capítulo 3: Juego de Niños",
        "sub": "Basado en el Episodio 113 · El enigma familiar de Triel, las fosas de Thanox y la guardería de Cóex y Nómina"
    },
    {
        "id": "cap_4",
        "search_key": "Capítulo 4: Lo que Oculta la Orcriada",
        "title": "Capítulo 4: Lo que Oculta la Orcriada",
        "sub": "Basado en el Episodio 114 · El pacto con Valeria, la cartografía del complejo Istrav y la cumbre matriarcal"
    },
    {
        "id": "cap_5",
        "search_key": "Capítulo 5: El Nido de la Araña",
        "title": "Capítulo 5: El Nido de la Araña",
        "sub": "Basado en el Episodio 115 · Infiltración de servicio, los tanques de eugenesia drow y el cerrojo de alcantarilla"
    },
    {
        "id": "cap_6",
        "search_key": "Capítulo 6: Servidumbre con Pesadumbre",
        "title": "Capítulo 6: Servidumbre con Pesadumbre",
        "sub": "Basado en el Episodio 116 · Bandejas de plata entre nobles, el cónclave de Jhidel y el desprecio de Niriel"
    },
    {
        "id": "cap_7",
        "search_key": "Capítulo 7: Babitas pa' que las Quiero",
        "title": "Capítulo 7: Babitas pa' que las Quiero",
        "sub": "Basado en el Episodio 117 · Incursión en los conductos, la caída en las sentinas y el rescate de Babitas"
    },
    {
        "id": "cap_8",
        "search_key": "Capítulo 8: Naves de Sangre",
        "title": "Capítulo 8: Naves de Sangre",
        "sub": "Basado en el Episodio 118 · Hackeo al núcleo de datos, la fuga colosal de Keiden Ashton y la libertad de Kroll"
    },
    {
        "id": "cap_9",
        "search_key": "Capítulo 9: Amor Fraternal",
        "title": "Capítulo 9: Amor Fraternal",
        "sub": "Basado en el Episodio 119 · El cerco en el vestíbulo de mármol, desafío entre hermanas y duelo de plasma"
    },
    {
        "id": "cap_10",
        "search_key": "Capítulo 10: Todo Sobre Mi Madre",
        "title": "Capítulo 10: Todo Sobre Mi Madre",
        "sub": "Basado en el Episodio 120 · La caída de Jhidel, el juicio glacial de la Matriarca Niriel y la brecha de Gerty"
    },
    {
        "id": "cap_11",
        "search_key": "Capítulo 11: Siempre nos quedará Thanox",
        "title": "Capítulo 11: Siempre nos quedará Thanox",
        "sub": "Basado en el Episodio 121 · Cacería en la roca porosa, la deuda saldada con Valeria y despegue de Eox"
    },
    {
        "id": "cap_12",
        "search_key": "Capítulo 12: El verdadero valor de A.Xel",
        "title": "Capítulo 12: El verdadero valor de A.Xel",
        "sub": "Basado en el Episodio 122 · Calma estelar, el chasis pre-Brecha de Ashera y el salto hacia Nejeor VI"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial: Dossier de Personajes y Glosario",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "La Casa Istrav, la urbe de Thanox, Keiden Ashton y secretos de la saga"
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
<title>Lasers y Dragones: La Sombra de Apostae</title>
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
    font-size: 8.4pt;
    line-height: 1.15;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 7.5pt;
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
  
  h3.section-title {{
    font-size: 14pt;
    color: #2b6cb0;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  
  h3.subsection-title {{
    font-size: 12.5pt;
    color: #2d3748;
    margin-top: 20px;
    margin-bottom: 10px;
    font-style: italic;
    border-left: 3px solid #b8860b;
    padding-left: 10px;
  }}
  
  h4.subsection-title {{
    font-size: 11pt;
    color: #1a365d;
    margin-top: 14px;
    margin-bottom: 6px;
    font-weight: bold;
  }}
  
  p {{
    text-align: justify;
    text-indent: 1.5em;
    margin-top: 0;
    margin-bottom: 0.6em;
  }}
  
  p:first-of-type {{
    text-indent: 0;
  }}
  
  .divider {{
    text-align: center;
    color: #b8860b;
    font-size: 14pt;
    margin: 25px 0;
    letter-spacing: 5px;
  }}
  
  blockquote.quote {{
    border-left: 3px solid #b8860b;
    margin: 15px 25px;
    padding: 8px 15px;
    background: #fdfaf6;
    font-style: italic;
    color: #4a5568;
  }}
  
  blockquote.quote p {{
    text-indent: 0;
    margin-bottom: 0;
  }}
  
  ul.bullet-list {{
    margin: 10px 0 15px 25px;
    padding: 0;
  }}
  
  ul.bullet-list li {{
    margin-bottom: 5px;
    text-align: justify;
  }}

  /* PORTADA A4 ELEGANTE */
  .cover-page {{
    page-break-before: auto;
    page-break-after: always;
    break-after: page;
    height: 92vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    border: 4px double #b8860b;
    padding: 35px 25px;
    box-sizing: border-box;
    background: radial-gradient(circle at center, #ffffff 0%, #fbf9f5 100%);
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
    La Sombra de Apostae
  </div>
  
  <div style="font-size: 13pt; font-weight: bold; color: #2b6cb0; margin: 0 0 20px 0; letter-spacing: 1.5px; text-transform: uppercase; text-align: center;">
    Lazos de Sangre
  </div>
  
  <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 20px auto;">
  
  <div style="font-size: 14pt; color: #2b6cb0; margin: 25px 0;">
    ✦ &nbsp; ◈ &nbsp; ✦
  </div>
  
  <p style="font-size: 10.5pt; line-height: 1.6; color: #4a5568; margin: 25px auto; max-width: 440px; text-indent: 0; text-align: center;">
    Adaptación literaria integral de los episodios 111 al 122 del podcast <strong>Lasers y Dragones</strong>.<br>
    <em>El fin de Marcellus y la revelación de Inversiones Estelares,<br>
    la infiltración servil en las fosas industriales de Thanox,<br>
    los archivos de Keiden Ashton y el duelo fratricida con la Casa Istrav.</em>
  </p>
  
  <hr style="border: none; border-top: 1px solid #cbd5e0; width: 80%; margin: 40px auto 20px auto;">
  
  <p style="font-family: 'Liberation Sans', sans-serif; font-size: 9.5pt; letter-spacing: 3px; text-transform: uppercase; color: #1a365d; margin: 0; text-indent: 0; text-align: center;">
    VOLUMEN X · LAZOS DE SANGRE: LA SOMBRA DE APOSTAE
  </p>
</div>

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 2 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 2: NOTA EDITORIAL E INTRODUCCIÓN -->
<div style="page-break-before: always; break-before: page; padding: 10px 0;">
  <h2 class="section-heading-main" style="page-break-before: avoid; break-before: avoid; margin-bottom: 12px; padding-bottom: 6px; font-size: 16pt;">
    Nota Editorial e Introducción
  </h2>
  
  <p style="font-size: 9.2pt; line-height: 1.45; text-align: justify; margin-bottom: 8px;">
    La presente obra constituye el décimo volumen de la novelización de las sesiones reales de juego de rol de mesa (<em>actual play</em>) emitidas en el podcast costarricense <strong>Lasers y Dragones</strong>, correspondiente a los episodios 111 al 122 de la campaña. Este libro desarrolla un arco dramático canónico propio y fundamental de la mesa de juego, conectando el desenlace del conflicto con la Flota de Cadáveres en Eox con los secretos más íntimos y dolorosos del linaje de Triel Istrav.
  </p>
  
  <p style="font-size: 9.2pt; line-height: 1.45; text-align: justify; margin-bottom: 8px;">
    En este volumen, la tripulación de la <em>Estrella Errante</em> (Benrey Galway, Triel Istrav, Marloc Boosmar, A.Xel 42 y el meca de asalto pesado Gerty) cierra definitivamente sus cuentas pendientes en <strong>Eox</strong>. Tras abatir al vampiro jiangshi Marcellus en la fosa de ácido de la Necrogarganta y encarar la revelación de la sede de <strong>Inversiones Estelares S.C.</strong> —donde Marloc Boosmar asume el sobrecogedor peso de haber fundado la corporación desde una línea temporal futura para otorgarles una segunda oportunidad—, el grupo emprende una incursión clandestina hacia la urbe industrial de <strong>Thanox</strong>. Disfrazados como personal de servicio doméstico en el complejo eugenésico y administrativo de la aristocrática <strong>Casa Istrav</strong>, la tripulación arriesga sus vidas entre intrigas palaciegas drow, conductos tóxicos y contratos de servidumbre para descubrir la verdad sobre la fuga de Keiden Ashton, culminando en un duelo fratricida encarnizado entre Triel y su hermanastra Jhidel Istrav antes de preparar el salto estelar hacia el distante gigante gaseoso Nejeor VI.
  </p>

  <p style="font-size: 9.2pt; line-height: 1.45; text-align: justify; margin-bottom: 10px;">
    La historia adapta con fidelidad absoluta y pulso literario la dirección narrativa del Game Master <strong>Roberto</strong>, junto al elenco original de jugadores:
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
    print("=== Compilación de Volumen 10: La Sombra de Apostae ===")
    
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
        central_pdf_path = os.path.join(central_pdf_dir, "10_Lasers_y_Dragones_Volumen_10_La_Sombra_de_Apostae.pdf")
        import shutil
        shutil.copy2(final_pdf, central_pdf_path)
        print(f"Biblioteca centralizada sincronizada: {central_pdf_path}")

    # Validación final de tamaño
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡Libro Volumen 10 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
