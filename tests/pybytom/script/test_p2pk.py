#!/usr/bin/env python3

from pybytom.script import (
    public_key_hash, p2pkh_program, p2wpkh_program, p2wpkh_address
)


public_key = "5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2"


def test_p2pk():

    assert public_key_hash(public_key=public_key) == \
        "875240ba66646d900c59dd20d843351c2fcbeedc"

    assert p2pkh_program(public_key_hash=public_key_hash(public_key=public_key)) == \
        "76ab14875240ba66646d900c59dd20d843351c2fcbeedc88ae7cac"

    assert p2wpkh_program(public_key_hash=public_key_hash(public_key=public_key)) == \
        "0014875240ba66646d900c59dd20d843351c2fcbeedc"

    assert p2wpkh_address(public_key_hash=public_key_hash(public_key=public_key),network="mainnet") == \
        "bm1qsafypwnxv3keqrzem5sdsse4rshuhmku7kpnxq"
