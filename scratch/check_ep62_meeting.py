with open("volumen_6/transcripciones/limpias/episodio_62.txt") as f:
    t62 = f.read()

import re
m = list(re.finditer(r'venimos de la estación', t62, re.I))
if m:
    pos = m[0].start()
    print(t62[pos-500:pos+1500])
