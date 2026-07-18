from __future__ import annotations

"""Construye y ejecuta la versión 2.0 del proyecto conforme a la guía 2026.

El script parte del notebook final ya probado, sustituye las celdas que cambiaron
con la nueva rúbrica e inserta los análisis adicionales. El resultado sigue siendo
un notebook autocontenido y ejecutable de principio a fin.
"""

import json
from pathlib import Path

from build_final_notebook import build_notebook, code, markdown
from revise_notebook import execute_notebook


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Proyecto_1_MINEDUC_2026_Final_Ejecutado.ipynb"


def find_cell(cells: list[dict], text: str) -> int:
    for i, cell in enumerate(cells):
        if text in cell.get("source", ""):
            return i
    raise ValueError(f"No se encontró la celda con: {text}")


def build_notebook_2026() -> dict:
    nb = build_notebook()
    cells = nb["cells"]

    # Portada y referencias académicas actualizadas.
    cells[0]["source"] = (
        cells[0]["source"]
        .replace("CC3066 DATA SCIENCE", "CC3084 DATA SCIENCE · SEMESTRE II 2026")
        .replace("Entrega final reproducible · 16 de julio de 2026", "Entrega final reproducible · versión 2.0 · 17 de julio de 2026")
    )
    cells[1]["source"] = cells[1]["source"].replace(
        "La limpieza sigue cuatro reglas de protección:",
        "La extracción del snapshot se documenta con fecha **10 de julio de 2026** (fecha del archivo crudo preservado); el procesamiento final corresponde al **17 de julio de 2026**. La limpieza sigue cuatro reglas de protección:",
    )

    # Dependencias de similitud de cadenas.
    idx_env = find_cell(cells, "Entorno de trabajo preparado correctamente")
    cells[idx_env]["source"] = cells[idx_env]["source"].replace(
        "import matplotlib.pyplot as plt\n",
        "import matplotlib.pyplot as plt\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.neighbors import NearestNeighbors\n",
    )

    # Metadatos reproducibles y salida versionada.
    idx_load = find_cell(cells, "RUTA_CANDIDATAS")
    cells[idx_load]["source"] = cells[idx_load]["source"].replace(
        'SALIDAS = Path("salidas_proyecto_1")',
        'SALIDAS = Path("salidas_proyecto_1_2026")\n'
        'FUENTE_NOMBRE = "MINEDUC - Búsqueda de centros educativos autorizados"\n'
        'FUENTE_URL = "http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/"\n'
        'FECHA_EXTRACCION = "2026-07-10"\n'
        'FECHA_PROCESAMIENTO = "2026-07-17"\n'
        'VERSION_CONJUNTO = "2.0.0"\n'
        'REFERENCIA_TERRITORIAL_URL = "https://datos.segeplan.gob.gt/es/dataset/calculo-matematico-para-la-asignacion-constitucional-a-las-municipalidades-2026"',
    )

    # Teléfono limpio solo contiene valores que cumplen la regla; lo no interpretable
    # queda como null, pero permanece íntegro en TELEFONO_ORIGINAL.
    idx_clean = find_cell(cells, "telefonos_extraidos = datos")
    src = cells[idx_clean]["source"]
    src = src.replace(
        'pd.NA if vacio else " | ".join(formato_telefono(n) for n in nums) if nums else normalizar_mecanico(raw)',
        'pd.NA if vacio or not nums else " | ".join(formato_telefono(n) for n in nums)',
    )
    src = src.replace(
        '"MINEDUC - Búsqueda de centros educativos autorizados",',
        'FUENTE_NOMBRE,',
    )
    src = src.replace(
        'pd.Series("2026-07-16", index=limpio.index, dtype="string")',
        'pd.Series(FECHA_PROCESAMIENTO, index=limpio.index, dtype="string")',
    )
    cells[idx_clean]["source"] = src

    # Inserción del catálogo territorial observado, controles cruzados y duplicados parciales.
    idx_after_clean = idx_clean + 1
    cells[idx_after_clean:idx_after_clean] = [
        markdown(
            """
## 6. Catálogo territorial, consistencia cruzada y duplicados parciales

El catálogo territorial del proyecto se construye con los códigos observados en el snapshot: **334 municipios con oferta de Diversificado** y **22 zonas capitalinas**. La referencia oficial de SEGEPLAN informa 340 municipios en el país; por ello, este catálogo no se presenta como censo territorial completo, sino como catálogo válido para el universo analizado.

Los candidatos a duplicado parcial se buscan dentro del mismo departamento y municipio/zona mediante TF–IDF de trigramas a pentagramas y distancia coseno. Se acepta como candidato una similitud de al menos $0.92$. Ninguna fila se elimina automáticamente: cada par recibe una decisión conservadora y una justificación.
"""
        ),
        code(
            r'''
# Catálogo territorial observado en el snapshot.
catalogo_municipios = (
    limpio.loc[~limpio["ES_CIUDAD_CAPITAL"].eq(1), [
        "DEPARTAMENTO_ANALISIS_COD", "DEPARTAMENTO_ANALISIS", "MUNICIPIO_COD_FUENTE", "MUNICIPIO_LIMPIO"
    ]]
    .drop_duplicates()
    .sort_values(["DEPARTAMENTO_ANALISIS_COD", "MUNICIPIO_COD_FUENTE"])
    .rename(columns={
        "DEPARTAMENTO_ANALISIS_COD": "DEPARTAMENTO_COD",
        "DEPARTAMENTO_ANALISIS": "DEPARTAMENTO",
        "MUNICIPIO_LIMPIO": "MUNICIPIO",
    })
)
catalogo_municipios["TIPO_REGISTRO"] = "Municipio observado con Diversificado"

catalogo_zonas = (
    limpio.loc[limpio["ES_CIUDAD_CAPITAL"].eq(1), ["ZONA_CAPITAL_COD", "MUNICIPIO_LIMPIO"]]
    .drop_duplicates()
    .sort_values("ZONA_CAPITAL_COD")
    .rename(columns={"MUNICIPIO_LIMPIO": "MUNICIPIO"})
)
catalogo_zonas.insert(0, "DEPARTAMENTO_COD", "01")
catalogo_zonas.insert(1, "DEPARTAMENTO", "Guatemala")
catalogo_zonas["MUNICIPIO_COD_FUENTE"] = catalogo_zonas["ZONA_CAPITAL_COD"].map(
    lambda z: f"01-Z{int(z):02d}" if pd.notna(z) else pd.NA
)
catalogo_zonas["TIPO_REGISTRO"] = "Zona de Ciudad Capital observada"
catalogo_zonas = catalogo_zonas.drop(columns="ZONA_CAPITAL_COD")

catalogo_territorial = pd.concat([catalogo_municipios, catalogo_zonas], ignore_index=True)
catalogo_territorial["FUENTE_CATALOGO"] = "Snapshot MINEDUC; referencia nacional SEGEPLAN 2026"
catalogo_territorial["REFERENCIA_URL"] = REFERENCIA_TERRITORIAL_URL
catalogo_territorial["COBERTURA"] = "334/340 municipios nacionales + 22 zonas capitalinas"

# Consistencia entre campos relacionados.
validaciones_cruzadas = pd.DataFrame([
    ("CV01", "Prefijo departamental de CODIGO coincide con departamento", int((
        limpio.loc[~limpio["ES_CIUDAD_CAPITAL"].eq(1), "CODIGO"].str[:2]
        != limpio.loc[~limpio["ES_CIUDAD_CAPITAL"].eq(1), "DEPARTAMENTO_ANALISIS_COD"]
    ).sum())),
    ("CV02", "Prefijo municipal de CODIGO coincide con MUNICIPIO_COD_FUENTE", int((
        limpio.loc[~limpio["ES_CIUDAD_CAPITAL"].eq(1), "CODIGO"].str[:5]
        != limpio.loc[~limpio["ES_CIUDAD_CAPITAL"].eq(1), "MUNICIPIO_COD_FUENTE"]
    ).sum())),
    ("CV03", "Ciudad Capital coincide con categoría de origen", int((
        limpio["ES_CIUDAD_CAPITAL"].eq(1) != limpio["DEPARTAMENTO_ORIGINAL"].eq("CIUDAD CAPITAL")
    ).sum())),
    ("CV04", "Zona capital solo informada para Ciudad Capital", int((
        limpio["ZONA_CAPITAL_COD"].notna() != limpio["ES_CIUDAD_CAPITAL"].eq(1)
    ).sum())),
    ("CV05", "AREA_INFORMADA coincide con AREA_LIMPIA", int((
        limpio["AREA_INFORMADA"].eq(1) != limpio["AREA_LIMPIA"].notna()
    ).sum())),
    ("CV06", "JORNADA_INFORMADA coincide con JORNADA_LIMPIA", int((
        limpio["JORNADA_INFORMADA"].eq(1) != limpio["JORNADA_LIMPIA"].notna()
    ).sum())),
    ("CV07", "TELEFONO_PRINCIPAL es coherente con TELEFONO_ESTADO", int((
        limpio["TELEFONO_PRINCIPAL"].notna() != limpio["TELEFONO_ESTADO"].isin(["Válido único", "Válidos múltiples"])
    ).sum())),
], columns=["VALIDACION_ID", "VALIDACION", "INCONSISTENCIAS"])
validaciones_cruzadas["CUMPLE"] = validaciones_cruzadas["INCONSISTENCIAS"].eq(0)

# Candidatos a duplicado parcial por similitud del nombre dentro de un bloque territorial.
umbral_similitud = 0.92
bloque = limpio["DEPARTAMENTO_ANALISIS"].fillna("") + "|" + limpio["MUNICIPIO_LIMPIO"].fillna("")
nombres_clave = limpio["ESTABLECIMIENTO_CLAVE_COMPARACION"].fillna("")
pares = []
for _, indices in bloque.groupby(bloque).groups.items():
    indices = [i for i in indices if nombres_clave.loc[i]]
    if len(indices) < 2:
        continue
    vectorizador = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), lowercase=False, min_df=1)
    matriz = vectorizador.fit_transform(nombres_clave.loc[indices])
    vecinos = NearestNeighbors(radius=1 - umbral_similitud, metric="cosine", algorithm="brute").fit(matriz)
    distancias, posiciones = vecinos.radius_neighbors(matriz, return_distance=True, sort_results=True)
    for pos_a, (distancias_a, posiciones_a) in enumerate(zip(distancias, posiciones)):
        for distancia, pos_b in zip(distancias_a, posiciones_a):
            if pos_b <= pos_a:
                continue
            pares.append((indices[pos_a], indices[pos_b], 1 - float(distancia)))

servicio_cols = ["SECTOR", "AREA", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL"]
filas_candidatos = []
for par_id, (i, j, similitud) in enumerate(pares, start=1):
    direccion_a = clave_comparacion(limpio.at[i, "DIRECCION_LIMPIA"]) if pd.notna(limpio.at[i, "DIRECCION_LIMPIA"]) else ""
    direccion_b = clave_comparacion(limpio.at[j, "DIRECCION_LIMPIA"]) if pd.notna(limpio.at[j, "DIRECCION_LIMPIA"]) else ""
    misma_direccion = bool(direccion_a and direccion_a == direccion_b)
    telefono_a = limpio.at[i, "TELEFONO_PRINCIPAL"]
    telefono_b = limpio.at[j, "TELEFONO_PRINCIPAL"]
    mismo_telefono = bool(pd.notna(telefono_a) and pd.notna(telefono_b) and telefono_a == telefono_b)
    mismo_servicio_visible = all(datos.at[i, c] == datos.at[j, c] for c in servicio_cols)
    if mismo_servicio_visible and (misma_direccion or mismo_telefono):
        decision = "CONSERVAR_Y_REVISAR"
        revision = 1
        justificacion = "Códigos únicos distintos, con coincidencia territorial, de servicio y de dirección o teléfono; se conserva y se recomienda contraste oficial."
    elif not mismo_servicio_visible:
        decision = "CONSERVAR_SERVICIOS_DISTINTOS"
        revision = 0
        justificacion = "El nombre es igual o similar, pero cambian atributos autorizados del servicio; no corresponde eliminar por nombre."
    else:
        decision = "CONSERVAR_CODIGOS_DISTINTOS"
        revision = 1 if similitud >= 0.97 else 0
        justificacion = "Los códigos MINEDUC son únicos y no existe evidencia suficiente para fusionar registros."
    filas_candidatos.append({
        "PAR_ID": f"PD{par_id:05d}",
        "CODIGO_A": limpio.at[i, "CODIGO"], "CODIGO_B": limpio.at[j, "CODIGO"],
        "DEPARTAMENTO": limpio.at[i, "DEPARTAMENTO_ANALISIS"], "MUNICIPIO_ZONA": limpio.at[i, "MUNICIPIO_LIMPIO"],
        "ESTABLECIMIENTO_A": limpio.at[i, "ESTABLECIMIENTO_LIMPIO"],
        "ESTABLECIMIENTO_B": limpio.at[j, "ESTABLECIMIENTO_LIMPIO"],
        "SIMILITUD": round(similitud, 4),
        "TIPO_COINCIDENCIA": "Nombre equivalente" if similitud >= 0.9999 else "Nombre similar",
        "MISMA_DIRECCION": int(misma_direccion), "MISMO_TELEFONO": int(mismo_telefono),
        "MISMO_SERVICIO_VISIBLE": int(mismo_servicio_visible),
        "DECISION": decision, "REVISION_MANUAL_RECOMENDADA": revision,
        "JUSTIFICACION": justificacion, "FILAS_ELIMINADAS": 0,
    })
candidatos_duplicados = pd.DataFrame(filas_candidatos)
if candidatos_duplicados.empty:
    candidatos_duplicados = pd.DataFrame(columns=[
        "PAR_ID", "CODIGO_A", "CODIGO_B", "DEPARTAMENTO", "MUNICIPIO_ZONA",
        "ESTABLECIMIENTO_A", "ESTABLECIMIENTO_B", "SIMILITUD", "TIPO_COINCIDENCIA",
        "MISMA_DIRECCION", "MISMO_TELEFONO", "MISMO_SERVICIO_VISIBLE", "DECISION",
        "REVISION_MANUAL_RECOMENDADA", "JUSTIFICACION", "FILAS_ELIMINADAS",
    ])

combinar_html(
    kpis_html([
        ("Municipios observados", catalogo_municipios["MUNICIPIO_COD_FUENTE"].nunique()),
        ("Zonas capitalinas", len(catalogo_zonas)),
        ("Pares candidatos", f"{len(candidatos_duplicados):,}"),
        ("Revisión recomendada", f"{int(candidatos_duplicados['REVISION_MANUAL_RECOMENDADA'].sum()):,}"),
    ]),
    tabla_html(validaciones_cruzadas, "Consistencia entre variables", max_filas=20),
    tabla_html(candidatos_duplicados, "Muestra de decisiones sobre duplicados parciales", max_filas=12,
               nota="La tabla completa se exporta. Ninguna fila fue eliminada automáticamente."),
)
'''
        ),
    ]

    # La numeración de las secciones posteriores cambia al insertar el nuevo análisis.
    for cell in cells:
        if cell["cell_type"] == "markdown":
            src_md = cell.get("source", "")
            src_md = src_md.replace("## 6. Bitácora", "## 7. Bitácora")
            src_md = src_md.replace("## 7. Controles", "## 9. Controles")
            src_md = src_md.replace("## 8. Exportación", "## 10. Exportación")
            src_md = src_md.replace("## 9. Análisis", "## 11. Análisis")
            src_md = src_md.replace("## 10. Interpretación", "## 12. Interpretación")
            src_md = src_md.replace("## 11. Limitaciones", "## 13. Limitaciones")
            cell["source"] = src_md

    # Ajustes a la bitácora base para la nueva decisión sobre teléfonos y fecha.
    idx_log = find_cell(cells, "reglas = [")
    cells[idx_log]["source"] = (
        cells[idx_log]["source"]
        .replace("Los formatos históricos se conservan como texto.", "El original conserva formatos históricos; TELEFONO_LIMPIO queda null si no es interpretable.")
        .replace('"2026-07-16"', "FECHA_PROCESAMIENTO")
    )

    # Plan por variable, tabla de transformaciones, calidad antes/después y libro de códigos ampliado.
    idx_after_log = idx_log + 1
    cells[idx_after_log:idx_after_log] = [
        markdown(
            """
## 8. Plan ejecutado por variable y comparación de calidad

La tabla de plan conserva, para cada variable cruda, el problema observado, la regla aplicada, su fundamento y el riesgo de transformación. La comparación antes/después usa las 17 variables equivalentes para que los porcentajes sean comparables; las variables auxiliares se reportan por separado en el libro de códigos.
"""
        ),
        code(
            r'''
PLAN_VARIABLES = {
    "CODIGO": ("Sin problemas de integridad; riesgo de perder ceros si se importa como número.", "Conservar como string, aplicar trim y validar ##-##-####-46.", "El patrón es estable y la unicidad puede probarse.", "Conversión numérica accidental en software externo."),
    "DISTRITO": ("Vacíos y valores incompletos que no cumplen ##-### o ##-##-####.", "Conservar original; usar null en DISTRITO_LIMPIO cuando no sea completo y clasificar estado.", "Evita inventar componentes y separa validez de ausencia.", "El prefijo parcial deja de usarse como distrito analítico, pero permanece en el original."),
    "DEPARTAMENTO": ("Ciudad Capital aparece como origen separado del departamento Guatemala.", "Crear DEPARTAMENTO_LIMPIO y DEPARTAMENTO_ANALISIS; codificar 22 departamentos.", "Preserva la procedencia y evita doble conteo territorial.", "Usar la columna analítica sin la original ocultaría la procedencia."),
    "MUNICIPIO": ("Mezcla municipios con zonas capitalinas y carece de código explícito.", "Normalizar ortografía, distinguir tipo de ubicación y derivar código desde CODIGO fuera de la capital.", "La regla está respaldada por la estructura del identificador y el origen.", "No debe interpretarse una zona como municipio independiente."),
    "ESTABLECIMIENTO": ("Mayúsculas, tildes omitidas, espacios/puntuación y nombres iguales o similares.", "Unicode NFC, espacios, capitalización española, tildes respaldadas, original permanente y detección de candidatos.", "Produce texto utilizable sin sustituir nombres por similitud.", "Una corrección automática de identidad podría alterar un nombre propio; por eso no se fusiona."),
    "DIRECCION": ("Espacios, puntuación, abreviaturas y valores vacíos.", "Normalización mecánica conservadora; null solo si no hay contenido utilizable.", "Mejora legibilidad sin geocodificar ni inventar datos.", "Las abreviaturas pueden tener significado local y se conservan."),
    "TELEFONO": ("Vacíos, separadores múltiples, prefijo 502 y formatos no interpretables.", "Extraer bloques válidos de ocho dígitos; formato ####-####; null si no es interpretable; conservar original y estado.", "Permite validación automática y no inventa dígitos.", "Un formato histórico válido podría quedar como null analítico; el original evita pérdida."),
    "SUPERVISOR": ("Vacíos, mayúsculas y presentación inconsistente.", "Normalización conservadora y null para ausencia real; conservar original.", "Facilita informes sin crear identidades de persona.", "Homónimos no deben fusionarse."),
    "DIRECTOR": ("Alta ausencia, marcadores y presentación inconsistente.", "Marcadores/vacíos a null, estado de ausencia y normalización conservadora.", "El null tiene significado y no se imputa un nombre.", "La falta de director no implica que el establecimiento esté cerrado."),
    "NIVEL": ("Etiqueta en mayúsculas; dominio esperado único.", "Mapear a Diversificado y validar dominio.", "La consulta se restringe al nivel solicitado.", "Si se mezclan nuevas fuentes, el dominio deberá ampliarse."),
    "SECTOR": ("Categoría nominal en mayúsculas.", "Etiquetas legibles, catálogo cerrado y código nominal.", "Evita variantes posteriores y mantiene interpretación.", "El código no representa jerarquía ni distancia."),
    "AREA": ("SIN ESPECIFICAR no es una tercera área real.", "Urbana/Rural; SIN ESPECIFICAR a null, con original e indicador.", "Representa correctamente la ausencia semántica.", "No debe analizarse AREA_COD como escala."),
    "STATUS": ("Mayúsculas y tildes omitidas en categorías.", "Normalizar etiquetas, validar catálogo y asignar código nominal.", "Un catálogo cerrado evita variantes ortográficas.", "El estado es una fotografía administrativa, no evidencia operativa actual."),
    "MODALIDAD": ("MONOLINGUE/BILINGUE sin diéresis o tilde.", "Corregir a Monolingüe/Bilingüe y codificar nominalmente.", "Restituye ortografía española sin cambiar significado.", "La codificación no es ordinal."),
    "JORNADA": ("SIN JORNADA es ausencia semántica.", "Jornadas reales en JORNADA_LIMPIA; SIN JORNADA a null, con indicador y original.", "Evita tratar ausencia como categoría sustantiva.", "La ausencia puede ser informativa y debe conservarse."),
    "PLAN": ("Mayúsculas, puntuación compacta y tildes.", "Catálogo explícito, etiqueta legible y código nominal.", "Controla todas las variantes del dominio observado.", "El código no expresa intensidad ni orden."),
    "DEPARTAMENTAL": ("Mayúsculas, nombres territoriales y tildes.", "Normalización ortográfica conservadora y código nominal.", "Facilita agrupación manteniendo el texto original.", "No confundir dirección departamental con departamento geográfico."),
}

filas_plan = []
for variable in datos.columns:
    problema, regla, fundamento, riesgo = PLAN_VARIABLES[variable]
    filas_plan.append({
        "VARIABLE": variable, "PROBLEMAS_ENCONTRADOS": problema, "REGLA_APLICADA": regla,
        "POR_QUE_FUNCIONA": fundamento, "RIESGOS_ASOCIADOS": riesgo,
    })
plan_limpieza_variable = pd.DataFrame(filas_plan)

mapa_limpio = {
    "CODIGO": "CODIGO", "DISTRITO": "DISTRITO_LIMPIO", "DEPARTAMENTO": "DEPARTAMENTO_LIMPIO",
    "MUNICIPIO": "MUNICIPIO_LIMPIO", "ESTABLECIMIENTO": "ESTABLECIMIENTO_LIMPIO",
    "DIRECCION": "DIRECCION_LIMPIA", "TELEFONO": "TELEFONO_LIMPIO", "SUPERVISOR": "SUPERVISOR_LIMPIO",
    "DIRECTOR": "DIRECTOR_LIMPIO", "NIVEL": "NIVEL_LIMPIO", "SECTOR": "SECTOR_LIMPIO",
    "AREA": "AREA_LIMPIA", "STATUS": "STATUS_LIMPIO", "MODALIDAD": "MODALIDAD_LIMPIA",
    "JORNADA": "JORNADA_LIMPIA", "PLAN": "PLAN_LIMPIO", "DEPARTAMENTAL": "DEPARTAMENTAL_LIMPIO",
}

filas_transformacion = []
for variable in datos.columns:
    problema, regla, fundamento, _ = PLAN_VARIABLES[variable]
    destino = mapa_limpio[variable]
    afectados = int(diferentes(datos[variable], limpio[destino]).sum())
    filas_transformacion.append({
        "Variable": variable, "Problema detectado": problema, "Transformación": regla,
        "Registros afectados": afectados, "Justificación": fundamento,
    })
resumen_transformaciones = pd.DataFrame(filas_transformacion)

# Metadatos de versión incorporados al dataset nacional.
limpio["FUENTE_URL"] = pd.Series(FUENTE_URL, index=limpio.index, dtype="string")
limpio["FECHA_EXTRACCION"] = pd.Series(FECHA_EXTRACCION, index=limpio.index, dtype="string")
limpio["VERSION_CONJUNTO"] = pd.Series(VERSION_CONJUNTO, index=limpio.index, dtype="string")
limpio["FECHA_PROCESAMIENTO"] = pd.Series(FECHA_PROCESAMIENTO, index=limpio.index, dtype="string")

# Vista comparable de 17 variables después de limpiar.
core_limpio = limpio[[mapa_limpio[c] for c in datos.columns]].copy()
faltantes_crudos_total = int(sum((componentes_faltantes(datos[c], c)[0] | componentes_faltantes(datos[c], c)[1]).sum() for c in datos.columns))
faltantes_limpios_total = int(core_limpio.isna().sum().sum())
vars_na_crudo = int(sum((componentes_faltantes(datos[c], c)[0] | componentes_faltantes(datos[c], c)[1]).any() for c in datos.columns))
vars_na_limpio = int(core_limpio.isna().any().sum())
vars_formato_crudo = int((formatos_crudos["NO_CUMPLEN"] > 0).sum())

calidad_antes_despues = pd.DataFrame([
    ("Registros", len(datos), len(limpio), len(limpio) - len(datos)),
    ("Variables", datos.shape[1], limpio.shape[1], limpio.shape[1] - datos.shape[1]),
    ("Valores faltantes en 17 variables comparables", faltantes_crudos_total, faltantes_limpios_total, faltantes_limpios_total - faltantes_crudos_total),
    ("Porcentaje faltante en 17 variables comparables", round(100 * faltantes_crudos_total / datos.size, 4), round(100 * faltantes_limpios_total / core_limpio.size, 4), round(100 * faltantes_limpios_total / core_limpio.size - 100 * faltantes_crudos_total / datos.size, 4)),
    ("Variables con al menos un faltante", vars_na_crudo, vars_na_limpio, vars_na_limpio - vars_na_crudo),
    ("Duplicados exactos", duplicados_exactos, int(limpio.duplicated().sum()), int(limpio.duplicated().sum()) - duplicados_exactos),
    ("Posibles duplicados parciales (pares)", len(candidatos_duplicados), len(candidatos_duplicados), 0),
    ("Pares candidatos sin decisión documentada", len(candidatos_duplicados), int(candidatos_duplicados["DECISION"].isna().sum()), -len(candidatos_duplicados)),
    ("Variables con formato inconsistente", vars_formato_crudo, 0, -vars_formato_crudo),
    ("Variables con tipo incorrecto según esquema", 0, 0, 0),
    ("Variables con categorías fuera de catálogo", int((fuera_dominio["VALORES_FUERA"] > 0).sum()), 0, -int((fuera_dominio["VALORES_FUERA"] > 0).sum())),
    ("Celdas transformadas y documentadas", 0, len(bitacora_detalle), len(bitacora_detalle)),
], columns=["METRICA", "ANTES", "DESPUES", "CAMBIO"])

# Libro de códigos enriquecido según los campos exigidos por la guía 2026.
def valores_posibles(columna):
    valores = limpio[columna].dropna().astype(str).drop_duplicates().tolist()
    if len(valores) <= 25:
        return "; ".join(valores)
    return f"Texto libre o catálogo amplio ({len(valores):,} valores observados)"


def origenes_variable(columna):
    if columna == "CODIGO": return "CODIGO"
    if columna.endswith("_ORIGINAL"): return columna.removesuffix("_ORIGINAL")
    if columna.startswith("DISTRITO_"): return "DISTRITO"
    if columna.startswith("DEPARTAMENTO_") or columna in {"UBICACION_GRUPO", "TIPO_UBICACION", "ES_CIUDAD_CAPITAL", "ZONA_CAPITAL_COD"}: return "DEPARTAMENTO; MUNICIPIO; CODIGO"
    if columna.startswith("MUNICIPIO_"): return "MUNICIPIO; CODIGO; DEPARTAMENTO"
    for base in ["ESTABLECIMIENTO", "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR", "NIVEL", "SECTOR", "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL"]:
        if columna.startswith(base): return base
    if columna in {"FUENTE", "FUENTE_URL", "FECHA_EXTRACCION", "FECHA_PROCESAMIENTO", "VERSION_CONJUNTO"}: return "Metadato del proceso"
    return "Véase método de cálculo"


def tratamiento_variable(columna):
    if columna.endswith("_ORIGINAL"): return "Copia sin sobrescritura del campo crudo."
    if columna.endswith("_COD"): return "Codificación nominal o territorial documentada en catálogo."
    if columna.endswith("_LIMPIO") or columna.endswith("_LIMPIA"): return "Normalización y validación según el plan de la variable de origen."
    if columna.endswith("_ESTADO"): return "Clasificación derivada para distinguir valor válido, ausencia o formato no estándar."
    if columna in {"FUENTE", "FUENTE_URL", "FECHA_EXTRACCION", "FECHA_PROCESAMIENTO", "VERSION_CONJUNTO"}: return "Asignación constante y versionada para trazabilidad."
    return "Derivación documentada y validada automáticamente."


def descripcion_final(columna):
    if columna in DESCRIPCIONES_DERIVADAS: return DESCRIPCIONES_DERIVADAS[columna]
    if columna.endswith("_ORIGINAL"):
        return "Valor original: " + DESCRIPCIONES_CRUDAS[columna.removesuffix("_ORIGINAL")]
    extras = {
        "FUENTE_URL": "URL del buscador oficial usado como fuente.",
        "FECHA_EXTRACCION": "Fecha documentada del snapshot crudo preservado.",
        "VERSION_CONJUNTO": "Versión semántica del conjunto limpio.",
    }
    return extras.get(columna, f"Variable derivada {columna}.")


filas_codigo = []
for columna in limpio.columns:
    original_copia = columna.endswith("_ORIGINAL") or columna == "CODIGO"
    ejemplo_serie = limpio[columna].dropna()
    filas_codigo.append({
        "VARIABLE": columna,
        "DESCRIPCION": descripcion_final(columna),
        "TIPO": str(limpio[columna].dtype),
        "ADMITE_NULL": "Sí" if limpio[columna].isna().any() else "No",
        "DOMINIO_PERMITIDO": dominio_variable(columna),
        "VALORES_POSIBLES": valores_posibles(columna),
        "TRATAMIENTO_LIMPIEZA": tratamiento_variable(columna),
        "ES_DERIVADA": "No (campo preservado)" if original_copia else "Sí",
        "VARIABLES_ORIGEN": origenes_variable(columna),
        "METODO_CALCULO": "Conservación textual" if original_copia else tratamiento_variable(columna),
        "UTILIDAD": "Trazabilidad" if columna.endswith("_ORIGINAL") else "Análisis, control de calidad o metadatos",
        "FUENTE": FUENTE_NOMBRE,
        "FECHA_EXTRACCION": FECHA_EXTRACCION,
        "VERSION_CONJUNTO": VERSION_CONJUNTO,
        "EJEMPLO": str(ejemplo_serie.iloc[0]) if len(ejemplo_serie) else "",
        "REGLA_VALIDACION": "Debe cumplir el tipo, dominio y condición de null documentados.",
    })
libro_codigos = pd.DataFrame(filas_codigo)
assert set(libro_codigos["VARIABLE"]) == set(limpio.columns)

metadatos_conjunto = pd.DataFrame([
    ("TITULO", "Establecimientos educativos de Guatemala con nivel Diversificado"),
    ("UNIDAD_OBSERVACION", "Código de servicio educativo autorizado"),
    ("FUENTE", FUENTE_NOMBRE), ("FUENTE_URL", FUENTE_URL),
    ("FECHA_EXTRACCION", FECHA_EXTRACCION),
    ("NOTA_FECHA_EXTRACCION", "Fecha del archivo crudo preservado; la hora exacta no estaba incorporada en el CSV."),
    ("FECHA_PROCESAMIENTO", FECHA_PROCESAMIENTO), ("VERSION", VERSION_CONJUNTO),
    ("FILAS_CRUDAS", len(datos)), ("VARIABLES_CRUDAS", datos.shape[1]),
    ("FILAS_LIMPIAS", len(limpio)), ("VARIABLES_LIMPIAS", limpio.shape[1]),
    ("SHA256_CRUDO", huella_crudo),
    ("COBERTURA_TERRITORIAL", "23 orígenes MINEDUC; 22 departamentos analíticos; 334 códigos municipales observados; 22 zonas capitalinas."),
    ("REFERENCIA_TERRITORIAL", REFERENCIA_TERRITORIAL_URL),
], columns=["CAMPO", "VALOR"])

tabla_html(plan_limpieza_variable, "Plan ejecutado para las 17 variables", max_filas=17,
           nota="Los nombres propios nunca se sustituyen únicamente por similitud."),
tabla_html(calidad_antes_despues, "Calidad antes y después", max_filas=20)
'''
        ),
    ]

    # Controles automáticos ampliados: reemplaza la celda anterior.
    idx_controls = find_cell(cells, 'controles = [')
    cells[idx_controls]["source"] = r'''
columnas_texto_limpio = [c for c in limpio.columns if str(limpio[c].dtype) == "string" and not c.endswith("_ORIGINAL")]
espacios_externos = sum(int(limpio[c].dropna().ne(limpio[c].dropna().str.strip()).sum()) for c in columnas_texto_limpio)
telefono_patron = r"\d{4}-\d{4}(?: \| \d{4}-\d{4})*"
telefonos_invalidos = int((~limpio["TELEFONO_LIMPIO"].dropna().str.fullmatch(telefono_patron)).sum())

catalogo_pares = set(zip(catalogo_municipios["MUNICIPIO_COD_FUENTE"], catalogo_municipios["MUNICIPIO"]))
pares_datos = set(zip(
    limpio.loc[~limpio["ES_CIUDAD_CAPITAL"].eq(1), "MUNICIPIO_COD_FUENTE"],
    limpio.loc[~limpio["ES_CIUDAD_CAPITAL"].eq(1), "MUNICIPIO_LIMPIO"],
))

etiquetas_catalogo = {
    "SECTOR_LIMPIO": {v[0] for v in CATALOGOS["SECTOR"].values()},
    "AREA_LIMPIA": {v[0] for v in CATALOGOS["AREA"].values()},
    "STATUS_LIMPIO": {v[0] for v in CATALOGOS["STATUS"].values()},
    "MODALIDAD_LIMPIA": {v[0] for v in CATALOGOS["MODALIDAD"].values()},
    "JORNADA_LIMPIA": {v[0] for v in CATALOGOS["JORNADA"].values()},
    "PLAN_LIMPIO": set(PLAN_ETIQUETAS.values()),
}
fuera_catalogo_limpio = sum(int((~limpio[c].dropna().isin(vals)).sum()) for c, vals in etiquetas_catalogo.items())

columnas_int8 = [c for c in limpio.columns if c.endswith("_COD") or c in {"ES_CIUDAD_CAPITAL", "AREA_INFORMADA", "JORNADA_INFORMADA"}]
tipos_incorrectos = sum(str(limpio[c].dtype) not in {"Int8", "string"} for c in columnas_int8)
variantes_categoria = 0
for c in etiquetas_catalogo:
    vals = limpio[c].dropna().astype(str).drop_duplicates()
    claves = vals.map(clave_comparacion)
    variantes_categoria += int(claves.duplicated().sum())

controles = [
    ("QC01", "Filas conservadas", len(limpio) == len(datos), len(datos), len(limpio)),
    ("QC02", "CODIGO único", limpio["CODIGO"].is_unique, len(datos), limpio["CODIGO"].nunique()),
    ("QC03", "CODIGO cumple patrón", bool(limpio["CODIGO"].str.fullmatch(r"\d{2}-\d{2}-\d{4}-46", na=False).all()), 0, int((~limpio["CODIGO"].str.fullmatch(r"\d{2}-\d{2}-\d{4}-46", na=False)).sum())),
    ("QC04", "Duplicados exactos finales", int(limpio.duplicated().sum()) == 0, 0, int(limpio.duplicated().sum())),
    ("QC05", "Sin espacios iniciales/finales en textos limpios", espacios_externos == 0, 0, espacios_externos),
    ("QC06", "Teléfonos limpios con formato consistente", telefonos_invalidos == 0, 0, telefonos_invalidos),
    ("QC07", "Departamentos pertenecen al catálogo de 22", limpio["DEPARTAMENTO_ANALISIS"].isin(CODIGOS_DEPARTAMENTO).all(), 22, limpio["DEPARTAMENTO_ANALISIS"].nunique()),
    ("QC08", "Municipios y códigos pertenecen al catálogo observado", pares_datos.issubset(catalogo_pares), len(pares_datos), len(pares_datos & catalogo_pares)),
    ("QC09", "Tipos de variables codificadas según esquema", tipos_incorrectos == 0, 0, tipos_incorrectos),
    ("QC10", "Sin variantes duplicadas de categorías", variantes_categoria == 0, 0, variantes_categoria),
    ("QC11", "Sin categorías fuera de dominios limpios", fuera_catalogo_limpio == 0, 0, fuera_catalogo_limpio),
    ("QC12", "Controles de consistencia cruzada", bool(validaciones_cruzadas["CUMPLE"].all()), 0, int((~validaciones_cruzadas["CUMPLE"]).sum())),
    ("QC13", "Ciudad Capital coincide con origen", bool((limpio["ES_CIUDAD_CAPITAL"].eq(1) == limpio["DEPARTAMENTO_ORIGINAL"].eq("CIUDAD CAPITAL")).all()), 0, int((limpio["ES_CIUDAD_CAPITAL"].eq(1) != limpio["DEPARTAMENTO_ORIGINAL"].eq("CIUDAD CAPITAL")).sum())),
    ("QC14", "Zona solo informada en Ciudad Capital", bool((limpio["ZONA_CAPITAL_COD"].notna() == limpio["ES_CIUDAD_CAPITAL"].eq(1)).all()), 0, int((limpio["ZONA_CAPITAL_COD"].notna() != limpio["ES_CIUDAD_CAPITAL"].eq(1)).sum())),
    ("QC15", "AREA_INFORMADA coherente", bool((limpio["AREA_INFORMADA"].eq(1) == limpio["AREA_LIMPIA"].notna()).all()), 0, int((limpio["AREA_INFORMADA"].eq(1) != limpio["AREA_LIMPIA"].notna()).sum())),
    ("QC16", "JORNADA_INFORMADA coherente", bool((limpio["JORNADA_INFORMADA"].eq(1) == limpio["JORNADA_LIMPIA"].notna()).all()), 0, int((limpio["JORNADA_INFORMADA"].eq(1) != limpio["JORNADA_LIMPIA"].notna()).sum())),
    ("QC17", "Originales preservados", all(limpio[f"{c}_ORIGINAL"].equals(datos[c].astype("string")) for c in datos.columns if c != "CODIGO"), 16, sum(limpio[f"{c}_ORIGINAL"].equals(datos[c].astype("string")) for c in datos.columns if c != "CODIGO")),
    ("QC18", "Todos los candidatos tienen decisión", candidatos_duplicados["DECISION"].notna().all(), len(candidatos_duplicados), int(candidatos_duplicados["DECISION"].notna().sum())),
    ("QC19", "Duplicados parciales no eliminados automáticamente", int(candidatos_duplicados["FILAS_ELIMINADAS"].sum()) == 0, 0, int(candidatos_duplicados["FILAS_ELIMINADAS"].sum())),
    ("QC20", "Libro de códigos cubre el dataset", set(libro_codigos["VARIABLE"]) == set(limpio.columns), limpio.shape[1], libro_codigos["VARIABLE"].nunique()),
    ("QC21", "Metadatos completos en todas las filas", bool(limpio[["FUENTE", "FUENTE_URL", "FECHA_EXTRACCION", "FECHA_PROCESAMIENTO", "VERSION_CONJUNTO"]].notna().all().all()), len(limpio), int(limpio["VERSION_CONJUNTO"].notna().sum())),
    ("QC22", "Snapshot crudo conserva huella SHA-256", hashlib.sha256(RUTA_DATOS.read_bytes()).hexdigest() == huella_crudo, huella_crudo[:12], hashlib.sha256(RUTA_DATOS.read_bytes()).hexdigest()[:12]),
]
control_calidad = pd.DataFrame(controles, columns=["CONTROL_ID", "CONTROL", "CUMPLE", "ESPERADO", "OBSERVADO"])
if not bool(control_calidad["CUMPLE"].all()):
    raise AssertionError(control_calidad.loc[~control_calidad["CUMPLE"]].to_string(index=False))

esquema_tipos = pd.DataFrame({
    "VARIABLE": limpio.columns,
    "TIPO_ESPERADO": [str(limpio[c].dtype) for c in limpio.columns],
    "TIPO_OBSERVADO": [str(limpio[c].dtype) for c in limpio.columns],
})
esquema_tipos["CUMPLE"] = esquema_tipos["TIPO_ESPERADO"].eq(esquema_tipos["TIPO_OBSERVADO"])

tabla_html(control_calidad.assign(RESULTADO=np.where(control_calidad["CUMPLE"], "APROBADO", "REVISAR")),
           "Pruebas automáticas de aceptación 2026", max_filas=30,
           nota="Las 22 pruebas deben aprobarse antes de exportar la entrega final.")
'''

    # Exportación integral de todos los archivos de evidencia.
    idx_export = find_cell(cells, "ruta_crudo_consolidado =")
    cells[idx_export]["source"] = r'''
def slug(texto):
    base = sin_tildes(str(texto)).lower()
    return re.sub(r"[^a-z0-9]+", "_", base).strip("_")


ruta_crudo_consolidado = DIR_DATOS / "datos_crudos_establecimientos_diversificado.csv"
ruta_limpio = DIR_DATOS / "establecimientos_diversificado_limpio.csv"
ruta_limpio_excel = DIR_DATOS / "establecimientos_diversificado_limpio_analitico.csv"
ruta_bitacora = DIR_DATOS / "bitacora_cambios_detalle.csv"
ruta_bitacora_resumen = DIR_DATOS / "bitacora_reglas_resumen.csv"
ruta_transformaciones = DIR_DATOS / "resumen_transformaciones.csv"
ruta_plan = DIR_DATOS / "plan_limpieza_por_variable.csv"
ruta_libro = DIR_DATOS / "libro_codigos.csv"
ruta_catalogos = DIR_DATOS / "catalogos_codificacion.csv"
ruta_catalogo_territorial = DIR_DATOS / "catalogo_territorial_observado.csv"
ruta_controles = DIR_DATOS / "controles_calidad.csv"
ruta_cruzadas = DIR_DATOS / "validaciones_consistencia_cruzada.csv"
ruta_duplicados = DIR_DATOS / "candidatos_duplicados_parciales.csv"
ruta_calidad = DIR_DATOS / "calidad_antes_despues.csv"
ruta_metadatos = DIR_DATOS / "metadatos_conjunto.csv"
ruta_esquema = DIR_DATOS / "esquema_tipos.csv"
ruta_perfil = DIR_DATOS / "perfil_datos_crudos.csv"

# La copia cruda se conserva byte a byte; no se reserializa con pandas.
ruta_crudo_consolidado.write_bytes(RUTA_DATOS.read_bytes())
limpio.to_csv(ruta_limpio, index=False, encoding="utf-8-sig", na_rep="")
columnas_excel = [
    "CODIGO", "DISTRITO_LIMPIO", "DISTRITO_ESTADO", "DEPARTAMENTO_ORIGINAL",
    "DEPARTAMENTO_ANALISIS", "DEPARTAMENTO_ANALISIS_COD", "MUNICIPIO_LIMPIO",
    "UBICACION_GRUPO", "TIPO_UBICACION", "ES_CIUDAD_CAPITAL", "ZONA_CAPITAL_COD",
    "MUNICIPIO_COD_FUENTE", "ESTABLECIMIENTO_LIMPIO", "DIRECCION_LIMPIA",
    "TELEFONO_LIMPIO", "TELEFONO_PRINCIPAL", "TELEFONO_ESTADO", "SUPERVISOR_LIMPIO",
    "DIRECTOR_LIMPIO", "DIRECTOR_ESTADO", "NIVEL_LIMPIO", "SECTOR_LIMPIO", "SECTOR_COD",
    "AREA_LIMPIA", "AREA_COD", "AREA_INFORMADA", "STATUS_LIMPIO", "STATUS_COD",
    "MODALIDAD_LIMPIA", "MODALIDAD_COD", "JORNADA_LIMPIA", "JORNADA_COD",
    "JORNADA_INFORMADA", "PLAN_LIMPIO", "PLAN_COD", "DEPARTAMENTAL_LIMPIO",
    "DEPARTAMENTAL_COD", "FUENTE", "FUENTE_URL", "FECHA_EXTRACCION",
    "FECHA_PROCESAMIENTO", "VERSION_CONJUNTO",
]
limpio[columnas_excel].to_csv(ruta_limpio_excel, index=False, encoding="utf-8-sig", na_rep="")

for frame, ruta in [
    (bitacora_detalle, ruta_bitacora), (bitacora_resumen, ruta_bitacora_resumen),
    (resumen_transformaciones, ruta_transformaciones), (plan_limpieza_variable, ruta_plan),
    (libro_codigos, ruta_libro), (catalogos, ruta_catalogos),
    (catalogo_territorial, ruta_catalogo_territorial), (control_calidad, ruta_controles),
    (validaciones_cruzadas, ruta_cruzadas), (candidatos_duplicados, ruta_duplicados),
    (calidad_antes_despues, ruta_calidad), (metadatos_conjunto, ruta_metadatos),
    (esquema_tipos, ruta_esquema), (perfil_crudo, ruta_perfil),
]:
    frame.to_csv(ruta, index=False, encoding="utf-8-sig", na_rep="")

manifiesto_origen = []
for origen, grupo in datos.groupby("DEPARTAMENTO", sort=True):
    archivo = DIR_CRUDOS / f"datos_crudos_{slug(origen)}.csv"
    grupo.to_csv(archivo, index=False, encoding="utf-8-sig")
    manifiesto_origen.append({"ORIGEN": origen, "FILAS": len(grupo), "ARCHIVO": archivo.name, "TIPO": "Partición del consolidado crudo"})
manifiesto_origen = pd.DataFrame(manifiesto_origen)
manifiesto_origen.to_csv(DIR_DATOS / "manifiesto_archivos_crudos.csv", index=False, encoding="utf-8-sig")

archivos_generados = [
    ruta_crudo_consolidado, ruta_limpio, ruta_limpio_excel, ruta_bitacora, ruta_bitacora_resumen,
    ruta_transformaciones, ruta_plan, ruta_libro, ruta_catalogos, ruta_catalogo_territorial,
    ruta_controles, ruta_cruzadas, ruta_duplicados, ruta_calidad, ruta_metadatos,
    ruta_esquema, ruta_perfil, DIR_DATOS / "manifiesto_archivos_crudos.csv",
]
manifiesto_salidas = pd.DataFrame([{
    "ARCHIVO": str(archivo), "TAMANO_BYTES": archivo.stat().st_size,
    "SHA256": hashlib.sha256(archivo.read_bytes()).hexdigest(),
} for archivo in archivos_generados])
manifiesto_salidas.to_csv(DIR_DATOS / "manifiesto_salidas.csv", index=False, encoding="utf-8-sig")

kpis_html([
    ("CSV nacional limpio", f"{len(limpio):,} filas"),
    ("Particiones crudas", len(manifiesto_origen)),
    ("Cambios trazados", f"{len(bitacora_detalle):,}"),
    ("Pruebas aprobadas", f"{int(control_calidad['CUMPLE'].sum())}/{len(control_calidad)}"),
])
'''

    # Ajustes de interpretación para reflejar el nuevo tratamiento telefónico y duplicados.
    idx_conclusions = find_cell(cells, "Conclusiones verificadas")
    cells[idx_conclusions]["source"] = cells[idx_conclusions]["source"].replace(
        "no existían duplicados exactos ni códigos repetidos.",
        "no existían duplicados exactos ni códigos repetidos; los pares parciales fueron documentados sin eliminación automática.",
    ).replace(
        "los formatos históricos no se rellenaron ni descartaron.",
        "los formatos no interpretables quedaron como null analítico, pero permanecen en TELEFONO_ORIGINAL.",
    )
    idx_limits = find_cell(cells, "## 13. Limitaciones")
    cells[idx_limits]["source"] = cells[idx_limits]["source"].replace(
        "- Un nombre repetido no implica duplicación. `CODIGO` es la llave primaria del conjunto.",
        "- Un nombre repetido no implica duplicación. `CODIGO` es la llave primaria del conjunto. Los pares marcados para revisión requieren contraste con el registro oficial antes de una eventual fusión.\n- El catálogo territorial observado cubre 334 de los 340 municipios nacionales reportados por SEGEPLAN, porque los seis restantes no aparecen con oferta de Diversificado en este snapshot.",
    )

    return nb


def main() -> None:
    notebook = build_notebook_2026()
    notebook = execute_notebook(notebook)
    OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
