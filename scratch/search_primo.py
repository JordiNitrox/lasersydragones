with open("volumen_6/transcripciones/limpias/episodio_67.txt") as f:
    text67 = f.read()

import re
matches = [m.start() for m in re.finditer(r'primo', text67, re.IGNORECASE)]
print("=== EPISODIO 67: PRIMO ===")
for pos in matches[:5]:
    snip = text67[max(0, pos-100):min(len(text67), pos+200)].replace('\n', ' ')
    print(f"[{pos}]: {' '.join(snip.split())}")

with open("volumen_6/transcripciones/limpias/episodio_68.txt") as f:
    text68 = f.read()

matches68 = [m.start() for m in re.finditer(r'primo', text68, re.IGNORECASE)]
print("\n=== EPISODIO 68: PRIMO ===")
for pos in matches68[:5]:
    snip = text68[max(0, pos-100):min(len(text68), pos+200)].replace('\n', ' ')
    print(f"[{pos}]: {' '.join(snip.split())}")
