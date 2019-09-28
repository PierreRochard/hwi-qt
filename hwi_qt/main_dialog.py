from PySide2.QtWidgets import QDialog, QGridLayout
from hwilib import commands

from hwi_qt.selectable_text import SelectableText
from hwi_qt.sync_button import SyncButton


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        devices = commands.enumerate()
        for device in devices:
            name = device['type'] + '-' + device['fingerprint']
            text = SelectableText(name)
            self.layout.addWidget(text, 0, 0)

            button = SyncButton('Sync', 'Syncing...', device['fingerprint'],
                                device['type'], device['path'])
            self.layout.addLayout(button, 0, 1)

        self.setLayout(self.layout)
