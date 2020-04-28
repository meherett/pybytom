#!/usr/bin/env python3

from .wallet import Wallet
from .tools import get_xpublic_key, get_expand_xprivate_key, get_child_xprivate_key, indexes_to_path, \
    get_child_xpublic_key, get_address, get_program, get_private_key, get_public_key, get_bytes, path_to_indexes


# Constant values
BIP32KEY_HARDEN = 0x80000000
# Derivation Path
PATH = "m/44/153/1/0/1"
# Derivation Indexes
INDEXES = [
    "2c000000",  # 44
    "99000000",  # 153
    "01000000",  # 1 Account
    "00000000",  # 0 Change
    "01000000"  # 1 Address
]


__all__ = [
    "Wallet",
    "get_xpublic_key",
    "get_expand_xprivate_key",
    "get_child_xprivate_key",
    "get_child_xpublic_key",
    "get_address",
    "get_program",
    "get_private_key",
    "get_public_key",
    "get_bytes",
    "indexes_to_path",
    "path_to_indexes"
]
