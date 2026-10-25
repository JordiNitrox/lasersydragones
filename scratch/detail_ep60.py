with open("volumen_6/transcripciones/limpias/episodio_60.txt") as f:
    t60 = f.read()

# In Ep 60:
# Where do they go after defeating Tahomen in the Temple?
# They exit the temple with Dr. Solstarni.
# What happens with Claire / Triuno?
import re
print("=== EP 60: DETALLES ===")
for m in re.finditer(r'(templo|solstarni|claire|río|viaje|caminata|tormenta)', t60, re.I):
    pos = m.start()
    print(f"[{m.group()}]: {' '.join(t60[pos-60:pos+150].split())}")
    if pos > 35000:
        break
