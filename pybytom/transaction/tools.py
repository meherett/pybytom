#!/usr/bin/env python3

from ..rpc import get_transaction


def find_contract_utxo_id(transaction_id, network):
    """
    Find Bytom smart contract UTXO id by transaction id/hash.

    :param transaction_id: Bytom transaction id/hash.
    :type transaction_id: str
    :param network: Bytom network.
    :type network: str
    :returns: str -- UTXO id.

    >>> from pybytom.transaction.tools import find_contract_utxo_id
    >>> find_contract_utxo_id("e4d4fab70a41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03", "mainnet")
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
