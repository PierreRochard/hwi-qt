from typing import List

from bitcoin.rpc import Proxy
from bitcoin import SelectParams


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