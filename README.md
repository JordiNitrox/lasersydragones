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
   * *Sinopsis:* Cuatro desconocidos con pasados marcados y cuentas pendientes coinciden en la monumental Estación Absalón. Lo que comienza como una escaramuza fortuita en los muelles de atraque pronto los arrastra a una turbia conspiración corporativa en los bajos fondos de la estación, obligándolos a forjar una alianza para sobrevivir.

2. **[Volumen 2: El Misterio del Acreon](soles_muertos/libros_pdf/02_Lasers_y_Dragones_Volumen_2_El_Misterio_del_Acreon.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_2/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Los Secretos del Vacío` (Episodios 11–22).
   * *Extensión:* 97 páginas, A4 editorial.
   * *Sinopsis:* Reclutados como mediadores independientes por los poderes fácticos de Absalón, la tripulación viaja al vacío para investigar el *Acreon*, un carguero minero a la deriva que ha reaparecido en cuarentena remolcando un asteroide desconocido. En los oscuros pasillos de la nave abandonada aguardan horrores extraterrestres y los primeros indicios de un enigma cósmico.

3. **[Volumen 3: La Roca del Drift](soles_muertos/libros_pdf/03_Lasers_y_Dragones_Volumen_3_La_Roca_del_Drift.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_3/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Enigma Ancestral` (Episodios 23–33).
   * *Extensión:* 77 páginas, A4 editorial.
   * *Sinopsis:* Con el carguero asegurado, los exploradores descienden a las entrañas del asteroide anómalo, un vestigio milenario arrancado de las profundidades del hiperespacio. Entre tecnología anterior a la Brecha y depredadores alienígenas, descubrirán secretos que sellarán su destino y les permitirán reclamar una nave propia.

4. **[Volumen 4: Las Torres de Qabarat](soles_muertos/libros_pdf/04_Lasers_y_Dragones_Volumen_4_Las_Torres_de_Qabarat.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_4/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Horizonte Esmeralda` (Episodios 34–45).
   * *Extensión:* 100 páginas, A4 editorial.
   * *Sinopsis:* Siguiendo el rastro de la misteriosa reliquia estelar, la tripulación viaja al planeta selvático de Castrovel. Tras navegar la intriga académica en la luminosa ciudad de Qabarat y eludir a facciones hostiles, deberán adentrarse en la peligrosa e inexplorada espesura de Ukulam en busca de una expedición científica desaparecida.

5. **[Volumen 5: El Templo de los Doce Soles](soles_muertos/libros_pdf/05_Lasers_y_Dragones_Volumen_5_El_Templo_de_los_Doce_Soles.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_5/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Templo de los Doce Soles` (Episodios 46–59).
   * *Extensión:* 66 páginas, A4 editorial.
   * *Sinopsis:* La expedición a través de la implacable jungla de Ukulam guía al grupo hasta las ruinas de un santuario legendario. En su interior deberán enfrentarse al avance del Culto del Devorador, cuyos fanáticos pretenden desatar una fuerza milenaria con el poder de aniquilar sistemas estelares enteros.

6. **[Volumen 6: El Fantasma en la Máquina](soles_muertos/libros_pdf/06_Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_6/)) · **`[BORRADOR]`**
   * *Subtítulo:* `El Fantasma en la Máquina` (Episodios 60–72).
   * *Extensión:* 59 páginas, A4 editorial.
   * *Sinopsis:* Tras la odisea en la jungla, el regreso a la civilización resulta tan peligroso como la naturaleza virgen. Acosados por agentes corporativos y desconcertados por anomalías que cobran vida en los sistemas de su propia nave, los protagonistas deben infiltrarse en las altas esferas de Castrovel antes de emprender rumbo a los confines del sistema.

7. **[Volumen 7: Mundos Fragmentados I - El Rastro hacia Eox](soles_muertos/libros_pdf/07_Lasers_y_Dragones_Volumen_7_Mundos_Fragmentados_I_El_Rastro_hacia_Eox.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_7/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Mundos Fragmentados I - El Rastro hacia Eox` (Episodios 76b–88).
   * *Extensión:* 105 páginas, A4 editorial.
   * *Sinopsis:* La búsqueda de respuestas sobre la superarma ancestral conduce a la tripulación a La Diáspora, un traicionero cinturón de asteroides. Entre piratas espaciales, emboscadas sectarias y gigantescos seres del vacío, deberán abrirse paso hacia las fronteras del siniestro planeta Eox.

8. **[Volumen 8: Mundos Fragmentados II - Las Cortes Cadavéricas de Eox](soles_muertos/libros_pdf/08_Lasers_y_Dragones_Volumen_8_Mundos_Fragmentados_II_Las_Cortes_Cadavericas_de_Eox.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_8/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Mundos Fragmentados II - Las Cortes Cadavéricas de Eox` (Episodios 89–98).
   * *Extensión:* 106 páginas, A4 editorial.
   * *Sinopsis:* En el gélido y macabro mundo gobernado por los nigromantes de Eox, los héroes deben desenvolverse entre la burocracia de los no-muertos y la fascinación mediática de la élite cadavérica, aceptando participar en una letal prueba televisada para conseguir las respuestas que buscan.

9. **[Volumen 9: Mundos Fragmentados III - La Necrogarganta de Eox](soles_muertos/libros_pdf/09_Lasers_y_Dragones_Volumen_9_Mundos_Fragmentados_III_La_Necrogarganta_de_Eox.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_9/)) · **`[BORRADOR]`**
   * *Subtítulo:* `Mundos Fragmentados III - La Necrogarganta de Eox` (Episodios 99–110).
   * *Extensión:* 85 páginas, A4 editorial.
   * *Sinopsis:* A través de páramos irradiados y desfiladeros custodiados por criaturas titánicas, la tripulación se adentra en el territorio prohibido de Eox para asaltar una instalación secreta donde los heraldos del Culto preparan su golpe definitivo.

10. **[Volumen 10: Lazos de Sangre - La Sombra de Apostae](soles_muertos/libros_pdf/10_Lasers_y_Dragones_Volumen_10_La_Sombra_de_Apostae.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_10/)) · **`[BORRADOR]`**
    * *Subtítulo:* `Lazos de Sangre - La Sombra de Apostae` (Episodios 111–122).
    * *Extensión:* 73 páginas, A4 editorial.
    * *Sinopsis:* Una arriesgada misión encubierta lleva a los protagonistas al interior del subterráneo planeta Apostae. Disfrazados e infiltrados en los palacios de los elfos oscuros, deberán sortear conspiraciones aristocráticas y afrontar deudas de sangre familiares.

11. **[Volumen 11: El Rally de la Muerte en el Asteroide-Casino](soles_muertos/libros_pdf/11_Lasers_y_Dragones_Volumen_11_El_Rally_de_la_Muerte.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_11/)) · **`[BORRADOR]`**
    * *Subtítulo:* `El Rally de la Muerte en el Asteroide-Casino` (Episodios 123–135).
    * *Extensión:* 68 páginas, A4 editorial.
    * *Sinopsis:* En un ostentoso asteroide-casino donde la fortuna y el peligro van de la mano, la tripulación debe arriesgarlo todo en una despiadada competición de vehículos espaciales en la que cualquier error se paga con la vida en el vacío.

12. **[Volumen 12: La Odisea de La Galway I - El Pecio de la Oscuridad](soles_muertos/libros_pdf/12_Lasers_y_Dragones_Volumen_12_El_Pecio_de_la_Oscuridad.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_12/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Odisea de La Galway I - El Pecio de la Oscuridad` (Episodios 136–147).
    * *Extensión:* 59 páginas, A4 editorial.
    * *Sinopsis:* Ante un desesperado llamado de auxilio que compromete a la familia de Benrey, la nave acude a los confines del espacio para abordar un crucero fantasmal de kilómetros de longitud, abandonado y repleto de misterios espectrales.

13. **[Volumen 13: La Odisea de La Galway II - El Laberinto de los Lovelorn](soles_muertos/libros_pdf/13_Lasers_y_Dragones_Volumen_13_El_Laberinto_de_los_Lovelorn.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_13/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Odisea de La Galway II - El Laberinto de los Lovelorn` (Episodios 148–162).
    * *Extensión:* 73 páginas, A4 editorial.
    * *Sinopsis:* Atrapados en las cubiertas corruptas del colosal pecio, los rescatadores deben abrirse paso a través de un dédalo de aberraciones y desafiar perturbadoras manifestaciones que ponen a prueba su cordura y su identidad para intentar salvar a los suyos.

14. **[Volumen 14: Las Nubes Arruinadas I - La Ciudadela de Istamak](soles_muertos/libros_pdf/14_Lasers_y_Dragones_Volumen_14_La_Ciudadela_de_Istamak.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_14/)) · **`[BORRADOR]`**
    * *Subtítulo:* `Las Nubes Arruinadas I - La Ciudadela de Istamak` (Episodios 163–173).
    * *Extensión:* 58 páginas, A4 editorial.
    * *Sinopsis:* Tras la angustiosa travesía del pecio, el grupo viaja a Nejeor, un inmenso gigante gaseoso en cuya atmósfera flota la mítica ciudadela en ruinas de Istamak. Allí buscarán entablar contacto con sus pobladores para descubrir el legado de una civilización pretérita.

15. **[Volumen 15: Las Nubes Arruinadas II - La Forja Kishalee](soles_muertos/libros_pdf/15_Lasers_y_Dragones_Volumen_15_La_Forja_Kishalee.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_15/)) · **`[BORRADOR]`**
    * *Subtítulo:* `Las Nubes Arruinadas II - La Forja Kishalee` (Episodios 174–185).
    * *Extensión:* 70 páginas, A4 editorial.
    * *Sinopsis:* Descendiendo a los complejos prohibidos de la metrópoli flotante entre nubes tóxicas, la tripulación busca la ancestral Forja Kishalee, desafiando peligros biológicos y guardianes celosos para obtener las coordenadas de la legendaria superarma.

16. **[Volumen 16: El Corazón del Padre I - El Secreto de la Deriva](soles_muertos/libros_pdf/16_Lasers_y_Dragones_Volumen_16_El_Secreto_de_la_Deriva.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_16/)) · **`[BORRADOR]`**
    * *Subtítulo:* `El Corazón del Padre I - El Secreto de la Deriva` (Episodios 186–201).
    * *Extensión:* 63 páginas, A4 editorial.
    * *Sinopsis:* Una revelación sobre el destino de un ser querido empuja a la tripulación hacia el turbulento Maelstrom, una peligrosa anomalía del hiperespacio donde el tiempo y las leyes físicas se desvanecen.

17. **[Volumen 17: El Corazón del Padre II - La Nave de Besmara](soles_muertos/libros_pdf/17_Lasers_y_Dragones_Volumen_17_La_Nave_de_Besmara.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_17/)) · **`[BORRADOR]`**
    * *Subtítulo:* `El Corazón del Padre II - La Nave de Besmara` (Episodios 202–222).
    * *Extensión:* 82 páginas, A4 editorial.
    * *Sinopsis:* En el corazón de la tormenta interdimensional, la tripulación asalta un navío mítico a la deriva. Rodeados de fuerzas incomprensibles y viejos adversarios, deberán arriesgar su cordura para consumar un rescate desesperado.

18. **[Volumen 18: La Decimotercera Puerta I - Los Doce Soles](soles_muertos/libros_pdf/18_Lasers_y_Dragones_Volumen_18_Los_Doce_Soles.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_18/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Decimotercera Puerta I - Los Doce Soles` (Episodios 223–235).
    * *Extensión:* 68 páginas, A4 editorial.
    * *Sinopsis:* Las coordenadas ancestrales guían a la nave hasta una colosal maravilla astronómica: un anillo de doce soles que custodian una red milenaria de portales estelares, mientras una inquietante presencia acecha desde la penumbra del vacío.

19. **[Volumen 19: La Decimotercera Puerta II - El Duelo de los Androides](soles_muertos/libros_pdf/19_Lasers_y_Dragones_Volumen_19_La_Decimotercera_Puerta.pdf)** ([Carpeta de Trabajo](soles_muertos/volumen_19/)) · **`[BORRADOR]`**
    * *Subtítulo:* `La Decimotercera Puerta II - El Duelo de los Androides` (Episodios 236–249).
    * *Extensión:* 64 páginas, A4 editorial.
    * *Sinopsis:* En el núcleo de control de la megaestructura estelar, la tripulación libra una batalla decisiva contra fuerzas sintéticas hostiles para activar la legendaria puerta y evitar que el Devastador Estelar caiga en las manos equivocadas.

20. **[Volumen 20: El Imperio de los Huesos - El Asalto al Dreadnought](soles_muertos/volumen_20/)** · **`[PLANIFICADO]`**
    * *Subtítulo:* `El Imperio de los Huesos - El Asalto al Dreadnought` (Episodios 250 al 272+).
    * *Extensión:* *Planificado (Mesa activa de podcast)*.
    * *Sinopsis:* El clímax de la saga. La tripulación encabeza una ofensiva desesperada junto a una gran coalición espacial para abordar la nave insignia de la Flota de los Cuerpos y librar el enfrentamiento definitivo por el destino de la galaxia.

---

## 📜 Archivo Maestro de Contexto Completo

* **[Contexto Completo y Guía de Continuidad](Contexto%20completo/Contexto_Completo_Lasers_y_Dragones.pdf)**
  * *Contenido:* Dossier maestro de todos los escenarios, personajes, corporaciones, bestias y matriz de continuidad con etiquetas de presencia por volumen (`[Volumen 1 al Volumen 19]`).
  * *Extensión:* 90 páginas, A4 editorial con índice y portada homogénea.


---

## 🎭 Directorio de Volúmenes Especiales y Spin-offs ([`especiales/`](especiales/))

Cada especial dispone de su carpeta propia con los recursos necesarios para su redacción:

* **[Especial 1: Hielo y Sangre (HyS)](especiales/01_hielo_y_sangre_2020/)** (22 Episodios, 2020)  
  *Sinopsis:* Campaña de fantasía medieval oscura en el Peñón de la Pena del Gran Imperio Dreki, donde un grupo de prisioneros encadenados lucha por sobrevivir y ganar su libertad (*Pathfinder 2e*).
* **[Especial 2: Mundo de Oscuridad (MdO) - La Caída de Piedra de Plaga](especiales/02_mundo_de_oscuridad_2022_2023/)** (48 Episodios, 2022-2023)  
  *Sinopsis:* Campaña de investigación, alquimia y misterio gótico en el remoto asentamiento de Piedra de Plaga, adaptando la célebre aventura de *Pathfinder 2e*.
* **[Especial 3: Spooky Octubre 2021 - Pesadilla en el Viejo Golarion](especiales/03_spooky_octubre_2021/)** (Episodios 73 al 76a)  
  *Sinopsis:* Una inmersión en realidad virtual en la que la tripulación experimenta una sesión de rol dentro del rol encarnando personajes en el legendario Viejo Golarion.
* **[Especial 4: Spooky Octubre 2025 - La Trilogía de la Muerte](especiales/04_spooky_octubre_2025/)** (3 Episodios)  
  *Sinopsis:* Aventura de horror y supervivencia en mazmorras bajo las implacables reglas de *Shadowdark RPG*, con la participación de la jugadora invitada Daneris.
* **[Especial 5: Spooky Octubre 2026 - La Guardia de Medianoche](especiales/05_spooky_octubre_2026/)** (Episodio 1 en adelante)  
  *Sinopsis:* Entrega anual de terror e investigación paranormal para la temporada de Halloween de 2026 (*en emisión activa*).

---

## ⚖️ Aviso Legal, Licencia Comunitaria y Atribución

Esta obra literaria y de documentación sin ánimo de lucro utiliza marcas comerciales y/o derechos de autor propiedad de **Paizo Inc.**, utilizados bajo la *Política de Uso Comunitario de Paizo* ([paizo.com/communityuse](https://paizo.com/communityuse)). Tenemos expresamente prohibido cobrar a los lectores por usar, descargar o acceder a este contenido. Esta obra no ha sido publicada, patrocinada ni aprobada específicamente por Paizo Inc. Para más información sobre Paizo Inc. y los productos de *Starfinder* y *Pathfinder*, visite [paizo.com](https://paizo.com).

Asimismo, este proyecto constituye un **homenaje fan no oficial** y de difusión cultural inspirado en las sesiones de rol en vivo del podcast costarricense **Lasers y Dragones**. Todos los personajes originales, diálogos, interpretaciones y expresiones creativas pertenecen a sus respectivos creadores y jugadores: **Roberto** (Game Master y Gerty), **Miguel** (Benrey Galway), **Irene** (Triel Istrav), **Juan Pablo** (Marloc Boosmar) y **Sofía** (A.Xel 42). Obra de distribución libre y gratuita para la comunidad rolera.
