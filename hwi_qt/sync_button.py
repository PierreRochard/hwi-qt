from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QVBoxLayout, QPushButton


class SyncButton(QVBoxLayout):
    def __init__(self, button_text: str, click_text: str):
        super(SyncButton, self).__init__()
        self.button_text = button_text
        self.click_text = click_text
        self.button = QPushButton(button_text)
        # noinspection PyUnresolvedReferences
        self.button.clicked.connect(self.action)
        self.addWidget(self.button)
        self.timer = QTimer(self.parentWidget())

    def action(self):
        # Action here
        self.button.setText(self.click_text)
        self.button.repaint()
        self.timer.singleShot(1000, self.remove_text)

    def remove_text(self):
        self.button.setText(self.button_text)
        self.button.repaint()
