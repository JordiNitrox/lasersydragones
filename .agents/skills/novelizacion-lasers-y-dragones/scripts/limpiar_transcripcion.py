#!/usr/bin/env python3
"""
Script utilitario para limpiar transcripciones de subtítulos VTT (YouTube)
o salidas de Whisper del podcast 'Lasers y Dragones'.

Elimina marcas temporales, etiquetas VTT, música, líneas repetitivas/acumulativas
y unifica el texto en párrafos limpios y legibles para el proceso de novelización.
"""

import sys
import os
import re

def limpiar_vtt(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"Error: No existe el archivo {input_path}")
        return False

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    clean_lines = []
    last_text = ""

    for line in lines:
        line = line.strip()
        # Ignorar metadatos de formato VTT
        if not line or "WEBVTT" in line or "Kind:" in line or "Language:" in line or "-->" in line:
            continue
        if line.startswith("align:") or line.startswith("position:"):
            continue
            
        # Eliminar etiquetas de tiempo internas como <00:00:29.269><c> ... </c>
        line = re.sub(r"<[^>]+>", "", line)
        line = line.strip()
        
        # Omitir acotaciones de música o texto idéntico consecutivo
        if line and line != last_text and line != "[Música]" and line != "[Risas]":
            clean_lines.append(line)
            last_text = line

    # Deduplicar líneas acumulativas típicas de subtítulos de YouTube
    deduped = []
    for text in clean_lines:
        if deduped and text.startswith(deduped[-1]):
            deduped[-1] = text
        elif deduped and deduped[-1].startswith(text):
            continue
        else:
            deduped.append(text)

    # Formatear en párrafos continuos
    full_text = " ".join(deduped)

    # Diccionario de correcciones fonéticas y de transcripción automática (STT)
    # Mitiga errores auditivos típicos de YouTube / Whisper en Starfinder / Lasers y Dragones
    CORRECCIONES_FONETICAS = [
        # La Roca del Drift / El Drift (STT suele oír "triunfo" o "deriva")
        (r"\b(la\s+)?piedra\s+del\s+triunfo\b", "la Roca del Drift"),
        (r"\b(la\s+)?piedra\s+del\s+[Dd]rift\b", "la Roca del Drift"),
        (r"\b(la\s+)?roca\s+del\s+triunfo\b", "la Roca del Drift"),
        (r"\b(el\s+)?motor\s+del\s+triunfo\b", "el motor del Drift"),
        (r"\b(el\s+)?viaje\s+por\s+el\s+triunfo\b", "el viaje por el Drift"),
        (r"\b(el\s+)?salto\s+al\s+triunfo\b", "el salto al Drift"),
        (r"\b(el\s+)?salto\s+del\s+triunfo\b", "el salto del Drift"),
        (r"\bhiperespacio\s+del\s+triunfo\b", "hiperespacio del Drift"),
        # Nombres de personajes secundarios
        (r"\bRing\s+Rey\b", "Rim Rey"),
        (r"\bRin\s+Rey\b", "Rim Rey"),
        (r"\bchischis\b", "Chiskisk"),
        (r"\bchischís\b", "Chiskisk"),
        (r"\bFerani\s+Krane\b", "Ferani Nadaz"),
        (r"\bFerani\s+Crane\b", "Ferani Nadaz"),
        (r"\bSunrise\s+Maiden\b", "Estrella Errante"),
        (r"\bKeltusa\b", "Keltus"),
        (r"\bque\s+el\s+t[uú]s\b", "Keltus"),
        (r"\bángel\s+tus\s+a\s+él\b", "Keltus"),
        (r"\bGevalnor\b", "Gevalarsk Nor"),
        (r"\bque\s+le\s+vasco\s+norma\b", "Gevalarsk Nor"),
        (r"\bque\s+elevarse\b", "Gevalarsk Nor"),
    ]

    reemplazos_hechos = 0
    for patron, reemplazo in CORRECCIONES_FONETICAS:
        nuevo_texto, n = re.subn(patron, reemplazo, full_text, flags=re.IGNORECASE)
        if n > 0:
            reemplazos_hechos += n
            full_text = nuevo_texto

    if reemplazos_hechos > 0:
        print(f"  [Aviso] Se aplicaron {reemplazos_hechos} correcciones fonéticas/STT automáticas.")
    
    # Separar en párrafos cada ~6-8 frases o pausas naturales para facilitar la lectura
    sentences = re.split(r'([.?!]\s+)', full_text)
    paragraphs = []
    current_p = []
    
    for i in range(0, len(sentences), 2):
        s = sentences[i]
        sep = sentences[i+1] if i+1 < len(sentences) else ""
        sentence = (s + sep).strip()
        if sentence:
            current_p.append(sentence)
            if len(current_p) >= 6:
                paragraphs.append(" ".join(current_p))
                current_p = []
                
    if current_p:
        paragraphs.append(" ".join(current_p))

    final_content = "\n\n".join(paragraphs)

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + "_limpio.txt"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    words = len(final_content.split())
    print(f"Transcripción limpia guardada en: {output_path}")
    print(f"Total de palabras: {words:,} palabras ({len(paragraphs)} párrafos)")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 limpiar_transcripcion.py <archivo.vtt> [archivo_salida.txt]")
        sys.exit(1)
    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    limpiar_vtt(in_file, out_file)
