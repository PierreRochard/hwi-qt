from typing import Dict, Optional

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from hwilib import commands

from hwi_qt.devices.derivation_paths.derivation_paths_dialog import DerivationPathsDialog
from hwi_qt.devices.device import Device


class DevicesTable(QTableWidget):
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.selected_device: Optional[Device] = None

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

        self.itemDoubleClicked.connect(self.handle_double_click)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.refresh()
        self.timer.start(10000)

    def handle_double_click(self, item):
        selected_row = item.row()
        path = self.item(selected_row, 5).text()
        self.selected_device = self.devices[path]
        self.show_derivation_paths(self.selected_device)

    def show_derivation_paths(self, device: Device):
        dialog = DerivationPathsDialog(self.parentWidget(), device)
        dialog.show()

    def add_device(self, device: Device):
        row_index = self.rowCount()
        self.insertRow(row_index)
        self.populate_row(row_index, device)

    def update_device(self, device: Device):
        for row_index in range(self.rowCount()):
            row_path = self.item(row_index, 5).text()
            if row_path == device.path:
                self.populate_row(row_index, device)

    def populate_row(self, row_index: int, device: Device):
        for column_index, cell_text in enumerate([
            device.type,
            device.model,
            device.fingerprint,
            device.needs_passphrase,
            device.needs_pin,
            device.path,
            device.error,
            device.code
        ]):
            item = QTableWidgetItem()
            item.setText(str(cell_text) if cell_text is not None else '')
            item.setFlags(Qt.ItemFlags() ^ Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.setItem(row_index, column_index, item)

    def remove_device(self):
        pass

    def refresh(self):
        devices_data = commands.enumerate()
        for device_data in devices_data:
            device = Device(device_data=device_data)
            if device.path not in self.devices.keys():
                self.add_device(device)
                self.devices[device.path] = device
            else:
                self.update_device(device)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.resizeColumnsToContents()
