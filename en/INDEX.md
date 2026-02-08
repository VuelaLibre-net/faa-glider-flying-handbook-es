# FAA Glider Flying Handbook - English Source Content

> **Source:** FAA-H-8083-13B (Glider Flying Handbook)  
> **Language:** English (Original)  
> **License:** Public Domain (17 U.S.C. § 105)  
> **Purpose:** Source materials for ES↔EN translation project

---

## 📁 Directory Structure

```
en/
├── INDEX.md                          # This file - Directory guide for AI skills
├── TOC.md                            # Table of Contents (structured outline)
├── faa-glider-flying-handbook/       # Original PDF files from FAA
├── markdown/                         # Extracted content in Markdown format
├── text/                             # Plain text extractions
└── images/                           # Extracted figures and diagrams
```

---

## ⚠️ IMPORTANTE: Jerarquía de Títulos / Heading Hierarchy

> **FUENTE DE VERDAD ÚNICA:** `en/TOC.md`

### Reglas de Jerarquía para Traducción AsciiDoc

| Nivel | AsciiDoc | Fuente | Ejemplo |
|-------|----------|--------|---------|
| 1 (Capítulo) | `=` | `TOC.md` - Primer nivel | `= Planeadores y Veleros` |
| 2 (Sección) | `==` | `TOC.md` - Segundo nivel | `== Componentes y Sistemas` |
| 3 (Subsección) | `===` | `TOC.md` - Tercer nivel | `=== Empenaje` |
| 4+ | `====` `=====` | **NO está en TOC.md** | `==== Tipos de estabilidad` |

### ⚡ Regla Crítica

**Los títulos que aparezcan a lo largo del texto y que NO estén en `en/TOC.md` serán inferiores al nivel 3 (`====` o `=====` en AsciiDoc).**

```
❌ INCORRECTO:
== Tipos de Estabilidad  (Si no está en TOC.md)

✅ CORRECTO:
==== Tipos de Estabilidad  (Si no está en TOC.md)
```

### Verificación

Antes de asignar un nivel de título, **siempre consultar `en/TOC.md`**:

```bash
# Buscar el título en TOC.md
grep -i "tipos de estabilidad" en/TOC.md

# Si NO aparece → usar ==== o =====
# Si aparece → usar el nivel indicado en TOC.md
```

---

## 📂 Detailed Directory Descriptions

### 1. `faa-glider-flying-handbook/` - Original PDF Source Files

**Contents:** Official PDF documents from the FAA

| File | Description | Pages | Size |
|------|-------------|-------|------|
| `000-gfh-front-cover.pdf` | Front cover and title page | ~2 | 2.0 MB |
| `001-gfh-toc.pdf` | Table of contents | ~4 | 209 KB |
| `01-gliders-and-sailplanes.pdf` | Chapter 1: Gliders & Sailplanes | ~30 | 1.1 MB |
| `02-components-and-systems.pdf` | Chapter 2: Components & Systems | ~50 | 3.8 MB |
| `03-aerodynamics-of-flight.pdf` | Chapter 3: Aerodynamics | ~40 | 1.9 MB |
| `04-flight-instruments.pdf` | Chapter 4: Flight Instruments | ~80 | 4.3 MB |
| `05-glider-performance.pdf` | Chapter 5: Performance | ~50 | 2.4 MB |
| `06-preflight-and-ground-operations.pdf` | Chapter 6: Preflight & Ground Ops | ~60 | 4.1 MB |
| `07-launch-recovery-procedures-flight-maneuvers.pdf` | Chapter 7: Launch, Landing, Maneuvers | ~120 | 7.9 MB |
| `08-abnormal-and-emergency-procedures.pdf` | Chapter 8: Emergency Procedures | ~50 | 2.9 MB |
| `09-soaring-weather.pdf` | Chapter 9: Weather | ~80 | 5.8 MB |
| `10-soaring-techniques.pdf` | Chapter 10: Soaring Techniques | ~150 | 13.5 MB |
| `11-cross-country-soaring.pdf` | Chapter 11: Cross-Country | ~80 | 5.4 MB |
| `12-towing.pdf` | Chapter 12: Aerotow | ~40 | 2.5 MB |
| `13-human-factors.pdf` | Chapter 13: Human Factors | ~40 | 2.4 MB |
| `99-gfh-glossary.pdf` | Glossary | ~20 | 281 KB |
| `Glider-Flying-Handbook.pdf` | **Complete handbook** | ~280 | 55.9 MB |

**Use for Skills:**
- `/skill:pdf-anthropic` - Extract text, tables, images
- `/skill:docugenius-converter` - Convert PDF → Markdown
- `/skill:doctoagent` - Extract with image descriptions

---

### 2. `markdown/` - Markdown Extractions

**Contents:** Text content extracted from PDFs in Markdown format

| File | Chapter | Size | Lines (approx) |
|------|---------|------|----------------|
| `chapter-01.md` | Gliders & Sailplanes | 7.4 KB | ~200 |
| `chapter-02.md` | Components & Systems | 9.8 KB | ~300 |
| `chapter-03.md` | Aerodynamics | 29.8 KB | ~900 |
| `chapter-04.md` | Flight Instruments | 48.4 KB | ~1,400 |
| `chapter-05.md` | Performance | 38.3 KB | ~1,100 |
| `chapter-06.md` | Preflight & Ground Ops | 17.5 KB | ~500 |
| `chapter-07.md` | Launch, Landing, Maneuvers | 125.7 KB | ~3,500 |
| `chapter-08.md` | Emergency Procedures | 75.3 KB | ~2,100 |
| `chapter-09.md` | Weather | 67.0 KB | ~1,900 |
| `chapter-10.md` | Soaring Techniques | 63.1 KB | ~1,800 |
| `chapter-11.md` | Cross-Country | 56.7 KB | ~1,600 |
| `chapter-12.md` | Aerotow | 28.2 KB | ~800 |
| `chapter-13.md` | Human Factors | 39.5 KB | ~1,100 |

**Format:**
- Headers (`#`, `##`, `###`) for structure
- Figure references as `[Figure X-Y]`
- Safety warnings in **bold**
- Lists for procedures and checklists

**Use for Skills:**
- Reference for translation (ES↔EN)
- `/skill:md-exporter` - Convert to DOCX, PDF, etc.
- Content analysis and terminology extraction

---

### 3. `text/` - Plain Text Extractions

**Contents:** Raw text extracted from PDFs (minimal formatting)

| File | Content | Size |
|------|---------|------|
| `000.txt` | Front matter | 4.1 KB |
| `001.txt` | Table of contents | 46.7 KB |
| `01.txt` | Chapter 1 | 7.5 KB |
| `02.txt` | Chapter 2 | 10.1 KB |
| `03.txt` | Chapter 3 | 33.7 KB |
| `04.txt` | Chapter 4 | 54.0 KB |
| `05.txt` | Chapter 5 | 41.5 KB |
| `06.txt` | Chapter 6 | 18.0 KB |
| `07.txt` | Chapter 7 | 131.7 KB |
| `08.txt` | Chapter 8 | 77.2 KB |
| `09.txt` | Chapter 9 | 69.4 KB |
| `10.txt` | Chapter 10 | 66.0 KB |
| `11.txt` | Chapter 11 | 59.2 KB |
| `12.txt` | Chapter 12 | 29.1 KB |
| `13.txt` | Chapter 13 | 40.8 KB |
| `99.txt` | Glossary | 22.6 KB |

**Format Characteristics:**
- Figure captions start with numbers (e.g., "20904")
- Minimal markup
- Good for text analysis and word counting
- Preserves original line breaks from PDF

**Use for Skills:**
- Text analysis and terminology extraction
- Word frequency analysis
- Quick content searches

---

### 4. `images/` - Extracted Figures and Diagrams

**Contents:** Visual materials organized by chapter

```
images/
├── 000/              # Cover/title page images
├── 001/              # TOC diagrams
├── 01/               # Chapter 1 figures
│   └── extracted/    # Processed/extracted versions
├── 02/               # Chapter 2 figures
│   └── extracted/
├── ...
├── 13/               # Chapter 13 figures
│   └── extracted/
└── 99/               # Glossary diagrams
```

**Structure per Chapter:**
- `NN/` - Original extracted figures
- `NN/extracted/` - Processed/cleaned versions
- `NN/extracted/debug/` - Debug outputs (if applicable)

**Image Types:**
- Technical diagrams (aircraft systems)
- Flight maneuver illustrations
- Weather pattern diagrams
- Performance charts and graphs
- Cockpit instrument layouts

**Naming Convention:**
- Original: Various from PDF extraction
- Processed: `figure-NN-XX-description.png`

**Use for Skills:**
- Reference for image translation/editing
- `scripts/imagemanager/` - Process and translate images
- Cross-reference with text content

---

## 🎯 Recommended Skill Workflows

### Workflow 1: Extract New Content from PDFs
```bash
# Extract text with layout preservation
/skill:pdf-anthropic extract text from faa-glider-flying-handbook/05-glider-performance.pdf

# Or convert to editable Markdown
/skill:docugenius-converter convert en/faa-glider-flying-handbook/05-glider-performance.pdf
```

### Workflow 2: Analyze Terminology
```bash
# Extract technical terms from glossary
/skill:i18n-localization analyze terminology in en/text/99.txt

# Compare ES/EN terminology
/skill:i18n-localization check consistency between en/text/ and es/capitulos/
```

### Workflow 3: Translation Preparation
```bash
# Create translation plan for a chapter
/skill:plan-writing create plan to translate chapter 7 (launch procedures)

# Review translated content
/skill:copy-editing review es/capitulos/07-lanzamiento-aterrizaje-maniobras.adoc with 7 sweeps
```

### Workflow 4: Export for Reviewers
```bash
# Export Spanish chapter to Word for human review
/skill:md-exporter md_to_docx es/capitulos/07-lanzamiento-aterrizaje-maniobras.adoc
```

---

## 📊 Content Statistics

| Metric | Value |
|--------|-------|
| Total PDF chapters | 16 (including glossary) |
| Total Markdown files | 13 |
| Total text files | 16 |
| Total image directories | 16 |
| Approximate total words (EN) | ~150,000 |
| Figures and diagrams | ~200+ |

---

## 🔗 Cross-References

### Related Directories in Project
- `../es/` - Spanish translations (target language)
- `../es/capitulos/` - Translated AsciiDoc chapters
- `../es/imagenes/` - Translated/processed images
- `../es/apendices/glosario.adoc` - ES↔EN glossary
- `../temas/` - PDF/HTML themes and styling
- `../scripts/imagemanager/` - Image processing tools

### Key Files
- **`en/TOC.md`** - **SOURCE OF TRUTH for heading hierarchy** ⚠️
- `../es/config/atributos.adoc` - Global AsciiDoc attributes
- `../es/config/regiones/es.adoc` - Spain terminology variants
- `../es/config/regiones/ar.adoc` - Argentina terminology variants
- `../AGENTS.md` - Project guide for AI agents

---

## 📝 Notes for AI Skills

### Translation Priorities
1. **High Priority:** Safety warnings, emergency procedures (Chapter 8)
2. **High Priority:** Technical terminology (use `{term-XXX}` attributes)
3. **Medium Priority:** Descriptive content, explanations
4. **Low Priority:** Historical notes, supplementary information

### Critical Terminology (Always use attributes)
- `glider` → `{term-glider}` (planeador/velero)
- `stall` → `{term-stall}` (pérdida)
- `spin` → `{term-spin}` (barrena)
- `thermal` → `{term-thermal}` (térmica)
- `airbrake` → `{term-airbrake}` (aerofreno)
- `tow` → `{term-aerotow}` (remolque)

### Format Preservation
- Figure references: `Figure X-Y` → `<<fig-XX-YY,Figura X-Y>>`
- Safety admonitions: `[WARNING]`, `[CAUTION]`, `[IMPORTANT]`, `[NOTE]`
- Chapter anchors: `[[capNN]]`
- Section hierarchy: `= Title`, `== Section`, `=== Subsection`

### ⚠️ CRITICAL: Heading Hierarchy Rule

**`en/TOC.md` is the SINGLE SOURCE OF TRUTH for heading levels.**

Before assigning any heading level:
1. Check if the heading exists in `en/TOC.md`
2. If YES → Use the level shown in TOC (1, 2, or 3)
3. If NO → Use level 4 (`====`) or 5 (`=====`) ONLY

**Example:**
```asciidoc
# If "Types of Stability" is NOT in TOC.md:
==== Types of Stability    ← CORRECT (level 4)

# If "Types of Stability" IS in TOC.md at level 3:
=== Types of Stability     ← CORRECT (level 3)
```

**Verification command:**
```bash
grep -i "types of stability" en/TOC.md
```

---

## 🛠️ Technical Information

**Extraction Tools Used:**
- PDF text: `pdftotext`, custom scripts
- Markdown: Pandoc with custom filters
- Images: `pdfimages`, ImageMagick, custom Python scripts

**Encoding:** UTF-8
**Line Endings:** Unix (LF)

---

*Generated for AI Agent Skills - FAA Glider Flying Handbook Translation Project*
