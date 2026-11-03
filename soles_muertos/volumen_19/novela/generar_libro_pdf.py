#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: La Decimotercera Puerta' (Volumen 19)
Genera un documento HTML con estilos editoriales de libro y lo convierte a PDF
siguiendo las directrices técnicas del skill para garantizar marcadores PDF correctos
y números de página exactos en el Índice de Contenidos mediante compilación de 2 pases.
"""

import os
import re
import glob
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPS_DIR = os.path.join(BASE_DIR, "capitulos")
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_19_La_Decimotercera_Puerta.pdf")
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

# Metadata de capítulos para el índice (17 ítems compactos)
TOC_ITEMS = [
    {
        "id": "nota_editorial",
        "search_key": "Nota Editorial e Introducción",
        "title": "Nota Editorial e Introducción",
        "sub": "Contexto, créditos de la mesa original y canon de Paizo Inc."
    },
    {
        "id": "prologo",
        "search_key": "Prólogo: El Eco de la Primera Causa",
        "title": "Prólogo: El Eco de la Primera Causa",
        "sub": "Salida del mainframe, enigma de Syd Velch y el rumor en los Doce Soles"
    },
    {
        "id": "cap_1",
        "search_key": "Capítulo 1: Tiempo de no Velchte",
        "title": "Capítulo 1: Tiempo de no Velchte",
        "sub": "Basado en el Episodio 236 · Revelación de Syd Velch, Ashera y la Forja Viviente"
    },
    {
        "id": "cap_2",
        "search_key": "Capítulo 2: Tal vez Syd Tal Vez No",
        "title": "Capítulo 2: Tal vez Syd Tal Vez No",
        "sub": "Basado en el Episodio 237 · Cifrado del brazo de Marloc y viaje a la Puerta Dos"
    },
    {
        "id": "cap_3",
        "search_key": "Capítulo 3: No me Digas las Probabilidades",
        "title": "Capítulo 3: No me Digas las Probabilidades",
        "sub": "Basado en el Episodio 238 · Travesía orbital y llegada a la fortaleza de la Puerta Dos"
    },
    {
        "id": "cap_4",
        "search_key": "Capítulo 4: Emboscada Inesperada",
        "title": "Capítulo 4: Emboscada Inesperada",
        "sub": "Basado en el Episodio 239 · Tormenta de plasma en el desfiladero y contraataque"
    },
    {
        "id": "cap_5",
        "search_key": "Capítulo 5: Ley 7600",
        "title": "Capítulo 5: Ley 7600",
        "sub": "Basado en el Episodio 240 · Combate de trincheras, rampa kishalee y resistencia heroica"
    },
    {
        "id": "cap_6",
        "search_key": "Capítulo 6: El Día que Marloc Arruinó el Combate",
        "title": "Capítulo 6: El Día que Marloc Arruinó el Combate",
        "sub": "Basado en el Episodio 241 · Llegada de Drech y el campo de ralentización temporal"
    },
    {
        "id": "cap_7",
        "search_key": "Capítulo 7: Maroon 1",
        "title": "Capítulo 7: Maroon 1",
        "sub": "Basado en el Episodio 242 · Botín de UPBs ensangrentados y avance hacia los servicios"
    },
    {
        "id": "cap_8",
        "search_key": "Capítulo 8: Terror en el Toilette",
        "title": "Capítulo 8: Terror en el Toilette",
        "sub": "Basado en el Episodio 243 · Monstruo en las letrinas y tarjetas de colores kishalee"
    },
    {
        "id": "cap_9",
        "search_key": "Capítulo 9: Nunca Te Dije Que Te Quería",
        "title": "Capítulo 9: Nunca Te Dije Que Te Quería",
        "sub": "Basado en el Episodio 244 · Trampa en el laboratorio y batalla contra las dos bestias"
    },
    {
        "id": "cap_10",
        "search_key": "Capítulo 10: Escaneando Ando",
        "title": "Capítulo 10: Escaneando Ando",
        "sub": "Basado en el Episodio 245 · Reparación de Kairos, ducto de A.Xel y mapeo del sector"
    },
    {
        "id": "cap_11",
        "search_key": "Capítulo 11: Null-9",
        "title": "Capítulo 11: Null-9",
        "sub": "Basado en el Episodio 246 · Cara a cara, duelo ideológico y redención maternal de Null-9"
    },
    {
        "id": "cap_12",
        "search_key": "Capítulo 12: ¿I.A.hora qué Hacemos?",
        "title": "Capítulo 12: ¿I.A.hora qué Hacemos?",
        "sub": "Basado en el Episodio 247 · Traición digital de Eltreth y rebelión de centinelas"
    },
    {
        "id": "cap_13",
        "search_key": "Capítulo 13: La Gran Loco-motora que No Pudo",
        "title": "Capítulo 13: La Gran Loco-motora que No Pudo",
        "sub": "Basado en el Episodio 248 · Choque frontal contra el titán de demolición de Eltreth"
    },
    {
        "id": "cap_14",
        "search_key": "Capítulo 14: La Treceava Puerta",
        "title": "Capítulo 14: La Treceava Puerta",
        "sub": "Basado en el Episodio 249 · Módulo maestro, alineación de los Doce Soles y salto al portal"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial: Dossier de Personajes y Glosario",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "Facciones galácticas, elenco de la mesa y dossier biográfico"
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
            
    # Generar filas del índice de contenidos
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
<title>Lasers y Dragones: La Decimotercera Puerta</title>
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
  margin-top: 20px;
  margin-bottom: 20px;
  line-height: 1.3;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 12px;
}}

.chap-sub {{
  font-size: 16pt;
  font-style: italic;
  color: #2b6cb0;
  font-weight: normal;
}}

h3.section-title {{
  font-size: 13.5pt;
  color: #2b6cb0;
  margin-top: 22px;
  margin-bottom: 10px;
  border-bottom: 1px dashed #e2e8f0;
  padding-bottom: 4px;
  font-family: 'Liberation Serif', serif;
}}

h3.subsection-title {{
  font-size: 12pt;
  color: #2d3748;
  margin-top: 18px;
  margin-bottom: 8px;
  font-family: 'Liberation Serif', serif;
}}

h4.subsection-title {{
  font-size: 11pt;
  color: #1a365d;
  margin-top: 14px;
  margin-bottom: 5px;
  font-weight: bold;
  font-family: 'Liberation Serif', serif;
}}

p {{
  text-align: justify;
  text-justify: inter-word;
  margin: 0 0 11px 0;
  text-indent: 1.5em;
}}

p:first-of-type, .divider + p, .section-title + p, .subsection-title + p {{
  text-indent: 0;
}}

.divider {{
  text-align: center;
  margin: 20px 0;
  color: #a0aec0;
  font-size: 9pt;
  letter-spacing: 5px;
}}

.bullet-list {{
  margin: 10px 0 12px 22px;
  padding: 0;
}}

.bullet-list li {{
  margin-bottom: 5px;
  text-align: justify;
}}

.quote {{
  margin: 15px 22px;
  padding: 8px 15px;
  border-left: 3px solid #b8860b;
  background: #f7fafc;
  font-style: italic;
  color: #4a5568;
}}

  /* ESTILOS DE LA TABLA DE ÍNDICE COMPACTA EN 1 SOLA PÁGINA (17 ENTRADAS) */
  .toc-container {{
    page-break-before: always;
    break-before: page;
    padding: 0;
    margin: 0;
  }}

  .toc-header {{
    font-size: 13.5pt;
    text-align: center;
    color: #0b1a30;
    margin: 0 0 6px 0;
    padding: 0 0 3px 0;
    border-bottom: 2px solid #b8860b;
    page-break-before: always;
    break-before: page;
    font-family: 'Liberation Serif', serif;
  }}

  .toc-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0;
    padding: 0;
  }}

  .toc-table td {{
    padding: 1.8px 3px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 7.6pt;
    line-height: 1.15;
    vertical-align: middle;
  }}

  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
    font-size: 7.8pt;
    line-height: 1.12;
    margin: 0;
    padding: 0;
  }}

  .toc-sub {{
    font-size: 6.6pt;
    color: #718096;
    font-style: italic;
    line-height: 1.05;
    margin: 0;
    padding: 0;
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
  
  <div style="font-size: 28pt; font-weight: bold; color: #0b1a30; margin: 20px 0 10px 0; letter-spacing: 2px; text-align: center;">
    LASERS Y DRAGONES
  </div>
  
  <div style="font-size: 20pt; font-style: italic; color: #b8860b; margin: 10px 0 20px 0; text-align: center;">
    La Decimotercera Puerta
  </div>
  
  <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 20px auto;">
  
  <div style="font-size: 14pt; color: #2b6cb0; margin: 25px 0;">
    ✦ &nbsp; ◈ &nbsp; ✦
  </div>
  
  <p style="font-size: 10.5pt; line-height: 1.6; color: #4a5568; margin: 30px auto; max-width: 420px; text-indent: 0; text-align: center;">
    Una adaptación novelada de la campaña oficial <em>Dead Suns</em> (Soles Muertos), inspirada en las sesiones de rol en vivo del podcast <strong>Lasers y Dragones</strong>.
  </p>
  
  <hr style="border: none; border-top: 1px solid #cbd5e0; width: 80%; margin: 50px auto 20px auto;">
  
  <p style="font-family: 'Liberation Sans', sans-serif; font-size: 9.5pt; letter-spacing: 3px; text-transform: uppercase; color: #1a365d; margin: 0; text-indent: 0; text-align: center;">
    VOLUMEN XIX · LA DECIMOTERCERA PUERTA II: EL DUELO DE LOS ANDROIDES
  </p>
</div>

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 2 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 2: NOTA EDITORIAL E INTRODUCCIÓN -->
<div style="page-break-before: always; break-before: page; padding: 5px 0 0 0;">
  <h2 class="section-heading-main" style="page-break-before: avoid; break-before: avoid; margin-bottom: 6px; padding-bottom: 3px; font-size: 13pt;">
    Nota Editorial e Introducción
  </h2>
  
  <p style="font-size: 8.2pt; line-height: 1.32; margin-bottom: 4px; text-align: justify; text-indent: 1.2em;">
    La presente obra constituye el decimonoveno volumen de la saga de novelizaciones del podcast de rol en vivo costarricense <strong>Lasers y Dragones</strong>, adaptando de manera íntegra, orgánica y cronológica los acontecimientos de los episodios 236 al 249 de la campaña oficial <em>Dead Suns</em> (Soles Muertos) de Paizo Inc. Este libro culmina la monumental adaptación del quinto módulo oficial (<em>The Thirteenth Gate: La Decimotercera Puerta</em>), llevando a su punto de máxima ebullición la confrontación filosófica, mística y militar entre la tripulación de la <em>Estrella Errante</em> y el Culto del Devorador.
  </p>
  
  <p style="font-size: 8.2pt; line-height: 1.32; margin-bottom: 4px; text-align: justify; text-indent: 1.2em;">
    Tras rescatar de las profundidades del mainframe central a la legendaria estrella de rock y poderoso telépata <strong>Syd Velch</strong>, y tras el conmovedor desarme emocional de la joven androide <strong>Jennifer</strong> (alias <strong>Miseria</strong>), el equipo —integrado por el audaz capitán ysoki <strong>Benrey Galway</strong>, la intrépida ingeniera semi-drow <strong>Triel Istrav</strong>, el tecnomante erudito <strong>Marloc Boosmar</strong>, la operativa androide <strong>A.Xel 42</strong>, el meca <strong>Kairos</strong> (la antigua IA del casino en su chasis de asalto de cuatro brazos), el monje androide <strong>Charlotte E2</strong> y su entrañable mascota alada <strong>Kiwi</strong>— descubre que la archirrival <strong>Null-9</strong> se ha atrincherado en la <strong>Puerta 2</strong> de la megaestructura para hacerse con el módulo maestro de control.
  </p>
  
  <p style="font-size: 8.2pt; line-height: 1.32; margin-bottom: 4px; text-align: justify; text-indent: 1.2em;">
    A lo largo de catorce intensos capítulos, los héroes deben surcar el vacío entre los soles en motos gravitatorias kishalee y resistir una implacable emboscada artillera. Tras doblegar al sanguinario enano <strong>Drech</strong> mediante la astucia temporal de Marloc («El Día que Marloc Arruinó el Combate»), sortear peligros insólitos en las instalaciones milenarias («Terror en el Toilette») y sobrevivir a una trampa mortal contra bestias bio-diseñadas en los laboratorios sellados («Nunca Te Dije Que Te Quería»), A.Xel encara su mayor destino: el duelo cara a cara contra Null-9 («Null-9»). Allí, la revelación de <strong>Ashera</strong> y de la <strong>Forja Viviente</strong> se alza como el baluarte espiritual definitivo contra el nihilismo del Devorador. Al destruir la titánica locomotora de guerra de la IA corrompida <strong>Eltreth</strong> («La Gran Loco-motora que No Pudo»), los héroes abren triunfalmente la mítica <strong>Decimotercera Puerta</strong>, desvelando el umbral cósmico que conduce al Devastador Estelar.
  </p>
  
  <div style="margin: 4px auto; max-width: 500px;">
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 3px auto;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 7.8pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 3px 0; text-indent: 0; text-align: center;">
      ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
    </p>
    <p style="margin: 1px 0; text-indent: 0; text-align: center; font-size: 8pt; color: #2d3748;">
      <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (y voces de Kairos, Charlotte, Syd Velch, Drech, Null-9 y Eltreth) &nbsp;|&nbsp; <strong style="color: #1a365d;">Miguel:</strong> Benrey Galway <em>(Emisario Ysoki)</em>
    </p>
    <p style="margin: 1px 0; text-indent: 0; text-align: center; font-size: 8pt; color: #2d3748;">
      <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc Boosmar <em>(Tecnomante Humano)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa Androide)</em>
    </p>
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 3px auto;">
  </div>
  
  <table style="width: 100%; margin: 3px 0 0 0; border: 1px solid #cbd5e0; background-color: #f8fafc; border-collapse: collapse; page-break-inside: avoid; break-inside: avoid;">
    <tr>
      <td style="padding: 4px 8px; font-size: 6.8pt; color: #4a5568; line-height: 1.2; text-align: justify; border: none;">
        <p style="margin: 0 0 2px 0; text-indent: 0; font-weight: bold; color: #1a365d; font-size: 7.2pt; text-transform: uppercase; letter-spacing: 1px; text-align: center;">
          Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución
        </p>
        <p style="margin: 0 0 2px 0; text-indent: 0;">
          Esta obra literaria y sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de <strong>Paizo Inc.</strong>, utilizados bajo la <em>Política de Uso Comunitario de Paizo</em> (<a href="https://paizo.com/communityuse" style="color: #2b6cb0; text-decoration: none;">paizo.com/communityuse</a>). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de <em>Starfinder</em> y <em>Pathfinder</em>, visite <a href="https://paizo.com" style="color: #2b6cb0; text-decoration: none;">paizo.com</a>.
        </p>
        <p style="margin: 0; text-indent: 0;">
          Asimismo, esta novelización constituye un tributo no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense <strong>Lasers y Dragones</strong>. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: <strong>Roberto</strong> (Game Master y Kairos), <strong>Miguel</strong> (Benrey Galway), <strong>Irene</strong> (Triel), <strong>Juan Pablo</strong> (Marloc Boosmar) y <strong>Sofía</strong> (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
        </p>
      </td>
    </tr>
  </table>
</div>

<!-- PÁGINA 3: ÍNDICE DE CONTENIDOS -->
<div class="toc-container" style="page-break-before: always; break-before: page; padding: 0; margin: 0;">
  <h2 class="toc-header" style="page-break-before: always; break-before: page;">
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
    print("=== Compilación de Volumen 19: La Decimotercera Puerta ===")
    
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
    if not os.path.exists(central_pdf_dir):
        central_pdf_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "libros_pdf"))
    if os.path.exists(central_pdf_dir):
        central_pdf_path = os.path.join(central_pdf_dir, "19_Lasers_y_Dragones_Volumen_19_La_Decimotercera_Puerta.pdf")
        shutil.copy2(final_pdf, central_pdf_path)
        print(f"Biblioteca centralizada sincronizada: {central_pdf_path}")

    # Validación final de tamaño
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡Libro Volumen 19 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
