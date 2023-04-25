import asyncio

import bitarray
from pytonlib import TonlibClient

from tonsdk.utils import to_nano,bytes_to_b64str
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.boc import Slice

from tvm_valuetypes import deserialize_boc, parse_hashmap

from wallet import wallet, wallet_address, mnemonics

import requests
from pathlib import Path


mnemonics, pub_k, priv_k, hv_wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.hv2, workchain=0)


async def get_client():
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=5, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


async def deploy():
    client = await get_client()

    state_init = hv_wallet.create_state_init()['state_init']

    query = wallet.create_transfer_message(to_addr=hv_wallet.address.to_string(), amount=to_nano(1, 'ton'), state_init=state_init,
                                   seqno=await get_seqno(client, wallet_address))

    await client.raw_send_message(query['message'].to_boc(False))


async def transfer():

    recipes = [
        {
            'address': 'EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
            'amount': to_nano(0.0001, 'ton'),
            'payload': 'comment1',
            'send_mode': 3
        },
        {
            'address': 'EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT',
            'amount': to_nano(0.0001, 'ton'),
            'payload': 'comment2',
            'send_mode': 3
        },
    ] * 10

    query = hv_wallet.create_transfer_message(recipients_list=recipes, query_id=0)

    query_id = query['query_id']
    print(query_id)
    client = await get_client()

    await client.raw_send_message(query['message'].to_boc(False))


async def get_query():
    client = await get_client()
    stack = (await client.raw_run_method(method='processed?', address=hv_wallet.address.to_string(), stack_data=[["num", 7225272436650934272]]))['stack']
    result = int(stack[0][1], 16)
    print(result)

    stack = (await client.raw_run_method(method='processed?', address=hv_wallet.address.to_string(),
                                         stack_data=[["num", 7225273321414197248]]))['stack']
    result = int(stack[0][1], 16)
    print(result)


def dict():

    recipes = [
                  {
                      'address': 'EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
                      'amount': to_nano(0.0001, 'ton'),
                      'payload': 'comment1',
                      'send_mode': 2
                  },
                  {
                      'address': 'EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT',
                      'amount': to_nano(0.0001, 'ton'),
                      'payload': 'comment2',
                      'send_mode': 3
                  },
              ] * 10

    query = hv_wallet.create_transfer_message(recipients_list=recipes, query_id=0)

    signing_message = query['signing_message']

    # print(signing_message)

    slice = Slice(signing_message)

    slice.read_bits(32 + 64)

    dict_cell = slice.load_dict()
    # print(dict_cell)

    cell = deserialize_boc(dict_cell.to_boc())

    # print(cell)

    result = {}

    parse_hashmap(cell, 16, result, bitarray.bitarray(''))

    print(len(result), result)

    print(result['0000000000000000'].refs[0])


if __name__ == '__main__':
    dict()
    # asyncio.get_event_loop().run_until_complete(get_query())
