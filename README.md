# Entrega final 2026 · Proyecto 1 · Obtención y limpieza de datos

## Descripción

Esta entrega reproduce el diagnóstico, la limpieza, la integración nacional, el control de calidad y la documentación de los establecimientos educativos autorizados por el MINEDUC para el nivel Diversificado.

- Fuente: <http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/>
- Fecha documentada del snapshot crudo: **2026-07-10**
- Fecha de procesamiento final: **2026-07-17**
- Versión del conjunto limpio: **2.0.0**
- Curso: **CC3084 – Data Science · Semestre II 2026**

## Resultados verificados

- Datos crudos: **11,603 filas × 17 variables**.
- Datos limpios completos: **11,603 filas × 59 variables**.
- Vista analítica: **11,603 filas × 42 variables**.
- Códigos únicos: **11,603**.
- Duplicados exactos: **0**.
- Pares candidatos a duplicado parcial: **13,031**, todos con decisión documentada.
- Revisión manual recomendada: **2,063 pares**.
- Filas eliminadas automáticamente: **0**.
- Controles automáticos aprobados: **27/27**.
- Validaciones cruzadas aprobadas: **7/7**.
- Catálogo observado: **334 códigos municipales y 22 zonas capitalinas**. La referencia nacional SEGEPLAN 2026 informa 340 municipios.

El incremento de faltantes analíticos de 5,253 a 5,370 celdas es intencional: 69 distritos incompletos y 48 teléfonos no interpretables dejan de aparentar validez. Sus valores originales permanecen en las columnas `*_ORIGINAL`.

## Archivos principales

- `codigo/Proyecto_1_MINEDUC_2026_Final_Ejecutado.ipynb`: notebook autocontenido, ejecutado, sin errores y con salidas HTML/MathJax.
- `documentacion/Informe_Final_Proyecto_1_MINEDUC.docx` y `.pdf`: informe formal de 22 páginas.
- `documentacion/Libro_de_Codigos_MINEDUC.docx`, `.pdf` y `.md`: descripción de las 59 variables, dominios, tratamientos, derivaciones, fuente, fecha y versión.
- `documentacion/Proyecto_1_MINEDUC_2026_Datos_Libro_Codigos.xlsx`: panel, muestra analítica de 3,000 filas, diagnóstico, plan, transformaciones, controles, catálogos y metadatos. Los CSV adjuntos contienen todos los registros y detalles.
- `datos/establecimientos_diversificado_limpio.csv`: conjunto nacional completo de 11,603 × 59.
- `datos/establecimientos_diversificado_limpio_analitico.csv`: vista analítica completa de 11,603 × 42.
- `datos/datos_crudos_establecimientos_diversificado.csv`: snapshot crudo preservado byte a byte.
- `datos/bitacora_cambios_detalle.csv`: 174,608 cambios por código y variable.
- `datos/candidatos_duplicados_parciales.csv`: evidencia y decisión para 13,031 pares.
- `datos/resumen_transformaciones.csv`: tabla de cinco columnas exigida por la guía.
- `datos/calidad_antes_despues.csv`: comparación de trece métricas.
- `datos/controles_calidad.csv`: 27 pruebas automáticas.
- `datos/verificacion_tipos.csv`: verificación de tipo esperado por columna (59 variables).
- `datos/verificacion_formatos.csv`: verificación de formato de teléfonos, códigos, distritos, nombres y direcciones.
- `datos/validaciones_consistencia_cruzada.csv`: siete pruebas entre variables.
- `datos/catalogo_territorial_observado.csv`: catálogo territorial del universo consultado.
- `datos/libro_codigos.csv`: versión tabular del libro de códigos.

## Reproducción

1. Instalar Python 3.11 o posterior.
2. Ejecutar `pip install -r requirements.txt`.
3. Colocar el notebook y `datos_crudos_establecimientos_diversificado.csv` en la misma carpeta.
4. Abrir `Proyecto_1_MINEDUC_2026_Final_Ejecutado.ipynb`.
5. Ejecutar **Restart Kernel and Run All Cells**.
6. Confirmar **27/27 controles**, **7/7 validaciones cruzadas** y ausencia de salidas de error.

## Convenciones

- `*_ORIGINAL`: valor publicado, sin sobrescritura.
- `*_LIMPIO` / `*_LIMPIA`: presentación analítica.
- `*_COD`: código nominal, salvo los territoriales documentados.
- `*_ESTADO` / `*_INFORMADA`: calidad, interpretación o ausencia.
- `null`: ausencia técnica o semántica documentada; nunca una imputación arbitraria.
- `CODIGO`: llave del servicio autorizado.
