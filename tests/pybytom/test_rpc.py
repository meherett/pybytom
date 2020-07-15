#!/usr/bin/env python3

from pybytom.rpc import (
    get_balance, list_address, submit_transaction_raw, decode_transaction_raw
)
from pybytom.exceptions import APIError

import pytest


def test_rpc():

    assert isinstance(get_balance("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7",
                                  "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                                  "mainnet"), int)

    assert isinstance(list_address("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", 1, network="mainnet"), dict)

    with pytest.raises(Exception):
        submit_transaction_raw(
            "22a71cb7-bfee-48bf-93e9-756bbe194737",
            "070100010160015e1a27542761cb9060e50ff53fe794a24fd59991aee13ee09f45536f40e5ab08ddfffffffffffffff"
            "ffffffffffffffffffffffffffffffffffffffffffffffffff0f287850801011600142cda4f99ea8112e6fa61cdd261"
            "57ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e202013cfffff"
            "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80c2d72f01160014875240ba66646d900c59"
            "dd20d843351c2fcbeedc00013dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff083c"
            "ed007011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00",
            [
                [
                    "33386e69735687f28ff3f864d7ae573928054f520b56b9f02799d85cdb69a07885923323cd10a0d9e5b062d"
                    "d8df4926c8b85c202f0af9e5632767f7355e0520c"
                ]
            ]

        )

    with pytest.raises(Exception):
        decode_transaction_raw(
            "070100010160015e1a27542761cb9060e50ff53fe794a24fd59991aee13ee09f45536f40e5ab08ddfffffffffffffff"
            "ffffffffffffffffffffffffffffffffffffffffffffffffff0f287850801011600142cda4f99ea8112e6fa61cdd261"
            "57ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e202013cfffff"
            "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80c2d72f01160014875240ba66646d900c59"
            "dd20d843351c2fcbeedc00013dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff083c"
            "ed007011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        )
