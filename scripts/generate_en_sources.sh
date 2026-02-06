#!/bin/bash
# generate_en_sources.sh
# Genera fuentes de alta resolución (300 DPI) y extrae texto de los manuales PDF
# Estructura de salida:
#   en/images/XX/page-YY.png
#   en/text/XX.txt

set -e

SOURCE_DIR="faa-glider-flying-handbook"
TARGET_BASE="en"
DPI=300

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando generación de fuentes en alta resolución ($DPI DPI)...${NC}"

# Verificar herramientas
if ! command -v mutool &> /dev/null; then
    echo "❌ Error: 'mutool' no encontrado. Instala mupdf-tools."
    exit 1
fi

mkdir -p "$TARGET_BASE/images"
mkdir -p "$TARGET_BASE/text"

# Procesar cada PDF
for pdf in "$SOURCE_DIR"/*.pdf; do
    [ -e "$pdf" ] || continue
    
    filename=$(basename "$pdf")
    basename="${filename%.*}"
    # Extraer el número de capítulo (ej. "02-components..." -> "02")
    # Si no empieza por número, usar el basename completo
    if [[ $basename =~ ^[0-9]+ ]]; then
        chapter_dir=$(echo "$basename" | cut -d'-' -f1)
    else
        chapter_dir="$basename"
    fi

    echo -e "📄 Procesando: ${GREEN}$filename${NC} -> Capítulo $chapter_dir"

    # 1. Crear directorios
    mkdir -p "$TARGET_BASE/images/$chapter_dir"
    mkdir -p "$TARGET_BASE/text"

    # 2. Renderizar páginas (imágenes)
    # Evitar regenerar si ya existen (opcional, por ahora sobrescribimos para garantizar calidad)
    echo "   🖼️  Renderizando páginas..."
    mutool draw -o "$TARGET_BASE/images/$chapter_dir/page-%d.png" -r $DPI "$pdf"

    # 3. Extraer texto
    echo "   📝 Extrayendo texto..."
    mutool draw -F text "$pdf" > "$TARGET_BASE/text/${chapter_dir}.txt"
done

echo -e "${GREEN}✅ Proceso completado.${NC}"
echo "Recursos generados en folder '$TARGET_BASE/'"
