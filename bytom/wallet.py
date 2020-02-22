#!/usr/bin/env python3

from bytom.libs.segwit import encode
from .signature import sign, verify
from .utils.utils import *

import hmac

# Constant values
HARDEN = 0x80000000
# Path
PATH = "m/44/153/1/0/1"
# Indexes
INDEXES = [
    "2c000000",  # 44
    "99000000",  # 153
    "01000000",  # 1 Account
    "00000000",  # 0 Change
    "01000000"  # 1 Address
]


class Wallet:

    def __init__(self, network="solonet"):
        self.network = network
        self._entropy = None
        self._seed = None
        self._mnemonic = None
        self.xprivate = None
        self.xpublic = None
        self._indexes = []
        self._path = None

    def from_entropy(self, entropy,
                     passphrase=str(), language="english", strength=128):

        if strength % 32 != 0:
            raise ValueError("strength must be a multiple of 32")
        if strength < 128 or strength > 256:
            raise ValueError("strength should be >= 128 and <= 256")

        self._entropy = entropy
        self._mnemonic = Mnemonic(language=language) \
            .to_mnemonic(self._entropy)
        self._seed = Mnemonic.to_seed(self._mnemonic, passphrase)

        self.from_seed(seed=self._seed)
        return self

    def entropy(self):
        return str(self._entropy)

    def from_mnemonic(self, mnemonic, passphrase=str()):

        self._mnemonic = mnemonic
        self._seed = Mnemonic.to_seed(self._mnemonic, passphrase)
        self.from_seed(seed=self._seed)
        return self

    def mnemonic(self):
        return str(self._mnemonic)

    def from_seed(self, seed):

        i = hmac.HMAC(b"Root", get_bytes(seed), digestmod=hashlib.sha512).hexdigest()
        il, ir = i[:64], i[64:]

        parse_il = str(il)
        if not parse_il:
            raise ValueError("bad seed, resulting in invalid key!")
        # get root xprivate key
        self.xprivate = prune_root_scalar(il).hex() + ir
        self._seed = seed
        return self

    def seed(self):
        return self._seed.hex() if self._seed else None

    def from_xprivate(self, xprivate):
        self.xprivate = xprivate
        return self
    
    def derive_private_key(self, index):
        index = int(index).to_bytes(4, byteorder="little").hex()
        self._indexes.append(index)
        return self
    
    def from_indexes(self, indexes):
        self._indexes = indexes
        return self

    def from_index(self, index):
        if not str(index)[0:2] != "m/":
            raise ValueError("bad Index, use fromPath not fromIndex for this %s" % index)
        if not isinstance(index, int):
            raise ValueError("bad Index, import only integer number!")
        self.derive_private_key(index)
        return self

    def from_path(self, path):
        if str(path)[0:2] != 'm/':
            raise ValueError("bad path, insert like this type of path \"m/0'/0\"! ")

        for index in path.lstrip('m/').split('/'):
            if "'" in index:
                self.derive_private_key(int(index[:-1]) + HARDEN)
            else:
                self.derive_private_key(int(index))
        return self

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
            i = hmac.HMAC(b"Expand", get_bytes(xprivate),
                          digestmod=hashlib.sha512).hexdigest()
            il, ir = i[:64], i[64:]
            parse_ir = str(ir)
            if not parse_ir:
                raise ValueError("bad seed, resulting in invalid key!")
            expand_xprivate = xprivate[:64] + ir
            return expand_xprivate
        i = hmac.HMAC(b"Expand", get_bytes(self.xprivate),
                      digestmod=hashlib.sha512).hexdigest()
        il, ir = i[:64], i[64:]
        parse_ir = str(ir)
        if not parse_ir:
            raise ValueError("bad seed, resulting in invalid key!")
        expand_xprivate = self.xprivate[:64] + ir
        return expand_xprivate
    
    def private_key(self, xprivate=None, indexes=None, path=None):
        if indexes is None and path is None:
            indexes = self._indexes
        elif path is not None:
            self.from_path(path)
            indexes = self._indexes

        if xprivate:
            child_xprivate = self.child_xprivate_key(
                xprivate=xprivate, indexes=indexes)
            child_private = child_xprivate
            return child_private
        else:
            child_xprivate = self.child_xprivate_key(
                xprivate=self.xprivate_key(), indexes=indexes)
            child_private = child_xprivate
            return child_private

    def public_key(self, xpublic=None, indexes=None, path=None):
        if indexes is None and path is None:
            indexes = self._indexes
        elif path is not None:
            self.from_path(path)
            indexes = self._indexes

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

    def indexes(self):
        return self._indexes

    def path(self, indexes=None):
        if indexes:
            path = "m/"
            for i, index in enumerate(indexes, 1):
                number = int.from_bytes(bytes.fromhex(index), byteorder="little")
                if i == len(indexes):
                    path = path + str(number)
                else:
                    path = path + str(number) + "/"
            return path
        path = "m/"
        for i, index in enumerate(self._indexes, 1):
            number = int.from_bytes(bytes.fromhex(index), byteorder="little")
            if i == len(self._indexes):
                path = path + str(number)
            else:
                path = path + str(number) + "/"
        return path

    def child_xprivate_key(self, xprivate=None, indexes=None, path=None):
        if indexes is None and path is None:
            indexes = self._indexes
        elif path is not None:
            self.from_path(path)
            indexes = self._indexes
        if xprivate:
            for index in range(len(indexes)):
                index_bytes = get_bytes(indexes[index])
                xpublic = self.xpublic_key(xprivate)
                xpublic_bytes = get_bytes(xpublic)
                xprivate_bytes = get_bytes(xprivate)
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
                xprivate = i.hex()

            child_xprivate = xprivate
            return child_xprivate
        for index in range(len(indexes)):
            index_bytes = get_bytes(indexes[index])
            xpublic = self.xpublic_key(self.xprivate)
            xpublic_bytes = get_bytes(xpublic)
            xprivate_bytes = get_bytes(self.xprivate)
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
            xprivate = i.hex()

        child_xprivate = xprivate
        return child_xprivate

    def child_xpublic_key(self, xpublic=None, indexes=None, path=None):
        if indexes is None and path is None:
            indexes = self._indexes
        elif path is not None:
            self.from_path(path)
            indexes = self._indexes
        if xpublic:
            for index in range(len(indexes)):
                index_bytes = get_bytes(indexes[index])
                xpublic_bytes = get_bytes(xpublic)
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
                xpublic = xpublic_bytes.hex()

            child_xpublic = xpublic
            return child_xpublic
        for index in range(len(indexes)):
            index_bytes = get_bytes(indexes[index])
            xpublic_bytes = get_bytes(self.xpublic_key())
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
            xpublic = xpublic_bytes.hex()

        child_xpublic = xpublic
        return child_xpublic

    def program(self, xpublic=None, indexes=None, path=None, public=None):
        if public and not xpublic:
            public_byte = get_bytes(public)

            ripemd160 = hashlib.new("ripemd160")
            ripemd160.update(public_byte)
            public_hash = ripemd160.hexdigest()
            control_program = "0014" + public_hash
            return control_program
        if xpublic:
            public = self.public_key(
                xpublic=xpublic, indexes=indexes, path=path)
            public_byte = get_bytes(public)

            ripemd160 = hashlib.new("ripemd160")
            ripemd160.update(public_byte)
            public_hash = ripemd160.hexdigest()
            control_program = "0014" + public_hash
            return control_program
        public = self.public_key(
            xpublic=self.xpublic, indexes=indexes, path=path)
        public_byte = get_bytes(public)

        ripemd160 = hashlib.new("ripemd160")
        ripemd160.update(public_byte)
        public_hash = ripemd160.hexdigest()
        program = "0014" + public_hash
        return program

    def address(self, program=None, network=None):
        if network is None:
            network = self.network
        if network == "mainnet":
            hrp = "bm"
        elif network == "solonet":
            hrp = "sm"
        elif network == "testnet":
            hrp = "tm"
        else:
            raise ValueError("invalid network.")
        if program:
            address_str = encode(hrp, 0, get_bytes(program[4:]))
            return address_str
        self.program()
        address_str = encode(hrp, 0, get_bytes(self.program()[4:]))
        return address_str

    def sign(self, message, private=None):
        if private is None:
            return sign(self.private_key(), message)
        return sign(private, message)

    def verify(self, message, signature, public=None):
        if public is None:
            return verify(self.public_key(), message, signature)
        return verify(public, message, signature)
