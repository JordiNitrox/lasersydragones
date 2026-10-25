import re

def search_text(ep, queries):
    fname = f"volumen_6/transcripciones/limpias/episodio_{ep}.txt"
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"\n================ EPISODIO {ep} ================")
    for q in queries:
        matches = [m.start() for m in re.finditer(re.escape(q), text, re.IGNORECASE)]
        print(f"Query '{q}': {len(matches)} matches")
        for pos in matches[:3]:
            snippet = text[max(0, pos-150):min(len(text), pos+250)].replace('\n', ' ')
            snippet = ' '.join(snippet.split())
            print(f"  [{pos}]: ...{snippet}...")

# Ep 66: Nor, Absalom, Eox
search_text(66, ["embajador", "nor", "gevalarsk", "eox", "ábsalon", "absalon", "huesos", "diáspora"])

# Ep 67: Cousin, Triel, Astral Extractions, photo
search_text(67, ["primo", "sobrino", "triel", "extracciones", "salas", "foto", "video", "marcelus"])

# Ep 68: Infiltration plan, Ms. Joss, disguise
search_text(68, ["joss", "extracciones", "edificio", "oficina", "disfraz", "seguridad", "cámara"])

# Ep 69: Combat in building, piano, robot
search_text(69, ["piano", "robot", "soldado", "disparo", "subir", "ascensor", "oficina", "joss"])

# Ep 70: Hacking, vault, automatic rifle, books
search_text(70, ["caja fuerte", "computadora", "hack", "joss", "escritorio", "automático", "balas"])

# Ep 71: Escape, smoke, jump, police
search_text(71, ["humo", "granada", "balcón", "saltar", "policía", "escapar", "marcelus", "llamada"])

# Ep 72: Ship, ghost, machine, Diaspora, space
search_text(72, ["nave", "fantasma", "máquina", "diáspora", "willy", "naru", "computadora", "estrella"])
