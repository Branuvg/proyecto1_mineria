# 📊 ANÁLISIS DATASET CONSOLIDADO DE MATRIMONIOS
## Base de Datos Multi-Año (750,000 registros)

---

## 📋 RESUMEN EJECUTIVO

**Características del Dataset:**
- 🗄️ **Registros:** ~750,000 matrimonios
- 📅 **Periodo:** Multi-año (varios años consolidados)
- 🗂️ **Variables:** 15 variables comunes
- 🌍 **Cobertura:** Guatemala, todos los departamentos
- 🔧 **Tipo:** Dataset limpio y estandarizado

**Decisión de diseño:**
Solo se incluyeron las variables que aparecían **consistentemente** en todos los años, garantizando compatibilidad y uniformidad de datos.

---

## 🗂️ DICCIONARIO DE VARIABLES (15 VARIABLES)

### 📅 INFORMACIÓN TEMPORAL

| # | Variable | Nombre Completo | Descripción | Tipo |
|---|----------|----------------|-------------|------|
| 1 | **AÑOREG** | **Año de Registro** | Año en que se inscribió el matrimonio | Numérico (YYYY) |
| 10 | **MESREG** | **Mes de Registro** | Mes en que se inscribió el matrimonio | 1-12 |
| 11 | **MESOCU** | **Mes de Ocurrencia** | Mes en que se celebró el matrimonio | 1-12 |
| 5 | **DIAOCU** | **Día de Ocurrencia** | Día en que se celebró el matrimonio | 1-31 |

### 🗺️ INFORMACIÓN GEOGRÁFICA

| # | Variable | Nombre Completo | Descripción | Valores |
|---|----------|----------------|-------------|---------|
| 4 | **DEPREG** | **Departamento de Registro** | Dónde se registró legalmente | 1-22 |
| 12 | **MUPREG** | **Municipio de Registro** | Municipio de registro | 101-2217 |
| 3 | **DEPOCU** | **Departamento de Ocurrencia** | Dónde se celebró | 1-22 |
| 13 | **MUPOCU** | **Municipio de Ocurrencia** | Municipio donde ocurrió | 101-2217 |

### 💍 INFORMACIÓN DEL MATRIMONIO

| # | Variable | Nombre Completo | Descripción | Valores |
|---|----------|----------------|-------------|---------|
| 2 | **CLAUNI** | **Clase de Unión** | Tipo de matrimonio | 1,2,3,9 |

### 👥 DATOS DE LOS CONTRAYENTES

#### Hombre:
| # | Variable | Nombre Completo | Descripción | Rango |
|---|----------|----------------|-------------|-------|
| 6 | **EDADHOM** | **Edad del Hombre** | Edad en años | 18-98 |
| 8 | **ESCHOM** | **Escolaridad del Hombre** | Nivel educativo | 1-6, 9 |
| 14 | **NACHOM** | **Nacionalidad del Hombre** | Código de país | 320=GT |

#### Mujer:
| # | Variable | Nombre Completo | Descripción | Rango |
|---|----------|----------------|-------------|-------|
| 7 | **EDADMUJ** | **Edad de la Mujer** | Edad en años | 18-90+ |
| 9 | **ESCMUJ** | **Escolaridad de la Mujer** | Nivel educativo | 1-6, 9 |
| 15 | **NACMUJ** | **Nacionalidad de la Mujer** | Código de país | 320=GT |

---

## ❌ VARIABLES EXCLUIDAS (no aparecían en todos los años)

Estas variables **NO están** en el dataset consolidado porque no eran consistentes:

### Variables ausentes:
- ❌ **NUNUHO** - Número de Unión del Hombre
- ❌ **NUNUMU** - Número de Unión de la Mujer
- ❌ **PUEHOM** - Pueblo/Etnia del Hombre
- ❌ **PUEMUJ** - Pueblo/Etnia de la Mujer
- ❌ **CIUOHOM** - Ciudad/Ocupación del Hombre
- ❌ **CIUOMUJ** - Ciudad/Ocupación de la Mujer
- ❌ **AÑOOCU** - Año de Ocurrencia (solo mes y día)

**Impacto:** Perdiste información sobre:
- 🚫 Composición étnica (indígena/ladino/garífuna)
- 🚫 Si es primera unión o subsecuente
- 🚫 Ocupación de los contrayentes
- 🚫 Año exacto de la ceremonia (solo mes/día)

---

## 🔍 CATÁLOGO DE CÓDIGOS

### 💍 CLASE DE UNIÓN (CLAUNI)

| Código | Tipo de Matrimonio | Significado |
|--------|-------------------|-------------|
| **1** | Matrimonio Civil | Solo registro civil |
| **2** | Matrimonio Religioso | Solo ceremonia religiosa (con efecto civil) |
| **3** | Matrimonio Mixto | Civil + Religioso (más común ~92%) |
| **9** | No especificado | Sin información |

### 📚 ESCOLARIDAD (ESCHOM / ESCMUJ)

| Código | Nivel Educativo | Descripción |
|--------|----------------|-------------|
| **1** | Ninguno | Sin escolaridad |
| **2** | Primaria | Primaria completa |
| **3** | Secundaria | Básicos (3 años) |
| **4** | Diversificado | Bachillerato/Carrera técnica |
| **5** | Universidad | Licenciatura |
| **6** | Posgrado | Maestría/Doctorado |
| **9** | No especificado | Sin información |

### 🌍 NACIONALIDAD (NACHOM / NACMUJ)

Códigos ISO de países:

| Código | País |
|--------|------|
| **320** | Guatemala (99%+ de los casos) |
| **840** | Estados Unidos |
| **222** | El Salvador |
| **484** | México |
| **340** | Honduras |
| **124** | Canadá |
| Otros | Múltiples países |

### 🗺️ DEPARTAMENTOS DE GUATEMALA (DEPREG / DEPOCU)

Los 22 departamentos codificados 1-22:

| Código | Departamento |
|--------|--------------|
| 1 | Guatemala |
| 2 | El Progreso |
| 3 | Sacatepéquez |
| 4 | Chimaltenango |
| 5 | Escuintla |
| 6 | Santa Rosa |
| 7 | Sololá |
| 8 | Totonicapán |
| 9 | Quetzaltenango |
| 10 | Suchitepéquez |
| 11 | Retalhuleu |
| 12 | San Marcos |
| 13 | Huehuetenango |
| 14 | Quiché |
| 15 | Baja Verapaz |
| 16 | Alta Verapaz |
| 17 | Petén |
| 18 | Izabal |
| 19 | Zacapa |
| 20 | Chiquimula |
| 21 | Jalapa |
| 22 | Jutiapa |

---

## 📊 ESTRUCTURA DE LOS DATOS

### Ejemplo de registro típico:

```
AÑOREG:  2011        → Se registró en 2011
MESREG:  12          → Registrado en diciembre
CLAUNI:  3           → Matrimonio mixto (civil+religioso)
DEPREG:  1           → Registrado en Guatemala
MUPREG:  101         → Municipio 101 (Guatemala capital)
DEPOCU:  1           → Celebrado en Guatemala
MUPOCU:  101         → En el municipio 101
DIAOCU:  20          → Día 20
MESOCU:  9           → Septiembre
EDADHOM: 27          → Él tiene 27 años
EDADMUJ: 32          → Ella tiene 32 años
ESCHOM:  9           → Escolaridad de él: no especificada
ESCMUJ:  5           → Escolaridad de ella: Universidad
NACHOM:  124         → Él es canadiense
NACMUJ:  320         → Ella es guatemalteca
```

---

## 🎯 ANÁLISIS QUE PUEDES HACER

### Con las 15 variables disponibles puedes analizar:

#### ✅ Análisis Temporal
- Tendencias de matrimonios por año
- Estacionalidad (meses más populares)
- Días más populares
- Tiempo entre ocurrencia y registro
- Evolución histórica

#### ✅ Análisis Demográfico
- Distribución de edades por sexo
- Diferencia de edad entre contrayentes
- Edad promedio por año
- Edad al matrimonio por departamento
- Tendencias de edad a lo largo del tiempo

#### ✅ Análisis Geográfico
- Distribución por departamento
- Distribución por municipio
- Migración (diferencia entre DEPOCU y DEPREG)
- Mapas de calor de matrimonios
- Análisis urbano vs rural

#### ✅ Análisis Educativo
- Nivel educativo por sexo
- Evolución educativa en el tiempo
- Homogamia educativa (parejas del mismo nivel)
- Educación por departamento
- Brecha educativa de género

#### ✅ Análisis de Tipo de Unión
- Preferencia civil vs religioso vs mixto
- Cambios en tipo de unión por año
- Tipo de unión por departamento
- Correlación con edad/educación

#### ✅ Análisis de Nacionalidad
- Matrimonios mixtos (guatemalteco-extranjero)
- Nacionalidades más comunes
- Tendencias migratorias
- Distribución geográfica de extranjeros

#### ❌ Análisis que NO puedes hacer (variables ausentes)
- Composición étnica
- Primera vs segunda unión
- Análisis ocupacional
- Año exacto de ocurrencia (solo tienes mes/día)

---

## 💡 CONSIDERACIONES IMPORTANTES

### Calidad de Datos:
- ✅ **15 variables consistentes** en todos los años
- ✅ **Estandarización completa** - mismos códigos en todo el periodo
- ⚠️ Código **9** = "No especificado" en variables categóricas
- ⚠️ Código **999** = "Sin información" en edades
- ⚠️ **Año de ocurrencia faltante** - solo puedes usar mes/día

### Limitaciones:
1. **Sin información étnica** - No puedes analizar composición indígena/ladino
2. **Sin número de unión** - No sabes si es primera vez o reincidente
3. **Sin ocupación** - No hay análisis socioeconómico directo
4. **Sin año de ocurrencia completo** - Solo mes/día, no año

### Fortalezas:
1. ✅ **Muestra muy grande** - 750,000 registros = alta confiabilidad estadística
2. ✅ **Multi-año** - Permite análisis de tendencias temporales
3. ✅ **Cobertura nacional** - Todos los departamentos
4. ✅ **Datos limpios** - Variables estandarizadas

---

## 📈 PREGUNTAS DE INVESTIGACIÓN POSIBLES

### Demografía:
1. ¿Cuál es la edad promedio al matrimonio y cómo ha cambiado?
2. ¿Cuál es la diferencia de edad típica entre cónyuges?
3. ¿Ha aumentado la edad al matrimonio en los últimos años?

### Educación:
4. ¿Cuál es el nivel educativo más común en matrimonios?
5. ¿Las parejas tienden a casarse con el mismo nivel educativo?
6. ¿Ha mejorado el nivel educativo de los contrayentes?
7. ¿Hay brecha educativa de género?

### Geografía:
8. ¿Qué departamentos tienen más matrimonios?
9. ¿Cuántos matrimonios se celebran en un departamento diferente al de registro?
10. ¿Hay migración campo-ciudad para registrar matrimonios?

### Temporal:
11. ¿En qué mes se casan más guatemaltecos?
12. ¿Ha aumentado o disminuido el número de matrimonios?
13. ¿Cuánto tiempo pasa entre la ceremonia y el registro?

### Tipo de Unión:
14. ¿Qué porcentaje son matrimonios religiosos vs civiles?
15. ¿Ha cambiado la preferencia de tipo de unión?

### Migración:
16. ¿Cuántos matrimonios son entre guatemalteco y extranjero?
17. ¿De qué países vienen los extranjeros que se casan en Guatemala?
18. ¿En qué departamentos hay más matrimonios con extranjeros?

---

## 🔧 RECOMENDACIONES PARA ANÁLISIS

### 1. Limpieza inicial:
```python
# Filtrar valores especiales
df_clean = df[
    (df['EDADHOM'] < 100) &  # Eliminar 999
    (df['EDADMUJ'] < 100) &  # Eliminar 999
    (df['ESCHOM'] != 9) &    # Opcional: eliminar "no especificado"
    (df['ESCMUJ'] != 9)
]
```

### 2. Variables derivadas útiles:
```python
# Diferencia de edad
df['DIFEDAD'] = df['EDADHOM'] - df['EDADMUJ']

# Edad promedio de la pareja
df['EDADPROM'] = (df['EDADHOM'] + df['EDADMUJ']) / 2

# Mismo departamento (celebración y registro)
df['MISMODEP'] = (df['DEPOCU'] == df['DEPREG']).astype(int)

# Matrimonio mixto (nacionalidad)
df['MIXTONAC'] = ((df['NACHOM'] != 320) | (df['NACMUJ'] != 320)).astype(int)

# Homogamia educativa
df['MISMAESC'] = (df['ESCHOM'] == df['ESCMUJ']).astype(int)

# Tiempo entre ocurrencia y registro (meses)
df['TIEMPOREG'] = df['MESREG'] - df['MESOCU']
```

### 3. Visualizaciones recomendadas:
- 📊 Serie temporal de matrimonios por año
- 🗺️ Mapa de calor por departamento
- 📈 Pirámide de edades
- 📊 Distribución de educación por sexo
- 📅 Calendario de meses populares
- 🌍 Nacionalidades extranjeras (top 10)

---

## 📌 RESUMEN DE VARIABLES

**Total: 15 variables**

**Temporales (3):** AÑOREG, MESREG, MESOCU, DIAOCU  
**Geográficas (4):** DEPREG, MUPREG, DEPOCU, MUPOCU  
**Tipo matrimonio (1):** CLAUNI  
**Hombre (3):** EDADHOM, ESCHOM, NACHOM  
**Mujer (3):** EDADMUJ, ESCMUJ, NACMUJ  

---

*Dataset consolidado multi-año de ~750,000 matrimonios en Guatemala*  
*Variables estandarizadas para análisis comparativo temporal*
