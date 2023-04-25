import asyncio

import bitarray
from pytonlib import TonlibClient

from tonsdk.utils import to_nano,bytes_to_b64str, b64str_to_bytes
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.boc import Slice, Cell

from tvm_valuetypes import deserialize_boc, parse_hashmap

from wallet import wallet, wallet_address, mnemonics

import requests
from pathlib import Path


mnemonics, pub_k, priv_k, hv_wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.hv2, workchain=0)


async def get_client():
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=5, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_config():
    client = await get_client()

    last_master_seqno = (await client.get_masterchain_info())['last']['seqno']

    config16 = (await client.get_config_param(config_id=16, seqno=last_master_seqno))['config']['bytes']

    config17 = (await client.get_config_param(config_id=17, seqno=last_master_seqno))['config']['bytes']

    config34 = (await client.get_config_param(config_id=34, seqno=last_master_seqno))['config']['bytes']

    parse16(config16)
    parse17(config17)
    parse34(config34)


    await client.close()


def parse16(b64str: str):

    cell = Cell.one_from_boc(b64str_to_bytes(b64str))

    slice = Slice(cell)

    max_validators = slice.read_uint(16)
    max_main_validators = slice.read_uint(16)
    min_validators = slice.read_uint(16)

    print({
        'max_validators':max_validators,
        'max_main_validators':max_main_validators,
        'min_validators':min_validators,
    })


def parse17(b64str: str):

    cell = Cell.one_from_boc(b64str_to_bytes(b64str))

    slice = Slice(cell)

    min_stake = slice.read_coins()
    max_stake = slice.read_coins()
    min_total_stake = slice.read_coins()

    print({
        'min_stake':min_stake/10**9,
        'max_stake':max_stake/10**9,
        'min_total_stake':min_total_stake/10**9,
    })


def parse34(b64str: str):

    cell = Cell.one_from_boc(b64str_to_bytes(b64str))

    slice = Slice(cell)

    slice.read_bits(8)

    t1 = slice.read_uint(32)
    t2 = slice.read_uint(32)
    total = slice.read_uint(16)
    main = slice.read_uint(16)

    print(t1,t2, total, main)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(get_config())
