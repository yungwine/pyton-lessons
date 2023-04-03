import asyncio

from pytonlib import TonlibClient
from pytonlib.utils.tlb import Transaction, Slice, Cell, deserialize_boc, CommentMessage, JettonInternalTransferMessage, JettonTransferNotificationMessage

from tonsdk.utils import b64str_to_bytes
from tonsdk.contract import Address

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


async def main():
    client = await get_client()
    trs = await client.get_transactions(account='EQB5DER03H1uhKGX6BJh_IWa_zV9MzvH2lcy6t30tZ9k4RSL', limit=4)

    for tr in trs:
        try:
            cell = deserialize_boc(b64str_to_bytes(tr['out_msgs'][0]['msg_data']['body']))
            result = JettonInternalTransferMessage(Slice(cell))
            print(result.amount)
        except:
            pass
        try:
            body = tr['in_msg']['msg_data']['body']
            cell = deserialize_boc(b64str_to_bytes(body))
            result = JettonTransferNotificationMessage(Slice(cell))
            sender_address = Address(str(result.sender.workchain_id) + ':' + str(result.sender.address)).to_string(True, True, True)
            print(result.amount, sender_address)
        except:
            pass


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())