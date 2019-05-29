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


def prune_intermediate_scalar(f):
    f = bytearray(f)
    # clear bottom 3 bits
    f[0] = f[0] & 248
    # clear 7 high bits
    f[29] = f[29] & 1
    # clear 8 bits
    f[30] = 0
    # clear 8 bits
    f[31] = 0
    return f


class BytomHDWallet:

    def __init__(self, xprivate=None, seed=None,
                 depth=None, index=None, fingerprint=None):
        self.xprivate = xprivate
        self.seed = seed
        self.depth = depth
        self.index = index
        self.fingerprint = fingerprint
        self.indexes = []

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
        self.indexes.append(index)

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

    def getIndexes(self):
        return self.indexes

    def childXPrivateKey(self, xprivate=None, indexes=None):
        if indexes is None:
            indexes = self.indexes
        if xprivate:
            for index in range(len(indexes)):
                index_bytes = get_bytes(indexes[index])
                xpublic = self.xpublicKey(xprivate)
                xpublic_bytes = get_bytes(xpublic)
                xprivate_bytes = get_bytes(xprivate)
                I = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                        b'N' + xpublic_bytes[:32] + index_bytes,
                                        digestmod=hashlib.sha512).digest())
                Il, Ir = I[:32], I[32:]

                parse_Il = int.from_bytes(Il, 'big')
                if parse_Il == 0:
                    raise ValueError("Bad seed, resulting in invalid key!")

                I = prune_intermediate_scalar(Il)[:32] + Ir

                carry = 0
                total = 0
                for i in range(32):
                    total = xprivate_bytes[i] + I[i] + carry
                    I[i] = total & 0xff
                    carry = total >> 8
                if (total >> 8) != 0:
                    print("sum does not fit in 256-bit int")
                xprivate = I.hex()

            child_xprivate = xprivate
            return child_xprivate
        for index in range(len(indexes)):
            index_bytes = get_bytes(indexes[index])
            xpublic = self.xpublicKey(self.xprivate)
            xpublic_bytes = get_bytes(xpublic)
            xprivate_bytes = get_bytes(self.xprivate)
            I = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                    b'N' + xpublic_bytes[:32] + index_bytes,
                                    digestmod=hashlib.sha512).digest())
            Il, Ir = I[:32], I[32:]

            parse_Il = int.from_bytes(Il, 'big')
            if parse_Il == 0:
                raise ValueError("Bad seed, resulting in invalid key!")

            I = prune_intermediate_scalar(Il)[:32] + Ir

            carry = 0
            total = 0
            for i in range(32):
                total = xprivate_bytes[i] + I[i] + carry
                I[i] = total & 0xff
                carry = total >> 8
            if (total >> 8) != 0:
                print("sum does not fit in 256-bit int")
            xprivate = I.hex()

        child_xprivate = xprivate
        return child_xprivate

    def childXPublicKey(self, xpublic=None, indexes=None):
        if indexes is None:
            indexes = self.indexes
        if xpublic:
            for index in range(len(indexes)):
                index_bytes = get_bytes(indexes[index])
                xpublic_bytes = get_bytes(xpublic)
                I = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                        b'N' + xpublic_bytes[:32] + index_bytes,
                                        digestmod=hashlib.sha512).digest())

                Il, Ir = I[:32], I[32:]

                parse_Il = int.from_bytes(Il, 'big')
                if parse_Il == 0:
                    raise ValueError("Bad seed, resulting in invalid key!")

                f = bytes(prune_intermediate_scalar(Il))
                scalar = decodeint(f)
                F = scalarmultbase(scalar)

                P = decodepoint(xpublic_bytes[:32])
                P = edwards_add(P, F)
                public_key = encodepoint(P)

                xpublic_bytes = public_key[:32] + Ir
                xpublic = xpublic_bytes.hex()

            child_xpublic = xpublic
            return child_xpublic
        for index in range(len(indexes)):
            index_bytes = get_bytes(indexes[index])
            xpublic_bytes = get_bytes(self.xpublicKey())
            I = bytearray(hmac.HMAC(xpublic_bytes[32:],
                                    b'N' + xpublic_bytes[:32] + index_bytes,
                                    digestmod=hashlib.sha512).digest())

            Il, Ir = I[:32], I[32:]

            parse_Il = int.from_bytes(Il, 'big')
            if parse_Il == 0:
                raise ValueError("Bad seed, resulting in invalid key!")

            f = bytes(prune_intermediate_scalar(Il))
            scalar = decodeint(f)
            F = scalarmultbase(scalar)

            P = decodepoint(xpublic_bytes[:32])
            P = edwards_add(P, F)
            public_key = encodepoint(P)

            xpublic_bytes = public_key[:32] + Ir
            xpublic = xpublic_bytes.hex()

        child_xpublic = xpublic
        return child_xpublic

    def controlProgram(self, xpublic=None, indexes=None, path=None):
        if indexes is None:
            if path is not None:
                self.fromPath(path)
                indexes = self.indexes
            else:
                indexes = self.indexes
        if xpublic:
            child_xpublic = self.childXPublicKey(xpublic=xpublic,
                                                 indexes=indexes)
            child_public = self.publicKey(xpublic=child_xpublic)
            child_public_byte = get_bytes(child_public)

            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(child_public_byte)
            public_hash = ripemd160.hexdigest()
            control_program = '0014' + public_hash
            return control_program
        child_xpublic = self.childXPublicKey(xpublic=self.publicKey(),
                                             indexes=indexes)
        child_public = self.publicKey(xpublic=child_xpublic)
        child_public_byte = get_bytes(child_public)

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(child_public_byte)
        public_hash = ripemd160.hexdigest()
        control_program = '0014' + public_hash
        return control_program


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
