from tonsdk.contract.token.nft import NFTCollection, NFTItem
from tonsdk.contract import Address
from tonsdk.utils import to_nano


def create_collection_mint():
    royalty_base = 1000
    royalty_factor = 55

    collection = NFTCollection(royalty_base=royalty_base,
                               royalty=royalty_factor)

    collection = NFTCollection(royalty_base=royalty_base,
                               royalty=royalty_factor,
                               royalty_address=Address('EQB_bTCXmQpIldjAj5tGKKKl6p7JD-jDF0YQqmoyxffjgzCJ'),
                               owner_address=Address('EQB_bTCXmQpIldjAj5tGKKKl6p7JD-jDF0YQqmoyxffjgzCJ'),
                               collection_content_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/meta.json',
                               nft_item_content_base_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/',
                               nft_item_code_hex=NFTItem.code)

    return collection


def create_nft_mint(index=0, address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'):

    collection = create_collection_mint()

    body = collection.create_mint_body(item_index=index,
                                new_owner_address=Address(address),
                                item_content_uri=f'{index + 1}/meta.json',
                                amount=to_nano(0.02, 'ton'))

    return body


def create_batch_nft_mint(index=0, address='EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N'):

    collection = create_collection_mint()

    contents_and_owners = []

    for i in range(1, 11):
        contents_and_owners.append((f'{i + 1}/meta.json', Address('EQB_bTCXmQpIldjAj5tGKKKl6p7JD-jDF0YQqmoyxffjgzCJ')))

    body = collection.create_batch_mint_body(from_item_index=1,
                                      contents_and_owners=contents_and_owners,
                                      amount_per_one=to_nano(0.01, 'ton'))
    return body
