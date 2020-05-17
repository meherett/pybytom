#!/usr/bin/env python3

from ..rpc import get_transaction


def find_contract_utxo_id(transaction_id, network):
    """
    Find smart contract UTXO id.

    :param transaction_id: Bytom transaction id or hash.
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


def spend_utxo_action(utxo):
    """
    Get spend UTXO action

    :param utxo: Bytom utxo id.
    :type utxo: str
    :returns: dict -- Bytom spend utxo action.

    >>> from pybytom.transaction.tools import spend_utxo_action
    >>> spend_utxo_action(bytom_utxo_id)
    {'type': 'spend_utxo, 'output_id': '...'}
    """

    return dict(type=str("spend_utxo"), output_id=utxo)


def contract_arguments(amount, address, value=None):
    """
    Get contract arguments.

    :param amount: Bytom amount.
    :type amount: int
    :param address: Bytom address.
    :type address: str
    :param value: value, default to None.
    :type value: str
    :returns: list -- Bytom contract arguments.

    >>> from pybytom.transaction.tools import contract_arguments
    >>> contract_arguments(bytom_amount, bytom_address)
    [{'integer': 100}, {'address': '...'}, {'data': ''}]
    """

    return [
        dict(type=str("integer"), value=amount),
        dict(type=str("address"), value=address),
        dict(type=str("data"), value=str() if value is None else value)
    ]


def spend_wallet_action(amount, asset):
    """
    Get spend wallet action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :returns: dict -- Bytom spend wallet action.

    >>> from pybytom.transaction.tools import spend_wallet_action
    >>> spend_wallet_action(bytom_amount, bytom_asset)
    {'type': 'spend_wallet', 'amount': 100, 'asset': '...'}
    """

    return dict(
        type=str("spend_wallet"),
        amount=amount, asset=asset
    )


def spend_account_action(account, amount, asset):
    """
    Get spend account action.

    :param account: Bytom account.
    :type account: str
    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :returns: dict -- Bytom spend account action.

    >>> from pybytom.transaction.tools import spend_account_action
    >>> spend_account_action(bytom_account, bytom_amount, bytom_asset)
    {type: 'spend_account', account='...', amount=1000, asset='...'}
    """

    return dict(type=str("spend_account"),
                account=account, amount=amount, asset=asset)


def control_program_action(amount, asset, control_program):
    """
    Get control program action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :param control_program: Bytom control program.
    :type control_program: str
    :returns: dict -- Bytom control program action.

    >>> from pybytom.transaction.tools import control_program_action
    >>> control_program_action(bytom_amount, bytom_asset, bytom_control_program)
    {'type': 'control_program', 'amount': 100, 'asset': '...', 'control_program': '...'}
    """

    return dict(
        type=str("control_program"),
        amount=amount, asset=asset,
        control_program=control_program
    )


def control_address_action(amount, asset, address):
    """
    Get control address action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :param address: Bytom address.
    :type address: str
    :returns: dict -- Bytom control address action.

    >>> from pybytom.transaction.tools import control_address_action
    >>> control_address_action(bytom_amount, bytom_asset, bytom_address)
    {'type': 'control_address', 'amount': 10000000, 'asset': '...', 'address': '...'}
    """

    return dict(
        type=str("control_address"),
        amount=amount, asset=asset, address=address
    )
