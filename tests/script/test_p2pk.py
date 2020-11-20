#!/usr/bin/env python3

import json
import os

from pybytom.script import (
    get_public_key_hash, get_p2pkh_program, get_p2wpkh_program,
    get_p2wpkh_address, get_p2wpkh_vapor_address
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_p2pk():

    assert get_public_key_hash(
        public_key=_["script"]["p2pk"]["public_key"]
    ) == _["script"]["p2pk"]["public_key_hash"]

    assert get_p2pkh_program(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"]
    ) == _["script"]["p2pk"]["program"]["p2pkh"]
    assert get_p2wpkh_program(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"]
    ) == _["script"]["p2pk"]["program"]["p2wpkh"]

    assert get_p2wpkh_address(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"], network="mainnet"
    ) == _["script"]["p2pk"]["address"]["mainnet"]
    assert get_p2wpkh_address(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"], network="solonet"
    ) == _["script"]["p2pk"]["address"]["solonet"]
    assert get_p2wpkh_address(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"], network="testnet"
    ) == _["script"]["p2pk"]["address"]["testnet"]

    assert get_p2wpkh_vapor_address(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"], network="mainnet"
    ) == _["script"]["p2pk"]["vapor_address"]["mainnet"]
    assert get_p2wpkh_vapor_address(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"], network="solonet"
    ) == _["script"]["p2pk"]["vapor_address"]["solonet"]
    assert get_p2wpkh_vapor_address(
        public_key_hash=_["script"]["p2pk"]["public_key_hash"], network="testnet"
    ) == _["script"]["p2pk"]["vapor_address"]["testnet"]
