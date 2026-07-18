from __future__ import annotations

import ast
import base64
import contextlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "upload" / "Avance_Proyecto_1_MINEDUC(2).ipynb"
OUTPUT = ROOT / "Avance_Proyecto_1_MINEDUC_Actualizado.ipynb"


def md(text: str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.strip() + "\n",
    }


def code(text: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.strip() + "\n",
    }


def source_text(cell) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def find_cell(cells, *, startswith: str | None = None, contains: str | None = None):
    for index, cell in enumerate(cells):
        source = source_text(cell)
        if startswith is not None and source.lstrip().startswith(startswith):
            return index
        if contains is not None and contains in source:
            return index
    raise ValueError(f"No se encontró la celda: startswith={startswith!r}, contains={contains!r}")


def build_notebook():
    nb = json.loads(SOURCE.read_text(encoding="utf-8"))
    cells = nb["cells"]
    for cell in cells:
        cell["source"] = source_text(cell)

    cells[0]["source"] = """
<div style="padding:30px 34px;border-radius:18px;background:linear-gradient(135deg,#123b6d 0%,#2563a8 64%,#2e8b8b 100%);color:white;box-shadow:0 10px 28px rgba(18,59,109,.20);">
  <p style="margin:0 0 8px;font-size:13px;letter-spacing:1.2px;text-transform:uppercase;opacity:.88;">Universidad del Valle de Guatemala · CC3066 Data Science</p>
  <h1 style="margin:0;font-size:32px;">Avance del Proyecto 1</h1>
  <h2 style="margin:8px 0 20px;font-size:21px;font-weight:500;">Obtención y limpieza de datos de establecimientos educativos</h2>
  <div style="padding:14px 16px;border-radius:10px;background:rgba(255,255,255,.12);line-height:1.55;font-size:14px;">
    <b>Integrantes:</b><br>
    Abby Sofia Donis Agreda — 22440 · Pablo Daniel Barillas Moreno — 22193<br>
    Jorge Palacios — 231385 · Roberto Emiliano Otoniel Camposeco Torres — 23968
  </div>
  <p style="margin:16px 0 0;opacity:.92;">Diagnóstico de datos crudos del nivel Diversificado · 14 de julio de 2026</p>
</div>
""".strip()

    cells[1]["source"] = """
## 1. Fuente, alcance y criterio de extracción

Los registros provienen del [buscador oficial de centros educativos autorizados del MINEDUC](https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/). Se consultó el filtro **Nivel Escolar = Diversificado** para las 23 opciones geográficas que ofrece el portal: los 22 departamentos, con **Ciudad Capital** presentada como una categoría de extracción separada de **Guatemala**.

La extracción se realizó el **10 de julio de 2026**. La consulta general de Ciudad Capital reportó 2,161 resultados, pero la tabla solo mostró 2,000; por ello se consultaron individualmente las 22 zonas disponibles y se unieron los códigos obtenidos. La suma final fue validada contra el total informado por el portal.

### Unidad de observación

Cada fila representa un **código de servicio educativo autorizado** en el nivel Diversificado. No necesariamente representa un edificio físico distinto: un centro puede contar con más de un código según nivel, plan, modalidad o jornada. Por esa razón, compartir nombre o dirección no basta para eliminar un registro como duplicado.
""".strip()

    load_index = find_cell(cells, contains="candidatos = [")
    cells[load_index]["source"] = cells[load_index]["source"].replace(
        'Path("datos_crudos_establecimientos_diversificado.csv"),',
        'Path("datos_crudos_establecimientos_diversificado.csv"),\n'
        '    Path("datos_crudos_establecimientos_diversificado(1).csv"),\n'
        '    Path("upload/datos_crudos_establecimientos_diversificado(1).csv"),',
    ).replace("extracapitalión", "extracción")

    # Retirar la exploración agregada de forma aislada y sustituirla por una
    # sección integrada, reproducible y con una decisión metodológica explícita.
    exploration_start = find_cell(cells, startswith="# EXPLORACION UNIFICACION DATOS")
    validation_start = find_cell(cells, startswith="## 6. Validación de formatos")
    del cells[exploration_start:validation_start]

    geographic_insert = find_cell(cells, startswith="## 5. Perfil de calidad")
    territorial_cells = [
        md("""
### 4.1 Ciudad Capital y Guatemala: revisión para la unión nacional

El portal separa **Ciudad Capital** de **Guatemala**, aunque ambas categorías pertenecen al mismo departamento administrativo cuando se elaboran resúmenes nacionales por 22 departamentos. Antes de definir una regla de integración se revisan tamaños, granularidad territorial, prefijos de código y posibles solapamientos. Esta comprobación evita dos errores opuestos: duplicar registros o borrar la procedencia original.
"""),
        code("""
capital = datos.loc[datos["DEPARTAMENTO"].eq("CIUDAD CAPITAL")].copy()
guatemala = datos.loc[datos["DEPARTAMENTO"].eq("GUATEMALA")].copy()

def resumen_categoria_territorial(nombre, bloque, tipo_ubicacion):
    return {
        "CATEGORIA_ORIGEN": nombre,
        "FILAS": len(bloque),
        "PORC_TOTAL": round(100 * len(bloque) / len(datos), 2),
        "CODIGOS_UNICOS": bloque["CODIGO"].nunique(),
        "UBICACIONES_UNICAS": bloque["MUNICIPIO"].nunique(),
        "TIPO_UBICACION": tipo_ubicacion,
        "PREFIJOS_CODIGO": ", ".join(sorted(bloque["CODIGO"].str[:2].unique())),
    }

resumen_territorial = pd.DataFrame(
    [
        resumen_categoria_territorial("CIUDAD CAPITAL", capital, "ZONA"),
        resumen_categoria_territorial("GUATEMALA", guatemala, "MUNICIPIO"),
    ]
)

zonas_capital = capital["MUNICIPIO"].str.fullmatch(r"ZONA\\s+\\d+", na=False)
zonas_en_guatemala = guatemala["MUNICIPIO"].str.fullmatch(r"ZONA\\s+\\d+", na=False)
codigos_compartidos = set(capital["CODIGO"]) & set(guatemala["CODIGO"])
ubicaciones_compartidas = set(capital["MUNICIPIO"]) & set(guatemala["MUNICIPIO"])
departamento_analisis_propuesto = datos["DEPARTAMENTO"].replace(
    {"CIUDAD CAPITAL": "GUATEMALA"}
)

assert len(capital) == 2161 and len(guatemala) == 1644
assert capital["CODIGO"].nunique() == len(capital)
assert guatemala["CODIGO"].nunique() == len(guatemala)
assert zonas_capital.all() and capital["MUNICIPIO"].nunique() == 22
assert not zonas_en_guatemala.any() and guatemala["MUNICIPIO"].nunique() == 15
assert not codigos_compartidos and not ubicaciones_compartidas
assert departamento_analisis_propuesto.nunique() == 22

resumen_territorial
"""),
        code("""
comparaciones = []
for variable in ["SECTOR", "AREA", "JORNADA"]:
    conteos = pd.crosstab(
        datos.loc[datos["DEPARTAMENTO"].isin(["CIUDAD CAPITAL", "GUATEMALA"]), variable],
        datos.loc[datos["DEPARTAMENTO"].isin(["CIUDAD CAPITAL", "GUATEMALA"]), "DEPARTAMENTO"],
    )
    porcentajes = conteos.div(conteos.sum(axis=0), axis=1).mul(100)
    for valor in conteos.index:
        comparaciones.append(
            {
                "VARIABLE": variable,
                "VALOR": valor,
                "CAPITAL_FILAS": int(conteos.loc[valor, "CIUDAD CAPITAL"]),
                "CAPITAL_PORC": round(porcentajes.loc[valor, "CIUDAD CAPITAL"], 2),
                "GUATEMALA_FILAS": int(conteos.loc[valor, "GUATEMALA"]),
                "GUATEMALA_PORC": round(porcentajes.loc[valor, "GUATEMALA"], 2),
            }
        )

comparacion_territorial = pd.DataFrame(comparaciones)
comparacion_territorial
"""),
        code("""
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle(
    "Ciudad Capital y Guatemala: volumen y composición",
    fontsize=16,
    fontweight="bold",
    x=0.05,
    ha="left",
)

axes[0, 0].bar(
    ["Ciudad Capital", "Guatemala"],
    [len(capital), len(guatemala)],
    color=[CELESTE, NARANJA],
)
axes[0, 0].set_title("Registros por categoría de origen", loc="left", weight="bold")
axes[0, 0].set_ylabel("Filas")
for i, valor in enumerate([len(capital), len(guatemala)]):
    axes[0, 0].text(i, valor + 35, f"{valor:,}", ha="center", weight="bold")

for ax, variable, titulo in [
    (axes[0, 1], "SECTOR", "Composición por sector"),
    (axes[1, 0], "AREA", "Composición por área"),
    (axes[1, 1], "JORNADA", "Composición por jornada"),
]:
    tabla = pd.crosstab(
        datos.loc[datos["DEPARTAMENTO"].isin(["CIUDAD CAPITAL", "GUATEMALA"]), variable],
        datos.loc[datos["DEPARTAMENTO"].isin(["CIUDAD CAPITAL", "GUATEMALA"]), "DEPARTAMENTO"],
        normalize="columns",
    ).mul(100)
    tabla.plot(kind="bar", ax=ax, color=[CELESTE, NARANJA], width=0.8)
    ax.set_title(titulo, loc="left", weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Porcentaje dentro de la categoría")
    ax.tick_params(axis="x", rotation=35)
    ax.grid(axis="y", alpha=0.2)
    ax.legend(title="Origen", frameon=False)

for ax in axes.flat:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.18)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
"""),
        md("""
#### Interpretación y decisión

- **No son bloques duplicados.** Ciudad Capital y Guatemala no comparten códigos; además, sus prefijos son `00` y `01`, respectivamente.
- **La granularidad es diferente.** En Ciudad Capital, los 22 valores de `MUNICIPIO` son rótulos de zona; en Guatemala se observan 15 municipios y ninguno tiene formato de zona.
- **Las distribuciones no son equivalentes.** Por ejemplo, Ciudad Capital es 99.40 % urbana y 93.20 % privada, mientras Guatemala es 80.05 % urbana y 87.90 % privada. Estas diferencias refuerzan la necesidad de conservar la procedencia.
- **La unión física conserva todas las filas.** No se elimina ni se agrega un registro por esta decisión.
- **La agregación territorial utiliza una variable derivada.** `DEPARTAMENTO_ORIGINAL` conservará las 23 categorías del portal; `DEPARTAMENTO_ANALISIS` mapeará Ciudad Capital a Guatemala únicamente cuando se necesite resumir los 22 departamentos administrativos.
"""),
        code("""
reglas_territoriales = pd.DataFrame(
    [
        {
            "CAMPO_PROPUESTO": "DEPARTAMENTO_ORIGINAL",
            "REGLA": "Conservar exactamente la categoría publicada por el portal.",
            "RAZON": "Mantiene procedencia y permite reproducir la extracción.",
        },
        {
            "CAMPO_PROPUESTO": "DEPARTAMENTO_ANALISIS",
            "REGLA": "Mapear CIUDAD CAPITAL a Guatemala; conservar los otros departamentos.",
            "RAZON": "Produce 22 categorías para agregación administrativa sin sobrescribir el origen.",
        },
        {
            "CAMPO_PROPUESTO": "UBICACION_ORIGINAL",
            "REGLA": "Conservar el valor original de MUNICIPIO.",
            "RAZON": "Protege los 22 rótulos de zona y los municipios publicados.",
        },
        {
            "CAMPO_PROPUESTO": "TIPO_UBICACION",
            "REGLA": "Asignar ZONA a Ciudad Capital y MUNICIPIO a las demás categorías.",
            "RAZON": "Evita comparar zonas con municipios como si tuvieran la misma granularidad.",
        },
        {
            "CAMPO_PROPUESTO": "ZONA_CAPITAL",
            "REGLA": "Copiar el rótulo de zona solo para Ciudad Capital; dejar nulo en otras filas.",
            "RAZON": "Permite análisis submunicipal sin contaminar el campo de municipio.",
        },
    ]
)
reglas_territoriales
"""),
    ]
    cells[geographic_insert:geographic_insert] = territorial_cells

    priority_index = find_cell(cells, contains="metricas_var = variantes_resumen")
    cells[priority_index]["source"] = """
metricas_var = variantes_resumen.set_index("VARIABLE").to_dict("index")
faltantes_por_variable = perfil.set_index("VARIABLE")["FALTANTES_EFECTIVOS"].to_dict()

telefonos_no_estandar = int(
    (telefono_solo_digitos & ~telefono_8_digitos).sum()
    + (~telefono_vacio & ~telefono_solo_digitos).sum()
)
distritos_invalidos = int((~distrito_valido).sum())

prioridades = pd.DataFrame(
    [
        (1, "ESTABLECIMIENTO", f"{faltantes_por_variable['ESTABLECIMIENTO']:,} vacíos y {metricas_var['ESTABLECIMIENTO']['GRUPOS_CANDIDATOS']:,} grupos candidatos que afectan {metricas_var['ESTABLECIMIENTO']['FILAS_AFECTADAS']:,} filas.", "Es la variable central y debe conservar ortografía, tildes, ñ, siglas y nombres propios."),
        (2, "DIRECTOR", f"{faltantes_por_variable['DIRECTOR']:,} faltantes efectivos y {metricas_var['DIRECTOR']['GRUPOS_CANDIDATOS']:,} grupos candidatos.", "Combina vacíos, marcadores y diferencias de escritura de nombres de personas."),
        (3, "DIRECCION", f"{faltantes_por_variable['DIRECCION']:,} faltantes efectivos y {metricas_var['DIRECCION']['GRUPOS_CANDIDATOS']:,} grupos candidatos.", "Presenta abreviaturas, signos y formas distintas de expresar una ubicación."),
        (4, "TELEFONO", f"{faltantes_por_variable['TELEFONO']:,} vacíos y {telefonos_no_estandar:,} valores no escritos como un único número de 8 dígitos.", "Puede contener separadores, varios contactos o longitudes antiguas/incompletas."),
        (5, "SUPERVISOR", f"{faltantes_por_variable['SUPERVISOR']:,} vacíos y {metricas_var['SUPERVISOR']['GRUPOS_CANDIDATOS']:,} grupos candidatos.", "Los nombres requieren revisión de tildes sin fusionar homónimos."),
        (6, "DISTRITO", f"{distritos_invalidos:,} valores vacíos o incompletos.", "No es seguro completar el distrito sin verificación oficial."),
        (7, "DEPARTAMENTO", "23 categorías de origen, pero 22 departamentos para agregación; Ciudad Capital y Guatemala suman 3,805 filas.", "Requiere conservar el origen y crear una variable derivada para análisis territorial."),
        (8, "MUNICIPIO", "350 valores: Ciudad Capital aporta 22 zonas y Guatemala 15 municipios, sin rótulos compartidos.", "Mezcla dos granularidades geográficas que deben distinguirse explícitamente."),
        (9, "JORNADA", f"{faltantes_por_variable['JORNADA']:,} filas registradas como SIN JORNADA.", "Debe conservarse como categoría conocida y separarse de un nulo técnico."),
    ],
    columns=["PRIORIDAD", "VARIABLE", "EVIDENCIA", "MOTIVO"],
)

prioridades
""".strip()

    strategy_index = find_cell(cells, startswith="## 10. Estrategia propuesta")
    cells[strategy_index]["source"] = """
## 10. Estrategia propuesta de limpieza

### 10.1 Principios generales

1. **Conservar los datos crudos sin alterarlos.** Las columnas limpias se crearán aparte o se trabajará sobre una copia.
2. **No eliminar tildes, diéresis ni la letra ñ.** Se aplicará normalización Unicode NFC, que corrige la representación informática sin borrar reglas ortográficas.
3. **Usar claves auxiliares solo para comparar.** Una versión en mayúsculas y sin signos puede servir para detectar candidatos, pero nunca será el texto final de informes.
4. **Documentar las correcciones.** Se mantendrá un diccionario `valor_crudo → valor_corregido`, junto con la razón y el número de filas afectadas.
5. **No imputar información desconocida.** Los vacíos y marcadores se representarán uniformemente como faltantes; no se inventarán nombres, teléfonos, distritos ni direcciones.
6. **Separar procedencia y variables analíticas.** La categoría geográfica original nunca se sobrescribirá con una agrupación derivada.
7. **Medir cada cambio.** Antes y después de cada operación se registrarán filas, valores únicos, faltantes y códigos duplicados.

### 10.2 Estrategia para `ESTABLECIMIENTO`

1. Conservar `ESTABLECIMIENTO_ORIGINAL` exactamente como fue descargado.
2. Crear `ESTABLECIMIENTO_LIMPIO` para la versión destinada a informes.
3. Aplicar Unicode NFC y eliminar únicamente espacios al inicio/final o espacios internos repetidos.
4. Estandarizar con cuidado comillas, puntos y guiones alrededor de siglas como `INED`, `INEB`, `CEEX` e `IGER`.
5. Detectar variantes que solo cambian por tildes o puntuación, por ejemplo `EDUCACION`/`EDUCACIÓN`.
6. Elegir la variante ortográficamente correcta mediante un diccionario documentado; nunca quitar tildes para forzar coincidencias.
7. Respetar siglas, números romanos, apellidos y nombres propios; no aplicar `.title()` de forma ciega.
8. Usar similitud difusa únicamente para producir una lista de candidatos.
9. Revisar manualmente coincidencias dudosas antes de reemplazar.
10. No eliminar filas por compartir nombre: se verificará `CODIGO`, municipio, dirección, jornada y plan.

### 10.3 `DIRECTOR` y `SUPERVISOR`

- Convertir vacíos, secuencias de guiones y `SIN DATO` a una representación uniforme de faltante en la copia limpia.
- Conservar el texto original y corregir tildes únicamente con reglas verificables.
- Comparar nombres con una clave auxiliar, sin usarla como nombre de presentación.
- No fusionar personas solo porque el nombre sea parecido; puede haber homónimos.

### 10.4 `DIRECCION`

- Normalizar Unicode, espacios y puntuación básica.
- Elaborar reglas consistentes para abreviaturas (`AV.`, `AVENIDA`, `CALLE`, `KM`) sin borrar información.
- Mantener números, zonas, aldeas, colonias y referencias.
- Marcar direcciones vacías o compuestas únicamente por signos como faltantes.
- Revisar direcciones similares dentro de la misma ubicación para detectar variantes, no para eliminarlas automáticamente.

### 10.5 `TELEFONO`

- Mantenerlo como texto para conservar ceros iniciales.
- Separar los casos que contienen varios teléfonos usando guiones, comas, espacios o `/`.
- Validar cada candidato contra el formato guatemalteco actual de 8 dígitos.
- No completar ni rellenar números antiguos o cortos sin una fuente de verificación.
- Conservar el valor original y crear un campo limpio; si existen varios números, usar una lista o una tabla secundaria.

### 10.6 `CODIGO` y `DISTRITO`

- Usar `CODIGO` como llave del registro porque los 11,603 valores son únicos y pasan el patrón esperado.
- Mantener ambos campos como texto.
- Validar `DISTRITO` con los formatos observados y convertir vacíos/incompletos en faltantes estandarizados.
- No deducir el distrito automáticamente desde `CODIGO` sin contrastarlo con información oficial.

### 10.7 Variables geográficas y categóricas

- Conservar `DEPARTAMENTO_ORIGINAL` con las 23 categorías del portal.
- Crear `DEPARTAMENTO_ANALISIS`, mapeando Ciudad Capital a Guatemala únicamente para resúmenes por los 22 departamentos.
- Conservar las 22 zonas de Ciudad Capital y añadir `TIPO_UBICACION`; no tratarlas como municipios.
- Validar los municipios y topónimos contra un catálogo oficial versionado antes de corregir tildes.
- Crear catálogos permitidos para sector, área, estado, modalidad, jornada y plan.
- Corregir ortografía de presentación con mapeos explícitos: por ejemplo `PETEN → Petén`, `QUICHE → Quiché` y `SOLOLA → Sololá`.
- Conservar `SIN JORNADA` y `SIN ESPECIFICAR` como categorías informativas diferenciadas de un vacío técnico.

### 10.8 Matriz resumida del plan por variable

La tabla siguiente resume el problema, la regla, la justificación y el principal riesgo para las 17 variables. El documento formal desarrolla cada caso con mayor detalle y controles específicos.
""".strip()

    plan_index = strategy_index + 1
    cells.insert(
        plan_index,
        code("""
plan_por_variable = pd.DataFrame(
    [
        ("CODIGO", "Riesgo de conversión o alteración futura.", "Conservar como texto y validar el patrón; usarlo como llave.", "Protege ceros, guiones y unicidad.", "Rechazar un código legítimo por una regla demasiado rígida."),
        ("DISTRITO", "522 vacíos y 69 valores incompletos.", "Separar original, limpio y estado; no completar sin fuente.", "Distingue vacío, incompleto y válido sin inventar datos.", "Perder el prefijo parcial o imputar un distrito incorrecto."),
        ("DEPARTAMENTO", "23 categorías de origen frente a 22 departamentos analíticos.", "Conservar origen y crear DEPARTAMENTO_ANALISIS.", "Mantiene procedencia y permite agregación administrativa.", "Sobrescribir Ciudad Capital o contarla dos veces."),
        ("MUNICIPIO", "Mezcla municipios y 22 zonas capitalinas.", "Conservar original, crear TIPO_UBICACION y validar con catálogo.", "Evita comparar granularidades distintas.", "Confundir una zona con un municipio o corregir mal un topónimo."),
        ("ESTABLECIMIENTO", "Vacíos y variantes de tildes, signos y siglas.", "Unicode NFC, espacios controlados, clave auxiliar y diccionario revisado.", "Detecta candidatos sin destruir la ortografía final.", "Fusionar instituciones distintas o eliminar tildes."),
        ("DIRECCION", "Abreviaturas, signos, vacíos y texto libre.", "Conservar original; normalizar espacios y abreviaturas aprobadas.", "Corrige aspectos mecánicos de forma reversible.", "Eliminar referencias o uniformar direcciones distintas."),
        ("TELEFONO", "Vacíos, varios contactos y formatos no estándar.", "Clasificar, extraer candidatos y validar cadenas de 8 dígitos.", "Preserva números adicionales y ceros iniciales.", "Inventar dígitos o perder contactos secundarios."),
        ("SUPERVISOR", "Vacíos y variantes de nombres.", "Unicode NFC, espacios y diccionario verificado.", "Normaliza escritura sin asumir identidad personal.", "Fusionar homónimos o aplicar una tilde incorrecta."),
        ("DIRECTOR", "Mayor cantidad de faltantes efectivos y marcadores.", "Uniformar nulos en copia limpia y conservar estado/original.", "Mejora completitud sin imputación injustificada.", "Asignar una persona incorrecta o perder el marcador original."),
        ("NIVEL", "No hay error actual; riesgo al integrar nuevos archivos.", "Validar dominio exclusivo DIVERSIFICADO.", "Protege el alcance del proyecto.", "Aceptar accidentalmente otro nivel."),
        ("SECTOR", "Dominio válido con presentación en mayúsculas.", "Validar cuatro categorías y mapear solo el rótulo.", "El catálogo pequeño permite control determinista.", "Reclasificar un sector legítimo."),
        ("AREA", "SIN ESPECIFICAR es ausencia semántica.", "Conservar categoría y crear indicador AREA_INFORMADA.", "Distingue categoría informativa de nulo técnico.", "Borrar el significado al convertirla silenciosamente en nulo."),
        ("STATUS", "Estados válidos; TEMPORAL TITULOS requiere tilde.", "Conservar todos los estados y corregir solo presentación.", "Evita sesgar el universo eliminando cierres.", "Filtrar registros durante la limpieza."),
        ("MODALIDAD", "Rótulos sin diéresis.", "Mapeo exacto a Monolingüe y Bilingüe.", "Corrección determinista y reversible.", "Confundir ortografía con reclasificación."),
        ("JORNADA", "1,072 valores SIN JORNADA.", "Conservar categoría y crear JORNADA_INFORMADA.", "Separa ausencia semántica de nulo técnico.", "Imputar una jornada no verificada."),
        ("PLAN", "Trece categorías parecidas pero distintas.", "Validar catálogo y crear rótulos de presentación.", "Preserva el detalle de cada plan.", "Fusionar modalidades temporales diferentes."),
        ("DEPARTAMENTAL", "26 direcciones regionales legítimas.", "Validar catálogo y correspondencia muchos-a-uno.", "Respeta subdivisiones administrativas.", "Reducir regiones válidas a una categoría única."),
    ],
    columns=["VARIABLE", "PROBLEMA", "REGLA", "POR_QUE_FUNCIONA", "RIESGO"],
)
plan_por_variable
"""),
    )

    conclusions_index = find_cell(cells, startswith="## 11. Conclusiones")
    # La conclusión sigue siendo la sección 11 porque el análisis territorial se
    # integró como subsección 4.1, sin alterar el resto de la estructura.
    conclusion_code_index = conclusions_index + 1
    cells[conclusion_code_index]["source"] = """
abiertos = int((datos["STATUS"] == "ABIERTA").sum())
porcentaje_abiertos = 100 * abiertos / len(datos)
filas_sin_nombre = int(datos["ESTABLECIMIENTO"].str.strip().eq("").sum())

print(
    "\\n".join(
        [
            f"1. El conjunto crudo contiene {len(datos):,} filas y {datos.shape[1]} variables.",
            f"2. Se obtuvieron {datos['CODIGO'].nunique():,} códigos únicos; no hay filas exactamente duplicadas ni códigos repetidos.",
            f"3. Los registros corresponden al nivel {datos['NIVEL'].iloc[0]} y abarcan {datos['DEPARTAMENTO'].nunique()} categorías geográficas de origen.",
            f"4. Ciudad Capital aporta {len(capital):,} filas y 22 zonas; Guatemala aporta {len(guatemala):,} filas y 15 municipios. No comparten códigos ni rótulos de ubicación.",
            "5. Para resúmenes por departamento se propone DEPARTAMENTO_ANALISIS con 22 categorías, sin sobrescribir las 23 categorías de origen.",
            f"6. Hay {abiertos:,} códigos con estado ABIERTA ({porcentaje_abiertos:.2f} %); los estados de cierre o temporalidad deben conservarse.",
            "7. Las variables prioritarias incluyen textos, contactos, distritos y ahora también DEPARTAMENTO/MUNICIPIO por su distinta granularidad territorial.",
            f"8. ESTABLECIMIENTO tiene {filas_sin_nombre:,} filas vacías; su limpieza exige preservar tildes, ñ, siglas y nombres propios.",
            f"9. DIRECTOR reúne {faltantes_por_variable['DIRECTOR']:,} faltantes efectivos; TELEFONO tiene {faltantes_por_variable['TELEFONO']:,} vacíos y {telefonos_no_estandar:,} formatos no estándar.",
            f"10. DISTRITO presenta {distritos_invalidos:,} valores vacíos o incompletos, mientras CODIGO cumple el formato esperado en todas las filas.",
            "11. En este avance no se eliminó ninguna fila ni se sobrescribió ningún texto; la siguiente fase aplicará las reglas sobre una copia y registrará cada transformación.",
        ]
    )
)
""".strip()

    # Limpiar outputs viejos y contadores antes de una ejecución integral.
    for cell in cells:
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    nb.setdefault("metadata", {}).setdefault(
        "kernelspec",
        {"display_name": "Python 3", "language": "python", "name": "python3"},
    )
    nb["metadata"].setdefault("language_info", {"name": "python", "version": "3"})
    return nb


def rich_data(value):
    data = {"text/plain": repr(value)}
    html = getattr(value, "_repr_html_", None)
    if callable(html):
        rendered = html()
        if rendered:
            data["text/html"] = rendered
    return data


def execute_notebook(nb):
    namespace = {"__name__": "__main__"}
    execution_count = 0

    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue

        execution_count += 1
        cell["execution_count"] = execution_count
        outputs = []
        stdout = io.StringIO()
        source = source_text(cell)

        if "plt" in namespace:
            plt = namespace["plt"]

            def capture_show(*_args, **_kwargs):
                for number in list(plt.get_fignums()):
                    figure = plt.figure(number)
                    buffer = io.BytesIO()
                    figure.savefig(buffer, format="png", dpi=120, bbox_inches="tight")
                    outputs.append(
                        {
                            "output_type": "display_data",
                            "metadata": {},
                            "data": {"image/png": base64.b64encode(buffer.getvalue()).decode("ascii")},
                        }
                    )
                plt.close("all")

            plt.show = capture_show

        tree = ast.parse(source, filename=f"cell-{execution_count}", mode="exec")
        result = None
        with contextlib.redirect_stdout(stdout):
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                prefix = ast.Module(body=tree.body[:-1], type_ignores=[])
                if prefix.body:
                    exec(compile(prefix, f"cell-{execution_count}", "exec"), namespace)
                result = eval(
                    compile(ast.Expression(tree.body[-1].value), f"cell-{execution_count}", "eval"),
                    namespace,
                )
            else:
                exec(compile(tree, f"cell-{execution_count}", "exec"), namespace)

        printed = stdout.getvalue()
        if printed:
            outputs.insert(0, {"output_type": "stream", "name": "stdout", "text": printed})
        if result is not None:
            outputs.append(
                {
                    "output_type": "execute_result",
                    "execution_count": execution_count,
                    "metadata": {},
                    "data": rich_data(result),
                }
            )
        cell["outputs"] = outputs

    return nb


def main():
    nb = build_notebook()
    nb = execute_notebook(nb)
    OUTPUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
