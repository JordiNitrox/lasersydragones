#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: La Nave de Besmara' (Volumen 17)
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
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_17_La_Nave_de_Besmara.pdf")
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
        "search_key": "Prólogo: Las Mareas del Caos",
        "title": "Prólogo: Las Mareas del Caos",
        "sub": "El salto dimensional, el influjo del Maelstrom y la búsqueda de Keiden Ashton"
    },
    {
        "id": "cap_1",
        "search_key": "Capítulo 1: Un ¿Viernes? de Locos",
        "title": "Capítulo 1: Un ¿Viernes? de Locos",
        "sub": "Basado en el Episodio 202 · Onda de caos, intercambio de cuerpos y el nacimiento en la niebla"
    },
    {
        "id": "cap_2",
        "search_key": "Capítulo 2: Se Viene el Culebrón",
        "title": "Capítulo 2: Se Viene el Culebrón",
        "sub": "Basado en el Episodio 203 · La taberna corsaria, sirenas serpentinas y la estatua de Keiden"
    },
    {
        "id": "cap_3",
        "search_key": "Capítulo 3: La Sombra del Cuervo",
        "title": "Capítulo 3: La Sombra del Cuervo",
        "sub": "Basado en el Episodio 204 · Retorno anatómico, psicoplástico vivo y la fragata drow de Apostae"
    },
    {
        "id": "cap_4",
        "search_key": "Capítulo 4: Esto me Parece Familiar",
        "title": "Capítulo 4: Esto me Parece Familiar",
        "sub": "Basado en el Episodio 205 · Rastro de la Casa Istrav, montacargas naval y la sombra de Jhidel"
    },
    {
        "id": "cap_5",
        "search_key": "Capítulo 5: King Golarian vs Los Atómicos",
        "title": "Capítulo 5: King Golarian vs Los Atómicos",
        "sub": "Basado en el Episodio 206 · Simulación de celuloide, King Golarian y el asalto de Los Atómicos"
    },
    {
        "id": "cap_6",
        "search_key": "Capítulo 6: Splinter Axcell",
        "title": "Capítulo 6: Splinter Axcell",
        "sub": "Basado en el Episodio 207 · Infiltración en vigas superiores, sigilo de A.Xel y sabotaje drow"
    },
    {
        "id": "cap_7",
        "search_key": "Capítulo 7: El Poder de Jhidel",
        "title": "Capítulo 7: El Poder de Jhidel",
        "sub": "Basado en el Episodio 208 · Fuego cruzado en el hangar, la Guardia Negra y el poder tecno-mágico"
    },
    {
        "id": "cap_8",
        "search_key": "Capítulo 8: Triel vs Jhidel (la Revancha)",
        "title": "Capítulo 8: Triel vs Jhidel (la Revancha)",
        "sub": "Basado en el Episodio 209 · Duelo fratricida, triunfo de Triel y la piedad que quiebra la venganza"
    },
    {
        "id": "cap_9",
        "search_key": "Capítulo 9: A Mi Hermana con Cariño",
        "title": "Capítulo 9: A Mi Hermana con Cariño",
        "sub": "Basado en el Episodio 210 · Retirada de la Casa Istrav, renuncia al blasón y libertad de Triel"
    },
    {
        "id": "cap_10",
        "search_key": "Capítulo 10: Elemental Mi Querido Marloc",
        "title": "Capítulo 10: Elemental Mi Querido Marloc",
        "sub": "Basado en el Episodio 211 · Realidad maleable, gabardinas de cine negro y la pista de los 20 años"
    },
    {
        "id": "cap_11",
        "search_key": "Capítulo 11: Llamada Mortal",
        "title": "Capítulo 11: Llamada Mortal",
        "sub": "Basado en el Episodio 212 · Tormenta de nieve, la cabina de teléfono y las voces del pasado"
    },
    {
        "id": "cap_12",
        "search_key": "Capítulo 12: ¡Caracoles amigos!",
        "title": "Capítulo 12: ¡Caracoles amigos!",
        "sub": "Basado en el Episodio 213 · Encuentro pacífico con caracoles psicoplásticos y el rescate de Panquecito"
    },
    {
        "id": "cap_13",
        "search_key": "Capítulo 13: Los Psicoplásticos son Inevitables",
        "title": "Capítulo 13: Los Psicoplásticos son Inevitables",
        "sub": "Basado en el Episodio 214 · Grietas axiomáticas en el nodo central e intrusión dimensional de Axis"
    },
    {
        "id": "cap_14",
        "search_key": "Capítulo 14: Nadie Espera la Inevitable Inquisición",
        "title": "Capítulo 14: Nadie Espera la Inevitable Inquisición",
        "sub": "Basado en el Episodio 215 · La inquisición del Inevitable, cuentas del tiempo y juicio a Marloc"
    },
    {
        "id": "cap_15",
        "search_key": "Capítulo 15: Marloc - El Juicio Final",
        "title": "Capítulo 15: Marloc - El Juicio Final",
        "sub": "Basado en el Episodio 216 · Juicio moral en el portal temporal, renuncia a Olivia y lealtad a la familia"
    },
    {
        "id": "cap_16",
        "search_key": "Capítulo 16: Triel, Eres un Caos",
        "title": "Capítulo 16: Triel, Eres un Caos",
        "sub": "Basado en el Episodio 217 · Corrientes caóticas en gravedad cero y acrobacias cinéticas de Triel"
    },
    {
        "id": "cap_17",
        "search_key": "Capítulo 17: Los Atómicos y el Multiverso de la Locura",
        "title": "Capítulo 17: Los Atómicos y el Multiverso de la Locura",
        "sub": "Basado en el Episodio 218 · Constructos oníricos del Maelstrom y asalto a través del vórtice"
    },
    {
        "id": "cap_18",
        "search_key": "Capítulo 18: Keiden Ashton",
        "title": "Capítulo 18: Keiden Ashton",
        "sub": "Basado en el Episodio 219 · El puente vivo de Besmara y el hallazgo del cuerpo marchito de Keiden"
    },
    {
        "id": "cap_19",
        "search_key": "Capítulo 19: El Corazón del Padre",
        "title": "Capítulo 19: El Corazón del Padre",
        "sub": "Basado en el Episodio 220 · Cirugía mística, división de la Piedra Corazón y abrazo filial"
    },
    {
        "id": "cap_20",
        "search_key": "Capítulo 20: Piratas a la Plancha",
        "title": "Capítulo 20: Piratas a la Plancha",
        "sub": "Basado en el Episodio 221 · Banquete corsario a la plancha, revelación del sacrificio y brindis"
    },
    {
        "id": "cap_21",
        "search_key": "Capítulo 21: Tintineo Intenso",
        "title": "Capítulo 21: Tintineo Intenso",
        "sub": "Basado en el Episodio 222 · Tributo de monedas a Besmara, despedida y rumbo a los Doce Soles"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial: Dossier de Personajes y Glosario",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "Facciones galácticas, elenco de la mesa y glosario de términos"
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
<title>Lasers y Dragones: La Nave de Besmara</title>
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

  /* ESTILOS DE LA TABLA DE ÍNDICE COMPACTA EN 1 SOLA PÁGINA (24 ENTRADAS) */
  .toc-header {{
    font-size: 13pt;
    text-align: center;
    color: #0b1a30;
    margin: 0 0 4px 0;
    padding: 0 0 2px 0;
    border-bottom: 2px solid #b8860b;
    page-break-before: avoid;
    break-before: avoid;
    font-family: 'Liberation Serif', serif;
  }}

  .toc-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0;
    padding: 0;
  }}

  .toc-table td {{
    padding: 0.4px 2px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 6.5pt;
    line-height: 1.02;
    vertical-align: middle;
  }}

  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
    font-size: 6.6pt;
    line-height: 1.02;
    margin: 0;
    padding: 0;
  }}

  .toc-sub {{
    font-size: 5.6pt;
    color: #718096;
    font-style: italic;
    line-height: 0.98;
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
  
  <div style="font-size: 19pt; font-style: italic; color: #b8860b; margin: 10px 0 20px 0; text-align: center;">
    La Nave de Besmara
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
    VOLUMEN XVII · EL CORAZÓN DEL PADRE II: LA NAVE DE BESMARA
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
    La presente obra constituye el decimoséptimo volumen de la saga de novelizaciones del podcast de rol en vivo costarricense <strong>Lasers y Dragones</strong>, adaptando de manera íntegra, orgánica y cronológica los acontecimientos de los episodios 202 al 222 de la campaña oficial <em>Dead Suns</em> (Soles Muertos) de Paizo Inc. Este volumen desarrolla en toda su magnitud el arco propio y canónico de la búsqueda de <strong>Keiden Ashton</strong>: la audaz incursión de la <em>Estrella Errante</em> en las corrientes enloquecidas del <strong>Maelstrom</strong> de la Deriva, el abordaje del legendario navío vivo psicoplástico bendecido por la diosa pirata <strong>Besmara</strong> y la histórica resolución de los lazos familiares de <strong>Triel</strong>.
  </p>
  
  <p style="font-size: 8.5pt; line-height: 1.38; text-align: justify; margin-bottom: 6px;">
    Tras atravesar la fractura hiperespacial abierta en el asteroide Kairos gracias a la resonancia de la Piedra Corazón ligada a su padre, la tripulación sufre de inmediato el influjo desquiciante del caos primordial. Una marea dimensional transmuta el navío e intercambia las mentes y cuerpos de los protagonistas en una caótica vorágine de identidades cruzadas, al tiempo que la inteligencia artificial del asteroide, <strong>Kairos</strong>, se adapta a su nueva existencia física habitando el chasis del meca bípedo y aportando su serenidad de tahúr y estratega probabilístico. Superado el estupor inicial y restaurada la anatomía de los tripulantes, el pasado persigue a Triel hasta los confines de la Deriva: su hermanastra drow pura, <strong>Jhidel Istrav</strong>, lidera una implacable fuerza de abordaje de la Casa Istrav dispuesta a exterminarla, desatando una cruenta revancha donde Triel, respaldada por la letalidad quirúrgica de <strong>A.Xel 42</strong> y el ingenio de <strong>Benrey Galway</strong>, quiebra para siempre el yugo aristocrático de Apostae.
  </p>

  <p style="font-size: 8.5pt; line-height: 1.38; text-align: justify; margin-bottom: 6px;">
    A medida que se adentran en las cubiertas más profundas del navío de Besmara, la realidad maleable de la nave proyecta visiones nacidas de los recuerdos y anhelos del capitán perdido: desde estrafalarias investigaciones detectivescas en blanco y negro hasta el severo tribunal de un <strong>Inevitable</strong> de Axis, constructo cósmico convocado por los agravios del tiempo. En este cruce de caminos dimensionales, <strong>Marloc Boosmar</strong> encara su más desgarradora prueba moral al confrontar el rencor de Olivia y la resucitada Amelie, eligiendo la lealtad hacia sus camaradas y el futuro de su familia mientras su esposa Ángela da a luz a su primogénita en Kairos bajo la custodia del enano Zivok. Finalmente, tras abrirse paso entre corsarios espectrales y reflejos deformados, Triel alcanza los motores de salto y encuentra el cuerpo marchito de su padre Keiden Ashton. Mediante una intervención quirúrgica mística en la que injerta la Piedra Corazón en su pecho, Triel devuelve el aliento al legendario corsario humano, fundiéndose en un abrazo largamente postergado y sellando una alianza pirata interdimensional antes de que la tripulación enfile sus motores hacia la mítica Puerta de los Doce Soles.
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
      <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (y las voces de <strong>Kairos</strong>, <strong>Keiden</strong> y el <strong>Inevitable</strong>) &nbsp;|&nbsp; <strong style="color: #1a365d;">Miguel:</strong> Benrey Galway <em>(Emisario Ysoki)</em>
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 8.2pt; color: #2d3748;">
      <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc Boosmar <em>(Tecnomante Humano)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa Androide)</em>
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

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 3 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 3: ÍNDICE DE CONTENIDOS -->
<div style="padding: 0; margin: 0;">
  <h2 class="toc-header">
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
    print("=== Compilación de Volumen 17: La Nave de Besmara ===")
    
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
        central_pdf_path = os.path.join(central_pdf_dir, "17_Lasers_y_Dragones_Volumen_17_La_Nave_de_Besmara.pdf")
        shutil.copy2(final_pdf, central_pdf_path)
        print(f"Biblioteca centralizada sincronizada: {central_pdf_path}")

    # Validación final de tamaño
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡Libro Volumen 17 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
