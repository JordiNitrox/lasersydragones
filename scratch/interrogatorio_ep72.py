with open("volumen_6/transcripciones/limpias/episodio_72.txt") as f:
    text = f.read()

# Let's see from char 10000 to 18000
chunk = text[10000:18000]
print("=== EPISODIO 72: INTERROGATORIO ===")
print(chunk[:4000])
