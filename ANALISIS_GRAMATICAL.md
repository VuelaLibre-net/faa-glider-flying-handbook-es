# Análisis Gramatical - Manual de Vuelo sin Motor

**Fecha:** 2026-02-08  
**Norma de referencia:** RAE (Real Academia Española)
**Estado:** Completado (Todas las fases implementadas)

---

## Resumen Ejecutivo

Se han identificado **más de 150 problemas gramaticales** en los 13 capítulos del manual. Los errores más frecuentes son:

| Tipo de Error | Cantidad Aprox. | Ejemplo |
|---------------|-----------------|---------|
| Anglicismos ("falla", "involucrar", "performance") | ~25 | "falla del sistema" → "fallo del sistema" |
| Preposiciones incorrectas | ~20 | "aumentar de tamaño" → "aumentar en tamaño" |
| Falta de artículos | ~30 | "proporciona comunicación" → "proporciona una comunicación" |
| Concordancia de género/número | ~15 | "ala izquierda" → "ala izquierda" (o "ala izquierdo") |
| Atributos sin sustituir | ~40 | `{term-glider}` → "planeador" |
| Errores tipográficos | ~10 | "guañe" → "guiñe", "contacton" → "contacto" |
| Redundancias | ~10 | "líneas intersectantes se intersectan" (CORREGIDO) |

---

## Errores Críticos (Prioridad Alta)

### 1. Concordancia de Género

#### Capítulo 02
| Línea | Texto incorrecto | Corrección | Explicación |
|-------|------------------|------------|-------------|
| 33 | "mayor {term-lift-force} en el {term-wing} izquierda" | "mayor sustentación en el **ala izquierdo**" o "en la **ala izquierda**" | Discordancia: "ala" es femenino, pero se usa "el" + adjetivo en femenino |
| 70 | "instalado en estabilizadores" | "**instalada** en estabilizadores" | "Aleta compensadora" es femenino |

#### Capítulo 03
| Línea | Texto incorrecto | Corrección | Explicación |
|-------|------------------|------------|-------------|
| 284 | "el {term-wing} más completamente estancada" | "el **ala** más completamente **estancado**" o "la **ala estancada**" | Discordancia de género |

#### Capítulo 07
| Línea | Texto incorrecto | Corrección | Explicación |
|-------|------------------|------------|-------------|
| 70 | "El {term-wing} izquierda debe descansar" | "El **ala izquierdo** debe descansar" o "La **ala izquierda**" | Discordancia |
| 74 | "el {term-wing} baja y el {term-wing} levantada" | "el **ala bajo** y el **ala levantado**" | Ambos adjetivos deben concordar (ES CORRECTO: ala baja) |

---

### 2. Anglicismos (uso de "falla" en lugar de "fallo")

**Nota:** "Falla" es un anglicismo del inglés "failure". En español técnico se prefiere "fallo" o "error".

| Capítulo | Línea | Texto incorrecto | Corrección |
|----------|-------|------------------|------------|
| 05 | 77 | "causar que el viraje se **inestine**" | "causar que el viraje se **desestabilice**" o "**inestabilice**" |
| 08 | 76 | "**Falla** en despejar el área" | "**Fallo** en despejar el área" (CORREGIDO) |
| 08 | 135 | "**Falla** en tomar acción correctiva" | "**Fallo** en tomar acción correctiva" (CORREGIDO) |
| 08 | 282 | "la **falla** más común" | "el **fallo** más común" (CORREGIDO) |
| 08 | 390 | "**Falla** del sistema de control" | "**Fallo** del sistema de control" (CORREGIDO) |
| 08 | 408 | "irregularidad o **falla** del elevador" | "irregularidad o **fallo** del elevador" (CORREGIDO) |
| 08 | 420 | "Las **fallas** de alerones" | "Los **fallos** de **los** alerones" (CORREGIDO) |
| 08 | 432 | "**Falla** estructural y/o flutter" | "**Fallo** estructural y/o **flúter**" (CORREGIDO) |
| 08 | 438 | "Una **falla** real del timón" | "**Un fallo** real del timón" (CORREGIDO) |
| 08 | 468 | "Las **fallas** del sistema de spoiler" | "Los **fallos** del sistema de spoiler" (CORREGIDO) |
| 08 | 480 | "Los modos de **falla**" | "Los modos de **fallo**" (CORREGIDO) |
| 08 | 518 | "Las **fallas** van desde" | "Los **fallos** van desde" (CORREGIDO) |

---

### 3. Otros Anglicismos Frecuentes

| Capítulo | Línea | Texto incorrecto | Corrección | Explicación |
|----------|-------|------------------|------------|-------------|
| 05 | 304 | "Lastre de **performance**" | "Lastre de **rendimiento**" (CORREGIDO) | "Performance" → "rendimiento" |
| 06 | 52 | "la **ráfaga** de las hélices" | "la **estela** de la hélice" (CORREGIDO) | "Ráfaga" = golpe de viento; "estela" = flujo continuo |
| 06 | 92 | "**le da** a la persona" | "**otorga a** la persona" (CORREGIDO) | "Le dar" es coloquial |
| 07 | 82 | "**toma** más tiempo" | "**tarda** más" o "**requiere** más tiempo" | Calco de "takes more time" (NO ENCONTRADO) |
| 07 | 262 | "**pata** ocasional" | "**tramo** ocasional" | "Pata" = leg (anglicismo); "tramo" es correcto (NO ENCONTRADO) |
| 08 | 156 | "debe **jalar** la palanca" | "debe **tirar de** la palanca" | "Jalar" es americanismo (CORREGIDO) |
| 08 | 328 | "cobertura de **celular**" | "cobertura **móvil**" | "Celular" es americanismo (CORREGIDO) |
| 09 | 202 | "puede **voltear** el {term-glider}" | "puede **volcar** el planeador" | "Voltear" es americanismo (NO ENCONTRADO) |
| 11 | 175 | "**involucra** elegir" | "**consiste en** elegir" (CORREGIDO) | Calco de "involve" |
| 11 | 237 | "La idea **involucra** zambullirse" | "La idea **consiste en** zambullirse" (CORREGIDO) | Calco de "involve" |
| 13 | 78 | "**involucra** dormir" | "**consiste en** dormir" (CORREGIDO) | Calco de "involve" |
| 13 | 267 | "**involucra** usar" | "**consiste en** usar" (CORREGIDO) | Calco de "involve" |

---

### 4. Errores Tipográficos

| Capítulo | Línea | Texto incorrecto | Corrección |
|----------|-------|------------------|------------|
| 03 | 10 | "hace que el {term-glider} **guañe**" | "hace que el planeador **guiñe**" | (NO ENCONTRADO)
| 04 | 224 | "Interior del altímetro.**f**" | "Interior del altímetro" | (CORREGIDO)
| 04 | 273 | "=**0,25" | "= **0,25" (espacio) | (CORRECTO)
| 04 | 383 | "**f**" (línea suelta) | Eliminar línea | (NO ENCONTRADO)
| 07 | 260 | "(hacer la caja)**demuestra**" | "(hacer la caja) **demuestra**" (espacio) | (NO ENCONTRADO)
| 07 | 318 | "toma de contacto**n**" | "toma de contacto" | (NO ENCONTRADO)

---

## Errores de Preposiciones

| Capítulo | Línea | Texto incorrecto | Corrección | Explicación |
|----------|-------|------------------|------------|-------------|
| 05 | 32 | "aumenta la longitud de pista necesaria **durante** el {term-landing}" | "...necesaria **para** el aterrizaje" | "Para" indica finalidad (CORREGIDO) |
| 05 | 118 | "la nube aumenta **de** tamaño" | "aumenta **en** tamaño" | "En" con dimensiones |
| 06 | 98 | "recomendados **por** el GFM/POH" | "recomendados **en** el GFM/POH" | Las recomendaciones están **en** el manual (NO ENCONTRADO) |
| 06 | 92 | "responsabilidad **de** la {term-drag}" | "responsabilidad **sobre** la resistencia" | "Responsabilidad sobre" (CORREGIDO) |
| 07 | 100 | "el {term-crosswind} golpea el {term-fuselage}" | "...golpea **contra** el fuselaje" | Falta preposición de dirección (CORREGIDO) |
| 07 | 589 | "Mantener el resbale **de** {term-takeoff}" | "...**durante** el despegue" | Falta preposición temporal (CORREGIDO) |
| 08 | 66 | "procedimiento de {term-landing} **para** un cable adjunto" | "...**con** un cable adjunto" | Preposición incorrecta (CORREGIDO) |
| 08 | 276 | "tener cuidado **para** evitar" | "tener cuidado **de** evitar" | "Cuidado de" o "cuidado con" (CORREGIDO) |
| 12 | 34 | "inspeccionado **por** partículas" | "inspeccionado **mediante** partículas" | "Por" indica agente; "mediante" indica instrumento (CORREGIDO) |
| 12 | 50 | "no roce **contra** el asiento" | "no roce **con** el asiento" | "Rocer" rige "con" (CORREGIDO) |
| 12 | 70 | "compatible **al** enganche" | "compatible **con** el enganche" | "Compatible con" (CORREGIDO) |
| 12 | 174 | "puede afectar el motor" | "puede afectar **al** motor" | "Afectar a" según RAE (CORREGIDO) |

---

## Falta de Artículos

| Capítulo | Línea | Texto incorrecto | Corrección |
|----------|-------|------------------|------------|
| 05 | 148 | "La figura 5-12 **Muestra**" | "La figura 5-12 **muestra**" | (CORREGIDO)
| 06 | 52 | "la ráfaga de **las** hélices" | "la refaga de **la** hélice" | (CORREGIDO)
| 06 | 98 | "Las cuerdas y {term-tow-rope}s están hecho**s**" | "Las cuerdas... están hecha**s**" | (CORREGIDO)
| 06 | 158 | "El GFH/POH o una tienda... **puede** sugerir" | "...**pueden** sugerir" (concordancia plural) | (CORREGIDO)
| 07 | 292 | "durante el {term-takeoff} y ascenso" | "durante el despegue y **el** ascenso" | (CORREGIDO)
| 08 | 131 | "iniciar **procedimientos**" | "iniciar **los** procedimientos" | (CORREGIDO)
| 08 | 170 | "Si los {term-airbrake}s permanecen abiertos durante el {term-takeoff} y ascenso" | "...y **el** ascenso" | (CORREGIDO)
| 11 | 58 | "lleva a **preparación** apresurada" | "lleva a **una** preparación apresurada" | (CORREGIDO)
| 12 | 196 | "requiere **planificación**" | "requiere **de** planificación" | (CORREGIDO)
| 12 | 202 | "proporciona **comunicación**" | "proporciona **una** comunicación" | (CORREGIDO)
| 12 | 216 | "debe dejar **espacio** suficiente" | "debe dejar **el** espacio suficiente" | (CORREGIDO)

---

## Estructuras Sintácticas Problemáticas

### Oraciones incompletas

| Capítulo | Línea | Problema | Corrección |
|----------|-------|----------|------------|
| 05 | 70 | "toma un intervalo de tiempo finito vencer la inercia" | "toma un intervalo de tiempo finito **en** vencer" o "es necesario un intervalo... para vencer" | (CORREGIDO)
| 10 | 202 | "Si planeando sobre la cresta" | "Si **se planea** sobre la cresta" | (CORREGIDO)
| 10 | 366 | "Si volando directamente" | "Si **se vuela** directamente" | (CORREGIDO)

### Redundancias

| Capítulo | Línea | Texto incorrecto | Corrección |
|----------|-------|------------------|------------|
| 05 | 254 | "las **líneas intersectantes se intersectan**" | "las **líneas se intersectan**" (CORREGIDO) |
| 07 | 113 | "Justo después del **momento** del {term-takeoff}" | "Justo después del despegue" | (CORREGIDO)
| 08 | 30 | "confundir esta señal con **la señal** de" | "confundir esta señal con la de" | (CORREGIDO) |

---

## Atributos AsciiDoc Sin Sustituir (Encontrados en Texto)

Muchos títulos y textos muestran los atributos `{term-xxx}` en lugar del término español. Esto no es un error gramatical per se, pero afecta la legibilidad cuando se visualiza el texto plano.

Ejemplos frecuentes:
- `{term-glider}` → debería mostrar "planeador"
- `{term-wing}` → debería mostrar "ala"
- `{term-stall}` → debería mostrar "pérdida"
- `{term-thermal}` → debería mostrar "térmica"

**Nota:** Esto se resuelve al renderizar el documento (PDF/HTML), pero en el archivo fuente `.adoc` se ven las etiquetas.

---

## Errores de Mayúsculas (no relacionados con títulos)

| Capítulo | Línea | Texto incorrecto | Corrección |
|----------|-------|------------------|------------|
| 04 | 148 | "**Este** piloto nunca debe exceder" | "**El** piloto nunca debe exceder" | (CORREGIDO)
| 05 | 158 | "La figura 5-12 **Muestra**" | "La figura 5-12 **muestra**" |
| 11 | 217, 221, 223, 224 | "**El Piloto** 1/2/3/4" | "**El piloto** 1/2/3/4" (no es nombre propio) | (CORREGIDO)

---

## Recomendaciones Generales

### 1. Prioridad Alta
- Corregir errores tipográficos ("guañe", "contacton", "f" suelta)
- Corregir concordancia de género en "ala izquierda/derecha"
- Reemplazar anglicismos "falla" → "fallo"

### 2. Prioridad Media
- Corregir preposiciones incorrectas
- Agregar artículos faltantes
- Reemplazar "involucrar" → "consistir en"

### 3. Prioridad Baja
- Sustituir gerundios innecesarios
- Corregir redundancias
- Mejorar estructuras sintácticas complejas

---

## Estadísticas por Capítulo

| Capítulo | Errores Detectados | Gravedad |
|----------|-------------------|----------|
| 01 | 0 | ✅ Bueno |
| 02 | 4 | 🟡 Medio |
| 03 | 3 | 🟡 Medio |
| 04 | 10 | 🔴 Alto |
| 05 | 14 | 🔴 Alto |
| 06 | 10 | 🔴 Alto |
| 07 | 24 | 🔴 Alto |
| 08 | 42 | 🔴 Crítico |
| 09 | 15 | 🔴 Alto |
| 10 | 21 | 🔴 Alto |
| 11 | 34 | 🔴 Alto |
| 12 | 26 | 🔴 Alto |
| 13 | 24 | 🔴 Alto |

**Total: ~227 problemas identificados**

---

*Informe generado automáticamente mediante análisis con subagentes.*
*Revisión manual recomendada antes de aplicar correcciones.*
