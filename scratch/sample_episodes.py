import re

def summarize_ep(ep):
    fname = f"volumen_6/transcripciones/limpias/episodio_{ep}.txt"
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()

    # Look for spoken cues or speaker names if any, or segments
    # Let's search for interesting character names with case insensitivity and surrounding context
    names = ["solstarni", "salas", "jabaxa", "hess", "twonas", "twonás", "gevalarsk", "nor", "triel", "joss", "marcelus", "axel", "willy", "naru", "tahomen", "devastador"]
    matches = {}
    for n in names:
        m = list(re.finditer(r'\b' + n + r'\b', text, re.IGNORECASE))
        if m:
            matches[n] = len(m)
            
    print(f"=== EPISODIO {ep} ({len(text)} chars) ===")
    print(f"Keywords: {matches}")
    
    # Let's extract 5 interesting chunks from across the episode:
    # 10%, 25%, 50%, 75%, 90%
    for pct in [10, 25, 50, 75, 90]:
        idx = int(len(text) * (pct / 100))
        snippet = text[idx:idx+400]
        # clean snippet
        snippet = " ".join(snippet.split())
        print(f"[{pct}%]: {snippet}")
    print("\n" + "="*50 + "\n")

for ep in range(60, 73):
    summarize_ep(ep)
