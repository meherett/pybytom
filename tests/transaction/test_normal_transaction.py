#!/usr/bin/env python3

import json
import os

from pybytom.transaction import NormalTransaction
from pybytom.assets import BTM as ASSET

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_normal_transaction():

    unsigned_normal_transaction: NormalTransaction = NormalTransaction(
        network=_["network"], vapor=False
    ).build_transaction(
        address=_["wallet"]["address"]["mainnet"],
        recipients={
            "bm1qg83h7fddr70dsw6c2c3zhc25fved9mhydp6u8d": 50_000
        },
        asset=ASSET
    )

    assert unsigned_normal_transaction.fee() == _["transaction"]["normal_transaction"]["unsigned"]["fee"]
    assert unsigned_normal_transaction.confirmations() == _["transaction"]["normal_transaction"]["unsigned"]["confirmations"]
    assert unsigned_normal_transaction.hash() == _["transaction"]["normal_transaction"]["unsigned"]["hash"]
    assert unsigned_normal_transaction.raw() == _["transaction"]["normal_transaction"]["unsigned"]["raw"]
    assert unsigned_normal_transaction.json() == _["transaction"]["normal_transaction"]["unsigned"]["json"]
    assert unsigned_normal_transaction.unsigned_datas(False) == _["transaction"]["normal_transaction"]["unsigned"]["unsigned_datas"]
    assert unsigned_normal_transaction.signatures() == _["transaction"]["normal_transaction"]["unsigned"]["signatures"]

    signed_normal_transaction: NormalTransaction = unsigned_normal_transaction.sign(
        xprivate_key=_["wallet"]["xprivate_key"],
        indexes=_["wallet"]["indexes"]
    )

    assert signed_normal_transaction.fee() == _["transaction"]["normal_transaction"]["signed"]["fee"]
    assert signed_normal_transaction.confirmations() == _["transaction"]["normal_transaction"]["signed"]["confirmations"]
    assert signed_normal_transaction.hash() == _["transaction"]["normal_transaction"]["signed"]["hash"]
    assert signed_normal_transaction.raw() == _["transaction"]["normal_transaction"]["signed"]["raw"]
    assert signed_normal_transaction.json() == _["transaction"]["normal_transaction"]["signed"]["json"]
    assert signed_normal_transaction.unsigned_datas(False) == _["transaction"]["normal_transaction"]["signed"]["unsigned_datas"]
    assert signed_normal_transaction.signatures() == _["transaction"]["normal_transaction"]["signed"]["signatures"]
