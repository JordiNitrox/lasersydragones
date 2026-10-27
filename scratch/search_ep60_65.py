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

# Ep 60: Temple exit, Claire message, river
search_text(60, ["claire", "triuno", "río", "lancha", "pantano", "solstarni"])

# Ep 61: Sanguijuelas, alucinaciones
search_text(61, ["sanguijuela", "alucin", "río", "mord", "veneno", "árbol", "piedra"])

# Ep 62: Standoff, locura, lluvia
search_text(62, ["standoff", "dispar", "locura", "lluvia", "salas", "benrey", "axel", "triel", "marlo"])

# Ep 63: Piratas, lancha, legión, chocopiratas
search_text(63, ["chocopiratas", "motor del sabor", "jabaxa", "hess", "twonas", "lancha", "legión", "cielofuego"])

# Ep 64: Trampa, combate, escape
search_text(64, ["trampa", "soldado", "lancha", "escapar", "motor", "fuego", "bomba"])

# Ep 65: Vuelta, Qabarat, Absalom, foto, video
search_text(65, ["foto", "video", "salas", "benrey", "turhalu", "qabarat", "absalon", "nave"])
