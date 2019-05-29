from .ed25519 import *
from .segwit import *
from mnemonic.mnemonic import Mnemonic
from two1.bitcoin.utils import rand_bytes

import hmac

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
                 index=None, xpublic=None):
        self.xprivate = xprivate
        self.seed = seed
        self.index = index
        self.xpublic = xpublic
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
                             index=0, xpublic=None)

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
        self.xpublic = buf + xprivate_bytes[len(xprivate_bytes) // 2:]
        return self.xpublic.hex()

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

    def fromIndexes(self, indexes):
        self.indexes = indexes

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

    def program(self, xpublic=None, indexes=None, path=None):
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
        child_xpublic = self.childXPublicKey(xpublic=self.xpublic,
                                             indexes=indexes)
        child_public = self.publicKey(xpublic=child_xpublic)
        child_public_byte = get_bytes(child_public)

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(child_public_byte)
        public_hash = ripemd160.hexdigest()
        program = '0014' + public_hash
        return program

    def address(self, control_program=None, network='sm'):
        if network == 'mainnet' or network == 'bm':
            hrp = 'bm'
        elif network == 'testnet' or network == 'tm':
            hrp = 'tm'
        elif network == 'solonet' or network == 'sm':
            hrp = 'sm'
        if control_program:
            address_str = encode(hrp, 0, get_bytes(control_program[4:]))
            return address_str
        address_str = encode(hrp, 0, get_bytes(self.program()[4:]))
        return address_str


class BTMHDW:

    def __init__(self):
        self.wallet = dict(
            mnemonic=str(),
            seed=str(),
            xprivate=str(),
            xpublic=str(),
            program=str()
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
    
    def create(self, mnemonic=None, passphrase=str(),
               account=1, change=0, address=1, path=None, indexes=None):
        if mnemonic is None:
            mnemonic = self.generateMnemonic()

        bytomHDWallet = BytomHDWallet.masterKeyFromMnemonic(mnemonic=mnemonic,
                                                            passphrase=passphrase)
        if indexes is not None:
            bytomHDWallet.fromIndexes(indexes=indexes)
        elif path is not None:
            bytomHDWallet.fromPath(path=path)
        else:
            bytomHDWallet.fromIndex(44)
            bytomHDWallet.fromIndex(153)
            bytomHDWallet.fromIndex(account)
            bytomHDWallet.fromIndex(change)
            bytomHDWallet.fromIndex(address)

