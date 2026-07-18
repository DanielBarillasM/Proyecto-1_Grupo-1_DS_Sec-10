# Libro de códigos — Establecimientos educativos MINEDUC

**Proyecto 1 · CC3084 Data Science · Semestre II 2026 · Versión 2.0.0**

## Descripción general

El conjunto contiene 11,603 códigos de servicio educativo autorizado del nivel Diversificado y 59 variables. La llave es `CODIGO`. Los campos `*_ORIGINAL` preservan la fuente, los campos `*_LIMPIO`/`*_LIMPIA` son de presentación analítica y los campos `*_COD` son códigos nominales salvo cuando se indique que son territoriales.

## Metadatos

| Campo | Valor |
|---|---|
| TITULO | Establecimientos educativos de Guatemala con nivel Diversificado |
| UNIDAD_OBSERVACION | Código de servicio educativo autorizado |
| FUENTE | MINEDUC - Búsqueda de centros educativos autorizados |
| FUENTE_URL | http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/ |
| FECHA_EXTRACCION | 2026-07-10 |
| NOTA_FECHA_EXTRACCION | Fecha del archivo crudo preservado; la hora exacta no estaba incorporada en el CSV. |
| FECHA_PROCESAMIENTO | 2026-07-17 |
| VERSION | 2.0.0 |
| FILAS_CRUDAS | 11603 |
| VARIABLES_CRUDAS | 17 |
| FILAS_LIMPIAS | 11603 |
| VARIABLES_LIMPIAS | 59 |
| SHA256_CRUDO | e7b9f1056e17fdf7eb994b8dc584f22671cdd3e78c388c85b2f547a2bae033af |
| COBERTURA_TERRITORIAL | 23 orígenes MINEDUC; 22 departamentos analíticos; 334 códigos municipales observados; 22 zonas capitalinas. |
| REFERENCIA_TERRITORIAL | https://datos.segeplan.gob.gt/es/dataset/calculo-matematico-para-la-asignacion-constitucional-a-las-municipalidades-2026 |

## Diccionario de variables

| Variable | Descripción | Tipo / null | Dominio y valores | Tratamiento / derivación | Fuente, fecha y versión |
|---|---|---|---|---|---|
| `CODIGO` | Identificador textual único del servicio educativo autorizado. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (11,603 valores observados) | Derivación documentada y validada automáticamente. Derivada: No (campo preservado); origen: CODIGO; método: Conservación textual; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DISTRITO_ORIGINAL` | Valor original: Código de distrito o supervisión educativa publicado por la fuente. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (1,667 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: DISTRITO; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DISTRITO_LIMPIO` | Distrito completo; null cuando la fuente está vacía o incompleta. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (1,663 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: DISTRITO; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DISTRITO_ESTADO` | Clasificación de completitud del distrito: Válido, Vacío o Incompleto. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Válido; Vacío; Incompleto | Clasificación derivada para distinguir valor válido, ausencia o formato no estándar. Derivada: Sí; origen: DISTRITO; método: Clasificación derivada para distinguir valor válido, ausencia o formato no estándar.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DEPARTAMENTO_ORIGINAL` | Valor original: Categoría territorial de origen utilizada por el portal. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: ALTA VERAPAZ; BAJA VERAPAZ; CHIMALTENANGO; CHIQUIMULA; CIUDAD CAPITAL; EL PROGRESO; ESCUINTLA; GUATEMALA; HUEHUETENANGO; IZABAL; JALAPA; JUTIAPA; PETEN; QUETZALTENANGO; QUICHE; RETALHULEU; SACATEPEQUEZ; SAN MARCOS; SANTA ROSA; SOLOLA; SUCHITEPEQUEZ; TOTONICAPAN; ZACAPA | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: DEPARTAMENTO; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DEPARTAMENTO_LIMPIO` | Categoría de origen con presentación ortográfica. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Alta Verapaz; Baja Verapaz; Chimaltenango; Chiquimula; Ciudad Capital; El Progreso; Escuintla; Guatemala; Huehuetenango; Izabal; Jalapa; Jutiapa; Petén; Quetzaltenango; Quiché; Retalhuleu; Sacatepéquez; San Marcos; Santa Rosa; Sololá; Suchitepéquez; Totonicapán; Zacapa | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: DEPARTAMENTO; MUNICIPIO; CODIGO; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DEPARTAMENTO_ANALISIS` | Departamento analítico de 22 categorías; Ciudad Capital se agrega a Guatemala. | string; null: No | 22 departamentos de Guatemala.. Valores: Alta Verapaz; Baja Verapaz; Chimaltenango; Chiquimula; Guatemala; El Progreso; Escuintla; Huehuetenango; Izabal; Jalapa; Jutiapa; Petén; Quetzaltenango; Quiché; Retalhuleu; Sacatepéquez; San Marcos; Santa Rosa; Sololá; Suchitepéquez; Totonicapán; Zacapa | Derivación documentada y validada automáticamente. Derivada: Sí; origen: DEPARTAMENTO; MUNICIPIO; CODIGO; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DEPARTAMENTO_ANALISIS_COD` | Código territorial de dos dígitos del departamento analítico. | string; null: No | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 16; 15; 04; 20; 01; 02; 05; 13; 18; 21; 22; 17; 09; 14; 11; 03; 12; 06; 07; 10; 08; 19 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: DEPARTAMENTO; MUNICIPIO; CODIGO; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `MUNICIPIO_ORIGINAL` | Valor original: Municipio o zona de Ciudad Capital publicado por el portal. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (350 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: MUNICIPIO; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `MUNICIPIO_LIMPIO` | Municipio o zona con presentación normalizada. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (350 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: MUNICIPIO; CODIGO; DEPARTAMENTO; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `UBICACION_GRUPO` | Distingue Ciudad Capital de otros municipios. | string; null: No | Ciudad Capital; Otros municipios.. Valores: Otros municipios; Ciudad Capital | Derivación documentada y validada automáticamente. Derivada: Sí; origen: DEPARTAMENTO; MUNICIPIO; CODIGO; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `TIPO_UBICACION` | Indica si la etiqueta territorial es Zona capital o Municipio. | string; null: No | Zona capital; Municipio.. Valores: Municipio; Zona capital | Derivación documentada y validada automáticamente. Derivada: Sí; origen: DEPARTAMENTO; MUNICIPIO; CODIGO; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `ES_CIUDAD_CAPITAL` | Indicador binario: 1 para Ciudad Capital y 0 para otros municipios. | Int8; null: No | 0 = No; 1 = Sí.. Valores: 0; 1 | Derivación documentada y validada automáticamente. Derivada: Sí; origen: DEPARTAMENTO; MUNICIPIO; CODIGO; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `ZONA_CAPITAL_COD` | Número de zona de Ciudad Capital; null fuera de la capital. | Int8; null: Sí | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 1; 10; 11; 12; 13; 14; 15; 16; 17; 18; 19; 2; 21; 24; 25; 3; 4; 5; 6; 7; 8; 9 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: DEPARTAMENTO; MUNICIPIO; CODIGO; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `MUNICIPIO_COD_FUENTE` | Prefijo departamento-municipio del CODIGO; null para zonas capitalinas. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (334 valores observados) | Derivación documentada y validada automáticamente. Derivada: Sí; origen: MUNICIPIO; CODIGO; DEPARTAMENTO; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `ESTABLECIMIENTO_ORIGINAL` | Valor original: Nombre registrado del establecimiento educativo. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (6,170 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: ESTABLECIMIENTO; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `ESTABLECIMIENTO_LIMPIO` | Nombre de presentación con ortografía conservadora y trazable. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (4,970 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: ESTABLECIMIENTO; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `ESTABLECIMIENTO_CLAVE_COMPARACION` | Clave sin tildes ni puntuación usada solo para detectar candidatos. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (4,970 valores observados) | Derivación documentada y validada automáticamente. Derivada: Sí; origen: ESTABLECIMIENTO; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DIRECCION_ORIGINAL` | Valor original: Dirección textual publicada. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (7,260 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: DIRECCION; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DIRECCION_LIMPIA` | Dirección de presentación; null cuando no existe contenido utilizable. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (6,626 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: DIRECCION; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `TELEFONO_ORIGINAL` | Valor original: Uno o varios contactos telefónicos publicados. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (6,429 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: TELEFONO; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `TELEFONO_LIMPIO` | Texto telefónico normalizado; conserva formatos históricos no interpretables. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (6,327 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: TELEFONO; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `TELEFONO_PRINCIPAL` | Primer candidato de ocho dígitos con formato ####-####. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (6,295 valores observados) | Derivación documentada y validada automáticamente. Derivada: Sí; origen: TELEFONO; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `TELEFONO_ESTADO` | Estado de interpretación del teléfono. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Vacío; Válido único; Formato no estándar; Válidos múltiples | Clasificación derivada para distinguir valor válido, ausencia o formato no estándar. Derivada: Sí; origen: TELEFONO; método: Clasificación derivada para distinguir valor válido, ausencia o formato no estándar.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `SUPERVISOR_ORIGINAL` | Valor original: Nombre de la persona supervisora publicada. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (1,268 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: SUPERVISOR; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `SUPERVISOR_LIMPIO` | Nombre de supervisión de presentación o null. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (1,085 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: SUPERVISOR; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DIRECTOR_ORIGINAL` | Valor original: Nombre de la persona directora publicada. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (5,397 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: DIRECTOR; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DIRECTOR_LIMPIO` | Nombre de dirección de presentación o null. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (5,218 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: DIRECTOR; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DIRECTOR_ESTADO` | Informado, Vacío o Marcador. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Marcador; Informado; Vacío | Clasificación derivada para distinguir valor válido, ausencia o formato no estándar. Derivada: Sí; origen: DIRECTOR; método: Clasificación derivada para distinguir valor válido, ausencia o formato no estándar.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `NIVEL_ORIGINAL` | Valor original: Nivel educativo consultado. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: DIVERSIFICADO | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: NIVEL; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `NIVEL_LIMPIO` | Nivel Diversificado con etiqueta legible. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Diversificado | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: NIVEL; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `SECTOR_ORIGINAL` | Valor original: Sector administrativo del servicio. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: PRIVADO; OFICIAL; MUNICIPAL; COOPERATIVA | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: SECTOR; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `SECTOR_LIMPIO` | Etiqueta de sector legible. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Privado; Oficial; Municipal; Cooperativa | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: SECTOR; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `SECTOR_COD` | Código nominal del sector. | Int8; null: No | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 1; 2; 4; 3 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: SECTOR; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `STATUS_ORIGINAL` | Valor original: Estado administrativo del servicio. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: CERRADA DEFINITIVAMENTE; ABIERTA; CERRADA TEMPORALMENTE; TEMPORAL NOMBRAMIENTO; TEMPORAL TITULOS | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: STATUS; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `STATUS_LIMPIO` | Estado administrativo con etiqueta legible. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Cerrada definitivamente; Abierta; Cerrada temporalmente; Temporal por nombramiento; Temporal por títulos | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: STATUS; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `STATUS_COD` | Código nominal del estado. | Int8; null: No | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 3; 1; 2; 5; 4 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: STATUS; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `MODALIDAD_ORIGINAL` | Valor original: Modalidad lingüística. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: MONOLINGUE; BILINGUE | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: MODALIDAD; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `MODALIDAD_LIMPIA` | Modalidad con ortografía corregida. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Monolingüe; Bilingüe | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: MODALIDAD; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `MODALIDAD_COD` | Código nominal de modalidad. | Int8; null: No | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 1; 2 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: MODALIDAD; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `AREA_ORIGINAL` | Valor original: Área territorial urbana o rural. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: URBANA; RURAL; SIN ESPECIFICAR | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: AREA; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `AREA_LIMPIA` | Urbana o Rural; null para SIN ESPECIFICAR. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Urbana; Rural | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: AREA; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `AREA_COD` | Código nominal del área. | Int8; null: Sí | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 1; 2 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: AREA; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `AREA_INFORMADA` | Indicador binario de área informada. | Int8; null: No | 0 = No; 1 = Sí.. Valores: 1; 0 | Derivación documentada y validada automáticamente. Derivada: Sí; origen: AREA; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `JORNADA_ORIGINAL` | Valor original: Jornada autorizada. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: NOCTURNA; MATUTINA; VESPERTINA; DOBLE; SIN JORNADA; INTERMEDIA | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: JORNADA; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `JORNADA_LIMPIA` | Jornada real; null para SIN JORNADA. | string; null: Sí | Véase descripción y catálogo cuando corresponda.. Valores: Nocturna; Matutina; Vespertina; Doble; Intermedia | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: JORNADA; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `JORNADA_COD` | Código nominal de jornada real. | Int8; null: Sí | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 3; 1; 2; 4; 5 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: JORNADA; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `JORNADA_INFORMADA` | Indicador binario de jornada informada. | Int8; null: No | 0 = No; 1 = Sí.. Valores: 1; 0 | Derivación documentada y validada automáticamente. Derivada: Sí; origen: JORNADA; método: Derivación documentada y validada automáticamente.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `PLAN_ORIGINAL` | Valor original: Plan o modalidad temporal de atención. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: DIARIO(REGULAR); FIN DE SEMANA; A DISTANCIA; SEMIPRESENCIAL; VIRTUAL A DISTANCIA; SEMIPRESENCIAL (FIN DE SEMANA); SEMIPRESENCIAL (UN DÍA A LA SEMANA); SABATINO; SEMIPRESENCIAL (DOS DÍAS A LA SEMANA); DOMINICAL; MIXTO; INTERCALADO; IRREGULAR | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: PLAN; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `PLAN_LIMPIO` | Plan con presentación normalizada. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Diario (regular); Fin de Semana; A Distancia; Semipresencial; Virtual a Distancia; Semipresencial (Fin de Semana); Semipresencial (Un Día a la Semana); Sabatino; Semipresencial (Dos Días a la Semana); Dominical; Mixto; Intercalado; Irregular | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: PLAN; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `PLAN_COD` | Código nominal del plan. | Int8; null: No | Catálogo documentado; identificador nominal salvo código territorial.. Valores: 1; 2; 5; 6; 8; 3; 4; 9; 7; 10; 11; 13; 12 | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: PLAN; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DEPARTAMENTAL_ORIGINAL` | Valor original: Dirección departamental responsable. | string; null: No | Texto publicado por MINEDUC; se conserva sin sobrescritura.. Valores: Texto libre o catálogo amplio (26 valores observados) | Copia sin sobrescritura del campo crudo. Derivada: No (campo preservado); origen: DEPARTAMENTAL; método: Conservación textual; uso: Trazabilidad. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DEPARTAMENTAL_LIMPIO` | Dirección departamental con presentación ortográfica. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: Texto libre o catálogo amplio (26 valores observados) | Normalización y validación según el plan de la variable de origen. Derivada: Sí; origen: DEPARTAMENTAL; método: Normalización y validación según el plan de la variable de origen.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `DEPARTAMENTAL_COD` | Código nominal de dirección departamental. | Int8; null: No | Catálogo documentado; identificador nominal salvo código territorial.. Valores: Texto libre o catálogo amplio (26 valores observados) | Codificación nominal o territorial documentada en catálogo. Derivada: Sí; origen: DEPARTAMENTAL; método: Codificación nominal o territorial documentada en catálogo.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `FUENTE` | Nombre de la fuente administrativa. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: MINEDUC - Búsqueda de centros educativos autorizados | Asignación constante y versionada para trazabilidad. Derivada: Sí; origen: Metadato del proceso; método: Asignación constante y versionada para trazabilidad.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `FECHA_PROCESAMIENTO` | Fecha reproducible de esta versión final. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: 2026-07-17 | Asignación constante y versionada para trazabilidad. Derivada: Sí; origen: Metadato del proceso; método: Asignación constante y versionada para trazabilidad.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `FUENTE_URL` | URL del buscador oficial usado como fuente. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/ | Asignación constante y versionada para trazabilidad. Derivada: Sí; origen: Metadato del proceso; método: Asignación constante y versionada para trazabilidad.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `FECHA_EXTRACCION` | Fecha documentada del snapshot crudo preservado. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: 2026-07-10 | Asignación constante y versionada para trazabilidad. Derivada: Sí; origen: Metadato del proceso; método: Asignación constante y versionada para trazabilidad.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |
| `VERSION_CONJUNTO` | Versión semántica del conjunto limpio. | string; null: No | Véase descripción y catálogo cuando corresponda.. Valores: 2.0.0 | Asignación constante y versionada para trazabilidad. Derivada: Sí; origen: Metadato del proceso; método: Asignación constante y versionada para trazabilidad.; uso: Análisis, control de calidad o metadatos. | MINEDUC - Búsqueda de centros educativos autorizados; 2026-07-10; v2.0.0 |

## Catálogos de codificación

### SECTOR

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| PRIVADO | Privado | 1 | Código nominal |
| OFICIAL | Oficial | 2 | Código nominal |
| COOPERATIVA | Cooperativa | 3 | Código nominal |
| MUNICIPAL | Municipal | 4 | Código nominal |

### AREA

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| URBANA | Urbana | 1 | Código nominal |
| RURAL | Rural | 2 | Código nominal |

### STATUS

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| ABIERTA | Abierta | 1 | Código nominal |
| CERRADA TEMPORALMENTE | Cerrada temporalmente | 2 | Código nominal |
| CERRADA DEFINITIVAMENTE | Cerrada definitivamente | 3 | Código nominal |
| TEMPORAL TITULOS | Temporal por títulos | 4 | Código nominal |
| TEMPORAL NOMBRAMIENTO | Temporal por nombramiento | 5 | Código nominal |

### MODALIDAD

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| MONOLINGUE | Monolingüe | 1 | Código nominal |
| BILINGUE | Bilingüe | 2 | Código nominal |

### JORNADA

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| MATUTINA | Matutina | 1 | Código nominal |
| VESPERTINA | Vespertina | 2 | Código nominal |
| NOCTURNA | Nocturna | 3 | Código nominal |
| DOBLE | Doble | 4 | Código nominal |
| INTERMEDIA | Intermedia | 5 | Código nominal |

### PLAN

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| DIARIO(REGULAR) | Diario (regular) | 1 | Código nominal |
| FIN DE SEMANA | Fin de Semana | 2 | Código nominal |
| SEMIPRESENCIAL (FIN DE SEMANA) | Semipresencial (Fin de Semana) | 3 | Código nominal |
| SEMIPRESENCIAL (UN DÍA A LA SEMANA) | Semipresencial (Un Día a la Semana) | 4 | Código nominal |
| A DISTANCIA | A Distancia | 5 | Código nominal |
| SEMIPRESENCIAL | Semipresencial | 6 | Código nominal |
| SEMIPRESENCIAL (DOS DÍAS A LA SEMANA) | Semipresencial (Dos Días a la Semana) | 7 | Código nominal |
| VIRTUAL A DISTANCIA | Virtual a Distancia | 8 | Código nominal |
| SABATINO | Sabatino | 9 | Código nominal |
| DOMINICAL | Dominical | 10 | Código nominal |
| MIXTO | Mixto | 11 | Código nominal |
| IRREGULAR | Irregular | 12 | Código nominal |
| INTERCALADO | Intercalado | 13 | Código nominal |

### DEPARTAMENTO_ANALISIS

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| Guatemala | Guatemala | 1 | Código territorial |
| El Progreso | El Progreso | 2 | Código territorial |
| Sacatepéquez | Sacatepéquez | 3 | Código territorial |
| Chimaltenango | Chimaltenango | 4 | Código territorial |
| Escuintla | Escuintla | 5 | Código territorial |
| Santa Rosa | Santa Rosa | 6 | Código territorial |
| Sololá | Sololá | 7 | Código territorial |
| Totonicapán | Totonicapán | 8 | Código territorial |
| Quetzaltenango | Quetzaltenango | 9 | Código territorial |
| Suchitepéquez | Suchitepéquez | 10 | Código territorial |
| Retalhuleu | Retalhuleu | 11 | Código territorial |
| San Marcos | San Marcos | 12 | Código territorial |
| Huehuetenango | Huehuetenango | 13 | Código territorial |
| Quiché | Quiché | 14 | Código territorial |
| Baja Verapaz | Baja Verapaz | 15 | Código territorial |
| Alta Verapaz | Alta Verapaz | 16 | Código territorial |
| Petén | Petén | 17 | Código territorial |
| Izabal | Izabal | 18 | Código territorial |
| Zacapa | Zacapa | 19 | Código territorial |
| Chiquimula | Chiquimula | 20 | Código territorial |
| Jalapa | Jalapa | 21 | Código territorial |
| Jutiapa | Jutiapa | 22 | Código territorial |

### DEPARTAMENTAL

| Valor original | Etiqueta limpia | Código | Tipo |
|---|---|---:|---|
| ALTA VERAPAZ | Alta Verapaz | 1 | Código nominal |
| BAJA VERAPAZ | Baja Verapaz | 2 | Código nominal |
| CHIMALTENANGO | Chimaltenango | 3 | Código nominal |
| CHIQUIMULA | Chiquimula | 4 | Código nominal |
| EL PROGRESO | El Progreso | 5 | Código nominal |
| ESCUINTLA | Escuintla | 6 | Código nominal |
| GUATEMALA NORTE | Guatemala Norte | 7 | Código nominal |
| GUATEMALA OCCIDENTE | Guatemala Occidente | 8 | Código nominal |
| GUATEMALA ORIENTE | Guatemala Oriente | 9 | Código nominal |
| GUATEMALA SUR | Guatemala Sur | 10 | Código nominal |
| HUEHUETENANGO | Huehuetenango | 11 | Código nominal |
| IZABAL | Izabal | 12 | Código nominal |
| JALAPA | Jalapa | 13 | Código nominal |
| JUTIAPA | Jutiapa | 14 | Código nominal |
| PETÉN | Petén | 15 | Código nominal |
| QUETZALTENANGO | Quetzaltenango | 16 | Código nominal |
| QUICHÉ | Quiché | 17 | Código nominal |
| QUICHÉ NORTE | Quiché Norte | 18 | Código nominal |
| RETALHULEU | Retalhuleu | 19 | Código nominal |
| SACATEPÉQUEZ | Sacatepéquez | 20 | Código nominal |
| SAN MARCOS | San Marcos | 21 | Código nominal |
| SANTA ROSA | Santa Rosa | 22 | Código nominal |
| SOLOLÁ | Sololá | 23 | Código nominal |
| SUCHITEPÉQUEZ | Suchitepéquez | 24 | Código nominal |
| TOTONICAPÁN | Totonicapán | 25 | Código nominal |
| ZACAPA | Zacapa | 26 | Código nominal |

## Reglas de uso

1. Usar `CODIGO` como llave; no deduplicar por nombre.
2. Conservar los campos `*_ORIGINAL` en cualquier proceso auditable.
3. Interpretar los códigos categóricos como nominales, no ordinales.
4. Consultar los indicadores de ausencia y el archivo de candidatos parciales antes de tomar decisiones.
5. Mantener fuente, fecha de extracción y versión al publicar derivados.
