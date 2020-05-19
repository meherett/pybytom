#!/usr/bin/env python3

from pybytom.wallet import Wallet

import pytest
import binascii


XPRIVATE_KEY = "6048e94ca15ea65c96244ab9284662a5b665a3cb8d0df329206e5b8db0b200444cbc8f1f55a072f92868ea5ccad46032a11b51ef74aad5981151737f7620e35c"


def test_from_seed():

    wallet = Wallet(network="solonet")
    wallet.from_xprivate_key(xprivate_key=XPRIVATE_KEY)

    wallet.from_path("m/44/153/1/0/1")

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.xprivate_key() == "6048e94ca15ea65c96244ab9284662a5b665a3cb8d0df329206e5b8db0b200444cbc8f1f55a072f92868ea5ccad46032a11b51ef74aad5981151737f7620e35c"
    assert wallet.xpublic_key() == "27b2fa6151dd27fbf91f11b19bc2798a725d267303105f9cd9df9f0ca999610b4cbc8f1f55a072f92868ea5ccad46032a11b51ef74aad5981151737f7620e35c"
    assert wallet.expand_xprivate_key() == "6048e94ca15ea65c96244ab9284662a5b665a3cb8d0df329206e5b8db0b20044c4cad6ae84e4de3f0cfef32340ab2c187a2d3b075f95a0b0b76bff00003a7c52"
    assert wallet.indexes() == ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    assert wallet.path() == "m/44/153/1/0/1"
    assert wallet.child_xprivate_key() == "d0196e49add578d260590dac3a484081e7c1992d21a0acb431fd9de0e8b500445cdbde63e5a2aaf550c382d9a80f365a226c59b5447c4194c57240931ac270c9"
    assert wallet.child_xpublic_key() == "3ed490f59aba816bf3ffb6ed14dc6bb8720597a3ad4a9ad093062cd0fd983b8d5cdbde63e5a2aaf550c382d9a80f365a226c59b5447c4194c57240931ac270c9"
    assert wallet.private_key() == "d0196e49add578d260590dac3a484081e7c1992d21a0acb431fd9de0e8b500445cdbde63e5a2aaf550c382d9a80f365a226c59b5447c4194c57240931ac270c9"
    assert wallet.public_key() == "3ed490f59aba816bf3ffb6ed14dc6bb8720597a3ad4a9ad093062cd0fd983b8d"
    assert wallet.program() == "0014f1004bccc1739409845aaa115ef95ec8179162ae"
    assert wallet.address() == "sm1q7yqyhnxpww2qnpz64gg4a727eqtezc4w7dw60p"

    assert wallet.dumps() == {
        "entropy": None,
        "mnemonic": None,
        "language": None,
        "passphrase": None,
        "seed": None,
        "xprivate_key": "6048e94ca15ea65c96244ab9284662a5b665a3cb8d0df329206e5b8db0b200444cbc8f1f55a072f92868ea5ccad46032a11b51ef74aad5981151737f7620e35c",
        "xpublic_key": "27b2fa6151dd27fbf91f11b19bc2798a725d267303105f9cd9df9f0ca999610b4cbc8f1f55a072f92868ea5ccad46032a11b51ef74aad5981151737f7620e35c",
        "expand_xprivate_key": "6048e94ca15ea65c96244ab9284662a5b665a3cb8d0df329206e5b8db0b20044c4cad6ae84e4de3f0cfef32340ab2c187a2d3b075f95a0b0b76bff00003a7c52",
        "guid": None,
        "indexes": ["2c000000", "99000000", "01000000", "00000000", "01000000"],
        "path": "m/44/153/1/0/1",
        "child_xprivate_key": "d0196e49add578d260590dac3a484081e7c1992d21a0acb431fd9de0e8b500445cdbde63e5a2aaf550c382d9a80f365a226c59b5447c4194c57240931ac270c9",
        "child_xpublic_key": "3ed490f59aba816bf3ffb6ed14dc6bb8720597a3ad4a9ad093062cd0fd983b8d5cdbde63e5a2aaf550c382d9a80f365a226c59b5447c4194c57240931ac270c9",
        "private_key": "d0196e49add578d260590dac3a484081e7c1992d21a0acb431fd9de0e8b500445cdbde63e5a2aaf550c382d9a80f365a226c59b5447c4194c57240931ac270c9",
        "public_key": "3ed490f59aba816bf3ffb6ed14dc6bb8720597a3ad4a9ad093062cd0fd983b8d",
        "program": "0014f1004bccc1739409845aaa115ef95ec8179162ae",
        "address": {
            "mainnet": "bm1q7yqyhnxpww2qnpz64gg4a727eqtezc4wluym00",
            "solonet": "sm1q7yqyhnxpww2qnpz64gg4a727eqtezc4w7dw60p",
            "testnet": "tm1q7yqyhnxpww2qnpz64gg4a727eqtezc4wm29l07"
        }
    }

    with pytest.raises(binascii.Error, match="Non-hexadecimal digit found"):
        wallet.from_seed(seed="asdfasdfasdf")
