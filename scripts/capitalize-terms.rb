# Extensión para capitalizar términos al inicio de títulos de secciones
# Usando TreeProcessor para modificar los títulos después del parsing
#
# Esta extensión detecta cuando un título de sección comienza con el valor de un
# atributo {term-*} (ya expandido) y capitaliza la primera letra automáticamente.
#
# Uso: Agregar a Makefile:
#   -r ./scripts/capitalize-terms.rb

require 'asciidoctor'
require 'asciidoctor/extensions'

# TreeProcessor para capitalizar términos en títulos
Asciidoctor::Extensions.register do
  treeprocessor do
    process do |doc|
      # Obtener todos los valores de atributos term-* del documento
      term_values = {}
      
      doc.attributes.each do |key, value|
        if key.to_s.start_with?('term-') && !value.nil?
          term_values[value.to_s.downcase.strip] = value.to_s.strip
        end
      end
      
      # Si no hay términos en el documento, leer del archivo de configuración regional
      if term_values.empty?
        region = doc.attr('region', 'es')
        config_file = File.join(doc.base_dir, 'config', 'regiones', "#{region}.adoc")
        
        if File.exist?(config_file)
          File.readlines(config_file).each do |line|
            if line =~ /^:term-([a-z-]+):\s*(.+)$/
              term_value = $2.strip
              term_values[term_value.downcase] = term_value
            end
          end
        end
      end
      
      next if term_values.empty?
      
      # Función para capitalizar primera letra
      capitalize_first = ->(str) { str[0].upcase + str[1..-1] }
      
      # Procesar todas las secciones del documento
      doc.find_by(context: :section).each do |section|
        title = section.title
        next if title.nil? || title.empty?
        
        title_str = title.to_s
        
        # Buscar si el título comienza con algún valor de término
        # Ordenar por longitud descendente para coincidir primero con términos más largos
        sorted_terms = term_values.keys.sort_by(&:length).reverse
        
        sorted_terms.each do |term_value|
          # Patrón: término al inicio, seguido de espacio, 's', 'es' o fin de cadena
          term_regex = Regexp.new("^(#{Regexp.escape(term_value)})(\\s|s\\b|es\\b|$)", Regexp::IGNORECASE)
          
          if match = title_str.match(term_regex)
            matched_text = match[1]
            
            # Verificar si ya está capitalizado
            if matched_text[0] != matched_text[0].upcase
              # Capitalizar el término encontrado
              capitalized = capitalize_first.call(matched_text)
              new_title = title_str.sub(matched_text, capitalized)
              
              # Actualizar el título de la sección
              section.title = new_title
            end
            
            break # Solo procesar el primer match
          end
        end
      end
      
      doc
    end
  end
end
