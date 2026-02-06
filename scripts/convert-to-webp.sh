#!/bin/bash
# Script para convertir imágenes a WebP (optimización para web)
# Mantiene las originales (PNG/JPEG) para uso en PDF

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IMAGES_DIR="$PROJECT_ROOT/es/imagenes"

echo "🖼️  Conversión de imágenes a WebP"
echo "================================"
echo ""

# Verificar que ImageMagick está instalado
if ! command -v convert &> /dev/null; then
    echo "❌ Error: ImageMagick no está instalado"
    echo "   Instala con: sudo apt-get install imagemagick"
    exit 1
fi

# Contadores
total=0
converted=0
skipped=0

# Procesar todas las imágenes
find "$IMAGES_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read -r img; do
    total=$((total + 1))
    
    # Obtener nombre sin extensión
    base="${img%.*}"
    webp="${base}.webp"
    
    # Verificar si ya existe WebP y es más reciente
    if [ -f "$webp" ] && [ "$webp" -nt "$img" ]; then
        echo "⏭️  Saltando: $(basename "$img") (WebP ya existe y está actualizado)"
        skipped=$((skipped + 1))
        continue
    fi
    
    # Convertir a WebP con calidad 90
    convert "$img" -quality 90 "$webp"
    
    # Mostrar estadísticas
    orig_size=$(stat -c%s "$img")
    webp_size=$(stat -c%s "$webp")
    reduction=$((100 - (webp_size * 100 / orig_size)))
    
    echo "✅ $(basename "$img") → $(basename "$webp") (${reduction}% menor)"
    converted=$((converted + 1))
done

echo ""
echo "================================"
echo "✅ Conversión completada"
echo "   Total procesadas: $total"
echo "   Convertidas: $converted"
echo "   Saltadas: $skipped"
echo ""
echo "💡 Las imágenes originales se mantienen para uso en PDF"
echo "   Las versiones WebP se usan para web/HTML"
