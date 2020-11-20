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


def test_from_private_key():

    wallet: Wallet = Wallet(
        network=_["network"]
    ).from_private_key(
        private_key=_["wallet"]["private_key"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.xprivate_key() is None
    assert wallet.xpublic_key() is None
    assert wallet.expand_xprivate_key() is None
    assert wallet.child_xprivate_key() is None
    assert wallet.child_xpublic_key() is None
    # assert wallet.guid() == _["wallet"]["guid"]
    assert wallet.private_key() == _["wallet"]["private_key"]
    assert wallet.public_key() == _["wallet"]["public_key"]
    assert wallet.program() == _["wallet"]["program"]
    assert wallet.indexes() == []
    assert wallet.path() is None
    assert wallet.address(network="mainnet") == _["wallet"]["address"]["mainnet"]
    assert wallet.address(network="solonet") == _["wallet"]["address"]["solonet"]
    assert wallet.address(network="testnet") == _["wallet"]["address"]["testnet"]
    assert wallet.vapor_address(network="mainnet") == _["wallet"]["vapor_address"]["mainnet"]
    assert wallet.vapor_address(network="solonet") == _["wallet"]["vapor_address"]["solonet"]
    assert wallet.vapor_address(network="testnet") == _["wallet"]["vapor_address"]["testnet"]

    assert isinstance(wallet.dumps(guid=False), dict)
    # assert isinstance(wallet.balance(vapor=False), int)
    # assert isinstance(wallet.balance(vapor=True), int)
    # assert isinstance(wallet.utxos(), list)
