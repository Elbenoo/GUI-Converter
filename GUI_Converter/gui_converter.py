import sys
from typing import Dict, List
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QComboBox,
    QLabel, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QAbstractItemView, QSizePolicy,
    QHeaderView, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QRegularExpression, QLocale, QEvent, QModelIndex, QSize
from PySide6.QtGui import QRegularExpressionValidator, QIcon

class UnitConverterUI(QMainWindow):

    #DATOS DE UNIDADES Y CONVERSIÓN

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
        "Expansion": ["1/K", "1/K", "1/K"],
        "Stefan Boltzmann": ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"],
    }

    @staticmethod
    def convert_to_html_unit(unit_str: str) -> str:
        """Convierte un string de unidad con superíndices a HTML."""
        unit_str = unit_str.replace("²", "<sup>2</sup>")
        unit_str = unit_str.replace("³", "<sup>3</sup>")
        unit_str = unit_str.replace("⁴", "<sup>4</sup>")
        unit_str = unit_str.replace("·", "⋅")
        unit_str = unit_str.replace("K⁴", "K<sup>4</sup>")
        return unit_str

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de Unidades Físicas")

        self.setGeometry(100, 100, 1000, 750)
        self.setMinimumHeight(750)
        self.setMaximumHeight(750)
        self.setMinimumWidth(800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel Izquierdo (Selector de Magnitudes)
        left_panel_widget = QWidget()
        left_panel_layout = QVBoxLayout(left_panel_widget)
        magnitude_label = QLabel("Select Magnitude:")

        self.combo_properties = QComboBox()
        self.combo_properties.addItems(list(self.UNIT_LABELS.keys()))
        self.combo_properties.setFixedHeight(35)
        self.combo_properties.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        left_panel_layout.addWidget(magnitude_label)
        left_panel_layout.addWidget(self.combo_properties)
        left_panel_layout.addStretch(1)
        left_panel_widget.setFixedWidth(250)
        left_panel_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        main_layout.addWidget(left_panel_widget)

        # 3. Panel Derecho
        right_panel_widget = QWidget()
        right_panel_layout = QVBoxLayout(right_panel_widget)
        right_panel_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        top_controls_widget = QWidget()
        top_controls_layout = QVBoxLayout(top_controls_widget)
        top_controls_layout.setContentsMargins(0, 0, 0, 0)

        # Sistema de unidadesS
        system_units_layout = QHBoxLayout()
        system_units_layout.addStretch(1)
        system_units_label = QLabel("System of Units")
        system_units_label.setFixedWidth(120)
        system_units_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.combo_source_system = QComboBox()
        self.combo_source_system.addItems(self.CATEGORY_UNITS.get("Force", []))
        self.combo_source_system.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.combo_source_system.setFixedWidth(150)

        system_units_layout.addWidget(system_units_label)
        system_units_layout.addWidget(self.combo_source_system)

        # Entrada de Valor
        conversion_input_layout = QHBoxLayout()
        self.line_edit_value = QLineEdit("")
        self.line_edit_value.setPlaceholderText("Value")
        self.line_edit_value.setFixedWidth(200)
        self.line_edit_value.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        value_regex = QRegularExpression(r"^[+-]?(\d+[.,]?\d*|\d*[.,]?\d+)([eE][+-]?\d+)?$")
        value_validator = QRegularExpressionValidator(value_regex)
        self.line_edit_value.setValidator(value_validator)

        self.label_source_unit = QLabel("N")
        self.label_source_unit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.label_source_unit.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        unit_style = """
                    QLabel {
                        background-color: transparent; 
                        border: none;
                        font-weight: bold;
                        color: #4A90E2; 
                        padding-left: 0px; 
                        text-align: left;
                    }
                """
        self.label_source_unit.setStyleSheet(unit_style)
        self.label_source_unit.setObjectName("unit_label")

        conversion_input_layout.addWidget(self.line_edit_value)
        conversion_input_layout.addWidget(self.label_source_unit)
        conversion_input_layout.addStretch(1)

        top_controls_layout.addLayout(system_units_layout)
        top_controls_layout.addLayout(conversion_input_layout)
        right_panel_layout.addWidget(top_controls_widget)

        # TABLA DE RESULTADOS
        self.table_results = QTableWidget()
        self.table_results.setColumnCount(4)
        self.table_results.setHorizontalHeaderLabels([
            "Unit system", "Converted Value", "Scientific notation", "UNITS"
        ])
        self.table_results.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_results.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_results.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_results.verticalHeader().setDefaultSectionSize(30)
        self.table_results.setRowCount(3)
        unit_systems = ["m,Kg,s,K (SI)", "mm,N,s,K", "cm,g,s,K (CGS)"]

        for row in range(3):
            item_unit_system = QTableWidgetItem(unit_systems[row])
            item_unit_system.setFlags(item_unit_system.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_results.setItem(row, 0, item_unit_system)
            item_value = QTableWidgetItem("")
            item_value.setFlags(item_value.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_results.setItem(row, 1, item_value)
            item_scientific = QTableWidgetItem("")
            item_scientific.setFlags(item_scientific.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_results.setItem(row, 2, item_scientific)
            label_unit = QLabel("")
            label_unit.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.table_results.setCellWidget(row, 3, label_unit)

        right_panel_layout.addWidget(self.table_results, 1)

        # SECCIÓN: Historial, Limpiar y Guardar
        history_actions_layout = QHBoxLayout()
        history_actions_layout.setSpacing(5)
        self.button_add_to_history = QPushButton("Add Selected Result to History")
        self.button_add_to_history.setFixedHeight(40)
        history_actions_layout.addWidget(self.button_add_to_history, 1)

        # CONFIGURACIÓN DEL ÍCONO SVG
        svg_path = r"C:\GUI_Converter\icons\Deleted_icon.svg"
        trash_icon = QIcon(svg_path)
        self.button_clear_history = QPushButton()
        self.button_clear_history.setIcon(trash_icon)
        self.button_clear_history.setIconSize(QSize(32, 32))
        self.button_clear_history.setFixedSize(40, 40)
        self.button_clear_history.setToolTip("Clear History")
        self.button_clear_history.setStyleSheet("""
            QPushButton { 
                border: none; 
                background-color: transparent; 
                border-radius: 5px; 
            }
            QPushButton:hover { 
                background-color: #E74C3C; 
            }
        """)
        history_actions_layout.addWidget(self.button_clear_history)

        right_panel_layout.addLayout(history_actions_layout)
        history_label = QLabel("Conversion History - Press BACKSPACE or DELETE to remove item")
        history_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        right_panel_layout.addWidget(history_label)

        self.list_history = QListWidget()
        self.list_history.setMinimumHeight(120)
        self.list_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        right_panel_layout.addWidget(self.list_history)

        history_buttons_layout = QHBoxLayout()
        self.button_save_history = QPushButton("Save History (.txt)")
        self.button_save_history.setFixedHeight(40)
        self.button_save_history.setStyleSheet("""
            QPushButton { background-color: #2ECC71; color: white; border: 1px solid #27AE60; border-radius: 5px; font-weight: bold;}
            QPushButton:hover { background-color: #27AE60; }
        """)
        self.button_exit = QPushButton("Exit Program")
        self.button_exit.setFixedHeight(40)
        self.button_exit.setStyleSheet("""
            QPushButton { background-color: #E74C3C; color: white; border: 1px solid #C0392B; border-radius: 5px; font-weight: bold;}
            QPushButton:hover { background-color: #C0392B; }
        """)
        history_buttons_layout.addWidget(self.button_save_history, 1)
        history_buttons_layout.addWidget(self.button_exit, 1)
        right_panel_layout.addLayout(history_buttons_layout)
        main_layout.addWidget(right_panel_widget, 1)

        # CONEXIONES DE EVENTOS
        self.table_results.doubleClicked.connect(self._handle_double_click_selection)
        self.table_results.itemPressed.connect(self._handle_single_click_deselection)
        self.line_edit_value.textChanged.connect(self.perform_conversion)
        self.combo_source_system.currentIndexChanged.connect(self.perform_conversion)
        self.combo_properties.currentIndexChanged.connect(self.reset_and_update_ui_from_combo)
        self.button_exit.clicked.connect(self.close)
        self.button_add_to_history.clicked.connect(self.add_to_history)
        self.button_save_history.clicked.connect(self.save_history)
        self.button_clear_history.clicked.connect(self.clear_history)
        self.table_results.installEventFilter(self)
        self.list_history.installEventFilter(self)
        if self.combo_properties.count() > 0:
            self.reset_and_update_ui_from_combo(0)

    # MÉTODOS DE LÓGICA DE INTERFAZ

    def perform_conversion(self):
        value_str = self.line_edit_value.text().strip()
        current_property = self.combo_properties.currentText()
        locale = QLocale.system()

        if not value_str or not current_property:
            # Limpiar tabla si no hay valor
            for row in range(self.table_results.rowCount()):
                item_value = self.table_results.item(row, 1)
                item_scientific = self.table_results.item(row, 2)
                if item_value: item_value.setText("")
                if item_scientific: item_scientific.setText("")
            return

        try:
            # Preparar valor para la función de conversión (punto decimal)
            normalized_value_str = value_str.replace(',', '.')
            base_value = float(normalized_value_str)
            system_index = self.combo_source_system.currentIndex()

            # LLAMADA A LA FUNCIÓN EXTERNA
            # Si main.py define la función, necesitas importarla
            # Si no puedes importarla, esta línea fallará con NameError

            from main import placeholder_convert

            for row in range(self.table_results.rowCount()):
                result_item_value = self.table_results.item(row, 1)
                result_item_scientific = self.table_results.item(row, 2)

                # LLAMADA A LA FUNCIÓN DE CONVERSIÓN
                converted_value = placeholder_convert(current_property, system_index, row, base_value)

                # Formato y presentación
                scientific_value = f"{converted_value:.12e}"
                result_item_scientific.setText(scientific_value)

                raw_formatted = locale.toString(converted_value, 'f', 12)

                if locale.decimalPoint() in raw_formatted:
                    parts = raw_formatted.split(locale.decimalPoint(), 1)
                    decimal_part_cleaned = parts[1].rstrip('0')

                    if decimal_part_cleaned:
                        formatted_value = f"{parts[0]}{locale.decimalPoint()}{decimal_part_cleaned}"
                    else:
                        formatted_value = parts[0]
                else:
                    formatted_value = raw_formatted

                result_item_value.setText(formatted_value)

        except ValueError:
            # Limpiar si el valor de entrada es incorrecto
            for row in range(self.table_results.rowCount()):
                item_value = self.table_results.item(row, 1)
                item_scientific = self.table_results.item(row, 2)
                if item_value: item_value.setText("")
                if item_scientific: item_scientific.setText("")
            return
        except ImportError:
            QMessageBox.critical(self, "Error de Módulo",
                                 "No se pudo importar 'placeholder_convert'. Asegúrate de que tu lógica de conversión esté disponible.")

    def _handle_double_click_selection(self, index: QModelIndex):
        self.table_results.selectRow(index.row())

    def _handle_single_click_deselection(self, item: QTableWidgetItem):
        self.table_results.clearSelection()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if source == self.list_history:
                if key == Qt.Key.Key_Delete or key == Qt.Key.Key_Backspace:
                    self.remove_selected_history_item()
                    return True
            elif source == self.table_results:
                if key == Qt.Key.Key_Space:
                    self.add_to_history()
                    return True
        return super().eventFilter(source, event)

    def get_output_unit(self, property_name, system_row):
        units_list = self.UNIT_LABELS.get(property_name, ["?", "?", "?"])
        return units_list[system_row] if 0 <= system_row < len(units_list) else "?"

    def get_default_unit(self, property_name):
        return self.UNIT_LABELS.get(property_name, ["Unit"])[0]

    def remove_selected_history_item(self):
        selected_items = self.list_history.selectedItems()
        if selected_items:
            for item in selected_items:
                row = self.list_history.row(item)
                self.list_history.takeItem(row)

    def reset_and_update_ui_from_combo(self, index: int):
        self.line_edit_value.setText("")
        property_name = self.combo_properties.currentText()
        if property_name:
            self.reset_and_update_ui(property_name)

    def reset_and_update_ui(self, current_property: str):
        if current_property:
            default_unit = self.get_default_unit(current_property)
            html_unit = self.convert_to_html_unit(default_unit)
            self.label_source_unit.setText(html_unit)

            units = self.CATEGORY_UNITS.get(current_property, ["m,kg,s,K", "mm,N,s,K", "cm,g,s,K"])
            self.combo_source_system.blockSignals(True)
            self.combo_source_system.clear()
            self.combo_source_system.addItems(units)
            self.combo_source_system.blockSignals(False)

            for row in range(self.table_results.rowCount()):
                item_value = self.table_results.item(row, 1)
                item_scientific = self.table_results.item(row, 2)
                if item_value: item_value.setText("")
                if item_scientific: item_scientific.setText("")

                unit_label = self.table_results.cellWidget(row, 3)
                if isinstance(unit_label, QLabel):
                    default_output_unit_plain = self.get_output_unit(current_property, row)
                    html_unit = self.convert_to_html_unit(default_output_unit_plain)
                    unit_label.setText(html_unit)

    def add_to_history(self):
        selected_rows = self.table_results.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()

        try:
            property_name = self.combo_properties.currentText()
            source_value = self.line_edit_value.text()
            source_unit = self.get_default_unit(property_name)
            unit_system = self.table_results.item(row, 0).text()
            converted_value_item = self.table_results.item(row, 1)
            scientific_notation_item = self.table_results.item(row, 2)

            if not converted_value_item or not converted_value_item.text().strip():
                return

            converted_value = converted_value_item.text()
            scientific_notation = scientific_notation_item.text()
            output_unit = self.get_output_unit(property_name, row)

            history_entry = (
                f"{property_name} | {source_value} {source_unit} | "
                f"[{unit_system}] {converted_value} {output_unit} | "
                f" ({scientific_notation})"
            )

            for i in range(self.list_history.count()):
                if self.list_history.item(i).text() == history_entry:
                    return

            self.list_history.addItem(history_entry)
            self.list_history.scrollToBottom()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add to history: {e}")
            return

    def save_history(self):
        if self.list_history.count() == 0:
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save conversion history",
            "conversion_history.txt",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write("--- Conversion History ---\n")
                    f.write(f"Source Property: {self.combo_properties.currentText()}\n\n")
                    for i in range(self.list_history.count()):
                        f.write(self.list_history.item(i).text() + "\n")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file:\n{e}")

    def clear_history(self):
        self.list_history.clear()


if __name__ == '__main__':
    # Este bloque solo es para probar la UI individualmente.
    app = QApplication(sys.argv)
    locale_es = QLocale(QLocale.Spanish, QLocale.Spain)
    QLocale.setDefault(locale_es)

    window = UnitConverterUI()

    print("El conversor está funcionando con el tema por defecto de PySide6.")
    app.setStyleSheet("""
        QTableWidget::item { padding: 4px; }
        QPushButton { border-radius: 5px; }
    """)

    window.show()
    sys.exit(app.exec())