#!/usr/bin/env python3

from typing import Optional, List

import hmac
import hashlib

from ..libs.segwit import encode
from ..libs.ed25519 import (
    encodepoint, decodepoint, decodeint, scalarmultbase, edwards_add
)
from .utils import (
    prune_intermediate_scalar, get_bytes, bad_seed_checker
)
from ..exceptions import NetworkError
from ..utils import is_network
from ..config import config


def get_xpublic_key(xprivate_key: str) -> str:
    """
    Get Bytom xpublic key from xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str

    :return: str -- Bytom xpublic key.

    >>> from pybytom.wallet.tools import get_xpublic_key
    >>> get_xpublic_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    """

    xprivate_bytes = get_bytes(xprivate_key)
    scalar = decodeint(xprivate_bytes[:len(xprivate_bytes) // 2])
    buf = encodepoint(scalarmultbase(scalar))
    xpublic_key = buf + xprivate_bytes[len(xprivate_bytes) // 2:]
    return xpublic_key.hex()


def get_expand_xprivate_key(xprivate_key: str) -> str:
    """
    Get Bytom expand xprivate key from xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str

    :return: str -- Bytom expand xprivate key.

    >>> from pybytom.wallet.tools import get_expand_xprivate_key
    >>> get_expand_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
    """

    i = hmac.HMAC(b"Expand", get_bytes(xprivate_key),
                  digestmod=hashlib.sha512).hexdigest()
    il, ir = i[:64], i[64:]
    bad_seed_checker(ir, True)

    expand_xprivate_key = xprivate_key[:64] + ir
    return expand_xprivate_key


def indexes_to_path(indexes: List[str]) -> str:
    """
    Change derivation indexes to path.

    :param indexes: Bytom derivation indexes.
    :type indexes: list

    :return: str -- Bytom derivation path.

    >>> from pybytom.wallet.tools import indexes_to_path
    >>> indexes_to_path(["2c000000", "99000000", "01000000", "00000000", "01000000"])
    "m/44/153/1/0/1"
    """

    path = "m/"
    for i, index in enumerate(indexes, 1):
        number = int.from_bytes(bytes.fromhex(index), byteorder="little")
        if i == len(indexes):
            path = path + str(number)
        else:
            path = path + str(number) + "/"
    return path


def path_to_indexes(path: str) -> List[str]:
    """
    Change derivation path to indexes.

    :param path: Bytom derivation path.
    :type path: str

    :return: list -- Bytom derivation indexes.

    >>> from pybytom.wallet.tools import path_to_indexes
    >>> path_to_indexes("m/44/153/1/0/1")
    ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    """

    if str(path)[0:2] != "m/":
        raise ValueError("bad path, insert like this type of path \"m/0'/0\"! ")

    indexes = list()
    for index in path.lstrip("m/").split("/"):
        if "'" in index:
            index = int(int(index[:-1]) + config["harden"]).to_bytes(4, byteorder="little").hex()
            indexes.append(index)
        else:
            index = int(int(index)).to_bytes(4, byteorder="little").hex()
            indexes.append(index)
    return indexes


def get_child_xprivate_key(xprivate_key: str, indexes: Optional[List[str]] = None,
                           path: Optional[str] = None) -> str:
    """
    Get Bytom get child xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list
    :param path: Bytom derivation path, default to None.
    :type path: str

    :return: str -- Bytom child xprivate key.

    >>> from pybytom.wallet.tools import get_child_xprivate_key
    >>> get_child_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "00ca8555655d336c4c0d11464a1d401f0cc7c29fdc52bf52f5fc8e0ced32ee51b9c62d145693b366cde5ba74a06962bfa9f6b1e810a3e15eadf791247333547e"
    """

    if indexes is None and path is None:
        indexes = []
    elif path is not None:
        indexes = path_to_indexes(path=path)

    for index in range(len(indexes)):
        index_bytes = get_bytes(indexes[index])
        xpublic_key = get_xpublic_key(xprivate_key=xprivate_key)
        xpublic_bytes = get_bytes(xpublic_key)
        xprivate_bytes = get_bytes(xprivate_key)
        i = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                b"N" + xpublic_bytes[:32] + index_bytes,
                                digestmod=hashlib.sha512).digest())
        il, ir = i[:32], i[32:]
        bad_seed_checker(il)

        i = prune_intermediate_scalar(il)[:32] + ir

        carry = 0
        total = 0
        for _i in range(32):
            total = xprivate_bytes[_i] + i[_i] + carry
            i[_i] = total & 0xff
            carry = total >> 8
        if (total >> 8) != 0:
            print("sum does not fit in 256-bit int")
        xprivate_key = i.hex()

    child_xprivate = xprivate_key
    return child_xprivate


def get_child_xpublic_key(xpublic_key, indexes: Optional[List[str]] = None,
                          path: Optional[str] = None) -> str:
    """
    Get Bytom get child xpublic key.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list
    :param path: Bytom derivation path, default to None.
    :type path: str

    :return: str -- Bytom child xpublic key.

    >>> from pybytom.wallet.tools import get_child_xpublic_key
    >>> get_child_xpublic_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
    """

    if indexes is None and path is None:
        indexes = []
    elif path is not None:
        indexes = path_to_indexes(path=path)

    for index in range(len(indexes)):
        index_bytes = get_bytes(indexes[index])
        xpublic_bytes = get_bytes(xpublic_key)
        i = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                b"N" + xpublic_bytes[:32] + index_bytes,
                                digestmod=hashlib.sha512).digest())

        il, ir = i[:32], i[32:]
        bad_seed_checker(il)

        f = bytes(prune_intermediate_scalar(il))
        scalar = decodeint(f)
        f = scalarmultbase(scalar)

        p = decodepoint(xpublic_bytes[:32])
        p = edwards_add(p, f)
        public_key = encodepoint(p)

        xpublic_bytes = public_key[:32] + ir
        xpublic_key = xpublic_bytes.hex()

    child_xpublic = xpublic_key
    return child_xpublic


def get_private_key(xprivate_key: str, indexes: Optional[List[str]] = None,
                    path: Optional[str] = None) -> str:
    """
    Get Bytom private key from xprivate key. This is also the same with get_child_xprivate_key function.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list
    :param path: Bytom derivation path, default to None.
    :type path: str

    :return: str -- Bytom private key.

    >>> from pybytom.wallet.tools import get_private_key
    >>> get_private_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
    """

    return get_child_xprivate_key(
        xprivate_key=xprivate_key, indexes=indexes, path=path)


def get_public_key(xpublic_key: str, indexes: Optional[List[str]] = None,
                   path: Optional[str] = None) -> str:
    """
    Get Bytom public key from xpublic key.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list
    :param path: Bytom derivation path, default to None.
    :type path: str

    :return: str -- Bytom public key.

    >>> from pybytom.wallet.tools import get_public_key
    >>> get_public_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
    """

    return get_child_xpublic_key(
            xpublic_key=xpublic_key, indexes=indexes, path=path)[:64]


def get_program(public_key: str) -> str:
    """
    Get Bytom control program from public key.

    :param public_key: Bytom public key.
    :type public_key: str
    :return: str -- Bytom control program.

    >>> from pybytom.wallet.tools import get_program
    >>> get_program("91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2")
    "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"
    """

    public_byte = get_bytes(public_key)
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(public_byte)
    public_hash = ripemd160.hexdigest()
    control_program = "0014" + public_hash
    return control_program


def get_address(program: str, network: str = config["network"], vapor: bool = config["vapor"]) -> str:
    """
    Get Bytom address from program.

    :param program: Bytom control program.
    :type program: str
    :param network: Bytom network, default to mainnet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :return: str -- Bytom address.

    >>> from pybytom.wallet.tools import get_address
    >>> get_address("00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "mainnet", False)
    "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
    >>> get_address("00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "mainnet", True)
    "vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    elif network == "mainnet" and not vapor:
        return encode("bm", 0, get_bytes(program[4:]))
    elif network == "solonet" and not vapor:
        return encode("sm", 0, get_bytes(program[4:]))
    elif network == "testnet" and not vapor:
        return encode("tm", 0, get_bytes(program[4:]))
    elif network == "mainnet" and vapor:
        return encode("vp", 0, get_bytes(program[4:]))
    elif network == "solonet" and vapor:
        return encode("sp", 0, get_bytes(program[4:]))
    elif network == "testnet" and vapor:
        return encode("tp", 0, get_bytes(program[4:]))
