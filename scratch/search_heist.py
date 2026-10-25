import re

def search_ep(ep, terms):
    fname = f"volumen_6/transcripciones/limpias/episodio_{ep}.txt"
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"\n================ EPISODIO {ep} ================")
    for t in terms:
        matches = [m.start() for m in re.finditer(re.escape(t), text, re.IGNORECASE)]
        print(f"Term '{t}': {len(matches)} matches")
        for pos in matches[:4]:
            snip = text[max(0, pos-120):min(len(text), pos+200)].replace('\n', ' ')
            print(f"   [{pos}]: {' '.join(snip.split())}")

search_ep(67, ["primo", "sobrino", "bumba", "marcelus", "joss", "contrato"])
search_ep(68, ["bumba", "marcelus", "joss", "disfraz", "edificio", "seguridad"])
search_ep(69, ["bumba", "piano", "robot", "oficina"])
search_ep(70, ["bumba", "joss", "escritorio", "computadora", "caja fuerte"])
search_ep(71, ["bumba", "marcelus", "salto", "escape", "policía", "humo"])
search_ep(72, ["marcelus", "ia", "conciencia", "voz", "nave", "willy"])
