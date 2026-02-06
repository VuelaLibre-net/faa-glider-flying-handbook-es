# Changelog - Manual de Vuelo sin Motor

>Todas las modificaciones notables de este proyecto se documentarán en este archivo.
>
>El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### Planned
- Traducción de textos en imágenes (279 figuras)
- Revisión técnica por pilotos titulados
- Implementación completa de atributos de terminología `{term-xxx}`
- Corrección de inconsistencias terminológicas ("patrón de tráfico" → "circuito de tráfico")
- Soporte para variante regional de México (mx)

---

## [0.1.1] - 2026-02-06

### Changed
- **Regeneración completa del Índice de Figuras** (`es/apendices/indice-figuras.adoc`)
  - Incremento de ~50 a **262 figuras** documentadas (+424%)
  - Todos los títulos extraídos automáticamente de captions en capítulos
  - Distribución por capítulo: 01(4), 02(12), 03(21), 04(30), 05(19), 06(17), 07(41), 08(11), 09(30), 10(37), 11(16), 12(11), 13(13)

### Added
- **Auditoría del repositorio** (`REVIEW.md`)
  - Análisis completo de estructura, contenido e infraestructura
  - Identificación de 17 inconsistencias terminológicas
  - Métricas de calidad y recomendaciones priorizadas
  - Estado: 262/279 figuras indexadas, 0/279 imágenes traducidas

---

## [0.1.0] - 2026-02-06

### Added
- **Estructura inicial del proyecto** con soporte multi-formato (PDF, HTML, EPUB)
- **13 capítulos traducidos** del FAA Glider Flying Handbook (FAA-H-8083-13B):
  - Capítulo 1: Planeadores y veleros
  - Capítulo 2: Componentes y sistemas
  - Capítulo 3: Aerodinámica del vuelo
  - Capítulo 4: Instrumentos de vuelo
  - Capítulo 5: Performance del planeador
  - Capítulo 6: Prevuelo y operaciones en tierra
  - Capítulo 7: Lanzamiento, aterrizaje y maniobras
  - Capítulo 8: Procedimientos de emergencia
  - Capítulo 9: Meteorología para vuelo a vela
  - Capítulo 10: Técnicas de vuelo a vela
  - Capítulo 11: Vuelo de travesía
  - Capítulo 12: Remolque
  - Capítulo 13: Factores humanos
- **Glosario completo** con 80+ términos aeronáuticos ES↔EN
- **Sistema de build** con Makefile automatizado:
  - `make pdf` - Generación de PDF con tema personalizado
  - `make html` - HTML multi-página
  - `make epub` - Generación de EPUB
  - `make validate` - Validación de terminología
  - `make watch` - Modo desarrollo con regeneración automática
- **Gestor de Imágenes v3.0** - Aplicación Python GUI para:
  - Compresión y optimización de imágenes
  - Traducción automática de texto en imágenes (integración Google Gemini)
  - Editor visual con etiquetado tipo "badges"
  - Gestión por capítulos (01-13)
- **Extensiones Ruby personalizadas**:
  - `figura-por-capitulo.rb` - Numeración de figuras formato X-Y (igual que manual FAA original)
- **Soporte de variantes regionales**:
  - España (es) - terminología AESA/EASA
  - Argentina (ar) - terminología local
- **Documentación completa**:
  - `AGENTS.md` - Guía para agentes de IA
  - `CONTRIBUTING.md` - Guía de contribución
  - `README.md` - Visión general del proyecto
- **Tema PDF personalizado** (A4, colores aviación)
- **Tema HTML responsive** con estilos CSS
- **Validación de terminología** - Script bash para detectar inconsistencias

### Imported
- **279 imágenes oficiales FAA** importadas y organizadas por capítulo
- Formatos duales: PNG (para PDF) y WebP (para web)
- Portada y mockups del manual

### Technical
- Configuración Ruby 3.3.5 con RVM gemset
- Gemas: asciidoctor, asciidoctor-pdf, asciidoctor-epub3, asciidoctor-mathematical, asciidoctor-multipage
- Entorno Python para gestor de imágenes
- Integración con Google Gemini API para traducción de imágenes

---

## Tipos de Cambios

- `Added` - Nuevas funcionalidades
- `Changed` - Cambios en funcionalidades existentes
- `Deprecated` - Funcionalidades marcadas para eliminación
- `Removed` - Funcionalidades eliminadas
- `Fixed` - Correcciones de errores
- `Security` - Mejoras de seguridad

---

## Notas de Versión

### Convención de Versionado

Este proyecto usa [Semantic Versioning](https://semver.org/lang/es/):

- **MAJOR** (X.y.z) - Cambios incompatibles con versiones anteriores
- **MINOR** (x.Y.z) - Nuevas funcionalidades, manteniendo compatibilidad
- **PATCH** (x.y.Z) - Correcciones de errores

### Versiones Planeadas

| Versión | Objetivo | Fecha Estimada |
|---------|----------|----------------|
| 0.2.0 | Corrección de terminología, uso de atributos {term-xxx} | TBD |
| 0.3.0 | Traducción de imágenes críticas (diagramas de emergencia) | TBD |
| 0.4.0 | Revisión técnica completa por pilotos titulados | TBD |
| 0.5.0 | Traducción de 50% de imágenes | TBD |
| 1.0.0 | Versión de producción completa | TBD |

---

## Referencias

- [FAA Glider Flying Handbook](https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook) - Documento original
- [Repositorio GitHub](https://github.com/VuelaLibre-net/faa-glider-flying-handbook-es)
- [VuelaLibre.net](https://vuelalibre.net) - Proyecto comunitario

---

*Este changelog se actualiza manualmente. Para ver cambios recientes, consultar el historial de git: `git log --oneline`*
