import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const ROOT = "/workspace/scratch/035c708243f8";
const DATA = path.join(ROOT, "salidas_proyecto_1_2026", "datos");
const OUT = path.join(ROOT, "salidas_proyecto_1_2026", "documentacion", "Proyecto_1_MINEDUC_2026_Datos_Libro_Codigos.xlsx");
const PREVIEW = path.join(ROOT, "tmp", "xlsx_previews_2026");

const NAVY = "#0B3558";
const BLUE = "#1769AA";
const TEAL = "#1B8A8F";
const GOLD = "#D59B28";
const LIGHT_BLUE = "#EAF2F8";
const LIGHT_TEAL = "#E8F5F2";
const LIGHT_GOLD = "#FFF4D6";
const LIGHT_GRAY = "#F4F6F8";
const BORDER = "#D4DEE7";
const WHITE = "#FFFFFF";
const RED = "#B42318";
const GREEN = "#137A55";

await fs.mkdir(path.dirname(OUT), { recursive: true });
await fs.mkdir(PREVIEW, { recursive: true });

const workbook = Workbook.create();
workbook.comments.setSelf({ displayName: "Equipo Proyecto 1 MINEDUC" });
const summary = workbook.worksheets.add("Resumen");

const specs = [
  ["Datos_Limpios_Muestra", "establecimientos_diversificado_limpio_analitico.csv"],
  ["Diagnostico", "perfil_datos_crudos.csv"],
  ["Calidad_Antes_Despues", "calidad_antes_despues.csv"],
  ["Plan_Limpieza", "plan_limpieza_por_variable.csv"],
  ["Transformaciones", "resumen_transformaciones.csv"],
  ["Bitacora_Reglas", "bitacora_reglas_resumen.csv"],
  ["Consistencia", "validaciones_consistencia_cruzada.csv"],
  ["Controles_Calidad", "controles_calidad.csv"],
  ["Libro_Codigos", "libro_codigos.csv"],
  ["Catalogos", "catalogos_codificacion.csv"],
  ["Catalogo_Territorial", "catalogo_territorial_observado.csv"],
  ["Metadatos", "metadatos_conjunto.csv"],
  ["Manifiesto", "manifiesto_salidas.csv"],
];

for (const [sheetName, fileName] of specs) {
  console.error(`IMPORT ${sheetName}`);
  const csv = await fs.readFile(path.join(DATA, fileName), "utf8");
  const parsed = await Workbook.fromCSV(csv, { sheetName });
  const parsedSheet = parsed.worksheets.getItem(sheetName);
  const parsedRange = parsedSheet.getUsedRange();
  const allValues = parsedRange.values;
  const values = sheetName === "Datos_Limpios_Muestra" ? allValues.slice(0, 3001) : allValues;
  const sheet = workbook.worksheets.add(sheetName);
  sheet.getRangeByIndexes(0, 0, values.length, values[0]?.length ?? 1).values = values;
}
console.error("IMPORT COMPLETE");
global.gc?.();

const duplicateSummary = workbook.worksheets.add("Duplicados_Resumen");
duplicateSummary.getRange("A1:D4").values = [
  ["DECISION", "PARES", "REVISION_MANUAL_RECOMENDADA", "FILAS_ELIMINADAS"],
  ["CONSERVAR_SERVICIOS_DISTINTOS", 10802, 0, 0],
  ["CONSERVAR_Y_REVISAR", 1306, 1306, 0],
  ["CONSERVAR_CODIGOS_DISTINTOS", 923, 757, 0],
];
duplicateSummary.getRange("A6:D7").values = [
  ["ARCHIVO_DETALLE", "candidatos_duplicados_parciales.csv", "PARES_TOTALES", 13031],
  ["NOTA", "El CSV completo contiene similitud, evidencias, decisión y justificación por par.", "UMBRAL", 0.92],
];

function columnName(index) {
  let n = index + 1;
  let out = "";
  while (n > 0) {
    const rem = (n - 1) % 26;
    out = String.fromCharCode(65 + rem) + out;
    n = Math.floor((n - 1) / 26);
  }
  return out;
}

function styleImportedSheet(sheetName) {
  const sheet = workbook.worksheets.getItem(sheetName);
  const used = sheet.getUsedRange();
  const rows = used.rowCount;
  const cols = used.columnCount;
  const last = columnName(cols - 1);
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  const header = sheet.getRange(`A1:${last}1`);
  header.format = {
    fill: NAVY,
    font: { bold: true, color: WHITE, size: 10 },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
    borders: { preset: "inside", style: "thin", color: "#355B78" },
  };
  header.format.rowHeight = 32;
  used.format.font = { name: "Aptos", size: rows > 50000 ? 8 : 9 };
  used.format.verticalAlignment = "center";
  used.format.borders = { insideHorizontal: { style: "thin", color: "#E7EDF2" } };

  const values = header.values[0] ?? [];
  for (let c = 0; c < cols; c++) {
    const name = String(values[c] ?? "");
    const col = sheet.getRange(`${columnName(c)}1:${columnName(c)}${Math.min(rows, 5000)}`);
    let width = 14;
    if (/DESCRIP|PROBLEMA|REGLA|TRANSFORM|JUSTIF|TRATAMIENTO|METODO|UTILIDAD|RIESGO|CONTROL|ACCION|DOMINIO|VALORES|ARCHIVO|FUENTE_URL|REFERENCIA|COBERTURA|ESTABLECIMIENTO|DIRECCION/i.test(name)) width = 30;
    if (/CODIGO|ID$|_COD|FILAS|PORCENTAJE|CUMPLE|ANTES|DESPUES|CAMBIO|SIMILITUD|NULL/i.test(name)) width = 14;
    if (/VARIABLE|DEPARTAMENTO|MUNICIPIO|CATEGORIA|DECISION|ESTADO|TELEFONO|FECHA|VERSION|TIPO/i.test(name)) width = 20;
    col.format.columnWidth = width;
    if (width >= 28 && rows < 5000) col.format.wrapText = true;
  }

  if (rows <= 5000 && cols <= 20) {
    const table = sheet.tables.add(`A1:${last}${rows}`, true, `T_${sheetName.replace(/[^A-Za-z0-9]/g, "").slice(0, 22)}`);
    table.style = "TableStyleMedium2";
    table.showBandedRows = true;
    table.showFilterButton = true;
    used.format.autofitRows();
    header.format.rowHeight = 32;
  }
  return { sheet, rows, cols, last };
}

const styled = new Map();
for (const [name] of specs) {
  console.error(`STYLE ${name}`);
  styled.set(name, styleImportedSheet(name));
}
console.error("STYLE COMPLETE");
styled.set("Duplicados_Resumen", styleImportedSheet("Duplicados_Resumen"));

const planSheet = styled.get("Plan_Limpieza").sheet;
planSheet.getRange("A1:A18").format.columnWidth = 18;
planSheet.getRange("B1:B18").format.columnWidth = 34;
planSheet.getRange("C1:C18").format.columnWidth = 38;
planSheet.getRange("D1:D18").format.columnWidth = 30;
planSheet.getRange("E1:E18").format.columnWidth = 34;
planSheet.getRange("A1:E18").format.wrapText = true;
planSheet.getRange("A1:E18").format.autofitRows();
planSheet.getRange("A1:E1").format.rowHeight = 34;

const transformationSheet = styled.get("Transformaciones").sheet;
transformationSheet.getRange("A1:A18").format.columnWidth = 18;
transformationSheet.getRange("B1:B18").format.columnWidth = 34;
transformationSheet.getRange("C1:C18").format.columnWidth = 38;
transformationSheet.getRange("D1:D18").format.columnWidth = 18;
transformationSheet.getRange("E1:E18").format.columnWidth = 34;
transformationSheet.getRange("A1:E18").format.wrapText = true;
transformationSheet.getRange("A1:E18").format.autofitRows();
transformationSheet.getRange("A1:E1").format.rowHeight = 34;

styled.get("Consistencia").sheet.getRange("B1:B8").format.columnWidth = 58;
styled.get("Controles_Calidad").sheet.getRange("B1:B23").format.columnWidth = 52;

// Identificadores y códigos permanecen como texto visible en las hojas principales.
for (const sheetName of ["Datos_Limpios_Muestra", "Catalogo_Territorial"]) {
  const { sheet, rows, cols } = styled.get(sheetName);
  const headers = sheet.getRange(`A1:${columnName(cols - 1)}1`).values[0];
  headers.forEach((h, i) => {
    if (/CODIGO|DISTRITO|TELEFONO|SHA256|VERSION/i.test(String(h))) {
      sheet.getRange(`${columnName(i)}2:${columnName(i)}${rows}`).format.numberFormat = "@";
    }
  });
}

// Formato semántico y condicional.
styled.get("Diagnostico").sheet.getRange("C2:F18").format.numberFormat = "#,##0";
styled.get("Diagnostico").sheet.getRange("G2:G18").format.numberFormat = "0.00";
styled.get("Calidad_Antes_Despues").sheet.getRange("B2:D4").format.numberFormat = "#,##0";
styled.get("Calidad_Antes_Despues").sheet.getRange("B5:D5").format.numberFormat = "0.0000";
styled.get("Calidad_Antes_Despues").sheet.getRange("B6:D13").format.numberFormat = "#,##0";

const controlsSheet = styled.get("Controles_Calidad").sheet;
controlsSheet.getRange("C2:C23").conditionalFormats.add("cellIs", {
  operator: "equal", formula: "TRUE", format: { fill: "#DFF3E8", font: { color: GREEN, bold: true } },
});
controlsSheet.getRange("C2:C23").conditionalFormats.add("cellIs", {
  operator: "equal", formula: "FALSE", format: { fill: "#FDE8E7", font: { color: RED, bold: true } },
});

const dupSheet = styled.get("Duplicados_Resumen").sheet;
dupSheet.getRange("A2:A4").conditionalFormats.add("containsText", {
  text: "REVISAR", format: { fill: LIGHT_GOLD, font: { color: "#7A5A00", bold: true } },
});
console.error("CONDITIONAL COMPLETE");

// Resumen ejecutivo con fórmulas auditables.
summary.showGridLines = false;
summary.freezePanes.freezeRows(2);
summary.mergeCells("A1:N1");
summary.getRange("A1").values = [["PROYECTO 1 · OBTENCIÓN Y LIMPIEZA DE DATOS MINEDUC"]];
summary.getRange("A1:N1").format = {
  fill: NAVY,
  font: { name: "Aptos Display", size: 20, bold: true, color: WHITE },
  horizontalAlignment: "left",
  verticalAlignment: "center",
};
summary.getRange("A1:N1").format.rowHeight = 40;
summary.mergeCells("A2:N2");
summary.getRange("A2").values = [["Nivel Diversificado · Guatemala · CC3084 Data Science · Versión 2.0.0 · 2026"]];
summary.getRange("A2:N2").format = {
  fill: BLUE,
  font: { size: 11, color: WHITE, italic: true },
  horizontalAlignment: "left",
  verticalAlignment: "center",
};
summary.getRange("A2:N2").format.rowHeight = 25;

const cardLabels = [["REGISTROS LIMPIOS", "", "VARIABLES FINALES", "", "CONTROLES APROBADOS", ""]];
summary.getRange("A4:F4").values = cardLabels;
summary.mergeCells("A4:B4"); summary.mergeCells("C4:D4"); summary.mergeCells("E4:F4");
summary.getRange("A4:F4").format = { fill: LIGHT_BLUE, font: { bold: true, color: NAVY, size: 9 }, horizontalAlignment: "center" };
summary.mergeCells("A5:B6"); summary.mergeCells("C5:D6"); summary.mergeCells("E5:F6");
summary.getRange("A5").formulas = [["='Metadatos'!$B$12"]];
summary.getRange("C5").formulas = [["='Metadatos'!$B$13"]];
summary.getRange("E5").formulas = [["=COUNTIF('Controles_Calidad'!$C$2:$C$23,TRUE)&\"/\"&COUNTA('Controles_Calidad'!$A$2:$A$23)"]];
summary.getRange("A5:F6").format = { fill: LIGHT_BLUE, font: { bold: true, color: NAVY, size: 20 }, horizontalAlignment: "center", verticalAlignment: "center" };

summary.getRange("A8:F8").values = [["PARES PARCIALES", "", "REVISIÓN RECOMENDADA", "", "FILAS ELIMINADAS", ""]];
summary.mergeCells("A8:B8"); summary.mergeCells("C8:D8"); summary.mergeCells("E8:F8");
summary.getRange("A8:F8").format = { fill: LIGHT_TEAL, font: { bold: true, color: NAVY, size: 9 }, horizontalAlignment: "center" };
summary.mergeCells("A9:B10"); summary.mergeCells("C9:D10"); summary.mergeCells("E9:F10");
summary.getRange("A9").formulas = [["=SUM('Duplicados_Resumen'!$B$2:$B$4)"]];
summary.getRange("C9").formulas = [["=SUM('Duplicados_Resumen'!$C$2:$C$4)"]];
summary.getRange("E9").formulas = [["=SUM('Duplicados_Resumen'!$D$2:$D$4)"]];
summary.getRange("A9:F10").format = { fill: LIGHT_TEAL, font: { bold: true, color: NAVY, size: 20 }, horizontalAlignment: "center", verticalAlignment: "center" };

summary.mergeCells("A12:F12");
summary.getRange("A12").values = [["Conclusión de calidad"]];
summary.getRange("A12:F12").format = { fill: LIGHT_GOLD, font: { bold: true, color: "#7A5A00", size: 11 } };
summary.mergeCells("A13:F16");
summary.getRange("A13").values = [["Se conservaron 11,603 registros. El aumento de 173 null analíticos es intencional: 69 distritos incompletos y 104 teléfonos no interpretables dejan de tratarse como válidos. Sus valores originales permanecen disponibles. Los 13,031 pares parciales tienen decisión documentada y ninguna fila fue eliminada por similitud. La hoja Datos_Limpios_Muestra contiene 3,000 filas para consulta ágil; el CSV limpio adjunto contiene las 11,603 filas."]];
summary.getRange("A13:F16").format = { fill: "#FFFAEC", font: { color: "#4C3A00", size: 10 }, wrapText: true, verticalAlignment: "top" };

summary.getRange("A18:F18").values = [["Metadato", "Valor", "", "", "", ""]];
summary.mergeCells("B18:F18");
summary.getRange("A18:F18").format = { fill: NAVY, font: { bold: true, color: WHITE } };
const metadataRows = [
  ["Fuente", "MINEDUC · Búsqueda de centros educativos autorizados"],
  ["URL", "http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/"],
  ["Fecha de extracción", "2026-07-10"],
  ["Fecha de procesamiento", "2026-07-17"],
  ["Versión", "2.0.0"],
  ["Cobertura", "334 municipios observados + 22 zonas capitalinas; referencia nacional: 340 municipios"],
  ["Referencia territorial", "https://datos.segeplan.gob.gt/es/dataset/calculo-matematico-para-la-asignacion-constitucional-a-las-municipalidades-2026"],
];
metadataRows.forEach((row, i) => {
  const excelRow = 19 + i;
  summary.getRange(`A${excelRow}`).values = [[row[0]]];
  summary.mergeCells(`B${excelRow}:F${excelRow}`);
  summary.getRange(`B${excelRow}`).values = [[row[1]]];
});
summary.getRange("A19:A25").format = { fill: LIGHT_GRAY, font: { bold: true, color: NAVY } };
summary.getRange("B19:F25").format = { wrapText: true, font: { color: "#263746" } };
summary.getRange("A24:F24").format.rowHeight = 30;
summary.getRange("A25:F25").format.rowHeight = 45;

const metadataSheet = styled.get("Metadatos").sheet;
metadataSheet.getRange("A1:A16").format.columnWidth = 30;
metadataSheet.getRange("B1:B16").format.columnWidth = 85;
metadataSheet.getRange("B2:B16").format.wrapText = true;
metadataSheet.getRange("A1:B16").format.autofitRows();
metadataSheet.getRange("A1:B1").format.rowHeight = 32;

// Tabla auxiliar y gráfico de decisiones.
summary.getRange("H4:I4").values = [["DECISIÓN", "PARES"]];
summary.getRange("H5:H7").values = [["Servicios distintos"], ["Conservar y revisar"], ["Códigos distintos"]];
summary.getRange("I5").formulas = [["='Duplicados_Resumen'!$B$2"]];
summary.getRange("I6").formulas = [["='Duplicados_Resumen'!$B$3"]];
summary.getRange("I7").formulas = [["='Duplicados_Resumen'!$B$4"]];
console.error("SUMMARY FORMULAS COMPLETE");
summary.getRange("H4:I7").format.borders = { preset: "all", style: "thin", color: BORDER };
summary.getRange("H4:I4").format = { fill: NAVY, font: { bold: true, color: WHITE } };
summary.getRange("I5:I7").format.numberFormat = "#,##0";
const chart = summary.charts.add("bar", summary.getRange("H4:I7"));
chart.title = "Decisiones para candidatos parciales";
chart.hasLegend = false;
chart.xAxis = { axisType: "textAxis", textStyle: { fontSize: 9 } };
chart.yAxis = { numberFormatCode: "#,##0" };
chart.setPosition("H9", "N24");

summary.getRange("A1:N25").format.borders = { outside: { style: "thin", color: BORDER } };
summary.getRange("A1:A25").format.columnWidth = 23;
summary.getRange("B1:F25").format.columnWidth = 16;
summary.getRange("G1:G25").format.columnWidth = 3;
summary.getRange("H1:H25").format.columnWidth = 24;
summary.getRange("I1:N25").format.columnWidth = 14;
summary.getRange("A19:A25").format.columnWidth = 23;

// Comentarios de procedencia en celdas clave.
workbook.comments.addThread({ cell: summary.getRange("B20") }, "Fuente oficial utilizada para el snapshot: portal de establecimientos autorizados del MINEDUC.");
workbook.comments.addThread({ cell: summary.getRange("B25") }, "SEGEPLAN informa 340 municipalidades para 2026. El catálogo observado del proyecto contiene solo las que aparecen con Diversificado en el snapshot.");
console.error("SUMMARY COMPLETE");

const inspect = await workbook.inspect({
  kind: "table",
  range: "Resumen!A1:N25",
  include: "values,formulas",
  tableMaxRows: 25,
  tableMaxCols: 14,
  maxChars: 10000,
});
await fs.writeFile(path.join(PREVIEW, "resumen_inspect.ndjson"), inspect.ndjson, "utf8");

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
  maxChars: 8000,
});
await fs.writeFile(path.join(PREVIEW, "formula_errors.ndjson"), errors.ndjson, "utf8");
console.error("INSPECT COMPLETE");

const previewRanges = new Map([
  ["Resumen", "A1:N25"], ["Datos_Limpios_Muestra", "A1:P22"],
  ["Diagnostico", "A1:G18"], ["Calidad_Antes_Despues", "A1:D13"],
  ["Plan_Limpieza", "A1:E18"], ["Transformaciones", "A1:E18"],
  ["Bitacora_Reglas", "A1:G13"],
  ["Duplicados_Resumen", "A1:D7"], ["Consistencia", "A1:D8"],
  ["Controles_Calidad", "A1:E23"], ["Libro_Codigos", "A1:H20"],
  ["Catalogos", "A1:E22"], ["Catalogo_Territorial", "A1:H22"],
  ["Metadatos", "A1:B16"], ["Manifiesto", "A1:C19"],
]);
for (const [name, range] of previewRanges) {
  console.error(`RENDER ${name}`);
  const blob = await workbook.render({ sheetName: name, range, scale: name === "Resumen" ? 1.2 : 0.9, format: "png" });
  await fs.writeFile(path.join(PREVIEW, `${name}.png`), new Uint8Array(await blob.arrayBuffer()));
}
console.error("RENDER COMPLETE");

const output = await SpreadsheetFile.exportXlsx(workbook);
console.error("EXPORT COMPLETE");
await output.save(OUT);
console.log(OUT);
