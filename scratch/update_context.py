import os

CONTEXT_FILE = "Contexto completo/CONTEXTO_COMPLETO_SAGA.md"

with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Protagonistas evolución al Vol 5
triel_old = "confiesa a Marloc en privado su verdadero anhelo: encontrar en el Vasto a su padre biológico, el pirata de los Capitanes Libres Cayden Aston."
triel_new = "confiesa a Marloc en privado su verdadero anhelo: encontrar en el Vasto a su padre biológico, el pirata de los Capitanes Libres Cayden Aston. En el Vol. 4 revela la esfera de ámbar legada por su padre; en el Vol. 5 sobrevive a ser izada por los tentáculos del Oshiga en los riscos de Ukulam, desactiva el detonador de plasma de Avissa en el Templo de los Doce Soles y sintoniza la consola cósmica pre-Brecha alcanzando el nivel 5 de maestría."
text = text.replace(triel_old, triel_new)

gerty_old = "así consolidándose como el muro indestructible de la tripulación."
gerty_new = "así consolidándose como el muro indestructible de la tripulación. En el Vol. 4 y Vol. 5 actúa como la vanguardia blindada ante estampidas de Yaruks, ráfagas de ametralladora rotatoria y estatuas de piedra milenarias con sus cuatro brazos mecánicos y pica de choque."
text = text.replace(gerty_old, gerty_new)

benray_old = "manda a paseo las cláusulas usureras de los productores de la holored."
benray_new = "manda a paseo las cláusulas usureras de los productores de la holored. En el Vol. 4 desata el motín del Domo Horizonte con su 'mosh pit de la rata'; en el Vol. 5 otorga un disparo compasivo a Aravask, sus compañeros descubren en el datapad de Salas sus temerarios vídeos de juventud en Absalón y abate a Tahomen con su maniobra de 'un paso a la izquierda' en la Cámara de las Estrellas."
text = text.replace(benray_old, benray_new)

marloc_old = "articula la victoria legal de Hardscrabble ante el juez Keltrosho."
marloc_new = "articula la victoria legal de Hardscrabble ante el juez Keltrosho. En el Vol. 4 encara a su pariente Ambrose Boosmar y honra a Marlene; en el Vol. 5 descifra las inscripciones astronómicas de Loskialua, conmueve al Último Elfo con su esfera rúnica dorada y neutraliza la magia entrópica del Devorador en el santuario cumbre."
text = text.replace(marloc_old, marloc_new)

axel_old = "consolida formalmente su romance con el **Oficial León** de Los Protectores."
axel_new = "consolida formalmente su romance con el **Oficial León** de Los Protectores (quien le entrega un token cuántico antes de partir). En el Vol. 5 afronta los recuerdos reprimidos de su servicio en la Unidad 42, sobrevive a las esporas carroñeras de un Khasari, abate al francotirador Salas en su nido del Elfo Reclinado y lidera el asalto táctico contra los mercenarios de Avissa en el templo."
text = text.replace(axel_old, axel_new)

# Reemplazar apariciones de protagonistas
for p in ['Triel Istrav', 'Gerty', 'Benray Galway', 'Marloc Boosmar', 'A.Xel 42']:
    header = f"#### {p}\n"
    pos = text.find(header)
    if pos != -1:
        end_aparicion = text.find("\n", pos + len(header) + 30)
        line = text[pos:end_aparicion]
        if "Volumen 1, Volumen 2, Volumen 3" in line and "Volumen 4" not in line:
            new_line = line.replace("Volumen 1, Volumen 2, Volumen 3", "Volumen 1, Volumen 2, Volumen 3, Volumen 4, Volumen 5")
            text = text[:pos] + new_line + text[end_aparicion:]

# 2. Actualizar ubicaciones de Ukulam
ukulam_anchor = "### El Puesto de Turhalu y el Continente de Ukulam"
pos_uk = text.find(ukulam_anchor)
if pos_uk != -1:
    pos_next = text.find("---", pos_uk)
    ukulam_section = """### El Puesto de Turhalu y el Continente de Ukulam
*Ubicación geográfica:* Ukulam, hemisferio salvaje de Castrovel  
*Aparición en volúmenes:* **Volumen 4, Volumen 5**  
*Descripción:* 
* **El Puesto de Turhalu:** Estación militar reconvertida en campamento científico en la punta de una península rocosa de Ukulam. Dirigida por el Doctor Kaeral Waft, está rodeada de defensas electrificadas, campos de hongos púrpuras gigantescos y una atmósfera viscosa de calor y esporas irisadas. `[Volumen 4, Volumen 5]`
* **Las Estepas de Cabo Turhalu y el Valle de los Yaruks:** Vastas llanuras de hierba blanca de dos metros donde pastan manadas de colosales Yaruks hexápodos, escenario de una estampida devastadora y el colapso del puente del cañón. `[Volumen 5]`
* **El Obelisco de la Runa:** Hito ancestral pre-Brecha en un claro enlosado rodeado de flores azul marino, escenario de la emboscada del enjambre de Kaukariki. `[Volumen 5]`
* **La Cordillera Cantante (*Singing Range*):** Majestuosa cadena montañosa septentrional de Castrovel con vientos polares silbantes. Aloja el coloso de El Elfo Reclinado, la ciudad de Loskialua y el templo cumbre. `[Volumen 4, Volumen 5]`
* **El Monumento de El Elfo Reclinado (*Guardián de la Plaga*):** Escultura colosal de cien metros labrada en el acantilado rocoso, que aloja galerías ceremoniales, la Fuente de la Purificación Mental y la cámara craneal donde se atrincheraba Salas. `[Volumen 5]`
* **La Ciudad Olvidada de Loskialua:** Acrópolis pre-Brecha enclavada en un valle de montaña, conformada por cientos de pirámides escalonadas de basalto que sirvieron de cimientos para antiguas edificaciones suspendidas dedicadas al culto de Desna. `[Volumen 5]`
* **Las Escaleras a la Eternidad:** Escalinata vertical de más de tres mil peldaños labrados a pico en el precipicio de la cordillera, conectando Loskialua con la cima sagrada. `[Volumen 5]`
* **El Templo de los Doce Soles:** Santuario astronómico supremo en la cumbre de la Cordillera Cantante. Alberga el Atrio de las Esferas, el Gran Atrio Columnado, la Antecámara de las Constelaciones y la Cámara de las Estrellas, donde reposa la consola que enlaza con el Devastador Estelar. `[Volumen 5]`

"""
    text = text[:pos_uk] + ukulam_section + text[pos_next:]

# 3. Actualizar y agregar personajes secundarios
# Doctora Solstarni
solstarni_old = """#### Doctora Omejia Solstarni
* **Especie:** Lashunta  
* **Rol:** Arqueoastrónoma y experta en la Dinastía Osuwak (secuestrada)  
* **Aparición en volúmenes:** **Volumen 4**  
* **Descripción:** Eminente investigadora de la Universidad de Qabarat raptada en su despacho por los mercenarios de Eroopa Cual debido a sus descubrimientos sobre la red de portales y las ruinas de Ukulam."""

solstarni_new = """#### Doctora Omejia Solstarni
* **Especie:** Kasatha (cuatro brazos)  
* **Rol:** Arqueoastrónoma y catedrática superior de la Universidad de Qabarat  
* **Aparición en volúmenes:** **Volumen 4 (mención/despacho), Volumen 5**  
* **Descripción:** Eminente investigadora kasatha raptada en su despacho de Qabarat por el Culto del Devorador y forzada bajo tortura a descifrar los controles astronómicos del Templo de los Doce Soles. Es rescatada por el pelotón en la antecámara del templo y revela la existencia de la superarma Devastador Estelar y la verdadera naturaleza de la Roca del Drift como fragmento de control."""

text = text.replace(solstarni_old, solstarni_new)

# Doctor Kaeral
kaeral_old = """#### Doctor Kaeral (Kaeral Waft)
* **Especie:** Humano  
* **Rol:** Naturalista, explorador y director del Puesto de Turhalu en Ukulam  
* **Aparición en volúmenes:** **Volumen 4**"""
kaeral_new = """#### Doctor Kaeral (Kaeral Waft)
* **Especie:** Humano  
* **Rol:** Naturalista, explorador y director del Puesto de Turhalu en Ukulam  
* **Aparición en volúmenes:** **Volumen 4, Volumen 5**"""
text = text.replace(kaeral_old, kaeral_new)

# Agregar nuevos personajes de Volumen 5 antes de '---' que cierra la sección 3
nuevos_personajes = """
#### Tahomen
* **Especie:** Lashunta  
* **Rol:** Sumo Sacerdote del Culto del Devorador en Castrovel (Comandante de Ukulam)  
* **Aparición en volúmenes:** **Volumen 5**  
* **Descripción:** Líder fanático y despiadado con el rostro desfigurado por escarificaciones rituales y manto de pieles de bestias. Obsesionado con abrir la Puerta de los Doce Soles y aniquilar las estrellas, fuerza a la doctora Solstarni a descifrar el templo antes de ser abatido de un disparo en el pecho por Benray en la Cámara de las Estrellas tras transmitir las coordenadas a La Diáspora.

#### Salas
* **Especie:** Lashunta  
* **Rol:** Exoficial renegado de la Legión del Fuego en el Cielo y Francotirador del Culto  
* **Aparición en volúmenes:** **Volumen 4 (mención), Volumen 5**  
* **Descripción:** Tirador sádico y demente expulsado de la Legión tras obsesionarse con contemplar a personas devoradas vivas por bestias salvajes. Custodió el acceso a la cordillera apostado en la cabeza del Elfo Reclinado junto a su monstruo Oshiga, hasta ser abatido por Axel 42.

#### Avissa
* **Especie:** Humana  
* **Rol:** Capitana Mercenaria del Culto del Devorador  
* **Aparición en volúmenes:** **Volumen 5**  
* **Descripción:** Brutal jefa de asalto acorazada con bandana roja y una colosal ametralladora rotatoria pesada de seis cañones. Comandó la defensa del Gran Atrio Columnado con órdenes de volar el templo entero por los aires; fue abatida por el equipo tras neutralizar Triel el detonador.

#### Aravask
* **Especie:** Lashunta  
* **Rol:** Exploradora y cultista del Devorador  
* **Aparición en volúmenes:** **Volumen 5**  
* **Descripción:** Fanática del culto abandonada en la espesura tras ser infectada por las esporas carroñeras de un Khasari. En medio de su agonía febril, recibe un disparo de compasión por parte de Benray y un entierro digno bajo las raíces de Ukulam.

#### El Último Elfo de Loskialua
* **Especie:** Elfo Pre-Brecha (Inmortal)  
* **Rol:** Centinela del Templo de los Doce Soles  
* **Aparición en volúmenes:** **Volumen 5**  
* **Descripción:** Guerrero celestial que custodió el Atrio de las Esferas durante tres milenios blandiendo una espada de plasma solar inmaterial. Reconoce la esfera rúnica de Marloc, prueba la valía del pelotón en un combate honorable y se disuelve en luz dorada declarando concluida su guardia.

#### Halkueth (Halconzan)
* **Especie:** Humano (Histórico)  
* **Rol:** Explorador legendario de Castrovel  
* **Aparición en volúmenes:** **Volumen 4 (mención), Volumen 5**  
* **Descripción:** Aventurero que exploró Ukulam trescientos años atrás. Su diario de viaje y mapas manuscritos guían a los aventureros a través de las estepas, el obelisco, el Elfo Reclinado y la ciudad de Loskialua.
"""

# Insertar nuevos personajes antes de '## 4. Corporaciones, Facciones e Instituciones'
pos_sec4 = text.find("## 4. Corporaciones, Facciones e Instituciones")
if pos_sec4 != -1:
    pos_sep = text.rfind("---", 0, pos_sec4)
    text = text[:pos_sep] + nuevos_personajes + "\n---\n\n" + text[pos_sec4:]

# 4. Facciones
facciones_nuevas = """### El Culto del Devorador (*Cult of the Devourer*)
*Aparición en volúmenes:* **Volumen 4 (menciones de Salas), Volumen 5**  
Secta apocalíptica y nihilista galáctica que rinde culto a una entidad cósmica consagrada a la destrucción total del universo. En Castrovel, su célula liderada por Tahomen secuestró a la doctora Solstarni para abrir la Puerta de los Doce Soles y activar el Devastador Estelar. Sus líderes en Ukulam fueron aniquilados, pero lograron transmitir la telemetría a su bastión secreto en La Diáspora.

### Universidad de Qabarat
*Aparición en volúmenes:* **Volumen 4, Volumen 5**  
Máxima institución académica de Castrovel. Tras el exitoso rescate de la doctora Solstarni por parte de la tripulación en el Templo de los Doce Soles, la decana Muhali y la universidad quedan en deuda de gratitud permanente con el pelotón de Inversiones Estelares.
"""

pos_sec5 = text.find("## 5. Bestiario y Amenazas Cósmicas")
if pos_sec5 != -1:
    pos_sep5 = text.rfind("---", 0, pos_sec5)
    text = text[:pos_sep5] + facciones_nuevas + "\n---\n\n" + text[pos_sec5:]

# 5. Bestiario
bestias_nuevas = """
### Yaruks (Colosos Hexápodos de Ukulam)
*Aparición en volúmenes:* **Volumen 5**  
Herbívoros gigantescos de quince metros de longitud y seis patas que pastan en Cabo Turhalu. Provocaron una estampida masiva que obligó al equipo a huir por el cañón y cruzar el puente que se derrumbó tras ellos.

### Brasilea (Planta Carnívora de Emboscada)
*Aparición en volúmenes:* **Volumen 5**  
Monstruosa flor depredadora provista de decenas de zarcillos musculosos, espinas óseas y enzimas corrosivas que emboscó a Axel atrapándola en su corola hasta ser pulverizada por el pelotón.

### Khasaris («El Perro Cthulín») y Esporas Carroñeras
*Aparición en volúmenes:* **Volumen 5**  
Aberraciones tetrapodales de tejido vegetal y muscular provistas de tentáculos faciales sobre fauces circulares retráctiles. Disparan espinas cargadas de esporas carroñeras que consumen los órganos internos de presas como Aravask.

### Renkruda Barbado
*Aparición en volúmenes:* **Volumen 5**  
Superdepredador reptiliano ápice de Ukulam. Terópodo carnívoro de cuatro metros con escamas verde oliva y zarcillos bucales que atacó el refugio del pelotón durante la tormenta de moho.

### Oshiga (Depredador Aéreo Manta-Raya)
*Aparición en volúmenes:* **Volumen 5**  
Bestia alada capaz de mimetizarse e invisibilizarse en vuelo. Provista de tentáculos prensiles y un terrorífico pico circular de calamar con bilis ácida. Capturó en el aire a Triel Istrav hasta que fue ensartada y abatida por el equipo.

### Anguila de Montaña
*Aparición en volúmenes:* **Volumen 5**  
Monstruo anfibio y serpentino de cuatro metros con aletas palmeadas provistas de garras y glándulas bioeléctricas que habitaba en las pirámides de Loskialua.

### Estatuas Élficas Guardianas
*Aparición en volúmenes:* **Volumen 5**  
Constructos de piedra sagrada con lanzas solares que custodiaban la antecámara del Templo de los Doce Soles, destruidos por el equipo para proteger a la doctora Solstarni.
"""

pos_sec6 = text.find("## 6. Matriz de Continuidad y Estado de la Tripulación")
if pos_sec6 != -1:
    pos_sep6 = text.rfind("---", 0, pos_sec6)
    text = text[:pos_sep6] + bestias_nuevas + "\n---\n\n" + text[pos_sec6:]

# 6. Matriz de Continuidad (actualizar tabla con columna Volumen 5)
tabla_old = """| Parámetro | Volumen 1 (*Sombras sobre Absalón*) | Volumen 2 (*El Misterio del Acreon*) | Volumen 3 (*La Roca del Drift*) | Volumen 4 (*Las Torres de Qabarat*) |
|---|---|---|---|---|
| **Naves Activas** | Ninguna (tránsito en motoneta y muelles) | **Hippocampus** (*El Caballito de Mar*) | **Estrella Errante** (*Vagabond*) y **Hippocampus** | **Estrella Errante** (órbita de Castrovel) / Compacto de alquiler de Sophie |
| **Cuartel / Base** | Cuartuchos de alquiler en el Anillo 9 | A bordo del *Hippocampus* | Muelle 94 / Sede Inversiones Estelares / Terraza *Las Lunas* | Campus Universidad de Qabarat / Puesto de Turhalu (Ukulam) |
| **Armamento de Gerty** | Cañón láser frontal, dos brazos pesados | Cuatro brazos (añadidos manipuladores finos) | Cuatro brazos reforzados + cañón láser pesado | Cuatro brazos pesados + pica de choque y cañón láser |
| **Aliados a Bordo** | Ninguno (solo los 4 fundadores + Gerty) | Se unen los goblins **Willy** y **Naru** | Willy y Naru (ciudadanos de honor y protegidos de Eox) | Willy y Naru (en órbita); Sophie Ren (Qabarat); Dr. Kaeral (Turhalu) |
| **Contactos / Red en Absalón** | **Null-9** (Club 13), Chic, Rim Rey | Rim Rey, Embajador Nor | **Null-9** (red androide), Rim Rey, Embajador Nor, Chiskisk | **Null-9**, Oficial León (token prioritario), Decana Muhali, Casonas y Thiable |
| **Vínculos Afectivos** | Cohesión fraternal inicial en combate | Creciente atracción entre **Axel 42** y el **Oficial León** | Romance formalizado entre **Axel 42** y el **Oficial León** | Axel y León se despiden con token cuántico; Triel revela a Cayden Aston |
| **Facciones Rivales** | Reyes del Nivel 21 (destruidos) | Extracciones Estelares (vía letrado Kaerom) | Extracciones Estelares (derrotada) y **Flota de los Cuerpos** | Legión del Fuego en el Cielo, mercenarios de Eroopa Cual y el cazador Salas |
| **Pactos Secretos** | Ninguno | Sarcófago funerario de Eox asegurado | Sarcófago entregado al Embajador Nor; recompensa cobrada | Contrato con la Decana Muhali (2.500 cr.); salvoconducto corsario de *La Venganza* |
| **Misterio Cósmico** | Asesinato de Marlene Boosmar | Anomalía dimensional de la Roca del Drift; enigma de Syd Velch | Revelación de la baliza hacia el **Degenerador Estelar** | Relación de la esfera con Aucturn, portales de Aiakos y Dinastía Osuwak |
| **Posición Actual** | Salida de la Estación Absalón | Umbral exterior de la Roca del Drift | Héroes aclamados en Absalón listos para viajar al Vasto | Internándose en la selva prohibida de Ukulam hacia la Cordillera Cantante |"""

tabla_new = """| Parámetro | Volumen 1 (*Sombras sobre Absalón*) | Volumen 2 (*El Misterio del Acreon*) | Volumen 3 (*La Roca del Drift*) | Volumen 4 (*Las Torres de Qabarat*) | Volumen 5 (*El Templo de los Doce Soles*) |
|---|---|---|---|---|---|
| **Naves Activas** | Ninguna (tránsito en motoneta y muelles) | **Hippocampus** (*El Caballito de Mar*) | **Estrella Errante** (*Vagabond*) y **Hippocampus** | **Estrella Errante** (órbita de Castrovel) / Compacto de alquiler de Sophie | **Estrella Errante** (órbita de Castrovel, lista para salto a La Diáspora) |
| **Cuartel / Base** | Cuartuchos de alquiler en el Anillo 9 | A bordo del *Hippocampus* | Muelle 94 / Sede Inversiones Estelares / Terraza *Las Lunas* | Campus Universidad de Qabarat / Puesto de Turhalu (Ukulam) | Vivac de campaña en Ukulam / Templo de los Doce Soles |
| **Armamento de Gerty** | Cañón láser frontal, dos brazos pesados | Cuatro brazos (añadidos manipuladores finos) | Cuatro brazos reforzados + cañón láser pesado | Cuatro brazos pesados + pica de choque y cañón láser | Cuatro brazos reforzados + pica de alta frecuencia, ametralladora pesada y escudos |
| **Aliados a Bordo** | Ninguno (solo los 4 fundadores + Gerty) | Se unen los goblins **Willy** y **Naru** | Willy y Naru (ciudadanos de honor y protegidos de Eox) | Willy y Naru (en órbita); Sophie Ren (Qabarat); Dr. Kaeral (Turhalu) | Willy y Naru (en órbita); **Doctora Omejia Solstarni** (rescatada); Dr. Kaeral |
| **Contactos / Red** | **Null-9** (Club 13), Chic, Rim Rey | Rim Rey, Embajador Nor | **Null-9** (red androide), Rim Rey, Embajador Nor, Chiskisk | **Null-9**, Oficial León (token prioritario), Decana Muhali, Casonas y Thiable | **Null-9**, Oficial León, Decana Muhali, claustro de la Universidad de Qabarat |
| **Vínculos Afectivos** | Cohesión fraternal inicial en combate | Creciente atracción entre **Axel 42** y el **Oficial León** | Romance formalizado entre **Axel 42** y el **Oficial León** | Axel y León se despiden con token cuántico; Triel revela a Cayden Aston | Triel supera trauma de Oshiga; Benray reconciliado con su pasado; Axel asume Unidad 42 |
| **Facciones Rivales** | Reyes del Nivel 21 (destruidos) | Extracciones Estelares (vía letrado Kaerom) | Extracciones Estelares (derrotada) y **Flota de los Cuerpos** | Legión del Fuego en el Cielo, mercenarios de Eroopa Cual y el cazador Salas | **Culto del Devorador** (célula de Castrovel destruida: Tahomen, Salas y Avissa muertos) |
| **Pactos Secretos** | Ninguno | Sarcófago funerario de Eox asegurado | Sarcófago entregado al Embajador Nor; recompensa cobrada | Contrato con la Decana Muhali (2.500 cr.); salvoconducto corsario de *La Venganza* | Rescate de Solstarni cumplido; telemetría del Devastador Estelar recuperada |
| **Misterio Cósmico** | Asesinato de Marlene Boosmar | Anomalía dimensional de la Roca del Drift; enigma de Syd Velch | Revelación de la baliza hacia el **Degenerador Estelar** | Relación de la esfera con Aucturn, portales de Aiakos y Dinastía Osuwak | Confirmado: la Roca del Drift es la llave de control; coordenadas apuntan a **La Diáspora** |
| **Posición Actual** | Salida de la Estación Absalón | Umbral exterior de la Roca del Drift | Héroes aclamados en Absalón listos para viajar al Vasto | Internándose en la selva prohibida de Ukulam hacia la Cordillera Cantante | Retornando de Ukulam a la *Estrella Errante* para zarpar rumbo a La Diáspora |"""

text = text.replace(tabla_old, tabla_new)

with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("CONTEXTO_COMPLETO_SAGA.md successfully updated with Volume 5!")
