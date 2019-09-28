import json
from hwilib import commands
from hwilib.devices import coldcard
from subprocess import Popen, PIPE, check_output, run, CalledProcessError
import subprocess
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

class RPC:

    uri_template = "http://{user}:{password}@{host}:{port}/wallet/{wallet_name}"

    def __init__(self, rpc_settings, wallet_name='', timeout=10):
        self.uri = self.uri_template.format(**rpc_settings, wallet_name=wallet_name)
        self.timeout = timeout

    def __getattr__(self, name):
        '''Create new proxy for every call to prevent timeouts'''
        rpc = AuthServiceProxy(self.uri, timeout=self.timeout)
        return getattr(rpc, name)

rpc = RPC(dict(user='bitcoin', password='python', host='127.0.0.1', port='18332'))

def get_client(device):
    if device['type'] == 'ledger':
        client = ledger.LedgerClient(device['path'])
    elif device['type'] == 'coldcard':
        client = coldcard.ColdcardClient(device['path'])
    elif device['type'] == 'trezor':
        client = trezor.TrezorClient(device['path'])
    else:
        raise Exception(f'Devices of type "{device["type"]}" not yet supported')
    client.is_testnet = True
    return client




def get_keypool(device):
    client = get_client(device)
    kp = commands.getkeypool(client, 'm/10/*', 0, 100, internal=True, keypool=True, account=0, sh_wpkh=False, wpkh=True)
    print(kp)
    assert 'error' not in kp
    client.close()
    return kp

def create_core_wallet(device):
    name = device['type'] + '-' + device['fingerprint']
    try:
        rpc.loadwallet(name)
    except:
        pass
    if name not in rpc.listwallets():
        rpc.createwallet(name, True)

def sync_core_wallet(args):
    rpc.importmulti(args)

def sync_device(device):
    args = get_keypool(device)
    create_core_wallet(device)
    result = sync_core_wallet(args)
    print(rpc.getnewaddress())

def test():
    device = commands.enumerate()[0]
    sync_device(device)

    
if __name__ == '__main__':
    test()
