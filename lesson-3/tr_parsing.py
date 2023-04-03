import asyncio

from pytonlib import TonlibClient
from pytonlib.utils.tlb import Transaction, Slice, Cell, deserialize_boc

from tonsdk.utils import b64str_to_bytes

import requests
from pathlib import Path


async def get_client():
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=0, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def main():
    client = await get_client()
    trs = await client.get_transactions(account='EQBvW8Z5huBkMJYdnfAEM5JqTNkuWX3diqYENkWsIL0XggGG', limit=10)

    for tr in trs:
        cell = deserialize_boc(b64str_to_bytes(tr['data']))
        tr_data = Transaction(Slice(cell))
        com_ph = tr_data.description.compute_ph
        act_ph = tr_data.description.action
        if com_ph.type == 'tr_phase_compute_vm':
            print('compute phase exit code is ', com_ph.exit_code)
        if act_ph is not None:
            print('action phase exit code is ',act_ph.result_code)

        print(tr)




if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())