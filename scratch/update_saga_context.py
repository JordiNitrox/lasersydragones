import re

context_file = "Contexto completo/CONTEXTO_COMPLETO_SAGA.md"
with open(context_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Cronología (insert Volumen 6 after Volumen 5)
vol6_chrono = """
### Volumen 6: *El Fantasma en la Máquina* (Episodios 60 al 72)
* **Arco Narrativo:** La Evasión de Ukulam, el Golpe Corporativo a Extracciones Astrales y el Despertar de la Estrella Errante.
* **Escenario Principal:** El río crecido y los pantanos de Ukulam (Castrovel), seguidos por el Ojo, el sector diplomático y el rascacielos blindado de Extracciones Astrales en la Estación Ábsalon, concluyendo en el Muelle 22 y el salto al Drift hacia La Diáspora.
* **Sinopsis Argumental:**
  1. *El Vado y el Campin (Ep. 60–61):* Tras la caída de Tahomen, la expedición desciende de la Cordillera Cantante bajo un diluvio implacable. En el río crecido sufren la emboscada del Campin —una aberración anfibia de mente bífida dividida en un coloso submarino y un enjambre de sanguijuelas alucinantes—. Axel, Triel y Gerty combaten en los rápidos mientras Marloc congela el agua y rescatan a la doctora Solstarni tras resbalar en las rocas.
  2. *Los Corsarios de La Furia y el Motor del Sabor (Ep. 62–64):* Desorientados por las toxinas alucinógenas y el lodo, el grupo encañona y luego pacta con el Capitán De Bonet y sus piratas de los Capitanes Libres. El reactor de su nave *La Furia* está averiado; cuando una cápsula orbital lanza el repuesto («el Motor del Sabor»), ocho cápsulas de asalto pesado de la Legión del Cielofuego caen tras ella debido al contrabando militar que transportaban. Durante doce horas, Triel, Axel, Marloc y Benray tienden trampas químicas, señuelos acústicos e interferencias de radar junto a la francotiradora Ila, permitiendo a los piratas reparar la nave y evacuar al equipo hacia Qabarat.
  3. *El Secreto de Axel y la Fotografía (Ep. 65):* En Qabarat, la doctora Solstarni se despide prometiendo confidencialidad. A bordo de la *Estrella Errante*, Axel recibe un mensaje anónimo que la lleva a examinar una fotografía en la Avenida 41 de Ábsalon: descubre con sobrecogimiento que su chasis fue habitado por otra alma consciente antes de su renovación en el Templo de Triuno, un secreto guardado por Claire y Null-9. Sus compañeros reafirman su identidad genuina.
  4. *Audiencia con Gevalarsk Nor (Ep. 66):* De regreso a la Estación Ábsalon, el grupo rinde cuentas ante el Embajador Gevalarsk Nor y Cheesecake en la embajada de Eox. El diplomático los recompensa financieramente y autoriza una expedición encubierta hacia La Diáspora para interceptar el Devastador Estelar antes que el Culto del Devorador.
  5. *El Asalto a la Torre Prisma (Ep. 67–71):* Triel es contactada por su primo Bumak Istrav, ejecutor y asesino corporativo de la Casa Istrav de Apostae. Bumak los contrata para un golpe negro contra la Torre Prisma de Extracciones Astrales, buscando arrebatar los registros clasificados de la señorita Joss. Marloc se suma para vengar a Marlene Boosmar, mientras Benray busca pistas sobre su antiguo productor Marcelus. El grupo se infiltra de noche, desatando un tiroteo con armas automáticas en el salón del piano de cola contra guardias y autómatas pesados. En el despacho privado, la señorita Joss los recibe a tiros de fusil de asalto militar; Axel la abate, Triel y Marloc revientan la caja fuerte y saquean los discos duros. El equipo escapa saltando desde el piso 28 en alas de planeo sobre la noche de Ábsalon.
  6. *El Fantasma en la Máquina y Partida (Ep. 72):* Benray y sus compañeros acorralan al supuesto Marcelus en el Muelle 22, descubriendo que es Bordin, un actor alienígena con modulador de voz; el verdadero Marcelus opera desde una fortaleza en un asteroide de La Diáspora cerca de Eox. De vuelta en la nave, Triel y Marloc integran el procesador militar recuperado en el reactor: las luces se apagan y una voz consciente y melancólica despierta en los circuitos de la *Estrella Errante*, reconociendo el nombre de Benray. La tripulación despega hacia el Drift, rumbo al cinturón de asteroides.
"""

# Insert vol6_chrono after Volumen 5 in section 1
pos_vol5 = content.find("### Volumen 5: *El Templo de los Doce Soles*")
if pos_vol5 != -1:
    pos_sec2 = content.find("## 2. Dossier Biográfico Integral", pos_vol5)
    content = content[:pos_sec2] + vol6_chrono + "\n---\n\n" + content[pos_sec2:]

# 2. Add Bestiario for Vol 6 before Section 6
bestiario_vol6 = """
### El Campin (Aberración Anfibia Bífida de Ukulam)
*Aparición en volúmenes:* **Volumen 6**  
Monstruo acuático milenario de los ríos de Ukulam dotado de dos cuerpos interconectados neurológicamente: un coloso acorazado de cartílago fosilizado con hendiduras sensoriales y fauces con ganchos, y un enjambre de miles de sanguijuelas púrpuras fosforescentes con secreciones neurotóxicas alucinógenas.

### Autómatas Corporativos de Asalto Pesado
*Aparición en volúmenes:* **Volumen 6**  
Mecas bípedos de seguridad privada desplegados en la planta ejecutiva de Extracciones Astrales, equipados con cañones rotatorios de plasma, visión térmica y blindajes capaces de resistir colisiones estructurales.

"""
pos_sec6 = content.find("## 6. Matriz de Continuidad")
if pos_sec6 != -1:
    content = content[:pos_sec6] + bestiario_vol6 + "\n" + content[pos_sec6:]

# 3. Update Matriz de Continuidad table to include column for Volumen 6
# Replace table header and rows
old_header = "| Parámetro | Volumen 1 (*Sombras sobre Absalón*) | Volumen 2 (*El Misterio del Acreon*) | Volumen 3 (*La Roca del Drift*) | Volumen 4 (*Las Torres de Qabarat*) | Volumen 5 (*El Templo de los Doce Soles*) |"
new_header = "| Parámetro | Volumen 1 (*Sombras sobre Absalón*) | Volumen 2 (*El Misterio del Acreon*) | Volumen 3 (*La Roca del Drift*) | Volumen 4 (*Las Torres de Qabarat*) | Volumen 5 (*El Templo de los Doce Soles*) | Volumen 6 (*El Fantasma en la Máquina*) |"

old_align = "|---|---|---|---|---|---|"
new_align = "|---|---|---|---|---|---|---|"

content = content.replace(old_header, new_header).replace(old_align, new_align)

rows_replacements = [
    (
        "| **Naves Activas** | Ninguna (tránsito en motoneta y muelles) | **Hippocampus** (*El Caballito de Mar*) | **Estrella Errante** (*Vagabond*) y **Hippocampus** | **Estrella Errante** (órbita de Castrovel) / Compacto de alquiler de Sophie | **Estrella Errante** (órbita de Castrovel, lista para salto a La Diáspora) |",
        "| **Naves Activas** | Ninguna (tránsito en motoneta y muelles) | **Hippocampus** (*El Caballito de Mar*) | **Estrella Errante** (*Vagabond*) y **Hippocampus** | **Estrella Errante** (órbita de Castrovel) / Compacto de alquiler de Sophie | **Estrella Errante** (órbita de Castrovel, lista para salto a La Diáspora) | **Estrella Errante** (dotada de procesador militar cuántico y conciencia viva) / *La Furia* (aliada) |"
    ),
    (
        "| **Cuartel / Base** | Cuartuchos de alquiler en el Anillo 9 | A bordo del *Hippocampus* | Muelle 94 / Sede Inversiones Estelares / Terraza *Las Lunas* | Campus Universidad de Qabarat / Puesto de Turhalu (Ukulam) | Vivac de campaña en Ukulam / Templo de los Doce Soles |",
        "| **Cuartel / Base** | Cuartuchos de alquiler en el Anillo 9 | A bordo del *Hippocampus* | Muelle 94 / Sede Inversiones Estelares / Terraza *Las Lunas* | Campus Universidad de Qabarat / Puesto de Turhalu (Ukulam) | Vivac de campaña en Ukulam / Templo de los Doce Soles | Café *Las Lunas* / Muelle 22 / A bordo de la *Estrella Errante* en el Drift |"
    ),
    (
        "| **Armamento de Gerty** | Cañón láser frontal, dos brazos pesados | Cuatro brazos (añadidos manipuladores finos) | Cuatro brazos reforzados + cañón láser pesado | Cuatro brazos pesados + pica de choque y cañón láser | Cuatro brazos reforzados + pica de alta frecuencia, ametralladora pesada y escudos |",
        "| **Armamento de Gerty** | Cañón láser frontal, dos brazos pesados | Cuatro brazos (añadidos manipuladores finos) | Cuatro brazos reforzados + cañón láser pesado | Cuatro brazos pesados + pica de choque y cañón láser | Cuatro brazos reforzados + pica de alta frecuencia, ametralladora pesada y escudos | Cuatro brazos pesados + pica de choque cuántica, ametralladora rotatoria y servos optimizados |"
    ),
    (
        "| **Aliados a Bordo** | Ninguno (solo los 4 fundadores + Gerty) | Se unen los goblins **Willy** y **Naru** | Willy y Naru (ciudadanos de honor y protegidos de Eox) | Willy y Naru (en órbita); Sophie Ren (Qabarat); Dr. Kaeral (Turhalu) | Willy y Naru (en órbita); **Doctora Omejia Solstarni** (rescatada); Dr. Kaeral |",
        "| **Aliados a Bordo** | Ninguno (solo los 4 fundadores + Gerty) | Se unen los goblins **Willy** y **Naru** | Willy y Naru (ciudadanos de honor y protegidos de Eox) | Willy y Naru (en órbita); Sophie Ren (Qabarat); Dr. Kaeral (Turhalu) | Willy y Naru (en órbita); **Doctora Omejia Solstarni** (rescatada); Dr. Kaeral | Willy y Naru; **La Conciencia de la Nave**; Bumak Istrav (enlace en Ábsalon); Capitán De Bonet e Ila |"
    ),
    (
        "| **Contactos / Red** | **Null-9** (Club 13), Chic, Rim Rey | Rim Rey, Embajador Nor | **Null-9** (red androide), Rim Rey, Embajador Nor, Chiskisk | **Null-9**, Oficial León (token prioritario), Decana Muhali, Casonas y Thiable | **Null-9**, Oficial León, Decana Muhali, claustro de la Universidad de Qabarat |",
        "| **Contactos / Red** | **Null-9** (Club 13), Chic, Rim Rey | Rim Rey, Embajador Nor | **Null-9** (red androide), Rim Rey, Embajador Nor, Chiskisk | **Null-9**, Oficial León (token prioritario), Decana Muhali, Casonas y Thiable | **Null-9**, Oficial León, Decana Muhali, claustro de la Universidad de Qabarat | **Bumak Istrav** (Casa Istrav), Embajador Gevalarsk Nor, Cheesecake, Capitán De Bonet, Templo de Triuno |"
    ),
    (
        "| **Vínculos Afectivos** | Cohesión fraternal inicial en combate | Creciente atracción entre **Axel 42** y el **Oficial León** | Romance formalizado entre **Axel 42** y el **Oficial León** | Axel y León se despiden con token cuántico; Triel revela a Cayden Aston | Triel supera trauma de Oshiga; Benray reconciliado con su pasado; Axel asume Unidad 42 |",
        "| **Vínculos Afectivos** | Cohesión fraternal inicial en combate | Creciente atracción entre **Axel 42** y el **Oficial León** | Romance formalizado entre **Axel 42** y el **Oficial León** | Axel y León se despiden con token cuántico; Triel revela a Cayden Aston | Triel supera trauma de Oshiga; Benray reconciliado con su pasado; Axel asume Unidad 42 | Axel asimila la verdad de su chasis previo; Triel reconciliada con la rama leal de su familia; Benray encuentra su voz de capitán |"
    ),
    (
        "| **Facciones Rivales** | Reyes del Nivel 21 (destruidos) | Extracciones Estelares (vía letrado Kaerom) | Extracciones Estelares (derrotada) y **Flota de los Cuerpos** | Legión del Fuego en el Cielo, mercenarios de Eroopa Cual y el cazador Salas | **Culto del Devorador** (célula de Castrovel destruida: Tahomen, Salas y Avissa muertos) |",
        "| **Facciones Rivales** | Reyes del Nivel 21 (destruidos) | Extracciones Estelares (vía letrado Kaerom) | Extracciones Estelares (derrotada) y **Flota de los Cuerpos** | Legión del Fuego en el Cielo, mercenarios de Eroopa Cual y el cazador Salas | **Culto del Devorador** (célula de Castrovel destruida: Tahomen, Salas y Avissa muertos) | **Extracciones Astrales** (Señorita Joss neutralizada; archivos expuestos) y Legión del Cielofuego (burlada) |"
    ),
    (
        "| **Pactos Secretos** | Ninguno | Sarcófago funerario de Eox asegurado | Sarcófago entregado al Embajador Nor; recompensa cobrada | Contrato con la Decana Muhali (2.500 cr.); salvoconducto corsario de *La Venganza* | Rescate de Solstarni cumplido; telemetría del Devastador Estelar recuperada |",
        "| **Pactos Secretos** | Ninguno | Sarcófago funerario de Eox asegurado | Sarcófago entregado al Embajador Nor; recompensa cobrada | Contrato con la Decana Muhali (2.500 cr.); salvoconducto corsario de *La Venganza* | Rescate de Solstarni cumplido; telemetría del Devastador Estelar recuperada | Alianza encubierta con Embajador Nor (fondos y salvoconducto); pacto de sangre con Bumak Istrav |"
    ),
    (
        "| **Misterio Cósmico** | Asesinato de Marlene Boosmar | Anomalía dimensional de la Roca del Drift; enigma de Syd Velch | Revelación de la baliza hacia el **Degenerador Estelar** | Relación de la esfera con Aucturn, portales de Aiakos y Dinastía Osuwak | Confirmado: la Roca del Drift es la llave de control; coordenadas apuntan a **La Diáspora** |",
        "| **Misterio Cósmico** | Asesinato de Marlene Boosmar | Anomalía dimensional de la Roca del Drift; enigma de Syd Velch | Revelación de la baliza hacia el **Degenerador Estelar** | Relación de la esfera con Aucturn, portales de Aiakos y Dinastía Osuwak | Confirmado: la Roca del Drift es la llave de control; coordenadas apuntan a **La Diáspora** | El alma previa de Axel en la Avenida 41; el traslado de conciencia en la nave; Marcelus oculto en el asteroide de La Diáspora |"
    ),
    (
        "| **Posición Actual** | Salida de la Estación Absalón | Umbral exterior de la Roca del Drift | Héroes aclamados en Absalón listos para viajar al Vasto | Internándose en la selva prohibida de Ukulam hacia la Cordillera Cantante | Retornando de Ukulam a la *Estrella Errante* para zarpar rumbo a La Diáspora |",
        "| **Posición Actual** | Salida de la Estación Absalón | Umbral exterior de la Roca del Drift | Héroes aclamados en Absalón listos para viajar al Vasto | Internándose en la selva prohibida de Ukulam hacia la Cordillera Cantante | Retornando de Ukulam a la *Estrella Errante* para zarpar rumbo a La Diáspora | Navegando por el Drift a bordo de la *Estrella Errante* con rumbo fijo al cinturón de La Diáspora |"
    )
]

for old_row, new_row in rows_replacements:
    content = content.replace(old_row, new_row)

with open(context_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Contexto actualizado exitosamente con Volumen 6.")
