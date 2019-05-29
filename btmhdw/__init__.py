import sha3
import hmac
import ecdsa
import struct
import codecs
import hashlib
import binascii

import pbkdf2

from .ed25519 import *

from hashlib import sha256
from ecdsa.curves import SECP256k1
from mnemonic.mnemonic import Mnemonic
from two1.bitcoin.utils import rand_bytes
from ecdsa.ecdsa import int_to_string, string_to_int


BTMHDW_HARDEN = 0x80000000


def get_bytes(string):
    if isinstance(string, bytes):
        byte = string
    elif isinstance(string, str):
        byte = bytes.fromhex(string)
    else:
        raise TypeError("Agreement must be either 'bytes' or 'string'!")
    return byte


# s_str must be >= 32 bytes long and gets rewritten in place.
# This is NOT the same pruning as in Ed25519: it additionally clears the third
# highest bit to ensure subkeys do not overflow passphrasethe second highest bit.
def prune_root_scalar(string):
    s = bytearray(get_bytes(string=string))
    s[0] = s[0] & 248
    # clear top 3 bits
    s[31] = s[31] & 31
    # set second highest bit
    s[31] = s[31] | 64
    return s


class BytomHDWallet:

    def __init__(self, xprivate=None, seed=None,
                 depth=None, index=None, fingerprint=None):
        self.xprivate = xprivate
        self.seed = seed
        self.depth = depth
        self.index = index
        self.fingerprint = fingerprint
        self.path = []

    @staticmethod
    def masterKeyFromMnemonic(mnemonic, passphrase=''):

        seed = Mnemonic.to_seed(mnemonic, passphrase)
        return BytomHDWallet.masterKeyFromSeed(seed=seed)

    @staticmethod
    def checkMnemonic(mnemonic, language='english'):
        try:
            Mnemonic(language=language).check(mnemonic)
            return True
        except Exception as exception:
            if exception:
                return False

    @staticmethod
    def masterKeyFromEntropy(passphrase=str(), language='english', strength=128):

        if strength % 32 != 0:
            raise ValueError("strength must be a multiple of 32")
        if strength < 128 or strength > 256:
            raise ValueError("strength should be >= 128 and <= 256")

        entropy = rand_bytes(strength // 8)
        mnemonic = Mnemonic(language=language) \
            .to_mnemonic(entropy)
        seed = Mnemonic.to_seed(mnemonic, passphrase)

        return BytomHDWallet.masterKeyFromSeed(seed=seed), mnemonic

    @staticmethod
    def masterKeyFromSeed(seed):

        I = hmac.HMAC(b'Root', get_bytes(seed), digestmod=hashlib.sha512).hexdigest()
        Il, Ir = I[:64], I[64:]

        parse_Il = str(Il)
        if not parse_Il:
            raise ValueError("Bad seed, resulting in invalid key!")
        # get root xprivate key
        xprivate = prune_root_scalar(Il).hex() + Ir

        return BytomHDWallet(xprivate=xprivate, seed=seed,
                             depth=0, index=0, fingerprint=b'\0\0\0\0')

    def xprivateKey(self):
        return str(self.xprivate)

    def xpublicKey(self, xprivate=None):
        if xprivate:
            xprivate_bytes = get_bytes(xprivate)
            scalar = decodeint(xprivate_bytes[:len(xprivate_bytes) // 2])
            buf = encodepoint(scalarmultbase(scalar))
            xpublic = buf + xprivate_bytes[len(xprivate_bytes) // 2:]
            return xpublic.hex()
        xprivate_bytes = get_bytes(self.xprivate)
        scalar = decodeint(xprivate_bytes[:len(xprivate_bytes) // 2])
        buf = encodepoint(scalarmultbase(scalar))
        xpublic = buf + xprivate_bytes[len(xprivate_bytes) // 2:]
        return xpublic.hex()

    def privateKey(self, xprivate=None):
        if xprivate:
            I = hmac.HMAC(b'Expand', get_bytes(xprivate), digestmod=hashlib.sha512).hexdigest()
            Il, Ir = I[:64], I[64:]
            parse_Ir = str(Ir)
            if not parse_Ir:
                raise ValueError("Bad seed, resulting in invalid key!")
            private = xprivate[:64] + Ir
            return private
        I = hmac.HMAC(b'Expand', get_bytes(self.xprivate), digestmod=hashlib.sha512).hexdigest()
        Il, Ir = I[:64], I[64:]
        parse_Ir = str(Ir)
        if not parse_Ir:
            raise ValueError("Bad seed, resulting in invalid key!")
        private = self.xprivate[:64] + Ir
        return private

    def publicKey(self, xpublic=None):
        if xpublic:
            return xpublic[:64]
        return self.xpublicKey()[:64]

    def derivePrivateKey(self, index):
        index = int(index).to_bytes(4, byteorder='little').hex()
        self.path.append(index)

        return BytomHDWallet()

    def fromIndex(self, index):
        if not str(index)[0:2] != "m/":
            raise ValueError("Bad Index, Please use fromPath not fromIndex for this %s" % index)
        if not isinstance(index, int):
            raise ValueError("Bad Index, Please import only integer number!")
        return self.derivePrivateKey(index)

    def fromPath(self, path):
        if str(path)[0:2] != 'm/':
            raise ValueError("Bad path, please insert like this type of path \"m/0'/0\"! ")

        for index in path.lstrip('m/').split('/'):
            if "'" in index:
                self.derivePrivateKey(int(index[:-1]) + BTMHDW_HARDEN)
            else:
                self.derivePrivateKey(int(index))
        return BytomHDWallet()

    def getPath(self):
        return self.path


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
        _, mnemonic = BytomHDWallet.masterKeyFromEntropy(passphrase=passphrase,
                                                         language=language,
                                                         strength=strength)
        return mnemonic

    @staticmethod
    def checkMnemonic(mnemonic, language='english'):
        boolean = BytomHDWallet.checkMnemonic(mnemonic, language)
        return boolean
