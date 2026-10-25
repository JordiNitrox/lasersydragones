# Volumen 6: El Fantasma en la Máquina (Episodios 60 a 72)

Adaptación literaria y maquetación editorial en PDF del sexto bloque de la campaña *Dead Suns* del podcast de rol en vivo **Lasers y Dragones**.

---

## 📖 Ficha Técnica del Libro

* **Título:** *Lasers y Dragones: El Fantasma en la Máquina*
* **Subtítulo:** *Volumen VI · El Fantasma en la Máquina*
* **Episodios Adaptados:** Episodios 60 al 72 (13 episodios, 13 capítulos novelados + prólogo, nota editorial y anexo).
* **Extensión del PDF:** 60 páginas en formato A4 editorial de alta fidelidad.
* **Archivo PDF:** [Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf](file:///home/jordi/Proyectos/lasersydragones/volumen_6/novela/Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf)

---

## 🌌 Sinopsis del Volumen

Tras derrotar al Sumo Sacerdote Tahomen en el Templo de los Doce Soles y evitar la demolición del santuario pre-Brecha, la tripulación de la *Estrella Errante* (Triel Istrav, Gerty, Benray Galway, Marloc Boosmar y A.Xel 42) debe escapar de las profundidades de Ukulam custodiando a la doctora Omejia Solstarni.

El descenso no es sencillo: las lluvias torrenciales inundan los cañones y una bestia anfibia milenaria —el temible Campin y sus sanguijuelas alucinantes— embosca al equipo en el vado del río. Extraviados en el barro, los exploradores pactan una alianza inesperada con el Capitán De Bonet y sus piratas de *La Furia*, colaborando en la recuperación del reactor de repuesto («el Motor del Sabor») y tendiendo trampas en la espesura para frenar durante doce horas a ocho cápsulas de asalto de la Legión del Cielofuego.

De regreso a la Estación Ábsalon, la calma es solo aparente:
1. **La Identidad de Axel:** Un mensaje anónimo y una fotografía en la Avenida 41 desvelan que el chasis de Axel fue habitado por otra alma antes de su renovación en el Templo de Triuno, un secreto sellado por Claire y Null-9.
2. **El Respaldo de Eox:** El Embajador Gevalarsk Nor y Cheesecake reciben al grupo en la embajada, recompensando sus esfuerzos y financiando una expedición encubierta hacia La Diáspora para impedir que el Culto del Devorador active el Devastador Estelar.
3. **El Asalto a la Torre Prisma:** A petición de su primo Bumak Istrav —ejecutor de la Casa Istrav de Apostae—, el grupo ejecuta un golpe de espionaje corporativo contra Extracciones Astrales. Tras un tiroteo alrededor de un piano de cola contra guardias y autómatas pesados, Axel abate a la señorita Joss en su despacho privado, Triel y Marloc saquean los discos duros de la caja fuerte, y el equipo escapa en alas de planeo desde el piso 28 sobre la noche de Ábsalon.
4. **El Fantasma en la Máquina:** Benray descubre que su productor Marcelus es personificado en la estación por un actor impostor, operando el auténtico desde una estación asteroide en La Diáspora. Al integrar el procesador militar recuperado en el motor de la *Estrella Errante*, una conciencia viva y melancólica despierta en los altavoces de la nave, reconociendo el nombre de Benray y guiando a la tripulación hacia el salto al Drift con rumbo a La Diáspora.

---

## 🗂️ Estructura del Volumen

```
volumen_6/
├── metadatos/
│   └── episodios_volumen_6.json           # URLs, IDs de YouTube y sinopsis oficiales
├── transcripciones/
│   ├── raw/                               # Archivos .vtt extraídos
│   └── limpias/                           # Transcripciones en texto continuo (Episodios 60 al 72)
└── novela/
    ├── capitulos/
    │   ├── 00_nota_editorial.md
    │   ├── 00_prologo.md
    │   ├── 01_capitulo_60_el_principio_es_el_final.md
    │   ├── 02_capitulo_61_sanguijuelas_alucinantes.md
    │   ├── 03_capitulo_62_ukulam_standoff.md
    │   ├── 04_capitulo_63_los_chocopiratas_y_el_motor_del_sabor.md
    │   ├── 05_capitulo_64_me_lleva_la_trampa.md
    │   ├── 06_capitulo_65_una_foto_vale_mas_que_mil_fantasmas.md
    │   ├── 07_capitulo_66_necronversaciones_en_absalon.md
    │   ├── 08_capitulo_67_primos_sobrinos_y_productores.md
    │   ├── 09_capitulo_68_leguleyos_de_espionaje.md
    │   ├── 10_capitulo_69_teme_al_espiritu_universitario.md
    │   ├── 11_capitulo_70_hack_e_mate.md
    │   ├── 12_capitulo_71_mision_imposible_protocolo_marcelus.md
    │   └── 13_capitulo_72_fantasmeame_la_maquina.md
    ├── GLOSARIO_Y_PERSONAJES.md           # Atlas, personajes y glosario técnico
    ├── generar_libro_pdf.py               # Script de maquetación en dos pases (LibreOffice + pdftotext)
    ├── libro_maquetado.html               # Documento fuente maquetado con estilos CSS Paged Media
    └── Lasers_y_Dragones_Volumen_6_El_Fantasma_en_la_Maquina.pdf # Libro final compilado (60 páginas)
```

---

## 🛠️ Compilación del PDF

Para compilar o regenerar el libro con números de página exactos en el Índice de Contenidos:
```bash
python3 volumen_6/novela/generar_libro_pdf.py
```
El script compila automáticamente una versión preliminar para extraer con `pdftotext` las páginas físicas de cada capítulo y regenera el índice con precisión matemática.
