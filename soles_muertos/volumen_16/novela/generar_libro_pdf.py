#!/usr/bin/env python3
"""
Compilador y maquetador de la novela 'Lasers y Dragones: El Secreto de la Deriva' (Volumen 16)
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
PDF_OUTPUT = os.path.join(BASE_DIR, "Lasers_y_Dragones_Volumen_16_El_Secreto_de_la_Deriva.pdf")
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
        "search_key": "Prólogo: El Laberinto de la Forja",
        "title": "Prólogo: El Laberinto de la Forja",
        "sub": "El enigma kishalee, la caída de Null-9 y la marcha hacia el Maelstrom"
    },
    {
        "id": "cap_1",
        "search_key": "Capítulo 1: Ridículo en el Cubículo",
        "title": "Capítulo 1: Ridículo en el Cubículo",
        "sub": "Basado en el Episodio 186 · Oficinas ancestrales, emboscada de eolis y la caída de Triel"
    },
    {
        "id": "cap_2",
        "search_key": "Capítulo 2: La Señora de los Aliolis",
        "title": "Capítulo 2: La Señora de los Aliolis",
        "sub": "Basado en el Episodio 187 · El martillo de Zivok, curación de campaña y la puerta secreta"
    },
    {
        "id": "cap_3",
        "search_key": "Capítulo 3: Xavra Dios",
        "title": "Capítulo 3: Xavra Dios",
        "sub": "Basado en el Episodio 188 · La gran biblioteca, el campeón solariano y el cono gravitatorio"
    },
    {
        "id": "cap_4",
        "search_key": "Capítulo 4: Dios Xavra",
        "title": "Capítulo 4: Dios Xavra",
        "sub": "Basado en el Episodio 189 · Supernova, el disparo crítico de Triel y el rescate de Charlotte E2"
    },
    {
        "id": "cap_5",
        "search_key": "Capítulo 5: La Telaraña de Charlotte",
        "title": "Capítulo 5: La Telaraña de Charlotte",
        "sub": "Basado en el Episodio 190 · Guerra Sivv-Kishalee, los Doce Soles y la leyenda de Besmara"
    },
    {
        "id": "cap_6",
        "search_key": "Capítulo 6: Escape de Nejeor",
        "title": "Capítulo 6: Escape de Nejeor",
        "sub": "Basado en el Episodio 191 · Vuelo de Benrey, caravana de Tzayl y el bloqueo de Kairos"
    },
    {
        "id": "cap_7",
        "search_key": "Capítulo 7: Yo Soy tu Amigobling Fiel",
        "title": "Capítulo 7: Yo Soy tu Amigobling Fiel",
        "sub": "Basado en el Episodio 192 · Oficiales Willy y Naru, Marloc y Ángela y la llegada de Alistrav"
    },
    {
        "id": "cap_8",
        "search_key": "Capítulo 8: Abuelita Dime Tú",
        "title": "Capítulo 8: Abuelita Dime Tú",
        "sub": "Basado en el Episodio 193 · El fraude post-Brecha de los Istrav, Keiden Ashton y el rechazo de Triel"
    },
    {
        "id": "cap_9",
        "search_key": "Capítulo 9: Se Me Subió el Muerto",
        "title": "Capítulo 9: Se Me Subió el Muerto",
        "sub": "Basado en el Episodio 194 · Intimidación a los emisarios de Eox y el barullo pirata en El Cuerno Oscuro"
    },
    {
        "id": "cap_10",
        "search_key": "Capítulo 10: Todos Somos Keiden",
        "title": "Capítulo 10: Todos Somos Keiden",
        "sub": "Basado en el Episodio 195 · Pelea de taberna, artes marciales de Charlotte y la espuma de Brangulya"
    },
    {
        "id": "cap_11",
        "search_key": "Capítulo 11: Dos Hombres, un Camino",
        "title": "Capítulo 11: Dos Hombres, un Camino",
        "sub": "Basado en el Episodio 196 · Negociación con León, filtro de datos kish y rumbo a Daline 3"
    },
    {
        "id": "cap_12",
        "search_key": "Capítulo 12: Mamma Mia",
        "title": "Capítulo 12: Mamma Mia",
        "sub": "Basado en el Episodio 197 · El mundo de agua, la estatua de A1 y las 42 vidas de A.Xel"
    },
    {
        "id": "cap_13",
        "search_key": "Capítulo 13: El Episodio de la Playa",
        "title": "Capítulo 13: El Episodio de la Playa",
        "sub": "Basado en el Episodio 198 · Emancipación de Charlotte, días de tregua y la emboscada del Fuego en el Cielo"
    },
    {
        "id": "cap_14",
        "search_key": "Capítulo 14: Láser y Dragón",
        "title": "Capítulo 14: Láser y Dragón",
        "sub": "Basado en el Episodio 199 · La libertad de Shirka, juicio en el hangar y la capitulación de Samanis"
    },
    {
        "id": "cap_15",
        "search_key": "Capítulo 15: De un Monstruo a Otro",
        "title": "Capítulo 15: De un Monstruo a Otro",
        "sub": "Basado en el Episodio 200 · Baby shower de Ángela y Marloc, Ambrose y el dilema de los monstruos"
    },
    {
        "id": "cap_16",
        "search_key": "Capítulo 16: El As Bajo la Manga",
        "title": "Capítulo 16: El As Bajo la Manga",
        "sub": "Basado en el Episodio 201 · La Piedra Corazón, el sacrificio de Gerty, el horror abisal y el salto al Maelstrom"
    },
    {
        "id": "glosario",
        "search_key": "Anexo Especial: Dossier de Personajes y Glosario",
        "title": "Anexo Especial: Dossier de Personajes y Glosario",
        "sub": "Kairos, Daline 3, la tripulación de la Estrella Errante y linajes ancestrales"
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

    # Filas de la tabla de contenidos compacta
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
<title>Lasers y Dragones: El Secreto de la Deriva</title>
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
    font-size: 20pt;
    text-align: center;
    color: #0b1a30;
    margin-top: 0;
    margin-bottom: 20px;
    border-bottom: 2px solid #b8860b;
    padding-bottom: 8px;
    page-break-before: always;
    break-before: page;
  }}
  
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
  
  /* ESTILOS DE LA TABLA DE ÍNDICE COMPACTA EN 1 SOLA PÁGINA (19 ENTRADAS) */
  .toc-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1px 0;
  }}
  
  .toc-table td {{
    padding: 1.5px 3px;
    border-bottom: 1px dotted #cbd5e0;
    font-size: 7.5pt;
    line-height: 1.10;
  }}
  
  .toc-title {{
    font-weight: bold;
    color: #0b1a30;
  }}
  
  .toc-sub {{
    font-size: 6.8pt;
    color: #718096;
    font-style: italic;
    line-height: 1.05;
  }}
</style>
</head>
<body>

<!-- PÁGINA 1: PORTADA -->
<div style="text-align: center; padding: 40px 10px; margin: 0 auto; max-width: 500px;">
  <p style="font-family: 'Liberation Sans', sans-serif; font-size: 11pt; letter-spacing: 5px; text-transform: uppercase; color: #2b6cb0; margin: 40px 0 20px 0; text-indent: 0;">
    Ópera Espacial · Universo Starfinder
  </p>
  
  <hr style="border: none; border-top: 2px solid #1a365d; width: 60%; margin: 25px auto;">
  
  <div style="font-size: 30pt; font-weight: bold; color: #0b1a30; margin: 20px 0 10px 0; letter-spacing: 2px; text-align: center;">
    LASERS Y DRAGONES
  </div>
  
  <div style="font-size: 20pt; font-style: italic; color: #b8860b; margin: 10px 0 20px 0; text-align: center;">
    El Secreto de la Deriva
  </div>
  
  <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 20px auto;">
  
  <div style="font-size: 14pt; color: #2b6cb0; margin: 25px 0;">
    ✦ &nbsp; ◈ &nbsp; ✦
  </div>
  
  <p style="font-size: 10.5pt; line-height: 1.6; color: #4a5568; margin: 25px auto; max-width: 440px; text-indent: 0; text-align: center;">
    Adaptación literaria integral de los episodios 186 al 201 del podcast <strong>Lasers y Dragones</strong>.<br>
    <em>El duelo contra Xavra y la caída del Portal Estelar en La Forja,<br>
    el rescate de Charlotte E2, la convocatoria drow de la Matriarca Alistrav,<br>
    el santuario de A1 en Daline 3, el juicio contra la Legión del Fuego en el Cielo<br>
    y el salto dimensional hacia el Maelstrom tras el sacrificio de Gerty.</em>
  </p>
  
  <hr style="border: none; border-top: 1px solid #cbd5e0; width: 80%; margin: 40px auto 20px auto;">
  
  <p style="font-family: 'Liberation Sans', sans-serif; font-size: 9.5pt; letter-spacing: 3px; text-transform: uppercase; color: #1a365d; margin: 0; text-indent: 0; text-align: center;">
    VOLUMEN XVI · EL CORAZÓN DEL PADRE I: EL SECRETO DE LA DERIVA
  </p>
</div>

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 2 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 2: NOTA EDITORIAL E INTRODUCCIÓN -->
<div style="page-break-before: always; break-before: page; padding: 10px 0;">
  <h2 class="section-heading-main" style="page-break-before: avoid; break-before: avoid; margin-bottom: 10px; padding-bottom: 4px; font-size: 15pt;">
    Nota Editorial e Introducción
  </h2>
  
  <p style="font-size: 8.8pt; line-height: 1.40; text-align: justify; margin-bottom: 7px;">
    La presente obra constituye el decimosexto volumen de la saga de novelizaciones del podcast de rol en vivo costarricense <strong>Lasers y Dragones</strong>, adaptando de manera íntegra, orgánica y cronológica los acontecimientos de los episodios 186 al 201 de la campaña oficial <em>Dead Suns</em> (Soles Muertos) de Paizo Inc. Este volumen culmina la desesperada incursión en las entrañas de la mítica metrópoli flotante de <strong>Istamak</strong> en <strong>Nejeor VI</strong>, el repliegue estratégico hacia el asteroide independiente <strong>Kairos</strong> y los trascendentales preparativos para la incursión definitiva hacia el <strong>Maelstrom</strong> en busca del legendario navío de la diosa Besmara capitaneado por Keiden Ashton.
  </p>
  
  <p style="font-size: 8.8pt; line-height: 1.40; text-align: justify; margin-bottom: 7px;">
    En el corazón de la Forja Kishalee, la tripulación de la <em>Estrella Errante</em> enfrenta su prueba de fuego más implacable contra los fanáticos del Culto del Devorador y las fuerzas ancestrales que custodian el Portal Estelar. Tras un cruento duelo en los cubículos de investigación y en la majestuosa biblioteca contra el campeón solar kish Xavra, el ingenio táctico y el devastador disparo de Triel Istrav permiten arrebatar la gema llave antes de la detonación del portal provocada por Null-9. En medio de los escombros de la civilización kishalee, un joven monje androide rebelde, rescatado del influjo del culto y bautizado por A.Xel 42 como <strong>Charlotte E2</strong>, se une a los héroes en su arriesgado escape de la atmósfera tóxica del gigante gaseoso con el invaluable apoyo de la tribu de la profetisa Tzayl.
  </p>

  <p style="font-size: 8.8pt; line-height: 1.40; text-align: justify; margin-bottom: 7px;">
    Al regresar a Kairos, la tripulación se encuentra con un asteroide saturado de tensiones políticas y militares: delegaciones de los Protectores, Caballeros de Golarion, corsarios del Espacio Libre y emisarios corporativos drow abarrotan las esclusas. Entre las sombras del casino y el bar pirata <em>El Cuerno Oscuro</em>, secretos enterrados durante siglos salen a la luz cuando la implacable matriarca <strong>Alistrav Istrav</strong> revela el fraude genealógico que dio origen a su casa noble y las maquinaciones que unieron a la madre de Triel con Keiden Ashton. Al mismo tiempo, en el planeta oceánico <strong>Daline 3</strong>, A.Xel descubre el santuario oculto de su linaje y el colosal legado de las cuarenta y dos encarnaciones de su chasis, antes de que Benrey Galway deba liderar a sus camaradas en una encarnizada batalla naval y cuerpo a cuerpo contra la <strong>Legión del Fuego en el Cielo</strong> para salvaguardar la autonomía de la inteligencia artificial Shirka. Finalmente, entre la emoción comunitaria del festejo por el futuro hijo de Marloc Boosmar y Ángela y la dolorosa decisión de Triel al sincronizar el núcleo del asteroide Kairos, una brecha hiperespacial abre el camino hacia lo desconocido.
  </p>

  <p style="font-size: 8.8pt; line-height: 1.40; text-align: justify; margin-bottom: 8px;">
    La historia traslada a la prosa literaria la espontaneidad, la comedia, el dramatismo y los vínculos forjados en la mesa de juego bajo la dirección del Game Master <strong>Roberto</strong>, rindiendo tributo al talento y la complicidad de su elenco de jugadores:
  </p>
  
  <!-- MESA DE JUEGO ORIGINAL -->
  <div style="margin: 6px auto; max-width: 500px;">
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 5px auto;">
    <p style="font-family: 'Liberation Sans', sans-serif; font-size: 8.2pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 5px 0; text-indent: 0; text-align: center;">
      ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 8.5pt; color: #2d3748;">
      <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (y la voz del meca <strong>Gerty</strong>) &nbsp;|&nbsp; <strong style="color: #1a365d;">Miguel:</strong> Benrey Galway <em>(Emisario Ysoki)</em>
    </p>
    <p style="margin: 2px 0; text-indent: 0; text-align: center; font-size: 8.5pt; color: #2d3748;">
      <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Juan Pablo:</strong> Zivok Jard / Marloc Boosmar &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa Androide)</em>
    </p>
    <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 5px auto;">
  </div>

  <!-- AVISO DE PAIZO Y ATRIBUCIÓN -->
  <table style="width: 100%; margin: 8px 0 0 0; border: 1px solid #cbd5e0; background-color: #f8fafc; border-collapse: collapse; page-break-inside: avoid; break-inside: avoid;">
    <tr>
      <td style="padding: 6px 10px; font-size: 7.2pt; color: #4a5568; line-height: 1.30; text-align: justify; border: none;">
        <p style="margin: 0 0 3px 0; text-indent: 0; font-weight: bold; color: #1a365d; font-size: 7.8pt; text-transform: uppercase; letter-spacing: 1px; text-align: center;">
          Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución
        </p>
        <p style="margin: 0 0 3px 0; text-indent: 0;">
          Esta obra literaria y sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de <strong>Paizo Inc.</strong>, utilizados bajo la <em>Política de Uso Comunitario de Paizo</em> (<a href="https://paizo.com/communityuse" style="color: #2b6cb0; text-decoration: none;">paizo.com/communityuse</a>). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de <em>Starfinder</em> y <em>Pathfinder</em>, visite <a href="https://paizo.com" style="color: #2b6cb0; text-decoration: none;">paizo.com</a>.
        </p>
        <p style="margin: 0; text-indent: 0;">
          Asimismo, esta novelización constituye un tributo no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense <strong>Lasers y Dragones</strong>. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: <strong>Roberto</strong> (Game Master y Gerty), <strong>Miguel</strong> (Benrey Galway), <strong>Irene</strong> (Triel Istrav), <strong>Juan Pablo</strong> (Zivok Jard) y <strong>Sofía</strong> (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
        </p>
      </td>
    </tr>
  </table>
</div>

<!-- SALTO DE PÁGINA OBLIGATORIO A PÁGINA 3 -->
<div style="page-break-before: always; break-before: page;"></div>

<!-- PÁGINA 3: ÍNDICE DE CONTENIDOS -->
<div style="padding: 8px 0;">
  <h2 class="section-heading-main" style="page-break-before: avoid; break-before: avoid; margin-bottom: 4px; padding-bottom: 2px; font-size: 14pt;">
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
    print("=== Compilación de Volumen 16: El Secreto de la Deriva ===")
    
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
        central_pdf_path = os.path.join(central_pdf_dir, "16_Lasers_y_Dragones_Volumen_16_El_Secreto_de_la_Deriva.pdf")
        shutil.copy2(final_pdf, central_pdf_path)
        print(f"Biblioteca centralizada sincronizada: {central_pdf_path}")

    # Validación final de tamaño
    size_mb = os.path.getsize(final_pdf) / (1024 * 1024)
    print(f"\n¡Libro Volumen 16 generado con éxito!")
    print(f"Ruta: {final_pdf}")
    print(f"Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    build_book()
