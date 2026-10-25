with open("volumen_6/transcripciones/limpias/episodio_66.txt") as f:
    t66 = f.read()

import re
print("=== EP 66: EMBAJADOR GEVALARSK NOR ===")
for m in re.finditer(r'(embajador|nor|gevalarsk|eox|diáspora|culto|devorador|absalon|ábsalon)', t66, re.I):
    pos = m.start()
    print(f"[{m.group()}]: {' '.join(t66[pos-60:pos+160].split())}")
    if pos > 25000:
        break
