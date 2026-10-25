# Lasers y Dragones: Proyecto de Novelización Oficial

Repositorio integral del proyecto de transcripción, adaptación literaria y maquetación editorial en PDF de la campaña *Dead Suns* del podcast de rol en español **Lasers y Dragones**.

---

## 📚 Estructura de Volúmenes

El proyecto se organiza en volúmenes narrativos modulares y autocontenidos:

```
lasersydragones/
├── Contexto completo/                       # Archivo Maestro de Canon, Continuidad y Resumen de la Saga
│   ├── CONTEXTO_COMPLETO_SAGA.md            # Documento maestro con referencias cruzadas de volúmenes
│   ├── Contexto_Completo_Lasers_y_Dragones.pdf  # Versión editorial en PDF (48 páginas)
│   ├── generar_contexto_pdf.py              # Script compilador con LibreOffice
│   └── README.md                            # Protocolo de mantenimiento
│
├── volumen_1/                               # Volumen 1: Sombras sobre Absalón (Episodios 1 a 10)
│   ├── audios/                              # 10 episodios MP3 originales (Libsyn)
│   ├── transcripciones/                     # Subtítulos .vtt y transcripciones limpias
│   ├── metadatos/                           # episodios.json y scripts de descarga
│   └── novela/
│       ├── capitulos/                       # Capítulos 1 al 10 en Markdown
│       ├── GLOSARIO_Y_PERSONAJES.md         # Facciones, escenario y fichas
│       ├── generar_libro_pdf.py             # Motor de maquetación LibreOffice
│       └── Lasers_y_Dragones_Volumen_1_Sombras_sobre_Absalon.pdf  # PDF Final Maquetado (60 páginas)
│
├── volumen_2/                               # Volumen 2: El Misterio del Acreon (Episodios 11 a 22)
│   ├── audios/                              # 12 episodios MP3 originales descargados
│   ├── transcripciones/                     # Subtítulos .vtt y transcripciones limpias (117,718 palabras)
│   ├── metadatos/                           # episodios_volumen_2.json
│   ├── scripts/                             # Scripts automatizados de descarga y limpieza
│   ├── plan_volumen_2.md                    # Plan maestro de novelización (12 capítulos del Acreon)
│   └── novela/
│       ├── capitulos/                       # Capítulos 11 al 22 completos en Markdown
│       ├── GLOSARIO_Y_PERSONAJES.md         # Canon expandido (Eox, Goblins, Protectores, Acreon)
│       ├── generar_libro_pdf.py             # Script maquetador LibreOffice
│       └── Lasers_y_Dragones_Volumen_2_El_Misterio_del_Acreon.pdf  # PDF Final Maquetado (59 páginas)
│
├── volumen_3/                               # Volumen 3: La Roca del Drift (Episodios 23 a 33)
│   ├── audios/                              # 11 episodios MP3 originales descargados
│   ├── transcripciones/                     # Subtítulos .vtt y transcripciones limpias
│   ├── metadatos/                           # episodios_volumen_3.json
│   └── novela/
│       ├── capitulos/                       # Capítulos 23 al 33 completos en Markdown
│       ├── GLOSARIO_Y_PERSONAJES.md         # Canon expandido (Roca del Drift, Garaggakal, etc.)
│       ├── generar_libro_pdf.py             # Script maquetador LibreOffice
│       └── Lasers_y_Dragones_Volumen_3_La_Roca_del_Drift.pdf  # PDF Final Maquetado (70 páginas)
│
├── volumen_4/                               # Volumen 4: Las Torres de Qabarat (Episodios 34 a 45)
│   ├── transcripciones/                     # Subtítulos .vtt y transcripciones limpias (136,356 palabras)
│   ├── metadatos/                           # episodios_volumen_4.json
│   ├── scripts/                             # Script de descarga y procesamiento
│   └── novela/
│       ├── capitulos/                       # Capítulos 34 al 45 completos en Markdown
│       ├── GLOSARIO_Y_PERSONAJES.md         # Canon expandido (Castrovel, Qabarat, Turhalu, etc.)
│       ├── generar_libro_pdf.py             # Script maquetador LibreOffice
│       └── Lasers_y_Dragones_Volumen_4_Las_Torres_de_Qabarat.pdf  # PDF Final Maquetado (78 páginas)
│
├── volumen_5/                               # Volumen 5: El Templo de los Doce Soles (Episodios 46 a 59)
│   ├── transcripciones/                     # Subtítulos .vtt y transcripciones limpias (160,439 palabras)
│   ├── metadatos/                           # episodios_volumen_5.json
│   ├── scripts/                             # Scripts de descarga y procesamiento
│   └── novela/
│       ├── capitulos/                       # Capítulos 46 al 59 completos en Markdown
│       ├── GLOSARIO_Y_PERSONAJES.md         # Canon expandido (Ukulam, Devorador, Bestiario, Superarma)
│       ├── generar_libro_pdf.py             # Script maquetador LibreOffice con 2 pases de TOC
│       └── Lasers_y_Dragones_Volumen_5_El_Templo_de_los_Doce_Soles.pdf  # PDF Final Maquetado (67 páginas)
│
├── volumen_6/                               # Volumen 6: El Fantasma en la Máquina (Episodios 60 a 72)
│   ├── transcripciones/                     # Subtítulos .vtt y transcripciones limpias (150,000 palabras)
│   ├── metadatos/                           # episodios_volumen_6.json
│   ├── scripts/                             # Scripts de extracción y análisis
│   └── novela/
│       ├── capitulos/                       # Capítulos 60 al 72 completos en Markdown
│       ├── GLOSARIO_Y_PERSONAJES.md         # Canon expandido (Ukulam, Extracciones Astrales, La Furia, Diáspora)
│       ├── generar_libro_pdf.py             # Script maquetador LibreOffice con 2 pases de TOC
│       └── Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf  # PDF Final Maquetado (60 páginas)
│
└── .agents/skills/novelizacion-lasers-y-dragones/  # Skill y reglas metodológicas del proyecto
    ├── SKILL.md                             # Protocolo integral de descarga, escritura, portadas y PDF
    ├── references/canon_y_personajes.md     # Registro canónico continuo de personajes y facciones
    ├── references/estandar_maquetacion_pdf.md # Estándar tipográfico, portadas y CSS Paged Media
    └── scripts/limpiar_transcripcion.py     # Utilidad de deduplicación de subtítulos
```

---

## 📕 Biblioteca de Libros en PDF

1. **[Volumen 1: Sombras sobre Absalón](file:///home/jordi/Proyectos/lasersydragones/volumen_1/novela/Lasers_y_Dragones_Volumen_1_Sombras_sobre_Absalon.pdf)**
   * *Subtítulo:* `Conspiración en la Espiga` (Episodios 1–10).
   * *Extensión:* 60 páginas, A4 editorial, navegación por marcadores, prólogo y anexo.
   * *Arco:* Llegada a la Estación Absalón, tiroteo en el Muelle 94, Chiskisk, asalto al Club Con-Fusión y caída de Ferani Nadaz.

2. **[Volumen 2: El Misterio del Acreon](file:///home/jordi/Proyectos/lasersydragones/volumen_2/novela/Lasers_y_Dragones_Volumen_2_El_Misterio_del_Acreon.pdf)**
   * *Subtítulo:* `Los Secretos del Vacío` (Episodios 11–22).
   * *Extensión:* 59 páginas, A4 editorial, navegación por marcadores, prólogo y anexo.
   * *Arco:* Arbitraje de Chiskisk, pacto con el embajador Gevalarsk Nor de Eox, nave *Hippocampus*, abordaje y exploración total del pecio *Acreon*, rescate de los goblins Willy y Naru, vínculo romántico con el Oficial León y umbral exterior de la Roca del Drift.

3. **[Volumen 3: La Roca del Drift](file:///home/jordi/Proyectos/lasersydragones/volumen_3/novela/Lasers_y_Dragones_Volumen_3_La_Roca_del_Drift.pdf)**
   * *Subtítulo:* `El Enigma Ancestral` (Episodios 23–33).
   * *Extensión:* 70 páginas, A4 editorial, navegación por marcadores, prólogo y anexo.
   * *Arco:* Descenso en gravedad cero a la Roca del Drift, caída de Clara-247, Driftdead de Moriko Nash, batalla contra el Garaggakal, rescate de la *Estrella Errante*, regreso a Absalón, arbitraje del juez Keltrosho, homenaje en *El Pulmón Negro*, mejoras cibernéticas y citación de Ambrose Boosmar.

4. **[Volumen 4: Las Torres de Qabarat](file:///home/jordi/Proyectos/lasersydragones/volumen_4/novela/Lasers_y_Dragones_Volumen_4_Las_Torres_de_Qabarat.pdf)**
   * *Subtítulo:* `El Horizonte Esmeralda` (Episodios 34–45).
   * *Extensión:* 78 páginas, A4 editorial, navegación por marcadores, prólogo y anexo.
   * *Arco:* Despedida en Absalón (concierto de Syd Velch, mosh pit de Benray, funeral de Marlene, token de León), llegada a Castrovel, investigación del secuestro de Solstarni con Muhali, persecución automovilística contra la Legión, pacto corsario con *La Venganza*, expolio cómico de Annabelle en los archivos, portal de Aiakos, llegada al puesto de Turhalu con el Dr. Kaeral y penetración en la jungla de Ukulam.

5. **[Volumen 5: El Templo de los Doce Soles](file:///home/jordi/Proyectos/lasersydragones/volumen_5/novela/Lasers_y_Dragones_Volumen_5_El_Templo_de_los_Doce_Soles.pdf)**
   * *Subtítulo:* `El Templo de los Doce Soles` (Episodios 46–59).
   * *Extensión:* 67 páginas, A4 editorial, navegación por marcadores, prólogo y anexo.
   * *Arco:* Estampida de los Yaruks en Cabo Turhalu, Obelisco de la Runa y monos Kaukariki, emboscada de la Brasilea (ascenso a nivel 4), acecho del Khasari y piedad con Aravask, tormenta de moho y Renkruda barbado, monumento de El Elfo Reclinado, Oshiga y muerte de Salas, pasado streamer de Benray, ciudad de Loskialua y anguila eléctrica, duelo con el Último Elfo (ascenso a nivel 5), asalto a la trinchera de Avissa, rescate de la Dra. Solstarni, muerte de Tahomen en la Cámara de las Estrellas, revelación del Devastador Estelar y coordenadas hacia La Diáspora.

6. **[Volumen 6: El Fantasma en la Máquina](file:///home/jordi/Proyectos/lasersydragones/volumen_6/novela/Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf)**
   * *Subtítulo:* `El Fantasma en la Máquina` (Episodios 60–72).
   * *Extensión:* 60 páginas, A4 editorial, navegación por marcadores, prólogo y anexo.
   * *Arco:* Evasión del vado fluvial y asedio del Campin bífido, pacto corsario con el Capitán De Bonet (*La Furia*), recuperación del «Motor del Sabor» y trampas contra ocho cápsulas de asalto de la Legión del Cielofuego, regreso a Qabarat, revelación de la fotografía de la Avenida 41 y el alma previa en el chasis de Axel, audiencia diplomática con Gevalarsk Nor y Cheesecake, infiltración en la Torre Prisma con Bumak Istrav, tiroteo del piano de cola, neutralización de la señorita Joss y saqueo de discos duros de Extracciones Astrales, fuga en alas de planeo, desenmascaramiento del falso Marcelus (el actor Bordin), despertar de la conciencia sintética en la *Estrella Errante* y salto al Drift rumbo a La Diáspora.

7. **[Contexto Completo y Guía de Continuidad](file:///home/jordi/Proyectos/lasersydragones/Contexto%20completo/Contexto_Completo_Lasers_y_Dragones.pdf)**
   * *Contenido:* Dossier maestro de todos los escenarios, personajes, corporaciones, bestias y matriz de continuidad con etiquetas de presencia por volumen (`[Volumen 1 al Volumen 6]`).
   * *Extensión:* 48 páginas, A4 editorial con índice y portada homogénea.

---

## ⚖️ Aviso Legal, Licencia Comunitaria y Atribución

Esta obra literaria y de documentación sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de **Paizo Inc.**, utilizados bajo la *Política de Uso Comunitario de Paizo* ([paizo.com/communityuse](https://paizo.com/communityuse)). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de *Starfinder* y *Pathfinder*, visite [paizo.com](https://paizo.com).

Asimismo, este proyecto constituye un homenaje no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense **Lasers y Dragones**. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: **Roberto** (Game Master y Gerty), **Miguel** (Benray Galway), **Irene** (Triel Istrav), **Juan Pablo** (Marloc Boosmar) y **Sofía** (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
