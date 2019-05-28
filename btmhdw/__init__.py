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

    def __init__(self, secret=None, seed=None, chain=None, depth=None, index=None, fingerprint=None):
        self.secret = secret
        self.seed = seed
        self.chain = chain
        self.depth = depth
        self.index = index
        self.fingerprint = fingerprint

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
        if parse_Il:
            raise ValueError("Bad seed, resulting in invalid key!")
        # get root xprivate key
        secret = prune_root_scalar(Il).hex() + Ir

        return BytomHDWallet(secret=secret, chain=Ir,
                             seed=seed, depth=0, index=0, fingerprint=b'\0\0\0\0')

    def privateKey(self):
        return str(self.secret)

    def chainCode(self):
        return str(self.chain)


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
