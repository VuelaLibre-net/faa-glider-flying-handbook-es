#!/usr/bin/env python3
"""
Generador de Place-holder genérico para el Manual de Vuelo de Planeador.

Este script crea una imagen PNG de place-holder basada en los argumentos proporcionados.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Colores (tema de aviación - consistente con scripts anteriores)
BG_COLOR = (240, 244, 248)  # #f0f4f8 - Azul claro cielo
TITLE_COLOR = (44, 62, 80)  # #2c3e50 - Azul oscuro
DESC_COLOR = (52, 73, 94)  # #34495e - Gris azulado
NOTE_COLOR = (127, 140, 141)  # #7f8c8d - Gris medio
REF_COLOR = (149, 165, 166)  # #95a5a6 - Gris claro

# Defaults
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 400
DEFAULT_NOTE = "Imagen pendiente de incorporación"
DEFAULT_REF = "Referencia: FAA-H-8083-13B"


def create_placeholder(
    output_path,
    title,
    description,
    width=DEFAULT_WIDTH,
    height=DEFAULT_HEIGHT,
    note=DEFAULT_NOTE,
    reference=DEFAULT_REF,
):
    """Crea un archivo PNG de place-holder."""

    # Crear imagen
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Intentar cargar fuentes
    try:
        # Intentar usar fuentes del sistema (puede variar por plataforma)
        # Priorizar fuentes que sabemos que funcionan en el entorno Linux
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
        )
        font_desc = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
        )
        font_note = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14
        )
        font_ref = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12
        )
    except Exception:
        # Usar fuente por defecto si no se encuentra
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_note = ImageFont.load_default()
        font_ref = ImageFont.load_default()

    # Calcular posiciones Y (centrado vertical)
    center_y = height // 2
    y_title = center_y - 50
    y_desc = center_y + 10
    y_note = center_y + 50
    y_ref = center_y + 80

    # Dibujar textos (centrados horizontalmente)
    draw.text(
        (width // 2, y_title),
        title,
        fill=TITLE_COLOR,
        font=font_title,
        anchor="mm",
    )
    draw.text(
        (width // 2, y_desc), description, fill=DESC_COLOR, font=font_desc, anchor="mm"
    )
    draw.text((width // 2, y_note), note, fill=NOTE_COLOR, font=font_note, anchor="mm")
    draw.text(
        (width // 2, y_ref), reference, fill=REF_COLOR, font=font_ref, anchor="mm"
    )

    # Asegurar que el directorio existe
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar imagen
    img.save(output_path, "PNG")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generar imagen de place-holder.")

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Ruta de salida del archivo (ej: imagenes/figura.png)",
    )
    parser.add_argument(
        "--title", "-t", required=True, help="Título de la figura (ej: 'Figura 03-01')"
    )
    parser.add_argument(
        "--description", "-d", required=True, help="Descripción de la figura"
    )
    parser.add_argument(
        "--note", "-n", default=DEFAULT_NOTE, help=f"Nota (Default: '{DEFAULT_NOTE}')"
    )
    parser.add_argument(
        "--reference",
        "-r",
        default=DEFAULT_REF,
        help=f"Referencia (Default: '{DEFAULT_REF}')",
    )
    parser.add_argument(
        "--width",
        "-W",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"Ancho (Default: {DEFAULT_WIDTH})",
    )
    parser.add_argument(
        "--height",
        "-H",
        type=int,
        default=DEFAULT_HEIGHT,
        help=f"Alto (Default: {DEFAULT_HEIGHT})",
    )

    args = parser.parse_args()

    output_path = Path(args.output).resolve()

    print(f"Generando place-holder: {output_path}")

    try:
        create_placeholder(
            output_path,
            args.title,
            args.description,
            width=args.width,
            height=args.height,
            note=args.note,
            reference=args.reference,
        )
        print(f"✅ Generado exitosamente.")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
