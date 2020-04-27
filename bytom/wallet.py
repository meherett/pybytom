#!/usr/bin/env python3

from binascii import hexlify, unhexlify

import hmac

from .libs.segwit import encode
from .signature import sign, verify
from .utils.utils import *

# Constant values
HARDEN = 0x80000000
# Derivation Path
PATH = "m/44/153/1/0/1"
# Derivation Indexes
INDEXES = [
    "2c000000",  # 44
    "99000000",  # 153
    "01000000",  # 1 Account
    "00000000",  # 0 Change
    "01000000"  # 1 Address
]


def get_xpublic_key(xprivate_key):
    """
    Get bytom xpublic key from xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :return: str -- bytom xpublic key.

    >>> from bytom.wallet import get_xpublic_key
    >>> get_xpublic_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    """

    # Checking parameters
    if not isinstance(xprivate_key, str):
        raise TypeError("xprivate key must be string format")

    xprivate_bytes = get_bytes(xprivate_key)
    scalar = decodeint(xprivate_bytes[:len(xprivate_bytes) // 2])
    buf = encodepoint(scalarmultbase(scalar))
    xpublic_key = buf + xprivate_bytes[len(xprivate_bytes) // 2:]
    return xpublic_key.hex()


class Wallet:
    """
    Bytom wallet class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns:  Wallet -- bytom wallet instance.

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

        self._entropy, self._mnemonic, self._seed = None, None, None
        self._xprivate_key = None
        self._xpublic_key = None
        self._indexes = list()
        self._path = None

    def from_entropy(self, entropy, passphrase=None, language="english"):
        """
        Get bytom wallet from entropy.

        :param entropy: Entropy hex string.
        :type entropy: str.
        :param passphrase: Secret password/passphrase, default to None.
        :type passphrase: str.
        :param language: Mnemonic language, default to english.
        :type language: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("8d7454bb99e8e68de6adfc5519cbee64")
        <bytom.wallet.Wallet object at 0x040DA268>
        """

        if passphrase is None:
            passphrase = str()

        # Checking parameters
        if not isinstance(entropy, str):
            raise TypeError("entropy must be string format")
        if not isinstance(passphrase, str):
            raise TypeError("passphrase must be string format")
        if not isinstance(language, str):
            raise TypeError("passphrase must be string format")
        if language not in "english/french/italian/spanish/chinese_simplified/chinese_traditional/korean".split("/"):
            raise ValueError("invalid language option, choose only english, french, italian, spanish, "
                             "chinese_simplified, chinese_traditional & korean language")
        if not isinstance(language, int):
            raise TypeError("passphrase must be integer format")

        self._entropy = entropy.encode()
        self._mnemonic = Mnemonic(language=language) \
            .to_mnemonic(data=self._entropy)
        self._seed = Mnemonic.to_seed(
            mnemonic=self._mnemonic, passphrase=passphrase)
        self.from_seed(seed=hexlify(self._seed).decode())
        return self

    def from_mnemonic(self, mnemonic, passphrase=None):
        """
        Get bytom wallet from mnemonic.

        :param mnemonic: 12 words mnemonic.
        :type mnemonic: str.
        :param passphrase: Secret password/passphrase, default to None.
        :type passphrase: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("8d7454bb99e8e68de6adfc5519cbee64")
        <bytom.wallet.Wallet object at 0x040DA268>
        """

        if passphrase is None:
            passphrase = str()

        # Checking parameters
        if not isinstance(mnemonic, str):
            raise TypeError("mnemonic must be string format")
        if not isinstance(passphrase, str):
            raise TypeError("passphrase must be string format")

        self._mnemonic = mnemonic
        self._seed = Mnemonic.to_seed(
            mnemonic=self._mnemonic, passphrase=passphrase)
        self.from_seed(seed=hexlify(self._seed).decode())
        return self

    def from_seed(self, seed):
        """
        Get bytom wallet from seed.

        :param seed: Mnemonic seed hex string.
        :type seed: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")
        <bytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(seed, str):
            raise TypeError("seed must be string format")

        self._seed = unhexlify(seed.encode())
        i = hmac.HMAC(b"Root", get_bytes(self._seed),
                      digestmod=hashlib.sha512).hexdigest()
        il, ir = i[:64], i[64:]

        parse_il = str(il)
        if not parse_il:
            raise ValueError("bad seed, resulting in invalid key!")
        # get root xprivate_key key
        self._xprivate_key = prune_root_scalar(il).hex() + ir
        return self

    def from_xprivate_key(self, xprivate_key):
        """
        Get bytom wallet from seed.

        :param xprivate_key: Bytom xprivate key.
        :type xprivate_key: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        <bytom.wallet.Wallet object at 0x040DA268>
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
        Drive bytom wallet from indexes.

        :param indexes: Bytom derivation indexes.
        :type indexes: list.
        :returns:  Wallet -- bytom wallet instance.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        <bytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(indexes, list):
            raise TypeError("indexes must be list format")

        self._indexes = indexes
        return self

    def from_index(self, index):
        """
        Drive bytom wallet from index.

        :param index: Bytom derivation index.
        :type index: int.
        :returns:  Wallet -- bytom wallet instance.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> wallet.from_index(44)
        <bytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(index, int):
            raise TypeError("index must be integer format")

        self.derive_private_key(index)
        return self

    def from_path(self, path):
        """
        Drive bytom wallet from path.

        :param path: Bytom derivation path.
        :type path: int.
        :returns:  Wallet -- bytom wallet instance.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> wallet.from_path("m/44/153/1/0/1")
        <bytom.wallet.Wallet object at 0x040DA268>
        """

        # Checking parameters
        if not isinstance(path, str):
            raise TypeError("index must be string format")
        if str(path)[0:2] != "m/":
            raise ValueError("bad path, insert like this type of path \"m/0'/0\"! ")

        for index in path.lstrip("m/").split("/"):
            if "'" in index:
                self.derive_private_key(int(index[:-1]) + HARDEN)
            else:
                self.derive_private_key(int(index))
        return self

    def entropy(self):
        """
        Get bytom wallet entropy.

        :return: str -- entropy.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="8d7454bb99e8e68de6adfc5519cbee64", language="korean")
        >>> wallet.entropy()
        "8d7454bb99e8e68de6adfc5519cbee64"
        """

        return hexlify(self._entropy).decode() if self._entropy else None

    def mnemonic(self):
        """
        Get bytom wallet mnemonic.

        :return: str -- 12 word mnemonic.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="8d7454bb99e8e68de6adfc5519cbee64", language="italian")
        >>> wallet.mnemonic()
        "occasione pizzico coltivato cremoso odorare epilogo patacca salone fonia sfuso vispo selettivo"
        """

        return str(self._mnemonic)

    def seed(self):
        """
        Get bytom wallet seed.

        :return: str -- Mnemonic seed.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.seed()
        "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"
        """

        return hexlify(self._seed).decode() if self._seed else None

    def xprivate_key(self):
        """
        Get bytom wallet xprivate key.

        :return: str -- bytom xprivate key.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        return str(self._xprivate_key)

    def xpublic_key(self):
        """
        Get bytom wallet xpublic key.

        :return: str -- bytom xpublic key.

        >>> from bytom.wallet import Wallet
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
        Get bytom wallet expand xprivate key.

        :return: str -- bytom expand xprivate key.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.expand_xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
        """

        i = hmac.HMAC(b"Expand", get_bytes(self._xprivate_key),
                      digestmod=hashlib.sha512).hexdigest()
        il, ir = i[:64], i[64:]
        parse_ir = str(ir)
        if not parse_ir:
            raise ValueError("bad seed, resulting in invalid key!")
        expand_xprivate = self._xprivate_key[:64] + ir
        return expand_xprivate

    def private_key(self):
        """
        Get bytom wallet private key.

        :return: str -- bytom private key.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.private_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self.child_xprivate_key()

    def public_key(self):
        """
        Get bytom wallet public key.

        :return: str -- bytom public key.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.public_key()
        "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
        """

        return self.child_xpublic_key()[:64]

    def indexes(self):
        """
        Get bytom wallet derivation indexes.

        :return: list -- bytom derivation indexes.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.indexes()
        ["2c000000", "99000000", "01000000", "00000000", "01000000"]
        """

        return self._indexes

    def path(self):
        """
        Get bytom wallet derivation path.

        :return: str -- bytom derivation path.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
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
        return path

    def child_xprivate_key(self):
        """
        Get bytom get child xprivate key.

        :return: str -- bytom child xprivate key.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
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

            parse_il = int.from_bytes(il, "big")
            if parse_il == 0:
                raise ValueError("bad seed, resulting in invalid key!")

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
        Get bytom get child xpublic key.

        :return: str -- bytom child xpublic key.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
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

            parse_il = int.from_bytes(il, "big")
            if parse_il == 0:
                raise ValueError("bad seed, resulting in invalid key!")

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
        Get bytom wallet control program.

        :return: str -- bytom control program.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
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
        Get bytom wallet address.

        :return: str -- bytom address.

        >>> from bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
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

    def sign(self, message, private=None):
        if private is None:
            return sign(self.private_key(), message)
        return sign(private, message)

    def verify(self, message, signature, public=None):
        if public is None:
            return verify(self.public_key(), message, signature)
        return verify(public, message, signature)


def get_expand_xprivate_key(xprivate_key):
    """
    Get bytom expand xprivate key from xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :return: str -- bytom expand xprivate key.

    >>> from bytom.wallet import get_expand_xprivate_key
    >>> get_expand_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
    """

    i = hmac.HMAC(b"Expand", get_bytes(xprivate_key),
                  digestmod=hashlib.sha512).hexdigest()
    il, ir = i[:64], i[64:]
    parse_ir = str(ir)
    if not parse_ir:
        raise ValueError("bad seed, resulting in invalid key!")
    expand_xprivate_key = xprivate_key[:64] + ir
    return expand_xprivate_key


def indexes_to_path(indexes):
    """
    Get bytom derivation path.

    :param indexes: Bytom derivation indexes.
    :type indexes: list.
    :return: str -- bytom derivation path.

    >>> from bytom.wallet import indexes_to_path
    >>> indexes_to_path(["2c000000", "99000000", "01000000", "00000000", "01000000"])
    "m/44/153/1/0/1"
    """

    # Checking parameters
    if not isinstance(indexes, list):
        raise TypeError("indexes must be list format")

    path = "m/"
    for i, index in enumerate(indexes, 1):
        number = int.from_bytes(bytes.fromhex(index), byteorder="little")
        if i == len(indexes):
            path = path + str(number)
        else:
            path = path + str(number) + "/"
    return path


def path_to_indexes(path):
    """
    Get bytom derivation path.

    :param path: Bytom derivation path.
    :type path: str.
    :return: list -- bytom derivation indexes.

    >>> from bytom.wallet import path_to_indexes
    >>> path_to_indexes("m/44/153/1/0/1")
    ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    """

    # Checking parameters
    if not isinstance(path, str):
        raise TypeError("index must be string format")
    if str(path)[0:2] != "m/":
        raise ValueError("bad path, insert like this type of path \"m/0'/0\"! ")

    indexes = list()
    for index in path.lstrip("m/").split("/"):
        if "'" in index:
            index = int(int(index[:-1]) + HARDEN).to_bytes(4, byteorder="little").hex()
            indexes.append(index)
        else:
            index = int(int(index)).to_bytes(4, byteorder="little").hex()
            indexes.append(index)
    return indexes


def get_child_xprivate_key(xprivate_key, indexes=None, path=None):
    """
    Get bytom get child xprivate key.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- bytom child xprivate key.

    >>> from bytom.wallet import get_child_xprivate_key
    >>> get_child_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "00ca8555655d336c4c0d11464a1d401f0cc7c29fdc52bf52f5fc8e0ced32ee51b9c62d145693b366cde5ba74a06962bfa9f6b1e810a3e15eadf791247333547e"
    """

    if indexes is None and path is None:
        indexes = INDEXES
    elif indexes is not None:
        if not isinstance(indexes, list):
            raise TypeError("indexes must be list format")
    elif path is not None:
        if not isinstance(path, str):
            raise TypeError("indexes must be string format")
        indexes = path_to_indexes(path=path)

    for index in range(len(indexes)):
        index_bytes = get_bytes(indexes[index])
        xpublic_key = get_xpublic_key(xprivate_key=xprivate_key)
        xpublic_bytes = get_bytes(xpublic_key)
        xprivate_bytes = get_bytes(xprivate_key)
        i = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                b"N" + xpublic_bytes[:32] + index_bytes,
                                digestmod=hashlib.sha512).digest())
        il, ir = i[:32], i[32:]

        parse_il = int.from_bytes(il, "big")
        if parse_il == 0:
            raise ValueError("bad seed, resulting in invalid key!")

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


def get_child_xpublic_key(xpublic_key, indexes=None, path=None):
    """
    Get bytom get child xpublic key.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- bytom child xpublic key.

    >>> from bytom.wallet import get_child_xpublic_key
    >>> get_child_xpublic_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
    """

    if indexes is None and path is None:
        indexes = INDEXES
    elif indexes is not None:
        if not isinstance(indexes, list):
            raise TypeError("indexes must be list format")
    elif path is not None:
        if not isinstance(path, str):
            raise TypeError("indexes must be string format")
        indexes = path_to_indexes(path=path)

    for index in range(len(indexes)):
        index_bytes = get_bytes(indexes[index])
        xpublic_bytes = get_bytes(xpublic_key)
        i = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                b"N" + xpublic_bytes[:32] + index_bytes,
                                digestmod=hashlib.sha512).digest())

        il, ir = i[:32], i[32:]

        parse_il = int.from_bytes(il, "big")
        if parse_il == 0:
            raise ValueError("bad seed, resulting in invalid key!")

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


def get_private_key(xprivate_key, indexes=None, path=None):
    """
    Get bytom private key from xprivate key. This is also the same with get_child_xprivate_key function.

    :param xprivate_key: Bytom xprivate key.
    :type xprivate_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- bytom private key.

    >>> from bytom.wallet import get_private_key
    >>> get_private_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
    """

    return get_child_xprivate_key(
        xprivate_key=xprivate_key, indexes=indexes, path=path)


def get_public_key(xpublic_key=None, indexes=None, path=None):
    """
    Get bytom private key from xpublic key.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str.
    :param indexes: Bytom derivation indexes, default to ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    :type indexes: list.
    :param path: Bytom derivation path, default to None.
    :type path: str.
    :return: str -- bytom public key.

    >>> from bytom.wallet import get_public_key
    >>> get_public_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
    """

    return get_child_xpublic_key(
            xpublic_key=xpublic_key, indexes=indexes, path=path)[:64]


def get_program(public_key):
    """
    Get bytom control program from public key.

    :param public_key: Bytom public key.
    :type public_key: str.
    :return: str -- bytom control program.

    >>> from bytom.wallet import get_program
    >>> get_program("91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2")
    "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"
    """

    # Checking parameters
    if not isinstance(public_key, str):
        raise TypeError("public key must be string format")

    public_byte = get_bytes(public_key)
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(public_byte)
    public_hash = ripemd160.hexdigest()
    control_program = "0014" + public_hash
    return control_program


def get_address(program, network="solonet"):
    """
    Get bytom address from program.

    :param program: Bytom control program.
    :type program: str.
    :param network: Bytom network, default to solonet.
    :type network: str.
    :return: str -- bytom address.

    >>> from bytom.wallet import get_address
    >>> get_address("00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "mainnet")
    "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
    """

    if not isinstance(program, str):
        raise TypeError("program must be string format")
    if not isinstance(network, str):
        raise TypeError("network must be string format")

    if network not in "mainnet/solonet/testnet".split("/"):
        raise ValueError("invalid network option, choose only mainnet, solonet and testnet network")
    elif network == "mainnet":
        return encode("bm", 0, get_bytes(program[4:]))
    elif network == "solonet":
        return encode("sm", 0, get_bytes(program[4:]))
    elif network == "testnet":
        return encode("tm", 0, get_bytes(program[4:]))
