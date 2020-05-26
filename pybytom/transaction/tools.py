#!/usr/bin/env python3

from binascii import unhexlify

from ..rpc import get_transaction
from ..libs.segwit import decode


def find_smart_contract_utxo(transaction_id, network):
    """
    Find Bytom smart contract UTXO id by transaction id/hash.

    :param transaction_id: Bytom transaction id/hash.
    :type transaction_id: str
    :param network: Bytom network.
    :type network: str
    :returns: str -- UTXO id.

    >>> from pybytom.transaction.tools import find_smart_contract_utxo
    >>> find_smart_contract_utxo("e4d4fab70a41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03", "mainnet")
    "169a45be47583f7240115c9059cd0d03e4d4fab70a41536cf298d6f261c0a1ac"
    """

    utxo_id = None
    contract_transaction = get_transaction(
        transaction_id=transaction_id, network=network)
    contract_outputs = contract_transaction["outputs"]
    for contract_output in contract_outputs:
        if contract_output["address"] == "smart contract":
            utxo_id = contract_output["utxo_id"]
            break
    return utxo_id


def find_p2wsh_utxo(transaction_id, network):
    """
    Find Bytom segwit pay to script hash UTXO id by transaction id/hash.

    :param transaction_id: Bytom transaction id/hash.
    :type transaction_id: str
    :param network: Bytom network.
    :type network: str
    :returns: str -- UTXO id.

    >>> from pybytom.transaction.tools import find_p2wsh_utxo
    >>> find_p2wsh_utxo("0a1ac169a45be47583f72401e4d4fab70a41536cf298d6f261c15c9059cd0d03", "mainnet")
    "cd0d03e4d4fab70a41536cf298d6f261c0a1ac169a45be47583f7240115c9059"
    """

    utxo_id = None
    if network == "mainnet":
        hrp = "bm"
    elif network == "solonet":
        hrp = "sm"
    elif network == "testnet":
        hrp = "tm"
    else:
        raise ValueError("invalid network option, choose only mainnet, solonet or testnet network")
    contract_transaction = get_transaction(
        transaction_id=transaction_id, network=network)
    contract_outputs = contract_transaction["outputs"]
    for contract_output in contract_outputs:
        try:
            _, address_hash = decode(hrp, contract_output["address"])
        except TypeError:
            continue
        if len(unhexlify(address_hash)) == 32:  # deep
            utxo_id = contract_output["utxo_id"]
            break
    return utxo_id
