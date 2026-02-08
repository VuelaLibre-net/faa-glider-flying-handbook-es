#!/usr/bin/env python3
"""
Convierte archivos Markdown (traducción revisada) a AsciiDoc con atributos de terminología.
Versión 2 - Mejorada
"""

import re
import sys
from pathlib import Path

def get_chapter_info(md_file):
    """Obtiene información del capítulo desde el archivo Markdown."""
    content = md_file.read_text(encoding='utf-8')
    
    # Extraer número de capítulo del nombre de archivo
    match = re.search(r'chapter-(\d+)\.md', md_file.name)
    if match:
        chapter_num = int(match.group(1))
    else:
        chapter_num = 0
    
    # Extraer título del capítulo
    title_match = re.search(r'^# Capítulo \d+: (.+)$', content, re.MULTILINE)
    if title_match:
        chapter_title = title_match.group(1)
    else:
        # Buscar en frontmatter
        fm_match = re.search(r'^title: "(.+)"', content, re.MULTILINE)
        if fm_match:
            chapter_title = fm_match.group(1)
        else:
            chapter_title = f"Capítulo {chapter_num}"
    
    return chapter_num, chapter_title

def convert_content(content, chapter_num, chapter_title):
    """Convierte el contenido Markdown a AsciiDoc."""
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    frontmatter_done = False
    
    # Agregar ancla del capítulo
    result.append(f'[[cap{chapter_num:02d}]]')
    result.append(f'= {chapter_title}')
    result.append('')
    
    for line in lines:
        # Skip frontmatter
        if line.startswith('---'):
            if not in_frontmatter and not frontmatter_done:
                in_frontmatter = True
                continue
            elif in_frontmatter:
                in_frontmatter = False
                frontmatter_done = True
                continue
        
        if in_frontmatter:
            continue
        
        # Skip title line (already added)
        if re.match(r'^# Capítulo \d+:', line):
            continue
        
        # Convertir títulos - ajustar nivel
        if line.startswith('## '):
            line = '== ' + line[3:]
        elif line.startswith('### '):
            line = '=== ' + line[4:]
        elif line.startswith('#### '):
            line = '==== ' + line[5:]
        elif line.startswith('##### '):
            line = '===== ' + line[6:]
        
        # Convertir figuras Markdown a AsciiDoc con ancla
        fig_match = re.match(r'> \*\*Figura (\d+)-(\d+):\*\* (.+)', line)
        if fig_match:
            chap, num, desc = fig_match.groups()
            chap_padded = chap.zfill(2)
            num_padded = num.zfill(2)
            result.append(f'[[fig-{chap_padded}-{num_padded}]]')
            result.append(f'.{desc}')
            # Intentar encontrar el nombre de archivo de imagen existente
            result.append(f'image::{chap_padded}/fig-{chap_padded}-{num_padded}.*[width=600]')
            continue
        
        # Convertir referencias a figuras
        line = re.sub(r'\[Figura (\d+)-(\d+)\]', r'<<fig-\1-\2>>', line)
        
        # Aplicar atributos de terminología (orden: términos compuestos primero)
        line = apply_terminology(line)
        
        result.append(line)
    
    return '\n'.join(result)

def apply_terminology(text):
    """Aplica atributos de terminología al texto."""
    # Lista ordenada por prioridad (términos compuestos primero)
    replacements = [
        # Términos compuestos (ordenados por longitud)
        (r'\bvelocidad de mínimo descenso\b', r'{term-min-sink}'),
        (r'\bvelocidad de mejor planeo\b', r'{term-best-glide}'),
        (r'\bremolque(s)? aéreo(s)?\b', r'{term-aerotow}\1'),
        (r'\bvuelo coordinado\b', r'{term-coordinated-flight}'),
        (r'\baterrizaje(s)? fuera de campo\b', r'{term-off-field-landing}\1'),
        (r'\bavión(es)? remolcador(es)?\b', r'{term-towplane}\1'),
        (r'\bcable(s)? de remolque\b', r'{term-tow-rope}\1'),
        (r'\beslabón(es)? fusible(s)?\b', r'{term-weak-link}\1'),
        (r'\bestabilizador(es)? horizontal(es)?\b', r'{term-tailplane}\1'),
        (r'\bestabilizador(es)? vertical(es)?\b', r'{term-fin}\1'),
        (r'\btimón(es)? de profundidad\b', r'{term-elevator}\1'),
        (r'\btimón(es)? de dirección\b', r'{term-rudder}\1'),
        (r'\bala(s)? izquierda(s)?\b', r'{term-wing} izquierda\1'),
        (r'\bala(s)? derecha(s)?\b', r'{term-wing} derecha\1'),
        (r'\btramo(s)? de viento en cola\b', r'{term-downwind}\1'),
        (r'\btramo(s)? base\b', r'{term-base}\1'),
        (r'\bcarrera de aterrizaje\b', r'{term-rollout}'),
        (r'\binspección prevuelo\b', r'{term-preflight}'),
        (r'\bcircuito(s)? de tráfico\b', r'{term-pattern}\1'),
        (r'\bcomputador(es)? de vuelo\b', r'{term-flight-computer}\1'),
        (r'\bvariómetro(s)? no compensado(s)?\b', r'{term-uncompensated-variometer}\1'),
        (r'\bvariómetro(s)? Netto\b', r'{term-netto}\1'),
        (r'\baltitud de presión\b', r'{term-pressure-altitude}'),
        (r'\baltitud de densidad\b', r'{term-density-altitude}'),
        (r'\baltitud indicada\b', r'{term-indicated-altitude}'),
        (r'\baltitud verdadera\b', r'{term-true-altitude}'),
        (r'\bvelocidad indicada\b', r'{term-ias}'),
        (r'\bvelocidad calibrada\b', r'{term-cas}'),
        (r'\bvelocidad verdadera\b', r'{term-tas}'),
        (r'\bviento de cara\b', r'{term-headwind}'),
        (r'\bviento de cola\b', r'{term-tailwind}'),
        (r'\bviento cruzado\b', r'{term-crosswind}'),
        (r'\bvelocidad sobre el suelo\b', r'{term-groundspeed}'),
        (r'\blastre de agua\b', r'{term-water-ballast}'),
        (r'\banillo MacCready\b', r'{term-maccready-ring}'),
        (r'\benergía total\b', r'{term-total-energy}'),
        (r'\btemperatura exterior\b', r'{term-oat}'),
        (r'\bángulo(s)? de ataque\b', r'{term-aoa}\1'),
        (r'\bviento relativo\b', r'{term-relative-wind}'),
        (r'\blínea(s)? de cuerda\b', r'{term-chord-line}\1'),
        (r'\bpunto(s)? de viraje\b', r'{term-turnpoint}\1'),
        (r'\bpolar(es)? de velocidades\b', r'{term-polar-curve}\1'),
        (r'\bremla\b', r'{term-sailplane}'),  # Remla -> velero
        
        # Términos simples
        (r'\bmotovelero(s)?\b', r'{term-motorglider}\1'),
        (r'\bplaneador(es)?\b', r'{term-glider}\1'),
        (r'\bvelero(s)?\b', r'{term-sailplane}\1'),
        (r'\balerón(es)?\b', r'{term-aileron}\1'),
        (r'\bflap(s)?\b', r'{term-flap}\1'),
        (r'\baerofreno(s)?\b', r'{term-airbrake}\1'),
        (r'\bcompensador(es)?\b', r'{term-trim}\1'),
        (r'\bcarlinga(s)?\b', r'{term-canopy}\1'),
        (r'\bfuselaje(s)?\b', r'{term-fuselage}\1'),
        (r'\bala(s)?\b', r'{term-wing}\1'),
        (r'\bpérdida(s)?\b', r'{term-stall}\1'),
        (r'\bbarrena(s)?\b', r'{term-spin}\1'),
        (r'\btérmica(s)?\b', r'{term-thermal}\1'),
        (r'\bascendencia(s)?\b', r'{term-lift}\1'),
        (r'\bsustentación\b', r'{term-lift-force}'),
        (r'\bresistencia\b', r'{term-drag}'),
        (r'\bempuje\b', r'{term-thrust}'),
        (r'\bfineza\b', r'{term-glide-ratio}'),
        (r'\balargamiento\b', r'{term-aspect-ratio}'),
        (r'\bdiedro\b', r'{term-dihedral}'),
        (r'\bpeso\b', r'{term-weight}'),
        (r'\baltímetro(s)?\b', r'{term-altimeter}\1'),
        (r'\banemómetro(s)?\b', r'{term-airspeed}\1'),
        (r'\bvariómetro(s)?\b', r'{term-variometer}\1'),
        (r'\binclinómetro(s)?\b', r'{term-inclinometer}\1'),
        (r'\bdespegue(s)?\b', r'{term-takeoff}\1'),
        (r'\baterrizaje(s)?\b', r'{term-landing}\1'),
        (r'\baproximación(es)?\b', r'{term-approach}\1'),
        (r'\bredondeo\b', r'{term-flare}'),
        (r'\btoma de contacto\b', r'{term-touchdown}'),
        (r'\blanzamiento(s)? con torno\b', r'{term-winch-launch}\1'),
        (r'\bautolanzable(s)?\b', r'{term-self-launch}\1'),
        (r'\bcúmulo(s)?\b', r'{term-cumulus}\1'),
        (r'\binversión(es)? térmica(s)?\b', r'{term-inversion}\1'),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def convert_file(md_path, adoc_path):
    """Convierte un archivo Markdown a AsciiDoc."""
    chapter_num, chapter_title = get_chapter_info(md_path)
    content = md_path.read_text(encoding='utf-8')
    
    # Convertir
    adoc_content = convert_content(content, chapter_num, chapter_title)
    
    # Guardar
    adoc_path.write_text(adoc_content, encoding='utf-8')
    print(f"✓ Convertido: {md_path.name} -> {adoc_path.name} (Capítulo {chapter_num}: {chapter_title})")
    return chapter_num

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python md_to_adoc_v2.py <archivo_md> <archivo_adoc>")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    adoc_path = Path(sys.argv[2])
    
    convert_file(md_path, adoc_path)
