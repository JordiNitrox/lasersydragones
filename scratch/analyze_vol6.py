import json
import re
import os

episodes = range(60, 73)

for ep in episodes:
    fname = f"volumen_6/transcripciones/limpias/episodio_{ep}.txt"
    if not os.path.exists(fname):
        print(f"Episodio {ep} not found!")
        continue
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"\n==========================================")
    print(f"=== EPISODIO {ep} (Total chars: {len(text)}) ===")
    print(f"==========================================")
    
    # Check mentions of characters
    chars = ["Marloc", "Benrey", "Darv", "Twonás", "Twonas", "Triel", "Willy", "Naru", "Solstarni", "Salas", "Tahomen", "Nor", "Gevalarsk", "Joss", "Marcelus", "Venture", "Chula", "Hess", "Jabaxa"]
    found = {c: len(re.findall(r'\b' + re.escape(c) + r'\b', text, re.IGNORECASE)) for c in chars if re.findall(r'\b' + re.escape(c) + r'\b', text, re.IGNORECASE)}
    print(f"Menciones de personajes: {found}")

    # Look for keywords about locations, actions, foes
    keywords = ["templo", "selva", "jungla", "rio", "nave", "lancha", "pantano", "piratas", "legion", "legión", "cielofuego", "absalon", "ábsalon", "estación", "universidad", "eox", "embajador", "devorador", "puerta", "ordenador", "consola", "cámara", "fantasma", "diaspora", "diáspora"]
    kw_found = {k: len(re.findall(r'\b' + re.escape(k) + r'\b', text, re.IGNORECASE)) for k in keywords if re.findall(r'\b' + re.escape(k) + r'\b', text, re.IGNORECASE)}
    print(f"Palabras clave: {kw_found}")

    # Sample snippet from beginning, middle, and end
    print("--- INICIO ---")
    print(text[:300].strip())
    print("--- MEDIO ---")
    mid = len(text)//2
    print(text[mid:mid+300].strip())
    print("--- FINAL ---")
    print(text[-300:].strip())
