# Extensión para numeración de figuras y tablas por capítulo - Versión 10
# Usando Module#prepend para modificar el comportamiento del convertidor
# Formato: Figura/Tabla X-Y (contador compartido, igual que el manual original FAA)
#
# Uso: Agregar a Makefile:
#   -r ./scripts/figura-por-capitulo.rb
#
# Esta extensión mantiene un contador compartido para figuras y tablas,
# permitiendo sustituir figuras por tablas sin alterar la numeración secuencial.

require 'asciidoctor'
require 'asciidoctor/pdf'

# Extender el convertidor PDF usando prepend
module FiguraPorCapitulo
  # Método auxiliar para obtener el número de capítulo actual
  def obtener_num_capitulo(node)
    section = node
    while section && section.context != :section
      section = section.parent
    end
    
    if section && (sectnum = section.sectnum)
      sectnum.to_s.split('.').first.to_i
    else
      1
    end
  end
  
  # Método auxiliar para obtener el siguiente número de figura/tabla
  # Comparte el contador entre figuras y tablas
  def siguiente_numero_elemento(num_capitulo)
    @elementos_por_capitulo ||= {}
    @capitulo_actual ||= nil
    
    if num_capitulo != @capitulo_actual
      @elementos_por_capitulo[num_capitulo] = 0
      @capitulo_actual = num_capitulo
    end
    
    @elementos_por_capitulo[num_capitulo] += 1
    @elementos_por_capitulo[num_capitulo]
  end

  # Procesar imágenes (figuras)
  def convert_image(node, opts = {})
    # Solo procesar si tiene título y hay caption activo
    if node.title? && (doc = node.document).attr?('figure-caption')
      num_capitulo = obtener_num_capitulo(node)
      num_elemento = siguiente_numero_elemento(num_capitulo)
      
      # Establecer el caption personalizado con formato X-Y
      prefijo_caption = doc.attr('figure-caption', 'Figura')
      caption_text = "#{prefijo_caption} #{num_capitulo}-#{num_elemento}. "
      node.instance_variable_set(:@caption, caption_text)
      
      # Establecer el numeral como el número por capítulo para referencias cruzadas
      numeral_text = "#{num_capitulo}-#{num_elemento}"
      node.instance_variable_set(:@numeral, numeral_text)
      
      # También actualizar el atributo reftext si existe
      if node.respond_to?(:attributes)
        node.attributes['reftext'] = numeral_text
      end
    end
    
    # Llamar al método original
    super
  end
  
  # Procesar tablas (comparten el mismo contador que las figuras)
  def convert_table(node)
    # Solo procesar si tiene título y hay caption activo para tablas
    if node.title? && (doc = node.document).attr?('table-caption')
      num_capitulo = obtener_num_capitulo(node)
      num_elemento = siguiente_numero_elemento(num_capitulo)
      
      # Establecer el caption personalizado con formato X-Y
      prefijo_caption = doc.attr('table-caption', 'Tabla')
      caption_text = "#{prefijo_caption} #{num_capitulo}-#{num_elemento}. "
      node.instance_variable_set(:@caption, caption_text)
      
      # Establecer el numeral como el número por capítulo para referencias cruzadas
      numeral_text = "#{num_capitulo}-#{num_elemento}"
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
      # Si es una referencia a una figura (formato fig-XX-YY o tab-XX-YY)
      if refid =~ /^(fig|tab)-(\d+)-(\d+)$/
        tipo = $1
        capitulo = $2.to_i
        elemento = $3.to_i
        
        # Verificar si el nodo tiene texto personalizado
        # Si no tiene texto, establecer el formato X-Y
        if node.text.nil? || node.text.empty? || node.text =~ /^(Figura|Tabla) \d+$/
          prefijo = if tipo == 'fig'
            node.document.attr('figure-caption', 'Figura')
          else
            node.document.attr('table-caption', 'Tabla')
          end
          node.instance_variable_set(:@text, "#{prefijo} #{capitulo}-#{elemento}")
        end
      end
    end
    
    # Llamar al método original
    super
  end
end

# Prepend el módulo al convertidor
Asciidoctor::PDF::Converter.prepend(FiguraPorCapitulo)
