#!/usr/bin/env python3
"""
Script utilitario para limpiar transcripciones de subtítulos VTT (YouTube)
o salidas de Whisper del podcast 'Lasers y Dragones' (Versión 2.0).

Características principales:
1. Deduplica subtítulos acumulativos de YouTube conservando el anclaje temporal de cada párrafo ([HH:MM:SS]).
2. Clasifica las correcciones fonéticas STT en dos niveles:
   - Nivel 1 (Seguro): Correcciones fonéticas unívocas sin riesgo de falsos positivos en español.
   - Nivel 2 (Contextual / Dudoso): Expresiones que pueden ser frases legítimas en español
     (ej. 'que elevarse'), las cuales solo se sustituyen si existe contexto explícito o se marcan para revisión humana.
3. Genera automáticamente un informe de auditoría (.log) con el detalle de cada sustitución y alertas de revisión.
"""

import sys
import os
import re
import argparse

# Diccionario de correcciones de Nivel 1 (Seguras e incondicionales)
REGLAS_NIVEL_1 = [
    # La Roca del Drift / El Drift (STT confunde Drift con "triunfo" o "deriva")
    (r"\bpiedra\s+del\s+triunfo\b", "Roca del Drift", "Roca del Drift"),
    (r"\bpiedra\s+del\s+[Dd]rift\b", "Roca del Drift", "Roca del Drift"),
    (r"\broca\s+del\s+triunfo\b", "Roca del Drift", "Roca del Drift"),
    (r"\bmotor\s+del\s+triunfo\b", "motor del Drift", "el Drift"),
    (r"\bviaje\s+por\s+el\s+triunfo\b", "viaje por el Drift", "el Drift"),
    (r"\bsalto\s+al\s+triunfo\b", "salto al Drift", "el Drift"),
    (r"\bsalto\s+del\s+triunfo\b", "salto del Drift", "el Drift"),
    (r"\bhiperespacio\s+del\s+triunfo\b", "hiperespacio del Drift", "el Drift"),
    
    # Grafía canónica oficial de A.Xel 42
    (r"\bAxel\s+42\b", "A.Xel 42", "A.Xel 42"),
    (r"\bA\.xel\s+42\b", "A.Xel 42", "A.Xel 42"),
    (r"\bAxel\b", "A.Xel", "A.Xel"),
    (r"\bA\.xel\b", "A.Xel", "A.Xel"),

    # Personajes secundarios y PNJs del podcast
    (r"\bRing\s+Rey\b", "Rim Rey", "Rim Rey"),
    (r"\bRin\s+Rey\b", "Rim Rey", "Rim Rey"),
    (r"\bchischis\b", "Chiskisk", "Chiskisk"),
    (r"\bchischís\b", "Chiskisk", "Chiskisk"),
    (r"\bFerani\s+Krane\b", "Ferani Nadaz", "Ferani Nadaz"),
    (r"\bFerani\s+Crane\b", "Ferani Nadaz", "Ferani Nadaz"),
    (r"\bBrock\s+Jabaxa\b", "Brock Hilario", "Brock Hilario"),
    (r"\bSunrise\s+Maiden\b", "Estrella Errante", "Estrella Errante"),
    (r"\bKeltusa\b", "Keltus", "Keltus"),
    (r"\bque\s+el\s+t[uú]s\b", "Keltus", "Keltus"),
    (r"\bángel\s+tus\s+a\s+él\b", "Keltus", "Keltus"),
    (r"\bGevalnor\b", "Gevalarsk Nor", "Gevalarsk Nor"),
    (r"\bque\s+le\s+vasco\s+norma\b", "Gevalarsk Nor", "Gevalarsk Nor"),
    (r"\bDuravor\s+Kreel\b", "Marlene Boosmar", "Marlene Boosmar"),
]

# Diccionario de correcciones de Nivel 2 (Contextuales / Requieren validación o alerta)
# Formato: (patrón, reemplazo, nombre, lista_palabras_clave_contexto)
REGLAS_NIVEL_2 = [
    (
        r"\bque\s+elevarse\b",
        "Gevalarsk Nor",
        "Gevalarsk Nor (Ambiguo con perífrasis verbal)",
        ["embajador", "eox", "elebriano", "nor", "keltus", "diplomático", "pacto", "muerto"]
    ),
]


def formatear_segundos_hhmmss(segundos_float):
    """Convierte segundos flotantes a formato HH:MM:SS."""
    total_seg = int(segundos_float)
    h = total_seg // 3600
    m = (total_seg % 3600) // 60
    s = total_seg % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def parsear_tiempo_vtt(timestamp_str):
    """Parsea una marca de tiempo '00:01:23.456' o '01:23.456' a segundos flotantes."""
    timestamp_str = timestamp_str.strip()
    partes = timestamp_str.split(":")
    if len(partes) == 3:
        h, m, s = partes
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(partes) == 2:
        m, s = partes
        return int(m) * 60 + float(s)
    return 0.0


def extraer_cues_vtt(lines):
    """
    Extrae bloques de texto con su tiempo inicial de un archivo WebVTT.
    Retorna una lista de tuplas (tiempo_segundos, texto_limpio).
    """
    cues = []
    current_time = 0.0
    time_regex = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})\s*-->")

    for line in lines:
        line_clean = line.strip()
        if not line_clean or "WEBVTT" in line_clean or "Kind:" in line_clean or "Language:" in line_clean:
            continue
        if line_clean.startswith("align:") or line_clean.startswith("position:"):
            continue

        m = time_regex.search(line_clean)
        if m:
            current_time = parsear_tiempo_vtt(m.group(1))
            continue

        # Eliminar marcas de tiempo internas estilo <00:00:29.269><c> ... </c>
        text = re.sub(r"<[^>]+>", "", line_clean).strip()
        
        # Omitir acotaciones automáticas irrelevantes
        if text and text not in ("[Música]", "[Risas]", "[Aplausos]"):
            cues.append((current_time, text))

    return cues


def deduplicar_cues(cues):
    """
    Deduplica subtítulos acumulativos generados automáticamente por YouTube.
    Conserva la marca de tiempo del inicio de cada fragmento consolidado.
    """
    deduped = []
    for t, text in cues:
        if not deduped:
            deduped.append((t, text))
            continue

        last_t, last_text = deduped[-1]
        if text == last_text:
            continue
        elif text.startswith(last_text):
            # Expansión del subtítulo actual
            deduped[-1] = (last_t, text)
        elif last_text.startswith(text):
            continue
        else:
            deduped.append((t, text))

    return deduped


def aplicar_correcciones_y_auditar(parrafos_con_tiempo):
    """
    Aplica las correcciones fonéticas en los párrafos y genera un log detallado.
    Retorna (parrafos_procesados, log_entries, estadisticas).
    """
    log_entries = []
    stats = {"nivel_1": 0, "nivel_2_aplicado": 0, "alertas_dudosas": 0}

    parrafos_finales = []

    for t_str, p_text in parrafos_con_tiempo:
        texto_actual = p_text

        # 1. Reglas Nivel 1 (Seguras)
        for patron, reemplazo, nombre in REGLAS_NIVEL_1:
            matches = [m for m in re.finditer(patron, texto_actual, flags=re.IGNORECASE) if m.group(0) != reemplazo]
            if matches:
                stats["nivel_1"] += len(matches)
                for match in matches:
                    snippet_inicio = max(0, match.start() - 25)
                    snippet_fin = min(len(texto_actual), match.end() + 25)
                    log_entries.append({
                        "tipo": "NIVEL_1_SEGURO",
                        "tiempo": t_str,
                        "patron": nombre,
                        "original": match.group(0),
                        "reemplazo": reemplazo,
                        "contexto": texto_actual[snippet_inicio:snippet_fin].replace("\n", " ")
                    })

                def _hacer_reemplazo(m, rep=reemplazo):
                    orig = m.group(0)
                    if orig == rep:
                        return orig
                    if orig and orig[0].isupper() and rep and rep[0].islower():
                        return rep[0].upper() + rep[1:]
                    return rep

                texto_actual = re.sub(patron, _hacer_reemplazo, texto_actual, flags=re.IGNORECASE)

        # 2. Reglas Nivel 2 (Contextuales)
        for patron, reemplazo, nombre, palabras_clave in REGLAS_NIVEL_2:
            matches = [m for m in re.finditer(patron, texto_actual, flags=re.IGNORECASE) if m.group(0) != reemplazo]
            if matches:
                for match in matches:
                    # Evaluar ventana de contexto alrededor del match (+/- 150 caracteres)
                    v_inicio = max(0, match.start() - 150)
                    v_fin = min(len(texto_actual), match.end() + 150)
                    ventana = texto_actual[v_inicio:v_fin].lower()

                    tiene_contexto = any(kw in ventana for kw in palabras_clave)

                    if tiene_contexto:
                        stats["nivel_2_aplicado"] += 1
                        log_entries.append({
                            "tipo": "NIVEL_2_CONTEXTUAL_OK",
                            "tiempo": t_str,
                            "patron": nombre,
                            "original": match.group(0),
                            "reemplazo": reemplazo,
                            "contexto": texto_actual[max(0, match.start() - 30):min(len(texto_actual), match.end() + 30)]
                        })
                        # Reemplazo seguro validado por contexto
                        texto_actual = (
                            texto_actual[:match.start()] +
                            reemplazo +
                            texto_actual[match.end():]
                        )
                    else:
                        stats["alertas_dudosas"] += 1
                        log_entries.append({
                            "tipo": "ALERTA_REVISION_DUDOSA",
                            "tiempo": t_str,
                            "patron": nombre,
                            "original": match.group(0),
                            "reemplazo": "[CONSERVADO ORIGINAL POR AMBIGÜEDAD]",
                            "contexto": texto_actual[max(0, match.start() - 35):min(len(texto_actual), match.end() + 35)]
                        })

        parrafos_finales.append((t_str, texto_actual))

    return parrafos_finales, log_entries, stats


def agrupar_en_parrafos(cues_deduped, oraciones_por_parrafo=6):
    """
    Agrupa los fragmentos continuos en párrafos de ~6 oraciones,
    conservando el tiempo del inicio de cada párrafo.
    """
    if not cues_deduped:
        return []

    parrafos = []
    current_sentences = []
    paragraph_start_time = cues_deduped[0][0]

    for t, text in cues_deduped:
        partes = re.split(r'([.?!]\s+)', text)
        for i in range(0, len(partes), 2):
            s = partes[i]
            sep = partes[i+1] if i+1 < len(partes) else ""
            frase = (s + sep).strip()
            if not frase:
                continue

            if not current_sentences:
                paragraph_start_time = t

            current_sentences.append(frase)

            if len(current_sentences) >= oraciones_por_parrafo:
                t_str = formatear_segundos_hhmmss(paragraph_start_time)
                parrafos.append((t_str, " ".join(current_sentences)))
                current_sentences = []

    if current_sentences:
        t_str = formatear_segundos_hhmmss(paragraph_start_time)
        parrafos.append((t_str, " ".join(current_sentences)))

    return parrafos


def escribir_informe_log(log_path, stats, log_entries, total_palabras, total_parrafos):
    """Genera un archivo de auditoría .log con todas las operaciones y advertencias."""
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("INFORME DE AUDITORÍA Y LIMPIEZA DE TRANSCRIPCIÓN (STT)\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Métricas Globales:\n")
        f.write(f"  - Total palabras: {total_palabras:,}\n")
        f.write(f"  - Total párrafos: {total_parrafos:,}\n")
        f.write(f"  - Correcciones automáticas Nivel 1 (Seguras): {stats['nivel_1']}\n")
        f.write(f"  - Correcciones validadas Nivel 2 (Contextuales): {stats['nivel_2_aplicado']}\n")
        f.write(f"  - Alertas dudosas (Conservado original para revisión): {stats['alertas_dudosas']}\n\n")

        if stats['alertas_dudosas'] > 0:
            f.write("⚠️  ATENCIÓN: Se detectaron expresiones dudosas que NO se sustituyeron automáticamente:\n")
            f.write("-" * 70 + "\n")
            for entry in log_entries:
                if entry["tipo"] == "ALERTA_REVISION_DUDOSA":
                    f.write(f"  [{entry['tiempo']}] '{entry['original']}' -> Contexto: \"...{entry['contexto']}...\"\n")
            f.write("\n")

        f.write("Detalle de Sustituciones Realizadas:\n")
        f.write("-" * 70 + "\n")
        if not log_entries:
            f.write("  (No se registraron sustituciones automáticas en este archivo)\n")
        else:
            for entry in log_entries:
                if entry["tipo"] != "ALERTA_REVISION_DUDOSA":
                    f.write(f"  [{entry['tiempo']}] [{entry['tipo']}] '{entry['original']}' -> '{entry['reemplazo']}'\n")
                    f.write(f"      Contexto: \"...{entry['contexto']}...\"\n")


def procesar_transcripcion(input_path, output_path=None, incluir_marcas=True, log_path=None):
    if not os.path.exists(input_path):
        print(f"Error: No existe el archivo de entrada: {input_path}")
        return False

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    cues_raw = extraer_cues_vtt(lines)
    if not cues_raw:
        print(f"Aviso: No se encontraron subtítulos o cues válidos en {input_path}")
        return False

    cues_deduped = deduplicar_cues(cues_raw)
    parrafos_crudos = agrupar_en_parrafos(cues_deduped)

    parrafos_finales, log_entries, stats = aplicar_correcciones_y_auditar(parrafos_crudos)

    # Construir texto final
    bloques = []
    for t_str, p_text in parrafos_finales:
        if incluir_marcas:
            bloques.append(f"[{t_str}] {p_text}")
        else:
            bloques.append(p_text)

    contenido_final = "\n\n".join(bloques)

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + "_limpio.txt"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(contenido_final)

    # Determinar ruta del log
    if log_path is None:
        base_out, _ = os.path.splitext(output_path)
        log_path = base_out + "_limpieza.log"

    total_palabras = len(contenido_final.split())
    escribir_informe_log(log_path, stats, log_entries, total_palabras, len(parrafos_finales))

    print(f"✓ Transcripción limpia guardada en: {output_path}")
    print(f"  - Palabras: {total_palabras:,} | Párrafos: {len(parrafos_finales)}")
    print(f"  - Correcciones automáticas (Nivel 1): {stats['nivel_1']}")
    print(f"  - Correcciones contextuales (Nivel 2): {stats['nivel_2_aplicado']}")
    if stats['alertas_dudosas'] > 0:
        print(f"  ⚠️  ALERTAS DUDOSAS: {stats['alertas_dudosas']} (revisar {log_path})")
    print(f"✓ Registro de auditoría guardado en: {log_path}")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Limpia subtítulos VTT de Lasers y Dragones conservando anclajes temporales y registrando auditoría."
    )
    parser.add_argument("input_file", help="Ruta al archivo .vtt original")
    parser.add_argument("output_file", nargs="?", default=None, help="Ruta al archivo de salida limpio (.txt)")
    parser.add_argument("--no-timestamps", action="store_true", help="Omitir las etiquetas [HH:MM:SS] al inicio de los párrafos")
    parser.add_argument("--log", default=None, help="Ruta personalizada para el archivo de informe .log")

    args = parser.parse_args()
    procesar_transcripcion(
        args.input_file,
        args.output_file,
        incluir_marcas=not args.no_timestamps,
        log_path=args.log
    )
