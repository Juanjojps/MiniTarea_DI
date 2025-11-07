from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal


class MoneyLineEdit(QLineEdit):
    """QLineEdit que emite `valueChanged(float)` cuando su texto representa un número.

    Acepta tanto punto como coma como separador decimal.
    """

    valueChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, txt):
        try:
            # Permitir coma como separador decimal
            val = float(txt.replace(",", "."))
            self.valueChanged.emit(val)
        except Exception:
            # Si no es convertible a float, ignorar
            pass