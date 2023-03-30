import asyncio
import random

from pytonlib import TonlibClient


from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

import requests
from pathlib import Path


async def archive_ls():
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    for index in range(len(config['liteservers'])):

        client = TonlibClient(ls_index=index, config=config, keystore=keystore_dir, tonlib_timeout=10)

        await client.init()

        try:
            print(await client.lookup_block(0, -9223372036854775808, random.randint(2, 4096)))
            print(index)
        except:
            pass


async def transactions():
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=2, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    await client.get_transactions(account='EQAMoPBaaE_ud88pid9_AW7hjWVz6hWfOXwmJtAdSXq4putF', limit=100)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(transactions())