import sys

from PySide2.QtWidgets import QApplication

from hwi_qt.logging import log
from hwi_qt.devices.devices_dialog import DevicesDialog

if __name__ == '__main__':
    # sys.excepthook = except_hook

    log.info('Starting hwi-qt')
    app = QApplication(sys.argv)

    dialog = DevicesDialog()
    dialog.show()

    sys.exit(app.exec_())
