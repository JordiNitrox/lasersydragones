import re

def analyze_all():
    with open("scratch/vol6_breakdown.txt", "w", encoding="utf-8") as out:
        for ep in range(60, 73):
            fname = f"volumen_6/transcripciones/limpias/episodio_{ep}.txt"
            with open(fname, "r", encoding="utf-8") as f:
                raw = f.read()

            out.write(f"\n{'='*60}\n")
            out.write(f"EPISODIO {ep} - Tamaño: {len(raw)} caracteres\n")
            out.write(f"{'='*60}\n")

            # Buscar menciones clave en minúsculas
            terms = [
                "solstarni", "salas", "tahomen", "avissa", "khasari", "yaruk", "turhalu", 
                "jabaxa", "hess", "twonas", "twonás", "chula", "lancha", "pantano", "río",
                "legion", "legión", "cielofuego", "skyfire", "qabarat", "absalon", "ábsalon",
                "gevalarsk", "nor", "eox", "extracciones", "inversiones", "joss", "chassi",
                "steel", "gerty", "claire", "triel", "benray", "marloc", "marlo", "axel",
                "devorador", "devastador", "diaspora", "diáspora", "willy", "naru",
                "fantasmeame", "marcelus", "computadora", "dron", "sanguijuelas"
            ]
            
            found_terms = {}
            for t in terms:
                cnt = len(re.findall(r'\b' + re.escape(t) + r'\b', raw, re.IGNORECASE))
                if cnt > 0:
                    found_terms[t] = cnt
            out.write(f"Términos encontrados: {found_terms}\n\n")

            # Extraer momentos donde el master (Roberto / DM) describe la escena o narración
            # En Lasers y Dragones, el DM a menudo dice "ustedes ven", "en este momento", "lo que pasa", "entonces", "cuando llegan", etc.
            # O podemos tomar fragmentos representativos cada 10% del episodio
            for i in range(10):
                pct = i * 10
                pos = int(len(raw) * (pct / 100))
                chunk = raw[pos:pos+500].replace('\n', ' ')
                chunk = ' '.join(chunk.split())
                out.write(f"[{pct}%]: {chunk}\n\n")

analyze_all()
print("Breakdown escrito en scratch/vol6_breakdown.txt")
