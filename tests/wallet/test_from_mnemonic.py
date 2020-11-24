#!/usr/bin/env python3

import json
import os

from pybytom.wallet import Wallet

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_from_mnemonic():

    wallet: Wallet = Wallet(
        network=_["network"]
    ).from_mnemonic(
        mnemonic=_["wallet"]["mnemonic"],
        passphrase=_["wallet"]["passphrase"],
        language=_["wallet"]["language"]
    ).from_path(
        path=_["wallet"]["path"]
    )

    assert wallet.entropy() == _["wallet"]["entropy"]
    assert wallet.mnemonic() == _["wallet"]["mnemonic"]
    assert wallet.language() == _["wallet"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["wallet"]["seed"]
    assert wallet.xprivate_key() == _["wallet"]["xprivate_key"]
    assert wallet.xpublic_key() == _["wallet"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["wallet"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["wallet"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["wallet"]["child_xpublic_key"]
    # assert wallet.guid() == _["wallet"]["guid"]
    assert wallet.private_key() == _["wallet"]["private_key"]
    assert wallet.public_key() == _["wallet"]["public_key"]
    assert wallet.program() == _["wallet"]["program"]
    assert wallet.indexes() == _["wallet"]["indexes"]
    assert wallet.path() == _["wallet"]["path"]
    assert wallet.address(network="mainnet", vapor=False) == _["wallet"]["address"]["mainnet"]
    assert wallet.address(network="solonet", vapor=False) == _["wallet"]["address"]["solonet"]
    assert wallet.address(network="testnet", vapor=False) == _["wallet"]["address"]["testnet"]
    assert wallet.address(network="mainnet", vapor=True) == _["wallet"]["vapor_address"]["mainnet"]
    assert wallet.address(network="solonet", vapor=True) == _["wallet"]["vapor_address"]["solonet"]
    assert wallet.address(network="testnet", vapor=True) == _["wallet"]["vapor_address"]["testnet"]

    assert isinstance(wallet.dumps(guid=False), dict)
    # assert isinstance(wallet.balance(vapor=False), int)
    # assert isinstance(wallet.balance(vapor=True), int)
    # assert isinstance(wallet.utxos(), list)
