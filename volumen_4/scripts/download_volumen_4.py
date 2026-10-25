#!/usr/bin/env python3
"""
Script de descarga y procesamiento para el Volumen 4 de 'Lasers y Dragones'
Campaña: Starfinder - Dead Suns (Episodios 34 al 45: Las Torres de Qabarat)
Descarga los subtítulos VTT de YouTube y genera las transcripciones limpias.
"""

import os
import sys
import json
import subprocess
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
RAW_DIR = os.path.join(BASE_DIR, "transcripciones", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "transcripciones", "limpias")
META_DIR = os.path.join(BASE_DIR, "metadatos")

CLEANER_SCRIPT = os.path.join(
    os.path.dirname(BASE_DIR),
    ".agents", "skills", "novelizacion-lasers-y-dragones", "scripts", "limpiar_transcripcion.py"
)

META_FILE = os.path.join(META_DIR, "episodios_volumen_4.json")
with open(META_FILE, "r", encoding="utf-8") as f:
    EPISODIOS = json.load(f)

def descargar_subtitulos():
    print("=== DESCARGANDO SUBTÍTULOS DE YOUTUBE (EPISODIOS 34 AL 45) ===")
    os.makedirs(RAW_DIR, exist_ok=True)
    
    for ep in EPISODIOS:
        num = ep["numero"]
        yt_id = ep["youtube_id"]
        salida_patron = os.path.join(RAW_DIR, f"episodio_{num:02d}.%(ext)s")
        target_vtt = os.path.join(RAW_DIR, f"episodio_{num:02d}.es.vtt")
        
        if os.path.exists(target_vtt):
            print(f"Subtítulo ya descargado: Ep {num} ({os.path.basename(target_vtt)})")
            continue
            
        print(f"Descargando subtítulos: Ep {num} - {ep['titulo']} (ID: {yt_id})...")
        cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "es",
            "--skip-download",
            "--no-warnings",
            "-o", salida_patron,
            f"https://www.youtube.com/watch?v={yt_id}"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            print(f"  ✓ Subtítulo obtenido con éxito para Ep {num}")
        else:
            print(f"  ✗ Error descargando subtítulo para Ep {num}: {res.stderr}")

def limpiar_transcripciones():
    print("\n=== LIMPIANDO TRANSCRIPCIONES (VTT -> TEXTO CORRIDO) ===")
    os.makedirs(CLEAN_DIR, exist_ok=True)
    
    sys.path.insert(0, os.path.dirname(CLEANER_SCRIPT))
    from limpiar_transcripcion import limpiar_vtt
    
    for ep in EPISODIOS:
        num = ep["numero"]
        vtt_file = os.path.join(RAW_DIR, f"episodio_{num:02d}.es.vtt")
        clean_file = os.path.join(CLEAN_DIR, f"episodio_{num:02d}.txt")
        
        if not os.path.exists(vtt_file):
            print(f"Aviso: No se encontró archivo VTT para el Ep {num}")
            continue
            
        print(f"Limpiando transcripción: Ep {num} ({ep['titulo']})...")
        limpiar_vtt(vtt_file, clean_file)
        if os.path.exists(clean_file):
            with open(clean_file, "r", encoding="utf-8") as f:
                content = f.read()
            words = len(content.split())
            print(f"  ✓ Archivo limpio generado: {os.path.basename(clean_file)} ({words:,} palabras)")

def main():
    descargar_subtitulos()
    limpiar_transcripciones()
    print("\n=== PROCESO COMPLETADO PARA VOLUMEN 4 ===")

if __name__ == "__main__":
    main()
