import asyncio

from wallet_creation import wallet, wallet_address
from make_message import make_message_body

from pathlib import Path
from pytonlib import TonlibClient

from tonsdk.utils import to_nano

import requests


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


async def main():
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=14, config=config, keystore=keystore_dir, tonlib_timeout=15)

    await client.init()

    seqno = await get_seqno(client, address=wallet_address)

    query = wallet.create_transfer_message(to_addr='kQDaglO5rQQF0eQe2E-kM_vsD7x6a2r8nMPdBYYIgxTkN1b_', amount=to_nano(0.01, 'ton'),
                                   seqno=seqno, payload=make_message_body())

    message = query['message'].to_boc(False)

    await client.raw_send_message(message)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
