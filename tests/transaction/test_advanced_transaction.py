#!/usr/bin/env python3

import json
import os

from pybytom.transaction import AdvancedTransaction
from pybytom.transaction.actions import spend_utxo, control_address
from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.rpc import estimate_transaction_fee
from pybytom.utils import amount_converter
from pybytom.assets import BTM as ASSET

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_advanced_transaction():

    estimated_transaction_fee: int = estimate_transaction_fee(
        address=_["wallet"]["address"]["mainnet"],
        asset=ASSET,
        amount=amount_converter(0.0001, "BTM2NEU"),
        confirmations=1,
        network=_["network"],
        vapor=False
    )

    assert isinstance(estimated_transaction_fee, int)
    assert estimated_transaction_fee == 449000

    unsigned_advanced_transaction: AdvancedTransaction = AdvancedTransaction(
        network=_["network"], vapor=False
    ).build_transaction(
        address=_["wallet"]["address"]["mainnet"],
        inputs=[
            spend_utxo(
                utxo=find_p2wsh_utxo(
                    transaction_id="049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b",
                    network=_["network"],
                    vapor=False
                )
            )
        ],
        outputs=[
            control_address(
                asset=ASSET,
                amount=10_000,
                address=_["wallet"]["address"]["mainnet"],
                symbol="NEU",
                vapor=False
            )
        ],
        fee=estimated_transaction_fee,
        confirmations=1,
        forbid_chain_tx=False
    )

    assert unsigned_advanced_transaction.fee() == _["transaction"]["advanced_transaction"]["unsigned"]["fee"]
    assert unsigned_advanced_transaction.confirmations() == _["transaction"]["advanced_transaction"]["unsigned"]["confirmations"]
    assert unsigned_advanced_transaction.hash() == _["transaction"]["advanced_transaction"]["unsigned"]["hash"]
    assert unsigned_advanced_transaction.raw() == _["transaction"]["advanced_transaction"]["unsigned"]["raw"]
    assert unsigned_advanced_transaction.json() == _["transaction"]["advanced_transaction"]["unsigned"]["json"]
    assert unsigned_advanced_transaction.unsigned_datas(False) == _["transaction"]["advanced_transaction"]["unsigned"]["unsigned_datas"]
    assert unsigned_advanced_transaction.signatures() == _["transaction"]["advanced_transaction"]["unsigned"]["signatures"]

    signed_advanced_transaction = unsigned_advanced_transaction.sign(
        xprivate_key=_["wallet"]["xprivate_key"],
        indexes=_["wallet"]["indexes"]
    )

    assert signed_advanced_transaction.fee() == _["transaction"]["advanced_transaction"]["signed"]["fee"]
    assert signed_advanced_transaction.confirmations() == _["transaction"]["advanced_transaction"]["signed"]["confirmations"]
    assert signed_advanced_transaction.hash() == _["transaction"]["advanced_transaction"]["signed"]["hash"]
    assert signed_advanced_transaction.raw() == _["transaction"]["advanced_transaction"]["signed"]["raw"]
    assert signed_advanced_transaction.json() == _["transaction"]["advanced_transaction"]["signed"]["json"]
    assert signed_advanced_transaction.unsigned_datas(False) == _["transaction"]["advanced_transaction"]["signed"]["unsigned_datas"]
    assert signed_advanced_transaction.signatures() == _["transaction"]["advanced_transaction"]["signed"]["signatures"]
