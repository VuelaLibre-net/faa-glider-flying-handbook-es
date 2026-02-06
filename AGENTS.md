# AGENTS.md - Guía para Agentes de IA

## Manual de Vuelo sin Motor

> **Versión:** 0.1.1  
> **Idioma:** Español (con variantes regionales)  
> **Formato:** AsciiDoc  
> **Licencia Traducción:** CC BY-SA 4.0  

---

## 1. Visión General del Proyecto

Este proyecto es una **traducción técnica 1:1** del *FAA Glider Flying Handbook* (FAA-H-8083-13B) del inglés al español. La obra original de la FAA está en **dominio público** (17 U.S.C. § 105).

**Objetivo:** Proporcionar una traducción fiel y completa del manual oficial de la FAA para pilotos de planeador, utilizando terminología aeronáutica estándar en español con variantes regionales para España y Latinoamérica.

**Formatos de salida:**
- PDF (A4, optimizado para impresión)
- HTML (multi-página, optimizado para web)
- EPUB (lectores electrónicos)

---

## 2. Arquitectura del Proyecto

### 2.1 Estructura de Directorios

```
.
├── es/                                    # Contenido en español
│   ├── manual-vuelo-sin-motor.adoc        # Documento maestro (entry point)
│   ├── capitulos/                         # 13 capítulos (01-13)
│   │   ├── 01-planeadores-y-veleros.adoc
│   │   ├── 02-componentes-y-sistemas.adoc
│   │   ├── 03-aerodinamica-del-vuelo.adoc
│   │   ├── 04-instrumentos-de-vuelo.adoc
│   │   ├── 05-performance.adoc
│   │   ├── 06-prevuelo-operaciones-tierra.adoc
│   │   ├── 07-lanzamiento-aterrizaje-maniobras.adoc
│   │   ├── 08-emergencias.adoc
│   │   ├── 09-meteorologia-vuelo-vela.adoc
│   │   ├── 10-tecnicas-vuelo-vela.adoc
│   │   ├── 11-vuelo-travesia.adoc
│   │   ├── 12-remolque.adoc
│   │   └── 13-factores-humanos.adoc
│   ├── config/                            # Configuración
│   │   ├── atributos.adoc                 # Variables globales y selector regional
│   │   └── regiones/                      # Variantes terminológicas
│   │       ├── es.adoc                    # España - default
│   │       ├── ar.adoc                    # Argentina
│   │       └── mx.adoc                    # México (placeholder)
│   ├── apendices/                         # Apéndices
│   │   ├── glosario.adoc                  # Glosario ES↔EN completo
│   │   └── indice-figuras.adoc            # Índice de figuras
│   └── imagenes/                          # Imágenes por capítulo
│       ├── 01/                            # Figuras capítulo 1
│       ├── 02/
│       └── ... (hasta 13)
├── temas/                                 # Temas de estilo
│   ├── pdf-theme.yml                      # Tema PDF (A4, colores aviación)
│   ├── styles.css                         # Estilos HTML
│   └── locales/es.yml                     # Localización española
├── scripts/                               # Scripts de automatización
│   ├── figura-por-capitulo.rb             # Extensión Ruby: numeración figuras X-Y
│   ├── validate-terminology.sh            # Validación de terminología
│   ├── imagen_manager.sh                  # Lanzador del gestor de imágenes
│   ├── setup-image-manager.sh             # Setup entorno Python
│   ├── generate-placeholder.py            # Generación de placeholders
│   ├── fix-crossreferences.py             # Corrección de referencias cruzadas
│   └── imagemanager/                      # Gestor de imágenes v3.0 (Python)
│       ├── __init__.py
│       ├── config.py                      # Configuración global
│       ├── clipboard_handler.py           # Manejo de portapapeles multiplataforma
│       ├── translation.py                 # Traducción con Google Gemini
│       ├── image_processor.py             # Procesamiento de imágenes
│       ├── file_manager.py                # Gestión de archivos y capítulos
│       ├── figure_detector.py             # Detector de figuras con IA
│       ├── main.py                        # Punto de entrada
│       └── ui/                            # Interfaz gráfica
│           ├── __init__.py
│           ├── main_window_v2.py          # Ventana principal (diseño moderno)
│           ├── image_editor.py            # Editor con etiquetado tipo «badges»
│           ├── translation_dialog.py      # Diálogos de traducción
│           └── themes.py                  # Temas visuales de la UI
├── faa-glider-flying-handbook/            # PDFs originales FAA (fuente)
├── en/                                    # Contenido original en inglés
│   ├── images/                            # Imágenes originales
│   ├── markdown/                          # Texto en Markdown
│   └── text/                              # Texto plano extraído
├── build/                                 # Archivos generados (gitignored)
├── Gemfile                                # Dependencias Ruby
├── Gemfile.lock                           # Lock de gemas
├── Makefile                               # Automatización de build
├── .ruby-version                          # Ruby 3.3.5
├── .ruby-gemset                           # Gemset: faa-gfh
├── .python-version                        # Python: faa-gfh-images (pyenv)
└── .env                                   # Variables de entorno (API keys)
```

### 2.2 Stack Tecnológico

#### Ruby (Document Processing)

| Gema | Versión | Uso |
|------|---------|-----|
| `asciidoctor` | ~> 2.0 | Motor AsciiDoc |
| `asciidoctor-pdf` | ~> 2.3 | Convertidor PDF |
| `asciidoctor-epub3` | ~> 2.1 | Convertidor EPUB |
| `asciidoctor-mathematical` | ~> 0.3 | Renderizado de ecuaciones STEM |
| `asciidoctor-diagram` | ~> 2.3 | Diagramas técnicos |
| `asciidoctor-multipage` | ~> 0.0 | HTML multi-página |
| `rouge` | ~> 4.0 | Resaltado de sintaxis |
| `base64` | - | Compatibilidad Ruby 3.4+ |

#### Python (Image Manager v3.0)

| Paquete | Versión | Uso |
|---------|---------|-----|
| `Pillow` | Última | Procesamiento de imágenes |
| `google-genai` | Última | Integración con Gemini API |
| `python-dotenv` | Última | Carga de variables de entorno |
| `pyperclip` | Última | Manejo de portapapeles |
| `tkinterdnd2` | Última | Drag & drop (opcional) |

---

## 3. Comandos de Build

### 3.1 Setup Inicial

```bash
# Configurar entorno Ruby completo
make setup

# O manualmente:
rvm use 3.3.5@faa-gfh
bundle install

# Configurar entorno Python para Image Manager
make setup-images
```

### 3.2 Generación de Documentos

```bash
make all              # Genera todos los formatos (PDF, HTML, EPUB)
make pdf              # Solo PDF (terminología española por defecto)
make pdf REGION=ar    # PDF con terminología argentina
make pdf-ar           # Atajo para Argentina
make pdf-mx           # Atajo para México
make html             # HTML multi-página (un archivo por capítulo)
make epub             # Solo EPUB
```

### 3.3 Mantenimiento y Validación

```bash
make clean            # Limpia archivos generados
make check            # Verifica herramientas instaladas
make install          # Instala dependencias (bundle install)
make validate         # Valida terminología en capítulos
make watch            # Observa cambios y regenera PDF automáticamente
```

### 3.4 Gestión de Imágenes

```bash
make images           # Abre el gestor de imágenes (GUI)
make setup-images     # Configura entorno Python para el gestor
make extract          # Extrae activos de los PDFs originales FAA
```

---

## 4. Convenciones de Código

### 4.1 Estructura de Capítulos (AsciiDoc)

Cada capítulo sigue esta estructura obligatoria:

```asciidoc
[[capNN]]                           # Ancla obligatoria (ej: [[cap01]])
= Título del Capítulo              # Título nivel 1

[abstract]                         # Resumen del capítulo (obligatorio)
--
Texto del resumen...
--

== Primera Sección                 # Sección nivel 2

=== Subsección                    # Nivel 3

==== Sub-subsección               # Nivel 4 (máximo)
```

### 4.2 Referencias Cruzadas

```asciidoc
<<cap02,Capítulo 2>>               # Referencia a capítulo
<<glosario,Glosario>>              # Referencia al glosario
<<fig-01-01,Figura 1-1>>           # Referencia a figura
<<tab-03-05>>                      # Referencia a tabla
```

### 4.3 Imágenes y Figuras

```asciidoc
[[fig-NN-XX]]                      # Ancla de figura obligatoria
.Título descriptivo               # Caption
image::NN/nombre-archivo.png["Texto alt", width=600]
```

**Convenciones de nomenclatura de imágenes:**
- Directorio: `es/imagenes/NN/` (NN = número de capítulo, 2 dígitos)
- Formato: `figura-NN-descripcion.png`
- Dual format: PNG (para PDF) + WebP (para web)

### 4.4 Admonitions (Avisos de Seguridad)

```asciidoc
[WARNING]                          # Advertencia crítica de seguridad
====
Texto de advertencia importante (ej: nunca exceder VNE)
====

[CAUTION]                          # Precaución
====
Texto de precaución (ej: revisar gancho de remolque)
====

[IMPORTANT]                        # Información importante
====
Notas o advertencias específicas del manual original FAA.
====

[NOTE]                             # Información adicional
====
Texto de información complementaria.
====

[TIP]                              # Consejo práctico
====
Recomendación o mejor práctica.
====
```

### 4.5 Terminología con Atributos

Usar atributos AsciiDoc para términos técnicos (definidos en `es/config/regiones/es.adoc`):

```asciidoc
La {term-thermal} permite...         # Resultado: "La térmica permite..."
El {term-stall} ocurre cuando...     # Resultado: "El pérdida ocurre..." ⚠️
```

**Términos estandarizados (España):**

| Inglés | Español | Atributo |
|--------|---------|----------|
| Glider | planeador | `{term-glider}` |
| Sailplane | velero | `{term-sailplane}` |
| Stall | pérdida | `{term-stall}` |
| Spin | barrena | `{term-spin}` |
| Thermal | térmica | `{term-thermal}` |
| Airbrake/Spoiler | aerofreno | `{term-airbrake}` |
| Flap | flap | `{term-flap}` |
| Lift (fuerza) | sustentación | `{term-lift-force}` |
| Lift (corriente) | ascendencia | `{term-lift}` |
| Tow | remolque | `{term-aerotow}` |
| Winch launch | lanzamiento con torno | `{term-winch-launch}` |
| Traffic pattern | circuito de tráfico | `{term-pattern}` |
| Downwind | tramo de viento en cola | `{term-downwind}` |
| Yaw string | lanita | `{term-yaw-string}` |

---

## 5. Gestión de Versiones

La versión del proyecto se define en **tres archivos** que deben mantenerse sincronizados:

| Archivo | Atributo | Ejemplo |
|---------|----------|---------|
| `es/manual-vuelo-sin-motor.adoc` | `:revnumber:` | `:revnumber: 0.1.1` |
| `es/config/atributos.adoc` | `:project-version:` | `:project-version: 0.1.1` |
| `README.md` | Badge | `version-0.1.1-blue` |

**Formato:** `MAJOR.MINOR.PATCH[-prerelease]`

---

## 6. Gestor de Imágenes v3.0

### 6.1 Arquitectura

Aplicación GUI modular escrita en Python 3.13+ con tkinter:

```
scripts/imagemanager/
├── config.py              # Configuración global y constantes
├── clipboard_handler.py   # Abstracción de portapapeles (Linux/Win/Mac)
├── translation.py         # Cliente Google Gemini API
├── image_processor.py     # Compresión y procesamiento PIL
├── file_manager.py        # Gestión de archivos y capítulos
├── figure_detector.py     # Detección de figuras con IA
├── main.py                # Punto de entrada
└── ui/
    ├── main_window_v2.py  # Ventana principal (sidebar + toolbar)
    ├── image_editor.py    # Editor visual con badges
    ├── translation_dialog.py  # UI de traducción
    └── themes.py          # Sistema de temas visuales
```

### 6.2 Funcionalidades

- **Compresión PNG:** Cuantización de colores + optimización
- **Traducción automática:** Integración con Google Gemini para traducir texto en imágenes
- **Editor visual:** Añadir badges/títulos a imágenes
- **Gestión de capítulos:** Organización por capítulos 01-13
- **Clipboard:** Soporte para pegar desde capturas de pantalla

### 6.3 Configuración de Traducción

Requiere archivo `.env` en la raíz:

```
GEMINI_API_KEY=tu_api_key_aqui
```

Modelos soportados:
- `gemini-2.5-flash-image` - Rápido y económico
- `gemini-3-pro-image-preview` - Mayor calidad

---

## 7. Extensión Ruby: Numeración de Figuras

El archivo `scripts/figura-por-capitulo.rb` es una extensión del convertidor PDF de Asciidoctor que implementa numeración por capítulo en formato **Figura X-Y** (igual que el manual original FAA).

**Características:**
- Las figuras se numeran secuencialmente dentro de cada capítulo
- El número de capítulo reinicia el contador de figuras
- Formato: `Figura {capítulo}-{figura}. Caption text`
- Modifica el comportamiento de `convert_image` y `convert_inline_anchor`

---

## 8. Validación de Terminología

El script `scripts/validate-terminology.sh` realiza las siguientes verificaciones:

1. **Cuenta de atributos usados:** Estadísticas de uso de `{term-...}` en capítulos
2. **Inconsistencias comunes:**
   - Detecta «entrada en pérdida» (debe ser «pérdida»)
   - Detecta «patrón de tráfico» (debe ser «circuito de tráfico»)
3. **Términos en inglés sin atributos:** Verifica términos que deberían usar `{term-...}`

---

## 9. Checklist de Calidad

Antes de marcar una tarea como completada:

- [ ] **Validación Terminológica:** `make validate` sin errores
- [ ] **Compilación PDF:** `make pdf` termina exitosamente
- [ ] **Referencias Cruzadas:** Todos los enlaces `<<...>>` son navegables
- [ ] **Admonitions:** WARNING, CAUTION, IMPORTANT renderizan correctamente
- [ ] **Admonitions:** Bloques IMPORTANT, WARNING, CAUTION renderizan correctamente
- [ ] **Imágenes:** Formatos PNG (PDF) y WebP (web) generados

---

## 10. Reglas de Oro para Agentes

1. **Validar Antes de Confirmar:** Nunca marques una tarea como completada sin ejecutar `make validate` y `make pdf`
2. **No Inventar:** Si un término no está en el glosario, **NO** lo traduzcas libremente. Consulta `es/apendices/glosario.adoc`
3. **Respetar la Estructura:** No modifiques nombres de archivos ni estructura de carpetas
4. **No Eliminar Anclas:** Nunca elimines etiquetas de anclaje `[[...]]`
5. **No Traducir Flap:** El término «flap» se mantiene en inglés
6. **Mantener PNGs:** Nunca borres PNGs originales (se necesitan para PDF)
7. **Capitalización de Títulos (Español):** En español, los títulos usan **mayúscula inicial solo en la primera palabra** (estilo oración), excepto nombres propios:
   - ✓ `== Despegue normal`
   - ✓ `== La atmósfera`
   - ✓ `== Programa FAA WINGS` (nombres propios)
   - ✗ `== Despegue Normal`
   - ✗ `== La Atmósfera`

---

## 11. Recursos

### Documentación del Proyecto
- **Glosario:** `es/apendices/glosario.adoc`
- **Atributos globales:** `es/config/atributos.adoc`
- **Terminología regional:** `es/config/regiones/{es,ar}.adoc`
- **README:** `README.md`
- **CHANGELOG:** `CHANGELOG.md`
- **CONTRIBUTING:** `CONTRIBUTING.md`

### Documentación Técnica
- **AsciiDoc Syntax:** https://docs.asciidoctor.org/asciidoc/latest/
- **Asciidoctor PDF:** https://docs.asciidoctor.org/pdf-converter/latest/

### Recursos de Aviación
- **FAA Glider Flying Handbook:** Manual original (FAA-H-8083-13B)
- **Glossary of Aeronautical Terms:** Referencia terminológica FAA

---

## 12. Contacto

- **Web:** https://vuelalibre.net
- **Email:** soporte@vuelalibre.net
- **GitHub:** https://github.com/VuelaLibre-net/faa-glider-flying-handbook-es

---

**Nota:** Este manual es una traducción del documento oficial de la FAA. Para operación de aeronaves, consulte siempre la normativa vigente de su autoridad aeronáutica local.
