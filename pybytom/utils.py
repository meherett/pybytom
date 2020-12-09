#!/usr/bin/env python3

from binascii import hexlify
from mnemonic.mnemonic import Mnemonic
from typing import (
    Optional, Union
)

import os
import unicodedata

from .libs.segwit import decode
from .exceptions import (
    SymbolError, NetworkError
)
from .config import config


def generate_entropy(strength: int = 128) -> str:
    """
    Generate entropy hex string.

    :param strength: Entropy strength, default to 128.
    :type strength: int

    :returns: str -- Entropy hex string.

    >>> from pybytom.utils import generate_entropy
    >>> generate_entropy(strength=128)
    "ee535b143b0d9d1f87546f9df0d06b1a"
    """

    if strength not in [128, 160, 192, 224, 256]:
        raise ValueError(
            "Strength should be one of the following "
            "[128, 160, 192, 224, 256], but it is not (%d)."
            % strength
        )

    return hexlify(os.urandom(strength // 8)).decode()


def generate_mnemonic(language: str = "english", strength: int = 128) -> str:
    """
    Generate mnemonic words.

    :param language: Mnemonic language, default to english.
    :type language: str
    :param strength: Entropy strength, default to 128.
    :type strength: int

    :returns: str -- Mnemonic words.

    >>> from pybytom.utils import generate_mnemonic
    >>> generate_mnemonic(language="french")
    "sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure"
    """

    if language and language not in ["english", "french", "italian", "japanese",
                                     "chinese_simplified", "chinese_traditional", "korean", "spanish"]:
        raise ValueError("Invalid language, choose only the following options 'english', 'french', 'italian', "
                         "'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese or 'korean' languages.")
    if strength not in [128, 160, 192, 224, 256]:
        raise ValueError(
            "Strength should be one of the following "
            "[128, 160, 192, 224, 256], but it is not (%d)."
            % strength
        )

    return Mnemonic(language=language).generate(strength=strength)


def is_entropy(entropy: str) -> bool:
    """
    Check entropy hex string.

    :param entropy: Entropy hex string.
    :type entropy: str

    :returns: bool -- True/False.

    >>> from pybytom.utils import is_entropy
    >>> is_entropy("ee535b143b0d9d1f87546f9df0d06b1a")
    True
    """

    return len(entropy) in [32, 40, 48, 56, 64]


def is_mnemonic(mnemonic: str, language: Optional[str] = None) -> bool:
    """
    Check mnemonic words.

    :param mnemonic: Mnemonic words.
    :type mnemonic: str
    :param language: Mnemonic language, default to None.
    :type language: str

    :returns: bool -- True/False.

    >>> from pybytom.utils import is_mnemonic
    >>> is_mnemonic("sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")
    True
    """

    if language and language not in ["english", "french", "italian", "japanese",
                                     "chinese_simplified", "chinese_traditional", "korean", "spanish"]:
        raise ValueError("Invalid language, choose only the following options 'english', 'french', 'italian', "
                         "'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese or 'korean' languages.")
    try:
        mnemonic = unicodedata.normalize("NFKD", mnemonic)
        if language is None:
            for _language in ["english", "french", "italian",
                              "chinese_simplified", "chinese_traditional", "japanese", "korean", "spanish"]:
                valid = False
                if Mnemonic(language=_language).check(mnemonic=mnemonic) is True:
                    valid = True
                    break
            return valid
        else:
            return Mnemonic(language=language).check(mnemonic=mnemonic)
    except:
        return False


def get_mnemonic_language(mnemonic: str) -> Optional[str]:
    """
    Get mnemonic language.

    :param mnemonic: Mnemonic words.
    :type mnemonic: str

    :returns: str -- Mnemonic language.

    >>> from pybytom.utils import get_mnemonic_language
    >>> get_mnemonic_language("sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")
    "french"
    """

    if not is_mnemonic(mnemonic=mnemonic):
        raise ValueError("Invalid mnemonic words.")

    language: Optional[str] = None
    mnemonic = unicodedata.normalize("NFKD", mnemonic)
    for _language in ["english", "french", "italian",
                      "chinese_simplified", "chinese_traditional", "japanese", "korean", "spanish"]:
        if Mnemonic(language=_language).check(mnemonic=mnemonic) is True:
            language = _language
            break
    return language


def get_entropy_strength(entropy: str) -> int:
    """
    Get entropy strength.

    :param entropy: Entropy hex string.
    :type entropy: str

    :returns: int -- strength.

    >>> from pybytom.utils import get_entropy_strength
    >>> get_entropy_strength("ee535b143b0d9d1f87546f9df0d06b1a")
    128
    """

    if not is_entropy(entropy=entropy):
        raise ValueError("Invalid entropy.")

    length = len(entropy)
    if length == 32:
        return 128
    elif length == 40:
        return 160
    elif length == 48:
        return 192
    elif length == 56:
        return 224
    elif length == 64:
        return 256


def get_mnemonic_strength(mnemonic: str) -> int:
    """
    Get mnemonic strength.

    :param mnemonic: Mnemonic words.
    :type mnemonic: str

    :returns: int -- strength.

    >>> from pybytom.utils import get_mnemonic_strength
    >>> get_mnemonic_strength("sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")
    128
    """

    if not is_mnemonic(mnemonic=mnemonic):
        raise ValueError("Invalid mnemonic words.")

    words = len(unicodedata.normalize("NFKD", mnemonic).split(" "))
    if words == 12:
        return 128
    elif words == 15:
        return 160
    elif words == 18:
        return 192
    elif words == 21:
        return 224
    elif words == 24:
        return 256


def amount_converter(amount: float, symbol: str = "NEU2BTM") -> Union[int, float]:
    """
    Bytom amount converter.

    :param amount: Bytom amount.
    :type amount: float
    :param symbol: Bytom symbol, default to NEU2BTM
    :type symbol: str

    :returns: float -- BTM asset amount.

    >>> from pybytom.utils import amount_converter
    >>> amount_converter(amount=10_000_000, symbol="NEU2BTM")
    0.1
    """

    if symbol not in ["BTM2mBTM", "BTM2NEU", "mBTM2BTM", "mBTM2NEU", "NEU2BTM", "NEU2mBTM"]:
        raise SymbolError(f"Invalid '{symbol}' symbol/type",
                          "choose only 'BTM2mBTM', 'BTM2NEU', 'mBTM2BTM', 'mBTM2NEU', 'NEU2BTM' or 'NEU2mBTM' symbols.")

    # Constant values
    BTM, mBTM, NEU = (
        config["symbols"]["BTM"],
        config["symbols"]["mBTM"],
        config["symbols"]["NEU"]
    )

    if symbol == "BTM2mBTM":
        return float((amount * mBTM) / BTM)
    elif symbol == "BTM2NEU":
        return int((amount * NEU) / BTM)
    elif symbol == "mBTM2BTM":
        return float((amount * BTM) / mBTM)
    elif symbol == "mBTM2NEU":
        return int((amount * NEU) / mBTM)
    elif symbol == "NEU2BTM":
        return float((amount * BTM) / NEU)
    elif symbol == "NEU2mBTM":
        return int((amount * mBTM) / NEU)


def is_network(network: str) -> bool:
    """
    Check network type.

    :param network: Bytom network.
    :type network: str

    :returns: bool -- Checked network.

    >>> from pybytom.utils import is_network
    >>> is_network("solonet")
    True
    """

    if isinstance(network, str):
        return network.lower() in ["mainnet", "solonet", "testnet"]
    raise TypeError("Network must be string format")


def is_address(address: str, network: Optional[str] = None, vapor: bool = config["vapor"]) -> bool:
    """
    Check Bytom address.

    :param address: Bytom address.
    :type address: str
    :param network: Bytom network, defaults to None.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :returns: bool -- Bytom valid/invalid address.

    >>> from pybytom.utils import is_address
    >>> is_address("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "mainnet", False)
    True
    >>> is_address("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "mainnet", True)
    False
    >>> is_address("vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", "mainnet", True)
    True
    >>> is_address("vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", "mainnet", False)
    False
    """

    if not isinstance(address, str) and not vapor:
        raise TypeError("Address must be string format")
    elif not isinstance(address, str) and vapor:
        raise TypeError("Vapor address must be string format")

    if network is None and not vapor:
        for hrp in ["bm", "sm", "tm"]:
            valid = False
            if address.startswith(hrp) and \
                    not decode(hrp, address) == (None, None):
                valid = True
                break
        return valid
    if network is None and vapor:
        for hrp in ["vp", "sp", "tp"]:
            valid = False
            if address.startswith(hrp) and \
                    not decode(hrp, address) == (None, None):
                valid = True
                break
        return valid
    elif network == "mainnet" and not vapor:
        return address.startswith("bm") and not decode("bm", address) == (None, None)
    elif network == "solonet" and not vapor:
        return address.startswith("sm") and not decode("sm", address) == (None, None)
    elif network == "testnet" and not vapor:
        return address.startswith("tm") and not decode("tm", address) == (None, None)
    elif network == "mainnet" and vapor:
        return address.startswith("vp") and not decode("vp", address) == (None, None)
    elif network == "solonet" and vapor:
        return address.startswith("sp") and not decode("sp", address) == (None, None)
    elif network == "testnet" and vapor:
        return address.startswith("tp") and not decode("tp", address) == (None, None)
    else:
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
