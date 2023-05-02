from tonsdk.contract.wallet import MultiSigWallet, MultiSigOrder, MultiSigOrderBuilder
from tonsdk.crypto import mnemonic_new, mnemonic_to_wallet_key
from tonsdk.utils import Address, bytes_to_b64str, b64str_to_bytes, to_nano, sign_message
from tonsdk.boc import Cell


mnemonics1 = ['rather', 'voice', 'zone', 'fold', 'rotate', 'crane', 'roast', 'brave', 'motor', 'kid', 'note', 'squirrel', 'piece', 'home', 'expose', 'bench', 'flame', 'wood', 'person', 'assist', 'vocal', 'bomb', 'dismiss', 'diesel']

pub_k1, priv_k1 = mnemonic_to_wallet_key(mnemonics1)


def sign(b64str_boc: str):

    cell = Cell.one_from_boc(b64str_to_bytes(b64str_boc))

    """
    verify message
    """

    return bytes_to_b64str(sign_message(bytes(cell.bytes_hash()), priv_k1).signature)
