# Análisis de Cumplimiento Norma RAE

Fecha: 2026-02-08

## Resumen Ejecutivo

Se han identificado **múltiples incumplimientos** de la norma de la RAE en los documentos de traducción, principalmente relacionados con:

1. **Capitalización en títulos** - Más de 100 títulos con palabras en mayúscula que deberían ir en minúscula
2. **Uso de "etc" sin puntos suspensivos** - Debe ser "etc."
3. **Números decimales con punto** - En español se usa la coma (3,5 en lugar de 3.5)

---

## 1. CAPITALIZACIÓN EN TÍTULOS (Estilo oración - RAE)

**Norma RAE**: En español, los títulos deben usar "estilo oración": solo la primera palabra lleva mayúscula inicial, excepto nombres propios y siglas.

### Archivos con mayor número de incidencias:

#### `es/capitulos/04-instrumentos-de-vuelo.adoc`
```
Línea 42:  Indicador de Velocidad Aerodinámica: Anemómetro
           → Indicador de velocidad aerodinámica: anemómetro

Línea 73:  Tipos de Velocidad Aerodinámica
           → Tipos de velocidad aerodinámica

Línea 82:  Velocidad Aerodinámica Indicada (IAS)
           → Velocidad aerodinámica indicada (IAS)

Línea 124: Marcas del Indicador de Velocidad Aerodinámica
           → Marcas del indicador de velocidad aerodinámica
```

#### `es/capitulos/13-factores-humanos.adoc`
```
Línea 59:  Factores Fisiológicos/Médicos que Afectan el Rendimiento del Piloto
           → Factores fisiológicos/médicos que afectan el rendimiento del piloto

Línea 229: Sistema de Flujo Continuo
           → Sistema de flujo continuo

Línea 245: Sistema de Demanda de Pulso Electrónico (EDS)
           → Sistema de demanda de pulso electrónico (EDS)
```

#### `es/capitulos/03-aerodinamica-del-vuelo.adoc`
```
Línea 16:  Fuerzas del Vuelo
           → Fuerzas del vuelo

Línea 94:  Efecto Suelo
           → Efecto suelo

Línea 205: Factor de Carga
           → Factor de carga
```

### Lista completa de títulos a corregir:

| Archivo | Línea | Título actual (incorrecto) | Título correcto (RAE) |
|---------|-------|---------------------------|----------------------|
| 01-planeadores-y-veleros.adoc | 42 | Elegibilidad para la Habilitación | Elegibilidad para la habilitación |
| 01-planeadores-y-veleros.adoc | 50 | Elegibilidad Médica | Elegibilidad médica |
| 01-planeadores-y-veleros.adoc | 60 | Resumen del Capítulo | Resumen del capítulo |
| 02-componentes-y-sistemas.adoc | 79 | Dispositivos de Gancho de Remolque | Dispositivos de gancho de remolque |
| 02-componentes-y-sistemas.adoc | 87 | Grupo Motopropulsor | Grupo motopropulsor |
| 03-aerodinamica-del-vuelo.adoc | 16 | Fuerzas del Vuelo | Fuerzas del vuelo |
| 03-aerodinamica-del-vuelo.adoc | 94 | Efecto Suelo | Efecto suelo |
| 03-aerodinamica-del-vuelo.adoc | 140 | Torsión Geométrica (Washout) | Torsión geométrica (washout) |
| 03-aerodinamica-del-vuelo.adoc | 162 | Estabilidad Lateral | Estabilidad lateral |
| 03-aerodinamica-del-vuelo.adoc | 182 | Oscilación Inducida por el Piloto (PIO) | Oscilación inducida por el piloto (PIO) |
| 04-instrumentos-de-vuelo.adoc | 12 | Instrumentos Pitot-Estática | Instrumentos pitot-estática |
| 04-instrumentos-de-vuelo.adoc | 22 | Líneas de Presión de Impacto y Estática | Líneas de presión de impacto y estática |
| 04-instrumentos-de-vuelo.adoc | 62 | Los Efectos de la Altitud en el anemómetro | Los efectos de la altitud en el anemómetro |
| 04-instrumentos-de-vuelo.adoc | 73 | Tipos de Velocidad Aerodinámica | Tipos de velocidad aerodinámica |
| 04-instrumentos-de-vuelo.adoc | 82 | Velocidad Aerodinámica Indicada (IAS) | Velocidad aerodinámica indicada (IAS) |
| 04-instrumentos-de-vuelo.adoc | 108 | Velocidad Aerodinámica Calibrada (CAS) | Velocidad aerodinámica calibrada (CAS) |
| 04-instrumentos-de-vuelo.adoc | 116 | Velocidad Aerodinámica Verdadera (TAS) | Velocidad aerodinámica verdadera (TAS) |
| 04-instrumentos-de-vuelo.adoc | 124 | Marcas del Indicador de Velocidad Aerodinámica | Marcas del indicador de velocidad aerodinámica |
| 04-instrumentos-de-vuelo.adoc | 150 | Efecto de la Altitud en V~NE~ | Efecto de la altitud en V~NE~ |
| 04-instrumentos-de-vuelo.adoc | 171 | Otras Limitaciones de Velocidad Aerodinámica | Otras limitaciones de velocidad aerodinámica |
| 04-instrumentos-de-vuelo.adoc | 215 | Principios de Operación | Principios de operación |
| 04-instrumentos-de-vuelo.adoc | 229 | Tipos de Altitud | Tipos de altitud |
| 04-instrumentos-de-vuelo.adoc | 249 | Efecto de la Presión No Estándar | Efecto de la presión no estándar |
| 04-instrumentos-de-vuelo.adoc | 281 | Efecto de la Temperatura No Estándar | Efecto de la temperatura no estándar |
| 04-instrumentos-de-vuelo.adoc | 400 | Brújula Magnética | Brújula magnética |
| 12-remolque.adoc | 136 | Posiciones de Remolque, Virajes y Suelta | Posiciones de remolque, virajes y suelta |
| 12-remolque.adoc | 194 | Remolque de Travesía | Remolque de travesía |
| 13-factores-humanos.adoc | 15 | Reconociendo Actitudes Peligrosas | Reconociendo actitudes peligrosas |
| 13-factores-humanos.adoc | 47 | Error del Piloto | Error del piloto |
| 13-factores-humanos.adoc | 51 | Tipos de Errores | Tipos de errores |
| 13-factores-humanos.adoc | 59 | Factores Fisiológicos/Médicos que Afectan el Rendimiento del Piloto | Factores fisiológicos/médicos que afectan el rendimiento del piloto |
| 13-factores-humanos.adoc | 255 | Gestión de Riesgo | Gestión de riesgo |

*(Ver archivo completo para lista exhaustiva de 100+ incidencias)*

---

## 2. ABREVIATURAS SIN PUNTOS

**Norma RAE**: Las abreviaturas deben llevar punto.

### Incidencias encontradas:

| Archivo | Línea | Texto incorrecto | Corrección |
|---------|-------|-----------------|------------|
| 04-instrumentos-de-vuelo.adoc | 243 | TAS, etc | TAS, etc. |
| 10-tecnicas-vuelo-vela.adoc | 238 | turbulencia, etc | turbulencia, etc. |
| 11-vuelo-travesia.adoc | 60 | encendido, etc | encendido, etc. |
| 11-vuelo-travesia.adoc | 309 | oxígeno, etc | oxígeno, etc. |

---

## 3. NÚMEROS DECIMALES

**Norma RAE**: En español, el separador decimal es la coma (,), no el punto (.).

### Incidencias encontradas:

| Archivo | Línea | Texto incorrecto | Corrección |
|---------|-------|-----------------|------------|
| 04-instrumentos-de-vuelo.adoc | 425 | 1.0 veces | 1,0 veces |
| 05-performance.adoc | 88 | raíz cuadrada de 2 o 1.41 | raíz cuadrada de 2 o 1,41 |
| 05-performance.adoc | 150 | 1.9 nudos | 1,9 nudos |
| 05-performance.adoc | 150 | 2.1 nudos | 2,1 nudos |
| 05-performance.adoc | 271 | 14.8–18.6 in | 14,8–18,6 in |
| 07-lanzamiento-aterrizaje-maniobras.adoc | 816 | (50/40)*2 = 1.56 | (50/40)*2 = 1,56 |
| 08-emergencias.adoc | 592 | 1.5 millas | 1,5 millas |

### 3a. APÓSTROFO COMO SEPARADOR DECIMAL (Uso incorrecto)

**Norma RAE**: El separador decimal debe ser la **coma**, nunca el apóstrofo.

Se encontró uso incorrecto del apóstrofo (') como separador decimal en ajustes de altímetro:

| Archivo | Línea | Texto incorrecto | Corrección |
|---------|-------|-----------------|------------|
| 04-instrumentos-de-vuelo.adoc | 257 | 29'92 | 29,92 |
| 04-instrumentos-de-vuelo.adoc | 261 | 29'85 | 29,85 |
| 04-instrumentos-de-vuelo.adoc | 263 | 29'94 | 29,94 |
| 04-instrumentos-de-vuelo.adoc | 269 | 29'94 | 29,94 |
| 04-instrumentos-de-vuelo.adoc | 271 | 29'69 | 29,69 |
| 04-instrumentos-de-vuelo.adoc | 273 | 0'25 | 0,25 |
| 04-instrumentos-de-vuelo.adoc | 277 | 0'25 | 0,25 |

**Total: 8 instancias**

### 3b. SEPARADOR DE MILES

**Norma RAE**: El separador de miles debe ser un **espacio** (preferiblemente **espacio duro/no-breaking space** U+00A0) para evitar división de línea.

Se encontraron números con espacio normal (U+0020) que deberían tener espacio duro (U+00A0):

| Archivo | Línea | Número actual | Corrección (con NBSP) |
|---------|-------|--------------|----------------------|
| 04-instrumentos-de-vuelo.adoc | 257 | 18 000 | 18&nbsp;000 |
| 04-instrumentos-de-vuelo.adoc | 259 | 1 000 | 1&nbsp;000 |
| 04-instrumentos-de-vuelo.adoc | 261 | 18 000 | 18&nbsp;000 |
| 04-instrumentos-de-vuelo.adoc | 263 | 1 000 | 1&nbsp;000 |
| 04-instrumentos-de-vuelo.adoc | 263 | 2 430 | 2&nbsp;430 |
| 04-instrumentos-de-vuelo.adoc | 263 | 3 400 | 3&nbsp;400 |
| 04-instrumentos-de-vuelo.adoc | 267 | 3 400 | 3&nbsp;400 |
| 04-instrumentos-de-vuelo.adoc | 275 | 1 000 | 1&nbsp;000 |
| 04-instrumentos-de-vuelo.adoc | 277 | 1 000 | 1&nbsp;000 |
| 04-instrumentos-de-vuelo.adoc | 283 | 10 000 | 10&nbsp;000 |

**Nota**: Los valores técnicos como 29.92 "Hg (pulgadas de mercurio estándar) y referencias FAA-H-8083-13B pueden mantenerse con punto por ser valores técnicos internacionales.

---

## 4. COMILLAS

**Norma RAE**: Se deben usar comillas latinas (« ») en lugar de comillas rectas (" ").

### Estado: ✅ CORRECTO

No se encontraron comillas rectas usadas incorrectamente en el texto. Las únicas comillas rectas encontradas son:
- Unidades técnicas: `"Hg` (pulgadas de mercurio) - Uso correcto
- Atributos AsciiDoc: `cols="1,1"` - Sintaxis requerida
- Referencias internas: `<<fig-04-01>>` - Sintaxis requerida

---

## 5. ESPACIOS ANTES DE SIGNOS DE PUNTUACIÓN

**Norma RAE**: No debe haber espacio antes de `?`, `!`, `:`, `;`.

### Estado: ✅ CORRECTO

No se encontraron espacios incorrectos antes de signos de puntuación.

---

## 6. TÉRMINOS EN INGLÉS SIN TRADUCIR

Se encontraron fragmentos en inglés que parecen ser notas del documento original:

| Archivo | Línea | Texto | Acción recomendada |
|---------|-------|-------|-------------------|
| 03-aerodinamica-del-vuelo.adoc | 40 | "A mathematical relationship exists between lift..." | Eliminar o traducir |
| 12-remolque.adoc | 199 | ".Cross-country tow." | Traducir o eliminar punto inicial |

---

## Recomendaciones

### Prioridad Alta
1. **Corregir títulos**: Más de 100 títulos necesitan cambio a "estilo oración"
2. **Corregir "etc"**: Agregar punto (etc.)
3. **Corregir decimales**: Cambiar punto por coma en números decimales

### Prioridad Media
4. Revisar términos en inglés sueltos

### Automatización sugerida
```bash
# Para corregir títulos, se podría usar:
sed -i 's/== \([A-Z][a-z]*\) \([A-Z][a-z]*\)/== \1 \L\2/g' es/capitulos/*.adoc

# Para corregir etc:
sed -i 's/\betc\b/etc./g' es/capitulos/*.adoc
```

---

## Conclusión

El documento tiene principalmente problemas de **capitalización en títulos**, un error común al traducir desde el inglés donde el estilo de títulos es diferente (Title Case). Se recomienda una revisión sistemática de todos los títulos para ajustarlos a la norma de la RAE (estilo oración).

---

*Informe generado automáticamente. Verificación manual recomendada para casos especiales.*
