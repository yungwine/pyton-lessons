import asyncio

import bitarray
from pytonlib import TonlibClient
from tonsdk.boc import Cell
import json
from TonTools import TonCenterClient
import requests
from pathlib import Path

from tvm_valuetypes import deserialize_boc, parse_hashmap


async def get_client() -> TonlibClient:

    with open('my_config.json') as f:
        config = json.loads(f.read())

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=0, config=config, keystore=keystore_dir, tonlib_timeout=10)
    await client.init()

    return client


async def main():
    # client = await get_client()
    client = TonCenterClient(base_url='http://94.103.85.17/')
    print(await client.get_balance(address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'))
    # print(await client.get_masterchain_info())

    # await client.close()




if __name__ == '__main__':
    asyncio.run(main())
