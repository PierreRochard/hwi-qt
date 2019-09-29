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
        self.wallet_names: List[str] = []

        super().__init__(0, 7)
        self.setHorizontalHeaderLabels(
            [
                'Fingerprint',
                'Purpose',
                'Coin Type',
                'Account',
                'Is Change',
                'Has Wallet',
                'Path'
            ]
        )
        self.refresh()
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.resizeColumnsToContents()

        self.menu = QMenu(self)
        refresh_action = QAction('Refresh', self)
        refresh_action.triggered.connect(lambda event: self.refresh(event))
        self.menu.addAction(refresh_action)

        sync_with_bitcoin_action = QAction('Sync with Bitcoin', self)
        sync_with_bitcoin_action.triggered.connect(lambda: self.sync_with_bitcoin(self.selected_derivation_path))
        self.menu.addAction(sync_with_bitcoin_action)

    def sync_with_bitcoin(self, selected_derivation_path: DerivationPath):
        client = commands.get_client(self.device.type, self.device.path)
        network = 'mainnet'
        if selected_derivation_path.coin_type:
            network = 'testnet'
            client.is_testnet = True
        self.bitcoin_wallets.create_wallet(network=network, name=selected_derivation_path.wallet_name)
        keypool = commands.getkeypool(client, selected_derivation_path.path, 0, 1000, wpkh=True,
                                      internal=selected_derivation_path.is_change, keypool=True)
        log.info('keypool', keypool=json.dumps(keypool))
        r = self.bitcoin_wallets.importmulti(network, self.selected_derivation_path.wallet_name, keypool)
        log.info(json.dumps(r))
        self.refresh()

    def add_derivation_path(self, derivation_path: DerivationPath):
        row_index = self.rowCount()
        self.insertRow(row_index)
        self.populate_row(row_index, derivation_path)

    def update_derivation_path(self, derivation_path: DerivationPath):
        for row_index in range(self.rowCount()):
            row_path = self.item(row_index, 6).text()
            if row_path == derivation_path.path:
                self.populate_row(row_index, derivation_path)

    def populate_row(self, row_index: int, derivation_path: DerivationPath):
        for column_index, cell_text in enumerate([
            derivation_path.fingerprint,
            derivation_path.purpose,
            derivation_path.coin_type,
            derivation_path.account,
            derivation_path.is_change,
            derivation_path.wallet_name in self.wallet_names,
            derivation_path.path
        ]):
            item = QTableWidgetItem()
            item.setText(str(cell_text) if cell_text is not None else '')
            item.setFlags(Qt.ItemFlags() ^ Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.setItem(row_index, column_index, item)

    def remove_derivation_path(self):
        pass

    def refresh(self, event=None):
        self.wallet_names = self.bitcoin_wallets.get_wallet_names()
        for derivation_path in self.device.get_derivation_paths():
            if derivation_path.path not in self.derivation_paths.keys():
                self.add_derivation_path(derivation_path)
                self.derivation_paths[derivation_path.path] = derivation_path
            else:
                self.update_derivation_path(derivation_path)

    def contextMenuEvent(self, event):
        selected_row = self.rowAt(event.y())
        path = self.item(selected_row, 6).text()
        self.selected_derivation_path = self.derivation_paths[path]
        self.menu.popup(QCursor.pos())
