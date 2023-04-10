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


async def pytonlib_burn():
    body = JettonWallet().create_burn_body(
        jetton_amount=to_nano(50000, 'ton')
    )

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr='EQCzBogP_bYYIPydqqnej7TKp8Ui5HNJgLFczBZBj7MiZZFO',
                                           amount=to_nano(0.05, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(pytonlib_burn())
