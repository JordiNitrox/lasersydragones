#!/usr/bin/env python3
"""
Script que automatiza la creación y provisión de recursos para:
1. Volúmenes de la saga principal: volumen_7 al volumen_14
2. Directorio de especiales: especiales/ con 5 subdirectorios
"""

import os
import shutil
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLAN_DIR = os.path.join(ROOT_DIR, "planificacion_global")
META_DIR = os.path.join(PLAN_DIR, "metadatos")
RAW_DIR = os.path.join(PLAN_DIR, "transcripciones", "raw")
CLEAN_DIR = os.path.join(PLAN_DIR, "transcripciones", "limpias")

# Cargar metadatos consolidados
with open(os.path.join(META_DIR, "episodios_starfinder_73_272.json"), "r", encoding="utf-8") as f:
    sf_episodes = json.load(f)
sf_map = {ep["numero"]: ep for ep in sf_episodes}

with open(os.path.join(META_DIR, "especiales_y_spinoffs.json"), "r", encoding="utf-8") as f:
    esp_data = json.load(f)

# Definición de Volúmenes 7 al 14
VOLUMENES = {
    7: {
        "titulo": "Mundos Fragmentados I: La Diáspora de Sangre",
        "subtitulo": "Volumen VII · Mundos Fragmentados I",
        "episodios": list(range(76, 89)), # 76b al 88
        "libro_paizo": "Starfinder: Dead Suns - Libro 3: Splintered Worlds (Parte 1: La Diáspora)",
        "escenario": "Estación Ábsalon, El Drift y Cinturón de Asteroides de La Diáspora",
        "sinopsis": "Despertar abrupto en Ábsalon tras la emboscada del Culto del Devorador en el simulador virtual. Tras repeler el asalto de gnolls gracias al ingeniero halfling Valdo y presenciar la reveladora visión estelar de Marloc con la esfera jerarca, Triel se despide del Oficial León. La Estrella Errante salta al Drift hacia La Diáspora: tensión con corsarios de los Capitanes Libres, exploración en baja gravedad de un asteroide sarcesiano habitado por vampiros plateados, asalto a la base fortificada del Culto y combate naval contra la Flota de los Cuerpos."
    },
    8: {
        "titulo": "Mundos Fragmentados II: El Planeta de los Muertos",
        "subtitulo": "Volumen VIII · Mundos Fragmentados II",
        "episodios": list(range(89, 111)), # 89 al 110
        "libro_paizo": "Starfinder: Dead Suns - Libro 3: Splintered Worlds (Parte 2: Eox)",
        "escenario": "Planeta Eox, Ministerio de los Vivos, Café Calavera y la Necrogarganta",
        "sinopsis": "Descenso sobre la atmósfera radiactiva y necromántica de Eox. Lucha burocrática en el Ministerio de los Vivos, emboscadas de asesinos nihili y visita al Café Calavera. El magnate mediático Zo! les exige sobrevivir a su sádico reality show en vivo («El Camino Furibundo») esquivando al Golem de Neutrones. Con el favor de la audiencia no-muerta, asaltan la Necrogarganta, pactan con el Dragonkin, destruyen al monstruoso Ellicoth («Ellicujo») y ejecutan a la sabio óseo Xerantha Zatus, huyendo bajo bombardeo orbital."
    },
    9: {
        "titulo": "Lazos de Sangre: La Sombra de Apostae",
        "subtitulo": "Volumen IX · Lazos de Sangre",
        "episodios": list(range(111, 123)), # 111 al 122
        "libro_paizo": "Arco Canónico Propio de la Mesa (Inversiones Estelares S.C. y la Casa Istrav)",
        "escenario": "Planetoide cavernoso de Apostae, Bastiones Drow de la Casa Istrav y Thanox",
        "sinopsis": "Marcelus se manifiesta en persona para cobrar sus deudas corporativas. Triel lidera una peligrosa misión encubierta en el planetoide cavernoso de Apostae, infiltrando al equipo como sirvientes domésticos en la fortaleza de la aristocracia drow. Descubren los archivos sobre la huida de Keiden Ashton y el desprecio de su madre drow, culminando en un feroz duelo fratricida a muerte entre Triel y su hermanastra Jhidel Istrav antes de huir hacia Thanox."
    },
    10: {
        "titulo": "El Rally de la Muerte en el Asteroide-Casino",
        "subtitulo": "Volumen X · El Rally de la Muerte",
        "episodios": list(range(123, 136)), # 123 al 135
        "libro_paizo": "Transición hacia el Libro 4 de Paizo / Aventura en el límite del espacio civilizado",
        "escenario": "Asteroide-Casino, circuitos de plasma y cinturón de asteroides exterior",
        "sinopsis": "Necesitados de créditos y repuestos, los héroes atracan en un asteroide-casino gobernado por mafias y androides de placer. Para saldar cuentas, se inscriben en el letal «Rally de la Muerte»: una despiadada carrera vehicular a través de cinturones de asteroides y campos de plasma donde Marloc asume el mando como piloto estrella, antes de que tensiones personales lo lleven a tomar un receso."
    },
    11: {
        "titulo": "La Odisea de La Galway",
        "subtitulo": "Volumen XI · La Odisea de La Galway",
        "episodios": list(range(136, 163)), # 136 al 162
        "libro_paizo": "Arco Canónico Propio: Familia Galway, Zivok y Rumbo al Vasto",
        "escenario": "Carguero familiar La Galway, espacio profundo y colonias mineras ysoki",
        "sinopsis": "Juan Pablo da descanso temporal a Marloc e introduce al operativo Zivok. A bordo del destartalado carguero familiar La Galway, Benrey debe lidiar con las vendettas, deudas y paranoias de su clan ysoki (Yolmar, Valentina, Gazit y Rinrey). Entre motines, abordajes en el vacío y claustrofobia espacial, Zivok demuestra su lealtad al equipo y Triel mantiene unida la nave mientras se aproximan a las coordenadas de Nejeor."
    },
    12: {
        "titulo": "Las Nubes Arruinadas: La Ciudadela de Istamak",
        "subtitulo": "Volumen XII · Las Nubes Arruinadas",
        "episodios": list(range(163, 186)), # 163 al 185
        "libro_paizo": "Starfinder: Dead Suns - Libro 4: The Ruined Clouds",
        "escenario": "Gigante gaseoso Nejeor y la ciudadela flotante de Istamak",
        "sinopsis": "En el Episodio 163 se produce el emotivo regreso de Juan Pablo y Marloc Boosmar. Reintegrado Marloc, la Estrella Errante desciende en la tormentosa atmósfera de Nejeor y localiza la fabulosa ciudadela flotante de Istamak. Contactan con los degenerados kishalee, exploran el gigantesco Museo de Istamak esquivando aberraciones micóticas y reactivan las inteligencias artificiales para revelar las coordenadas de la Puerta de los Doce Soles."
    },
    13: {
        "titulo": "El Corazón del Padre: La Redención de Apostae",
        "subtitulo": "Volumen XIII · El Corazón del Padre",
        "episodios": list(range(186, 223)), # 186 al 222
        "libro_paizo": "Arco Canónico Propio (Conclusión de la Casa Istrav y rescate de Keiden Ashton)",
        "escenario": "Fortalezas abisales de Apostae y calabozos de la nobleza drow",
        "sinopsis": "Triel descubre que su padre biológico, el humano Keiden Ashton, no murió en el pasado: está prisionero en las mazmorras más profundas de la nobleza drow, torturado y agonizante. La tripulación ejecuta un asalto a gran escala contra los bastiones de la Casa Istrav. Entre combates mágicos en los abismos subterráneos y conspiraciones matriarcales, Triel derrota a la jerarquía drow y rescata a su padre biológico en un clímax desgarrador."
    },
    14: {
        "titulo": "La Decimotercera Puerta",
        "subtitulo": "Volumen XIV · La Decimotercera Puerta",
        "episodios": list(range(223, 250)), # 223 al 249
        "libro_paizo": "Starfinder: Dead Suns - Libro 5: The Thirteenth Gate",
        "escenario": "Sistema de los Doce Soles, estaciones de control Kishalee y la Decimotercera Puerta",
        "sinopsis": "Con las coordenadas de Nejeor, los héroes viajan al remoto sistema de los Doce Soles. Mientras Axel-42 investiga la verdad sobre sus almas sintéticas previas y su chasis mecánico, el equipo explora la descomunal mega-estructura Kishalee, sorteando laboratorios abandonados y bestias milenarias. El arco culmina con el enfrentamiento a muerte contra la jerarca androide Null-9 y la IA Eltreth, abriendo triunfalmente la Decimotercera Puerta hacia el Devastador Estelar."
    }
}

def crear_volumenes():
    print(">>> Creando directorios y recursos para Volúmenes 7 al 14...")
    for v_num, info in VOLUMENES.items():
        v_dir = os.path.join(ROOT_DIR, f"volumen_{v_num}")
        meta_dir = os.path.join(v_dir, "metadatos")
        trans_clean_dir = os.path.join(v_dir, "transcripciones", "limpias")
        trans_raw_dir = os.path.join(v_dir, "transcripciones", "raw")
        novela_dir = os.path.join(v_dir, "novela")
        caps_dir = os.path.join(novela_dir, "capitulos")

        os.makedirs(meta_dir, exist_ok=True)
        os.makedirs(trans_clean_dir, exist_ok=True)
        os.makedirs(trans_raw_dir, exist_ok=True)
        os.makedirs(caps_dir, exist_ok=True)

        # 1. Metadatos del volumen
        v_episodes = []
        for ep_num in info["episodios"]:
            if ep_num in sf_map:
                v_episodes.append(sf_map[ep_num])
                # Copiar transcripciones si existen
                clean_src = os.path.join(CLEAN_DIR, f"episodio_{ep_num:02d}.txt")
                raw_src = os.path.join(RAW_DIR, f"episodio_{ep_num:02d}.es.vtt")
                if os.path.exists(clean_src):
                    shutil.copy2(clean_src, os.path.join(trans_clean_dir, f"episodio_{ep_num:02d}.txt"))
                if os.path.exists(raw_src):
                    shutil.copy2(raw_src, os.path.join(trans_raw_dir, f"episodio_{ep_num:02d}.es.vtt"))

        with open(os.path.join(meta_dir, f"episodios_volumen_{v_num}.json"), "w", encoding="utf-8") as f:
            json.dump(v_episodes, f, indent=2, ensure_ascii=False)

        # 2. README del volumen
        readme_content = f"""# Volumen {v_num}: {info['titulo']} (Episodios {info['episodios'][0]} a {info['episodios'][-1]})

> **Proyecto:** *Lasers y Dragones: La Novela* (Adaptación fan no oficial)  
> **Fuente de Audio:** Podcast Oficial de Rol en Vivo *Lasers y Dragones*  
> **Campaña Paizo:** {info['libro_paizo']}  
> **Estado:** Recursos preparados y estructurados (listo para redacción y adaptación literaria)

---

## 📖 Ficha Técnica del Libro

* **Título:** *Lasers y Dragones: {info['titulo'].split(':')[1].strip() if ':' in info['titulo'] else info['titulo']}*
* **Subtítulo:** *{info['subtitulo']}*
* **Episodios Asignados:** Episodios {info['episodios'][0]} al {info['episodios'][-1]} ({len(info['episodios'])} episodios).
* **Escenario Principal:** {info['escenario']}.

---

## 🌌 Sinopsis del Volumen

{info['sinopsis']}

---

## 🗂️ Estructura del Directorio

```
volumen_{v_num}/
├── README.md                              # Ficha técnica y guía del volumen
├── metadatos/
│   └── episodios_volumen_{v_num}.json     # URLs, enlaces YouTube y sinopsis oficiales
├── transcripciones/
│   ├── raw/                               # Archivos .es.vtt originales de YouTube
│   └── limpias/                           # Transcripciones limpias en texto corrido
└── novela/
    ├── capitulos/                         # Borradores y capítulos novelados
    └── GLOSARIO_Y_PERSONAJES.md           # Guía de continuidad, facciones y personajes
```

---

## 📋 Lista de Capítulos a Desarrollar

| Cap | Ep Podcast | Título Episodio | Arco Narrativo |
| :-: | :---: | :--- | :--- |
"""
        for idx, ep in enumerate(v_episodes, 1):
            readme_content += f"| {idx:02d} | {ep['numero']:03d} | {ep['titulo']} | {ep.get('arco_narrativo', info['titulo'])} |\n"

        readme_content += f"""
---

## ⚖️ Nota Legal y Reconocimiento
Este volumen es una adaptación literaria sin ánimo de lucro realizada por un seguidor del podcast *Lasers y Dragones*. Todos los derechos sobre la ambientación pertenecen a Paizo Inc., y las interpretaciones y personajes originales a la mesa de *Lasers y Dragones*.
"""
        with open(os.path.join(v_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

        # 3. GLOSARIO_Y_PERSONAJES.md
        glosario_content = f"""# Glosario y Personajes: *Lasers y Dragones*
## {info['subtitulo']}

---

## 1. El Escenario Principal
* **{info['escenario']}:** Escenario central de los eventos de este volumen.
* **Marco de Campaña:** {info['libro_paizo']}.

---

## 2. Los Protagonistas
* **Triel Istrav:** Mecánica Semi-drow (Jugadora: Irene).
* **Gerty:** Dron de Combate y Asalto Pesado (Voz: Roberto).
* **Benrey Galway:** Emisario Ysoki (Jugador: Miguel).
* **Marloc Boosmar:** Tecnomante Humano (Jugador: Juan Pablo).
* **A.Xel 42:** Operativa Androide (Jugadora: Sofía).
* *(Ver notas de mesa en metadatos para rotaciones de personajes como Zivok en Volumen 11).*

---

## 3. Sinopsis y Conflictos Clave
{info['sinopsis']}
"""
        with open(os.path.join(novela_dir, "GLOSARIO_Y_PERSONAJES.md"), "w", encoding="utf-8") as f:
            f.write(glosario_content)

        # 4. Plantillas iniciales de capítulos en capitulos/
        nota_ed = os.path.join(caps_dir, "00_nota_editorial.md")
        if not os.path.exists(nota_ed):
            with open(nota_ed, "w", encoding="utf-8") as f:
                f.write(f"# Nota Editorial\n\n*Lasers y Dragones: {info['titulo']}* es una adaptación fan no oficial inspirada en los episodios {info['episodios'][0]} a {info['episodios'][-1]} del podcast *Lasers y Dragones*.\n")

        for idx, ep in enumerate(v_episodes, 1):
            cap_file = os.path.join(caps_dir, f"{idx:02d}_capitulo_{ep['numero']:03d}_{re.sub(r'[^a-zA-Z0-9]+', '_', ep['titulo'].lower())[:30]}.md")
            if not os.path.exists(cap_file):
                with open(cap_file, "w", encoding="utf-8") as f:
                    f.write(f"# Capítulo {idx}\n\n*Adaptado del Episodio {ep['numero']:03d}: {ep['titulo']}*\n\n> **Sinopsis Oficial:** {ep['sinopsis']}\n\n---\n\n<!-- Escribir el texto novelado aquí siguiendo la transcripción limpia correspondiente -->\n")

        print(f"  ✓ Creado: volumen_{v_num} ({len(v_episodes)} episodios, metadatos y transcripciones)")

def crear_especiales():
    print("\n>>> Creando directorio 'especiales/' y subdirectorios de los 5 especiales...")
    esp_dir = os.path.join(ROOT_DIR, "especiales")
    os.makedirs(esp_dir, exist_ok=True)

    # 1. README general de especiales
    readme_gral = """# Volúmenes Especiales y Spin-offs: *Lasers y Dragones*

Este directorio recopila todas las campañas paralelas, especiales temáticos y spin-offs jugados por la mesa de **Lasers y Dragones** fuera de la línea principal de *Starfinder: Dead Suns*.

---

## 📚 Catálogo de Especiales

| Directorio | Título / Campaña | Año | Sistema | Episodios | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: |
| [`01_hielo_y_sangre_2020/`](./01_hielo_y_sangre_2020/) | *Hielo y Sangre (HyS)* | 2020 | *Pathfinder 2e* | 22 | Catalogado con metadatos |
| [`02_mundo_de_oscuridad_2022_2023/`](./02_mundo_de_oscuridad_2022_2023/) | *Mundo de Oscuridad (MdO)* | 2022-2023 | *Pathfinder 2e* | 48 | Catalogado con metadatos |
| [`03_spooky_octubre_2021/`](./03_spooky_octubre_2021/) | *Spooky Octubre: Pesadilla en el Viejo Golarion* | 2021 | *Pathfinder 2e* | 4 (Ep 73-76a) | Transcripciones limpias listas |
| [`04_spooky_octubre_2025/`](./04_spooky_octubre_2025/) | *Spooky Octubre: La Trilogía de la Muerte* | 2025 | *Shadowdark RPG* | 3 | Catalogado con metadatos |
| [`05_spooky_octubre_2026/`](./05_spooky_octubre_2026/) | *Spooky Octubre: La Guardia de Medianoche* | 2026 | *Horror Gótico* | 1+ | Transcripción limpia (En emisión) |

---

## ⚖️ Nota de Proyecto Fan
Adaptaciones y recursos sin ánimo de lucro elaborados por seguidores del podcast de rol en vivo *Lasers y Dragones*.
"""
    with open(os.path.join(esp_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_gral)

    # Especial 1: HyS
    dir_hys = os.path.join(esp_dir, "01_hielo_y_sangre_2020")
    os.makedirs(os.path.join(dir_hys, "metadatos"), exist_ok=True)
    os.makedirs(os.path.join(dir_hys, "novela"), exist_ok=True)
    hys_info = esp_data["campaña_hielo_y_sangre_2020"]
    with open(os.path.join(dir_hys, "metadatos", "episodios_hys.json"), "w", encoding="utf-8") as f:
        json.dump(hys_info, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_hys, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"""# Especial: Hielo y Sangre (HyS) - Campaña 2020

> **Contexto:** {hys_info['contexto']}  
> **Sistema:** {hys_info['sistema']}  
> **Ambientación:** {hys_info['ambientacion']}  
> **Total Episodios:** {hys_info['total_episodios']} episodios emitidos en 2020.  
> **Mesa:** Roberto (GM), Irene, Sofía, Miguel y Juan Pablo.

---

## 🗂️ Recursos en este Directorio
* `metadatos/episodios_hys.json`: Catálogo de los 22 episodios con URLs de audio Libsyn, YouTube y sinopsis completas.
* `novela/`: Espacio preparado para la futura adaptación literaria de la campaña.
""")
    print("  ✓ Creado: especiales/01_hielo_y_sangre_2020")

    # Especial 2: MdO
    dir_mdo = os.path.join(esp_dir, "02_mundo_de_oscuridad_2022_2023")
    os.makedirs(os.path.join(dir_mdo, "metadatos"), exist_ok=True)
    os.makedirs(os.path.join(dir_mdo, "novela"), exist_ok=True)
    mdo_info = esp_data["campaña_mundo_de_oscuridad_2022_2023"]
    with open(os.path.join(dir_mdo, "metadatos", "episodios_mdo.json"), "w", encoding="utf-8") as f:
        json.dump(mdo_info, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_mdo, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"""# Especial: Mundo de Oscuridad (MdO) - La Caída de Piedra de Plaga (2022-2023)

> **Contexto:** {mdo_info['contexto']}  
> **Sistema:** {mdo_info['sistema']}  
> **Ambientación:** {mdo_info['ambientacion']}  
> **Total Episodios:** {mdo_info['total_episodios']} episodios emitidos entre Septiembre 2022 y Agosto 2023.  
> **Mesa:** Roberto (GM), Irene, Sofía, Miguel y Juan Pablo.

---

## 🗂️ Recursos en este Directorio
* `metadatos/episodios_mdo.json`: Catálogo completo de los 48 episodios con URLs de audio, YouTube y descripciones.
* `novela/`: Espacio preparado para la futura novelización de la aventura.
""")
    print("  ✓ Creado: especiales/02_mundo_de_oscuridad_2022_2023")

    # Especial 3: Spooky 2021
    dir_spooky21 = os.path.join(esp_dir, "03_spooky_octubre_2021")
    os.makedirs(os.path.join(dir_spooky21, "metadatos"), exist_ok=True)
    os.makedirs(os.path.join(dir_spooky21, "transcripciones", "limpias"), exist_ok=True)
    os.makedirs(os.path.join(dir_spooky21, "transcripciones", "raw"), exist_ok=True)
    os.makedirs(os.path.join(dir_spooky21, "novela", "capitulos"), exist_ok=True)

    # Copiar transcripciones 73-76
    spooky_eps = []
    for ep_num in [73, 74, 75, 76]:
        if ep_num in sf_map:
            spooky_eps.append(sf_map[ep_num])
        c_src = os.path.join(CLEAN_DIR, f"episodio_{ep_num:02d}.txt")
        r_src = os.path.join(RAW_DIR, f"episodio_{ep_num:02d}.es.vtt")
        if os.path.exists(c_src):
            shutil.copy2(c_src, os.path.join(dir_spooky21, "transcripciones", "limpias", f"episodio_{ep_num:02d}.txt"))
        if os.path.exists(r_src):
            shutil.copy2(r_src, os.path.join(dir_spooky21, "transcripciones", "raw", f"episodio_{ep_num:02d}.es.vtt"))

    with open(os.path.join(dir_spooky21, "metadatos", "episodios_spooky_2021.json"), "w", encoding="utf-8") as f:
        json.dump(spooky_eps, f, indent=2, ensure_ascii=False)

    with open(os.path.join(dir_spooky21, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# Especial: Spooky Octubre 2021 - Pesadilla en el Viejo Golarion

> **Episodios:** 73 al 76a (4 episodios / ~4 capítulos).  
> **Sistema:** *Pathfinder 2e* dentro del universo Starfinder (Cámara de inmersión virtual EPIX en Ábsalon).  
> **Avatares:** Benrey (rana Isopi Flower), Marloc (orco Valor con Bigote Sangrienta), Axel (leshy Pastinaxcel 42) y Triel (mutante Monstruo).  
> **Estado:** Transcripciones limpias y raw integradas y listas para la redacción final.

---

## 🗂️ Recursos en este Directorio
* `metadatos/episodios_spooky_2021.json`: Metadatos de los 4 episodios del especial.
* `transcripciones/limpias/`: Archivos .txt limpios de los episodios 73, 74, 75 y 76.
* `transcripciones/raw/`: Subtítulos VTT originales.
* `novela/`: Capítulos y plantillas de redacción.
""")
    print("  ✓ Creado: especiales/03_spooky_octubre_2021 (con transcripciones copiadas)")

    # Especial 4: Spooky 2025
    dir_spooky25 = os.path.join(esp_dir, "04_spooky_octubre_2025")
    os.makedirs(os.path.join(dir_spooky25, "metadatos"), exist_ok=True)
    os.makedirs(os.path.join(dir_spooky25, "novela"), exist_ok=True)
    spooky_25_eps = [ep for ep in esp_data["especiales_halloween_spooky_octubre"].get("episodios", []) if "2025" in ep.get("titulo", "") or "Trilogía" in ep.get("titulo", "") or "Parte" in ep.get("titulo", "")]
    with open(os.path.join(dir_spooky25, "metadatos", "episodios_spooky_2025.json"), "w", encoding="utf-8") as f:
        json.dump(spooky_25_eps, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_spooky25, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# Especial: Spooky Octubre 2025 - La Trilogía de la Muerte

> **Episodios:** 3 partes (*Visiones de Verano*, *El Brindis de la Muerte*, *La Danza de la Muerte*).  
> **Sistema:** *Shadowdark RPG* (OSR de horror con antorchas a tiempo real).  
> **Mesa:** Roberto (GM), Irene, Sofía, Miguel, Juan Pablo y la **jugadora invitada especial Daneris**.

---

## 🗂️ Recursos en este Directorio
* `metadatos/episodios_spooky_2025.json`: Metadatos de la trilogía.
* `novela/`: Espacio para futura adaptación.
""")
    print("  ✓ Creado: especiales/04_spooky_octubre_2025")

    # Especial 5: Spooky 2026
    dir_spooky26 = os.path.join(esp_dir, "05_spooky_octubre_2026")
    os.makedirs(os.path.join(dir_spooky26, "metadatos"), exist_ok=True)
    os.makedirs(os.path.join(dir_spooky26, "transcripciones", "limpias"), exist_ok=True)
    os.makedirs(os.path.join(dir_spooky26, "transcripciones", "raw"), exist_ok=True)
    os.makedirs(os.path.join(dir_spooky26, "novela"), exist_ok=True)

    sp_clean_src = os.path.join(CLEAN_DIR, "spooky_octubre_2026_ep01.txt")
    sp_raw_src = os.path.join(RAW_DIR, "spooky_octubre_2026_ep01.es.vtt")
    if os.path.exists(sp_clean_src):
        shutil.copy2(sp_clean_src, os.path.join(dir_spooky26, "transcripciones", "limpias", "spooky_octubre_2026_ep01.txt"))
    if os.path.exists(sp_raw_src):
        shutil.copy2(sp_raw_src, os.path.join(dir_spooky26, "transcripciones", "raw", "spooky_octubre_2026_ep01.es.vtt"))

    spooky_26_eps = [ep for ep in esp_data["especiales_halloween_spooky_octubre"].get("episodios", []) if "2026" in ep.get("titulo", "") or "spooky_octubre_2026" in str(ep)]
    with open(os.path.join(dir_spooky26, "metadatos", "episodios_spooky_2026.json"), "w", encoding="utf-8") as f:
        json.dump(spooky_26_eps, f, indent=2, ensure_ascii=False)

    with open(os.path.join(dir_spooky26, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# Especial: Spooky Octubre 2026 - La Guardia de Medianoche

> **Estado:** **En emisión activa / Temporada de Halloween 2026 no finalizada.**  
> **Episodios:** Episodio 1 (emitido el 21 de octubre de 2026) en adelante.  
> **Sistema:** Horror gótico nocturno.  
> **Mesa:** Roberto (GM), Irene, Sofía, Miguel y Juan Pablo.

---

## 🗂️ Recursos en este Directorio
* `metadatos/episodios_spooky_2026.json`: Metadatos del episodio 1 y registro de emisión.
* `transcripciones/limpias/`: `spooky_octubre_2026_ep01.txt` (13.553 palabras depuradas).
* `transcripciones/raw/`: `spooky_octubre_2026_ep01.es.vtt` original.
* `novela/`: Espacio para la redacción de la aventura.
""")
    print("  ✓ Creado: especiales/05_spooky_octubre_2026 (con transcripción limpia copiada)")

if __name__ == "__main__":
    crear_volumenes()
    crear_especiales()
    print("\n¡Todos los directorios de la saga (Vol. 7 al 14) y de Especiales han sido creados y provistos con éxito!")
