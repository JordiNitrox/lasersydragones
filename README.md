# Lasers y Dragones: Proyecto Fan de Novelización (No Oficial)

> **Aviso de Proyecto Fan No Oficial:** Este proyecto es un homenaje y adaptación literaria sin ánimo de lucro realizada con dedicación por un seguidor del podcast costarricense de rol en vivo **Lasers y Dragones** (campaña *Starfinder: Dead Suns*). No es una publicación oficial de los autores del podcast ni de Paizo Inc. Su propósito es exclusivamente divulgar y permitir que tanto la comunidad de seguidores como los propios autores y jugadores de la mesa puedan disfrutar y revivir la campaña en formato de novela literaria.

Repositorio integral del proyecto de transcripción, adaptación literaria y maquetación editorial en PDF de la campaña *Dead Suns* del podcast de rol en español **Lasers y Dragones**.

---

## 📚 Estructura de Volúmenes y Directorios

El proyecto se organiza en una carpeta contenedora de la saga troncal (`soles_muertos/`), que incluye una biblioteca centralizada con todos los libros compilados en PDF y los directorios de trabajo de cada volumen, además de los módulos para campañas paralelas y especiales:

```
lasersydragones/
├── Contexto completo/                       # Archivo Maestro de Canon, Continuidad y Resumen de la Saga (49 págs PDF)
│
├── soles_muertos/                           # Campaña Troncal: Dead Suns (Episodios 1 al 272+)
│   ├── libros_pdf/                          # Biblioteca centralizada con todos los PDF compilados (01_..., 02_..., etc.)
│   ├── volumen_1/                           # Volumen 1: Sombras sobre Absalón (Ep 1 a 10) [FINALIZADO]
│   ├── volumen_2/                           # Volumen 2: El Misterio del Acreon (Ep 11 a 22) [BORRADOR]
│   ├── volumen_3/                           # Volumen 3: La Roca del Drift (Ep 23 a 33) [BORRADOR]
│   ├── volumen_4/                           # Volumen 4: Las Torres de Qabarat (Ep 34 a 45) [BORRADOR]
│   ├── volumen_5/                           # Volumen 5: El Templo de los Doce Soles (Ep 46 a 59) [BORRADOR]
│   ├── volumen_6/                           # Volumen 6: El Fantasma en la Máquina (Ep 60 a 72) [BORRADOR]
│   ├── volumen_7/                           # Volumen 7: Mundos Fragmentados I - El Rastro hacia Eox (Ep 76b a 88) [BORRADOR]
│   ├── volumen_8/                           # Volumen 8: Mundos Fragmentados II - Las Cortes Cadavéricas de Eox (Ep 89 a 98) [BORRADOR]
│   ├── volumen_9/                           # Volumen 9: Mundos Fragmentados III - La Necrogarganta de Eox (Ep 99 a 110) [BORRADOR]
│   ├── volumen_10/                          # Volumen 10: Lazos de Sangre - La Sombra de Apostae (Ep 111 a 122) [BORRADOR]
│   ├── volumen_11/                          # Volumen 11: El Rally de la Muerte en el Asteroide-Casino (Ep 123 a 135) [BORRADOR]
│   ├── volumen_12/                          # Volumen 12: La Odisea de La Galway I - El Pecio de la Oscuridad (Ep 136 a 147) [BORRADOR]
│   ├── volumen_13/                          # Volumen 13: La Odisea de La Galway II - El Laberinto de los Lovelorn (Ep 148 a 162) [BORRADOR]
│   ├── volumen_14/                          # Volumen 14: Las Nubes Arruinadas I - La Ciudadela de Istamak (Ep 163 a 173) [BORRADOR]
│   ├── volumen_15/                          # Volumen 15: Las Nubes Arruinadas II - La Forja Kishalee (Ep 174 a 185) [BORRADOR]
│   ├── volumen_16/                          # Volumen 16: El Corazón del Padre I - El Secreto de la Deriva (Ep 186 a 201) [BORRADOR]
│   ├── volumen_17/                          # Volumen 17: El Corazón del Padre II - La Nave de Besmara (Ep 202 a 222) [BORRADOR]
│   ├── volumen_18/                          # Volumen 18: La Decimotercera Puerta I - Los Doce Soles (Ep 223 a 235) [BORRADOR]
│   ├── volumen_19/                          # Volumen 19: La Decimotercera Puerta II - El Duelo de los Androides (Ep 236 a 249) [BORRADOR]
│   └── volumen_20/                          # Volumen 20: El Imperio de los Huesos - El Asalto al Dreadnought (Ep 250 a 272+) [PLANIFICADO]
│
├── especiales/                              # Directorio de Campañas Paralelas y Especiales Fuera de Serie
│   ├── 01_hielo_y_sangre_2020/              # HyS (22 eps, Pathfinder 2e en confinamiento COVID-19)
│   ├── 02_mundo_de_oscuridad_2022_2023/     # MdO (48 eps, La Caída de Piedra de Plaga, Pathfinder 2e)
│   ├── 03_spooky_octubre_2021/              # Pesadilla en Viejo Golarion (4 eps, VR en Ábsalon)
│   ├── 04_spooky_octubre_2025/              # La Trilogía de la Muerte (3 eps, Shadowdark RPG)
│   └── 05_spooky_octubre_2026/              # La Guardia de Medianoche (Ep 1+ en emisión activa)
│
├── planificacion_global/                    # Catálogo Maestro y 201 Transcripciones Limpias (2.313.687 palabras)
│   ├── PLAN_GLOBAL_SAGA_Y_ESPECIALES.md     # Guía Maestra de los 272 episodios de la serie y spin-offs
│   ├── PLAN_DETALLADO_VOLUMENES_7_A_15.md   # Mapeo y desglose detallado de los 200 episodios de Starfinder y Especial
│   ├── metadatos/                           # Catálogos JSON consolidados (200 eps Starfinder y especiales)
│   └── transcripciones/                     # Subtítulos raw y transcripciones limpias
│
└── .agents/skills/                          # Skills y reglas metodológicas del proyecto
    ├── novelizacion-lasers-y-dragones/      # Metodología y orquestación general de la saga
    ├── lasers-narrativa-y-canon/            # Estilo literario y canon de personajes
    ├── lasers-maquetacion-pdf/              # Compilación y maquetación de libros en PDF
    └── lasers-ingesta-transcripciones/      # Limpieza y minería de transcripciones
```

---

## 📕 Biblioteca de Libros y Estado Editorial

> **Biblioteca Centralizada:** Todos los volúmenes compilados en formato PDF se encuentran accesibles de forma directa y unificada en [`soles_muertos/libros_pdf/`](soles_muertos/libros_pdf/), con prefijo numérico de dos dígitos (`01_`, `02_`, etc.) para una rápida localización y descarga.
> 
> **Nota sobre el Estado Editorial:** Actualmente **solo el Volumen 1 está FINALIZADO** (completamente cerrado y consolidado al 100%, con 89 páginas en PDF maquetado, correcciones de canon, combate fiel al podcast y glosario exhaustivo). Los **Volúmenes 2 al 19 se encuentran en estado de BORRADOR** (cuentan con borradores novelados completos y maquetaciones preliminares en PDF, pendientes de revisión final y cierre). El **Volumen 20 se encuentra PLANIFICADO** (recursos preparados y estructuración para su desarrollo).

1. **[Volumen 1: Sombras sobre Absalón](soles_muertos/libros_pdf/01_Lasers_y_Dragones_Volumen_1_Sombras_sobre_Absalon.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_1/)) · **`[FINALIZADO]`**
   * *Subtítulo:* `Conspiración en la Espiga` (Episodios 1–10).
   * *Extensión:* 89 páginas, A4 editorial, navegación por marcadores, prólogo, nota editorial y anexo de personajes.
   * *Arco:* Llegada a la Estación Absalón (Sal, Marcellus, Null-9 y la sopa de almejas); colapso de Marloc y encuentro con Benrey en la motoneta amarilla; reunión en el Club 13 y revelación de la viuda Ángela; emboscada en el Muelle 94 con el sicario humano Kallio bajo órdenes de un enlace drow; combate táctico, hackeo de cámaras y huida; investigación con Chiskisk de Inversiones Estelares; reservado de Thalud en el Club 13, partida de cartas clandestina (D-52, Silo y Luigi) y rastro de Eclair; túneles de desagüe y combate en el muelle de carga; avistamiento de los emisarios drow y asalto a Con-Fusión, rendición de Ferani y Brock Hilario; botín de la caja fuerte y fuga tecno con holoskin; contrato con Chiskisk para Clamor Sambor y quiebre emocional de Marloc; arcos íntimos en el Hotel Las Lunas (Triel y Gerty, Marloc y el barman decrépito, A.Xel y Eclair, Benrey y Thalud con la llamada de Rim); y desayuno en el Ojo de Absalón con la emboscada del dron policial de los Protectores que enlaza de forma continua con el Volumen 2.

2. **[Volumen 2: El Misterio del Acreon](soles_muertos/libros_pdf/02_Lasers_y_Dragones_Volumen_2_El_Misterio_del_Acreon.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_2/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Los Secretos del Vacío` (Episodios 11–22).
   * *Extensión:* 97 páginas, A4 editorial.
   * *Arco:* Inicio inmediato con la evasión del dron policial en la terraza del Ojo y el pánico por el colapso del cantante Syd Velch; asesoría legal de Chiskisk y el letrado vesk Kaerom; visita a los archivos del Arcanamirium y graduación doctoral *Magna Cum Laude* de la shirren Sophie Ren; pacto secreto con el embajador Gevalarsk Nor y Keltus de Eox; ridículo lote corporativo de jabones de Extracciones Estelares; nave *Hippocampus* entregada por el Capitán Otal Seris; abordaje y exploración completa del pecio fantasma *Acreon*; plaga de Akatas y rescate de los amigoblins Willy y Naru; informe verídico y complicidad romántica de Triel con el Oficial León Anoxiar de los Protectores; y descenso final hacia el umbral de la Roca del Drift.

3. **[Volumen 3: La Roca del Drift](soles_muertos/libros_pdf/03_Lasers_y_Dragones_Volumen_3_La_Roca_del_Drift.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_3/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Enigma Ancestral` (Episodios 23–33).
   * *Extensión:* 77 páginas, A4 editorial.
   * *Arco:* Descenso en gravedad cero a la Roca del Drift, caída de Clara-247, zombis del vacío de la tripulación del Acreon, Driftdead de Moriko Nash pacificado con proyectiles mágicos por Marloc, autómata y dron de plasma pre-Brecha, reactivación y rescate de la *Estrella Errante* (*Vagabond*), combate decisivo contra el Garaggakal, destrucción de la corbeta de la Flota de los Cuerpos, regreso triunfal a Absalón escoltados por el Capitán Poko, locura mediática con Willy y Naru vitoreados por la comunidad goblin, cobro de recompensa y ciudadanía de Eox para Marloc ante el Embajador Nor, arbitraje supremo ante el juez kasatha Keltrosho desestimando a Extracciones Estelares, solemne homenaje popular en la taberna obrera *El Pulmón Negro* con las placas del *Acreon*, mejoras cibernéticas y despedida cómplice de Triel con el Oficial León.

4. **[Volumen 4: Las Torres de Qabarat](soles_muertos/libros_pdf/04_Lasers_y_Dragones_Volumen_4_Las_Torres_de_Qabarat.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_4/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Horizonte Esmeralda` (Episodios 34–45).
   * *Extensión:* 100 páginas, A4 editorial.
   * *Arco:* Respiro en Absalón (confrontación de Marloc con Ambrose Boosmar en el Arcanamirium sobre la esfera rúnica de Aucturn, concierto de Syd Velch en el Domo Horizonte con el «mosh pit de la rata» de Benrey, funeral de Marlene en el Jardín de Cenizas con la viuda Ángela entregando el medallón, despedida en el Club 13 y entrega a Triel por parte de León de un token cuántico cifrado); salto por el Drift hacia Castrovel; bienvenida en el espaciopuerto de Qabarat por la investigadora shirren Sophie Ren y su modesto compacto turquesa de alquiler; encargo institucional en la Universidad de Qabarat de la decana kasatha Sava Muhali para investigar el secuestro de la doctora Omejia Solstarni; pistas en la cantina Los Cinco Arcos con el contrabandista Tuwanas En y persecución automovilística contra el warwagon artillado de la Legión del Fuego en el Cielo conducida por Sophie; refugio con los corsarios Casonas y Thiable de *La Venganza* (fragata del Capitán Bonet); Triel revela a sus amigos que Keiden Ashton es su padre biológico mostrando la esfera ámbar; distracción disparatada de Benrey y A.Xel con la muñeca de trapo Annabelle en los archivos históricos para sustraer las tres placas pre-Brecha; tránsito por el portal de Aiakos hacia Turhalu; acogida por el naturalista Dr. Kaeral Waft y penetración en la jungla virgen de Ukulam mientras A.Xel afronta el recuerdo bloqueado de su servicio previo en una escuadra militar androide de exterminio.

5. **[Volumen 5: El Templo de los Doce Soles](soles_muertos/libros_pdf/05_Lasers_y_Dragones_Volumen_5_El_Templo_de_los_Doce_Soles.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_5/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Templo de los Doce Soles` (Episodios 46–59).
   * *Extensión:* 66 páginas, A4 editorial.
   * *Arco:* Estampida de los Yaruks en Cabo Turhalu, Obelisco de la Runa y monos Kaukariki, emboscada de la Brasilea (ascenso a nivel 4), acecho del Khasari y piedad con Aravask, tormenta de moho y Renkruda barbado, monumento de El Elfo Reclinado, Oshiga y muerte de Salas, pasado streamer de Benrey, ciudad de Loskialua y anguila eléctrica, duelo con el Último Elfo (ascenso a nivel 5), asalto a la trinchera de Avissa, rescate de la Dra. Solstarni, muerte de Tahomen en la Cámara de las Estrellas, revelación del Devastador Estelar y coordenadas hacia La Diáspora.

6. **[Volumen 6: El Fantasma en la Máquina](soles_muertos/libros_pdf/06_Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_6/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Fantasma en la Máquina` (Episodios 60–72).
   * *Extensión:* 59 páginas, A4 editorial.
   * *Arco:* Evasión del vado fluvial y asedio del Campin bífido, pacto corsario con el Capitán De Bonet (*La Furia*), recuperación del «Motor del Sabor» y trampas contra ocho cápsulas de asalto de la Legión del Cielofuego, regreso a Qabarat, revelación de la fotografía de la Avenida 41 y el alma previa en el chasis de A.Xel, audiencia diplomática con Gevalarsk Nor y Cheesecake, infiltración en la Torre Prisma con Bumak Istrav, tiroteo del piano de cola, neutralización de la señorita Joss y saqueo de discos duros de Extracciones Astrales, fuga en alas de planeo, desenmascaramiento del falso Marcelus (el actor Bordin), despertar de la conciencia sintética en la *Estrella Errante* y salto al Drift rumbo a La Diáspora.

7. **[Volumen 7: Mundos Fragmentados I - El Rastro hacia Eox](soles_muertos/libros_pdf/07_Lasers_y_Dragones_Volumen_7_Mundos_Fragmentados_I_El_Rastro_hacia_Eox.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_7/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Mundos Fragmentados I - El Rastro hacia Eox` (Episodios 76b–88).
   * *Extensión:* 105 páginas, A4 editorial.
   * *Arco:* Emboscada del Culto en Absalón, visión cósmica de Marloc, salto a La Diáspora, asteroide sarcesiano, base del Culto y batalla naval contra la Flota de los Cuerpos.

8. **[Volumen 8: Mundos Fragmentados II - Las Cortes Cadavéricas de Eox](soles_muertos/libros_pdf/08_Lasers_y_Dragones_Volumen_8_Mundos_Fragmentados_II_Las_Cortes_Cadavericas_de_Eox.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_8/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Mundos Fragmentados II - Las Cortes Cadavéricas de Eox` (Episodios 89–98).
   * *Extensión:* 106 páginas, A4 editorial.
   * *Arco:* Descenso en Eox, Ministerio de los Vivos, asesinos nihili, Café Calavera y supervivencia en el sádico reality show en vivo de Zo! esquivando al Golem de Neutrones.

9. **[Volumen 9: Mundos Fragmentados III - La Necrogarganta de Eox](soles_muertos/libros_pdf/09_Lasers_y_Dragones_Volumen_9_Mundos_Fragmentados_III_La_Necrogarganta_de_Eox.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_9/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Mundos Fragmentados III - La Necrogarganta de Eox` (Episodios 99–110).
   * *Extensión:* 85 páginas, A4 editorial.
   * *Arco:* Marcha por los páramos marchitos de Eox, pacto con el Dragonkin, combate contra el monstruoso Ellicoth («Ellicujo»), caída de Xerantha Zatus y huida bajo fuego orbital.

10. **[Volumen 10: Lazos de Sangre - La Sombra de Apostae](soles_muertos/libros_pdf/10_Lasers_y_Dragones_Volumen_10_La_Sombra_de_Apostae.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_10/)) · **`[BORRADOR]`**
    * *Subtítulo:* `Lazos de Sangre - La Sombra de Apostae` (Episodios 111–122).
    * *Extensión:* 73 páginas, A4 editorial.
    * *Arco:* Marcelus al descubierto, infiltración encubierta como sirvientes drow en la Casa Istrav, secretos de Keiden Ashton y primer duelo fratricida de Triel contra Jhidel.

11. **[Volumen 11: El Rally de la Muerte en el Asteroide-Casino](soles_muertos/libros_pdf/11_Lasers_y_Dragones_Volumen_11_El_Rally_de_la_Muerte.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_11/)) · **`[BORRADOR]`**
    * *Subtítulo:* `El Rally de la Muerte en el Asteroide-Casino` (Episodios 123–135).
    * *Extensión:* 68 páginas, A4 editorial.
    * *Arco:* Apuestas espaciales, robots corruptos y la despiadada carrera vehicular mortal en el vacío con Marloc de piloto estrella antes de su receso.

12. **[Volumen 12: La Odisea de La Galway I - El Pecio de la Oscuridad](soles_muertos/libros_pdf/12_Lasers_y_Dragones_Volumen_12_El_Pecio_de_la_Oscuridad.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_12/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Odisea de La Galway I - El Pecio de la Oscuridad` (Episodios 136–147).
    * *Extensión:* 59 páginas, A4 editorial.
    * *Arco:* Salida temporal de Marloc y llegada de Zivok a *La Galway*; reunión con el clan ysoki y abordaje del colosal pecio no-muerto eoxiano de kilómetros de largo en el vacío (*El Corazón de la Oscuridad*).

13. **[Volumen 13: La Odisea de La Galway II - El Laberinto de los Lovelorn](soles_muertos/libros_pdf/13_Lasers_y_Dragones_Volumen_13_El_Laberinto_de_los_Lovelorn.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_13/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Odisea de La Galway II - El Laberinto de los Lovelorn` (Episodios 148–162).
    * *Extensión:* 73 páginas, A4 editorial.
    * *Arco:* Asedio de abominaciones *Lovelorn*, rescate del clan Galway, combate fratricida contra clones no-muertos de A.Xel («A.Xel vs A.Xel») y reflejos espectrales de Benrey antes de huir a Nejeor.

14. **[Volumen 14: Las Nubes Arruinadas I - La Ciudadela de Istamak](soles_muertos/libros_pdf/14_Lasers_y_Dragones_Volumen_14_La_Ciudadela_de_Istamak.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_14/)) · **`[BORRADOR]`**
    * *Subtítulo:* `Las Nubes Arruinadas I - La Ciudadela de Istamak` (Episodios 163–173).
    * *Extensión:* 58 páginas, A4 editorial.
    * *Arco:* Emotivo retorno de Juan Pablo y Marloc (Ep 163), descenso en Nejeor, contacto con los Kish y exploración de la fabulosa ciudad flotante de Istamak y su Museo.

15. **[Volumen 15: Las Nubes Arruinadas II - La Forja Kishalee](soles_muertos/libros_pdf/15_Lasers_y_Dragones_Volumen_15_La_Forja_Kishalee.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_15/)) · **`[BORRADOR]`**
    * *Subtítulo:* `Las Nubes Arruinadas II - La Forja Kishalee` (Episodios 174–185).
    * *Extensión:* 70 páginas, A4 editorial.
    * *Arco:* Complejos micóticos, clínica médica ancestral, la forja kishalee, combate contra el campeón Xavra y obtención de las coordenadas de los Doce Soles.

16. **[Volumen 16: El Corazón del Padre I - El Secreto de la Deriva](soles_muertos/libros_pdf/16_Lasers_y_Dragones_Volumen_16_El_Secreto_de_la_Deriva.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_16/)) · **`[BORRADOR]`**
    * *Subtítulo:* `El Corazón del Padre I - El Secreto de la Deriva` (Episodios 186–201).
    * *Extensión:* 63 páginas, A4 editorial.
    * *Arco:* Escape de Nejeor, reparaciones en Kairos, la matriarca Alistrav revela la supervivencia de Keiden Ashton a la deriva en la nave de Besmara y travesía hacia el torbellino del Maelstrom.

17. **[Volumen 17: El Corazón del Padre II - La Nave de Besmara](soles_muertos/libros_pdf/17_Lasers_y_Dragones_Volumen_17_La_Nave_de_Besmara.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_17/)) · **`[BORRADOR]`**
    * *Subtítulo:* `El Corazón del Padre II - La Nave de Besmara` (Episodios 202–222).
    * *Extensión:* 82 páginas, A4 editorial.
    * *Arco:* Incursión en la nave viva de Besmara en el Maelstrom, distorsiones psicoplásticas, revancha contra Jhidel Istrav, juicio del Inevitable y salvación de Keiden Ashton con el motor recuperado.

18. **[Volumen 18: La Decimotercera Puerta I - Los Doce Soles](soles_muertos/libros_pdf/18_Lasers_y_Dragones_Volumen_18_Los_Doce_Soles.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_18/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Decimotercera Puerta I - Los Doce Soles` (Episodios 223–235).
    * *Extensión:* 68 páginas, A4 editorial.
    * *Arco:* El Hombre Tintineante, salto a los Doce Soles, exploración de portales y estaciones Kishalee, y misterios de las almas anteriores de A.Xel 42.

19. **[Volumen 19: La Decimotercera Puerta II - El Duelo de los Androides](soles_muertos/libros_pdf/19_Lasers_y_Dragones_Volumen_19_La_Decimotercera_Puerta.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_19/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Decimotercera Puerta II - El Duelo de los Androides` (Episodios 236–249).
    * *Extensión:* 64 páginas, A4 editorial.
    * *Arco:* Asalto al complejo de mando Kishalee, confrontación contra la jerarca androide Null-9 y la hostil IA Eltreth, apertura triunfal de la Decimotercera Puerta al Devastador Estelar.

20. **[Volumen 20: El Imperio de los Huesos - El Asalto al Dreadnought](soles_muertos/volumen_20/)** · **`[PLANIFICADO]`**
    * *Subtítulo:* `El Imperio de los Huesos - El Asalto al Dreadnought` (Episodios 250 al 272+).
    * *Extensión:* *Planificado (Mesa activa de podcast)*.
    * *Arco:* Movilización masiva de la Flota de los Cuerpos («Atómicos Assemble»), asalto al super-dreadnought *Imperio de los Huesos*, persecución en tren de la muerte, duelo con Malakar, francotiradores baykok, visiones de sangre de Marloc y combate contra la tejedora Anasi.

---

## 📜 Archivo Maestro de Contexto Completo

* **[Contexto Completo y Guía de Continuidad](Contexto%20completo/Contexto_Completo_Lasers_y_Dragones.pdf)**
  * *Contenido:* Dossier maestro de todos los escenarios, personajes, corporaciones, bestias y matriz de continuidad con etiquetas de presencia por volumen (`[Volumen 1 al Volumen 19]`).
  * *Extensión:* 90 páginas, A4 editorial con índice y portada homogénea.


---

## 🎭 Directorio de Volúmenes Especiales y Spin-offs ([`especiales/`](especiales/))

Cada especial dispone de su carpeta propia con los recursos necesarios para su redacción:

* **[Especial 1: Hielo y Sangre (HyS)](especiales/01_hielo_y_sangre_2020/)** (22 Episodios, 2020)  
  *Arco:* Campaña medieval de *Pathfinder 2e* jugada durante el confinamiento de la pandemia. Prisioneros encadenados en el Peñón de la Pena en el Gran Imperio Dreki.
* **[Especial 2: Mundo de Oscuridad (MdO) - La Caída de Piedra de Plaga](especiales/02_mundo_de_oscuridad_2022_2023/)** (48 Episodios, 2022-2023)  
  *Arco:* Campaña completa de *Pathfinder 2e* adaptando la aventura oficial de Paizo durante la pausa de un año de Starfinder. Misterios y alquimia en Piedra de Plaga.
* **[Especial 3: Spooky Octubre 2021 - Pesadilla en el Viejo Golarion](especiales/03_spooky_octubre_2021/)** (Episodios 73 al 76a)  
  *Arco:* Simulación virtual de rol dentro del rol (*Pathfinder 2e* en Ábsalon): *Isopi Flower* (druida rana), *Valor* (orco), *Pastinaxcel* (leshy) y *Monstruo* (mutante). Transcripciones limpias listas.
* **[Especial 4: Spooky Octubre 2025 - La Trilogía de la Muerte](especiales/04_spooky_octubre_2025/)** (3 Episodios)  
  *Arco:* Sistema *Shadowdark RPG*, con la participación de la **jugadora invitada especial Daneris**.
* **[Especial 5: Spooky Octubre 2026 - La Guardia de Medianoche](especiales/05_spooky_octubre_2026/)** (Episodio 1 en adelante)  
  *Arco:* Entrega anual de horror para la temporada de Halloween de 2026 (*Temporada en emisión activa / No finalizada*). Transcripción limpia del Episodio 1 lista.

---

## ⚖️ Aviso Legal, Licencia Comunitaria y Atribución

Esta obra literaria y de documentación sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de **Paizo Inc.**, utilizados bajo la *Política de Uso Comunitario de Paizo* ([paizo.com/communityuse](https://paizo.com/communityuse)). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de *Starfinder* y *Pathfinder*, visite [paizo.com](https://paizo.com).

Asimismo, este proyecto constituye un **homenaje fan no oficial** y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense **Lasers y Dragones**. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: **Roberto** (Game Master y Gerty), **Miguel** (Benrey Galway), **Irene** (Triel Istrav), **Juan Pablo** (Marloc Boosmar) y **Sofía** (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
