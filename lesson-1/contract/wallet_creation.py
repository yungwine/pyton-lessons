from tonsdk.contract.wallet import Wallets, WalletVersionEnum


mnemonics = ['early', 'claw', 'echo', 'energy', 'erase', 'damp', 'expire', 'brush', 'scrub', 'ripple', 'skirt', 'beach', 'club', 'believe', 'firm', 'rely', 'head', 'neck', 'doll', 'punch', 'domain', 'phone', 'render', 'dad']

mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v3r2, workchain=0)

wallet_address = wallet.address.to_string(True, True, True, True)

if __name__ == '__main__':
    print(mnemonics)
    print(wallet.address.to_string(True, True, True, True))
