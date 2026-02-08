# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] (v0.1.3)

### Añadido
- Reglas de capitalización y uso de comillas latinas en `AGENTS.md`.

### Corregido
- Script `validate-terminology.sh`: corregido error que impedía detectar atributos definidos debido a la inclusión del nombre del archivo en la salida de `grep`.
- Eliminadas inconsistencias críticas de terminología ("patrón de tráfico", "entrada en pérdida").

### Actualizado
- `REVIEW.md` actualizado con métricas precisas y estado real de los capítulos.

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
