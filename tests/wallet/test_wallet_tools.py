#!/usr/bin/env python3

import json
import os

from pybytom.wallet.tools import (
    path_to_indexes, indexes_to_path, get_xpublic_key, get_expand_xprivate_key,
    get_child_xprivate_key, get_child_xpublic_key, get_private_key,
    get_public_key, get_program, get_address, get_vapor_address
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_wallet_tools():

    assert get_xpublic_key(xprivate_key=_["wallet"]["xprivate_key"]) == _["wallet"]["xpublic_key"]
    assert get_expand_xprivate_key(xprivate_key=_["wallet"]["xprivate_key"]) == _["wallet"]["expand_xprivate_key"]

    assert indexes_to_path(indexes=_["wallet"]["indexes"]) == _["wallet"]["path"]
    assert path_to_indexes(path=_["wallet"]["path"]) == _["wallet"]["indexes"]

    assert get_child_xprivate_key(xprivate_key=_["wallet"]["xprivate_key"]) == _["wallet"]["xprivate_key"]
    assert get_child_xprivate_key(xprivate_key=_["wallet"]["xprivate_key"], indexes=_["wallet"]["indexes"]) == _["wallet"]["child_xprivate_key"]
    assert get_child_xprivate_key(xprivate_key=_["wallet"]["xprivate_key"], path=_["wallet"]["path"]) == _["wallet"]["child_xprivate_key"]

    assert get_child_xpublic_key(xpublic_key=_["wallet"]["xpublic_key"]) == _["wallet"]["xpublic_key"]
    assert get_child_xpublic_key(xpublic_key=_["wallet"]["xpublic_key"], indexes=_["wallet"]["indexes"]) == _["wallet"]["child_xpublic_key"]
    assert get_child_xpublic_key(xpublic_key=_["wallet"]["xpublic_key"], path=_["wallet"]["path"]) == _["wallet"]["child_xpublic_key"]

    assert get_private_key(xprivate_key=_["wallet"]["xprivate_key"]) == _["wallet"]["xprivate_key"]
    assert get_private_key(xprivate_key=_["wallet"]["xprivate_key"], indexes=_["wallet"]["indexes"]) == _["wallet"]["child_xprivate_key"]
    assert get_private_key(xprivate_key=_["wallet"]["xprivate_key"], path=_["wallet"]["path"]) == _["wallet"]["child_xprivate_key"]

    assert get_public_key(xpublic_key=_["wallet"]["xpublic_key"]) == _["wallet"]["xpublic_key"][:64]
    assert get_public_key(xpublic_key=_["wallet"]["xpublic_key"], indexes=_["wallet"]["indexes"]) == _["wallet"]["public_key"]
    assert get_public_key(xpublic_key=_["wallet"]["xpublic_key"], path=_["wallet"]["path"]) == _["wallet"]["public_key"]

    assert get_program(public_key=_["wallet"]["public_key"]) == _["wallet"]["program"]

    assert get_address(program=_["wallet"]["program"], network="mainnet") == _["wallet"]["address"]["mainnet"]
    assert get_address(program=_["wallet"]["program"], network="solonet") == _["wallet"]["address"]["solonet"]
    assert get_address(program=_["wallet"]["program"], network="testnet") == _["wallet"]["address"]["testnet"]

    assert get_vapor_address(program=_["wallet"]["program"], network="mainnet") == _["wallet"]["vapor_address"]["mainnet"]
    assert get_vapor_address(program=_["wallet"]["program"], network="solonet") == _["wallet"]["vapor_address"]["solonet"]
    assert get_vapor_address(program=_["wallet"]["program"], network="testnet") == _["wallet"]["vapor_address"]["testnet"]
