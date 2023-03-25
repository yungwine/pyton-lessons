import asyncio

from wallet_creation import wallet, wallet_address
from make_message import make_message_body

from pathlib import Path
from pytonlib import TonlibClient

import requests
from ton.utils import read_address
from tonsdk.utils import b64str_to_bytes
from tonsdk.boc import Cell


async def main():
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=14, config=config, keystore=keystore_dir, tonlib_timeout=15)

    await client.init()

    data = await client.raw_run_method(address='kQDaglO5rQQF0eQe2E-kM_vsD7x6a2r8nMPdBYYIgxTkN1b_',
                                method='get_contract_storage_data', stack_data=[])

    stack = data['stack'][0][1], data['stack'][1][1]['bytes']

    counter_value = int(stack[0], 16)
    address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[1])))
    return counter_value, address.to_string(True, True, True, True)


if __name__ == '__main__':
    result = asyncio.get_event_loop().run_until_complete(main())
    while result[0] == 2:
        result = asyncio.get_event_loop().run_until_complete(main())
    print(result)
