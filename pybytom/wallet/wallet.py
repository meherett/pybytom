#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from typing import TypeVar, Optional, List
from mnemonic import Mnemonic

import hmac
import hashlib

from ..config import config
from ..signature import sign, verify
from ..utils import get_mnemonic_language, is_mnemonic, is_network
from ..exceptions import NetworkError, DerivationError, ClientError
from ..rpc import account_create, get_balance

from .tools import (
    get_xpublic_key, get_address,
    get_vapor_address, get_program,
    get_child_xpublic_key, get_child_xprivate_key,
    get_private_key, get_public_key,
    get_expand_xprivate_key
)
from .utils import (
    prune_root_scalar, prune_intermediate_scalar,
    get_bytes, bad_seed_checker
)

# Bytom config
config = config()
# Wallet class
_Wallet = TypeVar("_Wallet", bound="Wallet")


class Wallet:
    """
    Bytom wallet class.

    :param network: Bytom network, defaults to solonet.
    :type network: str
    :returns:  Wallet -- Bytom wallet instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"]):

        # Bytom network.
        if not is_network(network=network):
            raise NetworkError(f"Invalid '{network}' network/type",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        self.network = network

        self._entropy, self._mnemonic, self._passphrase, self._language = (
            None, None, None, None
        )
        self._seed, self._guid, self._xprivate_key, self._private_key = (
            None, None, None, None
        )
        self._indexes, self._path = (
            list(), None
        )

    def from_entropy(self, entropy: str,
                     passphrase: Optional[str] = None, language: str = "english") -> _Wallet:
        """
        Initialize Bytom wallet from entropy.

        :param entropy: Entropy hex string.
        :type entropy: str.
        :param passphrase: Secret password/passphrase, default to None.
        :type passphrase: str.
        :param language: Mnemonic language, default to english.
        :type language: str.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("8d7454bb99e8e68de6adfc5519cbee64")
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        if passphrase is None:
            passphrase = str()

        # Checking parameters
        if not isinstance(entropy, str):
            raise TypeError("entropy must be string format")
        if not isinstance(passphrase, str):
            raise TypeError("passphrase must be string format")
        if not isinstance(language, str):
            raise TypeError("language must be string format")
        if language not in "english/french/italian/spanish/" \
                           "chinese_simplified/chinese_traditional/japanese/korean".split("/"):
            raise ValueError("invalid language option, choose only english, french, italian, spanish, "
                             "chinese_simplified, chinese_traditional, japanese & korean language")

        self._entropy = unhexlify(entropy.encode())
        self._passphrase, self._language = passphrase, language
        self._mnemonic = Mnemonic(language=self._language) \
            .to_mnemonic(data=self._entropy)
        self._seed = Mnemonic.to_seed(
            mnemonic=self._mnemonic, passphrase=self._passphrase)
        self.from_seed(seed=hexlify(self._seed).decode())
        return self

    def from_mnemonic(self, mnemonic: str,
                      passphrase: Optional[str] = None, language: Optional[str] = None) -> _Wallet:
        """
        Initialize Bytom wallet from mnemonic.

        :param mnemonic: 12 words mnemonic.
        :type mnemonic: str.
        :param passphrase: Secret password/passphrase, default to None.
        :type passphrase: str.
        :param language: Mnemonic language, default to None.
        :type language: str.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("舒 使 系 款 株 擾 麼 鄉 狗 振 誤 謀")
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        if passphrase is None:
            passphrase = str()

        # Checking parameters
        if not isinstance(mnemonic, str):
            raise TypeError("mnemonic must be string format")
        if not isinstance(passphrase, str):
            raise TypeError("passphrase must be string format")
        if language and language not in "english/french/italian/spanish/chinese_simplified" \
                                        "/chinese_traditional/japanese/korean".split("/"):
            raise ValueError("invalid language option, choose only english, french, italian, spanish, "
                             "chinese_simplified, chinese_traditional, japanese & korean language")
        if not is_mnemonic(mnemonic=mnemonic, language=language):
            raise ValueError("invalid 12 word mnemonic.")

        self._mnemonic = mnemonic
        self._passphrase, self._language = \
            passphrase, get_mnemonic_language(mnemonic=self._mnemonic)
        self._seed = Mnemonic.to_seed(
            mnemonic=self._mnemonic, passphrase=self._passphrase)
        self.from_seed(seed=hexlify(self._seed).decode())
        return self

    def from_seed(self, seed: str) -> _Wallet:
        """
        Initialize Bytom wallet from seed.

        :param seed: Mnemonic seed hex string.
        :type seed: str.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(seed, str):
            raise TypeError("seed must be string format")

        self._seed = unhexlify(seed.encode())
        i = hmac.HMAC(b"Root", get_bytes(self._seed),
                      digestmod=hashlib.sha512).hexdigest()
        il, ir = i[:64], i[64:]
        bad_seed_checker(il, True)

        # get root xprivate_key key
        self._xprivate_key = prune_root_scalar(il).hex() + ir
        self._private_key = get_private_key(str(self._xprivate_key), self._indexes)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> _Wallet:
        """
        Initialize Bytom wallet from xprivate key.

        :param xprivate_key: Bytom xprivate key.
        :type xprivate_key: str.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(xprivate_key, str):
            raise TypeError("xprivate key must be string format")

        self._xprivate_key = xprivate_key
        return self

    def from_private_key(self, private_key: str) -> _Wallet:
        """
        Initialize Bytom wallet from private key.

        :param private_key: Bytom private key.
        :type private_key: str.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key("e0d42c3a1d9e1c54c09d5da9fd582afb1d053d3c033c3a07fedf2a709ce3f4477b4b52132f610150767edac6e1c2934d34780a9340a56a9dea58e070e44b70f1")
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(private_key, str):
            raise TypeError("private key must be string format")

        self._private_key = private_key
        return self

    def derivation(self, index: Optional[int] = None) -> _Wallet:
        if index is not None:
            index = int(index).to_bytes(4, byteorder="little").hex()
            self._indexes.append(index)
        if not self._xprivate_key:
            raise DerivationError("You can't drive private key", "xprivate key is also None.")
        self._private_key = get_private_key(str(self._xprivate_key), self._indexes)
        return self

    def from_indexes(self, indexes: List[str]) -> _Wallet:
        """
        Drive Bytom wallet from indexes.

        :param indexes: Bytom derivation indexes.
        :type indexes: list.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(indexes, list):
            raise TypeError("indexes must be list format")

        self._indexes = indexes
        self.derivation()
        return self

    def from_index(self, index: int, harden: bool = False) -> _Wallet:
        """
        Drive Bytom wallet from index.

        :param index: Bytom derivation index.
        :type index: int.
        :param harden: BIP 32 key harden, default to False.
        :type harden: bool.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="8d7454bb99e8e68de6adfc5519cbee64", language="japaneses")
        >>> wallet.from_index(44)
        >>> wallet.from_index(153)
        >>> wallet.from_index(1)  # Account
        >>> wallet.from_index(0)  # Change False(0)/True(1)
        >>> wallet.from_index(1)  # Address
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(index, int):
            raise TypeError("index must be integer format")

        if harden:
            self.derivation(index + 0x80000000)
        else:
            self.derivation(index)
        return self

    def from_path(self, path: str) -> _Wallet:
        """
        Drive Bytom wallet from path.

        :param path: Bytom derivation path.
        :type path: str.
        :returns:  Wallet -- Bytom wallet instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic(mnemonic="舒 使 系 款 株 擾 麼 鄉 狗 振 誤 謀", passphrase="Hello Meheret!")
        >>> wallet.from_path("m/44/153/1/0/1")
        <pybytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(path, str):
            raise TypeError("path must be string format")
        if str(path)[0:2] != "m/":
            raise DerivationError("Bad path", "insert like this type of path \"m/0'/0\"! ")

        for index in path.lstrip("m/").split("/"):
            if "'" in index:
                self.derivation(int(index[:-1]) + 0x80000000)
            else:
                self.derivation(int(index))
        return self

    def clean_derivation(self) -> _Wallet:
        """
        Clean derivation indexes/path.

        :returns:  Wallet -- Bytom wallet instance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic(mnemonic="舒 使 系 款 株 擾 麼 鄉 狗 振 誤 謀", passphrase="Hello Meheret!")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.indexes()
        ["2c000000", "99000000", "01000000", "00000000", "01000000"]
        >>> wallet.path()
        "m/44/153/1/0/1"
        >>> wallet.clean_derivation()
        >>> wallet.indexes()
        []
        >>> wallet.path()
        None
        """
        self._indexes = list()
        self.derivation()
        return self

    # Getting guid from blockcenter
    def guid(self) -> Optional[str]:
        """
        Get Bytom wallet blockcenter guid.

        :return: str -- Bytom blockcenter guid.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.guid()
        "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b"
        """

        if self._guid is None:
            if not self.xpublic_key():
                raise ClientError("You can't get GUID", "xpublic key is None.")
            self._guid = account_create(
                xpublic_key=self.xpublic_key(), network=self.network)["guid"]
        return self._guid

    def entropy(self) -> Optional[str]:
        """
        Get wallet entropy.

        :return: str -- Entropy hex string.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="8d7454bb99e8e68de6adfc5519cbee64", language="korean")
        >>> wallet.entropy()
        "8d7454bb99e8e68de6adfc5519cbee64"
        """

        return hexlify(self._entropy).decode() if self._entropy else None

    def mnemonic(self) -> Optional[str]:
        """
        Get wallet mnemonic.

        :return: str -- 12 word mnemonic.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="8d7454bb99e8e68de6adfc5519cbee64", language="italian")
        >>> wallet.mnemonic()
        "occasione pizzico coltivato cremoso odorare epilogo patacca salone fonia sfuso vispo selettivo"
        """

        return str(self._mnemonic) if self._mnemonic else None

    def passphrase(self) -> Optional[str]:
        """
        Get wallet secret password/passphrase.

        :return: str -- Secret password/passphrase.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="8d7454bb99e8e68de6adfc5519cbee64", passphrase="Hello Meheret!", language="italian")
        >>> wallet.passphrase()
        "Hello Meheret!"
        """

        return str(self._passphrase) if self._passphrase else None

    def language(self) -> Optional[str]:
        """
        Get wallet mnemonic language.

        :return: str -- Mnemonic language.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="8d7454bb99e8e68de6adfc5519cbee64", language="italian")
        >>> wallet.language()
        "italian"
        """

        return str(self._language) if self._language else None

    def seed(self) -> Optional[str]:
        """
        Get wallet mnemonic seed.

        :return: str -- Mnemonic seed.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.seed()
        "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"
        """

        return hexlify(self._seed).decode() if self._seed else None

    def xprivate_key(self) -> Optional[str]:
        """
        Get Bytom wallet xprivate key.

        :return: str -- Bytom xprivate key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        return str(self._xprivate_key)

    def xpublic_key(self) -> Optional[str]:
        """
        Get Bytom wallet xpublic key.

        :return: str -- Bytom xpublic key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.xpublic_key()
        "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        return get_xpublic_key(xprivate_key=self.xprivate_key()) if self._xprivate_key else None

    def expand_xprivate_key(self)-> Optional[str]:
        """
        Get Bytom wallet expand xprivate key.

        :return: str -- Bytom expand xprivate key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.expand_xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
        """

        return get_expand_xprivate_key(xprivate_key=self.xprivate_key()) if self._xprivate_key else None

    def private_key(self) -> str:
        """
        Get Bytom wallet private key.

        :return: str -- Bytom private key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.private_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return str(self._private_key)

    def public_key(self) -> str:
        """
        Get Bytom wallet public key.

        :return: str -- Bytom public key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.public_key()
        "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
        """

        return get_public_key(xpublic_key=self.xpublic_key(), indexes=self.indexes()) \
            if self._xprivate_key else get_xpublic_key(xprivate_key=self.private_key())[:64]

    def indexes(self) -> Optional[list]:
        """
        Get Bytom wallet derivation indexes.

        :return: list -- Bytom derivation indexes.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.indexes()
        ["2c000000", "99000000", "01000000", "00000000", "01000000"]
        """

        return self._indexes

    def path(self) -> Optional[str]:
        """
        Get Bytom wallet derivation path.

        :return: str -- Bytom derivation path.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.path()
        "m/44/153/1/0/1"
        """

        path = "m/"
        for i, index in enumerate(self._indexes, 1):
            number = int.from_bytes(bytes.fromhex(index), byteorder="little")
            if i == len(self._indexes):
                path = path + str(number)
            else:
                path = path + str(number) + "/"
        return path if not path == "m/" else None

    def child_xprivate_key(self) -> Optional[str]:
        """
        Get Bytom get child xprivate key.

        :return: str -- Bytom child xprivate key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.child_xprivate_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return get_child_xprivate_key(xprivate_key=self.xprivate_key(),
                                      indexes=self.indexes()) if self._xprivate_key else None

    def child_xpublic_key(self) -> Optional[str]:
        """
        Get Bytom get child xpublic key.

        :return: str -- Bytom child xpublic key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.child_xpublic_key()
        "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return get_child_xpublic_key(xpublic_key=self.xpublic_key(),
                                     indexes=self.indexes()) if self._xprivate_key else None

    def program(self) -> str:
        """
        Get Bytom wallet control program.

        :return: str -- Bytom wallet control program.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.program()
        "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"
        """

        return get_program(public_key=self.public_key())

    def address(self, network: Optional[str] = None) -> str:
        """
        Get Bytom wallet address.

        :param network: Bytom network, defaults to solonet.
        :type network: str
        :return: str -- Bytom wallet address.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.address(network="mainnet")
        "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
        """

        if network is None:
            network = self.network
        if not isinstance(network, str):
            raise TypeError("network must be string format")

        return get_address(program=self.program(), network=network)

    def vapor_address(self, network: Optional[str] = None) -> str:
        """
        Get Bytom wallet vapor address.

        :param network: Bytom network, defaults to solonet.
        :type network: str
        :return: str -- Bytom wallet vapor address.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.vapor_address(network="mainnet")
        "vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag"
        """

        if network is None:
            network = self.network
        if not isinstance(network, str):
            raise TypeError("network must be string format")

        return get_vapor_address(program=self.program(), network=network)

    def balance(self, asset: str = config["asset"]) -> int:
        """
        Get Bytom wallet balance.

        :param asset: Bytom asset, defaults to BTM asset.
        :type asset: str
        :return: int -- Bytom balance.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.balance()
        2450000000
        """

        return get_balance(address=self.address(), asset=asset, network=self.network)

    def sign(self, message: str) -> str:
        """
        Sign message data by private key.

        :param message: Message data.
        :type message: str.
        :return: str -- Signed message data (signature).

        >>> from pybytom.wallet import Wallet
        >>> message = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.sign(message=message)
        "f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a1524470549992c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05"
        """

        if not isinstance(message, str):
            raise TypeError("message must be string format")

        return sign(self.private_key(), message)

    def verify(self, message: str, signature: str) -> bool:
        """
        Verify signature by public key.

        :param message: Message data.
        :type message: str.
        :param signature: Signed message data.
        :type signature: str.
        :return: bool -- Verified signature (True/False).

        >>> from pybytom.wallet import Wallet
        >>> message = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"
        >>> signature = "f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a1524470549992c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05"
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.verify(message=message, signature=signature)
        True
        """

        if not isinstance(message, str):
            raise TypeError("message must be string format")
        if not isinstance(signature, str):
            raise TypeError("signature must be string format")

        return verify(self.public_key(), message, signature)

    def dumps(self, guid: bool = False) -> dict:
        """
        Get Bytom all wallet information's

        :param guid: Get GUID, default to False.
        :type guid: bool.
        :return: dict -- Bytom all wallet information's.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet()
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.dumps()
        {'entropy': None, 'mnemonic': 'indicate warm sock mistake code spot acid ribbon sing over taxi toast', 'language': 'english', 'passphrase': None, 'seed': 'baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49', 'xprivate_key': '205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b', 'xpublic_key': '16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b', 'expand_xprivate_key': '205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e', 'guid': None, 'indexes': ['2c000000', '99000000', '01000000', '00000000', '01000000'], 'path': 'm/44/153/1/0/1', 'child_xprivate_key': 'e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141', 'child_xpublic_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141', 'private_key': 'e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141', 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': {'mainnet': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'solonet': 'sm1q9ndylx02syfwd7npehfxz4lddhzqsve2gdsdcs', 'testnet': 'tm1q9ndylx02syfwd7npehfxz4lddhzqsve2d2mgc0'}}
        """

        return dict(
            entropy=self.entropy(),
            mnemonic=self.mnemonic(),
            language=self.language(),
            passphrase=self.passphrase(),
            seed=self.seed(),
            xprivate_key=self.xprivate_key(),
            xpublic_key=self.xpublic_key(),
            expand_xprivate_key=self.expand_xprivate_key(),
            guid=self.guid() if guid else None,
            indexes=self.indexes(),
            path=self.path(),
            child_xprivate_key=self.child_xprivate_key(),
            child_xpublic_key=self.child_xpublic_key(),
            private_key=self.private_key(),
            public_key=self.public_key(),
            program=self.program(),
            address=dict(
                mainnet=self.address(network="mainnet"),
                solonet=self.address(network="solonet"),
                testnet=self.address(network="testnet")
            ),
            vapor_address=dict(
                mainnet=self.vapor_address(network="mainnet"),
                solonet=self.vapor_address(network="solonet"),
                testnet=self.vapor_address(network="testnet")
            )
        )
