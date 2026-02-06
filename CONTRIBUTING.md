# Guía de Contribución - FAA-GFH

> Manual completo para contribuir al proyecto de traducción del FAA Glider Flying Handbook

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Tipos de Contribución](#tipos-de-contribución)
3. [Primeros Pasos](#primeros-pasos)
4. [Guía de Traducción](#guía-de-traducción)
5. [Convenciones de Código/Estilo](#convenciones-de-códigoestilo)
6. [Proceso de Pull Request](#proceso-de-pull-request)
7. [Recursos](#recursos)
8. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

### ¿Qué es FAA-GFH?

FAA-GFH es un proyecto de traducción comunitaria del **FAA Glider Flying Handbook** (FAA-H-8083-13B) al español. El objetivo es proporcionar material educativo de calidad para pilotos de planeador de habla hispana.

### ¿Por qué contribuir?

- **Impacto real:** Tu trabajo ayudará a pilotos de habla hispana a aprender vuelo a vela
- **Aprendizaje:** Mejora tus habilidades técnicas y de traducción
- **Comunidad:** Únete a un grupo de entusiastas de la aviación
- **Reconocimiento:** Tu nombre aparecerá en los agradecimientos del manual

### Código de Conducta

Este proyecto sigue un código de conducta de respeto y colaboración. Al contribuir, aceptas:

- Ser respetuoso con otros contribuidores
- Aceptar retroalimentación constructiva
- Enfocarte en lo que es mejor para el proyecto y los usuarios
- Reportar problemas de manera responsable

---

## Tipos de Contribución

### 1. Traducción de Capítulos

**Dificultad:** Media | **Tiempo:** 2-4 horas por capítulo

Traduce un capítulo completo del inglés al español siguiendo las convenciones del proyecto.

**Requisitos:**
- Conocimiento de aviación (deseable)
- Dominio del español (nativo o equivalente)
- Atención al detalle
- Capacidad de seguir guías de estilo

**Pasos:**
1. Elige un capítulo pendiente del [README.md](../../README.md)
2. Crea una rama para tu capítulo
3. Traduce siguiendo las convenciones
4. Envía un Pull Request

### 2. Revisión de Traducciones

**Dificultad:** Baja | **Tiempo:** 30-60 minutos por capítulo

Revisa las traducciones de otros contribuidores para asegurar calidad.

**Qué revisar:**
- Terminología (consistencia)
- Precisión técnica
- Claridad del español
- Formato y estilo

### 3. Mejoras de Infraestructura

**Dificultad:** Alta | **Tiempo:** Variable

Mejora el sistema de build, automatización, o herramientas del proyecto.

**Ejemplos:**
- Script de validación de terminología
- Integración con CI/CD
- Mejora de temas PDF/HTML
- Documentación adicional

### 4. Corrección de Errores

**Dificultad:** Baja | **Tiempo:** 15-30 minutos

Corrige errores tipográficos, gramaticales, o técnicos.

**Tipos de errores:**
- Errores ortográficos
- Inconsistencias de formato
- Problemas de build
- Errores en glosario

### 5. Imágenes y Figuras

**Dificultad:** Media | **Tiempo:** Variable

Ayuda a traducir, adaptar o crear las figuras del manual.

**Tipos de tareas:**
- Traducir texto en imágenes (diagramas, instrumentos)
- Adaptar figuras del manual original FAA
- Crear diagramas nuevos si es necesario
- Optimizar imágenes existentes

**Herramientas disponibles:**
```bash
make setup-images     # Configura el entorno Python necesario para asistencia con imágenes
make images           # Abre el gestor de imágenes (GUI)
```

**Requisitos técnicos:**
- Formato PNG para PDF y epub (compresión muy optimizada)
- Formato WebP para web (si aplica)
- Resolución mínima: 150 DPI para impresión
- Directorio: `es/imagenes/NN/` (NN = número de capítulo)

### 6. Documentación

**Dificultad:** Baja | **Tiempo:** Variable

Mejora la documentación del proyecto.

**Qué documentar:**
- Guías de contribución
- Tutoriales de configuración
- Mejores prácticas
- FAQ

---

## Primeros pasos

Para contribuir basta con que abras un `issue` en https://github.com/VuelaLibre-net/faa-glider-flying-handbook-es/issues describiendo tu propuesta. La estudiaremos a la mayor brevedad.

### 1. Configura tu Entorno

Si quieres generar los documentos por tí mismo puedes hacer lo siguiente:

```bash
# Clona el repositorio
git clone https://github.com/VuelaLibre-net/faa-glider-flying-handbook-es.git
cd faa-gfh

# Configura Ruby con RVM
rvm use 3.3.5@faa-gfh

# Instala dependencias
make install

# Verifica la instalación
make check
```

### 2. Familiarízate con el Proyecto

```bash
# Lee la documentación principal
cat README.md           # Visión general del proyecto
cat AGENTS.md           # Guías para agentes AI (útil para entender convenciones)

# Explora la estructura
ls es/                  # Contenido en español
ls es/capitulos/        # Capítulos
ls es/config/           # Configuración y glosario

# Revisa el glosario de términos
cat es/apendices/glosario.adoc
```

### 3. Elige una Tarea

Revisa el estado de traducción en README.md y elige:

- Un capítulo pendiente de traducir
- Una traducción existente para revisar
- Un error para corregir
- Una mejora de infraestructura

### 4. Crea tu Rama

```bash
# Actualiza tu repositorio local
git checkout main
git pull origin main

# Crea tu rama de trabajo
git checkout -b traduccion/capitulo-XX

# O para correcciones:
git checkout -b fix/descripcion-del-error
```

---

## Guía de Traducción

### Principios fundamentales

#### Precisión Técnica

La traducción debe ser técnicamente precisa. Los términos técnicos tienen significados específicos en aviación.

**✓ CORRECTO:**
- «pérdida» (stall)
- «circuito de tráfico» (traffic pattern)
- «aerofreno» (airbrake/spoiler)

**✗ INCORRECTO:**
- «entrada en pérdida» (stall) - usar solo «pérdida»
- «patrón de tráfico» (traffic pattern) - usar «circuito de tráfico»

#### Claridad

El español debe ser claro y comprensible. Evita traducciones literales que resulten confusas.

**✓ CORRECTO:**
- «La velocidad de pérdida aumenta con el peso.»

**✗ INCORRECTO:**
- «La velocidad a la cual ocurre la pérdida aumenta con el peso.» (demasiado literal)

#### Consistencia

Usa los mismos términos a lo largo de todo el documento. Consulta el glosario.

### Uso del Glosario

El glosario es tu mejor amigo. Está en `es/apendices/glosario.adoc`.

**Cómo usar:**
1. Busca el término inglés en el glosario
2. Usa el término español indicado
3. Mantén consistencia en todo el capítulo

### Sistema de Atributos para Términos Técnicos

El proyecto utiliza atributos AsciiDoc para garantizar consistencia terminológica y permitir variantes regionales automáticas:

```asciidoc
La {term-thermal} permite ganar altitud...     % Resultado: «La térmica permite...»
El {term-stall} ocurre cuando...              % Resultado: «El pérdida ocurre...»
```

**Beneficios:**
- Consistencia automática en todo el documento
- Soporte para variantes regionales (España, Argentina, México)
- Cambios centralizados desde `es/config/regiones/`

**Atributos disponibles:**
- `{term-glider}` → planeador
- `{term-sailplane}` → velero
- `{term-stall}` → pérdida
- `{term-spin}` → barrena
- `{term-thermal}` → térmica
- `{term-airbrake}` → aerofreno
- `{term-lift}` → ascendencia
- `{term-lift-force}` → sustentación
- `{term-aerotow}` → remolque
- `{term-winch-launch}` → lanzamiento con torno

Consulta el archivo `es/config/regiones/es.adoc` para la lista completa.

**Términos comunes:**

| Inglés | Español | Notas |
|--------|---------|-------|
| Glider | planeador | Término genérico |
| Sailplane | velero | Planeador de altas prestaciones |
| Stall | pérdida | NO «entrada en pérdida» |
| Spin | barrena | (giro en barrena)
| Thermal | térmica | Sustantivo femenino |
| Lift | ascendencia | |
| Sink | descendencia | |
| Airbrake | aerofreno | |
| Spoiler | aerofreno | |
| Flap | flap | Mantener inglés |
| Aileron | alerón | |
| Rudder | timón de dirección | |
| Elevator | timón de profundidad | |
| Yaw | guiñada | |
| Pitch | cabeceo | |
| Roll | balanceo | |
| Tow | remolque | |
| Winch | cabrestante | |
| Aerotow | remolque aéreo | |
| Pattern | circuito de tráfico | |

### Validación de Terminología

Antes de hacer commit de tus cambios, ejecuta el script de validación de terminología:

```bash
make validate
```

Este script verifica:

1. **Términos inconsistentes:** Busca usos incorrectos como «entrada en pérdida» (debe ser solo «pérdida»)
2. **Uso de atributos:** Verifica que los términos técnicos usen los atributos definidos (`{term-xxx}`)
3. **Comillas:** Detecta comillas rectas (recomendadas tipográficas)

### Variantes regionales

El manual soporta variantes terminológicas para diferentes regiones hispanohablantes:

| Región | Archivo | Uso típico |
|--------|---------|------------|
| `es` | `es/config/regiones/es.adoc` | España - por defecto |
| `ar` | `es/config/regiones/ar.adoc` | Argentina |
| `mx` | `es/config/regiones/mx.adoc` | México |

**Generar PDF con variante regional:**
```bash
make pdf REGION=ar    # PDF con terminología argentina
make pdf-ar           # Atajo equivalente
make pdf-mx           # PDF con terminología mexicana
```

**Añadir nueva región:**
1. Crea `es/config/regiones/XX.adoc` (donde XX = código de país)
2. Define los atributos de términos que difieran del español estándar
3. Usa el archivo existente como plantilla

#### Corregir problemas detectados

Si el script encuentra inconsistencias, corrígelas antes de hacer commit:

```bash
# Ejemplo: cambiar 'entrada en pérdida' por 'pérdida'
# Incorrecto:
El punto de entrada en pérdida es...

# Correcto:
El punto de {term-stall} es...
```

### Estructura de Documentos AsciiDoc

#### Anclajes de Capítulo

Cada capítulo debe comenzar con un anclaje:

```asciidoc
[[cap01]]
= Capítulo 1. Planeadores y Veleros
```

#### Secciones

Usa los niveles de encabezado correctamente:

```asciidoc
= Capítulo N. Título      (Nivel 1 - Capítulo)
== Sección Principal      (Nivel 2)
=== Subsección            (Nivel 3)
==== Sub-subsección       (Nivel 4)
```

#### Admonitions (Avisos de Seguridad)

Usa admonitions semánticos para información importante:

```asciidoc
[WARNING]
====
Advertencia crítica de seguridad.
====

[CAUTION]
====
Precaución importante.
====

[IMPORTANT]
====
Información importante del manual original.
====

[NOTE]
====
Información adicional o contexto.
====

[TIP]
====
Consejo práctico.
====
```

#### Referencias cruzadas

```asciidoc
<<cap02,Capítulo 2>>                    % Referencia a otro capítulo
<<glosario,Glosario>>                   % Referencia al glosario
<<figura-1-1,Figura 1-1>>               % Referencia a figura
```

#### Imágenes

```asciidoc
[[figura-1-1]]
.Imagen descriptiva
image::imagenes/01/figura-1-1.png["Texto alternativo",width=100%]
```

### Formato de Texto

#### Negrita y Cursiva

```asciidoc
*texto en negrita*    % Énfasis en términos técnicos
_cursiva_             % Títulos de libros, términos extranjeros
```

#### Listas

```asciidoc
* Item de lista no ordenada
* Otro item

. Primer paso
. Segundo paso
. Tercer paso
```

#### Tablas

```asciidoc
|===
| Columna 1 | Columna 2 | Columna 3

| Dato 1 | Dato 2 | Dato 3
| Dato 4 | Dato 5 | Dato 6
|===
```

### Comentarios del Traductor

Usa comentarios para notas internas:

```asciidoc
// Nota: Figura 1-1 del original muestra un DG-800
// TODO: Añadir referencia a figura cuando esté disponible
```

---

## Convenciones de Código/Estilo

### Estilo de Código (AsciiDoc)

#### Sangría y Espaciado

```asciidoc
% Sangría: usar 2 espacios para contenido anidado
% Espaciado en blanco: una línea entre secciones

= Capítulo 1

== Sección 1

Contenido del texto...

=== Subsección

Más contenido...
```

#### Longitud de Línea

- Mantén las líneas por debajo de 120 caracteres
- Esto facilita la revisión en GitHub

#### Nomenclatura de Archivos

```
NN-nombre-descriptivo.adoc
01-planeadores-y-veleros.adoc
02-componentes-y-sistemas.adoc
```

### Convenciones de Git

#### Ramas

```bash
# Rama de traducción de capítulo
traduccion/capitulo-01

# Rama de corrección de errores
fix/error-tipografico-cap01

# Rama de mejora de infraestructura
feat/validacion-terminologia
```

#### Commits

Usa mensajes de commit convencionales:

```bash
# Translation complete
feat(cap01): traducción completa del capítulo 1 - Planeadores y Veleros

# Typo correction
fix(cap01): corrección de errata en sección de aerodinámica

# Documentation update
docs: actualización del glosario con nuevos términos

# Infrastructure improvement
feat(build): añadir validación de terminología al make check

# Terminology update
refactor(glosario): unificar terminología de aerofrenos
```

Estructura:
```
<tipo>(<alcance>): <descripción>

[ cuerpo opcional ]

[ notas de pie opcional ]
```

Tipos:
- `feat`: Nueva característica o capítulo
- `fix`: Corrección de error
- `docs`: Documentación
- `refactor`: Reestructuración sin cambio funcional
- `style`: Formato (no cambio de código)
- `chore`: Tareas de mantenimiento

### Reglas de Oro para Contribuidores

1. **Validar Antes de Confirmar:** Ejecuta `make validate` y `make pdf` antes de hacer PR
2. **No Inventar Términos:** Si un término no está en el glosario, consulta antes de traducir
3. **No Eliminar Anclas:** Nunca elimines etiquetas `[[...]]` existentes
4. **Mantener "Flap" en Inglés:** El término técnico «flap» no se traduce
5. **Preservar PNGs Originales:** Nunca borres las imágenes fuente originales

---

## Proceso de Pull Request

### 1. Prepara tu Rama

```bash
# Asegúrate de estar en tu rama
git checkout traduccion/capitulo-XX

# Actualiza con la última versión de main
git fetch origin
git merge origin/main

# Resuelve conflictos si los hay

# Verifica que el build funcione
make pdf
```

### 2. Crea el Pull Request

1. Ve a GitHub
2. Haz clic en "New Pull Request"
3. Selecciona tu rama como "head" y "main" como "base"
4. Completa la plantilla de PR

#### Plantilla de PR

```markdown
## Descripción
[Describe los cambios realizados]

## Tipo de Cambio
- [ ] Traducción de capítulo nuevo
- [ ] Revisión de traducción existente
- [ ] Corrección de error
- [ ] Mejora de infraestructura
- [ ] Documentación

## Capítulo(s) Afectado(s)
- Capítulo XX: [Título del capítulo]

## Checklist
- [ ] La traducción sigue las convenciones del proyecto
- [ ] Se usó el glosario de términos
- [ ] Las admonitions están correctamente usadas
- [ ] Las referencias cruzadas funcionan
- [ ] El build genera correctamente
- [ ] No hay erratas u errores ortográficos

## Notas adicionales
[Información adicional relevante]

## Screenshots (si aplica)
[Añade capturas de pantalla del PDF generado]
```

### 3. Proceso de Revisión

- Un revisor revisará tu PR
- Puede pedir cambios o aprobarlo
- Una vez aprobado, se hace merge a main

### 4. Após el Merge

- Tu capítulo aparecerá en el manual oficial
- Te añadimos a los agradecimientos
- ¡Comparte tu logro!

---

## Recursos

### Documentación del Proyecto

| Recurso | Ubicación | Descripción |
|---------|-----------|-------------|
| README.md | `/README.md` | Visión general del proyecto |
| AGENTS.md | `/AGENTS.md` | Guías para agentes AI |
| Contexto FAA-GFH | `.opencode/context/` | Documentación completa del proyecto |

### Documentación Técnica

| Recurso | URL | Descripción |
|---------|-----|-------------|
| AsciiDoc Syntax | https://docs.asciidoctor.org/asciidoc/latest/ | Referencia oficial de AsciiDoc |
| Asciidoctor PDF | https://docs.asciidoctor.org/pdf-converter/latest/ | Guía de temas PDF |
| Asciidoctor EPUB3 | https://docs.asciidoctor.org/epub3-converter/latest/ | Guía de EPUB |

### Recursos de Aviación

| Recurso | Descripción |
|---------|-------------|
| FAA Glider Flying Handbook | Manual original en inglés |
| FAA | Federal Aviation Administration (autoridad aeronáutica de EE.UU.) |

### Glosario

| Glosario | Ubicación | Descripción |
|----------|-----------|-------------|
| Glosario EN↔ES | `es/apendices/glosario.adoc` | Términos normalizados |
| Atributos | `es/config/atributos.adoc` | Variables de AsciiDoc |

---

## Preguntas frecuentes

### ¿Puedo traducir aunque no sea piloto?

**Sí.** Aunque el conocimiento de aviación ayuda, muchas contribuciones valiosas vienen de:
- Traductores profesionales
- Editores y correctores
- Desarrolladores que mejoran la infraestructura
- Documentalistas

### ¿Qué pasa si no conozco un término técnico?

1. Consulta el glosario (`es/apendices/glosario.adoc`)
2. Busca en el original inglés para entender el contexto
3. Consulta manuales de aviación en español o documentación de tu autoridad aeronáutica local
4. Pregunta en GitHub Discussions

### ¿Cómo manejo términos técnicos específicos?

Si encuentras un término técnico que no está en el glosario:
1. Consulta el contexto en el manual original FAA
2. Busca equivalencias en terminología aeronáutica estándar en español
3. Propón el término en un issue para discusión

### ¿Puedo trabajar en varios capítulos a la vez?

**Sí,** pero se sugiere trabajar en un único capítulo para mantener la calidad. Si quieres trabajar en varios:

1. Crea una rama por capítulo
2. Envía PRs separados
3. Mantén actualizada la lista de progreso

### ¿Cómo reporto un error?

1. Ve a GitHub Issues
2. Crea un nuevo issue
3. Usa la plantilla de bug report
4. Incluye:
   - Descripción del error
   - Pasos para reproducir
   - Capturas de pantalla
   - Archivo/línea afectado

### ¿Cuánto tiempo toma traducir un capítulo?

**Promedio:** 2-4 horas por capítulo

Factores que afectan el tiempo:
- Complejidad técnica del capítulo
- Tu familiaridad con la aviación
- Tu experiencia con AsciiDoc
- Revisiones necesarias

### ¿Cómo puedo ayudar si no tengo tiempo para traducir?

¡Hay muchas formas de ayudar!

- Revisar PRs de otros
- Corregir erratas
- Mejorar la documentación
- Responder preguntas en Discussions
- Compartir el proyecto
- Reportar errores

---

## Agradecimientos

Gracias por tu interés en contribuir al proyecto FAA-GFH. Tu trabajo ayuda a pilotos de habla hispana a acceder a educación de calidad en su idioma.

**¡Bienvenido a la comunidad! 🛫**

---

## Contacto

- **Email:** soporte@vuelalibre.net
- **GitHub:** https://github.com/VuelaLibre-net/faa-glider-flying-handbook-es
- **Issues:** https://github.com/VuelaLibre-net/faa-glider-flying-handbook-es/issues
- **Discussions:** https://github.com/VuelaLibre-net/faa-glider-flying-handbook-es/discussions

---

**Última actualización:** 2026-01-31
**Versión:** 0.1.1
**Licencia:** CC BY-SA 4.0
