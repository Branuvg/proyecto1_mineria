# 📋 DICCIONARIO DE VARIABLES - REGISTRO DE MATRIMONIOS

**Base de datos:** d20.csv / d20.sav  
**Registros:** 4,074 matrimonios  
**Periodo:** 2020-2021  
**País:** Guatemala (código 320)

---

## 🗂️ VARIABLES COMPLETAS

### 📍 INFORMACIÓN DE REGISTRO (Lugar/Fecha donde se registró el matrimonio)

| Variable | Nombre Completo | Descripción | Valores |
|----------|----------------|-------------|---------|
| **DEPREG** | **Departamento de Registro** | Código del departamento donde se registró el matrimonio | 1-22 (22 departamentos) |
| **MUPREG** | **Municipio de Registro** | Código del municipio donde se registró el matrimonio | 101-2217 (271 municipios) |
| **MESREG** | **Mes de Registro** | Mes en que se registró el matrimonio | 1-12 |
| **AÑOREG** | **Año de Registro** | Año en que se registró el matrimonio | 2020-2021 |

### 📅 INFORMACIÓN DE OCURRENCIA (Lugar/Fecha donde ocurrió el matrimonio)

| Variable | Nombre Completo | Descripción | Valores |
|----------|----------------|-------------|---------|
| **DIAOCU** | **Día de Ocurrencia** | Día en que se celebró el matrimonio | 1-31 |
| **MESOCU** | **Mes de Ocurrencia** | Mes en que se celebró el matrimonio | 1-12 |
| **AÑOOCU** | **Año de Ocurrencia** | Año en que se celebró el matrimonio | 2020 |
| **DEPOCU** | **Departamento de Ocurrencia** | Código del departamento donde se celebró el matrimonio | 1-22 (22 departamentos) |
| **MUPOCU** | **Municipio de Ocurrencia** | Código del municipio donde se celebró el matrimonio | 101-2217 (302 municipios) |

### 👨 INFORMACIÓN DEL HOMBRE (Contrayente masculino)

| Variable | Nombre Completo | Descripción | Valores |
|----------|----------------|-------------|---------|
| **EDADHOM** | **Edad del Hombre** | Edad en años del contrayente masculino | 19-78 años* |
| **PPERHOM** | **Pueblo de Pertenencia del Hombre** | Grupo étnico o pueblo al que pertenece | Códigos: 1,2,4,5,9 |
| **NACHOM** | **Nacionalidad del Hombre** | Código de país de nacionalidad | 320=Guatemala, 840=USA, etc. |
| **ESCHOM** | **Escolaridad del Hombre** | Nivel educativo alcanzado | Códigos: 1-6, 9 |
| **CIUOHOM** | **Ciudad/Ocupación del Hombre** | Código de ocupación o residencia | 1-99 |

### 👩 INFORMACIÓN DE LA MUJER (Contrayente femenina)

| Variable | Nombre Completo | Descripción | Valores |
|----------|----------------|-------------|---------|
| **EDADMUJ** | **Edad de la Mujer** | Edad en años de la contrayente femenina | 19-70 años* |
| **PPERMUJ** | **Pueblo de Pertenencia de la Mujer** | Grupo étnico o pueblo al que pertenece | Códigos: 1,4,5,9 |
| **NACMUJ** | **Nacionalidad de la Mujer** | Código de país de nacionalidad | 320=Guatemala, 840=USA, etc. |
| **ESCMUJ** | **Escolaridad de la Mujer** | Nivel educativo alcanzado | Códigos: 1-6, 9 |
| **CIUOMUJ** | **Ciudad/Ocupación de la Mujer** | Código de ocupación o residencia | 3-99 |

*Nota: El valor 999 probablemente significa "No especificado" o "Sin información"

---

## 🔍 CÓDIGOS Y CATÁLOGOS

### Departamentos de Guatemala (DEPREG, DEPOCU)
Los 22 departamentos están codificados del 1 al 22. Los más frecuentes en la base:
- **1** = Probablemente Guatemala (1,412 registros)
- **9** = Probablemente Quetzaltenango (442 registros)
- **12** = (178 registros)
- **6** = (160 registros)

### Nacionalidad (NACHOM, NACMUJ)
Códigos de país según estándar internacional:
- **320** = Guatemala (98.5% de los casos)
- **840** = Estados Unidos
- **222** = El Salvador
- **484** = México
- **340** = Honduras
- **9999** = Probablemente "Desconocido" o "Sin especificar"

### Pueblo de Pertenencia (PPERHOM, PPERMUJ)
Probablemente códigos de grupos étnicos de Guatemala:
- **1** = Posiblemente Indígena Maya (~374 hombres, ~354 mujeres)
- **2** = (solo 1 caso)
- **4** = Posiblemente Ladino/No indígena (~1,924 hombres, ~1,944 mujeres)
- **5** = Posiblemente Garífuna (~44 hombres, ~47 mujeres)
- **9** = Probablemente "No especificado" (~1,731 hombres, ~1,729 mujeres)

### Escolaridad (ESCHOM, ESCMUJ)
Niveles educativos (probablemente):
- **1** = Ninguno / Primaria incompleta
- **2** = Primaria completa
- **3** = Secundaria/Básicos incompletos
- **4** = Secundaria/Básicos completos
- **5** = Diversificado incompleto
- **6** = Diversificado completo
- **9** = No especificado / Sin información

### Ciudad/Ocupación (CIUOHOM, CIUOMUJ)
Códigos de 1-99, posiblemente clasificación de:
- Ocupaciones
- Códigos de municipios de residencia
- Categorías mixtas

**Valores más comunes:**
- **97** = Muy frecuente en mujeres
- **92** = Frecuente en hombres
- **99** = Posiblemente "No especificado"

---

## 📊 ESTADÍSTICAS GENERALES

### Distribución Temporal
- **Año de ocurrencia:** Todos en 2020
- **Año de registro:** 2,788 en 2020 + 1,286 en 2021
- Esto indica que algunos matrimonios de 2020 se registraron en 2021

### Edades
- **Edad promedio hombres:** ~30 años (excluyendo 999)
- **Edad promedio mujeres:** ~27 años (excluyendo 999)
- **Edad mínima legal:** 19 años (ambos)

### Nacionalidad
- **98.5%** de guatemaltecos
- **1.5%** extranjeros (principalmente estadounidenses, salvadoreños, mexicanos)

### Educación
- **Nivel más común:** Sin especificar (código 9) - ~36%
- **Segundo más común:** Básicos completos (código 4) - ~24%

---

## ⚠️ NOTAS IMPORTANTES

1. **Código 999:** En edades significa "Sin información" o "No especificado"
2. **Código 9999:** En nacionalidad significa "Sin información"
3. **Código 9:** En varios campos significa "No especificado"
4. **Diferencia entre REGISTRO y OCURRENCIA:** 
   - OCURRENCIA = Cuándo y dónde se celebró el matrimonio
   - REGISTRO = Cuándo y dónde se inscribió legalmente en el registro civil

---

## 🎯 TIPO DE DATOS

**Este es un registro de MATRIMONIOS CIVILES de Guatemala**

Características que lo confirman:
✅ Datos de dos personas (hombre y mujer)  
✅ Fecha de celebración (ocurrencia)  
✅ Fecha de inscripción (registro)  
✅ Información sociodemográfica de ambos contrayentes  
✅ Periodo: año 2020  
✅ Estructura típica de registros civiles  

---

*Documento generado el 09 de febrero de 2026*  
*Fuente: Análisis de d20.csv (4,074 registros)*
