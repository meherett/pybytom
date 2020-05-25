#!/usr/bin/env python3


def spend_utxo(utxo: str) -> dict:
    """
    Get spend UTXO action.

    :param utxo: Bytom utxo id.
    :type utxo: str
    :returns: dict -- Bytom spend utxo action.

    >>> from pybytom.transaction.actions import spend_utxo
    >>> spend_utxo("169a45be47583f7240115c9059cd0d03e4d4fab70a41536cf298d6f261c0a1ac")
    {'type': 'spend_utxo, 'output_id': '169a45be47583f7240115c9059cd0d03e4d4fab70a41536cf298d6f261c0a1ac'}
    """

    return dict(type=str("spend_utxo"), output_id=utxo)


def spend_wallet(amount: int, asset: str) -> dict:
    """
    Get spend wallet action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :returns: dict -- Bytom spend wallet action.

    >>> from pybytom.transaction.actions import spend_wallet
    >>> spend_wallet(100000000, "41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a")
    {'type': 'spend_wallet', 'amount': 100000000, 'asset': '41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a'}
    """

    return dict(
        type=str("spend_wallet"),
        amount=amount, asset=asset
    )


def control_program(amount: int, asset: str, program: str) -> dict:
    """
    Get control program action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :param program: Bytom control program.
    :type program: str
    :returns: dict -- Bytom control program action.

    >>> from pybytom.transaction.actions import control_program
    >>> control_program(10000, "41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a", "0020e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3")
    {'type': 'control_program', 'amount': 10000, 'asset': '41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a', 'control_program': '0020e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3'}
    """

    return dict(
        type=str("control_program"),
        amount=amount, asset=asset,
        control_program=program
    )


def control_address(amount: int, asset: str, address: str) -> dict:
    """
    Get control address action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :param address: Bytom address.
    :type address: str
    :returns: dict -- Bytom control address action.

    >>> from pybytom.transaction.actions import control_address
    >>> control_address(10000000, "41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a", "bm1qzx7pjr6whcaxmh9u0thkjuavf2ynk3zkgshhle")
    {'type': 'control_address', 'amount': 10000000, 'asset': '41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a', 'address': 'bm1qzx7pjr6whcaxmh9u0thkjuavf2ynk3zkgshhle'}
    """

    return dict(
        type=str("control_address"),
        amount=amount, asset=asset, address=address
    )
