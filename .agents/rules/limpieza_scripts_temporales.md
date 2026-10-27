# Regla de Higiene del Entorno y Limpieza de Scripts Temporales (`scratch/`)

> 🧹 **REGLA MANDATORIA DE GESTIÓN DE ARCHIVOS TEMPORALES:**
> **Los scripts de usar y tirar, análisis puntuales y volcados de texto nunca deben acumularse en el espacio de trabajo.**

---

### 1. Ubicación y Uso de Scripts Temporales
1. **Preferir ejecución en memoria o sesión efímera:**  
   Para comprobaciones rápidas de transcripciones, recuentos o búsquedas de patrones, se debe priorizar comandos *inline* (`python3 -c "..."` o `grep`) o el directorio de scratch propio de la sesión del agente.
2. **Uso de la carpeta `scratch/`:**  
   Si una tarea compleja requiere generar scripts o archivos auxiliares en la carpeta `scratch/` del repositorio, su vigencia es estrictamente transitoria mientras dure dicha tarea.

---

### 2. Protocolo de Limpieza Inmediata
* **Limpieza tras finalizar:** En cuanto el script o archivo auxiliar haya proporcionado los datos necesarios (o tras redactar/validar el capítulo o documento en curso), el agente debe eliminar inmediatamente el archivo o vaciar la carpeta (`rm -rf scratch/*`).
* **Verificación al inicio/cierre:** Al iniciar o concluir cualquier sesión o tanda de trabajo, el agente verificará si existen restos huérfanos en `scratch/` y los limpiará para mantener el árbol de trabajo impecable.

---

### 3. Exclusión de Control de Versiones
* `scratch/` y cualquier archivo contenido en ella están excluidos permanentemente en `.gitignore`.
* Queda terminantemente prohibido añadir archivos de `scratch/` al índice de Git o incluirlos en ningún commit.
