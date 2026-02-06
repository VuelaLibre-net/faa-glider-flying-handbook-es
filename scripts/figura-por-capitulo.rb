# Extensión para numeración de figuras por capítulo - Versión 9
# Usando Module#prepend para modificar el comportamiento del convertidor
# Formato: Figura X-Y (igual que el manual original FAA)
#
# Uso: Agregar a Makefile:
#   -r ./scripts/figura-por-capitulo.rb

require 'asciidoctor'
require 'asciidoctor/pdf'

# Extender el convertidor PDF usando prepend
module FiguraPorCapitulo
  def convert_image(node, opts = {})
    # Solo procesar si tiene título y hay caption activo
    if node.title? && (doc = node.document).attr?('figure-caption')
      # Obtener número de capítulo
      section = node
      while section && section.context != :section
        section = section.parent
      end
      
      num_capitulo = if section && (sectnum = section.sectnum)
        sectnum.to_s.split('.').first.to_i
      else
        1
      end
      
      # Obtener contador de figuras para este capítulo
      @figuras_por_capitulo ||= {}
      @capitulo_actual ||= nil
      
      if num_capitulo != @capitulo_actual
        @figuras_por_capitulo[num_capitulo] = 0
        @capitulo_actual = num_capitulo
      end
      
      @figuras_por_capitulo[num_capitulo] += 1
      num_figura = @figuras_por_capitulo[num_capitulo]
      
      # Establecer el caption personalizado con formato X-Y
      prefijo_caption = doc.attr('figure-caption', 'Figura')
      caption_text = "#{prefijo_caption} #{num_capitulo}-#{num_figura}. "
      node.instance_variable_set(:@caption, caption_text)
      
      # Establecer el numeral como el número por capítulo para referencias cruzadas
      numeral_text = "#{num_capitulo}-#{num_figura}"
      node.instance_variable_set(:@numeral, numeral_text)
      
      # También actualizar el atributo reftext si existe
      if node.respond_to?(:attributes)
        node.attributes['reftext'] = numeral_text
      end
    end
    
    # Llamar al método original
    super
  end
  
  # Método para convertir referencias cruzadas
  def convert_inline_anchor(node)
    if node.type == :xref
      refid = node.attr('refid')
      # Si es una referencia a una figura (formato fig-XX-YY)
      if refid =~ /^fig-(\d+)-(\d+)$/
        capitulo = $1.to_i
        figura = $2.to_i
        
        # Verificar si el nodo tiene texto personalizado
        # Si no tiene texto, establecer el formato X-Y
        if node.text.nil? || node.text.empty? || node.text =~ /^Figura \d+$/
          prefijo = node.document.attr('figure-caption', 'Figura')
          node.instance_variable_set(:@text, "#{prefijo} #{capitulo}-#{figura}")
        end
      end
    end
    
    # Llamar al método original
    super
  end
end

# Prepend el módulo al convertidor
Asciidoctor::PDF::Converter.prepend(FiguraPorCapitulo)
