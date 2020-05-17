#!/usr/bin/env python3

from pybytom.transaction import NormalTransaction

NETWORK = "mainnet"

ASSET = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"


def test_normal_transaction():

    unsigned_normal_transaction = NormalTransaction(network=NETWORK)
    unsigned_normal_transaction.build_transaction(
        guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b",
        recipients={
            "bm1qzx7pjr6whcaxmh9u0thkjuavf2ynk3zkgshhle": 1_000_000
        },
        asset=ASSET
    )

    assert unsigned_normal_transaction.fee()
    assert unsigned_normal_transaction.confirmations()
    assert unsigned_normal_transaction.hash()
    assert unsigned_normal_transaction.raw()
    assert unsigned_normal_transaction.json()
    assert unsigned_normal_transaction.unsigned_datas(False)
    assert unsigned_normal_transaction.signatures() == []

    # Singing unsigned normal transaction by xprivate key
    signed_normal_transaction = unsigned_normal_transaction.sign(
        xprivate_key="3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338ff590dedc7ddff447797e1"
                     "e781190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed",
        account=1,
        change=False,
        address=1,
        path="m/44/153/1/0/1",
        indexes=None
    )

    assert signed_normal_transaction.fee()
    assert signed_normal_transaction.confirmations()
    assert signed_normal_transaction.hash()
    assert signed_normal_transaction.raw()
    assert signed_normal_transaction.json()
    assert signed_normal_transaction.unsigned_datas(False)
    assert signed_normal_transaction.signatures() != []
