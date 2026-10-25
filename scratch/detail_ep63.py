with open("volumen_6/transcripciones/limpias/episodio_63.txt") as f:
    t63 = f.read()

import re
print("=== EP 63: LOS CHOCOPIRATAS ===")
for m in re.finditer(r'(motor|chocopirata|sabor|bonet|legión|cielofuego|fuego|nave|lancha|campamento)', t63, re.I):
    pos = m.start()
    print(f"[{m.group()}]: {' '.join(t63[pos-60:pos+150].split())}")
    if pos > 25000:
        break
