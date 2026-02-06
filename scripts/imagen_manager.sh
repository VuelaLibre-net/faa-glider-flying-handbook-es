#!/bin/bash
# Script de lanzamiento para el Gestor de Imágenes v3.0

echo "🖼️  Gestor de Imágenes v3.0 - Manual de Vuelo sin Motor"
echo "========================================================"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/imagemanager/main.py"
VENV_NAME="faa-gfh-images"

cd "$SCRIPT_DIR/.."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Intentar usar el entorno virtual de pyenv
if command -v pyenv &> /dev/null && pyenv virtualenvs 2>/dev/null | grep -q "$VENV_NAME"; then
    echo "✓ Activando entorno virtual: $VENV_NAME"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    pyenv activate "$VENV_NAME"
    echo "✓ Entorno activado"
else
    echo "⚠️  Entorno virtual no encontrado. Usando Python del sistema..."
    echo "   Para crear el entorno, ejecuta:"
    echo "   ./scripts/setup-image-manager.sh"
    echo ""
fi

# Verificar dependencias
echo ""
echo "🔍 Verificando dependencias..."

if ! python3 -c "from PIL import Image" 2>/dev/null; then
    echo "❌ Pillow no está instalado"
    echo "   Instala con: pip3 install Pillow"
    exit 1
fi
echo "✓ Pillow instalado"

if python3 -c "from google import genai" 2>/dev/null; then
    echo "✓ google-genai instalado"
else
    echo "⚠️  google-genai no instalado (traducción no disponible)"
    echo "   Para habilitar: pip3 install google-genai python-dotenv pyperclip"
fi

if python3 -c "import tkinterdnd2" 2>/dev/null; then
    echo "✓ tkinterdnd2 instalado"
else
    echo "⚠️  tkinterdnd2 no instalado (opcional, para drag & drop)"
fi

# Verificar tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Error: tkinter no está instalado"
    echo "   En Ubuntu/Debian: sudo apt install python3-tk"
    exit 1
fi
echo "✓ tkinter instalado"

echo ""
echo "🚀 Iniciando aplicación..."
echo ""

python3 "$PYTHON_SCRIPT"
