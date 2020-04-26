#!/usr/bin/env python3

from bytom.wallet import Wallet, HARDEN, PATH, INDEXES
from bytom.utils import check_mnemonic, generate_entropy

import hashlib

MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac" \
           "51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4" \
          "de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"


def test_from_mnemonic():
    wallet = Wallet()\
        .from_mnemonic(mnemonic=MNEMONIC)\
        .from_path("m/44/153/1/0/1")
    assert wallet.private_key() == "8808c97a060e8c56cbf41a2fb6296d71592362ada9c98b3890c777a78182b8489a022e8" \
                                   "9f786faccebf5d11f8d1638bf156f4828e623dc984d33555bb4a943a5"
    assert wallet.public_key() == "41eeff845c6bd6d13351572cec08900f23365fb2685b64ce01784792457804a5"
    assert wallet.program() == "00143ed47dc9522049f3dfc7571a5063236e6407cd59"
    assert wallet.address(network="mainnet") == "bm1q8m28mj2jypyl8h782ud9qcerdejq0n2e7525f3"
    assert wallet.address(network="solonet") == "sm1q8m28mj2jypyl8h782ud9qcerdejq0n2el9q4fl"
    assert wallet.address(network="testnet") == "tm1q8m28mj2jypyl8h782ud9qcerdejq0n2e6ztsfq"
    assert (wallet.seed())

    assert Wallet().program(public=wallet.public_key())
    assert Wallet().address(program=Wallet()
                            .program(public=wallet.public_key()), network="mainnet")
    assert Wallet().public_key(wallet.xpublic_key(), path=PATH)


def test_harden():
    wallet = Wallet().from_entropy(
        entropy=generate_entropy(), passphrase="meherett", language="japanese")

    wallet.from_index(44 + HARDEN)
    wallet.from_index(153)
    wallet.from_index(1 + HARDEN)
    wallet.from_index(0)
    wallet.from_index(1)
    assert (wallet.program())
    assert (wallet.address(network="testnet"))


def test_sing_and_verify():
    wallet = Wallet().from_entropy(
        entropy=generate_entropy(), passphrase="meherett", language="japanese")

    wallet.from_index(44 + HARDEN)
    wallet.from_index(153)
    wallet.from_index(1 + HARDEN)
    wallet.from_index(0)
    wallet.from_index(1)

    signature = wallet.sign(message=hashlib.sha256("meherett".encode()).hexdigest())
    assert signature

    assert wallet.verify(message=hashlib.sha256("meherett".encode()).hexdigest(),
                         signature=signature)
