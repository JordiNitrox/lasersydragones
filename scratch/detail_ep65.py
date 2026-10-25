with open("volumen_6/transcripciones/limpias/episodio_65.txt") as f:
    t65 = f.read()

import re
print("=== EP 65: FOTO Y MENSAJE ===")
for m in re.finditer(r'(foto|mensaje|video|salas|benray|claire|archivo|qabarat)', t65, re.I):
    pos = m.start()
    print(f"[{m.group()}]: {' '.join(t65[pos-60:pos+160].split())}")
    if pos > 30000:
        break
