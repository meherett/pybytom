#!/usr/bin/env python3

from binascii import unhexlify
from hashlib import (
    new, sha3_256
)

from ..libs.segwit import encode
from ..exceptions import NetworkError
from ..utils import is_network
from ..config import config
from .opcode import (
    OP_DUP, OP_HASH160, OP_SHA3, OP_EQUALVERIFY, OP_TXSIGHASH, OP_SWAP, OP_CHECKPREDICATE, OP_CHECKSIG
)
from .builder import Builder


def get_public_key_hash(public_key: str) -> str:
    """
    Get Bytom public key hash.

    :param public_key: Bytom contract program(bytecode).
    :type public_key: str

    :return: str -- Public key ripemd160 hash.

    >>> from pybytom.script import get_public_key_hash
    >>> get_public_key_hash(public_key="5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2")
    "875240ba66646d900c59dd20d843351c2fcbeedc"
    """

    ripemd160 = new("ripemd160")
    ripemd160.update(unhexlify(public_key))
    public_hash = ripemd160.hexdigest()
    return public_hash


def get_script_hash(bytecode: str) -> str:
    """
    Get Bytom Smart Contract program(bytecode) script hash.

    :param bytecode: Bytom contract program(bytecode).
    :type bytecode: str

    :return: str -- Smart Contract program script SHA3-256 hash.

    >>> from pybytom.script import get_script_hash
    >>> get_script_hash(bytecode="7baa8800c3c251547ac1")
    "e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3"
    """

    return sha3_256(unhexlify(bytecode)).hexdigest()


def get_p2pkh_program(public_key_hash: str) -> str:
    """
    Get Pay to Public Key Hash (P2PKH) program.

    :param public_key_hash: Bytom public key hash.
    :type public_key_hash: str

    :return: str -- Bytom Pay to Public Key Hash (P2PKH) program.

    >>> from pybytom.script import get_p2pkh_program
    >>> get_p2pkh_program(public_key_hash="875240ba66646d900c59dd20d843351c2fcbeedc")
    "76ab14875240ba66646d900c59dd20d843351c2fcbeedc88ae7cac"
    """

    builder: Builder = Builder()
    builder.add_op(OP_DUP)
    builder.add_op(OP_HASH160)
    builder.add_bytes(unhexlify(public_key_hash))
    builder.add_op(OP_EQUALVERIFY)
    builder.add_op(OP_TXSIGHASH)
    builder.add_op(OP_SWAP)
    builder.add_op(OP_CHECKSIG)
    return builder.hex_digest()


def get_p2wpkh_program(public_key_hash: str) -> str:
    """
    Get Pay to Witness Public Key Hash (P2WPKH) program.

    :param public_key_hash: Bytom public key hash.
    :type public_key_hash: str

    :return: str -- Bytom Pay to Witness Public Key Hash (P2WPKH) program.

    >>> from pybytom.script import get_p2wpkh_program
    >>> get_p2wpkh_program(public_key_hash="875240ba66646d900c59dd20d843351c2fcbeedc")
    "0014875240ba66646d900c59dd20d843351c2fcbeedc"
    """

    builder: Builder = Builder()
    builder.add_int(0)
    builder.add_bytes(unhexlify(public_key_hash))
    return builder.hex_digest()


def get_p2wpkh_address(public_key_hash: str, network: str = config["network"], vapor: bool = config["vapor"]) -> str:
    """
    Get Pay to Witness Public Key Hash (P2WPKH) address.

    :param public_key_hash: Bytom public key hash.
    :type public_key_hash: str
    :param network: Bytom network, default to mainnet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :return: str -- Bytom Pay to Witness Public Key Hash (P2WPKH) address.

    >>> from pybytom.script import get_p2wpkh_address
    >>> get_p2wpkh_address(public_key_hash="875240ba66646d900c59dd20d843351c2fcbeedc", vapor=False)
    "bm1qsafypwnxv3keqrzem5sdsse4rshuhmku7kpnxq"
    >>> get_p2wpkh_address(public_key_hash="875240ba66646d900c59dd20d843351c2fcbeedc", vapor=True)
    "vp1qsafypwnxv3keqrzem5sdsse4rshuhmku4h3wrk"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if len(unhexlify(public_key_hash)) != 20:
        raise ValueError("Invalid script hash, witness program must be 20 bytes for p2wpkh.")

    if network == "mainnet" and not vapor:
        return encode("bm", 0x00, unhexlify(public_key_hash))
    elif network == "solonet" and not vapor:
        return encode("sm", 0x00, unhexlify(public_key_hash))
    elif network == "testnet" and not vapor:
        return encode("tm", 0x00, unhexlify(public_key_hash))
    elif network == "mainnet" and vapor:
        return encode("vp", 0x00, unhexlify(public_key_hash))
    elif network == "solonet" and vapor:
        return encode("sp", 0x00, unhexlify(public_key_hash))
    elif network == "testnet" and vapor:
        return encode("tp", 0x00, unhexlify(public_key_hash))


def get_p2sh_program(script_hash: str) -> str:
    """
    Get Pay to Script Hash (P2SH) program.

    :param script_hash: Bytom contract program(bytecode) script hash.
    :type script_hash: str

    :return: str -- Bytom Pay to Script Hash (P2SH) program.

    >>> from pybytom.script import get_p2sh_program
    >>> get_p2sh_program(script_hash="e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3")
    "76aa20e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d38808ffffffffffffffff7c00c0"
    """

    builder: Builder = Builder()
    builder.add_op(OP_DUP)
    builder.add_op(OP_SHA3)
    builder.add_bytes(unhexlify(script_hash))
    builder.add_op(OP_EQUALVERIFY)
    builder.add_int(-1)
    builder.add_op(OP_SWAP)
    builder.add_int(0)
    builder.add_op(OP_CHECKPREDICATE)
    return builder.hex_digest()


def get_p2wsh_program(script_hash: str) -> str:
    """
    Get Pay to Witness Script Hash (P2WSH) program.

    :param script_hash: Bytom contract program(bytecode) script hash.
    :type script_hash: str

    :return: str -- Bytom Pay to Witness Script Hash (P2WSH) program.

    >>> from pybytom.script import get_p2wsh_program
    >>> get_p2wsh_program(script_hash="e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3")
    "0020e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3"
    """

    builder: Builder = Builder()
    builder.add_int(0)
    builder.add_bytes(unhexlify(script_hash))
    return builder.hex_digest()


def get_p2wsh_address(script_hash: str, network: str = config["network"], vapor: bool = config["vapor"]) -> str:
    """
    Get Pay to Witness Script Hash (P2WSH) address.

    :param script_hash: Bytom contract program(bytecode) script hash.
    :type script_hash: str
    :param network: Bytom network, default to mainnet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :return: str -- Bytom Pay to Witness Script Hash (P2WSH) address.

    >>> from pybytom.script import get_p2wsh_address
    >>> get_p2wsh_address(script_hash="e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3", vapor=False)
    "bm1qu3l27h360zvpjurgutwhcqsfxvdndgdh5uawhqysm7qk5089klfsrrlhez"
    >>> get_p2wsh_address(script_hash="e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3", vapor=True)
    "vp1qu3l27h360zvpjurgutwhcqsfxvdndgdh5uawhqysm7qk5089klfs2r64gm"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if len(unhexlify(script_hash)) != 32:
        raise ValueError("Invalid script hash, witness program must be 32 bytes for p2wsh.")

    if network == "mainnet" and not vapor:
        return encode("bm", 0x00, unhexlify(script_hash))
    elif network == "solonet" and not vapor:
        return encode("sm", 0x00, unhexlify(script_hash))
    elif network == "testnet" and not vapor:
        return encode("tm", 0x00, unhexlify(script_hash))
    elif network == "mainnet" and vapor:
        return encode("vp", 0x00, unhexlify(script_hash))
    elif network == "solonet" and vapor:
        return encode("sp", 0x00, unhexlify(script_hash))
    elif network == "testnet" and vapor:
        return encode("tp", 0x00, unhexlify(script_hash))
