import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt

# IMPORTANTE: importar recursos_rc antes de cargar la UI
import recursos_rc

from t2_moneylineedit import MoneyLineEdit
from t3_batterywidget import BatteryWidget
from t4_searchinput import SearchInput

def main() -> int:
    """Cargar la interfaz y ejecutar la aplicación."""
    global w, loader  # necesario para que las funciones open_tX_window() accedan a w y loader
    app = QApplication(sys.argv)
    loader = QUiLoader()

    # Cargar ventana principal
    ui_file = QFile("ui/CustomWidgetsCompany.ui")
    if not ui_file.open(QFile.ReadOnly):
        print("Error: no se pudo abrir 'ui/CustomWidgetsCompany.ui'")
        return 1

    try:
        w = loader.load(ui_file)
    finally:
        ui_file.close()

    if w is None:
        print("Error: no se pudo cargar la interfaz")
        return 1
    
    # Conectar botones a sus funciones
    try:
        w.btnT1.clicked.connect(open_t1_window)
        w.btnT2.clicked.connect(open_t2_window)  
        w.btnT3.clicked.connect(open_t3_window)
        w.btnT4.clicked.connect(open_t4_window)
    except Exception as e:
        print("Warning: algún botón no se pudo conectar:", e)
    
    # Establecer mensaje en la barra de estado
    w.statusBar().showMessage("Listo")
    
    # Mostrar ventana principal y ejecutar la aplicación
    w.show()
    return app.exec()

# Mantener referencias a ventanas secundarias para evitar que el GC las cierre
open_windows = []


def open_t1_window():
	"""Abrir la ventana de la Tarea 1 cargando `ui/t1_switch.ui` y configurar el switch."""
	ui_f = QFile("ui/t1_switch.ui")
	if not ui_f.open(QFile.ReadOnly):
		print("No se pudo abrir 'ui/t1_switch.ui'")
		return
	try:
		t1 = loader.load(ui_f)
	finally:
		ui_f.close()

	if t1 is None:
		print("Error cargando 't1_switch.ui'")
		return

	# aplicar estilo al checkbox y conectar toggle
	try:
		chk = t1.findChild(object, "chkSwitch")
		# findChild devuelve cualquier QObject; si preferimos explícito:
		# from PySide6.QtWidgets import QCheckBox
		# chk = t1.findChild(QCheckBox, "chkSwitch")
		if chk is not None:
			chk.setStyleSheet("""
QCheckBox::indicator { width: 46px; height: 24px; }
QCheckBox::indicator:unchecked { border-radius: 12px; background:#ccc; }
QCheckBox::indicator:checked { border-radius: 12px; background:#2ecc71; }
""")
			chk.toggled.connect(lambda s: chk.setText("ON" if s else "OFF"))
	except Exception:
		# no bloquear si algo falla; la ventana igualmente se mostrará
		pass

	t1.show()
	open_windows.append(t1)


# conectar el botón de la ventana principal
try:
	w.btnT1.clicked.connect(open_t1_window)
except Exception:
	# Si la UI principal no tiene btnT1, no hacemos nada
	pass


def open_t2_window():
	"""Abrir ventana de la Tarea 2 (MoneyLineEdit + QLabel), igual que en main_t2.py."""
	try:
		w2 = QWidget()
		layout = QVBoxLayout(w2)
		txt = MoneyLineEdit()
		lbl = QLabel("Valor:")
		txt.valueChanged.connect(lambda v: lbl.setText(f"Valor: {v:.2f} €"))
		layout.addWidget(txt)
		layout.addWidget(lbl)
		w2.show()
		open_windows.append(w2)
	except Exception as e:
		print("Error abriendo ventana T2:", e)


# conectar el botón de la ventana principal para Tarea 2
try:
	w.btnT2.clicked.connect(open_t2_window)
except Exception:
	pass

def open_t3_window():
	"""Abrir la ventana de la Tarea 3 (BatteryWidget + QSlider), igual que en main_t3.py."""
	try:
		w3 = QWidget()
		w3.setWindowTitle("Prueba QSlider - BatteryWidget")
		w3.resize(300, 160)

		battery = BatteryWidget()

		slider = QSlider(Qt.Horizontal, w3)
		slider.setRange(0, 100)
		slider.setTickPosition(QSlider.TicksBelow)
		slider.setTickInterval(10)

		def _read_level() -> int:
			# intentar varias convenciones de API posibles
			b = battery
			for attr in ("level", "getLevel", "get_level", "value", "getValue"):
				if hasattr(b, attr):
					try:
						a = getattr(b, attr)
						return int(a()) if callable(a) else int(a)
					except Exception:
						pass
			return 0

		def _on_slider_changed(val: int):
			b = battery
			# intentar varias convenciones de API para ajustar el nivel
			if hasattr(b, "setLevel"):
				try:
					b.setLevel(val)
					return
				except Exception:
					pass
			if hasattr(b, "set_level"):
				try:
					b.set_level(val)
					return
				except Exception:
					pass
			if hasattr(b, "setValue"):
				try:
					b.setValue(val)
					return
				except Exception:
					pass
			# fallback: intentar asignar atributo
			try:
				setattr(b, "level", val)
			except Exception:
				pass

		slider.valueChanged.connect(_on_slider_changed)

		layout = QVBoxLayout(w3)
		layout.addWidget(battery)
		layout.addWidget(slider)

		# inicializar el slider al nivel actual del widget battery si existe
		slider.setValue(_read_level())

		w3.show()
		open_windows.append(w3)
	except Exception as e:
		print("Error abriendo ventana T3:", e)


# conectar el botón de la ventana principal para Tarea 3
try:
	w.btnT3.clicked.connect(open_t3_window)
except Exception:
	pass


def open_t4_window():
	"""Abrir la ventana de la Tarea 4 (SearchInput + QLabel), igual que en main_t4.py."""
	try:
		w4 = QWidget()
		v = QVBoxLayout(w4)
		s = SearchInput()
		lbl = QLabel("0 caracteres")
		# conectar el QLineEdit interno (atributo .text) a la etiqueta
		try:
			s.text.textChanged.connect(lambda t: lbl.setText(f"{len(t)} caracteres"))
		except Exception:
			# si la API del widget cambia, intentar detectar un QLineEdit hijo
			try:
				le = s.findChild(object, "text")
				if le is not None:
					le.textChanged.connect(lambda t: lbl.setText(f"{len(t)} caracteres"))
			except Exception:
				pass

		v.addWidget(s)
		v.addWidget(lbl)
		w4.show()
		open_windows.append(w4)
	except Exception as e:
		print("Error abriendo ventana T4:", e)


# conectar el botón de la ventana principal para Tarea 4
try:
	w.btnT4.clicked.connect(open_t4_window)
except Exception:
	pass

  
# Ejecutar la aplicación
if __name__ == "__main__":
    sys.exit(main())