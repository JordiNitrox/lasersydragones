# Lasers y Dragones: Proyecto Fan de Novelización (No Oficial)

> **Aviso de Proyecto Fan No Oficial:** Este proyecto es un homenaje y adaptación literaria sin ánimo de lucro realizada con dedicación por un seguidor del podcast costarricense de rol en vivo **Lasers y Dragones** (campaña *Starfinder: Dead Suns*). No es una publicación oficial de los autores del podcast ni de Paizo Inc. Su propósito es exclusivamente divulgar y permitir que tanto la comunidad de seguidores como los propios autores y jugadores de la mesa puedan disfrutar y revivir la campaña en formato de novela literaria.

Repositorio integral del proyecto de transcripción, adaptación literaria y maquetación editorial en PDF de la campaña *Dead Suns* del podcast de rol en español **Lasers y Dragones**.

---

## 📚 Estructura de Volúmenes y Directorios

El proyecto se organiza en volúmenes narrativos modulares de la saga troncal y un directorio especializado para campañas paralelas y especiales fuera de serie:

```
lasersydragones/
├── Contexto completo/                       # Archivo Maestro de Canon, Continuidad y Resumen de la Saga (49 págs PDF)
│
├── volumen_1/                               # Volumen 1: Sombras sobre Absalón (Ep 1 a 10) [CERRADO DEFINITIVAMENTE]
├── volumen_2/                               # Volumen 2: El Misterio del Acreon (Ep 11 a 22) [AUDITADO Y CORREGIDO]
├── volumen_3/                               # Volumen 3: La Roca del Drift (Ep 23 a 33) [AUDITADO Y CORREGIDO]
├── volumen_4/                               # Volumen 4: Las Torres de Qabarat (Ep 34 a 45) [AUDITADO Y CORREGIDO]
├── volumen_5/                               # Volumen 5: El Templo de los Doce Soles (Ep 46 a 59) [EN REVISIÓN]
├── volumen_6/                               # Volumen 6: El Fantasma en la Máquina (Ep 60 a 72) [EN REVISIÓN]
│
├── volumen_7/                               # Volumen 7: Mundos Fragmentados I - El Rastro hacia Eox (Ep 76b a 88) [BORRADOR EN PDF]
├── volumen_8/                               # Volumen 8: Mundos Fragmentados II - Las Cortes Cadavéricas de Eox (Ep 89 a 98) [BORRADOR EN PDF]
├── volumen_9/                               # Volumen 9: Mundos Fragmentados III - La Necrogarganta de Eox (Ep 99 a 110) [BORRADOR EN PDF]
├── volumen_10/                              # Volumen 10: Lazos de Sangre - La Sombra de Apostae (Ep 111 a 122) [PREPARADO]
├── volumen_11/                              # Volumen 11: El Rally de la Muerte en el Asteroide-Casino (Ep 123 a 135) [PREPARADO]
├── volumen_12/                              # Volumen 12: La Odisea de La Galway I - El Pecio de la Oscuridad (Ep 136 a 147) [PREPARADO]
├── volumen_13/                              # Volumen 13: La Odisea de La Galway II - El Laberinto de los Lovelorn (Ep 148 a 162) [PREPARADO]
├── volumen_14/                              # Volumen 14: Las Nubes Arruinadas I - La Ciudadela de Istamak (Ep 163 a 173) [PREPARADO]
├── volumen_15/                              # Volumen 15: Las Nubes Arruinadas II - La Forja Kishalee (Ep 174 a 185) [PREPARADO]
├── volumen_16/                              # Volumen 16: El Corazón del Padre I - El Secreto de la Deriva (Ep 186 a 201) [PREPARADO]
├── volumen_17/                              # Volumen 17: El Corazón del Padre II - La Nave de Besmara (Ep 202 a 222) [PREPARADO]
├── volumen_18/                              # Volumen 18: La Decimotercera Puerta I - Los Doce Soles (Ep 223 a 235) [PREPARADO]
├── volumen_19/                              # Volumen 19: La Decimotercera Puerta II - El Duelo de los Androides (Ep 236 a 249) [PREPARADO]
├── volumen_20/                              # Volumen 20: El Imperio de los Huesos - El Asalto al Dreadnought (Ep 250 a 272+) [EN CURSO]
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

> **Nota sobre el Estado Editorial:** Actualmente **el Volumen 1 se encuentra cerrado definitivamente y consolidado al 100%** (87 páginas en PDF maquetado con todas las correcciones de canon, combate fiel al podcast y glosario exhaustivo). Los **Volúmenes 2, 3 y 4 han sido exhaustivamente auditados y corregidos** en cuanto a continuidad, raccord y coherencia argumental con el podcast y la campaña (95, 76 y 100 páginas en PDF respectivamente). Los **Volúmenes 5 y 6 se encuentran maquetados y en fase de revisión** (66 y 59 páginas), mientras que los **Volúmenes 7, 8 y 9 disponen ya de su primer borrador completo maquetado en PDF** (105, 43 y 39 páginas). Los **Volúmenes 10 al 20** disponen de todos sus recursos preparados (transcripciones limpias, metadatos, glosarios y plantillas) para iniciar su redacción.

1. **[Volumen 1: Sombras sobre Absalón](volumen_1/novela/Lasers_y_Dragones_Volumen_1_Sombras_sobre_Absalon.pdf)** · **`[CERRADO DEFINITIVAMENTE]`**
   * *Subtítulo:* `Conspiración en la Espiga` (Episodios 1–10).
   * *Extensión:* 87 páginas, A4 editorial, navegación por marcadores, prólogo, nota editorial y anexo de personajes.
   * *Arco:* Llegada a la Estación Absalón (Sal, Marcellus, Null-9 y la sopa de almejas); colapso de Marloc y encuentro con Benrey en la motoneta amarilla; reunión en el Club 13 y revelación de la viuda Ángela; emboscada en el Muelle 94 con el sicario humano Kallio bajo órdenes de un enlace drow; combate táctico, hackeo de cámaras y huida; investigación con Chiskisk de Inversiones Estelares; reservado de Thalud en el Club 13, partida de cartas clandestina (D-52, Silo y Luigi) y rastro de Eclair; túneles de desagüe y combate en el muelle de carga; avistamiento de los emisarios drow y asalto a Con-Fusión, rendición de Ferani y Brock Hilario; botín de la caja fuerte y fuga tecno con holoskin; contrato con Chiskisk para Clamor Sambor y quiebre emocional de Marloc; arcos íntimos en el Hotel Las Lunas (Triel y Gerty, Marloc y el barman decrépito, Axel y Eclair, Benrey y Thalud con la llamada de Rim); y desayuno en el Ojo de Absalón con la emboscada del dron policial de los Protectores que enlaza de forma continua con el Volumen 2.

2. **[Volumen 2: El Misterio del Acreon](volumen_2/novela/Lasers_y_Dragones_Volumen_2_El_Misterio_del_Acreon.pdf)** · **`[AUDITADO Y CORREGIDO]`**
   * *Subtítulo:* `Los Secretos del Vacío` (Episodios 11–22).
   * *Extensión:* 95 páginas, A4 editorial.
   * *Arco:* Inicio inmediato con la evasión del dron policial en la terraza del Ojo y el pánico por el colapso del cantante Syd Velch; asesoría legal de Chiskisk y el letrado vesk Kaerom; visita a los archivos del Arcanamirium y graduación doctoral *Magna Cum Laude* de la shirren Sophie Ren; pacto secreto con el embajador Gevalarsk Nor y Keltus de Eox; ridículo lote corporativo de jabones de Extracciones Estelares; nave *Hippocampus* entregada por el Capitán Otal Seris; abordaje y exploración completa del pecio fantasma *Acreon*; plaga de Akatas y rescate de los amigoblins Willy y Naru; informe verídico y complicidad romántica de Triel con el Oficial León Anoxiar de los Protectores; y descenso final hacia el umbral de la Roca del Drift.

3. **[Volumen 3: La Roca del Drift](volumen_3/novela/Lasers_y_Dragones_Volumen_3_La_Roca_del_Drift.pdf)** · **`[AUDITADO Y CORREGIDO]`**
   * *Subtítulo:* `El Enigma Ancestral` (Episodios 23–33).
   * *Extensión:* 76 páginas, A4 editorial.
   * *Arco:* Descenso en gravedad cero a la Roca del Drift, caída de Clara-247, zombis del vacío de la tripulación del Acreon, Driftdead de Moriko Nash pacificado con proyectiles mágicos por Marloc, autómata y dron de plasma pre-Brecha, reactivación y rescate de la *Estrella Errante* (*Vagabond*), combate decisivo contra el Garaggakal, destrucción de la corbeta de la Flota de los Cuerpos, regreso triunfal a Absalón escoltados por el Capitán Poko, locura mediática con Willy y Naru vitoreados por la comunidad goblin, cobro de recompensa y ciudadanía de Eox para Marloc ante el Embajador Nor, arbitraje supremo ante el juez kasatha Keltrosho desestimando a Extracciones Estelares, solemne homenaje popular en la taberna obrera *El Pulmón Negro* con las placas del *Acreon*, mejoras cibernéticas y despedida cómplice de Triel con el Oficial León.

4. **[Volumen 4: Las Torres de Qabarat](volumen_4/novela/Lasers_y_Dragones_Volumen_4_Las_Torres_de_Qabarat.pdf)** · **`[AUDITADO Y CORREGIDO]`**
   * *Subtítulo:* `El Horizonte Esmeralda` (Episodios 34–45).
   * *Extensión:* 100 páginas, A4 editorial.
   * *Arco:* Respiro en Absalón (confrontación de Marloc con Ambrose Boosmar en el Arcanamirium sobre la esfera rúnica de Aucturn, concierto de Syd Velch en el Domo Horizonte con el «mosh pit de la rata» de Benrey, funeral de Marlene en el Jardín de Cenizas con la viuda Ángela entregando el medallón, despedida en el Club 13 y entrega a Triel por parte de León de un token cuántico cifrado); salto por el Drift hacia Castrovel; bienvenida en el espaciopuerto de Qabarat por la investigadora shirren Sophie Ren y su modesto compacto turquesa de alquiler; encargo institucional en la Universidad de Qabarat de la decana kasatha Sava Muhali para investigar el secuestro de la doctora Omejia Solstarni; pistas en la cantina Los Cinco Arcos con el contrabandista Tuwanas En y persecución automovilística contra el warwagon artillado de la Legión del Fuego en el Cielo conducida por Sophie; refugio con los corsarios Casonas y Thiable de *La Venganza* (fragata del Capitán Bonet); Triel revela a sus amigos que Keiden Ashton es su padre biológico mostrando la esfera ámbar; distracción disparatada de Benrey y Axel con la muñeca de trapo Annabelle en los archivos históricos para sustraer las tres placas pre-Brecha; tránsito por el portal de Aiakos hacia Turhalu; acogida por el naturalista Dr. Kaeral Waft y penetración en la jungla virgen de Ukulam mientras Axel afronta el recuerdo bloqueado de su servicio previo en una escuadra militar androide de exterminio.

5. **[Volumen 5: El Templo de los Doce Soles](volumen_5/novela/Lasers_y_Dragones_Volumen_5_El_Templo_de_los_Doce_Soles.pdf)** · **`[EN REVISIÓN]`**
   * *Subtítulo:* `El Templo de los Doce Soles` (Episodios 46–59).
   * *Extensión:* 66 páginas, A4 editorial.
   * *Arco:* Estampida de los Yaruks en Cabo Turhalu, Obelisco de la Runa y monos Kaukariki, emboscada de la Brasilea (ascenso a nivel 4), acecho del Khasari y piedad con Aravask, tormenta de moho y Renkruda barbado, monumento de El Elfo Reclinado, Oshiga y muerte de Salas, pasado streamer de Benrey, ciudad de Loskialua y anguila eléctrica, duelo con el Último Elfo (ascenso a nivel 5), asalto a la trinchera de Avissa, rescate de la Dra. Solstarni, muerte de Tahomen en la Cámara de las Estrellas, revelación del Devastador Estelar y coordenadas hacia La Diáspora.

6. **[Volumen 6: El Fantasma en la Máquina](volumen_6/novela/Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf)** · **`[EN REVISIÓN]`**
   * *Subtítulo:* `El Fantasma en la Máquina` (Episodios 60–72).
   * *Extensión:* 59 páginas, A4 editorial.
   * *Arco:* Evasión del vado fluvial y asedio del Campin bífido, pacto corsario con el Capitán De Bonet (*La Furia*), recuperación del «Motor del Sabor» y trampas contra ocho cápsulas de asalto de la Legión del Cielofuego, regreso a Qabarat, revelación de la fotografía de la Avenida 41 y el alma previa en el chasis de Axel, audiencia diplomática con Gevalarsk Nor y Cheesecake, infiltración en la Torre Prisma con Bumak Istrav, tiroteo del piano de cola, neutralización de la señorita Joss y saqueo de discos duros de Extracciones Astrales, fuga en alas de planeo, desenmascaramiento del falso Marcelus (el actor Bordin), despertar de la conciencia sintética en la *Estrella Errante* y salto al Drift rumbo a La Diáspora.

7. **[Contexto Completo y Guía de Continuidad](Contexto%20completo/Contexto_Completo_Lasers_y_Dragones.pdf)**
   * *Contenido:* Dossier maestro de todos los escenarios, personajes, corporaciones, bestias y matriz de continuidad con etiquetas de presencia por volumen (`[Volumen 1 al Volumen 6]`).
   * *Extensión:* 49 páginas, A4 editorial con índice y portada homogénea.

---

## 🚀 Volúmenes en Desarrollo de la Saga Troncal (7 al 20)

Para garantizar un formato literario equilibrado y homogéneo (entre 10 y 15 capítulos por libro, ~40 a 105 páginas), todos los arcos han sido estructurados en entregas autoconclusivas en sus directorios correspondientes ([`volumen_7/`](volumen_7/) al [`volumen_20/`](volumen_20/)):

* **[Volumen 7: Mundos Fragmentados I - El Rastro hacia Eox](volumen_7/novela/Lasers_y_Dragones_Volumen_7_Mundos_Fragmentados_I_El_Rastro_hacia_Eox.pdf)** (Episodios 76b al 88) · *[BORRADOR COMPLETO - 105 PÁGS PDF]*  
  *Arco:* Emboscada del Culto en Ábsalon, visión cósmica de Marloc, salto a La Diáspora, asteroide sarcesiano, base del Culto y batalla naval contra la Flota de los Cuerpos.
* **[Volumen 8: Mundos Fragmentados II - Las Cortes Cadavéricas de Eox](volumen_8/novela/Lasers_y_Dragones_Volumen_8_Mundos_Fragmentados_II_Las_Cortes_Cadavericas_de_Eox.pdf)** (Episodios 89 al 98) · *[BORRADOR COMPLETO - 43 PÁGS PDF]*  
  *Arco:* Descenso en Eox, Ministerio de los Vivos, asesinos nihili, Café Calavera y supervivencia en el sádico reality show en vivo de Zo! esquivando al Golem de Neutrones.
* **[Volumen 9: Mundos Fragmentados III - La Necrogarganta de Eox](volumen_9/novela/Lasers_y_Dragones_Volumen_9_Mundos_Fragmentados_III_La_Necrogarganta_de_Eox.pdf)** (Episodios 99 al 110) · *[BORRADOR COMPLETO - 39 PÁGS PDF]*  
  *Arco:* Marcha por los páramos marchitos de Eox, pacto con el Dragonkin, combate contra el monstruoso Ellicoth («Ellicujo»), caída de Xerantha Zatus y huida bajo fuego orbital.
* **[Volumen 10: Lazos de Sangre - La Sombra de Apostae](volumen_10/)** (Episodios 111 al 122) · *[RECURSOS PREPARADOS]*  
  *Arco:* Marcelus al descubierto, infiltración encubierta como sirvientes drow en la Casa Istrav, secretos de Keiden Ashton y primer duelo fratricida de Triel contra Jhidel.
* **[Volumen 11: El Rally de la Muerte en el Asteroide-Casino](volumen_11/)** (Episodios 123 al 135) · *[RECURSOS PREPARADOS]*  
  *Arco:* Apuestas espaciales, robots corruptos y la despiadada carrera vehicular mortal en el vacío con Marloc de piloto estrella antes de su receso.
* **[Volumen 12: La Odisea de La Galway I - El Pecio de la Oscuridad](volumen_12/)** (Episodios 136 al 147) · *[RECURSOS PREPARADOS]*  
  *Arco:* Salida temporal de Marloc y llegada de Zivok a *La Galway*; reunión con el clan ysoki y abordaje del colosal pecio no-muerto eoxiano de kilómetros de largo en el vacío (*El Corazón de la Oscuridad*).
* **[Volumen 13: La Odisea de La Galway II - El Laberinto de los Lovelorn](volumen_13/)** (Episodios 148 al 162) · *[RECURSOS PREPARADOS]*  
  *Arco:* Asedio de abominaciones *Lovelorn*, rescate del clan Galway, combate fratricida contra clones no-muertos de Axel («Axel vs Axel») y reflejos espectrales de Benrey antes de huir a Nejeor.
* **[Volumen 14: Las Nubes Arruinadas I - La Ciudadela de Istamak](volumen_14/)** (Episodios 163 al 173) · *[RECURSOS PREPARADOS]*  
  *Arco:* Emotivo retorno de Juan Pablo y Marloc (Ep 163), descenso en Nejeor, contacto con los Kish y exploración de la fabulosa ciudad flotante de Istamak y su Museo.
* **[Volumen 15: Las Nubes Arruinadas II - La Forja Kishalee](volumen_15/)** (Episodios 174 al 185) · *[RECURSOS PREPARADOS]*  
  *Arco:* Complejos micóticos, clínica médica ancestral, la forja kishalee, combate contra el campeón Xavra y obtención de las coordenadas de los Doce Soles.
* **[Volumen 16: El Corazón del Padre I - El Secreto de la Deriva](volumen_16/)** (Episodios 186 al 201) · *[RECURSOS PREPARADOS]*  
  *Arco:* Escape de Nejeor, reparaciones en Kairos, la matriarca Alistrav revela la supervivencia de Keiden Ashton a la deriva en la nave de Besmara y travesía hacia el torbellino del Maelstrom.
* **[Volumen 17: El Corazón del Padre II - La Nave de Besmara](volumen_17/)** (Episodios 202 al 222) · *[RECURSOS PREPARADOS]*  
  *Arco:* Incursión en la nave viva de Besmara en el Maelstrom, distorsiones psicoplásticas, revancha contra Jhidel Istrav, juicio del Inevitable y salvación de Keiden Ashton con el motor recuperado.
* **[Volumen 18: La Decimotercera Puerta I - Los Doce Soles](volumen_18/)** (Episodios 223 al 235) · *[RECURSOS PREPARADOS]*  
  *Arco:* El Hombre Tintineante, salto a los Doce Soles, exploración de portales y estaciones Kishalee, y misterios de las almas anteriores de Axel-42.
* **[Volumen 19: La Decimotercera Puerta II - El Duelo de los Androides](volumen_19/)** (Episodios 236 al 249) · *[RECURSOS PREPARADOS]*  
  *Arco:* Asalto al complejo de mando Kishalee, confrontación contra la jerarca androide Null-9 y la hostil IA Eltreth, apertura triunfal de la Decimotercera Puerta al Devastador Estelar.
* **[Volumen 20: El Imperio de los Huesos - El Asalto al Dreadnought](volumen_20/)** (Episodios 250 al 272+) · *[EN CURSO]*  
  *Arco:* Movilización masiva de la Flota de los Cuerpos («Atómicos Assemble»), asalto al super-dreadnought *Imperio de los Huesos*, persecución en tren de la muerte, duelo con Malakar, francotiradores baykok, visiones de sangre de Marloc y combate contra la tejedora Anasi (*Campaña activa en mesa*).

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
