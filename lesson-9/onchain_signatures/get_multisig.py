import asyncio

from client import *

from tonsdk.utils import b64str_to_bytes
from tonsdk.boc import Cell, Slice
from tonsdk.contract.wallet import MultiSigWallet


async def get_multisig(client: TonlibClient, address:str):

    data = (await client.raw_get_account_state(address=address))['data']

    data_cell = Cell.one_from_boc(b64str_to_bytes(data))

    data_slice = data_cell.begin_parse()

    wallet_id = data_slice.read_uint(32)
    n, k = data_slice.read_uint(8), data_slice.read_uint(8)

    data_slice.read_uint(64)

    owners = read_dict(data_slice.load_dict(), 8)

    public_keys = []

    for i in owners:
        public_keys.append(owners[i].begin_parse().read_bytes(32))

    wallet = MultiSigWallet(public_keys=public_keys, k=k, wallet_id=wallet_id)

    return wallet


if __name__ == '__main__':
    asyncio.run(get_multisig())
