import asyncio

from TonTools import TonCenterClient, Wallet
from secret import testnet_api_key
from wallet import mnemonics, wallet_address, wallet

from tonsdk.contract.token.ft import JettonWallet
from tonsdk.utils import to_nano, Address

from pytonlib import TonlibClient

import requests
from pathlib import Path

async def get_client():
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=2, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


async def tontools_transfer():
    client = TonCenterClient(base_url='https://testnet.toncenter.com/api/v2/', key=testnet_api_key)
    wallet = Wallet(mnemonics=mnemonics, provider=client, version='v3r2')

    # await wallet.transfer_jetton(destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
    #                              jetton_master_address='EQDZADmMBA5A10sLWNssTjH-2FS8aix2UixT48Xt3j_g0G3S',
    #                              jettons_amount=1000)

    await wallet.transfer_jetton_by_jetton_wallet(destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
                                                  jetton_wallet='EQCzBogP_bYYIPydqqnej7TKp8Ui5HNJgLFczBZBj7MiZZFO',
                                                  jettons_amount=1500)


async def pytonlib_transfer():
    body = JettonWallet().create_transfer_body(
        to_address=Address('EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'),
        jetton_amount=to_nano(111, 'ton'),
    )

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr='EQCzBogP_bYYIPydqqnej7TKp8Ui5HNJgLFczBZBj7MiZZFO',
                                           amount=to_nano(0.05, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(pytonlib_transfer())
