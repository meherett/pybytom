#!/usr/bin/env python3

from binascii import unhexlify

from ..rpc import get_transaction
from ..libs.segwit import decode
from ..exceptions import NetworkError
from ..config import config


def find_smart_contract_utxo(transaction_id: str, network: str = config["network"],
                             vapor: bool = config["vapor"]) -> str:
    """
    Find Bytom smart contract UTXO id by transaction id/hash.

    :param transaction_id: Bytom transaction id/hash.
    :type transaction_id: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :returns: str -- Smart Contract UTXO id.

    >>> from pybytom.transaction.tools import find_smart_contract_utxo
    >>> find_smart_contract_utxo("e4d4fab70a41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03", "mainnet", False)
    "169a45be47583f7240115c9059cd0d03e4d4fab70a41536cf298d6f261c0a1ac"
    """

    utxo_id = None
    contract_transaction = get_transaction(
        transaction_id=transaction_id, network=network, vapor=vapor
    )
    contract_outputs = contract_transaction["outputs"]
    for contract_output in contract_outputs:
        if contract_output["address"] == "smart contract":
            utxo_id = contract_output["id"]
            break
    return utxo_id


def find_p2wsh_utxo(transaction_id: str, network: str = config["network"],
                    vapor: bool = config["vapor"]) -> str:
    """
    Find Bytom segwit pay to script hash UTXO id by transaction id/hash.

    :param transaction_id: Bytom transaction id/hash.
    :type transaction_id: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :returns: str -- Pay to Witness Secript Hash (P2WSH) UTXO id.

    >>> from pybytom.transaction.tools import find_p2wsh_utxo
    >>> find_p2wsh_utxo("0a1ac169a45be47583f72401e4d4fab70a41536cf298d6f261c15c9059cd0d03", "mainnet", False)
    "cd0d03e4d4fab70a41536cf298d6f261c0a1ac169a45be47583f7240115c9059"
    """

    utxo_id = None
    if network == "mainnet":
        hrp = "vp" if vapor else "bm"
    elif network == "solonet":
        hrp = "sp" if vapor else "sm"
    elif network == "testnet":
        hrp = "tp" if vapor else "tm"
    else:
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    contract_transaction = get_transaction(
        transaction_id=transaction_id, network=network, vapor=vapor
    )
    contract_outputs = contract_transaction["outputs"]
    for contract_output in contract_outputs:
        _, address_hash = decode(hrp, contract_output["address"])
        if address_hash is not None and \
                len(unhexlify(bytearray(address_hash).hex())) == 32:  # deep
            utxo_id = contract_output["id"]
            break
    return utxo_id
