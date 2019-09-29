import sys

from PySide2.QtWidgets import QApplication

from hwi_qt.except_hook import except_hook
from hwi_qt.logging import log
from hwi_qt.main_dialog import MainDialog

if __name__ == '__main__':
    # sys.excepthook = except_hook

    log.info('Starting hwi-qt')
    app = QApplication(sys.argv)

    dialog = MainDialog()
    dialog.show()

    sys.exit(app.exec_())
