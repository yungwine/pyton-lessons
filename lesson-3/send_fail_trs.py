import asyncio

from TonTools import Wallet, TonApiClient
from secret import mnemonics


async def main():
    client = TonApiClient()
    wallet = Wallet(mnemonics=mnemonics, provider=client)

    # print(await wallet.get_seqno())
    # await wallet.transfer_ton(destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N', amount=100, send_mode=2)

    print('\n'.join(list(map(str, (await wallet.get_transactions(10))))))

if __name__ == '__main__':
    asyncio.run(main())

