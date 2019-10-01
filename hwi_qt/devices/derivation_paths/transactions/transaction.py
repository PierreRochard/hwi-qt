import json

from hwilib import commands
from hwilib.hwwclient import HardwareWalletClient

from hwi_qt.bitcoin_wallets import BitcoinWallets
from hwi_qt.logging import log


class Transaction(object):
    def __init__(self, fingerprint: str, client: HardwareWalletClient, purpose: int, coin_type: int, account: int,
                 is_change: int):
        self.fingerprint = fingerprint
        self.client = client
        self.purpose = purpose
        self.coin_type = coin_type
        self.account = account
        self.is_change = is_change
        self.bitcoin_wallets: BitcoinWallets = BitcoinWallets()

        self.network = 'mainnet'
        if self.coin_type:
            self.network = 'testnet'
            self.client.is_testnet = True

    @property
    def path(self) -> str:
        return f'm/{self.purpose}h/{self.coin_type}h/{self.account}h/{self.is_change}/*'

    @property
    def wallet_name(self) -> str:
        return f'{self.fingerprint}-{self.purpose}-{self.coin_type}-{self.account}-{self.is_change}'

    def get_keypool_from_device(self):
        keypool = commands.getkeypool(self.client, self.path, 0, 100, wpkh=True, internal=bool(self.is_change),
                                      keypool=True)
        log.info('keypool', keypool=json.dumps(keypool))
        return keypool

    def add_watch_only_to_bitcoin_wallet(self):
        r = self.bitcoin_wallets.importmulti(self.network, self.wallet_name, self.get_keypool_from_device())
        return r
