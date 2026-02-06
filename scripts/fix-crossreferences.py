#!/usr/bin/env python3
"""
Script para corregir referencias cruzadas en archivos AsciiDoc.
- Agrega anclas a las figuras
- Convierte referencias de texto plano [Figura X-X] o Figura X-X a <<fig-X-X>>
"""

import re
import sys
from pathlib import Path

def fix_chapter_references(filepath, chapter_num):
    """Fix cross-references in a single chapter file."""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    new_lines = []
    
    # Track which figures have anchors added
    figures_with_anchors = set()
    
    # First pass: add anchors to figures and track them
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for lines that start with a dot (caption) followed by image:: line
        if line.startswith('.') and i + 1 < len(lines):
            next_line = lines[i + 1]
            # Match image::NN/figura-NN-XX pattern
            img_match = re.match(r'image::(\d\d)/figura-(\d\d)-(\d+[\w-]*)[^[]+\[', next_line)
            if img_match:
                fig_chapter = img_match.group(2)
                fig_num = img_match.group(3).split('-')[0]  # Get just the number part
                anchor = f"fig-{fig_chapter}-{fig_num}"
                
                # Check if previous line is already an anchor
                if i > 0 and lines[i-1].strip().startswith('[['):
                    new_lines.append(line)
                    new_lines.append(next_line)
                else:
                    # Add anchor before caption
                    new_lines.append(f"[[{anchor}]]")
                    new_lines.append(line)
                    new_lines.append(next_line)
                figures_with_anchors.add(f"{fig_chapter}-{fig_num}")
                i += 2
                continue
        
        # Handle image:: lines without preceding caption line
        img_match = re.match(r'image::(\d\d)/figura-(\d\d)-(\d+[\w-]*)[^[]+\[', line)
        if img_match:
            fig_chapter = img_match.group(2)
            fig_num = img_match.group(3).split('-')[0]  # Get just the number part
            anchor = f"fig-{fig_chapter}-{fig_num}"
            
            # Check if previous line is already an anchor
            if i > 0 and lines[i-1].strip().startswith('[['):
                new_lines.append(line)
            else:
                new_lines.append(f"[[{anchor}]]")
                new_lines.append(line)
            figures_with_anchors.add(f"{fig_chapter}-{fig_num}")
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    # Second pass: convert text references to cross-references
    result = '\n'.join(new_lines)
    
    # Pattern to match [Figura X-X] or [Figura X-XX]
    # Also handles variations like [Figura X-X panel Y], [Figura X-X, panel Y], etc.
    def replace_figure_ref(match):
        full_match = match.group(0)
        prefix = match.group(1)  # Optional text before
        fig_chapter = match.group(2)
        fig_num = match.group(3)
        suffix = match.group(4) or ''  # Optional suffix like " A", ", panel 1", etc.
        
        anchor = f"fig-{fig_chapter.zfill(2)}-{fig_num}"
        
        # Build the replacement
        if prefix and prefix.strip():
            # If there's text before, we need to handle it
            return f"{prefix}<<{anchor}>>"
        else:
            return f"<<{anchor}>>"
    
    # Replace [Figura X-X] patterns
    def format_fig_num(num):
        # Handle cases like "15 A" -> "15a", or keep as "15"
        # Also ensure single-digit numbers have leading zero for consistency
        num = num.strip().replace(' ', '-').lower()
        # Extract just the numeric part and format with leading zeros
        num_match = re.match(r'(\d+)(.*)', num)
        if num_match:
            return num_match.group(1).zfill(2) + num_match.group(2)
        return num
    
    result = re.sub(r'(?<![<\w])\[Figura (\d+)-(\d+[a-zA-Z\s-]*)([^\]]*)\]', 
                    lambda m: f"<<fig-{m.group(1).zfill(2)}-{format_fig_num(m.group(2))}>>", 
                    result)
    
    # Replace "Figura X-X" in text (when it's a standalone reference)
    # Be careful not to replace "Figura X-X" that's part of a caption or description
    def format_single_num(m):
        return f"<<fig-{m.group(1).zfill(2)}-{format_fig_num(m.group(2))}>>"
    
    result = re.sub(r'(?<![\w\[])Figura (\d+)-(\d+[a-zA-Z]?) muestra',
                    lambda m: f"{format_single_num(m)} muestra",
                    result)
    
    result = re.sub(r'(?<![\w\[])Figura (\d+)-(\d+[a-zA-Z]?) ilustra', 
                    lambda m: f"{format_single_num(m)} ilustra",
                    result)
    
    result = re.sub(r'(?<![\w\[])en la Figura (\d+)-(\d+[a-zA-Z]?) anterior',
                    lambda m: f"en la {format_single_num(m)} anterior",
                    result)
    
    result = re.sub(r'(?<![\w\[])como se muestra en la Figura (\d+)-(\d+[a-zA-Z]?)',
                    lambda m: f"como se muestra en la {format_single_num(m)}",
                    result)
    
    result = re.sub(r'(?<![\w\[])de la Figura (\d+)-(\d+[a-zA-Z]?) ',
                    lambda m: f"de la {format_single_num(m)} ",
                    result)
    
    result = re.sub(r'(?<![\w\[])de la Figura (\d+)-(\d+[a-zA-Z]?)\n',
                    lambda m: f"de la {format_single_num(m)}\n",
                    result)
    
    # Handle "Capítulo X" references
    result = re.sub(r'Capítulo (\d+), ([^,]+),',
                    lambda m: f"<<cap{m.group(1).zfill(2)},{m.group(2)}>>",
                    result)
    
    result = re.sub(r'el Capítulo (\d+), ([^,]+), contiene',
                    lambda m: f"el <<cap{m.group(1).zfill(2)},{m.group(2)}>> contiene",
                    result)
    
    result = re.sub(r'en el Capítulo (\d+), ([^,]+)\.',
                    lambda m: f"en el <<cap{m.group(1).zfill(2)},{m.group(2)}>>.",
                    result)
    
    result = re.sub(r'en el Capítulo (\d+), ([^,]+),',
                    lambda m: f"en el <<cap{m.group(1).zfill(2)},{m.group(2)}>>",
                    result)
    
    result = re.sub(r'discutidas en el Capítulo (\d+), ([^,]+)\.',
                    lambda m: f"discutidas en el <<cap{m.group(1).zfill(2)},{m.group(2)}>>.",
                    result)
    
    filepath.write_text(result, encoding='utf-8')
    print(f"Fixed: {filepath}")

def main():
    base_dir = Path('/home/camus/ws/VuelaLibre.net/faa-gfh/es/capitulos')
    
    chapters = [
        (1, '01-planeadores-y-veleros.adoc'),
        (2, '02-componentes-y-sistemas.adoc'),
        (3, '03-aerodinamica-del-vuelo.adoc'),
        (4, '04-instrumentos-de-vuelo.adoc'),
        (5, '05-performance.adoc'),
        (6, '06-prevuelo-operaciones-tierra.adoc'),
        (7, '07-lanzamiento-aterrizaje-maniobras.adoc'),
        (8, '08-emergencias.adoc'),
    ]
    
    for num, filename in chapters:
        filepath = base_dir / filename
        if filepath.exists():
            fix_chapter_references(filepath, num)
        else:
            print(f"File not found: {filepath}")

if __name__ == '__main__':
    main()
