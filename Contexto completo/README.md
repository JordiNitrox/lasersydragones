# Contexto Completo y Guía de Continuidad
## Archivo Maestro de la Saga Novelizada *Lasers y Dragones*

Este directorio funciona como la **Única Fuente de Verdad** (*Single Source of Truth*) del universo narrativo novelizado a partir de las sesiones del podcast *Lasers y Dragones* (Campaña Starfinder: *Dead Suns*).

---

## 📕 Documentos Disponibles

1. **[CONTEXTO_COMPLETO_SAGA.md](CONTEXTO_COMPLETO_SAGA.md)**:
   Documento maestro en Markdown que consolida:
   - Resumen cronológico y canónico de los **Volúmenes 1 al 6** (Episodios 1 al 72: desde la llegada a Absalón hasta el salto al Drift hacia la Diáspora).
   - Índice maestro de todos los escenarios y ubicaciones con indicación explícita de aparición en volúmenes (`[Aparece en: ...]`).
   - Dossier exhaustivo de personajes protagonistas y secundarios con sus arcos, armas, evoluciones y estado actual.
   - Directorio de corporaciones, facciones galácticas, bestiario cósmico y matriz de continuidad comparativa.

2. **[Descargar PDF Editorial (46 Páginas)](Contexto_Completo_Lasers_y_Dragones.pdf)**:
   Versión maquetada con la misma portada y diseño tipográfico de las novelas, ideal para una lectura cómoda y rápida de toda la historia acumulada.

3. **`generar_contexto_pdf.py`**:
   Script de compilación que transforma el archivo Markdown en HTML estructurado y lo compila a PDF mediante LibreOffice headless en dos pases con pdftotext.

---

## 🔄 Protocolo de Actualización para Futuros Volúmenes

De acuerdo con el skill de novelización:
1. **Fase Pre-Novelización:** Consultar este directorio antes de redactar cualquier volumen futuro (ej. Volumen 7) para mantener estricta coherencia con las naves, mejoras de Gerty, armas, deudas y vínculos románticos previos.
2. **Fase Post-Novelización:** Tras finalizar la redacción de cada nuevo volumen:
   - Añadir el resumen del volumen en la Sección 1.
   - Actualizar las etiquetas de aparición `[Aparece en: Volumen X, Volumen Y...]` de personajes y lugares recurrentes.
   - Añadir nuevos personajes y planetas introducidos.
   - Actualizar la Matriz de Continuidad (Sección 6).
   - Ejecutar `python3 "Contexto completo/generar_contexto_pdf.py"` para refrescar el PDF maestro.
