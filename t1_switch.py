from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

import sys
 
app = QApplication(sys.argv)
loader = QUiLoader()
ui_file = QFile("ui/t1_switch.ui")
ui_file.open(QFile.ReadOnly)
w = loader.load(ui_file)
ui_file.close()

w.chkSwitch.setStyleSheet("""
QCheckBox::indicator { width: 46px; height: 24px; }
QCheckBox::indicator:unchecked { border-radius: 12px; background:#ccc; }
QCheckBox::indicator:checked { border-radius: 12px; background:#2ecc71; }
""")

w.chkSwitch.toggled.connect(lambda s: w.chkSwitch.setText("ON" if s else "OFF"))

w.show()
app.exec()