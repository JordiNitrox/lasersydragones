---
name: lasers-maquetacion-pdf
description: >-
  Guía técnica y de maquetación editorial para compilar novelas de 'Lasers y Dragones'
  en documentos HTML y PDF homogéneos con LibreOffice. Úsalo cuando necesites formatear,
  maquetar, ajustar estilos CSS, corregir portadas A4, Nota Editorial, Índice de Contenidos
  o compilar/validar PDFs de la saga.
---

# Skill: Maquetación Editorial y Compilación PDF (*Lasers y Dragones*)

Este skill define las especificaciones técnicas obligatorias para compilar cualquier volumen de la saga en un PDF editorial homogéneo, elegante y profesional utilizando HTML/CSS y LibreOffice Writer en modo headless.

---

## 1. Geometría de Página y Jerarquía Semántica

### A. Formato de Página Estricto
Todos los volúmenes de la saga se maquetan en **formato A4 estándar**:
```css
@page {
  size: A4;
  margin: 25mm 22mm 25mm 22mm;
}
```
*(⚠️ Queda terminantemente prohibido utilizar formatos alternativos como 6x9 pulgadas o Letter).*

### B. Mapeo de Niveles de Esquema para Marcadores PDF (*Bookmarks*)
LibreOffice Writer/Web genera el árbol lateral de navegación a partir de las siguientes etiquetas:

| Elemento del Libro | Etiqueta HTML Requerida | Nivel en Marcadores PDF |
|---|---|---|
| **Portada (Títulos/Textos)** | `<div>` y `<p>` con estilos en línea | *Excluido del árbol* (nunca usar `<h1>` ni `<h2>`) |
| **Secciones Principales / Capítulos** | `<h2 class="chapter-name">` o `.section-heading-main` | **Nivel 1** (Salto de página obligatorio) |
| **Escenas dentro de capítulo** | `<h3 class="subsection-title">` | **Nivel 2** |
| **Categorías del Glosario** | `<h3 class="section-title">` | **Nivel 2** |
| **Fichas individuales en Glosario** | `<h4 class="subsection-title">` | **Nivel 3** |

> 🚨 **REGLA CRÍTICA:**  
> **NUNCA usar `<h1>` en el HTML.** LibreOffice Writer/Web importa las etiquetas `<h1>` sin nivel de esquema (*Outline Level*), lo que hace que los capítulos desaparezcan del panel de marcadores.  
> **NUNCA usar `<h1>` ni `<h2>` en la portada**, para evitar falsas raíces en el índice.

---

## 2. Estructura Estricta de Primeras Páginas (Front Matter)

Cada volumen debe estructurar sus primeras tres páginas de forma idéntica:

### Página 1: Portada Editorial Homogénea
```html
<div style="text-align: center; padding: 40px 10px; margin: 0 auto; max-width: 500px;">
  <p style="font-family: 'Liberation Sans', sans-serif; font-size: 11pt; letter-spacing: 5px; text-transform: uppercase; color: #2b6cb0; margin: 40px 0 20px 0; text-indent: 0;">
    Ópera Espacial · Universo Starfinder
  </p>
  
  <hr style="border: none; border-top: 2px solid #1a365d; width: 60%; margin: 25px auto;">
  
  <div style="font-size: 30pt; font-weight: bold; color: #0b1a30; margin: 20px 0 10px 0; letter-spacing: 2px; text-align: center;">
    LASERS Y DRAGONES
  </div>
  
  <div style="font-size: 20pt; font-style: italic; color: #b8860b; margin: 10px 0 20px 0; text-align: center;">
    {TITULO_DEL_VOLUMEN}
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
    VOLUMEN {ROMANO} · {SUBTITULO_INDICATIVO_NOVELA}
  </p>
</div>
```

### Página 2: Nota Editorial e Introducción
Debe contener:
1. Párrafo introductorio contextualizando el volumen y los episodios adaptados.
2. Caja de la **✦ Mesa de Juego Original ✦**:
```html
<div style="margin: 8px auto; max-width: 500px;">
  <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 6px auto;">
  <p style="font-family: 'Liberation Sans', sans-serif; font-size: 8.5pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; color: #1a365d; margin: 0 0 6px 0; text-indent: 0; text-align: center;">
    ✦ &nbsp; Mesa de Juego Original &nbsp; ✦
  </p>
  <p style="margin: 3px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
    <strong style="color: #1a365d;">Roberto:</strong> Game Master / Narrador (y la voz del meca <strong>Gerty</strong>) &nbsp;|&nbsp; <strong style="color: #1a365d;">Miguel:</strong> Benray Galway <em>(Emisario Ysoki)</em>
  </p>
  <p style="margin: 3px 0; text-indent: 0; text-align: center; font-size: 9pt; color: #2d3748;">
    <strong style="color: #1a365d;">Irene:</strong> Triel Istrav <em>(Mecánica Semi-drow)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Juan Pablo:</strong> Marloc Boosmar <em>(Tecnomante Humano)</em> &nbsp;|&nbsp; <strong style="color: #1a365d;">Sofía:</strong> A.Xel 42 <em>(Operativa Androide)</em>
  </p>
  <hr style="border: none; border-top: 1px solid #b8860b; width: 40%; margin: 6px auto;">
</div>
```
3. Recuadro formal obligatorio de **Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución**:
```html
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
        Asimismo, esta novelización constituye un tributo no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense <strong>Lasers y Dragones</strong>. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: <strong>Roberto</strong> (Game Master y Gerty), <strong>Miguel</strong> (Benray Galway), <strong>Irene</strong> (Triel Istrav), <strong>Juan Pablo</strong> (Marloc Boosmar) y <strong>Sofía</strong> (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
      </p>
    </td>
  </tr>
</table>
```

### Página 3: Índice de Contenidos (Compacto en 1 sola página)
Para evitar que la última fila del índice desborde a la página 4, se deben usar exactamente estos estilos CSS compactos:
```css
.toc-table {
  width: 100%;
  border-collapse: collapse;
  margin: 4px 0;
}
.toc-table td {
  padding: 2px 3px;
  border-bottom: 1px dotted #cbd5e0;
  font-size: 8.8pt;
  line-height: 1.15;
}
.toc-title {
  font-weight: bold;
  color: #0b1a30;
}
.toc-sub {
  font-size: 7.8pt;
  color: #718096;
  font-style: italic;
  line-height: 1.1;
}
```

---

## 3. Hoja de Estilos CSS Estándar

```css
body {
  font-family: 'Liberation Serif', 'Georgia', 'Palatino Linotype', serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #1a1a1a;
  background: #ffffff;
  margin: 0;
  padding: 0;
}

.section-heading-main {
  font-size: 22pt;
  text-align: center;
  color: #0b1a30;
  margin-top: 0;
  margin-bottom: 25px;
  border-bottom: 2px solid #b8860b;
  padding-bottom: 10px;
  page-break-before: always;
  break-before: page;
}

h2.chapter-name {
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
}

.chap-sub {
  font-size: 18pt;
  font-style: italic;
  color: #2b6cb0;
  font-weight: normal;
}

h3.section-title {
  font-size: 14pt;
  color: #2b6cb0;
  margin-top: 25px;
  margin-bottom: 12px;
  border-bottom: 1px dashed #e2e8f0;
  padding-bottom: 4px;
  font-family: 'Liberation Serif', serif;
}

h3.subsection-title {
  font-size: 12.5pt;
  color: #2d3748;
  margin-top: 20px;
  margin-bottom: 10px;
  font-family: 'Liberation Serif', serif;
}

h4.subsection-title {
  font-size: 11.5pt;
  color: #1a365d;
  margin-top: 16px;
  margin-bottom: 6px;
  font-weight: bold;
  font-family: 'Liberation Serif', serif;
}

p {
  text-align: justify;
  text-justify: inter-word;
  margin: 0 0 12px 0;
  text-indent: 1.5em;
}

p:first-of-type, .divider + p, .section-title + p, .subsection-title + p {
  text-indent: 0;
}

.divider {
  text-align: center;
  margin: 25px 0;
  color: #a0aec0;
  font-size: 10pt;
  letter-spacing: 6px;
}

.bullet-list {
  margin: 12px 0 15px 25px;
  padding: 0;
}

.bullet-list li {
  margin-bottom: 6px;
  text-align: justify;
}

.quote {
  margin: 18px 25px;
  padding: 10px 18px;
  border-left: 3px solid #b8860b;
  background: #f7fafc;
  font-style: italic;
  color: #4a5568;
}
```

---

## 4. Compilación en 2 Pases y Extracción de Paginación Real

Para garantizar que el número de página en el Índice de Contenidos refleje la página exacta donde comienza cada capítulo, el script `generar_libro_pdf.py` ejecuta dos pases:

1. **Pase 1 (Preliminar):** Genera el HTML y compila un PDF provisional con LibreOffice.
2. **Extracción:** Ejecuta `pdftotext` para detectar la página física de cada encabezado `h2.chapter-name`:
```python
def extract_page_numbers_from_pdf(pdf_path):
    res = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
    pages = res.stdout.split("\x0c") # Form feed separa páginas
    found_pages = {}
    
    # Nota Editorial en pág. 2
    for idx, page_text in enumerate(pages[:3]):
        if "nota editorial e introducción" in page_text.lower():
            found_pages["nota_editorial"] = idx + 1
            break
            
    for item in TOC_ITEMS:
        if item["id"] == "nota_editorial":
            continue
        key = item["search_key"].lower()
        for idx in range(3, len(pages)):
            lines = [l.strip() for l in pages[idx].split("\n") if l.strip()][:6]
            header_text = " ".join(lines).lower()
            if key in header_text:
                found_pages[item["id"]] = idx + 1
                break
    return found_pages
```
3. **Pase 2 (Definitivo):** Regenera el HTML inyectando los números de página extraídos en la tabla `.toc-table` y compila el PDF final.

---

## 5. Compilación Headless con LibreOffice

```bash
user_prof="file://$(pwd)/.libreoffice_profile"
libreoffice -env:UserInstallation=$user_prof --headless --convert-to pdf libro_maquetado.html
```

### Verificación Visual Obligatoria con `pdftoppm`:
```bash
pdftoppm -png -r 150 -f 1 -l 4 Lasers_y_Dragones_Volumen_X.pdf scratch/preview_page
```
Verificar con `view_file` que la Portada (pág. 1), Nota Editorial (pág. 2), Índice (pág. 3) y Prólogo (pág. 4) no tienen desbordamientos ni saltos no deseados.
