# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5-dev] - En desarrollo

### Añadido
- En desarrollo.

### Cambiado
- Versión: Bump a 0.1.5-dev.

### Corregido
- En desarrollo.

## [0.1.4] - 2026-02-09

### Añadido
- **Scripts de post-procesamiento**:
  - `capitalize-terms.rb`: Capitalización automática de términos técnicos.
  - Extensión `figura-por-capitulo.rb`: Contador compartido para figuras y tablas.
- **Imágenes del Capítulo 4**: Todas las 31 figuras traducidas al español (instrumentos de vuelo).

### Cambiado
- **Revisión masiva de capítulos 1-8**: Mejoras en terminología, estilo y gramática.
  - Capítulos 1-3: Revisión terminológica y correcciones de estilo.
  - Capítulo 4: ✅ COMPLETADO - Texto revisado, 31 imágenes traducidas y validadas. Figuras 04-08 y 04-09 comentadas (reemplazadas por tablas equivalentes).
  - Capítulos 5-6: Revisiones de terminología y estilo.
  - Capítulo 7: Correcciones gramaticales fases 3 y 4.
  - Capítulo 8: Reemplazo sistemático "falla" → "fallo".
- **Formato según norma RAE**:
  - Separadores numéricos aplicados (ej: `1 000` en lugar de `1000`).
  - Capitalización en estilo oración (solo primera palabra en mayúscula en títulos).
  - Comillas latinas (« ») en todo el documento.
- **Estilo PDF**: Tablas con esquinas redondeadas, header ajustado a 10mm.
- **Versión**: Bump a 0.1.4.

### Corregido
- **URL de GitHub**: Referencia obsoleta `faa-gfh-castellano` → `faa-glider-flying-handbook-es`.
- **Referencias de imágenes**: 6 figuras con nombres de archivo incorrectos corregidos:
  - Capítulo 2: fig-02-11
  - Capítulo 5: fig-05-14, fig-05-15, fig-05-16
  - Capítulo 7: fig-07-07
  - Capítulo 10: fig-10-17
- **Estructura**: Jerarquía de secciones y numeración de figuras (cap. 12).
- **AGENTS.md**: Reglas de autorización y estilo actualizadas.

## [0.1.3] - 2026-02-08

### Añadido
- Reglas de capitalización y uso de comillas latinas en `AGENTS.md`.
- **Capítulo 3 completamente traducido**: Todas las 22 imágenes del capítulo de Aerodinámica del Vuelo traducidas al español con etiquetas técnicas correctas.

### Corregido
- Script `validate-terminology.sh`: corregido error que impedía detectar atributos definidos debido a la inclusión del nombre del archivo en la salida de `grep`.
- Eliminadas inconsistencias críticas de terminología ("patrón de tráfico", "entrada en pérdida").
- **Comillas angulares**: Corrección masiva de comillas rectas (") por comillas latinas (« ») en los 12 capítulos según norma RAE.
- **Capítulo 12**: Corregida numeración duplicada de figuras 12-9 a 12-12.

### Actualizado
- `REVIEW.md` actualizado con métricas precisas y estado real de los capítulos.
- Imágenes del capítulo 3: figuras 03-01 a 03-22 con texto traducido al español.

## [0.1.2] - 2026-02-06

### Añadido
- **Image Manager v3.0**: Nueva herramienta en Python para gestión de imágenes con:
  - Compresión adaptativa (PNG/WebP).
  - Traducción automática con Google Gemini API.
  - Persistencia de configuración.
- Auditoría del repositorio (`REVIEW.md`).

### Cambios
- Actualización de versión a 0.1.2 en todos los archivos de configuración.
- Mejoras en la documentación y guías de contribución.
- Procesamiento masivo de imágenes con esquinas redondeadas.

### Corregido
- Ajuste de altura del header en PDF (10mm) para evitar solapamiento.
- Eliminación de bloques `[abstract]` en capítulos para mejorar formato.
- Corrección de tamaño fijo en imágenes del capítulo 01.

## [0.1.1] - 2026-02-06

### Inicial
- Estructura inicial del proyecto.
- Configuración de `Makefile` y `Gemfile`.
- Importación inicial de capítulos y recursos.
