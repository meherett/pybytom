#!/usr/bin/env python3

import json
import os

from pybytom.utils import (
    generate_mnemonic, generate_entropy, is_mnemonic,
    get_mnemonic_language, is_address, is_vapor_address
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_utils():

    assert len(generate_entropy(strength=128)) == 32
    assert len(generate_entropy(strength=160)) == 40
    assert len(generate_entropy(strength=192)) == 48
    assert len(generate_entropy(strength=224)) == 56
    assert len(generate_entropy(strength=256)) == 64

    assert len(generate_mnemonic(language="chinese_traditional", strength=128).split(" ")) == 12
    assert get_mnemonic_language(mnemonic=_["wallet"]["mnemonic"]) == _["wallet"]["language"]
    assert is_mnemonic(mnemonic=_["wallet"]["mnemonic"])
    assert is_mnemonic(mnemonic=_["wallet"]["mnemonic"], language=_["wallet"]["language"])

    assert is_address(address=_["wallet"]["address"]["mainnet"])
    assert is_address(address=_["wallet"]["address"]["mainnet"], network="mainnet")
    assert is_address(address=_["wallet"]["address"]["solonet"])
    assert is_address(address=_["wallet"]["address"]["solonet"], network="solonet")
    assert is_address(address=_["wallet"]["address"]["testnet"])
    assert is_address(address=_["wallet"]["address"]["testnet"], network="testnet")

    assert is_vapor_address(address=_["wallet"]["vapor_address"]["mainnet"])
    assert is_vapor_address(address=_["wallet"]["vapor_address"]["mainnet"], network="mainnet")
    assert is_vapor_address(address=_["wallet"]["vapor_address"]["solonet"])
    assert is_vapor_address(address=_["wallet"]["vapor_address"]["solonet"], network="solonet")
    assert is_vapor_address(address=_["wallet"]["vapor_address"]["testnet"])
    assert is_vapor_address(address=_["wallet"]["vapor_address"]["testnet"], network="testnet")
