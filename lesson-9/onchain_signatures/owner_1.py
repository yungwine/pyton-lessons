import asyncio

from tonsdk.boc._bit_string import BitString
from tonsdk.contract.wallet import MultiSigWallet, MultiSigOrder, MultiSigOrderBuilder
from tonsdk.crypto import mnemonic_new, mnemonic_to_wallet_key
from tonsdk.utils import Address, bytes_to_b64str, b64str_to_bytes, to_nano, sign_message
from tonsdk.boc import Cell
from client import *
from get_multisig import get_multisig

mnemonics1 = ['rather', 'voice', 'zone', 'fold', 'rotate', 'crane', 'roast', 'brave', 'motor', 'kid', 'note',
              'squirrel', 'piece', 'home', 'expose', 'bench', 'flame', 'wood', 'person', 'assist', 'vocal', 'bomb',
              'dismiss', 'diesel']

pub_k1, priv_k1 = mnemonic_to_wallet_key(mnemonics1)


async def main():
    client = await get_client(0, testnet=False)

    stack = await run_get_method(client, method='get_messages_unsigned_by_id',
                                 address='EQCOpgZNmHhDe4nuZY6aQh3sgqgwgTBtCL4kZPYTDTDlZY_Y', stack=[["num", 1]])

    print(stack)
    # 7228136655851356160

    dict_cell = Cell.one_from_boc(b64str_to_bytes(stack[0][1]['bytes']))
    result = read_dict(dict_cell=dict_cell, key_len=64)

    print(len(result))

    message = result['0110010001001111011111111111111000000000000000000000000000000000']

    message: Cell

    wallet = await get_multisig(client, 'EQCOpgZNmHhDe4nuZY6aQh3sgqgwgTBtCL4kZPYTDTDlZY_Y')

    order1 = MultiSigOrderBuilder(wallet.options["wallet_id"], query_id=7228136655851356160)

    order1.add_message_from_cell(message.refs[0])

    order1b = order1.build()

    query = wallet.create_transfer_message(order=order1b, private_key=priv_k1)

    transfer_boc = query["message"].to_boc(False)

    await client.raw_send_message(transfer_boc)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
