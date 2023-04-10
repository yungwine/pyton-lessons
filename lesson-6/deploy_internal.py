import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from wallet import wallet, wallet_address

import requests
from pathlib import Path

from mint_bodies import create_state_init_jetton, increase_supply, change_owner


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


async def deploy_minter():

    state_init, jetton_address = create_state_init_jetton()

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=jetton_address,
                                   amount=to_nano(0.05, 'ton'), seqno=seqno, state_init=state_init)

    await client.raw_send_message(query['message'].to_boc(False))


async def mint_tokens():

    body = increase_supply()
    state_init, jetton_address = create_state_init_jetton()

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=jetton_address,
                                   amount=to_nano(0.05, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


async def change_admin():

    body = change_owner()
    state_init, jetton_address = create_state_init_jetton()

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=jetton_address,
                                   amount=to_nano(0.05, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(change_admin())
