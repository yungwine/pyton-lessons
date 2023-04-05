import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from wallet import wallet, wallet_address
from mint_bodies import *

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


async def deploy_collection():

    collection = create_collection_mint()
    state_init = collection.create_state_init()['state_init']

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=collection.address.to_string(),
                                   amount=to_nano(0.05, 'ton'), seqno=seqno, state_init=state_init)

    await client.raw_send_message(query['message'].to_boc(False))


async def deploy_one_item():
    body = create_nft_mint()
    collection = create_collection_mint()

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=collection.address.to_string(),
                                   amount=to_nano(0.04, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


async def deploy_batch_items():
    body = create_batch_nft_mint()
    collection = create_collection_mint()

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=collection.address.to_string(),
                                   amount=to_nano(0.2, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(deploy_batch_items())
