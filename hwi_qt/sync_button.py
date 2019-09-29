import json

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QVBoxLayout, QPushButton
from hwilib import commands

from bitcoin.rpc import Proxy
from bitcoin import SelectParams

from hwi_qt.logging import log

params = SelectParams('testnet')


class SyncButton(QVBoxLayout):
    def __init__(self, button_text: str, click_text: str,
                 device_fingerprint: str, device_type: str, device_path: str):
        super(SyncButton, self).__init__()
        self.button_text = button_text
        self.click_text = click_text
        self.device_fingerprint = device_fingerprint
        self.device_type = device_type
        self.device_path = device_path

        self.client = commands.get_client(self.device_type, self.device_path)
        if __debug__:
            self.client.is_testnet = True

        self.button = QPushButton(button_text)
        # noinspection PyUnresolvedReferences
        self.button.clicked.connect(self.action)
        self.addWidget(self.button)
        self.timer = QTimer(self.parentWidget())

    def create_core_wallet(self):
        client = Proxy()
        name = self.device_type + '-' + self.device_fingerprint
        try:
            client.call('loadwallet', name)
        except:
            pass
        if name not in client.call('listwallets'):
            client.call('createwallet', name, True)

    def action(self):
        # Action here
        self.button.setText(self.click_text)
        self.button.repaint()

        wallet_name = self.device_type + '-' + self.device_fingerprint
        client = Proxy(wallet=wallet_name, timeout=60000)

        self.create_core_wallet()

        purpose = 84
        coin_type = 0
        account = 0
        if __debug__:
            coin_type = 0

        external_keypool = commands.getkeypool(self.client,
                                               f'm/{purpose}h/{coin_type}h/{account}h/0/*',
                                               0, 1000,
                                               wpkh=True,
                                               internal=False,
                                               keypool=True)
        log.info('external_keypool', external_keypool=json.dumps(external_keypool))
        response_external = client.call('importmulti', external_keypool)
        log.info(json.dumps(response_external))

        change_keypool = commands.getkeypool(self.client,
                                             f'm/{purpose}h/{coin_type}h/{account}h/1/*',
                                             0, 1000, wpkh=True, internal=True,
                                             keypool=True)
        log.info('change_keypool', change_keypool=json.dumps(change_keypool))
        response_change = client.call('importmulti', change_keypool)
        log.info(json.dumps(response_change))
        self.timer.singleShot(1000, self.remove_text)

    def remove_text(self):
        self.button.setText(self.button_text)
        self.button.repaint()
