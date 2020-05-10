#!/usr/bin/env python3


def get_bytes(string):
    if isinstance(string, bytes):
        byte = string
    elif isinstance(string, str):
        byte = bytes.fromhex(string)
    else:
        raise TypeError("Agreement must be either 'bytes' or 'string'!")
    return byte


def bad_seed_checker(il, ir=False):
    if ir:
        parse_ir = str(il)
        if not parse_ir:
            raise ValueError("Bad seed, resulting in invalid key!")
    else:
        parse_il = int.from_bytes(il, "big")
        if parse_il == 0:
            raise ValueError("Bad seed, resulting in invalid key!")


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
