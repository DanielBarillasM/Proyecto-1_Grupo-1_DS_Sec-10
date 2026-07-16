# Entrega final · Proyecto 1 · Obtención y limpieza de datos

## Descripción

Esta entrega documenta y ejecuta la obtención, el diagnóstico, la limpieza, la integración nacional y la documentación de los datos de establecimientos educativos autorizados por el MINEDUC para el nivel Diversificado.

Fuente declarada: <http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/>

Fecha de procesamiento reproducible: **16 de julio de 2026**.

## Resultados principales

- Conjunto crudo: **11,603 filas × 17 variables**.
- Conjunto limpio completo: **11,603 filas × 56 variables**.
- Vista analítica: **11,603 filas × 39 variables**.
- Códigos únicos: **11,603**.
- Duplicados exactos crudos: **0**.
- Filas eliminadas: **0**.
- Categorías geográficas de origen: **23**.
- Departamentos analíticos: **22**.
- Registros de Ciudad Capital: **2,161**.
- Controles aprobados: **17 de 17**.

## Archivos principales

- `Proyecto_1_MINEDUC_Final_Ejecutado.ipynb`: notebook ejecutado de principio a fin, con Markdown HTML, salidas HTML, fórmulas MathJax, tablas, gráficos, interpretación y limitaciones.
- `Informe_Final_Proyecto_1_MINEDUC.docx` y `.pdf`: informe formal completo.
- `Libro_de_Codigos_MINEDUC.docx` y `.pdf`: descripción general, diccionario de las 56 variables y catálogos.
- `Proyecto_1_MINEDUC_Datos_Libro_Codigos.xlsx`: panel de resultados, datos analíticos, diagnóstico, reglas, controles, manifiesto y catálogos.
- `datos/establecimientos_diversificado_limpio.csv`: conjunto nacional completo y trazable.
- `datos/establecimientos_diversificado_limpio_analitico.csv`: subconjunto práctico para análisis en Excel.
- `datos/datos_crudos_establecimientos_diversificado.csv`: consolidado crudo preservado.
- `datos/bitacora_cambios_detalle.csv`: cambios por código y variable.
- `datos/bitacora_reglas_resumen.csv`: reglas, razones, riesgos, controles y filas afectadas.
- `datos/catalogos_codificacion.csv`: códigos nominales y etiquetas.
- `datos/controles_calidad.csv`: 17 pruebas de calidad.
- `datos/perfil_datos_crudos.csv`: diagnóstico cuantitativo de las 17 variables iniciales.
- `datos_crudos_por_origen/`: 23 particiones auditables derivadas del consolidado crudo.

## Cómo reproducir

1. Instalar Python 3.11 o posterior y las dependencias indicadas en `requirements.txt`.
2. Colocar `Proyecto_1_MINEDUC_Final_Ejecutado.ipynb` y el CSV crudo en la misma carpeta.
3. Abrir el notebook con JupyterLab o Jupyter Notebook.
4. Ejecutar **Restart Kernel and Run All Cells**.
5. Confirmar que la sección de control muestre **17/17** y que no exista ninguna salida de error.

El notebook busca primero el archivo `datos_crudos_establecimientos_diversificado.csv`. Si no se encuentra junto al cuaderno, utiliza la copia incluida en `salidas_proyecto_1/datos/`.

## Convenciones de limpieza

- Las columnas `*_ORIGINAL` preservan la fuente.
- Las columnas `*_LIMPIO` contienen una presentación apta para análisis e informes.
- Las columnas `*_COD` son códigos nominales, salvo los códigos territoriales documentados.
- Las columnas `*_ESTADO` y `*_INFORMADA` explican calidad o ausencia.
- `null` se usa solamente cuando existe ausencia real o semántica; no se imputan nombres, teléfonos, distritos ni jornadas.
- `SIN JORNADA` y `SIN ESPECIFICAR` se conservan en la columna original y se representan como `null` en la columna analítica.
- Ciudad Capital se mantiene como origen y como grupo de ubicación, pero se integra a Guatemala en `DEPARTAMENTO_ANALISIS`.
- Los nombres no se deduplican por similitud. `CODIGO` es la llave de cada servicio.

## Precauciones de interpretación

Cada fila representa un código de servicio educativo autorizado, no necesariamente un edificio físico único. Las correcciones ortográficas son conservadoras y trazables; para usos legales o administrativos debe contrastarse el nombre con la fuente oficial y consultarse la columna original.

