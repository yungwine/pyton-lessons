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

    stack = (await client.raw_run_method(address='EQC9QpdKuL0s5kNYdq-ELm-iFw4PUFX-l-FpHLQ12O_AbaPe',
                                         method='get_wallet_data', stack_data=[]))['stack']

    balance = int(stack[0][1], 16)

    owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[1][1]['bytes']))).to_string(True, True, True)
    minter_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[2][1]['bytes']))).to_string(True, True, True)

    print(balance, owner_address, minter_address)

    await client.close()



if __name__ == '__main__':
    asyncio.run(pytonlib_get_data())
