from PySide2.QtWidgets import QDialog, QGridLayout

from hwi_qt.devices.derivation_paths.derivation_path import DerivationPath


class TransactionsDialog(QDialog):
    def __init__(self, parent, derivation_path: DerivationPath):
        super().__init__(parent)
        self.layout = QGridLayout()
        self.table = TransactionsTable(derivation_path)
        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)

    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()
