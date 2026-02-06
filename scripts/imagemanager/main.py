#!/usr/bin/env python3
"""
Gestor de Imágenes - Manual de Vuelo sin Motor v3.0

Aplicación GUI para gestionar, comprimir y traducir imágenes
del manual de vuelo a vela.

Uso:
    python -m imagemanager
    python scripts/imagemanager/main.py

Versiones disponibles:
    - main_window: Versión clásica (2 paneles laterales)
    - main_window_v2: Versión con sidebar y toolbar (nuevo diseño)
"""

import sys
from pathlib import Path

# Añadir el directorio scripts al path para imports
script_dir = Path(__file__).parent.parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

def main():
    """Punto de entrada principal - usa la nueva versión por defecto."""
    import tkinter as tk
    from imagemanager.ui import ImageManagerAppV2
    
    root = tk.Tk()
    app = ImageManagerAppV2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
