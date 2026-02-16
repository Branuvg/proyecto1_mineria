# Descripción de Variables - Dataset de Matrimonios en Guatemala
**Período:** 2011-2021
**Total de registros:** 752264
**Total de variables:** 15

## Descripción Detallada de las 15 Variables

### 1. AÑOREG - Año de Registro

**Descripción:** Año en que se registró formalmente el matrimonio ante el Registro Civil.

**Tipo de variable:** Numérica (año calendario)

**Valores posibles:**
- 2011: 8,660 registros (86.6%)
- 2012: 1,339 registros (13.4%)

**Interpretación:** La mayoría de los datos corresponden a 2011. Los datos de 2012 parecen estar incompletos o representar solo una porción del año.

**Uso en análisis:** Variable temporal para análisis de tendencias entre años.

---

### 2. CLAUNI - Clase de Unión (Régimen Patrimonial)

**Descripción:** Tipo de régimen patrimonial o económico que rige el matrimonio, es decir, cómo se administrarán los bienes durante el matrimonio.

**Tipo de variable:** Categórica nominal

**Categorías:**
1. **Comunidad de gananciales** - 8,195 casos (82.0%)
   - Los bienes adquiridos durante el matrimonio pertenecen a ambos cónyuges por igual
   - Los bienes anteriores al matrimonio permanecen como propiedad individual

2. **Comunidad absoluta** - 731 casos (7.3%)
   - Todos los bienes, tanto anteriores como posteriores al matrimonio, se comparten
   - Régimen más integrador

3. **Separación absoluta** - 402 casos (4.0%)
   - Cada cónyuge mantiene la propiedad individual de sus bienes
   - No hay bienes compartidos durante el matrimonio

4. **No especificado** - 671 casos (6.7%)
   - No se declaró el régimen patrimonial o no quedó registrado


**Uso en análisis:** Estudiar preferencias sociales, analizar relación con edad, educación o nacionalidad.

---

### 3. DEPOCU - Departamento de Ocurrencia

**Descripción:** Departamento (división administrativa de primer nivel en Guatemala) donde ocurrió el matrimonio, es decir, donde se celebró la ceremonia o unión.

**Tipo de variable:** Categórica geográfica

**Valores:** 22 departamentos de Guatemala

**Uso en análisis:** Análisis geográfico, mapas de calor, patrones regionales, comparación urbano-rural.

---

### 4. DEPREG - Departamento de Registro

**Descripción:** Departamento donde se registró formalmente el matrimonio ante el Registro Civil. Puede ser diferente del departamento de ocurrencia si la pareja viajó a otra región para el registro.

**Tipo de variable:** Categórica geográfica

**Valores:** 22 departamentos de Guatemala

**Uso en análisis:** Análisis de movilidad, comparación con DEPOCU para entender patrones de registro.

---

### 5. DIAOCU - Día de Ocurrencia

**Descripción:** Día del mes (1-31) en que se celebró el matrimonio.

**Tipo de variable:** Numérica discreta

**Rango:** 1 a 31

**Uso en análisis:** Identificar días populares para bodas, patrones de estacionalidad dentro del mes, preferencias por fechas específicas.

---

### 6. EDADHOM - Edad del Hombre

**Descripción:** Edad en años cumplidos del contrayente masculino al momento del matrimonio.

**Tipo de variable:** Numérica continua

**Estadísticas:**
- **Mínimo:** 15 años
- **Máximo:** 90 años
- **Media:** 27.8 años
- **Mediana:** 26 años
- **Desviación estándar:** 7.48 años

**Distribución:**
- 18-24 años: 37.5%
- 25-34 años: 49.1%
- 35-44 años: 9.2%
- 45+ años: 3.7%

**Uso en análisis:** Estudios demográficos, análisis de diferencias de edad con la pareja, correlación con educación y otros factores.

---

### 7. EDADMUJ - Edad de la Mujer

**Descripción:** Edad en años cumplidos de la contrayente femenina al momento del matrimonio.

**Tipo de variable:** Numérica continua

**Estadísticas:**
- **Mínimo:** 16 años
- **Máximo:** 73 años
- **Media:** 26.0 años
- **Mediana:** 25 años
- **Desviación estándar:** 6.21 años

**Distribución:**
- 18-24 años: 49.2%
- 25-34 años: 42.3%
- 35-44 años: 6.0%
- 45+ años: 2.1%

**Uso en análisis:** Comparación con edad del hombre, análisis de diferencias generacionales, correlación con variables educativas y sociales.

---

### 8. ESCHOM - Escolaridad del Hombre

**Descripción:** Nivel educativo más alto alcanzado por el contrayente masculino al momento del matrimonio.

**Tipo de variable:** Categórica ordinal (tiene orden jerárquico)

**Categorías (de menor a mayor nivel):**

1. **Ninguno** - 1,594 casos (15.9%)
   - Sin educación formal

2. **Primaria** - 1,112 casos (11.1%)
   - Educación primaria (grados 1-6)

3. **Básico** - 1,000 casos (10.0%)
   - Educación secundaria básica (grados 7-9)

4. **Diversificado** - 4,190 casos (41.9%)
   - Educación media superior/bachillerato (grados 10-12 aproximadamente)
   - **Nivel más común**

5. **Universitario** - 1,006 casos (10.1%)
   - Educación superior universitaria

6. **Ignorado** - 1,097 casos (11.0%)
   - Nivel educativo desconocido o no registrado

**Uso en análisis:** Estudios de equidad educativa, correlación con edad y tipo de unión, análisis de brechas de género.

---

### 9. ESCMUJ - Escolaridad de la Mujer

**Descripción:** Nivel educativo más alto alcanzado por la contrayente femenina al momento del matrimonio.

**Tipo de variable:** Categórica ordinal

**Categorías (de menor a mayor nivel):**

1. **Ninguno** - 1,133 casos (11.3%)
   - Sin educación formal

2. **Primaria** - 122 casos (1.2%)
   - Educación primaria (grados 1-6)

3. **Básico** - 336 casos (3.4%)
   - Educación secundaria básica (grados 7-9)

4. **Diversificado** - 6,822 casos (68.2%)
   - Educación media superior/bachillerato
   - **Nivel dominante con amplia mayoría**

5. **Universitario** - 1,013 casos (10.1%)
   - Educación superior universitaria

6. **Ignorado** - 573 casos (5.7%)
   - Nivel educativo desconocido o no registrado

**Uso en análisis:** Análisis de brecha de género educativa, emparejamiento educativo (homogamia), cambios generacionales.

---

### 10. MESOCU - Mes de Ocurrencia

**Descripción:** Mes del año en que se celebró el matrimonio.

**Tipo de variable:** Categórica temporal

**Valores:** 12 meses del año

**Uso en análisis:** Análisis de estacionalidad, patrones culturales, planificación de recursos para el Registro Civil.

---

### 11. MESREG - Mes de Registro

**Descripción:** Mes del año en que se registró formalmente el matrimonio ante el Registro Civil.

**Tipo de variable:** Categórica temporal

**Valores:** 12 meses del año

**Uso en análisis:** Estudiar tiempo entre ocurrencia y registro, eficiencia administrativa, patrones de formalización.

---

### 12. MUPOCU - Municipio de Ocurrencia

**Descripción:** Municipio (división administrativa de segundo nivel) donde se celebró el matrimonio.

**Tipo de variable:** Categórica geográfica

**Valores únicos:** 322 municipios diferentes de los 340 municipios de Guatemala

**Uso en análisis:** Análisis detallado a nivel municipal, mapeo geográfico fino, identificar destinos populares para ceremonias.

---

### 13. MUPREG - Municipio de Registro

**Descripción:** Municipio donde se registró formalmente el matrimonio ante las oficinas del Registro Civil.

**Tipo de variable:** Categórica geográfica

**Valores únicos:** 323 municipios diferentes

**Uso en análisis:** Accesibilidad a servicios de registro, patrones de movilidad administrativa.

---

### 14. NACHOM - Nacionalidad del Hombre

**Descripción:** País de nacionalidad legal del contrayente masculino.

**Tipo de variable:** Categórica nominal

**Valores únicos:** 38 nacionalidades diferentes

**Uso en análisis:** Matrimonios internacionales, migración, vínculos transnacionales, análisis de comunidades binacionales.

---

### 15. NACMUJ - Nacionalidad de la Mujer

**Descripción:** País de nacionalidad legal de la contrayente femenina.

**Tipo de variable:** Categórica nominal

**Valores únicos:** 32 nacionalidades diferentes

**Distribución:**
- **Guatemala:** 9,816 casos (98.17%)
- **Extranjeras:** 183 casos (1.83%)

**Top 5 nacionalidades extranjeras:**
| Nacionalidad | Frecuencia |
|--------------|------------|
| Estados Unidos de América | 51 |
| México | 20 |
| Honduras | 18 |
| Nicaragua | 16 |
| El Salvador | 16 |

**Interpretación:** 
- Similar al patrón masculino, pero ligeramente más mujeres extranjeras (1.83% vs 1.64%)
- Estados Unidos nuevamente lidera
- Mayor presencia de países centroamericanos (Honduras, Nicaragua)
- Sugiere ligera preferencia por matrimonios donde el hombre es guatemalteco y la mujer extranjera

**Matrimonios internacionales:** 328 matrimonios (3.28%) tienen al menos un cónyuge extranjero.

**Uso en análisis:** Patrones de migración femenina, matrimonios binacionales, integración regional centroamericana.

---

## Relaciones Entre Variables

### Variables Temporales
- **AÑOREG, MESOCU, MESREG, DIAOCU:** Permiten análisis temporal completo (año, mes, día)
- **MESOCU vs MESREG:** Diferencia entre fecha de ceremonia y fecha de registro

### Variables Geográficas
- **DEPOCU, DEPREG:** Análisis a nivel departamental
- **MUPOCU, MUPREG:** Análisis detallado a nivel municipal
- **DEPOCU vs DEPREG:** Movilidad entre ocurrencia y registro

### Variables Demográficas
- **EDADHOM, EDADMUJ:** Permiten calcular diferencia de edad entre cónyuges
- **NACHOM, NACMUJ:** Identifican matrimonios nacionales vs internacionales

### Variables Sociales
- **ESCHOM, ESCMUJ:** Permiten análisis de homogamia educativa (parejas con mismo nivel)
- **CLAUNI:** Preferencias de régimen patrimonial

### 💡 Variables Clave para Análisis Común

**Para análisis demográfico:**
- EDADHOM, EDADMUJ (calcular diferencia de edad)

**Para análisis educativo:**
- ESCHOM, ESCMUJ (brecha de género)

**Para análisis temporal:**
- MESOCU (estacionalidad)
- AÑOREG (tendencias anuales)

**Para análisis geográfico:**
- DEPOCU, DEPREG (concentración regional)
- MUPOCU, MUPREG (urbanización)

**Para análisis social:**
- CLAUNI (preferencias legales)
- NACHOM, NACMUJ (internacionalización)

---

## Preguntas que Puedes Responder con este Dataset

1. ¿Cuál es la edad promedio de matrimonio en Guatemala?
2. ¿Existe diferencia de edad significativa entre hombres y mujeres?
3. ¿Qué nivel educativo tienen típicamente los contrayentes?
4. ¿Existe brecha educativa de género?
5. ¿En qué meses se casan más las personas?
6. ¿Qué departamentos/municipios tienen más matrimonios?
7. ¿Qué tipo de unión conyugal prefieren las parejas?
8. ¿Cuántos matrimonios son internacionales?
9. ¿Las parejas tienden a casarse con el mismo nivel educativo?
10. ¿Hay diferencia entre dónde ocurre el matrimonio y dónde se registra?