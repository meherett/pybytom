import sha3
import hmac
import ecdsa
import struct
import codecs
import hashlib
import binascii

import pbkdf2

from hashlib import sha256
from ecdsa.curves import SECP256k1
from mnemonic.mnemonic import Mnemonic
from two1.bitcoin.utils import rand_bytes
from ecdsa.ecdsa import int_to_string, string_to_int


class BytomHDWallet:

    def __init__(self, seed=None):
        self.seed = seed

    @staticmethod
    def fromMnemonic(mnemonic, passphrase=''):

        seed = Mnemonic.to_seed(mnemonic, passphrase)
        return BytomHDWallet.fromSeed(seed=seed)

    @staticmethod
    def checkMnemonic(mnemonic, language='english'):
        try:
            Mnemonic(language=language).check(mnemonic)
            return True
        except Exception as exception:
            if exception:
                return False

    @staticmethod
    def fromEntropy(passphrase=str(), language='english', strength=128):

        if strength % 32 != 0:
            raise ValueError("strength must be a multiple of 32")
        if strength < 128 or strength > 256:
            raise ValueError("strength should be >= 128 and <= 256")

        entropy = rand_bytes(strength // 8)
        mnemonic = Mnemonic(language=language) \
            .to_mnemonic(entropy)
        seed = Mnemonic.to_seed(mnemonic, passphrase)

        return BytomHDWallet.fromSeed(seed=seed), mnemonic

    @staticmethod
    def fromSeed(seed):
        salt_str = "mnemonic"
        seed = pbkdf2.PBKDF2(seed, salt_str,
                             iterations=2048,
                             digestmodule=hashlib.sha512,
                             macmodule=hmac).hexread(64)
        return BytomHDWallet(seed=seed)


class BTMHDW:

    def __init__(self):
        self.hdwallet = dict(
            mnmonic=str(),
            seed=str(),
            root_xprv=str(),
            xpub=str(),
            xprv=str()
        )

    @staticmethod
    def generateMnemonic(passphrase=str(), language='english', strength=128):
        _, mnemonic = BytomHDWallet.fromEntropy(passphrase=passphrase,
                                                language=language,
                                                strength=strength)
        return mnemonic

    @staticmethod
    def checkMnemonic(mnemonic, language='english'):
        boolean = BytomHDWallet.checkMnemonic(mnemonic, language)
        return boolean
