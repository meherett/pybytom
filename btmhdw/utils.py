#!/usr/bin/env python3

from binascii import hexlify, unhexlify

import ed25519
import hmac

from .ed25519 import *


L = 2 ** 252 + 27742317777372353535851937790883648493


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
