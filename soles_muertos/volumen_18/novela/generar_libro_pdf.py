#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: Los Doce Soles' (Volumen 18)
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
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_18_Los_Doce_Soles.pdf")
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
        "sub": "Contexto, créditos de la mesa original y canon de Paizo Inc."
    },
    {
        "id": "prologo",
        "search_key": "Prólogo: El Eco de los Doce Soles",
        "title": "Prólogo: El Eco de los Doce Soles",
        "sub": "Salida del Maelstrom, coordenadas kishalee y el susurro en los conductos"
    },
    {
        "id": "cap_1",
        "search_key": "Capítulo 1: El Tintineo se Intensifica",
        "title": "Capítulo 1: El Tintineo se Intensifica",
        "sub": "Basado en el Episodio 223 · El polizón de la infoesfera, trampa en camarotes y asalto de sombras"
    },
    {
        "id": "cap_2",
        "search_key": "Capítulo 2: En el Espacio Nadie Te Puede Oír Tintinear",
        "title": "Capítulo 2: En el Espacio Nadie Te Puede Oír Tintinear",
        "sub": "Basado en el Episodio 224 · Duelo en el pasillo, giro de noventa grados y expulsión al vacío"
    },
    {
        "id": "cap_3",
        "search_key": "Capítulo 3: Ponce de Ratón",
        "title": "Capítulo 3: Ponce de Ratón",
        "sub": "Basado en el Episodio 225 · Botín del esquife, salto estelar y llegada al anillo de los Doce Soles"
    },
    {
        "id": "cap_4",
        "search_key": "Capítulo 4: De Boca en Boca",
        "title": "Capítulo 4: De Boca en Boca",
        "sub": "Basado en el Episodio 226 · Travesía en la selva alienígena y choque contra el leviatán de doble mandíbula"
    },
    {
        "id": "cap_5",
        "search_key": "Capítulo 5: Mi Pobre Angelito",
        "title": "Capítulo 5: Mi Pobre Angelito",
        "sub": "Basado en el Episodio 227 · Descenso del heraldo alado del Devorador y el torbellino de basalto"
    },
    {
        "id": "cap_6",
        "search_key": "Capítulo 6: Maldita A.Xel",
        "title": "Capítulo 6: Maldita A.Xel",
        "sub": "Basado en el Episodio 228 · La ponzoña del vacío, agonía biotecnológica y el ritual místico de Charlotte"
    },
    {
        "id": "cap_7",
        "search_key": "Capítulo 7: Granada que Ver",
        "title": "Capítulo 7: Granada que Ver",
        "sub": "Basado en el Episodio 229 · Refugio en las ruinas anegadas, cebo táctico y la emboscada de plasma"
    },
    {
        "id": "cap_8",
        "search_key": "Capítulo 8: ¿Quién es Ustheth?",
        "title": "Capítulo 8: ¿Quién es Ustheth?",
        "sub": "Basado en el Episodio 230 · El rescate de Kiwi, motos gravitatorias y el sello de la directora Osteth"
    },
    {
        "id": "cap_9",
        "search_key": "Capítulo 9: Syfus? Cyrus? Sisyrus? Sisyfo?",
        "title": "Capítulo 9: Syfus? Cyrus? Sisyrus? Sisyfo?",
        "sub": "Basado en el Episodio 231 · Archivos kishalee, emboscada en la oficina y caída de Sangre Fría"
    },
    {
        "id": "cap_10",
        "search_key": "Capítulo 10: ¿Es este el fin de A.Xel 42?",
        "title": "Capítulo 10: ¿Es este el fin de A.Xel 42?",
        "sub": "Basado en el Episodio 232 · Lásers de seguridad, el androide devoto y la salutación a la Primera Causa"
    },
    {
        "id": "cap_11",
        "search_key": "Capítulo 11: Chicas Pesadas",
        "title": "Capítulo 11: Chicas Pesadas",
        "sub": "Basado en el Episodio 233 · Barricadas de chatarra, el ejército de robots y la hija rebelde"
    },
    {
        "id": "cap_12",
        "search_key": "Capítulo 12: Mi Nombre es Jennifer",
        "title": "Capítulo 12: Mi Nombre es Jennifer",
        "sub": "Basado en el Episodio 234 · Desvelo de Jennifer, el refugio de Kiwi y el farol del Martillo del Alba"
    },
    {
        "id": "cap_13",
        "search_key": "Capítulo 13: No sé lo que Hicimos el Año Pasado",
        "title": "Capítulo 13: No sé lo que Hicimos el Año Pasado",
        "sub": "Basado en el Episodio 235 · Asalto al mainframe de Eltreth, caída de las sombras y hallazgo de Syd Velch"
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
<title>Lasers y Dragones: Los Doce Soles</title>
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

  /* ESTILOS DE LA TABLA DE ÍNDICE COMPACTA EN 1 SOLA PÁGINA (16 ENTRADAS) */
  .toc-container {{
    page-break-before: always;
    break-before: page;
    padding: 0;
    margin: 0;
  }}

  .toc-header {{
    font-size: 14pt;
    text-align: center;
    color: #0b1a30;
    margin: 0 0 8px 0;
    padding: 0 0 4px 0;
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
    padding: 2.2px 3px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 7.8pt;
    line-height: 1.15;
    vertical-align: middle;
  }}

  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
    font-size: 8.0pt;
    line-height: 1.15;
    margin: 0;
    padding: 0;
  }}

  .toc-sub {{
    font-size: 6.8pt;
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
    Los Doce Soles
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
    VOLUMEN XVIII · LA DECIMOTERCERA PUERTA I: LOS DOCE SOLES
  </p>
</div>

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 2 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 2: NOTA EDITORIAL E INTRODUCCIÓN -->
<div style="page-break-before: always; break-before: page; padding: 10px 0;">
  <h2 class="section-heading-main" style="page-break-before: avoid; break-before: avoid; margin-bottom: 8px; padding-bottom: 4px; font-size: 14pt;">
    Nota Editorial e Introducción
  </h2>
  
  <p style="font-size: 8.5pt; line-height: 1.38; text-align: justify; margin-bottom: 6px;">
    La presente obra constituye el decimoctavo volumen de la saga de novelizaciones del podcast de rol en vivo costarricense <strong>Lasers y Dragones</strong>, adaptando de manera íntegra, orgánica y cronológica los acontecimientos de los episodios 223 al 235 de la campaña oficial <em>Dead Suns</em> (Soles Muertos) de Paizo Inc. Este libro abre la trascendental adaptación del quinto módulo oficial (<em>The Thirteenth Gate: La Decimotercera Puerta</em>), marcando un hito definitivo en la mitología de los protagonistas con la llegada al legendario sistema de los <strong>Doce Soles</strong> y el desvelo de los misterios biotecnológicos más íntimos de <strong>A.Xel 42</strong>.
  </p>
  
  <p style="font-size: 8.5pt; line-height: 1.38; text-align: justify; margin-bottom: 6px;">
    Tras abandonar las turbulentas corrientes del Maelstrom y sellar la despedida de <strong>Keiden Ashton</strong> a bordo de la nave corsaria de Besmara, la tripulación de la <em>Estrella Errante</em> encara una amenaza insólita y claustrofóbica en los propios pasillos del navío. Un asesino perturbador procedente de los rincones más oscuros de la infoesfera, conocido como el <strong>Hombre Tintineante</strong>, se ha infiltrado a bordo junto a entidades incorpóreas de sombra. El grupo —integrado por el elocuente capitán ysoki <strong>Benrey Galway</strong>, la ingeniosa mecánica semi-drow <strong>Triel Istrav</strong>, el tecnomante de porte académico <strong>Marloc Boosmar</strong>, la letal operativa androide <strong>A.Xel 42</strong>, el meca <strong>Kairos</strong> (la antigua IA del asteroide adaptada al chasis de cuatro brazos con elegancia de tahúr cósmico) y el joven monje androide <strong>Charlotte E2</strong>— debe librar un combate táctico al milímetro en sus propios camarotes para purgar la nave antes de acometer el salto hiperespacial.
  </p>

  <p style="font-size: 8.5pt; line-height: 1.38; text-align: justify; margin-bottom: 6px;">
    Guiada por las coordenadas ancestrales de la Forja Kishalee, la <em>Estrella Errante</em> emerge ante un prodigio de la ingeniería estelar primigenia: un anillo de doce soles en miniatura orbitando un vacío misterioso que custodia la Decimotercera Puerta. Al descender sobre la superficie de una estación biosférica cubierta por una espesa selva extraterrestre, los héroes se enfrentan a depredadores bio-diseñados y a un emisario alado del Culto del Devorador cuya maldición sitúa a A.Xel al borde de la extinción, exigiendo la intervención mística de Charlotte para rescatarla. Adentrándose en el complejo kishalee tras adoptar al animalito alado <strong>Kiwi</strong>, doblegan a la infame mercenaria <strong>Sisyrus Sangre Fría</strong> y descubren que el chasis de A.Xel es reverenciado como la sagrada «Primera Causa». Tras desarmar con ternura filial a su descendiente directa, <strong>Jennifer (Miseria)</strong>, y quebrar el asedio del mainframe corrompido de <strong>Eltreth</strong>, rescatan con vida a la legendaria estrella de rock y telépata <strong>Syd Velch</strong>, preparando el asalto final a la Puerta.
  </p>

  <p style="font-size: 8.5pt; line-height: 1.38; text-align: justify; margin-bottom: 6px;">
    La historia traslada a la prosa literaria la espontaneidad, la comedia, el dramatismo y los profundos lazos afectivos forjados en la mesa de juego bajo la dirección del Game Master <strong>Roberto</strong>, rindiendo tributo al talento y la complicidad de su elenco de jugadores:
  </p>
  
  <!-- MESA DE JUEGO ORIGINAL -->
  <div style="margin: 4px auto; max-width: 500px;">
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 4px auto;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 8.0pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 4px 0; text-indent: 0; text-align: center;">
      ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 8.2pt; color: #2d3748;">
      <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (voces de <strong>Kairos</strong>, <strong>Charlotte</strong>, <strong>Hombre Tintineante</strong>, <strong>Sisyrus</strong>, <strong>Jennifer</strong> y <strong>Syd Velch</strong>)
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 8.2pt; color: #2d3748;">
      <strong style="color: #1a365d;">Miguel:</strong> Benrey Galway <em>(Emisario Ysoki)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em>
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 8.2pt; color: #2d3748;">
      <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc Boosmar <em>(Tecnomante Humano)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa Androide)</em>
    </p>
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 4px auto;">
  </div>

  <!-- AVISO DE PAIZO Y ATRIBUCIÓN -->
  <table style="width: 100%; margin: 6px 0 0 0; border: 1px solid #cbd5e0; background-color: #f8fafc; border-collapse: collapse; page-break-inside: avoid; break-inside: avoid;">
    <tr>
      <td style="padding: 5px 8px; font-size: 7.0pt; color: #4a5568; line-height: 1.25; text-align: justify; border: none;">
        <p style="margin: 0 0 2px 0; text-indent: 0; font-weight: bold; color: #1a365d; font-size: 7.5pt; text-transform: uppercase; letter-spacing: 1px; text-align: center;">
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
    print("=== Compilación de Volumen 18: Los Doce Soles ===")
    
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
        central_pdf_path = os.path.join(central_pdf_dir, "18_Lasers_y_Dragones_Volumen_18_Los_Doce_Soles.pdf")
        shutil.copy2(final_pdf, central_pdf_path)
        print(f"Biblioteca centralizada sincronizada: {central_pdf_path}")

    # Validación final de tamaño
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡Libro Volumen 18 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
