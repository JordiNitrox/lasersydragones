import re

def analyze_episode_full(ep):
    fname = f"volumen_6/transcripciones/limpias/episodio_{ep}.txt"
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"==================================================")
    print(f"ANÁLISIS PROFUNDO EPISODIO {ep} (Longitud: {len(text)})")
    print(f"==================================================")

    # Buscar nombres propios clave
    proper_names = set(re.findall(r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?', text))
    # Filtrar palabras comunes
    common = {"El", "La", "Los", "Las", "Un", "Una", "De", "En", "Por", "Para", "Con", "Sin", "Sobre", "Tras", "Y", "O", "Pero", "Si", "No", "Que", "Como", "Cuando", "Donde", "Este", "Esta", "Ese", "Esa", "Aquel", "Aquella", "Yo", "Tu", "Él", "Ella", "Nosotros", "Vosotros", "Ellos", "Usted", "Ustedes", "Bueno", "Bien", "Sí", "Claro", "Entonces", "Luego", "Después", "Ahora", "Aquí", "Ahí", "Allí", "Al", "Del", "Muy", "Más", "Menos", "Mucho", "Poco", "Todo", "Nada", "Algo", "Alguien", "Nadie"}
    filtered_names = [n for n in proper_names if n not in common and len(n) > 2]
    
    # Contar frecuencias de los nombres filtrados
    counts = {}
    for n in filtered_names:
        c = len(re.findall(r'\b' + re.escape(n) + r'\b', text, re.IGNORECASE))
        if c >= 5:
            counts[n] = c
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:25]
    print("Nombres más frecuentes:")
    for n, c in sorted_counts:
        print(f"  - {n}: {c}")

    # Buscar eventos o temas clave buscando patrones
    # Dividir el texto en 4 cuartos y mostrar el inicio de cada cuarto
    quarter = len(text) // 4
    for i in range(4):
        pos = i * quarter
        chunk = text[pos:pos+350].replace('\n', ' ')
        print(f"\n[Sección {i+1}/4 - pos {pos}]:\n{chunk}")
    print("\n")

for ep in range(60, 73):
    analyze_episode_full(ep)
