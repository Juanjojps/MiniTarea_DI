from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from t4_searchinput import SearchInput
import sys

app = QApplication(sys.argv)
w = QWidget(); 
v = QVBoxLayout(w)
s = SearchInput(); 
lbl = QLabel("0 caracteres")
s.text.textChanged.connect(lambda t: lbl.setText(f"{len(t)} caracteres"))
v.addWidget(s); 
v.addWidget(lbl)
w.show(); 
app.exec()