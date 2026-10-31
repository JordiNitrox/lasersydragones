# Contexto Completo y Guía de Continuidad
## Archivo Maestro de la Saga Novelizada *Lasers y Dragones*

Este directorio funciona como la **Única Fuente de Verdad** (*Single Source of Truth*) del universo narrativo novelizado a partir de las sesiones del podcast *Lasers y Dragones* (Campaña Starfinder: *Dead Suns*).

---

## 📕 Documentos y Estructura Modular

Para facilitar la lectura, edición y mantenimiento independiente sin manipular un único archivo masivo, el contexto completo está organizado de forma modular en la carpeta [`secciones/`](secciones/):

1. **Estructura Modular (`secciones/`):**
   - **[`01_resumen_cronologico_volumenes.md`](secciones/01_resumen_cronologico_volumenes.md):** Título, presentación y resumen cronológico de los **Volúmenes 1 al 6** (Episodios 1 al 72) y visión de tramas futuras.
   - **[`02_indice_maestro_escenarios.md`](secciones/02_indice_maestro_escenarios.md):** Índice maestro de escenarios, estaciones, planetas y pecios con etiquetas de aparición `[Volumen X]`.
   - **[`03_dossier_maestro_personajes.md`](secciones/03_dossier_maestro_personajes.md):** Dossier exhaustivo de protagonistas, secundarios clave y antagonistas.
   - **[`04_corporaciones_facciones.md`](secciones/04_corporaciones_facciones.md):** Directorio de megacorporaciones, sindicatos mineros, flotas renegadas y casas nobles.
   - **[`05_bestiario_y_amenazas.md`](secciones/05_bestiario_y_amenazas.md):** Bestiario cósmico y amenazas de la campaña (akatas, garaggakal, driftdead, etc.).
   - **[`06_matriz_continuidad.md`](secciones/06_matriz_continuidad.md):** Tabla comparativa de evolución de naves, bases, armas de Gerty, romances y estado de la tripulación.

2. **[CONTEXTO_COMPLETO_SAGA.md](CONTEXTO_COMPLETO_SAGA.md)**:
   Documento consolidado generado automáticamente por el compilador, que unifica todas las secciones anteriores en un único archivo de referencia.

3. **[Descargar PDF Editorial (49 Páginas)](Contexto_Completo_Lasers_y_Dragones.pdf)**:
   Versión maquetada con portada y diseño editorial homogéneo, ideal para lectura rápida y consulta con marcadores interactivos.

4. **`generar_contexto_pdf.py`**:
   Script de compilación que consolida automáticamente los archivos de `secciones/` en `CONTEXTO_COMPLETO_SAGA.md`, genera el HTML estructurado y renderiza el PDF en dos pases calculando la paginación exacta.

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
