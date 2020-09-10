#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.utils import is_mnemonic, generate_entropy
from pybytom.wallet.utils import get_bytes, bad_seed_checker
from pybytom.exceptions import NetworkError, DerivationError

import hashlib
import pytest

MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac" \
           "51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4" \
          "de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"


def test_harden():
    wallet = Wallet().from_entropy(
        entropy=generate_entropy(), passphrase="meherett", language="japanese")

    wallet.from_path("m/44/153'/1/0")
    wallet.from_index(1, harden=True)

    assert (wallet.program())
    assert (wallet.address(network="testnet"))


def test_sing_and_verify():
    wallet = Wallet().from_entropy(
        entropy=generate_entropy(), passphrase="meherett", language="japanese")

    wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
    wallet.from_index(1)

    signature = wallet.sign(message=hashlib.sha256("meherett".encode()).hexdigest())
    assert signature

    assert wallet.verify(message=hashlib.sha256("meherett".encode()).hexdigest(),
                         signature=signature)


def test_wallet_errors():

    with pytest.raises(TypeError, match="network must be string format"):
        Wallet(123)
    with pytest.raises(NetworkError, match=r"Invalid 'meheretnet' network/type, .*"):
        Wallet("meheretnet")

    # from entropy
    with pytest.raises(TypeError, match="entropy must be string format"):
        Wallet("solonet").from_entropy(bool(True))
    with pytest.raises(TypeError, match="passphrase must be string format"):
        Wallet("testnet").from_entropy(str(), float())
    with pytest.raises(ValueError, match=r"invalid language option, .*"):
        Wallet("mainnet").from_entropy(str(), str(), "amharic")
    # from mnemonic
    with pytest.raises(TypeError, match="mnemonic must be string format"):
        Wallet("solonet").from_mnemonic(int())
    with pytest.raises(TypeError, match="passphrase must be string format"):
        Wallet("testnet").from_mnemonic(str(), float())
    with pytest.raises(ValueError, match=r"invalid language option, .*"):
        Wallet("mainnet").from_mnemonic(str(), str(), "amharic")
    # from seed
    with pytest.raises(TypeError, match="seed must be string format"):
        Wallet("solonet").from_seed(float())
    # from xprivate key
    with pytest.raises(TypeError, match="xprivate key must be string format"):
        Wallet("solonet").from_xprivate_key(float())
    # from indexes
    with pytest.raises(TypeError, match="indexes must be list format"):
        Wallet("solonet").from_indexes(int())
    # from index
    with pytest.raises(TypeError, match="index must be integer format"):
        Wallet("testnet").from_index(str())
    # from path
    with pytest.raises(TypeError, match="path must be string format"):
        Wallet("solonet").from_path(int())
    with pytest.raises(DerivationError, match=r"Bad path, insert like this type of path .*"):
        Wallet("mainnet").from_path("mm/")
    # address
    with pytest.raises(TypeError, match="network must be string format"):
        Wallet("solonet").address(int())
    # sign
    with pytest.raises(TypeError, match="message must be string format"):
        Wallet("solonet").sign(int())
    # verify
    with pytest.raises(TypeError, match="message must be string format"):
        Wallet("solonet").verify(int(), bool())
    with pytest.raises(TypeError, match="signature must be string format"):
        Wallet("solonet").verify(str(), float())

    with pytest.raises(TypeError, match=r".*'bytes' or 'string'.*"):
        get_bytes(float())

    with pytest.raises(ValueError, match="Bad seed, resulting in invalid key!"):
        bad_seed_checker(str(), True)

    with pytest.raises(ValueError, match="Bad seed, resulting in invalid key!"):
        bad_seed_checker(b"", False)
