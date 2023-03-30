from tonsdk.boc import Cell, begin_cell, Slice
from tonsdk.contract import Address
import bitarray


address = 'EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'

message = begin_cell()\
    .store_uint(15, 32)\
    .store_address(Address(address))\
    .store_coins(10000)\
    .end_cell()


def bit_parsing():
    array = message.bits.array

    x = bitarray.bitarray()
    x.frombytes(array)

    op_code = int(x[:32].to01(), 2)
    print(op_code)
    del x[:32]

    del x[:3]

    wc = int(x[:8].to01(), 2)
    del x[:8]

    hash_part = hex(int(x[:256].to01(), 2))

    address = str(wc) + ':' + str(hash_part.split('0x')[1])
    print(Address(address).to_string(True, True, True))

    del x[:256]

    l = int(x[:4].to01(), 2)
    del x[:4]

    amount = int(x[:l * 8].to01(), 2)
    print(amount)


def tonsdk_parsing():
    slice = Slice(message)

    op_code = slice.read_uint(32)
    address = slice.read_msg_addr().to_string(True, True, True)
    coins = slice.read_coins()

    print(op_code, address, coins)


if __name__ == '__main__':
    tonsdk_parsing()




