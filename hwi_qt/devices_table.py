from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from hwilib import commands


class DevicesTable(QTableWidget):
    def __init__(self):

        super().__init__(0, 3)
        self.setHorizontalHeaderLabels(
            [
                'Type',
                'Model',
                'Fingerprint',
                'Needs Passphrase',
                'Device Path'
            ]
        )
        self.refresh()
        self.device_fingerprints = []

    def add_device(self, device):
        row_index = self.rowCount()
        self.insertRow(row_index)

        for column_index, cell_text in enumerate([
            device['type'],
            device['model'],
            device['fingerprint'],
            device['needs_passphrase'],
            device['path']
        ]):
            item = QTableWidgetItem()
            item.setText(str(cell_text) if cell_text is not None else '')

            if column_index != 2:
                item.setFlags(Qt.ItemFlags() ^ Qt.ItemIsEnabled)

            self.setItem(row_index, column_index, item)

    def remove_device(self):
        pass

    def refresh(self):
        devices = commands.enumerate()
        for device in devices:
            if device['fingerprint'] not in self.device_fingerprints:
                self.add_device(device)
