from PySide2.QtWidgets import QDialog, QGridLayout

from hwi_qt.devices_table import DevicesTable


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.devices_table = DevicesTable()
        self.layout.addWidget(self.devices_table, 0, 0)
        self.setLayout(self.layout)
