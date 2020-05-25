#!/usr/bin/env python3

from pybytom.script import (
    get_public_key_hash, get_script_hash,
    get_p2wpkh_program, get_p2wsh_program,
    get_p2wpkh_address, get_p2wsh_address
)


def test_p2wpk():

    # P2WPK
    public_key = "5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2"
    public_key_hash = get_public_key_hash(public_key=public_key)
    assert public_key_hash == "875240ba66646d900c59dd20d843351c2fcbeedc"
    assert get_p2wpkh_program(
        public_key_hash=public_key_hash) == "0014875240ba66646d900c59dd20d843351c2fcbeedc"
    assert get_p2wpkh_address(public_key_hash=public_key_hash,
                              network="mainnet") == "bm1qsafypwnxv3keqrzem5sdsse4rshuhmku7kpnxq"


def test_p2ws():

    # P2WS
    bytecode = "7baa8800c3c251547ac1"
    script_hash = get_script_hash(bytecode=bytecode)
    assert script_hash == "e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3"
    assert get_p2wsh_program(
        script_hash=script_hash) == "0020e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3"
    assert get_p2wsh_address(
        script_hash=script_hash, network="mainnet") == "bm1qu3l27h360zvpjurgutwhcqsfxvdndgdh5uawhqysm7qk5089klfsrrlhez"

