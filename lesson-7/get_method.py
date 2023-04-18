import asyncio
import codecs

import bitarray
from pytonlib import TonlibClient

from ton.utils import read_address

from tonsdk.utils import to_nano, b64str_to_bytes
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.contract import Address
from tonsdk.boc import Cell, Slice

from tvm_valuetypes import deserialize_boc, parse_hashmap

import bitarray
from hashlib import sha256

import TonTools
from secret import mainnet_api_key

import requests
from pathlib import Path


async def tontools_get_data():
    client = TonTools.TonCenterClient(key=mainnet_api_key)

    jetton_minter = TonTools.Jetton(data='EQDCJL0iQHofcBBvFBHdVG233Ri2V4kCNFgfRT-gqAd3Oc86', provider=client)

    await jetton_minter.update()

    print(jetton_minter)


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

    stack = (await client.raw_run_method(address='EQDCJL0iQHofcBBvFBHdVG233Ri2V4kCNFgfRT-gqAd3Oc86',
                                         method='get_jetton_data', stack_data=[]))['stack']

    supply = int(stack[0][1], 16)

    admin_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[2][1]['bytes']))).to_string(True,True, True)

    content = parse_onchain_metadata(stack[3][1]['bytes'])

    print(supply,admin_address,content)

    await client.close()


def parse_offchain_metadata(b64str: str):
    content = Cell.one_from_boc(b64str_to_bytes(b64str)).bits.get_top_upped_array().decode().split('\x01')[-1]
    return content


def get_keys():
    metadata_keys = {}
    metadata = ['image', 'description', 'symbol']
    for i in metadata:
        array = bitarray.bitarray()
        array.frombytes(sha256(i.encode()).digest())
        metadata_keys[array.to01()] = i
    return metadata_keys


def parse_onchain_metadata(b64str: str):

    boc = codecs.decode(b64str_to_bytes(b64str).hex(), 'hex')

    cell = deserialize_boc(boc)

    result = {}

    parse_hashmap(cell.refs[0], 256, result, prefix=bitarray.bitarray(''))

    metadata_keys = get_keys()

    parsed_meta = {}

    for key in result:
        parsed_meta[metadata_keys.get(key)] = result[key].refs[0]

    print(parsed_meta)
    # print(result)
    # print(list(result.values())[0].refs[0])


if __name__ == '__main__':
    asyncio.run(pytonlib_get_data())
