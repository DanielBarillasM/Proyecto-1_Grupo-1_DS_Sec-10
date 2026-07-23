# Universidad del Valle de Guatemala

**Facultad de Ingeniería · Departamento de Ciencias de la Computación**
**CC3084 – Data Science · Semestre II 2026**

# Proyecto 1: Obtención y Limpieza de Datos

## Establecimientos educativos de Guatemala · Nivel Diversificado

**Integrantes**

| Nombre | Carné |
|---|---|
| Abby Sofia Donis Agreda | 22440 |
| Pablo Daniel Barillas Moreno | 22193 |
| Jorge Palacios | 231385 |
| Roberto Emiliano Otoniel Camposeco Torres | 23968 |

**Versión de la entrega:** 2.0.0
**Fecha de extracción del snapshot:** 10 de julio de 2026
**Fecha de procesamiento final:** 17 de julio de 2026

## Descripción

Este repositorio documenta el proceso completo de obtención, diagnóstico, limpieza, integración nacional, control de calidad y documentación de los establecimientos educativos autorizados por el Ministerio de Educación de Guatemala (MINEDUC) en el nivel Diversificado, conforme a la guía oficial del curso (`Entrega_Final_Proyecto_1_MINEDUC/lineamientos/`).

- Fuente: <http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/>

## Correspondencia con la guía del proyecto

| Actividad exigida | Evidencia | Ubicación |
|---|---|---|
| Obtención y unión nacional de los datos | 23 particiones geográficas crudas consolidadas en un único CSV | `datos/datos_crudos_establecimientos_diversificado.csv`, `datos_crudos_por_origen/` |
| Diagnóstico del estado inicial | Perfil por variable: tipo, valores únicos, faltantes técnicos/semánticos, dominios y formatos | `datos/perfil_datos_crudos.csv` |
| Plan de limpieza | Problema, regla, justificación y riesgo documentados para las 17 variables crudas | `datos/plan_limpieza_por_variable.csv` |
| Limpieza de todas las variables | Reglas ejecutadas y trazadas por código y variable; ninguna fila se elimina | `datos/bitacora_cambios_detalle.csv`, `datos/bitacora_reglas_resumen.csv` |
| Registro de transformaciones | Tabla de cinco columnas exigida por la guía, para las 17 variables | `datos/resumen_transformaciones.csv` |
| Duplicados exactos y parciales | 0 duplicados exactos; 13,031 pares evaluados con similitud de cadenas (TF–IDF) y decisión conservadora por par, sin eliminaciones automáticas | `datos/candidatos_duplicados_parciales.csv` |
| Consistencia entre variables | 7 validaciones cruzadas entre campos relacionados (CV01–CV07) | `datos/validaciones_consistencia_cruzada.csv` |
| Pruebas automáticas del conjunto limpio | 27 controles de aceptación (QC01–QC27) | `datos/controles_calidad.csv` |
| Informe de calidad antes/después | 13 métricas comparables sobre registros, faltantes, formatos y categorías | `datos/calidad_antes_despues.csv` |
| Generación del conjunto limpio | Unión nacional de 11,603 filas × 59 variables, sin errores detectados | `datos/establecimientos_diversificado_limpio.csv` |
| Libro de códigos | 59 variables documentadas: descripción, tipo, dominio, valores posibles, tratamiento, variables derivadas, fecha de extracción, fuente y versión | `documentacion/Libro_de_Codigos_MINEDUC.docx`, `.pdf`, `.md` |
| Reproducibilidad | Notebook ejecutado de punta a punta con kernel limpio, sin pasos manuales ocultos | `codigo/Proyecto_1_MINEDUC_2026_Final_Ejecutado.ipynb` |

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
- Catálogo territorial observado: **334 códigos municipales y 22 zonas capitalinas**. La referencia nacional SEGEPLAN 2026 informa 340 municipios.

El incremento de faltantes analíticos de 5,253 a 5,370 celdas es intencional: 69 distritos incompletos y 48 teléfonos no interpretables dejan de aparentar validez. Sus valores originales permanecen en las columnas `*_ORIGINAL`.

## Estructura del repositorio

```
Entrega_Final_Proyecto_1_MINEDUC/
├── codigo/                    notebooks ejecutados (ver "Notebook principal")
├── codigo_fuente/              scripts que generan el notebook y los documentos
├── datos/                      CSV de entrega: crudo, limpio, bitácora, controles, libro de códigos
├── datos_crudos_por_origen/    23 particiones crudas por categoría geográfica
├── resultados/                 gráficas y tablas de distribución del conjunto limpio
├── documentacion/               informe final, libro de códigos y panel Excel
└── lineamientos/                guía oficial del proyecto (PDF)
```

## Notebook principal

`codigo/Proyecto_1_MINEDUC_2026_Final_Ejecutado.ipynb` es el notebook autoritativo de esta entrega: produce todos los archivos de `datos/` y `resultados/`, y alimenta la documentación en `documentacion/`. `codigo/Proyecto_1_MINEDUC_Final.ipynb` corresponde a una versión preliminar (1.0) que se conserva por trazabilidad del proceso de desarrollo, pero no genera los entregables finales de esta versión 2.0.0.

## Archivos principales

- `codigo/Proyecto_1_MINEDUC_2026_Final_Ejecutado.ipynb`: notebook autocontenido, ejecutado, sin errores y con salidas HTML/MathJax.
- `documentacion/Informe_Final_Proyecto_1_MINEDUC.docx` y `.pdf`: informe formal de la entrega.
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
3. Colocar `codigo/Proyecto_1_MINEDUC_2026_Final_Ejecutado.ipynb` y `datos_crudos_establecimientos_diversificado.csv` en la misma carpeta.
4. Abrir el notebook.
5. Ejecutar **Restart Kernel and Run All Cells**.
6. Confirmar **27/27 controles**, **7/7 validaciones cruzadas** y ausencia de salidas de error.

## Convenciones

- `*_ORIGINAL`: valor publicado, sin sobrescritura.
- `*_LIMPIO` / `*_LIMPIA`: presentación analítica.
- `*_COD`: código nominal, salvo los territoriales documentados.
- `*_ESTADO` / `*_INFORMADA`: calidad, interpretación o ausencia.
- `null`: ausencia técnica o semántica documentada; nunca una imputación arbitraria.
- `CODIGO`: llave del servicio autorizado.

## Licencia

Distribuido bajo licencia MIT — ver [`LICENSE`](LICENSE). © 2026 Abby Sofia Donis Agreda, Pablo Daniel Barillas Moreno, Jorge Palacios y Roberto Emiliano Otoniel Camposeco Torres.
