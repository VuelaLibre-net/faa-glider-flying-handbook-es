#!/bin/bash
# Setup script para el entorno virtual del Image Manager v3.0
# Crea un entorno pyenv/virtualenv con las dependencias necesarias

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_NAME="faa-gfh-images"
PYTHON_VERSION="3.13"

echo "🖼️  Setup del Gestor de Imágenes v3.0"
echo "======================================"
echo ""

# Verificar pyenv
if ! command -v pyenv &> /dev/null; then
    echo "❌ pyenv no está instalado"
    echo ""
    echo "Instala pyenv:"
    echo "  curl https://pyenv.run | bash"
    exit 1
fi

echo "✓ pyenv encontrado: $(pyenv --version)"

# Verificar python version
if ! pyenv versions | grep -q "$PYTHON_VERSION"; then
    echo ""
    echo "📦 Instalando Python $PYTHON_VERSION..."
    pyenv install "$PYTHON_VERSION"
fi

echo "✓ Python $PYTHON_VERSION disponible"

# Crear virtualenv
echo ""
echo "🔧 Creando entorno virtual: $VENV_NAME"
cd "$PROJECT_DIR"

# Eliminar si existe
if pyenv virtualenvs | grep -q "$VENV_NAME"; then
    echo "   Eliminando entorno existente..."
    pyenv uninstall -f "$VENV_NAME" 2>/dev/null || true
fi

# Crear nuevo
pyenv virtualenv "$PYTHON_VERSION" "$VENV_NAME"
echo "✓ Entorno creado: $VENV_NAME"

# Activar y instalar dependencias
echo ""
echo "📦 Instalando dependencias..."

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate "$VENV_NAME"

pip install --upgrade pip

# Dependencias base
pip install Pillow tkinterdnd2

# Dependencias opcionales para traducción
echo ""
echo "📦 Instalando dependencias de traducción (opcional)..."
pip install google-genai python-dotenv pyperclip

echo ""
echo "✅ Instalación completada:"
pip list | grep -E "Pillow|tkinterdnd2|google-genai|pyperclip"

# Crear archivo .python-version local
echo "$VENV_NAME" > "$PROJECT_DIR/.python-version"

echo ""
echo "======================================"
echo "✅ Entorno configurado correctamente"
echo ""
echo "Para activar manualmente:"
echo "  pyenv activate $VENV_NAME"
echo ""
echo "Para lanzar el Image Manager:"
echo "  ./scripts/imagen_manager.sh"
echo ""
