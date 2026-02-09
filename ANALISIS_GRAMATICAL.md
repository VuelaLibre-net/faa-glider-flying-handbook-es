# Análisis Gramatical y Ortográfico (RAE)

Este documento detalla el análisis realizado sobre los ficheros en `es/capitulos/` siguiendo las directrices de la Real Academia Española (RAE) y las convenciones aeronáuticas estándar.

## Resumen Ejecutivo

Se han identificado patrones recurrentes de:
1.  **Anglicismos y Calcos Semánticos**: Traducciones literales que no corresponden al uso natural en español (ej. "estancada" para *stalled*, "balance" para *balance/equilibrium*, "compuesto" para *compound/combination*).
2.  **Terminología Inconsistente**: Variación en términos clave como "resbale" vs "deslizamiento", "perilla" vs "knob".
3.  **Gramática y Estilo**: Uso de gerundios en títulos, coordinación de adverbios en *-mente*, y concordancia de género.

## Hallazgos Principales

### 1. Terminología Aerodinámica: "Stall" vs "Estancamiento/Pérdida"

**Problema Crítico**: Se ha detectado el uso del término "estancada" o "estancamiento" para referirse al fenómeno aerodinámico de *stall*. En español aeronáutico, el término correcto y estándar es **pérdida**. "Estancar" significa detener el flujo de un fluido (como agua en un estanque), no la separación de la capa límite en un ala.

*   **Archivo**: `03-aerodinamica-del-vuelo.adoc`
    *   *Texto actual*: "...un {term-wing} se estanca más que la otra."
    *   *Corrección*: "...un {term-wing} entra en pérdida más que la otra."
    *   *Texto actual*: "...el {term-wing} más completamente estancada..."
    *   *Corrección*: "...el {term-wing} que ha entrado en pérdida más profundamente..."
    *   *Texto actual*: "...estancamiento del {term-wing}..."
    *   *Corrección*: "...entrada en pérdida del ala..."

### 2. Terminología Médica: "Stagnant Hypoxia"

**Problema**: Traducción literal "Hipoxia estancada".
*   **Archivo**: `13-factores-humanos.adoc`
    *   *Texto actual*: "Hipoxia estancada"
    *   *Corrección*: **Hipoxia por estancamiento** o **Hipoxia isquémica**. La RAE define "estancado" como suspendido o detenido, lo cual es semánticamente cercano, pero la terminología médica prefiere "por estancamiento".

### 3. Anglicismos Léxicos

Se han encontrado palabras en inglés o adaptaciones incorrectas que deben ser corregidas:

*   **Knob**:
    *   **Archivo**: `04-instrumentos-de-vuelo.adoc`
    *   *Texto actual*: "...ajustando el knob de control..."
    *   *Corrección*: **mando**, **perilla** o **botón**.
*   **Sustainer**:
    *   **Archivo**: `01-planeadores-y-veleros.adoc`, `02-componentes-y-sistemas.adoc`
    *   *Texto actual*: "...motor (sustainer)..."
    *   *Corrección*: Debe ir en cursiva (*sustainer*) si se mantiene como término extranjero, o traducirse como **motor de sustento** / **motor de crucero**.
*   **Balance**:
    *   **Archivo**: `13-factores-humanos.adoc`
    *   *Texto actual*: "...coordinación, velocidad, fuerza y balance."
    *   *Corrección*: **equilibrio**. "Balance" en español se refiere al movimiento de vaivén o a un estado de cuentas (balance contable). Para estabilidad física, se usa "equilibrio".
*   **Compuesto**:
    *   **Archivo**: `13-factores-humanos.adoc`
    *   *Texto actual*: "El compuesto de severidad predicha y probabilidad..."
    *   *Corrección*: **La combinación** o **El conjunto**.
*   **Vienen en una variedad**:
    *   **Archivo**: `02-componentes-y-sistemas.adoc`
    *   *Texto actual*: "...vienen en una variedad de formas..."
    *   *Corrección*: **se presentan en** o **existen en**. "Vienen" es un calco de "come in".

### 4. Gramática y Estilo

#### Coordinación de Adverbios (Regla RAE)
Cuando dos o más adverbios terminados en *-mente* se coordinan, solo el último debe llevar la terminación.
*   **Archivo**: `13-factores-humanos.adoc`
*   *Texto actual*: "...soplar lentamente y suavemente..."
*   *Corrección*: "...soplar **lenta y suavemente**..."

#### Concordancia
*   **Archivo**: `03-aerodinamica-del-vuelo.adoc`
*   *Texto actual*: "Juntas, estos modelos..."
*   *Corrección*: "**Juntos**, estos modelos..." (referencia a "Tercera Ley" y "Principio", uno femenino y otro masculino -> masculino plural).
*   *Texto actual*: "...a través de ella..." (refiriéndose al aire).
*   *Corrección*: "...a través de **él**..."

#### Inconsistencia en Terminología
*   **Resbale vs. Deslizamiento**:
    *   En `03-aerodinamica` se usa "Resbale" (correcto para *slip*).
    *   En `04-instrumentos` se usa "Deslizamiento" y "Deslizamiento excesivo".
    *   *Recomendación*: Unificar a **Resbale** (Slip) y **Derrape** (Skid) para mantener consistencia técnica.

### 5. Puntuación y Formato

*   **Coma Oxford**: Se detectó uso de la coma antes de la "y" en enumeraciones simples (ej. "A, B, y C"). En español no se usa salvo para evitar ambigüedad.
    *   *Ejemplo*: "colegio, universidad, o club" -> "colegio, universidad o club".
*   **Paréntesis y Corchetes**:
    *   **Archivo**: `04-instrumentos-de-vuelo.adoc`
    *   *Texto actual*: `["Hg]`
    *   *Corrección*: Revisar el cierre de corchetes o comillas. Probablemente debería ser `["Hg"]` o `("Hg)`.

## Acciones Recomendadas

1.  Ejecutar un reemplazo global de "estancada/o" por "en pérdida" o "pérdida" en contextos aerodinámicos.
2.  Unificar "deslizamiento/deslizamiento excesivo" a "resbale/derrape".
3.  Corregir la lista de anglicismos identificados (*knob*, *balance*).
4.  Revisar manualmente los casos de concordancia "Juntas" y adverbios en *-mente*.

