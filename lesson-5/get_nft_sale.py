import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano, b64str_to_bytes
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.contract import Address
from tonsdk.boc import Cell, Slice

from ton.utils import read_address

import TonTools
from secret import mainnet_api_key

import requests
from pathlib import Path


async def tontools_get_data():
    client = TonTools.TonCenterClient(key=mainnet_api_key)

    item = TonTools.NftItem(data='EQApEyJpNAhozbidKYsNfU1cFwCm1X8-sl17Ijmu2JyiA_3A', provider=client)

    await item.update()

    print(item.sale)


async def get_client():
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=0, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_owner(client, address: str):
    stack = (await client.raw_run_method(address=address,
                                         method='get_nft_data', stack_data=[]))['stack']

    owner_address = Slice(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).read_msg_addr().to_string(True, True, True)

    return owner_address


def parse_sale_stack(stack):
    if stack[0][1] == '0x415543':
        return parse_auction_stack(stack)
    is_complete = bool(int(stack[1][1], 16))
    created_at = int(stack[2][1], 16)
    marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).to_string(True, True, True)
    nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes']))).to_string(True, True, True)
    nft_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[5][1]['bytes']))).to_string(True, True, True)
    full_price = int(stack[6][1], 16)

    return is_complete, created_at, marketplace_address, nft_address, nft_owner_address, full_price


def parse_auction_stack(stack):
    is_end = bool(int(stack[1][1], 16))
    end_time = int(stack[2][1], 16)
    marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).to_string(True, True, True)
    nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes']))).to_string(True, True, True)
    nft_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[5][1]['bytes']))).to_string(True, True, True)
    last_bid = int(stack[6][1], 16)
    min_bid = int(stack[16][1], 16)
    is_canceled = bool(int(stack[19][1], 16))
    return is_end, end_time, marketplace_address, nft_address, nft_owner_address, last_bid, min_bid, is_canceled


async def pytonlib_get_data():
    nft_address = 'EQApEyJpNAhozbidKYsNfU1cFwCm1X8-sl17Ijmu2JyiA_3A'
    client = await get_client()

    owner_address = await get_owner(client, nft_address)
    print(owner_address)
    input()
    response = await client.raw_run_method(address=owner_address,
                                         method='get_sale_data', stack_data=[])

    # print(response)

    if response['exit_code'] == 0:
        result = parse_sale_stack(response['stack'])
        print(result)

    await client.close()


if __name__ == '__main__':
    asyncio.run(pytonlib_get_data())
