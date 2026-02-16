# Descripción de Variables - Dataset de Divorcios en Guatemala
**Período:** 2011-2021  
**Total de registros:** 56,349 divorcios  
**Total de variables:** 12

---

## Descripción Detallada de las 12 Variables

### 1. AÑOREG - Año de Registro

**Descripción:** Año en que se registró formalmente el divorcio ante el Registro Civil.

**Tipo de variable:** Numérica (año calendario)

**Rango:** 2011-2021 (11 años completos)

---

### 2. DEPOCU - Departamento de Ocurrencia

**Descripción:** Departamento (división administrativa de primer nivel) donde se emitió la sentencia de divorcio o donde ocurrió el proceso legal.

**Tipo de variable:** Categórica geográfica

**Valores únicos:** 28 departamentos (nota: Guatemala tiene 22 departamentos oficiales; los 6 adicionales pueden incluir categorías como "Extranjero" o "No especificado")

---

### 3. DEPREG - Departamento de Registro

**Descripción:** Departamento donde se registró oficialmente el divorcio ante el Registro Civil, que puede ser diferente del departamento donde ocurrió el proceso.

**Tipo de variable:** Categórica geográfica

**Valores únicos:** 28 departamentos

---

### 4. DIAOCU - Día de Ocurrencia

**Descripción:** Día del mes (1-31) en que se emitió la sentencia de divorcio o se finalizó el proceso legal.

**Tipo de variable:** Numérica discreta

**Rango:** 1 a 31

---

### 5. EDADHOM - Edad del Hombre

**Descripción:** Edad en años cumplidos del ex-cónyuge masculino al momento del divorcio.

**Tipo de variable:** Numérica continua

**Valores válidos:** 25,467 (45.2% del total)  
**Valores "Ignorados":** 30,882 (54.8% del total)

**Estadísticas (solo valores válidos):**
- **Mínimo:** 15 años
- **Máximo:** 96 años
- **Media:** 35.5 años
- **Mediana:** 33 años
- **Desviación estándar:** 10.2 años

**Distribución estimada (valores válidos):**
- 20-29 años: ~25%
- 30-39 años: ~40%
- 40-49 años: ~20%
- 50+ años: ~15%

---

### 6. EDADMUJ - Edad de la Mujer

**Descripción:** Edad en años cumplidos de la ex-cónyuge femenina al momento del divorcio.

**Tipo de variable:** Numérica continua

**Valores válidos:** 25,584 (45.4% del total)  
**Valores "Ignorados":** 30,765 (54.6% del total)

**Estadísticas (solo valores válidos):**
- **Mínimo:** 14 años
- **Máximo:** 80 años
- **Media:** 32.2 años
- **Mediana:** 30 años
- **Desviación estándar:** 9.3 años

**Distribución estimada (valores válidos):**
- 20-29 años: ~40%
- 30-39 años: ~35%
- 40-49 años: ~15%
- 50+ años: ~10%

---

### 7. MESOCU - Mes de Ocurrencia

**Descripción:** Mes del año en que se emitió la sentencia de divorcio o se finalizó el proceso.

**Tipo de variable:** Categórica temporal

**Valores únicos:** 12 meses del año

---

### 8. MESREG - Mes de Registro

**Descripción:** Mes del año en que se registró oficialmente el divorcio ante el Registro Civil.

**Tipo de variable:** Categórica temporal

**Valores únicos:** 12 meses del año

---

### 9. MUPOCU - Municipio de Ocurrencia

**Descripción:** Municipio (división administrativa de segundo nivel) donde se emitió la sentencia de divorcio.

**Tipo de variable:** Categórica geográfica

**Valores únicos:** 331 municipios diferentes (de 340 municipios en Guatemala)

---

### 10. MUPREG - Municipio de Registro

**Descripción:** Municipio donde se registró oficialmente el divorcio ante las oficinas del Registro Civil.

**Tipo de variable:** Categórica geográfica

**Valores únicos:** 331 municipios diferentes

---

### 11. NACHOM - Nacionalidad del Hombre

**Descripción:** País de nacionalidad legal del ex-cónyuge masculino.

**Tipo de variable:** Categórica nominal

**Valores únicos:** 72 nacionalidades diferentes (vs 38 en matrimonios)

**Distribución:**
- **Guatemala:** 55,226 (98.01%)
- **Extranjeros:** 1,123 (1.99%)
- **Ignorado:** 191 (incluido en extranjeros)

---

### 12. NACMUJ - Nacionalidad de la Mujer

**Descripción:** País de nacionalidad legal de la ex-cónyuge femenina.

**Tipo de variable:** Categórica nominal

**Valores únicos:** 55 nacionalidades diferentes (vs 32 en matrimonios)

**Distribución:**
- **Guatemala:** 55,219 (97.99%)
- **Extranjeras:** 1,130 (2.01%)
- **Ignorado:** 202 (incluido en extranjeras)

---

## Relaciones Entre Variables

### Variables Temporales
- **AÑOREG, MESOCU, MESREG, DIAOCU:** Permiten análisis temporal completo
- **AÑOREG:** Variable clave para tendencias de 11 años
- **MESOCU vs MESREG:** Diferencia entre sentencia y registro

### Variables Geográficas
- **DEPOCU, DEPREG:** Análisis departamental
- **MUPOCU, MUPREG:** Análisis municipal detallado
- **Comparación ocurrencia vs registro:** Movilidad administrativa

### Variables Demográficas
- **EDADHOM, EDADMUJ:** 
  - Calcular diferencia de edad
  - **LIMITACIÓN:** 54% de datos faltantes
- **NACHOM, NACMUJ:** Identificar divorcios internacionales

### Variables Ausentes (vs Matrimonios)
- **Sin CLAUNI:** No se registra tipo de unión en divorcios
- **Sin ESCHOM/ESCMUJ:** No hay información educativa

---

## Preguntas que Puedes Responder con este Dataset

### Temporales
1. ¿Cómo ha evolucionado la tasa de divorcios en Guatemala (2011-2021)?
2. ¿Qué impacto tuvo COVID-19 en los divorcios (2020-2021)?
3. ¿En qué meses del año se divorcian más las personas?
4. ¿Existe estacionalidad en los divorcios?

### Geográficas
5. ¿Qué departamentos tienen más divorcios?
6. ¿Cuál es la diferencia entre divorcios urbanos y rurales?
7. ¿Dónde se concentran los servicios de divorcio?
8. ¿Hay movilidad entre municipio de sentencia y registro?

### Demográficas (limitado por datos faltantes)
9. ¿A qué edad se divorcian las personas en Guatemala?
10. ¿Cuál es la diferencia de edad entre hombres y mujeres al divorciarse?
11. ¿Cuánto tiempo aproximadamente dura un matrimonio? (edad divorcio - edad matrimonio)

### Internacionales
12. ¿Cuántos divorcios involucran extranjeros?
13. ¿Qué nacionalidades están más representadas?
14. ¿Los matrimonios binacionales tienen mayor tasa de divorcio?

### Comparativas
15. ¿Cómo se comparan los patrones de divorcio con los de matrimonio?
16. ¿Hay diferencias estacionales entre matrimonios y divorcios?
17. ¿Los divorcios se concentran más en ciudades que los matrimonios?

---

## Variables Clave por Tipo de Análisis

### Para Series Temporales
- **AÑOREG** (principal)
- MESOCU
- MESREG

### Para Análisis Geográfico
- **DEPOCU, DEPREG** (departamental)
- **MUPOCU, MUPREG** (municipal)

### Para Análisis Demográfico (limitado)
- EDADHOM (45% disponible)
- EDADMUJ (45% disponible)

### Para Análisis Internacional
- NACHOM
- NACMUJ
