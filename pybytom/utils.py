#!/usr/bin/env python3

from binascii import hexlify
from mnemonic.mnemonic import Mnemonic
from typing import Optional, Union

import os

from .libs.segwit import decode
from .exceptions import SymbolError
from .config import config

# Bytom config
config = config()


def generate_entropy(strength=128) -> str:
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


def generate_mnemonic(language="english", strength=128) -> str:
    """
    Generate 12 word mnemonic.

    :param language: Mnemonic language, default to english.
    :type language: str
    :param strength: Entropy strength, default to 128.
    :type strength: int
    :returns: str -- 12 word mnemonic.

    >>> from pybytom.utils import generate_mnemonic
    >>> generate_mnemonic(language="french")
    "sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure"
    """

    if language and language not in ["english", "french", "italian", "japanese",
                                     "chinese_simplified", "chinese_traditional", "korean", "spanish"]:
        raise ValueError("invalid language, use only this options english, french, "
                         "italian, spanish, chinese_simplified, chinese_traditional, japanese or korean languages.")
    if strength not in [128, 160, 192, 224, 256]:
        raise ValueError(
            "Strength should be one of the following "
            "[128, 160, 192, 224, 256], but it is not (%d)."
            % strength
        )

    return Mnemonic(language=language).generate(strength=strength)


def is_mnemonic(mnemonic, language=None) -> bool:
    """
    Check 12 word mnemonic is Valid.

    :param mnemonic: 12 word mnemonic.
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
        raise ValueError("invalid language, use only this options english, french, "
                         "italian, spanish, chinese_simplified, chinese_traditional, japanese or korean languages.")
    try:
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


def get_mnemonic_language(mnemonic) -> Optional[str]:
    """
    Get mnemonic language.

    :param mnemonic: 12 word mnemonic.
    :type mnemonic: str
    :returns: str -- Mnemonic language.

    >>> from pybytom.utils import get_mnemonic_language
    >>> get_mnemonic_language("sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")
    "french"
    """

    if not is_mnemonic(mnemonic=mnemonic):
        raise ValueError("invalid 12 word mnemonic.")

    language = None
    for _language in ["english", "french", "italian",
                      "chinese_simplified", "chinese_traditional", "japanese", "korean", "spanish"]:
        if Mnemonic(language=_language).check(mnemonic=mnemonic) is True:
            language = _language
            break
    return language


def amount_converter(amount: float, symbol: str = "NEU2BTM") -> Union[int, float]:
    """
    Amount converter

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
    raise TypeError("network must be string format")


def is_address(address, network=None) -> bool:
    """
    Check Bytom address.

    :param address: Bytom address.
    :type address: str
    :param network: Bytom network, defaults to None.
    :type network: str
    :returns: bool -- Bytom valid/invalid address.

    >>> from pybytom.utils import is_address
    >>> is_address("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "mainnet")
    True
    """

    if isinstance(address, str):
        if network is None:
            for hrp in ["bm", "sm", "tm"]:
                valid = False
                if address.startswith(hrp) and \
                        not decode(hrp, address) == (None, None):
                    valid = True
                    break
            return valid
        if not isinstance(network, str):
            raise TypeError("network must be string format")
        elif network == "mainnet":
            return address.startswith("bm") and not decode("bm", address) == (None, None)
        elif network == "solonet":
            return address.startswith("sm") and not decode("sm", address) == (None, None)
        elif network == "testnet":
            return address.startswith("tm") and not decode("tm", address) == (None, None)
        else:
            raise ValueError("invalid network, use only this options mainnet, solonet or testnet networks.")
    raise TypeError("address must be string format")


def is_vapor_address(address, network=None) -> bool:
    """
    Check Bytom vapor address.

    :param address: Bytom vapor address.
    :type address: str
    :param network: Bytom network, defaults to None.
    :type network: str
    :returns: bool -- Bytom valid/invalid address.

    >>> from pybytom.utils import is_vapor_address
    >>> is_vapor_address("vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", "mainnet")
    True
    """

    if isinstance(address, str):
        if network is None:
            for hrp in ["vp", "sp", "tp"]:
                valid = False
                if address.startswith(hrp) and \
                        not decode(hrp, address) == (None, None):
                    valid = True
                    break
            return valid
        if not isinstance(network, str):
            raise TypeError("network must be string format")
        elif network == "mainnet":
            return address.startswith("vp") and not decode("vp", address) == (None, None)
        elif network == "solonet":
            return address.startswith("sp") and not decode("sp", address) == (None, None)
        elif network == "testnet":
            return address.startswith("tp") and not decode("tp", address) == (None, None)
        else:
            raise ValueError("invalid network, use only this options mainnet, solonet or testnet networks.")
    raise TypeError("address must be string format")
