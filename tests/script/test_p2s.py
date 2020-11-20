#!/usr/bin/env python3

import json
import os

from pybytom.script import (
    get_script_hash, get_p2sh_program, get_p2wsh_program,
    get_p2wsh_address, get_p2wsh_vapor_address
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_p2s():

    assert get_script_hash(
        bytecode=_["script"]["p2s"]["bytecode"]
    ) == _["script"]["p2s"]["script_hash"]

    assert get_p2sh_program(
        script_hash=_["script"]["p2s"]["script_hash"]
    ) == _["script"]["p2s"]["program"]["p2sh"]
    assert get_p2wsh_program(
        script_hash=_["script"]["p2s"]["script_hash"]
    ) == _["script"]["p2s"]["program"]["p2wsh"]

    assert get_p2wsh_address(
        script_hash=_["script"]["p2s"]["script_hash"], network="mainnet"
    ) == _["script"]["p2s"]["address"]["mainnet"]
    assert get_p2wsh_address(
        script_hash=_["script"]["p2s"]["script_hash"], network="solonet"
    ) == _["script"]["p2s"]["address"]["solonet"]
    assert get_p2wsh_address(
        script_hash=_["script"]["p2s"]["script_hash"], network="testnet"
    ) == _["script"]["p2s"]["address"]["testnet"]

    assert get_p2wsh_vapor_address(
        script_hash=_["script"]["p2s"]["script_hash"], network="mainnet"
    ) == _["script"]["p2s"]["vapor_address"]["mainnet"]
    assert get_p2wsh_vapor_address(
        script_hash=_["script"]["p2s"]["script_hash"], network="solonet"
    ) == _["script"]["p2s"]["vapor_address"]["solonet"]
    assert get_p2wsh_vapor_address(
        script_hash=_["script"]["p2s"]["script_hash"], network="testnet"
    ) == _["script"]["p2s"]["vapor_address"]["testnet"]
