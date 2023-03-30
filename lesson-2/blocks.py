import asyncio
import random

from pytonlib import TonlibClient


from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

import requests
from pathlib import Path


async def get_client(index):
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=index, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_block_transactions(client: TonlibClient, wc, shard, seqno):
    return (await client.get_block_transactions(workchain=wc, shard=shard, seqno=seqno, count=40))['transactions']


async def main():
    client = await get_client(11)

    last_master_block = (await client.get_masterchain_info())['last']

    # print(last_master_block)

    base_data = (await client.get_shards(master_seqno=last_master_block['seqno']))['shards'][0]

    base_shard = base_data['shard']
    base_seqno = base_data['seqno']

    transactions = await get_block_transactions(client, 0, base_shard, base_seqno)

    for tr in transactions:
        full_tr = (await client.get_transactions(account=tr['account'], from_transaction_lt=tr['lt'], from_transaction_hash=tr['hash']))[0]
        print(full_tr)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())