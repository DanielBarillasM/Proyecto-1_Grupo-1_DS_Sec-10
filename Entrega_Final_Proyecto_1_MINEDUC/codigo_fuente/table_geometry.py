from __future__ import annotations

from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def _set_table_width(table, width_dxa: int) -> None:
    tbl_pr = table._tbl.tblPr
    layout = tbl_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")

    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:type"), "dxa")
    tbl_w.set(qn("w:w"), str(width_dxa))


def _set_table_indent(table, indent_dxa: int) -> None:
    tbl_pr = table._tbl.tblPr
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:type"), "dxa")
    tbl_ind.set(qn("w:w"), str(indent_dxa))


def _set_table_cell_margins(table, margins_dxa: dict) -> None:
    tbl_pr = table._tbl.tblPr
    tbl_cell_mar = tbl_pr.find(qn("w:tblCellMar"))
    if tbl_cell_mar is None:
        tbl_cell_mar = OxmlElement("w:tblCellMar")
        tbl_pr.append(tbl_cell_mar)
    sides = {"top": "top", "bottom": "bottom", "start": "start", "end": "end"}
    for key, tag in sides.items():
        value = margins_dxa.get(key)
        if value is None:
            continue
        node = tbl_cell_mar.find(qn(f"w:{tag}"))
        if node is None:
            node = OxmlElement(f"w:{tag}")
            tbl_cell_mar.append(node)
        node.set(qn("w:type"), "dxa")
        node.set(qn("w:w"), str(value))


def _set_grid_and_cell_widths(table, widths_dxa: list[int]) -> None:
    grid = table._tbl.find(qn("w:tblGrid"))
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        table._tbl.insert(0, grid)
    for child in list(grid):
        grid.remove(child)
    for width in widths_dxa:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for row in table.rows:
        for cell, width in zip(row.cells, widths_dxa):
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.find(qn("w:tcW"))
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:type"), "dxa")
            tc_w.set(qn("w:w"), str(width))


def apply_table_geometry(
    table,
    widths_dxa: list[int],
    *,
    table_width_dxa: int,
    indent_dxa: int = 0,
    cell_margins_dxa: dict | None = None,
) -> None:
    table.autofit = False
    table.allow_autofit = False
    _set_table_width(table, table_width_dxa)
    _set_table_indent(table, indent_dxa)
    if cell_margins_dxa:
        _set_table_cell_margins(table, cell_margins_dxa)
    _set_grid_and_cell_widths(table, widths_dxa)
