from typing import Dict, Optional

from PySide2.QtWidgets import QTableWidget

from hwi_qt.devices.derivation_paths.derivation_path import DerivationPath
from hwi_qt.devices.derivation_paths.transactions.transaction import Transaction


class TransactionsTable(QTableWidget):
    def __init__(self, derivation_path: DerivationPath):
        self.derivation_path: DerivationPath = derivation_path
        self.transactions: Dict[str, Transaction] = {}
        self.selected_transaction: Optional[Transaction] = None

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