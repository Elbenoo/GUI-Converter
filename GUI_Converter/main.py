import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QComboBox,
    QLabel, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QAbstractItemView, QSizePolicy,
    QHeaderView
)
from PySide6.QtCore import Qt, QRegularExpression, QLocale
from PySide6.QtGui import QDoubleValidator, QRegularExpressionValidator
from PySide6 import QtCore, QtWidgets
from typing import Dict, List

try:
    from gui_converter import UnitConverterUI
except ImportError as e:
    # Esto ayuda a diagnosticar si el archivo de la GUI no se encuentra
    print(f"Error: No se pudo importar UnitConverterUI desde gui_converter.py. {e}")
    sys.exit(1)

# FUNCIONES AUXILIARES Y DATOS

def convert_to_html_unit(unit_str: str) -> str:
    """Convierte un string de unidad con superíndices (ej. 'm³') a HTML."""
    unit_str = unit_str.replace("²", "<sup>2</sup>")
    unit_str = unit_str.replace("³", "<sup>3</sup>")
    unit_str = unit_str.replace("⁴", "<sup>4</sup>")
    unit_str = unit_str.replace("·", "⋅")
    unit_str = unit_str.replace("K⁴", "K<sup>4</sup>")
    return unit_str


def placeholder_convert(category: str, src_idx: int, dst_idx: int, qty: float) -> float:
    """Función central de conversión de unidades."""

    if category == "Force":
        if src_idx == 0 and dst_idx == 1:
            return qty
        elif src_idx == 0 and dst_idx == 2:
            return qty * 100000.0
        elif src_idx == 1 and dst_idx == 0:
            return qty
        elif src_idx == 1 and dst_idx == 2:
            return qty * 100000.0
        elif src_idx == 2 and dst_idx == 0:
            return qty / 100000.0
        elif src_idx == 2 and dst_idx == 1:
            return qty / 100000.0
        else:
            return qty
    if category == "Pressure":
        if src_idx == 0 and dst_idx == 1:
            return qty / 1000000
        elif src_idx == 0 and dst_idx == 2:
            return qty * 10
        elif src_idx == 1 and dst_idx == 0:
            return qty * 1000000
        elif src_idx == 1 and dst_idx == 2:
            return qty * 10000000
        elif src_idx == 2 and dst_idx == 0:
            return qty / 10
        elif src_idx == 2 and dst_idx == 1:
            return qty / 10000000
        else:
            return qty
    if category == "Density":
        if src_idx == 0 and dst_idx == 1:
            return qty / 1000000000
        elif src_idx == 0 and dst_idx == 2:
            return qty / 1000
        elif src_idx == 1 and dst_idx == 0:
            return qty * 1000000000
        elif src_idx == 1 and dst_idx == 2:
            return qty * 1000000
        elif src_idx == 2 and dst_idx == 0:
            return qty * 1000
        elif src_idx == 2 and dst_idx == 1:
            return qty / 1000000
        else:
            return qty
    if category == "Thermal Conductivity":
        if src_idx == 0 and dst_idx == 1:
            return qty * 1000
        elif src_idx == 0 and dst_idx == 2:
            return qty * 100000
        elif src_idx == 1 and dst_idx == 0:
            return qty / 1000
        elif src_idx == 1 and dst_idx == 2:
            return qty * 100
        elif src_idx == 2 and dst_idx == 0:
            return qty / 100000
        elif src_idx == 2 and dst_idx == 1:
            return qty / 100
        else:
            return qty
    if category == "Specific heat":
        if src_idx == 0 and dst_idx == 1:
            return qty * 1000000
        elif src_idx == 0 and dst_idx == 2:
            return qty * 10000
        elif src_idx == 1 and dst_idx == 0:
            return qty / 1000000
        elif src_idx == 1 and dst_idx == 2:
            return qty / 100
        elif src_idx == 2 and dst_idx == 0:
            return qty / 10000
        elif src_idx == 2 and dst_idx == 1:
            return qty * 100
        else:
            return qty
    if category == "Young’s Modulus":
        if src_idx == 0 and dst_idx == 1:
            return qty / 1000000
        elif src_idx == 0 and dst_idx == 2:
            return qty * 10
        elif src_idx == 1 and dst_idx == 0:
            return qty * 1000000
        elif src_idx == 1 and dst_idx == 2:
            return qty * 10000000
        elif src_idx == 2 and dst_idx == 0:
            return qty / 10
        elif src_idx == 2 and dst_idx == 1:
            return qty / 10000000
        else:
            return qty
    if category == "Film Coefficient":
        if src_idx == 0 and dst_idx == 1:
            return qty
        elif src_idx == 0 and dst_idx == 2:
            return qty * 1000
        elif src_idx == 1 and dst_idx == 0:
            return qty
        elif src_idx == 1 and dst_idx == 2:
            return qty * 1000
        elif src_idx == 2 and dst_idx == 0:
            return qty / 1000
        elif src_idx == 2 and dst_idx == 1:
            return qty / 1000
        else:
            return qty
    if category == "Dynamic Viscosity":
        if src_idx == 0 and dst_idx == 1:
            return qty / 1000000
        elif src_idx == 0 and dst_idx == 2:
            return qty * 10
        elif src_idx == 1 and dst_idx == 0:
            return qty * 1000000
        elif src_idx == 1 and dst_idx == 2:
            return qty * 10000000
        elif src_idx == 2 and dst_idx == 0:
            return qty / 10
        elif src_idx == 2 and dst_idx == 1:
            return qty / 10000000
        else:
            return qty
    if category == "Elastic":
        if src_idx == 0 and dst_idx == 1:
            return qty / 1000000
        elif src_idx == 0 and dst_idx == 2:
            return qty * 10
        elif src_idx == 1 and dst_idx == 0:
            return qty * 1000000
        elif src_idx == 1 and dst_idx == 2:
            return qty * 10000000
        elif src_idx == 2 and dst_idx == 0:
            return qty / 10
        elif src_idx == 2 and dst_idx == 1:
            return qty / 10000000
        else:
            return qty
    if category == "Expansion":
        if src_idx == 0 and dst_idx == 1:
            return qty
        elif src_idx == 0 and dst_idx == 2:
            return qty
        elif src_idx == 1 and dst_idx == 0:
            return qty
        elif src_idx == 1 and dst_idx == 2:
            return qty
        elif src_idx == 2 and dst_idx == 0:
            return qty
        elif src_idx == 2 and dst_idx == 1:
            return qty
        else:
            return qty
    if category == "Stefan Boltzmann":
        if src_idx == 0 and dst_idx == 1:
            return qty / 1000
        elif src_idx == 0 and dst_idx == 2:
            return qty * 1000
        elif src_idx == 1 and dst_idx == 0:
            return qty * 1000
        elif src_idx == 1 and dst_idx == 2:
            return qty * 1000000
        elif src_idx == 2 and dst_idx == 0:
            return qty / 1000
        elif src_idx == 2 and dst_idx == 1:
            return qty / 1000000
        else:
            return qty
    return qty


CATEGORY_UNITS: Dict[str, List[str]] = {
    "Force": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Pressure": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Density": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Thermal Conductivity": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Specific heat": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Young’s Modulus": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Film Coefficient": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Dynamic Viscosity": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Elastic": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Expansion": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    "Stefan Boltzmann": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
}

UNIT_LABELS: Dict[str, List[str]] = {
    "Force": ["N", "N", "dyn"],
    "Pressure": ["Pa", "N/mm²", "dyn/cm²"],
    "Density": ["kg/m³", "kg/mm³", "g/cm³"],
    "Thermal Conductivity": ["W/(m·K)", "N·mm/(s·K)", "g·cm/(s³·K)"],
    "Specific heat": ["J/(kg·K)", "mm²/(s²·K)", "cm²/(s²·K)"],
    "Young’s Modulus": ["Pa", "N/mm²", "dyn/cm²"],
    "Film Coefficient": ["W/(m²·K)", "N/(m·m·s·K)", "g/(s³·K)"],
    "Dynamic Viscosity": ["Pa·s", "N·s/mm²", "Poise"],
    "Elastic": ["Pa", "N/mm²", "dyn/cm²"],
    "Expansion": ["1/K", "1/K", "1/K"],
    "Stefan Boltzmann": ["W/(m²·K⁴)", "N/(mm·s·K⁴)", "erg/(cm²·s·K⁴)"],
}

def main():
    app = QApplication(sys.argv)
    window = UnitConverterUI()

    try:
        from qt_material import apply_stylesheet
        apply_stylesheet(app, theme='dark_teal.xml')
    except ImportError:
        pass

    # Referencias a Widgets
    # Estas variables son necesarias para las conexiones de eventos.
    combo_left = window.combo_properties
    value_edit = window.line_edit_value
    combo_source = window.combo_source_system

    # Lógica de Manejo de Eventos

    def on_convert_clicked():
        # Esta lógica se mantiene aquí para manejar la conversión y el formato del resultado.
        category = combo_left.currentText()

        try:
            qty_text = value_edit.text().strip()
            if not qty_text or qty_text in ['+', '-']:
                raise ValueError("Value field is empty or incomplete.")

            qty = float(qty_text)

        except ValueError:
            # Limpieza simple de tabla
            for r in range(window.table_results.rowCount()):
                if window.table_results.item(r, 1): window.table_results.item(r, 1).setText("")
                if window.table_results.item(r, 2): window.table_results.item(r, 2).setText("")
            return

        if not category: return

        src_idx = combo_source.currentIndex()
        units_list = CATEGORY_UNITS.get(category, [])
        window.table_results.setRowCount(len(units_list))
        locale_us = QLocale(QLocale.English, QLocale.UnitedStates)  # Definido dentro para simplicidad

        for dst_idx, _dst_unit in enumerate(units_list):
            result = placeholder_convert(category, src_idx, dst_idx, qty)

            # Columna 2: Scientific notation
            item_scientific = window.table_results.item(dst_idx, 2)
            if item_scientific is None:
                item_scientific = QTableWidgetItem()
                window.table_results.setItem(dst_idx, 2, item_scientific)

            item_scientific.setText(f"{result:.4e}")

            # Columna 1: Converted Value
            item_value = window.table_results.item(dst_idx, 1)
            if item_value is None:
                item_value = QTableWidgetItem()
                window.table_results.setItem(dst_idx, 1, item_value)

            if result == 0.0:
                formatted_result = "0"
            elif abs(result) >= 1e16 or abs(result) < 1e-15:
                formatted_result = f"{result:.16e}"
            else:
                raw_formatted = locale_us.toString(result, 'f', 16)
                formatted_result = raw_formatted.rstrip('0')
                if formatted_result.endswith('.'):
                    formatted_result = formatted_result.rstrip('.')

            window.table_results.item(dst_idx, 1).setText(formatted_result)

    def on_category_changed(idx: int):
        # Cuando se cambia la categoría, solo se reinicia el valor a la UI para actualizarse.
        value_edit.setText("")

        # El resto de la lógica de actualización de la UI se delega a gui_converter.py
        if hasattr(window, 'reset_and_update_ui_from_combo'):
            window.reset_and_update_ui_from_combo(idx)

    # CONEXIONES
    value_edit.textChanged.connect(on_convert_clicked)
    combo_source.currentIndexChanged.connect(on_convert_clicked)
    combo_left.currentIndexChanged.connect(on_category_changed)

    # Inicialización
    if combo_left.count() > 0:
        combo_left.setCurrentIndex(0)
        on_category_changed(0)

    window.setWindowTitle("Unit converter")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()