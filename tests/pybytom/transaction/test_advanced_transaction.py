#!/usr/bin/env python3

from pybytom.transaction import AdvancedTransaction
from pybytom.transaction.actions import spend_utxo, control_address
from pybytom.transaction.tools import find_smart_contract_utxo, find_p2wsh_utxo

NETWORK = "mainnet"

ASSET = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"


def test_advanced_transaction():

    unsigned_advanced_transaction = AdvancedTransaction(network=NETWORK)
    unsigned_advanced_transaction.build_transaction(
        address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7",
        inputs=[
            spend_utxo(
                utxo=find_p2wsh_utxo(
                    transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                    network=NETWORK
                )
            )
        ],
        outputs=[
            control_address(
                asset=ASSET,
                amount=10_000_000,
                address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7",
                symbol="NEU"
            )
        ],
        fee=10_000_000,
        confirmations=1
    )

    assert unsigned_advanced_transaction.fee()
    assert unsigned_advanced_transaction.confirmations()
    assert unsigned_advanced_transaction.hash()
    assert unsigned_advanced_transaction.raw()
    assert unsigned_advanced_transaction.json()
    assert unsigned_advanced_transaction.unsigned_datas(False)
    assert unsigned_advanced_transaction.signatures() == []

    # Singing unsigned advanced transaction by xprivate key
    signed_advanced_transaction = unsigned_advanced_transaction.sign(
        xprivate_key="3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338ff590dedc7ddff447797e1"
                     "e781190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed",
        account=1,
        change=False,
        address=1,
        path=None,
        indexes=['2c000000', '99000000', '01000000', '00000000', '01000000']
    )

    assert signed_advanced_transaction.fee()
    assert signed_advanced_transaction.confirmations()
    assert signed_advanced_transaction.hash()
    assert signed_advanced_transaction.raw()
    assert signed_advanced_transaction.json()
    assert signed_advanced_transaction.unsigned_datas(False)
    assert signed_advanced_transaction.signatures() != []
