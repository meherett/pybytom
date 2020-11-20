#!/usr/bin/env python3

import json
import os

from pybytom.transaction import Transaction
from pybytom.transaction.actions import spend_utxo, control_address
from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.assets import BTM as ASSET

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_transaction():

    unsigned_transaction: Transaction = Transaction(
        network=_["network"], vapor=False
    ).build_transaction(
        address=_["wallet"]["address"]["mainnet"],
        inputs=[
            spend_utxo(
                utxo=find_p2wsh_utxo(
                    transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                    network=_["network"]
                )
            )
        ],
        outputs=[
            control_address(
                asset=ASSET,
                amount=10_000,
                address="bm1qwk4kpx09ehccrna3enqqwhrj9xt7pwxd4sufkw",
                symbol="NEU",
                vapor=False
            )
        ],
        fee=10_000_000,
        confirmations=1,
        forbid_chain_tx=False
    )

    assert unsigned_transaction.fee() == _["transaction"]["transaction"]["unsigned"]["fee"]
    assert unsigned_transaction.confirmations() == _["transaction"]["transaction"]["unsigned"]["confirmations"]
    assert unsigned_transaction.hash() == _["transaction"]["transaction"]["unsigned"]["hash"]
    assert unsigned_transaction.raw() == _["transaction"]["transaction"]["unsigned"]["raw"]
    assert unsigned_transaction.json() == _["transaction"]["transaction"]["unsigned"]["json"]
    assert unsigned_transaction.unsigned_datas(False) == _["transaction"]["transaction"]["unsigned"]["unsigned_datas"]
    assert unsigned_transaction.signatures() == _["transaction"]["transaction"]["unsigned"]["signatures"]

    signed_transaction = unsigned_transaction.sign(
        xprivate_key=_["wallet"]["xprivate_key"],
        indexes=_["wallet"]["indexes"]
    )

    assert signed_transaction.fee() == _["transaction"]["transaction"]["signed"]["fee"]
    assert signed_transaction.confirmations() == _["transaction"]["transaction"]["signed"]["confirmations"]
    assert signed_transaction.hash() == _["transaction"]["transaction"]["signed"]["hash"]
    assert signed_transaction.raw() == _["transaction"]["transaction"]["signed"]["raw"]
    assert signed_transaction.json() == _["transaction"]["transaction"]["signed"]["json"]
    assert signed_transaction.unsigned_datas(False) == _["transaction"]["transaction"]["signed"]["unsigned_datas"]
    assert signed_transaction.signatures() == _["transaction"]["transaction"]["signed"]["signatures"]
