import sys

from PySide2.QtWidgets import QApplication, QMessageBox, QGridLayout, QDialog
from hwilib import commands, serializations
from hwilib.devices import trezor, ledger, coldcard

from hwi_qt.except_hook import except_hook
from hwi_qt.logging import log
from hwi_qt.selectable_text import SelectableText
from hwi_qt.sync_button import SyncButton

if __name__ == '__main__':
    devices = commands.enumerate()
    print(devices)

    sys.excepthook = except_hook

    log.info('Starting hwi-qt')
    app = QApplication(sys.argv)

    dialog = QDialog()
    dialog.layout = QGridLayout()

    for device in devices:
        name = device['type'] + '-' + device['fingerprint']
        text = SelectableText(name)
        dialog.layout.addWidget(text, 0, 0)

        button = SyncButton('Sync', 'Syncing...')
        dialog.layout.addLayout(button, 0, 1)

    dialog.setLayout(dialog.layout)

    dialog.show()

    sys.exit(app.exec_())
