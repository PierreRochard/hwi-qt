import sys

from PySide2.QtWidgets import QApplication, QMessageBox
from hwilib import commands, serializations
from hwilib.devices import trezor, ledger, coldcard

from hwi_qt.except_hook import except_hook
from hwi_qt.logging import log

if __name__ == '__main__':
    devices = commands.enumerate()
    print(devices)

    sys.excepthook = except_hook

    log.info('Starting hwi-qt')
    # Create the application object
    app = QApplication(sys.argv)

    # Create a simple dialog box
    msg_box = QMessageBox()
    output_text = ''
    for device in devices:
        name = device['type'] + '-' + device['fingerprint']
        output_text += name
    msg_box.setText(output_text)
    msg_box.show()

    sys.exit(app.exec_())
