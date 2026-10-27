---
name: novelizacion-lasers-y-dragones
description: >-
  Guía metodológica maestra y orquestadora del proyecto de novelización de 'Lasers y Dragones'.
  Úsalo para planificar nuevos volúmenes, coordinar el flujo completo de producción
  (ingesta, redacción, maquetación y control de calidad) y gestionar la continuidad global de la saga.
---

# Skill Maestro: Flujo Global de Novelización de *Lasers y Dragones*

Este skill constituye la **guía orquestadora de alto nivel** para coordinar la producción de cada volumen de la saga de novelizaciones del podcast de rol en vivo **Lasers y Dragones** (campaña *Starfinder: Dead Suns*), articulando el trabajo entre los skills especializados del proyecto.

---

## 1. Criterios de Delimitación de un Volumen

Cada volumen debe concebirse como una **novela autoconclusiva en su arco inmediato**, respetando los siguientes parámetros:

1. **Unidad Temática y Espacial:**
   * Cada libro debe corresponder a un hito geográfico o dramático claro (ej. la conspiración de Absalón, el abordaje del *Acreon*, la exploración de la *Roca del Drift*, la travesía selvática en Castrovel, o las intrigas mineras en La Diáspora).
2. **Extensión Óptima:**
   * Entre **8 y 12 episodios de podcast** por volumen.
   * Rendimiento literario: **10 a 14 capítulos** de entre 1.500 y 3.000 palabras cada uno (más prólogo, nota editorial y glosario), totalizando entre **60 y 100 páginas** maquetadas en A4.
3. **Estructura en Cuatro Actos:**
   * **Acto I (Disparador):** Entrada al nuevo escenario o planteamiento del conflicto.
   * **Acto II (Investigación / Tensión):** Exploración, pistas y confrontaciones tácticas menores.
   * **Acto III (Punto de inflexión y Clímax):** Revelación de la verdad o batalla crucial.
   * **Acto IV (Desenlace y Puente):** Consecuencias inmediatas y gancho hacia el siguiente volumen.

---

## 2. Estructura Canónica de Carpetas de cada Volumen

```text
volumen_X/
├── README.md                      # Ficha técnica, episodios asignados y estado
├── metadatos/
│   └── episodios_volumen_X.json  # URLs de Libsyn/YouTube, títulos y sinopsis
├── transcripciones/
│   ├── raw/                       # Subtítulos .es.vtt originales de YouTube
│   └── limpias/                   # Transcripciones depuradas en texto continuo
└── novela/
    ├── capitulos/                 # Borradores en Markdown (00_prologo.md, 01_capitulo...md)
    ├── GLOSARIO_Y_PERSONAJES.md   # Dossier del volumen con secundarios y facciones
    ├── generar_libro_pdf.py       # Script compilador HTML/CSS a PDF en 2 pases
    └── Lasers_y_Dragones_Volumen_X_Titulo.pdf
```

---

## 3. Las Cuatro Fases de Producción y Skills Especializados

El ciclo de vida de un volumen se divide en cuatro fases modulares, cada una respaldada por su skill específico:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INGESTA Y MINERÍA   ──► Skill: lasers-ingesta-transcripciones
├─────────────────────────────────────────────────────────────┤
│ 2. REDACCIÓN Y CANON   ──► Skill: lasers-narrativa-y-canon
├─────────────────────────────────────────────────────────────┤
│ 3. MAQUETACIÓN Y PDF   ──► Skill: lasers-maquetacion-pdf
├─────────────────────────────────────────────────────────────┤
│ 4. AUDITORÍA Y CIERRE  ──► Checklist Maestro de 10 Puntos
└─────────────────────────────────────────────────────────────┘
```

### Fase 1: Ingesta, Saneamiento y Minería Temática
* **Skill activo:** `lasers-ingesta-transcripciones`
* **Acciones:**
  1. Descarga de subtítulos con `yt-dlp` en `transcripciones/raw/`.
  2. Limpieza fonética y de repeticiones con `limpiar_transcripcion.py`.
  3. **Minería obligatoria de los 4 ejes:** Extraer secretos familiares, parentescos reales, dinámicas de la tripulación y traumas antes de escribir.

### Fase 2: Redacción Literaria y Continuidad
* **Skill activo:** `lasers-narrativa-y-canon`
* **Acciones:**
  1. Transformar las tiradas y combates en prosa fluida de ópera espacial (cero jerga de mesa).
  2. Aplicar la **inmersión diegética absoluta**: PROHIBIDO usar nombres de jugadores en el texto narrativo; Gerty habla mediante su sintetizador vocal.
  3. Preservar las personalidades de Benrey, Triel, Marloc y Axel, así como la primacía de la partida real sobre Paizo.
  4. Actualizar el `GLOSARIO_Y_PERSONAJES.md` del volumen.

### Fase 3: Maquetación Editorial y Compilación del PDF
* **Skill activo:** `lasers-maquetacion-pdf`
* **Acciones:**
  1. Aplicar la geometría A4 estricta (`size: A4; margin: 25mm 22mm 25mm 22mm;`).
  2. Configurar la Portada estándar, la Página 2 (Nota Editorial con créditos de mesa y aviso de Paizo) y la Página 3 (Índice de 1 sola página).
  3. Ejecutar el script `generar_libro_pdf.py` con el algoritmo de doble pase (`pdftotext`) para calcular la paginación real.
  4. Compilar con LibreOffice en modo headless y verificar visualmente las páginas 1 a 4 con `pdftoppm`.

---

## 4. Fase 4: Checklist Maestro de Calidad y Cierre (10 Puntos)

Antes de dar por cerrado cualquier volumen, es preceptivo verificar los 10 puntos de control:

1. **Marcadores PDF:** Todos los capítulos y preliminares deben figurar en el Nivel 1 en el panel de marcadores de LibreOffice (usar `<h2 class="chapter-name">`, nunca `<h1>`).
2. **Concordancia de Páginas:** La página física del PDF donde empieza cada capítulo debe coincidir con el número impreso en el Índice de Contenidos.
3. **Índice en 1 sola página:** La tabla del índice no debe desbordarse hacia la página 4.
4. **Inmersión Diegética (Barrido Anti-Fugas de Nombres de Jugadores):**
   ```bash
   grep -rnEi "\b(Roberto|Juan Pablo|Juanpa|Sofía|Sofia|Irene|Miguel)\b" novela/capitulos/*.md --exclude="00_nota_editorial.md"
   ```
   *(Cero coincidencias en la narrativa de los capítulos).*
5. **Barrido Anti-Alucinaciones Fonéticas del STT:**
   ```bash
   grep -rnEi "\b(piedra del triunfo|deriva|Ring Rey|Kreel|Ferani Krane|Sociedad Starfinder)\b" novela/capitulos/*.md
   ```
   *(Cero coincidencias).*
6. **Fidelidad Canónica a la Mesa:** Cero extrapolaciones no confirmadas (ej. no llamar a Marlene «hermana de Marloc», no llamar a Triel «corsaria»).
7. **Integración de Giros y Vidas Personales:** Todos los datos familiares y emocionales descubiertos en la minería deben estar reflejados en los capítulos y en el glosario.
8. **Inclusión de Descargos Legales:** Presencia obligatoria del Aviso de Política de Uso Comunitario de Paizo Inc. y Atribución en la Nota Editorial.
9. **Sincronización del Compendio Maestro:** Resumir el volumen en `Contexto completo/CONTEXTO_COMPLETO_SAGA.md` y actualizar las etiquetas de aparición de personajes y facciones.
10. **Recompilación de Contexto Completo:** Ejecutar `python3 "Contexto completo/generar_contexto_pdf.py"` para mantener al día el libro maestro de la saga.

---

## 5. Política Estricta de Control de Versiones (Git)

> 🚨 **REGLA MANDATORIA DE CONTROL DE VERSIONES:**  
> **NUNCA realizar `git commit` ni `git push` de forma autónoma o automática.**  
> * Toda operación de `git commit` o `git push` hacia el repositorio debe ser solicitada **de manera explícita y directa por el usuario** (por ejemplo: *«haz commit de esto»* o *«haz push de los cambios»*).  
> * Durante las tareas ordinarias de redacción de capítulos, revisión de erratas, maquetación editorial, compilación de PDFs o actualización de glosarios y compendios, los cambios deben permanecer en el árbol de trabajo local (*working directory*) sin comitear ni subir al remoto hasta recibir la orden expresa.

---

## 6. Higiene del Entorno y Limpieza de Scripts Temporales (`scratch/`)

> 🧹 **REGLA DE LIMPIEZA DE SCRIPTS TEMPORALES (ver `.agents/rules/limpieza_scripts_temporales.md`):**  
> * Los scripts de un solo uso para análisis de transcripciones, búsquedas de texto o pruebas ad-hoc en la carpeta `scratch/` deben ser eliminados inmediatamente tras finalizar la tarea (`rm -rf scratch/*`).
> * La carpeta `scratch/` debe permanecer limpia y nunca incluirse en el control de versiones.
