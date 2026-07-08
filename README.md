# Manual de Vuelo sin Motor

![Versión](https://img.shields.io/badge/version-0.1.5-blue)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

<p align="center">
  <img src="es/imagenes/mockup.webp" alt="Mockup del Manual" width="600">
</p>

> Traducción al español del [**FAA Glider Flying Handbook**](https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook) (FAA-H-8083-13B), Federal Aviation Administration, U.S. Department of Transportation, para la comunidad de pilotos de España y Latinoamérica.

---

## ⚠️ Aviso Importante

**TRADUCCIÓN EN CURSO, INDEPENDIENTE Y NO OFICIAL**

Este documento es una traducción independiente realizada por la comunidad. **No está avalado, patrocinado ni aprobado por la FAA, el Departamento de Transporte de EE.UU., ni ninguna autoridad aeronáutica.**

El documento original en inglés es la única fuente autorizada. En caso de discrepancia, prevalece siempre el texto original. Se ha traducido al español porque, en España, aún no existe ninguna documentación oficial para el estudio de los exámenes oficiales y EASA ha extraido varias preguntas de examen de este manual en inglés.

### Exención de Responsabilidad

La aviación es una actividad que conlleva riesgos inherentes. **Los traductores, editores y colaboradores de este proyecto NO asumen responsabilidad alguna** por daños que pudieran derivarse del uso de esta traducción.

Antes de aplicar cualquier procedimiento:
- Consulte el documento original en inglés
- Verifique la normativa de su autoridad aeronáutica (AESA/EASA en España)
- Confirme los procedimientos con un instructor cualificado

---

## Sobre el Proyecto

Este proyecto tiene como objetivo proporcionar una traducción de calidad del manual de la FAA para vuelo en planeador, adaptando la terminología aeronáutica al español estándar utilizado en la aviación general.

## Estado del Proyecto

**Versión actual: 0.1.5**

Esta versión está en fase **inicial de desarrollo**. Se ha completado la importación de todas las imágenes del manual original, pero el proyecto requiere trabajo significativo antes de estar listo para producción:

- ✅ 280 imágenes oficiales FAA importadas (100%)
- ✅ Capítulos 1-4: Texto revisado y completo
- ✅ 83/279 imágenes con texto traducido al español (30%)
- ⚠️ Capítulos 5-13: En revisión inicial
- 🔍 Terminología técnica por validar con pilotos titulados

### Estrategia de imágenes

| Formato | Uso | Estado |
|---------|-----|--------|
| **WebP** | Web, README, HTML | ✅ Optimizado (91% menor tamaño) |
| **PNG** | PDF, impresión, epub | ✅ Alta calidad preservada |

Las imágenes se mantienen en ambos formatos: PNG para el PDF (máxima compatibilidad) y WebP para web (máximo rendimiento).

**Para producción 1.0.0:** Consulta el [CHANGELOG](CHANGELOG.md) y el roadmap de tareas pendientes.

---

## Estructura del Proyecto

```
faa-gfh/
├── es/                              # Contenido en español
│   ├── manual-vuelo-planeador.adoc  # Documento maestro
│   ├── config/                      # Configuración
│   │   ├── atributos.adoc           # Variables globales y selector regional
│   │   └── regiones/                # Variantes terminológicas por región
│   │       ├── es.adoc              # España - default
│   │       └── ar.adoc              # Argentina
│   ├── capitulos/                   # Capítulos traducidos (01-13)
│   └── apendices/                   # Apéndices
│       └── glosario.adoc            # Glosario completo
├── temas/                           # Temas de estilo
│   ├── pdf-theme.yml                # Tema PDF (A4, moderno)
│   └── styles.css                   # Estilos HTML
├── scripts/
│   └── validate-terminology.sh      # Validación de terminología
├── CHANGELOG.md                     # Historial de cambios
├── CONTRIBUTING.md                  # Guía de contribución
├── AGENTS.md                        # Guía para agentes AI
├── Makefile                         # Automatización de build
└── build/                           # Archivos generados (gitignored)
```

## Requisitos

- [Ruby](https://www.ruby-lang.org/) 2.7+
- [Asciidoctor](https://asciidoctor.org/) 2.0+
- [Asciidoctor PDF](https://docs.asciidoctor.org/pdf-converter/latest/)
- [Asciidoctor EPUB3](https://docs.asciidoctor.org/epub3-converter/latest/) (opcional)

### Instalación de dependencias

```bash
# Con gem (Ruby)
gem install asciidoctor asciidoctor-pdf asciidoctor-epub3

# Verificar instalación
make check
```

## Generación de Documentos

```bash
# Generar todos los formatos (PDF, HTML, EPUB)
make all

# Solo PDF (terminología española por defecto)
make pdf

# PDF con terminología argentina
make pdf REGION=ar
# o
make pdf-ar

# PDF con terminología mexicana
make pdf REGION=mx
# o
make pdf-mx

# Solo HTML
make html

# Solo EPUB
make epub

# Limpiar archivos generados
make clean

# Ver ayuda
make help
```

Los archivos generados se encuentran en:
- `build/pdf/manual-vuelo-planeador.pdf`
- `build/html/manual-vuelo-planeador.html`
- `build/epub/manual-vuelo-planeador.epub`

### Variantes regionales

El manual soporta adaptaciones terminológicas para diferentes regiones de habla hispana:

| Región | Código | Ejemplo de variante |
|--------|--------|---------------------|
| España | `es` | "tramo de viento en cola", "lanita" |
| Argentina | `ar` | "tramo de viento de cola", "cinta de guinada" |
| México | `mx` | (por definir) |

Para generar una versión regional específica:
```bash
make pdf REGION=ar
```

Las variantes terminológicas se definen en `es/config/regiones/{código}.adoc`.

## Herramientas de Desarrollo

### Gestor de Imágenes (Image Manager v3.0)

Incluye una herramienta GUI modular para gestionar, comprimir y *traducir automáticamente* los textos de las imágenes del manual.

<p align="center">
  <img src="es/imagenes/mockup-gestor-imagenes.webp" alt="Gestor de Imágenes v3.0" width="400">
</p>


```bash
# Configurar (primera vez)
make setup-images

# Lanzar
make images
```

**Características:**
- 🗜️ **Compresión PNG**: Reduce tamaño manteniendo calidad (cuantización a 256 colores)
- 🔄 **Reemplazo inteligente**: Selecciona imagen destino y fuente, comprime y reemplaza
- 📋 **Portapapeles multiplataforma**: Copiar/pegar imágenes desde/hacia el gestor
- 🌍 **Traducción automática nativa**: Integración con Google Gemini para traducir texto en imágenes del inglés al español
- 🖼️ **Editor integrado**: Etiquetado tipo «badges» en imágenes

**Configuración de traducción automática:**
```bash
# 1. Configurar API key
echo "GEMINI_API_KEY=tu_api_key_aqui" > .env

# 2. Verificar dependencias (instaladas automáticamente con make setup-images)
```

Más detalles en [AGENTS.md](AGENTS.md).

## Contenido

| Capítulo | Título | Estado Traducción | Img. Importadas | Img. Revisadas | Img. Traducidas |
|----------|--------|-------------------|-----------------|----------------|-----------------|
| 1 | Planeadores y Veleros | ✅ Revisado | 4 | ✅ | ✅ |
| 2 | Componentes y Sistemas | ✅ Revisado | 12 | ✅ | ✅ |
| 3 | Aerodinámica del Vuelo | ✅ Revisado | 23 | ✅ | ✅ |
| 4 | Instrumentos de Vuelo | ✅ Completado | 31 | ✅ | ✅ |
| 5 | Performance del Planeador | 📝 Borrador | 21 | ⏳ | ⏳ |
| 6 | Prevuelo y Operaciones en Tierra | 📝 Borrador | 17 | ⏳ | ⏳ |
| 7 | Lanzamiento, Aterrizaje y Maniobras | 📝 Borrador | 41 | ⏳ | ⏳ |
| 8 | Procedimientos de Emergencia | 📝 Borrador | 11 | ⏳ | ⏳ |
| 9 | Meteorología para Vuelo a Vela | 📝 Borrador | 30 | ⏳ | ⏳ |
| 10 | Técnicas de Vuelo a Vela | 📝 Borrador | 37 | ⏳ | ⏳ |
| 11 | Vuelo de Travesía | 📝 Borrador | 17 | ⏳ | ⏳ |
| 12 | Remolque | 📝 Borrador | 11 | ⏳ | ⏳ |
| 13 | Factores Humanos | 📝 Borrador | 13 | ⏳ | ⏳ |
| - | Glosario | 📝 Borrador | - | - | - |

**Progreso:** 4/13 capítulos revisados (31%) - 280/280 imágenes importadas (100%) - 83/280 imágenes traducidas (30%)

## Contribuir

Las contribuciones son bienvenidas. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para la guía completa.

### Proceso rápido:

1. Fork del repositorio
2. Crea una rama (`git checkout -b traduccion/capitulo-X`)
3. Realiza tus cambios siguiendo la guía de estilo
4. Actualiza el [CHANGELOG.md](CHANGELOG.md) si aplica
5. Envía un Pull Request

### Guía de Estilo

- Usar terminología del glosario (`es/apendices/glosario.adoc`)
- Para variantes regionales, editar `es/config/regiones/{código}.adoc`
- Mantener consistencia con capítulos ya traducidos
- Usar admonitions de AsciiDoc para avisos de seguridad:
  - `[WARNING]` para advertencias críticas
  - `[CAUTION]` para precauciones
  - `[NOTE]` para información adicional
  - `[TIP]` para consejos
- Seguir [Conventional Commits](https://www.conventionalcommits.org/) para mensajes de commit

## Licencia

### Obra original
La obra original (FAA Glider Flying Handbook) es un documento del gobierno federal de Estados Unidos y se encuentra en el **dominio público** según 17 U.S.C. § 105.

### Esta traducción
Esta traducción se distribuye bajo licencia [**Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC BY-SA 4.0)**](https://creativecommons.org/licenses/by-sa/4.0/deed.es).

Usted es libre de:
- **Compartir** — copiar y redistribuir el material
- **Adaptar** — remezclar, transformar y construir a partir del material

Bajo los términos de atribución y compartir igual.

### Nota sobre Contenido de Terceros
Algunas imágenes o diagramas del original pueden pertenecer a terceros (fabricantes, etc.) y tener derechos independientes. Cuando se ha identificado dicho contenido, se ha sustituido o se indica su origen.

## Contacto

- Web: [VuelaLibre.net](https://vuelalibre.net)
- Email: soporte@vuelalibre.net

---

⚠️ *Este manual es una traducción del documento oficial de la FAA. Para operación de aeronaves, consulte siempre la normativa vigente de su autoridad aeronáutica local y el manual oficial de su aeronave.*

<div align="center">
  <p>Construido con ❤️ y térmicas para la comunidad de <b>Vuelo a Vela</b>.</p>
</div>
