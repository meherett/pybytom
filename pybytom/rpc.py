#!/usr/bin/env python3

from typing import Optional

import requests
import json

from .utils import (
    amount_converter, is_address, is_network
)
from .exceptions import (
    APIError, NetworkError, AddressError, BalanceError
)
from .config import config


def get_balance(address: str, asset: str = config["asset"], network: str = config["network"],
                vapor: bool = config["vapor"], headers: dict = config["headers"],
                timeout: int = config["timeout"]) -> int:
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
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: int -- Bytom asset balance.

    >>> from pybytom.rpc import get_balance
    >>> from pybytom.assets import BTM as ASSET
    >>> get_balance(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", asset=ASSET, network="mainnet", vapor=False)
    71560900
    >>> get_balance(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", asset=ASSET, network="mainnet", vapor=True)
    126990000
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network.",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if vapor:
        if not is_address(address=address, network=network, vapor=True):
            raise AddressError(f"Invalid '{address}' {network} vapor address.")
        url = f"{config['sidechain'][network]['blockmeta']}/address/{address}"
        response = requests.get(url=url, headers=headers, timeout=timeout)
        if response.json() is None or response.json()["data"] is None:
            return 0
        for _asset in response.json()["data"]["address"]:
            if asset == _asset["asset_id"]:
                return int(_asset["balance"])
        return 0
    else:
        if not is_address(address=address, network=network, vapor=False):
            raise AddressError(f"Invalid '{address}' {network} address.")
        url = f"{config['mainchain'][network]['blockmeta']}/address/{address}/asset"
        response = requests.get(url=url, headers=headers, timeout=timeout)
        if response.json() is None:
            return 0
        for _asset in response.json():
            if asset == _asset["asset_id"]:
                return int(_asset["balance"])
        return 0


def get_utxos(program: str, network: str = config["network"], asset: str = config["asset"],
              limit: int = 15, by: str = "amount", order: str = "desc", vapor: bool = config["vapor"],
              headers: dict = config["headers"], timeout: int = config["timeout"]) -> list:
    """
    Get Bytom unspent transaction outputs (UTXO's).

    :param program: Bytom control program.
    :type program: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param asset: Bytom asset id, defaults to BTM asset.
    :type asset: str
    :param limit: Bytom utxo's limit, defaults to 15.
    :type limit: int
    :param by: Sort by, defaults to amount.
    :type by: str
    :param order: Sort order, defaults to desc.
    :type order: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int

    :returns: list -- Bytom unspent transaction outputs (UTXO's).

    >>> from pybytom.rpc import get_utxos
    >>> get_utxos(program="00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", network="mainnet", vapor=False)
    [{'hash': 'e152f88d33c6659ad823d15c5c65b2ed946d207c42430022cba9bb9b9d70a7a4', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 587639800}, {'hash': '88289fa4c7633574931be7ce4102aeb24def0de20e38e7d69a5ddd6efc116b95', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 8160000}, {'hash': 'f71c68f921b434cc2bcd469d26e7927aa6db7500e4cdeef814884f11c10f5de2', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000}, {'hash': 'e46cfecc1f1a26413172ce81c78affb19408e613915642fa5fb04d3b0a4ffa65', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 100}]
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")
    if vapor:
        url = f"{config['sidechain'][network]['blockcenter']}/q/utxos"
    else:
        url = f"{config['mainchain'][network]['blockcenter']}/q/utxos"
    data = dict(filter=dict(script=program, asset=asset), sort=dict(by=by, order=order))
    params = dict(limit=limit)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json["data"]


def account_create(xpublic_key: str, label: str = "1st address", email: Optional[str] = None,
                   network: str = config["network"], headers: dict = config["headers"],
                   timeout: int = config["timeout"]) -> dict:
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
    :param headers: Request headers, default to common headers.
    :type headers: dict
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

    url = f"{config['mainchain'][network]['blockcenter']}/account/create"
    data = dict(pubkey=xpublic_key, label=label, email=email)
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return response.json()["data"]
    raise APIError(response.json()["msg"], response.json()["code"])


def addresses(guid: str, limit: int = 10, network: str = config["network"],
              vapor: bool = config["vapor"], headers: dict = config["headers"],
              timeout: int = config["timeout"]) -> list:
    """
    List all addresses of a GUID.

    :param guid: Bytom blockcenter guid.
    :type guid: str
    :param limit: blockcenter limit default to 10.
    :type limit: int
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: list -- Bytom blockcenter list of addresses.

    >>> from pybytom.rpc import addresses
    >>> addresses(guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", limit=5, network="mainnet", vapor=False)
    [{'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'label': '1st address', 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'balance': '71560900', 'available_balance': '71560900', 'unconfirmed_balance': '0', 'total_received': '4968220000', 'total_sent': '4896659100', 'decimals': 8, 'alias': 'BTM', 'icon': 'https://cdn.blockmeta.com/resources/logo/btm.png', 'name': 'Bytom', 'symbol': 'BTM', 'type': '', 'in_usd': '0.05', 'in_cny': '0.32', 'in_btc': '0.000003'}, {'asset': 'f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf', 'balance': '69999998100', 'available_balance': '69999998100', 'unconfirmed_balance': '0', 'total_received': '100000000200', 'total_sent': '30000002100', 'decimals': 8, 'alias': 'Asset', 'icon': '', 'name': 'f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf', 'symbol': 'Asset', 'type': '', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}]}, {'address': 'bm1qr8nzcxudexul7hpyfvyn69qapwzlfv0ztlqszc', 'label': '', 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '2498900000', 'total_sent': '2498900000', 'decimals': 8, 'alias': 'BTM', 'icon': 'https://cdn.blockmeta.com/resources/logo/btm.png', 'name': 'Bytom', 'symbol': 'BTM', 'type': '', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}]}, {'address': 'bm1q9dw3zz5f6xf74re0re2n4zfqsjd93e5f9l4jxl', 'label': '', 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '48200000', 'total_sent': '48200000', 'decimals': 8, 'alias': 'BTM', 'icon': 'https://cdn.blockmeta.com/resources/logo/btm.png', 'name': 'Bytom', 'symbol': 'BTM', 'type': '', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}]}]
    >>> addresses(guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", limit=5, network="mainnet", vapor=True)
    [{'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag', 'label': '1st address', 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'balance': '126990000', 'available_balance': '126990000', 'unconfirmed_balance': '0', 'total_received': '190000000', 'total_sent': '63010000', 'decimals': 8, 'alias': 'BTM', 'icon': 'https://cdn.bystack.com/bystack/logo/btm_vapor.png', 'name': 'Bytom', 'symbol': 'BTM', 'type': 'BTM', 'in_usd': '0.09', 'in_cny': '0.58', 'in_btc': '0.000005'}, {'asset': 'bda946b3110fa46fd94346ce3f05f0760f1b9de72e238835bc4d19f9d64f1742', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '0', 'total_sent': '0', 'decimals': 8, 'alias': 'BTC', 'icon': 'https://cdn.blockmeta.com/resources/logo/btc_vapor.png', 'name': 'Bitcoin', 'symbol': 'BTC', 'type': 'BTC', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}, {'asset': '47fcd4d7c22d1d38931a6cd7767156babbd5f05bbbb3f7d3900635b56eb1b67e', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '0', 'total_sent': '0', 'decimals': 8, 'alias': 'SUP', 'icon': 'https://cdn.blockmeta.com/resources/logo/vapor/sup.png', 'name': 'SUP', 'symbol': 'SUP', 'type': 'BTM', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}, {'asset': '78de44ffa1bce37b757c9eae8925b5f199dc4621b412ef0f3f46168865284a93', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '0', 'total_sent': '0', 'decimals': 9, 'alias': 'ETH', 'icon': 'https://cdn.bystack.com/bystack/logo/eth_vapor.png', 'name': 'Ethereum', 'symbol': 'ETH', 'type': 'ETH', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}, {'asset': '184e1cc4ee4845023888810a79eed7a42c02c544cf2c61ceac05e176d575bd46', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '0', 'total_sent': '0', 'decimals': 6, 'alias': 'USDT', 'icon': 'https://cdn.bystack.com/bystack/logo/usdt_vapor.png', 'name': 'USDT-ERC20', 'symbol': 'USDT', 'type': 'ETH', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}, {'asset': '25f2069140fa3ff4d6e0dc1d0fcaa11ace01eb721f115f0f1a5a3782db597fb1', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '0', 'total_sent': '0', 'decimals': 6, 'alias': 'DAI', 'icon': '', 'name': 'Dai Stablecoin', 'symbol': 'DAI', 'type': 'ETH', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}, {'asset': 'c4644dd6643475d57ed624f63129ab815f282b61f4bb07646d73423a6e1a1563', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '0', 'total_sent': '0', 'decimals': 6, 'alias': 'USDC', 'icon': '', 'name': 'USDC-ERC20', 'symbol': 'USDC', 'type': 'ETH', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}, {'asset': '011a24f9da7551d4cd9ae0f194aa1d1691e22a173edf7d81aabd9a97ca386252', 'balance': '0', 'available_balance': '0', 'unconfirmed_balance': '0', 'total_received': '0', 'total_sent': '0', 'decimals': 8, 'alias': 'LTC', 'icon': '', 'name': 'Litecoin', 'symbol': 'LTC', 'type': 'LTC', 'in_usd': '0.00', 'in_cny': '0.00', 'in_btc': '0.000000'}], 'votes': []}]
    """

    if vapor:
        url = f"{config['sidechain'][network]['blockcenter']}/account/addresses"
    else:
        url = f"{config['mainchain'][network]['blockcenter']}/account/addresses"
    data, params = dict(guid=guid), dict(limit=limit)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return response.json()["data"]
    raise APIError(response.json()["msg"], response.json()["code"])


def estimate_transaction_fee(address: str, amount: int, asset: str = config["asset"],
                             confirmations: int = config["confirmations"], network: str = config["network"],
                             vapor: bool = config["vapor"], headers: dict = config["headers"],
                             timeout: int = config["timeout"]) -> int:
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
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: str -- Estimated transaction fee.

    >>> from pybytom.rpc import estimate_transaction_fee
    >>> from pybytom.assets import BTM as ASSET
    >>> estimate_transaction_fee(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", asset=ASSET, amount=100_000, confirmations=6, network="mainnet", vapor=False)
    "0.0044900000"
    >>> estimate_transaction_fee(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", asset=ASSET, amount=100_000_000, confirmations=100, network="mainnet", vapor=True)
    "0.0089800000"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if vapor:
        if not is_address(address=address, network=network, vapor=True):
            raise AddressError(f"Invalid Vapor '{address}' {network} address.")
        url = f"{config['sidechain'][network]['mov']}/merchant/estimate-tx-fee"
    else:
        if not is_address(address=address, network=network, vapor=False):
            raise AddressError(f"Invalid '{address}' {network} address.")
        url = f"{config['mainchain'][network]['mov']}/merchant/estimate-tx-fee"

    data = dict(
        asset_amounts={
            asset: str(amount_converter(
                amount=amount, symbol="NEU2BTM"
            ))
        },
        confirmations=confirmations
    )
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return amount_converter(amount=float(response.json()["data"]["fee"]), symbol="BTM2NEU")
    raise APIError(response.json()["msg"], response.json()["code"])


def build_transaction(address: str, transaction: dict, network: str = config["network"],
                      vapor: bool = config["vapor"], headers: dict = config["headers"],
                      timeout: int = config["timeout"]) -> dict:
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
    :param headers: Request headers, default to common headers.
    :type headers: dict
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
        if not is_address(address=address, network=network, vapor=True):
            raise AddressError(f"Invalid '{address}' {network} vapor address.")
        url = f"{config['sidechain'][network]['blockcenter']}/merchant/build-advanced-tx"
    else:
        if not is_address(address=address, network=network, vapor=False):
            raise AddressError(f"Invalid '{address}' {network} address.")
        url = f"{config['mainchain'][network]['blockcenter']}/merchant/build-advanced-tx"
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(transaction), params=params, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 422:
        raise BalanceError(f"There is no any asset balance recorded on this '{address}' address.")
    elif response.status_code == 200 and response.json()["code"] == 515:
        raise BalanceError(f"Insufficient balance, check your balance and try again.")
    elif response.status_code == 200 and response.json()["code"] == 504:
        raise BalanceError(f"Insufficient balance, check your balance and try again.")
    return response.json()["data"][0]


def get_transaction(transaction_id: str, network: str = config["network"], vapor: bool = config["vapor"],
                    headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Get Bytom transaction detail.

    :param transaction_id: Bytom transaction id.
    :type transaction_id: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param headers: Request headers, default to common headers.
    :type headers: dict
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
        url = f"{config['sidechain'][network]['blockmeta']}/tx/hash/{transaction_id}"
        response = requests.get(
            url=url, headers=headers, timeout=timeout
        )
        if response.status_code == 200 and response.json()["code"] == 200:
            return response.json()["data"]["transaction"]
        raise APIError(f"Not found this '{transaction_id}' vapor transaction id.", 500)
    else:
        url = f"{config['mainchain'][network]['blockmeta']}/transaction/{transaction_id}"
        response = requests.get(
            url=url, headers=headers, timeout=timeout
        )
        if response.status_code == 200 and response.json()["inputs"] is not None:
            return response.json()
        raise APIError(f"Not found this '{transaction_id}' transaction id.", 500)


def decode_transaction_raw(transaction_raw: str, network: str = config["network"], vapor: bool = config["vapor"],
                           headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Get decode transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool
    :param headers: Request headers, default to common headers.
    :type headers: dict
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
    if vapor:
        url = f"{config['sidechain'][network]['vapor-core']}/decode-raw-transaction"
    else:
        url = f"{config['mainchain'][network]['bytom-core']}/decode-raw-transaction"
    data = dict(raw_transaction=transaction_raw)
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    if response.status_code == 400:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["data"]


def submit_transaction_raw(address: str, transaction_raw: str, signatures: list,
                           network: str = config["network"], vapor: bool = config["vapor"],
                           headers: dict = config["headers"], timeout: int = config["timeout"]) -> str:
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
    :param headers: Request headers, default to common headers.
    :type headers: dict
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
        if not is_address(address=address, network=network, vapor=True):
            raise AddressError(f"Invalid '{address}' {network} vapor address.")
        url = f"{config['sidechain'][network]['blockcenter']}/merchant/submit-payment"
    else:
        if not is_address(address=address, network=network, vapor=False):
            raise AddressError(f"Invalid '{address}' {network} address.")
        url = f"{config['mainchain'][network]['blockcenter']}/merchant/submit-payment"
    data = dict(raw_transaction=transaction_raw, signatures=signatures)
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    if requests.status_codes == 200 and response.json()["code"] != 200:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["data"]["tx_hash"]
