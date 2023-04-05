from tonsdk.contract.wallet import Wallets, WalletVersionEnum


mnemonics = ['always', 'crystal', 'grab', 'glance', 'cause', 'dismiss', 'answer', 'expose', 'once', 'session', 'tunnel', 'topic', 'defense', 'such', 'army', 'smile', 'exhibit', 'misery', 'runway', 'tone', 'want', 'primary', 'piano', 'language']


mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v3r2, workchain=0)

wallet_address = wallet.address.to_string(True, True, True, True)
