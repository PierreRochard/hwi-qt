from PySide2.QtWidgets import QDialog, QGridLayout

from hwi_qt.devices.derivation_paths.derivation_paths_table import DerivationPathsTable
from hwi_qt.devices.device import Device


class DerivationPathsDialog(QDialog):
    def __init__(self, parent, device: Device):
        super().__init__(parent)
        self.layout = QGridLayout()
        self.table = DerivationPathsTable(device)
        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)

    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()
