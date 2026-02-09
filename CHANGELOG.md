# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Añadido

### Cambiado

### Corregido
- **URL de GitHub**: Corregida referencia obsoleta al repositorio en sección "Cómo Contribuir".
- **Referencias de imágenes**: Corregidas 6 referencias a figuras con nombres de archivo incorrectos:
  - Capítulo 2: fig-02-11 (sustainer-engine → sustainer)
  - Capítulo 5: fig-05-14, fig-05-15, fig-05-16 (rendimiento-polar → performance-polar)
  - Capítulo 7: fig-07-07 (roll-oscillations → balanceo-oscillations)
  - Capítulo 10: fig-10-17 (roll-the-craft → balanceo-the-craft)

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
