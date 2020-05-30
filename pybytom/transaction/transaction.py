#!/usr/bin/env python3

from ..rpc import config
from ..wallet import Wallet
from ..wallet.tools import (
    indexes_to_path, get_program, get_address
)
from ..rpc import build_transaction
from ..exceptions import ClientError, NetworkError
from .actions import spend_wallet, control_address


# Byrom transaction
class Transaction:
    """
    Bytom Transaction class.

    :param network: Bytom network, defaults to solonet.
    :type network: str

    :returns: Transaction -- Bytom transaction instance.
    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``testnet``.
    """

    # Initialization transaction
    def __init__(self, network=config["network"]):

        # Checking network
        if not isinstance(network, str):
            raise TypeError("invalid network instance, only takes string type")
        if network not in ["mainnet", "solonet", "testnet"]:
            raise NetworkError("invalid network type",
                               "choose only mainnet, solonet or testnet networks")
        # Bytom network and transaction
        self.network, self.transaction = network, None
        # Bytom fee, signed datas/signatures and confirmations
        self._fee, self._signatures, self._confirmations = \
            config["fee"], [], config["confirmations"]

    # Building Bytom transaction
    def build_transaction(self, **kwargs):
        """
        Build Bytom transaction.

        :param kwargs: Arbitrary keyword arguments. If you do accept ``**kwargs``, make sure
        you link to documentation that describes what keywords are accepted,
        or list the keyword arguments as a definition list:
        ``guid`` (str) Bytom blockcenter guid.
        ``inputs`` (list) Bytom transaction inputs.
        ``outputs`` (list) Bytom transaction outputs.
        ``fee`` (int) Bytom transaction fee, defaults to 10000000.
        ``confirmations`` (int) confirmations: Bytom transaction confirmations, defaults to 1.
        :returns:  Transaction -- Bytom transaction class instance.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction(guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[[...], ...], outputs=[[...], ...], fee=10000000, confirmations=3)
        <pybytom.transaction.transaction.Transaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if {"guid", "inputs", "outputs"} - set(kwargs.keys()):
            raise ClientError("you can't build transaction without 'guid', 'inputs' and 'outputs'",
                              "default fee is 10000000 and confirmations to 1.")
        if not isinstance(kwargs["guid"], str):
            raise TypeError("invalid guid instance, only takes string type")
        if not isinstance(kwargs["inputs"], list):
            raise TypeError("invalid inputs instance, only takes list type")
        if not isinstance(kwargs["outputs"], list):
            raise TypeError("invalid outputs instance, only takes list type")
        if "fee" in kwargs.keys() and not isinstance(kwargs["fee"], int):
            raise TypeError("invalid fee instance, only takes integer type")
        if "confirmations" in kwargs.keys() and not isinstance(kwargs["confirmations"], int):
            raise TypeError("invalid confirmations instance, only takes integer type")

        # Setting fee and confirmations
        self._fee = kwargs["fee"] \
            if "fee" in kwargs.keys() else config["fee"]
        self._confirmations = kwargs["confirmations"] \
            if "confirmations" in kwargs.keys() else config["confirmations"]

        # Transaction config
        transaction = dict(
            guid=kwargs["guid"],
            inputs=kwargs["inputs"],
            outputs=kwargs["outputs"],
            fee=self._fee,
            confirmations=self._confirmations
        )
        # Building transaction
        self.transaction = build_transaction(
            transaction=transaction, network=self.network)
        return self

    # Transaction fee
    def fee(self) -> int:
        """
        Bytom transaction fee.

        :returns: int -- Bytom transaction fee.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.fee()
        10000000
        """

        return self._fee

    # Transaction confirmations
    def confirmations(self) -> int:
        """
        Bytom transaction confirmations.

        :returns: int -- Bytom transaction confirmations.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.confirmations()
        2
        """

        return self._confirmations

    # Transaction hash
    def hash(self) -> str:
        """
        Bytom transaction hash.

        :returns: str -- Bytom transaction hash or transaction id.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["tx"]["hash"]

    # Transaction json
    def json(self):
        """
        Bytom transaction json format.

        :returns: dict -- Bytom transaction json format.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.json()
        {'hash': '2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492', 'status_fail': false, 'size': 379, 'submission_timestamp': 0, 'memo': "", 'inputs': [{'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2450000000, 'type': 'spend'}], 'outputs': [{'utxo_id': '5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc', 'script': '01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0', 'address': 'smart contract', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 1000, 'type': 'control'}, {'utxo_id': 'f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa', 'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2439999000, 'type': 'control'}], 'fee': 10000000, 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': '-10001000'}], 'types': ['ordinary']}
        """
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["tx"]

    # Transaction raw
    def raw(self) -> str:
        """
        Bytom transaction raw.

        :returns: str -- Bytom transaction raw.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["raw_transaction"]

    # Unsigned datas with instructions
    def unsigned_datas(self, detail=False) -> list:
        """
        Bytom unsigned transaction datas with signing instructions.

        :returns: dict -- Bytom transaction json format.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.unsigned_datas()
        [{'datas': ['a7ba7ffd969e4150b36ea9f1f861d53c6f69226a3519023899d27bf1f85be3d9'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}, {'datas': ['0dbf0e408099017711a941d9a9899541afa64eb31a7118815d37e6d603b7c329'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")

        unsigned_datas: list = []
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
        Bytom sign unsigned transaction datas.

        :param xprivate_key: Bytom xprivate key.
        :type xprivate_key: str
        :param account: Bytom derivation account, defaults to 1.
        :type account: int
        :param change: Bytom derivation change, defaults to False.
        :type change: bool
        :param address: Bytom derivation address, defaults to 1.
        :type address: int
        :param path: Bytom derivation path, default to None.
        :type path: str.
        :param indexes: Bytom derivation indexes, default to None.
        :type indexes: list.
        :returns: Transaction -- Bytom transaction instance.

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

        self._signatures.clear()
        wallet = Wallet(network=self.network)
        wallet.from_xprivate_key(xprivate_key=xprivate_key)
        for signing_instruction in self.unsigned_datas(detail=True):
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
            self._signatures.append(signed_data)
            wallet.clean_derivation()
        return self

    # Signed datas/signatures
    def signatures(self) -> list:
        """
        Bytom signed datas/signatures.

        :returns: list -- Bytom sign datas/signatures.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", inputs=[...], outputs=[...])
        >>> transaction.sign(xprivate_key="3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338ff590dedc7ddff447797e1e781190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed")
        >>> transaction.signatures()
        [[...], ...]
        """

        return self._signatures


# Normal transaction
class NormalTransaction(Transaction):
    """
    Bytom Normal transaction class.

    :param network: Bytom network, defaults to solonet.
    :type network: str

    :returns:  NormalTransaction -- Bytom normal transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``testnet``.
    """

    # Init normal transaction
    def __init__(self, network="solonet"):
        # Transaction
        super().__init__(network)

    # Building Bytom normal transaction
    def build_transaction(self, guid: str, recipients: dict, asset: str,
                          fee=config["fee"], confirmations=config["confirmations"]):
        """
        Build Bytom normal transaction.

        :param guid: Bytom sender blockcenter guid.
        :type guid: str
        :param recipients: Recipients Bytom address and amount.
        :type recipients: dict
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :param fee: Bytom transaction fee, defaults to 10000000.
        :type fee: int
        :param confirmations: Bytom transaction confirmations, defaults to 1.
        :type confirmations: int
        :returns: NormalTransaction -- Bytom normal transaction instance.

        >>> from pybytom.transaction import NormalTransaction
        >>> normal_transaction = NormalTransaction(network="mainnet")
        >>> normal_transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", {"bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7": 10_000_000_000}, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <pybytom.transaction.transaction.NormalTransaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if not isinstance(guid, str):
            raise TypeError("invalid guid instance, only takes Bytom string type")
        if not isinstance(recipients, dict):
            raise TypeError("invalid recipients instance, only takes Bytom dictionary type")
        if not isinstance(asset, str):
            raise TypeError("invalid asset instance, only takes string type")
        # Actions
        inputs, outputs = list(), list()
        # Input action
        inputs.append(
            spend_wallet(
                asset=asset,
                amount=sum(recipients.values())
            )
        )
        # Output action
        for address, amount in recipients.items():
            outputs.append(
                control_address(
                    asset=asset,
                    amount=amount,
                    address=address
                )
            )
        # Setting transaction fee and confirmations
        self._fee, self._confirmations = fee, confirmations
        # Transaction
        transaction = dict(
            guid=guid,
            inputs=inputs,
            outputs=outputs,
            fee=self._fee,
            confirmations=self._confirmations
        )
        # Building transaction
        self.transaction = build_transaction(
            transaction=transaction, network=self.network)
        return self


# Advanced transaction
class AdvancedTransaction(Transaction):
    """
    Bytom Advanced transaction class.

    :param network: Bytom network, defaults to solonet.
    :type network: str

    :returns:  AdvancedTransaction -- Bytom advanced transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``testnet``.
    """

    # Init advanced transaction
    def __init__(self, network="solonet"):
        # Transaction
        super().__init__(network)

    # Building Bytom advanced transaction
    def build_transaction(self, guid: str, inputs: list, outputs: list,
                          fee=config["fee"], confirmations=config["confirmations"]):
        """
        Build Bytom advanced transaction.

        :param guid: Bytom blockcenter guid.
        :type guid: str
        :param inputs: Bytom transaction inputs.
        :type inputs: list
        :param outputs: Bytom transaction outputs.
        :type outputs: list
        :param fee: Bytom transaction fee, defaults to 10000000.
        :type fee: int
        :param confirmations: Bytom transaction confirmations, defaults to 1.
        :type confirmations: int
        :returns:  AdvancedTransaction -- Bytom advanced transaction instance.

        >>> from pybytom.transaction import AdvancedTransaction
        >>> advanced_transaction = AdvancedTransaction(network="mainnet")
        >>> advanced_transaction.build_transaction("f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", [[...], ...], outputs=[[...], ...], 10000000, 3)
        <pybytom.transaction.transaction.AdvancedTransaction object at 0x0409DAF0>
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

        # Setting transaction fee and confirmations
        self._fee, self._confirmations = fee, confirmations
        # Transaction
        transaction = dict(
            guid=guid,
            inputs=inputs,
            outputs=outputs,
            fee=self._fee,
            confirmations=self._confirmations
        )
        # Building transaction
        self.transaction = build_transaction(
            transaction=transaction, network=self.network)
        return self
