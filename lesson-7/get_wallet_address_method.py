import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano, b64str_to_bytes, bytes_to_b64str
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.contract import Address
from tonsdk.boc import Cell, Slice,begin_cell

from ton.utils import read_address

import TonTools
from secret import mainnet_api_key

import requests
from pathlib import Path


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

    cell = begin_cell().store_address(Address('EQBvW8Z5huBkMJYdnfAEM5JqTNkuWX3diqYENkWsIL0XggGG')).end_cell()

    print(bytes_to_b64str(cell.to_boc()))

    request_stack = [
        ["tvm.Slice", bytes_to_b64str(cell.to_boc())]
    ]

    response = await client.raw_run_method(address='EQDCJL0iQHofcBBvFBHdVG233Ri2V4kCNFgfRT-gqAd3Oc86',
                                         method='get_wallet_address', stack_data=request_stack)

    print(response)

    addr_boc = response['stack'][0][1]['bytes']

    address = read_address(Cell.one_from_boc(b64str_to_bytes(addr_boc))).to_string(True, True, True)

    print(address)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib_get_data())
