#!/usr/bin/env python3
"""
Convierte archivos Markdown (traducción revisada) a AsciiDoc con atributos de terminología.
"""

import re
import sys
from pathlib import Path

# Mapeo de términos a atributos (basado en es/config/regiones/es.adoc)
TERM_MAP = {
    # Aeronaves
    r'\bplaneador(es)?\b': r'{term-glider}\1',
    r'\bvelero(s)?\b': r'{term-sailplane}\1',
    r'\bmotovelero(s)?\b': r'{term-motorglider}\1',
    r'\bavión(es)? remolcador(es)?\b': r'{term-towplane}\1',
    
    # Componentes
    r'\balerón(es)?\b': r'{term-aileron}\1',
    r'\btimón(es)? de profundidad\b': r'{term-elevator}\1',
    r'\btimón(es)? de dirección\b': r'{term-rudder}\1',
    r'\bflap(s)?\b': r'{term-flap}\1',
    r'\baerofreno(s)?\b': r'{term-airbrake}\1',
    r'\bcompensador(es)?\b': r'{term-trim}\1',
    r'\bcarlinga(s)?\b': r'{term-canopy}\1',
    r'\bfuselaje(s)?\b': r'{term-fuselage}\1',
    r'\bala(s)?\b': r'{term-wing}\1',
    r'\bestabilizador(es)? horizontal(es)?\b': r'{term-tailplane}\1',
    r'\bestabilizador(es)? vertical(es)?\b': r'{term-fin}\1',
    
    # Vuelo
    r'\bpérdida(s)?\b': r'{term-stall}\1',
    r'\bbarrena(s)?\b': r'{term-spin}\1',
    r'\btérmica(s)?\b': r'{term-thermal}\1',
    r'\bascendencia(s)?\b': r'{term-lift}\1',
    r'\bsustentación\b': r'{term-lift-force}',
    r'\bresistencia\b': r'{term-drag}',
    r'\bempuje\b': r'{term-thrust}',
    r'\bángulo(s)? de ataque\b': r'{term-aoa}\1',
    r'\bviento relativo\b': r'{term-relative-wind}',
    r'\blínea(s)? de cuerda\b': r'{term-chord-line}',
    r'\bfineza\b': r'{term-glide-ratio}',
    r'\balargamiento\b': r'{term-aspect-ratio}',
    r'\bdiedro\b': r'{term-dihedral}',
    r'\bpeso\b': r'{term-weight}',
    
    # Instrumentos
    r'\baltímetro(s)?\b': r'{term-altimeter}\1',
    r'\banemómetro(s)?\b': r'{term-airspeed}\1',
    r'\baltitud de presión\b': r'{term-pressure-altitude}',
    r'\baltitud de densidad\b': r'{term-density-altitude}',
    r'\bvariómetro(s)?\b': r'{term-variometer}\1',
    r'\btemperatura exterior\b': r'{term-oat}',
    r'\binclinómetro(s)?\b': r'{term-inclinometer}\1',
    r'\bcomputador(es)? de vuelo\b': r'{term-flight-computer}\1',
    r'\bvelocidad indicada\b': r'{term-ias}',
    r'\bvelocidad calibrada\b': r'{term-cas}',
    r'\bvelocidad verdadera\b': r'{term-tas}',
    
    # Operaciones
    r'\binspección prevuelo\b': r'{term-preflight}',
    r'\bdespegue(s)?\b': r'{term-takeoff}\1',
    r'\baterrizaje(s)?\b': r'{term-landing}\1',
    r'\baproximación(es)?\b': r'{term-approach}\1',
    r'\bcircuito(s)? de tráfico\b': r'{term-pattern}\1',
    r'\btramo(s)? de viento en cola\b': r'{term-downwind}\1',
    r'\btramo(s)? base\b': r'{term-base}\1',
    r'\bfinal\b': r'{term-final}',
    r'\bredondeo\b': r'{term-flare}',
    r'\bcarrera de aterrizaje\b': r'{term-rollout}',
    
    # Remolque
    r'\bremolque(s)? aéreo(s)?\b': r'{term-aerotow}\1',
    r'\blanzamiento(s)? con torno\b': r'{term-winch-launch}\1',
    r'\bautolanzable(s)?\b': r'{term-self-launch}\1',
    r'\bcable(s)? de remolque\b': r'{term-tow-rope}\1',
    r'\beslabón(es)? fusible(s)?\b': r'{term-weak-link}\1',
    
    # Otros
    r'\bviento de cara\b': r'{term-headwind}',
    r'\bviento de cola\b': r'{term-tailwind}',
    r'\bviento cruzado\b': r'{term-crosswind}',
    r'\bvelocidad sobre el suelo\b': r'{term-groundspeed}',
    r'\blastre de agua\b': r'{term-water-ballast}',
    r'\bpolar(es)? de velocidades\b': r'{term-polar-curve}\1',
}

def convert_markdown_to_adoc(content, chapter_num):
    """Convierte contenido Markdown a AsciiDoc."""
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    frontmatter_done = False
    
    for line in lines:
        # Skip frontmatter
        if line.startswith('---') and not frontmatter_done:
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                in_frontmatter = False
                frontmatter_done = True
                continue
        
        if in_frontmatter:
            continue
        
        # Convertir títulos
        if line.startswith('# Capítulo'):
            # Ya tenemos el título en el capítulo
            continue
        elif line.startswith('## '):
            line = '= ' + line[3:]
        elif line.startswith('### '):
            line = '== ' + line[4:]
        elif line.startswith('#### '):
            line = '=== ' + line[5:]
        
        # Convertir figuras Markdown a AsciiDoc
        # Markdown: > **Figura X-Y:** Descripción
        fig_match = re.match(r'> \*\*Figura (\d+)-(\d+):\*\* (.+)', line)
        if fig_match:
            chap, num, desc = fig_match.groups()
            line = f'.{desc}\nimage::{chap.zfill(2)}/fig-{chap.zfill(2)}-{num.zfill(2)}.png[width=600]'
        
        # Convertir referencias a figuras
        # [Figura X-Y] -> <<fig-XX-YY>>
        line = re.sub(r'\[Figura (\d+)-(\d+)\]', r'<<fig-\1-\2>>', line)
        
        result.append(line)
    
    return '\n'.join(result)

def apply_terminology(text):
    """Aplica atributos de terminología al texto."""
    # Procesar en orden específico para evitar conflictos
    # Primero términos compuestos, luego simples
    sorted_patterns = sorted(TERM_MAP.items(), key=lambda x: len(x[0]), reverse=True)
    
    for pattern, replacement in sorted_patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def convert_file(md_path, adoc_path, chapter_num):
    """Convierte un archivo Markdown a AsciiDoc."""
    content = md_path.read_text(encoding='utf-8')
    
    # Convertir estructura Markdown a AsciiDoc
    adoc_content = convert_markdown_to_adoc(content, chapter_num)
    
    # Aplicar atributos de terminología
    adoc_content = apply_terminology(adoc_content)
    
    # Guardar
    adoc_path.write_text(adoc_content, encoding='utf-8')
    print(f"Convertido: {md_path} -> {adoc_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python md_to_adoc_converter.py <archivo_md> <archivo_adoc> <num_capitulo>")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    adoc_path = Path(sys.argv[2])
    chapter_num = sys.argv[3]
    
    convert_file(md_path, adoc_path, chapter_num)
