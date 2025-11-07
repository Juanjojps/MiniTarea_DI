import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PySide6.QtCore import Qt
from t3_batterywidget import BatteryWidget

class TestWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prueba QSlider - BatteryWidget")
        self.resize(300, 160)

        self.battery = BatteryWidget(self)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self._on_slider_changed)

        layout = QVBoxLayout(self)
        layout.addWidget(self.battery)
        layout.addWidget(self.slider)

        # inicializar el slider al nivel actual del widget battery si existe
        self.slider.setValue(self._read_level())

    def _read_level(self) -> int:
        b = self.battery
        # intentar varias convenciones de API posibles
        for attr in ("level", "getLevel", "get_level", "value", "getValue"):
            if hasattr(b, attr):
                try:
                    a = getattr(b, attr)
                    return int(a()) if callable(a) else int(a)
                except Exception:
                    pass
        return 0

    def _on_slider_changed(self, val: int):
        b = self.battery
        # intentar varias convenciones de API para ajustar el nivel
        if hasattr(b, "setLevel"):
            try: b.setLevel(val); return
            except Exception: pass
        if hasattr(b, "set_level"):
            try: b.set_level(val); return
            except Exception: pass
        if hasattr(b, "setValue"):
            try: b.setValue(val); return
            except Exception: pass
        # fallback: intentar asignar atributo
        try:
            setattr(b, "level", val)
        except Exception:
            pass

def main():
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
