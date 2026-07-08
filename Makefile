# Makefile para Manual de Vuelo sin Motor
# Genera PDF, HTML y EPUB desde AsciiDoc

# === CONFIGURACIÓN ===
SHELL := /bin/bash
.DEFAULT_GOAL := help

# Directorios
SRC_DIR := es
BUILD_DIR := build
THEME_DIR := temas

# Variante regional (es=ar, mx, etc.)
REGION ?= es

# Archivo principal
MAIN_DOC := $(SRC_DIR)/manual-vuelo-sin-motor.adoc
BOOK_NAME := manual-vuelo-sin-motor

# Todos los archivos fuente .adoc (capítulos, config, apéndices)
SRC_FILES := $(wildcard $(SRC_DIR)/capitulos/*.adoc) \
             $(wildcard $(SRC_DIR)/config/*.adoc) \
             $(wildcard $(SRC_DIR)/apendices/*.adoc)

# Imágenes PNG (usadas en PDF)
PNG_IMAGES := $(wildcard $(SRC_DIR)/imagenes/*/*.png)

# Imágenes JPEG (también usadas en PDF)
JPEG_IMAGES := $(wildcard $(SRC_DIR)/imagenes/*/*.jpg) $(wildcard $(SRC_DIR)/imagenes/*/*.jpeg) $(wildcard $(SRC_DIR)/imagenes/*.jpeg)

# Todas las imágenes para el PDF
ALL_IMAGES := $(PNG_IMAGES) $(JPEG_IMAGES)

# Imágenes WebP (generadas desde PNG y JPEG para HTML)
WEBP_FROM_PNG := $(patsubst %.png,%.webp,$(PNG_IMAGES))
WEBP_FROM_JPEG := $(patsubst %.jpg,%.webp,$(filter %.jpg,$(JPEG_IMAGES))) $(patsubst %.jpeg,%.webp,$(filter %.jpeg,$(JPEG_IMAGES)))
WEBP_IMAGES := $(WEBP_FROM_PNG) $(WEBP_FROM_JPEG)

# Tema PDF
PDF_THEME := $(THEME_DIR)/pdf-theme.yml
CSS_THEME := $(THEME_DIR)/styles.css

# Comandos (usando bundle exec para gemset)
ASCIIDOCTOR := bundle exec asciidoctor
ASCIIDOCTOR_PDF := bundle exec asciidoctor-pdf
ASCIIDOCTOR_EPUB3 := bundle exec asciidoctor-epub3

# Opciones comunes
ASCIIDOCTOR_OPTS := -a data-uri -a allow-uri-read

# === TARGETS ===

.PHONY: all pdf html epub clean mrproper help setup check install validate watch

## Genera todos los formatos (PDF, HTML, EPUB)
all: pdf html epub

## Genera PDF para una región específica (ej: make pdf-ar REGION=ar)
pdf-ar:
	@$(MAKE) pdf REGION=ar

## Genera PDF para México (ej: make pdf-mx REGION=mx)
pdf-mx:
	@$(MAKE) pdf REGION=mx

## Valida la terminología utilizada en los capítulos
validate:
	@echo "🔍 Validando terminología..."
	@bash scripts/validate-terminology.sh
	@echo "✅ Validación completada"

## Genera el PDF con tema personalizado
pdf: $(BUILD_DIR)/pdf/$(BOOK_NAME).pdf

$(BUILD_DIR)/pdf/$(BOOK_NAME).pdf: $(MAIN_DOC) $(SRC_FILES) $(PDF_THEME) $(ALL_IMAGES)
	@echo "📄 Generando PDF..."
	@mkdir -p $(BUILD_DIR)/pdf
	@# Copiar archivos STEM existentes antes de generar (asciidoctor-mathematical los genera en $(SRC_DIR))
	@cp $(SRC_DIR)/stem-*.png $(SRC_DIR)/imagenes/ 2>/dev/null || true
	$(ASCIIDOCTOR_PDF) \
		$(ASCIIDOCTOR_OPTS) \
		-r asciidoctor-mathematical \
		-r ./scripts/figura-por-capitulo.rb \
		-r ./scripts/capitalize-terms.rb \
		-a pdf-theme=$(PDF_THEME) \
		-a pdf-fontsdir=GEM_FONTS_DIR \
		-a front-cover-image=imagenes/cover-beta.jpeg \
		-a title-page \
		-a toc \
		-a toclevels=3 \
		-a sectnumlevels=2 \
		-a lang=es \
		-a chapter-signifier=Capítulo \
		-a region=$(REGION) \
		-o $@ \
		$<
	@# Copiar archivos STEM generados durante el build a imagenes/ para futuras compilaciones
	@cp $(SRC_DIR)/stem-*.png $(SRC_DIR)/imagenes/ 2>/dev/null || true
	@echo "✅ PDF generado: $@"

## Genera el HTML multi-página (un archivo por capítulo)
html: $(MAIN_DOC) $(SRC_FILES) $(CSS_THEME) $(WEBP_IMAGES)
	@echo "🌐 Generando HTML multi-página..."
	@mkdir -p $(BUILD_DIR)/html
	@cp $(CSS_THEME) $(BUILD_DIR)/html/
	$(ASCIIDOCTOR) \
		$(ASCIIDOCTOR_OPTS) \
		-r asciidoctor-multipage \
		-b multipage_html5 \
		-a stylesheet=styles.css \
		-a linkcss \
		-D $(BUILD_DIR)/html \
		$<
	@echo "✅ HTML multi-página generado en: $(BUILD_DIR)/html/"

# Reglas para generar imágenes WebP desde PNG y JPEG
%.webp: %.png
	@echo "🖼️  Convirtiendo $< a WebP..."
	@convert "$<" -quality 90 "$@"
	@echo "✅ $@ generado"

%.webp: %.jpg
	@echo "🖼️  Convirtiendo $< a WebP..."
	@convert "$<" -quality 90 "$@"
	@echo "✅ $@ generado"

%.webp: %.jpeg
	@echo "🖼️  Convirtiendo $< a WebP..."
	@convert "$<" -quality 90 "$@"
	@echo "✅ $@ generado"

## Genera el EPUB
epub: $(BUILD_DIR)/epub/$(BOOK_NAME).epub

$(BUILD_DIR)/epub/$(BOOK_NAME).epub: $(MAIN_DOC) $(SRC_FILES)
	@echo "📱 Generando EPUB..."
	@mkdir -p $(BUILD_DIR)/epub
	$(ASCIIDOCTOR_EPUB3) \
		$(ASCIIDOCTOR_OPTS) \
		-a toc \
		-a toclevels=2 \
		-a source-highlighter=none \
		-o $@ \
		$<
	@echo "✅ EPUB generado: $@"


## Limpia los artefactos de build
clean:
	@echo "🧹 Limpiando archivos generados..."
	@rm -rf $(BUILD_DIR)
	@echo "✅ Limpieza completada"

## Limpia todo: artefactos de build + backups de imágenes + webp temporales
mrproper: clean
	@echo "🧹 Limpiando backups de imágenes..."
	@find $(SRC_DIR)/imagenes -type f \( -name '*.bak' -o -name '*.bak[0-9]*' -o -name '*~' -o -name '*.backup' -o -name '*.backup[0-9]*' -o -name '*.tmp' \) -exec rm -v {} + 2>/dev/null || true
	@echo "🧹 Limpiando imágenes WebP temporales..."
	@find $(SRC_DIR)/imagenes -type f -name '*.webp' ! -name 'mockup*.webp' ! -name 'cover-*.webp' -exec rm -v {} + 2>/dev/null || true
	@echo "✅ Limpieza completa (mrproper)"

## Verifica que las herramientas necesarias están instaladas
check:
	@echo "🔍 Verificando entorno y herramientas..."
	@echo ""
	@echo "📦 mise:"
	@mise --version 2>/dev/null || echo "⚠️  mise no instalado (ver https://mise.jdx.dev)"
	@echo ""
	@echo "📦 Ruby:"
	@ruby --version || (echo "❌ Ruby no instalado" && exit 1)
	@echo ""
	@echo "📚 Gemas Ruby (requeridas):"
	@$(ASCIIDOCTOR) --version 2>/dev/null | head -1 || echo "❌ asciidoctor no instalado"
	@$(ASCIIDOCTOR_PDF) --version 2>/dev/null | head -1 || echo "❌ asciidoctor-pdf no instalado"
	@$(ASCIIDOCTOR_EPUB3) --version 2>/dev/null | head -1 || echo "❌ asciidoctor-epub3 no instalado"
	@bundle list | grep -q asciidoctor-mathematical && echo "asciidoctor-mathematical: OK" || echo "❌ asciidoctor-mathematical no instalado (requerido para PDF)"
	@bundle list | grep -q asciidoctor-multipage && echo "asciidoctor-multipage: OK" || echo "❌ asciidoctor-multipage no instalado (requerido para HTML)"
	@echo ""
	@echo "🐍 Python (opcional, para gestor de imágenes):"
	@python3 --version 2>/dev/null || echo "⚠️  Python3 no disponible"
	@echo ""
	@echo "✅ Verificación completada"

## Instala las dependencias con Bundler
install:
	@echo "📦 Instalando dependencias con Bundler..."
	bundle install
	@echo "✅ Dependencias instaladas"

## Abre el gestor de imágenes (GUI desktop para comprimir/reemplazar)
images:
	@echo "🖼️  Iniciando gestor de imágenes..."
	@scripts/imagen_manager.sh

## Extrae activos (imágenes y texto) de los PDFs originales
extract:
	@echo "📦 Extrayendo activos en alta resolución..."
	@bash scripts/generate_en_sources.sh

## Configura el entorno virtual Python para el gestor de imágenes
setup-images:
	@echo "🔧 Configurando entorno virtual para el gestor de imágenes..."
	@scripts/setup-image-manager.sh

## Configura el entorno completo (mise + gemas)
setup:
	@echo "🔧 Configurando entorno Ruby con mise..."
	@mise --version >/dev/null 2>&1 || (echo "❌ mise no está instalado. Instálalo desde https://mise.jdx.dev" && exit 1)
	@echo "1. Confiando en configuración de mise..."
	@mise trust
	@echo "2. Instalando/verificando Ruby 3.3.5 con mise..."
	@mise install
	@echo "3. Instalando gemas..."
	@mise exec -- bundle install
	@echo ""
	@echo "✅ Entorno configurado"
	@echo ""
	@echo "Para activar el entorno en una nueva terminal:"
	@echo "  cd $(shell pwd) && mise activate"
	@echo ""
	@echo "O ejecuta comandos directamente con:"
	@echo "  mise exec -- make pdf"

## Observa cambios y regenera el PDF automáticamente
watch:
	@echo "👁️  Iniciando modo watch..."
	@echo "   Monitoreando: archivos .adoc e imágenes"
	@echo "   Presiona Ctrl+C para detener"
	@echo ""
	@which entr > /dev/null 2>&1 || (echo "❌ 'entr' no está instalado. Instálalo con: sudo apt-get install entr" && exit 1)
	@ls $(MAIN_DOC) $(SRC_FILES) $(ALL_IMAGES) 2>/dev/null | entr -r -c sh -c 'echo "📝 Cambio detectado, regenerando PDF..." && make pdf && echo "" && echo "✅ PDF actualizado: $(BUILD_DIR)/pdf/$(BOOK_NAME).pdf" && echo "   Presiona Ctrl+C para detener el watch"'

## Muestra esta ayuda
help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║     Manual de Vuelo sin Motor - Sistema de Build         ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Uso: make [target]"
	@echo ""
	@echo "Targets de generación:"
	@echo "  all          Genera todos los formatos (PDF, HTML, EPUB)"
	@echo "  pdf          Genera el PDF con tema personalizado"
	@echo "  html         Genera HTML multi-página (un archivo por capítulo)"
	@echo "  epub         Genera el EPUB"
	
	@echo ""
	@echo "Targets de mantenimiento:"
	@echo "  clean        Limpia los artefactos de build"
	@echo "  mrproper     Limpia todo (build + backups de imágenes)"
	@echo "  check        Verifica las herramientas instaladas"
	@echo "  install      Instala dependencias (bundle install dentro de mise)"
	@echo "  setup        Configura entorno completo (mise + gemas)"
	@echo "  validate     Valida terminología en capítulos"
	@echo "  watch        Observa cambios y regenera PDF automáticamente"
	@echo "  pdf-ar       Genera PDF con terminología argentina"
	@echo "  pdf-mx       Genera PDF con terminología mexicana"
	@echo ""
	@echo "Variables de entorno:"
	@echo "  REGION=es|ar|mx  Variante terminológica (default: es)"
	@echo "  help         Muestra esta ayuda"
	@echo ""
	@echo "Ejemplos:"
	@echo "  make setup   # Primera vez: configura todo"
	@echo "  make pdf     # Solo genera el PDF"
	@echo "  make all     # Genera PDF, HTML y EPUB"
	@echo "  make clean    # Elimina archivos de build"
	@echo "  make mrproper # Elimina build + backups de imágenes"
	@echo ""
	@echo "Requisitos:"
	@echo "  - mise (https://mise.jdx.dev)"
	@echo "  - Ruby 3.3.5 (gestionado por mise)"
	@echo "  - Bundler"
	@echo ""
