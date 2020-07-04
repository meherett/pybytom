#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from mnemonic.mnemonic import Mnemonic

import os

from .libs.segwit import decode


def generate_entropy(strength=128):
    """
    Generate entropy hex string.

    :param strength: Entropy strength, default to 128.
    :type strength: str.
    :returns:  entropy -- Entropy hex string.

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


def generate_mnemonic(language="english", strength=128):
    """
    Generate 12 word mnemonic.

    :param language: Mnemonic language, default to english.
    :type language: str.
    :param strength: Entropy strength, default to 128.
    :type strength: str.
    :returns:  mnemonic -- 12 word mnemonic.

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


def is_mnemonic(mnemonic, language=None):
    """
    Check 12 word mnemonic is Valid.

    :param mnemonic: 12 word mnemonic.
    :type mnemonic: str.
    :param language: Mnemonic language, default to None.
    :type language: str.
    :returns:  mnemonic -- True/False.

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


def get_mnemonic_language(mnemonic):
    """
    Get mnemonic language.

    :param mnemonic: 12 word mnemonic.
    :type mnemonic: str.
    :returns:  language -- Mnemonic language.

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


def is_address(address, network=None):
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
