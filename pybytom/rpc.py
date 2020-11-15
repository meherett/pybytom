#!/usr/bin/env python3

from typing import Optional

import requests
import json

from .utils import (
    amount_converter, is_address, is_vapor_address, is_network
)
from .exceptions import (
    APIError, NetworkError, AddressError, BalanceError
)
from .config import config

# Bytom config
config: dict = config()


def get_balance(address: str, asset: str = config["asset"], network: str = config["network"],
                vapor: bool = False, timeout: int = config["timeout"]) -> int:
    """
    Get Bytom balance.

    :param address: Bytom address.
    :type address: str
    :param asset: Bytom asset, default to BTM asset.
    :type asset: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: int -- Bytom asset balance.

    >>> from pybytom.rpc import get_balance
    >>> get_balance("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "mainnet")
    2580000000
    """
    
    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network.",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if vapor:
        if not is_vapor_address(address=address, network=network):
            raise AddressError(f"Invalid '{address}' {network} vapor address.")
        url = f"{config['vapor'][network]['blockmeta']}/address/{address}"
        response = requests.get(url=url, headers=config["headers"], timeout=timeout)
        if response.json() is None or response.json()["data"] is None:
            return 0  # 该数据不存在 -> መረጃው የለም!
        for _asset in response.json()["data"]["address"]:
            if asset == _asset["asset_id"]:
                return int(_asset["balance"])
        return 0
    else:
        if not is_address(address=address, network=network):
            raise AddressError(f"Invalid '{address}' {network} address.")
        url = f"{config['bytom'][network]['blockmeta']}/address/{address}/asset"
        response = requests.get(url=url, headers=config["headers"], timeout=timeout)
        if response.json() is None:
            return 0
        for _asset in response.json():
            if asset == _asset["asset_id"]:
                return int(_asset["balance"])
        return 0


def account_create(xpublic_key: str, label: str = "1st address", email: Optional[str] = None,
                   network: str = config["network"], timeout: int = config["timeout"]) -> dict:
    """
    Create account in blockcenter.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str
    :param label: Bytom limit, defaults to 1st address.
    :type label: str
    :param email: email address, defaults to None.
    :type email: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- Bytom blockcenter guid, address and label.

    >>> from pybytom.rpc import account_create
    >>> account_create(xpublic_key, "mainnet")
    {"guid": "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "label": "1st address"}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']['v2']}/account/create"
    data = dict(pubkey=xpublic_key, label=label, email=email)
    response = requests.post(
        url=url, data=json.dumps(data), headers=config["headers"], timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["result"]["data"]


def list_address(guid, limit: int = 10, network: str = config["network"],
                 timeout: int = config["timeout"]) -> list:
    """
    Get list address from blockcenter.

    :param guid: Bytom blockcenter guid.
    :type guid: str
    :param limit: blockcenter limit default to 10.
    :type limit: int
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: list -- Bytom blockcenter list of addresses.

    >>> from pybytom.rpc import list_address
    >>> list_address(guid, 5 "mainnet")
    [{"guid": "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "label": "1st address", "balances": [{"asset": "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf", "balance": "100000000000", "total_received": "100000000000", "total_sent": "0", "decimals": 8, "alias": "Asset", "icon": "", "name": "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf", "symbol": "Asset", "in_usd": "0.00", "in_cny": "0.00", "in_btc": "0.000000"}, {"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "balance": "2450000000", "total_received": "4950000000", "total_sent": "2500000000", "decimals": 8, "alias": "btm", "icon": "", "name": "BTM", "symbol": "BTM", "in_usd": "2.90", "in_cny": "20.58", "in_btc": "0.000283"}]}]
    """

    url = f"{config[network]['blockcenter']['v2']}/account/list-addresses"
    data, params = dict(guid=guid), dict(limit=limit)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=config["headers"], timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    if response.status_code == 200 and response.json()["code"] == 414:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()


def estimate_transaction_fee(address: str, amount: int, asset: str = config["asset"],
                             confirmations: int = config["confirmations"],
                             network: str = config["network"], timeout: int = config["timeout"]) -> str:
    """
    Estimate transaction fee.

    :param address: Bytom address.
    :type address: str
    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset id, default to BTM asset.
    :type asset: str
    :param confirmations: Bytom confirmations, default to 1.
    :type confirmations: int
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: str -- Estimated transaction fee.

    >>> from pybytom.rpc import estimate_transaction_fee
    >>> estimate_transaction_fee(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", amount=100_000_000, confirmations=6, network="mainnet")
    "0.0044900000"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid '{address}' {network} address.")

    url = f"{config[network]['mov']}/merchant/estimate-tx-fee"
    data = dict(
        asset_amounts={
            asset: str(amount_converter(amount=amount, symbol="NEU2BTM"))
        },
        confirmations=confirmations
    )
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=config["headers"], timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["data"]["fee"]


def build_transaction(address: str, transaction: dict, network: str = config["network"],
                      vapor: bool = False, timeout: int = config["timeout"]) -> dict:
    """
    Build Bytom transaction in blockcenter.

    :param address: Bytom address.
    :type address: str
    :param transaction: Bytom transaction.
    :type transaction: dict
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom built transaction.

    >>> from pybytom.rpc import build_transaction
    >>> build_transaction(address, transaction, "mainnet")
    {"transaction": {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utransactiono_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utransactiono_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}, "raw_transaction": "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", "signing_instructions": [{"derivation_path": ["2c000000", "99000000", "01000000", "00000000", "01000000"], "sign_data": ["37727d44af9801e9723eb325592f4d55cc8d7e3815b1d663d61b7f1af9fc13a7"], "pubkey": "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"}], "fee": 10000000}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if vapor:
        if not is_vapor_address(address=address, network=network):
            raise AddressError(f"Invalid '{address}' {network} vapor address.")
        url = f"{config['vapor'][network]['blockcenter']}/merchant/build-advanced-tx"
    else:
        if not is_address(address=address, network=network):
            raise AddressError(f"Invalid '{address}' {network} address.")
        url = f"{config['bytom'][network]['blockcenter']}/merchant/build-advanced-tx"
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(transaction),
        params=params, headers=config["headers"], timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 422:
        raise BalanceError(f"There is no any asset balance recorded on this '{address}' address.")
    elif response.status_code == 200 and response.json()["code"] == 515:
        raise BalanceError(f"Insufficient balance, check your balance and try again.")
    return response.json()["data"][0]


def get_transaction(transaction_id: str, network: str = config["network"],
                    vapor: bool = False, timeout: int = config["timeout"]) -> dict:
    """
    Get Bytom transaction detail.

    :param transaction_id: Bytom transaction id.
    :type transaction_id: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom transaction detail.

    >>> from pybytom.rpc import get_transaction
    >>> get_transaction(transaction_id, "mainnet")
    {"transaction": {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utransactiono_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utransactiono_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}, "raw_transaction": "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", "signing_instructions": [{"derivation_path": ["2c000000", "99000000", "01000000", "00000000", "01000000"], "sign_data": ["37727d44af9801e9723eb325592f4d55cc8d7e3815b1d663d61b7f1af9fc13a7"], "pubkey": "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"}], "fee": 10000000}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if vapor:
        url = f"{config['vapor'][network]['blockmeta']}/tx/hash/{transaction_id}"
        response = requests.get(
            url=url, headers=config["headers"], timeout=timeout
        )
        if response.status_code == 200 and response.json()["code"] == 200:
            return response.json()["data"]["transaction"]
        raise APIError(f"Not found this '{transaction_id}' vapor transaction id.", 500)
    else:
        url = f"{config['bytom'][network]['blockmeta']}/transaction/{transaction_id}"
        response = requests.get(
            url=url, headers=config["headers"], timeout=timeout
        )
        if response.status_code == 200 and response.json()["inputs"] is not None:
            return response.json()
        raise APIError(f"Not found this '{transaction_id}' transaction id.", 500)


def submit_transaction_raw(address: str, transaction_raw: str, signatures: list, network: str = config["network"],
                           vapor: bool = False, timeout: int = config["timeout"]) -> str:
    """
     Submit transaction raw to Bytom blockchain.

    :param address: Bytom address.
    :type address: str
    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param signatures: Bytom signed datas.
    :type signatures: list
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom transaction id/hash.

    >>> from pybytom.rpc import submit_transaction_raw
    >>> submit_transaction_raw("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", transaction_raw, [[...], [...]], "mainent")
    "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
    """
    
    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if vapor:
        if not is_vapor_address(address=address, network=network):
            raise AddressError(f"Invalid '{address}' {network} vapor address.")
        url = f"{config['vapor'][network]['blockcenter']}/merchant/submit-payment"
    else:
        if not is_address(address=address, network=network):
            raise AddressError(f"Invalid '{address}' {network} address.")
        url = f"{config['bytom'][network]['blockcenter']}/merchant/submit-payment"
    data = dict(raw_transaction=transaction_raw, signatures=signatures)
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=config["headers"], timeout=timeout
    )
    if requests.status_codes == 200 and response.json()["code"] != 200:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["data"]["tx_hash"]


def decode_transaction_raw(transaction_raw: str, network: str = config["network"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Get decode transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom decoded transaction raw.

    >>> from pybytom.rpc import decode_transaction_raw
    >>> decode_transaction_raw(transaction_raw, "testnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    url = f"{config[network]['bytom']}/decode-raw-transaction"
    data = dict(raw_transaction=transaction_raw)
    response = requests.post(
        url=url, data=json.dumps(data), headers=config["headers"], timeout=timeout
    )
    if response.status_code == 400:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["data"]
