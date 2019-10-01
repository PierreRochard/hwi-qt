import json
from typing import List

from bitcoin.rpc import Proxy
from bitcoin import SelectParams

from hwi_qt.logging import log


class BitcoinWallets(object):
    def __init__(self):
        pass

    @staticmethod
    def get_wallet_names() -> List[str]:
        wallet_names = []
        for network in ['mainnet', 'testnet']:
            params = SelectParams(network)
            client = Proxy()
            wallet_names.extend(client.call('listwallets'))
        return wallet_names

    def create_wallet(self, network: str, name: str):
        params = SelectParams(network)
        client = Proxy()
        try:
            client.call('loadwallet', name)
        except:
            pass
        if name not in client.call('listwallets'):
            r = client.call('createwallet', name, True)
            return r

    def importmulti(self, network: str, wallet_name: str, keypool):
        params = SelectParams(network)
        self.create_wallet(network, wallet_name)
        client = Proxy(wallet=wallet_name)
        log.info('importmulti', keypool=keypool)
        r = client.call('importmulti', keypool)
        log.info(json.dumps(r))
        return r
