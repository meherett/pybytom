#!/usr/bin/env python3

from ..utils import (
    amount_converter, is_address
)
from ..exceptions import (
    SymbolError, AddressError
)
from ..config import config


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


def spend_wallet(amount: float, asset: str, symbol: str = "NEU") -> dict:
    """
    Get spend wallet action.

    :param amount: Bytom amount.
    :type amount: float
    :param asset: Bytom asset.
    :type asset: str
    :param symbol: Bytom symbol, default to NEU
    :type symbol: str

    :returns: dict -- Bytom spend wallet action.

    >>> from pybytom.transaction.actions import spend_wallet
    >>> spend_wallet(10_000_000, "41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a")
    {'type': 'spend_wallet', 'amount': '0.1', 'asset': '41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a'}
    """

    if symbol.startswith("BTM"):
        amount = amount
    elif symbol.startswith("mBTM"):
        amount = amount_converter(amount, symbol="mBTM2BTM")
    elif symbol.startswith("NEU"):
        amount = amount_converter(amount, symbol="NEU2BTM")
    else:
        raise SymbolError(f"Invalid '{symbol}' symbol/type",
                          "choose only 'BTM', 'mBTM' or 'NEU' symbols.")

    return dict(
        type=str("spend_wallet"),
        amount=str(amount), asset=asset
    )


def control_program(amount: float, asset: str, program: str, symbol: str = "NEU") -> dict:
    """
    Get control program action.

    :param amount: Bytom amount.
    :type amount: float
    :param asset: Bytom asset.
    :type asset: str
    :param program: Bytom control program.
    :type program: str
    :param symbol: Bytom symbol, default to NEU
    :type symbol: str

    :returns: dict -- Bytom control program action.

    >>> from pybytom.transaction.actions import control_program
    >>> control_program(10_000_000, "41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a", "0020e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3")
    {'type': 'control_program', 'amount': '0.1', 'asset': '41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a', 'control_program': '0020e47eaf5e3a7898197068e2dd7c0209331b36a1b7a73aeb8090df816a3ce5b7d3'}
    """

    if symbol.startswith("BTM"):
        amount = amount
    elif symbol.startswith("mBTM"):
        amount = amount_converter(amount, symbol="mBTM2BTM")
    elif symbol.startswith("NEU"):
        amount = amount_converter(amount, symbol="NEU2BTM")
    else:
        raise SymbolError(f"Invalid '{symbol}' symbol/type",
                          "choose only 'BTM', 'mBTM' or 'NEU' symbols.")

    return dict(
        type=str("control_program"),
        amount=str(amount), asset=asset,
        control_program=program
    )


def control_address(amount: float, asset: str, address: str,
                    vapor: bool = config["vapor"], symbol: str = "NEU") -> dict:
    """
    Get control address action.

    :param amount: Bytom amount.
    :type amount: float
    :param asset: Bytom asset.
    :type asset: str
    :param address: Bytom address.
    :type address: str
    :param symbol: Bytom symbol, default to NEU
    :type symbol: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :returns: dict -- Bytom control address action.

    >>> from pybytom.transaction.actions import control_address
    >>> control_address(10_000_000, "41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a", "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7")
    {'type': 'control_address', 'amount': '0.1', 'asset': '41536cf298d6f261c0a1ac169a45be47583f7240115c9059cd0d03e4d4fab70a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7'}
    """

    if vapor and not is_address(address=address, vapor=True):
        raise AddressError(f"Invalid recipient '{address}' vapor address.")
    elif not vapor and not is_address(address=address, vapor=False):
        raise AddressError(f"Invalid recipient '{address}' address.")

    if symbol.startswith("BTM"):
        amount = amount
    elif symbol.startswith("mBTM"):
        amount = amount_converter(amount, symbol="mBTM2BTM")
    elif symbol.startswith("NEU"):
        amount = amount_converter(amount, symbol="NEU2BTM")
    else:
        raise SymbolError(f"Invalid '{symbol}' symbol/type",
                          "choose only 'BTM', 'mBTM' or 'NEU' symbols.")

    return dict(
        type=str("control_address"),
        amount=str(amount), asset=asset, address=address
    )
