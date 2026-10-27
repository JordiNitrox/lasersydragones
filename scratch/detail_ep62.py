with open("volumen_6/transcripciones/limpias/episodio_62.txt") as f:
    t62 = f.read()

import re
print("=== EP 62: UKULAM STANDOFF ===")
for m in re.finditer(r'(dispar|standoff|locura|lluvia|solstarni|benrey|marloc|axel|triel|alucin|sanguijuela)', t62, re.I):
    pos = m.start()
    print(f"[{m.group()}]: {' '.join(t62[pos-60:pos+150].split())}")
    if pos > 20000:
        break
