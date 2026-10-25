---
name: novelizacion-lasers-y-dragones
description: >-
  Guía metodológica, literaria y técnica integral para descargar, transcribir,
  estructurar y novelizar lotes de episodios del podcast de rol 'Lasers y Dragones'
  (campaña Starfinder: Dead Suns) en volúmenes literarios homogéneos con maquetación
  editorial profesional en PDF.
---

# Skill: Novelización de Episodios de *Lasers y Dragones*

Este skill contiene el procedimiento paso a paso para continuar con la saga de novelizaciones del podcast **Lasers y Dragones**, transformando las partidas de rol de mesa en vivo en novelas literarias de ópera espacial y ciencia ficción, garantizando coherencia argumental, fidelidad a la mesa de juego y uniformidad en el diseño editorial en PDF.

---

## 1. Criterios de Delimitación de un Volumen (Arco Narrativo Coherente)

No se debe realizar un corte arbitrario por número de episodios. Cada volumen debe concebirse como una **novela autoconclusiva en su arco inmediato**, aunque forme parte de la campaña mayor (*Dead Suns*):

1. **Unidad Temática y Espacial:**
   - **Volumen 1 (*Sombras sobre Absalón* - Episodios 1 al 10):** Abarca la llegada a la Estación Absalón, la reunión en el Club 13, el asesinato en el Muelle 94, la conspiración de Extracciones Estelares contra Hardscrabble y la huida de la estación.
   - **Volumen 2 (Planificado - Próximo bloque de episodios):** Debe centrarse en la travesía hacia el Vasto, el abordaje e investigación de la nave fantasma *Acreon*, y la exploración de la *Roca del Drift* (*The Drift Rock*).
   - **Volúmenes futuros:** Identificar el clímax dramático de la aventura (cambio de planeta, derrota de un antagonista principal, resolución de un enigma alienígena).
2. **Extensión Óptima:**
   - Entre **8 y 12 episodios de podcast** por volumen.
   - Rendimiento literario: **10 a 12 capítulos** de entre 1.500 y 3.000 palabras cada uno (más prólogo, introducción y glosario), totalizando entre **50 y 75 páginas** maquetadas en A4.
3. **Estructura en Cuatro Actos:**
   - **Acto I (Disparador):** Entrada al nuevo escenario o planteamiento del conflicto.
   - **Acto II (Investigación / Tensión):** Exploración, recolección de pistas, confrontaciones tácticas menores.
   - **Acto III (Punto de inflexión y Clímax):** Revelación de la verdad o batalla crucial.
   - **Acto IV (Desenlace y Puente):** Consecuencias inmediatas y gancho (*cliffhanger*) hacia el siguiente volumen.

---

## 2. Ingesta y Transcripción de Episodios

### A. Descarga de Metadatos y Audio
1. Localizar los episodios en el archivo mensual de Libsyn (`https://lasersydragones.libsyn.com/YYYY/MM`) o mediante el canal oficial de YouTube de *Lasers y Dragones*.
2. Obtener el enlace directo del audio MP3 en `traffic.libsyn.com` o descargarlo mediante script.

### B. Extracción de Subtítulos y Transcripción
Para obtener la transcripción original en español con marcas de diálogo:
```bash
# Descarga de subtítulos automáticos en español desde YouTube sin descargar el vídeo:
yt-dlp --write-auto-sub --sub-lang es --skip-download -o "transcripciones/raw/episodio_XX.%(ext)s" "<URL_YOUTUBE_DEL_EPISODIO>"
```

### C. Limpieza Automatizada y Filtro Fonético
Ejecutar el script de limpieza provisto en el skill para eliminar marcas temporales, etiquetas VTT, duplicaciones acumulativas y **corregir automáticamente alucinaciones acústicas típicas de los subtítulos automáticos (STT)**:
```bash
python3 .agents/skills/novelizacion-lasers-y-dragones/scripts/limpiar_transcripcion.py \
  transcripciones/raw/episodio_XX.es.vtt \
  transcripciones/limpias/episodio_XX.txt
```
El script incorpora un diccionario fonético (`CORRECCIONES_FONETICAS`) que sustituye errores habituales de YouTube (como «del triunfo» por «del Drift», o «Ring Rey» por «Rim Rey»). El resultado será un texto continuo y saneado, listo para el análisis narrativo.

---

## 3. Manual de Estilo Literario y Adaptación

### A. De Mesa de Rol a Narrativa Orgánica
- **Cero jerga de mesa:** Prohibido mencionar "puntos de golpe", "dados d20", "tirada de salvación", "iniciativa" o "clase de armadura".
- **Traducción física y sensorial:**
  - Un *20 natural* se describe como un golpe de genialidad improvisada o una falla estructural oportuna en el blanco.
  - Una *pifia (1 natural)* se narra como sobrecalentamiento de circuitos, un tropiezo por condensación de refrigerante o la distracción por un chiste inoportuno.
  - El daño se describe como abolladuras de blindaje, blindajes de plasma drenados al rojo vivo o heridas cauterizadas.

### B. Voces y Personalidades de los Personajes
Consultar siempre el dossier detallado en [canon_y_personajes.md](./references/canon_y_personajes.md):
- **Roberto (GM):** La voz omnisciente del narrador y creador de la atmósfera. En el diálogo encarna a **Gerty** con su sintetizador plano, quejándose con cinismo de los "bichos de carbono" y padeciendo actualizaciones de firmware lentas estilo *Windows 95*.
- **Benray Galway (Miguel):** Ysoki pícaro, verborrea acelerada, paranoico con la comida envenenada, motoneta abollada y lealtad incondicional a su primo **Rim Rey**.
- **Triel Istrav (Irene):** Mecánica semi-drow de 19 años, pelo níveo, piel cenicienta con matiz violáceo, chaqueta de segunda mano con emblema de los *Free Captains* (NUNCA fue corsaria ni perteneció a los piratas; es una mecánica civil independiente). Cariñosa, ingeniosa y protectora con Gerty.
- **Marloc Boosmar (Juan Pablo):** Tecnomante humano, mente académica desordenada, visiones cósmicas de la amnesia de la Brecha, fusiona nanitos y fórmulas matemáticas mágicas (*Null-Vector*). Despertó sin registro oficial en Absalón tras tocar una esfera rúnica; su relación con Marlene Boosmar es un enigma abierto (NUNCA se confirma que sean hermanos).
- **A.Xel 42 (Sofía):** Androide operativa, líneas bioluminiscentes rosadas, precisión quirúrgica, letal en sigilo, analítica y observadora de las rarezas humanas. Mantiene un vínculo fraternal profundo con su «unidad hermana» **Null-9** desde su rescate diez años atrás en el Vasto.

### C. Canon de Nombres y Terminología Oficial
- **Inversiones Estelares S.C.:** Compañía corporativa de mediación e inversiones con sede en el Ojo de la Estación Absalón, liderada por **Chiskisk** y para la que trabajaba **Marlene Boosmar**. Los protagonistas son contratados por ella como peritos/árbitros independientes (*freelancers*). *(⚠️ **Regla Crítica:** En el módulo de Paizo Chiskisk pertenecía a la «Sociedad Starfinder», pero en el podcast Roberto la sustituyó por completo por **Inversiones Estelares S.C.** La «Sociedad Starfinder» NUNCA existe como facción de los protagonistas en la historia).*
- **El Drift**: Plano hiperespacial. Nunca traducir como "la deriva" cuando se hable del hiperespacio.
- **La Roca del Drift (*The Drift Rock*):** Asteroide remolcado por el carguero *Acreon* que alberga el santuario pre-Brecha y la consola del Devastador Estelar. **NUNCA denominar como "Piedra del Triunfo"** ni "Piedra de la Deriva". *(⚠️ Los motores STT transcriben acústicamente "del Drift" como "del triunfo". Consultar siempre la Tabla Maestra de Corrupciones Fonéticas en [canon_y_personajes.md](./references/canon_y_personajes.md)).*
- **La Brecha** (*The Gap*) y **Los Protectores** (*The Stewards*).
- **Corporaciones:** *Extracciones Estelares* (*Astral Extractions* / *Extracciones Astrales*), *Colectivo Hardscrabble*, *Los Reyes del Nivel 21* (*21st Crew*).
- **Personajes secundarios:** **Rim Rey** (primo de Benray, NUNCA "Ring Rey"), **Chiskisk** (shirren no binario de Inversiones Estelares S.C.), **Chic**, **Ferani Nadaz** (líder de la Con-Fusión / Reyes de Abajo, NO "Ferani Krane"), **Brock Hilario «el Rompeportones»** (lugarteniente vesk), **Capitán Frederick**, **Null-9**, **Syd Velch**, **Willy**, **Naru**, **Oficial León**, **Carne Yac** (corresponsal vegetal de Noticias en Movimiento), **Embajador Gevalarsk Nor**, **Keltus**, **Ambrose Boosmar**.

### D. Primacía Absoluta del Podcast frente al Manual de Paizo (Partida Real vs. Aventura Escrita)

Este proyecto adapta una **partida real de rol en vivo** (*actual play*), NO el módulo impreso de *Dead Suns* (*Soles Muertos*) de Paizo Publishing. El manual de rol solo proporciona un armazón geográfico e institucional muy esquemático. Por tanto, rigen los siguientes principios inquebrantables:

1. **Los Jugadores Crean sus Propios Pasados y Relaciones:**
   - Benray, Triel, Marloc, Axel 42 y Gerty no son personajes pregenerados de Paizo ni siguen sus esquemas. Sus biografías, traumas, familias biológicas, clanes y motivos personales proceden exclusivamente de lo que los jugadores (**Miguel, Irene, Juan Pablo, Sofía**) y **Roberto** expresan en las sesiones de juego.
2. **Roberto (el GM) Introduce Tramas Adicionales y Sustituye Facciones:**
   - El director de juego ha enriquecido profundamente la campaña introduciendo arcos originales que no existen en la aventura de Paizo: la sustitución de la Sociedad Starfinder y su líder por **Inversiones Estelares S.C.** y **Chiskisk**; la sustitución del PNJ del manual por **Marlene Boosmar** (investigadora del Arcanamirium asociada a Inversiones Estelares y casada con Ángela); el enigma multiversal de **Ambrose Boosmar** y la esfera rúnica dorada; la «unidad hermana» de Axel **Null-9** y la resistencia sintética; la estrella del rock espacial **Syd Velch** y sus mensajes proféticos; los goblins espaciales **Willy y Naru** obteniendo visados diplomáticos de Eox; la dinámica de fricción y humor entre la tripulación (especialmente Benray) y el **Oficial León** de los Protectores; o la búsqueda del padre biológico de Triel (**Keiden Ashton**). Estas subtramas y cambios de facción son **canon primordial absoluto**.
3. **Prohibición Terminante de Suposiciones No Mencionadas en el Podcast:**
   - **Cero extrapolaciones no confirmadas:** Queda terminantemente prohibido inventar o dar por sentadas relaciones familiares, vínculos afectivos o románticos, filiaciones a facciones o hechos del pasado que no hayan sido verbalizados explícitamente en el audio del podcast o en sus transcripciones limpias.
   - **Suposiciones de PNJs en la mesa:** Si un personaje no jugador (o incluso un jugador) plantea una hipótesis o malentendido durante la partida (por ejemplo, cuando el intermediario Chic asume que Marloc es «el hermano de Marlene» debido a la coincidencia de apellido y físico), la novelización DEBE narrarlo estrictamente como lo que fue: una suposición no contrastada de un PNJ, y reflejar la respuesta real del protagonista (Marloc negando tajantemente tener hermanas). **Bajo ningún concepto el narrador omnisciente debe convertir en verdad fáctica lo que en la mesa fue una especulación o un error de un personaje.**
   - **Indumentaria y objetos vs. afiliación:** Llevar una prenda o símbolo (como la cazadora con el emblema de los Capitanes Libres que Triel compró de segunda mano en los mercadillos de la Diáspora) NUNCA debe interpretarse como que el personaje perteneció a esa facción o fue pirata, salvo que el jugador o el GM lo afirmen expresamente en el juego.
4. **Obligación de Registrar e Integrar Todo Detalle Personal Explicado en Mesa:**
   - Cada revelación sobre el pasado de un personaje (el despertar de Marloc en el aula 17 del Arcanamirium con Ritchie el barathu; la huida de Triel de la xenófoba familia drow de su madre en Apostae y su búsqueda de su padre humano Keiden Ashton; el pasado de esclavitud de Axel y su rescate por Null-9 hace diez años en el Vasto; los vídeos suicidas de Benray en la holored y su clan ysoki) debe ser extraída minuciosamente de las transcripciones e integrada de forma orgánica en la novela y en los dossiers.

---

## 4. Instrucción Específica: Auditoría y Preservación Obligatoria del Trasfondo y Evolución de los Personajes

> ⚠️ **INSTRUCCIÓN OBLIGATORIA PREVIA A LA REDACCIÓN O REVISIÓN DE CUALQUIER CAPÍTULO O VOLUMEN:**  
> Los elementos de trasfondo, secretos familiares, traumas del pasado, fobias psicológicas y motivaciones personales que los jugadores y el GM revelan en la mesa de juego son **el verdadero corazón emocional de la saga**. Estos detalles enriquecen la aventura prefabricada de Paizo y generan los cambios más profundos e interesantes en la historia. **Bajo ninguna circunstancia deben omitirse, recortarse o reemplazarse por acción genérica o romances inventados.**

### Procedimiento Obligatorio de Auditoría de Personajes:
Antes de estructurar o escribir un volumen, o al revisar capítulos existentes, se debe cotejar sistemáticamente el texto contra las transcripciones limpias y notas del podcast verificando:

1. **Triel Istrav:**
   - **Padre canónico:** Su padre biológico es el pirata humano de los *Free Captains* **Keiden Ashton** (según consta formalmente en las notas del podcast, NUNCA «Cayden Aston» ni «Cayden Gastón»).
   - **Origen familiar y rechazo drow:** Su madre es una influyente aristócrata drow de Apostae que despreciaba a los humanos y odiaba a Triel por ser mestiza; Triel creció sintiendo el rechazo y odio de toda su familia materna, lo que la empujó a escapar de casa con Gerty.
   - **Motivación vital:** Busca a Keiden Ashton no por gloria pirata, sino anhelando encontrar el afecto paternal y el verdadero hogar que Apostae le negó.
   - **Fobias y traumas:** Terror visceral a los **akatas** (es el primer monstruo espacial que conoció en su vida y la marcó para siempre, ocupando el puesto número uno en su lista de miedos).
2. **A.Xel 42:**
   - **Origen como esclava:** Nació como esclava minera adulta; su primer recuerdo consciente al despertar en su chasis fue que le pusieran una pala en las manos con la única consigna de «no morir hoy» (Episodio 14).
   - **El trauma de la esclavitud:** Su terror más visceral y paralizante es **volver a ser esclava** (Episodio 21: *«Usted puede ser libre, pero la esclavitud nunca sale de usted»*). Vive con la constante paranoia de que cualquier nave corporativa o corsaria los intercepte y vuelva a someterlos a todos.
   - **Lazos sintéticos y causa androide:** Rescatada hace diez años en el Vasto por su «unidad hermana» **Null-9**; comprometida con la emancipación sintética y dolida por la muerte de sus congéneres (como Clara).
   - **Prohibición de romances inventados:** Axel es lacónica, analítica y pragmática. **No existe ningún romance con el Oficial León** ni con ningún otro PNJ, salvo que surja expresamente en la mesa de juego.
3. **Marloc Boosmar:**
   - **Pérdida conyugal y duelo:** Atormentado por la pérdida de su amada esposa **Ángela**, a quien teme perder de nuevo en sus pesadillas recurrentes (Episodio 21).
   - **Fobias cósmicas:** Terror físico y existencial hacia el planeta viviente y aberrante **Aucturn**.
   - **Conflicto paterno y amnesia:** Desconfianza visceral hacia su padre **Ambrose Boosmar**, a quien culpa en el fondo de su corazón por la muerte de su madre; desconcierto ante la amnesia de la Brecha tras despertar en el aula 17 del Arcanamirium con el barathu Ritchie.
4. **Benray Galway:**
   - **Fobias:** Terror absoluto e irracional hacia los **no-muertos (*undead*)** y hacia el planeta **Eox** (Episodio 21).
   - **Clan y culpa:** Lealtad incondicional a su primo **Rim Rey** y al clan ysoki; culpa soterrada por haber huido de su familia en Triaxus tras un fatal accidente de carreras de motos de nieve que costó la vida a su mejor amigo.
   - **Fama y comedia:** Relación oportunista y tensa con su productor **Marcellus**; picardía constante con las fuerzas del orden, en particular tomando el pelo, guiñando el ojo y desafiando con humor la paciencia del **Oficial León** de los Protectores.

---

## 5. Protocolo de Expansión Continua del Canon, Escenarios y Personajes

A medida que se transcriben y novelizan nuevos lotes de episodios, la saga introduce gradualmente nuevos personajes secundarios recurrentes, escenarios clave, facciones y dinámicas personales (alianzas, lazos familiares, intrigas diplomáticas). Para preservar la coherencia absoluta a lo largo de toda la obra:

### A. Detección Temprana en Transcripciones y Auditoría de Trasfondos
Antes de redactar los capítulos de un nuevo volumen, realizar una lectura exploratoria exhaustiva de las transcripciones con una lista de control obligatoria:
1. **Auditoría de Pasado y Referencias Personales:**
   - Identificar cualquier conversación íntima, diálogo en fiestas, confesión en cabinas o mensaje privado por comunicador donde los protagonistas revelen recuerdos, mentores, naves anteriores, cicatrices o traumas familiares.
   - Contrastar cada mención familiar para distinguir hechos confirmados por el jugador/GM frente a conjeturas externas de PNJs.
2. **Detección de Subtramas Originales de Roberto (el GM):**
   - Registrar cualquier elemento que no pertenezca a la aventura de Paizo (apariciones mediáticas, transmisiones encriptadas de Null-9, enigmas rúnicos, noticias holográficas sobre Syd Velch, diplomáticos no oficiales).
3. **Nuevos Personajes Recurrentes:**
   - *Diplomáticos e Instituciones:* Identificar figuras como el **Embajador y su asistente**, registrando su personalidad, especie, intereses políticos y nivel de fricción o alianza con el grupo.
   - *Fuerzas del Orden y Vínculos Institucionales / Romances Canónicos:* Identificar al oficial de los Protectores (*The Stewards*), el **Capitán / Oficial León Holden**. Registrar su doble dimensión en mesa: por un lado, su exasperación ante las payasadas y guiños de Benray Galway; y por otro, la **relación romántica, picante y clandestina canónica con Triel Stravinski** (iniciada en los Episodios 31-32 mediante mensajes etílicos y una visita de paisano a su hotel, mantenida con miradas en el arbitraje y llamadas de preocupación, y confirmada en la despedida de Absalón y en la cita del Episodio 66). NUNCA atribuir este romance a Axel 42 (quien carece de relaciones románticas con las autoridades y está centrada en Null-9 y la causa androide) ni inventar romances con PNJs que no existan en el podcast.
   - *Lazos Familiares Reales:* Registrar con precisión los parientes genuinos de cada protagonista (madre drow en Apostae y padre **Keiden Ashton** de Triel; padre Ambrose Boosmar de Marloc; red ysoki y primo Rim Rey de Benray).
4. **Nuevos Escenarios, Naves y Objetos con Historia:**
   - Registrar naves adquiridas (*Hippocampus*, *Estrella Errante*), pecios a la deriva, reliquias mágicas u objetos tecnológicos recuperados.
5. **Pactos, Deudas y Consecuencias Legales:**
   - Acuerdos con Eox, resoluciones judiciales de arbitraje con Los Protectores, contratos con Inversiones Estelares S.C.
6. **Supremacía Absoluta del Podcast sobre el Módulo Oficial de Paizo:**
   - La partida real de *Lasers y Dragones* altera nombres de PNJs (ej. Ferani Nadaz en vez de Krane, Brock Hilario en vez de Jabaxa), modifica afiliaciones institucionales (Inversiones Estelares S.C. en vez de la Sociedad Starfinder), omite o transforma personajes oficiales (Marlene Boosmar en vez de Duravor Kreel) e introduce tramas, misterios y romances completamente originales de Roberto y los jugadores.
   - **REGLA DE ORO:** NUNCA recurrir a la wiki de Starfinder o a los manuales de Paizo como referencia de hechos, nombres o motivaciones. La única fuente canónica y fidedigna son las transcripciones de audio del podcast.
7. **Filtro Anti-Corrupción Fonética del STT y Consistencia Inter-Volumen:**
   - El reconocimiento de voz automático (STT) de YouTube o Whisper confunde con frecuencia nombres propios o anglicismos de Starfinder con palabras españolas fonéticamente similares (ej. *del Drift* -> *del triunfo*, *Aucturn* -> *octurno/autor*).
   - **Principio Inquebrantable:** NUNCA adoptar un nombre nuevo o alternativo para una entidad, lugar, nave o reliquia que ya haya aparecido en volúmenes anteriores. Ante cualquier duda, verificar siempre contra `Contexto completo/CONTEXTO_COMPLETO_SAGA.md` y [canon_y_personajes.md](./references/canon_y_personajes.md).
8. **Física del Vacío y Coherencia en Entornos Despresurizados:**
   - En naves a la deriva despresurizadas, en el vacío del espacio o en asteroides sin atmósfera, los personajes operan bajo soporte vital en escafandras o armaduras con sello ambiental (*second skin* o trajes espaciales).
   - **Administración de Sueros y Fármacos:** En el vacío NUNCA se abren viales ni se describe a personajes 'bebiendo' o 'oliendo' líquidos (se evaporarían/hervirían instantáneamente al vacío y despresurizarían al usuario). Los sueros curativos se administran mediante inyectores dérmicos (*hyposprays*) acoplados a los puertos médicos sellados de las escafandras.
   - **Brechas de Traje y Curación:** Los impactos que perforan una armadura en el vacío provocan alarmas de fuga de oxígeno y descompresión. Se resuelven aplicando parches médicos de sellado rápido (*medpatches* presurizados), que obturan la fuga contra el vacío en milésimas de segundo y liberan coagulantes y analgésicos dérmicos.
   - **Soporte Vital y Consumo de Aire:** Si se describe que una escafandra improvisada tiene autonomía limitada (ej. 10 minutos para un abordaje exterior), debe explicarse siempre la coherencia del soporte vital para estancias prolongadas (ej. adaptación de cartuchos de reciclaje de aire, tanques de oxígeno de repuesto o filtros saqueados de los almacenes de la nave).

### B. Actualización del Canon Maestro Global
Cada hallazgo debe registrarse de inmediato en [canon_y_personajes.md](./references/canon_y_personajes.md):
- Añadir la ficha del personaje usando la plantilla oficial (especie, rol, voz, vínculos, estado).
- Actualizar la tabla de continuidad de la tripulación (nave actual, refugio, estado romántico/emocional y enemigos activos).
- Fijar la grafía canónica en español e inglés para que ningún capítulo posterior sufra incongruencias ortográficas.

### C. Sincronización del Dossier del Volumen (`GLOSARIO_Y_PERSONAJES.md`)
Cada volumen (`novela_vol_X/`) debe incluir al final su propio `GLOSARIO_Y_PERSONAJES.md` actualizado:
- **1. El Escenario:** Incluir tanto Absalón como las nuevas localizaciones exploradas en ese volumen (ej. la nave *Acreon*, la *Roca del Drift*, etc.).
- **2. Los Protagonistas:** Mantener las fichas actualizadas con su evolución psicológica y de equipo.
- **3. Personajes Secundarios Clave:** Añadir las nuevas incorporaciones del volumen (el embajador y su asistente, el oficial de los Protectores / interés romántico, familiares de Triel, etc.) reflejando su estado actual al cierre de ese libro.
- **4. Corporaciones y Facciones:** Incorporar cualquier nuevo consorcio, sindicato o flota estelar que haya intervenido.

### D. Continuidad y Memoria Emocional entre Volúmenes
- Los sucesos de volúmenes previos deben dejar huella: traumas por tiroteos pasados, bromas recurrentes entre Benray y Gerty, la evolución de la desconfianza hacia la lealtad fraternal, y el florecimiento progresivo del romance entre el protagonista y el oficial de los Protectores a través de miradas, comunicaciones cuánticas a distancia o rescates arriesgados.

---

## 5. Estructura de Carpetas del Volumen

Para cada volumen nuevo, crear una carpeta independiente con la siguiente nomenclatura:

```text
novela_vol_X/
├── capitulos/
│   ├── 00_prologo.md
│   ├── 01_capitulo_1_...md
│   ├── ...
│   └── 10_capitulo_10_...md
├── GLOSARIO_Y_PERSONAJES.md      # Fichas actualizadas con los nuevos secundarios y lugares
├── generar_libro_pdf.py          # Script de maquetación y renderizado
├── README.md                     # Índice de capítulos y enlace al PDF
└── Lasers_y_Dragones_Volumen_X_Titulo.pdf
```

---

---

## 6. Maquetación Editorial y Generación del PDF

Consultar las especificaciones técnicas completas en [estandar_maquetacion_pdf.md](./references/estandar_maquetacion_pdf.md).

### A. Plantilla Estándar y Estricta de Portada Editorial
Todas las portadas de todos los volúmenes deben ser visualmente idénticas en estructura, proporciones, paleta y jerarquía. Está terminantemente prohibido alterar esta plantilla:

```html
<!-- 1. PORTADA EDITORIAL HOMOGÉNEA -->
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

> ⚠️ **Regla Crítica del Pie de Portada:**
> El pie de portada debe tener siempre la forma `VOLUMEN [X] · [TÍTULO INDICATIVO DE LA NOVELA/ARCO]` (por ejemplo: `VOLUMEN I · CONSPIRACIÓN EN LA ESPIGA` o `VOLUMEN II · LOS SECRETOS DEL VACÍO`).  
> **NUNCA** utilizar expresiones técnicas o de podcast como "Los 10 primeros episodios" ni referencias al número de capítulos emitidos.

### B. Reglas críticas de marcado HTML para LibreOffice:
1. **Portada:**
   - Usar contenedores `<div>` con estilos en línea.
   - **NO utilizar `<h1>` ni `<h2>` en la portada**, para evitar que la portada se convierta en una falsa raíz en el índice de marcadores.
2. **Capítulos y Secciones Mayores (Nivel 1 de Marcadores):**
   - Utilizar `<h2 class="chapter-name">{prefix}: <br><span class="chap-sub">{subtitle}</span></h2>`.
   - **NO utilizar `<h1>`**, ya que el filtro de importación de LibreOffice Writer/Web las ignora en el árbol de navegación.
3. **Escenas y Subsecciones (Nivel 2 de Marcadores):**
   - Utilizar `<h3 class="subsection-title">I. Nombre de la Escena</h3>`.
4. **Glosario (Nivel 2 y 3 de Marcadores):**
   - Secciones del glosario: `<h3 class="section-title">1. El Escenario</h3>`.
   - Fichas individuales: `<h4 class="subsection-title">Nombre del Personaje</h4>`.

### C. Compilación y Renderizado Headless:
```bash
user_prof="file://$(pwd)/.libreoffice_profile"
libreoffice -env:UserInstallation=$user_prof --headless --convert-to pdf libro_maquetado.html
```

---

## 7. Protocolo del Directorio Maestro `Contexto completo/` y Continuidad Global

Para asegurar que la historia, la evolución de los personajes y los hilos abiertos se mantengan impecables a lo largo de decenas de episodios, el proyecto cuenta con el directorio maestro `Contexto completo/`:

```text
Contexto completo/
├── CONTEXTO_COMPLETO_SAGA.md          # Resumen acumulativo y dossier unificado con referencias a volúmenes
├── generar_contexto_pdf.py            # Compilador HTML/CSS a PDF para LibreOffice
└── Contexto_Completo_Lasers_y_Dragones.pdf  # Libro de referencia editorial en PDF
```

### Ciclo de Mantenimiento Obligatorio en Cada Nuevo Volumen:

1. **Antes de Novelizar (Lectura de Referencia):**
   - Consultar `Contexto completo/CONTEXTO_COMPLETO_SAGA.md` para refrescar el estado emocional de los protagonistas, el inventario y mejoras de Gerty (ej. 4 brazos tras el Vol. 2), el estado romántico (interés entre Axel y el Oficial León), la nave activa (*Hippocampus*) y los aliados que viajan con el grupo (Willy y Naru).
2. **Durante la Novelización:**
   - Mantener la fidelidad absoluta a las personalidades, términos y precedentes narrativos ya establecidos.
3. **Al Culminar un Volumen (Actualización y Recompilación):**
   - **Añadir el Resumen del Nuevo Volumen:** Sintetizar los acontecimientos clave y el clímax en la Parte I.
   - **Actualizar Etiquetas de Presencia:** En cada escenario, personaje o facción que vuelva a aparecer, añadir el volumen a su campo de aparición: `[Aparece en: Volumen 1, Volumen 2, ...]`.
   - **Registrar Nuevas Entradas:** Añadir los nuevos NPCs, planetas, pecios, bestias o gremios descubiertos en ese volumen.
   - **Recompilar el PDF de Contexto:** Ejecutar `python3 "Contexto completo/generar_contexto_pdf.py"` para mantener al día el PDF para lectura del usuario y del agente.

---

## 8. Verificación de Calidad

Tras compilar cada volumen:
1. **Comprobación de Marcadores:** Ejecutar una inspección de los objetos `/Title` del PDF para verificar que todos los capítulos aparecen en el Nivel 1.
2. **Concordancia de Páginas:** Revisar que el número de página indicado para cada capítulo en la tabla del **Índice de Contenidos** coincide exactamente con la página física del PDF.
3. **Revisión Textual:** Comprobar la ortografía de los nombres canónicos (**Rim Rey**, **Chiskisk**, **Extracciones Estelares**, **Inversiones Estelares S.C.**, **Gevalarsk Nor**, **Keltus**, **Oficial León**, **Willy**, **Naru**, **Null-9**, **Syd Velch**, **Ambrose Boosmar**).
4. **Actualización de Contexto Completo:** Verificar que el archivo `Contexto completo/CONTEXTO_COMPLETO_SAGA.md` y su respectivo PDF hayan sido actualizados.
5. **Filtro Anti-Suposiciones y Verificación de Trasfondos:**
   - Comprobar rigurosamente que el texto no contenga afirmaciones de parentesco, afiliaciones o eventos pasados inventados o deducidos sin respaldo en el podcast (ej. no llamar a Marlene «hermana de Marloc», no calificar a Triel de «corsaria o pirata»).
   - Verificar que todas las referencias personales, subtramas del GM y recuerdos genuinos expresados por los jugadores y por Roberto en ese lote de episodios hayan quedado reflejados con fidelidad en la novela y en los glosarios.
6. **Auditoría Sistemática Obligatoria contra Transcripciones del Podcast (Canon vs. Paizo):**
   - Antes de dar por finalizado cualquier volumen, realizar un barrido cruzado capítulo por capítulo frente a las transcripciones limpias del lote correspondiente (`transcripciones/limpias/episodio_XX.txt`).
   - **Cero Fugas de Paizo:** Comprobar rigurosamente que NINGÚN nombre, PNJ genérico o resolución del módulo impreso de Paizo haya suplantado a la partida real (ej. jamás usar «Kreel» por Marlene, ni «Ferani Krane» por Ferani Nadaz, ni «Jabaxa» por Brock Hilario, ni «Sunrise Maiden» por Estrella Errante, ni «Sociedad Starfinder» / «Lorexpe» por Inversiones Estelares S.C.).
   - **Protagonistas Exactos de Cada Encuentro:** Verificar quiénes participaron realmente en cada escena en el audio (ej. quién se sienta a la mesa de juego, quién realiza el engaño, quién habla con un PNJ), sin trasladar artificialmente acciones de unos personajes a otros.
   - **Fidelidad Textual a Pistas y Documentos:** Las notas en datapads, cartas o mensajes de comunicador dictados por Roberto deben reproducir su tenor literal exacto (ej. nota de Clara-247: *«Triel Istrav: para herir, no matar, es un drow»*).
   - **Integración de Escenas y Rituales Canónicos:** No omitir celebraciones, rituales de luto o anécdotas de la mesa (ej. el brindis en el bar *El Pulmón Negro* ante las fotos de Marlene y Amelie, o el mote y hazaña de Brock Hilario arrancando un portón con sus manos).
7. **Auditoría de Consistencia Inter-Volumen y Barrido Anti-Alucinaciones Fonéticas:**
   - **Búsqueda activa de patrones corruptos:** Ejecutar búsquedas grep para certificar que ninguna alucinación fonética del STT se haya colado en los capítulos, glosarios o resúmenes (ej. buscar `Piedra del Triunfo`, `deriva`, `Ring Rey`, `Krane`, `Kreel`, `Sociedad Starfinder`).
   - **Cotejo Terminológico con Volúmenes Anteriores:** Contrastar el nuevo `GLOSARIO_Y_PERSONAJES.md` y los capítulos redactados con los glosarios de volúmenes previos y con `Contexto completo/CONTEXTO_COMPLETO_SAGA.md`. La toponimia (ej. *Roca del Drift*, *Estación Absalón*, *Qabarat*, *Ukulam*), las naves (*Estrella Errante*, *Acreon*, *Hippocampus*) y las reliquias pre-Brecha deben mantener una denominación 100% idéntica y homogénea a lo largo de toda la saga.

