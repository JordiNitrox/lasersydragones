# Protocolo de Auditoría de Fidelidad Narrativa
## Guía de Verificación Dramática y Fidelidad a la Mesa
### Saga *Lasers y Dragones* (Campaña Starfinder: Dead Suns)

Este documento define el protocolo preceptivo de **control de calidad narrativo** previo a la maquetación de cualquier volumen. Su objetivo es garantizar que la transformación literaria enriquezca la prosa sin inventar tramas espurias, sin suplantar las decisiones de los jugadores y sin anticipar revelaciones fuera de tiempo.

---

## 1. El Doble Filtro de Calidad del Proyecto

La producción editorial se divide en dos auditorías independientes:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. AUDITORÍA NARRATIVA (AUDITORIA_DE_FIDELIDAD.md)          │
│    Fidelidad a las sesiones, agencia, voces y spoilers      │
├─────────────────────────────────────────────────────────────┤
│ 2. AUDITORÍA EDITORIAL Y PDF (Skill: lasers-maquetacion-pdf)│
│    Geometría A4, LibreOffice, marcadores, índice y páginas  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Los Ocho Puntos de Control Narrativo

Todo capítulo o volumen debe superar satisfactoriamente estos ocho controles:

### Control 1: Fidelidad Fáctica a las Sesiones
* **Pregunta:** ¿Todos los acontecimientos nucleares proceden del audio de la partida real?
* **Criterio:** La novela puede añadir descripciones sensoriales, reflexiones íntimas y transiciones escénicas fluidas, pero **JAMÁS inventar tramas principales, combates inexistentes o muertes que no ocurrieron en la mesa**.
* **Evidencia:** Toda escena mayor debe poder localizarse en `transcripciones/limpias/` mediante su correspondiente marca de tiempo.

### Control 2: Respeto Absoluto a la Agencia de los Jugadores
* **Pregunta:** ¿Se han respetado las iniciativas, ocurrencias tácticas y elecciones de los jugadores?
* **Criterio:** Si los jugadores idearon un farol ingenioso (ej. Triel haciéndose pasar por la despótica «Señorita Istrav» en el Club Con-Fusión), la novela debe reflejar exactamente esa treta y no una resolución heroica genérica ajena a lo jugado.
* **Traducción de Tiradas:** Un *20 natural* se describe como un golpe de genialidad o suerte táctica; una *pifia (1 natural)* se narra como falla mecánica, sobrecalentamiento o resbalón por condensación, preservando el desenlace cómico o trágico de la mesa.

### Control 3: Barrera Temporal de Revelaciones (*Anti-Spoilers*)
* **Pregunta:** ¿El texto contiene algún dato, actitud o sospecha que pertenezca a episodios posteriores?
* **Criterio:** Es obligatorio contrastar el borrador con la tabla de [CRONOLOGIA_Y_REVELACIONES.md](./CRONOLOGIA_Y_REVELACIONES.md).
* **Ejemplos de Fugas Inadmisibles:**
  * Insinuar atracción o romance entre Triel y León en los Volúmenes 1 o 2.
  * Mencionar a Clara-247 antes del Volumen 3.
  * Anticipar la duplicidad de Marcellus antes del Volumen 6.

### Control 4: Distinción entre Conjeturas de PNJs y Hechos Canónicos
* **Pregunta:** ¿Las hipótesis infundadas formuladas por los PNJs se narran como conjeturas subjetivas o como verdades absolutas?
* **Criterio:** Si un PNJ formula una deducción precipitada (como Chic presumiendo en el Club 13 que Marloc es el hermano de Marlene), la narración debe evidenciar que se trata de una conclusión errónea del PNJ y reflejar la perplejidad y negativa del protagonista.

### Control 5: Consistencia de Voces y Psicología de los Protagonistas
* **Pregunta:** ¿Los cinco personajes centrales hablan y actúan de acuerdo con su psicología canónica?
  * **Benrey Galway:** Verborrea acelerada, pícaro callejero, paranoico compulsivo respecto a ser envenenado (analiza comida ajena) y pánico visceral a Eox y a los no-muertos.
  * **Triel Istrav:** Mecánica independiente pragmática, leal, protectora de Gerty, marcada por el desprecio aristocrático de Apostae y anhelante de encontrar a su padre humano **Keiden Ashton**.
  * **Gerty:** Sintetizador vocal cavernoso y plano; desprecio cómico hacia los «bichos de carbono»; chiste recurrente de reinicios lentos estilo *Windows 95* en momentos de tensión.
  * **Marloc Boosmar:** Tecnomante distinguido, amnésico tras tocar la esfera dorada, con brazo cibernético; atrapado en el dolor dimensional al ver a la viuda Ángela.
  * **A.Xel 42:** Androide analítica, silenciosa y letal; circuitos bioluminiscentes rosados y ojos multiespectrales; terror paralizante a volver a caer en la esclavitud.

### Control 6: Equilibrio de Ritmo y Extensión de Capítulos
* **Pregunta:** ¿La extensión de los capítulos se mantiene en la horquilla de balance literario?
* **Horquilla Recomendada:** Entre **1.500 y 3.500 palabras** por capítulo.
* **Criterio de Alerta:**
  * Si un capítulo queda por debajo de **1.200 palabras**, evaluar si requiere mayor desarrollo ambiental o fusión de escenas breves.
  * Si un capítulo supera las **4.500 palabras**, evaluar si debe dividirse en dos partes (ej. *Parte I* y *Parte II*) para mantener la cadencia ágil de lectura, salvo que constituya el gran clímax unificado del volumen.

### Control 7: Inmersión Diegética y Barrido Anti-Alucinaciones STT
* **Comprobación Automatizada Obligatoria:**
  1. *Cero nombres de jugadores en prosa:*
     ```bash
     grep -rnEi "\b(Roberto|Juan Pablo|Juanpa|Sofía|Sofia|Irene|Miguel)\b" novela/capitulos/*.md --exclude="00_nota_editorial.md"
     ```
     *(Debe dar 0 coincidencias en la narrativa).*
  2. *Cero términos de alucinación STT o manual de Paizo:*
     ```bash
     grep -rnEi "\b(piedra del triunfo|roca del triunfo|Ring Rey|Ferani Krane|Sociedad Starfinder|Duravor Kreel)\b" novela/capitulos/*.md
     ```
     *(Debe dar 0 coincidencias).*

### Control 8: Presencia y Calidad del Prólogo Narrativo
* **Pregunta:** ¿Cuenta el volumen con un `00_prologo.md` que funcione como puente dramático y sensorial?
* **Criterio:** Todo volumen debe incluir preceptivamente un archivo de prólogo que enlace orgánicamente con el desenlace del volumen anterior, recapitulando el estado psicológico, físico y táctico de los protagonistas y anticipando el conflicto inmediato sin vulnerar la barrera temporal anti-spoilers.
* **Inmersión y Formato:** Debe cumplir estrictamente la regla de oro diegética (cero nombres de jugadores en prosa, cero jerga de mesa), titularse `# Prólogo: {Subtítulo Temático}` y ubicarse en la página 4 física del PDF (inmediatamente después del Índice de Contenidos en la página 3).

---

## 3. Plantilla de Informe de Auditoría Narrativa

Al auditar un volumen, registrar el resultado en `soles_muertos/volumen_X/metadatos/AUDITORIA_NARRATIVA_VOLUMEN_X.md`:

```markdown
# Auditoría Narrativa: Volumen X
**Fecha de Revisión:** AAAA-MM-DD  
**Revisor:** Agente / Editor  
**Episodios Contrastados:** Ep. XX al Ep. YY  

| Control | Estado | Observaciones / Acciones Tomadas |
|---|---|---|
| 1. Fidelidad Fáctica | [CONFORME / CORREGIDO] | Acontecimientos alineados con las sesiones originales. |
| 2. Agencia de Jugadores | [CONFORME / CORREGIDO] | Ocurrencias y tiradas de mesa respetadas fielmente. |
| 3. Barrera de Spoilers | [CONFORME / CORREGIDO] | Ninguna revelación futura filtrada en el texto. |
| 4. Conjeturas de PNJs | [CONFORME / CORREGIDO] | Teorías erróneas tratadas como deducciones subjetivas. |
| 5. Consistencia de Voces | [CONFORME / CORREGIDO] | Voces de Benrey, Triel, Gerty, Marloc y A.Xel afinadas. |
| 6. Extensión y Ritmo | [CONFORME / CORREGIDO] | Horquilla de palabras equilibrada por capítulo. |
| 7. Inmersión Diegética | [CONFORME / CORREGIDO] | Cero fugas de nombres de jugadores ni jerga de rol. |
| 8. Prólogo Narrativo | [CONFORME / CORREGIDO] | Presencia y calidad de 00_prologo.md como puente orgánico entre volúmenes. |
```
```
