#!/usr/bin/env python3

from .. import configuration as config
from ..wallet import Wallet
from ..wallet.tools import (
    indexes_to_path, get_program, get_address
)
from ..rpc import build_transaction  # , decode_tx_raw
from .tools import spend_wallet_action, control_address_action


class Transaction:
    """
    Bytom Transaction class.

    :param network: bytom network, defaults to solonet.
    :type network: str

    :returns:  Transaction -- bytom transaction instance.
    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``testnet``.
    """

    # Initialization transaction
    def __init__(self, network="solonet"):
        # Transaction
        self.transaction = None
        # Bytom network
        self.network: str = network
        # Bytom fee
        self.fee: int = config["fee"]
        # Signed datas
        self.signatures: list = []

    # Building bytom transaction
    def build_transaction(self, guid: str, inputs: list, outputs: list, fee=config["fee"],
                          confirmations=config["confirmations"], *args, **kwargs):
        """
        Build bytom transaction.

        :param guid: bytom blockcenter guid.
        :type guid: str
        :param inputs: bytom transaction inputs.
        :type inputs: list
        :param outputs: bytom transaction outputs.
        :type outputs: list
        :param fee: bytom transaction fee, defaults to 10000000.
        :type fee: int
        :param confirmations: bytom transaction confirmations, defaults to 1.
        :type confirmations: int
        :returns:  Transaction -- bytom transaction instance.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...], fee=10000000, confirmations=3)
        <pybytom.transaction.transaction.Transaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if not isinstance(guid, str):
            raise TypeError("invalid guid instance, only takes string type")
        if not isinstance(inputs, list):
            raise TypeError("invalid inputs instance, only takes list type")
        if not isinstance(outputs, list):
            raise TypeError("invalid outputs instance, only takes list type")
        if not isinstance(fee, int):
            raise TypeError("invalid fee instance, only takes integer type")
        if not isinstance(confirmations, int):
            raise TypeError("invalid confirmations instance, only takes integer type")

        self.fee = fee
        # Transaction
        transaction = dict(
            guid=guid,
            inputs=inputs,
            outputs=outputs,
            fee=fee,
            confirmations=confirmations
        )
        # Building transaction
        self.transaction = build_transaction(
            transaction=transaction, network=self.network)
        return self

    # Transaction hash
    def hash(self) -> str:
        """
        Get bytom transaction hash.

        :returns: str -- bytom transaction hash or transaction id.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["tx"]["hash"]

    # Transaction raw
    def raw(self) -> str:
        """
        Get bytom transaction raw.

        :returns: str -- bytom transaction raw.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["raw_transaction"]

    # Signing Instructions
    def signing_instructions(self, detail=False) -> list:
        unsigned_datas = list()
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        for signing_instruction in self.transaction["signing_instructions"]:
            unsigned_data = dict(datas=signing_instruction["sign_data"])
            if "pubkey" in signing_instruction and signing_instruction["pubkey"]:
                unsigned_data.setdefault("public_key", signing_instruction["pubkey"])
                if detail:
                    program = get_program(public_key=signing_instruction["pubkey"])
                    address = get_address(program=program, network=self.network)
                    unsigned_data.setdefault("program", program)
                    unsigned_data.setdefault("address", address)
                else:
                    unsigned_data.setdefault("network", self.network)
            else:
                if detail:
                    unsigned_data.setdefault("public_key", None)
                    unsigned_data.setdefault("program", None)
                    unsigned_data.setdefault("address", None)
                else:
                    unsigned_data.setdefault("network", self.network)
            if "derivation_path" in signing_instruction and signing_instruction["derivation_path"]:
                path = indexes_to_path(indexes=signing_instruction["derivation_path"])
                if detail:
                    unsigned_data.setdefault("indexes", signing_instruction["derivation_path"])
                unsigned_data.setdefault("path", path)
            else:
                if detail:
                    unsigned_data.setdefault("indexes", None)
                unsigned_data.setdefault("path", None)
            # Append unsigned datas
            unsigned_datas.append(unsigned_data)
        # Returning
        return unsigned_datas

    # Signing transaction using xprivate keys
    def sign(self, xprivate_key: str, account=1,
             change=False, address=1, path=None, indexes=None):
        """
        Sign bytom transaction.

        :param xprivate_key: bytom xprivate key.
        :type xprivate_key: str
        :param account: bytom derivation account, defaults to 1.
        :type account: int
        :param change: bytom derivation change, defaults to False.
        :type change: bool
        :param address: bytom derivation address, defaults to 1.
        :type address: int
        :param path: Bytom derivation path, default to None.
        :type path: str.
        :param indexes: Bytom derivation indexes, default to None.
        :type indexes: list.
        :returns: Transaction -- bytom transaction instance.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.sign(xprivate_key)
        <pybytom.transaction.transaction.Transaction object at 0x0409DAF0>
        """

        if not isinstance(xprivate_key, str):
            raise TypeError("invalid xprivate_key instance, only takes string type")
        if not isinstance(account, int):
            raise TypeError("invalid account instance, only takes integer type")
        if not isinstance(change, bool):
            raise TypeError("invalid change instance, only takes boolean type")
        if not isinstance(address, int):
            raise TypeError("invalid address instance, only takes integer type")
        if path and not isinstance(path, str):
            raise TypeError("invalid path instance, only takes string type")
        if indexes and not isinstance(indexes, list):
            raise TypeError("invalid indexes instance, only takes list type")

        wallet = Wallet(network=self.network)
        wallet.from_xprivate_key(xprivate_key=xprivate_key)
        for signing_instruction in self.signing_instructions(detail=True):
            signed_data: list = []
            unsigned_datas = signing_instruction["datas"]
            if signing_instruction["path"]:
                wallet.from_path(signing_instruction["path"])
            elif not path and not indexes:
                wallet.from_path(f"m/44/153/{account}/{1 if change else 0}/{address}")
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
            wallet.clean_derivation()
        return self


# Normal transaction
class NormalTransaction(Transaction):
    """
    Bytom Normal transaction class.

    :param network: bytom network, defaults to solonet.
    :type network: str

    :returns:  NormalTransaction -- bytom normal transaction instance.
    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``testnet``.
    """

    # Initialization transaction
    def __init__(self, network="solonet"):
        # Transaction
        super().__init__(network)

    # Building bytom transaction
    def build_transaction(self, guid: str, recipients: dict, asset: str, amount: str, *args, **kwargs):
        """
        Build bytom fund transaction.

        :param wallet: bytom sender wallet.
        :type wallet: bytom.wallet.Wallet
        :param htlc: bytom hash time lock contract (HTLC).
        :type htlc: bytom.htlc.HTLC
        :param amount: bytom amount to fund.
        :type amount: int
        :param asset: bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: FundTransaction -- bytom fund transaction instance.

        >>> from pybytom.transaction import NormalTransaction
        >>> normal_transaction = NormalTransaction(network="mainnet")
        >>> normal_transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        <pybytom.transaction.transaction.NormalTransaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bytom Wallet class")
        if not isinstance(htlc, HTLC):
            raise TypeError("invalid htlc instance, only takes bytom HTLC class")
        if not isinstance(amount, int):
            raise TypeError("invalid amount instance, only takes integer type")
        if not isinstance(asset, str):
            raise TypeError("invalid asset instance, only takes string type")
        # Setting wallet GUID
        self.guid = wallet.guid()
        # Actions
        inputs, outputs = list(), list()
        # Input action
        inputs.append(
            spend_wallet_action(
                asset=asset,
                amount=amount
            )
        )
        # Output action
        outputs.append(
            control_address_action(
                asset=asset,
                amount=amount,
                address=address
            )
        )
        # Transaction
        tx = dict(
            guid=self.guid,
            inputs=inputs,
            outputs=outputs,
            fee=config["fee"], confirmations=config["confirmations"]
        )
        # Building transaction
        self.transaction = build_transaction(tx=tx, network=self.network)
        return self

    # Transaction json
    def json(self) -> any:
        """
        Get bytom normal transaction json format.

        :returns: dict -- bytom normal transaction json format.

        >>> from pybytom.transaction import NormalTransaction
        >>> normal_transaction = NormalTransaction(network="mainnet")
        >>> normal_transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> normal_transaction.json()
        {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        # return decode_tx_raw(tx_raw=self.transaction["raw_transaction"])
        return self
