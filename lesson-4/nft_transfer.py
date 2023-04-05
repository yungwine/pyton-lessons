import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from wallet import wallet, wallet_address, mnemonics
from mint_bodies import *


import requests
from pathlib import Path

from TonTools import TonCenterClient, Wallet


async def get_client():
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=2, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


async def transfer_nft():
    provider = TonCenterClient(base_url='https://testnet.toncenter.com/api/v2/')

    wallet = Wallet(mnemonics=mnemonics, version='v3r2', provider=provider)

    await wallet.transfer_nft(destination_address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
                              nft_address='EQDggDSP50itUg6EKnmD1uKthWU0Qq7my7u2nLYDHnqdRo3k', fee=0.1)


async def transfer_nft_pytonlib():
    body = NFTItem().create_transfer_body(new_owner_address=Address('EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'))

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr='EQDLuRLQetsm2GyLuYvr5YS1SJk79dDFhl3a-x_7LhfT3uCp',
                                           amount=to_nano(0.1, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(transfer_nft_pytonlib())

