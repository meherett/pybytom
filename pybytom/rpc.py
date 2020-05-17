#!/usr/bin/env python3

import requests
import json

from .exceptions import APIError

# Request headers
headers = dict()
# headers.setdefault("Content-Type", "application/json")

# Bytom configuration
config = {
    "mainnet": {
        "bytom": "http://localhost:9888",
        "blockmeta": "https://blockmeta.com/api/v3",
        "blockcenter": "https://bcapi.bystack.com/api/v2/btm"
    },
    "solonet": {
        "bytom": "http://localhost:9888",
        "blockmeta": None,
        "blockcenter": None
    },
    "testnet": {
        "bytom": "http://localhost:9888",
        "blockmeta": None,
        "blockcenter": None
    },
    "network": "solonet",  # mainnet, solonet & testnet
    "timeout": 60,
    "BTM_ASSET": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "fee": 10_000_000,  # 0.1 BTM
    "confirmations": 1
}


# Get balance by address
def get_balance(address, asset=config["BTM_ASSET"], network=config["network"], limit=1, page=1, timeout=config["timeout"]):
    """
    Get Bytom balance.

    :param address: Bytom address.
    :type address: str
    :param asset: Bytom asset, default to BTM asset.
    :type asset: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param limit: Bytom limit, defaults to 1.
    :type limit: str
    :param page: Bytom network, defaults to 1.
    :type page: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: int -- Bytom balance.

    >>> from pybytom.rpc import get_balance
    >>> get_balance(bytom_address, "mainnet")
    25800000
    """

    parameter = dict(limit=limit, page=page)
    url = f"{config[network]['blockmeta']}/address/{address}/asset"
    response = requests.get(url=url, params=parameter,
                            headers=headers, timeout=timeout)
    if response.status_code == 204:
        return 0
    for _asset in response.json():
        if asset == _asset["asset_id"]:
            return _asset["balance"]
    return None


# Create account in blockcenter
def account_create(xpublic_key, label="1st address", email=None,
                   network=config["network"], timeout=config["timeout"]):
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

    url = str(config[network]["blockcenter"]) + "/account/create"
    data = dict(pubkey=xpublic_key, label=label, email=email)
    response = requests.post(url=url, data=json.dumps(data),
                             headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["code"], response.json()["msg"])
    return response.json()["result"]["data"]


# List addresses from blockcenter
def list_address(guid, limit=10, network=config["network"], timeout=config["timeout"]):
    """
    List address from blockcenter.

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

    url = str(config[network]["blockcenter"]) + "/account/list-address"
    response = requests.post(url=url, data=json.dumps(dict(guid=guid)),
                             params=dict(limit=limit), headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["code"], response.json()["msg"])
    return response.json()["result"]["data"]


# Build transaction in blockcenter
def build_transaction(transaction, network=config["network"], timeout=config["timeout"]):
    """
    Build Bytom transaction in blockcenter.

    :param transaction: Bytom transaction.
    :type transaction: dict
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- Bytom built transaction.

    >>> from pybytom.rpc import build_transaction
    >>> build_transaction(transaction, "mainnet")
    {"transaction": {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utransactiono_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utransactiono_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}, "raw_transaction": "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", "signing_instructions": [{"derivation_path": ["2c000000", "99000000", "01000000", "00000000", "01000000"], "sign_data": ["37727d44af9801e9723eb325592f4d55cc8d7e3815b1d663d61b7f1af9fc13a7"], "pubkey": "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"}], "fee": 10000000}
    """

    url = str(config[network]["blockcenter"]) + "/merchant/build-transaction"
    response = requests.post(url=url, data=json.dumps(transaction),
                             headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["code"], response.json()["msg"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["code"], response.json()["msg"])
    return response.json()["result"]["data"]


# Get transaction from blockcenter
def get_transaction(transaction_id, network=config["network"], timeout=config["timeout"]):
    """
    Get Bytom transaction detail.

    :param transaction_id: Bytom transaction id.
    :type transaction_id: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- Bytom built transaction.

    >>> from pybytom.rpc import get_transaction
    >>> get_transaction(transaction_id, "mainnet")
    {"transaction": {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utransactiono_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utransactiono_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}, "raw_transaction": "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", "signing_instructions": [{"derivation_path": ["2c000000", "99000000", "01000000", "00000000", "01000000"], "sign_data": ["37727d44af9801e9723eb325592f4d55cc8d7e3815b1d663d61b7f1af9fc13a7"], "pubkey": "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"}], "fee": 10000000}
    """

    url = str(config[network]["blockcenter"]) + "/merchant/get-transaction"
    response = requests.post(url=url, data=json.dumps(dict(tx_id=transaction_id)),
                             headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["result"]["data"]


# Submit transaction raw from blockcenter
def submit_transaction_raw(guid, transaction_raw, signatures,
                           network, memo="mock", timeout=config["timeout"]):
    """
     Submit transaction raw to Bytom blockchain.

    :param guid: Bytom blockcenter id.
    :type guid: str
    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param signatures: Bytom signed datas.
    :type signatures: list
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param memo: memo, defaults to mock.
    :type memo: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- Bytom transaction id, fee, type and date.

    >>> from pybytom.rpc import submit_transaction_raw
    >>> submit_transaction_raw("guid", transaction_raw, [[...], [...]], "mainent")
    {...}
    """
    if not isinstance(signatures, list):
        raise TypeError("signatures must be list format")
    url = str(config[network]["blockcenter"]) + "/merchant/submit-payment"
    data = dict(guid=guid, raw_transaction=transaction_raw, signatures=signatures, memo=memo)
    response = requests.post(url=url, data=json.dumps(data),
                             headers=headers, timeout=timeout)
    if response.json()["code"] != 200:
        raise APIError(response.json()["code"], response.json()["msg"])
    return response.json()["result"]["data"]["transaction_hash"]


# Decode transaction raw
def decode_transaction_raw(transaction_raw, network=config["network"], timeout=config["timeout"]):
    """
    Get decoded transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- Bytom decoded transaction raw.

    >>> from pybytom.rpc import decode_transaction_raw
    >>> decode_transaction_raw(transaction_raw, "testnet")
    {...}
    """

    url = str(config[network]["bytom"]) + "/decode-raw-transaction"
    response = requests.post(url=url, data=json.dumps(dict(raw_transaction=transaction_raw)),
                             headers=headers, timeout=timeout)
    if response.status_code == 400:
        raise APIError(response.json()["code"], response.json()["msg"])
    return response.json()["data"]
