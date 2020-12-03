#!/usr/bin/env python3

import json
import os

from pybytom.transaction import Transaction
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


def test_transaction():

    estimated_transaction_fee: int = estimate_transaction_fee(
        address=_["wallet"]["vapor_address"]["mainnet"],
        asset=ASSET,
        amount=amount_converter(0.0001, "BTM2NEU"),
        confirmations=1,
        network=_["network"],
        vapor=True
    )

    assert isinstance(estimated_transaction_fee, int)
    assert estimated_transaction_fee == 449000

    unsigned_transaction: Transaction = Transaction(
        network=_["network"], vapor=True
    ).build_transaction(
        address=_["wallet"]["vapor_address"]["mainnet"],
        inputs=[
            spend_utxo(
                utxo=find_p2wsh_utxo(
                    transaction_id="969d871257b53c067f473b3894c68bf7be11673e4f3905d432954d97dbf34751",
                    network=_["network"],
                    vapor=True
                )
            )
        ],
        outputs=[
            control_address(
                asset=ASSET,
                amount=10_000,
                address=_["wallet"]["vapor_address"]["mainnet"],
                symbol="NEU",
                vapor=True
            )
        ],
        fee=estimated_transaction_fee,
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
