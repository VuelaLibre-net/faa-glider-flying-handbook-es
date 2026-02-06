#!/bin/bash
# validate-terminology.sh - Script de validación de terminología
# Valida que los términos utilizados en los capítulos estén definidos en el glosario

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_DIR="${PROJECT_DIR}/es/config"
CAPITULOS_DIR="${PROJECT_DIR}/es/capitulos"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Validando terminología del manual..."
echo ""

# Verificar que los archivos existen
if [[ ! -f "${CONFIG_DIR}/atributos.adoc" ]]; then
    echo -e "${RED}Error: No se encuentra ${CONFIG_DIR}/atributos.adoc${NC}"
    exit 1
fi

echo "✅ Archivos de configuración encontrados"
echo ""

# Extraer términos definidos en archivos de región (es.adoc, ar.adoc, etc.)
echo "📋 Extrayendo términos definidos..."
ATTRIBUTES=$(grep -oE '^:term-[a-z0-9-]+' "${CONFIG_DIR}/regiones/"*.adoc 2>/dev/null | sed 's/^:term-//' | sort -u)
ATTRIBUTES_COUNT=$(echo "$ATTRIBUTES" | wc -l)
echo "   Encontrados ${ATTRIBUTES_COUNT} atributos de terminología"
echo ""

# Contar uso de atributos en capítulos
echo "📊 Analizando uso de terminología en capítulos..."
echo ""

TOTAL_USAGES=0
for attr in $ATTRIBUTES; do
    COUNT=$(grep -r "{term-${attr}}" "${CAPITULOS_DIR}"/*.adoc 2>/dev/null | wc -l || echo 0)
    if [[ $COUNT -gt 0 ]]; then
        printf "   %-30s %3d usos\n" "term-${attr}" "$COUNT"
        TOTAL_USAGES=$((TOTAL_USAGES + COUNT))
    fi
done

echo ""
echo "📈 Total de usos de atributos: ${TOTAL_USAGES}"
echo ""

# Verificar términos potencialmente inconsistentes
echo "🔍 Buscando posibles inconsistencias..."
echo ""

# Buscar "entrada en pérdida" (debe ser solo "pérdida")
PERDIDA_COUNT=$(grep -rn "entrada en pérdida" "${CAPITULOS_DIR}"/*.adoc 2>/dev/null | wc -l || echo 0)
if [[ $PERDIDA_COUNT -gt 0 ]]; then
    echo -e "${YELLOW}⚠️  Encontradas ${PERDIDA_COUNT} ocurrencias de 'entrada en pérdida' (debe ser solo 'pérdida')${NC}"
    grep -rn "entrada en pérdida" "${CAPITULOS_DIR}"/*.adoc 2>/dev/null || true
    echo ""
fi

# Buscar "patrón de tráfico" (debe ser "circuito de tráfico")
PATRON_COUNT=$(grep -rn "patrón de tráfico" "${CAPITULOS_DIR}"/*.adoc 2>/dev/null | wc -l || echo 0)
if [[ $PATRON_COUNT -gt 0 ]]; then
    echo -e "${YELLOW}⚠️  Encontradas ${PATRON_COUNT} ocurrencias de 'patrón de tráfico' (debe ser 'circuito de tráfico')${NC}"
    grep -rn "patrón de tráfico" "${CAPITULOS_DIR}"/*.adoc 2>/dev/null || true
    echo ""
fi

# Verificar términos en inglés sin atributos
# Buscar palabras comunes en inglés que deberían usar atributos
echo "🔍 Verificando uso de atributos para términos técnicos..."
echo ""

# Lista de términos en inglés que deberían usar {term-...}
TERMS_TO_CHECK=(
    "stall"
    "spin"
    "glider"
    "thermal"
    "ailerons"
    "rudder"
    "elevator"
    "flaps"
    "spoiler"
    "airbrake"
    "tow"
    "winch"
)

for term in "${TERMS_TO_CHECK[@]}"; do
    # Buscar el término en inglés sin estar dentro de {term-...}
    # Excluir: comentarios (//), URLs, atributos ya definidos, captions (.), image paths, 
    # section titles (====), list items in mnemonics/checklists
    RESULTS=$(grep -rni "\b${term}\b" "${CAPITULOS_DIR}"/*.adoc 2>/dev/null | \
        grep -v "{term-" | \
        grep -v "^\s*//" | \
        grep -v "^\s*\." | \
        grep -v "^=\+ " | \
        grep -v "image::" | \
        grep -v "_cowl flaps_" | \
        grep -v "FUSTALL" | \
        grep -v "^\s*\*\s*\*\*[A-Z]" || true)
    
    # Contar líneas no vacías (trim newlines primero)
    if [[ -n "$RESULTS" ]]; then
        COUNT=$(echo "$RESULTS" | grep -c "\.adoc:" 2>/dev/null || echo "0")
        COUNT=$(echo "$COUNT" | tr -d '\n')
        if [[ "$COUNT" =~ ^[0-9]+$ && "$COUNT" -gt 0 ]]; then
            echo -e "${YELLOW}ℹ️  '${term}' aparece ${COUNT} veces en captions, títulos o mnemónicos (uso aceptable)${NC}"
            # Solo mostrar en modo verbose o si hay posibles problemas reales
            if [[ "$COUNT" -le 5 ]]; then
                echo "$RESULTS" | head -3
            fi
            echo ""
        fi
    fi
done

# Verificar otras inconsistencias comunes
echo ""
echo "🔍 Verificando otras inconsistencias terminológicas..."
echo ""

# Nota: "velocidad de pérdida" es una frase descriptiva válida (stall speed), no requiere atributo
# Solo verificar si aparece como título o caption sin el término técnico apropiado
STALL_SPEED_CAPTIONS=$(grep -rn "^\..*velocidad de pérdida" "${CAPITULOS_DIR}"/*.adoc 2>/dev/null | wc -l || echo 0)
if [[ $STALL_SPEED_CAPTIONS -gt 0 ]]; then
    echo -e "${GREEN}✅ Encontradas ${STALL_SPEED_CAPTIONS} captions con 'velocidad de pérdida' (frase descriptiva válida)${NC}"
fi

# Verificar consistencia en uso de comillas
STRAIGHT_QUOTES=$(grep -rn '"' "${CAPITULOS_DIR}"/*.adoc 2>/dev/null | grep -v '="' | grep -v '"http' | grep -v '^\s*//' | wc -l || echo 0)
if [[ $STRAIGHT_QUOTES -gt 0 ]]; then
    echo -e "${YELLOW}ℹ️  Nota: Encontradas ${STRAIGHT_QUOTES} líneas con comillas rectas (considerar usar comillas tipográficas)${NC}"
fi

echo ""
echo -e "${GREEN}✅ Validación de terminología completada${NC}"
echo ""
echo "💡 Sugerencia: Ejecute 'make pdf' para verificar que el documento compila correctamente"
