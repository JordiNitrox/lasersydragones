---
name: lasers-ingesta-transcripciones
description: >-
  Guía para descargar episodios, extraer y limpiar transcripciones automáticas
  y realizar minería de canon, secretos y relaciones del podcast 'Lasers y Dragones'.
  Úsalo cuando necesites procesar nuevos episodios, limpiar subtítulos VTT con
  diccionarios fonéticos o analizar el audio previo a la redacción.
---

# Skill: Ingesta, Limpieza y Minería de Transcripciones (*Lasers y Dragones*)

Este skill define el procedimiento técnico para descargar los episodios del podcast, sanear las transcripciones automáticas mediante filtros fonéticos y realizar la minería obligatoria de secretos, familias y giros argumentales antes de iniciar la redacción de cualquier volumen.

---

## 1. Descarga y Extracción de Subtítulos

Para procesar un nuevo lote de episodios desde el canal oficial de YouTube de *Lasers y Dragones*:

```bash
# Descarga de subtítulos automáticos en español (.vtt) sin descargar el archivo de vídeo:
yt-dlp --write-auto-sub --sub-lang es --skip-download \
  -o "transcripciones/raw/episodio_XX.%(ext)s" \
  "<URL_DEL_EPISODIO_EN_YOUTUBE>"
```

*(Si se dispone del archivo MP3 directo de Libsyn, pueden transcribirse localmente con Whisper en modo español).*

---

## 2. Limpieza Automatizada y Filtro Fonético (STT)

Las herramientas de reconocimiento de voz automático (YouTube / Whisper) sufren alucinaciones acústicas recurrentes al enfrentarse a términos de ciencia ficción en inglés o nombres propios de *Starfinder*.

Para sanear las transcripciones, ejecutar el script provisto en este skill:
```bash
python3 .agents/skills/lasers-ingesta-transcripciones/scripts/limpiar_transcripcion.py \
  transcripciones/raw/episodio_XX.es.vtt \
  transcripciones/limpias/episodio_XX.txt
```

### Tabla Maestra de Corrupciones Fonéticas Habituales:
| Error Típico del STT | Término Canónico Real | Contexto en la Campaña |
|---|---|---|
| *piedra del triunfo* / *del triunfo* | **Roca del Drift** / **del Drift** | Asteroide y plano hiperespacial |
| *Ring Rey* | **Rim Rey** | Primo ysoki de Benrey |
| *octurno* / *autor* | **Aucturn** | El planeta viviente del Pacto |
| *Sociedad Starfinder* / *Lorexpe* | **Inversiones Estelares S.C.** | Corporación patrona de Chiskisk |
| *durabor kril* / *kreel* | **Marlene Boosmar** | Investigadora asesinada (PNJ de Roberto) |
| *ferani krane* | **Ferani Nadaz** | Líder de los Reyes de Abajo |
| *jabaxa* | **Brock Hilario** | Lugarteniente vesk «el Rompeportones» |
| *sunrise maiden* | **Estrella Errante** | Nave principal de la tripulación |

---

## 3. Protocolo Obligatorio de Minería Previa (Los Cuatro Ejes)

> 🚨 **REGLA DE ORO DE INVESTIGACIÓN:**  
> **Queda terminantemente prohibido comenzar a redactar un volumen basándose solo en sinopsis superficiales o módulos de Paizo.**  
> El corazón que da vida a la saga son las vidas personales, revelaciones y traumas que los jugadores introducen en sus improvisaciones de mesa.

Antes de escribir el primer capítulo de un volumen, es obligatorio ejecutar barridos de búsqueda en `transcripciones/limpias/`:

### Eje 1: Giros Argumentales y Revelaciones Mayores
* Buscar términos: `secreto`, `verdad`, `plan`, `futuro`, `dimensión`, `consola`, `esfera`.
* *Ejemplos clave:* Anagramas de empresas (Sambert Klamburg / Marloc), identidades de chasis (Axel / Ashera), secretos de naves o reliquias pre-Brecha.

### Eje 2: Familias, Linajes y Vínculos Biológicos/Sintéticos
* Buscar términos: `padre`, `madre`, `hijo`, `hija`, `esposa`, `familia`, `clan`, `hermano`, `hermana`.
* *Identificar:* El padre de Triel (**Keiden Ashton**) y su madre drow; el linaje de Benrey y los parientes Galway; el enigma del padre de Marloc (**Ambrose Boosmar**) y su esposa Ángela; los vínculos androides de Axel (**Null-9**, Éclair, la nueva conciencia).

### Eje 3: Relaciones Interpersonales y Dinámicas de la Tripulación
* Buscar términos: `León`, `oficial`, `comunicador`, `cita`, `despedida`, `promesa`, `confianza`.
* *Registrar:* El desarrollo del romance canónico entre **Triel y el Oficial León**; las charlas íntimas de cabina; los pactos de lealtad entre Benrey y Gerty.

### Eje 4: Traumas, Fobias y Cicatrices Psicológicas
* Buscar términos: `miedo`, `terror`, `pesadilla`, `recuerdo`, `dolor`, `esclavitud`.
* *Capturar:* La fobia de Benrey a Eox y los no-muertos; el pánico de Axel a perder la libertad y volver a ser esclavizada; el duelo autodestructivo de Marloc; los traumas de Triel en Apostae.

---

## 4. Registro y Entrega de la Minería

Todos los hallazgos deben volcarse de inmediato en dos destinos:
1. **Dossier del Volumen:** Actualizar [GLOSARIO_Y_PERSONAJES.md](../../../volumen_X/novela/GLOSARIO_Y_PERSONAJES.md) con las nuevas biografías y evoluciones.
2. **Plantillas de Capítulo:** Si en un episodio ocurre una confesión o giro crucial, insertar una cabecera de hito obligatorio en el borrador de markdown antes de la redacción definitiva.
