

class DerivationPath(object):
    def __init__(self, fingerprint: str, purpose: int, coin_type: int, account: int, is_change: int):
        self.fingerprint = fingerprint
        self.purpose = purpose
        self.coin_type = coin_type
        self.account = account
        self.is_change = is_change

    @property
    def path(self) -> str:
        return f'm/{self.purpose}h/{self.coin_type}h/{self.account}h/{self.is_change}/*'

    @property
    def wallet_name(self) -> str:
        return f'{self.fingerprint}-{self.purpose}-{self.coin_type}-{self.account}-{self.is_change}'
