import asyncio

from ton import TonlibClient
from wallet_creation import wallet, wallet_address, mnemonics
from tonsdk.utils import to_nano


async def main():
    client = TonlibClient(config='https://ton.org/testnet-global.config.json', ls_index=11, verbosity_level=3)

    client.enable_unaudited_binaries()
    await client.init_tonlib(cdll_path='libtonlibjson.x86_64.dylib')

    wallet = await client.import_wallet(' '.join(mnemonics), wallet_id=698983191)

    await wallet.transfer(destination='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
                          amount=to_nano(0.01, 'ton'), comment='hello from pyton lessons', allow_send_to_uninited=True)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())