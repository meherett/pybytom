#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from mnemonic.mnemonic import Mnemonic

import ed25519
import random
import hmac

from ..libs.ed25519 import *


L = 2 ** 252 + 27742317777372353535851937790883648493


def generate_entropy():
    return random.randint(0, 2 ** 128 - 1) \
        .to_bytes(16, byteorder='big')


def check_mnemonic(mnemonic, language='english'):
    try:
        Mnemonic(language=language).check(mnemonic)
        return True
    except Exception as exception:
        if exception:
            return False


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


def _sign(private_key_str, message_str):
    signing_key = ed25519.SigningKey(bytes.fromhex(private_key_str))
    signature = signing_key.sign(bytes.fromhex(message_str), encoding='hex')
    return signature.decode()


def _verify(public_key_str, signature_str, message_str):
    result = False
    verifying_key = ed25519.VerifyingKey(public_key_str.encode(), encoding='hex')
    try:
        verifying_key.verify(signature_str.encode(), bytes.fromhex(message_str), encoding='hex')
        result = True
    except ed25519.BadSignatureError:
        result = False
    return result


def byte2int(_b):
    return _b


def int2byte(i):
    return bytes(chr(i % 256), encoding="UTF-8")


def hmac_sha_512(data, key):
    digest = hmac.new(key, msg=data, digestmod=hashlib.sha512).digest()
    return digest


def sha_512(data):
    md = hashlib.sha512()
    md.update(data)
    return md.digest()


def hex2int(_hex):
    unhex = unhexlify(_hex)
    s = 0
    for i in range(len(unhex)):
        s += 256 ** i * byte2int(unhex[i])
    return s


def int2hex(_int):
    return hexlify(encodeint(_int))


def sc_reduce32(inputs):
    _int = hex2int(inputs)
    modulo = _int % L
    return int2hex(modulo)


def sc_muladd(a, _b, c):
    a_int = hex2int(a)
    b_int = hex2int(_b)
    c_int = hex2int(c)

    s = a_int * b_int + c_int
    modulo = s % L
    return int2hex(modulo)
