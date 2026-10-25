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
│   ├── audios/                              # Registro y enlaces de los 12 episodios (Libsyn / YouTube)
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
│   ├── audios/                              # Registro y enlaces de los 14 episodios (Libsyn / YouTube)
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
│   ├── audios/                              # Registro y enlaces de los 13 episodios (Libsyn / YouTube)
│   ├── transcripciones/                     # Subtítulos .vtt y transcripciones limpias (150,000 palabras)
│   ├── metadatos/                           # episodios_volumen_6.json
│   ├── scripts/                             # Scripts de extracción y análisis
│   └── novela/
│       ├── capitulos/                       # Capítulos 60 al 72 completos en Markdown
│       ├── GLOSARIO_Y_PERSONAJES.md         # Canon expandido (Ukulam, Extracciones Astrales, La Furia, Diáspora)
│       ├── generar_libro_pdf.py             # Script maquetador LibreOffice con 2 pases de TOC
│       └── Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf  # PDF Final Maquetado (60 páginas)
│
├── planificacion_global/                    # Plan Maestro y 201 Transcripciones Procesadas (Episodios 73 al 272 + Especial 2026)
│   ├── PLAN_GLOBAL_SAGA_Y_ESPECIALES.md     # Guía Maestra Global de los 272 episodios de la serie y spin-offs
│   ├── PLAN_DETALLADO_VOLUMENES_7_A_15.md   # Mapeo y desglose detallado de los 200 episodios de Starfinder y Especial
│   ├── metadatos/                           # Catálogos JSON consolidados (200 eps Starfinder y especiales)
│   ├── transcripciones/                     # 201 transcripciones raw y limpias (2.313.687 palabras)
│   └── scripts/                             # Utilidades de descarga, extracción y consolidación
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

## 🚀 Próximos Volúmenes en Planificación y Catálogo de Especiales

Para consultar el mapeo exhaustivo de los 272 episodios frente a los libros de Paizo (*Dead Suns*), la rotación de personajes en mesa y los spin-offs, consulte la **[Guía Maestra Global de Novelización y Especiales](file:///home/jordi/Proyectos/lasersydragones/planificacion_global/PLAN_GLOBAL_SAGA_Y_ESPECIALES.md)** y el desglose de los 200 episodios procesados en el **[Plan Detallado de Volúmenes 7 al 15](file:///home/jordi/Proyectos/lasersydragones/planificacion_global/PLAN_DETALLADO_VOLUMENES_7_A_15.md)**:

### 🌌 Saga Principal (*Starfinder: Dead Suns*):
* **Volumen 7:** *Mundos Fragmentados I: La Diáspora de Sangre* (Episodios 76b al 88)  
  *Arco:* Emboscada real del Culto en Ábsalon, rescate de Valdo, visión cósmica de Marloc, salto al Drift hacia La Diáspora, asteroide sarcesiano, base del Culto y batalla naval contra la Flota de los Cuerpos.
* **Volumen 8:** *Mundos Fragmentados II: El Planeta de los Muertos* (Episodios 89 al 110)  
  *Arco:* Eox, Sabios Óseos, asesinos nihili, Café Calavera, reality show de Zo! («El Camino Furibundo») y asedio a la Necrogarganta contra Xerantha Zatus (Cierre Libro 3).
* **Volumen 9:** *Lazos de Sangre: La Sombra de Apostae* (Episodios 111 al 122)  
  *Arco:* Marcelus al descubierto, infiltración encubierta como sirvientes drow en la Casa Istrav, secretos de Keiden Ashton y duelo fratricida de Triel contra Jhidel.
* **Volumen 10:** *El Rally de la Muerte en el Asteroide-Casino* (Episodios 123 al 135)  
  *Arco:* Transición espacial, apuestas, robots corruptos y la carrera vehicular mortal en el vacío con Marloc de piloto.
* **Volumen 11:** *La Odisea de La Galway* (Episodios 136 al 162)  
  *Arco:* Salida temporal de Marloc; Juan Pablo introduce a Zivok; conflicto de clanes ysoki, deudas de honor y Roberto llevando a Marloc en segundo plano.
* **Volumen 12:** *Las Nubes Arruinadas: La Ciudadela de Istamak* (Episodios 163 al 185)  
  *Arco:* Retorno de Juan Pablo y Marloc (Ep 163), descenso en Nejeor, ciudad flotante de Istamak, civilización Kishalee y misterio de la Puerta Estelar (Libro 4).
* **Volumen 13:** *El Corazón del Padre: La Redención de Apostae* (Episodios 186 al 222)  
  *Arco:* Descubrimiento de que Keiden Ashton vive prisionero; asalto definitivo a Apostae, caída de la jerarquía drow y rescate agónico del padre de Triel.
* **Volumen 14:** *La Decimotercera Puerta* (Episodios 223 al 249)  
  *Arco:* Sistema de los Doce Soles, misterios de las almas previas de Axel-42, exploración de mega-ingeniería Kishalee, caída de Null-9 y de la IA Eltreth, apertura triunfal de la Decimotercera Puerta al Devastador Estelar (Libro 5).
* **Volumen 15:** *El Imperio de los Huesos (Parte 1 / En Curso)* (Episodios 250 al 272+)  
  *Arco:* La armada no-muerta de la Flota de los Cuerpos moviliza su nave insignia («Atómicos Assemble»), infiltración en el super-dreadnought *Imperio de los Huesos*, persecución en tren de la muerte, duelo con Malakar, francotiradores baykok, visiones de sangre de Marloc y combate contra la tejedora Anasi rumbo al Almirante (*Historia en curso / Campaña activa en mesa*).

### 🎭 Volúmenes Especiales y Spin-offs (Fuera de Serie):
* **Especial 1:** *Hielo y Sangre (HyS)* (22 Episodios, 2020)  
  *Arco:* Campaña medieval de *Pathfinder 2e* jugada durante el confinamiento de la pandemia. Prisioneros encadenados en el Peñón de la Pena en el Gran Imperio Dreki.
* **Especial 2:** *Mundo de Oscuridad (MdO) - La Caída de Piedra de Plaga* (48 Episodios, 2022-2023)  
  *Arco:* Campaña completa de *Pathfinder 2e* adaptando la aventura oficial de Paizo durante la pausa de un año de Starfinder. Misterios y alquimia en Piedra de Plaga.
* **Especial 3:** *Spooky Octubre 2021: Pesadilla en el Viejo Golarion* (Episodios 73 al 76a)  
  *Arco:* Simulación virtual de rol dentro del rol (*Pathfinder 2e* en Ábsalon): *Isopi Flower* (druida rana), *Valor* (orco), *Pastinaxcel* (leshy) y *Monstruo* (mutante).
* **Especial 4:** *Spooky Octubre 2025: La Trilogía de la Muerte* (3 Episodios)  
  *Arco:* Sistema *Shadowdark RPG*, con la participación de la **jugadora invitada especial Daneris**.
* **Especial 5:** *Spooky Octubre 2026: La Guardia de Medianoche* (Episodio 1 en adelante)  
  *Arco:* Entrega anual de horror para la temporada de Halloween de 2026. Misión nocturna para el Imperio (*Temporada en emisión activa / No finalizada*).


---

## ⚖️ Aviso Legal, Licencia Comunitaria y Atribución

Esta obra literaria y de documentación sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de **Paizo Inc.**, utilizados bajo la *Política de Uso Comunitario de Paizo* ([paizo.com/communityuse](https://paizo.com/communityuse)). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de *Starfinder* y *Pathfinder*, visite [paizo.com](https://paizo.com).

Asimismo, este proyecto constituye un homenaje no oficial y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense **Lasers y Dragones**. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: **Roberto** (Game Master y Gerty), **Miguel** (Benray Galway), **Irene** (Triel Istrav), **Juan Pablo** (Marloc Boosmar) y **Sofía** (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
