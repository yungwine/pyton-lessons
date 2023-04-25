from tonsdk.contract.wallet import Wallets, WalletVersionEnum


mnemonics = ['sunny', 'damp', 'ten', 'easy', 'poet', 'visit', 'regret', 'oyster', 'surprise', 'play', 'output', 'service', 'artwork', 'team', 'pave', 'erase', 'board', 'sentence', 'young', 'mobile', 'priority', 'remain', 'flat', 'kangaroo']


mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v3r2, workchain=0)

wallet_address = wallet.address.to_string(True, True, True, True)

if __name__ == '__main__':
    print(wallet_address)  # kQAEC5wtm4vlNVhu_zP88QYjLRljcja_S8nXNt0fX0vtXcSp
