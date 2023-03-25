import asyncio

from TonTools import TonCenterClient, Wallet
from wallet_creation import mnemonics


async def main():
    provider = TonCenterClient(base_url='https://testnet.toncenter.com/api/v2/')
    wallet = Wallet(mnemonics=mnemonics, version='v3r2', provider=provider)

    await wallet.transfer_ton(destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
                              amount=0.01, message='hello from pyton lessons')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())