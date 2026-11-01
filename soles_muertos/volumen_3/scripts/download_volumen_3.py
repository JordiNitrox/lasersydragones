#!/usr/bin/env python3
"""
Script de descarga y procesamiento para el Volumen 3 de 'Lasers y Dragones'
Campaña: Starfinder - Dead Suns (Episodios 23 al 33: El Arco de la Roca del Drift)
Descarga los audios oficiales de Libsyn, extrae los subtítulos VTT de YouTube y
genera las transcripciones limpias listas para la novelización.
"""

import os
import sys
import json
import subprocess
import urllib.request
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
RAW_DIR = os.path.join(BASE_DIR, "transcripciones", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "transcripciones", "limpias")
META_DIR = os.path.join(BASE_DIR, "metadatos")

CLEANER_SCRIPT = os.path.join(
    os.path.dirname(BASE_DIR),
    ".agents", "skills", "novelizacion-lasers-y-dragones", "scripts", "limpiar_transcripcion.py"
)

# Cargar lista de episodios desde metadatos
META_FILE = os.path.join(META_DIR, "episodios_volumen_3.json")
with open(META_FILE, "r", encoding="utf-8") as f:
    EPISODIOS = json.load(f)

def descargar_subtitulos():
    print("=== DESCARGANDO SUBTÍTULOS DE YOUTUBE (EPISODIOS 23 AL 33) ===")
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

def descargar_audios(descargar_ahora=False):
    print("\n=== GESTIÓN DE AUDIOS MP3 OFICIALES (LIBSYN) ===")
    os.makedirs(AUDIOS_DIR, exist_ok=True)
    
    for ep in EPISODIOS:
        num = ep["numero"]
        nombre_archivo = ep["archivo_audio"]
        ruta_archivo = os.path.join(AUDIOS_DIR, nombre_archivo)
        url_mp3 = ep["url_audio"]
        
        if os.path.exists(ruta_archivo) and os.path.getsize(ruta_archivo) > 1000000:
            size_mb = os.path.getsize(ruta_archivo) / (1024 * 1024)
            print(f"Audio ya disponible: {nombre_archivo} ({size_mb:.2f} MB)")
            continue
            
        if descargar_ahora:
            print(f"Descargando audio: {nombre_archivo} desde {url_mp3}...")
            req = urllib.request.Request(url_mp3, headers={"User-Agent": "Mozilla/5.0"})
            try:
                with urllib.request.urlopen(req) as resp, open(ruta_archivo, "wb") as out_file:
                    out_file.write(resp.read())
                size_mb = os.path.getsize(ruta_archivo) / (1024 * 1024)
                print(f"  ✓ Descargado con éxito ({size_mb:.2f} MB)")
            except Exception as e:
                print(f"  ✗ Error descargando {nombre_archivo}: {e}")
        else:
            print(f"Audio pendiente de descarga: {nombre_archivo} -> {url_mp3}")

if __name__ == "__main__":
    descargar_subtitulos()
    limpiar_transcripciones()
    descargar_audios(descargar_ahora=True)
