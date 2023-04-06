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

    item = TonTools.NftItem(data='EQCuLDZf-__TDCZN4Vo6Q4Fc4yj3xMsX6kkxeszzaFo4T1Ac', provider=client)

    await item.update()

    print(item)


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

    stack = (await client.raw_run_method(address='EQCuLDZf-__TDCZN4Vo6Q4Fc4yj3xMsX6kkxeszzaFo4T1Ac',
                                         method='get_nft_data', stack_data=[]))['stack']

    print(stack)

    index = int(stack[1][1], 16)

    collection_address = Address(Slice(Cell.one_from_boc(b64str_to_bytes(stack[2][1]['bytes']))).read_msg_addr()).to_string(True, True, True)

    owner_address = Address(Slice(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).read_msg_addr()).to_string(True, True, True)

    individual_content = Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]

    request_stack = [
        ["number", index],
        ["tvm.Cell", stack[4][1]['bytes']]
    ]

    collection_stack = (await client.raw_run_method(address='EQDvRFMYLdxmvY3Tk-cfWMLqDnXF_EclO2Fp4wwj33WhlNFT',
                                         method='get_nft_content', stack_data=request_stack))['stack']

    print(collection_stack)
    content = Cell.one_from_boc(b64str_to_bytes(collection_stack[0][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]
    content += individual_content
    metadata = requests.get(url=f'https://ipfs.io/ipfs/{content.split("ipfs://")[-1]}').json()

    print(index, collection_address, owner_address, content, metadata)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib_get_data())
