from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt


class BatteryWidget(QWidget):
    """Simple widget que dibuja una batería con nivel de carga.

    API mínima ofrecida:
    - constructor: BatteryWidget(parent=None)
    - setLevel(int) -> establece 0..100 y llama a update()
    - paintEvent: dibuja la batería con color rojo si <20%, verde en otro caso
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._level = 50
        self.setMinimumSize(150, 50)

    def setLevel(self, val: int):
        self._level = max(0, min(100, int(val)))
        self.update()

    # Proporcionar también una alternativa con nombre distinto por compatibilidad
    def set_level(self, val: int):
        self.setLevel(val)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setPen(QPen(Qt.black, 2))
        # cuerpo de la batería
        p.drawRect(10, 10, 120, 30)
        # color según nivel
        color = QColor("red") if self._level < 20 else QColor("green")
        p.setBrush(QBrush(color))
        # ancho proporcional (aprox 1.16 px por % para llenar ~116 px a 100%)
        p.drawRect(12, 12, int(1.16 * self._level), 26)

    # Exponer lectura del nivel
    def level(self) -> int:
        return int(self._level)
