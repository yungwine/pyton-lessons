import bitarray
from pytonlib import TonlibClient
from tonsdk.boc import Cell

import requests
from pathlib import Path

from tvm_valuetypes import deserialize_boc, parse_hashmap


async def get_client(ls_index: int, testnet: bool) -> TonlibClient:
    if testnet:
        url = 'https://ton.org/testnet-global.config.json'
    else:
        url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=ls_index, config=config, keystore=keystore_dir, tonlib_timeout=10)
    await client.init()

    return client


async def get_seqno(client: TonlibClient, address: str) -> int:
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


async def run_get_method(client: TonlibClient, address: str, method: str, stack: list) -> list:
    response = await client.raw_run_method(method=method, address=address,
                                           stack_data=stack)

    if response['exit_code'] != 0:
        raise Exception(f'get method exit code is {response["exit_code"]}')

    stack = response['stack']

    return stack


def read_dict(dict_cell: Cell, key_len: int) -> dict:
    cell = deserialize_boc(dict_cell.to_boc())

    result = {}

    parse_hashmap(cell, key_len, result, bitarray.bitarray(''))

    for i in result:
        result[i] = Cell.one_from_boc(result[i].serialize_boc())

    return result
