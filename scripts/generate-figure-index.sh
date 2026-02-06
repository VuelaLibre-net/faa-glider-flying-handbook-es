#!/bin/bash
# Genera índice de figuras para el manual
# Extrae anclas [[fig-CC-NN]] y títulos de figuras de los capítulos

OUTPUT="es/apendices/indice-figuras.adoc"

mkdir -p es/apendices

cat > "$OUTPUT" << 'HEADER'
[[indice-figuras]]
= Índice de Figuras

Este apéndice lista todas las figuras del manual organizadas por capítulo.

HEADER

# Procesar cada capítulo
for cap in es/capitulos/*.adoc; do
    cap_num=$(basename "$cap" | sed 's/^0*//' | sed 's/-.*//')
    cap_name=$(basename "$cap" .adoc | sed 's/^[0-9]*-//' | tr '-' ' ' | sed 's/.*/\u&/')
    
    # Verificar si hay figuras en este capítulo
    fig_count=$(grep -c "\[\[fig-$(printf "%02d" $cap_num)-" "$cap" 2>/dev/null || echo "0")
    
    if [ "$fig_count" -gt 0 ]; then
        echo "== Capítulo $cap_num: ${cap_name}" >> "$OUTPUT"
        echo "" >> "$OUTPUT"
        
        # Extraer figuras de este capítulo
        grep -E "^\[\[fig-$(printf "%02d" $cap_num)-[0-9]+\]\]$" "$cap" | while read -r anchor_line; do
            anchor=$(echo "$anchor_line" | tr -d '[]')
            fig_num=$(echo "$anchor" | sed 's/fig-//')
            
            # Buscar el título de la figura (línea siguiente que empiece con .)
            title=$(grep -A1 "^\[\[$anchor\]\]$" "$cap" | grep "^\." | head -1 | sed 's/^\.//' | xargs)
            
            # Si no hay título, buscar en líneas anteriores
            if [ -z "$title" ]; then
                title=$(grep -B1 "^\[\[$anchor\]\]$" "$cap" | grep "^\." | head -1 | sed 's/^\.//' | xargs)
            fi
            
            if [ -n "$title" ]; then
                echo "* <<$anchor,Figura $fig_num>>: $title" >> "$OUTPUT"
            fi
        done
        
        echo "" >> "$OUTPUT"
    fi
done

echo "✅ Índice de figuras generado: $OUTPUT ($fig_count figuras)"
