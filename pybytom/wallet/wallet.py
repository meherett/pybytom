#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from mnemonic import Mnemonic

import hmac
import hashlib

from ..libs.segwit import encode, decode
from ..libs.ed25519 import (
    encodeint, encodepoint, decodeint, decodepoint,
    scalarmultbase, edwards_double, edwards_add
)
from ..signature import sign, verify
from ..utils import get_mnemonic_language, is_mnemonic
from ..rpc import config, account_create, get_balance
from .tools import get_xpublic_key
from .utils import (
    prune_root_scalar, prune_intermediate_scalar,
    get_bytes, bad_seed_checker
)


class Wallet:
    """
    Bytom wallet class.

    :param network: Bytom network, defaults to solonet.
    :type network: str
    :returns:  Wallet -- Bytom wallet instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network="solonet"):

        # Bytom network.
        if not isinstance(network, str):
            raise TypeError("network must be string format")
        if network not in "mainnet/solonet/testnet".split("/"):
            raise ValueError("invalid network option, choose only mainnet, solonet and testnet network")
        self.network = network

        self._entropy, self._mnemonic, self._passphrase, \
            self._language, self._seed = None, None, None, None, None
        self._xprivate_key, self._xpublic_key, self._indexes, \
            self._path, self._guid = None, None, list(), None, None

    def from_entropy(self, entropy, passphrase=None, language="english"):
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

    def from_mnemonic(self, mnemonic, passphrase=None, language=None):
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

    def from_seed(self, seed):
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
        return self

    def from_xprivate_key(self, xprivate_key):
        """
        Initialize Bytom wallet from seed.

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

    def derive_private_key(self, index):
        index = int(index).to_bytes(4, byteorder="little").hex()
        self._indexes.append(index)
        return self

    def from_indexes(self, indexes):
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
        return self

    def from_index(self, index, harden=False):
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
            self.derive_private_key(index + 0x80000000)
        else:
            self.derive_private_key(index)
        return self

    def from_path(self, path):
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
            raise ValueError("bad path, insert like this type of path \"m/0'/0\"! ")

        for index in path.lstrip("m/").split("/"):
            if "'" in index:
                self.derive_private_key(int(index[:-1]) + 0x80000000)
            else:
                self.derive_private_key(int(index))
        return self

    def clean_derivation(self):
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
        return self

    # Getting guid from blockcenter
    def guid(self):
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
            self._guid = account_create(
                xpublic_key=self.xpublic_key(), network=self.network)["guid"]
        return self._guid

    def entropy(self):
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

    def mnemonic(self):
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

    def passphrase(self):
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

    def language(self):
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

    def seed(self):
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

    def xprivate_key(self):
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

    def xpublic_key(self):
        """
        Get Bytom wallet xpublic key.

        :return: str -- Bytom xpublic key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.xpublic_key()
        "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        xprivate_bytes = get_bytes(self.xprivate_key())
        scalar = decodeint(xprivate_bytes[:len(xprivate_bytes) // 2])
        buf = encodepoint(scalarmultbase(scalar))
        xpublic_key = buf + xprivate_bytes[len(xprivate_bytes) // 2:]
        self._xpublic_key = xpublic_key.hex()
        return self._xpublic_key

    def expand_xprivate_key(self):
        """
        Get Bytom wallet expand xprivate key.

        :return: str -- Bytom expand xprivate key.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.expand_xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
        """

        i = hmac.HMAC(b"Expand", get_bytes(self._xprivate_key),
                      digestmod=hashlib.sha512).hexdigest()
        il, ir = i[:64], i[64:]
        bad_seed_checker(ir, True)

        expand_xprivate = self._xprivate_key[:64] + ir
        return expand_xprivate

    def private_key(self):
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

        return self.child_xprivate_key()

    def public_key(self):
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

        return self.child_xpublic_key()[:64]

    def indexes(self):
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

    def path(self):
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

    def child_xprivate_key(self):
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

        xprivate_key = self.xprivate_key()
        for index in range(len(self._indexes)):
            index_bytes = get_bytes(self._indexes[index])
            xpublic_key = get_xpublic_key(xprivate_key=xprivate_key)
            xpublic_bytes = get_bytes(xpublic_key)
            xprivate_bytes = get_bytes(xprivate_key)
            i = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                    b"N" + xpublic_bytes[:32] + index_bytes,
                                    digestmod=hashlib.sha512).digest())
            il, ir = i[:32], i[32:]
            bad_seed_checker(il)

            i = prune_intermediate_scalar(il)[:32] + ir

            carry = 0
            total = 0
            for _i in range(32):
                total = xprivate_bytes[_i] + i[_i] + carry
                i[_i] = total & 0xff
                carry = total >> 8
            if (total >> 8) != 0:
                print("sum does not fit in 256-bit int")
            xprivate_key = i.hex()

        child_xprivate = xprivate_key
        return child_xprivate

    def child_xpublic_key(self):
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

        xpublic_key = self.xpublic_key()
        for index in range(len(self._indexes)):
            index_bytes = get_bytes(self._indexes[index])
            xpublic_bytes = get_bytes(xpublic_key)
            i = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                    b"N" + xpublic_bytes[:32] + index_bytes,
                                    digestmod=hashlib.sha512).digest())

            il, ir = i[:32], i[32:]
            bad_seed_checker(il)

            f = bytes(prune_intermediate_scalar(il))
            scalar = decodeint(f)
            f = scalarmultbase(scalar)

            p = decodepoint(xpublic_bytes[:32])
            p = edwards_add(p, f)
            public_key = encodepoint(p)

            xpublic_bytes = public_key[:32] + ir
            xpublic_key = xpublic_bytes.hex()

        child_xpublic = xpublic_key
        return child_xpublic

    def program(self):
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

        public = self.public_key()
        public_byte = get_bytes(public)

        ripemd160 = hashlib.new("ripemd160")
        ripemd160.update(public_byte)
        public_hash = ripemd160.hexdigest()
        program = "0014" + public_hash
        return program

    def address(self, network=None):
        """
        Get Bytom wallet address.

        :param network: Bytom network, defaults to solonet.
        :type network: str
        :return: str -- Bytom wallet address.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.address()
        "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
        """

        if network is None:
            network = self.network
        if not isinstance(network, str):
            raise TypeError("network must be string format")

        if network not in "mainnet/solonet/testnet".split("/"):
            raise ValueError("invalid network option, choose only mainnet, solonet and testnet network")
        elif network == "mainnet":
            return encode("bm", 0, get_bytes(self.program()[4:]))
        elif network == "solonet":
            return encode("sm", 0, get_bytes(self.program()[4:]))
        elif network == "testnet":
            return encode("tm", 0, get_bytes(self.program()[4:]))

    def balance(self, asset=config["BTM_ASSET"]):
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

    def sign(self, message):
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

    def verify(self, message, signature):
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

    def dumps(self):
        """
        Get Bytom all wallet information's

        :return: dict -- Bytom all wallet information's.

        >>> from pybytom.wallet import Wallet
        >>> wallet = Wallet()
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.dumps()
        {'entropy': None, 'mnemonic': 'indicate warm sock mistake code spot acid ribbon sing over taxi toast', 'language': 'english', 'passphrase': None, 'seed': 'baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49', 'xprivate_key': '205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b', 'xpublic_key': '16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b', 'expand_xprivate_key': '205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e', 'indexes': ['2c000000', '99000000', '01000000', '00000000', '01000000'], 'path': 'm/44/153/1/0/1', 'child_xprivate_key': 'e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141', 'child_xpublic_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141', 'private_key': 'e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141', 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': {'mainnet': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'solonet': 'sm1q9ndylx02syfwd7npehfxz4lddhzqsve2gdsdcs', 'testnet': 'tm1q9ndylx02syfwd7npehfxz4lddhzqsve2d2mgc0'}}
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
            )
        )
