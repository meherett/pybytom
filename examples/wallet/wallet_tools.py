#!/usr/bin/env python3

from pybytom.wallet.tools import (
    path_to_indexes, indexes_to_path, get_xpublic_key, get_expand_xprivate_key,
    get_child_xprivate_key, get_child_xpublic_key, get_private_key,
    get_public_key, get_program, get_address, get_vapor_address
)


XPRIVATE_KEY = "3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338ff590dedc7ddff447797e1e" \
               "781190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed"

XPUBLIC_KEY = "38a1bfcb82358bc9657c725d5d708c9d0ce115474466520e88fca233be2bc7e3797e1e7" \
              "81190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed"

INDEXES = ['2c000000', '99000000', '01000000', '00000000', '01000000']

PATH = "m/44/153/1/0/1"


print("Get XPublic Key:", get_xpublic_key(xprivate_key=XPRIVATE_KEY))
print("Get Expand XPrivate Key:", get_expand_xprivate_key(xprivate_key=XPRIVATE_KEY))

print("Indexes To Path:", indexes_to_path(indexes=INDEXES))
print("Path To Indexes:", path_to_indexes(path=PATH))

print("Get Child XPrivate Key:", get_child_xprivate_key(xprivate_key=XPRIVATE_KEY))
print("Get Child XPublic Key:", get_child_xpublic_key(xpublic_key=XPUBLIC_KEY))

print("Get Private Key:", get_private_key(xprivate_key=XPRIVATE_KEY))
print("Get Public Key:", get_public_key(xpublic_key=XPUBLIC_KEY))

print("Get Program:", get_program(public_key=get_public_key(xpublic_key=XPUBLIC_KEY)))
print("Get Address:", get_address(program=get_program(
    public_key=get_public_key(xpublic_key=XPUBLIC_KEY)), network="mainnet"))
print("Get Vapor Address:", get_vapor_address(program=get_program(
    public_key=get_public_key(xpublic_key=XPUBLIC_KEY)), network="mainnet"))
