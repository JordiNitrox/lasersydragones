# Estándar Editorial y Maquetación PDF
## Reglas Técnicas para Compilar Libros Idénticos en la Saga

Para garantizar que todos los volúmenes futuros (*Volumen 2, Volumen 3...*) tengan exactamente el mismo aspecto editorial, maquetación tipográfica y un árbol de marcadores PDF perfecto en visores como Okular, Evince, Adobe Acrobat y navegadores, deben seguirse estrictamente estas pautas técnicas.

---

### 1. La Jerarquía Semántica para Marcadores PDF (*Bookmarks*)

En LibreOffice Writer (filtro HTML a PDF), la asignación de niveles en el panel lateral de navegación depende de las etiquetas HTML utilizadas:

| Nivel en Navegación PDF | Etiqueta HTML | Elemento del Libro | Ejemplo en Código |
|---|---|---|---|
| **Excluido del Esquema** | `<div class="...">` | Título y Subtítulo de Portada | `<div style="font-size: 30pt; font-weight: bold; ...">LASERS Y DRAGONES</div>` |
| **Nivel 1 (Capítulo Principal)** | `<h2 class="chapter-name">` | Capítulos y Secciones Mayores | `<h2 class="chapter-name">Capítulo 1: <br><span class="chap-sub">Senderos hacia la Chatarra</span></h2>` |
| **Nivel 2 (Subsección/Escena)** | `<h3 class="subsection-title">` | Escenas dentro de capítulos | `<h3 class="subsection-title">I. El enjambre de la Armada</h3>` |
| **Nivel 2 (Categoría de Anexo)** | `<h3 class="section-title">` | Secciones del Dossier | `<h3 class="section-title">1. El Escenario</h3>` |
| **Nivel 3 (Ficha individual)** | `<h4 class="subsection-title">` | Personajes y Facciones en Dossier | `<h4 class="subsection-title">Triel Istrav</h4>` |

> ⚠️ **CRÍTICO:** Nunca usar etiquetas `<h1>` en el HTML. LibreOffice Writer/Web las importa sin nivel de esquema (*Outline Level*), lo que hace que los capítulos desaparezcan del índice de marcadores. Tampoco usar `<h2>` en la portada, ya que se convertiría en una falsa raíz.

---

### 2. Estructura Tipográfica y CSS Estándar

El compilador de cada volumen debe emplear esta hoja de estilos en la cabecera `<style>`:

```css
@page {
  size: A4;
  margin: 25mm 22mm 25mm 22mm;
}

body {
  font-family: 'Liberation Serif', 'Georgia', 'Palatino Linotype', serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #1a1a1a;
  background: #ffffff;
  margin: 0;
  padding: 0;
}

/* Encabezados de secciones preliminares (Introducción, Índice) */
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

/* Encabezados de capítulo con salto de página infalible */
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

/* Subsecciones y divisiones de escenas */
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

/* Párrafos con sangría editorial */
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

.quote {
  border-left: 3px solid #cbd5e0;
  margin: 15px 25px;
  padding: 6px 12px;
  font-style: italic;
  color: #4a5568;
}

.toc-table {
  width: 100%;
  border-collapse: collapse;
  margin: 25px 0;
}

.toc-table td {
  padding: 8px 4px;
  border-bottom: 1px dotted #cbd5e0;
  font-size: 10.5pt;
}
```

---

### 3. Plantilla Estándar y Estricta de Portada Editorial

Todas las portadas deben mantener la misma geometría, jerarquía visual y paleta de colores cromática:

```html
<!-- PORTADA EDITORIAL HOMOGÉNEA -->
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

> **Regla de oro:** El pie de portada debe ser siempre un subtítulo narrativo de la novela (e.g. `VOLUMEN I · CONSPIRACIÓN EN LA ESPIGA`, `VOLUMEN II · LOS SECRETOS DEL VACÍO`), jamás una mención técnica a recuentos de episodios del podcast.

---

### 4. Compilación Headless con LibreOffice

Para compilar de manera no interactiva y segura:

```bash
user_prof="file://$(pwd)/.libreoffice_profile"
libreoffice -env:UserInstallation=$user_prof --headless --convert-to pdf libro_maquetado.html
```

#### Protocolo de validación posterior:
1. Extraer los marcadores generados con un script de inspección en Python para confirmar que los capítulos figuran en el Nivel 1.
2. Comprobar que los números de página calculados en la tabla del **Índice de Contenidos** coinciden con la página física donde arranca cada capítulo en el PDF final.
