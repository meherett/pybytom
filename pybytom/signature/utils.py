#!/usr/bin/env python3

from binascii import hexlify, unhexlify

import ed25519
import hmac

from ..libs.ed25519 import *


L = 2 ** 252 + 27742317777372353535851937790883648493


def prune_root_scalar(s_str):
    s_bytes = bytes.fromhex(s_str)
    s = bytearray(s_bytes)
    s[0] = s[0] & 248
    s[31] = s[31] & 31  # clear top 3 bits
    s[31] = s[31] | 64  # set second highest bit
    return s


def get_root_xprivate(seed_hexstr):
    hc_hexstr = hmac.HMAC(b'Root', bytes.fromhex(seed_hexstr), digestmod=hashlib.sha512).hexdigest()
    root_xprivate_hexstr = prune_root_scalar(hc_hexstr[:64]).hex() + hc_hexstr[64:]
    return root_xprivate_hexstr


def get_xpublic_key(xprivate):
    xprivate_bytes = bytes.fromhex(xprivate)
    scalar = decodeint(xprivate_bytes[:len(xprivate_bytes)//2])
    buf = encodepoint(scalarmultbase(scalar))
    xpublic = buf + xprivate_bytes[len(xprivate_bytes)//2:]
    xpublic = xpublic.hex()
    return xpublic


def get_expanded_private_key(xprivate):
    hc_hexstr = hmac.HMAC(b"Expand", bytes.fromhex(xprivate), digestmod=hashlib.sha512).hexdigest()
    expanded_private_key_hexstr = xprivate[:64] + hc_hexstr[64:]
    return expanded_private_key_hexstr


def get_public_key(xpublic):
    public_key_hexstr = xpublic[:64]
    return public_key_hexstr


def prune_intermediate_scalar(f):
    f = bytearray(f)
    f[0] = f[0] & 248       # clear bottom 3 bits
    f[29] = f[29] & 1       # clear 7 high bits
    f[30] = 0               # clear 8 bits
    f[31] = 0               # clear 8 bits
    return f


def get_bytes(string):
    if isinstance(string, bytes):
        byte = string
    elif isinstance(string, str):
        byte = bytes.fromhex(string)
    else:
        raise TypeError("Agreement must be either 'bytes' or 'string'!")
    return byte


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
