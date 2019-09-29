from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from hwilib import commands


class DevicesTable(QTableWidget):
    def __init__(self):
        self.device_fingerprints = []

        super().__init__(0, 8)
        self.setHorizontalHeaderLabels(
            [
                'Type',
                'Model',
                'Fingerprint',
                'Needs Passphrase',
                'Needs Pin',
                'Device Path',
                'Error',
                'Code'
            ]
        )
        self.refresh()
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.resizeColumnsToContents()

    def add_device(self, device):
        row_index = self.rowCount()
        self.insertRow(row_index)

        for column_index, cell_text in enumerate([
            device['type'],
            device['model'],
            device.get('fingerprint', None),
            device.get('needs_passphrase', None) or device.get('needs_passphrase_sent', None),
            device.get('needs_pin_sent', None),
            device['path'],
            device.get('error'),
            device.get('code')
        ]):
            item = QTableWidgetItem()
            item.setText(str(cell_text) if cell_text is not None else '')
            item.setFlags(Qt.ItemFlags() ^ Qt.ItemIsEnabled)
            self.setItem(row_index, column_index, item)

        # devices = commands.enumerate()
        # for device in devices:
            # name = device['type'] + '-' + device['fingerprint']
            # text = SelectableText(name)
            # self.layout.addWidget(text, 1, 0)

            # button = SyncButton('Sync', 'Syncing...', device['fingerprint'],
            #                     device['type'], device['path'])
            # self.layout.addLayout(button, 1, 1)

    def remove_device(self):
        pass

    def refresh(self):
        devices = commands.enumerate()
        for device in devices:
            if device.get('fingerprint', None) not in self.device_fingerprints:
                self.add_device(device)
