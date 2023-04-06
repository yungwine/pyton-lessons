import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano, b64str_to_bytes
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.contract import Address
from tonsdk.boc import Cell, Slice


import TonTools
from secret import mainnet_api_key

import requests
from pathlib import Path


async def tontools_get_data():
    client = TonTools.TonCenterClient(key=mainnet_api_key)

    collection = TonTools.NftCollection(data='EQDvRFMYLdxmvY3Tk-cfWMLqDnXF_EclO2Fp4wwj33WhlNFT', provider=client)

    await collection.update()

    print(collection)


async def get_client():
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=2, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def pytonlib_get_data():
    client = await get_client()

    stack = (await client.raw_run_method(address='EQDvRFMYLdxmvY3Tk-cfWMLqDnXF_EclO2Fp4wwj33WhlNFT',
                                         method='get_collection_data', stack_data=[]))['stack']

    next_item_index = int(stack[0][1], 16)

    content = Cell.one_from_boc(b64str_to_bytes(stack[1][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]

    owner_address = Address(Slice(Cell.one_from_boc(b64str_to_bytes(stack[2][1]['bytes']))).read_msg_addr()).to_string(True, True, True)

    content = requests.get(url=f'https://ipfs.io/ipfs/{content.split("ipfs://")[-1]}').json()

    await client.close()
    return next_item_index, content, owner_address


async def pytonlib_get_royalty():
    client = await get_client()

    stack = (await client.raw_run_method(address='EQDvRFMYLdxmvY3Tk-cfWMLqDnXF_EclO2Fp4wwj33WhlNFT',
                                         method='royalty_params', stack_data=[]))['stack']

    print(stack)

    royalty_factor = int(stack[0][1], 16)
    royalty_base = int(stack[1][1], 16)

    royalty = royalty_factor / royalty_base

    royalty_address = Address(Slice(Cell.one_from_boc(b64str_to_bytes(stack[2][1]['bytes']))).read_msg_addr()).to_string(True, True, True)

    print(royalty, royalty_address)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib_get_royalty())