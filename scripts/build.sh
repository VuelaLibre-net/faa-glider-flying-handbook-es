#!/bin/bash
# Script de build para Manual de Vuelo sin Motor
# Genera PDF, HTML y EPUB desde AsciiDoc

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directorios
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_DIR/es"
BUILD_DIR="$PROJECT_DIR/build"
THEME_DIR="$PROJECT_DIR/temas"

# Archivos
MAIN_DOC="$SRC_DIR/manual-vuelo-planeador.adoc"
BOOK_NAME="manual-vuelo-planeador"
PDF_THEME="$THEME_DIR/pdf-theme.yml"
CSS_THEME="$THEME_DIR/styles.css"

# Funciones de utilidad
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar dependencias
check_dependencies() {
    log_info "Verificando dependencias..."
    
    local missing=0
    
    if ! command -v asciidoctor &> /dev/null; then
        log_error "asciidoctor no encontrado"
        missing=1
    else
        log_success "asciidoctor: $(asciidoctor --version | head -1)"
    fi
    
    if ! command -v asciidoctor-pdf &> /dev/null; then
        log_error "asciidoctor-pdf no encontrado"
        missing=1
    else
        log_success "asciidoctor-pdf: $(asciidoctor-pdf --version | head -1)"
    fi
    
    if ! command -v asciidoctor-epub3 &> /dev/null; then
        log_warning "asciidoctor-epub3 no encontrado (EPUB no disponible)"
    else
        log_success "asciidoctor-epub3: instalado"
    fi
    
    if [ $missing -eq 1 ]; then
        log_error "Faltan dependencias. Ejecuta: gem install asciidoctor asciidoctor-pdf asciidoctor-epub3"
        exit 1
    fi
}

# Generar PDF
build_pdf() {
    log_info "Generando PDF..."
    mkdir -p "$BUILD_DIR/pdf"
    
    asciidoctor-pdf \
        -a data-uri \
        -a allow-uri-read \
        -a pdf-theme="$PDF_THEME" \
        -a pdf-fontsdir=GEM_FONTS_DIR \
        -a title-page \
        -a toc \
        -a toclevels=3 \
        -o "$BUILD_DIR/pdf/$BOOK_NAME.pdf" \
        "$MAIN_DOC"
    
    log_success "PDF generado: $BUILD_DIR/pdf/$BOOK_NAME.pdf"
}

# Generar HTML
build_html() {
    log_info "Generando HTML..."
    mkdir -p "$BUILD_DIR/html"
    
    asciidoctor \
        -a data-uri \
        -a allow-uri-read \
        -a stylesheet="$CSS_THEME" \
        -a linkcss! \
        -a toc=left \
        -a toclevels=3 \
        -a sectanchors \
        -a sectlinks \
        -o "$BUILD_DIR/html/$BOOK_NAME.html" \
        "$MAIN_DOC"
    
    cp "$CSS_THEME" "$BUILD_DIR/html/"
    
    log_success "HTML generado: $BUILD_DIR/html/$BOOK_NAME.html"
}

# Generar EPUB
build_epub() {
    if ! command -v asciidoctor-epub3 &> /dev/null; then
        log_warning "asciidoctor-epub3 no disponible, saltando EPUB"
        return
    fi
    
    log_info "Generando EPUB..."
    mkdir -p "$BUILD_DIR/epub"
    
    asciidoctor-epub3 \
        -a data-uri \
        -a allow-uri-read \
        -a toc \
        -a toclevels=2 \
        -o "$BUILD_DIR/epub/$BOOK_NAME.epub" \
        "$MAIN_DOC"
    
    log_success "EPUB generado: $BUILD_DIR/epub/$BOOK_NAME.epub"
}

# Limpiar
clean() {
    log_info "Limpiando archivos generados..."
    rm -rf "$BUILD_DIR"
    log_success "Limpieza completada"
}

# Mostrar ayuda
show_help() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║     Manual de Vuelo sin Motor - Script de Build          ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos:"
    echo "  all      Genera todos los formatos (PDF, HTML, EPUB)"
    echo "  pdf      Genera solo el PDF"
    echo "  html     Genera solo el HTML"
    echo "  epub     Genera solo el EPUB"
    echo "  clean    Elimina archivos generados"
    echo "  check    Verifica dependencias"
    echo "  help     Muestra esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 pdf     # Solo genera el PDF"
    echo "  $0 all     # Genera todos los formatos"
    echo ""
}

# Main
main() {
    cd "$PROJECT_DIR"
    
    case "${1:-all}" in
        all)
            check_dependencies
            build_pdf
            build_html
            build_epub
            echo ""
            log_success "¡Build completado!"
            echo ""
            echo "Archivos generados:"
            echo "  📄 PDF:  $BUILD_DIR/pdf/$BOOK_NAME.pdf"
            echo "  🌐 HTML: $BUILD_DIR/html/$BOOK_NAME.html"
            echo "  📱 EPUB: $BUILD_DIR/epub/$BOOK_NAME.epub"
            ;;
        pdf)
            check_dependencies
            build_pdf
            ;;
        html)
            check_dependencies
            build_html
            ;;
        epub)
            check_dependencies
            build_epub
            ;;
        clean)
            clean
            ;;
        check)
            check_dependencies
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Comando desconocido: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
