# 🌐 Unit Converter GUI
Una aplicación de escritorio creada con **Python + PySide6 (Qt)** para realizar conversiones precisas entre distintas unidades del sistema internacional y derivados, ideal para **ingenieros**, **científicos**, **estudiantes** o cualquier persona que trabaje con unidades técnicas.

## 🚀 Características

- ✅ Interfaz gráfica clara, responsiva y moderna (opcionalmente con tema oscuro vía `qt-material`)
- 🔁 Conversión de unidades en tiempo real mientras se escribe
- 📊 Soporte para múltiples categorías científicas:
  - Force
  - Pressure
  - Density
  - Thermal Conductivity
  - Specific heat
  - Young’s Modulus
  - Film Coefficient
  - Dynamic Viscosity
  - Elastic
  - Expansion
  - Stefan Boltzmann
- 🔣 Resultados en:
  - Formato numérico adaptado a la configuración local del sistema
  - Notación científica
-  Conversión entre diferentes sistemas técnicos:
  - `m, kg, s, K`
  - `mm, N, s, K`
  - `cm, g, s, K`
  
Es útil para estudiantes, ingenieros, científicos o cualquier persona que necesite realizar conversiones entre unidades científicas de forma rápida, clara y precisa.

---
## 🖥️ Interfaz de Usuario

La interfaz está dividida en los siguientes componentes:

### 🔘 Combo Box: **Categoría física**
- **Ubicación:** Esquina superior izquierda.
- **Función:** Permite seleccionar la categoría física que deseas convertir (por ejemplo, "Force", "Density", etc.).
- **Acción al cambiar:** Al seleccionar una nueva categoría:
  - Se limpia el campo de entrada.
  - Se actualizan las etiquetas de las unidades en la tabla de resultados.
  - Se reinician los sistemas de unidades disponibles.

---

### 📥 Campo de entrada: **Valor a convertir**
- **Función:** Introducir el valor numérico que deseas convertir.
- **Validación:**
  - Solo permite números positivos o negativos con coma o punto decimal, según la configuración regional del sistema operativo.
- **Atajo de teclado:** Puedes presionar `Tab` para saltar entre este campo y los combo boxes.

---

### 🌐 Combo Box: **Sistema de unidades origen**
- **Función:** Selecciona el sistema de unidades del valor que ingresaste.
- **Ejemplos de opciones:**
  - `"m,kg,s,K"` (Sistema Internacional)
  - `"mm,N,s,K"` (Sistema técnico)
  - `"cm,g,s,K"` (Sistema CGS)
- **Acción al cambiar:** Se recalculan automáticamente los valores convertidos en la tabla.

---

### 🧮 Tabla de resultados
- **Columnas:**
  1. **Sistema de destino** (ej. `"cm,g,s,K"`)
  2. **Valor convertido** (con formato regional y limpieza de ceros)
  3. **Notación científica** (ej. `1.23e+03`)
- **Filas:** Se corresponden con los distintos sistemas de unidades disponibles para la categoría seleccionada.

---

## 🔄 Conversión automática

La conversión ocurre automáticamente en los siguientes eventos:
- Cuando escribes/modificas un número en el campo de entrada.
- Cuando cambias la categoría física.
- Cuando cambias el sistema de unidades de origen.

---

## 🧠 Lógica de conversión

Se implementa una función central que:
- Toma la categoría, índice de unidad origen, índice de unidad destino y el valor a convertir.
- Devuelve el valor convertido, utilizando factores predefinidos.
- Es fácilmente extensible si deseas añadir más categorías o sistemas.

---
## 🎨 Estilo

Si tienes instalada la librería `qt-material`, se aplicará automáticamente el tema **Dark Teal** para mejorar la estética.

```python
from qt_material import apply_stylesheet
apply_stylesheet(app, theme='dark_teal.xml')
```
## 📦 Requisitos

- Python 3.7 o superior
- [PySide6](https://pypi.org/project/PySide6/)
- (Opcional) [qt-material](https://github.com/UN-GCPDS/qt-material) para el tema visual


