from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QToolButton

class SearchInput(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        self.text = QLineEdit(placeholderText="Buscar…")
        self.btn = QToolButton(text="✖")
        self.btn.clicked.connect(self.text.clear)
        layout.addWidget(self.text)
        layout.addWidget(self.btn)