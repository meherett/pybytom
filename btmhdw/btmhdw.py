#!/usr/bin/env python3

from mnemonic.mnemonic import Mnemonic

from .segwit import encode
from .key import sign, verify
from .ed25519 import *

import random
import hmac

BTMHDW_HARDEN = 0x80000000
PATH = "m/44/153/1/0/1"
INDEXES = ['2c000000', '99000000', '01000000', '00000000', '01000000']


def get_bytes(string):
    if isinstance(string, bytes):
        byte = string
    elif isinstance(string, str):
        byte = bytes.fromhex(string)
    else:
        raise TypeError("Agreement must be either 'bytes' or 'string'!")
    return byte


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

    def __init__(self, entropy=str(),
                 xprivate=None, seed=None, xpublic=None):
        self.entropy = entropy
        self.xprivate = xprivate
        self.seed = seed
        self.xpublic = xpublic
        self.indexes = []

    @staticmethod
    def master_key_from_mnemonic(mnemonic, passphrase=''):

        seed = Mnemonic.to_seed(mnemonic, passphrase)
        return BytomHDWallet.master_key_from_seed(seed=seed, entropy=str())

    @staticmethod
    def check_mnemonic(mnemonic, language='english'):
        try:
            Mnemonic(language=language).check(mnemonic)
            return True
        except Exception as exception:
            if exception:
                return False

    @staticmethod
    def generate_entropy():
        return random.randint(0, 2 ** 128 - 1) \
            .to_bytes(16, byteorder='big')

    @staticmethod
    def master_key_from_entropy(entropy=None,
                                passphrase=str(), language='english', strength=128):

        if strength % 32 != 0:
            raise ValueError("strength must be a multiple of 32")
        if strength < 128 or strength > 256:
            raise ValueError("strength should be >= 128 and <= 256")

        if not entropy:
            entropy = BytomHDWallet.generate_entropy()
        mnemonic = Mnemonic(language=language) \
            .to_mnemonic(entropy)
        seed = Mnemonic.to_seed(mnemonic, passphrase)

        return BytomHDWallet.master_key_from_seed(seed=seed,
                                                  entropy=entropy), mnemonic

    @staticmethod
    def master_key_from_seed(seed, entropy=str()):

        I = hmac.HMAC(b'Root', get_bytes(seed), digestmod=hashlib.sha512).hexdigest()
        Il, Ir = I[:64], I[64:]

        parse_Il = str(Il)
        if not parse_Il:
            raise ValueError("Bad seed, resulting in invalid key!")
        # get root xprivate key
        xprivate = prune_root_scalar(Il).hex() + Ir

        return BytomHDWallet(entropy=entropy,
                             xprivate=xprivate, seed=seed, xpublic=None)

    @staticmethod
    def master_key_from_xprivate(xprivate):
        return BytomHDWallet(xprivate=xprivate, seed=None, xpublic=None)

    def xprivate_key(self):
        return str(self.xprivate)

    def xpublic_key(self, xprivate=None):
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
        self.xpublic = xpublic.hex()
        return self.xpublic

    def expand_xprivate_key(self, xprivate=None):
        if xprivate:
            I = hmac.HMAC(b'Expand', get_bytes(xprivate), digestmod=hashlib.sha512).hexdigest()
            Il, Ir = I[:64], I[64:]
            parse_Ir = str(Ir)
            if not parse_Ir:
                raise ValueError("Bad seed, resulting in invalid key!")
            expandPrivate = xprivate[:64] + Ir
            return expandPrivate
        I = hmac.HMAC(b'Expand', get_bytes(self.xprivate), digestmod=hashlib.sha512).hexdigest()
        Il, Ir = I[:64], I[64:]
        parse_Ir = str(Ir)
        if not parse_Ir:
            raise ValueError("Bad seed, resulting in invalid key!")
        expandPrivate = self.xprivate[:64] + Ir
        return expandPrivate

    def public_key(self, xpublic=None, indexes=None, path=None):
        if indexes is None and path is None:
            indexes = self.indexes
        elif path is not None:
            self.from_path(path)
            indexes = self.indexes

        if xpublic:
            child_xpublic = self.child_xpublic_key(
                xpublic=xpublic, indexes=indexes)
            child_public = child_xpublic[:64]
            return child_public
        else:
            child_xpublic = self.child_xpublic_key(
                xpublic=self.xpublic_key(), indexes=indexes)
            child_public = child_xpublic[:64]
            return child_public

    def derive_private_key(self, index):
        index = int(index).to_bytes(4, byteorder='little').hex()
        self.indexes.append(index)

        return self

    def from_indexes(self, indexes):
        self.indexes = indexes
        return self

    def from_index(self, index):
        if not str(index)[0:2] != "m/":
            raise ValueError("Bad Index, Please use fromPath not fromIndex for this %s" % index)
        if not isinstance(index, int):
            raise ValueError("Bad Index, Please import only integer number!")
        return self.derive_private_key(index)

    def from_path(self, path):
        if str(path)[0:2] != 'm/':
            raise ValueError("Bad path, please insert like this type of path \"m/0'/0\"! ")

        for index in path.lstrip('m/').split('/'):
            if "'" in index:
                self.derive_private_key(int(index[:-1]) + BTMHDW_HARDEN)
            else:
                self.derive_private_key(int(index))
        return self

    def get_indexes(self):
        return self.indexes

    def get_path(self, indexes=None):
        if indexes:
            path = 'm/'
            for i, index in enumerate(indexes, 1):
                number = int.from_bytes(bytes.fromhex(index), byteorder='little')
                if i == len(indexes):
                    path = path + str(number)
                else:
                    path = path + str(number) + '/'
            return path
        path = 'm/'
        for i, index in enumerate(self.get_indexes(), 1):
            number = int.from_bytes(bytes.fromhex(index), byteorder='little')
            if i == len(self.get_indexes()):
                path = path + str(number)
            else:
                path = path + str(number) + '/'
        return path

    def child_xprivate_key(self, xprivate=None, indexes=None, path=None):
        if indexes is None and path is None:
            indexes = self.indexes
        elif path is not None:
            self.from_path(path)
            indexes = self.indexes
        if xprivate:
            for index in range(len(indexes)):
                index_bytes = get_bytes(indexes[index])
                xpublic = self.xpublic_key(xprivate)
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
            xpublic = self.xpublic_key(self.xprivate)
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

    def child_xpublic_key(self, xpublic=None, indexes=None, path=None):
        if indexes is None and path is None:
            indexes = self.indexes
        elif path is not None:
            self.from_path(path)
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
            xpublic_bytes = get_bytes(self.xpublic_key())
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

    def program(self, xpublic=None, indexes=None, path=None, public=None):
        if public and not xpublic:
            public_byte = get_bytes(public)

            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(public_byte)
            public_hash = ripemd160.hexdigest()
            control_program = '0014' + public_hash
            return control_program
        if xpublic:
            public = self.public_key(
                xpublic=xpublic, indexes=indexes, path=path)
            public_byte = get_bytes(public)

            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(public_byte)
            public_hash = ripemd160.hexdigest()
            control_program = '0014' + public_hash
            return control_program
        public = self.public_key(
            xpublic=self.xpublic, indexes=indexes, path=path)
        public_byte = get_bytes(public)

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(public_byte)
        public_hash = ripemd160.hexdigest()
        program = '0014' + public_hash
        return program

    def address(self, program=None, network='sm'):
        hrp = None
        if network == 'mainnet' or network == 'bm':
            hrp = 'bm'
        elif network == 'testnet' or network == 'tm':
            hrp = 'tm'
        elif network == 'solonet' or network == 'sm':
            hrp = 'sm'
        if program:
            address_str = encode(hrp, 0, get_bytes(program[4:]))
            return address_str
        self.program()
        address_str = encode(hrp, 0, get_bytes(self.program()[4:]))
        return address_str

    def sign(self, message, xprivate=None):
        if xprivate is None:
            return sign(self.xprivate, message)
        return sign(xprivate, message)

    def verify(self, message, signature, xpublic=None):
        if xpublic is None:
            return verify(self.xpublic_key(), message, signature)
        return verify(xpublic, message, signature)


class BTMHDW:

    def __init__(self):
        pass

    @staticmethod
    def generate_mnemonic(passphrase=str(), language='english', strength=128):
        _, mnemonic = BytomHDWallet.master_key_from_entropy(passphrase=passphrase,
                                                            language=language,
                                                            strength=strength)
        return mnemonic

    @staticmethod
    def check_mnemonic(mnemonic, language='english'):
        boolean = BytomHDWallet.check_mnemonic(mnemonic, language)
        return boolean

    @staticmethod
    def generate_entropy():
        return BytomHDWallet.generate_entropy()

    @staticmethod
    def create(mnemonic=None, passphrase=str(), network='sm',
               account=1, change=0, address=1, path=None, indexes=None, entropy=None):
        if mnemonic is None and entropy is None:
            bytomHDWallet, mnemonic = BytomHDWallet \
                .master_key_from_entropy(passphrase=passphrase,
                                         language='english',
                                         strength=128)
        elif mnemonic is None and entropy is not None:
            bytomHDWallet, mnemonic = BytomHDWallet \
                .master_key_from_entropy(passphrase=passphrase,
                                         language='english',
                                         strength=128, entropy=entropy)
        else:
            bytomHDWallet = BytomHDWallet \
                .master_key_from_mnemonic(mnemonic=mnemonic,
                                          passphrase=passphrase)
        if indexes is not None \
                and path is None:
            bytomHDWallet.from_indexes(indexes=indexes)
        elif path is not None \
                and indexes is None:
            bytomHDWallet.from_path(path=path)
        else:
            bytomHDWallet.from_index(44)
            bytomHDWallet.from_index(153)
            bytomHDWallet.from_index(account)
            bytomHDWallet.from_index(change)
            bytomHDWallet.from_index(address)

        if not bytomHDWallet.entropy:
            return dict(
                mnemonic=mnemonic,
                address=bytomHDWallet.address(network=network),
                seed=bytomHDWallet.seed.hex(),
                xprivate=bytomHDWallet.xprivate,
                xpublic=bytomHDWallet.xpublic,
                program=bytomHDWallet.program(),
                path=bytomHDWallet.get_path()
            )

        return dict(
            entropy=bytomHDWallet.entropy.hex(),
            mnemonic=mnemonic,
            address=bytomHDWallet.address(network=network),
            seed=bytomHDWallet.seed.hex(),
            xprivate=bytomHDWallet.xprivate,
            xpublic=bytomHDWallet.xpublic,
            program=bytomHDWallet.program(),
            path=bytomHDWallet.get_path()
        )

    @staticmethod
    def from_xprivate(xprivate, network='sm', account=1,
                      change=0, address=1, path=None, indexes=None):
        bytomHDWallet = BytomHDWallet.master_key_from_xprivate(xprivate=xprivate)

        if indexes is not None \
                and path is None:
            bytomHDWallet.from_indexes(indexes=indexes)
        elif path is not None \
                and indexes is None:
            bytomHDWallet.from_path(path=path)
        else:
            bytomHDWallet.from_index(44)
            bytomHDWallet.from_index(153)
            bytomHDWallet.from_index(account)
            bytomHDWallet.from_index(change)
            bytomHDWallet.from_index(address)

        return dict(
            address=bytomHDWallet.address(network=network),
            xprivate=bytomHDWallet.xprivate,
            xpublic=bytomHDWallet.xpublic,
            program=bytomHDWallet.program(),
            path=bytomHDWallet.get_path()
        )
