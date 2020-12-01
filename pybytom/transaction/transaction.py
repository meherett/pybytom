#!/usr/bin/env python3

from typing import (Optional, List)

from ..wallet import Wallet
from ..wallet.tools import (
    indexes_to_path, get_program, get_address
)
from ..rpc import build_transaction
from ..exceptions import (
    ClientError, NetworkError, AddressError
)
from ..utils import (
    amount_converter, is_network, is_address
)
from ..config import config
from .actions import (
    spend_wallet, control_address
)


class Transaction:
    """
    Bytom Transaction class.

    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :returns: Transaction -- Bytom transaction instance.
    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], vapor: bool = config["vapor"]):
        if not is_network(network=network):
            raise NetworkError(f"Invalid '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        self._network: str = network
        self._vapor: bool = vapor

        self._transaction: Optional[dict] = None
        self._fee: int = config["fee"]
        self._signatures: List[List[str]] = []
        self._confirmations: int = config["confirmations"]
        self._forbid_chain_tx: bool = config["forbid_chain_tx"]

    def build_transaction(self, **kwargs):
        """
        Build Bytom transaction.

        :param kwargs: Arbitrary keyword arguments. If you do accept ``**kwargs``, make sure
        you link to documentation that describes what keywords are accepted,
        or list the keyword arguments as a definition list:
        ``address`` (str) Bytom address.
        ``inputs`` (list) Bytom transaction inputs.
        ``outputs`` (list) Bytom transaction outputs.
        ``fee`` (int) Bytom transaction fee, defaults to 10000000.
        ``confirmations`` (int) confirmations: Bytom transaction confirmations, defaults to 1.
        ``forbid_chain_tx`` (bool) forbid_chain_tx: Whether to prohibit chain transactions, defaults to False.

        :returns: Transaction -- Bytom transaction class instance.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[[...], ...], outputs=[[...], ...], fee=10000000, confirmations=3)
        <pybytom.transaction.transaction.Transaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if {"address", "inputs", "outputs"} - set(kwargs.keys()):
            raise ClientError("You can't build transaction without 'address', 'inputs' and 'outputs'",
                              "default fee is 10000000 and confirmations to 1.")
        if self._vapor and not is_address(address=kwargs["address"], network=self._network, vapor=True):
            raise AddressError(f"Invalid '{kwargs['address']}' {self._network} vapor address.")
        if not self._vapor and not is_address(address=kwargs["address"], network=self._network, vapor=False):
            raise AddressError(f"Invalid '{kwargs['address']}' {self._network} address.")
        if not isinstance(kwargs["inputs"], list):
            raise TypeError("Invalid inputs instance, only takes list type.")
        if not isinstance(kwargs["outputs"], list):
            raise TypeError("Invalid outputs instance, only takes list type.")
        if "fee" in kwargs.keys() and not isinstance(kwargs["fee"], int):
            raise TypeError("Invalid fee instance, only takes integer type.")
        if "confirmations" in kwargs.keys() and not isinstance(kwargs["confirmations"], int):
            raise TypeError("Invalid confirmations instance, only takes integer type.")
        if "forbid_chain_tx" in kwargs.keys() and not isinstance(kwargs["confirmations"], int):
            raise TypeError("Invalid forbid_chain_tx instance, only takes boolean type.")

        # Setting fee, confirmations & forbid_chain_tx
        self._fee = kwargs["fee"] if "fee" in kwargs.keys() else config["fee"]
        self._confirmations = kwargs["confirmations"] \
            if "confirmations" in kwargs.keys() else config["confirmations"]
        self._forbid_chain_tx = kwargs["forbid_chain_tx"] \
            if "forbid_chain_tx" in kwargs.keys() else config["forbid_chain_tx"]

        # Building transaction
        self._transaction = build_transaction(
            address=kwargs["address"],
            transaction=dict(
                fee=str(amount_converter(self._fee, "NEU2BTM")),
                inputs=kwargs["inputs"],
                outputs=kwargs["outputs"],
                confirmations=self._confirmations,
                forbid_chain_tx=self._forbid_chain_tx
            ),
            network=self._network,
            vapor=self._vapor
        )
        return self

    def fee(self) -> int:
        """
        Bytom transaction fee.

        :returns: int -- Bytom transaction fee.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.fee()
        10000000
        """

        return self._fee

    def confirmations(self) -> int:
        """
        Bytom transaction confirmations.

        :returns: int -- Bytom transaction confirmations.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.confirmations()
        2
        """

        return self._confirmations

    def hash(self) -> str:
        """
        Bytom transaction hash.

        :returns: str -- Bytom transaction hash or transaction id.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["tx"]["hash"]

    def json(self):
        """
        Bytom transaction json format.

        :returns: dict -- Bytom transaction json format.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.json()
        {'hash': '2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492', 'status_fail': false, 'size': 379, 'submission_timestamp': 0, 'memo': "", 'inputs': [{'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2450000000, 'type': 'spend'}], 'outputs': [{'utxo_id': '5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc', 'script': '01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0', 'address': 'smart contract', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 1000, 'type': 'control'}, {'utxo_id': 'f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa', 'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2439999000, 'type': 'control'}], 'fee': 10000000, 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': '-10001000'}], 'types': ['ordinary']}
        """
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["tx"]

    def raw(self) -> str:
        """
        Bytom transaction raw.

        :returns: str -- Bytom transaction raw.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["raw_transaction"]

    def unsigned_datas(self, detail: bool = False) -> List[dict]:
        """
        Bytom unsigned transaction datas with signing instructions.

        :returns: dict -- Bytom transaction json format.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.unsigned_datas()
        [{'datas': ['a7ba7ffd969e4150b36ea9f1f861d53c6f69226a3519023899d27bf1f85be3d9'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}, {'datas': ['0dbf0e408099017711a941d9a9899541afa64eb31a7118815d37e6d603b7c329'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]
        """

        # Checking transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        unsigned_datas: List[dict] = []
        for signing_instruction in self._transaction["signing_instructions"]:
            unsigned_data = dict(datas=signing_instruction["sign_data"])
            if "pubkey" in signing_instruction and signing_instruction["pubkey"]:
                unsigned_data.setdefault("public_key", signing_instruction["pubkey"])
                if detail:
                    program = get_program(public_key=signing_instruction["pubkey"])
                    address = get_address(program=program, network=self._network)
                    unsigned_data.setdefault("program", program)
                    unsigned_data.setdefault("address", address)
                else:
                    unsigned_data.setdefault("network", self._network)
            else:
                if detail:
                    unsigned_data.setdefault("public_key", None)
                    unsigned_data.setdefault("program", None)
                    unsigned_data.setdefault("address", None)
                else:
                    unsigned_data.setdefault("network", self._network)
            if "derivation_path" in signing_instruction and signing_instruction["derivation_path"]:
                path = indexes_to_path(indexes=signing_instruction["derivation_path"])
                if detail:
                    unsigned_data.setdefault("indexes", signing_instruction["derivation_path"])
                unsigned_data.setdefault("path", path)
            else:
                if detail:
                    unsigned_data.setdefault("indexes", None)
                unsigned_data.setdefault("path", None)
            unsigned_datas.append(unsigned_data)
        return unsigned_datas

    def sign(self, private_key: Optional[str] = None, xprivate_key: Optional[str] = None,
             account: int = 1, change: bool = False, address: int = 1,
             path: str = None, indexes: List[str] = None) -> "Transaction":
        """
        Bytom sign unsigned transaction datas.

        :param private_key: Bytom private key, default to None.
        :type private_key: str
        :param xprivate_key: Bytom xprivate key, default to None.
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
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.sign(xprivate_key)
        <pybytom.transaction.transaction.Transaction object at 0x0409DAF0>
        """

        self._signatures = []
        wallet = Wallet(network=self._network)
        if private_key and not xprivate_key:
            wallet.from_private_key(private_key=private_key)
        elif not private_key and xprivate_key:
            wallet.from_xprivate_key(xprivate_key=xprivate_key)
        for signing_instruction in self.unsigned_datas(detail=True):
            signed_data: list = []
            unsigned_datas = signing_instruction["datas"]
            if not private_key and signing_instruction["path"]:
                wallet.from_path(signing_instruction["path"])
            elif not private_key and not path and not indexes:
                wallet.from_path(f"m/44/153/{account}/{1 if change else 0}/{address}")
            elif not private_key and path:
                wallet.from_path(path)
            elif not private_key and indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()
        return self

    def signatures(self) -> List[List[str]]:
        """
        Bytom signed datas/signatures.

        :returns: list -- Bytom sign datas/signatures.

        >>> from pybytom.transaction import Transaction
        >>> transaction = Transaction(network="mainnet")
        >>> transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", inputs=[...], outputs=[...])
        >>> transaction.sign(xprivate_key="3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338ff590dedc7ddff447797e1e781190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed")
        >>> transaction.signatures()
        [[...], ...]
        """

        return self._signatures


class NormalTransaction(Transaction):
    """
    Bytom Normal transaction class.

    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :returns:  NormalTransaction -- Bytom normal transaction instance.
    """

    def __init__(self, network: str = config["network"], vapor: bool = config["vapor"]):
        super().__init__(network=network, vapor=vapor)

    def build_transaction(self, address: str, recipients: dict, asset: str = config["asset"],
                          fee: int = config["fee"], confirmations: int = config["confirmations"],
                          forbid_chain_tx: bool = config["forbid_chain_tx"]) -> "NormalTransaction":
        """
        Build Bytom normal transaction.

        :param address: Bytom sender blockcenter guid.
        :type address: str
        :param recipients: Recipients Bytom address and amount.
        :type recipients: dict
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :param fee: Bytom transaction fee, defaults to 10000000.
        :type fee: int
        :param confirmations: Bytom transaction confirmations, defaults to 1.
        :type confirmations: int
        :param forbid_chain_tx: Whether to prohibit chain transactions, defaults to False.
        :type forbid_chain_tx: int

        :returns: NormalTransaction -- Bytom normal transaction instance.

        >>> from pybytom.transaction import NormalTransaction
        >>> normal_transaction = NormalTransaction(network="mainnet")
        >>> normal_transaction.build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", recipients={"bm1qtwtdhf6jmxhfhutjacmgxyv6levnkuhad67wqh": 10_000_000_000}, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <pybytom.transaction.transaction.NormalTransaction object at 0x0409DAF0>
        """

        if self._vapor and not is_address(address=address, network=self._network, vapor=True):
            raise AddressError(f"Invalid '{address}' {self._network} vapor address.")
        elif not self._vapor and not is_address(address=address, network=self._network, vapor=False):
            raise AddressError(f"Invalid '{address}' {self._network} address.")

        # Setting transaction fee and confirmations
        self._fee, self._confirmations, self._forbid_chain_tx = (
            fee, confirmations, forbid_chain_tx
        )

        inputs, outputs = [], []
        # Inputs action
        inputs.append(
            spend_wallet(
                asset=asset, amount=sum(recipients.values())
            )
        )
        # Outputs action
        for _address, _amount in recipients.items():
            outputs.append(
                control_address(
                    asset=asset, address=_address, amount=_amount,
                    vapor=self._vapor, symbol="NEU"
                )
            )

        # Building transaction
        self._transaction = build_transaction(
            address=address,
            transaction=dict(
                fee=str(amount_converter(self._fee, "NEU2BTM")),
                inputs=inputs,
                outputs=outputs,
                confirmations=self._confirmations,
                forbid_chain_tx=self._forbid_chain_tx
            ),
            network=self._network,
            vapor=self._vapor
        )
        return self


class AdvancedTransaction(Transaction):
    """
    Bytom Advanced transaction class.

    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param vapor: Bytom sidechain vapor, defaults to False.
    :type vapor: bool

    :returns: AdvancedTransaction -- Bytom advanced transaction instance.
    """

    def __init__(self, network: str = config["network"], vapor: bool = config["vapor"]):
        super().__init__(network=network, vapor=vapor)

    def build_transaction(self, address: str, inputs: list, outputs: list,
                          fee: int = config["fee"], confirmations: int = config["confirmations"],
                          forbid_chain_tx: int = config["forbid_chain_tx"]) -> "AdvancedTransaction":
        """
        Build Bytom advanced transaction.

        :param address: Bytom address.
        :type address: str
        :param inputs: Bytom transaction inputs.
        :type inputs: list
        :param outputs: Bytom transaction outputs.
        :type outputs: list
        :param fee: Bytom transaction fee, defaults to 10000000.
        :type fee: int
        :param confirmations: Bytom transaction confirmations, defaults to 1.
        :type confirmations: int
        :param forbid_chain_tx: Whether to prohibit chain transactions, defaults to False.
        :type forbid_chain_tx: int

        :returns:  AdvancedTransaction -- Bytom advanced transaction instance.

        >>> from pybytom.transaction import AdvancedTransaction
        >>> advanced_transaction = AdvancedTransaction(network="mainnet")
        >>> advanced_transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", [[...],...], [[...],...], 10000000, 3)
        <pybytom.transaction.transaction.AdvancedTransaction object at 0x0409DAF0>
        """

        if self._vapor and not is_address(address=address, network=self._network, vapor=True):
            raise AddressError(f"Invalid '{address}' {self._network} vapor address.")
        elif not self._vapor and not is_address(address=address, network=self._network, vapor=False):
            raise AddressError(f"Invalid '{address}' {self._network} address.")

        # Setting transaction fee and confirmations
        self._fee, self._confirmations, self._forbid_chain_tx = (
            fee, confirmations, forbid_chain_tx
        )

        # Building transaction
        self._transaction = build_transaction(
            address=address,
            transaction=dict(
                fee=str(amount_converter(self._fee, "NEU2BTM")),
                inputs=inputs,
                outputs=outputs,
                confirmations=self._confirmations,
                forbid_chain_tx=self._forbid_chain_tx
            ),
            network=self._network,
            vapor=self._vapor
        )
        return self
