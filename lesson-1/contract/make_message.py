from tonsdk.boc import begin_cell


def make_message_body():
    return begin_cell()\
        .store_uint(1, 32)\
        .end_cell()


if __name__ == '__main__':
    print(make_message_body())