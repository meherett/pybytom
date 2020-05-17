#!/usr/bin/env python3

from pybytom.transaction import AdvancedTransaction
from pybytom.transaction.tools import spend_utxo_action, find_contract_utxo_id, control_address_action

NETWORK = "mainnet"

ASSET = "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"


def test_advanced_transaction():

    unsigned_advanced_transaction = AdvancedTransaction(network=NETWORK)
    unsigned_advanced_transaction.build_transaction(
        guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b",
        inputs=[
            spend_utxo_action(
                utxo=find_contract_utxo_id(
                    transaction_id="5268c5a52f22141521833d79ad69c27a2760e99cb0f8386c3e02cf5d1bb0832f",
                    network=NETWORK
                )
            )
        ],
        outputs=[
            control_address_action(
                asset=ASSET,
                amount=100,
                address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
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
