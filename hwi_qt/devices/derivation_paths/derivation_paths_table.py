import json
from typing import Dict, Optional, List

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QAction, QMenu
from hwilib import commands

from hwi_qt.bitcoin_wallets import BitcoinWallets
from hwi_qt.devices.derivation_paths.derivation_path import DerivationPath
from hwi_qt.devices.device import Device
from hwi_qt.logging import log


class DerivationPathsTable(QTableWidget):
    def __init__(self, device: Device):
        self.device: Device = device
        self.derivation_paths: Dict[str, DerivationPath] = {}
        self.selected_derivation_path: Optional[DerivationPath] = None
        self.bitcoin_wallets: BitcoinWallets = BitcoinWallets()

        super().__init__(0, 6)
        self.setHorizontalHeaderLabels(
            [
                'Fingerprint',
                'Purpose',
                'Coin Type',
                'Account',
                'Is Change',
                'Path'
            ]
        )
        self.refresh()

        self.menu = QMenu(self)
        refresh_action = QAction('Refresh', self)
        refresh_action.triggered.connect(lambda event: self.refresh(event))
        self.menu.addAction(refresh_action)

        sync_with_bitcoin_action = QAction('Sync with Bitcoin', self)
        sync_with_bitcoin_action.triggered.connect(lambda: self.add_watch_only_to_bitcoin_wallet(
            self.selected_derivation_path))
        self.menu.addAction(sync_with_bitcoin_action)

    def handle_double_click(self, item):
        selected_row = item.row()
        path = self.item(selected_row, 5).text()
        self.selected_derivation_path = self.derivation_paths[path]
        self.show_transactions(self.selected_derivation_path)

    def show_transactions(self, derivation_path: DerivationPath):
        dialog = TransactionsDialog(self.parentWidget(), derivation_path)
        dialog.show()

    def add_watch_only_to_bitcoin_wallet(self, selected_derivation_path: DerivationPath):
        selected_derivation_path.add_watch_only_to_bitcoin_wallet()
        self.refresh()

    def add_derivation_path(self, derivation_path: DerivationPath):
        row_index = self.rowCount()
        self.insertRow(row_index)
        self.populate_row(row_index, derivation_path)

    def update_derivation_path(self, derivation_path: DerivationPath):
        for row_index in range(self.rowCount()):
            row_path = self.item(row_index, 5).text()
            if row_path == derivation_path.path:
                self.populate_row(row_index, derivation_path)

    def populate_row(self, row_index: int, derivation_path: DerivationPath):
        for column_index, cell_text in enumerate([
            derivation_path.fingerprint,
            derivation_path.purpose,
            derivation_path.coin_type,
            derivation_path.account,
            derivation_path.is_change,
            derivation_path.path
        ]):
            item = QTableWidgetItem()
            item.setText(str(cell_text) if cell_text is not None else '')
            item.setFlags(Qt.ItemFlags() ^ Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.setItem(row_index, column_index, item)

    def remove_derivation_path(self):
        pass

    def refresh(self, event=None):
        for derivation_path in self.device.get_derivation_paths():
            if derivation_path.path not in self.derivation_paths.keys():
                self.add_derivation_path(derivation_path)
                self.derivation_paths[derivation_path.path] = derivation_path
            else:
                self.update_derivation_path(derivation_path)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.resizeColumnsToContents()
