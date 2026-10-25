with open("volumen_6/transcripciones/limpias/episodio_61.txt") as f:
    t61 = f.read()

import re
print("=== EP 61: SANGUIJUELAS Y COMBATE ===")
for m in re.finditer(r'(sanguijuela|río|iniciativa|ataque|morder|alucin|piedra|criatura)', t61, re.I):
    pos = m.start()
    print(f"[{m.group()}]: {' '.join(t61[pos-60:pos+150].split())}")
    if pos > 20000:
        break
