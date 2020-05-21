#!/usr/bin/env python3

import hmac
import hashlib

from ..libs.segwit import encode
from ..libs.ed25519 import (encodepoint, decodepoint, decodeint, scalarmultbase, edwards_add)
from .utils import prune_intermediate_scalar, get_bytes, bad_seed_checker


# Constant values
HARDEN = 0x80000000
# Derivation Path
PATH = "m/44/153/1/0/1"
# Derivation Indexes
INDEXES = [
    "2c000000",  # 44
    "99000000",  # 153
    "01000000",  # 1 Account
    "00000000",  # 0 Change
    "01000000"  # 1 Address
]


def get_xpublic_key(xprivate_key):
    """
    Get bytom xpublic key from xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :return: str -- Bytom xpublic key.

    >>> from pybytom.wallet.tools import get_xpublic_key
    >>> get_xpublic_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    """

    # Checking parameters
    if not isinstance(xprivate_key, str):
        raise TypeError("xprivate key must be string format")

    xprivate_bytes = get_bytes(xprivate_key)
    scalar = decodeint(xprivate_bytes[:len(xprivate_bytes) // 2])
    buf = encodepoint(scalarmultbase(scalar))
    xpublic_key = buf + xprivate_bytes[len(xprivate_bytes) // 2:]
    return xpublic_key.hex()


def get_expand_xprivate_key(xprivate_key):
    """
    Get bytom expand xprivate key from xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :return: str -- Bytom expand xprivate key.

    >>> from pybytom.wallet.tools import get_expand_xprivate_key
    >>> get_expand_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
    """

    # Checking parameters
    if not isinstance(xprivate_key, str):
        raise TypeError("xprivate key must be string format")

    i = hmac.HMAC(b"Expand", get_bytes(xprivate_key),
                  digestmod=hashlib.sha512).hexdigest()
    il, ir = i[:64], i[64:]
    bad_seed_checker(ir, True)

    expand_xprivate_key = xprivate_key[:64] + ir
    return expand_xprivate_key


def indexes_to_path(indexes):
    """
    Change derivation indexes to path.

    :param indexes: Bytom derivation indexes.
    :type indexes: list.
    :return: str -- Bytom derivation path.

    >>> from pybytom.wallet.tools import indexes_to_path
    >>> indexes_to_path(["2c000000", "99000000", "01000000", "00000000", "01000000"])
    "m/44/153/1/0/1"
    """

    # Checking parameters
    if not isinstance(indexes, list):
        raise TypeError("indexes must be list format")

    path = "m/"
    for i, index in enumerate(indexes, 1):
        number = int.from_bytes(bytes.fromhex(index), byteorder="little")
        if i == len(indexes):
            path = path + str(number)
        else:
            path = path + str(number) + "/"
    return path


def path_to_indexes(path):
    """
    Change derivation path to indexes.

    :param path: Bytom derivation path.
    :type path: str.
    :return: list -- Bytom derivation indexes.

    >>> from pybytom.wallet.tools import path_to_indexes
    >>> path_to_indexes("m/44/153/1/0/1")
    ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    """

    # Checking parameters
    if not isinstance(path, str):
        raise TypeError("path must be string format")
    if str(path)[0:2] != "m/":
        raise ValueError("bad path, insert like this type of path \"m/0'/0\"! ")

    indexes = list()
    for index in path.lstrip("m/").split("/"):
        if "'" in index:
            index = int(int(index[:-1]) + HARDEN).to_bytes(4, byteorder="little").hex()
            indexes.append(index)
        else:
            index = int(int(index)).to_bytes(4, byteorder="little").hex()
            indexes.append(index)
    return indexes


def get_child_xprivate_key(xprivate_key, indexes=None, path=None):
    """
    Get bytom get child xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- Bytom child xprivate key.

    >>> from pybytom.wallet.tools import get_child_xprivate_key
    >>> get_child_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "00ca8555655d336c4c0d11464a1d401f0cc7c29fdc52bf52f5fc8e0ced32ee51b9c62d145693b366cde5ba74a06962bfa9f6b1e810a3e15eadf791247333547e"
    """

    # Checking parameters
    if not isinstance(xprivate_key, str):
        raise TypeError("xprivate key must be string format")
    if indexes is None and path is None:
        indexes = INDEXES
    elif indexes is not None:
        if not isinstance(indexes, list):
            raise TypeError("indexes must be list format")
    elif path is not None:
        if not isinstance(path, str):
            raise TypeError("path must be string format")
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


def get_child_xpublic_key(xpublic_key, indexes=None, path=None):
    """
    Get bytom get child xpublic key.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- Bytom child xpublic key.

    >>> from pybytom.wallet.tools import get_child_xpublic_key
    >>> get_child_xpublic_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
    """

    # Checking parameters
    if not isinstance(xpublic_key, str):
        raise TypeError("xpublic key must be string format")
    if indexes is None and path is None:
        indexes = INDEXES
    elif indexes is not None:
        if not isinstance(indexes, list):
            raise TypeError("indexes must be list format")
    elif path is not None:
        if not isinstance(path, str):
            raise TypeError("path must be string format")
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


def get_private_key(xprivate_key, indexes=None, path=None):
    """
    Get bytom private key from xprivate key. This is also the same with get_child_xprivate_key function.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- Bytom private key.

    >>> from pybytom.wallet.tools import get_private_key
    >>> get_private_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
    """

    return get_child_xprivate_key(
        xprivate_key=xprivate_key, indexes=indexes, path=path)


def get_public_key(xpublic_key=None, indexes=None, path=None):
    """
    Get bytom public key from xpublic key.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"].
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- Bytom public key.

    >>> from pybytom.wallet.tools import get_public_key
    >>> get_public_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
    """

    return get_child_xpublic_key(
            xpublic_key=xpublic_key, indexes=indexes, path=path)[:64]


def get_program(public_key):
    """
    Get bytom control program from public key.

    :param public_key: Bytom public key.
    :type public_key: str.
    :return: str -- Bytom control program.

    >>> from pybytom.wallet.tools import get_program
    >>> get_program("91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2")
    "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"
    """

    # Checking parameters
    if not isinstance(public_key, str):
        raise TypeError("public key must be string format")

    public_byte = get_bytes(public_key)
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(public_byte)
    public_hash = ripemd160.hexdigest()
    control_program = "0014" + public_hash
    return control_program


def get_address(program, network="solonet"):
    """
    Get bytom address from program.

    :param program: Bytom control program.
    :type program: str.
    :param network: Bytom network, default to solonet.
    :type network: str.
    :return: str -- Bytom address.

    >>> from pybytom.wallet.tools import get_address
    >>> get_address("00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "mainnet")
    "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
    """

    if not isinstance(program, str):
        raise TypeError("program must be string format")
    if not isinstance(network, str):
        raise TypeError("network must be string format")

    if network not in "mainnet/solonet/testnet".split("/"):
        raise ValueError("invalid network option, choose only mainnet, solonet and testnet network")
    elif network == "mainnet":
        return encode("bm", 0, get_bytes(program[4:]))
    elif network == "solonet":
        return encode("sm", 0, get_bytes(program[4:]))
    elif network == "testnet":
        return encode("tm", 0, get_bytes(program[4:]))


def get_vapor_address(program, network="solonet"):
    """
    Get bytom vapor address from program.

    :param program: Bytom control program.
    :type program: str.
    :param network: Bytom network, default to solonet.
    :type network: str.
    :return: str -- Bytom vapor address.

    >>> from pybytom.wallet.tools import get_vapor_address
    >>> get_vapor_address("00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "mainnet")
    "vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag"
    """

    if not isinstance(program, str):
        raise TypeError("program must be string format")
    if not isinstance(network, str):
        raise TypeError("network must be string format")

    if network not in "mainnet/solonet/testnet".split("/"):
        raise ValueError("invalid network option, choose only mainnet, solonet and testnet network")
    elif network == "mainnet":
        return encode("vp", 0, get_bytes(program[4:]))
    elif network == "solonet":
        return encode("sp", 0, get_bytes(program[4:]))
    elif network == "testnet":
        return encode("tp", 0, get_bytes(program[4:]))
